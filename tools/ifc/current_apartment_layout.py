"""Generate a first current-apartment IFC seed from visual-plan evidence.

This is a planned geometry seed, not an as-built model. The primary dimensions
come from the current detailed plan image, with comparable measured plans used
only as calibration evidence for uncertain spans such as entrance-hall depth.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ifcopenshell
import ifcopenshell.api

from poc_renovation import add_owner_history, add_relationship, create_product, extruded_representation, placement


WALL_T = 0.15
EXT_T = 0.25
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


def wall(model, body, storey, owner, name, x, y, length, horizontal, thickness=WALL_T):
    return add_box(model, body, storey, owner, "IfcWall", name, x, y, length, thickness, HEIGHT, rotation=0.0 if horizontal else 90.0)


def opening(model, body, storey, owner, host, name, x, y, width, horizontal, bottom, height, kind, created):
    if horizontal:
        item = add_box(model, body, storey, owner, "IfcOpeningElement", name, x, y - 0.08, width, 0.31, height, z=bottom)
    else:
        item = add_box(model, body, storey, owner, "IfcOpeningElement", name, x - 0.08, y, width, 0.31, height, z=bottom, rotation=90.0)
    add_relationship(model, "IfcRelVoidsElement", owner, RelatingBuildingElement=host, RelatedOpeningElement=item)
    created[kind].append(item)
    return item


def add_fill(model, body, storey, owner, cls, name, x, y, width, depth, height, rotation, openings):
    fill = add_box(model, body, storey, owner, cls, name, x, y, width, depth, height, rotation=rotation)
    opening_item = openings.pop(0)
    add_relationship(model, "IfcRelFillsElement", owner, RelatingOpeningElement=opening_item, RelatedBuildingElement=fill)
    return fill


def add_pset(model, product, name, properties):
    pset = ifcopenshell.api.run("pset.add_pset", model, product=product, name=name)
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset, properties=properties)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    model = ifcopenshell.file(schema="IFC4")
    owner = add_owner_history(model)
    project = create_product(model, "IfcProject", "Current apartment planned seed", owner)
    ifcopenshell.api.run("unit.assign_unit", model, length={"is_metric": True, "raw": "METERS"}, area={"is_metric": True, "raw": "SQUARE_METERS"}, volume={"is_metric": True, "raw": "CUBIC_METERS"})
    context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body = ifcopenshell.api.run("context.add_context", model, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=context)
    project.RepresentationContexts = [context]
    site = create_product(model, "IfcSite", "Minsk apartment site placeholder", owner)
    building = create_product(model, "IfcBuilding", "Apartment building placeholder", owner)
    storey = create_product(model, "IfcBuildingStorey", "Apartment level", owner)
    for parent, child in [(project, site), (site, building), (building, storey)]:
        ifcopenshell.api.run("aggregate.assign_object", model, products=[child], relating_object=parent)

    rooms = [
        {"name": "Living room", "x_m": 6.28, "y_m": 0.60, "width_m": 3.46, "depth_m": 5.63, "area_m2": 19.49, "source": "current detailed plan"},
        {"name": "Kitchen", "x_m": 6.28, "y_m": 6.23, "width_m": 3.75, "depth_m": 1.40, "area_m2": 5.24, "source": "current detailed plan"},
        {"name": "Bedroom", "x_m": 3.05, "y_m": 0.60, "width_m": 2.97, "depth_m": 5.68, "area_m2": 16.64, "source": "current detailed plan and comparable plans"},
        {"name": "Small bedroom", "x_m": 0.15, "y_m": 1.84, "width_m": 2.79, "depth_m": 3.35, "area_m2": 9.36, "source": "current detailed plan"},
        {"name": "Bathroom", "x_m": 0.15, "y_m": 5.19, "width_m": 1.80, "depth_m": 1.72, "area_m2": 3.09, "source": "current detailed plan"},
        {"name": "WC", "x_m": 0.15, "y_m": 6.91, "width_m": 1.14, "depth_m": 1.09, "area_m2": 1.24, "source": "current detailed plan"},
        {"name": "Entrance hall", "x_m": 2.00, "y_m": 6.10, "width_m": 4.10, "depth_m": 2.31, "area_m2": 9.79, "source": "current detailed plan; depth calibrated from comparable plans"},
        {"name": "Loggia", "x_m": 0.15, "y_m": 0.00, "width_m": 2.93, "depth_m": 1.84, "area_m2": 6.05, "source": "current detailed plan"},
    ]
    spaces = {}
    for room_data in rooms:
        space = add_box(model, body, storey, owner, "IfcSpace", room_data["name"], room_data["x_m"], room_data["y_m"], room_data["width_m"], room_data["depth_m"], 0.02, z=0.01)
        add_pset(model, space, "Pset_CurrentApartmentEvidence", {
            "Source": room_data["source"],
            "AreaM2": room_data["area_m2"],
            "GeometryStatus": "planned_not_field_verified",
        })
        spaces[room_data["name"]] = space

    # A conservative wall skeleton from the current plan. It preserves the
    # main room topology and measured spans, but keeps irregular façade details
    # as a later refinement after CAD/field confirmation.
    created = {"door": [], "window": []}
    walls = {}
    wall_meta = {}
    opening_meta = []
    def add_wall(name, x, y, length, horizontal, thickness=WALL_T):
        item = wall(model, body, storey, owner, name, x, y, length, horizontal, thickness=thickness)
        walls[name] = item
        wall_meta[name] = {
            "horizontal": horizontal,
            "bbox": (x, y, x + length, y + thickness) if horizontal else (x, y, x + thickness, y + length),
        }
        return item

    add_wall("North exterior wall", 0.0, 8.16, 10.20, True, EXT_T)
    add_wall("East exterior wall", 10.03, 0.60, 7.81, False, EXT_T)
    add_wall("West exterior wall upper", 0.0, 1.84, 6.32, False, EXT_T)
    add_wall("West exterior wall loggia", 0.0, 0.0, 1.84, False, EXT_T)
    add_wall("South living wall", 6.02, 0.35, 4.01, True, EXT_T)
    add_wall("South bedroom wall", 2.94, 0.35, 3.23, True, EXT_T)
    add_wall("South loggia wall", 0.0, -0.15, 3.08, True, EXT_T)

    add_wall("Small-bedroom east wall", 2.94, 1.84, 3.35, False)
    add_wall("Small-bedroom north wall", 0.0, 5.19, 2.94, True)
    add_wall("Bathroom north wall", 0.0, 6.91, 1.95, True)
    add_wall("Bathroom east wall", 1.95, 5.19, 1.72, False)
    add_wall("WC east wall", 1.29, 6.91, 1.09, False)
    add_wall("Bedroom west wall", 2.94, 0.60, 5.68, False)
    add_wall("Bedroom east wall", 6.02, 0.60, 5.68, False)
    add_wall("Bedroom north wall", 2.94, 6.28, 3.08, True)
    add_wall("Living west wall", 6.02, 0.60, 7.03, False)
    add_wall("Kitchen-living top partition", 6.02, 6.23, 4.01, True)
    add_wall("Hall lower wall", 1.95, 6.10, 4.07, True)

    def add_opening(wall_name, name, x, y, width, horizontal, bottom, height, kind):
        item = opening(model, body, storey, owner, walls[wall_name], name, x, y, width, horizontal, bottom, height, kind, created)
        opening_meta.append({
            "host_wall": wall_name,
            "bbox": (x, y - 0.08, x + width, y + 0.23) if horizontal else (x - 0.08, y, x + 0.23, y + width),
        })
        return item

    add_opening("North exterior wall", "Entrance opening 1010 mm", 2.40, 8.16, 1.01, True, 0.0, 2.1, "door")
    add_opening("Small-bedroom east wall", "Small bedroom doorway", 2.94, 2.00, 0.91, False, 0.0, 2.1, "door")
    add_opening("Bathroom east wall", "Bathroom doorway", 1.95, 5.75, 0.71, False, 0.0, 2.1, "door")
    add_opening("WC east wall", "WC doorway", 1.29, 7.10, 0.71, False, 0.0, 2.1, "door")
    add_opening("Bedroom north wall", "Bedroom doorway", 3.35, 6.28, 0.91, True, 0.0, 2.1, "door")
    add_opening("Living west wall", "Kitchen doorway", 6.02, 6.35, 1.20, False, 0.0, 2.1, "door")
    add_opening("Kitchen-living top partition", "Kitchen living doorway", 8.20, 6.23, 1.20, True, 0.0, 2.1, "door")
    add_opening("South living wall", "Living room window opening", 7.30, 0.35, 1.80, True, 1.0, 1.1, "window")
    add_opening("South bedroom wall", "Bedroom window opening", 3.60, 0.35, 1.80, True, 1.0, 1.1, "window")
    add_opening("West exterior wall upper", "Small bedroom window opening", 0.0, 3.00, 1.40, False, 1.0, 1.1, "window")
    add_opening("North exterior wall", "Kitchen window opening", 7.55, 8.16, 1.80, True, 1.0, 1.1, "window")

    door_specs = [
        ("Entrance door probable 910 mm leaf", 2.45, 8.17, 0.91, 0.08, 2.1, 0.0),
        ("Small bedroom door", 2.94, 2.00, 0.91, 0.08, 2.1, 90.0),
        ("Bathroom door", 1.95, 5.75, 0.71, 0.08, 2.1, 90.0),
        ("WC door", 1.29, 7.10, 0.71, 0.08, 2.1, 90.0),
        ("Bedroom door", 3.35, 6.28, 0.91, 0.08, 2.1, 0.0),
        ("Kitchen doorway", 6.02, 6.35, 1.20, 0.08, 2.1, 90.0),
        ("Kitchen living doorway", 8.20, 6.23, 1.20, 0.08, 2.1, 0.0),
    ]
    for spec in door_specs:
        add_fill(model, body, storey, owner, "IfcDoor", *spec, created["door"])
    window_specs = [
        ("Living room window", 7.30, 0.36, 1.80, 0.08, 1.1, 0.0),
        ("Bedroom window", 3.60, 0.36, 1.80, 0.08, 1.1, 0.0),
        ("Small bedroom window", 0.02, 3.00, 1.40, 0.08, 1.1, 90.0),
        ("Kitchen window", 7.55, 8.08, 1.80, 0.08, 1.1, 0.0),
    ]
    for spec in window_specs:
        add_fill(model, body, storey, owner, "IfcWindow", *spec, created["window"])

    boundary_map = {
        "North exterior wall": ["Entrance hall", "Kitchen", "WC"],
        "East exterior wall": ["Kitchen", "Living room"],
        "West exterior wall upper": ["Small bedroom", "Bathroom", "WC"],
        "West exterior wall loggia": ["Loggia"],
        "South living wall": ["Living room"],
        "South bedroom wall": ["Bedroom"],
        "South loggia wall": ["Loggia"],
        "Small-bedroom east wall": ["Small bedroom", "Bedroom", "Entrance hall"],
        "Small-bedroom north wall": ["Small bedroom", "Bathroom"],
        "Bathroom north wall": ["Bathroom", "WC"],
        "Bathroom east wall": ["Bathroom", "Entrance hall"],
        "WC east wall": ["WC", "Entrance hall"],
        "Bedroom west wall": ["Bedroom", "Small bedroom", "Loggia"],
        "Bedroom east wall": ["Bedroom", "Living room"],
        "Bedroom north wall": ["Bedroom", "Entrance hall"],
        "Living west wall": ["Living room", "Bedroom", "Entrance hall", "Kitchen"],
        "Kitchen-living top partition": ["Kitchen", "Living room", "Entrance hall"],
        "Hall lower wall": ["Entrance hall", "Bathroom", "Bedroom"],
    }
    for wall_name, room_names in boundary_map.items():
        for room_name in room_names:
            boundary = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcRelSpaceBoundary", name="PlannedCurrentApartmentBoundary")
            ifcopenshell.api.run(
                "boundary.edit_attributes",
                model,
                entity=boundary,
                relating_space=spaces[room_name],
                related_building_element=walls[wall_name],
                physical_or_virtual="PHYSICAL",
                internal_or_external="EXTERNAL" if "exterior" in wall_name.lower() or wall_name.startswith("South") else "INTERNAL",
            )

    def room_point(room_data, side, fraction):
        x, y = room_data["x_m"], room_data["y_m"]
        w, d = room_data["width_m"], room_data["depth_m"]
        if side == "bottom":
            return x + w * fraction, y
        if side == "top":
            return x + w * fraction, y + d
        if side == "left":
            return x, y + d * fraction
        if side == "right":
            return x + w, y + d * fraction
        raise ValueError(f"Unsupported side: {side}")

    def snap_to_wall(candidate, side):
        cx, cy = candidate
        best = None
        for wall_name, meta in wall_meta.items():
            x0, y0, x1, y1 = meta["bbox"]
            if side in {"bottom", "top"} and meta["horizontal"] and x0 - 0.05 <= cx <= x1 + 0.05:
                distance = abs(cy - ((y0 + y1) / 2.0))
                if best is None or distance < best[0]:
                    best = (distance, wall_name, cx, (y0 + y1) / 2.0)
            if side in {"left", "right"} and not meta["horizontal"] and y0 - 0.05 <= cy <= y1 + 0.05:
                distance = abs(cx - ((x0 + x1) / 2.0))
                if best is None or distance < best[0]:
                    best = (distance, wall_name, (x0 + x1) / 2.0, cy)
        if best is None:
            raise RuntimeError(f"Cannot snap service at {candidate} on {side}.")
        return best[1], best[2], best[3]

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

    def add_terminal(name, room_name, side, fraction, z, width, depth, pset_name, properties):
        room_data = next(item for item in rooms if item["name"] == room_name)
        wall_name, sx, sy = snap_to_wall(room_point(room_data, side, fraction), side)
        if opening_collision(sx, sy, wall_name):
            raise RuntimeError(f"{name} overlaps an opening on {wall_name}.")
        horizontal = wall_meta[wall_name]["horizontal"]
        box_w, box_d = (width, depth) if horizontal else (depth, width)
        terminal = add_box(model, body, storey, owner, "IfcFlowTerminal", name, sx - box_w / 2.0, sy - box_d / 2.0, box_w, box_d, 0.16, z=z)
        enriched = {"Room": room_name, "HostWall": wall_name, "Mounting": "wall_centerline_coordination_symbol", "CoordinationStatus": "conceptual_not_engineered"}
        enriched.update(properties)
        add_pset(model, terminal, pset_name, enriched)
        return terminal

    electrical_plan = {
        "Entrance hall": [("bottom", 0.75), ("top", 0.65)],
        "Kitchen": [("top", 0.15), ("right", 0.55)],
        "Living room": [("bottom", 0.10), ("right", 0.50), ("top", 0.25)],
        "Bedroom": [("left", 0.70), ("right", 0.65)],
        "Small bedroom": [("bottom", 0.25), ("right", 0.55)],
        "Bathroom": [("top", 0.40)],
        "WC": [("top", 0.40)],
    }
    electrical_devices = []
    for room_name, positions in electrical_plan.items():
        for index, (side, fraction) in enumerate(positions, 1):
            electrical_devices.append(add_terminal(
                f"{room_name} outlet {index}",
                room_name,
                side,
                fraction,
                1.05,
                0.12,
                0.04,
                "Pset_DemoElectricalCoordination",
                {"DeviceType": "outlet_or_switch_placeholder"},
            ))

    plumbing_devices = [
        add_terminal("Kitchen sink plumbing connection", "Kitchen", "right", 0.55, 0.65, 0.24, 0.05, "Pset_DemoPlumbingCoordination", {"DeviceType": "sink_hot_cold_drain_placeholder", "System": "water_and_waste"}),
        add_terminal("Bathroom vanity plumbing connection", "Bathroom", "top", 0.50, 0.65, 0.24, 0.05, "Pset_DemoPlumbingCoordination", {"DeviceType": "vanity_hot_cold_drain_placeholder", "System": "water_and_waste"}),
        add_terminal("WC cistern plumbing connection", "WC", "top", 0.50, 0.65, 0.24, 0.05, "Pset_DemoPlumbingCoordination", {"DeviceType": "wc_cistern_water_placeholder", "System": "cold_water_and_waste"}),
    ]

    lighting_fixtures = []
    for room_data in rooms:
        if room_data["name"] == "Loggia":
            continue
        fixture = add_box(
            model,
            body,
            storey,
            owner,
            "IfcLightFixture",
            f"{room_data['name']} ceiling light",
            room_data["x_m"] + room_data["width_m"] / 2.0 - 0.175,
            room_data["y_m"] + room_data["depth_m"] / 2.0 - 0.175,
            0.35,
            0.35,
            0.05,
            z=2.62,
        )
        add_pset(model, fixture, "Pset_DemoLightingCoordination", {
            "Room": room_data["name"],
            "Mounting": "ceiling_center_visual_fixture",
            "DeviceType": "ceiling_light_placeholder",
            "TemperatureKelvin": 3000,
            "ApproxLumens": 550,
            "CoordinationStatus": "visual_scenario_not_lux_validated",
        })
        lighting_fixtures.append(fixture)

    add_box(model, body, storey, owner, "IfcSlab", "Current apartment floor seed", 0.0, -0.15, 10.28, 8.56, 0.12, z=-0.12)

    evidence = {
        "primary_sources": [
            "00_Inbox/_Visual_Drop/fllor_plan_detailed.jpeg",
            "00_Inbox/_Visual_Drop/floor_plan_basic.jpg",
        ],
        "calibration_sources": [
            "00_Inbox/_Visual_Drop/floor plan_1.jpg",
            "00_Inbox/_Visual_Drop/floor plan_2.jpg",
            "00_Inbox/_Visual_Drop/floor plan_3.jpg",
        ],
        "cad_underlay": {
            "source": "00_Inbox/cad/20260727-ZK Dubravinskiy.dwg",
            "policy": "reference_underlay_not_authoritative_bim_geometry",
            "intake_summary": "tools/cad/CAD_INTAKE_SUMMARY.md",
            "observed_dxf_units": "millimetres",
            "candidate_controls": {
                "entrance_opening_target_mm": 1010,
                "nearest_cad_dimension_mm": 1014.671,
                "probable_door_leaf_target_mm": 910,
                "door_leaf_exact_matches_found": True,
                "entrance_hall_depth_target_mm": 2310,
                "nearest_cad_dimension_mm_for_hall_depth": 2308.734,
            },
        },
        "entrance_opening_mm": 1010,
        "probable_door_leaf_mm": 910,
        "hall_depth_scenarios_m": [2.28, 2.31, 2.33],
        "nominal_hall_depth_m": 2.31,
        "geometry_status": "planned_from_visual_sources_not_field_verified",
        "model_limitations": [
            "irregular loggia facade simplified",
            "some service shaft and column details approximated",
            "room polygons represented with rectangular spaces for first seed",
            "final millimetre dimensions require site measurement",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    model.write(str(args.output))
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps({"model_type": "current_apartment_seed", "status": evidence["geometry_status"], "rooms": rooms, "electrical_devices": len(electrical_devices), "plumbing_devices": len(plumbing_devices), "lighting_fixtures": len(lighting_fixtures), "evidence": evidence}, indent=2) + "\n", encoding="utf-8")
    reopened = ifcopenshell.open(str(args.output))
    print(json.dumps({
        "ifc": str(args.output),
        "manifest": str(args.manifest),
        "walls": len(reopened.by_type("IfcWall")),
        "spaces": len(reopened.by_type("IfcSpace")),
        "doors": len(reopened.by_type("IfcDoor")),
        "windows": len(reopened.by_type("IfcWindow")),
        "flow_terminals": len(reopened.by_type("IfcFlowTerminal")),
        "light_fixtures": len(reopened.by_type("IfcLightFixture")),
        "status": evidence["geometry_status"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
