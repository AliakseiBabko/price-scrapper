#!/usr/bin/env python3
"""Seed every way IFC could become a SECOND corner solver.

⚠️⚠️ The whole point of step 4 is that `wall_corners.csv` decides ownership and
IFC is told the answer. These seeds are the ways that could quietly stop being
true: a junction lost, a junction invented, an ownership flipped, a joint
asserted inside the monolithic casting, or priorities written against material
layers that do not exist.

⚠️ AND ONE SEED RECORDS A DEFECT THIS PASS ACTUALLY HAD. The first filter
allow-listed only `L` corners and silently dropped the three `owner_directed`
junctions - real joints, recorded as "MC extends onto R7 to CLOSE A JUNCTION".
An unrecognised kind must now raise.

    .venv-ifc314\\Scripts\\python.exe scripts/connections_selftest.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "ifc"))

import ifcopenshell  # noqa: E402

from check_connections import check  # noqa: E402
from connections_pass import JUNCTION_KINDS, NON_JUNCTION_KINDS, load_corners

GENERATOR = os.path.join(REPO, "tools", "ifc", "model_from_resolved.py")


def build():
    out = os.path.join(tempfile.gettempdir(), "connections_selftest.ifc")
    man = os.path.join(tempfile.gettempdir(), "connections_selftest.json")
    proc = subprocess.run([sys.executable, GENERATOR, "--output", out,
                           "--manifest", man], capture_output=True, cwd=REPO)
    if proc.returncode != 0:
        raise SystemExit("build failed: %s"
                         % proc.stderr.decode("utf-8", "replace")[-300:])
    return out


def main() -> int:
    failures = 0
    base = build()

    def expect(label, problems, want, needle=""):
        nonlocal failures
        hit = any(needle in p for p in problems) if needle else bool(problems)
        if hit == want:
            print("PASS %-56s %s" % (label, (problems[0][:28] if problems
                                             else "no problems")))
        else:
            print("FAIL %-56s wanted %s, got %d: %s"
                  % (label, want, len(problems), problems[:1]))
            failures += 1

    expect("the real model passes", check(ifcopenshell.open(base)), False)

    # ⚠️ Every junction kind in the ledger must be accounted for - the defect
    # that lost three owner_directed joints.
    kinds = set((r.get("kind") or "").strip() for r in load_corners())
    unaccounted = kinds - JUNCTION_KINDS - NON_JUNCTION_KINDS
    expect("every ledger corner kind is declared",
           ["undeclared: %s" % sorted(unaccounted)] if unaccounted else [],
           False)
    model = ifcopenshell.open(base)
    expect("all 7 junctions are emitted, not just the 4 `L` ones",
           [] if len(model.by_type("IfcRelConnectsPathElements")) == 7
           else ["%d connections" % len(model.by_type("IfcRelConnectsPathElements"))],
           False)

    # ── a junction LOST ──────────────────────────────────────────────────────
    model = ifcopenshell.open(base)
    model.remove(model.by_type("IfcRelConnectsPathElements")[0])
    expect("a lost junction is caught", check(model), True, "has NO IFC connection")

    # ── a junction INVENTED ──────────────────────────────────────────────────
    model = ifcopenshell.open(base)
    walls = [w for w in model.by_type("IfcWall") if not w.is_a("IfcWallType")]
    model.create_entity("IfcRelConnectsPathElements", GlobalId="1" * 22,
                        Name="C_INVENTED", RelatingElement=walls[0],
                        RelatedElement=walls[1],
                        RelatingConnectionType="ATEND",
                        RelatedConnectionType="ATPATH")
    expect("an INVENTED junction is caught", check(model), True,
           "may not invent a junction")

    # ⚠️ a joint asserted inside the monolithic casting
    model = ifcopenshell.open(base)
    named = dict((w.Name, w) for w in walls)
    model.create_entity("IfcRelConnectsPathElements", GlobalId="2" * 22,
                        Name="C_R1a_R1b",
                        RelatingElement=named["R1a"], RelatedElement=named["R1b"],
                        RelatingConnectionType="ATEND",
                        RelatedConnectionType="ATPATH")
    expect("a joint inside the monolithic casting is caught", check(model),
           True, "one monolithic pour has no joint")

    # ── OWNERSHIP FLIPPED - IFC re-deciding what the ledger decided ──────────
    model = ifcopenshell.open(base)
    connection = model.by_type("IfcRelConnectsPathElements")[0]
    connection.RelatingElement, connection.RelatedElement = (
        connection.RelatedElement, connection.RelatingElement)
    expect("a FLIPPED ownership is caught", check(model), True,
           "ownership decision has been re-made")

    # ── the owner connected at an END rather than along its path ─────────────
    model = ifcopenshell.open(base)
    model.by_type("IfcRelConnectsPathElements")[0].RelatedConnectionType = "ATEND"
    expect("the owner not connected ATPATH is caught", check(model), True,
           "must be connected ATPATH")

    # ⚠️ PRIORITIES WITHOUT LAYERS - inventing a layer to index
    model = ifcopenshell.open(base)
    model.by_type("IfcRelConnectsPathElements")[0].RelatingPriorities = [50]
    expect("priorities without any material layer set are caught", check(model),
           True, "invents one")

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
