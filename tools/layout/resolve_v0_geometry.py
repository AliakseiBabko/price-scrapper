# -*- coding: utf-8 -*-
"""THE geometry compiler: canonical authored data -> one resolved model.

WHY THIS EXISTS
---------------
The reconciliation that turns authored facts into geometry - corner closure,
лоджия loop closure, placement yielding and near-miss snapping - lived inside
`export_v0_dxf.py`. That made the DXF the only artefact that knew what the
geometry actually was, so a second consumer had to either re-implement the
reconciliation or read the DXF back. `model_from_dxf.py` does the second, which
is why 2D currently sits between the authored data and the 3D model.

That is the wrong shape. `on_element`, `along_wall_mm`, a wall face, a service
normal and a local->world transform have to mean EXACTLY the same thing in the
IFC and in every discipline sheet, and today only one script knows.

So the reconciliation moves here, and both exporters become serialisers over the
resolved model. This module holds no drawing code and no IFC code on purpose.

WHAT IT RETURNS, AND WHY ALL THREE PARTS
----------------------------------------
`resolve()` returns a `ResolvedGeometry` carrying:

  * `walls`    - the resolved geometry, after every reconciliation rule;
  * `sources`  - the PRE-RECONCILIATION value of every field a rule can move;
  * `report`   - machine-readable: which rule moved what, by how much, and why.

The second and third are not diagnostics. An authored figure carries a
measurement basis, and once closure or snapping has moved it, a consumer that
sees only the final number cannot tell a tape measurement from a value the
compiler nudged 12 mm to close a corner. Keeping the source value and the
rule that moved it is what stops the compiler becoming the same kind of
silent authority the retired schematic was.

WHAT THIS MODULE DOES NOT DO
----------------------------
It does not draw, it does not write IFC, and it does not invent geometry. Every
rule here already existed and is exercised by `check_dxf_closure` (24 seeded
defects), `raster_fidelity` (7), `check_wall_junctions` and
`vector_extent_oracle`. Those gates remain the permanent acceptance - NOT a
diff against the old implementation, because keeping the old reconciliation
around to compare against would make it a second authority, which is the defect
being removed.
"""
from __future__ import annotations

import copy
import csv
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PLACED = os.path.join(REPO, "data", "canonical", "v0_named_walls_placed.json")
ELEMENTS = os.path.join(REPO, "data", "canonical", "v0_elements_extracted.json")
BLOCKS = os.path.join(REPO, "data", "canonical", "wall_blocks.csv")

# Fields a reconciliation rule is allowed to move. Snapshotted before any rule
# runs, so the report can state a before and an after for each one.
MUTABLE_FIELDS = ("from_mm", "to_mm", "face_lo_mm", "face_hi_mm", "laid_length_mm")


class ResolvedGeometry(object):
    """The resolved model. Generated data - never authored, never hand-edited."""

    def __init__(self, walls, sources, report, elements, blocks, raw=None):
        self.walls = walls
        self.sources = sources
        self.report = report
        self.elements = elements
        self.blocks = blocks
        # Each rule's own return value, verbatim, for consumers that print it.
        self.raw = raw or {}

    def wall(self, wall_id):
        for w in self.walls:
            if w["wall_id"] == wall_id:
                return w
        return None

    def moved(self, wall_id):
        """Every rule that moved this wall, with before and after.

        The question a consumer actually needs to ask: is this number the one
        that was authored, or one the compiler adjusted?
        """
        return [m for m in self.report["movements"] if m["wall_id"] == wall_id]

    def as_dict(self):
        return {
            "walls": self.walls,
            "sources": self.sources,
            "report": self.report,
        }


def _load_blocks():
    with io.open(BLOCKS, encoding="utf-8") as fh:
        return {r["wall_id"]: r for r in csv.DictReader(fh)}


def _snapshot(walls):
    """Pre-reconciliation values of every movable field, by wall id."""
    out = {}
    for w in walls:
        out[w["wall_id"]] = {f: w.get(f) for f in MUTABLE_FIELDS}
    return out


def _movements(before, walls, rule):
    """Which walls this rule actually moved, and by how much.

    Compares field by field rather than trusting the rule's own return value:
    a rule that reports nothing while moving geometry is exactly the failure
    this report exists to make visible.
    """
    moves = []
    for w in walls:
        prev = before.get(w["wall_id"], {})
        for field in MUTABLE_FIELDS:
            old, new = prev.get(field), w.get(field)
            if old is None or new is None:
                continue
            if abs(float(new) - float(old)) > 1e-9:
                moves.append({
                    "wall_id": w["wall_id"],
                    "rule": rule,
                    "field": field,
                    "from": round(float(old), 3),
                    "to": round(float(new), 3),
                    "delta_mm": round(float(new) - float(old), 3),
                })
    return moves


def resolve(verbose=False):
    """Authored data -> resolved geometry, with provenance for every movement.

    The rule ORDER is the existing one and is load-bearing: corners are closed
    before the лоджия loop, the loop before yielding, yielding before snapping.
    Laying at clear and then closing corners is the only order under which a
    wall's drawn extent equals its recorded solid_mm - laying at solid and then
    closing counts the corner twice, which is how R8 once came out 2390 against
    a recorded 2090.
    """
    # Imported here, not at module load: the rules still live in the exporter
    # during the extraction. They move into this module once both consumers
    # read the resolved model and the gates have confirmed the move.
    from export_v0_dxf import (close_corners, close_loggia_loop,
                               snap_near_misses, yield_to_reference)

    # ⚠️ THE RULES READ CANONICAL FILES BY RELATIVE PATH, so they resolve
    # differently depending on the working directory - and they do it SILENTLY.
    # Run from tools/layout, close_corners found nothing and returned 0 fixes
    # instead of 8, yielding 16 of 25 walls closing against solid_mm instead of
    # 19. No error, just different geometry. A compiler that produces a
    # different model depending on where it was invoked from is not a compiler,
    # so the working directory is pinned here rather than assumed.
    previous_cwd = os.getcwd()
    os.chdir(REPO)
    try:
        return _resolve_in_repo(
            verbose, close_corners, close_loggia_loop,
            yield_to_reference, snap_near_misses)
    finally:
        os.chdir(previous_cwd)


def _resolve_in_repo(verbose, close_corners, close_loggia_loop,
                     yield_to_reference, snap_near_misses):
    with io.open(PLACED, encoding="utf-8") as fh:
        placed = json.load(fh)
    with io.open(ELEMENTS, encoding="utf-8") as fh:
        elements = json.load(fh)

    walls = placed["walls"]
    sources = _snapshot(walls)
    authored = copy.deepcopy(sources)

    report = {
        "inputs": {
            "placed": os.path.relpath(PLACED, REPO).replace("\\", "/"),
            "elements": os.path.relpath(ELEMENTS, REPO).replace("\\", "/"),
            "blocks": os.path.relpath(BLOCKS, REPO).replace("\\", "/"),
            "placed_authoritative_for": placed.get("authoritative_for"),
        },
        "rules_in_order": [],
        "movements": [],
    }

    # The rules' own return values are kept verbatim. The DXF exporter prints
    # them, and reproducing that output exactly is part of showing the
    # extraction changed nothing: a serialiser that reports differently is a
    # serialiser whose inputs may differ.
    raw = {}
    for name, run in (
        ("close_corners", lambda: close_corners(walls)),
        ("close_loggia_loop", lambda: close_loggia_loop(walls, elements.get("loggia_glazing"))),
        ("yield_to_reference", lambda: yield_to_reference(walls)),
        ("snap_near_misses", lambda: snap_near_misses(walls)),
    ):
        before = _snapshot(walls)
        returned = run()
        raw[name] = returned
        moves = _movements(before, walls, name)
        report["rules_in_order"].append({
            "rule": name,
            "reported": len(returned) if returned is not None else 0,
            "measured_movements": len(moves),
        })
        report["movements"].extend(moves)

    blocks = _load_blocks()

    # The standing invariant, computed here so every consumer sees the same
    # verdict rather than reading it off the exporter's console output.
    drawn_vs_solid = []
    for w in walls:
        recorded = blocks.get(w["wall_id"], {}).get("solid_mm")
        if not recorded or w.get("from_mm") is None:
            continue
        drawn = float(w["to_mm"]) - float(w["from_mm"])
        drawn_vs_solid.append({
            "wall_id": w["wall_id"],
            "drawn_mm": round(drawn, 1),
            "solid_mm": float(recorded),
            "delta_mm": round(drawn - float(recorded), 1),
        })
    report["drawn_vs_solid"] = drawn_vs_solid
    report["drawn_vs_solid_within_15mm"] = sum(
        1 for r in drawn_vs_solid if abs(r["delta_mm"]) <= 15.0)

    if verbose:
        print("resolved %d walls; %d movements across %d rules"
              % (len(walls), len(report["movements"]), len(report["rules_in_order"])))

    return ResolvedGeometry(walls, authored, report, elements, blocks, raw)


def main():
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", help="write the reconciliation report as JSON")
    a = ap.parse_args()

    resolved = resolve(verbose=True)
    for rule in resolved.report["rules_in_order"]:
        print("   %-20s reported %2d, measured %2d movement(s)"
              % (rule["rule"], rule["reported"], rule["measured_movements"]))
    print("drawn == solid_mm within 15 mm: %d of %d"
          % (resolved.report["drawn_vs_solid_within_15mm"],
             len(resolved.report["drawn_vs_solid"])))

    if a.report:
        os.makedirs(os.path.dirname(os.path.abspath(a.report)), exist_ok=True)
        with io.open(a.report, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(resolved.as_dict(), ensure_ascii=False, indent=2))
        print("wrote %s" % a.report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
