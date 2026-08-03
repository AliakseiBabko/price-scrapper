"""Build a conceptual IFC model from apartment design JSON.

Rooms, furniture, MEP devices, and light fixtures are represented as simple
parametric boxes. The output is coordination geometry, not engineered MEP.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ifcopenshell
import ifcopenshell.api
from ifcopenshell.guid import new as new_guid

from poc_renovation import add_owner_history, add_relationship, create_product, extruded_representation, placement


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    model = ifcopenshell.file(schema="IFC4")
    owner = add_owner_history(model)
    project = create_product(model, "IfcProject", data["project_name"], owner)
    ifcopenshell.api.run("unit.assign_unit", model, length={"is_metric": True, "raw": "METERS"}, area={"is_metric": True, "raw": "SQUARE_METERS"}, volume={"is_metric": True, "raw": "CUBIC_METERS"})
    context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body = ifcopenshell.api.run("context.add_context", model, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=context)
    project.RepresentationContexts = [context]
    site = create_product(model, "IfcSite", "Design site", owner)
    building = create_product(model, "IfcBuilding", "Design building", owner)
    storey = create_product(model, "IfcBuildingStorey", "Apartment level", owner)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[site], relating_object=project)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[building], relating_object=site)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[storey], relating_object=building)

    room_positions = {}
    x_cursor = 0.0
    for room in data.get("rooms", []):
        room_positions[room["room_id"]] = (x_cursor, 0.0)
        space = create_product(model, "IfcSpace", room["name"], owner)
        space.Representation, _ = extruded_representation(model, body, room["length_m"], room["width_m"], 0.01)
        space.ObjectPlacement = placement(model, x_cursor, 0.0, 0.0, 0.0)
        ifcopenshell.api.run("aggregate.assign_object", model, products=[space], relating_object=storey)
        x_cursor += room["length_m"] + 0.3

    def add_box(ifc_class: str, name: str, room_id: str, x: float, y: float, width: float, depth: float, height: float):
        item = create_product(model, ifc_class, name, owner)
        item.Representation, _ = extruded_representation(model, body, width, depth, height)
        room_x, room_y = room_positions[room_id]
        item.ObjectPlacement = placement(model, room_x + x, room_y + y, 0.0, 0.0)
        ifcopenshell.api.run("spatial.assign_container", model, products=[item], relating_structure=storey)
        return item

    for item in data.get("furniture", []):
        add_box("IfcFurniture", item["item_id"], item["room_id"], item["x_m"], item["y_m"], item["width_m"], item["depth_m"], item["height_m"])
    for discipline, ifc_class in [("electrical", "IfcFlowTerminal"), ("plumbing", "IfcFlowTerminal"), ("hvac", "IfcFlowTerminal")]:
        for item in data.get("mep", {}).get(discipline, []):
            add_box(ifc_class, item["id"], item["room_id"], item["x_m"], item["y_m"], 0.1, 0.1, max(item.get("height_m", 0.3), 0.1))
    for item in data.get("lighting_scenarios", []):
        room = item["room_id"]
        for index in range(item.get("fixture_count", 0)):
            add_box("IfcLightFixture", f"{item['scenario_id']}-fixture-{index + 1}", room, 0.5 + index * 0.6, 1.0, 0.1, 0.1, 0.05)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    model.write(str(args.output))
    reopened = ifcopenshell.open(str(args.output))
    result = {"ifc": str(args.output), "spaces": len(reopened.by_type("IfcSpace")), "furniture": len(reopened.by_type("IfcFurniture")), "flow_terminals": len(reopened.by_type("IfcFlowTerminal")), "light_fixtures": len(reopened.by_type("IfcLightFixture")), "status": "conceptual_coordination_only"}
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
