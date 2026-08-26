#!/usr/bin/env python3
"""Export a layout variant as a DXF plan, for DWG TrueView and other CAD viewers.

The variant pipeline produces IFC, SVG and PDF. None of those open in TrueView,
which is the CAD viewer actually installed here - so this writes the same plan
as a millimetre DXF that TrueView can open, zoom and measure with its own
dimension tool.

Layers follow the phase distinction the model carries, so the drawing reads the
way a demolition plan reads: what stays, what goes, what is new.

  A-WALL-EXIST   existing walls          white
  A-WALL-DEMO    walls to be removed     red, dashed
  A-WALL-NEW     walls to be built       cyan
  A-DOOR         door openings           yellow
  A-WINDOW       window openings         green
  A-ROOM         room outlines           grey
  A-ROOM-TEXT    room names and areas    grey
  A-FURN         furniture               magenta

Usage:
  python tools/drawings/export_variant_dxf.py --all
  python tools/drawings/export_variant_dxf.py v1-kitchen-living
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import ezdxf

REPO = Path(__file__).resolve().parents[2]
OUTPUTS = REPO / "data" / "outputs" / "variants"

M = 1000.0  # the spec is in metres; CAD viewers expect millimetres

LAYERS = {
    "A-WALL-EXIST": {"color": 7},
    "A-WALL-DEMO": {"color": 1, "linetype": "DASHED"},
    "A-WALL-NEW": {"color": 4},
    "A-WALL-MOD": {"color": 2},
    "A-DOOR": {"color": 2},
    "A-OPENING": {"color": 6},
    "A-BALCONY-BLOCK": {"color": 3},   # glazing too - it is a window with a door in it
    "A-WINDOW": {"color": 3},   # green - glazing
    "A-ROOM": {"color": 8},
    "A-ROOM-TEXT": {"color": 8},
    "A-FURN": {"color": 6},
}

RU = {
    "kitchen": "Кухня", "living": "Гостиная", "kids": "Детская", "bedroom": "Спальня",
    "hallway": "Коридор", "corridor": "Коридор", "entrance": "Прихожая",
    "bathroom": "Ванная", "wc": "Туалет", "combined_bath": "Санузел",
    "laundry": "Постирочная", "balcony": "Балкон", "storage": "Кладовая",
}


def bilingual(name: str, role: str) -> str:
    ru = RU.get(role)
    return "%s / %s" % (ru, name) if ru and ru.lower() != name.lower() else name


PHASE_LAYER = {"existing": "A-WALL-EXIST", "demolished": "A-WALL-DEMO",
               "new": "A-WALL-NEW", "modified": "A-WALL-MOD"}


def wall_rect(w: dict) -> tuple[float, float, float, float]:
    t = w["thickness_m"]
    if w["horizontal"]:
        return w["x_m"], w["y_m"], w["x_m"] + w["length_m"], w["y_m"] + t
    return w["x_m"], w["y_m"], w["x_m"] + t, w["y_m"] + w["length_m"]


def add_rect(msp, layer, x0, y0, x1, y1, hatch_layer=None):
    pts = [(x0 * M, y0 * M), (x1 * M, y0 * M), (x1 * M, y1 * M), (x0 * M, y1 * M)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})
    return pts


def export(spec: dict, out_path: Path) -> dict:
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4  # millimetres, so TrueView measures in mm
    doc.header["$MEASUREMENT"] = 1
    for name, attrs in LAYERS.items():
        layer = doc.layers.add(name)
        layer.color = attrs["color"]
        lt = attrs.get("linetype")
        if lt and doc.linetypes.has_entry(lt):
            layer.dxf.linetype = lt
    # Cyrillic needs a TrueType style; the default SHX font renders it as boxes
    # in most viewers, TrueView included.
    if "CYR" not in doc.styles:
        doc.styles.add("CYR", font="arial.ttf")
    msp = doc.modelspace()

    counts = {"walls": 0, "openings": 0, "rooms": 0, "furniture": 0}

    # No room rectangle. The extent is recovered geometry and approximate, so
    # drawing it puts a box over the walls that is close to the room but not
    # the room. The label carries the authoritative area; the walls show the
    # shape.
    for room in spec["rooms"]:
        x0, y0 = room["x_m"], room["y_m"]
        x1, y1 = x0 + room["width_m"], y0 + room["depth_m"]
        cx, cy = (x0 + x1) / 2 * M, (y0 + y1) / 2 * M
        msp.add_text(bilingual(room["name"], room.get("role", "")), height=120,
                     dxfattribs={"layer": "A-ROOM-TEXT", "style": "CYR"}
                     ).set_placement((cx, cy + 90))
        msp.add_text("%.2f m²" % room["area_m2"], height=120,
                     dxfattribs={"layer": "A-ROOM-TEXT", "style": "CYR"}
                     ).set_placement((cx, cy - 90))
        counts["rooms"] += 1

    outline = spec.get("wall_outline_mm") or []
    if outline:
        # The source's own wall outline: one continuous region, no internal
        # lines where the decomposition happened to cut. Even-odd fill so the
        # rooms stay holes rather than becoming wall.
        hatch = msp.add_hatch(color=8, dxfattribs={"layer": "A-WALL-EXIST"})
        hatch.set_pattern_fill("ANSI31", scale=18)
        for cycle in outline:
            pts = [(px, py) for px, py in cycle]
            msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "A-WALL-EXIST"})
            hatch.paths.add_polyline_path(pts, is_closed=True)
        counts["walls"] = len(outline)
    for w in spec["walls"]:
        phase = w.get("phase", "existing")
        if outline and phase == "existing":
            continue  # already drawn as part of the outline
        layer = PHASE_LAYER.get(phase, "A-WALL-EXIST")
        x0, y0, x1, y1 = wall_rect(w)
        pts = add_rect(msp, layer, x0, y0, x1, y1)
        if phase != "demolished":
            hatch = msp.add_hatch(color=8, dxfattribs={"layer": layer})
            hatch.paths.add_polyline_path(pts, is_closed=True)
            hatch.set_pattern_fill("ANSI31", scale=18)
        counts["walls"] += 1

    wall_by_name = {w["name"]: w for w in spec["walls"]}

    def room_at(x_m: float, y_m: float):
        """Which room a point falls in - used to decide which way a door opens."""
        for r in spec["rooms"]:
            if r["x_m"] <= x_m <= r["x_m"] + r["width_m"] \
                    and r["y_m"] <= y_m <= r["y_m"] + r["depth_m"]:
                return r
        return None

    def swing_side(o, t: float) -> int:
        """+1 or -1: the side with the bigger room, or outward-safe if unknown.

        A door drawn with a fixed swing opens into a wall about half the time.
        Choosing the side by what is actually there is the difference between a
        door symbol and a door.
        """
        cx = o["x_m"] + (o["width_m"] / 2 if o["horizontal"] else t / 2)
        cy = o["y_m"] + (t / 2 if o["horizontal"] else o["width_m"] / 2)
        reach = 0.6
        if o["horizontal"]:
            plus, minus = room_at(cx, cy + reach), room_at(cx, cy - reach)
        else:
            plus, minus = room_at(cx + reach, cy), room_at(cx - reach, cy)
        a = plus["area_m2"] if plus else 0.0
        b = minus["area_m2"] if minus else 0.0
        return 1 if a >= b else -1

    def host_thickness(o) -> float:
        w = wall_by_name.get(o.get("host_wall") or "")
        return w["thickness_m"] if w else 0.15

    for o in spec["openings"]:
        if o.get("phase") == "demolished":
            continue
        kind = o["kind"]
        layer = {"door": "A-DOOR", "window": "A-WINDOW", "opening": "A-OPENING",
                 "balcony_block": "A-BALCONY-BLOCK"}.get(kind, "A-DOOR")
        t = host_thickness(o)
        width = o["width_m"]
        # Along the wall the opening runs `width`; across it, exactly the wall
        # thickness. Drawing a fixed 190 mm depth is what made these look
        # misplaced - they straddled the wall instead of sitting in it.
        if o["horizontal"]:
            x0, y0, x1, y1 = o["x_m"], o["y_m"], o["x_m"] + width, o["y_m"] + t
        else:
            x0, y0, x1, y1 = o["x_m"], o["y_m"], o["x_m"] + t, o["y_m"] + width

        if kind in ("window", "balcony_block"):
            # three lines across the reveal, the way a window is drawn
            for frac in (0.25, 0.5, 0.75):
                if o["horizontal"]:
                    yy = (y0 + (y1 - y0) * frac) * M
                    msp.add_line((x0 * M, yy), (x1 * M, yy), dxfattribs={"layer": layer})
                else:
                    xx = (x0 + (x1 - x0) * frac) * M
                    msp.add_line((xx, y0 * M), (xx, y1 * M), dxfattribs={"layer": layer})
        if kind in ("door", "balcony_block"):
            # leaf plus swing, opening into the larger adjacent room
            leaf = width
            side = swing_side(o, t)
            if o["horizontal"]:
                hx, hy = x0 * M, (y0 + t / 2) * M
                # leaf lies along the wall; the arc sweeps to the chosen side
                msp.add_line((hx, hy), (hx + leaf * M, hy), dxfattribs={"layer": layer})
                start, end = (0, 90) if side > 0 else (270, 360)
            else:
                hx, hy = (x0 + t / 2) * M, y0 * M
                msp.add_line((hx, hy), (hx, hy + leaf * M), dxfattribs={"layer": layer})
                start, end = (0, 90) if side > 0 else (90, 180)
            msp.add_arc(center=(hx, hy), radius=leaf * M, start_angle=start, end_angle=end,
                        dxfattribs={"layer": layer})
        if kind == "opening":
            # a проём has no leaf: mark the jambs and leave the gap empty
            for px, py in (((x0, y0), (x0, y1)) if not o["horizontal"] else ((x0, y0), (x1, y0))):
                pass
            if o["horizontal"]:
                msp.add_line((x0 * M, y0 * M), (x0 * M, y1 * M), dxfattribs={"layer": layer})
                msp.add_line((x1 * M, y0 * M), (x1 * M, y1 * M), dxfattribs={"layer": layer})
            else:
                msp.add_line((x0 * M, y0 * M), (x1 * M, y0 * M), dxfattribs={"layer": layer})
                msp.add_line((x0 * M, y1 * M), (x1 * M, y1 * M), dxfattribs={"layer": layer})

        msp.add_text("%d" % round(width * M), height=90,
                     dxfattribs={"layer": layer, "style": "CYR"}
                     ).set_placement(((x0 + x1) / 2 * M, (y0 + y1) / 2 * M))
        counts["openings"] += 1

    for f in spec.get("furniture", []):
        add_rect(msp, "A-FURN", f["x_m"], f["y_m"],
                 f["x_m"] + f["width_m"], f["y_m"] + f["depth_m"])
        counts["furniture"] += 1

    # A dimension line along the envelope, so the drawing states its own size.
    xs = [wall_rect(w)[0] for w in spec["walls"]] + [wall_rect(w)[2] for w in spec["walls"]]
    ys = [wall_rect(w)[1] for w in spec["walls"]] + [wall_rect(w)[3] for w in spec["walls"]]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    dim = msp.add_linear_dim(base=(x0 * M, (y0 - 0.8) * M), p1=(x0 * M, y0 * M),
                             p2=(x1 * M, y0 * M), dxfattribs={"layer": "A-ROOM-TEXT"})
    dim.render()

    msp.add_text("Dubravinsky - %s - %s - НЕ ДЛЯ СТРОИТЕЛЬСТВА / NOT FOR CONSTRUCTION"
                 % (spec.get("spec_id", ""), spec.get("status", "")),
                 height=200, dxfattribs={"layer": "A-ROOM-TEXT", "style": "CYR"}
                 ).set_placement((x0 * M, (y1 + 0.6) * M))
    msp.add_text("размеры номинальные ±25 мм / dimensions nominal ±25 mm",
                 height=130, dxfattribs={"layer": "A-ROOM-TEXT", "style": "CYR"}
                 ).set_placement((x0 * M, (y1 + 0.3) * M))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(str(out_path))
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("variants", nargs="*", help="variant ids; default is every built variant")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    ids = a.variants or sorted(p.name for p in OUTPUTS.iterdir()
                               if (p / "spec.json").exists() and p.name != "comparison")
    results = []
    for vid in ids:
        spec = json.loads((OUTPUTS / vid / "spec.json").read_text(encoding="utf-8"))
        out = OUTPUTS / vid / ("%s_plan.dxf" % vid)
        counts = export(spec, out)
        results.append({"variant": vid, "dxf": str(out.relative_to(REPO)), **counts})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
