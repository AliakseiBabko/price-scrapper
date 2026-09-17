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

import io
import os
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "ifc"))
sys.path.insert(0, os.path.join(REPO, "tools"))

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

    # ⚠️⚠️ LAYER SETS ARE NOW EMITTED, so the rule is no longer "none allowed"
    # but "no layer invented". These seed the ways a layer could be fiction.
    import ifcopenshell.util.element as ue

    def layered_wall(m, name=None):
        for w in m.by_type("IfcWall"):
            if w.is_a("IfcWallType"):
                continue
            if name and w.Name != name:
                continue
            mat = ue.get_material(w)
            if getattr(mat, "MaterialLayers", None):
                return w, mat
        raise SystemExit("no layered wall found")

    # a render layer nobody measured
    model = ifcopenshell.open(base)
    wall, mat = layered_wall(model)
    render = model.create_entity("IfcMaterial", Name="render")
    mat.MaterialLayers = list(mat.MaterialLayers) + [model.create_entity(
        "IfcMaterialLayer", Material=render, LayerThickness=0.02,
        Name="render", Priority=10)]
    expect("an INVENTED render layer is caught", check(model), True,
           "no layer may be invented")

    # a substrate thickness that is not the recorded one
    model = ifcopenshell.open(base)
    wall, mat = layered_wall(model)
    mat.MaterialLayers[0].LayerThickness = 0.999
    expect("a substrate thickness that is not recorded is caught",
           check(model), True, "wall_materials.json records")

    # ⚠️ insulation on a wall recorded as having NONE - the M2/M6b conflation.
    # ⚠️ It FINDS such a wall rather than naming one: this seed named M2, and
    # M2's insulation changed twice in a day. A seed pinned to a wall id goes
    # vacuous the moment that wall's record moves.
    from check_types_and_materials import _recorded_insulation
    recorded_ins = _recorded_insulation()
    model = ifcopenshell.open(base)
    m2 = next(w for w in model.by_type("IfcWall")
              if not w.is_a("IfcWallType")
              and not recorded_ins.get(w.Name)
              and getattr(ue.get_material(w), "MaterialLayers", None))
    mat = ue.get_material(m2)
    wool = model.create_entity("IfcMaterial", Name="mineral wool")
    mat.MaterialLayers = list(mat.MaterialLayers) + [model.create_entity(
        "IfcMaterialLayer", Material=wool, LayerThickness=0.07,
        Name="external insulation", Priority=30)]
    expect("insulation on a wall recorded as having NONE is caught",
           check(model), True, "records none")

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

    # ⚠️⚠️ PARTIAL INSULATION. These four seed the defect that SHIPPED and the
    # ways its fix could quietly stop holding. M2's insulation covers 570 mm of
    # a much longer wall; `wall_blocks.csv` has recorded that interval all
    # along and `place_insulation.py` has clipped the drawn band to it, but the
    # IFC side read the thickness alone and emitted a uniform 200+150 layer
    # set. The drawing and the model disagreed about one wall, and both looked
    # complete.
    from typing_pass import _insulation_extent
    recorded_extents = _insulation_extent()

    def extent_wall(m):
        """⚠️ FOUND, never named. A seed pinned to `M2` goes vacuous the moment
        that wall's record changes - which M2's has, four times in three days."""
        for w in m.by_type("IfcWall"):
            if not w.is_a("IfcWallType") and w.Name in recorded_extents:
                return w
        raise SystemExit("no wall with a recorded insulation extent")

    # 1. the defect itself: the band expressed as a uniform LAYER
    model = ifcopenshell.open(base)
    wall = extent_wall(model)
    mat = ue.get_material(wall)
    wool = model.create_entity("IfcMaterial", Name="mineral wool")
    mat.MaterialLayers = list(mat.MaterialLayers) + [model.create_entity(
        "IfcMaterialLayer", Material=wool, LayerThickness=0.15,
        Name="external insulation", Priority=30)]
    expect("partial insulation emitted as a uniform LAYER is caught",
           check(model), True, "belongs in an IfcCovering")

    # 2. the band LOST
    model = ifcopenshell.open(base)
    for rel in model.by_type("IfcRelCoversBldgElements"):
        model.remove(rel)
    expect("a LOST insulation band is caught", check(model), True,
           "has lost a band")

    # 3. the band INVENTED on a wall that records no extent
    model = ifcopenshell.open(base)
    victim = next(w for w in model.by_type("IfcWall")
                  if not w.is_a("IfcWallType")
                  and w.Name not in recorded_extents)
    bogus = ifcopenshell.api.run("root.create_entity", model,
                                 ifc_class="IfcCovering", name="INS_BOGUS")
    bogus.PredefinedType = "INSULATION"
    model.create_entity("IfcRelCoversBldgElements", GlobalId="3" * 22,
                        Name="COVERS_BOGUS", RelatingBuildingElement=victim,
                        RelatedCoverings=[bogus])
    expect("an INVENTED insulation band is caught", check(model), True,
           "may not invent a band")

    # 4. the extent SILENTLY WIDENED - the band is present and wrong
    model = ifcopenshell.open(base)
    covering = [c for c in model.by_type("IfcCovering")
                if c.PredefinedType == "INSULATION"][0]
    for pset in (covering.IsDefinedBy or []):
        definition = getattr(pset, "RelatingPropertyDefinition", None)
        if definition is None or definition.Name != "Pset_ApartmentInsulation":
            continue
        for prop in definition.HasProperties:
            if prop.Name == "ExtentToMM":
                prop.NominalValue = model.create_entity(
                    "IfcReal", float(prop.NominalValue.wrappedValue) + 2000.0)
    expect("a WIDENED insulation extent is caught", check(model), True,
           "ExtentToMM")

    # ⚠️⚠️ THE COVERING'S BODY. Properties alone let the DXF draw a physical
    # 120 mm band while the model showed nothing - a 2D/3D disagreement
    # standing in for the semantic one. These seed both ways it could return.
    model = ifcopenshell.open(base)
    ins = [c for c in model.by_type("IfcCovering")
           if c.PredefinedType == "INSULATION"][0]
    ins.Representation = None
    expect("an insulation covering with NO body is caught", check(model), True,
           "may not show an element the other omits")

    # ⚠️ and a body that no longer matches the band the DRAWING renders
    model = ifcopenshell.open(base)
    ins = [c for c in model.by_type("IfcCovering")
           if c.PredefinedType == "INSULATION"][0]
    for point in model.by_type("IfcCartesianPoint"):
        if len(point.Coordinates) == 2 and abs(point.Coordinates[1] - 7.5472) < 1e-6:
            point.Coordinates = (point.Coordinates[0], 9.0)
    expect("a covering body that has DRIFTED from the drawn band is caught",
           check(model), True, "two views have drifted")

    # ⚠️⚠️ MALFORMED NUMBERS IN THE SOURCE FILE. These drive the REAL readers
    # over a REAL seeded CSV, because a fixture that cannot mutate an input
    # leaves that input reading as covered while nothing tests it.
    # `nan..7547.2` was ACCEPTED by the shipped version: `float("nan")` parses,
    # and every comparison against the result is false, so a malformed band
    # looks valid everywhere.
    import csv as _csv
    from typing_pass import BLOCKS, _insulation_extent, _wall_insulation
    from lib.tabular import ValidationError

    def seeded(mutate):
        rows = list(_csv.DictReader(io.open(BLOCKS, encoding="utf-8")))
        fields = list(rows[0].keys())
        for row in rows:
            if row["wall_id"] == "M2":
                mutate(row)
        handle, path = tempfile.mkstemp(suffix=".csv")
        os.close(handle)
        with io.open(path, "w", encoding="utf-8", newline="") as fh:
            writer = _csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def refuses(label, mutate, reader):
        nonlocal failures
        path = seeded(mutate)
        try:
            value = reader(path)
            print("FAIL %-56s ACCEPTED it: %s" % (label, str(value)[:30]))
            failures += 1
        except (ValidationError, ValueError) as exc:
            print("PASS %-56s %s" % (label, str(exc).strip()[:28]))
        finally:
            os.unlink(path)

    def set_extent(lo, hi):
        def mutate(row):
            row["insulation_from_mm"] = lo
            row["insulation_to_mm"] = hi
        return mutate

    refuses("a nan insulation EXTENT is refused",
            set_extent("nan", "7547.2"), _insulation_extent)
    refuses("an inf insulation extent is refused",
            set_extent("6977.2", "inf"), _insulation_extent)
    refuses("HALF an extent is refused, not read as full-length",
            set_extent("6977.2", ""), _insulation_extent)
    refuses("a REVERSED extent is refused",
            set_extent("7547.2", "6977.2"), _insulation_extent)
    refuses("a nan insulation THICKNESS is refused",
            lambda r: r.__setitem__("insulation_mm", "nan"), _wall_insulation)
    refuses("a negative insulation thickness is refused",
            lambda r: r.__setitem__("insulation_mm", "-120"), _wall_insulation)

    # ⚠️ ...and the SHAPE failures DictReader hides: a stray cell it drops, and
    # a missing one it turns into None.
    def with_line(extra):
        raw = io.open(BLOCKS, encoding="utf-8").read().rstrip("\n").split("\n")
        handle, path = tempfile.mkstemp(suffix=".csv")
        os.close(handle)
        io.open(path, "w", encoding="utf-8", newline="").write(
            "\n".join(raw[:2] + [extra] + raw[2:]) + "\n")
        return path

    for label, line in (
            ("a STRAY extra cell is refused", "SEED," * 20 + "SEED"),
            ("a MISSING cell is refused", "SEED,SEED")):
        path = with_line(line)
        try:
            _insulation_extent(path)
            print("FAIL %-56s ACCEPTED it" % label)
            failures += 1
        except (ValidationError, ValueError) as exc:
            print("PASS %-56s %s" % (label, str(exc).strip()[:28]))
        finally:
            os.unlink(path)

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
