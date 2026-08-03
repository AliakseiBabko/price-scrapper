"""Validate and enrich the demonstrator IFC with wall-face boundaries.

This is deliberately a demonstrator gate, not a universal IFC validator.  It
uses the conventions of ``demo_apartment_layout.py`` (centred rectangular
wall profiles, local X = wall length, local Y = wall thickness) and refuses
to silently fall back when those conventions are not present.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import ifcopenshell
import ifcopenshell.api
import ifcopenshell.geom
import ifcopenshell.util.placement
import ifcopenshell.util.unit
import numpy as np


class QTOValidationError(RuntimeError):
    """A required demonstrator validation check failed."""


def mesh(model_settings: Any, product: Any) -> np.ndarray:
    shape: Any = ifcopenshell.geom.create_shape(model_settings, product)
    vertices = np.asarray(shape.geometry.verts, dtype=float).reshape((-1, 3))
    if len(vertices) == 0:
        raise QTOValidationError(f"{product.GlobalId} has empty geometry.")
    return vertices


def placement_matrix(product: Any, unit_scale: float) -> np.ndarray:
    placement = getattr(product, "ObjectPlacement", None)
    if not placement:
        return np.eye(4, dtype=float)
    result = np.asarray(ifcopenshell.util.placement.get_local_placement(placement), dtype=float)
    result[:3, 3] *= unit_scale
    return result


def wall_dimensions(wall: Any, unit_scale: float) -> tuple[float, float, float]:
    representation = getattr(wall, "Representation", None)
    for rep in getattr(representation, "Representations", []) or []:
        for item in rep.Items or []:
            if not item.is_a("IfcExtrudedAreaSolid"):
                continue
            profile = item.SweptArea
            if not (profile.is_a("IfcRectangleProfileDef") and hasattr(profile, "XDim")):
                continue
            if abs(float(getattr(profile.Position.Location, "Coordinates", (0, 0))[0])) > 1e-9:
                raise QTOValidationError(f"Wall {wall.Name} has a non-centred profile origin.")
            if abs(float(getattr(profile.Position.Location, "Coordinates", (0, 0))[1])) > 1e-9:
                raise QTOValidationError(f"Wall {wall.Name} has a non-centred profile origin.")
            return (
                float(profile.XDim) * unit_scale,
                float(item.Depth) * unit_scale,
                float(profile.YDim) * unit_scale,
            )
    raise QTOValidationError(f"Wall {wall.Name} lacks a rectangular extruded profile.")


def side_face(wall: Any, space: Any, length: float, height: float, thickness: float,
              settings: Any, unit_scale: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, str]:
    """Return face origin, tangent, up and side using the real space mesh."""
    wall_matrix = placement_matrix(wall, unit_scale)
    wall_inverse = np.linalg.inv(wall_matrix)
    space_vertices = mesh(settings, space)
    space_center = np.mean(space_vertices, axis=0)
    center_local = (wall_inverse @ np.append(space_center, 1.0))[:3]

    if abs(center_local[1]) < 1e-4:
        raise QTOValidationError(f"Space {space.Name} lies on the wall centre plane; side is ambiguous.")

    if center_local[1] > 0:
        side = "SIDE_A_POSITIVE_Y"
        local_origin = np.array([-length / 2, thickness / 2, 0, 1], dtype=float)
        local_tangent = np.array([1.0, 0.0, 0.0])
        local_normal = np.array([0.0, 1.0, 0.0])
    else:
        side = "SIDE_B_NEGATIVE_Y"
        local_origin = np.array([length / 2, -thickness / 2, 0, 1], dtype=float)
        local_tangent = np.array([-1.0, 0.0, 0.0])
        local_normal = np.array([0.0, -1.0, 0.0])

    rotation = wall_matrix[:3, :3]
    origin = (wall_matrix @ local_origin)[:3]
    tangent = rotation @ local_tangent
    normal = rotation @ local_normal
    tangent /= np.linalg.norm(tangent)
    normal /= np.linalg.norm(normal)
    up = np.cross(tangent, normal)
    up /= np.linalg.norm(up)
    if up[2] < 0.99:
        raise QTOValidationError(f"Wall {wall.Name} does not have a +Z up direction.")
    return origin, tangent, up, side


def project_opening(opening: Any, origin: np.ndarray, tangent: np.ndarray,
                    up: np.ndarray, length: float, height: float,
                    settings: Any) -> tuple[list[tuple[float, float]], float, float]:
    points = mesh(settings, opening)
    coords = np.column_stack(((points - origin) @ tangent, (points - origin) @ up))
    u_min, v_min = coords.min(axis=0)
    u_max, v_max = coords.max(axis=0)
    tolerance = 1e-4
    if u_min < -tolerance or u_max > length + tolerance or v_min < -tolerance or v_max > height + tolerance:
        raise QTOValidationError(
            f"Opening {opening.Name} is outside its wall face: "
            f"u=[{u_min:.3f},{u_max:.3f}], v=[{v_min:.3f},{v_max:.3f}]."
        )
    return [(u_min, v_min), (u_max, v_min), (u_max, v_max), (u_min, v_max)], u_max - u_min, v_max - v_min


def polygon_area(poly: list[tuple[float, float]]) -> float:
    return 0.5 * abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))))


def overlap(poly_a: list[tuple[float, float]], poly_b: list[tuple[float, float]]) -> bool:
    if polygon_area(poly_a) < 1e-8 or polygon_area(poly_b) < 1e-8:
        raise QTOValidationError("Degenerate projected opening polygon.")
    for poly in (poly_a, poly_b):
        for i, first in enumerate(poly):
            second = poly[(i + 1) % len(poly)]
            axis = np.array([-(second[1] - first[1]), second[0] - first[0]], dtype=float)
            axis /= np.linalg.norm(axis)
            a = [point[0] * axis[0] + point[1] * axis[1] for point in poly_a]
            b = [point[0] * axis[0] + point[1] * axis[1] for point in poly_b]
            if max(a) <= min(b) + 1e-4 or max(b) <= min(a) + 1e-4:
                return False
    return True


def audit_relationships(model: Any, wall: Any) -> None:
    for void in getattr(wall, "VoidsElements", []) or []:
        opening = void.RelatedOpeningElement
        if void.RelatingBuildingElement != wall or not opening or not opening.is_a("IfcOpeningElement"):
            raise QTOValidationError(f"Invalid void ownership on wall {wall.Name}.")
        fills = list(getattr(opening, "HasFillings", []) or [])
        if len(fills) > 1:
            raise QTOValidationError(f"Opening {opening.Name} has multiple filling relationships.")
        if fills:
            filling = fills[0].RelatedBuildingElement
            if not (filling and (filling.is_a("IfcDoor") or filling.is_a("IfcWindow"))):
                raise QTOValidationError(f"Opening {opening.Name} has an invalid filling.")


def run(source: Path, output: Path, schedule_path: Path | None = None) -> dict:
    model = ifcopenshell.open(str(source))
    unit_scale = ifcopenshell.util.unit.calculate_unit_scale(model)
    if unit_scale <= 0:
        raise QTOValidationError("Invalid IFC unit scale.")
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)
    schedule = json.loads(schedule_path.read_text(encoding="utf-8")) if schedule_path else None
    boundaries = model.by_type("IfcRelSpaceBoundary")
    walls = model.by_type("IfcWall", include_subtypes=True)
    openings = model.by_type("IfcOpeningElement")
    if not boundaries or not walls or not openings:
        raise QTOValidationError("Model is missing walls, openings, or space boundaries.")
    if len(model.by_type("IfcRelVoidsElement")) != len(openings):
        raise QTOValidationError("Every demonstrator opening must have one void relationship.")

    covered_spaces: set[str] = set()
    wall_reports = []
    for wall in walls:
        audit_relationships(model, wall)

    for boundary in boundaries:
        wall = boundary.RelatedBuildingElement
        space = boundary.RelatingSpace
        length, height, thickness = wall_dimensions(wall, unit_scale)
        origin, tangent, up, side = side_face(wall, space, length, height, thickness, settings, unit_scale)
        polygons = []
        opening_rows = []
        for relation in getattr(wall, "HasOpenings", []) or []:
            opening = relation.RelatedOpeningElement
            poly, width, opening_height = project_opening(opening, origin, tangent, up, length, height, settings)
            polygons.append(poly)
            opening_rows.append({"name": opening.Name, "width_m": round(width, 4), "height_m": round(opening_height, 4), "side": side})
        for index, first in enumerate(polygons):
            for second in polygons[index + 1:]:
                if overlap(first, second):
                    raise QTOValidationError(f"Openings overlap on wall {wall.Name}.")

        space_name = str(space.Name or "")
        covered_spaces.add(space_name)
        space_matrix = placement_matrix(space, unit_scale)
        space_inverse = np.linalg.inv(space_matrix)
        local_origin = (space_inverse @ np.append(origin, 1.0))[:3]
        local_normal = space_matrix[:3, :3].T @ (np.cross(tangent, up))
        local_tangent = space_matrix[:3, :3].T @ tangent
        if np.linalg.norm(local_normal) == 0 or np.linalg.norm(local_tangent) == 0:
            raise QTOValidationError(f"Invalid boundary basis for {boundary.GlobalId}.")
        ifcopenshell.api.run(
            "boundary.assign_connection_geometry", model,
            rel_space_boundary=boundary,
            outer_boundary=[(0.0, 0.0), (length, 0.0), (length, height), (0.0, height)],
            inner_boundaries=polygons,
            location=list(local_origin), axis=list(local_normal), ref_direction=list(local_tangent),
        )
        wall_reports.append({"wall": wall.Name, "space": space_name, "side": side, "openings": opening_rows})

    schedule_status = "SKIPPED_NO_SCHEDULE_PROVIDED"
    if schedule is not None:
        missing = sorted(name for name in covered_spaces if name and name not in schedule)
        if missing:
            raise QTOValidationError(f"Missing finish schedule entries: {', '.join(missing)}")
        schedule_status = "VERIFIED"

    output.parent.mkdir(parents=True, exist_ok=True)
    model.write(str(output))
    reopened = ifcopenshell.open(str(output))
    for boundary in reopened.by_type("IfcRelSpaceBoundary"):
        geometry = boundary.ConnectionGeometry
        if not geometry or not geometry.SurfaceOnRelatingElement:
            raise QTOValidationError(f"ConnectionGeometry did not persist for {boundary.GlobalId}.")
    return {"source": str(source), "output": str(output), "unit_scale": unit_scale, "wall_count": len(walls), "opening_count": len(openings), "boundary_count": len(boundaries), "schedule_status": schedule_status, "wall_reports": wall_reports, "status": "PASSED_GEOMETRY_REVIEW_REQUIRED"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("data/outputs/demo/generic_enclosed_apartment.ifc"))
    parser.add_argument("--output", type=Path, default=Path("data/outputs/demo/generic_enclosed_apartment_validated.ifc"))
    parser.add_argument("--finish-schedule", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(run(args.source, args.output, args.finish_schedule), indent=2))
    except Exception as error:
        print(json.dumps({"status": "BLOCKED", "error": str(error)}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
