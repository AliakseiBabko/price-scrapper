"""Calculate host-wall finish quantities and wall-elevation SVGs.

This is intentionally conservative: it reports the source of every dimension
and leaves room-side finishes unassigned when IFC boundaries or an explicit
finish schedule are unavailable.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
from pathlib import Path
from typing import Any

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element
import ifcopenshell.util.placement
import numpy as np


def solids(product):
    representation = getattr(product, "Representation", None)
    if not representation:
        return []
    result = []
    for shape_rep in representation.Representations or []:
        result.extend(item for item in shape_rep.Items or [] if item.is_a("IfcExtrudedAreaSolid"))
    return result


def placement_matrix(product):
    return np.asarray(ifcopenshell.util.placement.get_local_placement(product.ObjectPlacement), dtype=float)


def simple_dimensions(product):
    """Return local width/depth/height for a rectangular extruded product."""
    items = solids(product)
    if not items:
        return None
    solid = items[0]
    profile = solid.SweptArea
    if not (hasattr(profile, "XDim") and hasattr(profile, "YDim")):
        return None
    return {
        "local_x_m": float(profile.XDim),
        "local_y_m": float(profile.YDim),
        "height_m": float(solid.Depth),
        "source": "IfcExtrudedAreaSolid/IfcRectangleProfileDef",
    }


def mesh_dimensions(product, settings):
    # IfcOpenShell exposes multiple runtime geometry wrapper variants through
    # one factory, while its stubs do not describe the shared `.geometry`
    # property consistently. Keep this dynamic boundary narrow for Pylance.
    shape: Any = ifcopenshell.geom.create_shape(settings, product)
    verts = np.asarray(shape.geometry.verts, dtype=float).reshape((-1, 3))
    if len(verts) == 0:
        return None
    low, high = verts.min(axis=0), verts.max(axis=0)
    return {
        "local_x_m": float(high[0] - low[0]),
        "local_y_m": float(high[1] - low[1]),
        "height_m": float(high[2] - low[2]),
        "source": "tessellated-world-bounding-box-fallback",
    }


def dimensions(product, settings):
    return simple_dimensions(product) or mesh_dimensions(product, settings)


def local_center(host, opening):
    relative = np.linalg.inv(placement_matrix(host)) @ placement_matrix(opening)
    return float(relative[0, 3]), float(relative[1, 3])


def finish_schedule(path: Path | None) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path else {}


def adjacent_rooms(model, wall):
    names = []
    for boundary in getattr(wall, "ProvidesBoundaries", []) or []:
        space = getattr(boundary, "RelatingSpace", None)
        if space and getattr(space, "Name", None):
            names.append(str(space.Name))
    return list(dict.fromkeys(names))


def infer_rooms_from_rectangles(model, wall):
    """Fallback adjacency for our rectangular demonstrator spaces."""
    wall_dims = simple_dimensions(wall)
    if not wall_dims:
        return []
    wall_matrix = placement_matrix(wall)
    origin = wall_matrix[:3, 3]
    wall_length = max(wall_dims["local_x_m"], wall_dims["local_y_m"])
    wall_thickness = min(wall_dims["local_x_m"], wall_dims["local_y_m"])
    wall_angle = math.atan2(wall_matrix[1, 0], wall_matrix[0, 0])
    wall_axis = np.array([math.cos(wall_angle), math.sin(wall_angle)])
    names = []
    for space in model.by_type("IfcSpace"):
        dims = simple_dimensions(space)
        if not dims:
            continue
        sm = placement_matrix(space)
        sx, sy = dims["local_x_m"], dims["local_y_m"]
        # The demonstrator's rectangular profiles are centered on their local
        # placements, so convert the placement center to a lower-left corner.
        sc = sm[:2, 3] - np.array([sx / 2.0, sy / 2.0])
        # The demonstrator spaces are axis-aligned. Test wall endpoints and
        # room rectangle proximity without claiming this is a general solver.
        corners = np.array([[sc[0], sc[1]], [sc[0] + sx, sc[1]], [sc[0], sc[1] + sy], [sc[0] + sx, sc[1] + sy]])
        distances = np.abs((corners - origin[:2]) @ np.array([-wall_axis[1], wall_axis[0]]))
        along = (corners - origin[:2]) @ wall_axis
        if distances.min() <= wall_thickness + 0.2 and along.max() >= -0.2 and along.min() <= wall_length + 0.2:
            if getattr(space, "Name", None):
                names.append(str(space.Name))
    return list(dict.fromkeys(names))


def calculate(ifc_path: Path, schedule_path: Path | None = None) -> dict:
    model = ifcopenshell.open(str(ifc_path))
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    schedule = finish_schedule(schedule_path)
    rows = []
    walls = model.by_type("IfcWall", include_subtypes=True)
    for wall in walls:
        dims = dimensions(wall, settings)
        if not dims:
            continue
        psets = ifcopenshell.util.element.get_psets(wall)
        qto = psets.get("Qto_WallBaseQuantities", {})
        length = float(qto.get("Length", max(dims["local_x_m"], dims["local_y_m"])))
        height = float(qto.get("Height", dims["height_m"]))
        gross = float(qto.get("GrossSideArea", length * height))
        rooms = adjacent_rooms(model, wall)
        adjacency_source = "IfcRelSpaceBoundary" if rooms else "rectangular-space-fallback"
        if not rooms:
            rooms = infer_rooms_from_rectangles(model, wall)
        openings = []
        deducted = 0.0
        for relation in getattr(wall, "HasOpenings", []) or []:
            opening = relation.RelatedOpeningElement
            op_dims = dimensions(opening, settings)
            if not op_dims:
                continue
            width = max(op_dims["local_x_m"], op_dims["local_y_m"])
            opening_height = op_dims["height_m"]
            center_x, center_y = local_center(wall, opening)
            # Host and opening extrusions use centered profiles. Report the
            # station from the wall's start, rather than the relative center
            # of the host profile.
            center_x += max(dims["local_x_m"], dims["local_y_m"]) / 2.0
            filling = "Unfilled Opening"
            for fill in getattr(opening, "HasFillings", []) or []:
                if fill.RelatedBuildingElement:
                    filling = fill.RelatedBuildingElement.is_a()
            area = width * opening_height
            deducted += area
            openings.append({
                "opening_guid": opening.GlobalId,
                "type": filling,
                "width_m": round(width, 3),
                "height_m": round(opening_height, 3),
                "center_along_wall_m": round(center_x, 3),
                "bottom_m": round(float(placement_matrix(opening)[2, 3]), 3),
                "area_m2": round(area, 3),
            })
        net = max(0.0, gross - deducted)
        sides = []
        for room in (rooms[:2] or ["Unassigned"]):
            sides.append({
                "room_name": room,
                "net_finish_area_m2": round(net, 3),
                "finish": schedule.get(room, {"trade": "unassigned", "material": "unassigned"}),
            })
        rows.append({
            "wall_guid": wall.GlobalId,
            "wall_name": wall.Name or "Unnamed wall",
            "length_m": round(length, 3),
            "height_m": round(height, 3),
            "gross_face_area_m2": round(gross, 3),
            "deducted_opening_area_m2": round(deducted, 3),
            "net_face_area_m2": round(net, 3),
            "dimensions_source": dims["source"],
            "adjacency_source": adjacency_source,
            "adjacent_rooms": rooms,
            "sides": sides,
            "openings": openings,
        })
    return {"source": str(ifc_path), "wall_count": len(rows), "walls": rows, "status": "quantity_estimate_requires_review"}


def render_svg(row: dict, destination: Path, scale: int = 100):
    width, height = row["length_m"] * scale, row["height_m"] * scale
    opening_svg = []
    for opening in row["openings"]:
        x = (opening["center_along_wall_m"] - opening["width_m"] / 2) * scale
        y = height - (opening["bottom_m"] + opening["height_m"]) * scale
        opening_svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{opening["width_m"] * scale:.1f}" height="{opening["height_m"] * scale:.1f}" class="void"/>')
        label = html.escape(f'{opening["type"]} {opening["width_m"]:.2f} x {opening["height_m"]:.2f} m')
        opening_svg.append(f'<text x="{x + 5:.1f}" y="{y + 18:.1f}" class="label">{label}</text>')
    title = html.escape(row["wall_name"])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width + 220:.0f}" height="{height + 100:.0f}" viewBox="-110 -60 {width + 220:.0f} {height + 100:.0f}">
<style>.wall {{ fill:#d9d9d9; stroke:#111; stroke-width:2; }} .void {{ fill:#fff; stroke:#c00; stroke-width:2; stroke-dasharray:5 3; }} .label {{ font:12px sans-serif; fill:#111; }} </style>
<text x="0" y="-25" class="label">Wall elevation: {title}</text>
<rect x="0" y="0" width="{width:.1f}" height="{height:.1f}" class="wall"/>
{''.join(opening_svg)}
<text x="0" y="{height + 35:.1f}" class="label">Gross {row["gross_face_area_m2"]:.2f} m2 | Openings -{row["deducted_opening_area_m2"]:.2f} m2 | Net {row["net_face_area_m2"]:.2f} m2</text>
</svg>'''
    destination.write_text(svg, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--finish-schedule", type=Path)
    parser.add_argument("--svg-dir", type=Path)
    args = parser.parse_args()
    report = calculate(args.source, args.finish_schedule)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.svg_dir:
        args.svg_dir.mkdir(parents=True, exist_ok=True)
        for index, row in enumerate(report["walls"], 1):
            render_svg(row, args.svg_dir / f"wall_{index:03d}.svg")
    print(json.dumps({"wall_count": report["wall_count"], "output": str(args.output), "status": report["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
