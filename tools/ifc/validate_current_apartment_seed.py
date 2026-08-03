"""Validate the current-apartment planned IFC seed.

This validator is intentionally stricter than a generic IFC syntax check. It
captures the residential layout rules repeatedly verified by visual inspection:
reachable rooms, required living-room windows, native opening/fill objects, and
wall-mounted coordination symbols that do not collide with doors/windows.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.placement


EXPECTED_ROOMS = {
    "Living room",
    "Kitchen",
    "Bedroom",
    "Small bedroom",
    "Bathroom",
    "WC",
    "Entrance hall",
    "Loggia",
}

WINDOW_REQUIRED = {"Living room", "Kitchen", "Bedroom", "Small bedroom"}

EXPECTED_DOOR_CONNECTIONS = {
    "Kitchen doorway": ("Entrance hall", "Kitchen"),
    "Kitchen living doorway": ("Kitchen", "Living room"),
    "Bedroom door": ("Entrance hall", "Bedroom"),
    "Small bedroom door": ("Bedroom", "Small bedroom"),
    "Bathroom door": ("Entrance hall", "Bathroom"),
    "WC door": ("Entrance hall", "WC"),
}

EXPECTED_STATUS = "planned_from_visual_sources_not_field_verified"


def _name(entity: Any) -> str:
    return str(getattr(entity, "Name", "") or "")


def _product_bbox_xy(product: Any) -> tuple[float, float, float, float] | None:
    """Return an approximate XY bbox from rectangular profile + placement.

    The demonstrator generator uses centered rectangular extrusions, so this is
    more stable here than tessellated shape bounding boxes and avoids expensive
    geometry settings during validation.
    """

    representation = getattr(product, "Representation", None)
    if not representation:
        return None
    reps = getattr(representation, "Representations", None) or []
    solid = None
    for rep in reps:
        for item in getattr(rep, "Items", None) or []:
            if item.is_a("IfcExtrudedAreaSolid"):
                solid = item
                break
        if solid:
            break
    if not solid:
        return None
    profile = getattr(solid, "SweptArea", None)
    if not profile or not profile.is_a("IfcRectangleProfileDef"):
        return None
    xdim = float(profile.XDim)
    ydim = float(profile.YDim)
    matrix = ifcopenshell.util.placement.get_local_placement(product.ObjectPlacement)
    corners = [
        (-xdim / 2.0, -ydim / 2.0, 0.0, 1.0),
        (xdim / 2.0, -ydim / 2.0, 0.0, 1.0),
        (xdim / 2.0, ydim / 2.0, 0.0, 1.0),
        (-xdim / 2.0, ydim / 2.0, 0.0, 1.0),
    ]
    xs: list[float] = []
    ys: list[float] = []
    for corner in corners:
        gx = sum(float(matrix[0][idx]) * corner[idx] for idx in range(4))
        gy = sum(float(matrix[1][idx]) * corner[idx] for idx in range(4))
        xs.append(gx)
        ys.append(gy)
    return min(xs), min(ys), max(xs), max(ys)


def _center_xy(product: Any) -> tuple[float, float] | None:
    try:
        matrix = ifcopenshell.util.placement.get_local_placement(product.ObjectPlacement)
    except Exception:
        return None
    return float(matrix[0][3]), float(matrix[1][3])


def _bbox_contains_point(bbox: tuple[float, float, float, float], x: float, y: float, tolerance: float = 0.08) -> bool:
    return bbox[0] - tolerance <= x <= bbox[2] + tolerance and bbox[1] - tolerance <= y <= bbox[3] + tolerance


def _bbox_axis_overlap(
    service: tuple[float, float],
    opening_bbox: tuple[float, float, float, float],
    wall_bbox: tuple[float, float, float, float],
    clearance: float = 0.22,
) -> bool:
    wall_width = wall_bbox[2] - wall_bbox[0]
    wall_depth = wall_bbox[3] - wall_bbox[1]
    if wall_width >= wall_depth:
        return opening_bbox[0] - clearance <= service[0] <= opening_bbox[2] + clearance
    return opening_bbox[1] - clearance <= service[1] <= opening_bbox[3] + clearance


def _fills_by_host_wall(model: ifcopenshell.file) -> dict[int, dict[str, list[Any]]]:
    result: dict[int, dict[str, list[Any]]] = {}
    for wall in model.by_type("IfcWall"):
        wall_result = {"doors": [], "windows": [], "openings": []}
        for rel in getattr(wall, "HasOpenings", None) or []:
            opening = rel.RelatedOpeningElement
            wall_result["openings"].append(opening)
            for fill_rel in getattr(opening, "HasFillings", None) or []:
                fill = fill_rel.RelatedBuildingElement
                if fill.is_a("IfcDoor"):
                    wall_result["doors"].append(fill)
                elif fill.is_a("IfcWindow"):
                    wall_result["windows"].append(fill)
        result[wall.id()] = wall_result
    return result


def _space_boundary_walls(model: ifcopenshell.file) -> dict[str, set[int]]:
    walls_by_room: dict[str, set[int]] = {}
    for boundary in model.by_type("IfcRelSpaceBoundary"):
        space = getattr(boundary, "RelatingSpace", None)
        wall = getattr(boundary, "RelatedBuildingElement", None)
        if not space or not wall or not wall.is_a("IfcWall"):
            continue
        walls_by_room.setdefault(_name(space), set()).add(wall.id())
    return walls_by_room


def _psets(entity: Any) -> dict[str, dict[str, Any]]:
    try:
        return ifcopenshell.util.element.get_psets(entity)
    except Exception:
        return {}


def run(ifc_path: Path, manifest_path: Path | None = None) -> dict[str, Any]:
    model = ifcopenshell.open(str(ifc_path))
    errors: list[str] = []
    warnings: list[str] = []
    rooms = {_name(space): space for space in model.by_type("IfcSpace")}
    missing_rooms = sorted(EXPECTED_ROOMS - set(rooms))
    if missing_rooms:
        errors.append(f"Missing expected rooms: {', '.join(missing_rooms)}.")

    manifest: dict[str, Any] = {}
    if manifest_path and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status") != EXPECTED_STATUS:
            errors.append(f"Unexpected manifest status: {manifest.get('status')!r}.")
    else:
        warnings.append("Manifest was not supplied; evidence status could not be checked.")

    doors_by_name = {_name(door): door for door in model.by_type("IfcDoor")}
    graph: dict[str, set[str]] = {room_name: set() for room_name in rooms}
    for door_name, (left_room, right_room) in EXPECTED_DOOR_CONNECTIONS.items():
        if door_name not in doors_by_name:
            errors.append(f"Missing required door/doorway fill: {door_name}.")
            continue
        if left_room not in rooms or right_room not in rooms:
            errors.append(f"{door_name}: references a missing room.")
            continue
        graph.setdefault(left_room, set()).add(right_room)
        graph.setdefault(right_room, set()).add(left_room)

    reachable: set[str] = set()
    pending = ["Entrance hall"] if "Entrance hall" in rooms else []
    while pending:
        current = pending.pop()
        if current in reachable:
            continue
        reachable.add(current)
        pending.extend(sorted(graph.get(current, set()) - reachable))
    for room_name in sorted(EXPECTED_ROOMS - {"Loggia"}):
        if room_name in rooms and room_name not in reachable:
            errors.append(f"{room_name}: no validated door-connected route from Entrance hall.")

    fills_by_wall = _fills_by_host_wall(model)
    boundary_walls = _space_boundary_walls(model)
    room_reports = []
    for room_name in sorted(EXPECTED_ROOMS & set(rooms)):
        wall_ids = boundary_walls.get(room_name, set())
        door_count = sum(len(fills_by_wall.get(wall_id, {}).get("doors", [])) for wall_id in wall_ids)
        window_count = sum(len(fills_by_wall.get(wall_id, {}).get("windows", [])) for wall_id in wall_ids)
        if room_name != "Loggia" and len(wall_ids) < 4:
            errors.append(f"{room_name}: only {len(wall_ids)} boundary walls; expected at least 4.")
        if room_name != "Loggia" and door_count < 1:
            errors.append(f"{room_name}: no native door/doorway fill found on boundary walls.")
        if room_name in WINDOW_REQUIRED and window_count < 1:
            errors.append(f"{room_name}: no native window fill found on boundary walls.")
        room_reports.append(
            {
                "room": room_name,
                "boundary_walls": len(wall_ids),
                "native_door_fills_on_boundary_walls": door_count,
                "native_window_fills_on_boundary_walls": window_count,
                "reachable_from_entrance": room_name in reachable,
                "window_required": room_name in WINDOW_REQUIRED,
            }
        )

    wall_by_name = {_name(wall): wall for wall in model.by_type("IfcWall")}
    wall_bboxes = {name: bbox for name, wall in wall_by_name.items() if (bbox := _product_bbox_xy(wall))}
    opening_bboxes_by_wall: dict[str, list[tuple[float, float, float, float]]] = {}
    for wall_name, wall in wall_by_name.items():
        for rel in getattr(wall, "HasOpenings", None) or []:
            bbox = _product_bbox_xy(rel.RelatedOpeningElement)
            if bbox:
                opening_bboxes_by_wall.setdefault(wall_name, []).append(bbox)

    service_reports = []
    for terminal in model.by_type("IfcFlowTerminal"):
        psets = _psets(terminal)
        if "Pset_DemoLightingCoordination" in psets:
            continue
        coordination = psets.get("Pset_DemoElectricalCoordination") or psets.get("Pset_DemoPlumbingCoordination")
        if not coordination:
            continue
        terminal_name = _name(terminal)
        host_wall = str(coordination.get("HostWall", "") or "")
        center = _center_xy(terminal)
        attached = False
        collides_opening = False
        if not host_wall:
            errors.append(f"{terminal_name}: missing HostWall coordination property.")
        elif host_wall not in wall_bboxes:
            errors.append(f"{terminal_name}: HostWall {host_wall!r} not found or has no bbox.")
        elif center:
            attached = _bbox_contains_point(wall_bboxes[host_wall], center[0], center[1], tolerance=0.09)
            if not attached:
                errors.append(f"{terminal_name}: not attached to declared host wall {host_wall}.")
            for opening_bbox in opening_bboxes_by_wall.get(host_wall, []):
                if _bbox_axis_overlap(center, opening_bbox, wall_bboxes[host_wall]):
                    collides_opening = True
                    errors.append(f"{terminal_name}: collides with or is too close to an opening on {host_wall}.")
                    break
        else:
            errors.append(f"{terminal_name}: placement could not be resolved.")
        service_reports.append(
            {
                "name": terminal_name,
                "host_wall": host_wall,
                "attached_to_host_wall": attached,
                "clear_of_openings": not collides_opening,
            }
        )

    light_fixtures = model.by_type("IfcLightFixture")
    if len(light_fixtures) < 7:
        errors.append(f"Expected at least 7 ceiling light fixtures, found {len(light_fixtures)}.")
    for fixture in light_fixtures:
        center = _center_xy(fixture)
        if center is None:
            errors.append(f"{_name(fixture)}: light fixture placement could not be resolved.")
            continue
        if not math.isfinite(center[0]) or not math.isfinite(center[1]):
            errors.append(f"{_name(fixture)}: invalid light fixture placement.")

    return {
        "source": str(ifc_path),
        "manifest": str(manifest_path) if manifest_path else None,
        "status": "valid" if not errors else "invalid",
        "errors": errors,
        "warnings": warnings,
        "rooms": room_reports,
        "services": service_reports,
        "counts": {
            "spaces": len(model.by_type("IfcSpace")),
            "walls": len(model.by_type("IfcWall")),
            "doors": len(model.by_type("IfcDoor")),
            "windows": len(model.by_type("IfcWindow")),
            "flow_terminals": len(model.by_type("IfcFlowTerminal")),
            "light_fixtures": len(light_fixtures),
            "space_boundaries": len(model.by_type("IfcRelSpaceBoundary")),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifc", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = run(args.ifc, args.manifest)
    text = json.dumps(result, indent=2)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    return 0 if result["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
