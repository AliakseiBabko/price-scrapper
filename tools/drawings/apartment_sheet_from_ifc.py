"""Generate an A3 coordination floor-plan sheet from the apartment IFC.

The output is a deterministic SVG/PDF drawing for checking the OpenBIM flow. It
is not a licensed construction drawing and remains labelled accordingly.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.placement
import ifcopenshell.util.unit

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

PROJECT_NAME = "Dubravinsky"

# Sheets are bilingual: the contractor reads the Russian, the owner reads both.
RU = {
    "kitchen": "Кухня", "living": "Гостиная", "kids": "Детская", "bedroom": "Спальня",
    "hallway": "Коридор", "corridor": "Коридор", "entrance": "Прихожая",
    "bathroom": "Ванная", "wc": "Туалет", "combined_bath": "Санузел",
    "laundry": "Постирочная", "balcony": "Балкон", "storage": "Кладовая", "other": "Помещение",
}
WET_ROLES = {"kitchen", "bathroom", "wc", "combined_bath", "laundry"}
ROLE_FILL = {
    "wet": "#dceaf5", "living": "#f4f4f2", "circulation": "#ecebe7",
    "balcony": "#f7f7f7", "other": "#f4f4f2",
}
PHASE_STYLE = {
    "existing": ("#3a3a3a", "none"),
    "demolished": ("#c23b3b", "1.4 1.0"),
    "new": ("#1c6ea4", "none"),
    "modified": ("#8a6d1f", "none"),
}


def role_fill(role: str) -> str:
    if role in WET_ROLES:
        return ROLE_FILL["wet"]
    if role in {"entrance", "hallway", "corridor"}:
        return ROLE_FILL["circulation"]
    if role == "balcony":
        return ROLE_FILL["balcony"]
    return ROLE_FILL["living"]


def bilingual(name: str, role: str) -> str:
    """`Кухня / Kitchen` - Russian first, because the builder reads that one."""
    ru = RU.get(role)
    return f"{ru} / {name}" if ru and ru.lower() != name.lower() else name


SHEET_CONFIG = {
    "combined": {
        "sheet_number": "A-101",
        "title": "Floor plan - coordination",
        "stem": "apartment_floor_plan_a3",
        "electrical": True,
        "plumbing": True,
        "lighting": True,
    },
    "architectural": {
        "sheet_number": "A-101",
        "title": "Architectural floor plan",
        "stem": "apartment_architectural_plan_a3",
        "electrical": False,
        "plumbing": False,
        "lighting": False,
    },
    "electrical": {
        "sheet_number": "E-101",
        "title": "Electrical and lighting coordination plan",
        "stem": "apartment_electrical_lighting_plan_a3",
        "electrical": True,
        "plumbing": False,
        "lighting": True,
    },
    "plumbing": {
        "sheet_number": "P-101",
        "title": "Plumbing coordination plan",
        "stem": "apartment_plumbing_plan_a3",
        "electrical": False,
        "plumbing": True,
        "lighting": False,
    },
}


@dataclass(frozen=True)
class BBox:
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    zmin: float
    zmax: float

    @property
    def width(self) -> float:
        return self.xmax - self.xmin

    @property
    def depth(self) -> float:
        return self.ymax - self.ymin

    @property
    def cx(self) -> float:
        return (self.xmin + self.xmax) / 2.0

    @property
    def cy(self) -> float:
        return (self.ymin + self.ymax) / 2.0


@dataclass(frozen=True)
class Item:
    kind: str
    name: str
    global_id: str
    bbox: BBox
    host_wall: str | None = None


@dataclass(frozen=True)
class ServiceSymbol:
    service: str
    name: str
    room: str
    x: float
    y: float
    wall: str
    side: str


@dataclass(frozen=True)
class LightSymbol:
    name: str
    room: str
    x: float
    y: float


class SheetError(RuntimeError):
    pass


def svg_el(tag: str, **attrs: Any) -> ET.Element:
    return ET.Element(f"{{{SVG_NS}}}{tag}", {key: str(value) for key, value in attrs.items()})


def append_text(parent: ET.Element, value: str, x: float, y: float, size: float = 3.0,
                anchor: str = "start", weight: str = "normal", klass: str | None = None,
                fill: str | None = None) -> ET.Element:
    attrs: dict[str, Any] = {
        "x": f"{x:.3f}",
        "y": f"{y:.3f}",
        "font-size": f"{size:.3f}",
        "font-family": "Arial, sans-serif",
        "text-anchor": anchor,
        "font-weight": weight,
    }
    if klass:
        attrs["class"] = klass
    if fill:
        attrs["fill"] = fill
    node = svg_el("text", **attrs)
    node.text = value
    parent.append(node)
    return node


def placement_matrix(product: Any, unit_scale: float) -> list[list[float]]:
    object_placement = getattr(product, "ObjectPlacement", None)
    if not object_placement:
        return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    matrix = ifcopenshell.util.placement.get_local_placement(object_placement).tolist()
    matrix[0][3] *= unit_scale
    matrix[1][3] *= unit_scale
    matrix[2][3] *= unit_scale
    return matrix


def transform(matrix: list[list[float]], point: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = point
    return (
        matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z + matrix[0][3],
        matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z + matrix[1][3],
        matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z + matrix[2][3],
    )


def rectangular_profile_bbox(product: Any, unit_scale: float) -> BBox:
    representation = getattr(product, "Representation", None)
    if not representation:
        raise SheetError(f"{product.is_a()} {product.Name} has no representation.")
    for shape_rep in representation.Representations or []:
        for body_item in shape_rep.Items or []:
            if not body_item.is_a("IfcExtrudedAreaSolid"):
                continue
            profile = body_item.SweptArea
            if not profile.is_a("IfcRectangleProfileDef"):
                continue
            xdim = float(profile.XDim) * unit_scale
            ydim = float(profile.YDim) * unit_scale
            depth = float(body_item.Depth) * unit_scale
            matrix = placement_matrix(product, unit_scale)
            local = [
                (-xdim / 2.0, -ydim / 2.0, 0.0),
                (xdim / 2.0, -ydim / 2.0, 0.0),
                (xdim / 2.0, ydim / 2.0, 0.0),
                (-xdim / 2.0, ydim / 2.0, 0.0),
                (-xdim / 2.0, -ydim / 2.0, depth),
                (xdim / 2.0, -ydim / 2.0, depth),
                (xdim / 2.0, ydim / 2.0, depth),
                (-xdim / 2.0, ydim / 2.0, depth),
            ]
            world = [transform(matrix, point) for point in local]
            return BBox(
                min(p[0] for p in world),
                min(p[1] for p in world),
                max(p[0] for p in world),
                max(p[1] for p in world),
                min(p[2] for p in world),
                max(p[2] for p in world),
            )
    raise SheetError(f"{product.is_a()} {product.Name} lacks rectangular extrusion geometry.")


def collect_items(model: ifcopenshell.file) -> tuple[list[Item], list[Item], list[Item], list[Item], list[Item]]:
    unit_scale = ifcopenshell.util.unit.calculate_unit_scale(model)
    walls = [
        Item("wall", str(wall.Name or "Wall"), wall.GlobalId, rectangular_profile_bbox(wall, unit_scale))
        for wall in model.by_type("IfcWall")
    ]
    spaces = [
        Item("space", str(space.Name or "Space"), space.GlobalId, rectangular_profile_bbox(space, unit_scale))
        for space in model.by_type("IfcSpace")
    ]
    doors = [
        Item("door", str(door.Name or "Door"), door.GlobalId, rectangular_profile_bbox(door, unit_scale))
        for door in model.by_type("IfcDoor")
    ]
    windows = [
        Item("window", str(window.Name or "Window"), window.GlobalId, rectangular_profile_bbox(window, unit_scale))
        for window in model.by_type("IfcWindow")
    ]
    openings: list[Item] = []
    for wall in model.by_type("IfcWall"):
        for relation in getattr(wall, "HasOpenings", []) or []:
            opening = relation.RelatedOpeningElement
            openings.append(
                Item(
                    "opening",
                    str(opening.Name or "Opening"),
                    opening.GlobalId,
                    rectangular_profile_bbox(opening, unit_scale),
                    host_wall=str(wall.Name or ""),
                )
            )
    return walls, spaces, openings, doors, windows


def collect_flow_terminals(model: ifcopenshell.file) -> list[ServiceSymbol]:
    unit_scale = ifcopenshell.util.unit.calculate_unit_scale(model)
    symbols: list[ServiceSymbol] = []
    for terminal in model.by_type("IfcFlowTerminal"):
        psets = ifcopenshell.util.element.get_psets(terminal)
        if "Pset_DemoElectricalCoordination" in psets:
            service = "electrical"
            coordination = psets["Pset_DemoElectricalCoordination"]
        elif "Pset_DemoPlumbingCoordination" in psets:
            service = "plumbing"
            coordination = psets["Pset_DemoPlumbingCoordination"]
        else:
            continue
        room = str(coordination.get("Room") or "Unassigned")
        wall = str(coordination.get("HostWall") or "Unassigned")
        box = rectangular_profile_bbox(terminal, unit_scale)
        side = "horizontal" if box.width >= box.depth else "vertical"
        symbols.append(ServiceSymbol(service, str(terminal.Name or "Service terminal"), room, box.cx, box.cy, wall, side))
    return symbols


def collect_light_fixtures(model: ifcopenshell.file) -> list[LightSymbol]:
    unit_scale = ifcopenshell.util.unit.calculate_unit_scale(model)
    lights: list[LightSymbol] = []
    for fixture in model.by_type("IfcLightFixture"):
        psets = ifcopenshell.util.element.get_psets(fixture)
        coordination = psets.get("Pset_DemoLightingCoordination", {})
        box = rectangular_profile_bbox(fixture, unit_scale)
        lights.append(LightSymbol(str(fixture.Name or "Light fixture"), str(coordination.get("Room") or "Unassigned"), box.cx, box.cy))
    return lights


def union_bbox(items: list[Item]) -> BBox:
    if not items:
        raise SheetError("No geometry to draw.")
    return BBox(
        min(item.bbox.xmin for item in items),
        min(item.bbox.ymin for item in items),
        max(item.bbox.xmax for item in items),
        max(item.bbox.ymax for item in items),
        min(item.bbox.zmin for item in items),
        max(item.bbox.zmax for item in items),
    )


def is_horizontal(bbox: BBox) -> bool:
    return bbox.width >= bbox.depth


def overlaps_interval(a0: float, a1: float, b0: float, b1: float, clearance: float = 0.0) -> bool:
    return max(a0, b0 - clearance) <= min(a1, b1 + clearance)


def wall_for_candidate(candidate: tuple[float, float], side: str, walls: list[Item]) -> tuple[Item, float, float]:
    """Nearest wall on the given side, or None when there is nothing to hang on.

    These symbols are placeholders placed by a heuristic, not designed
    positions. On a CAD-derived model with fragmentary walls some candidates
    have no wall to snap to, and losing one placeholder socket is not a reason
    to lose the whole drawing.
    """
    x, y = candidate
    best: tuple[float, Item, float, float] | None = None
    for wall in walls:
        box = wall.bbox
        if side in {"bottom", "top"} and is_horizontal(box):
            if box.xmin - 0.05 <= x <= box.xmax + 0.05:
                distance = abs(y - box.cy)
                if best is None or distance < best[0]:
                    best = (distance, wall, x, box.cy)
        if side in {"left", "right"} and not is_horizontal(box):
            if box.ymin - 0.05 <= y <= box.ymax + 0.05:
                distance = abs(x - box.cx)
                if best is None or distance < best[0]:
                    best = (distance, wall, box.cx, y)
    if best is None:
        return None
    return best[1], best[2], best[3]


def collides_with_opening(x: float, y: float, wall: Item, openings: list[Item], clearance: float = 0.22) -> bool:
    for opening in openings:
        if opening.host_wall != wall.name:
            continue
        box = opening.bbox
        if is_horizontal(wall.bbox):
            if abs(y - wall.bbox.cy) <= wall.bbox.depth / 2.0 + 0.05:
                if overlaps_interval(x, x, box.xmin, box.xmax, clearance):
                    return True
        else:
            if abs(x - wall.bbox.cx) <= wall.bbox.width / 2.0 + 0.05:
                if overlaps_interval(y, y, box.ymin, box.ymax, clearance):
                    return True
    return False


def symbol_is_on_host_wall(symbol: ServiceSymbol, wall: Item, tolerance: float = 0.06) -> bool:
    box = wall.bbox
    if is_horizontal(box):
        return box.xmin - tolerance <= symbol.x <= box.xmax + tolerance and abs(symbol.y - box.cy) <= box.depth / 2.0 + tolerance
    return box.ymin - tolerance <= symbol.y <= box.ymax + tolerance and abs(symbol.x - box.cx) <= box.width / 2.0 + tolerance


def room_electrical_positions(room: Item) -> list[tuple[str, float]]:
    key = room.name.lower()
    if "entrance" in key:
        return [("bottom", 0.25), ("bottom", 0.78)]
    if "living" in key:
        return [("bottom", 0.18), ("bottom", 0.78), ("right", 0.62)]
    if "bedroom" in key:
        return [("bottom", 0.25), ("bottom", 0.75)]
    if "kitchen" in key:
        return [("top", 0.2), ("top", 0.7), ("left", 0.25)]
    return [("top", 0.18)]


def candidate_point(room: Item, side: str, fraction: float) -> tuple[float, float]:
    box = room.bbox
    if side == "bottom":
        return box.xmin + box.width * fraction, box.ymin
    if side == "top":
        return box.xmin + box.width * fraction, box.ymax
    if side == "left":
        return box.xmin, box.ymin + box.depth * fraction
    if side == "right":
        return box.xmax, box.ymin + box.depth * fraction
    raise SheetError(f"Unsupported room side: {side}")


skipped_symbols: list[str] = []


def electrical_symbols(spaces: list[Item], walls: list[Item], openings: list[Item]) -> list[ServiceSymbol]:
    alternates = [("bottom", 0.35), ("top", 0.35), ("left", 0.5), ("right", 0.5), ("bottom", 0.65), ("top", 0.65)]
    symbols: list[ServiceSymbol] = []
    for room in sorted(spaces, key=lambda item: item.name):
        for index, (side, fraction) in enumerate(room_electrical_positions(room), 1):
            placed = False
            for candidate_side, candidate_fraction in [(side, fraction)] + alternates:
                snapped = wall_for_candidate(
                    candidate_point(room, candidate_side, candidate_fraction), candidate_side, walls)
                if snapped is None:
                    continue
                wall, x, y = snapped
                if not collides_with_opening(x, y, wall, openings):
                    symbols.append(ServiceSymbol("electrical", f"{room.name} outlet {index}",
                                                 room.name, x, y, wall.name, candidate_side))
                    placed = True
                    break
            if not placed:
                # A placeholder that will not sit anywhere is dropped and
                # reported. Losing one heuristic socket must not lose the sheet.
                skipped_symbols.append(f"{room.name} outlet {index}")
    return symbols


def project_point(x: float, y: float, origin: BBox, scale: float, px: float, py: float, drawing_h: float) -> tuple[float, float]:
    return px + (x - origin.xmin) * scale, py + drawing_h - (y - origin.ymin) * scale


def rect_attrs(box: BBox, origin: BBox, scale: float, px: float, py: float, drawing_h: float) -> dict[str, str]:
    x0, y1 = project_point(box.xmin, box.ymin, origin, scale, px, py, drawing_h)
    x1, y0 = project_point(box.xmax, box.ymax, origin, scale, px, py, drawing_h)
    return {"x": f"{x0:.3f}", "y": f"{y0:.3f}", "width": f"{x1 - x0:.3f}", "height": f"{y1 - y0:.3f}"}


def add_dimension(parent: ET.Element, p0: tuple[float, float], p1: tuple[float, float], label: str,
                  text_offset: tuple[float, float] = (0.0, -2.0)) -> None:
    parent.append(svg_el("line", x1=f"{p0[0]:.3f}", y1=f"{p0[1]:.3f}", x2=f"{p1[0]:.3f}", y2=f"{p1[1]:.3f}", **{"class": "dimension"}))
    append_text(parent, label, (p0[0] + p1[0]) / 2.0 + text_offset[0], (p0[1] + p1[1]) / 2.0 + text_offset[1], 3.0, "middle")


def draw_door(parent: ET.Element, opening: Item, origin: BBox, scale: float, px: float, py: float, drawing_h: float) -> None:
    box = opening.bbox
    if is_horizontal(box):
        hinge_x, hinge_y = project_point(box.xmin, box.cy, origin, scale, px, py, drawing_h)
        leaf_x, leaf_y = project_point(box.xmax, box.cy, origin, scale, px, py, drawing_h)
        radius = abs(leaf_x - hinge_x)
        parent.append(svg_el("line", x1=f"{hinge_x:.3f}", y1=f"{hinge_y:.3f}", x2=f"{leaf_x:.3f}", y2=f"{hinge_y:.3f}", **{"class": "door-leaf"}))
        parent.append(svg_el("path", d=f"M {hinge_x:.3f} {hinge_y:.3f} A {radius:.3f} {radius:.3f} 0 0 0 {hinge_x:.3f} {hinge_y - radius:.3f}", **{"class": "door-arc"}))
    else:
        hinge_x, hinge_y = project_point(box.cx, box.ymin, origin, scale, px, py, drawing_h)
        leaf_x, leaf_y = project_point(box.cx, box.ymax, origin, scale, px, py, drawing_h)
        radius = abs(leaf_y - hinge_y)
        parent.append(svg_el("line", x1=f"{hinge_x:.3f}", y1=f"{hinge_y:.3f}", x2=f"{hinge_x:.3f}", y2=f"{leaf_y:.3f}", **{"class": "door-leaf"}))
        parent.append(svg_el("path", d=f"M {hinge_x:.3f} {hinge_y:.3f} A {radius:.3f} {radius:.3f} 0 0 1 {hinge_x + radius:.3f} {hinge_y:.3f}", **{"class": "door-arc"}))


def draw_window(parent: ET.Element, opening: Item, origin: BBox, scale: float, px: float, py: float, drawing_h: float) -> None:
    box = opening.bbox
    if is_horizontal(box):
        x0, y = project_point(box.xmin, box.cy, origin, scale, px, py, drawing_h)
        x1, _ = project_point(box.xmax, box.cy, origin, scale, px, py, drawing_h)
        parent.append(svg_el("line", x1=f"{x0:.3f}", y1=f"{y - 1.2:.3f}", x2=f"{x1:.3f}", y2=f"{y - 1.2:.3f}", **{"class": "window-line"}))
        parent.append(svg_el("line", x1=f"{x0:.3f}", y1=f"{y + 1.2:.3f}", x2=f"{x1:.3f}", y2=f"{y + 1.2:.3f}", **{"class": "window-line"}))
    else:
        x, y0 = project_point(box.cx, box.ymin, origin, scale, px, py, drawing_h)
        _, y1 = project_point(box.cx, box.ymax, origin, scale, px, py, drawing_h)
        parent.append(svg_el("line", x1=f"{x - 1.2:.3f}", y1=f"{y0:.3f}", x2=f"{x - 1.2:.3f}", y2=f"{y1:.3f}", **{"class": "window-line"}))
        parent.append(svg_el("line", x1=f"{x + 1.2:.3f}", y1=f"{y0:.3f}", x2=f"{x + 1.2:.3f}", y2=f"{y1:.3f}", **{"class": "window-line"}))


def read_phase(product) -> str:
    """The phase property, so a wall can be drawn as what it is."""
    try:
        import ifcopenshell.util.element as _el
        psets = _el.get_psets(product)
    except Exception:
        return "existing"
    return str((psets.get("Pset_ApartmentPhase") or {}).get("Phase", "existing"))


def build_svg(ifc_path: Path, manifest_path: Path | None, output_svg: Path, output_pdf: Path | None, sheet_kind: str = "combined") -> dict[str, Any]:
    config = SHEET_CONFIG[sheet_kind]
    model = ifcopenshell.open(str(ifc_path))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) \
        if manifest_path and manifest_path.is_file() else {}
    wall_phase = {str(w.Name or ""): read_phase(w) for w in model.by_type("IfcWall")}
    walls, spaces, openings, doors, windows = collect_items(model)
    symbols = collect_flow_terminals(model)
    light_symbols = collect_light_fixtures(model)
    # A model that contains no sockets must not gain sockets by being drawn.
    # This used to fabricate a placeholder per room when the model had none,
    # which put positions on a drawing that nobody had decided.
    electrical_source = "native_ifc_flow_terminals" if symbols else "none_in_model"
    for symbol in symbols:
        host_wall = next((wall for wall in walls if wall.name == symbol.wall), None)
        if not host_wall:
            raise SheetError(f"{symbol.name} references missing host wall {symbol.wall}.")
        if not symbol_is_on_host_wall(symbol, host_wall):
            raise SheetError(f"{symbol.name} is not mounted on host wall {symbol.wall}.")
        if host_wall and collides_with_opening(symbol.x, symbol.y, host_wall, openings):
            raise SheetError(f"{symbol.name} overlaps a door/window opening on {symbol.wall}.")
    visible_symbols = [
        symbol for symbol in symbols
        if (symbol.service == "electrical" and config["electrical"]) or (symbol.service == "plumbing" and config["plumbing"])
    ]
    visible_lights = light_symbols if config["lighting"] else []
    for light in light_symbols:
        containing_space = next((space for space in spaces if space.bbox.xmin <= light.x <= space.bbox.xmax and space.bbox.ymin <= light.y <= space.bbox.ymax), None)
        if not containing_space:
            raise SheetError(f"{light.name} is not inside any room footprint.")
    envelope = union_bbox(walls)
    page_w, page_h = 420.0, 297.0
    plan_x, plan_y, plan_w, plan_h = 24.0, 34.0, 260.0, 205.0
    scale = min(plan_w / envelope.width, plan_h / envelope.depth)
    drawing_w, drawing_h = envelope.width * scale, envelope.depth * scale
    placed_x = plan_x + (plan_w - drawing_w) / 2.0
    placed_y = plan_y + (plan_h - drawing_h) / 2.0

    root = svg_el("svg", width=f"{page_w}mm", height=f"{page_h}mm", viewBox=f"0 0 {page_w} {page_h}", version="1.1")
    root.append(svg_el("title"))
    root[0].text = f"Apartment {config['title']} sheet"
    style = svg_el("style")
    style.text = """
.wall { fill: #4f5356; stroke: #111; stroke-width: 0.25; }
.space { fill: #f4f4f1; stroke: #c8c8c8; stroke-width: 0.12; }
.opening-cut { fill: #ffffff; stroke: #ffffff; stroke-width: 0.1; }
.door-leaf { fill: none; stroke: #5b331f; stroke-width: 0.45; }
.door-arc { fill: none; stroke: #5b331f; stroke-width: 0.25; stroke-dasharray: 1.2 0.8; }
.window-line { stroke: #0a5b78; stroke-width: 0.55; }
.electrical { fill: #d92118; stroke: #111; stroke-width: 0.12; }
.plumbing { fill: #1265d8; stroke: #111; stroke-width: 0.12; }
.lighting { fill: #f2c94c; stroke: #111; stroke-width: 0.12; }
.dimension { stroke: #111; stroke-width: 0.18; marker-start: url(#arrow); marker-end: url(#arrow); }
.thin { stroke: #111; stroke-width: 0.12; fill: none; }
.note { fill: #111; font-family: Arial, sans-serif; }
"""
    root.append(style)
    defs = svg_el("defs")
    marker = svg_el("marker", id="arrow", markerWidth="2", markerHeight="2", refX="1", refY="1", orient="auto")
    marker.append(svg_el("path", d="M 2 0 L 0 1 L 2 2 z", fill="#111"))
    defs.append(marker)
    root.append(defs)

    root.append(svg_el("rect", x="5", y="5", width="410", height="287", fill="none", stroke="#000", **{"stroke-width": "0.35"}))
    option_name = str(manifest.get("name") or manifest.get("spec_id") or "")
    option_status = str(manifest.get("status", ""))
    chain = " → ".join(manifest.get("variant_chain") or []) or str(manifest.get("spec_id", ""))
    append_text(root, PROJECT_NAME, 24, 18, 5.0, weight="bold")
    append_text(root, option_name, 24, 25, 3.4)
    append_text(root, f"{config['sheet_number']}  {config['title']}", 24, 30.5, 2.8)

    plan = svg_el("g", id="plan")
    root.append(plan)
    room_meta = {str(r.get("name")): r for r in (manifest.get("rooms") or [])}
    for space in sorted(spaces, key=lambda item: item.name):
        meta = room_meta.get(space.name, {})
        plan.append(svg_el("rect", **rect_attrs(space.bbox, envelope, scale, placed_x, placed_y, drawing_h),
                           fill=role_fill(str(meta.get("role", "other"))), stroke="#c8c8c8",
                           **{"stroke-width": "0.12"}))
    for wall in sorted(walls, key=lambda item: item.name):
        phase = wall_phase.get(wall.name, "existing")
        colour, dash = PHASE_STYLE.get(phase, PHASE_STYLE["existing"])
        plan.append(svg_el("rect", **rect_attrs(wall.bbox, envelope, scale, placed_x, placed_y, drawing_h),
                           fill=colour, stroke=colour, **{"stroke-width": "0.2",
                                                          "stroke-dasharray": dash,
                                                          "fill-opacity": "0.35" if phase == "demolished" else "1",
                                                          "data-name": wall.name, "data-phase": phase}))
    for opening in openings:
        plan.append(svg_el("rect", **rect_attrs(opening.bbox, envelope, scale, placed_x, placed_y, drawing_h), **{"class": "opening-cut", "data-host-wall": opening.host_wall or ""}))

    door_openings = {filling.RelatingOpeningElement.GlobalId for door in model.by_type("IfcDoor") for filling in getattr(door, "FillsVoids", []) or []}
    window_openings = {filling.RelatingOpeningElement.GlobalId for window in model.by_type("IfcWindow") for filling in getattr(window, "FillsVoids", []) or []}
    for opening in openings:
        if opening.global_id in door_openings:
            draw_door(plan, opening, envelope, scale, placed_x, placed_y, drawing_h)
        if opening.global_id in window_openings:
            draw_window(plan, opening, envelope, scale, placed_x, placed_y, drawing_h)

    # Label with the schedule's area, never the bounding box: the box is
    # recovered geometry and approximate, the area is the source's own figure.
    for number, space in enumerate(sorted(spaces, key=lambda item: -(room_meta.get(item.name, {}).get("area_m2") or 0)), 1):
        meta = room_meta.get(space.name, {})
        sx, sy = project_point(space.bbox.cx, space.bbox.cy, envelope, scale, placed_x, placed_y, drawing_h)
        append_text(plan, f"{number}", sx, sy - 4.4, 2.6, "middle", "bold")
        append_text(plan, bilingual(space.name, str(meta.get("role", "other"))), sx, sy - 1.2, 2.7, "middle", "bold")
        if meta.get("area_m2"):
            append_text(plan, f"{meta['area_m2']:.2f} m²", sx, sy + 2.0, 2.5, "middle")

    for symbol in visible_symbols:
        sx, sy = project_point(symbol.x, symbol.y, envelope, scale, placed_x, placed_y, drawing_h)
        size = 2.4
        if symbol.service == "plumbing":
            plan.append(svg_el("circle", cx=f"{sx:.3f}", cy=f"{sy:.3f}", r=f"{size / 2:.3f}", **{"class": "plumbing", "data-name": symbol.name, "data-host-wall": symbol.wall}))
            plan.append(svg_el("path", d=f"M {sx - 0.75:.3f} {sy:.3f} L {sx:.3f} {sy + 0.75:.3f} L {sx + 0.75:.3f} {sy:.3f}", fill="none", stroke="#fff", **{"stroke-width": "0.25"}))
        else:
            plan.append(svg_el("rect", x=f"{sx - size / 2:.3f}", y=f"{sy - size / 2:.3f}", width=f"{size:.3f}", height=f"{size:.3f}", **{"class": "electrical", "data-name": symbol.name, "data-host-wall": symbol.wall}))
            plan.append(svg_el("circle", cx=f"{sx:.3f}", cy=f"{sy:.3f}", r="0.65", fill="#ffffff", stroke="#111", **{"stroke-width": "0.12"}))
    for light in visible_lights:
        sx, sy = project_point(light.x, light.y, envelope, scale, placed_x, placed_y, drawing_h)
        plan.append(svg_el("circle", cx=f"{sx:.3f}", cy=f"{sy:.3f}", r="2.2", **{"class": "lighting", "data-name": light.name}))
        plan.append(svg_el("line", x1=f"{sx - 1.4:.3f}", y1=f"{sy:.3f}", x2=f"{sx + 1.4:.3f}", y2=f"{sy:.3f}", stroke="#111", **{"stroke-width": "0.18"}))
        plan.append(svg_el("line", x1=f"{sx:.3f}", y1=f"{sy - 1.4:.3f}", x2=f"{sx:.3f}", y2=f"{sy + 1.4:.3f}", stroke="#111", **{"stroke-width": "0.18"}))

    x0, y0 = project_point(envelope.xmin, envelope.ymin, envelope, scale, placed_x, placed_y, drawing_h)
    x1, y1 = project_point(envelope.xmax, envelope.ymax, envelope, scale, placed_x, placed_y, drawing_h)
    add_dimension(root, (x0, y1 - 10.0), (x1, y1 - 10.0), f"{envelope.width:.2f} m")
    add_dimension(root, (x1 + 10.0, y0), (x1 + 10.0, y1), f"{envelope.depth:.2f} m", (8.0, 0.0))
    root.append(svg_el("line", x1=f"{x0:.3f}", y1=f"{y1 - 6:.3f}", x2=f"{x0:.3f}", y2=f"{y1:.3f}", **{"class": "thin"}))
    root.append(svg_el("line", x1=f"{x1:.3f}", y1=f"{y1 - 6:.3f}", x2=f"{x1:.3f}", y2=f"{y1:.3f}", **{"class": "thin"}))
    root.append(svg_el("line", x1=f"{x1:.3f}", y1=f"{y0:.3f}", x2=f"{x1 + 6:.3f}", y2=f"{y0:.3f}", **{"class": "thin"}))
    root.append(svg_el("line", x1=f"{x1:.3f}", y1=f"{y1:.3f}", x2=f"{x1 + 6:.3f}", y2=f"{y1:.3f}", **{"class": "thin"}))

    legend_x, legend_y = 300.0, 36.0
    # ЭКСПЛИКАЦИЯ / room schedule - numbered to match the plan labels
    sched_x, sched_y = 300.0, 36.0
    append_text(root, "ЭКСПЛИКАЦИЯ / ROOM SCHEDULE", sched_x, sched_y, 3.2, weight="bold")
    sched_y += 5.0
    total_area = 0.0
    for number, space in enumerate(sorted(spaces, key=lambda item: -(room_meta.get(item.name, {}).get("area_m2") or 0)), 1):
        meta = room_meta.get(space.name, {})
        area = float(meta.get("area_m2") or 0)
        total_area += area
        append_text(root, f"{number}", sched_x, sched_y, 2.5)
        append_text(root, bilingual(space.name, str(meta.get("role", "other")))[:34], sched_x + 5, sched_y, 2.5)
        append_text(root, f"{area:.2f}", sched_x + 104, sched_y, 2.5, anchor="end")
        sched_y += 3.6
    root.append(svg_el("line", x1=f"{sched_x:.1f}", y1=f"{sched_y - 1.6:.1f}",
                       x2=f"{sched_x + 104:.1f}", y2=f"{sched_y - 1.6:.1f}",
                       stroke="#999", **{"stroke-width": "0.2"}))
    append_text(root, "ИТОГО / TOTAL", sched_x + 5, sched_y + 1.6, 2.5, weight="bold")
    append_text(root, f"{total_area:.2f} m²", sched_x + 104, sched_y + 1.6, 2.5, "end", weight="bold")

    # legend: what the colours mean
    leg_y = sched_y + 9.0
    append_text(root, "УСЛОВНЫЕ ОБОЗНАЧЕНИЯ / LEGEND", sched_x, leg_y, 3.2, weight="bold")
    leg_y += 5.0
    for label, colour, dash in [
            ("существующая стена / existing wall", PHASE_STYLE["existing"][0], "none"),
            ("демонтируется / to be removed", PHASE_STYLE["demolished"][0], "1.4 1.0"),
            ("возводится / new wall", PHASE_STYLE["new"][0], "none"),
            ("мокрая зона / wet zone", ROLE_FILL["wet"], "none")]:
        root.append(svg_el("rect", x=f"{sched_x:.1f}", y=f"{leg_y - 2.2:.1f}", width="6", height="2.6",
                           fill=colour, stroke="#555", **{"stroke-width": "0.2", "stroke-dasharray": dash}))
        append_text(root, label, sched_x + 8, leg_y, 2.5)
        leg_y += 4.2

    # scale bar - one metre, measured in the drawing's own scale
    bar_x, bar_y = sched_x, leg_y + 4.0
    metre = scale
    root.append(svg_el("rect", x=f"{bar_x:.1f}", y=f"{bar_y:.1f}", width=f"{metre:.2f}", height="1.4",
                       fill="#1a1a1a"))
    root.append(svg_el("rect", x=f"{bar_x + metre:.2f}", y=f"{bar_y:.1f}", width=f"{metre:.2f}",
                       height="1.4", fill="#ffffff", stroke="#1a1a1a", **{"stroke-width": "0.2"}))
    append_text(root, "0", bar_x, bar_y + 4.4, 2.2, "middle")
    append_text(root, "1", bar_x + metre, bar_y + 4.4, 2.2, "middle")
    append_text(root, "2 m", bar_x + 2 * metre, bar_y + 4.4, 2.2, "middle")

    # provenance - what produced this drawing and how far it may be trusted
    prov_y = bar_y + 10.0
    append_text(root, "ИСТОЧНИК / PROVENANCE", sched_x, prov_y, 3.2, weight="bold")
    for line in [f"вариант / option: {chain}",
                 f"статус / status: {option_status}",
                 f"модель / model: {ifc_path.name}",
                 "размеры номинальные ±25 мм / dimensions nominal ±25 mm",
                 "обмеры не выполнялись / not field verified"]:
        prov_y += 3.6
        append_text(root, line[:60], sched_x, prov_y, 2.3, fill="#555")

    title_x, title_y = 280.0, 246.0
    root.append(svg_el("rect", x=title_x, y=title_y, width=130, height=41, fill="#fff", stroke="#000", **{"stroke-width": "0.35"}))
    for offset in (12, 25, 33):
        root.append(svg_el("line", x1=title_x, y1=title_y + offset, x2=title_x + 130, y2=title_y + offset, stroke="#000", **{"stroke-width": "0.2"}))
    root.append(svg_el("line", x1=350, y1=title_y, x2=350, y2=title_y + 41, stroke="#000", **{"stroke-width": "0.2"}))
    append_text(root, PROJECT_NAME, title_x + 4, title_y + 6, 3.0, weight="bold")
    append_text(root, str(config["title"]), title_x + 4, title_y + 10, 2.5)
    append_text(root, "STATUS", title_x + 4, title_y + 18, 2.2, weight="bold")
    append_text(root, "COORDINATION ONLY / NOT FOR CONSTRUCTION", title_x + 22, title_y + 18, 2.2)
    append_text(root, "SOURCE", title_x + 4, title_y + 23, 2.2, weight="bold")
    append_text(root, ifc_path.name, title_x + 22, title_y + 23, 2.2)
    append_text(root, "SCALE", title_x + 4, title_y + 30, 2.2, weight="bold")
    append_text(root, "1:50 visual sheet", title_x + 22, title_y + 30, 2.2)
    append_text(root, "DATE", title_x + 4, title_y + 38, 2.2, weight="bold")
    append_text(root, date.today().isoformat(), title_x + 22, title_y + 38, 2.2)
    append_text(root, str(config["sheet_number"]), 354, title_y + 38, 6.0, weight="bold")

    output_svg.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output_svg, encoding="utf-8", xml_declaration=True)
    ET.parse(output_svg)
    if output_pdf:
        write_pdf(output_svg, output_pdf)

    source_manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path and manifest_path.is_file() else {}
    return {
        "source_ifc": str(ifc_path),
        "source_manifest": str(manifest_path) if manifest_path else None,
        "source_model_mtime": ifc_path.stat().st_mtime if ifc_path.exists() else None,
        "source_model_size": ifc_path.stat().st_size if ifc_path.exists() else None,
        "output_svg": str(output_svg),
        "output_pdf": str(output_pdf) if output_pdf else None,
        "classification": "coordination-ready; professional review required; not for construction",
        "page": "A3 landscape",
        "sheet_kind": sheet_kind,
        "sheet_number": config["sheet_number"],
        "scale_label": "1:50 visual sheet",
        "generated": date.today().isoformat(),
        "counts": {
            "walls": len(walls),
            "spaces": len(spaces),
            "openings": len(openings),
            "doors": len(doors),
            "windows": len(windows),
            "electrical_symbols": len([symbol for symbol in visible_symbols if symbol.service == "electrical"]),
            "plumbing_symbols": len([symbol for symbol in visible_symbols if symbol.service == "plumbing"]),
            "lighting_symbols": len(visible_lights),
            "model_electrical_symbols": len([symbol for symbol in symbols if symbol.service == "electrical"]),
            "model_plumbing_symbols": len([symbol for symbol in symbols if symbol.service == "plumbing"]),
            "model_lighting_symbols": len(light_symbols),
            "ifc_flow_terminals": len(model.by_type("IfcFlowTerminal")),
            "ifc_light_fixtures": len(model.by_type("IfcLightFixture")),
        },
        "validation": {
            "service_symbols_snap_to_walls": True,
            "service_symbols_avoid_openings": True,
            "lighting_symbols_inside_rooms": True,
            "service_symbol_source": electrical_source,
            "native_void_fill_relationships_used": True,
            "source_model_status": source_manifest.get("status"),
        },
    }


def write_pdf(svg_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import cairosvg  # type: ignore
    except (ImportError, OSError):
        try:
            from reportlab.graphics import renderPDF  # type: ignore
            from svglib.svglib import svg2rlg  # type: ignore
        except ImportError as exc:
            raise SheetError("No SVG-to-PDF renderer is installed. Install CairoSVG or svglib/reportlab.") from exc
        drawing = svg2rlg(str(svg_path))
        renderPDF.drawToFile(drawing, str(pdf_path))
        return
    cairosvg.svg2pdf(url=str(svg_path), write_to=str(pdf_path))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifc", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sheet-kind", choices=sorted(SHEET_CONFIG), default="combined")
    parser.add_argument("--sheet-set", action="store_true", help="Generate architectural, electrical, plumbing, and combined sheets.")
    args = parser.parse_args()
    results = []
    sheet_kinds = ["architectural", "electrical", "plumbing", "combined"] if args.sheet_set else [args.sheet_kind]
    for sheet_kind in sheet_kinds:
        stem = str(SHEET_CONFIG[sheet_kind]["stem"])
        svg_path = args.output_dir / f"{stem}.svg"
        pdf_path = args.output_dir / f"{stem}.pdf"
        manifest_path = args.output_dir / f"{stem}_manifest.json"
        result = build_svg(args.ifc, args.manifest, svg_path, pdf_path, sheet_kind=sheet_kind)
        manifest_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        results.append(result)
    print(json.dumps({"generated_sheets": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
