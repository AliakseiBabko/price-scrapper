#!/usr/bin/env python3
"""Assert that types and materials are REAL RELATIONSHIPS, not lookalikes.

⚠️⚠️ WHY THIS EXISTS SEPARATELY FROM THE IDS
--------------------------------------------
The IDS designation requirement is a property carried by the type and inherited
by the instance. That is a good proxy — an instance cannot inherit what it is
not typed to — but it is still a proxy, and two things would satisfy a careless
version of it while no `IfcRelDefinesByType` existed at all:

  1. populating `ObjectType` with the type's name, and
  2. attaching `Pset_ApartmentType` DIRECTLY to each instance.

Both would read as "typed" and neither would group, inherit or schedule. So the
relationship itself is asserted here, in Python, where it can be checked
exactly. Both lookalikes are seeded in `scripts/types_materials_selftest.py`.

⚠️ AND IT REFUSES AN INVENTED BUILD-UP. `IfcMaterialLayerSet` is NOT emitted
yet: layer priority and connection geometry must be reconciled with
`wall_corners.csv` first, and a render-plus-insulation assembly nobody measured
would look complete and be fiction. This fails if one appears before that work.

    .venv-ifc314\\Scripts\\python.exe tools/ifc/check_types_and_materials.py --model out.ifc
"""
from __future__ import annotations

import argparse
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TYPED = {"IfcWall": "IfcWallType", "IfcDoor": "IfcDoorType",
         "IfcWindow": "IfcWindowType"}

# Walls whose material is genuinely unrecorded. ⚠️ Listed so their absence is a
# KNOWN GAP rather than an unnoticed one - `wall_materials.json` leaves M2 and
# M6b unset deliberately, because its own thickness record contradicts itself.
MATERIAL_UNKNOWN = {"M2", "M6b"}


def check(model):
    import ifcopenshell.util.element as ue

    problems = []
    typed_by_rel = {}
    for rel in model.by_type("IfcRelDefinesByType"):
        for obj in (rel.RelatedObjects or []):
            typed_by_rel.setdefault(obj.id(), []).append(rel.RelatingType)

    for cls, type_cls in TYPED.items():
        for product in model.by_type(cls):
            if product.is_a(type_cls):
                continue
            relating = typed_by_rel.get(product.id())
            if not relating:
                problems.append(
                    "%s %r has NO IfcRelDefinesByType. A populated ObjectType "
                    "or an instance-attached property set would look typed and "
                    "group nothing" % (cls, product.Name))
                continue
            if len(relating) > 1:
                problems.append("%s %r is typed %d times"
                                % (cls, product.Name, len(relating)))
            entity = relating[0]
            if not entity.is_a(type_cls):
                problems.append("%s %r is typed by a %s, expected %s"
                                % (cls, product.Name, entity.is_a(), type_cls))
                continue
            # ⚠️ The property must come FROM the type. If the instance carries
            # its own copy, inheritance is not what satisfied the IDS.
            own = ue.get_psets(product, psets_only=True, should_inherit=False)
            if "Pset_ApartmentType" in own:
                problems.append(
                    "%s %r carries Pset_ApartmentType DIRECTLY - the "
                    "designation must be INHERITED from its type, or the IDS "
                    "is satisfied by a lookalike" % (cls, product.Name))
            from_type = ue.get_psets(entity, psets_only=True)
            if "Pset_ApartmentType" not in from_type:
                problems.append("%s %r does not carry Pset_ApartmentType"
                                % (type_cls, entity.Name))

    # ── materials ────────────────────────────────────────────────────────────
    for wall in model.by_type("IfcWall"):
        if wall.is_a("IfcWallType"):
            continue
        material = ue.get_material(wall)
        known = wall.Name not in MATERIAL_UNKNOWN
        if known and material is None:
            problems.append("IfcWall %r has no material association, but its "
                            "material IS recorded" % wall.Name)
        if not known and material is not None:
            problems.append(
                "IfcWall %r has a material association, but its material is "
                "NOT recorded anywhere - an invented material is worse than an "
                "absent one" % wall.Name)

    # ⚠️ NO INVENTED BUILD-UP, until the joint reconciliation is done.
    layer_sets = model.by_type("IfcMaterialLayerSet")
    if layer_sets:
        problems.append(
            "%d IfcMaterialLayerSet present. Multi-layer sets may not be "
            "emitted until canonical corner ownership is reconciled into IFC "
            "connection geometry and priorities - and no layer may be invented"
            % len(layer_sets))
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
    # ⚠️ `by_type` is INCLUSIVE of subtypes, so counting occurrences by
    # subtraction mis-reported. Count the occurrences themselves.
    typed = sum(1 for c, t in TYPED.items() for e in model.by_type(c)
                if not e.is_a(t))
    print("%d typed occurrence(s), %d type(s), %d material association(s)"
          % (typed, len(model.by_type("IfcTypeObject")),
             len(model.by_type("IfcRelAssociatesMaterial"))))
    if problems:
        print("FAILED: %d problem(s)" % len(problems))
        return 1
    print("PASS - types and materials are real relationships")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
