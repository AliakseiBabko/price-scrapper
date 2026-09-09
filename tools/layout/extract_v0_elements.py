#!/usr/bin/env python3
"""Read the v0 elements the wall model does not carry: glazing, frames, dashed furniture.

The named wall model (wall_blocks.csv + place_named_walls.py) covers the flat's
walls. Three things on the developer's drawing are not walls and are not in it:

  loggia-glazing   the лоджия's diagonal glazed enclosure, WITH its bay
                   subdivision -- "one block but in four segments" (owner,
                   2026-09-08). The vault's O9 had the four-bay pattern only
                   from a PHOTO OF ANOTHER FLAT (109), and recorded that the
                   pattern transfers but the bay count and widths do not. This
                   reads count and widths off OUR OWN type's drawing.

  slab-extension   a closed rectangle projecting OUTWARD from the façade at the
                   19,49 room's window. Owner, 2026-09-08: an extension of the
                   floor concrete slab, decorative. It is not a wall and must
                   not be counted as one.

  dashed-furniture the developer's SUGGESTED furniture. !! Two traps here:
                   (a) the drawing has NO PDF dash operator at all -- the dashes
                   are exploded into short segments, so a dashed line is not
                   distinguishable by graphics state and has to be found by its
                   gap rhythm; (b) suggested furniture is NOT built fabric and
                   must never reach a quantity.

!! NOT IMPLEMENTED YET: the frame subdivision inside the FACADE window openings
   (MA / MB / MC), wanted for the 3D model. The geometry is present -- the 19,49
   window shows jamb frames and a central mullion pair as short verticals across
   the reveal -- but it is not extracted here. The лоджия glazing below is.

!! Nothing here is named or classified beyond what the owner has said. Which
   dashed run is "the wardrobe" is left to him -- see the ПР/правая mistake in
   00_Master/Vector_Plan_Identity_Test.md for why guessing an abbreviation or a
   role off a drawing is a bad trade.
"""
import argparse
import importlib.util
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join("_Inbox", "_Visual_Drop", "3Б_3+ МН5_287.pdf")

DASH_MIN_MM, DASH_MAX_MM = 15.0, 200.0
DASH_MIN_SEGMENTS = 4


def _extractor():
    spec = importlib.util.spec_from_file_location(
        "ex", os.path.join(HERE, "extract_v0_walls.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def loggia_glazing(segments, mm):
    """The diagonal glazed enclosure, projected onto its own axis."""
    diag = []
    for x0, y0, x1, y1 in segments:
        X0, Y0, X1, Y1 = x0 * mm, y0 * mm, x1 * mm, y1 * mm
        L = math.hypot(X1 - X0, Y1 - Y0)
        if L <= 1500:
            continue
        a = math.degrees(math.atan2(Y1 - Y0, X1 - X0)) % 180
        # genuinely oblique only: a line at 89.99 deg is a vertical wall face
        # with rounding on it, not the лоджия's splayed glazing
        if not (5.0 < a < 85.0 or 95.0 < a < 175.0):
            continue
        diag.append((L, X0, Y0, X1, Y1))
    if not diag:
        return None
    diag.sort(key=lambda t: -t[0])
    # the OUTER line is longest; the glazing proper is the longest line that is
    # not it but shares its bearing -- the inner face of the same assembly
    bearing = math.degrees(math.atan2(diag[0][4] - diag[0][2],
                                      diag[0][3] - diag[0][1])) % 180
    same = [d for d in diag
            if abs((math.degrees(math.atan2(d[4] - d[2], d[3] - d[1])) % 180)
                   - bearing) < 1.0]
    axis = same[1] if len(same) > 1 else same[0]
    L, ax, ay, bx, by = axis
    ux, uy = (bx - ax) / L, (by - ay) / L

    def proj(px, py):
        return ((px - ax) * ux + (py - ay) * uy, -(px - ax) * uy + (py - ay) * ux)

    # glass bays: long runs lying inside the frame band
    bays = []
    for x0, y0, x1, y1 in segments:
        X0, Y0, X1, Y1 = x0 * mm, y0 * mm, x1 * mm, y1 * mm
        seg_len = math.hypot(X1 - X0, Y1 - Y0)
        if not 300 < seg_len < 1200:
            continue
        a = math.degrees(math.atan2(Y1 - Y0, X1 - X0)) % 180
        if abs(a - bearing) > 1.0:
            continue
        p0, q0 = proj(X0, Y0)
        p1, q1 = proj(X1, Y1)
        q = (q0 + q1) / 2
        if not 0 < q < 200:
            continue
        bays.append((round(min(p0, p1), 1), round(max(p0, p1), 1)))
    merged = []
    for a0, b0 in sorted(set(bays)):
        if merged and a0 <= merged[-1][1] + 6 and abs(a0 - merged[-1][0]) < 12:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b0))
        elif not merged or a0 > merged[-1][1] - 6:
            merged.append((a0, b0))
    mullions = [{"from_mm": round(merged[i][1], 1),
                 "to_mm": round(merged[i + 1][0], 1),
                 "width_mm": round(merged[i + 1][0] - merged[i][1], 1)}
                for i in range(len(merged) - 1)]
    # perpendicular depth of the assembly = offset of the parallel outer line
    depth = None
    for d in same:
        p, q = proj(d[1], d[2])
        if abs(q) > 5:
            depth = round(abs(q), 1)
            break
    return {
        "axis_from": [round(ax, 1), round(ay, 1)],
        "axis_to": [round(bx, 1), round(by, 1)],
        "run_mm": round(L, 1),
        "bearing_deg": round(bearing, 2),
        "assembly_depth_mm": depth,
        "bays": [{"from_mm": a0, "to_mm": b0, "width_mm": round(b0 - a0, 1)}
                 for a0, b0 in merged],
        "mullions": mullions,
    }


def dashed_runs(segments, mm):
    """Exploded dashed lines, found by their gap rhythm."""
    hor, ver = defaultdict(list), defaultdict(list)
    for x0, y0, x1, y1 in segments:
        X0, Y0, X1, Y1 = x0 * mm, y0 * mm, x1 * mm, y1 * mm
        if abs(Y1 - Y0) < 0.05 and DASH_MIN_MM <= abs(X1 - X0) <= DASH_MAX_MM:
            hor[round(Y0, 1)].append((min(X0, X1), max(X0, X1)))
        elif abs(X1 - X0) < 0.05 and DASH_MIN_MM <= abs(Y1 - Y0) <= DASH_MAX_MM:
            ver[round(X0, 1)].append((min(Y0, Y1), max(Y0, Y1)))

    def scan(d, axis):
        out = []
        for k, v in d.items():
            v = sorted(set(v))
            if len(v) < DASH_MIN_SEGMENTS:
                continue
            gaps = [v[i + 1][0] - v[i][1] for i in range(len(v) - 1)]
            good = [g for g in gaps if DASH_MIN_MM <= g <= DASH_MAX_MM]
            if len(good) >= 3 and len(good) >= 0.6 * len(gaps):
                out.append({"axis": axis, "line_mm": k,
                            "from_mm": round(v[0][0], 1), "to_mm": round(v[-1][1], 1),
                            "span_mm": round(v[-1][1] - v[0][0], 1),
                            "dashes": len(v), "mean_gap_mm": round(sum(good) / len(good), 1),
                            "role": "SUGGESTED FURNITURE - not built fabric. Identity not assigned."})
        return out

    runs = scan(hor, "EW") + scan(ver, "NS")
    runs.sort(key=lambda r: -r["span_mm"])
    return runs


def closed_rectangles(segments, mm, ymax, xrange_):
    """Closed axis-aligned rectangles outside the façade -- the slab extension."""
    hor, ver = defaultdict(list), defaultdict(list)
    for x0, y0, x1, y1 in segments:
        X0, Y0, X1, Y1 = x0 * mm, y0 * mm, x1 * mm, y1 * mm
        if abs(Y1 - Y0) < 0.05 and abs(X1 - X0) > 200:
            hor[round(Y0, 1)].append((min(X0, X1), max(X0, X1)))
        elif abs(X1 - X0) < 0.05 and abs(Y1 - Y0) > 200:
            ver[round(X0, 1)].append((min(Y0, Y1), max(Y0, Y1)))
    out = []
    for xa in sorted(ver):
        for xb in sorted(ver):
            if xb - xa < 400 or not (xrange_[0] <= xa and xb <= xrange_[1]):
                continue
            for ya in sorted(hor):
                if ya > ymax:
                    continue
                for yb in sorted(hor):
                    if not 100 < yb - ya < 800 or yb > ymax + 120:
                        continue
                    if not (any(a - 4 <= ya and yb <= b + 4 for a, b in ver[xa])
                            and any(a - 4 <= ya and yb <= b + 4 for a, b in ver[xb])):
                        continue
                    if not (any(a - 4 <= xa and xb <= b + 4 for a, b in hor[ya])
                            and any(a - 4 <= xa and xb <= b + 4 for a, b in hor[yb])):
                        continue
                    out.append({"x_from_mm": xa, "x_to_mm": xb, "y_from_mm": ya,
                                "y_to_mm": yb, "width_mm": round(xb - xa, 1),
                                "depth_mm": round(yb - ya, 1)})
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", default=PDF)
    ap.add_argument("--out")
    ap.add_argument("--facade-outer-mm", type=float, default=8230.6,
                    help="outer face of the 19,49 room's façade (MC)")
    ap.add_argument("--slab-x", type=float, nargs=2, default=(9800.0, 12600.0))
    args = ap.parse_args()

    ex = _extractor()
    plan = ex._load_parser().parse(args.pdf)
    segs, mm = plan["segments"], ex.MM_PER_PT

    gl = loggia_glazing(segs, mm)
    print("=== лоджия glazing ===")
    if gl:
        print("  run %.1f mm, bearing %.2f, assembly depth %s mm"
              % (gl["run_mm"], gl["bearing_deg"], gl["assembly_depth_mm"]))
        print("  %d bays: %s" % (len(gl["bays"]),
                                 ", ".join("%.0f" % b["width_mm"] for b in gl["bays"])))
        print("  %d mullions: %s" % (len(gl["mullions"]),
                                     ", ".join("%.0f" % m["width_mm"] for m in gl["mullions"])))

    rects = closed_rectangles(segs, mm, args.facade_outer_mm, args.slab_x)
    print("\n=== projecting rectangles outside the façade ===")
    for r in rects:
        print("  %.0f wide x %.0f deep   x %.1f..%.1f  y %.1f..%.1f"
              % (r["width_mm"], r["depth_mm"], r["x_from_mm"], r["x_to_mm"],
                 r["y_from_mm"], r["y_to_mm"]))

    dr = dashed_runs(segs, mm)
    print("\n=== dashed runs (suggested furniture) ===")
    for d in dr:
        print("  %s line %.1f  %.1f..%.1f  span %.0f  dashes %d  gap %.0f"
              % (d["axis"], d["line_mm"], d["from_mm"], d["to_mm"],
                 d["span_mm"], d["dashes"], d["mean_gap_mm"]))

    if args.out:
        json.dump({
            "id": "zk-dubravinskiy-v0-elements",
            "status": "DRAFT - extracted, roles not assigned by the owner.",
            "units": "mm, same sheet-relative frame as v0_named_walls_placed.json",
            "loggia_glazing": gl,
            "slab_extension_candidates": rects,
            "dashed_suggested_furniture": dr,
            "generated_by": "tools/layout/extract_v0_elements.py",
        }, open(args.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("\nwrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
