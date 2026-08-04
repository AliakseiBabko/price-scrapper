"""Create a reviewable, cropped DXF from a noisy Homestyler export.

The original DWG/DXF is never modified.  This tool selects the repeated plan
instance whose control dimensions agree with the current apartment evidence,
then retains only model-space entities intersecting that plan crop.

The result is a cleaned reference drawing, not native BIM and not a substitute
for field measurement.  It is intentionally conservative: unused block
definitions may remain in the file, while visible model-space noise outside
the selected crop is removed.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ezdxf
from ezdxf import bbox


def point_from_candidate(candidate: dict[str, Any]) -> tuple[float, float] | None:
    points = candidate.get("points") or {}
    point = points.get("text_midpoint") or points.get("defpoint") or points.get("defpoint2")
    if not point:
        return None
    return float(point[0]), float(point[1])


def select_instance(report: dict[str, Any]) -> dict[str, Any]:
    """Select the plan cluster supported by entrance, leaf, span, and hall depth."""
    by_target = {float(t["target_mm"]): t.get("matches", []) for t in report.get("targets", [])}
    entrance = [m for m in by_target.get(1010.0, []) if point_from_candidate(m)]
    leaf = [m for m in by_target.get(910.0, []) if point_from_candidate(m)]
    span = [m for m in by_target.get(3275.0, []) if point_from_candidate(m)]
    hall = [m for m in by_target.get(2310.0, []) if point_from_candidate(m)]

    candidates: list[dict[str, Any]] = []
    for e in entrance:
        ex, ey = point_from_candidate(e)  # type: ignore[misc]
        # The repeated plan dimensions are in the upper annotation band. The
        # lower band contains nearby 3D/detail measurements (often 1000/905),
        # which must not become the apartment-instance anchor.
        if ey < 30000 or ey > 35000:
            continue
        nearby_leaf = [
            m for m in leaf
            if 30000 < point_from_candidate(m)[1] < 35000
        ]
        nearby_span = [
            m for m in span
            if 30000 < point_from_candidate(m)[1] < 35000
        ]
        nearest_leaf = min(nearby_leaf, key=lambda m: abs(point_from_candidate(m)[0] - ex))
        nearest_span = min(nearby_span, key=lambda m: abs(point_from_candidate(m)[0] - ex))
        lx, ly = point_from_candidate(nearest_leaf)  # type: ignore[misc]
        sx, sy = point_from_candidate(nearest_span)  # type: ignore[misc]
        nearby_hall = [
            m for m in hall
            if abs(point_from_candidate(m)[0] - ex) < 5000
            and 26000 < point_from_candidate(m)[1] < 31000
        ]
        hall_match = min(nearby_hall, key=lambda m: abs(point_from_candidate(m)[0] - ex), default=None)
        score = 0
        if abs(lx - ex) < 2500 and abs(ly - ey) < 2500:
            score += 2
        if abs(sx - ex) < 5000 and abs(sy - ey) < 5000:
            score += 1
        if hall_match:
            score += 3
        # Prefer measurements closest to the user-provided controls when
        # several repeated dimension bands are otherwise equivalent.
        score -= min(abs(float(e.get("measurement_mm", 1010.0)) - 1010.0) / 10.0, 2.0)
        score -= min(abs(float(nearest_leaf.get("measurement_mm", 910.0)) - 910.0) / 10.0, 2.0)
        candidates.append({
            "anchor_x_mm": ex,
            "anchor_y_mm": ey,
            "entrance": e,
            "leaf": nearest_leaf,
            "span": nearest_span,
            "hall_depth": hall_match,
            "score": score,
        })
    if not candidates:
        raise ValueError("No repeated plan instance matched the supplied control candidates.")
    candidates.sort(key=lambda item: (-item["score"], item["anchor_x_mm"]))
    selected = candidates[0]
    if selected["score"] < 5:
        raise ValueError(f"No unambiguous control-dimension cluster found: {selected['score']=}")
    return {"selected": selected, "ranked_candidates": candidates}


def entity_bbox(entity: Any, doc: ezdxf.document.Drawing) -> tuple[float, float, float, float] | None:
    if entity.dxftype() == "INSERT":
        try:
            block = doc.blocks.get(str(entity.dxf.name))
            local = block_local_bbox(block)
            if local:
                x = float(entity.dxf.insert.x)
                y = float(entity.dxf.insert.y)
                return x + local[0], y + local[1], x + local[2], y + local[3]
        except Exception:
            pass
    try:
        extents = bbox.extents(entity, doc=doc)
        if extents.has_data:
            return float(extents.extmin.x), float(extents.extmin.y), float(extents.extmax.x), float(extents.extmax.y)
    except Exception:
        pass
    # Dimensions and a few imported symbols can have incomplete block metadata.
    points: list[tuple[float, float]] = []
    for attr in ("insert", "defpoint", "defpoint2", "textmidpoint"):
        try:
            value = getattr(entity.dxf, attr)
        except Exception:
            continue
        if hasattr(value, "x"):
            points.append((float(value.x), float(value.y)))
    if not points:
        return None
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs), max(ys)


def block_local_bbox(block: Any) -> tuple[float, float, float, float] | None:
    """Get a simple local block extent without relying on damaged block caches."""
    points: list[tuple[float, float]] = []
    for entity in block:
        for attr in ("start", "end", "insert", "center", "defpoint", "defpoint2"):
            try:
                value = getattr(entity.dxf, attr)
            except Exception:
                continue
            if hasattr(value, "x"):
                points.append((float(value.x), float(value.y)))
        if entity.dxftype() == "INSERT":
            try:
                value = entity.dxf.insert
                points.append((float(value.x), float(value.y)))
            except Exception:
                pass
    if not points:
        return None
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs), max(ys)


def intersects(box: tuple[float, float, float, float] | None, crop: tuple[float, float, float, float]) -> bool:
    if box is None:
        return False
    xmin, ymin, xmax, ymax = box
    cxmin, cymin, cxmax, cymax = crop
    return xmax >= cxmin and xmin <= cxmax and ymax >= cymin and ymin <= cymax


def clean(source: Path, candidates: Path, output: Path, margin_x: float, margin_y: float) -> dict[str, Any]:
    candidate_report = json.loads(candidates.read_text(encoding="utf-8"))
    selection = select_instance(candidate_report)
    selected = selection["selected"]
    anchor_x = selected["anchor_x_mm"]
    anchor_y = selected["anchor_y_mm"]
    doc = ezdxf.readfile(source)
    msp = doc.modelspace()
    wall_section = None
    for entity in msp:
        if entity.dxftype() != "INSERT" or str(entity.dxf.get("layer", "")) != "P-Wall-Section":
            continue
        # Plan dimension annotations sit above the apartment block. The
        # corresponding wall footprint is the nearby P-Wall-Section insert,
        # typically about 5.4 m below the dimension band in this export.
        if abs(float(entity.dxf.insert.x) - anchor_x) < 3000 and 22000 < float(entity.dxf.insert.y) < 29000:
            wall_section = entity
            break
    if wall_section is None:
        raise ValueError("Selected plan instance has no matching P-Wall-Section footprint.")
    local_wall_bbox = block_local_bbox(doc.blocks.get(str(wall_section.dxf.name)))
    if local_wall_bbox is None:
        raise ValueError("Selected P-Wall-Section has no readable geometry.")
    wall_bbox = (
        float(wall_section.dxf.insert.x) + local_wall_bbox[0],
        float(wall_section.dxf.insert.y) + local_wall_bbox[1],
        float(wall_section.dxf.insert.x) + local_wall_bbox[2],
        float(wall_section.dxf.insert.y) + local_wall_bbox[3],
    )
    # Keep a modest annotation margin around the actual wall footprint. This
    # includes dimensions/title annotations but excludes outside storage and
    # repeated elevation rows that a rectangular crop accidentally preserved.
    crop = (
        wall_bbox[0] - margin_x,
        wall_bbox[1] - margin_y,
        wall_bbox[2] + margin_x,
        wall_bbox[3] + margin_y,
    )
    before = Counter(str(entity.dxf.get("layer", "0")) for entity in msp)
    removed = Counter()
    kept = Counter()
    for entity in list(msp):
        if intersects(entity_bbox(entity, doc), crop):
            kept[str(entity.dxf.get("layer", "0"))] += 1
        else:
            removed[str(entity.dxf.get("layer", "0"))] += 1
            msp.delete_entity(entity)

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(output)
    report = {
        "report_version": "1.0.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(source),
        "output": str(output),
        "policy": "derived_reference_dxf_only_original_source_preserved",
        "selected_instance": {
            "anchor_mm": [round(anchor_x, 3), round(anchor_y, 3)],
            "crop_mm": [round(value, 3) for value in crop],
            "wall_footprint_bbox_mm": [round(value, 3) for value in wall_bbox],
            "score": selected["score"],
            "controls": {
                "entrance_opening": selected["entrance"].get("measurement_mm"),
                "door_leaf": selected["leaf"].get("measurement_mm"),
                "hall_depth": (selected["hall_depth"] or {}).get("measurement_mm"),
                "span": selected["span"].get("measurement_mm"),
            },
        },
        "modelspace": {
            "entities_before": sum(before.values()),
            "entities_kept": sum(kept.values()),
            "entities_removed": sum(removed.values()),
            "kept_by_layer": dict(sorted(kept.items())),
            "removed_by_layer": dict(sorted(removed.items())),
        },
        "status": "footprint_filtered_reference_underlay_requires_visual_review_in_dwg_trueview",
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--margin-x-mm", type=float, default=1500.0)
    parser.add_argument("--margin-y-mm", type=float, default=3500.0)
    args = parser.parse_args()
    result = clean(args.source, args.candidates, args.output, args.margin_x_mm, args.margin_y_mm)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
