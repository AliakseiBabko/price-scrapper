#!/usr/bin/env python3
"""Assert IFC wall connections are a COMPILED CONSEQUENCE of the ledger.

⚠️⚠️ THE FAILURE THIS PREVENTS IS A SECOND CORNER SOLVER.
`wall_corners.csv` decides ownership — thicker, then longer, with three corners
directed by the owner. IFC must reflect that decision and never make its own.
So the mapping is checked in BOTH directions:

  every junction in the ledger  →  exactly one IfcRelConnectsPathElements
  every IfcRelConnectsPathElements  →  a junction in the ledger

⚠️ AND `C_R1a_R1b` MUST HAVE NO CONNECTION. It is `continuous_casting`: one
monolithic pour, not a joint. A connection there would assert a junction inside
a single casting.

⚠️ PRIORITIES MUST STAY EMPTY until material layer sets exist. They are
per-layer, so writing them against single-material walls would mean inventing
layers for them to index.

    .venv-ifc314\\Scripts\\python.exe tools/ifc/check_connections.py --model out.ifc
"""
from __future__ import annotations

import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from connections_pass import (  # noqa: E402
    JUNCTION_KINDS, NON_JUNCTION_KINDS, load_corners)


def check(model):
    problems = []
    rows = load_corners()
    expected, forbidden = {}, set()
    for row in rows:
        kind = (row.get("kind") or "").strip()
        if kind in NON_JUNCTION_KINDS:
            forbidden.add(row["corner_id"])
        elif kind in JUNCTION_KINDS:
            expected[row["corner_id"]] = row
        else:
            problems.append(
                "corner %s has undeclared kind %r - it is neither emitted nor "
                "deliberately omitted" % (row["corner_id"], kind))

    connections = model.by_type("IfcRelConnectsPathElements")
    seen = {}
    for connection in connections:
        name = connection.Name
        if name in forbidden:
            problems.append(
                "%s has an IFC connection, but the ledger records it as "
                "`continuous_casting` - one monolithic pour has no joint"
                % name)
            continue
        if name not in expected:
            problems.append(
                "IFC carries a wall connection %r that the ledger does not - "
                "IFC may not invent a junction" % name)
            continue
        if name in seen:
            problems.append("%s has %d connections; a corner is one junction"
                            % (name, seen[name] + 1))
        seen[name] = seen.get(name, 0) + 1

        row = expected[name]
        owner = (row.get("owner") or "").strip()
        stopper = row["wall_b"] if owner == row["wall_a"] else row["wall_a"]
        # ⚠️ The OWNER runs through, so it is the one met ALONG ITS PATH.
        if connection.RelatedElement.Name != owner:
            problems.append(
                "%s: the ledger's owner is %s, but IFC has %s running through "
                "- the ownership decision has been re-made"
                % (name, owner, connection.RelatedElement.Name))
        if connection.RelatingElement.Name != stopper:
            problems.append("%s: expected %s to stop on the owner, IFC has %s"
                            % (name, stopper, connection.RelatingElement.Name))
        if connection.RelatedConnectionType != "ATPATH":
            problems.append("%s: the owner must be connected ATPATH, not %r"
                            % (name, connection.RelatedConnectionType))
        if connection.RelatingConnectionType not in ("ATSTART", "ATEND"):
            problems.append(
                "%s: the stopping wall must meet at an END (ATSTART/ATEND), "
                "not %r" % (name, connection.RelatingConnectionType))
        # ⚠️⚠️ PRIORITIES MUST ENCODE THE LEDGER'S DECISION.
        # IFC resolves a junction by letting the HIGHER priority protrude, so
        # the owner - which the ledger says runs through - must outrank the
        # wall that stops on it. If IFC's numbers said otherwise, IFC would be
        # deciding the junction, which is the second solver this forbids.
        relating = list(getattr(connection, "RelatingPriorities", None) or [])
        related = list(getattr(connection, "RelatedPriorities", None) or [])
        layered = bool(model.by_type("IfcMaterialLayerSet"))
        if layered and not related:
            problems.append(
                "%s has no RelatedPriorities although the model carries layer "
                "sets - the ledger's ownership would not survive into IFC"
                % name)
        if relating and related and min(related) <= max(relating):
            problems.append(
                "%s: the owner's priorities %s do not outrank the stopping "
                "wall's %s, so IFC would resolve this junction differently "
                "from wall_corners.csv" % (name, related, relating))
        # one priority per layer, or the list indexes nothing
        for element, values, label in (
                (connection.RelatedElement, related, "RelatedPriorities"),
                (connection.RelatingElement, relating, "RelatingPriorities")):
            import ifcopenshell.util.element as ue
            material = ue.get_material(element)
            layers = getattr(material, "MaterialLayers", None) if material else None
            want = len(layers) if layers else 0
            if len(values) != want:
                problems.append(
                    "%s.%s has %d entries for %d material layer(s) on %s"
                    % (name, label, len(values), want, element.Name))

    for name in expected:
        if name not in seen:
            problems.append(
                "junction %s is in the ledger but has NO IFC connection - the "
                "model has lost a joint the canonical data records" % name)
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default=os.path.join(
        REPO, "data", "outputs", "model_from_resolved.ifc"))
    a = ap.parse_args()

    import ifcopenshell
    model = ifcopenshell.open(a.model)
    problems = check(model)
    for problem in problems:
        print("FAIL %s" % problem)
    print("%d wall connection(s) against %d ledger corner(s)"
          % (len(model.by_type("IfcRelConnectsPathElements")),
             len(load_corners())))
    if problems:
        print("FAILED: %d problem(s)" % len(problems))
        return 1
    print("PASS - connections are a compiled consequence of wall_corners.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
