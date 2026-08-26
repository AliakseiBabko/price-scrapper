#!/usr/bin/env python3
"""Recover room polygons by growing each room from its own label.

Earlier attempts tried to find rooms from the geometry alone and failed: the
wall footprint has a gap at every opening, so interior space escapes, and some
rooms are joined by 3 m openings that no narrowness test should split anyway.

With the labels extracted from the DWG the problem changes shape. Every room
has a seed point inside it and a known area, so the rooms can be grown from
their seeds all at once, competing for cells. Where two rooms meet at a
doorway the frontier stops halfway, which is where a room boundary belongs.

And because Homestyler also states each room's area, every recovered polygon is
checked against it - a room that disagrees is reported, not quietly shipped.

Usage:
  python tools/cad/build_rooms_from_seeds.py [--res 10] [--tolerance 8]
"""
from __future__ import annotations

import argparse
import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
WALL_PLAN = REPO / "data" / "cad" / "wall_plan.json"
LABELS = REPO / "data" / "cad" / "room_labels.json"


def wall_mask(cycles, w, h, res):
    nx, ny = int(w / res) + 2, int(h / res) + 2
    edges = [(c[i][0], c[i][1], c[i + 1][0], c[i + 1][1])
             for c in cycles for i in range(len(c) - 1)
             if abs(c[i + 1][1] - c[i][1]) > 1e-9]
    mask = np.zeros((ny, nx), dtype=bool)
    for row in range(ny):
        yc = (row + 0.5) * res
        xs = sorted(x0 + (yc - y0) * (x1 - x0) / (y1 - y0)
                    for x0, y0, x1, y1 in edges if (y0 > yc) != (y1 > yc))
        for i in range(0, len(xs) - 1, 2):
            lo, hi = max(0, int(xs[i] / res)), min(nx, int(xs[i + 1] / res) + 1)
            if hi > lo:
                mask[row, lo:hi] = True
    return mask


def box_filter(mask, radius):
    pad = np.pad(mask.astype(np.int32), radius + 1)
    c = pad.cumsum(0).cumsum(1)
    k = 2 * radius + 1
    h, w = mask.shape
    return (c[k:k + h, k:k + w] - c[0:h, k:k + w] - c[k:k + h, 0:w] + c[0:h, 0:w])


def interior_of(walls, openings, res):
    """Free space inside the flat, with the openings sealed.

    Without sealing, growth escapes through the window and loggia gaps and a
    room claims the outside world - which is exactly what the first run did,
    overshooting the labelled total by 15 m2. Sealing also separates rooms at
    their doorways, which is what lets each seed own one room.
    """
    ny, nx = walls.shape

    def plug(mask, subset):
        for o in subset:
            ow = o["width_mm"] if o["horizontal"] else o["depth_mm"]
            oh = o["depth_mm"] if o["horizontal"] else o["width_mm"]
            y0 = max(0, int((o["y_mm"] - 90) / res))
            y1 = min(ny, int((o["y_mm"] + oh + 90) / res) + 1)
            x0 = max(0, int((o["x_mm"] - 90) / res))
            x1 = min(nx, int((o["x_mm"] + ow + 90) / res) + 1)
            mask[y0:y1, x0:x1] = True
        return mask

    # Two different jobs. Sealing everything defines the envelope; sealing only
    # the facade keeps interior doorways open so neighbouring rooms compete for
    # them, which is what stops a doorway being carved out of both rooms.
    facade = [o for o in openings if o.get("layer") == "P-Window"]
    growth_barrier = plug(walls.copy(), facade)
    sealed = walls.copy()
    for o in openings:
        ow = o["width_mm"] if o["horizontal"] else o["depth_mm"]
        oh = o["depth_mm"] if o["horizontal"] else o["width_mm"]
        y0 = max(0, int((o["y_mm"] - 90) / res))
        y1 = min(ny, int((o["y_mm"] + oh + 90) / res) + 1)
        x0 = max(0, int((o["x_mm"] - 90) / res))
        x1 = min(nx, int((o["x_mm"] + ow + 90) / res) + 1)
        sealed[y0:y1, x0:x1] = True
    r = int(200.0 / res / 2)
    closed = box_filter(box_filter(sealed, r) > 0, r) == (2 * r + 1) ** 2
    solid = sealed | closed
    left = np.maximum.accumulate(solid, axis=1)
    right = np.maximum.accumulate(solid[:, ::-1], axis=1)[:, ::-1]
    up = np.maximum.accumulate(solid, axis=0)
    down = np.maximum.accumulate(solid[::-1, :], axis=0)[::-1, :]
    envelope = left & right & up & down
    return envelope & ~growth_barrier


def grow(free, seeds, res):
    """Multi-source breadth-first growth: every cell joins its nearest seed."""
    ny, nx = free.shape
    label = np.zeros((ny, nx), dtype=np.int16)
    q = deque()
    for idx, (sx, sy) in enumerate(seeds, start=1):
        cx, cy = int(sx / res), int(sy / res)
        if not (0 <= cx < nx and 0 <= cy < ny):
            continue
        if not free[cy, cx]:  # a label can sit on a fitting; step to open floor
            found = None
            for r in range(1, 30):
                ys, xs = np.where(free[max(0, cy - r):cy + r + 1, max(0, cx - r):cx + r + 1])
                if ys.size:
                    found = (max(0, cy - r) + ys[0], max(0, cx - r) + xs[0])
                    break
            if not found:
                continue
            cy, cx = found
        label[cy, cx] = idx
        q.append((cy, cx))
    while q:
        y, x = q.popleft()
        cur = label[y, x]
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny_, nx_ = y + dy, x + dx
            if 0 <= ny_ < free.shape[0] and 0 <= nx_ < free.shape[1] \
                    and free[ny_, nx_] and label[ny_, nx_] == 0:
                label[ny_, nx_] = cur
                q.append((ny_, nx_))
    return label


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", type=float, default=10.0, help="mm per cell")
    ap.add_argument("--tolerance", type=float, default=8.0,
                    help="percent an area may differ from the label before it is flagged")
    ap.add_argument("--out", type=Path, default=REPO / "data" / "cad" / "room_polygons.json")
    a = ap.parse_args()

    plan = json.loads(WALL_PLAN.read_text(encoding="utf-8"))
    labels = json.loads(LABELS.read_text(encoding="utf-8"))
    w = plan["envelope_mm"]["width"]
    h = plan["envelope_mm"]["depth"]
    cycles = [[(p[0], p[1]) for p in c] for c in plan["outline_mm"]]

    walls = wall_mask(cycles, w, h, a.res)
    free = interior_of(walls, plan["openings"], a.res)
    seeds = [r["seed_mm"] for r in labels["rooms"]]
    label = grow(free, seeds, a.res)

    cell_m2 = (a.res / 1000.0) ** 2
    rooms, flagged = [], []
    for idx, r in enumerate(labels["rooms"], start=1):
        cells = int((label == idx).sum())
        area = round(cells * cell_m2, 2)
        ys, xs = np.where(label == idx)
        if not ys.size:
            flagged.append({"room": r["name"], "problem": "seed grew nothing"})
            continue
        delta = (area - r["area_m2"]) / r["area_m2"] * 100 if r["area_m2"] else 0
        rec = {
            "name": r["name"],
            "label_area_m2": r["area_m2"],
            "grown_area_m2": area,
            "delta_pct": round(delta, 1),
            "x_mm": round(float(xs.min()) * a.res, 1),
            "y_mm": round(float(ys.min()) * a.res, 1),
            "width_mm": round(float(xs.max() - xs.min() + 1) * a.res, 1),
            "depth_mm": round(float(ys.max() - ys.min() + 1) * a.res, 1),
            "seed_mm": r["seed_mm"],
            "perimeter_m": r["perimeter_m"],
            "trustworthy": abs(delta) <= a.tolerance,
        }
        rooms.append(rec)
        if not rec["trustworthy"]:
            flagged.append({"room": r["name"], "problem": "grown area is %+.1f%% off the label"
                            % delta})

    unassigned = int((free & (label == 0)).sum()) * cell_m2
    result = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "method": "multi-source growth from the DWG's own room labels, %d mm cells" % int(a.res),
        "sources": {"geometry": "data/cad/wall_plan.json", "labels": "data/cad/room_labels.json"},
        "rooms": rooms,
        "label_total_m2": labels["total_area_m2"],
        "grown_total_m2": round(sum(r["grown_area_m2"] for r in rooms), 2),
        "unassigned_free_m2": round(unassigned, 2),
        "flagged": flagged,
        "caveats": [
            "Bounding boxes, not outlines - an L-shaped room's box overstates it.",
            "Where growth escapes through a window gap it claims outside space; that shows up "
            "as a positive delta against the label, which is why every room is checked.",
        ],
    }
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("%-24s %8s %8s %7s" % ("room", "label", "grown", "delta"))
    for r in rooms:
        print("%-24s %8.2f %8.2f %6.1f%%%s"
              % (r["name"], r["label_area_m2"], r["grown_area_m2"], r["delta_pct"],
                 "" if r["trustworthy"] else "   <-- check"))
    print("totals: label %.2f, grown %.2f, unassigned free space %.2f m2"
          % (result["label_total_m2"], result["grown_total_m2"], unassigned))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
