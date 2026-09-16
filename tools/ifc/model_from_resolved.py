#!/usr/bin/env python3
"""Build the apartment IFC from the RESOLVED MODEL - no DXF anywhere.

WHY THIS REPLACES `model_from_spec.py` AS THE EXISTING-STATE GENERATOR
---------------------------------------------------------------------
`data/canonical/current_apartment_base.json` was an early reconstruction that
nothing read except the model generator, so no gate ever compared it with
anything. It described the right flat - room areas agree to within 1.4% - with
18 walls against 25, two wall thicknesses assigned by default against five
measured ones, no material classes, no ventilation shafts, a rectangular
лоджия, and openings carrying NO provenance at all: all four windows got the
same 1800 wide / sill 1000 / head 2100, where the gated data records O3
tape-measured at 1763 / 266 / 2251. Retired by the owner 2026-09-16.

It reads `tools/layout/resolve_v0_geometry.py` - the compiler both this and
the DXF serialiser consume, so the two draw the SAME geometry. Until
2026-09-16 this read the DXF back instead, which put 2D between the authored
data and the 3D model and let the reader's bounding-box return silently
un-mitre two walls. Verified to build with the DXF absent.

The gated DXF remains the artefact that
`check_dxf_closure.py`, `raster_fidelity.py`, `check_wall_junctions.py` and
`vector_extent_oracle.py` already assert against the canonical tables and the
source PDF. The 3D model therefore inherits what those gates guarantee, rather
than being a second opinion about the same flat.

Walls come through `tools/layout/dxf_wall_entities.py`, which is THE reader and
refuses anything that is not the rectangle the exporter promises. Verticals come
from `wall_openings.csv`; frame members from `window_frames.csv`; ceiling height
from `building_spec.json`.

EVERY SOLID IS A POLYGON EXTRUDED VERTICALLY, including the axis-aligned ones.
A rectangle-plus-rotation representation cannot express O9 - the лоджия glazing
runs DIAGONALLY, because the лоджия is not rectangular: west side M2 = 1850,
east side M6b 1170 + R8 1490 = 2660, so it splays 810 mm over MA's 2825 and
hypot(2825, 810) = 2939. Using one polygon path for everything means the
diagonal is not a special case that could quietly get a different treatment.

    python tools/ifc/model_from_resolved.py --output out.ifc --manifest out.json
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path

import ifcopenshell
import ifcopenshell.api

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "layout"))

from poc_renovation import add_owner_history, add_relationship, create_product  # noqa: E402
import resolve_v0_geometry  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DXF = REPO / "data" / "cad" / "dxf" / "v0_developer_layout.dxf"
OPENINGS_CSV = REPO / "data" / "canonical" / "wall_openings.csv"
BLOCKS_CSV = REPO / "data" / "canonical" / "wall_blocks.csv"
BUILDING = REPO / "data" / "canonical" / "building_spec.json"

LAYER_FOR_CLASS = {
    "concrete": "V0-WALL-CONCRETE",
    "aerated_block": "V0-WALL-AERATED",
    "external": "V0-WALL-EXTERNAL",
    "loggia_enclosure": "V0-WALL-LOGGIA",
}

LAYER_CLASS = {
    "V0-WALL-CONCRETE": "concrete",
    "V0-WALL-AERATED": "aerated_block",
    "V0-WALL-EXTERNAL": "external",
    "V0-WALL-LOGGIA": "loggia_enclosure",
}

# A door head with no measurement. `wall_openings.csv` carries `2050?` on every
# internal door, derived from one photo of another flat at +/-60 mm. Kept as the
# fallback rather than invented here, and reported as assumed - the developer
# fits no doors, so these are openings the owner specifies later anyway.
DEFAULT_DOOR_HEAD_MM = 2050.0

# A door leaf is not a plug of wall, and a glazing unit is not a reveal. Drawn at
# the opening's full footprint depth, a door reads as nothing but a seam - which
# is what the first build produced. These are ordinary domestic figures; none is
# measured on this flat, and they are appearance only.
DOOR_LEAF_MM = 40.0        # interior leaf
GLAZING_MM = 24.0          # double-glazed unit
FRAME_MM = 70.0            # PVC frame face width, and its depth in the reveal
FRAME_DEPTH_MM = 80.0


def mm(value: float) -> float:
    return float(value) / 1000.0


def parse_mm(raw: str) -> tuple[float | None, bool]:
    """Return (value, certain). A trailing '?' in the canonical data means the
    figure is DERIVED rather than measured, and that distinction is carried into
    the model instead of being rounded away."""
    if raw is None:
        return None, False
    text = raw.strip()
    if not text:
        return None, False
    certain = not text.endswith("?")
    match = re.match(r"^(-?\d+(?:\.\d+)?)", text.rstrip("?"))
    return (float(match.group(1)) if match else None), certain


def resolve_opening(table: dict, oid: str) -> dict:
    """An opening's record, following LEAF suffixes when the id itself is absent.

    The DXF labels one opening `O4`, but `wall_openings.csv` records it as two
    LEAVES of a single unit - O4a, the window leaf on a 735 sill with a radiator
    under it, and O4b, the full-height glass door to the лоджия, divided by a
    frame mullion. `_Survey/apartment_53_mirrored/9db4.jpg` shows exactly that.
    Looking up 'O4' and finding nothing, the first build fell back to a head at
    CEILING height - a 2500 opening where the record says 2235.
    """
    if oid in table:
        rec = dict(table[oid])
        rec["leaves"] = []
        return rec
    leaves = [(k, v) for k, v in table.items()
              if k.startswith(oid) and len(k) == len(oid) + 1 and k[-1].isalpha()]
    if not leaves:
        return {}
    sills = [v["sill_mm"] for _, v in leaves if v["sill_mm"] is not None]
    heads = [v["head_mm"] for _, v in leaves if v["head_mm"] is not None]
    return {
        "type": "combined",
        "wall": leaves[0][1]["wall"],
        "sill_mm": min(sills) if sills else None,
        "sill_measured": all(v["sill_measured"] for _, v in leaves),
        "head_mm": max(heads) if heads else None,
        "head_measured": all(v["head_measured"] for _, v in leaves),
        "leaves": [{"id": k, **v} for k, v in sorted(leaves)],
    }


def read_openings_table() -> dict:
    out = {}
    with OPENINGS_CSV.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            oid = (row["opening_id"] or "").strip()
            if not oid:
                continue
            sill, sill_ok = parse_mm(row.get("sill_height_mm"))
            head, head_ok = parse_mm(row.get("head_height_mm"))
            out[oid] = {
                "type": (row.get("type") or "").strip(),
                "wall": (row.get("in_wall_or_divider") or "").strip(),
                "width_mm": (row.get("width_mm") or "").strip(),
                "sill_mm": sill, "sill_measured": sill_ok,
                "head_mm": head, "head_measured": head_ok,
            }
    return out


def read_wall_classes() -> dict:
    out = {}
    with BLOCKS_CSV.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            out[row["wall_id"]] = {
                "class": row.get("class", ""),
                "thickness_mm": float(row["thickness_mm"]) if row.get("thickness_mm") else None,
            }
    return out


def dxf_entities() -> dict:
    """Polylines and labels by layer, straight from the gated DXF."""
    import ezdxf

    doc = ezdxf.readfile(str(DXF))
    msp = doc.modelspace()
    polys: dict[str, list] = {}
    texts: dict[str, list] = {}
    for entity in msp:
        layer = entity.dxf.layer
        if entity.dxftype() == "LWPOLYLINE":
            polys.setdefault(layer, []).append(
                [(float(p[0]), float(p[1])) for p in entity.get_points()])
        elif entity.dxftype() == "TEXT":
            texts.setdefault(layer, []).append(
                (entity.dxf.text, float(entity.dxf.insert.x), float(entity.dxf.insert.y)))
    return {"polys": polys, "texts": texts}


def centroid(points) -> tuple[float, float]:
    return (sum(p[0] for p in points) / len(points),
            sum(p[1] for p in points) / len(points))


def nearest_label(points, labels) -> str:
    cx, cy = centroid(points)
    if not labels:
        return "?"
    return min(labels, key=lambda t: (t[1] - cx) ** 2 + (t[2] - cy) ** 2)[0]


def shrink_across(points, target_mm: float):
    """Thin a 4-point footprint across its SHORT axis, about its centre.

    A door leaf is not as thick as the wall it hangs in, and a glazing unit is
    not as thick as the reveal. The DXF footprint of an opening is the full wall
    depth, so using it directly draws a door as a plug of wall - which is what
    the first build did, and why doors read as nothing but a seam in the wall.

    Works on the polygon's own edge directions rather than on X and Y, so the
    diagonal лоджия elements thin correctly too.
    """
    if len(points) != 4:
        return points
    (p0, p1, p2, _p3) = points
    e0 = (p1[0] - p0[0], p1[1] - p0[1])
    e1 = (p2[0] - p1[0], p2[1] - p1[1])
    len0, len1 = math.hypot(*e0), math.hypot(*e1)
    short, current = (e0, len0) if len0 < len1 else (e1, len1)
    if current <= 0 or target_mm >= current:
        return points
    ux, uy = short[0] / current, short[1] / current
    cx, cy = centroid(points)
    half = target_mm / 2.0
    out = []
    for x, y in points:
        # distance of this corner from the centre along the short axis
        d = (x - cx) * ux + (y - cy) * uy
        keep = half if d > 0 else -half
        out.append((x - d * ux + keep * ux, y - d * uy + keep * uy))
    return out


def slice_along(points, t0: float, t1: float):
    """The sub-rectangle between two fractions along the footprint's LONG axis.

    Used to cut a window's jambs, head bar and sill bar out of the one opening
    footprint, so every part of the frame is positioned by the measured opening
    rather than by a second set of numbers that could drift from it.
    """
    if len(points) != 4:
        return points
    (p0, p1, p2, p3) = points
    e0 = math.dist(p0, p1)
    e1 = math.dist(p1, p2)
    if e0 >= e1:
        a, b, c, d = p0, p1, p2, p3      # long edge is p0->p1
    else:
        a, b, c, d = p1, p2, p3, p0      # long edge is p1->p2
    def lerp(u, v, t):
        return (u[0] + (v[0] - u[0]) * t, u[1] + (v[1] - u[1]) * t)
    return [lerp(a, b, t0), lerp(a, b, t1), lerp(d, c, t1), lerp(d, c, t0)]


def polygon_solid(model, body, storey, owner, cls, name, points_m, z0_m, z1_m):
    """One arbitrary polygon, extruded vertically. Used for EVERY solid.

    Axis-aligned and diagonal elements take the same path deliberately: see the
    module docstring - O9 cannot be expressed as a rectangle plus a rotation,
    and a second code path for it is a second thing to get wrong.
    """
    height = z1_m - z0_m
    pts = list(points_m)
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    ifc_points = [model.create_entity("IfcCartesianPoint", Coordinates=(float(x), float(y)))
                  for x, y in pts]
    polyline = model.create_entity("IfcPolyline", Points=ifc_points)
    profile = model.create_entity("IfcArbitraryClosedProfileDef",
                                  ProfileType="AREA", OuterCurve=polyline)
    solid = model.create_entity(
        "IfcExtrudedAreaSolid",
        SweptArea=profile,
        Position=model.create_entity(
            "IfcAxis2Placement3D",
            Location=model.create_entity("IfcCartesianPoint", Coordinates=(0.0, 0.0, float(z0_m)))),
        ExtrudedDirection=model.create_entity("IfcDirection", DirectionRatios=(0.0, 0.0, 1.0)),
        Depth=float(height),
    )
    shape = model.create_entity("IfcShapeRepresentation", ContextOfItems=body,
                                RepresentationIdentifier="Body",
                                RepresentationType="SweptSolid", Items=[solid])
    product = create_product(model, cls, name, owner)
    product.Representation = model.create_entity("IfcProductDefinitionShape",
                                                 Representations=[shape])
    product.ObjectPlacement = model.create_entity(
        "IfcLocalPlacement",
        RelativePlacement=model.create_entity(
            "IfcAxis2Placement3D",
            Location=model.create_entity("IfcCartesianPoint", Coordinates=(0.0, 0.0, 0.0))))
    if cls == "IfcSpace":
        ifcopenshell.api.run("aggregate.assign_object", model,
                             products=[product], relating_object=storey)
    elif cls != "IfcOpeningElement":
        ifcopenshell.api.run("spatial.assign_container", model,
                             products=[product], relating_structure=storey)
    return product


def add_pset(model, product, name, properties):
    pset = ifcopenshell.api.run("pset.add_pset", model, product=product, name=name)
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset,
                         properties={k: v for k, v in properties.items() if v is not None})


def rect_contains(outer, inner, tol=1.0) -> bool:
    ox0, ox1, oy0, oy1 = outer
    xs = [p[0] for p in inner]
    ys = [p[1] for p in inner]
    return (min(xs) >= ox0 - tol and max(xs) <= ox1 + tol
            and min(ys) >= oy0 - tol and max(ys) <= oy1 + tol)


def build(output: Path, manifest_path: Path) -> dict:
    # ⚠️ NO LONGER READS THE DXF. Walls, their exact body polygons, openings,
    # shafts, frame members and лоджия bays all come from the compiler, which is
    # the same resolved model the DXF serialiser draws. While this read the DXF,
    # 2D sat between the authored data and the 3D model, and the reader's
    # bounding-box return silently un-mitred two walls.
    resolved = resolve_v0_geometry.resolve()
    walls_raw = [{"id": w["wall_id"],
                  "layer": LAYER_FOR_CLASS.get(w["class"], "V0-WALL-CONCRETE"),
                  "polygon": resolved.plan_polygons.get(w["wall_id"]),
                  "body": resolved.body_polygons.get(w["wall_id"])}
                 for w in resolved.walls if w.get("from_mm") is not None]
    for w, src in zip(walls_raw, [x for x in resolved.walls if x.get("from_mm") is not None]):
        bx = resolve_v0_geometry.wall_box(src)
        w["x0"], w["y0"], w["x1"], w["y1"] = bx[0], bx[1], bx[2], bx[3]
    opening_table = read_openings_table()
    wall_meta = read_wall_classes()
    building = json.loads(BUILDING.read_text(encoding="utf-8"))
    ceiling_mm = float(building["ceiling_height_mm"]["this_flat"])

    # ONE stated transform, recorded in the manifest. The gated data is in
    # millimetres on the drawing's own origin (x ~ 2930..12946, y ~ 6120..16240);
    # the IFC is metres from zero. Getting this wrong is silent, so it is
    # computed once here and written down.
    xs = [v for w in walls_raw for v in (w["x0"], w["x1"])]
    ys = [v for w in walls_raw for v in (w["y0"], w["y1"])]
    # ⚠️ THE COMPILER'S PUBLISHED FRAME, not an offset computed here. Taking
    # min() over whatever geometry this generator happens to load would let an
    # element outside the wall envelope - insulation, a service, a variant
    # primitive - translate the whole model, so every previously issued IFC and
    # every annotation against it would refer to a different place while still
    # loading cleanly. The datum is the base-wall envelope and it is gated.
    frame = resolved.frame
    off_x, off_y = frame.origin_mm

    def to_m(points):
        return [frame.drawing_to_model(p) for p in points]

    model = ifcopenshell.file(schema="IFC4")
    owner = add_owner_history(model)
    project = create_product(model, "IfcProject", "Current apartment (v0 existing)", owner)
    ifcopenshell.api.run("unit.assign_unit", model,
                         length={"is_metric": True, "raw": "METERS"},
                         area={"is_metric": True, "raw": "SQUARE_METERS"},
                         volume={"is_metric": True, "raw": "CUBIC_METERS"})
    context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body = ifcopenshell.api.run("context.add_context", model, context_type="Model",
                                context_identifier="Body", target_view="MODEL_VIEW",
                                parent=context)
    project.RepresentationContexts = [context]
    site = create_product(model, "IfcSite", "Apartment site", owner)
    building_p = create_product(model, "IfcBuilding", "Apartment building", owner)
    storey = create_product(model, "IfcBuildingStorey", "Apartment level", owner)
    for parent, child in [(project, site), (site, building_p), (building_p, storey)]:
        ifcopenshell.api.run("aggregate.assign_object", model,
                             products=[child], relating_object=parent)

    h_m = mm(ceiling_mm)
    manifest: dict = {
        "source_dxf": str(DXF.relative_to(REPO)).replace("\\", "/"),
        "ceiling_height_mm": ceiling_mm,
        "transform": resolved.report["coordinate_frame"],
        "opening_counts": resolved.report["opening_counts"],
        "assumptions": [],
    }

    # ---- walls -------------------------------------------------------------
    # ⚠️ THERE ARE NO STRUCTURAL LINTELS IN THIS FLAT, and the model must not
    # invent one. Owner, 2026-09-16: an opening is just a big opening, and
    # everything visible in it is the window or door joinery - no concrete or
    # other hard lintel over it. wall_blocks.csv agrees about what these walls
    # are: G4d is 120 mm aerated block and G6 is 75 mm, thin partitions where
    # the block simply continues over the doorway.
    #
    # So where the DXF draws a wall as STOPPING at a doorway - because a plan
    # shows the gap and cannot show the material above it - the wall is EXTENDED
    # across the opening here and the opening is cut out of it as a void. The
    # result is one continuous wall, exactly as built, instead of the separate
    # "Lintel over O5/O6" blocks the previous build bolted on. Those blocks were
    # my invention: they named a structural element that does not exist.
    #
    # The consequence for take-off is the point of the change: the material over
    # a door now belongs to the wall it is part of, and any query over that wall
    # picks it up without knowing about openings at all.
    # The compiler decides which openings the plan draws as a GAP and therefore
    # which walls extend across them - it publishes the body polygon directly,
    # so this generator no longer computes an extension of its own.
    extensions: dict[str, list] = {}
    for rec_o in resolved.openings:
        if rec_o.get("hosting") == "gap_between_walls" and rec_o.get("host_wall"):
            extensions.setdefault(rec_o["host_wall"], []).append(
                (rec_o["opening_id"], rec_o["polygon"]))

    wall_objects = {}
    for w in walls_raw:
        meta = wall_meta.get(w["id"], {})
        x0, x1, y0, y1 = w["x0"], w["x1"], w["y0"], w["y1"]
        for oid, poly in extensions.get(w["id"], []):
            x0 = min(x0, min(p[0] for p in poly))
            x1 = max(x1, max(p[0] for p in poly))
            y0 = min(y0, min(p[1] for p in poly))
            y1 = max(y1, max(p[1] for p in poly))
        # ⚠️ THE WALL'S OWN POLYGON, not a rectangle rebuilt from its bounding
        # box. M2 and M6b are MITRED on the лоджия glazing plane - the owner:
        # "not squared but inclined... the cut under one angle and we have one
        # surface". Rebuilding from min/max silently restored 5,710 mm2 on M2
        # and 5,707 mm2 on M6b and pushed both walls back through the glazing.
        #
        # THE BODY footprint is the plan polygon EXTENDED across any doorway the
        # plan draws the wall as stopping at, because the block continues over a
        # door head and a plan cannot say so. Where nothing is extended the two
        # are the same polygon; where something is, the extension is a rectangle
        # spanning the opening and the mitre is untouched, since no opening and
        # no mitre occur on the same wall.
        # THE COMPILER'S BODY POLYGON. It already unions the plan polygon with
        # any doorway extension, and RAISES if a wall is both mitred and
        # extended rather than silently choosing one - the earlier
        # "extended rectangle if extension else mitred polygon" was right only
        # because no wall has both today.
        body_poly = w.get("body") or w.get("polygon")
        obj = polygon_solid(model, body, storey, owner, "IfcWall", w["id"],
                            to_m(body_poly), 0.0, h_m)
        add_pset(model, obj, "Pset_ApartmentPhase", {
            "Phase": "existing",
            "WallClass": meta.get("class") or LAYER_CLASS.get(w["layer"], ""),
            "ThicknessMM": meta.get("thickness_mm"),
            "Source": "v0_developer_layout.dxf via dxf_wall_entities",
        })
        wall_objects[w["id"]] = (obj, (x0, x1, y0, y1))
    manifest["walls"] = len(wall_objects)
    manifest["walls_extended_across_openings"] = {
        wid: [oid for oid, _ in items] for wid, items in extensions.items()}

    # ---- floor and ceiling slabs -------------------------------------------
    # ⚠️ A BOUNDING RECTANGLE, and that is an approximation this model states
    # rather than hides. The flat's true outline is not rectangular - the лоджия
    # juts and the plan carries a 1800x370 slab extension - so these two slabs
    # cover a little more than the real floor plate. They exist because a 3D
    # view with no floor is unreadable and the walkable view needs something to
    # stand on. NOTHING should take an area off them: room areas come from
    # room_schedules.json and finish areas from room_rollouts.csv, both of which
    # are measured. Recorded in `assumptions` so it cannot be forgotten.
    floor_rect = [(min(xs), min(ys)), (max(xs), min(ys)),
                  (max(xs), max(ys)), (min(xs), max(ys))]
    slab_t = 0.12
    polygon_solid(model, body, storey, owner, "IfcSlab", "Floor slab",
                  to_m(floor_rect), -slab_t, 0.0)
    polygon_solid(model, body, storey, owner, "IfcSlab", "Ceiling slab",
                  to_m(floor_rect), h_m, h_m + slab_t)
    manifest["slabs"] = 2
    manifest["assumptions"].append({
        "element": "Floor and ceiling slabs",
        "assumed": "rectangular, the bounding box of all walls (%.2f x %.2f m)"
                   % (mm(max(xs) - min(xs)), mm(max(ys) - min(ys))),
        "why": "the flat outline is NOT rectangular - the лоджия juts and the plan "
               "carries an 1800x370 slab extension. Present so the 3D view has a "
               "floor; NOT an area source. Use room_schedules.json / room_rollouts.csv.",
    })

    # ---- ventilation shafts -----------------------------------------------
    shafts = 0
    for rec_s in resolved.shafts:
        poly = rec_s["polygon"]
        name = rec_s["shaft_id"]
        obj = polygon_solid(model, body, storey, owner, "IfcBuildingElementProxy",
                            "Vent shaft %s" % name, to_m(poly), 0.0, h_m)
        # NOT a wall. The DXF legend says so explicitly, and counting a shaft as
        # wall area would corrupt every finish take-off that reads this model.
        add_pset(model, obj, "Pset_ApartmentPhase",
                 {"Phase": "existing", "Role": "ventilation_shaft", "IsWall": "false"})
        shafts += 1
    manifest["vent_shafts"] = shafts

    # ---- openings, with their measured verticals ---------------------------
    openings_built, assumed, lintels, spandrels = [], [], [], []
    for rec_o in resolved.openings:
        poly = rec_o["polygon"]
        if not poly:
            continue
        oid = rec_o["opening_id"]
        kind = rec_o["kind"]
        label = "%s %s" % (oid, kind)
        rec = resolve_opening(opening_table, oid)

        sill = rec.get("sill_mm")
        head = rec.get("head_mm")
        if sill is None:
            sill = 0.0
        if head is None:
            head = DEFAULT_DOOR_HEAD_MM if kind == "door" else ceiling_mm
            assumed.append({"opening": oid, "field": "head_mm", "value": head,
                            "why": "no head recorded in wall_openings.csv"})
        if not rec.get("sill_measured", False) and rec.get("sill_mm") is not None:
            assumed.append({"opening": oid, "field": "sill_mm", "value": sill,
                            "why": "recorded DERIVED (trailing ?) in wall_openings.csv"})
        if not rec.get("head_measured", False) and rec.get("head_mm") is not None:
            assumed.append({"opening": oid, "field": "head_mm", "value": head,
                            "why": "recorded DERIVED (trailing ?) in wall_openings.csv"})

        # TWO HOSTING MODELS, and the DXF uses both. A window is a VOID inside a
        # continuous wall - O2 sits wholly within MB. An interior doorway is a
        # GAP BETWEEN wall segments: G4d runs x 3230.9..5146.0 and O6 runs
        # 5146.0..6056.0, meeting exactly at 5146.0, so the wall already stops at
        # the opening and there is nothing to subtract. Cutting a void there
        # would remove material that was never drawn. Treating the gap case as a
        # failure - which the first run did, reporting O5 and O6 as "unhosted" -
        # gets the model right and the diagnosis wrong.
        host_id = None
        for wid, (_, rect) in wall_objects.items():
            if rect_contains(rect, poly):
                host_id = wid
                break

        if host_id:
            void = polygon_solid(model, body, storey, owner, "IfcOpeningElement",
                                 label, to_m(poly), mm(sill), mm(head))
            add_relationship(model, "IfcRelVoidsElement", owner,
                             RelatingBuildingElement=wall_objects[host_id][0],
                             RelatedOpeningElement=void)
            hosting = "void_in_wall"
        else:
            void = None
            hosting = "gap_between_walls"
            # Nothing is added here. An opening that still has no host wall
            # spans BETWEEN elements rather than sitting in one - O10 passes
            # through the V2/R5 divider, O9 runs diagonally from M2 to M6b - and
            # both are full height, so there is no material over them to model.
            # Openings inside a wall were made continuous before the walls were
            # built; see the extension note above.
            pass

        # O9 is drawn twice in the DXF - once as an opening on V0-OPENING and
        # again as its bays and mullions on V0-LOGGIA-GLAZING. The bays ARE the
        # glazing, so filling the opening as well puts a second solid in the
        # same place.
        fill_class = None if oid == "O9" else {
            "window": "IfcWindow", "door": "IfcDoor"}.get(kind)

        # A COMBINED UNIT IS GLAZED PER LEAF, because its leaves do not share a
        # sill. O4 is one 1380 opening holding a window leaf on a 735 sill with
        # a radiator under it and a full-height glass door beside it, divided by
        # a frame mullion - see _Survey/apartment_53_mirrored/9db4.jpg. Glazing
        # it as one pane from the unit's lowest sill would put glass across the
        # solid wall under the window leaf.
        if rec.get("leaves"):
            widths = [(l, abs(parse_mm(str(l.get("width_mm", "") or "0"))[0] or 0.0))
                      for l in rec["leaves"]]
            total = sum(w for _, w in widths) or 1.0
            t = 0.0
            for leaf, width in widths:
                frac = width / total
                seg = slice_along(shrink_across(poly, GLAZING_MM), t, min(t + frac, 1.0))
                l_sill = leaf["sill_mm"] if leaf["sill_mm"] is not None else sill
                l_head = leaf["head_mm"] if leaf["head_mm"] is not None else head
                cls = "IfcDoor" if leaf["type"] == "door" else "IfcWindow"
                pane = polygon_solid(model, body, storey, owner, cls,
                                     "%s %s" % (leaf["id"], leaf["type"]),
                                     to_m(seg), mm(l_sill), mm(l_head))
                add_pset(model, pane, "Pset_ApartmentOpening", {
                    "OpeningId": leaf["id"], "PartOfUnit": oid,
                    "SillMM": l_sill, "SillMeasured": str(bool(leaf["sill_measured"])),
                    "HeadMM": l_head, "HeadMeasured": str(bool(leaf["head_measured"])),
                    "Source": "wall_openings.csv leaf record",
                })
                t += frac
            fill_class = None       # the leaves ARE the fill

        if fill_class == "IfcWindow":
            # A FRAME PLUS GLASS, not one slab. Every part is cut out of the same
            # measured opening footprint, so the frame cannot drift from the
            # opening the way a second set of numbers would.
            span = max(math.dist(poly[0], poly[1]), math.dist(poly[1], poly[2]))
            f = min(FRAME_MM / span, 0.45) if span else 0.0
            frame_poly = shrink_across(poly, FRAME_DEPTH_MM)
            glass_poly = shrink_across(poly, GLAZING_MM)
            for tag, pts, z0, z1 in [
                ("jamb L", slice_along(frame_poly, 0.0, f), sill, head),
                ("jamb R", slice_along(frame_poly, 1.0 - f, 1.0), sill, head),
                ("head", slice_along(frame_poly, f, 1.0 - f), head - FRAME_MM, head),
                ("sill", slice_along(frame_poly, f, 1.0 - f), sill, sill + FRAME_MM),
            ]:
                member = polygon_solid(model, body, storey, owner, "IfcMember",
                                       "%s frame %s" % (oid, tag), to_m(pts),
                                       mm(z0), mm(z1))
                add_pset(model, member, "Pset_ApartmentOpening",
                         {"OpeningId": oid, "Role": "window_frame_%s" % tag.split()[0],
                          "Source": "geometry from the opening footprint; profile sizes are APPEARANCE"})
            fill = polygon_solid(model, body, storey, owner, "IfcWindow",
                                 "%s %s" % (oid, kind),
                                 to_m(slice_along(glass_poly, f, 1.0 - f)),
                                 mm(sill + FRAME_MM), mm(head - FRAME_MM))
        elif fill_class:
            fill = polygon_solid(model, body, storey, owner, fill_class,
                                 "%s %s" % (oid, kind),
                                 to_m(shrink_across(poly, DOOR_LEAF_MM)),
                                 mm(sill), mm(head))
            if void is not None:
                add_relationship(model, "IfcRelFillsElement", owner,
                                 RelatingOpeningElement=void, RelatedBuildingElement=fill)
            add_pset(model, fill, "Pset_ApartmentOpening", {
                "OpeningId": oid,
                "SillMM": sill, "SillMeasured": str(bool(rec.get("sill_measured"))),
                "HeadMM": head, "HeadMeasured": str(bool(rec.get("head_measured"))),
                "HostingModel": hosting,
                "RecordedWall": rec.get("wall", ""),
                "Source": "wall_openings.csv",
            })
        openings_built.append({"id": oid, "kind": kind, "host": host_id,
                               "hosting": hosting,
                               "recorded_wall": rec.get("wall", ""),
                               "sill_mm": sill, "head_mm": head,
                               "leaves": [l["id"] for l in rec.get("leaves", [])],
                               "bbox": (min(p[0] for p in poly), max(p[0] for p in poly),
                                        min(p[1] for p in poly), max(p[1] for p in poly))})

    manifest["openings"] = openings_built
    manifest["lintels_added"] = lintels
    manifest["spandrels_added"] = spandrels
    manifest["hosting_counts"] = {
        "void_in_wall": sum(1 for o in openings_built if o["hosting"] == "void_in_wall"),
        "gap_between_walls": sum(1 for o in openings_built if o["hosting"] == "gap_between_walls"),
    }

    # ---- лоджия glazing bays and frame members -----------------------------
    # The DXF draws 4 bays and 3 mullions. THE BAY COUNT IS AN ASSUMPTION, not a
    # measurement: the pattern - full height, no parapet, one transom at ~1000,
    # vertical bays - is confirmed from a handover photo, but that photo is flat
    # 109, whose лоджия is 2.5 m2 against our 6.05, and wall_openings.csv states
    # that "the PATTERN transfers and the bay count and widths do not".
    # The layer carries BOTH the bays and the mullions between them - 7 polygons
    # for 4 bays and 3 mullions. Separated by their long edge (~650 mm against
    # ~48 mm) rather than by index, so a redraw with a different bay count still
    # classifies correctly.
    def long_edge(points) -> float:
        return max(math.dist(points[i], points[(i + 1) % len(points)])
                   for i in range(len(points)))

    loggia = [b["polygon"] for b in resolved.loggia_bays]
    threshold = (max((long_edge(p) for p in loggia), default=0.0) / 3.0) if loggia else 0.0
    bays = mullions = 0
    for poly in loggia:
        is_bay = long_edge(poly) >= threshold
        if is_bay:
            bays += 1
            name, role = "Loggia glazing bay %d" % bays, "loggia_glazing_bay"
        else:
            mullions += 1
            name, role = "Loggia glazing mullion %d" % mullions, "loggia_glazing_mullion"
        obj = polygon_solid(model, body, storey, owner, "IfcPlate", name,
                            to_m(poly), 0.0, h_m)
        add_pset(model, obj, "Pset_ApartmentOpening", {
            "OpeningId": "O9", "Role": role,
            "BayCountBasis": "ASSUMED from the DXF; pattern from flat 109, bay count NOT transferable",
            "WidthBasis": "O9 width 2939 DERIVED, corroborated to 9 mm by flat 53's printed 2.93 m",
        })
    glazing = bays
    manifest["loggia_glazing_bays"] = bays
    manifest["loggia_glazing_mullions"] = mullions
    if glazing:
        manifest["assumptions"].append({
            "element": "O9 loggia glazing",
            "assumed": "bay count and bay widths (%d bays drawn)" % glazing,
            "why": "pattern confirmed from flat 109 (2.5 m2 loggia vs our 6.05); "
                   "wall_openings.csv states the bay count and widths do NOT transfer",
        })
        manifest["assumptions"].append({
            "element": "O9 loggia glazing",
            "assumed": "single vs double glazing is UNKNOWN",
            "why": "wall_openings.csv flags it; a dark aluminium loggia frame is often "
                   "cold single glazing, which changes the thermal case completely",
        })

    # ⚠️ A MULLION SPANS ITS OPENING, NOT THE STOREY. Extruded 0 to ceiling,
    # these read as full-height posts standing in front of each window and
    # carrying on past its head - which is what the owner saw, and nothing like
    # the real units in IMG_20260913_133523.jpg or 9db4.jpg. The mullion is a
    # member INSIDE a frame, so it takes the vertical extent of the opening
    # whose footprint contains it.
    frames, orphan_mullions = 0, 0
    # ⚠️ EVERY member, including the HORIZONTAL transom. Filtering on
    # "has a plan footprint" dropped O3's transom from the 3D model - a member
    # the compiler had resolved, recorded in window_frames.csv as position 0.44
    # of the opening height, which makes O3 the 2x2 unit the facade photo shows.
    # A plan consumer filters it; the IFC has no reason to.
    for rec_f in resolved.window_frames:
        poly = rec_f["polygon"]
        if not poly:
            continue
        cx, cy = centroid(poly)
        owner_open = None
        for rec in openings_built:
            ox0, ox1, oy0, oy1 = rec["bbox"]
            if ox0 - 1.0 <= cx <= ox1 + 1.0 and oy0 - 1.0 <= cy <= oy1 + 1.0:
                owner_open = rec
                break
        if owner_open is None:
            orphan_mullions += 1
            continue
        frames += 1
        vertical = rec_f["axis"] == "vertical"
        role = "window_frame_mullion" if vertical else "window_frame_transom"
        z0 = rec_f.get("z_from_mm")
        z1 = rec_f.get("z_to_mm")
        if z0 is None or z1 is None:
            z0, z1 = owner_open["sill_mm"], owner_open["head_mm"]
        member = polygon_solid(
            model, body, storey, owner, "IfcMember",
            "%s frame %s" % (rec_f["opening_id"], rec_f["member"]),
            to_m(shrink_across(poly, FRAME_DEPTH_MM)), mm(z0), mm(z1))
        add_pset(model, member, "Pset_ApartmentOpening", {
            "OpeningId": rec_f["opening_id"], "Role": role,
            "Member": rec_f["member"], "Axis": rec_f["axis"],
            "HasPlanFootprint": str(bool(rec_f.get("has_plan_footprint"))),
            "Source": "window_frames.csv; opening-local 3D extent",
        })
    manifest["window_frame_members"] = frames
    if orphan_mullions:
        manifest["assumptions"].append({
            "element": "window frame mullions",
            "assumed": "%d mullion(s) matched no opening and were DROPPED" % orphan_mullions,
            "why": "a mullion outside every opening footprint cannot be placed vertically",
        })

    manifest["assumptions"].extend(assumed)

    output.parent.mkdir(parents=True, exist_ok=True)
    model.write(str(output))
    manifest["ifc"] = str(output)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path,
                    default=REPO / "data" / "outputs" / "variants" / "v0-existing" / "model.ifc")
    ap.add_argument("--manifest", type=Path,
                    default=REPO / "data" / "outputs" / "variants" / "v0-existing" / "model.json")
    a = ap.parse_args()
    m = build(a.output, a.manifest)
    print("walls %d, vent shafts %d, openings %d, loggia bays %d, frame members %d"
          % (m["walls"], m["vent_shafts"], len(m["openings"]),
             m["loggia_glazing_bays"], m["window_frame_members"]))
    if False:
        pass
    print("assumptions carried: %d (see the manifest)" % len(m["assumptions"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
