"""Extract a safe, evidence-oriented summary from a converted apartment DXF.

This does not scale, flatten, or rewrite the source drawing.  Homestyler exports
architectural symbols as INSERT blocks, so the report records both layer and
block structure instead of pretending that every INSERT is a wall polyline.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import ezdxf

UNIT_LABELS = {0: "unitless", 1: "inches", 2: "feet", 4: "millimetres", 5: "centimetres", 6: "metres"}
INTERESTING_LAYERS = {
    "E-Wall", "E-Door", "E-Opening", "E-Window", "E-Switch",
    "E-Cabinet", "E-Movable Furniture", "P-Room", "P-Dimension Mark",
}


def dimension_summary(msp) -> dict:
    dimensions = list(msp.query("DIMENSION"))
    values: Counter[str] = Counter()
    override_count = 0
    for entity in dimensions:
        text = str(entity.dxf.get("text", "") or "")
        if text:
            override_count += 1
        try:
            value = round(float(entity.get_measurement()), 3)
        except Exception:
            continue
        values[str(value)] += 1
    return {
        "entity_count": len(dimensions),
        "override_text_count": override_count,
        "most_common_measured_values": [
            {"value": float(value), "count": count}
            for value, count in values.most_common(20)
        ],
        "note": "Dimension values are observations only; user control measurements govern provisional scaling.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--entrance-opening-mm", type=float, default=1010.0)
    parser.add_argument("--hall-depth-m", type=float, default=2.31)
    parser.add_argument("--hall-scenario-m", type=float, action="append", default=[2.28, 2.33])
    args = parser.parse_args()

    if not args.source.is_file():
        raise SystemExit(f"DXF not found: {args.source}")
    doc = ezdxf.readfile(args.source)
    msp = doc.modelspace()
    layer_entities: dict[str, Counter[str]] = defaultdict(Counter)
    block_names: dict[str, Counter[str]] = defaultdict(Counter)
    for entity in msp:
        layer = str(entity.dxf.get("layer", "0"))
        kind = entity.dxftype()
        layer_entities[layer][kind] += 1
        if layer in INTERESTING_LAYERS and kind == "INSERT":
            block_names[layer][str(entity.dxf.get("name", "<unnamed>"))] += 1

    insunits = int(doc.header.get("$INSUNITS", 0) or 0)
    scenario_values = [args.hall_depth_m, *args.hall_scenario_m]
    # Stable ordering and de-duplication make the report easy to diff.
    scenario_values = sorted({round(value, 3) for value in scenario_values})
    report = {
        "report_version": "1.0.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(args.source),
        "dxf": {
            "version": doc.dxfversion,
            "insunits_code": insunits,
            "insunits_label": UNIT_LABELS.get(insunits, "unknown"),
            "modelspace_entity_count": len(msp),
        },
        "layer_summary": {
            layer: dict(sorted(counts.items()))
            for layer, counts in sorted(layer_entities.items())
            if layer in INTERESTING_LAYERS
        },
        "block_summary": {
            layer: dict(sorted(counts.items()))
            for layer, counts in sorted(block_names.items())
        },
        "dimensions": dimension_summary(msp),
        "provisional_controls": {
            "entrance_opening_mm": {
                "value": args.entrance_opening_mm,
                "source": "user-provided measurement",
                "status": "accepted_for_provisional_scaling",
            },
            "dxf_control_match": {
                "status": "not_used_as_authority",
                "reason": "The DXF contains dimension entities and text overrides; no automatic match is promoted to a field measurement.",
            },
            "entrance_hall_depth_m": {
                "nominal": args.hall_depth_m,
                "scenarios": scenario_values,
                "source": "comparable reference plans; not the current apartment as-built measurement",
                "status": "provisional_sensitivity_parameter",
            },
        },
        "geometry_status": "planned_not_as_built",
        "next_measurement_gate": "Replace provisional controls with field measurements before procurement, permit, or construction issue.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote DXF extraction report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
