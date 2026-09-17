#!/usr/bin/env python3
"""Seed the two LOOKALIKES that would satisfy a careless type requirement.

⚠️⚠️ THE POINT. The IDS designation requirement is a property carried by the
type and inherited. That is a good proxy, but two arrangements would read as
"typed" while no `IfcRelDefinesByType` existed and nothing could group:

  1. `ObjectType` populated with the type's name — a LABEL;
  2. `Pset_ApartmentType` attached DIRECTLY to each instance — a property that
     looks inherited and is not.

Both are seeded here and must be rejected. A gate nobody has watched fail is
not a gate, and a gate that accepts the imitation of the thing it checks is
worse than none.

    .venv-ifc314\\Scripts\\python.exe scripts/types_materials_selftest.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "ifc"))

import ifcopenshell  # noqa: E402
import ifcopenshell.api  # noqa: E402

from check_types_and_materials import check  # noqa: E402

GENERATOR = os.path.join(REPO, "tools", "ifc", "model_from_resolved.py")


def build():
    out = os.path.join(tempfile.gettempdir(), "types_selftest.ifc")
    man = os.path.join(tempfile.gettempdir(), "types_selftest.json")
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
            print("PASS %-56s %s" % (label, (problems[0][:30] if problems
                                             else "no problems")))
        else:
            print("FAIL %-56s wanted %s, got %d: %s"
                  % (label, want, len(problems), problems[:1]))
            failures += 1

    expect("the real model passes", check(ifcopenshell.open(base)), False)

    # ⚠️ LOOKALIKE 1 - the LABEL. Strip every type relationship and write the
    # type's name into ObjectType instead.
    model = ifcopenshell.open(base)
    for rel in model.by_type("IfcRelDefinesByType"):
        for obj in (rel.RelatedObjects or []):
            obj.ObjectType = rel.RelatingType.Name
        model.remove(rel)
    expect("ObjectType alone does NOT count as a type", check(model), True,
           "has NO IfcRelDefinesByType")

    # ⚠️ LOOKALIKE 2 - the property attached DIRECTLY to the instance, so it
    # looks inherited and is not.
    model = ifcopenshell.open(base)
    walls = [w for w in model.by_type("IfcWall") if not w.is_a("IfcWallType")]
    pset = ifcopenshell.api.run("pset.add_pset", model, product=walls[0],
                                name="Pset_ApartmentType")
    ifcopenshell.api.run("pset.edit_pset", model, pset=pset,
                         properties={"TypeKey": "FAKE"})
    expect("an instance-attached designation is caught", check(model), True,
           "DIRECTLY")

    # ⚠️ AN INVENTED BUILD-UP must be refused until the joint work is done.
    model = ifcopenshell.open(base)
    layer_set = model.create_entity("IfcMaterialLayerSet",
                                    LayerSetName="INVENTED")
    expect("an IfcMaterialLayerSet is refused for now", check(model), True,
           "may not be emitted until")
    model.remove(layer_set)

    # ⚠️ AN INVENTED MATERIAL on a wall whose material is unrecorded. Making a
    # gate pass by guessing is the failure this whole pass exists to avoid.
    model = ifcopenshell.open(base)
    # ⚠️ THE SEED INJECTS ITS OWN UNKNOWN. It used to name a real wall - M2,
    # then M6b - and each time the owner resolved that wall the seed kept
    # passing while testing nothing. Every wall now has a recorded material, so
    # naming one would make this seed permanently vacuous.
    victim = [w for w in model.by_type("IfcWall")
              if not w.is_a("IfcWallType")][0]
    material = ifcopenshell.api.run("material.add_material", model,
                                    name="guessed")
    ifcopenshell.api.run("material.assign_material", model,
                         products=[victim], material=material)
    expect("a GUESSED material on an unrecorded wall is caught",
           check(model, material_unknown={victim.Name}),
           True, "invented material is worse")

    # ...and removing a real one is caught too, so the check is not one-sided
    model = ifcopenshell.open(base)
    for rel in model.by_type("IfcRelAssociatesMaterial"):
        model.remove(rel)
    expect("a MISSING material on a recorded wall is caught", check(model),
           True, "material IS recorded")

    # a type of the wrong class
    model = ifcopenshell.open(base)
    rel = model.by_type("IfcRelDefinesByType")[0]
    wrong = ifcopenshell.api.run("root.create_entity", model,
                                 ifc_class="IfcFurnitureType", name="WRONG")
    rel.RelatingType = wrong
    expect("a type of the WRONG class is caught", check(model), True,
           "expected")

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
