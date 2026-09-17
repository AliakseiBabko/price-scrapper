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
import sys

import ifcopenshell.api
import ifcopenshell.util.element as ue

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))

# ⚠️ THE SHARED STRICT READERS, not csv.DictReader + float. AGENTS.md
# mandates them because DictReader drops a stray cell and turns a missing one
# into None, and float("nan") parses and then defeats every comparison it
# reaches. Both failures were live in this file.
from lib.tabular import ValidationError, finite, read_csv  # noqa: E402

MATERIALS = os.path.join(REPO, "data", "canonical", "wall_materials.json")

TYPE_CLASS = {"IfcWall": "IfcWallType", "IfcDoor": "IfcDoorType",
              "IfcWindow": "IfcWindowType"}


def _wall_materials(path=MATERIALS):
    with io.open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return dict((w.get("id"), w.get("material")) for w in data.get("walls", []))


BLOCKS = os.path.join(REPO, "data", "canonical", "wall_blocks.csv")


def _wall_insulation(path=BLOCKS):
    """wall id -> external insulation in mm, from wall_blocks.csv.

    ⚠️ ONE SOURCE. The column was already there; a second copy briefly existed
    in wall_materials.json on 2026-09-17 and the two disagreed within minutes -
    150 against 70 for M6b. Read per wall, never inferred from `class`: M2 and
    M6b are both `loggia_enclosure` and differ, 0 against 70.

    ⚠️ `read_csv` + `finite`, NEVER `DictReader` + `float`. `float("nan")`
    parses happily and then defeats every comparison it reaches, and a stray or
    missing cell slides past `DictReader` in silence. AGENTS.md requires the
    shared helpers for exactly this and I used the raw pair here anyway.
    """
    out = {}
    for row in read_csv(path, required=["wall_id", "insulation_mm"]):
        raw = (row.get("insulation_mm") or "").strip()
        if not raw:
            out[row.get("wall_id")] = 0.0
            continue
        value = finite(raw)
        if value is None or value < 0:
            raise ValidationError(
                "wall %s has insulation_mm %r, which is not a usable "
                "thickness. A non-finite value must FAIL here: it parses, then "
                "makes every comparison downstream meaningless"
                % (row.get("wall_id"), raw))
        out[row.get("wall_id")] = value
    return out


def _insulation_extent(path=BLOCKS):
    """wall id -> (from_mm, to_mm) for insulation that STOPS PARTWAY.

    ⚠️⚠️ THE DEFECT THIS CLOSES WAS A SPLIT BRAIN, not a missing feature.
    `wall_blocks.csv` has carried `insulation_from_mm`/`insulation_to_mm` for
    M2 since the owner supplied them - his лоджия wall is shared with the
    neighbour's along most of its run and exposed only at the southern end -
    and `tools/layout/place_insulation.py` has clipped the drawn band to that
    interval all along. The IFC side read `insulation_mm` ALONE, so the drawing
    showed 570 mm of insulation while the model asserted a uniform 200+150
    build-up over the whole wall. Two representations of one wall, disagreeing,
    each looking complete - which is the exact failure the compiler exists to
    prevent.

    ⚠️ A LAYER IS UNIFORM BY DEFINITION. `IfcMaterialLayerSet` is a stack of
    thicknesses through a wall, so it CANNOT express a layer that stops
    partway. Insulation with a recorded extent is therefore not a layer at all
    here - it becomes an `IfcCovering` bounded to the interval. See
    `apply_insulation_coverings`.

    ⚠️⚠️ `finite`, NOT `float`. `float("nan")` PARSES, and a nan extent then
    survives every downstream comparison because comparisons against it are all
    false - so a malformed interval would read as a valid band. This reader
    shipped with the raw pair and `nan..7547.2` was accepted.
    """
    out = {}
    for row in read_csv(path, required=["wall_id", "insulation_from_mm",
                                        "insulation_to_mm"]):
        wall = row.get("wall_id")
        lo_raw = (row.get("insulation_from_mm") or "").strip()
        hi_raw = (row.get("insulation_to_mm") or "").strip()
        if not lo_raw and not hi_raw:
            continue
        if not lo_raw or not hi_raw:
            raise ValidationError(
                "wall %s has half an insulation extent (%r..%r). One end alone "
                "describes no band, and must not be read as full-length"
                % (wall, lo_raw, hi_raw))
        lo, hi = finite(lo_raw), finite(hi_raw)
        if lo is None or hi is None:
            raise ValidationError(
                "wall %s has a non-finite insulation extent %r..%r - it parses "
                "and then makes every comparison against it false, so the band "
                "would look valid everywhere" % (wall, lo_raw, hi_raw))
        if hi <= lo:
            raise ValidationError(
                "wall %s has an insulation extent %.1f..%.1f that does not run "
                "forward - an empty or reversed band is not a band"
                % (wall, lo, hi))
        out[wall] = (lo, hi)
    return out


# ⚠️⚠️ THE EXISTING COVERING RECORD IS THE SOURCE OF TRUTH FOR WHAT IS BUILT.
# `wall_covering_patches.csv` states presence, extent and thickness per FACE,
# each with its own value state. The wall-wide columns stated one number per
# wall and every consumer read them its own way - which is precisely how this
# file came to assert a uniform 200+150 on M2 while the drawing showed 570 mm.
# ⚠️ `_wall_insulation` and `_insulation_extent` below are NOT dead: they are
# the legacy half of the parity bridge, and check_parity() runs them against
# the patches on every build. They stay strict, and they stay seeded.
def _covering():
    """{wall: {insulation_mm, side, extent_from_mm, extent_to_mm}} - BUILT."""
    import sys as _sys
    _sys.path.insert(0, os.path.join(REPO, "tools", "layout"))
    import covering_patches
    parity = covering_patches.check_parity()
    if parity:
        raise ValidationError(
            "the covering patches and the legacy wall_blocks columns "
            "disagree, so no build may proceed: %s" % "; ".join(parity))
    return covering_patches.legacy_equivalent()


def _covering_thickness():
    return dict((k, v["insulation_mm"]) for k, v in _covering().items())


def _covering_extent():
    """wall -> (from, to) in FACE-LOCAL mm, for a band that stops partway."""
    out = {}
    for wall, band in _covering().items():
        if band.get("extent_from_mm") is None:
            continue
        out[wall] = (band["from_mm"], band["to_mm"])
    return out


# ⚠️ STRUCTURE PROTRUDES INSULATION at a junction, which is the practitioner's
# own worked example (structure 50, insulation 30, finish 10). These are the
# layer-set defaults; a CONNECTION may override them, and does - compiled from
# wall_corners.csv so the ledger's ownership decision wins.
PRIORITY_SUBSTRATE = 50
PRIORITY_INSULATION = 30
INSULATION_MATERIAL = "mineral wool"


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
        insulation = _covering_thickness().get(product.Name) or 0
        # ⚠️ INSULATION IS PART OF THE KEY, because two walls of the same
        # material and thickness can differ only in it - M6b is insulated and
        # M2's main run is not - and without it they would share a type and one
        # build-up would silently win.
        # ⚠️⚠️ BUT ONLY WHEN IT RUNS THE WHOLE WALL. A type describes a uniform
        # cross-section, so insulation recorded with an EXTENT does not belong
        # in the designation: putting it there made M2's type assert 200+150
        # along its full length while the drawing showed 570 mm of it.
        if _covering_extent().get(product.Name):
            insulation = 0
        stem = "WALL_%s_%s" % ((material or "UNKNOWNMATERIAL").upper(),
                               thickness if thickness is not None else "UNMEASURED")
        return stem + ("_INS%d" % insulation if insulation else "")
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
    unlayered = []
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
    # ⚠️⚠️ AND NOW AS A LAYER SET, because the build-ups are recorded: the
    # owner confirmed 200 + 70 for M6b on 2026-09-17, and the warm perimeter is
    # 300 + 70. NO RENDER LAYER IS INVENTED - the owner named two values and
    # those are the two layers.
    def layers_for(key):
        """(material, substrate_mm, insulation_mm) from a wall type key.

        ⚠️ The material name may itself contain underscores -
        `REINFORCED_CONCRETE` - so it is taken as everything BETWEEN the
        `WALL_` prefix and the trailing thickness. The first version used
        `key.split("_")[1]` and silently named the material "reinforced".
        """
        parts = key.split("_INS")
        insulation = int(parts[1]) if len(parts) > 1 else 0
        stem = parts[0]
        assert stem.startswith("WALL_")
        body = stem[len("WALL_"):]
        name, _sep, thickness = body.rpartition("_")
        try:
            substrate_mm = float(thickness)
        except ValueError:
            # an unmeasured thickness: the material is still known
            return name, None, insulation
        return name, substrate_mm, insulation

    for key, entity in made_types.items():
        if not key.startswith("WALL_"):
            continue                      # door/window materials are unknown
        name, substrate_mm, insulation_mm = layers_for(key)
        if name == "UNKNOWNMATERIAL":
            no_material.append(key)
            continue                      # ⚠️ associate NOTHING rather than guess
        material = material_entities.get(name)
        if material is None:
            material = ifcopenshell.api.run("material.add_material", model,
                                            name=name.lower())
            material_entities[name] = material

        # ⚠️ AN L-SHAPED CASTING HAS NO SINGLE THICKNESS. A_NW_CORNER is one
        # monolithic pour whose two legs differ, so a LAYER SET - which is a
        # stack of uniform thicknesses through a wall - does not describe it.
        # It gets the honest single-material association instead.
        if substrate_mm is None:
            ifcopenshell.api.run("material.assign_material", model,
                                 products=[entity], material=material)
            associated += 1
            unlayered.append(key)
            continue

        layer_set = model.create_entity("IfcMaterialLayerSet",
                                        LayerSetName=key)
        layers = [model.create_entity(
            "IfcMaterialLayer", Material=material,
            LayerThickness=substrate_mm / 1000.0, Name="substrate",
            Priority=PRIORITY_SUBSTRATE)]
        if insulation_mm:
            insulation = material_entities.get(INSULATION_MATERIAL)
            if insulation is None:
                insulation = ifcopenshell.api.run(
                    "material.add_material", model, name=INSULATION_MATERIAL)
                material_entities[INSULATION_MATERIAL] = insulation
            layers.append(model.create_entity(
                "IfcMaterialLayer", Material=insulation,
                LayerThickness=insulation_mm / 1000.0, Name="external insulation",
                Priority=PRIORITY_INSULATION))
        layer_set.MaterialLayers = layers
        ifcopenshell.api.run("material.assign_material", model,
                             products=[entity], material=layer_set)
        associated += 1

    return {"types": len(made_types), "assigned": assigned,
            "materials_associated": associated,
            "single_material_no_layer_set": sorted(unlayered),
            "types_without_material": sorted(no_material),
            "type_names": sorted(made_types)}


PLACED = os.path.join(REPO, "data", "canonical", "v0_insulation_placed.json")


def _placed_bands(path=PLACED):
    """wall id -> the band rectangles `place_insulation.py` already resolved.

    ⚠️⚠️ THE SAME RECTANGLE THE DRAWING USES, deliberately. Re-deriving the band
    from the extent and thickness here would be a SECOND placement solver, and
    the whole reason this defect existed is that two representations of one wall
    were computed independently and drifted. The 2D band and the 3D body are now
    the same computed object rendered twice.
    """
    with io.open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    out = {}
    for band in data.get("bands", []):
        corners = [finite(band.get(k)) for k in ("x0", "y0", "x1", "y1")]
        if any(c is None for c in corners):
            raise ValidationError(
                "insulation band for %s has a non-finite corner %r - a band "
                "that cannot be located must FAIL, not be drawn at nan"
                % (band.get("wall_id"), corners))
        out.setdefault(band.get("wall_id"), []).append(tuple(corners))
    return out


def apply_insulation_coverings(model, make_solid=None, height_m=None):
    """Insulation that STOPS PARTWAY becomes an `IfcCovering`, not a layer.

    ⚠️⚠️ WHY A COVERING AND NOT A LAYER. `IfcMaterialLayerSet` is a stack of
    uniform thicknesses through a wall; it has no extent along the wall, so it
    can only ever say "all of it". M2's insulation covers 570 mm of a much
    longer wall, and expressing that as a layer made the model claim insulation
    it does not have. IFC4 has the right element for this - `IfcCovering` with
    `PredefinedType = INSULATION`, attached by `IfcRelCoversBldgElements`.

    ⚠️⚠️ AND IT CARRIES A REAL BODY. The first version gave the covering
    properties and no shape, on the reasoning that an assumed thickness should
    not become geometry. That was inconsistent rather than cautious: the DXF has
    been drawing the band as settled physical geometry the whole time, so
    omitting it from the 3D view alone left a 2D/3D disagreement in place of the
    semantic one just fixed. Uncertainty is expressed by ThicknessValueState,
    and it is expressed identically in both views or in neither.

    ⚠️ THE BODY IS NOT RE-DERIVED. It extrudes the rectangle
    `place_insulation.py` already resolved into v0_insulation_placed.json - the
    same object the drawing renders - because a second placement solver is
    exactly how the two views drifted apart in the first place.

    ⚠️ THE THICKNESS IS CARRIED WITH ITS VALUE STATE. Where insulation is
    required is a topological fact; how thick it is is a measurement, and M2's
    has none - the figure is the owner's stated assumption by symmetry with
    M6b. The two travel together so a consumer cannot mistake one for the
    other.
    """
    import ifcopenshell.api

    extents = _covering_extent()
    thicknesses = _covering_thickness()
    placed = _placed_bands()
    walls = dict((w.Name, w) for w in model.by_type("IfcWall")
                 if not w.is_a("IfcWallType"))

    made, missing = [], []
    material = None
    for wall_id, (lo, hi) in sorted(extents.items()):
        wall = walls.get(wall_id)
        if wall is None:
            # ⚠️ RECORDED but not in the model - stated, never skipped quietly.
            missing.append(wall_id)
            continue
        thickness = thicknesses.get(wall_id) or 0.0
        if not thickness:
            raise ValueError(
                "wall %s has an insulation EXTENT but no thickness. An extent "
                "without a thickness describes insulation of unknown depth; "
                "record the thickness or remove the extent" % wall_id)
        if material is None:
            material = ifcopenshell.api.run("material.add_material", model,
                                            name=INSULATION_MATERIAL)
        covering = ifcopenshell.api.run(
            "root.create_entity", model, ifc_class="IfcCovering",
            name="INS_%s" % wall_id)
        covering.PredefinedType = "INSULATION"
        covering.Description = (
            "external insulation over %.1f..%.1f mm of %s - compiled from "
            "wall_blocks.csv, which is also what place_insulation.py clips the "
            "drawn band to" % (lo, hi, wall_id))
        ifcopenshell.api.run("material.assign_material", model,
                             products=[covering], material=material)
        model.create_entity("IfcRelCoversBldgElements",
                            GlobalId="0" * 22,   # ⚠️ replaced by identity pass
                            Name="COVERS_%s" % wall_id,
                            RelatingBuildingElement=wall,
                            RelatedCoverings=[covering])
        pset = ifcopenshell.api.run("pset.add_pset", model, product=covering,
                                    name="Pset_ApartmentInsulation")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset, properties={
            "HostWall": wall_id,
            "ExtentFromMM": float(lo),
            "ExtentToMM": float(hi),
            "ThicknessMM": float(thickness),
            # ⚠️ EXTENT AND THICKNESS HAVE DIFFERENT AUTHORITY, so they say so.
            "ExtentBasis": "owner_stated",
            "ThicknessValueState": "assumed_not_measured",
        })
        # ⚠⚠ THE BODY, from the SAME placed rectangle the drawing uses.
        bodies = placed.get(wall_id) or []
        if make_solid is not None:
            if not bodies:
                raise ValidationError(
                    "wall %s has a recorded insulation extent but "
                    "v0_insulation_placed.json holds no band for it. The 3D "
                    "body and the drawn band come from ONE placement; a missing "
                    "one means the placement is stale, not that the band is "
                    "absent - re-run tools/layout/place_insulation.py" % wall_id)
            # ⚠ ONE covering, one body - several disjoint rectangles where the
            # band is interrupted, as Items of a single representation.
            make_solid(covering, [
                [(x0 / 1000.0, y0 / 1000.0), (x1 / 1000.0, y0 / 1000.0),
                 (x1 / 1000.0, y1 / 1000.0), (x0 / 1000.0, y1 / 1000.0)]
                for x0, y0, x1, y1 in bodies], 0.0, height_m)
        made.append({"wall": wall_id, "from_mm": lo, "to_mm": hi,
                     "thickness_mm": thickness, "bands": len(bodies)})

    return {"coverings": len(made), "detail": made,
            "recorded_but_not_in_model": sorted(missing)}
