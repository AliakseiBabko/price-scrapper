"""Find DXF dimension entities near known control measurements.

This is an evidence tool, not an automatic approval step. It helps locate
candidate CAD dimensions matching user-provided or visual-plan controls such as
the 1010 mm entrance opening, probable 910 mm door leaf, and 2310 mm entrance
hall depth. The output must still be reviewed against the drawing visually.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ezdxf


def _point_tuple(value: Any) -> list[float] | None:
    if value is None:
        return None
    try:
        return [round(float(value[0]), 3), round(float(value[1]), 3), round(float(value[2]), 3)]
    except Exception:
        return None


def _dimension_measurement(entity: Any) -> float | None:
    try:
        return float(entity.get_measurement())
    except Exception:
        return None


def _dimension_points(entity: Any) -> dict[str, list[float] | None]:
    fields = ["defpoint", "defpoint2", "defpoint3", "defpoint4", "defpoint5", "text_midpoint"]
    result: dict[str, list[float] | None] = {}
    for field in fields:
        try:
            result[field] = _point_tuple(entity.dxf.get(field))
        except Exception:
            result[field] = None
    return result


def find_candidates(source: Path, targets: list[float], tolerance: float) -> dict[str, Any]:
    doc = ezdxf.readfile(source)
    dimensions = list(doc.modelspace().query("DIMENSION"))
    target_reports = []
    for target in targets:
        matches = []
        for entity in dimensions:
            measurement = _dimension_measurement(entity)
            if measurement is None:
                continue
            delta = abs(measurement - target)
            if delta <= tolerance:
                text = str(entity.dxf.get("text", "") or "")
                matches.append(
                    {
                        "handle": entity.dxf.handle,
                        "layer": str(entity.dxf.get("layer", "")),
                        "dimension_type": int(entity.dxf.get("dimtype", 0) or 0),
                        "measurement_mm": round(measurement, 3),
                        "target_mm": round(target, 3),
                        "delta_mm": round(delta, 3),
                        "text_override": text or None,
                        "points": _dimension_points(entity),
                    }
                )
        matches.sort(key=lambda item: (item["delta_mm"], item["measurement_mm"], item["handle"]))
        target_reports.append(
            {
                "target_mm": round(target, 3),
                "tolerance_mm": tolerance,
                "match_count": len(matches),
                "matches": matches[:50],
                "truncated": len(matches) > 50,
            }
        )
    return {
        "report_version": "1.0.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(source),
        "dimension_entity_count": len(dimensions),
        "status": "candidate_search_only_manual_visual_confirmation_required",
        "targets": target_reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target-mm", type=float, action="append", required=True)
    parser.add_argument("--tolerance-mm", type=float, default=8.0)
    args = parser.parse_args()

    if not args.source.is_file():
        raise SystemExit(f"DXF not found: {args.source}")
    report = find_candidates(args.source, args.target_mm, args.tolerance_mm)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "targets": len(report["targets"]), "status": report["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
