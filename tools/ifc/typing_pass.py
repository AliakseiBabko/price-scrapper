#!/usr/bin/env python3
"""Emit real types and honest material associations. Steps 1-2 of the plan.

⚠️⚠️ WHAT THIS DELIBERATELY DOES NOT DO
---------------------------------------
**It does not invent a layer build-up.** A `IfcMaterialLayerSet` with render
and insulation layers we have never measured would look complete and be
fiction. Where only one material is known, ONE material is associated. Where
none is known — `M2` and `M6b`, the loggia enclosure, whose thickness record
contradicts itself — **nothing is associated**, and those walls go on failing
the material requirement. That failure is the honest state of our knowledge.

**It does not reconcile wall joints.** Layer priority and connection geometry
are only needed for MULTI-LAYER connection semantics, which is step 5. Types
and single-material association do not depend on it.

⚠️ AND A TYPE IS A REAL RELATIONSHIP, NOT A LABEL. Populating `ObjectType`
would satisfy a naive reading of the IDS designation requirement while no
`IfcRelDefinesByType` existed and nothing could be grouped. This emits the
relationship; `check_types_and_materials.py` asserts the relationship rather
than the label.

TYPE KEYS COME FROM MEASURED DATA
  walls    material + thickness      6 distinct kinds
  doors    width + head, from the opening record; `UNMEASURED` where absent
  windows  width + sill + head, likewise
"""
from __future__ import annotations

import io
import json
import os

import ifcopenshell.api
import ifcopenshell.util.element as ue

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MATERIALS = os.path.join(REPO, "data", "canonical", "wall_materials.json")

TYPE_CLASS = {"IfcWall": "IfcWallType", "IfcDoor": "IfcDoorType",
              "IfcWindow": "IfcWindowType"}


def _wall_materials(path=MATERIALS):
    with io.open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return dict((w.get("id"), w.get("material")) for w in data.get("walls", []))


def _round(value):
    """A dimension rounded to whole millimetres, or None."""
    if value is None:
        return None
    return int(round(float(value)))


def _opening_size(product):
    """(width, sill, head) from the model's own opening record."""
    psets = ue.get_psets(product)
    rec = psets.get("Pset_ApartmentOpening", {})
    sill = _round(rec.get("SillMM"))
    head = _round(rec.get("HeadMM"))
    width = None
    shape = getattr(product, "Representation", None)
    if shape is not None:
        try:
            import ifcopenshell.util.shape
            import ifcopenshell.geom
            settings = ifcopenshell.geom.settings()
            created = ifcopenshell.geom.create_shape(settings, product)
            geometry = created.geometry          # ⚠️ hold the reference
            verts = ifcopenshell.util.shape.get_vertices(geometry)
            xs = [v[0] for v in verts]
            ys = [v[1] for v in verts]
            width = _round(max(max(xs) - min(xs), max(ys) - min(ys)) * 1000.0)
        except Exception:                        # noqa: BLE001
            width = None
    return width, sill, head


def type_key(product, materials):
    """The type designation, from measured data only."""
    cls = product.is_a()
    if cls == "IfcWall":
        material = materials.get(product.Name)
        psets = ue.get_psets(product)
        thickness = _round(psets.get("Pset_ApartmentPhase", {}).get("ThicknessMM"))
        # ⚠️ `UNKNOWN` is stated, not guessed. M2 and M6b genuinely have no
        # recorded material and must not be given one to make a gate pass.
        return "WALL_%s_%s" % ((material or "UNKNOWNMATERIAL").upper(),
                               thickness if thickness is not None else "UNMEASURED")
    width, sill, head = _opening_size(product)
    stem = "DOOR" if cls == "IfcDoor" else "WINDOW"
    parts = [str(width) if width is not None else "UNMEASURED"]
    if cls == "IfcWindow":
        parts.append(str(sill) if sill is not None else "UNMEASURED")
    parts.append(str(head) if head is not None else "UNMEASURED")
    return "%s_%s" % (stem, "x".join(parts))


def apply_types(model):
    """Create types, assign them, and associate known materials. Returns stats."""
    materials = _wall_materials()
    made_types, assigned, associated, no_material = {}, 0, 0, []
    material_entities = {}

    for cls, type_cls in TYPE_CLASS.items():
        for product in model.by_type(cls):
            # ⚠️ by_type is inclusive of subtypes; guard against re-typing a
            # type entity itself.
            if product.is_a(type_cls):
                continue
            key = type_key(product, materials)
            entity = made_types.get(key)
            if entity is None:
                entity = ifcopenshell.api.run(
                    "root.create_entity", model, ifc_class=type_cls, name=key)
                made_types[key] = entity
            ifcopenshell.api.run("type.assign_type", model,
                                 related_objects=[product], relating_type=entity)
            assigned += 1

    # ⚠️⚠️ A PROPERTY ON THE TYPE IS HOW THE IDS TESTS THE RELATIONSHIP.
    # Requiring `ObjectType` would have been satisfied by a label with no
    # IfcRelDefinesByType behind it - the lookalike this must not accept.
    # Properties are inherited from type to instance, so an instance can only
    # carry `Pset_ApartmentType.TypeKey` if it is genuinely type-assigned.
    for key, entity in made_types.items():
        pset = ifcopenshell.api.run("pset.add_pset", model, product=entity,
                                    name="Pset_ApartmentType")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset,
                             properties={"TypeKey": key})

    # ⚠️ A proxy must say what it is. These two ARE vent shafts; naming them is
    # description, not invention.
    for proxy in model.by_type("IfcBuildingElementProxy"):
        if not proxy.ObjectType:
            proxy.ObjectType = "VENT_SHAFT"

    # ⚠️ MATERIAL ON THE TYPE, not the instance: a type carries material and
    # the instances inherit it, which is the schema's own arrangement.
    for key, entity in made_types.items():
        if not key.startswith("WALL_"):
            continue                      # door/window materials are unknown
        name = key.split("_")[1]
        if name == "UNKNOWNMATERIAL":
            no_material.append(key)
            continue                      # ⚠️ associate NOTHING rather than guess
        material = material_entities.get(name)
        if material is None:
            material = ifcopenshell.api.run("material.add_material", model,
                                            name=name.lower())
            material_entities[name] = material
        ifcopenshell.api.run("material.assign_material", model,
                             products=[entity], material=material)
        associated += 1

    return {"types": len(made_types), "assigned": assigned,
            "materials_associated": associated,
            "types_without_material": sorted(no_material),
            "type_names": sorted(made_types)}
