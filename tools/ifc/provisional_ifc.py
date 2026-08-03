"""Generate adjustable, explicitly provisional apartment IFC variants.

The current source does not provide field-verified room dimensions.  This tool
therefore generates coordination geometry from labelled areas and aspect-ratio
assumptions, preserving the hall-depth sensitivity scenarios in the output
metadata.  It is not a construction or procurement model.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ifcopenshell
import ifcopenshell.api

from poc_renovation import add_owner_history, add_relationship, create_product, extruded_representation, placement


def rectangle_dimensions(area: float, aspect: float) -> tuple[float, float]:
    width = (area * aspect) ** 0.5
    return round(width, 3), round(area / width, 3)


def build_variant(data: dict, hall_depth: float, output: Path) -> dict:
    model = ifcopenshell.file(schema="IFC4")
    owner = add_owner_history(model)
    project = create_product(model, "IfcProject", data["project_name"], owner)
    ifcopenshell.api.run("unit.assign_unit", model, length={"is_metric": True, "raw": "METERS"}, area={"is_metric": True, "raw": "SQUARE_METERS"}, volume={"is_metric": True, "raw": "CUBIC_METERS"})
    context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body = ifcopenshell.api.run("context.add_context", model, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=context)
    project.RepresentationContexts = [context]
    site = create_product(model, "IfcSite", "Provisional site", owner)
    building = create_product(model, "IfcBuilding", "Provisional building", owner)
    storey = create_product(model, "IfcBuildingStorey", "Apartment level", owner)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[site], relating_object=project)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[building], relating_object=site)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[storey], relating_object=building)

    wall_height, wall_thickness = 2.8, 0.12
    area_labels = data["room_area_labels_m2"]
    specs = [
        ("Entrance hall", "hall", max(hall_depth, 0.1), 1.0),
        ("Living group (area proxy)", "living_group_total", 1.65, 1.0),
        ("Kitchen (area proxy)", "kitchen", 1.25, 1.0),
        ("Bathroom (area proxy)", "bathroom", 1.0, 1.0),
        ("WC (area proxy)", "wc", 1.15, 1.0),
    ]
    x_cursor = 0.0
    room_records = []
    for name, key, aspect, _ in specs:
        width, depth = rectangle_dimensions(float(area_labels[key]), aspect)
        # Hall depth is the sensitivity variable; preserve its area label by
        # adjusting the other rectangle dimension rather than scaling the plan.
        if key == "hall":
            depth, width = hall_depth, round(float(area_labels[key]) / hall_depth, 3)
        x, y = x_cursor, 0.0
        space = create_product(model, "IfcSpace", name, owner)
        space.Representation, _ = extruded_representation(model, body, width, depth, 0.01)
        space.ObjectPlacement = placement(model, x, y, 0.0, 0.0)
        ifcopenshell.api.run("aggregate.assign_object", model, products=[space], relating_object=storey)
        # A simple perimeter is useful for viewing and plan projection; it is
        # intentionally not claimed to be the surveyed apartment wall layout.
        wall_specs = [
            ("South", width, wall_thickness, x, y, 0.0),
            ("East", depth, wall_thickness, x + width, y, 90.0),
            ("North", width, wall_thickness, x + width, y + depth, 180.0),
            ("West", depth, wall_thickness, x, y + depth, 270.0),
        ]
        walls = []
        for side, wx, wy, px, py, rotation in wall_specs:
            wall = create_product(model, "IfcWall", f"{name} {side} wall", owner)
            wall.Representation, _ = extruded_representation(model, body, wx, wy, wall_height)
            wall.ObjectPlacement = placement(model, px, py, 0.0, rotation)
            ifcopenshell.api.run("spatial.assign_container", model, products=[wall], relating_structure=storey)
            walls.append(wall)
        room_records.append({"name": name, "area_m2": area_labels[key], "width_m": width, "depth_m": depth, "x_m": x, "y_m": y})
        x_cursor += width + 0.25

    # Entrance opening is attached to the provisional hall west wall. Its
    # location is only a placeholder until the real entrance geometry is known.
    hall = room_records[0]
    hall_west = model.by_type("IfcWall")[3]
    opening = create_product(model, "IfcOpeningElement", "Entrance opening (provisional 1010 mm)", owner)
    opening.Representation, _ = extruded_representation(model, body, data["control_geometry"]["entrance_opening_m"], wall_thickness * 1.2, 2.1)
    opening.ObjectPlacement = placement(model, hall["x_m"] - wall_thickness * 0.1, hall["y_m"] + 0.35, 0.0, 0.0)
    add_relationship(model, "IfcRelVoidsElement", owner, RelatingBuildingElement=hall_west, RelatedOpeningElement=opening)
    door = create_product(model, "IfcDoor", "Entrance door leaf (probable 910 mm)", owner)
    door.Representation, _ = extruded_representation(model, body, data["control_geometry"]["probable_door_leaf_m"], wall_thickness * 0.4, 2.1)
    door.ObjectPlacement = placement(model, hall["x_m"], hall["y_m"] + 0.35, 0.0, 0.0)
    ifcopenshell.api.run("spatial.assign_container", model, products=[door], relating_structure=storey)
    add_relationship(model, "IfcRelFillsElement", owner, RelatingOpeningElement=opening, RelatedBuildingElement=door)
    model.write(str(output))
    return {"ifc": str(output), "hall_depth_m": hall_depth, "rooms": room_records, "status": "planned_not_as_built", "qto_status": data["qto_status"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    scenarios = [float(data["control_geometry"]["entrance_hall_depth_m"]["nominal"]), *map(float, data["control_geometry"]["entrance_hall_depth_m"]["scenarios"])]
    results = [build_variant(data, depth, args.output_dir / f"apartment_provisional_hall_{depth:.2f}m.ifc") for depth in sorted(set(scenarios))]
    manifest = {"source": str(args.input), "model_status": data["model_status"], "variants": results, "note": "Replace provisional dimensions with field survey before construction use."}
    (args.output_dir / "apartment_provisional_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
