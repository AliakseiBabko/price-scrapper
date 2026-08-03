"""Deterministic vector floor-plan sheet from the canonical renovation JSON.

This is a lightweight drawing milestone. It is not an IFC HLR renderer and does
not claim to replace Bonsai/IfcConvert. Its purpose is to prove sheet geometry,
dimensions, symbols, and repeatable SVG output before adding those dependencies.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def svg_escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(data: dict) -> str:
    dims = data["room_dimensions"]
    length = float(dims["length"])
    width = float(dims["width"])
    thickness = float(dims["wall_thickness"])
    door = data["door_opening"]
    offset = float(door["offset_from_corner"])
    door_width = float(door["width"])
    scale = 100.0
    margin = 110.0
    x0 = margin
    y0 = margin
    room_w = length * scale
    room_h = width * scale
    wall = thickness * scale
    opening_x = x0 + offset * scale
    opening_w = door_width * scale
    page_w = margin * 2 + room_w + 140
    page_h = margin * 2 + room_h + 150

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{page_w:.0f}" height="{page_h:.0f}" viewBox="0 0 {page_w:.0f} {page_h:.0f}">
  <title>{svg_escape(data["project_name"])} floor plan</title>
  <style>
    .cut {{ fill: #d9d9d9; stroke: #111; stroke-width: 2; }}
    .opening {{ fill: #fff; stroke: #b00020; stroke-width: 2; }}
    .door {{ fill: none; stroke: #0645ad; stroke-width: 2; }}
    .dimension {{ fill: none; stroke: #333; stroke-width: 1; marker-start: url(#arrow); marker-end: url(#arrow); }}
    .extension {{ stroke: #333; stroke-width: 1; }}
    .label {{ font-family: Arial, sans-serif; font-size: 14px; fill: #111; }}
    .title {{ font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; fill: #111; }}
  </style>
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
      <path d="M 8 0 L 0 4 L 8 8 z" fill="#333" />
    </marker>
  </defs>

  <text x="{x0}" y="32" class="title">{svg_escape(data["project_name"])} — floor plan</text>
  <text x="{x0}" y="54" class="label">Scale 1:100 · units: metres · generated from canonical JSON</text>

  <!-- Four wall solids -->
  <rect x="{x0:.2f}" y="{y0:.2f}" width="{room_w:.2f}" height="{wall:.2f}" class="cut" />
  <rect x="{x0 + room_w - wall:.2f}" y="{y0:.2f}" width="{wall:.2f}" height="{room_h:.2f}" class="cut" />
  <rect x="{x0:.2f}" y="{y0 + room_h - wall:.2f}" width="{room_w:.2f}" height="{wall:.2f}" class="cut" />
  <rect x="{x0:.2f}" y="{y0:.2f}" width="{wall:.2f}" height="{room_h:.2f}" class="cut" />

  <!-- South-wall door opening and swing -->
  <rect x="{opening_x:.2f}" y="{y0:.2f}" width="{opening_w:.2f}" height="{wall:.2f}" class="opening" />
  <path d="M {opening_x:.2f} {y0 + wall:.2f} A {opening_w:.2f} {opening_w:.2f} 0 0 1 {opening_x + opening_w:.2f} {y0 + wall + opening_w:.2f}" class="door" />
  <line x1="{opening_x:.2f}" y1="{y0 + wall:.2f}" x2="{opening_x + opening_w:.2f}" y2="{y0 + wall:.2f}" class="door" />

  <!-- Overall dimensions -->
  <line x1="{x0:.2f}" y1="{y0 - 28:.2f}" x2="{x0:.2f}" y2="{y0:.2f}" class="extension" />
  <line x1="{x0 + room_w:.2f}" y1="{y0 - 28:.2f}" x2="{x0 + room_w:.2f}" y2="{y0:.2f}" class="extension" />
  <line x1="{x0:.2f}" y1="{y0 - 18:.2f}" x2="{x0 + room_w:.2f}" y2="{y0 - 18:.2f}" class="dimension" />
  <text x="{x0 + room_w / 2:.2f}" y="{y0 - 25:.2f}" text-anchor="middle" class="label">{length:.2f} m</text>

  <line x1="{x0 + room_w + 28:.2f}" y1="{y0:.2f}" x2="{x0 + room_w + 28:.2f}" y2="{y0 + room_h:.2f}" class="dimension" />
  <text x="{x0 + room_w + 48:.2f}" y="{y0 + room_h / 2:.2f}" transform="rotate(90 {x0 + room_w + 48:.2f} {y0 + room_h / 2:.2f})" text-anchor="middle" class="label">{width:.2f} m</text>

  <text x="{x0}" y="{y0 + room_h + 42:.2f}" class="label">Door: {door_width:.2f} m wide · wall thickness: {thickness:.2f} m</text>
  <text x="{x0}" y="{y0 + room_h + 66:.2f}" class="label">STATUS: coordination prototype — professional review required</text>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_svg(load(args.input)), encoding="utf-8")
    print(f"Wrote SVG floor plan: {args.output}")


if __name__ == "__main__":
    main()
