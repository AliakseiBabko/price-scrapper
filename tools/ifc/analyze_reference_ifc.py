"""Summarize reference IFC structure for model and sheet conventions."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import ifcopenshell


def analyze(path: Path) -> dict:
    model = ifcopenshell.open(str(path))
    type_counts = Counter(entity.is_a() for entity in model)
    walls = model.by_type("IfcWall") + model.by_type("IfcWallStandardCase")
    spaces = model.by_type("IfcSpace")
    doors = model.by_type("IfcDoor")
    windows = model.by_type("IfcWindow")
    voids = model.by_type("IfcRelVoidsElement")
    fills = model.by_type("IfcRelFillsElement")
    void_host_names = Counter(rel.RelatingBuildingElement.is_a() for rel in voids if rel.RelatingBuildingElement)
    filled_names = Counter(rel.RelatedBuildingElement.is_a() for rel in fills if rel.RelatedBuildingElement)
    representation_types = Counter()
    for entity in model:
        representation = getattr(entity, "Representation", None)
        if representation:
            for shape in representation.Representations or []:
                representation_types[str(shape.RepresentationType)] += 1
    return {
        "source": str(path),
        "schema": model.schema,
        "entity_count": sum(1 for _ in model),
        "units": [unit.is_a() for unit in model.by_type("IfcUnit")],
        "spatial": {
            "projects": len(model.by_type("IfcProject")),
            "sites": len(model.by_type("IfcSite")),
            "buildings": len(model.by_type("IfcBuilding")),
            "storeys": len(model.by_type("IfcBuildingStorey")),
            "spaces": len(spaces),
        },
        "architecture": {
            "walls": len(walls),
            "slabs": len(model.by_type("IfcSlab")),
            "doors": len(doors),
            "windows": len(windows),
            "openings": len(model.by_type("IfcOpeningElement")),
            "void_relationships": len(voids),
            "void_host_types": dict(void_host_names),
            "fill_relationships": len(fills),
            "filled_element_types": dict(filled_names),
        },
        "representation_types": dict(representation_types),
        "top_entity_types": type_counts.most_common(30),
        "assessment": {
            "has_native_wall_opening_relationships": bool(voids),
            "has_native_door_window_fill_relationships": bool(fills),
            "useful_for": ["IFC spatial hierarchy", "native openings/fills", "geometry import regression"],
            "not_a_sheet_style_reference": "IFC carries model semantics; it does not define contractor sheet lineweights, title blocks, or regional drafting conventions.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = {"reports": [analyze(path) for path in args.source]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
