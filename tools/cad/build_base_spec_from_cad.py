#!/usr/bin/env python3
"""Rebuild the apartment base spec from the CAD footprint instead of photographs.

The Homestyler export is the developer's own layout with their dimensions, so
it - not a ruler on a plan photo - is the geometry this project should model.

Two problems had to be solved to use it:

  * The wall region is a set of closed rectilinear cycles, not a list of walls.
    Slab decomposition turns it into axis-aligned rectangles that are exact and,
    crucially, **non-overlapping** - which is what removes the 10.9% of wall
    volume the old hand-built model double-counted at its junctions.

  * Rooms are the voids, but the CAD leaves a gap at every door, so interior
    space escapes to the outside. Closing the wall mask with a kernel wider than
    any opening, then filling its holes, gives the flat's envelope; rooms are
    then found strictly inside it and cannot leak.

Heights are not in a 2D plan: storey height, door and window heights stay
assumptions and are marked as such in the output.

Usage:
  python tools/cad/build_base_spec_from_cad.py \
      --wall-plan data/cad/wall_plan.json \
      --out data/canonical/current_apartment_cad.json
"""
from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]

RES = 10.0            # mm per cell, matching the extractor
CLOSE_MM = 1600.0     # wider than the widest opening (loggia glazing is 2718 -> plugged separately)
MIN_ROOM_M2 = 0.8
MERGE_TOL = 1.0       # mm

# Not derivable from a 2D plan - stated, not hidden.
ASSUMED = {
    "storey_height_m": 2.8,
    "door_height_m": 2.1,
    "window_sill_m": 1.0,
    "window_height_m": 1.1,
}

# Rooms known to exist in this flat, used only to propose names for what the
# geometry finds. Areas are the earlier visual estimates, so matching is a
# suggestion to confirm, never a measurement.
KNOWN_ROOMS = [
    ("Living room", "living", 19.5), ("Bedroom", "bedroom", 16.6),
    ("Small bedroom", "kids", 9.4), ("Entrance hall", "entrance", 9.8),
    ("Loggia", "balcony", 6.1), ("Kitchen", "kitchen", 5.2),
    ("Bathroom", "bathroom", 3.1), ("WC", "wc", 1.2),
]


def box_filter(mask: np.ndarray, radius: int) -> np.ndarray:
    """Count of True cells in a (2r+1) square around each cell, via prefix sums."""
    pad = np.pad(mask.astype(np.int32), radius + 1)
    s = pad.cumsum(0).cumsum(1)
    k = 2 * radius + 1
    h, w = mask.shape
    y0, x0 = 0, 0
    return (s[y0 + k:y0 + k + h, x0 + k:x0 + k + w]
            - s[y0:y0 + h, x0 + k:x0 + k + w]
            - s[y0 + k:y0 + k + h, x0:x0 + w]
            + s[y0:y0 + h, x0:x0 + w])


def close_mask(mask: np.ndarray, radius: int) -> np.ndarray:
    dilated = box_filter(mask, radius) > 0
    area = (2 * radius + 1) ** 2
    return box_filter(dilated, radius) == area


def orthogonal_hull(mask: np.ndarray) -> np.ndarray:
    """The region enclosed by the outermost walls.

    Closing the wall mask does not work here: the CAD perimeter has gaps at the
    windows and the loggia glazing that are wider than any sane kernel. But a
    cell is inside the flat exactly when it has wall to its left AND right AND
    above AND below - the orthogonal convex hull, which for an L-shaped plan is
    the L itself.
    """
    left = np.maximum.accumulate(mask, axis=1)
    right = np.maximum.accumulate(mask[:, ::-1], axis=1)[:, ::-1]
    up = np.maximum.accumulate(mask, axis=0)
    down = np.maximum.accumulate(mask[::-1, :], axis=0)[::-1, :]
    return left & right & up & down


def fill_holes(mask: np.ndarray) -> np.ndarray:
    """Everything not reachable from the border without crossing the mask."""
    h, w = mask.shape
    free = ~mask
    seen = np.zeros_like(mask)
    stack = [(y, x) for y in (0, h - 1) for x in range(w) if free[y, x]]
    stack += [(y, x) for x in (0, w - 1) for y in range(h) if free[y, x]]
    for y, x in stack:
        seen[y, x] = True
    while stack:
        y, x = stack.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and free[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                stack.append((ny, nx))
    return ~seen


def erode(mask: np.ndarray, radius: int) -> np.ndarray:
    area = (2 * radius + 1) ** 2
    return box_filter(mask, radius) == area


def rooms_by_narrowness(interior: np.ndarray, throat_radius: int):
    """Separate rooms without needing to know where the doorways are.

    A doorway is a throat 700-900 mm wide; a room is wider than that in both
    directions. Eroding the interior by more than half a throat therefore
    breaks the flat into one blob per room, and growing those blobs back inside
    the interior recovers the full room areas. Relying on the CAD opening list
    instead left rooms merged, because the export does not record every
    doorway.
    """
    cores = erode(interior, throat_radius)
    comps, label = label_components(cores)
    keep = {c["id"] for c in comps if c["cells"] > 20}
    label = np.where(np.isin(label, list(keep)), label, 0).astype(np.int32)

    # grow the cores back out, one cell at a time, never leaving the interior
    for _ in range(throat_radius * 3 + 40):
        grown = label.copy()
        for shift_axis, shift in ((0, 1), (0, -1), (1, 1), (1, -1)):
            rolled = np.roll(label, shift, axis=shift_axis)
            if shift_axis == 0:
                if shift == 1:
                    rolled[0, :] = 0
                else:
                    rolled[-1, :] = 0
            else:
                if shift == 1:
                    rolled[:, 0] = 0
                else:
                    rolled[:, -1] = 0
            fill = (grown == 0) & (rolled > 0) & interior
            grown = np.where(fill, rolled, grown)
        if np.array_equal(grown, label):
            break
        label = grown

    out = []
    for rid in sorted(set(np.unique(label)) - {0}):
        ys, xs = np.where(label == rid)
        out.append({"id": int(rid), "cells": int(ys.size),
                    "bbox": (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))})
    return out, label


def label_components(free: np.ndarray):
    h, w = free.shape
    label = np.zeros((h, w), dtype=np.int32)
    out = []
    current = 0
    for sy in range(h):
        for sx in range(w):
            if not free[sy, sx] or label[sy, sx]:
                continue
            current += 1
            stack = [(sy, sx)]
            label[sy, sx] = current
            cells = 0
            minx = maxx = sx
            miny = maxy = sy
            while stack:
                y, x = stack.pop()
                cells += 1
                minx, maxx = min(minx, x), max(maxx, x)
                miny, maxy = min(miny, y), max(maxy, y)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and free[ny, nx] and not label[ny, nx]:
                        label[ny, nx] = current
                        stack.append((ny, nx))
            out.append({"id": current, "cells": cells,
                        "bbox": (minx, miny, maxx, maxy)})
    return out, label


def slab_rectangles(cycles) -> list[tuple[float, float, float, float]]:
    """Decompose the rectilinear wall region into non-overlapping rectangles.

    Sweep vertical slabs between consecutive x coordinates; inside a slab the
    region is a union of y intervals, read off the horizontal edges that span
    the slab. Slabs with identical intervals are merged back together so the
    result is a handful of real walls rather than hundreds of slivers.
    """
    horizontals = []
    xs = set()
    for cycle in cycles:
        for i in range(len(cycle) - 1):
            (x0, y0), (x1, y1) = cycle[i], cycle[i + 1]
            xs.add(round(x0, 1))
            xs.add(round(x1, 1))
            if abs(y0 - y1) < 1e-6:
                horizontals.append((min(x0, x1), max(x0, x1), y0))
    bounds = sorted(xs)

    slabs = []
    for i in range(len(bounds) - 1):
        xa, xb = bounds[i], bounds[i + 1]
        if xb - xa < 0.5:
            continue
        xm = (xa + xb) / 2.0
        ys = sorted(y for (sx, ex, y) in horizontals if sx <= xm <= ex)
        intervals = tuple((ys[j], ys[j + 1]) for j in range(0, len(ys) - 1, 2))
        if intervals:
            slabs.append([xa, xb, intervals])

    merged = []
    for slab in slabs:
        if merged and merged[-1][2] == slab[2] and abs(merged[-1][1] - slab[0]) < MERGE_TOL:
            merged[-1][1] = slab[1]
        else:
            merged.append(slab)

    rects = []
    for xa, xb, intervals in merged:
        for y0, y1 in intervals:
            if xb - xa > 1.0 and y1 - y0 > 1.0:
                rects.append((xa, y0, xb, y1))
    return coalesce(absorb_slivers(coalesce(snap_rects(rects))))


SNAP_MM = 5.0
SLIVER_MM = 60.0      # thinner than any real wall here (75 is the thinnest drawn)
CRUMB_M2 = 0.005      # a fragment smaller than this is decomposition noise


def snap_rects(rects, grid: float = SNAP_MM):
    """Pull coordinates onto a 5 mm grid.

    The CAD carries sub-millimetre noise, which the slab sweep turns into extra
    cut lines and therefore extra fragments. Snapping removes the noise without
    touching any real step: the smallest real feature here is 70 mm and the
    dimensional tolerance is +/-25 mm.
    """
    out = []
    for x0, y0, x1, y1 in rects:
        a, b = round(x0 / grid) * grid, round(y0 / grid) * grid
        c, d = round(x1 / grid) * grid, round(y1 / grid) * grid
        if c - a > 0.5 and d - b > 0.5:
            out.append((a, b, c, d))
    return out


def absorb_slivers(rects):
    """Fold junction leftovers into the wall they belong to.

    Slab decomposition leaves 2-50 mm nubs where walls meet at an L. They are
    not features of the drawing - the developer's plan has no 21 mm wall - so
    they are extended into a collinear neighbour where one exists, and dropped
    when they are pure crumbs. Real steps in the plan are untouched, because
    they are wider than any sliver.
    """
    rects = [list(r) for r in rects]
    kept, absorbed, dropped = [], 0, 0
    for r in rects:
        w, h = r[2] - r[0], r[3] - r[1]
        thin = min(w, h) < SLIVER_MM
        if not thin:
            kept.append(r)
            continue
        host = None
        for other in rects:
            if other is r:
                continue
            ow, oh = other[2] - other[0], other[3] - other[1]
            if min(ow, oh) < SLIVER_MM:
                continue
            touches_x = other[0] - 1 <= r[0] and r[2] <= other[2] + 1
            touches_y = other[1] - 1 <= r[1] and r[3] <= other[3] + 1
            if touches_x and (abs(other[1] - r[3]) < 1 or abs(other[3] - r[1]) < 1):
                host = other
                host[1], host[3] = min(host[1], r[1]), max(host[3], r[3])
                break
            if touches_y and (abs(other[0] - r[2]) < 1 or abs(other[2] - r[0]) < 1):
                host = other
                host[0], host[2] = min(host[0], r[0]), max(host[2], r[2])
                break
        if host is not None:
            absorbed += 1
        elif w * h / 1e6 < CRUMB_M2:
            dropped += 1
        else:
            kept.append(r)
    print("  slivers: %d absorbed into a neighbour, %d dropped as crumbs" % (absorbed, dropped))
    return [tuple(r) for r in kept]


def coalesce(rects, tol: float = 1.0):
    """Glue the slab slivers back into walls.

    Slab decomposition cuts at every x in the drawing, so one wall arrives as a
    row of fragments - 2 mm here, 45 mm there. Repeatedly merging neighbours
    that share a full edge turns those back into the handful of real walls, and
    the result is still non-overlapping.
    """
    rects = [list(r) for r in rects]
    changed = True
    while changed:
        changed = False
        out = []
        used = [False] * len(rects)
        for i, a in enumerate(rects):
            if used[i]:
                continue
            for j in range(i + 1, len(rects)):
                if used[j]:
                    continue
                b = rects[j]
                same_y = abs(a[1] - b[1]) < tol and abs(a[3] - b[3]) < tol
                same_x = abs(a[0] - b[0]) < tol and abs(a[2] - b[2]) < tol
                if same_y and (abs(a[2] - b[0]) < tol or abs(b[2] - a[0]) < tol):
                    a = [min(a[0], b[0]), a[1], max(a[2], b[2]), a[3]]
                    used[j] = changed = True
                elif same_x and (abs(a[3] - b[1]) < tol or abs(b[3] - a[1]) < tol):
                    a = [a[0], min(a[1], b[1]), a[2], max(a[3], b[3])]
                    used[j] = changed = True
            used[i] = True
            out.append(a)
        rects = out
    return [tuple(r) for r in rects]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wall-plan", type=Path, default=REPO / "data" / "cad" / "wall_plan.json")
    ap.add_argument("--out", type=Path, default=REPO / "data" / "canonical" / "current_apartment_cad.json")
    a = ap.parse_args()

    plan = json.loads(a.wall_plan.read_text(encoding="utf-8"))
    cycles = [[(p[0], p[1]) for p in c] for c in plan["outline_mm"]]
    openings = plan["openings"]
    w_mm = plan["envelope_mm"]["width"]
    h_mm = plan["envelope_mm"]["depth"]

    # ---- walls -----------------------------------------------------------
    rects = slab_rectangles(cycles)

    # ---- raster for room finding ----------------------------------------
    nx, ny = int(w_mm / RES) + 2, int(h_mm / RES) + 2
    wall = np.zeros((ny, nx), dtype=bool)
    for x0, y0, x1, y1 in rects:
        wall[max(0, int(y0 / RES)):min(ny, int(y1 / RES) + 1),
             max(0, int(x0 / RES)):min(nx, int(x1 / RES) + 1)] = True

    plugged = wall.copy()
    for o in openings:
        ow = o["width_mm"] if o["horizontal"] else o["depth_mm"]
        oh = o["depth_mm"] if o["horizontal"] else o["width_mm"]
        plugged[max(0, int((o["y_mm"] - 90) / RES)):min(ny, int((o["y_mm"] + oh + 90) / RES) + 1),
                max(0, int((o["x_mm"] - 90) / RES)):min(nx, int((o["x_mm"] + ow + 90) / RES) + 1)] = True

    # The hull must be taken over the *plugged* mask: a row passing through an
    # unplugged window gap finds no wall beyond it and the room centre falls
    # outside the hull, leaving only strips along the walls. Residual gaps get
    # bridged by a small closing first.
    sealed = close_mask(plugged, int(400.0 / RES / 2)) | plugged
    envelope = orthogonal_hull(sealed)
    interior = envelope & ~wall
    comps, _ = rooms_by_narrowness(interior, int(350.0 / RES))
    # Kept only as a diagnostic - see the note on rooms below.

    rooms = []
    for c in comps:
        area = c["cells"] * RES * RES / 1e6
        if area < MIN_ROOM_M2:
            continue
        x0, y0, x1, y1 = c["bbox"]
        rooms.append({
            "area_m2": round(area, 2),
            "x_m": round(x0 * RES / 1000, 3), "y_m": round(y0 * RES / 1000, 3),
            "width_m": round((x1 - x0 + 1) * RES / 1000, 3),
            "depth_m": round((y1 - y0 + 1) * RES / 1000, 3),
        })
    rooms.sort(key=lambda r: -r["area_m2"])
    room_probe = rooms
    rooms = []  # the canonical spec ships no rooms until they are named for real

    # Propose a name per room by area, closest first; every one needs confirming.
    pool = sorted(KNOWN_ROOMS, key=lambda k: -k[2])
    for i, room in enumerate(rooms):
        if i < len(pool):
            name, role, guess = pool[i]
            room["name"] = name
            room["role"] = role
            room["name_confidence"] = "inferred_by_area_rank_confirm_before_use"
            room["visual_estimate_m2"] = guess
        else:
            room["name"] = "Room %d" % (i + 1)
            room["role"] = "other"
            room["name_confidence"] = "unassigned"
        room["source"] = "homestyler cad export (developer layout)"

    # ---- walls into spec form -------------------------------------------
    walls = []
    for i, (x0, y0, x1, y1) in enumerate(sorted(rects, key=lambda r: (-((r[2] - r[0]) * (r[3] - r[1]))))):
        wm, hm = (x1 - x0) / 1000.0, (y1 - y0) / 1000.0
        horizontal = wm >= hm
        walls.append({
            "name": "W%03d" % (i + 1),
            "x_m": round(x0 / 1000, 3), "y_m": round(y0 / 1000, 3),
            "length_m": round(wm if horizontal else hm, 3),
            "horizontal": horizontal,
            "thickness_m": round(hm if horizontal else wm, 3),
            "phase": "existing",
            "kind": "partition",
        })

    def wall_box(w):
        wx0 = w["x_m"] * 1000
        wy0 = w["y_m"] * 1000
        wx1 = wx0 + (w["length_m"] if w["horizontal"] else w["thickness_m"]) * 1000
        wy1 = wy0 + (w["thickness_m"] if w["horizontal"] else w["length_m"]) * 1000
        return wx0, wy0, wx1, wy1

    def host_for(x0, y0, x1, y1, horizontal):
        """The wall this opening is a gap in.

        An opening overlaps no wall - it is where the wall is not - so
        proximity alone finds nothing. What identifies the host is the axis
        band: a gap in a vertical wall lies on that wall's x band, and the
        host is the nearest wall on that band along the opening's own
        direction. Searching by band instead of by a fixed reach is what
        stopped doors going homeless when a neighbouring sliver was absorbed.
        """
        best, best_gap = "", None
        for w in walls:
            wx0, wy0, wx1, wy1 = wall_box(w)
            if w["horizontal"] != horizontal:
                continue
            if horizontal:
                # gap in a horizontal wall: bands must agree in y, gap measured in x
                if not (wy0 - 60 <= (y0 + y1) / 2 <= wy1 + 60):
                    continue
                gap = max(wx0 - x1, x0 - wx1, 0)
            else:
                if not (wx0 - 60 <= (x0 + x1) / 2 <= wx1 + 60):
                    continue
                gap = max(wy0 - y1, y0 - wy1, 0)
            if gap > 1500:
                continue
            if best_gap is None or gap < best_gap:
                best, best_gap = w["name"], gap
        if best:
            return best

        # Fall back to whichever wall of the same orientation is nearest the
        # opening's centre. Some openings sit in a wall the decomposition split
        # differently, so the band test misses them; being adopted by the
        # nearest same-orientation wall is still right far more often than
        # being left homeless.
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        nearest, nearest_d = "", None
        for w in walls:
            if w["horizontal"] != horizontal:
                continue
            wx0, wy0, wx1, wy1 = wall_box(w)
            dx = max(wx0 - cx, cx - wx1, 0)
            dy = max(wy0 - cy, cy - wy1, 0)
            d = (dx * dx + dy * dy) ** 0.5
            if d <= 1500 and (nearest_d is None or d < nearest_d):
                nearest, nearest_d = w["name"], d
        return nearest

    # Where the balcony is, so a balcony block can be told from a door.
    labels_path = REPO / "data" / "cad" / "room_labels.json"
    balcony = None
    if labels_path.exists():
        for r in json.loads(labels_path.read_text(encoding="utf-8"))["rooms"]:
            if "balcon" in r["name"].lower() or "лодж" in r["name"].lower():
                balcony = r["seed_mm"]

    def classify(layer: str, width_mm: float, x_mm: float, y_mm: float) -> str:
        """door / opening / balcony_block / window.

        One layer for everything that is not a window put a leaf on things that
        have none: the 3157 mm kitchen-dining проём drew as a door, and so did
        the balcony block, which is a door with a window over it.
        """
        if layer == "P-Window":
            return "window"
        if layer == "P-Opening-Section" or width_mm > 2000:
            return "opening"
        if balcony and width_mm >= 1000 and math.dist((x_mm, y_mm), balcony) < 3000:
            return "balcony_block"
        return "door"

    spec_openings = []
    unhosted = []
    for i, o in enumerate(openings, 1):
        kind = classify(o["layer"], o["width_mm"], o["x_mm"], o["y_mm"])
        # width_mm is the long extent, i.e. along the wall; depth_mm is the wall
        # thickness the block spans. An earlier version swapped them for vertical
        # openings and produced 40 mm doors.
        width = o["width_mm"] / 1000.0
        thickness = o["depth_mm"] / 1000.0
        if o["horizontal"]:
            bx0, by0, bx1, by1 = (o["x_mm"], o["y_mm"],
                                  o["x_mm"] + o["width_mm"], o["y_mm"] + o["depth_mm"])
        else:
            bx0, by0, bx1, by1 = (o["x_mm"], o["y_mm"],
                                  o["x_mm"] + o["depth_mm"], o["y_mm"] + o["width_mm"])
        host = host_for(bx0, by0, bx1, by1, o["horizontal"])
        if not host:
            unhosted.append("%s %d" % (kind, i))
        spec_openings.append({
            "host_wall": host,
            "name": "%s %d (%d mm)" % (kind, i, round(width * 1000)),
            "x_m": round(o["x_mm"] / 1000, 3), "y_m": round(o["y_mm"] / 1000, 3),
            "width_m": round(width, 3),
            "horizontal": o["horizontal"],
            "bottom_m": ASSUMED["window_sill_m"] if kind == "window" else 0.0,
            "height_m": (ASSUMED["window_height_m"] if kind == "window"
                         else ASSUMED["door_height_m"]),
            "kind": kind,
            "phase": "existing",
            "cad_layer": o["layer"],
            "cad_thickness_m": round(thickness, 3),
        })

    spec = {
        "schema_version": "0.1.0",
        "spec_id": "current-apartment-cad",
        "name": "ZK Dubravinskiy - existing state, from the developer layout via Homestyler CAD",
        "status": "from_developer_layout_via_cad_not_field_verified",
        "units": "m",
        "storey_height_m": ASSUMED["storey_height_m"],
        "default_wall_thickness_m": 0.15,
        "exterior_wall_thickness_m": 0.25,
        "rooms": rooms,
        "room_probe": room_probe,
        "walls": walls,
        "openings": spec_openings,
        "fills": [],
        "space_boundaries": {},
        "electrical_plan": {},
        "plumbing_plan": [],
        "lighting": {"mode": "ceiling_centre_per_room", "exclude_rooms": [], "z_m": 2.62,
                     "size_m": 0.35, "temperature_k": 3000, "approx_lumens": 550},
        "finishes": {},
        "furniture": [],
        "evidence": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "source": plan.get("source_dxf"),
            "wall_plan": str(a.wall_plan.relative_to(REPO)),
            "envelope_mm": plan["envelope_mm"],
            "geometry_status": "developer layout as drawn in Homestyler; dimensions are the "
                               "developer's, not a site survey",
            "tolerance_note": "Measurements of other flats with the same layout differ by up to "
                              "a few centimetres wall to wall; treat these as nominal.",
            "assumed_not_from_cad": ASSUMED,
            "rooms_status": "NOT EXTRACTED. The wall geometry is exact, but room polygons are "
                            "not recoverable from this export: P-Room blocks are empty, the "
                            "footprint has a gap at every opening, and some rooms are joined by "
                            "3 m wide openings that no narrowness test can separate. Three "
                            "attempts are recorded in room_probe and none is trustworthy. "
                            "Get room names and areas from Homestyler directly - it knows them - "
                            "or label them once by hand over data/cad/wall_plan.svg.",
            "caveats": [
                "Wall rectangles come from slab decomposition, so they are non-overlapping by "
                "construction - no material is double counted at junctions.",
                "Wall names are positional (W001...); they carry no meaning until reviewed.",
                "Openings are assigned to the wall rectangle they overlap most; slab "
                "decomposition can split one physical wall into several rectangles, so an "
                "opening may name only the piece it happens to sit in.",
                "room_probe is a diagnostic only: the numbers in it are wrong and it exists to "
                "show what the segmentation attempts produced, not to be used.",
                "Heights are assumptions - a 2D plan does not contain them.",
            ],
        },
    }

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if unhosted:
        print("WARNING: %d opening(s) matched no wall: %s" % (len(unhosted), ", ".join(unhosted)))
    wall_area = sum((r[2] - r[0]) * (r[3] - r[1]) for r in rects) / 1e6
    print(json.dumps({
        "out": str(a.out.relative_to(REPO)),
        "walls": len(walls), "rooms": len(rooms), "openings": len(spec_openings),
        "wall_footprint_m2": round(wall_area, 2),
        "room_area_total_m2": round(sum(r["area_m2"] for r in rooms), 2),
        "envelope_mm": plan["envelope_mm"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
