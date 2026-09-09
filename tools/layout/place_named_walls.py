#!/usr/bin/env python3
"""Attach the EXISTING wall names to the vector plan's own wall solids.

The architecture, and why it changed twice
-----------------------------------------
Owner, 2026-09-08: *"We already have all the wall segments. We determine the
thickness, the length. So you're kind of doing double job."* -- so the walls are
not re-derived. `wall_blocks.csv` holds 25 named walls with owner-confirmed
classes, thicknesses and lengths; the model lacked only POSITION, because
`wall_runs.csv` is in basic-plan pixels.

Owner, 2026-09-09, on the second attempt: *"It looks like this is interpretation
of the vector image, not the real displacement... build a processed image where
I overlay this PDF document, everything is aligned. For example R4, G8 and R8 --
they completely off the line... they randomly scattered."*

**He is right and the diagnosis is exact.** The previous version routed every
POSITION through an affine fit of basic-plan pixels. That fit has a 3.3%
anisotropy between its two axes and per-wall residuals up to 93 mm, so it
scattered walls the drawing had drawn perfectly aligned. Proof, on his own
example -- in the vector:

    R8  250   faces 5881.0 / 6131.0    along  7610.6 ..  9350.6
    G8   75   faces 6056.0 / 6131.0    along  9350.6 .. 12600.3
    R4  250   faces 6056.0 / 6305.9    along 12600.3 .. 13650.3

R8 and G8 share the face 6131.0; G8 and R4 share 6056.0; and their ends meet
exactly. **The drawing already contains touching, aligned walls.** The old code
placed G8 at 5981/6056 -- out by 75 mm, exactly one wall thickness.

So the rule is now:

  **GEOMETRY comes from the vector solids. The pixel fit is used ONLY to decide
  WHICH named wall belongs to which solid, never to position anything.**

A solid is a hatch-validated face pair -- a wall is a hatched solid, which is
also what keeps MC off the decorative slab projecting beside it. Where several
named walls share one solid (a chain), their RECORDED lengths are laid along it
in order, so a gap or overlap between them is impossible.

!! Insulation is not modelled as a layer, per the owner: external walls stay at
   their recorded thickness.
!! These are PROJECT dimensions; the as-built runs 1.0-1.9% smaller.
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
THICK_MATCH_MM = 12.0        # a named wall may only take a solid of its thickness
CROSS_MAX_MM = 400.0         # how far the fit may be wrong and still identify
# A wall continues through its door, so collinear solids sharing a face pair are
# merged across a gap up to a wide doorway. The flat's widest opening is the
# 1455 mm O10 passway; 1500 leaves margin without bridging a whole room.
MERGE_OVER_OPENING_MM = 1500.0

PAIR_TOTALS = {("R3", "G3"): 5830.0}

CLASS_COLOUR = {
    "concrete": (215, 40, 40),
    "aerated_block": (40, 170, 60),
    "external": (225, 90, 200),
    "loggia_enclosure": (225, 90, 200),
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
    """RANSAC mm = a*px + b -- used for IDENTIFICATION ONLY.

    !! Nothing is positioned by this. A loose tolerance once produced a
    degenerate HALF-SCALE fit that scored a perfect 15/15, because with 117 face
    lines a wall hits some line by chance about half the time and inlier count
    cannot separate a scale from a submultiple. The tight tolerance, the scale
    hint and the cross-axis check remain, but the fit's job is now only to say
    which solid a name belongs to.
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


def vector_solids(ex, plan, min_cover=0.15):
    """Hatch-validated face pairs, merged where they are collinear and adjacent.

    These -- not the pixel runs -- are the geometry of record.
    """
    hor, ver, hatch = ex.collect(plan["segments"])
    H, V = ex.merge_faces(hor), ex.merge_faces(ver)
    runs = ex.dedupe(ex.build_runs(H, "EW", hatch, min_cover)
                     + ex.build_runs(V, "NS", hatch, min_cover))
    # A WALL CONTINUES THROUGH ITS DOOR. An opening carries no hatch, so a wall
    # with a doorway in it arrives here as two solids -- which then pulls the
    # named walls to the wrong side of the gap. The top wall is the clear case:
    # split at the 1010 mm entrance door into 3230.9..5146.0 and
    # 6155.9..12946.0, where merging the two gives 9715.1 mm against a recorded
    # R1a + G2 + (R3+G3) of exactly 9715.
    merged = []
    for r in sorted(runs, key=lambda r: (r["axis"], r["face_lo_mm"], r["from_mm"])):
        prev = merged[-1] if merged else None
        if (prev and prev["axis"] == r["axis"]
                and abs(prev["face_lo_mm"] - r["face_lo_mm"]) < 1.5
                and abs(prev["face_hi_mm"] - r["face_hi_mm"]) < 1.5
                and r["from_mm"] <= prev["to_mm"] + MERGE_OVER_OPENING_MM):
            if r["from_mm"] > prev["to_mm"] + 2:
                prev.setdefault("bridged_openings_mm", []).append(
                    [round(prev["to_mm"], 1), round(r["from_mm"], 1)])
            prev["to_mm"] = max(prev["to_mm"], r["to_mm"])
            continue
        merged.append(dict(r))
    for i, s in enumerate(merged):
        s["solid_id"] = "S%02d" % (i + 1)
        s["length_mm"] = round(s["to_mm"] - s["from_mm"], 1)
    return merged


def clip_to_envelope(solids):
    """Clip every solid to the flat's own envelope.

    The drawing continues the neighbour's structure past this flat -- the SE
    façade solid runs 1680.9..5881.0, some 1300 mm of it beyond the party wall --
    so an unclipped solid makes a wall look far too long. The envelope is taken
    from the outermost face of the perimeter solids themselves.
    """
    xs = [f for s in solids if s["axis"] == "NS" for f in (s["face_lo_mm"], s["face_hi_mm"])]
    ys = [f for s in solids if s["axis"] == "EW" for f in (s["face_lo_mm"], s["face_hi_mm"])]
    env = {"x": (min(xs), max(xs)), "y": (min(ys), max(ys))}
    for s in solids:
        lo, hi = env["x"] if s["axis"] == "EW" else env["y"]
        before = (s["from_mm"], s["to_mm"])
        s["from_mm"] = round(max(s["from_mm"], lo), 1)
        s["to_mm"] = round(min(s["to_mm"], hi), 1)
        s["length_mm"] = round(s["to_mm"] - s["from_mm"], 1)
        if (s["from_mm"], s["to_mm"]) != before:
            s["clipped_from_mm"] = [round(before[0], 1), round(before[1], 1)]
    return env


def match(walls, solids, fx, fy):
    """Assign each named wall to a vector solid, by thickness then proximity."""
    for w in walls:
        cross = fx if w["axis"] == "NS" else fy
        along = fy if w["axis"] == "NS" else fx
        w["pred_cross_mm"] = cross[2] * w["fixed_px"] + cross[3]
        a0 = along[2] * w["lo_px"] + along[3]
        a1 = along[2] * w["hi_px"] + along[3]
        w["pred_from_mm"], w["pred_to_mm"] = min(a0, a1), max(a0, a1)

        best = None
        for s in solids:
            if s["axis"] != w["axis"]:
                continue
            if abs(s["thickness_mm"] - w["thickness_mm"]) > THICK_MATCH_MM:
                continue
            centre = (s["face_lo_mm"] + s["face_hi_mm"]) / 2.0
            dcross = min(abs(w["pred_cross_mm"] - s["face_lo_mm"]),
                         abs(w["pred_cross_mm"] - s["face_hi_mm"]),
                         abs(w["pred_cross_mm"] - centre))
            if dcross > CROSS_MAX_MM:
                continue
            ov = min(w["pred_to_mm"], s["to_mm"]) - max(w["pred_from_mm"], s["from_mm"])
            score = dcross - 0.35 * max(ov, 0.0)
            if best is None or score < best[0]:
                best = (score, dcross, ov, s)
        w["solid"] = best[3] if best else None
        w["match_cross_mm"] = round(best[1], 1) if best else None
        w["match_overlap_mm"] = round(best[2], 1) if best else None
    return walls


def solid_joints(plan, solid, mm, tol=2.0):
    """The BLOCK JOINTS the drawing itself marks inside a wall solid.

    This is the thing the basic raster could never show. `Apartment_Geometry_Sources.md`
    put it exactly: the basic plan "draws the same walls without the numbers -- so
    it cannot show where one block ends and the next begins". **The vector plan
    draws a line right across the wall's thickness at every joint**, so the
    segmentation is read rather than inferred.

    A joint is a perpendicular line reaching BOTH faces of the solid.
    """
    f_lo, f_hi = solid["face_lo_mm"], solid["face_hi_mm"]
    a_lo, a_hi = solid["from_mm"], solid["to_mm"]
    out = set()
    for x0, y0, x1, y1 in plan["segments"]:
        X0, Y0, X1, Y1 = x0 * mm, y0 * mm, x1 * mm, y1 * mm
        if solid["axis"] == "EW":
            if abs(X1 - X0) > 0.05:
                continue
            lo, hi, pos = min(Y0, Y1), max(Y0, Y1), X0
        else:
            if abs(Y1 - Y0) > 0.05:
                continue
            lo, hi, pos = min(X0, X1), max(X0, X1), Y0
        if lo <= f_lo + tol and hi >= f_hi - tol and a_lo - tol <= pos <= a_hi + tol:
            out.add(round(pos, 1))
    out.add(round(a_lo, 1))
    out.add(round(a_hi, 1))
    return sorted(out)


def lay_on_joints(members, solid, joints):
    """Walk the drawn joints, giving each wall the segments that make its length.

    A wall may span several joints -- G2 runs across the entrance door and its
    leaf, so its 2219 mm is five drawn segments. Accumulating segments until the
    recorded length is reached lands each boundary ON A DRAWN JOINT, which is
    why this removes both the residuals and the overlaps instead of trimming
    them away afterwards.
    """
    members.sort(key=lambda w: w["pred_from_mm"])
    segs = list(zip(joints, joints[1:]))
    laid, i = [], 0
    for n, w in enumerate(members):
        # !! Match against clear_mm, NOT solid_mm. A drawn joint bounds the wall's
        # CLEAR internal run; solid_mm adds the corners the wall owns on top.
        # R1a is the proof: drawn 1415.0 against a recorded clear_mm of 1416, and
        # against its solid_mm of 1666 it looks 250 mm short -- which is exactly
        # the corner it owns. Matching on solid_mm made it overshoot to the next
        # joint and swallow 500 mm of G2.
        target = float(w["clear_mm"]) if w["clear_mm"] else None
        start = segs[i][0] if i < len(segs) else solid["to_mm"]
        if target is None:
            # No recorded length -- the R3 | G3 indeterminate split. Take the
            # drawn joint nearest where the pixel fit predicts the boundary, so
            # the split still lands ON a joint the developer drew.
            if n == len(members) - 1:
                end = solid["to_mm"]
                i = len(segs)
            else:
                pred_end = w["pred_to_mm"]
                cand = [k for k in range(i + 1, len(segs) + 1)]
                i = min(cand, key=lambda k: abs(segs[k - 1][1] - pred_end))
                end = segs[i - 1][1]
        else:
            acc, best, best_err = 0.0, None, None
            j = i
            while j < len(segs):
                acc += segs[j][1] - segs[j][0]
                err = abs(acc - target)
                if best_err is None or err < best_err:
                    best_err, best = err, j + 1
                if acc > target + 400:
                    break
                j += 1
            i = best if best is not None else i + 1
            end = segs[i - 1][1] if i - 1 < len(segs) else solid["to_mm"]
        w["from_mm"], w["to_mm"] = round(start, 1), round(end, 1)
        w["laid_length_mm"] = round(end - start, 1)
        w["length_from"] = "drawn block joints"
        w["vs_recorded_mm"] = (round(w["laid_length_mm"] - float(w["clear_mm"]), 1)
                               if w["clear_mm"] else None)
        laid.append(w)
    return {"joints": joints,
            "segments_mm": [round(b - a, 1) for a, b in segs],
            "residual_mm": round(solid["to_mm"] - (laid[-1]["to_mm"] if laid else solid["from_mm"]), 1)}


def wall_box(w):
    if w["axis"] == "EW":
        return (w["from_mm"], w["face_lo_mm"], w["to_mm"], w["face_hi_mm"])
    return (w["face_lo_mm"], w["from_mm"], w["face_hi_mm"], w["to_mm"])


def overlaps(walls):
    """Every pair of wall rectangles that intersect. This is a GATE, not a report.

    Owner, 2026-09-09: *"If you see the walls overlapping, this is not a question
    for me. This is question for your method of extracting the vector graphics."*
    Quite right, so overlap is measured here and driven to zero rather than
    printed for him to adjudicate.
    """
    out = []
    for i, a in enumerate(walls):
        ax0, ay0, ax1, ay1 = wall_box(a)
        for b in walls[i + 1:]:
            bx0, by0, bx1, by1 = wall_box(b)
            ix = min(ax1, bx1) - max(ax0, bx0)
            iy = min(ay1, by1) - max(ay0, by0)
            if ix > 1.0 and iy > 1.0:
                out.append({"a": a, "b": b, "ix": ix, "iy": iy,
                            "same_axis": a["axis"] == b["axis"],
                            "area_m2": round(ix * iy / 1e6, 4)})
    return out


def _rank(w):
    """Which wall wins a contested corner: thicker, then longer. The repo's own
    rule, from tools/layout/build_wall_corners.py."""
    return (w["thickness_mm"], float(w["solid_mm"] or 0))


def resolve_overlaps(walls, ledger):
    """Trim until no two walls overlap. A corner is a solid: owned exactly once.

    Two distinct faults are handled, and they are not the same thing:

    SAME AXIS -- a thin face pair nested inside a thick one, e.g. G7's 75 mm
      band (9131.0/9206.0) lying inside R9's 250 mm band (9131.0/9380.9), where
      both pass the hatch test because the thin band is literally inside the
      thick solid. This is an EXTRACTION artefact. The thinner wall is trimmed
      back to where the thicker one ends.

    CORNER -- two perpendicular walls meeting. Exactly one owns the corner
      volume; the other stops on its face. wall_corners.csv decides where it
      has an entry, otherwise thicker-then-longer.
    """
    fixes = []
    for _ in range(12):
        bad = overlaps(walls)
        if not bad:
            break
        o = max(bad, key=lambda o: o["area_m2"])
        a, b = o["a"], o["b"]
        if o["same_axis"]:
            keep, trim = (a, b) if _rank(a) >= _rank(b) else (b, a)
            k0, t0 = keep["from_mm"], trim["from_mm"]
            if trim["from_mm"] < keep["from_mm"]:
                trim["to_mm"] = round(min(trim["to_mm"], keep["from_mm"]), 1)
            else:
                trim["from_mm"] = round(max(trim["from_mm"], keep["to_mm"]), 1)
            why = "nested same-axis solid (extraction artefact)"
        else:
            key = tuple(sorted((a["wall_id"], b["wall_id"])))
            owner_id = ledger.get(key)
            if owner_id:
                keep = a if a["wall_id"] == owner_id else b
                trim = b if keep is a else a
                why = "corner owner from wall_corners.csv"
            else:
                keep, trim = (a, b) if _rank(a) >= _rank(b) else (b, a)
                why = "corner owner by thicker-then-longer"
            # trim the loser along its own axis, back to the owner's near face
            kb = wall_box(keep)
            if trim["axis"] == "EW":
                lo, hi = kb[0], kb[2]
            else:
                lo, hi = kb[1], kb[3]
            if abs(trim["from_mm"] - hi) < abs(trim["to_mm"] - lo):
                trim["from_mm"] = round(max(trim["from_mm"], hi), 1)
            else:
                trim["to_mm"] = round(min(trim["to_mm"], lo), 1)
        trim["laid_length_mm"] = round(trim["to_mm"] - trim["from_mm"], 1)
        trim["trimmed"] = True
        fixes.append({"kept": keep["wall_id"], "trimmed": trim["wall_id"],
                      "was_mm": [round(o["ix"], 1), round(o["iy"], 1)],
                      "area_m2": o["area_m2"], "why": why,
                      "trimmed_to_mm": [trim["from_mm"], trim["to_mm"]]})
    return fixes


def load_corner_ledger():
    path = os.path.join("data", "canonical", "wall_corners.csv")
    if not os.path.exists(path):
        return {}
    out = {}
    for r in csv.DictReader(io.open(path, encoding="utf-8")):
        out[tuple(sorted((r["wall_a"], r["wall_b"])))] = r["owner"]
    return out


def lay_on_solid(members, solid):
    """Lay the members' RECORDED lengths in order along the solid's own extent."""
    members.sort(key=lambda w: w["pred_from_mm"])
    known = [w for w in members if w["solid_mm"]]
    unknown = [w for w in members if not w["solid_mm"]]
    span = solid["length_mm"]
    known_total = sum(float(w["solid_mm"]) for w in known)
    pair_total = PAIR_TOTALS.get(tuple(w["wall_id"] for w in unknown))
    if unknown:
        share = (pair_total if pair_total is not None
                 else max(span - known_total, 0.0)) / len(unknown)
    else:
        share = 0.0
    pos = solid["from_mm"]
    for w in members:
        L = float(w["solid_mm"]) if w["solid_mm"] else share
        w["from_mm"], w["to_mm"] = round(pos, 1), round(pos + L, 1)
        w["laid_length_mm"] = round(L, 1)
        w["length_from"] = ("recorded solid_mm" if w["solid_mm"]
                            else ("pair total %.0f, split evenly (undimensioned)" % pair_total
                                  if pair_total is not None else "solid remainder"))
        pos += L
    return {"solid_span_mm": span, "laid_total_mm": round(pos - solid["from_mm"], 1),
            "residual_mm": round(solid["to_mm"] - pos, 1),
            "pair_total_used_mm": pair_total}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", default=PDF)
    ap.add_argument("--out")
    args = ap.parse_args()

    ex = _extractor()
    plan = ex._load_parser().parse(args.pdf)
    hor, ver, _h = ex.collect(plan["segments"])
    HY, VX = sorted(ex.merge_faces(hor)), sorted(ex.merge_faces(ver))
    solids = vector_solids(ex, plan)
    env = clip_to_envelope(solids)
    print("vector solids (hatch-validated, merged over openings, clipped): %d" % len(solids))
    print("flat envelope: x %.1f..%.1f   y %.1f..%.1f"
          % (env["x"][0], env["x"][1], env["y"][0], env["y"][1]))

    walls = load_walls()
    vert = [w for w in walls if w["axis"] == "NS"]
    horz = [w for w in walls if w["axis"] == "EW"]
    fy = fit_axis([w["fixed_px"] for w in horz], HY)
    fx = fit_axis([w["fixed_px"] for w in vert], VX, scale_hint=abs(fy[2]))
    print("identification fit only:  x %.4f mm/px,  y %.4f mm/px" % (fx[2], fy[2]))

    match(walls, solids, fx, fy)
    groups = {}
    unmatched = []
    for w in walls:
        if w["solid"] is None:
            unmatched.append(w)
        else:
            groups.setdefault(w["solid"]["solid_id"], []).append(w)

    report = []
    for sid, members in sorted(groups.items()):
        solid = members[0]["solid"]
        js = solid_joints(plan, solid, ex.MM_PER_PT)
        lay = (lay_on_joints(members, solid, js) if len(js) > 2
               else lay_on_solid(members, solid))
        report.append({"solid_id": sid, "axis": solid["axis"],
                       "thickness_mm": solid["thickness_mm"],
                       "face_lo_mm": solid["face_lo_mm"], "face_hi_mm": solid["face_hi_mm"],
                       "from_mm": solid["from_mm"], "to_mm": solid["to_mm"],
                       "walls": [w["wall_id"] for w in members], "lay": lay})

    print("\n%-5s %-4s %-5s %-9s %-9s %-9s %-9s %-8s %s"
          % ("solid", "ax", "t", "face_lo", "face_hi", "from", "to", "resid", "walls"))
    for r in sorted(report, key=lambda r: (r["axis"], r["face_lo_mm"])):
        print("%-5s %-4s %-5.0f %-9.1f %-9.1f %-9.1f %-9.1f %+-8.1f %s"
              % (r["solid_id"], r["axis"], r["thickness_mm"], r["face_lo_mm"],
                 r["face_hi_mm"], r["from_mm"], r["to_mm"],
                 r["lay"]["residual_mm"], ", ".join(r["walls"])))

    print("\nDRAWN length against the RECORDED length, per wall:")
    print("  %-5s %-5s %-10s %-10s %-9s %s"
          % ("wall", "t", "clear_mm", "drawn", "delta", "from the"))
    deltas = []
    for w in sorted((w for w in walls if w["solid"]),
                    key=lambda w: -abs(w.get("vs_recorded_mm") or 0)):
        d = w.get("vs_recorded_mm")
        print("  %-5s %-5.0f %-10s %-10.1f %-9s %s"
              % (w["wall_id"], w["thickness_mm"], w["solid_mm"] or "-",
                 w.get("laid_length_mm") or 0.0,
                 ("%+.1f" % d) if d is not None else "-",
                 w.get("length_from") or "-"))
        if d is not None:
            deltas.append(abs(d))
    if deltas:
        deltas.sort()
        print("  |delta|: median %.1f mm, p90 %.1f mm, max %.1f mm, n=%d"
              % (deltas[len(deltas) // 2], deltas[int(len(deltas) * 0.9)],
                 deltas[-1], len(deltas)))

    if unmatched:
        print("\n⚠ UNMATCHED -- no hatched vector solid of this thickness nearby:")
        for w in unmatched:
            print("   %-5s %-16s t=%3.0f  predicted cross %.1f"
                  % (w["wall_id"], w["class"], w["thickness_mm"], w["pred_cross_mm"]))

    # --- drive overlaps to zero -------------------------------------
    ledger = load_corner_ledger()
    positioned = [w for w in walls if w["solid"] is not None]
    for w in positioned:
        w["face_lo_mm"] = w["solid"]["face_lo_mm"]
        w["face_hi_mm"] = w["solid"]["face_hi_mm"]
    before = overlaps(positioned)
    fixes = resolve_overlaps(positioned, ledger)
    after = overlaps(positioned)
    print("\noverlaps: %d before (%.3f m2) -> %d after"
          % (len(before), sum(o["area_m2"] for o in before), len(after)))
    for f in fixes:
        print("   kept %-5s trimmed %-5s  %5.0f x %-5.0f mm  %s"
              % (f["kept"], f["trimmed"], f["was_mm"][0], f["was_mm"][1], f["why"]))
    if after:
        print("\n!! STILL OVERLAPPING -- an extraction fault, not a model question:")
        for o in after:
            print("   %-5s x %-5s  %.0f x %.0f mm"
                  % (o["a"]["wall_id"], o["b"]["wall_id"], o["ix"], o["iy"]))

    placed = []
    for w in walls:
        rec = {k: v for k, v in w.items()
               if k not in ("fixed_px", "lo_px", "hi_px", "solid")}
        rec["solid_id"] = w["solid"]["solid_id"] if w["solid"] else None
        if w["solid"]:
            rec["face_lo_mm"] = w["solid"]["face_lo_mm"]
            rec["face_hi_mm"] = w["solid"]["face_hi_mm"]
        else:
            rec["face_lo_mm"] = rec["face_hi_mm"] = None
            rec["from_mm"] = rec["to_mm"] = None
        placed.append(rec)

    print("\nmatched %d of %d walls onto %d solids"
          % (len(walls) - len(unmatched), len(walls), len(report)))

    if args.out:
        json.dump({
            "id": "zk-dubravinskiy-v0-named-walls-placed",
            "status": "DRAFT - not owner-reviewed.",
            "what": ("The 25 NAMED walls of wall_blocks.csv attached to the vector plan's "
                     "own hatch-validated wall solids. GEOMETRY comes from the vector; the "
                     "pixel fit is used only to decide which name belongs to which solid."),
            "why": ("Owner, 2026-09-09: routing positions through the basic-plan pixel fit "
                    "scattered walls the drawing had drawn aligned -- R8/G8/R4 share faces "
                    "exactly in the vector and were placed up to one wall thickness apart. "
                    "The fit has a 3.3% anisotropy and residuals to 93 mm; the vector does not."),
            "authoritative_for": "POSITION and FACES. clear_mm / solid_mm stay the length of record.",
            "identification_fit_basic_px_to_mm": {
                "x": {"a": round(fx[2], 5), "b": round(fx[3], 2)},
                "y": {"a": round(fy[2], 5), "b": round(fy[3], 2)},
                "use": ("IDENTIFICATION ONLY -- deciding which solid a name belongs to. "
                        "No wall face or extent comes from this. Still needed to place "
                        "OPENING spans, which exist only as basic-plan pixels in "
                        "wall_opening_spans.csv; those inherit the fit's error until the "
                        "openings are matched to the vector's own unhatched gaps."),
                "known_error": ("3.3% anisotropy between the axes, per-wall residuals to "
                                "93 mm. This is exactly why geometry no longer uses it."),
            },
            "flat_envelope_mm": {"x": [round(env["x"][0], 1), round(env["x"][1], 1)],
                                 "y": [round(env["y"][0], 1), round(env["y"][1], 1)]},
            "overlap_resolution": {
                "before": len(before), "after": len(after), "fixes": fixes,
                "rule": ("A corner is a solid, owned exactly once. wall_corners.csv "
                         "decides where it has an entry, otherwise thicker-then-longer. "
                         "A same-axis overlap is an extraction artefact -- a thin face "
                         "pair nested inside a thick one -- and the thinner wall is "
                         "trimmed to where the thicker ends."),
            },
            "solids": report,
            "unmatched": [w["wall_id"] for w in unmatched],
            "walls": placed,
        }, open(args.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
