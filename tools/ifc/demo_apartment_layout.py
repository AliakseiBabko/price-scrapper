"""Generate a generic enclosed apartment layout for technology testing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ifcopenshell
import ifcopenshell.api

from poc_renovation import add_owner_history, add_relationship, create_product, extruded_representation, placement


def add_box(model, body, storey, owner, cls, name, x, y, width, depth, height, z=0.0, rotation=0.0):
    item = create_product(model, cls, name, owner)
    item.Representation, _ = extruded_representation(model, body, width, depth, height)
    # IfcRectangleProfileDef is centered on its local origin. Convert the
    # supplied lower-left bounding-box coordinates into a placement at the
    # object's world-space center. For 90-degree objects, local width maps to
    # world Y and local depth maps to world X.
    if abs(float(rotation)) in (90.0, 270.0):
        px, py = float(x) + float(depth) / 2.0, float(y) + float(width) / 2.0
    else:
        px, py = float(x) + float(width) / 2.0, float(y) + float(depth) / 2.0
    item.ObjectPlacement = placement(model, px, py, float(z), float(rotation))
    if cls not in {"IfcSpace"}:
        ifcopenshell.api.run("spatial.assign_container", model, products=[item], relating_structure=storey)
    else:
        ifcopenshell.api.run("aggregate.assign_object", model, products=[item], relating_object=storey)
    return item


def wall(model, body, storey, owner, name, x, y, length, horizontal, thickness=0.15, height=2.8, z=0.0):
    return add_box(model, body, storey, owner, "IfcWall", name, x, y, length, thickness, height, z=z, rotation=0.0 if horizontal else 90.0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    model = ifcopenshell.file(schema="IFC4")
    owner = add_owner_history(model)
    project = create_product(model, "IfcProject", "Generic enclosed apartment demonstrator", owner)
    ifcopenshell.api.run("unit.assign_unit", model, length={"is_metric": True, "raw": "METERS"}, area={"is_metric": True, "raw": "SQUARE_METERS"}, volume={"is_metric": True, "raw": "CUBIC_METERS"})
    context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body = ifcopenshell.api.run("context.add_context", model, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=context)
    project.RepresentationContexts = [context]
    site = create_product(model, "IfcSite", "Generic site", owner)
    building = create_product(model, "IfcBuilding", "Generic building", owner)
    storey = create_product(model, "IfcBuildingStorey", "Apartment level", owner)
    for parent, child in [(project, site), (site, building), (building, storey)]:
        ifcopenshell.api.run("aggregate.assign_object", model, products=[child], relating_object=parent)

    width, depth, thickness = 10.0, 8.0, 0.15
    # Floor and enclosed room slabs.
    # Match the slab footprint to the finished exterior wall envelope. The
    # perimeter walls extend one thickness at the east/north outside edges,
    # so the underside must not stop short of those corners.
    add_box(model, body, storey, owner, "IfcSlab", "Apartment floor", 0, 0, width + thickness, depth + thickness, 0.12, z=-0.12)
    rooms = [
        {"name": "Living room", "x_m": 0.15, "y_m": 4.15, "width_m": 5.7, "depth_m": 3.7, "area_m2": 21.09},
        {"name": "Bedroom", "x_m": 6.15, "y_m": 4.15, "width_m": 3.7, "depth_m": 3.7, "area_m2": 13.69},
        {"name": "Kitchen", "x_m": 0.15, "y_m": 0.15, "width_m": 3.7, "depth_m": 3.7, "area_m2": 13.69},
        {"name": "Bathroom", "x_m": 4.15, "y_m": 2.15, "width_m": 1.7, "depth_m": 1.7, "area_m2": 2.89},
        {"name": "WC", "x_m": 4.15, "y_m": 0.15, "width_m": 1.7, "depth_m": 1.7, "area_m2": 2.89},
        {"name": "Entrance hall", "x_m": 6.15, "y_m": 0.15, "width_m": 3.7, "depth_m": 3.7, "area_m2": 13.69},
    ]
    spaces = {}
    for room in rooms:
        spaces[room["name"]] = add_box(model, body, storey, owner, "IfcSpace", room["name"], room["x_m"], room["y_m"], room["width_m"], room["depth_m"], 0.02, z=0.01)

    created_openings = {"door": [], "window": []}
    opening_registry = []

    wall_registry = {}
    def host_wall(name, x, y, length, horizontal, openings=()):
        """Create one wall and native IfcOpeningElement voids in that wall."""
        # Wall coordinates are lower-left bounding-box coordinates. Clean
        # junctions are obtained by continuous wall runs, without decorative
        # overlap or filler geometry.
        perimeter_extension = thickness if "exterior" in name.lower() and horizontal else 0.0
        host = wall(model, body, storey, owner, name, x, y, length + perimeter_extension, horizontal)
        actual_length = length + perimeter_extension
        bbox = (x, y, x + actual_length, y + thickness) if horizontal else (x, y, x + thickness, y + actual_length)
        wall_registry[name] = {"entity": host, "horizontal": horizontal, "bbox": bbox}
        for index, (start, opening_width, bottom, opening_height, opening_kind) in enumerate(openings, 1):
            if horizontal:
                opening = add_box(model, body, storey, owner, "IfcOpeningElement", f"{name} opening {index}", start, y - 0.08, opening_width, 0.31, opening_height, z=bottom)
                opening_bbox = (start, y - 0.08, start + opening_width, y + 0.23)
            else:
                opening = add_box(model, body, storey, owner, "IfcOpeningElement", f"{name} opening {index}", x - 0.08, start, opening_width, 0.31, opening_height, z=bottom, rotation=90.0)
                opening_bbox = (x - 0.08, start, x + 0.23, start + opening_width)
            add_relationship(model, "IfcRelVoidsElement", owner, RelatingBuildingElement=host, RelatedOpeningElement=opening)
            created_openings[opening_kind].append(opening)
            opening_registry.append({"host_wall": name, "bbox": opening_bbox})
        return host

    # One host object per construction wall. Openings are bounded vertically
    # by the opening bottom/top, so the wall remains present as sill/header.
    host_wall("South exterior wall", 0.0, 0.0, width, True, [(7.2, 1.0, 0.0, 2.1, "door")])
    host_wall("North exterior wall", 0.0, depth, width, True, [(3.0, 1.8, 1.0, 1.1, "window"), (7.0, 1.8, 1.0, 1.1, "window")])
    host_wall("West exterior wall", 0.0, 0.0, depth, False, [(1.4, 1.4, 1.0, 1.1, "window")])
    host_wall("East exterior wall", width, 0.0, depth, False)
    host_wall("Living-bedroom wall", 6.0, 4.0, 4.0, False, [(5.0, 1.0, 0.0, 2.1, "door")])
    host_wall("Kitchen-bath wall", 4.0, 0.0, 4.0, False)
    host_wall("Hall-bath wall", 6.0, 0.0, 4.0, False, [(0.55, 0.8, 0.0, 2.1, "door"), (2.35, 0.8, 0.0, 2.1, "door")])
    host_wall("Bathroom-WC wall", 4.0, 2.0, 2.0, True)
    host_wall("Living lower wall", 0.0, 4.0, 6.0, True, [(2.9, 1.2, 0.0, 2.1, "door")])
    host_wall("Bedroom south wall", 6.0, 4.0, 4.0, True, [(7.0, 1.0, 0.0, 2.1, "door")])

    def add_space_boundary(space_name, wall_name):
        boundary = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcRelSpaceBoundary", name="1stLevelBoundary")
        ifcopenshell.api.run(
            "boundary.edit_attributes",
            model,
            entity=boundary,
            relating_space=spaces[space_name],
            related_building_element=wall_registry[wall_name]["entity"],
            physical_or_virtual="PHYSICAL",
            internal_or_external="INTERNAL" if "exterior" not in wall_name.lower() else "EXTERNAL",
        )

    # First-level semantic adjacency. ConnectionGeometry is intentionally
    # left unset until exact boundary surfaces are authored.
    boundary_map = {
        "South exterior wall": ["Kitchen", "WC", "Entrance hall"],
        "North exterior wall": ["Living room", "Bedroom"],
        "West exterior wall": ["Living room", "Kitchen"],
        "East exterior wall": ["Bedroom", "Entrance hall"],
        "Living-bedroom wall": ["Living room", "Bedroom"],
        "Kitchen-bath wall": ["Kitchen", "Bathroom", "WC"],
        "Hall-bath wall": ["Entrance hall", "Bathroom", "WC"],
        "Bathroom-WC wall": ["Bathroom", "WC"],
        "Living lower wall": ["Living room", "Kitchen", "Bathroom"],
        "Bedroom south wall": ["Bedroom", "Entrance hall"],
    }
    for wall_name, room_names in boundary_map.items():
        for room_name in room_names:
            add_space_boundary(room_name, wall_name)

    # Doors are placed in the deliberate wall gaps; windows are thin visible
    # objects on the exterior. They are design placeholders, not code details.
    # The order follows native opening creation order: exterior entrance,
    # living-bedroom, WC, bathroom, living-kitchen, bedroom-entrance.
    doors = [("Entrance door", 7.2, 0.02, 1.0, 0.08, 0.0), ("Bedroom living door", 6.0, 5.0, 1.0, 0.08, 90.0), ("WC door", 6.0, 0.55, 0.8, 0.08, 90.0), ("Bathroom door", 6.0, 2.35, 0.8, 0.08, 90.0), ("Living door", 2.9, 4.0, 1.2, 0.08, 0.0), ("Bedroom entrance door", 7.0, 4.0, 1.0, 0.08, 0.0)]
    for name, x, y, w, d, rotation in doors:
        door = add_box(model, body, storey, owner, "IfcDoor", name, x, y, w, d, 2.1, z=0.0, rotation=rotation)
        door_opening = created_openings["door"].pop(0)
        add_relationship(model, "IfcRelFillsElement", owner, RelatingOpeningElement=door_opening, RelatedBuildingElement=door)
    windows = [("Living window", 3.0, 7.92, 1.8, 0.08, 0.0), ("Bedroom window", 7.0, 7.92, 1.8, 0.08, 0.0), ("Kitchen window", 0.02, 1.4, 1.4, 0.08, 90.0)]
    for name, x, y, w, d, rotation in windows:
        window = add_box(model, body, storey, owner, "IfcWindow", name, x, y, w, d, 1.1, z=1.0, rotation=rotation)
        window_opening = created_openings["window"].pop(0)
        add_relationship(model, "IfcRelFillsElement", owner, RelatingOpeningElement=window_opening, RelatedBuildingElement=window)

    def opening_collision(x, y, wall_name, clearance=0.22):
        for opening in opening_registry:
            if opening["host_wall"] != wall_name:
                continue
            ox0, oy0, ox1, oy1 = opening["bbox"]
            wall_meta = wall_registry[wall_name]
            if wall_meta["horizontal"]:
                if ox0 - clearance <= x <= ox1 + clearance:
                    return True
            elif oy0 - clearance <= y <= oy1 + clearance:
                return True
        return False

    def room_point(room, side, fraction):
        x0, y0 = room["x_m"], room["y_m"]
        w, d = room["width_m"], room["depth_m"]
        if side == "bottom":
            return x0 + w * fraction, y0
        if side == "top":
            return x0 + w * fraction, y0 + d
        if side == "left":
            return x0, y0 + d * fraction
        if side == "right":
            return x0 + w, y0 + d * fraction
        raise ValueError(f"Unsupported side: {side}")

    def snap_to_wall(candidate, side):
        cx, cy = candidate
        best = None
        for wall_name, meta in wall_registry.items():
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
            raise RuntimeError(f"Cannot snap electrical device at {candidate} on {side}.")
        return best[1], best[2], best[3]

    def electrical_positions(room_name):
        key = room_name.lower()
        if "entrance" in key:
            return [("bottom", 0.25), ("bottom", 0.78)]
        if "living" in key:
            return [("bottom", 0.18), ("bottom", 0.78), ("right", 0.62)]
        if "bedroom" in key:
            return [("bottom", 0.25), ("bottom", 0.75)]
        if "kitchen" in key:
            return [("top", 0.2), ("top", 0.7), ("left", 0.25)]
        return [("top", 0.18)]

    electrical_devices = []
    alternates = [("bottom", 0.35), ("top", 0.35), ("left", 0.5), ("right", 0.5), ("bottom", 0.65), ("top", 0.65)]
    for room in rooms:
        for index, (side, fraction) in enumerate(electrical_positions(room["name"]), 1):
            for candidate_side, candidate_fraction in [(side, fraction)] + alternates:
                host_name, sx, sy = snap_to_wall(room_point(room, candidate_side, candidate_fraction), candidate_side)
                if not opening_collision(sx, sy, host_name):
                    horizontal = wall_registry[host_name]["horizontal"]
                    symbol_width, symbol_depth = (0.12, 0.04) if horizontal else (0.04, 0.12)
                    device = add_box(
                        model,
                        body,
                        storey,
                        owner,
                        "IfcFlowTerminal",
                        f"{room['name']} outlet {index}",
                        sx - symbol_width / 2.0,
                        sy - symbol_depth / 2.0,
                        symbol_width,
                        symbol_depth,
                        0.18,
                        z=1.05,
                    )
                    pset = ifcopenshell.api.run("pset.add_pset", model, product=device, name="Pset_DemoElectricalCoordination")
                    ifcopenshell.api.run(
                        "pset.edit_pset",
                        model,
                        pset=pset,
                        properties={
                            "Room": room["name"],
                            "HostWall": host_name,
                            "Mounting": "wall_centerline_coordination_symbol",
                            "DeviceType": "outlet_or_switch_placeholder",
                            "CoordinationStatus": "conceptual_not_engineered",
                        },
                    )
                    electrical_devices.append(device)
                    break
            else:
                raise RuntimeError(f"Cannot place {room['name']} outlet {index} without opening collision.")

    model.write(str(args.output))
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps({"model_type": "generic_enclosed_apartment", "status": "technology_demonstrator", "rooms": rooms, "electrical_devices": len(electrical_devices)}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ifc": str(args.output), "manifest": str(args.manifest), "rooms": len(rooms), "doors": len(doors), "windows": len(windows), "electrical_devices": len(electrical_devices), "status": "enclosed_layout"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
