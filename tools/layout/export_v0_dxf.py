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
    "V0-SLAB-EXTENSION": 2,
    "V0-SUGGESTED-FURN": 30,
}
CLASS_LAYER = {
    "concrete": "V0-WALL-CONCRETE",
    "aerated_block": "V0-WALL-AERATED",
    "external": "V0-WALL-EXTERNAL",
    "loggia_enclosure": "V0-WALL-LOGGIA",
}


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
    tx = placed["transform_basic_px_to_mm"]
    elements = json.load(io.open(ELEMENTS, encoding="utf-8"))

    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4          # millimetres
    for name, colour in LAYERS.items():
        lt = "DASHED" if name == "V0-SUGGESTED-FURN" else "CONTINUOUS"
        doc.layers.add(name, color=colour, linetype=lt)
    msp = doc.modelspace()

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

    # --- openings, transformed with the same fit ---------------------
    by_id = {w["wall_id"]: w for w in walls}
    notes = {r["opening_id"]: r for r in csv.DictReader(io.open(OPENINGS, encoding="utf-8"))}
    n_open = 0
    for r in csv.DictReader(io.open(SPANS, encoding="utf-8")):
        w = by_id.get(r["wall_id"])
        if not w or w.get("face_lo_mm") is None:
            continue
        along = tx["x"] if w["axis"] == "EW" else tx["y"]
        a = along["a"] * float(r["span_lo_basic_px"]) + along["b"]
        b = along["a"] * float(r["span_hi_basic_px"]) + along["b"]
        lo, hi = min(a, b), max(a, b)
        if w["axis"] == "EW":
            rect(msp, "V0-OPENING", lo, w["face_lo_mm"], hi, w["face_hi_mm"])
        else:
            rect(msp, "V0-OPENING", w["face_lo_mm"], lo, w["face_hi_mm"], hi)
        kind = notes.get(r["opening_id"], {}).get("type", "opening")
        msp.add_text("%s %s" % (r["opening_id"], kind), height=70,
                     dxfattribs={"layer": "V0-OPENING"}).set_placement(
            ((lo + hi) / 2.0, (w["face_lo_mm"] + w["face_hi_mm"]) / 2.0))
        n_open += 1
    print("openings: %d" % n_open)

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

    # --- suggested furniture ----------------------------------------
    for d in elements.get("dashed_suggested_furniture") or []:
        if d["axis"] == "EW":
            msp.add_line((d["from_mm"], d["line_mm"]), (d["to_mm"], d["line_mm"]),
                         dxfattribs={"layer": "V0-SUGGESTED-FURN"})
        else:
            msp.add_line((d["line_mm"], d["from_mm"]), (d["line_mm"], d["to_mm"]),
                         dxfattribs={"layer": "V0-SUGGESTED-FURN"})
    print("suggested-furniture lines: %d"
          % len(elements.get("dashed_suggested_furniture") or []))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    doc.saveas(args.out)
    print("\nwrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
