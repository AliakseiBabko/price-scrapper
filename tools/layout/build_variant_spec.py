#!/usr/bin/env python3
"""Generate a variant spec DIRECTLY from `ResolvedGeometry`. Schema v2.

⚠️⚠️ WHY THIS EXISTS
--------------------
`data/outputs/variants/v0-existing/spec.json` was an early SCHEMATIC carrying
its own `_retired` warning — 18 walls against 25, no ventilation shafts, a
rectangular loggia, invented opening verticals — and `compare_variants.py` read
it. So an owner acceptance of the gated DXF would have unblocked a comparison
sheet built from the superseded file. The acceptance would not have unblocked
the thing it claimed to.

⚠️ NO DXF COORDINATES ARE READ, AND NO SOLVER IS ADDED. Everything here comes
from `resolve()` — the same compiler the DXF and the IFC are generated from.
A spec built by reading the DXF back would be a second path to the same
geometry, and the two would drift exactly as the schematic did.

⚠️⚠️ SCHEMA v2 CARRIES REAL POLYGONS. v1's `horizontal + length + thickness`
rectangle cannot express a mitred wall: `M2` and `M6b` are cut on the лоджия
glazing plane and have five corners each. Representing them as rectangles
squares the mitre silently, and the лоджия's whole outline depends on it.

    .venv-ifc314\\Scripts\\python.exe tools/layout/build_variant_spec.py --write
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = os.path.join(REPO, "data", "outputs", "variants", "v0-existing",
                   "spec.json")

SCHEMA_VERSION = 2


def is_mitred(polygon):
    """True when any edge is neither horizontal nor vertical.

    ⚠ NOT a corner count. M2 is a mitred QUADRILATERAL - four points, one
    diagonal edge - so counting vertices missed it entirely and reported "no
    mitred walls" on a model that has two.
    """
    pts = list(polygon)
    for i in range(len(pts)):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % len(pts)]
        if abs(ax - bx) > 0.5 and abs(ay - by) > 0.5:
            return True
    return False


def _round_poly(polygon):
    return [[round(float(x), 1), round(float(y), 1)] for x, y in polygon]


def shell_signature(spec):
    """A hash over the STRUCTURAL SHELL only — frame, RC walls, façade, shafts.

    ⚠️⚠️ THIS IS WHAT TWO VARIANTS MUST SHARE BEFORE ANY DELTA IS COMPUTED.
    v0 and v1 were each built on their own shell — v1 from
    `current_apartment_shell.json` plus absolute Homestyler walls — so a
    difference between them mixed a layout decision with two different
    reconstructions of the same building. Partitions are deliberately EXCLUDED:
    they are what a variant is allowed to change.
    """
    shell = {
        "frame": spec.get("frame"),
        "walls": sorted(
            (w["id"], tuple(map(tuple, w["polygon_mm"])))
            for w in spec.get("walls", []) if w.get("structural")),
        "shafts": sorted(
            (s["id"], tuple(map(tuple, s["polygon_mm"])))
            for s in spec.get("shafts", [])),
    }
    return hashlib.sha256(
        json.dumps(shell, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


# ⚠️ A wall is STRUCTURAL - and therefore part of the shared shell that no
# variant may move - if it is the RC frame, the façade, or the loggia
# enclosure. Everything else is an infill partition a layout may change.
STRUCTURAL_CLASSES = ("concrete", "external", "loggia_enclosure")


def build():
    from resolve_v0_geometry import resolve
    resolved = resolve()

    frame = resolved.frame.as_dict() if hasattr(resolved.frame, "as_dict") else {}

    walls = []
    for wall in sorted(resolved.walls, key=lambda w: w["wall_id"]):
        wid = wall["wall_id"]
        walls.append({
            "id": wid,
            "class": wall.get("class"),
            "structural": wall.get("class") in STRUCTURAL_CLASSES,
            "thickness_mm": wall.get("thickness_mm"),
            "axis": wall.get("axis"),
            # ⚠️ BOTH polygons are published, deliberately. The PLAN polygon is
            # the 2D section - a doorway reads as the wall stopping - and the
            # BODY is the semantic solid, extended across a door head. They
            # differ and a consumer must choose knowingly.
            "polygon_mm": _round_poly(resolved.plan_polygons.get(wid) or []),
            "body_polygon_mm": _round_poly(resolved.body_polygons.get(wid) or []),
            "faces": dict(
                (role, {"endpoints": _round_poly(rec["endpoints"]),
                        "length_mm": round(rec["length_mm"], 1),
                        "outward_normal": list(rec["outward_normal"])})
                for role, rec in sorted((resolved.faces.get(wid) or {}).items())),
            "phase": "existing",
        })

    shafts = [{"id": s["shaft_id"], "polygon_mm": _round_poly(s["polygon"]),
               "room": s.get("room"), "channels": s.get("channels"),
               "immovable": True,
               "note": ("common property serving the whole riser - no layout "
                        "variant may touch it")}
              for s in sorted(resolved.shafts, key=lambda s: s["shaft_id"])]

    openings = [{"id": o["opening_id"], "kind": o["kind"],
                 "host_wall": o.get("host_wall") or o.get("recorded_wall"),
                 "hosting": o.get("hosting"), "axis": o.get("axis"),
                 "polygon_mm": _round_poly(o.get("polygon") or [])}
                for o in sorted(resolved.openings,
                                key=lambda o: str(o["opening_id"]))]

    loggia = [{"id": b["id"], "role": b.get("role"),
               "from_mm": b.get("from_mm"), "to_mm": b.get("to_mm"),
               "polygon_mm": _round_poly(b.get("polygon") or [])}
              for b in resolved.loggia_bays]

    spec = {
        "schema_version": SCHEMA_VERSION,
        "spec_id": "v0-existing",
        "name": "v0 - existing state, compiled",
        "status": "baseline",
        "units": "mm",
        "generated_by": "tools/layout/build_variant_spec.py",
        "!!_source": ("resolve_v0_geometry.resolve() ONLY. No DXF coordinate "
                      "is read and no second solver exists - a spec built by "
                      "reading the DXF back would drift from the compiler "
                      "exactly as the retired schematic did."),
        "!!_polygons_are_real": ("Walls carry POLYGONS, not horizontal+length+"
                                 "thickness. M2 and M6b are mitred on the "
                                 "glazing plane and have five corners; a "
                                 "rectangle squares that silently."),
        "frame": frame,
        "walls": walls,
        "shafts": shafts,
        "openings": openings,
        "loggia_bays": loggia,
        "!!_rooms_and_areas": (
            "DELIBERATELY ABSENT. Room areas may only be compared between "
            "variants when BOTH obtain them by the same method; v0's were the "
            "developer's published figures and v1's are Homestyler's own "
            "computation, and every delta mixing them is withdrawn."),
        "phase": "existing",
    }
    # ⚠ LEAVES vs UNITS. `O4` is ONE opening unit carrying TWO leaves - the
    # window O4a and the full-height loggia door O4b - so 11 leaves and 10
    # units are both true and neither alone describes it.
    import csv as _csv
    leaves = [r["opening_id"] for r in _csv.DictReader(io.open(
        os.path.join(REPO, "data", "canonical", "wall_openings.csv"),
        encoding="utf-8"))]
    spec["opening_leaves"] = sorted(leaves)
    spec["counts"] = {
        "walls": len(walls),
        "structural_walls": sum(1 for w in walls if w["structural"]),
        "opening_units": len(openings),
        "opening_leaves": len(leaves),
        "shafts": len(shafts),
        "loggia_bays": len(loggia),
        "mitred_walls": sorted(w["id"] for w in walls
                               if is_mitred(w["polygon_mm"])),
    }
    spec["shell_signature"] = shell_signature(spec)
    return spec


def load(path=OUT):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()

    spec = build()
    print("walls %d (structural %d), shafts %d, openings %d, loggia bays %d"
          % (len(spec["walls"]),
             sum(1 for w in spec["walls"] if w["structural"]),
             len(spec["shafts"]), len(spec["openings"]),
             len(spec["loggia_bays"])))
    print("opening leaves %d, units %d" % (spec["counts"]["opening_leaves"],
                                            spec["counts"]["opening_units"]))
    print("mitred wall(s): %s"
          % (", ".join(spec["counts"]["mitred_walls"]) or "none"))
    print("shell signature %s" % spec["shell_signature"][:16])
    if a.write:
        with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
            fh.write(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
        print("wrote %s" % os.path.relpath(a.out, REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
