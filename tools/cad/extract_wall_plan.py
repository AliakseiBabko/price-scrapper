#!/usr/bin/env python3
"""Extract the real wall footprint, rooms and openings from the Homestyler DXF.

The apartment model so far was estimated from plan photographs. This DXF is an
actual export with millimetre geometry, so it should be the base instead.

Structure of the export, established by inspection:
  - `P-Wall-Section` holds 8 INSERTs of the same 135-line wall footprint - the
    plan is repeated once per sheet, so any instance gives the same geometry.
  - The 135 lines trace the *faces* of the walls: the outer loop is the flat's
    envelope, and each inner loop is a room.
  - `P-Door-Section`, `P-Opening-Section`, `P-Window` carry the openings.

So rooms are recovered as the holes in the wall region, and each room's real
size comes out of the CAD rather than out of a ruler on a photograph.

Usage:
  python tools/cad/extract_wall_plan.py [--dxf PATH] [--out data/cad/wall_plan.json]
      [--svg data/cad/wall_plan.svg] [--instance N]
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import ezdxf

REPO = Path(__file__).resolve().parents[2]
DEFAULT_DXF = REPO / "data" / "cad" / "dxf" / "20260727-ZK Dubravinskiy.dxf"
TOL = 1.0  # mm - Homestyler emits coordinates with sub-millimetre noise


RES = 10.0  # mm per cell - fine enough to separate rooms, coarse enough to stay fast


def polygon_area(loop: list[tuple[float, float]]) -> float:
    """Signed shoelace area in mm^2."""
    a = 0.0
    for i in range(len(loop) - 1):
        x0, y0 = loop[i]
        x1, y1 = loop[i + 1]
        a += x0 * y1 - x1 * y0
    return a / 2.0


def cycles_from_segments(segments, tol: float = 1.0):
    """Walk the segments into closed cycles.

    Every node in this export has exactly two incident segments, so the soup is
    a clean set of cycles - the outer envelope plus one per enclosed void. An
    earlier version assumed the block stored the lines in path order and simply
    concatenated them; where that assumption broke it inserted a diagonal jump,
    which then flipped the even-odd fill and swallowed a third of the flat.
    Walking the graph removes the assumption.
    """
    from collections import defaultdict

    def key(x, y):
        return (round(x / tol), round(y / tol))

    nodes = {}
    adj = defaultdict(list)
    for i, (x0, y0, x1, y1) in enumerate(segments):
        a, b = key(x0, y0), key(x1, y1)
        if a == b:
            continue
        nodes[a], nodes[b] = (x0, y0), (x1, y1)
        adj[a].append((b, i))
        adj[b].append((a, i))

    used = set()
    cycles = []
    for start in list(adj):
        for _, first in adj[start]:
            if first in used:
                continue
            cycle = [nodes[start]]
            node, edge = start, first
            while edge is not None and edge not in used:
                used.add(edge)
                nxt = next(n for n, e in adj[node] if e == edge)
                cycle.append(nodes[nxt])
                node = nxt
                edge = next((e for _, e in adj[node] if e not in used), None)
            if len(cycle) > 3:
                if cycle[0] != cycle[-1]:
                    cycle.append(cycle[0])
                cycles.append(cycle)
    return cycles


PAD = 40  # cells of guaranteed-free margin, so "outside" is unambiguous


def rasterise(cycles, ox, oy, w, h):
    """Even-odd scanline fill of the wall region. True where there is wall.

    The grid carries a free margin on every side: without it a room whose wall
    happens to sit on the bounding box edge reads as touching the border and
    gets mistaken for the exterior.
    """
    import numpy as np
    nx, ny = int(w / RES) + 2 * PAD, int(h / RES) + 2 * PAD
    grid = np.zeros((ny, nx), dtype=bool)
    edges = []
    for cycle in cycles:
        for i in range(len(cycle) - 1):
            x0, y0 = cycle[i][0] - ox, cycle[i][1] - oy
            x1, y1 = cycle[i + 1][0] - ox, cycle[i + 1][1] - oy
            if abs(y1 - y0) < 1e-9:
                continue  # horizontal edges never cross a scanline centre
            edges.append((x0, y0, x1, y1))
    for row in range(ny):
        yc = (row - PAD + 0.5) * RES
        xs = []
        for x0, y0, x1, y1 in edges:
            if (y0 > yc) != (y1 > yc):
                xs.append(x0 + (yc - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            a = max(0, int(xs[i] / RES) + PAD)
            b = min(nx, int(xs[i + 1] / RES) + 1 + PAD)
            if b > a:
                grid[row, a:b] = True
    return grid


def components(free, ny, nx):
    """Flood-fill the non-wall cells; the one touching the border is outside."""
    import numpy as np
    label = np.zeros((ny, nx), dtype=np.int32)
    current = 0
    out = []
    for sy in range(ny):
        for sx in range(nx):
            if not free[sy, sx] or label[sy, sx]:
                continue
            current += 1
            stack = [(sy, sx)]
            label[sy, sx] = current
            cells = 0
            minx = maxx = sx
            miny = maxy = sy
            touches_border = False
            while stack:
                y, x = stack.pop()
                cells += 1
                if y in (0, ny - 1) or x in (0, nx - 1):
                    touches_border = True
                minx, maxx = min(minx, x), max(maxx, x)
                miny, maxy = min(miny, y), max(maxy, y)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny_, nx_ = y + dy, x + dx
                    if 0 <= ny_ < ny and 0 <= nx_ < nx and free[ny_, nx_] and not label[ny_, nx_]:
                        label[ny_, nx_] = current
                        stack.append((ny_, nx_))
            out.append({"cells": cells, "bbox_cells": (minx, miny, maxx, maxy),
                        "outside": touches_border})
    return out


def snap(value: float, candidates: list[float], tol: float = 60.0) -> float:
    """Pull a rasterised edge back onto the nearest real CAD coordinate."""
    best = min(candidates, key=lambda c: abs(c - value))
    return best if abs(best - value) <= tol else value


def collect_block_lines(doc, insert) -> list[tuple[float, float, float, float]]:
    block = doc.blocks.get(insert.dxf.name)
    ox, oy = insert.dxf.insert.x, insert.dxf.insert.y
    rot = float(insert.dxf.rotation or 0.0)
    if abs(rot) > 0.001:
        raise SystemExit("rotated plan instance is not handled; pick another --instance")
    sx = float(insert.dxf.xscale or 1.0)
    sy = float(insert.dxf.yscale or 1.0)
    out = []
    for e in block:
        if e.dxftype() == "LINE":
            out.append((ox + e.dxf.start.x * sx, oy + e.dxf.start.y * sy,
                        ox + e.dxf.end.x * sx, oy + e.dxf.end.y * sy))
    return out


def near(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def openings_near(doc, msp, layers: list[str], origin, extent) -> list[dict]:
    """Openings whose insertion point falls inside this plan instance."""
    ox, oy = origin
    w, h = extent
    found = []
    for layer in layers:
        for e in msp.query('INSERT[layer=="%s"]' % layer):
            x, y = e.dxf.insert.x, e.dxf.insert.y
            if not (ox - 200 <= x <= ox + w + 200 and oy - 200 <= y <= oy + h + 200):
                continue
            block = doc.blocks.get(e.dxf.name)
            xs, ys = [], []
            for item in block:
                if item.dxftype() == "LINE":
                    xs += [item.dxf.start.x, item.dxf.end.x]
                    ys += [item.dxf.start.y, item.dxf.end.y]
                elif item.dxftype() == "LWPOLYLINE":
                    for p in item.get_points("xy"):
                        xs.append(p[0])
                        ys.append(p[1])
            if not xs:
                continue
            bw, bh = max(xs) - min(xs), max(ys) - min(ys)
            found.append({
                "layer": layer,
                "block": e.dxf.name,
                "x_mm": round(x + min(xs), 1),
                "y_mm": round(y + min(ys), 1),
                "width_mm": round(max(bw, bh), 1),
                "depth_mm": round(min(bw, bh), 1),
                "horizontal": bw >= bh,
                "rotation_deg": float(e.dxf.rotation or 0.0),
            })
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dxf", type=Path, default=DEFAULT_DXF)
    ap.add_argument("--out", type=Path, default=REPO / "data" / "cad" / "wall_plan.json")
    ap.add_argument("--svg", type=Path, default=REPO / "data" / "cad" / "wall_plan.svg")
    ap.add_argument("--instance", type=int, default=None,
                    help="which P-Wall-Section instance to use (default: the one nearest the "
                         "anchor the earlier control-dimension pass selected)")
    ap.add_argument("--min-room-m2", type=float, default=0.6)
    a = ap.parse_args()

    doc = ezdxf.readfile(str(a.dxf))
    msp = doc.modelspace()
    inserts = list(msp.query('INSERT[layer=="P-Wall-Section"]'))
    if not inserts:
        raise SystemExit("no P-Wall-Section inserts in this DXF")

    # All instances are copies of one plan; default to the instance the earlier
    # control-dimension work already scored, so the two agree.
    anchor = (52274.836, 31819.746)
    if a.instance is not None:
        chosen = inserts[a.instance]
    else:
        chosen = min(inserts, key=lambda e: math.dist((e.dxf.insert.x, e.dxf.insert.y), anchor))

    segments = collect_block_lines(doc, chosen)
    cycles = cycles_from_segments(segments)
    if not cycles:
        raise SystemExit("could not close the wall outline into cycles")
    xs = [p[0] for c in cycles for p in c]
    ys = [p[1] for c in cycles for p in c]
    ox0, oy0, ox1, oy1 = min(xs), min(ys), max(xs), max(ys)
    w, h = ox1 - ox0, oy1 - oy0

    grid = rasterise(cycles, ox0, oy0, w, h)
    ny, nx = grid.shape

    # The wall footprint has a gap at every door and opening, so interior space
    # is one connected region that escapes through the entrance. Plug the gaps
    # with the openings the CAD already records, and the rooms separate.
    raw_ops = openings_near(doc, msp, ["P-Door-Section", "P-Opening-Section", "P-Window"],
                            (ox0, oy0), (w, h))
    plug = 80.0  # mm of overlap into the wall on each side
    for o in raw_ops:
        lx = o["x_mm"] - ox0
        ly = o["y_mm"] - oy0
        ow = o["width_mm"] if o["horizontal"] else o["depth_mm"]
        oh = o["depth_mm"] if o["horizontal"] else o["width_mm"]
        cx0 = max(0, int((lx - plug) / RES) + PAD)
        cy0 = max(0, int((ly - plug) / RES) + PAD)
        cx1 = min(nx, int((lx + ow + plug) / RES) + 1 + PAD)
        cy1 = min(ny, int((ly + oh + plug) / RES) + 1 + PAD)
        grid[cy0:cy1, cx0:cx1] = True
    # Rooms are holes reached through zero-width seams in the source polygon.
    # A raster cannot represent a zero-width seam, so without closing them every
    # room leaks into the exterior and reads as one component. Dilating the wall
    # mask by one cell seals the seams; walls here are >= 70 mm, so a 10 mm
    # dilation cannot swallow a real wall.
    sealed = grid.copy()
    sealed[1:, :] |= grid[:-1, :]
    sealed[:-1, :] |= grid[1:, :]
    sealed[:, 1:] |= grid[:, :-1]
    sealed[:, :-1] |= grid[:, 1:]
    comps = components(~sealed, ny, nx)

    # Real CAD coordinates to snap rasterised room edges back onto.
    cand_x = sorted({round(x - ox0, 1) for x in xs})
    cand_y = sorted({round(y - oy0, 1) for y in ys})

    rooms = []
    for c in comps:
        if c["outside"]:
            continue
        # add back the one-cell rim lost to the seal
        cx0_, cy0_, cx1_, cy1_ = c["bbox_cells"]
        rim = 2 * ((cx1_ - cx0_ + 1) + (cy1_ - cy0_ + 1))
        area_m2 = (c["cells"] + rim) * RES * RES / 1e6
        if area_m2 < a.min_room_m2:
            continue
        cx0, cy0, cx1, cy1 = c["bbox_cells"]
        x0 = snap((cx0 - PAD) * RES, cand_x)
        y0 = snap((cy0 - PAD) * RES, cand_y)
        x1 = snap((cx1 + 1 - PAD) * RES, cand_x)
        y1 = snap((cy1 + 1 - PAD) * RES, cand_y)
        filled = c["cells"] * RES * RES / max((x1 - x0) * (y1 - y0), 1e-6)
        rooms.append({
            "index": 0,
            "area_m2": round(area_m2, 2),
            "x_mm": round(x0, 1), "y_mm": round(y0, 1),
            "width_mm": round(x1 - x0, 1), "depth_mm": round(y1 - y0, 1),
            "bbox_area_m2": round((x1 - x0) * (y1 - y0) / 1e6, 2),
            "rectangular": filled > 0.97,
        })
    rooms.sort(key=lambda r: -r["area_m2"])
    for i, r in enumerate(rooms, 1):
        r["index"] = i

    ops = raw_ops
    for o in ops:
        o["x_mm"] = round(o["x_mm"] - ox0, 1)
        o["y_mm"] = round(o["y_mm"] - oy0, 1)

    result = {
        "report_version": "1.0.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_dxf": str(a.dxf.relative_to(REPO)) if a.dxf.is_relative_to(REPO) else str(a.dxf),
        "units": "mm",
        "instance_insert_mm": [round(chosen.dxf.insert.x, 1), round(chosen.dxf.insert.y, 1)],
        "instances_available": len(inserts),
        "envelope_mm": {"width": round(ox1 - ox0, 1), "depth": round(oy1 - oy0, 1)},
        "segments": len(segments),
        "raster_resolution_mm": RES,
        "cycles": len(cycles),
        "outline_mm": [[[round(px - ox0, 1), round(py - oy0, 1)] for px, py in c] for c in cycles],
        "rooms": rooms,
        "openings": ops,
        "geometry_status": "from_cad_export_not_field_verified",
        "caveats": [
            "Homestyler export, not a site survey: it records what was drawn, not what was built.",
            "Room polygons are the holes in the wall footprint, so they are clear internal "
            "dimensions before plaster and finishes.",
            "Rooms are recovered by rasterising at %d mm and flood-filling; edges are snapped "
            "back onto real CAD coordinates, so width/depth are exact where a room is "
            "rectangular, and area_m2 carries roughly a one-cell uncertainty where it is not."
            % int(RES),
            "Openings are taken from block insertion points and block extents; each still needs "
            "checking against the plan before it drives anything.",
        ],
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if a.svg:
        parts = ['<?xml version="1.0" encoding="utf-8"?>',
                 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="900">' % (w, h),
                 '<rect width="%.0f" height="%.0f" fill="#ffffff"/>' % (w, h),
                 '<g transform="translate(0,%.0f) scale(1,-1)">' % h]
        for x0, y0, x1, y1 in segments:
            parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#333" stroke-width="12"/>'
                         % (x0 - ox0, y0 - oy0, x1 - ox0, y1 - oy0))
        for r in rooms:
            parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#dbe9f4" '
                         'fill-opacity="0.55" stroke="#1c6ea4" stroke-width="6"/>'
                         % (r["x_mm"], r["y_mm"], r["width_mm"], r["depth_mm"]))
        for o in ops:
            parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#c23b3b" '
                         'fill-opacity="0.5"/>' % (o["x_mm"], o["y_mm"],
                                                   max(o["width_mm"], 60), max(o["depth_mm"], 60)))
        parts.append("</g>")
        for r in rooms:
            parts.append('<text x="%.1f" y="%.1f" font-size="150" text-anchor="middle" fill="#123">'
                         '%d: %.2f m²</text>'
                         % (r["x_mm"] + r["width_mm"] / 2, h - (r["y_mm"] + r["depth_mm"] / 2),
                            r["index"], r["area_m2"]))
        parts.append("</svg>")
        a.svg.write_text("\n".join(parts), encoding="utf-8")

    print(json.dumps({"envelope_mm": result["envelope_mm"],
                      "rooms": len(rooms), "openings": len(ops),
                      "out": str(a.out), "svg": str(a.svg)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
