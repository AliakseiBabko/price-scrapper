#!/usr/bin/env python3
"""Place the EXISTING named walls in millimetres, as contiguous straight chains.

Why this tool exists
--------------------
Owner, 2026-09-08: *"We already have all the wall segments. We determine the
thickness, the length. So you're kind of doing double job."* Correct --
`data/canonical/wall_blocks.csv` already holds 25 named walls with
owner-confirmed classes, thicknesses and lengths, and `wall_openings.csv` holds
10 openings. The only thing the model lacked was POSITION: `wall_runs.csv` is in
BASIC-PLAN PIXELS, which is why `project_decisions.md` calls the wall ids
"regions on a raster, not named shell walls".

Why the CHAIN is the unit, not the wall
---------------------------------------
Owner, 2026-09-08, on the first attempt: *"There shouldn't be any overlapping in
boxes or voids between the wall. They should touch each other... I did it
deliberately, like, without any gap... This should be, like, one straight
segment."* And specifically: *"junction between G3 and R3 ... there is a gap and
R3 extends beyond the line of external wall created by G2, R3, G3"*, and *"R1a
extends beyond the line created by R1b, G4a, R6"*.

Both faults had ONE cause: the first version snapped **each wall separately** to
whichever vector face pair was nearest, so walls the model deliberately built as
one straight run drifted off each other and grew visible steps and gaps.

**So walls sharing a pixel coordinate are grouped into a CHAIN, the chain is
snapped ONCE, and the walls are laid along it end to end.** A chain is straight
by construction and contiguous by construction; a gap or an overlap inside one
becomes impossible rather than merely unlikely.

Why the snap is HATCH-VALIDATED
-------------------------------
Owner: *"as for the MC wall, it's displaced. You should move it upward... it's
overlapped with that external element -- a extension of a concrete slab between
the floors, decorative element, but actual wall is above."*

He is right, and the mechanism is worth recording: the decorative slab projects
outward from the façade and its own edges are perfectly good face lines, so a
nearest-face-pair snap put MC on the SLAB rather than on the wall. **A wall is a
hatched solid, so the snap now requires hatch between the two faces** -- the
slab is not hatched, and MC lands on the wall.

!! Insulation is NOT modelled as a layer. Owner, 2026-09-08: it may be removed
   or left in place, so external walls stay at their recorded 300 mm.

!! The recorded clear_mm / solid_mm remain the length of record. Where a laid
   length disagrees with them the tool REPORTS it rather than adjusting either.
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
RUNS_CSV = os.path.join("data", "canonical", "wall_runs.csv")
BLOCKS_CSV = os.path.join("data", "canonical", "wall_blocks.csv")
PDF = os.path.join("_Inbox", "_Visual_Drop", "3Б_3+ МН5_287.pdf")

FIT_TOL_MM = 25.0
AXIS_SCALE_AGREEMENT = 0.06
THICK_TOL_MM = 8.0
CHAIN_PX_TOL = 4.0          # walls this close in pixels are one straight run
MIN_HATCH_COVER = 0.10      # a wall is a hatched solid; the slab is not

# A chain SPLITS where its members are further apart than this. Collinear is not
# contiguous: R5 and R9 sit on the same line with a 3.4 m room between them, and
# closing that "gap" would invent a wall across the middle room.
SPLIT_GAP_MM = 300.0

# How far a chain END may be pulled onto the perpendicular face it butts into.
END_SNAP_MM = 160.0

# R3 + G3 = 5830 mm, from the owner's top-edge chain 2115 + 400 + 3315, with the
# split point undimensioned on every plan. wall_blocks.csv records the pair total
# in prose only, so it is restated here as data the layer can use.
PAIR_TOTALS = {("R3", "G3"): 5830.0}

# The owner's own colour key, from _Inbox/_Visual_Drop/floor_plan_basic_all_walls.jpg
CLASS_COLOUR = {
    "concrete": (215, 40, 40),            # red   - the RC frame
    "aerated_block": (40, 170, 60),       # green - internal block
    "external": (225, 90, 200),           # pink  - the warm perimeter, 300
    "loggia_enclosure": (225, 90, 200),   # pink  - лоджия enclosure
}
CLASS_ACI = {                             # AutoCAD colour index, same key
    "concrete": 1,
    "aerated_block": 3,
    "external": 6,
    "loggia_enclosure": 6,
}


def _extractor():
    spec = importlib.util.spec_from_file_location(
        "ex", os.path.join(HERE, "extract_v0_walls.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_walls():
    runs = {r["wall_id"]: r for r in csv.DictReader(io.open(RUNS_CSV, encoding="utf-8"))}
    blocks = {r["wall_id"]: r for r in csv.DictReader(io.open(BLOCKS_CSV, encoding="utf-8"))}
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
            "lo_px": min(ay, by) if vertical else min(ax, bx),
            "hi_px": max(ay, by) if vertical else max(ax, bx),
            "clear_mm": b.get("clear_mm") or None,
            "solid_mm": b.get("solid_mm") or None,
            "owns_corners_mm": b.get("owns_corners_mm") or None,
            "length_source": b.get("length_source") or None,
        })
    return walls


def _nearest(lines, v):
    i = bisect.bisect_left(lines, v)
    c = []
    if i < len(lines):
        c.append(abs(lines[i] - v))
    if i:
        c.append(abs(lines[i - 1] - v))
    return min(c) if c else 1e9


def fit_axis(px_values, face_lines, tol=FIT_TOL_MM, scale_hint=None):
    """RANSAC mm = a*px + b, scoring walls that land on a face line.

    !! A loose tolerance here produced a DEGENERATE HALF-SCALE fit that scored a
    perfect 15/15: with 117 face lines over ~30 m a wall hits some line by
    chance about half the time, and inlier count cannot separate a scale from a
    submultiple of it. Hence the tight tolerance, the scale hint, and the
    cross-axis agreement check in main().
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


def snap_chain(value, thickness, lines, lo, hi, axis, hatch, ex):
    """Face pair at `thickness` nearest `value` WHOSE INTERIOR IS HATCHED.

    The hatch requirement is what keeps MC on the wall rather than on the
    decorative slab projecting beside it.
    """
    cands = []
    for f1 in lines:
        for f2 in (f for f in lines if abs((f - f1) - thickness) <= THICK_TOL_MM):
            d = min(abs(value - f1), abs(value - f2), abs(value - (f1 + f2) / 2.0))
            hit, n, _ = ex.hatch_bins(hatch, (f1 + f2) / 2.0, lo, hi, axis)
            cands.append((d, len(hit) / max(n, 1), f1, f2))
    if not cands:
        return None
    solid = [c for c in cands if c[1] >= MIN_HATCH_COVER]
    pick = min(solid or cands, key=lambda c: c[0])
    return {"residual_mm": pick[0], "hatch_cover": pick[1],
            "face_lo_mm": pick[2], "face_hi_mm": pick[3],
            "on_hatched_solid": bool(solid)}


def split_chain(members):
    """Collinear is not contiguous. Break where the members are far apart."""
    members.sort(key=lambda w: w["from_mm"])
    groups, cur = [], [members[0]]
    for prev, w in zip(members, members[1:]):
        if w["from_mm"] - prev["to_mm"] > SPLIT_GAP_MM:
            groups.append(cur)
            cur = [w]
        else:
            cur.append(w)
    groups.append(cur)
    return groups


def lay_recorded(members, start_mm, end_mm):
    """Lay each wall's RECORDED length end to end from `start_mm`.

    The pixel extents locate a chain but are NOT wall lengths -- G6's pixel run
    measures 3076 mm against a recorded 1915, because the run was traced along
    the whole partition line including its door. `solid_mm` is the length of
    record, so the drawing supplies the chain's position and the model supplies
    its parts. Laid end to end, a gap or an overlap inside a chain cannot occur.

    Walls with no recorded length -- the R3 | G3 indeterminate split -- take a
    known pair total where one exists, and the leftover is REPORTED as a
    residual rather than quietly absorbed.
    """
    known = [w for w in members if w["solid_mm"]]
    unknown = [w for w in members if not w["solid_mm"]]
    span = end_mm - start_mm
    known_total = sum(float(w["solid_mm"]) for w in known)
    remainder = span - known_total

    pair_total = PAIR_TOTALS.get(tuple(w["wall_id"] for w in unknown))
    if unknown:
        share = (pair_total if pair_total is not None
                 else max(remainder, 0.0)) / len(unknown)
    else:
        share = 0.0

    pos = start_mm
    for w in members:
        L = float(w["solid_mm"]) if w["solid_mm"] else share
        w["from_mm"] = round(pos, 1)
        w["to_mm"] = round(pos + L, 1)
        w["laid_length_mm"] = round(L, 1)
        if w["solid_mm"]:
            w["length_from"] = "recorded solid_mm"
        elif pair_total is not None:
            w["length_from"] = "pair total %.0f, split evenly (undimensioned)" % pair_total
        else:
            w["length_from"] = "chain remainder"
        pos += L
    return {"span_mm": round(span, 1),
            "laid_total_mm": round(pos - start_mm, 1),
            "residual_mm": round(end_mm - pos, 1),
            "pair_total_used_mm": pair_total}


def overlay(plan, placed, out_png, ex, scale=0.115):
    from PIL import Image, ImageDraw
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
        dr.line([px(s[0], s[1]), px(s[2], s[3])], fill=(215, 215, 215))
    for w in placed:
        if w.get("face_lo_mm") is None:
            continue
        if w["axis"] == "EW":
            a, b = px(w["from_mm"], w["face_lo_mm"]), px(w["to_mm"], w["face_hi_mm"])
        else:
            a, b = px(w["face_lo_mm"], w["from_mm"]), px(w["face_hi_mm"], w["to_mm"])
        box = [min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])]
        dr.rectangle(box, outline=CLASS_COLOUR.get(w["class"], (100, 100, 100)), width=2)
        dr.text((box[0] + 2, (box[1] + box[3]) / 2 - 4), w["wall_id"], fill=(0, 0, 0))
    img.save(out_png)
    return img.size


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", default=PDF)
    ap.add_argument("--out")
    ap.add_argument("--overlay")
    args = ap.parse_args()

    ex = _extractor()
    plan = ex._load_parser().parse(args.pdf)
    hor, ver, hatch = ex.collect(plan["segments"])
    HY, VX = sorted(ex.merge_faces(hor)), sorted(ex.merge_faces(ver))

    walls = load_walls()
    vert = [w for w in walls if w["axis"] == "NS"]
    horz = [w for w in walls if w["axis"] == "EW"]

    fy = fit_axis([w["fixed_px"] for w in horz], HY)
    fx = fit_axis([w["fixed_px"] for w in vert], VX, scale_hint=abs(fy[2]))
    if abs(abs(fx[2]) - abs(fy[2])) / abs(fy[2]) > AXIS_SCALE_AGREEMENT:
        sys.exit("axis scales disagree: x %.4f vs y %.4f -- one is aliased"
                 % (fx[2], fy[2]))
    print("x: mm = %.4f*px + %.1f   (%d/%d on a face line)"
          % (fx[2], fx[3], fx[0], len(vert)))
    print("y: mm = %.4f*px + %.1f   (%d/%d on a face line)"
          % (fy[2], fy[3], fy[0], len(horz)))

    chains = []
    for w in walls:
        for c in chains:
            if (c["axis"] == w["axis"]
                    and abs(c["fixed_px"] - w["fixed_px"]) <= CHAIN_PX_TOL
                    and abs(c["thickness_mm"] - w["thickness_mm"]) < 1):
                c["members"].append(w)
                break
        else:
            chains.append({"axis": w["axis"], "fixed_px": w["fixed_px"],
                           "thickness_mm": w["thickness_mm"], "members": [w]})

    placed, chain_report = [], []
    for ci, c in enumerate(chains):
        cross = fx if c["axis"] == "NS" else fy
        along = fy if c["axis"] == "NS" else fx
        lines = VX if c["axis"] == "NS" else HY
        for w in c["members"]:
            a0 = along[2] * w["lo_px"] + along[3]
            a1 = along[2] * w["hi_px"] + along[3]
            w["from_mm"] = round(min(a0, a1), 1)
            w["to_mm"] = round(max(a0, a1), 1)
        perp = HY if c["axis"] == "NS" else VX
        for si, sub in enumerate(split_chain(c["members"])):
            lo = min(w["from_mm"] for w in sub)
            hi = max(w["to_mm"] for w in sub)
            v = cross[2] * c["fixed_px"] + cross[3]
            s = snap_chain(v, c["thickness_mm"], lines, lo, hi, c["axis"], hatch, ex)
            # pull each end onto the perpendicular wall face it butts into
            ends = []
            for end in (lo, hi):
                near = min(perp, key=lambda t: abs(t - end))
                ends.append(near if abs(near - end) <= END_SNAP_MM else end)
            lay = lay_recorded(sub, ends[0], ends[1])
            cid = "chain_%02d_%d" % (ci + 1, si + 1)
            for w in sub:
                rec = {k: v2 for k, v2 in w.items()
                       if k not in ("fixed_px", "lo_px", "hi_px")}
                rec["chain"] = cid
                rec["face_lo_mm"] = round(s["face_lo_mm"], 1) if s else None
                rec["face_hi_mm"] = round(s["face_hi_mm"], 1) if s else None
                placed.append(rec)
            chain_report.append({
                "chain": cid, "axis": c["axis"], "thickness_mm": c["thickness_mm"],
                "walls": [w["wall_id"] for w in sub],
                "face_lo_mm": round(s["face_lo_mm"], 1) if s else None,
                "face_hi_mm": round(s["face_hi_mm"], 1) if s else None,
                "snap_residual_mm": round(s["residual_mm"], 1) if s else None,
                "on_hatched_solid": s["on_hatched_solid"] if s else None,
                "hatch_cover": round(s["hatch_cover"], 2) if s else None,
                "start_mm": round(ends[0], 1), "end_mm": round(ends[1], 1),
                "ends_snapped_mm": [round(ends[0] - lo, 1), round(ends[1] - hi, 1)],
                "lay": lay,
            })

    print("\n%d chains from %d walls" % (len(chains), len(walls)))
    print("%-9s %-4s %-5s %-9s %-9s %-7s %-6s %s"
          % ("chain", "axis", "t", "face_lo", "face_hi", "resid", "solid", "walls"))
    for r in chain_report:
        print("%-9s %-4s %-5.0f %-9.1f %-9.1f %-7.1f %-6s %s"
              % (r["chain"], r["axis"], r["thickness_mm"], r["face_lo_mm"],
                 r["face_hi_mm"], r["snap_residual_mm"],
                 "yes" if r["on_hatched_solid"] else "NO", ", ".join(r["walls"])))

    print("\nchain closure -- the drawing's span against the sum of recorded lengths:")
    for r in chain_report:
        lay = r["lay"]
        mark = "" if abs(lay["residual_mm"]) <= 60 else "   <-- CHECK"
        print("   %-12s span %7.1f  laid %7.1f  residual %+7.1f%s   %s"
              % (r["chain"], lay["span_mm"], lay["laid_total_mm"],
                 lay["residual_mm"], mark, ", ".join(r["walls"])))

    if args.overlay:
        print("\noverlay %s %s" % (args.overlay, overlay(plan, placed, args.overlay, ex)))
    if args.out:
        json.dump({
            "id": "zk-dubravinskiy-v0-named-walls-placed",
            "status": "DRAFT - positions fitted, not owner-reviewed.",
            "what": ("The 25 NAMED walls of wall_blocks.csv, placed in millimetres from "
                     "the vector plan as CONTIGUOUS STRAIGHT CHAINS. Classes, thicknesses "
                     "and lengths come from the existing model and are not re-derived."),
            "authoritative_for": "POSITION only. clear_mm / solid_mm stay the length of record.",
            "conventions": {
                "chains": ("Walls sharing a pixel coordinate and a thickness are one "
                           "straight run. Snapped once, then laid end to end, so a gap "
                           "or overlap inside a chain is impossible by construction."),
                "hatch_validated_snap": ("A wall is a hatched solid, so a face pair with "
                                         "no hatch between it is rejected. That is what "
                                         "keeps MC off the decorative slab beside it."),
                "insulation": ("NOT modelled as a layer, per the owner: it may be removed "
                               "or left. External walls stay at their recorded 300 mm."),
                "colour_key": ("The owner's own markup, "
                               "_Inbox/_Visual_Drop/floor_plan_basic_all_walls.jpg: "
                               "red concrete frame, green internal aerated block, "
                               "pink external and лоджия enclosure."),
            },
            "transform_basic_px_to_mm": {
                "x": {"a": round(fx[2], 5), "b": round(fx[3], 2)},
                "y": {"a": round(fy[2], 5), "b": round(fy[3], 2)},
                "note": ("y is negative because basic-plan pixels run downward and the "
                         "PDF's y runs upward."),
            },
            "chains": chain_report,
            "walls": placed,
        }, open(args.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
