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
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.tabular import ValidationError, finite, read_csv  # noqa: E402

TYPED = {"IfcWall": "IfcWallType", "IfcDoor": "IfcDoorType",
         "IfcWindow": "IfcWindowType"}

# Walls whose material is genuinely unrecorded.
# ⚠️ NOW EMPTY. M2 left on 2026-09-17 (owner rule 4 recorded it all along) and
# M6b the same day, when the owner stated its substrate directly. Every wall in
# the model now has a recorded material.
# ⚠️ The set is KEPT rather than deleted: it is the honest place for the next
# wall whose material is unknown, and an empty set states that today there is
# none - which is a different claim from the check not existing.
MATERIAL_UNKNOWN = set()


def check(model, material_unknown=None):
    """⚠️ `material_unknown` is injectable so a SEED never has to name a real
    wall that might later be resolved. Three seeds went stale that way - they
    used M2, then M6b, and each time the data improved they kept passing while
    testing nothing."""
    if material_unknown is None:
        material_unknown = MATERIAL_UNKNOWN
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
        known = wall.Name not in material_unknown
        if known and material is None:
            problems.append("IfcWall %r has no material association, but its "
                            "material IS recorded" % wall.Name)
        if not known and material is not None:
            problems.append(
                "IfcWall %r has a material association, but its material is "
                "NOT recorded anywhere - an invented material is worse than an "
                "absent one" % wall.Name)

    # ⚠️⚠️ LAYER SETS ARE NOW PERMITTED - and every layer must be RECORDED.
    # The rule did not become "anything goes": it became "no layer may be
    # invented". Each set is checked against wall_materials.json, so a render
    # layer nobody measured, or a thickness nobody stated, still fails.
    recorded = _recorded_walls()
    thicknesses = _recorded_thicknesses()
    insulations = _recorded_insulation()
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from typing_pass import _covering_extent, _placed_bands  # noqa: E402
    extents = _covering_extent()
    placed = _placed_bands()
    for wall in model.by_type("IfcWall"):
        if wall.is_a("IfcWallType"):
            continue
        material = ue.get_material(wall)
        layers = getattr(material, "MaterialLayers", None) if material else None
        if not layers:
            continue                      # single-material or unlayered
        record = recorded.get(wall.Name, {})
        # ⚠️ THICKNESS COMES FROM wall_blocks.csv, which is where it is
        # authoritative. Reading it from wall_materials.json silently SKIPPED
        # every wall that file does not carry a thickness for - most of the
        # R-series - so a wrong substrate thickness went unchecked there.
        want_substrate = thicknesses.get(wall.Name, record.get("thickness_mm"))
        # ⚠️⚠️ INSULATION WITH A RECORDED EXTENT IS NOT A LAYER, so no layer is
        # expected for it here - it must appear as an IfcCovering instead, which
        # is asserted separately below. A layer set is uniform through the wall
        # and says nothing about extent, so carrying M2's 570 mm band as a layer
        # asserted insulation along its whole length while the drawing showed
        # otherwise.
        want_insulation = (0 if extents.get(wall.Name)
                           else (insulations.get(wall.Name) or 0))
        substrate = [l for l in layers if (l.Name or "") == "substrate"]
        insulation = [l for l in layers if (l.Name or "") == "external insulation"]
        if len(layers) != len(substrate) + len(insulation):
            problems.append(
                "IfcWall %r has a layer named neither `substrate` nor "
                "`external insulation` - no layer may be invented" % wall.Name)
        if want_substrate is not None and substrate:
            got = round(substrate[0].LayerThickness * 1000.0)
            if abs(got - float(want_substrate)) > 0.5:
                problems.append(
                    "IfcWall %r substrate layer is %d mm, wall_materials.json "
                    "records %s" % (wall.Name, got, want_substrate))
        if want_insulation and not insulation:
            problems.append("IfcWall %r records %s mm insulation but carries "
                            "no insulation layer" % (wall.Name, want_insulation))
        if insulation and extents.get(wall.Name):
            lo, hi = extents[wall.Name]
            problems.append(
                "IfcWall %r carries an insulation LAYER, but its insulation is "
                "recorded with an EXTENT (%.1f..%.1f mm). A layer set is "
                "uniform through the wall and says nothing about extent, so "
                "this asserts insulation along the WHOLE wall - it belongs in "
                "an IfcCovering" % (wall.Name, lo, hi))
        elif insulation and not want_insulation:
            problems.append(
                "IfcWall %r carries an insulation layer, but "
                "wall_blocks.csv records none - insulation follows the "
                "RENDERED FACADE PLANE, not the thermal envelope, so it "
                "can never be inferred from a wall class or an exposure"
                % wall.Name)
        if insulation and want_insulation:
            got = round(insulation[0].LayerThickness * 1000.0)
            if abs(got - float(want_insulation)) > 0.5:
                problems.append(
                    "IfcWall %r insulation layer is %d mm, recorded %s"
                    % (wall.Name, got, want_insulation))

    # ⚠️⚠️ PARTIAL INSULATION, CHECKED BOTH WAYS so the model can neither lose
    # a recorded band nor invent one. The first version checked only that a
    # covering existed for each extent; that would have passed a model carrying
    # a covering for a wall with no recorded extent at all - insulation
    # conjured onto a wall, which is the M2/M6b conflation in a new costume.
    covered = {}
    for rel in model.by_type("IfcRelCoversBldgElements"):
        host = rel.RelatingBuildingElement
        for covering in (rel.RelatedCoverings or []):
            if covering.PredefinedType != "INSULATION":
                continue
            covered.setdefault(host.Name if host else None, []).append(covering)

    for wall_name, coverings in sorted(covered.items()):
        if wall_name not in extents:
            problems.append(
                "IfcWall %r carries an INSULATION covering, but wall_blocks.csv "
                "records no insulation extent for it - a covering may not "
                "invent a band" % wall_name)
            continue
        if len(coverings) > 1:
            problems.append("IfcWall %r has %d insulation coverings; the "
                            "record describes one band"
                            % (wall_name, len(coverings)))
        lo, hi = extents[wall_name]
        import ifcopenshell.util.element as _ue
        props = _ue.get_psets(coverings[0]).get("Pset_ApartmentInsulation", {})
        for key, want in (("ExtentFromMM", lo), ("ExtentToMM", hi),
                          ("ThicknessMM", insulations.get(wall_name) or 0)):
            got = props.get(key)
            if got is None or abs(float(got) - float(want)) > 0.5:
                problems.append(
                    "IfcWall %r insulation covering %s is %r, wall_blocks.csv "
                    "records %s" % (wall_name, key, got, want))

        # ⚠️⚠️ AND IT MUST HAVE A BODY THAT MATCHES THE DRAWN BAND. Properties
        # alone left the DXF showing a physical band and the model showing
        # nothing - a 2D/3D disagreement standing in for the semantic one. The
        # body is checked against the SAME placement the drawing renders, so
        # the two cannot drift apart again without this failing.
        if coverings[0].Representation is None:
            problems.append(
                "IfcWall %r insulation covering has NO body, but the DXF draws "
                "the band as physical geometry - one view may not show an "
                "element the other omits" % wall_name)
            continue
        want_band = placed.get(wall_name) or []
        if not want_band:
            problems.append(
                "IfcWall %r has an insulation covering but "
                "v0_insulation_placed.json holds no band - the placement is "
                "stale" % wall_name)
            continue
        try:
            import ifcopenshell.geom
            import ifcopenshell.util.shape
            shape = ifcopenshell.geom.create_shape(
                ifcopenshell.geom.settings(), coverings[0])
            verts = ifcopenshell.util.shape.get_vertices(shape.geometry)
        except Exception as exc:                    # noqa: BLE001
            problems.append("IfcWall %r insulation covering has a body that "
                            "will not evaluate: %s" % (wall_name, exc))
            continue
        got_box = (min(v[0] for v in verts) * 1000.0,
                   min(v[1] for v in verts) * 1000.0,
                   max(v[0] for v in verts) * 1000.0,
                   max(v[1] for v in verts) * 1000.0)
        want_box = (min(b[0] for b in want_band), min(b[1] for b in want_band),
                    max(b[2] for b in want_band), max(b[3] for b in want_band))
        if any(abs(a - b) > 1.0 for a, b in zip(got_box, want_box)):
            problems.append(
                "IfcWall %r insulation covering body is %s, but "
                "v0_insulation_placed.json - which is what the DXF draws - "
                "places the band at %s. The two views have drifted"
                % (wall_name, tuple(round(v, 1) for v in got_box),
                   tuple(round(v, 1) for v in want_box)))

    for wall_name in sorted(extents):
        if wall_name in covered:
            continue
        if not any(w.Name == wall_name for w in model.by_type("IfcWall")
                   if not w.is_a("IfcWallType")):
            continue                        # not in the model at all
        problems.append(
            "IfcWall %r has a RECORDED insulation extent but no insulation "
            "covering - the model has lost a band the canonical data carries, "
            "and a layer set cannot express one" % wall_name)
    return problems


def _recorded_thicknesses():
    """wall id -> solid thickness in mm, from wall_blocks.csv.

    ⚠️ `thickness_mm` ONLY. `solid_mm` and `clear_mm` are LENGTHS - solid_mm
    is clear_mm plus the corners a wall owns - and reading them here compared a
    250 mm thickness against a 1925 mm length.

    ⚠️⚠️ AND THE SHARED READERS, not DictReader + float. This checker shares
    its inputs with the thing it checks, so a nan it silently dropped would be a
    nan the compiler silently kept.
    """
    from typing_pass import BLOCKS
    out = {}
    for row in read_csv(BLOCKS, required=["wall_id", "thickness_mm"]):
        raw = (row.get("thickness_mm") or "").strip()
        if not raw:
            continue
        value = finite(raw)
        if value is None or value <= 0:
            raise ValidationError(
                "wall %s has thickness_mm %r, which is not a usable thickness"
                % (row.get("wall_id"), raw))
        out[row.get("wall_id")] = value
    return out


def _recorded_insulation():
    """wall id -> insulation mm, from wall_blocks.csv - the ONE source.

    ⚠️ Delegates to the compiler's own reader so the checker and the thing it
    checks cannot disagree about what the file says. What they must disagree
    about is what the MODEL says.
    """
    from typing_pass import _wall_insulation
    return _wall_insulation()


def _recorded_walls():
    import io as _io
    import json as _json
    path = os.path.join(REPO, "data", "canonical", "wall_materials.json")
    with _io.open(path, encoding="utf-8") as fh:
        data = _json.load(fh)
    return dict((w.get("id"), w) for w in data.get("walls", []))


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
