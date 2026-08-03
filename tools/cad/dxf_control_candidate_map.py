"""Render a simple SVG map of DXF control-dimension candidates.

The map is a review aid. It shows where candidate dimensions are located in
model space so repeated apartment instances can be identified before any CAD
dimension is promoted into the canonical apartment model.
"""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

COLOURS = ["#d62728", "#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf", "#8c564b"]


def svg_el(tag: str, **attrs: Any) -> ET.Element:
    return ET.Element(f"{{{SVG_NS}}}{tag}", {key.replace("_", "-"): str(value) for key, value in attrs.items()})


def append_text(parent: ET.Element, text: str, x: float, y: float, size: float = 3.0, anchor: str = "start") -> None:
    element = svg_el(
        "text",
        x=f"{x:.3f}",
        y=f"{y:.3f}",
        fill="#111",
        font_family="Arial, sans-serif",
        font_size=f"{size:.3f}",
        text_anchor=anchor,
    )
    element.text = text
    parent.append(element)


def _candidate_point(candidate: dict[str, Any]) -> tuple[float, float] | None:
    points = candidate.get("points") or {}
    point = points.get("text_midpoint") or points.get("defpoint") or points.get("defpoint2")
    if not point:
        return None
    return float(point[0]), float(point[1])


def _collect_points(report: dict[str, Any]) -> list[dict[str, Any]]:
    points = []
    for target_index, target in enumerate(report.get("targets", [])):
        colour = COLOURS[target_index % len(COLOURS)]
        for candidate in target.get("matches", []):
            point = _candidate_point(candidate)
            if not point:
                continue
            points.append(
                {
                    "x": point[0],
                    "y": point[1],
                    "target_mm": target.get("target_mm"),
                    "measurement_mm": candidate.get("measurement_mm"),
                    "delta_mm": candidate.get("delta_mm"),
                    "handle": candidate.get("handle"),
                    "colour": colour,
                }
            )
    return points


def render_map(candidate_report: Path, output: Path) -> dict[str, Any]:
    report = json.loads(candidate_report.read_text(encoding="utf-8"))
    points = _collect_points(report)
    if not points:
        raise SystemExit("No candidate points available to render.")
    xmin = min(point["x"] for point in points)
    xmax = max(point["x"] for point in points)
    ymin = min(point["y"] for point in points)
    ymax = max(point["y"] for point in points)
    margin = 18.0
    page_w = 420.0
    page_h = 297.0
    span_x = max(xmax - xmin, 1.0)
    span_y = max(ymax - ymin, 1.0)
    scale = min((page_w - margin * 2.0) / span_x, (page_h - margin * 2.0) / span_y)

    def project(x: float, y: float) -> tuple[float, float]:
        return margin + (x - xmin) * scale, page_h - margin - (y - ymin) * scale

    root = svg_el("svg", width=f"{page_w}mm", height=f"{page_h}mm", viewBox=f"0 0 {page_w} {page_h}", version="1.1")
    style = svg_el("style")
    style.text = """
.candidate { stroke: #111; stroke-width: 0.18; fill-opacity: 0.82; }
.cluster-box { fill: none; stroke: #777; stroke-width: 0.2; stroke-dasharray: 2 1; }
"""
    root.append(style)
    root.append(svg_el("rect", x="5", y="5", width="410", height="287", fill="#fff", stroke="#111", stroke_width="0.35"))
    append_text(root, "DXF control-dimension candidate map", 14, 15, 5.0)
    append_text(root, "Review aid only - repeated apartment instances require manual visual confirmation", 14, 22, 3.0)

    for point in points:
        x, y = project(point["x"], point["y"])
        title = svg_el("title")
        title.text = f"{point['target_mm']} mm target | {point['measurement_mm']} mm | delta {point['delta_mm']} | handle {point['handle']}"
        circle = svg_el("circle", cx=f"{x:.3f}", cy=f"{y:.3f}", r="2.2", fill=point["colour"], **{"class": "candidate"})
        circle.append(title)
        root.append(circle)

    legend_x = 292.0
    legend_y = 34.0
    root.append(svg_el("rect", x=legend_x - 5, y=legend_y - 10, width=112, height=70, fill="#fff", stroke="#111", stroke_width="0.2"))
    append_text(root, "Targets", legend_x, legend_y, 3.5)
    for target_index, target in enumerate(report.get("targets", [])):
        y = legend_y + 8 + target_index * 8
        colour = COLOURS[target_index % len(COLOURS)]
        root.append(svg_el("circle", cx=legend_x + 2, cy=y - 1, r="2.0", fill=colour, **{"class": "candidate"}))
        append_text(root, f"{target.get('target_mm')} mm: {target.get('match_count')} candidates", legend_x + 8, y, 2.8)

    append_text(root, f"Source: {report.get('source')}", 14, 282, 2.5)
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
    return {
        "source": str(candidate_report),
        "output_svg": str(output),
        "candidate_points": len(points),
        "bbox_modelspace_mm": [round(xmin, 3), round(ymin, 3), round(xmax, 3), round(ymax, 3)],
        "status": "review_aid_only",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(render_map(args.candidates, args.output), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
