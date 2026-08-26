#!/usr/bin/env python3
"""Split the CAD model into the shell that never changes and the partitions that do.

Every layout option for this flat shares the same structural shell - the
exterior walls, the façade openings and the service blocks that are common
property. What varies between options is only the partitions. Modelling it that
way means an option is a short list of walls to add rather than a whole
building, and it makes the invariants literally impossible to edit by accident.

Produces:
  data/canonical/current_apartment_shell.json   the shell, as a base spec
  data/variants/v1-homestyler.json              the owner's design, as a patch

Usage:
  python tools/cad/split_shell_and_partitions.py [--threshold-mm 200]
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CAD = REPO / "data" / "canonical" / "current_apartment_cad.json"
SCHEDULES = REPO / "data" / "canonical" / "room_schedules.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold-mm", type=float, default=200.0,
                    help="walls at least this thick count as structural shell")
    ap.add_argument("--min-stub-mm", type=float, default=120.0,
                    help="shorter fragments than this are decomposition stubs, kept but flagged")
    a = ap.parse_args()

    cad = json.loads(CAD.read_text(encoding="utf-8"))
    schedules = json.loads(SCHEDULES.read_text(encoding="utf-8"))

    shell_walls, partitions = [], []
    for w in cad["walls"]:
        target = shell_walls if w["thickness_m"] * 1000 >= a.threshold_mm else partitions
        w = dict(w)
        if w["length_m"] * 1000 < a.min_stub_mm:
            w["note"] = "short fragment from slab decomposition - geometry is real, naming is not"
        target.append(w)

    shell_names = {w["name"] for w in shell_walls}
    shell_openings = [o for o in cad["openings"] if o.get("host_wall") in shell_names]
    partition_names = {w["name"] for w in partitions}
    other_openings = [o for o in cad["openings"] if o.get("host_wall") in partition_names]
    # Four openings sit in gaps too wide for the host search to bridge; they are
    # carried as a list to resolve, not silently dropped and not fed to a builder
    # that would refuse them.
    unresolved = [o for o in cad["openings"] if not o.get("host_wall")]

    shell = {
        "schema_version": "0.1.0",
        "spec_id": "current-apartment-shell",
        "name": "ZK Dubravinskiy - structural shell, common to every layout option",
        "status": "from_developer_layout_via_cad_not_field_verified",
        "units": "m",
        "storey_height_m": cad["storey_height_m"],
        "default_wall_thickness_m": 0.075,
        "exterior_wall_thickness_m": 0.25,
        "rooms": [],
        "wall_outline_mm": cad.get("wall_outline_mm", []),
        "walls": shell_walls,
        "openings": shell_openings,
        "fills": [],
        "space_boundaries": {},
        "electrical_plan": {},
        "plumbing_plan": [],
        "lighting": cad["lighting"],
        "finishes": {},
        "furniture": [],
        "constraints": schedules["developer_plan"].get("constraints", []),
        "evidence": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "derived_from": str(CAD.relative_to(REPO)),
            "rule": "Walls %d mm and thicker are treated as structural shell; thinner walls are "
                    "partitions and belong to a layout option, not to the shell."
                    % int(a.threshold_mm),
            "shell_walls": len(shell_walls),
            "partitions_moved_to_variant": len(partitions),
            "tolerance_reference": "data/canonical/dimension_tolerance.json",
            "area_convention": "Developer areas are clear (service blocks deducted). Never "
                               "compare them with БТИ gross areas - see the skill.",
            "caveats": [
                "The 200 mm threshold is a heuristic on thickness, not a structural survey. "
                "Nothing here has been checked against the building's structural drawings, so "
                "no wall may be assumed non-load-bearing on the strength of this file.",
                "Openings whose host wall is a partition move to the variant with it.",
            ],
        },
    }
    (REPO / "data" / "canonical" / "current_apartment_shell.json").write_text(
        json.dumps(shell, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    hs = schedules["homestyler_modified"]
    variant = {
        "schema_version": "0.1.0",
        "variant_id": "v1-homestyler",
        "name": "Вариант 1 - планировка владельца из Homestyler",
        "base_spec": "data/canonical/current_apartment_shell.json",
        "status": "owner_first_approximation",
        "concept": hs["relationship"],
        "authored_by": "apartment owner, in Homestyler; geometry extracted from the CAD export",
        "scope_note": "Layout only. Finishes, colour and decoration are explicitly not part of "
                      "this variant.",
        "room_schedule": hs["rooms"],
        "operations": [{"op": "wall.add", "wall": w} for w in partitions]
                      + [{"op": "opening.create", "opening": o} for o in other_openings],
        "unresolved_openings": unresolved,
        "evidence": {
            "areas": "_assets/floor_plan_modified.png",
            "geometry": "data/cad/dxf/20260727-ZK Dubravinskiy.dxf",
            "note": "The owner built this on the developer plan, so the shell is shared and only "
                    "the partitions differ. It is a first approximation of the wanted layout, "
                    "not a final decision.",
        },
    }
    (REPO / "data" / "variants" / "v1-homestyler.json").write_text(
        json.dumps(variant, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "shell_walls": len(shell_walls),
        "shell_openings": len(shell_openings),
        "partitions_in_variant": len(partitions),
        "openings_in_variant": len(other_openings),
        "openings_unresolved": len(unresolved),
        "shell_thicknesses_mm": sorted({round(w["thickness_m"] * 1000) for w in shell_walls}),
        "partition_thicknesses_mm": sorted({round(w["thickness_m"] * 1000) for w in partitions}),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
