#!/usr/bin/env python3
"""Compare layout variants as a drawing, not as JSON.

Draws every built variant side by side on one A3 landscape sheet - plan,
room areas, what was demolished and what was added - and under each one the
metrics and the rule checks it passes or fails. The rules come from
data/layout_rules/rules.jsonl, so a variant is judged against what named
practitioners actually said, with the attribution printed on the sheet.

Only some rules are mechanically checkable from geometry; the rest are listed
as advisory rather than silently ignored.

Usage:
  python tools/layout/compare_variants.py                     # every built variant
  python tools/layout/compare_variants.py v0-existing v1-kitchen-living
"""
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUTPUTS = REPO / "data" / "outputs" / "variants"
RULES = REPO / "data" / "layout_rules" / "rules.jsonl"

A3_W, A3_H = 420.0, 297.0
HABITABLE = {"living", "bedroom", "kids", "kitchen"}
WET = {"bathroom", "wc", "combined_bath", "laundry"}
CIRCULATION = {"entrance", "hallway", "corridor"}

ROLE_FILL = {
    "kitchen": "#dceaf5", "bathroom": "#dceaf5", "wc": "#dceaf5",
    "combined_bath": "#dceaf5", "laundry": "#dceaf5",
    "living": "#f4f4f2", "bedroom": "#f4f4f2", "kids": "#f4f4f2",
    "entrance": "#ecebe7", "hallway": "#ecebe7", "corridor": "#ecebe7",
    "balcony": "#f7f7f7", "storage": "#efeee9", "other": "#f4f4f2",
}


def load_rules() -> dict:
    rules = {}
    for line in RULES.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            rules[r["rule_id"]] = r
    return rules


def wall_bbox(w):
    t = w["thickness_m"]
    return ((w["x_m"], w["y_m"], w["x_m"] + w["length_m"], w["y_m"] + t) if w["horizontal"]
            else (w["x_m"], w["y_m"], w["x_m"] + t, w["y_m"] + w["length_m"]))


def rooms_touching(spec, wall_name):
    return (spec.get("space_boundaries") or {}).get(wall_name, [])


def rooms_with_windows(spec) -> set[str]:
    lit = set()
    for o in spec["openings"]:
        if o["kind"] != "window" or o.get("phase") == "demolished":
            continue
        for room in rooms_touching(spec, o["host_wall"]):
            lit.add(room)
    return lit


def metrics(spec: dict) -> dict:
    by_role = lambda roles: round(sum(r["area_m2"] for r in spec["rooms"]
                                      if r.get("role") in roles), 2)
    walls = spec["walls"]
    return {
        "rooms": len(spec["rooms"]),
        "habitable_m2": by_role(HABITABLE),
        "wet_m2": by_role(WET),
        "circulation_m2": by_role(CIRCULATION),
        "total_m2": round(sum(r["area_m2"] for r in spec["rooms"]), 2),
        "walls_demolished": sum(1 for w in walls if w.get("phase") == "demolished"),
        "walls_new": sum(1 for w in walls if w.get("phase") == "new"),
        "doors": sum(1 for o in spec["openings"]
                     if o["kind"] == "door" and o.get("phase") != "demolished"),
    }


def check_rules(spec: dict, rules: dict) -> list[dict]:
    """Only the checks geometry can actually settle. Everything else is advisory."""
    out = []

    r = rules.get("corridor.min_clear_width")
    if r:
        min_mm = r["params"]["min_clear_width_mm"]
        worst = None
        for room in spec["rooms"]:
            if room.get("role") not in CIRCULATION:
                continue
            clear = min(room["width_m"], room["depth_m"]) * 1000
            if worst is None or clear < worst[1]:
                worst = (room["name"], clear)
        if worst:
            out.append({"rule": r["rule_id"], "ok": worst[1] >= min_mm,
                        "detail": "%s clear %d mm (min %d)" % (worst[0], round(worst[1]), min_mm),
                        "author": r["attribution"]["author"]})

    r = rules.get("corridor.excess_width_is_stolen_from_rooms")
    if r:
        flag_mm = r["params"]["flag_above_mm"]
        widest = None
        for room in spec["rooms"]:
            if room.get("role") not in CIRCULATION:
                continue
            clear = min(room["width_m"], room["depth_m"]) * 1000
            if widest is None or clear > widest[1]:
                widest = (room["name"], clear)
        if widest:
            out.append({"rule": r["rule_id"], "ok": widest[1] <= flag_mm,
                        "detail": "%s clear %d mm (flag above %d)" % (widest[0], round(widest[1]), flag_mm),
                        "author": r["attribution"]["author"]})

    r = rules.get("daylight.third_room_costs_a_window")
    if r:
        lit = rooms_with_windows(spec)
        dark = [x["name"] for x in spec["rooms"]
                if x.get("role") in HABITABLE and x["name"] not in lit]
        out.append({"rule": r["rule_id"], "ok": not dark,
                    "detail": "all habitable rooms have a window" if not dark
                              else "no window: " + ", ".join(dark),
                    "author": r["attribution"]["author"]})
    return out


def advisory(rules: dict, spec: dict) -> list[str]:
    """Rules that bear on this layout but cannot be settled from geometry."""
    notes = []
    for rid in ("kitchen.trade_area_for_openness", "layout.furniture_first_before_walls",
                "process.minimum_two_variants", "hall.prefer_rectangular"):
        r = rules.get(rid)
        if r:
            notes.append("%s - %s" % (rid, r["attribution"]["author"]))
    return notes


def el(tag, **attrs):
    return ET.Element(tag, {k.replace("_", "-"): str(v) for k, v in attrs.items()})


def text(parent, value, x, y, size=3.0, weight="normal", fill="#1a1a1a", anchor="start"):
    node = ET.SubElement(parent, "text", {
        "x": str(round(x, 2)), "y": str(round(y, 2)), "font-size": str(size),
        "font-family": "DejaVu Sans, Arial, sans-serif", "font-weight": weight,
        "fill": fill, "text-anchor": anchor})
    node.text = value
    return node


def draw_variant(parent, spec, variant_meta, ox, oy, panel_w, panel_h, rules):
    """One column: title, plan, metrics, rule checks."""
    ET.SubElement(parent, "rect", {"x": str(ox), "y": str(oy), "width": str(panel_w),
                                   "height": str(panel_h), "fill": "#ffffff",
                                   "stroke": "#c9c9c4", "stroke-width": "0.3"})
    title_h = 9.0
    text(parent, variant_meta.get("name", spec.get("spec_id", "")), ox + 3, oy + 5.5, 4.0, "bold")
    status = spec.get("status", "")
    if status != "baseline":
        text(parent, status.replace("_", " ").upper(), ox + panel_w - 3, oy + 5.5, 2.6,
             "bold", "#b03030", "end")

    # plan area
    plan_h = panel_h * 0.52
    px, py = ox + 3, oy + title_h
    pw, ph = panel_w - 6, plan_h

    xs = [w["x_m"] for w in spec["walls"]] + [r["x_m"] for r in spec["rooms"]]
    ys = [w["y_m"] for w in spec["walls"]] + [r["y_m"] for r in spec["rooms"]]
    xe = [wall_bbox(w)[2] for w in spec["walls"]] + [r["x_m"] + r["width_m"] for r in spec["rooms"]]
    ye = [wall_bbox(w)[3] for w in spec["walls"]] + [r["y_m"] + r["depth_m"] for r in spec["rooms"]]
    x0, y0, x1, y1 = min(xs), min(ys), max(xe), max(ye)
    scale = min(pw / (x1 - x0), ph / (y1 - y0)) * 0.94
    offx = px + (pw - (x1 - x0) * scale) / 2.0
    offy = py + (ph - (y1 - y0) * scale) / 2.0

    def P(x, y):
        # flip Y: model Y grows north, SVG Y grows down
        return offx + (x - x0) * scale, offy + ((y1 - y0) - (y - y0)) * scale

    g = ET.SubElement(parent, "g")
    for room in spec["rooms"]:
        rx, ry = P(room["x_m"], room["y_m"] + room["depth_m"])
        ET.SubElement(g, "rect", {
            "x": str(round(rx, 2)), "y": str(round(ry, 2)),
            "width": str(round(room["width_m"] * scale, 2)),
            "height": str(round(room["depth_m"] * scale, 2)),
            "fill": ROLE_FILL.get(room.get("role", "other"), "#f4f4f2"),
            "stroke": "none"})
        cx, cy = P(room["x_m"] + room["width_m"] / 2.0, room["y_m"] + room["depth_m"] / 2.0)
        # keep the label inside its room: narrow rooms get smaller, clipped text
        box_w = room["width_m"] * scale
        size = 2.4 if box_w > 20 else (2.0 if box_w > 13 else 1.6)
        budget = max(4, int(box_w / (size * 0.52)))
        label = room["name"] if len(room["name"]) <= budget else room["name"][:budget - 1] + "…"
        text(g, label, cx, cy - 0.6, size, "normal", "#333", "middle")
        text(g, "%.1f m²" % room["area_m2"], cx, cy + size, size, "bold", "#333", "middle")

    for w in spec["walls"]:
        bx0, by0, bx1, by1 = wall_bbox(w)
        sx, sy = P(bx0, by1)
        phase = w.get("phase", "existing")
        style = {"existing": ("#3a3a3a", "none"), "demolished": ("#c23b3b", "1.4 1.0"),
                 "new": ("#1c6ea4", "none"), "modified": ("#8a6d1f", "none")}[phase]
        ET.SubElement(g, "rect", {
            "x": str(round(sx, 2)), "y": str(round(sy, 2)),
            "width": str(round((bx1 - bx0) * scale, 2)),
            "height": str(round((by1 - by0) * scale, 2)),
            "fill": "#c23b3b" if phase == "demolished" else style[0],
            "fill-opacity": "0.35" if phase == "demolished" else "1",
            "stroke": style[0], "stroke-width": "0.25",
            "stroke-dasharray": style[1]})

    for o in spec["openings"]:
        if o.get("phase") == "demolished":
            continue
        ox0, oy0 = (o["x_m"], o["y_m"] + (o["width_m"] if not o["horizontal"] else 0))
        sx, sy = P(ox0, oy0)
        w_mm = o["width_m"] * scale
        ET.SubElement(g, "rect", {
            "x": str(round(sx, 2)), "y": str(round(sy, 2)),
            "width": str(round(w_mm if o["horizontal"] else 0.9, 2)),
            "height": str(round(0.9 if o["horizontal"] else w_mm, 2)),
            "fill": "#ffffff", "stroke": "#7a7a7a", "stroke-width": "0.2"})

    # metrics + checks
    m = metrics(spec)
    ty = oy + title_h + plan_h + 6
    text(parent, "Метрики", ox + 3, ty, 3.2, "bold")
    ty += 4.2
    for label, value in [
        ("жилая площадь", "%.1f m²" % m["habitable_m2"]),
        ("мокрые зоны", "%.1f m²" % m["wet_m2"]),
        ("коридоры/прихожая", "%.1f m²" % m["circulation_m2"]),
        ("помещений / дверей", "%d / %d" % (m["rooms"], m["doors"])),
        ("сносится / строится стен", "%d / %d" % (m["walls_demolished"], m["walls_new"])),
    ]:
        text(parent, label, ox + 3, ty, 2.7)
        text(parent, value, ox + panel_w - 3, ty, 2.7, "bold", anchor="end")
        ty += 3.6

    ty += 2.0
    text(parent, "Проверка по правилам источников", ox + 3, ty, 3.2, "bold")
    ty += 4.2
    for check in check_rules(spec, rules):
        mark, colour = ("OK", "#2c7a3f") if check["ok"] else ("!", "#b03030")
        text(parent, mark, ox + 3, ty, 2.7, "bold", colour)
        text(parent, check["detail"], ox + 9, ty, 2.7, "normal", "#333")
        ty += 3.3
        text(parent, check["rule"] + " — " + check["author"], ox + 9, ty, 2.1, "normal", "#777")
        ty += 4.0
    return ty


def build_sheet(variants: list[tuple[dict, dict]], out_svg: Path, rules: dict) -> None:
    svg = el("svg", xmlns="http://www.w3.org/2000/svg", width="%.0fmm" % A3_W,
             height="%.0fmm" % A3_H, viewBox="0 0 %.0f %.0f" % (A3_W, A3_H), version="1.1")
    ET.SubElement(svg, "rect", {"x": "0", "y": "0", "width": str(A3_W), "height": str(A3_H),
                                "fill": "#ffffff"})
    text(svg, "СРАВНЕНИЕ ВАРИАНТОВ ПЛАНИРОВКИ", 12, 14, 6.0, "bold")
    text(svg, "ZK Dubravinskiy · A3 · масштаб не проверен · не для строительства", 12, 20, 3.0,
         "normal", "#666")

    margin, gap, top = 12.0, 6.0, 26.0
    panel_w = (A3_W - 2 * margin - gap * (len(variants) - 1)) / len(variants)
    panel_h = A3_H - top - 22.0
    for i, (spec, meta) in enumerate(variants):
        draw_variant(svg, spec, meta, margin + i * (panel_w + gap), top, panel_w, panel_h, rules)

    ly = A3_H - 14
    for i, (label, colour, dash) in enumerate([
            ("существующая стена", "#3a3a3a", "none"),
            ("демонтируется", "#c23b3b", "1.4 1.0"),
            ("возводится", "#1c6ea4", "none"),
            ("мокрая зона", "#dceaf5", "none")]):
        lx = margin + i * 60
        ET.SubElement(svg, "rect", {"x": str(lx), "y": str(ly - 2.6), "width": "6", "height": "2.6",
                                    "fill": colour, "stroke": "#555", "stroke-width": "0.2",
                                    "stroke-dasharray": dash})
        text(svg, label, lx + 8, ly, 2.8, "normal", "#333")
    text(svg, "Правила и их авторы — data/layout_rules/rules.jsonl. Ничто здесь не является "
              "измерением: модель не подтверждена натурными обмерами.",
         margin, A3_H - 6, 2.5, "normal", "#777")

    out_svg.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(svg).write(out_svg, encoding="utf-8", xml_declaration=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("variants", nargs="*", help="variant ids; default is every built variant")
    ap.add_argument("--out", default=str(OUTPUTS / "comparison"))
    a = ap.parse_args()

    ids = a.variants or sorted(p.name for p in OUTPUTS.iterdir()
                               if (p / "spec.json").exists() and p.name != "comparison")
    loaded = []
    for vid in ids:
        spec = json.loads((OUTPUTS / vid / "spec.json").read_text(encoding="utf-8"))
        meta_path = REPO / "data" / "variants" / (vid + ".json")
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        loaded.append((spec, meta))

    rules = load_rules()
    out = Path(a.out)
    svg_path = out / "variant_comparison_a3.svg"
    build_sheet(loaded, svg_path, rules)
    pdf_path = out / "variant_comparison_a3.pdf"
    try:
        sys.path.insert(0, str(REPO / "tools" / "drawings"))
        from apartment_sheet_from_ifc import write_pdf
        write_pdf(svg_path, pdf_path)
    except Exception as exc:  # a missing renderer must not lose the SVG
        pdf_path = None
        print("note: no PDF written (%s)" % exc)

    table = {vid: {"metrics": metrics(spec), "checks": check_rules(spec, rules),
                   "advisory_rules": advisory(rules, spec)}
             for vid, (spec, _) in zip(ids, loaded)}
    (out / "variant_comparison.json").write_text(
        json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"variants": ids, "sheet": str(svg_path.relative_to(REPO)),
                      "pdf": str(pdf_path.relative_to(REPO)) if pdf_path else None,
                      "table": str((out / "variant_comparison.json").relative_to(REPO))},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
