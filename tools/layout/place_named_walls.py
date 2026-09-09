#!/usr/bin/env python3
"""Give the EXISTING named walls real millimetre positions, from the vector plan.

Why this replaces the earlier approach
--------------------------------------
Owner, 2026-09-08: *"We already have all the wall segments. We determine the
thickness, the length. So you're kind of doing double job right now. Try to sort
out the polygons in the vector image just to create overlay and include all of
the wall segments we already marked and with their parameters."*

He is right. `data/canonical/wall_blocks.csv` already holds 25 named walls with
owner-confirmed classes, thicknesses and lengths, and `wall_openings.csv` holds
10 openings with their host walls. **None of that needed re-deriving.** The one
thing the model lacked was POSITION -- `wall_runs.csv` carries coordinates in
BASIC-PLAN PIXELS, which is why `project_decisions.md` says the wall ids are
"regions on a raster, not named shell walls".

So this tool does exactly one job: **fit basic-plan pixels to the vector plan's
millimetres, and place the named walls.** The recorded parameters are carried
through untouched; nothing about a wall is re-measured.

Method
------
1. A wall in `wall_runs.csv` is axis-aligned, so it contributes ONE coordinate
   (x for a vertical wall, y for a horizontal one).
2. RANSAC a 1-D affine per axis, `mm = a*px + b`, scoring how many wall
   coordinates land on a vector FACE LINE. Both axes fit all walls.
3. Each wall is then snapped to the face PAIR whose separation matches its
   RECORDED thickness -- so the drawing supplies the position and the existing
   model supplies the wall.
4. The per-wall snap residual is reported. **It is the quality signal: a wall
   with a large residual is one whose pixel run was poor, not one whose recorded
   thickness is wrong.**

!! The recorded clear_mm / solid_mm stay authoritative for LENGTH. This tool
   does not touch them, and a face-pair span is not a substitute for them --
   see the corner-ownership convention in check_wall_junctions.py.
"""
import argparse
import bisect
import csv
import io
import itertools
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE)) if os.path.basename(HERE) == "layout" else "."
RUNS_CSV = os.path.join("data", "canonical", "wall_runs.csv")
BLOCKS_CSV = os.path.join("data", "canonical", "wall_blocks.csv")
PDF = os.path.join("_Inbox", "_Visual_Drop", "3Б_3+ МН5_287.pdf")

# !! 60 mm was too loose and produced a DEGENERATE FIT. With 117 face lines
# spread over ~30 m the mean spacing is ~250 mm, so at 60 mm tolerance a wall
# lands on some line by chance about half the time -- and a HALF-SCALE solution
# (5.56 mm/px against the true 10.16) scored a perfect 15/15. Inlier count alone
# cannot separate the right scale from a submultiple of it; the same aliasing
# that put the drawing at 1:150 instead of 1:75.
FIT_TOL_MM = 25.0

# The two axes describe one drawing, so their scales must agree. The raster's
# own aspect error is ~1.7%, so 6% is generous and still excludes a submultiple.
AXIS_SCALE_AGREEMENT = 0.06
THICK_TOL_MM = 8.0

CLASS_COLOUR = {
    "concrete": (120, 120, 130),
    "aerated_block": (140, 200, 140),
    "external": (150, 185, 255),
    "loggia_enclosure": (235, 180, 120),
}


def _extractor():
    spec = importlib.util.spec_from_file_location(
        "ex", os.path.join(HERE, "extract_v0_walls.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_walls():
    runs = {r["wall_id"]: r for r in
            csv.DictReader(io.open(RUNS_CSV, encoding="utf-8"))}
    blocks = {r["wall_id"]: r for r in
              csv.DictReader(io.open(BLOCKS_CSV, encoding="utf-8"))}
    walls = []
    for wid, r in runs.items():
        ax, ay = float(r["ax_basic_px"]), float(r["ay_basic_px"])
        bx, by = float(r["bx_basic_px"]), float(r["by_basic_px"])
        vertical = abs(ax - bx) < abs(ay - by)
        b = blocks.get(wid, {})
        walls.append({
            "wall_id": wid,
            "class": r["class"],
            "thickness_mm": float(r["thickness_mm"]),
            "axis": "NS" if vertical else "EW",
            "fixed_px": ax if vertical else ay,
            "span_px": (min(ay, by), max(ay, by)) if vertical else (min(ax, bx), max(ax, bx)),
            "clear_mm": b.get("clear_mm") or None,
            "solid_mm": b.get("solid_mm") or None,
            "owns_corners_mm": b.get("owns_corners_mm") or None,
            "length_source": b.get("length_source") or None,
        })
    return walls


def _nearest(sorted_lines, v):
    i = bisect.bisect_left(sorted_lines, v)
    cands = []
    if i < len(sorted_lines):
        cands.append(abs(sorted_lines[i] - v))
    if i:
        cands.append(abs(sorted_lines[i - 1] - v))
    return min(cands) if cands else 1e9


def fit_axis(px_values, face_lines, tol=FIT_TOL_MM, scale_hint=None):
    """RANSAC mm = a*px + b, scoring walls that land on a face line.

    Only the WIDEST pixel pairs seed a hypothesis -- a short baseline turns a
    one-pixel reading error into a large scale error -- and the scoring uses a
    bisect against the sorted face lines rather than a linear scan, which is the
    difference between this finishing in a second and in several minutes.
    """
    lines = sorted(face_lines)
    pairs = sorted(itertools.combinations(px_values, 2),
                   key=lambda pr: -abs(pr[1] - pr[0]))[:6]
    best = None
    for p1, p2 in pairs:
        if abs(p2 - p1) < 30:
            continue
        for t1 in lines:
            for t2 in lines:
                if t1 == t2:
                    continue
                a = (t2 - t1) / (p2 - p1)
                if not 5 < abs(a) < 40:
                    continue
                if scale_hint and abs(abs(a) - scale_hint) / scale_hint > AXIS_SCALE_AGREEMENT:
                    continue
                b = t1 - a * p1
                inl, err = 0, 0.0
                for p in px_values:
                    d = _nearest(lines, a * p + b)
                    if d <= tol:
                        inl += 1
                        err += d
                if best is None or (inl, -err) > (best[0], -best[1]):
                    best = (inl, err, a, b)
    if best is None:
        sys.exit("could not fit an axis")
    return best


def snap(value, thickness, face_lines):
    """Best face pair separated by `thickness`, nearest to `value`."""
    best = None
    for f1 in face_lines:
        f2c = [f for f in face_lines if abs((f - f1) - thickness) <= THICK_TOL_MM]
        for f2 in f2c:
            d = min(abs(value - f1), abs(value - f2), abs(value - (f1 + f2) / 2.0))
            if best is None or d < best[0]:
                best = (d, f1, f2)
    return best


def overlay(plan, placed, out_png, scale=0.115):
    from PIL import Image, ImageDraw
    ex = _extractor()
    segs = [[c * ex.MM_PER_PT for c in s] for s in plan["segments"]]
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
        dr.line([px(s[0], s[1]), px(s[2], s[3])], fill=(210, 210, 210))
    for w in placed:
        if w.get("face_lo_mm") is None:
            continue
        if w["axis"] == "EW":
            a = px(w["from_mm"], w["face_lo_mm"])
            b = px(w["to_mm"], w["face_hi_mm"])
        else:
            a = px(w["face_lo_mm"], w["from_mm"])
            b = px(w["face_hi_mm"], w["to_mm"])
        box = [min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])]
        dr.rectangle(box, fill=CLASS_COLOUR.get(w["class"], (200, 200, 200)),
                     outline=(60, 60, 60))
        dr.text((box[0] + 1, (box[1] + box[3]) / 2 - 5), w["wall_id"], fill=(140, 0, 0))
    img.save(out_png)
    return img.size


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", default=PDF)
    ap.add_argument("--out", help="write the placed walls as JSON")
    ap.add_argument("--overlay", help="write a labelled PNG")
    args = ap.parse_args()

    ex = _extractor()
    plan = ex._load_parser().parse(args.pdf)
    hor, ver, _hatch = ex.collect(plan["segments"])
    HY, VX = sorted(ex.merge_faces(hor)), sorted(ex.merge_faces(ver))

    walls = load_walls()
    vert = [w for w in walls if w["axis"] == "NS"]
    horz = [w for w in walls if w["axis"] == "EW"]

    # Fit each axis alone, then re-fit the weaker one under the other's scale.
    # Two independent fits that disagree on scale mean at least one is aliased,
    # and the check is cheap next to the cost of not noticing.
    fy = fit_axis([w["fixed_px"] for w in horz], HY)
    fx = fit_axis([w["fixed_px"] for w in vert], VX, scale_hint=abs(fy[2]))
    if abs(abs(fx[2]) - abs(fy[2])) / abs(fy[2]) > AXIS_SCALE_AGREEMENT:
        sys.exit("axis scales disagree: x %.4f vs y %.4f mm/px -- one is aliased"
                 % (fx[2], fy[2]))
    print("x fit: %d/%d walls on a face line, mean residual %.1f mm"
          % (fx[0], len(vert), fx[1] / max(fx[0], 1)))
    print("       mm = %.4f * basic_px + %.1f" % (fx[2], fx[3]))
    print("y fit: %d/%d walls on a face line, mean residual %.1f mm"
          % (fy[0], len(horz), fy[1] / max(fy[0], 1)))
    print("       mm = %.4f * basic_px + %.1f" % (fy[2], fy[3]))

    placed = []
    for w in walls:
        cross = fx if w["axis"] == "NS" else fy
        along = fy if w["axis"] == "NS" else fx
        lines = VX if w["axis"] == "NS" else HY
        v = cross[2] * w["fixed_px"] + cross[3]
        s = snap(v, w["thickness_mm"], lines)
        a0 = along[2] * w["span_px"][0] + along[3]
        a1 = along[2] * w["span_px"][1] + along[3]
        rec = dict(w)
        rec.pop("fixed_px")
        rec.pop("span_px")
        rec["placed_mm"] = round(v, 1)
        rec["face_lo_mm"] = round(s[1], 1) if s else None
        rec["face_hi_mm"] = round(s[2], 1) if s else None
        rec["snap_residual_mm"] = round(s[0], 1) if s else None
        rec["from_mm"] = round(min(a0, a1), 1)
        rec["to_mm"] = round(max(a0, a1), 1)
        rec["drawn_span_mm"] = round(abs(a1 - a0), 1)
        placed.append(rec)

    placed.sort(key=lambda w: (w["axis"], w["face_lo_mm"] or 0))
    print("\n%-5s %-16s %-4s %-6s %-9s %-9s %-8s %-8s %s"
          % ("id", "class", "axis", "t", "face_lo", "face_hi", "recorded", "drawn", "resid"))
    for w in placed:
        print("%-5s %-16s %-4s %-6.0f %-9.1f %-9.1f %-8s %-8.0f %+.1f"
              % (w["wall_id"], w["class"], w["axis"], w["thickness_mm"],
                 w["face_lo_mm"], w["face_hi_mm"], w["solid_mm"] or "-",
                 w["drawn_span_mm"], w["snap_residual_mm"]))

    worst = sorted(placed, key=lambda w: -(w["snap_residual_mm"] or 0))[:4]
    print("\nworst snaps: %s" % ", ".join(
        "%s %+.0f" % (w["wall_id"], w["snap_residual_mm"]) for w in worst))

    if args.overlay:
        print("overlay %s %s" % (args.overlay, overlay(plan, placed, args.overlay)))
    if args.out:
        json.dump({
            "id": "zk-dubravinskiy-v0-named-walls-placed",
            "status": "DRAFT - positions fitted, not owner-reviewed.",
            "what": ("The 25 NAMED walls of wall_blocks.csv, given millimetre positions "
                     "from the vector plan. Classes, thicknesses and lengths are carried "
                     "through from the existing model and are NOT re-derived here."),
            "authoritative_for": "POSITION only. clear_mm / solid_mm remain the length of record.",
            "transform_basic_px_to_mm": {
                "x": {"a": round(fx[2], 5), "b": round(fx[3], 2),
                      "walls_on_a_face_line": fx[0], "of": len(vert)},
                "y": {"a": round(fy[2], 5), "b": round(fy[3], 2),
                      "walls_on_a_face_line": fy[0], "of": len(horz)},
                "note": ("y is negative because basic-plan pixels run downward and the "
                         "PDF's y runs upward. The two scales differ by 0.33%, which is "
                         "the raster's own aspect error, not a disagreement about the flat."),
            },
            "generated_by": "tools/layout/place_named_walls.py",
            "walls": placed,
        }, open(args.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
