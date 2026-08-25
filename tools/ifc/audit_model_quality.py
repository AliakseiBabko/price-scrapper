#!/usr/bin/env python3
"""Measure the geometric quality of an apartment model instead of eyeballing it.

Three questions this answers objectively:

  1. Do the openings actually cut the walls? (compares each wall's solid volume
     against its bounding box; a wall with a real void is smaller than its box)
  2. Is any wall modelled twice?
  3. How much material is double-counted where walls meet?

Walls built as independent boxes butt into each other at corners, so the shared
corner volume is counted twice in every quantity taken off the model. That is
invisible in a render and shows up as inflated finishes and material take-offs.

Usage:
  python tools/ifc/audit_model_quality.py --spec data/canonical/current_apartment_base.json
  python tools/ifc/audit_model_quality.py --ifc data/outputs/variants/base/model.ifc
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

DUPLICATE_MIN_OVERLAP = 0.9   # share of the smaller wall covered -> duplicate, not a junction
JUNCTION_BUDGET = 0.02        # double-counted volume tolerated, as a share of wall volume


def wall_bbox(w: dict) -> tuple[float, float, float, float]:
    t = w["thickness_m"]
    if w["horizontal"]:
        return (w["x_m"], w["y_m"], w["x_m"] + w["length_m"], w["y_m"] + t)
    return (w["x_m"], w["y_m"], w["x_m"] + t, w["y_m"] + w["length_m"])


def audit_spec(spec: dict) -> dict:
    height = spec.get("storey_height_m", 2.8)
    walls = spec["walls"]
    total = sum(w["length_m"] * w["thickness_m"] * height for w in walls)

    duplicates, junctions = [], []
    double_counted = 0.0
    for i in range(len(walls)):
        for j in range(i + 1, len(walls)):
            a, b = wall_bbox(walls[i]), wall_bbox(walls[j])
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox <= 1e-6 or oy <= 1e-6:
                continue
            volume = ox * oy * height
            double_counted += volume
            area_i = (a[2] - a[0]) * (a[3] - a[1])
            area_j = (b[2] - b[0]) * (b[3] - b[1])
            share = (ox * oy) / min(area_i, area_j)
            record = {"a": walls[i]["name"], "b": walls[j]["name"],
                      "overlap_mm": [round(ox * 1000), round(oy * 1000)],
                      "volume_m3": round(volume, 3), "share_of_smaller": round(share, 3)}
            (duplicates if share >= DUPLICATE_MIN_OVERLAP else junctions).append(record)

    hosted = {}
    for o in spec.get("openings", []):
        hosted.setdefault(o["host_wall"], []).append(o["name"])
    orphan_openings = [o["name"] for o in spec.get("openings", [])
                       if o["host_wall"] not in {w["name"] for w in walls}]

    return {
        "source": "spec",
        "wall_count": len(walls),
        "wall_volume_m3": round(total, 3),
        "duplicate_walls": duplicates,
        "junction_overlaps": junctions,
        "double_counted_m3": round(double_counted, 3),
        "double_counted_share": round(double_counted / total, 4) if total else 0.0,
        "walls_without_openings": sorted({w["name"] for w in walls} - set(hosted)),
        "orphan_openings": orphan_openings,
    }


def audit_ifc(path: Path) -> dict:
    import ifcopenshell
    import ifcopenshell.geom
    import numpy as np

    model = ifcopenshell.open(str(path))
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)

    def solid_volume(shape):
        v = np.array(shape.geometry.verts).reshape(-1, 3)
        idx = np.array(shape.geometry.faces).reshape(-1, 3)
        a, b, c = v[idx[:, 0]], v[idx[:, 1]], v[idx[:, 2]]
        return abs(float(np.sum(np.einsum("ij,ij->i", a, np.cross(b, c))) / 6.0)), v

    cut, uncut, failed = [], [], []
    for wall in model.by_type("IfcWall"):
        try:
            shape = ifcopenshell.geom.create_shape(settings, wall)
        except Exception as exc:  # a wall whose geometry will not build is itself a defect
            failed.append({"wall": wall.Name, "error": str(exc)[:120]})
            continue
        volume, verts = solid_volume(shape)
        size = verts.max(0) - verts.min(0)
        box = float(size[0] * size[1] * size[2])
        ratio = volume / box if box else 0.0
        record = {"wall": wall.Name, "volume_m3": round(volume, 3),
                  "bbox_m3": round(box, 3), "ratio": round(ratio, 3)}
        (cut if ratio < 0.985 else uncut).append(record)

    return {
        "source": str(path),
        "wall_count": len(model.by_type("IfcWall")),
        "walls_with_voids_cut": len(cut),
        "walls_without_voids": len(uncut),
        "geometry_failures": failed,
        "cut_detail": cut,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", type=Path, default=REPO / "data" / "canonical" / "current_apartment_base.json")
    ap.add_argument("--ifc", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero when duplicates exist or double counting exceeds the budget")
    a = ap.parse_args()

    report = {}
    if a.spec and a.spec.exists():
        report["spec_audit"] = audit_spec(json.loads(a.spec.read_text(encoding="utf-8")))
    if a.ifc:
        report["ifc_audit"] = audit_ifc(a.ifc)

    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sa = report.get("spec_audit")
    if sa:
        print("walls %d, volume %.2f m3" % (sa["wall_count"], sa["wall_volume_m3"]))
        print("duplicate walls: %d" % len(sa["duplicate_walls"]))
        for d in sa["duplicate_walls"]:
            print("  %s == %s  (%.0f%% of the smaller, %.3f m3)"
                  % (d["a"], d["b"], d["share_of_smaller"] * 100, d["volume_m3"]))
        print("junction overlaps: %d, double counted %.3f m3 (%.1f%% of wall volume)"
              % (len(sa["junction_overlaps"]), sa["double_counted_m3"],
                 sa["double_counted_share"] * 100))
        if sa["orphan_openings"]:
            print("openings with no host wall: %s" % ", ".join(sa["orphan_openings"]))
    ia = report.get("ifc_audit")
    if ia:
        print("IFC: %d walls, %d with voids cut, %d solid, %d failed to build"
              % (ia["wall_count"], ia["walls_with_voids_cut"], ia["walls_without_voids"],
                 len(ia["geometry_failures"])))

    if a.strict and sa:
        bad = bool(sa["duplicate_walls"]) or sa["double_counted_share"] > JUNCTION_BUDGET
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
