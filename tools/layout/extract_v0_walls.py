#!/usr/bin/env python3
"""Extract wall-like runs and candidate openings from the vector plan.

!! SUPERSEDED 2026-09-08 AS A WALL INVENTORY. The flat's walls are already
   modelled and named in data/canonical/wall_blocks.csv, with owner-confirmed
   thicknesses and lengths; positioning them is tools/layout/place_named_walls.py.
   Owner: "We already have all the wall segments... you're kind of doing double
   job." What this tool still earns its place for is the HATCH reading and the
   candidate OPENINGS that fall out of it, plus the face lines the placement
   tool consumes.

v0 is the baseline layout: the flat exactly as the developer builds it. Its room
schedule and dimensions were always known; its PARTITION POSITIONS were not,
because they existed only on a raster. `_Inbox/_Visual_Drop/3Б_3+ МН5_287.pdf` is
the same drawing as CAD vectors (see 00_Master/Vector_Plan_Identity_Test.md), so
they can be read rather than traced.

Method, and why each step is there
----------------------------------
1. Axis-aligned long lines are candidate WALL FACES; they are clustered and their
   spans unioned, because a face is drawn in pieces.
2. Faces are paired at a plausible wall thickness. **Pairing alone
   over-generates** -- it will happily pair one wall's face with another wall's
   face across a room.
3. A drawn wall is a SOLID and the drawing says so by HATCHING it. So a pair
   survives only if hatch strokes cross its centre line. **The threshold is low
   on purpose:** a wall with a window or a door has no hatch across the opening,
   and those are precisely the walls that matter. A cross-room false pair has
   hatch almost nowhere; a real wall with two openings still has hatch in
   between.
4. The UNHATCHED stretches of a surviving wall are reported as candidate
   OPENINGS, which is the same evidence read the other way round.

!! What this does NOT do
   - It does not name walls. Mapping these runs onto the ids in
     data/canonical/wall_blocks.csv (R1a..R9, G1..G5, M1..M6) is a separate,
     judgement-carrying step.
   - It does not decide corner ownership. That lives in wall_corners.csv and is
     enforced by build_wall_corners.py.
   - It reads PROJECT dimensions. The as-built runs +1.0% to +1.9% smaller.
"""
import argparse
import importlib.util
import json
import math
import os
import sys
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
MM_PER_PT = 75.0 / 72.0 * 25.4          # scale 1:75, derived in the identity test

THICKNESSES = [75, 100, 120, 150, 175, 200, 250, 300, 400]
THICK_TOL = 4.0
FACE_CLUSTER_MM = 1.5
FACE_MIN_MM = 150.0
GAP_JOIN_MM = 30.0
BIN_MM = 150.0
# Low on purpose -- see step 3 above. !! Calibrated, not guessed: at 0.35 the SE
# facade under the 9,36 room scored 0.34 and was deleted, because that 4200 mm
# stretch is mostly window and балконный блок. Sweeping 0.10..0.35 moves the run
# count only 41 -> 36, so this threshold is NOT what separates walls from
# non-walls; the thickness-and-overlap pairing is. What a positive threshold does
# buy is dropping the cover == 0.00 pairs, which are the true voids -- two real
# walls with a room between them.
MIN_COVER = 0.15

# Hatch angles the drawing actually uses. 45/135 fill the internal partitions;
# 50 fills the external aerated-block envelope, which is why an earlier pass
# that accepted only 45/135 dropped the whole SE facade. !! The angle is
# RECORDED, not interpreted: this repo's standing position is that the plan does
# not distinguish concrete from aerated block, and one hatch angle is not enough
# to overturn it.
HATCH_ANGLES = (45.0, 135.0, 50.0)
HATCH_ANGLE_TOL = 3.0
MIN_LEN_MM = 300.0


def _load_parser():
    spec = importlib.util.spec_from_file_location(
        "pvp", os.path.join(HERE, "parse_vector_plan.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def collect(segments):
    """-> horizontal faces, vertical faces, hatch strokes; all in mm."""
    hor, ver, hatch = defaultdict(list), defaultdict(list), []
    for x0, y0, x1, y1 in segments:
        X0, Y0 = x0 * MM_PER_PT, y0 * MM_PER_PT
        X1, Y1 = x1 * MM_PER_PT, y1 * MM_PER_PT
        dx, dy = X1 - X0, Y1 - Y0
        if abs(dy) < 0.05 and abs(dx) >= FACE_MIN_MM:
            hor[round(Y0, 1)].append((min(X0, X1), max(X0, X1)))
        elif abs(dx) < 0.05 and abs(dy) >= FACE_MIN_MM:
            ver[round(X0, 1)].append((min(Y0, Y1), max(Y0, Y1)))
        else:
            L = math.hypot(dx, dy)
            if 1.0 < L < 900:
                a = math.degrees(math.atan2(dy, dx)) % 180
                if any(abs(a - h) < HATCH_ANGLE_TOL for h in HATCH_ANGLES):
                    hatch.append((X0, Y0, X1, Y1, round(a)))
    return hor, ver, hatch


def merge_faces(d):
    out = {}
    for k in sorted(d):
        hit = next((kk for kk in out if abs(kk - k) <= FACE_CLUSTER_MM), None)
        if hit is None:
            out[k] = list(d[k])
        else:
            out[hit].extend(d[k])
    merged = {}
    for k, spans in out.items():
        spans.sort()
        acc = []
        for a, b in spans:
            if acc and a <= acc[-1][1] + GAP_JOIN_MM:
                acc[-1] = (acc[-1][0], max(acc[-1][1], b))
            else:
                acc.append((a, b))
        merged[k] = acc
    return merged


def hatch_bins(hatch, centre, lo, hi, axis):
    """Which bins along the run have a hatch stroke crossing its centre line."""
    n = max(1, int(math.ceil((hi - lo) / BIN_MM)))
    hit, angles = set(), []
    for X0, Y0, X1, Y1, ang in hatch:
        if axis == "EW":
            if (Y0 - centre) * (Y1 - centre) > 0 or abs(Y1 - Y0) < 1e-9:
                continue
            p = X0 + (centre - Y0) / (Y1 - Y0) * (X1 - X0)
        else:
            if (X0 - centre) * (X1 - centre) > 0 or abs(X1 - X0) < 1e-9:
                continue
            p = Y0 + (centre - X0) / (X1 - X0) * (Y1 - Y0)
        if lo - 1 <= p <= hi + 1:
            hit.add(min(n - 1, max(0, int((p - lo) / BIN_MM))))
            angles.append(ang)
    return hit, n, angles


def openings_from(hit, n, lo):
    """Runs of consecutive unhatched bins -> candidate openings."""
    out, i = [], 0
    while i < n:
        if i in hit:
            i += 1
            continue
        j = i
        while j < n and j not in hit:
            j += 1
        width = (j - i) * BIN_MM
        if width >= 400:                       # below a door leaf, ignore
            out.append({"from_mm": round(lo + i * BIN_MM, 1),
                        "to_mm": round(lo + j * BIN_MM, 1),
                        "approx_width_mm": round(width, 1)})
        i = j
    return out


def build_runs(faces, axis, hatch, min_cover=MIN_COVER):
    runs = []
    keys = sorted(faces)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            t = b - a
            if t > max(THICKNESSES) + THICK_TOL:
                break
            if not any(abs(t - n) <= THICK_TOL for n in THICKNESSES):
                continue
            for sa in faces[a]:
                for sb in faces[b]:
                    lo, hi = max(sa[0], sb[0]), min(sa[1], sb[1])
                    if hi - lo < MIN_LEN_MM:
                        continue
                    hit, n, angles = hatch_bins(hatch, (a + b) / 2.0, lo, hi, axis)
                    cover = len(hit) / n
                    if cover < min_cover:
                        continue
                    runs.append({
                        "axis": axis,
                        "thickness_mm": round(t, 1),
                        "face_lo_mm": round(a, 1),
                        "face_hi_mm": round(b, 1),
                        "from_mm": round(lo, 1),
                        "to_mm": round(hi, 1),
                        "length_mm": round(hi - lo, 1),
                        "hatch_cover": round(cover, 2),
                        "hatch_angle": Counter(angles).most_common(1)[0][0] if angles else None,
                        "candidate_openings": openings_from(hit, n, lo),
                    })
    return runs


def dedupe(runs):
    """Drop a run wholly inside a thicker one on the same axis -- a thin wall's
    face paired with a neighbour's far face across a hatched joint."""
    keep = []
    for r in runs:
        if any(o is not r and o["axis"] == r["axis"]
               and o["face_lo_mm"] - 1 <= r["face_lo_mm"]
               and r["face_hi_mm"] <= o["face_hi_mm"] + 1
               and o["from_mm"] - 1 <= r["from_mm"]
               and r["to_mm"] <= o["to_mm"] + 1
               and o["thickness_mm"] > r["thickness_mm"] + 1
               for o in runs):
            continue
        keep.append(r)
    return keep


def overlay(plan, runs, out_png, scale=0.115):
    """Draw the extracted runs over the plan. Looking at this is the check that
    matters -- a run list reads as plausible long after it has stopped being."""
    from PIL import Image, ImageDraw
    segs = [[c * MM_PER_PT for c in s] for s in plan["segments"]]
    xs = [v for s in segs for v in (s[0], s[2])]
    ys = [v for s in segs for v in (s[1], s[3])]
    x0, y0 = min(xs), min(ys)
    W = int((max(xs) - x0) * scale) + 20
    H = int((max(ys) - y0) * scale) + 20
    img = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(img)

    def px(x, y):
        return ((x - x0) * scale + 10, H - ((y - y0) * scale + 10))

    for s in segs:
        dr.line([px(s[0], s[1]), px(s[2], s[3])], fill=(185, 185, 185))
    for r in runs:
        if r["axis"] == "EW":
            a = px(r["from_mm"], r["face_lo_mm"])
            b = px(r["to_mm"], r["face_hi_mm"])
        else:
            a = px(r["face_lo_mm"], r["from_mm"])
            b = px(r["face_hi_mm"], r["to_mm"])
        fill = (140, 180, 255) if r["hatch_angle"] == 50 else (255, 140, 140)
        dr.rectangle([min(a[0], b[0]), min(a[1], b[1]),
                      max(a[0], b[0]), max(a[1], b[1])],
                     outline=(180, 0, 0), fill=fill)
    img = img.crop((int(W * 0.13), int(H * 0.16), int(W * 0.90), int(H * 0.80)))
    img.save(out_png)
    return img.size


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", help="the vector plan PDF")
    ap.add_argument("--out", help="write the runs as JSON")
    ap.add_argument("--min-cover", type=float, default=MIN_COVER)
    ap.add_argument("--overlay", help="write a PNG of the runs over the plan")
    args = ap.parse_args()

    plan = _load_parser().parse(args.pdf)
    hor, ver, hatch = collect(plan["segments"])
    H, V = merge_faces(hor), merge_faces(ver)

    runs = dedupe(build_runs(H, "EW", hatch, args.min_cover)
                  + build_runs(V, "NS", hatch, args.min_cover))
    runs.sort(key=lambda r: -r["length_mm"])

    print("face lines           : %d horizontal, %d vertical" % (len(H), len(V)))
    print("hatch strokes        : %d  (angles %s)"
          % (len(hatch), sorted(Counter(h[4] for h in hatch).items())))
    print("wall runs            : %d" % len(runs))
    print("thicknesses          : %s"
          % sorted(Counter(int(round(r["thickness_mm"])) for r in runs).items()))
    print()
    for r in runs:
        print("  %s t=%3d  %8.1f -> %8.1f  len %7.1f  cover %.2f  hatch %s  faces %.1f/%.1f%s"
              % (r["axis"], round(r["thickness_mm"]), r["from_mm"], r["to_mm"],
                 r["length_mm"], r["hatch_cover"], r["hatch_angle"],
                 r["face_lo_mm"], r["face_hi_mm"],
                 "  openings: " + ", ".join("%.0f@%.0f" % (o["approx_width_mm"],
                                                           o["from_mm"])
                                            for o in r["candidate_openings"])
                 if r["candidate_openings"] else ""))
    if args.overlay:
        print("\noverlay %s %s" % (args.overlay, overlay(plan, runs, args.overlay)))
    if args.out:
        payload = {
            "id": "zk-dubravinskiy-v0-wall-runs-extracted",
            "status": ("SUPERSEDED for wall inventory - DRAFT evidence only. "
                       "The flat's walls are the 25 NAMED walls in wall_blocks.csv, "
                       "positioned by tools/layout/place_named_walls.py. Owner, "
                       "2026-09-08: re-deriving a wall list from the drawing is "
                       "duplicate work. This file is kept for what it alone carries - "
                       "hatch angles and the unhatched stretches read as candidate "
                       "OPENINGS - and must not be used as a wall inventory."),
            "what": ("v0 wall runs read from the developer's vector plan. Positions and "
                     "thicknesses are the drawing's own, to ~0.1 mm. Walls are NOT named, "
                     "corners are NOT resolved, and the run list is NOT complete - see "
                     "00_Master/V0_Geometry_Status.md for what is missing."),
            "source_pdf": os.path.basename(args.pdf),
            "scale": "1:75, derived in 00_Master/Vector_Plan_Identity_Test.md",
            "units": "mm; axis EW means the run extends along x, NS along y",
            "coordinates": ("PDF user space scaled to mm, origin at the sheet, NOT a flat-local "
                            "datum. Differences between runs are meaningful; absolute values are not."),
            "dimensions_are": ("the developer's PROJECT dimensions. As-built measures +1.0% to "
                               "+1.9% SMALLER - see dimension_tolerance.json."),
            "generated_by": "tools/layout/extract_v0_walls.py",
            "runs": runs,
        }
        json.dump(payload, open(args.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("\nwrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
