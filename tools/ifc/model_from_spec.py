#!/usr/bin/env python3
"""Build an apartment IFC from a data spec instead of hardcoded geometry.

`tools/ifc/current_apartment_layout.py` builds the existing-state seed from
literals in the script. That is fine for one state and useless for comparing
several, so the same geometry now lives in `data/canonical/current_apartment_base.json`
and this module interprets it. A layout variant is that spec with a patch
applied (see tools/layout/build_variant.py) - which is what makes it possible
to draw two options and put them side by side.

Every wall, opening and fill carries a `phase`: existing / demolished / new.
That is what the demolition and new-partition sheets are drawn from.

Usage:
  python tools/ifc/model_from_spec.py --spec data/canonical/current_apartment_base.json \
      --output out.ifc --manifest out.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import ifcopenshell
import ifcopenshell.api

from poc_renovation import add_owner_history, add_relationship, create_product, extruded_representation, placement

HEIGHT = 2.8


def add_box(model, body, storey, owner, cls, name, x, y, width, depth, height, z=0.0, rotation=0.0):
    item = create_product(model, cls, name, owner)
    item.Representation, _ = extruded_representation(model, body, width, depth, height)
    if abs(float(rotation)) in (90.0, 270.0):
        px, py = float(x) + float(depth) / 2.0, float(y) + float(width) / 2.0
    else:
        px, py = float(x) + float(width) / 2.0, float(y) + float(depth) / 2.0
    item.ObjectPlacement = placement(model, px, py, float(z), float(rotation))
    if cls == "IfcSpace":
        ifcopenshell.api.run("aggregate.assign_object", model, products=[item], relating_object=storey)
    else:
        ifcopenshell.api.run("spatial.assign_container", model, products=[item], relating_structure=storey)
    return item


def add_pset(model, product, name, properties):
    pset = ifcopenshell.api.run("pset.add_pset", model, product=product, name=name)
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset, properties=properties)


def wall_bbox(w: dict) -> tuple[float, float, float, float]:
    t = w["thickness_m"]
    if w["horizontal"]:
        return (w["x_m"], w["y_m"], w["x_m"] + w["length_m"], w["y_m"] + t)
    return (w["x_m"], w["y_m"], w["x_m"] + t, w["y_m"] + w["length_m"])


def room_point(room, side, fraction):
    x, y, w, d = room["x_m"], room["y_m"], room["width_m"], room["depth_m"]
    return {"bottom": (x + w * fraction, y), "top": (x + w * fraction, y + d),
            "left": (x, y + d * fraction), "right": (x + w, y + d * fraction)}[side]


def build(spec: dict, output: Path, manifest_path: Path) -> dict:
    model = ifcopenshell.file(schema="IFC4")
    owner = add_owner_history(model)
    project = create_product(model, "IfcProject", spec.get("name", "Apartment"), owner)
    ifcopenshell.api.run("unit.assign_unit", model,
                         length={"is_metric": True, "raw": "METERS"},
                         area={"is_metric": True, "raw": "SQUARE_METERS"},
                         volume={"is_metric": True, "raw": "CUBIC_METERS"})
    context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body = ifcopenshell.api.run("context.add_context", model, context_type="Model",
                                context_identifier="Body", target_view="MODEL_VIEW", parent=context)
    project.RepresentationContexts = [context]
    site = create_product(model, "IfcSite", "Apartment site", owner)
    building = create_product(model, "IfcBuilding", "Apartment building", owner)
    storey = create_product(model, "IfcBuildingStorey", "Apartment level", owner)
    for parent, child in [(project, site), (site, building), (building, storey)]:
        ifcopenshell.api.run("aggregate.assign_object", model, products=[child], relating_object=parent)

    height = spec.get("storey_height_m", HEIGHT)

    spaces = {}
    for room in spec["rooms"]:
        space = add_box(model, body, storey, owner, "IfcSpace", room["name"],
                        room["x_m"], room["y_m"], room["width_m"], room["depth_m"], 0.02, z=0.01)
        props = {"Source": room.get("source", "spec"), "AreaM2": room["area_m2"],
                 "GeometryStatus": spec.get("status", "planned"), "Role": room.get("role", "")}
        finish = (spec.get("finishes") or {}).get(room["name"])
        if finish:
            props.update({"FloorFinish": finish.get("floor", ""),
                          "WallFinish": finish.get("wall", ""),
                          "CeilingFinish": finish.get("ceiling", ""),
                          "CeilingHeightM": finish.get("ceiling_height_m", 0.0)})
        add_pset(model, space, "Pset_ApartmentSpecEvidence", props)
        spaces[room["name"]] = space

    # Demolished elements are still built, so the demolition sheet can draw
    # what goes away; the phase property is what distinguishes them.
    walls, wall_meta = {}, {}
    for w in spec["walls"]:
        item = add_box(model, body, storey, owner, "IfcWall", w["name"], w["x_m"], w["y_m"],
                       w["length_m"], w["thickness_m"], height,
                       rotation=0.0 if w["horizontal"] else 90.0)
        add_pset(model, item, "Pset_ApartmentPhase",
                 {"Phase": w.get("phase", "existing"), "Kind": w.get("kind", "partition"),
                  "ThicknessMM": round(w["thickness_m"] * 1000)})
        walls[w["name"]] = item
        wall_meta[w["name"]] = {"horizontal": w["horizontal"], "bbox": wall_bbox(w),
                                "phase": w.get("phase", "existing")}

    created = {"door": [], "window": []}
    opening_meta = []
    unhosted = []
    for o in spec["openings"]:
        host = walls.get(o.get("host_wall") or "")
        if host is None:
            # An opening is a gap in the footprint, so CAD-derived ones do not
            # always resolve to a wall. Losing the void is better than losing
            # the model, but it must be visible in the manifest.
            unhosted.append({"opening": o["name"], "host_wall": o.get("host_wall", "")})
            continue
        if o["horizontal"]:
            item = add_box(model, body, storey, owner, "IfcOpeningElement", o["name"],
                           o["x_m"], o["y_m"] - 0.08, o["width_m"], 0.31, o["height_m"], z=o["bottom_m"])
        else:
            item = add_box(model, body, storey, owner, "IfcOpeningElement", o["name"],
                           o["x_m"] - 0.08, o["y_m"], o["width_m"], 0.31, o["height_m"],
                           z=o["bottom_m"], rotation=90.0)
        add_relationship(model, "IfcRelVoidsElement", owner,
                         RelatingBuildingElement=host, RelatedOpeningElement=item)
        add_pset(model, item, "Pset_ApartmentPhase", {"Phase": o.get("phase", "existing"),
                                                      "Kind": o["kind"]})
        created[o["kind"]].append(item)
        opening_meta.append({"host_wall": o["host_wall"],
                             "bbox": (o["x_m"], o["y_m"] - 0.08, o["x_m"] + o["width_m"], o["y_m"] + 0.23)
                             if o["horizontal"] else
                             (o["x_m"] - 0.08, o["y_m"], o["x_m"] + 0.23, o["y_m"] + o["width_m"])})

    for f in spec["fills"]:
        kind = "door" if f["ifc_class"] == "IfcDoor" else "window"
        if not created[kind]:
            raise SystemExit("fill %r has no matching opening left" % f["name"])
        item = add_box(model, body, storey, owner, f["ifc_class"], f["name"], f["x_m"], f["y_m"],
                       f["width_m"], f["depth_m"], f["height_m"], rotation=f["rotation_deg"])
        add_relationship(model, "IfcRelFillsElement", owner,
                         RelatingOpeningElement=created[kind].pop(0), RelatedBuildingElement=item)
        add_pset(model, item, "Pset_ApartmentPhase", {"Phase": f.get("phase", "existing"),
                                                      "Mark": f.get("mark", "")})

    for wall_name, room_names in spec.get("space_boundaries", {}).items():
        if wall_name not in walls:
            continue
        for room_name in room_names:
            if room_name not in spaces:
                continue
            boundary = ifcopenshell.api.run("root.create_entity", model,
                                            ifc_class="IfcRelSpaceBoundary", name="SpecBoundary")
            ifcopenshell.api.run("boundary.edit_attributes", model, entity=boundary,
                                 relating_space=spaces[room_name],
                                 related_building_element=walls[wall_name],
                                 physical_or_virtual="PHYSICAL",
                                 internal_or_external="EXTERNAL"
                                 if wall_meta[wall_name].get("bbox") and "exterior" in wall_name.lower()
                                 or wall_name.startswith("South") else "INTERNAL")

    rooms_by_name = {r["name"]: r for r in spec["rooms"]}

    def snap_to_wall(candidate, side):
        cx, cy = candidate
        best = None
        for wall_name, meta in wall_meta.items():
            if meta["phase"] == "demolished":
                continue  # never hang a socket on a wall that is being removed
            x0, y0, x1, y1 = meta["bbox"]
            if side in {"bottom", "top"} and meta["horizontal"] and x0 - 0.05 <= cx <= x1 + 0.05:
                distance = abs(cy - ((y0 + y1) / 2.0))
                if best is None or distance < best[0]:
                    best = (distance, wall_name, cx, (y0 + y1) / 2.0)
            if side in {"left", "right"} and not meta["horizontal"] and y0 - 0.05 <= cy <= y1 + 0.05:
                distance = abs(cx - ((x0 + x1) / 2.0))
                if best is None or distance < best[0]:
                    best = (distance, wall_name, (x0 + x1) / 2.0, cy)
        return None if best is None else (best[1], best[2], best[3])

    def opening_collision(x, y, wall_name, clearance=0.22):
        for item in opening_meta:
            if item["host_wall"] != wall_name:
                continue
            ox0, oy0, ox1, oy1 = item["bbox"]
            if wall_meta[wall_name]["horizontal"]:
                if ox0 - clearance <= x <= ox1 + clearance:
                    return True
            elif oy0 - clearance <= y <= oy1 + clearance:
                return True
        return False

    skipped = []

    def add_terminal(name, room_name, side, fraction, z, width, depth, pset_name, properties):
        room = rooms_by_name.get(room_name)
        if room is None:
            skipped.append({"name": name, "reason": "room %r not in this variant" % room_name})
            return None
        snapped = snap_to_wall(room_point(room, side, fraction), side)
        if snapped is None:
            skipped.append({"name": name, "reason": "no surviving wall on the %s side" % side})
            return None
        wall_name, sx, sy = snapped
        if opening_collision(sx, sy, wall_name):
            skipped.append({"name": name, "reason": "overlaps an opening on %s" % wall_name})
            return None
        horizontal = wall_meta[wall_name]["horizontal"]
        box_w, box_d = (width, depth) if horizontal else (depth, width)
        terminal = add_box(model, body, storey, owner, "IfcFlowTerminal", name,
                           sx - box_w / 2.0, sy - box_d / 2.0, box_w, box_d, 0.16, z=z)
        enriched = {"Room": room_name, "HostWall": wall_name,
                    "Mounting": "wall_centerline_coordination_symbol",
                    "CoordinationStatus": "conceptual_not_engineered"}
        enriched.update(properties)
        add_pset(model, terminal, pset_name, enriched)
        return terminal

    electrical = []
    for room_name, positions in (spec.get("electrical_plan") or {}).items():
        for index, (side, fraction) in enumerate(positions, 1):
            t = add_terminal("%s outlet %d" % (room_name, index), room_name, side, fraction,
                             1.05, 0.12, 0.04, "Pset_DemoElectricalCoordination",
                             {"DeviceType": "outlet_or_switch_placeholder"})
            if t is not None:
                electrical.append(t)

    plumbing = []
    for p in (spec.get("plumbing_plan") or []):
        t = add_terminal(p["name"], p["room"], p["side"], p["fraction"], 0.65, 0.24, 0.05,
                         "Pset_DemoPlumbingCoordination",
                         {"DeviceType": p["device_type"], "System": p["system"]})
        if t is not None:
            plumbing.append(t)

    lighting = []
    lc = spec.get("lighting") or {}
    for room in spec["rooms"]:
        if room["name"] in (lc.get("exclude_rooms") or []):
            continue
        size = lc.get("size_m", 0.35)
        fixture = add_box(model, body, storey, owner, "IfcLightFixture",
                          "%s ceiling light" % room["name"],
                          room["x_m"] + room["width_m"] / 2.0 - size / 2.0,
                          room["y_m"] + room["depth_m"] / 2.0 - size / 2.0,
                          size, size, 0.05, z=lc.get("z_m", 2.62))
        add_pset(model, fixture, "Pset_DemoLightingCoordination", {
            "Room": room["name"], "Mounting": "ceiling_center_visual_fixture",
            "DeviceType": "ceiling_light_placeholder",
            "TemperatureKelvin": lc.get("temperature_k", 3000),
            "ApproxLumens": lc.get("approx_lumens", 550),
            "Circuit": (spec.get("circuits") or {}).get(room["name"], ""),
            "CoordinationStatus": "visual_scenario_not_lux_validated"})
        lighting.append(fixture)

    furniture = []
    for f in (spec.get("furniture") or []):
        item = add_box(model, body, storey, owner, f.get("ifc_class", "IfcFurniture"), f["name"],
                       f["x_m"], f["y_m"], f["width_m"], f["depth_m"], f.get("height_m", 0.8),
                       rotation=f.get("rotation_deg", 0.0))
        add_pset(model, item, "Pset_ApartmentFurniture",
                 {"Room": f.get("room", ""), "ProductId": f.get("product_id", ""),
                  "Phase": f.get("phase", "new")})
        furniture.append(item)

    s = spec.get("slab")
    if s:
        add_box(model, body, storey, owner, "IfcSlab", s["name"], s["x_m"], s["y_m"],
                s["width_m"], s["depth_m"], s["thickness_m"], z=s["z_m"])

    output.parent.mkdir(parents=True, exist_ok=True)
    model.write(str(output))

    phases = {}
    for w in spec["walls"]:
        phases[w.get("phase", "existing")] = phases.get(w.get("phase", "existing"), 0) + 1

    manifest = {
        "model_type": spec.get("spec_id", "apartment_spec"),
        "spec_id": spec.get("spec_id"),
        "derived_from": spec.get("derived_from"),
        "status": spec.get("status", "planned"),
        "rooms": spec["rooms"],
        "wall_phases": phases,
        "electrical_devices": len(electrical),
        "plumbing_devices": len(plumbing),
        "lighting_fixtures": len(lighting),
        "furniture_items": len(furniture),
        "skipped_services": skipped,
        "unhosted_openings": unhosted,
        "finishes": spec.get("finishes", {}),
        "evidence": spec.get("evidence", {}),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    reopened = ifcopenshell.open(str(output))
    return {"ifc": str(output), "manifest": str(manifest_path),
            "walls": len(reopened.by_type("IfcWall")), "spaces": len(reopened.by_type("IfcSpace")),
            "openings": len(reopened.by_type("IfcOpeningElement")),
            "doors": len(reopened.by_type("IfcDoor")), "windows": len(reopened.by_type("IfcWindow")),
            "flow_terminals": len(reopened.by_type("IfcFlowTerminal")),
            "light_fixtures": len(reopened.by_type("IfcLightFixture")),
            "furniture": len(reopened.by_type("IfcFurniture")),
            "skipped_services": len(skipped), "unhosted_openings": len(unhosted),
            "status": manifest["status"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    a = ap.parse_args()
    spec = json.loads(a.spec.read_text(encoding="utf-8"))
    print(json.dumps(build(spec, a.output, a.manifest), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
