#!/usr/bin/env python3
"""Export v0 to DXF for AutoCAD -- walls, openings, glazing, slab, suggested furniture.

Part one of the two the owner asked for on 2026-09-08: *"I would like to have
something which could be exported into AutoCAD format. And also I would like
something I can use for my own model."* This is the AutoCAD half; the 3D half is
separate.

What goes in, and on which layer
--------------------------------
Layer colours follow **the owner's own markup**,
`_Inbox/_Visual_Drop/floor_plan_basic_all_walls.jpg`:

  V0-WALL-CONCRETE    red      the monolithic RC frame (R1a..R9)
  V0-WALL-AERATED     green    internal aerated block (G2..G8)
  V0-WALL-EXTERNAL    magenta  the 300 mm warm perimeter (MA, MB, MC)
  V0-WALL-LOGGIA      magenta  лоджия enclosure (M2, M6b)
  V0-WALL-LABEL       grey     the wall id, so a name survives the round trip
  V0-OPENING          cyan     doors and windows, from wall_opening_spans.csv
  V0-LOGGIA-GLAZING   cyan     the four glass bays and their three mullions
  V0-SLAB-EXTENSION   yellow   the decorative slab projecting at the 19,49 window
  V0-SUGGESTED-FURN   orange, DASHED   the developer's suggested wardrobes

!! V0-SUGGESTED-FURN IS NOT BUILT FABRIC. It is on its own layer, dashed, in the
   drawing's own convention, so it can be frozen or deleted in one action. The
   source drawing contains no PDF dash operator at all -- its dashes are exploded
   into short segments -- so this layer is the only thing separating the
   developer's furniture suggestion from the flat.

!! Insulation is NOT a layer here. Owner: it may be removed or left in place, so
   external walls are exported at their recorded 300 mm and nothing else.

!! These are PROJECT dimensions. The as-built measures +1.0% to +1.9% smaller.
"""
import argparse
import csv
import io
import json
import os
import sys

import ezdxf

PLACED = os.path.join("data", "canonical", "v0_named_walls_placed.json")
OPENINGS_PLACED = os.path.join("data", "canonical", "v0_openings_placed.json")
CORNERS = os.path.join("data", "canonical", "wall_corners.csv")
ELEMENTS = os.path.join("data", "canonical", "v0_elements_extracted.json")
SPANS = os.path.join("data", "canonical", "wall_opening_spans.csv")
OPENINGS = os.path.join("data", "canonical", "wall_openings.csv")

LAYERS = {
    "V0-WALL-CONCRETE": 1,
    "V0-WALL-AERATED": 3,
    "V0-WALL-EXTERNAL": 6,
    "V0-WALL-LOGGIA": 6,
    "V0-WALL-LABEL": 8,
    "V0-OPENING": 4,
    "V0-LOGGIA-GLAZING": 4,
    # the frame spanning the FULL run. The bays stop 43.5 mm short at one end
    # and 91.8 mm at the other, which is the assembly's end reveals - real
    # frame, and drawing only the glass left the enclosure visibly open there.
    "V0-LOGGIA-FRAME": 5,
    "V0-SLAB-EXTENSION": 2,
}
# !! V0-SUGGESTED-FURN is GONE. Owner, 2026-09-09: the dashed lines in the G3 /
# kitchen area are "not necessary here, absolutely" - a leftover from the CAD
# file, not a decision. Exporting the developer's furniture suggestion onto a
# drawing of the flat invites it to be read as fabric, and it has no standing.
# The runs are still recorded in v0_elements_extracted.json if ever wanted.
CLASS_LAYER = {
    "concrete": "V0-WALL-CONCRETE",
    "aerated_block": "V0-WALL-AERATED",
    "external": "V0-WALL-EXTERNAL",
    "loggia_enclosure": "V0-WALL-LOGGIA",
}


def close_corners(walls):
    """Extend each corner OWNER so the corner is solid, not a void.

    Owner, 2026-09-09: *"if I have this corner, R1b and R1a, one of this wall
    should go up to the end of the another one... we need to factor in the
    thickness of the wall to have a closed corner, which is actually the case in
    reality."*

    He is right, and this is the gap between the two lengths the model already
    carries. The walls are laid at their CLEAR run, which is what a tape inside
    the room reads - so every L-corner comes out as an open square. `solid_mm`
    is `clear_mm` plus the corners that wall OWNS, and `wall_corners.csv` says
    who owns which. Applying it here closes every corner with no double count,
    because exactly one of the two walls is extended.
    """
    by_id = {w["wall_id"]: w for w in walls}
    fixes = []
    if not os.path.exists(CORNERS):
        return fixes
    for r in csv.DictReader(io.open(CORNERS, encoding="utf-8")):
        own, other = by_id.get(r["owner"]), None
        pair = (r["wall_a"], r["wall_b"])
        other_id = pair[1] if r["owner"] == pair[0] else pair[0]
        other = by_id.get(other_id)
        if not own or not other or own.get("from_mm") is None                 or other.get("from_mm") is None:
            continue
        gain = float(r["owner_gains_mm"])
        ob = wall_box(other)
        # the corner sits at whichever end of the owner is nearer the other wall
        lo, hi = (ob[1], ob[3]) if own["axis"] == "NS" else (ob[0], ob[2])
        centre = (lo + hi) / 2.0
        # !! Extend only AS FAR AS the other wall's far face, never by a flat
        # thickness. R8 already spanned MA's band, so adding its full 300 mm gain
        # pushed it 350 mm past the corner and straight into G8 - an overlap the
        # closure gate caught. Clamping makes the corner exactly solid and no
        # more, which is what "owns the corner" means.
        if abs(own["from_mm"] - centre) <= abs(own["to_mm"] - centre):
            target = lo
            if own["from_mm"] > target:
                own["from_mm"] = round(target, 1)
                end = "start"
            else:
                end = "start (already covered)"
                gain = 0.0
        else:
            target = hi
            if own["to_mm"] < target:
                own["to_mm"] = round(target, 1)
                end = "end"
            else:
                end = "end (already covered)"
                gain = 0.0
        own["closed_corner"] = True
        fixes.append((r["corner_id"], r["owner"], other_id, gain, end))
    return fixes


def yield_quarantined(walls):
    """A wall placed by directive gives way to the accepted geometry it abuts.

    !! M6b is placed from R8's *pre-extension* start, but `close_corners` then
    grows R8 onto MB's face - so R8's DRAWN body ran 50 mm into M6b and the gate
    reported an unsanctioned overlap. Reordering will not help in general: the
    directive is written against a declared face, and corner closure legitimately
    moves drawn extents afterwards.

    The rule is an ordering of authority, not a nudge. Quarantined geometry
    (`provisional_*` status, excluded from quantities) never displaces accepted
    geometry: it is trimmed back to abut, keeping its declared face alignment and
    losing length. The trim is reported, because a quarantined wall that has lost
    length is a fact about the unresolved thickness question, not a detail.
    """
    out = []
    q = [w for w in walls if w.get("placement_directive")
         and "quarantin" in (w.get("status") or "")]
    if not q:
        return out
    for w in q:
        ref = None
        for o in walls:
            if o is w or o.get("from_mm") is None or o.get("placement_directive"):
                continue
            if o["axis"] != w["axis"]:
                continue
            # collinear: the cross-axis bands must overlap
            if min(o["face_hi_mm"], w["face_hi_mm"]) <= max(o["face_lo_mm"],
                                                            w["face_lo_mm"]):
                continue
            ov = min(o["to_mm"], w["to_mm"]) - max(o["from_mm"], w["from_mm"])
            if ov <= 0:
                continue
            if ref is None or ov > ref[1]:
                ref = (o, ov)
        if ref is None:
            continue
        o, ov = ref
        was = w["to_mm"] - w["from_mm"]
        # trim at the end that meets the accepted wall
        if abs(w["to_mm"] - o["from_mm"]) < abs(w["from_mm"] - o["to_mm"]):
            w["to_mm"] = round(o["from_mm"], 1)
        else:
            w["from_mm"] = round(o["to_mm"], 1)
        w["laid_length_mm"] = round(w["to_mm"] - w["from_mm"], 1)
        w["yielded_mm"] = round(was - w["laid_length_mm"], 1)
        out.append((w["wall_id"], o["wall_id"], w["yielded_mm"],
                    w["laid_length_mm"]))
    return out


SNAP_MM = 25.0     # below this a perpendicular gap is extraction noise


LOGGIA_ENCLOSURE = ('M2', 'M6b')


def close_loggia_loop(walls, gl):
    """Bring the лоджия's enclosure walls down onto the glazing axis.

    !! CODEX round 3, finding 5, and it is right that this is *"locally
    modellable work, not an owner blocker"*: M6b existing did not make the
    лоджия a closed loop. The glazing runs at the drawing's true splay while M2
    and M6b are axis-aligned boxes, and both stopped short of the glazing line -
    M2 by 58 mm, M6b by 291 mm. So the enclosure had a hole at each end and the
    review PNG showed the glazing floating.

    The axis is the DRAWING's, from `loggia_glazing.axis_from/axis_to`, not a
    line fitted to anything here. For each enclosure wall the target is the
    axis's y at the LOWER of its two faces, so the wall's whole thickness meets
    the line rather than just its centreline.
    """
    out = []
    if not gl:
        return out
    ax, ay = gl["axis_from"]
    bx, by = gl["axis_to"]
    if abs(bx - ax) < 1e-6:
        return out

    def y_on_axis(x):
        return ay + (by - ay) * (x - ax) / (bx - ax)

    by_id = {w["wall_id"]: w for w in walls}
    for wid in LOGGIA_ENCLOSURE:
        w = by_id.get(wid)
        if not w or w.get("from_mm") is None or w["axis"] != "NS":
            continue
        target = min(y_on_axis(w["face_lo_mm"]), y_on_axis(w["face_hi_mm"]))
        if w["from_mm"] <= target + 1.0:
            continue                      # already reaches the glazing
        gain = w["from_mm"] - target
        w["from_mm"] = round(target, 1)
        w["laid_length_mm"] = round(w["to_mm"] - w["from_mm"], 1)
        out.append((wid, gain, w["laid_length_mm"]))
    return out


def snap_near_misses(walls):
    """Close a SUB-TOLERANCE perpendicular gap by extending the lesser wall.

    !! MA's top face lands at 9350.3 and R6 starts at 9360.6 - a 10.3 mm butt
    joint the owner would read as one of the cavities he has asked three times to
    be rid of. Nothing caught it, because the near-miss check was documented in
    the closure gate and never implemented.

    10 mm is not a model question. `Geometry_Variance_Study.md` puts the BUILD
    tolerance at +30/-45 mm against three surveyed flats, so a gap an order of
    magnitude below that is noise in the vector extraction, not a design
    decision, and snapping it is a statement about the drawing rather than about
    the flat. A gap ABOVE `SNAP_MM` is left alone deliberately: the closure gate
    fails on it and the owner decides, which is what happened with J_G4a_G4b.

    The wall that yields is the lesser one under the ledger's own ownership rule
    - thinner first, then shorter - so the thicker/longer wall's recorded extent
    is never disturbed.
    """
    out = []
    for i, a in enumerate(walls):
        for b in walls[i + 1:]:
            if a.get("from_mm") is None or b.get("from_mm") is None:
                continue
            if a["axis"] == b["axis"]:
                continue
            ax0, ay0, ax1, ay1 = wall_box(a)
            bx0, by0, bx1, by1 = wall_box(b)
            ix = min(ax1, bx1) - max(ax0, bx0)
            iy = min(ay1, by1) - max(ay0, by0)
            if ix > 1.0 and -SNAP_MM <= iy < 0.0:
                gap, axis_gap = -iy, "y"
            elif iy > 1.0 and -SNAP_MM <= ix < 0.0:
                gap, axis_gap = -ix, "x"
            else:
                continue
            # the lesser wall yields: thinner, then shorter
            ka = (a["face_hi_mm"] - a["face_lo_mm"], a["to_mm"] - a["from_mm"])
            kb = (b["face_hi_mm"] - b["face_lo_mm"], b["to_mm"] - b["from_mm"])
            mover, fixed = (a, b) if ka < kb else (b, a)
            fb = wall_box(fixed)
            lo, hi = ((fb[1], fb[3]) if mover["axis"] == "NS"
                      else (fb[0], fb[2]))
            if abs(mover["from_mm"] - hi) < abs(mover["to_mm"] - lo):
                mover["from_mm"] = round(hi, 1)
            else:
                mover["to_mm"] = round(lo, 1)
            mover["laid_length_mm"] = round(mover["to_mm"] - mover["from_mm"], 1)
            out.append((mover["wall_id"], fixed["wall_id"], gap, axis_gap))
    return out


def wall_box(w):
    """(x0, y0, x1, y1) of a placed wall."""
    if w["axis"] == "EW":
        return w["from_mm"], w["face_lo_mm"], w["to_mm"], w["face_hi_mm"]
    return w["face_lo_mm"], w["from_mm"], w["face_hi_mm"], w["to_mm"]


def rect(msp, layer, x0, y0, x1, y1):
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                       close=True, dxfattribs={"layer": layer})


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=os.path.join("data", "cad", "dxf", "v0_developer_layout.dxf"))
    args = ap.parse_args()

    placed = json.load(io.open(PLACED, encoding="utf-8"))
    walls = placed["walls"]
    tx = placed["identification_fit_basic_px_to_mm"]
    elements = json.load(io.open(ELEMENTS, encoding="utf-8"))

    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4          # millimetres
    for name, colour in LAYERS.items():
        doc.layers.add(name, color=colour, linetype="CONTINUOUS")
    msp = doc.modelspace()

    fixes = close_corners(walls)
    loop = close_loggia_loop(walls, elements.get("loggia_glazing"))
    yields = yield_quarantined(walls)
    snaps = snap_near_misses(walls)
    # The invariant, reported every run: once the owned corners are added, a
    # wall's DRAWN extent must equal its recorded solid_mm. Laying at clear and
    # then closing corners is the only way that holds; laying at solid and
    # closing counted them twice, which is how R8 came out 2390 against 2090.
    for wid, gain, now in loop:
        print("   %-5s extended %.1f mm onto the glazing axis (now %.1f mm "
              "drawn) - the лоджия loop" % (wid, gain, now))
    for wid, ref, gap, ax in snaps:
        print("   %-5s snapped %.1f mm in %s onto %-5s (below the %.0f mm "
              "extraction-noise floor)" % (wid, gap, ax, ref, SNAP_MM))
    for wid, ref, lost, now in yields:
        print("   %-5s yielded %.0f mm to %-5s (quarantined; now %.0f mm drawn)"
              % (wid, lost, ref, now))
    blocks = {r["wall_id"]: r for r in
              csv.DictReader(io.open(os.path.join("data", "canonical",
                                                  "wall_blocks.csv"),
                                     encoding="utf-8"))}
    off = []
    for w in walls:
        s_mm = blocks.get(w["wall_id"], {}).get("solid_mm")
        if not s_mm or w.get("from_mm") is None:
            continue
        drawn = w["to_mm"] - w["from_mm"]
        if abs(drawn - float(s_mm)) > 15.0:
            off.append((w["wall_id"], drawn, float(s_mm)))
    print("drawn == solid_mm: %d of %d walls within 15 mm"
          % (sum(1 for w in walls if w.get("from_mm") is not None) - len(off),
             sum(1 for w in walls if w.get("from_mm") is not None)))
    for wid, drawn, want in sorted(off, key=lambda t: -abs(t[1] - t[2])):
        print("   %-5s drawn %8.1f  solid_mm %8.0f  %+8.1f" % (wid, drawn, want, drawn - want))

    print("corners closed: %d" % len(fixes))
    for cid, own, oth, gain, end in fixes:
        print("   %-12s %s extended %+.0f mm at its %s, over %s"
              % (cid, own, gain, end, oth))

    # --- walls -------------------------------------------------------
    for w in walls:
        if w.get("face_lo_mm") is None:
            continue
        x0, y0, x1, y1 = wall_box(w)
        rect(msp, CLASS_LAYER.get(w["class"], "V0-WALL-CONCRETE"), x0, y0, x1, y1)
        msp.add_text(w["wall_id"], height=90,
                     dxfattribs={"layer": "V0-WALL-LABEL"}).set_placement(
            ((x0 + x1) / 2.0, (y0 + y1) / 2.0))
    print("walls: %d" % len(walls))

    # --- openings, from the VECTOR ------------------------------------
    # !! No longer transformed from basic-plan pixels. The fit has 3.3%
    # anisotropy and it moved O3 106 mm off the decorative slab the developer
    # drew concentric with it. An opening that cannot be found in the vector is
    # OMITTED, not drawn at a plausible guess.
    notes = {r["opening_id"]: r for r in csv.DictReader(io.open(OPENINGS, encoding="utf-8"))}
    n_open, omitted = 0, []
    if os.path.exists(OPENINGS_PLACED):
        op = json.load(io.open(OPENINGS_PLACED, encoding="utf-8"))
        for o in op.get("openings", []):
            if o["axis"] == "EW":
                rect(msp, "V0-OPENING", o["from_mm"], o["face_lo_mm"],
                     o["to_mm"], o["face_hi_mm"])
            else:
                rect(msp, "V0-OPENING", o["face_lo_mm"], o["from_mm"],
                     o["face_hi_mm"], o["to_mm"])
            kind = notes.get(o["opening_id"], {}).get("type", "opening")
            msp.add_text("%s %s" % (o["opening_id"], kind), height=70,
                         dxfattribs={"layer": "V0-OPENING"}).set_placement(
                ((o["from_mm"] + o["to_mm"]) / 2.0,
                 (o["face_lo_mm"] + o["face_hi_mm"]) / 2.0))
            n_open += 1
        omitted = [u["opening_id"] for u in op.get("unplaced", [])]
    print("openings: %d from the vector" % n_open)
    if omitted:
        print("           OMITTED, not guessed: %s" % ", ".join(omitted))

    # --- лоджия glazing: four bays and three mullions ----------------
    gl = elements.get("loggia_glazing")
    if gl:
        import math
        ax, ay = gl["axis_from"]
        bx, by = gl["axis_to"]
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = -uy, ux
        d = gl["assembly_depth_mm"] or 150.0

        def band(p0, p1, layer):
            pts = [(ax + ux * p0, ay + uy * p0),
                   (ax + ux * p1, ay + uy * p1),
                   (ax + ux * p1 + nx * d, ay + uy * p1 + ny * d),
                   (ax + ux * p0 + nx * d, ay + uy * p0 + ny * d)]
            msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})

        band(0.0, gl["run_mm"], "V0-LOGGIA-FRAME")
        for i, bay in enumerate(gl["bays"], 1):
            band(bay["from_mm"], bay["to_mm"], "V0-LOGGIA-GLAZING")
        for m in gl["mullions"]:
            band(m["from_mm"], m["to_mm"], "V0-LOGGIA-GLAZING")
        print("лоджия glazing: %d bays, %d mullions, run %.1f"
              % (len(gl["bays"]), len(gl["mullions"]), gl["run_mm"]))

    # --- the decorative slab: the DEEPEST candidate rectangle --------
    cands = elements.get("slab_extension_candidates") or []
    if cands:
        s = max(cands, key=lambda r: r["depth_mm"])
        rect(msp, "V0-SLAB-EXTENSION", s["x_from_mm"], s["y_from_mm"],
             s["x_to_mm"], s["y_to_mm"])
        msp.add_text("slab extension %.0fx%.0f" % (s["width_mm"], s["depth_mm"]),
                     height=80, dxfattribs={"layer": "V0-SLAB-EXTENSION"}).set_placement(
            (s["x_from_mm"], s["y_from_mm"] - 140))
        print("slab extension: %.0f x %.0f" % (s["width_mm"], s["depth_mm"]))

    # Suggested furniture is deliberately NOT exported - see the note above.

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    doc.saveas(args.out)
    print("\nwrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
