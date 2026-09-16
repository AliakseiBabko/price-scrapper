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

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
from lib import rectunion as ru  # noqa: E402

# ⚠️ REPO-ABSOLUTE, not relative. These were relative to the working directory,
# so running from tools/layout silently resolved them to nothing: close_corners
# returned 0 fixes instead of 8 and the geometry came out DIFFERENT with no
# error. Anchoring on this file's own location makes the output independent of
# where the process was started, which a compiler consumed by several generators
# has to be.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _canon(name):
    return os.path.join(REPO, "data", "canonical", name)


PLACED = _canon("v0_named_walls_placed.json")
OPENINGS_PLACED = _canon("v0_openings_placed.json")
CORNERS = _canon("wall_corners.csv")
ELEMENTS = _canon("v0_elements_extracted.json")
SPANS = _canon("wall_opening_spans.csv")
SHAFTS = _canon("ventilation_shafts.csv")
OPENINGS = _canon("wall_openings.csv")

LAYERS = {
    "V0-WALL-CONCRETE": 1,
    "V0-WALL-AERATED": 3,
    "V0-WALL-EXTERNAL": 6,
    "V0-WALL-LOGGIA": 6,
    "V0-WALL-LABEL": 8,
    "V0-OPENING": 4,
    "V0-LOGGIA-GLAZING": 4,
    # The external insulation. Owner 2026-09-10 reversed his 2026-09-08
    # instruction that it must not be a modelled layer: "There should be an
    # insulation layer, which is outside - 70 millimetres thick. I want you to
    # draw this external insulation layer instead of leaving the gap." The gap
    # he pointed at, M2 to MA, is exactly 70.0 mm - it was never a defect, it
    # was a missing element. Placed by tools/layout/place_insulation.py, which
    # takes the SIDE from the drawing rather than from a heuristic.
    "V0-INSULATION": 33,
    # the frame spanning the FULL run. The bays stop 43.5 mm short at one end
    # and 91.8 mm at the other, which is the assembly's end reveals - real
    # frame, and drawing only the glass left the enclosure visibly open there.
    "V0-LOGGIA-FRAME": 5,
    "V0-SLAB-EXTENSION": 2,
    # The two common-property ventilation shafts. They are NOT walls and must
    # never be counted as walls - but the approved wall model has always held
    # "25 walls + 2 shafts", and they were the one part of it the DXF omitted
    # entirely. Owner: "we need to include the ventilation shaft, which is next
    # between R3 and R5. This is not a wall, but it is a structural element
    # [that] will surface a wall, actually." They ADD finishable surface inside
    # a room and SUBTRACT floor, which is the opposite of how a wall behaves,
    # so a quantity take-off that iterates walls only will under-count.
    # Their own layer so they can be isolated for exactly that reason.
    "V0-VENT-SHAFT": 6,
    # The window frame members. ⚠️ ONLY THE VERTICAL ONES APPEAR HERE: a
    # transom is horizontal, so it exists in elevation and is invisible in
    # plan. O3's transom is recorded in window_frames.csv and deliberately not
    # drawn - a plan that showed it would be lying about what a plan is.
    "V0-WINDOW-FRAME": 4,
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


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.console import utf8_console  # noqa: E402


# ⚠️ THE RECONCILIATION RULES NOW LIVE IN THE COMPILER.
# close_corners, yield_to_reference, close_loggia_loop, snap_near_misses and
# wall_box moved to `resolve_v0_geometry.py` unchanged. They are imported back
# here only so this module's remaining drawing code keeps working; nothing in
# this file may call them to make a geometry decision of its own. The compiler
# is the one place that decides what the geometry IS.
from resolve_v0_geometry import (  # noqa: E402
    LOGGIA_ENCLOSURE, SNAP_MM, close_corners, close_loggia_loop,
    snap_near_misses, wall_box, yield_to_reference)


def rect(msp, layer, x0, y0, x1, y1):
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                       close=True, dxfattribs={"layer": layer})


def main():
    utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=os.path.join(REPO, "data", "cad", "dxf", "v0_developer_layout.dxf"))
    args = ap.parse_args()

    # ⚠️ THE RECONCILIATION NO LONGER HAPPENS HERE. It lives in
    # `resolve_v0_geometry.py`, so the IFC generator and every discipline sheet
    # can read the SAME resolved model instead of re-deriving it or reading this
    # DXF back. This function is now a serialiser: it draws what the compiler
    # resolved and decides nothing about geometry.
    #
    # The rule functions still live in this file during the extraction and the
    # compiler imports them, which is why nothing about their behaviour changed.
    # They move across once both consumers read the resolved model.
    import resolve_v0_geometry

    resolved = resolve_v0_geometry.resolve()
    walls = resolved.walls
    elements = resolved.elements
    placed = json.load(io.open(PLACED, encoding="utf-8"))
    tx = placed["identification_fit_basic_px_to_mm"]

    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4          # millimetres
    for name, colour in LAYERS.items():
        doc.layers.add(name, color=colour, linetype="CONTINUOUS")
    msp = doc.modelspace()

    fixes = resolved.raw["close_corners"]
    loop = resolved.raw["close_loggia_loop"]
    yields = resolved.raw["yield_to_reference"]
    snaps = resolved.raw["snap_near_misses"]
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
        print("   %-5s yielded %.0f mm to %-5s (placed by directive; now %.0f mm drawn)"
              % (wid, lost, ref, now))
    blocks = {r["wall_id"]: r for r in
              csv.DictReader(io.open(_canon("wall_blocks.csv"),
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
    # !! THE WALLS ARE MITRED ON THE GLAZING PLANE TOO, not only the insulation.
    # Owner, 2026-09-15: "M2 and M6b are indeed not squared but inclined - the
    # surface is flush with the glazing and the insulation, this is the cut
    # under one angle and we have one surface." The лоджия face is a splay, so
    # a wall running into it ends on the slope, and an axis-aligned rectangle
    # overshoots by a triangle - about 200 x 55 mm at each of M2 and M6b.
    #
    # Cutting the WALL on the same plane as the insulation is what makes the
    # two read as one surface; mitring only the layer left the block sticking
    # through the glass underneath it.
    gl_clip = None
    if elements.get("loggia_glazing"):
        import math as _mm
        _g = elements["loggia_glazing"]
        _a, _b = _g["axis_from"], _g["axis_to"]
        _L = _mm.hypot(_b[0] - _a[0], _b[1] - _a[1])
        gl_clip = (_a[0], _a[1], -(_b[1] - _a[1]) / _L, (_b[0] - _a[0]) / _L)
    n_wall_mitre = 0
    for w in walls:
        if w.get("face_lo_mm") is None:
            continue
        x0, y0, x1, y1 = wall_box(w)
        loop = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        if gl_clip:
            cut = ru.clip_halfplane(loop, *gl_clip)
            if len(cut) >= 3 and abs(ru._shoelace_area(cut)
                                     - (x1 - x0) * (y1 - y0)) > 1.0:
                loop = cut
                n_wall_mitre += 1
                print("   %-5s MITRED on the glazing plane - %d corners, "
                      "%.0f mm2 cut off"
                      % (w["wall_id"], len(loop),
                         (x1 - x0) * (y1 - y0) - ru._shoelace_area(loop)))
        msp.add_lwpolyline(loop, close=True, dxfattribs={
            "layer": CLASS_LAYER.get(w["class"], "V0-WALL-CONCRETE")})
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
            # !! O9 is DIAGONAL and is drawn by the лоджия glazing block below,
            # which is the only code that knows its rotation. Falling through
            # to the rectangle branch here raised KeyError: 'face_lo_mm' and
            # aborted the whole export - and because the wall report prints
            # BEFORE this point, the run still looked correct on screen while
            # the DXF on disk was the previous one. A crash after the report is
            # the worst place for one.
            if o.get("axis") == "DIAGONAL":
                n_open += 1
                continue
            if o["axis"] == "EW":
                rect(msp, "V0-OPENING", o["from_mm"], o["face_lo_mm"],
                     o["to_mm"], o["face_hi_mm"])
            else:
                rect(msp, "V0-OPENING", o["face_lo_mm"], o["from_mm"],
                     o["face_hi_mm"], o["to_mm"])
            kind = notes.get(o["opening_id"], {}).get("type", "opening")
            # !! from/to are the ALONG axis and face_lo/hi the ACROSS axis, so
            # which is x and which is y depends on the opening's orientation.
            # Feeding them in fixed order put every NS opening's label at
            # (y, x) - O10's landed 5 m outside the flat, in the legend.
            if o["axis"] == "EW":
                cx = (o["from_mm"] + o["to_mm"]) / 2.0
                cy = (o["face_lo_mm"] + o["face_hi_mm"]) / 2.0
            else:
                cx = (o["face_lo_mm"] + o["face_hi_mm"]) / 2.0
                cy = (o["from_mm"] + o["to_mm"]) / 2.0
            msp.add_text("%s %s" % (o["opening_id"], kind), height=70,
                         dxfattribs={"layer": "V0-OPENING"}).set_placement(
                (cx, cy))
            n_open += 1
        omitted = [u["opening_id"] for u in op.get("unplaced", [])]
    print("openings: %d from the vector" % n_open)
    if omitted:
        print("           OMITTED, not guessed: %s" % ", ".join(omitted))

    # --- window frame members, from window_frames.csv -----------------
    # The subdivision is what part 2, the owner's own 3D model, needs: how many
    # sashes, where the mullion falls, whether there is a transom. It comes
    # from photographs, so the PATTERN is evidence and the SIZES are nominal -
    # each row says which is which.
    n_frame = 0
    _wf = _canon("window_frames.csv")
    if os.path.exists(_wf) and os.path.exists(OPENINGS_PLACED):
        _op = {o["opening_id"]: o
               for o in json.load(io.open(OPENINGS_PLACED, encoding="utf-8"))
               .get("openings", [])}
        for r in csv.DictReader(io.open(_wf, encoding="utf-8")):
            if r["axis"] != "vertical":
                continue                      # a transom does not exist in plan
            o = _op.get(r["opening_id"])
            if not o or o.get("axis") not in ("EW", "NS"):
                continue
            t = float(r["member_mm"])
            at = o["from_mm"] + float(r["position"]) * (o["to_mm"] - o["from_mm"])
            a, b = at - t / 2.0, at + t / 2.0
            if o["axis"] == "EW":
                rect(msp, "V0-WINDOW-FRAME", a, o["face_lo_mm"],
                     b, o["face_hi_mm"])
            else:
                rect(msp, "V0-WINDOW-FRAME", o["face_lo_mm"], a,
                     o["face_hi_mm"], b)
            n_frame += 1
            print("frame  %-4s %-10s at %.1f (%.0f mm member)"
                  % (r["opening_id"], r["member"], at, t))
    print("window frame members in PLAN: %d vertical - transoms are recorded "
          "but horizontal, so they belong to elevation" % n_frame)

    # --- the ventilation shafts --------------------------------------
    # !! Drawn from ventilation_shafts.csv, whose footprints are the 4th-floor
    # sub-type read off the BASIC plan. The vector plan under everything else
    # here is the DETAILED one, which draws the floors-10-and-up variant with
    # DOUBLED vent sections - so for these two elements, and only these two,
    # the detailed plan is the wrong sub-type and is deliberately not used.
    # room_schedules.json: "USE THE BASIC PLAN for the vent shafts".
    n_shaft = 0
    if os.path.exists(SHAFTS):
        for r in csv.DictReader(io.open(SHAFTS, encoding="utf-8")):
            x0, y0 = float(r["x0_mm"]), float(r["y0_mm"])
            x1, y1 = float(r["x1_mm"]), float(r["y1_mm"])
            rect(msp, "V0-VENT-SHAFT", x0, y0, x1, y1)
            msp.add_text(r["shaft_id"], height=90,
                         dxfattribs={"layer": "V0-VENT-SHAFT"}).set_placement(
                ((x0 + x1) / 2.0, (y0 + y1) / 2.0))
            n_shaft += 1
            print("shaft %-3s %.0f x %.0f at x %.1f..%.1f  y %.1f..%.1f"
                  % (r["shaft_id"], float(r["width_mm"]), float(r["depth_mm"]),
                     x0, x1, y0, y1))
    print("ventilation shafts: %d (NOT walls - surface added, floor removed)"
          % n_shaft)

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

        # O9 as an OPENING in its own right. Owner, 2026-09-15, arrow on the
        # glazing: *"draw it as another opening."* It was exported only as
        # frame + bays + mullions, so the one element that actually breaks the
        # лоджия enclosure was the only one carrying no opening entity - it did
        # not read as an opening, and a downstream consumer iterating
        # V0-OPENING would not have found the biggest hole in the envelope.
        # Drawn as the full assembly footprint on the opening layer, UNDER the
        # frame and glass so those still read on top.
        band(0.0, gl["run_mm"], "V0-OPENING")
        msp.add_text("O9 glazing", height=70,
                     dxfattribs={"layer": "V0-OPENING"}).set_placement(
            (ax + ux * gl["run_mm"] / 2.0 + nx * d / 2.0,
             ay + uy * gl["run_mm"] / 2.0 + ny * d / 2.0))
        band(0.0, gl["run_mm"], "V0-LOGGIA-FRAME")
        for i, bay in enumerate(gl["bays"], 1):
            band(bay["from_mm"], bay["to_mm"], "V0-LOGGIA-GLAZING")
        for m in gl["mullions"]:
            band(m["from_mm"], m["to_mm"], "V0-LOGGIA-GLAZING")
        print("лоджия glazing: %d bays, %d mullions, run %.1f"
              % (len(gl["bays"]), len(gl["mullions"]), gl["run_mm"]))

    # --- the external insulation band ---
    # Two sources are trusted here and they are named explicitly rather than by
    # negation: the drawing's own evidence, and an OWNER DIRECTIVE. Anything
    # else - notably a band the drawing does not settle and nobody has directed
    # - is skipped, which is the whole point of the guard. Listing the allowed
    # statuses means a new one has to be admitted deliberately; `!= from_drawing`
    # would have admitted it silently.
    TRUSTED_BAND_STATUS = ("from_drawing", "from_owner_directive")
    ins_path = _canon("v0_insulation_placed.json")
    n_ins = 0
    n_directed = 0
    if os.path.exists(ins_path):
        ins = json.load(io.open(ins_path, encoding="utf-8"))
        keep = [b for b in ins.get("bands", [])
                if b.get("status") in TRUSTED_BAND_STATUS]
        n_ins = len(keep)
        n_directed = sum(1 for b in keep
                         if b.get("status") == "from_owner_directive")
        # !! ONE SURFACE, not one rectangle per wall. Owner, 2026-09-15:
        # "one surface means literally one surface." The photo
        # _Survey/IMG_20260913_134256_with_wall_segments.jpg catches the
        # building mid-insulation and settles it: the mineral wool boards turn
        # from M6b's face onto MB's WITHOUT A BREAK and the render closes over
        # them, so the wall boundary underneath is invisible in the finished
        # skin. Drawing a rectangle per wall put a seam in our data that does
        # not exist in the building, and made a take-off iterating surfaces see
        # four where the builder sees one.
        rects = [(b["x0"], b["y0"], b["x1"], b["y1"]) for b in keep]
        comps = ru.groups(rects)
        # !! MITRE ON THE GLAZING PLANE. The лоджия's glazed face is diagonal,
        # so anything built from axis-aligned rectangles overshoots it by a
        # small triangle - about 200 x 55 mm at M2's south-west corner and the
        # same at M6b's. Owner: "here should be a sharp corner, not a square."
        # Cutting on the glazing's own outer plane mitres every run that
        # reaches it, and because it is ONE plane the surface stays continuous
        # across the corner instead of gaining a step of its own.
        gl0 = elements.get("loggia_glazing")
        clip = None
        if gl0:
            import math as _m
            _ax, _ay = gl0["axis_from"]
            _bx, _by = gl0["axis_to"]
            _L = _m.hypot(_bx - _ax, _by - _ay)
            clip = (_ax, _ay, -(_by - _ay) / _L, (_bx - _ax) / _L)
        n_loops, n_mitred = 0, 0
        for comp in comps:
            for loop in ru.union_loops([rects[k] for k in comp]):
                if clip:
                    cut = ru.clip_halfplane(loop, *clip)
                    if len(cut) >= 3 and len(cut) != len(loop):
                        n_mitred += 1
                    loop = cut or loop
                if len(loop) < 3:
                    continue
                msp.add_lwpolyline(loop, close=True,
                                   dxfattribs={"layer": "V0-INSULATION"})
                n_loops += 1
        print("insulation: %d band segment(s) - %d from the drawing's evidence, "
              "%d by owner directive - drawn as %d CONTINUOUS surface(s) in %d "
              "connected run(s)"
              % (n_ins, n_ins - n_directed, n_directed, n_loops, len(comps)))
        if n_mitred:
            print("            %d surface(s) MITRED on the glazing plane - the "
                  "лоджия face is diagonal, so a square end would stub through "
                  "the glass" % n_mitred)
        for comp in comps:
            ids = sorted(set(keep[k]["wall_id"] for k in comp))
            print("            one surface wrapping: %s" % " + ".join(ids))
        for u in ins.get("unresolved", []):
            print("            !! %s SKIPPED - the drawing settles neither "
                  "face and it is not guessed" % u["wall_id"])

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
