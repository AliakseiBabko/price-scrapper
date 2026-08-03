"""Run the pinned IfcConvert floor-plan export and perform basic output checks."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from xml.etree import ElementTree


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifc", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ifcconvert", type=Path, default=Path("tools/ifc/bin/IfcConvert.exe"))
    parser.add_argument("--section-height", type=float, default=1.2)
    parser.add_argument("--scale", default="1:100")
    parser.add_argument("--bounds", default="1000x1000")
    args = parser.parse_args()

    if not args.ifc.is_file():
        raise SystemExit(f"IFC file not found: {args.ifc}")
    if not args.ifcconvert.is_file():
        raise SystemExit(f"IfcConvert not found: {args.ifcconvert}")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        str(args.ifcconvert), "--yes", "--no-progress", "--bounds", args.bounds,
        "--scale", args.scale, "--section-height", str(args.section_height),
        "--door-arcs", "--use-element-names", "--filter-file",
        "tools/ifc/ifcconvert-floor-plan.filter", str(args.ifc), str(args.output),
    ]
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        return result.returncode
    if not args.output.is_file() or args.output.stat().st_size == 0:
        raise SystemExit("IfcConvert completed without a non-empty SVG output")

    root = ElementTree.parse(args.output).getroot()
    elements = root.findall(".//{http://www.w3.org/2000/svg}g[@data-name]")
    if not elements:
        raise SystemExit("SVG is valid XML but contains no IFC-named drawing elements")
    print(f"Wrote {args.output} with {len(elements)} IFC-named drawing elements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
