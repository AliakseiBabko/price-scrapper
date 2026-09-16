#!/usr/bin/env python3
"""Build the apartment IFC from the GATED geometry, not from a schematic.

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

This reads `data/cad/dxf/v0_developer_layout.dxf` instead - the artefact that
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

    python tools/ifc/model_from_dxf.py --output out.ifc --manifest out.json
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
import dxf_wall_entities  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DXF = REPO / "data" / "cad" / "dxf" / "v0_developer_layout.dxf"
OPENINGS_CSV = REPO / "data" / "canonical" / "wall_openings.csv"
BLOCKS_CSV = REPO / "data" / "canonical" / "wall_blocks.csv"
BUILDING = REPO / "data" / "canonical" / "building_spec.json"

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
    walls_raw, wall_problems = dxf_wall_entities.read_walls(str(DXF))
    if wall_problems:
        raise SystemExit("malformed wall entities in the gated DXF: %r" % wall_problems)

    ents = dxf_entities()
    polys, texts = ents["polys"], ents["texts"]
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
    off_x, off_y = min(xs), min(ys)

    def to_m(points):
        return [(mm(x - off_x), mm(y - off_y)) for x, y in points]

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
        "transform": {
            "units": "DXF millimetres -> IFC metres, divided by 1000",
            "origin_offset_mm": [round(off_x, 1), round(off_y, 1)],
            "note": "every coordinate below is DXF mm minus this offset, over 1000",
        },
        "assumptions": [],
    }

    # ---- walls -------------------------------------------------------------
    wall_objects = {}
    for w in walls_raw:
        meta = wall_meta.get(w["id"], {})
        rect = [(w["x0"], w["y0"]), (w["x1"], w["y0"]), (w["x1"], w["y1"]), (w["x0"], w["y1"])]
        obj = polygon_solid(model, body, storey, owner, "IfcWall", w["id"],
                            to_m(rect), 0.0, h_m)
        add_pset(model, obj, "Pset_ApartmentPhase", {
            "Phase": "existing",
            "WallClass": meta.get("class") or LAYER_CLASS.get(w["layer"], ""),
            "ThicknessMM": meta.get("thickness_mm"),
            "Source": "v0_developer_layout.dxf via dxf_wall_entities",
        })
        wall_objects[w["id"]] = (obj, (w["x0"], w["x1"], w["y0"], w["y1"]))
    manifest["walls"] = len(wall_objects)

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
    shaft_labels = texts.get("V0-VENT-SHAFT", [])
    shafts = 0
    for poly in polys.get("V0-VENT-SHAFT", []):
        name = nearest_label(poly, shaft_labels)
        obj = polygon_solid(model, body, storey, owner, "IfcBuildingElementProxy",
                            "Vent shaft %s" % name, to_m(poly), 0.0, h_m)
        # NOT a wall. The DXF legend says so explicitly, and counting a shaft as
        # wall area would corrupt every finish take-off that reads this model.
        add_pset(model, obj, "Pset_ApartmentPhase",
                 {"Phase": "existing", "Role": "ventilation_shaft", "IsWall": "false"})
        shafts += 1
    manifest["vent_shafts"] = shafts

    # ---- openings, with their measured verticals ---------------------------
    opening_labels = texts.get("V0-OPENING", [])
    openings_built, assumed, lintels, spandrels = [], [], [], []
    for poly in polys.get("V0-OPENING", []):
        label = nearest_label(poly, opening_labels)
        oid = label.split()[0]
        kind = label.split()[1] if len(label.split()) > 1 else "opening"
        rec = opening_table.get(oid, {})

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
            # ⚠️ LINTEL AND SPANDREL. A gap-type opening leaves the wall absent
            # for its WHOLE height, because the DXF is a plan and a plan cannot
            # say that a wall continues over a door head. Built as drawn, every
            # internal doorway ran floor to ceiling - a 450 mm strip of missing
            # wall above each 2050 head under a 2500 ceiling, which is what the
            # owner saw on G4d and G6. The opening footprint IS the wall's own
            # section there, so extruding it above the head rebuilds exactly the
            # material the plan could not express.
            if head < ceiling_mm - 1.0:
                lintel = polygon_solid(model, body, storey, owner, "IfcWall",
                                       "Lintel over %s" % oid, to_m(poly),
                                       mm(head), h_m)
                add_pset(model, lintel, "Pset_ApartmentPhase", {
                    "Phase": "existing", "Role": "lintel_over_opening",
                    "OpeningId": oid,
                    "Source": "reconstructed: the plan cannot express wall over a head",
                })
                lintels.append(oid)
            if sill > 1.0:
                spandrel = polygon_solid(model, body, storey, owner, "IfcWall",
                                         "Spandrel under %s" % oid, to_m(poly),
                                         0.0, mm(sill))
                add_pset(model, spandrel, "Pset_ApartmentPhase", {
                    "Phase": "existing", "Role": "spandrel_under_opening",
                    "OpeningId": oid,
                    "Source": "reconstructed: the plan cannot express wall under a sill",
                })
                spandrels.append(oid)

        # O9 is drawn twice in the DXF - once as an opening on V0-OPENING and
        # again as its bays and mullions on V0-LOGGIA-GLAZING. The bays ARE the
        # glazing, so filling the opening as well puts a second solid in the
        # same place.
        fill_class = None if oid == "O9" else {
            "window": "IfcWindow", "door": "IfcDoor"}.get(kind)
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
                               "sill_mm": sill, "head_mm": head})

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

    loggia = polys.get("V0-LOGGIA-GLAZING", [])
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

    frames = 0
    for poly in polys.get("V0-WINDOW-FRAME", []):
        obj = polygon_solid(model, body, storey, owner, "IfcMember",
                            "Window frame member %d" % (frames + 1), to_m(poly), 0.0, h_m)
        add_pset(model, obj, "Pset_ApartmentOpening",
                 {"Role": "window_frame_mullion", "Source": "window_frames.csv"})
        frames += 1
    manifest["window_frame_members"] = frames

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
