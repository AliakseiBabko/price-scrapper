"""Package an IFC-derived SVG into a printable A3 landscape sheet.

The SVG is always produced. PDF output is produced when CairoSVG is installed;
otherwise the command reports the missing optional renderer and still leaves a
validated, print-sized SVG deliverable.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def element(tag: str, **attributes):
    return ET.Element(f"{{{SVG_NS}}}{tag}", {key: str(value) for key, value in attributes.items()})


def text_node(parent, value: str, x: float, y: float, size: float = 3.0, weight: str = "normal"):
    node = element("text", x=x, y=y, **{"font-size": size, "font-family": "Arial", "font-weight": weight})
    node.text = value
    parent.append(node)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-svg", type=Path, required=True)
    parser.add_argument("--output-pdf", type=Path)
    parser.add_argument("--project", default="Residential renovation")
    parser.add_argument("--sheet-number", default="A-101")
    parser.add_argument("--sheet-title", default="Floor plan — coordination")
    parser.add_argument("--revision", default="P01")
    parser.add_argument("--scale", default="1:100")
    parser.add_argument("--status", default="COORDINATION ONLY")
    args = parser.parse_args()

    root = ET.parse(args.input).getroot()
    source_viewbox = root.get("viewBox", "0 0 1000 1000").split()
    if len(source_viewbox) != 4:
        raise SystemExit("Input SVG must have a four-value viewBox")
    source_width = float(source_viewbox[2])
    source_height = float(source_viewbox[3])

    # A3 landscape in millimetres. Reserve the bottom-right area for the title block.
    page_width, page_height = 420.0, 297.0
    drawing_x, drawing_y, drawing_width, drawing_height = 15.0, 15.0, 260.0, 220.0
    scale = min(drawing_width / source_width, drawing_height / source_height)
    placed_width, placed_height = source_width * scale, source_height * scale
    placed_x = drawing_x + (drawing_width - placed_width) / 2
    placed_y = drawing_y + (drawing_height - placed_height) / 2

    root.set("width", f"{page_width}mm")
    root.set("height", f"{page_height}mm")
    root.set("viewBox", f"0 0 {page_width} {page_height}")
    root.set("data-sheet-number", args.sheet_number)
    root.set("data-revision", args.revision)
    root.set("data-status", args.status)
    root.set("data-generated", date.today().isoformat())

    # Preserve defs/style, then move the existing drawing groups into a scaled viewport.
    preserved = [child for child in list(root) if child.tag.rsplit("}", 1)[-1] in {"defs", "style"}]
    drawing_group = element("g", id="ifc-drawing", transform=f"translate({placed_x:.3f} {placed_y:.3f}) scale({scale:.6f})")
    for child in list(root):
        if child not in preserved:
            root.remove(child)
            drawing_group.append(child)
    root.append(drawing_group)

    frame = element("rect", x=5, y=5, width=410, height=287, fill="none", stroke="#000", **{"stroke-width": 0.35})
    root.append(frame)
    root.append(element("rect", x=280, y=247, width=130, height=40, fill="white", stroke="#000", **{"stroke-width": 0.35}))
    root.append(element("line", x1=280, y1=259, x2=410, y2=259, stroke="#000", **{"stroke-width": 0.25}))
    root.append(element("line", x1=280, y1=273, x2=410, y2=273, stroke="#000", **{"stroke-width": 0.25}))
    root.append(element("line", x1=350, y1=247, x2=350, y2=287, stroke="#000", **{"stroke-width": 0.25}))
    text_node(root, args.project, 284, 253, 3.2, "bold")
    text_node(root, args.sheet_title, 284, 257, 2.6)
    text_node(root, "STATUS", 284, 264, 2.2, "bold")
    text_node(root, args.status, 295, 264, 2.2)
    text_node(root, "SCALE", 284, 270, 2.2, "bold")
    text_node(root, args.scale, 295, 270, 2.2)
    text_node(root, "REVISION", 284, 278, 2.2, "bold")
    text_node(root, args.revision, 295, 278, 2.2)
    text_node(root, "SHEET", 354, 278, 2.2, "bold")
    text_node(root, args.sheet_number, 354, 284, 6.0, "bold")
    text_node(root, "NOT FOR CONSTRUCTION", 284, 284, 2.2, "bold")

    args.output_svg.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(args.output_svg, encoding="utf-8", xml_declaration=True)
    ET.parse(args.output_svg)

    manifest = args.output_svg.with_suffix(".manifest.json")
    manifest.write_text(json.dumps({
        "source_svg": str(args.input), "sheet_number": args.sheet_number,
        "revision": args.revision, "scale": args.scale, "status": args.status,
        "page": "A3 landscape", "generated": date.today().isoformat(),
        "classification": "coordination-ready; professional review required",
    }, indent=2) + "\n", encoding="utf-8")

    if args.output_pdf:
        try:
            import cairosvg  # type: ignore
        except (ImportError, OSError):
            try:
                from reportlab.graphics import renderPDF  # type: ignore
                from svglib.svglib import svg2rlg  # type: ignore
            except ImportError:
                print("SVG sheet created; PDF skipped (no SVG-to-PDF renderer installed)")
            else:
                drawing = svg2rlg(str(args.output_svg))
                renderPDF.drawToFile(drawing, str(args.output_pdf))
                print(f"Wrote {args.output_pdf} using the ReportLab fallback")
        else:
            cairosvg.svg2pdf(url=str(args.output_svg), write_to=str(args.output_pdf))
            print(f"Wrote {args.output_pdf}")
    print(f"Wrote {args.output_svg} and {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
