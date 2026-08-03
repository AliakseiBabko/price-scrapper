"""Validate basic residential layout rules for the IFC demonstrator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import ifcopenshell


class LayoutError(RuntimeError):
    pass


def run(path: Path) -> dict:
    model = ifcopenshell.open(str(path))
    spaces = model.by_type("IfcSpace")
    errors: list[str] = []
    reports = []
    excluded = ("shaft", "technical", "void", "service")
    occupiable = [space for space in spaces if not any(token in str(space.Name or "").lower() for token in excluded)]
    room_by_name = {str(space.Name or ""): space for space in occupiable}
    graph = {space.id(): set() for space in occupiable}
    connectivity_rules = {
        "Living door": ("Living room", "Kitchen"),
        "Bedroom living door": ("Living room", "Bedroom"),
        "WC door": ("Entrance hall", "WC"),
        "Bathroom door": ("Entrance hall", "Bathroom"),
        "Bedroom entrance door": ("Entrance hall", "Bedroom"),
    }
    doors = {str(door.Name or ""): door for door in model.by_type("IfcDoor")}
    for door_name, (left_name, right_name) in connectivity_rules.items():
        if door_name not in doors:
            errors.append(f"Missing required doorway: {door_name}.")
            continue
        left = room_by_name.get(left_name)
        right = room_by_name.get(right_name)
        if not left or not right:
            errors.append(f"Doorway {door_name} references a missing room.")
            continue
        graph[left.id()].add(right.id())
        graph[right.id()].add(left.id())
    entrance = next((space for space in occupiable if str(space.Name or "").lower() == "entrance hall"), None)
    reachable = set()
    if entrance:
        pending = [entrance.id()]
        while pending:
            current = pending.pop()
            if current in reachable:
                continue
            reachable.add(current)
            pending.extend(graph[current] - reachable)
    for space in occupiable:
        if space.id() not in reachable:
            errors.append(f"{space.Name}: no door-connected route from Entrance hall.")
    for space in occupiable:
        boundaries = [b for b in model.by_type("IfcRelSpaceBoundary") if b.RelatingSpace == space]
        walls = {b.RelatedBuildingElement for b in boundaries if b.RelatedBuildingElement and b.RelatedBuildingElement.is_a("IfcWall")}
        doors = []
        windows = []
        for wall in walls:
            for void in getattr(wall, "HasOpenings", []) or []:
                opening = void.RelatedOpeningElement
                for fill in getattr(opening, "HasFillings", []) or []:
                    element = fill.RelatedBuildingElement
                    if element.is_a("IfcDoor"):
                        doors.append(element)
                    if element.is_a("IfcWindow"):
                        windows.append(element)
        name = str(space.Name or "Unnamed space")
        requires_window = name.lower() in {"living room", "bedroom", "kitchen"}
        if len(walls) < 4:
            errors.append(f"{name}: only {len(walls)} boundary walls; occupiable rooms require at least four.")
        if not doors:
            errors.append(f"{name}: no door or doorway connection.")
        if requires_window and not windows:
            errors.append(f"{name}: no exterior window connection.")
        reports.append({"room": name, "boundary_walls": len(walls), "doors": len(doors), "windows": len(windows), "reachable_from_entrance": space.id() in reachable, "window_rule": requires_window})
    return {"source": str(path), "occupiable_spaces": len(occupiable), "rooms": reports, "errors": errors, "status": "valid" if not errors else "invalid"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifc", type=Path, default=Path("data/outputs/demo/generic_enclosed_apartment_validated.ifc"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.ifc)
    text = json.dumps(result, indent=2)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    return 0 if result["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
