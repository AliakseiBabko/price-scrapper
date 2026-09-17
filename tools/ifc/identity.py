#!/usr/bin/env python3
"""Stable IFC identity: every `IfcRoot` gets a GlobalId that survives a rebuild.

⚠️⚠️ THE DEFECT THIS FIXES
--------------------------
`root.create_entity` and `new_guid()` mint a RANDOM GlobalId, so every rebuild
gave the same wall a different identity:

    run1  3ZhvrV1OzFdvQfK9LxCTqv
    run2  0iAXyw7RfE2AAXJQL2v2Yp     # same wall G3, same code

An authoritative issued representation whose identities change on every run
cannot carry a durable annotation, a diff, or a review reference.

⚠️ AND THE EASILY-MISSED HALF IS RELATIONSHIPS. Stabilising walls while
`IfcRelVoidsElement`, containment, type assignment and port connections
re-mint themselves leaves IFC diffs just as noisy, and makes a durable
reference to a relationship impossible. `IfcRoot` includes relationships and
types, so all of them are covered here.

THE RULES
  1. Every persistent element has an IMMUTABLE canonical UUID, minted ONCE and
     committed as authored identity in `data/canonical/ifc_identity.csv`.
  2. ⚠️ The GlobalId derives ONLY from that UUID - never from a name, a
     readable id, coordinates, geometry or array order. Renaming `G3` must not
     move its identity, and neither must reordering the input.
  3. ⚠️ Relationship identity is DERIVED, not minted: `uuid5` over the
     relationship kind plus its endpoint UUIDs, with endpoint order
     CANONICALISED where the relationship is unordered. So a relationship is
     stable exactly as long as the things it relates are.
  4. Duplicate canonical UUIDs are a hard error.
  5. ⚠️ A deleted identity is NEVER reused - `retired` rows stay in the
     registry precisely so the UUID cannot be handed to something else.

⚠️ NOT BYTE-IDENTICAL FILES. OwnerHistory timestamps, entity ordering and STEP
line numbers differ harmlessly between builds. What is gated is the SEMANTIC
MAPPING: `canonical identity -> IFC class -> GlobalId`.
"""
from __future__ import annotations

import csv
import io
import os
import uuid

import ifcopenshell.guid

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRY = os.path.join(REPO, "data", "canonical", "ifc_identity.csv")

# A fixed namespace so relationship UUIDs are reproducible across machines and
# runs. It is arbitrary but must never change once identities are committed.
RELATION_NS = uuid.UUID("6f1b8f4e-6c2a-4d9b-9a3e-2f5c7d8e1a04")

# Relationships whose endpoint order carries no meaning, so the endpoints are
# sorted before hashing. ⚠️ An ORDERED relationship must not be listed here:
# sorting it would make two genuinely different relationships collide.
UNORDERED = {
    "IfcRelAggregates",
    "IfcRelContainedInSpatialStructure",
    "IfcRelAssociatesMaterial",
    "IfcRelDefinesByProperties",
    "IfcRelDefinesByType",
    "IfcRelConnectsPorts",
}


class IdentityError(Exception):
    """The registry is unusable, or an entity has no identity."""


def guid_for(canonical_uuid):
    """The IFC GlobalId for a canonical UUID. The ONLY derivation permitted."""
    if not isinstance(canonical_uuid, uuid.UUID):
        canonical_uuid = uuid.UUID(str(canonical_uuid))
    return ifcopenshell.guid.compress(canonical_uuid.hex)


def relationship_uuid(kind, endpoint_uuids):
    """Deterministic identity for a relationship, from kind + endpoints.

    ⚠️ Derived rather than minted, so it needs no registry row and cannot go
    stale against the things it relates. Unordered kinds have their endpoints
    sorted first; ordered kinds keep their given order.
    """
    parts = [str(u) for u in endpoint_uuids]
    if kind in UNORDERED:
        parts = sorted(parts)
    return uuid.uuid5(RELATION_NS, kind + "|" + "|".join(parts))


def load_registry(path=REGISTRY):
    """key -> uuid for ACTIVE rows, raising on any duplicate.

    ⚠️ `retired` rows are loaded too, but only so their UUIDs can be refused to
    anything else. A deleted identity is never reused.
    """
    if not os.path.exists(path):
        raise IdentityError("no identity registry at %s - run mint_identities"
                            % os.path.relpath(path, REPO))
    active, seen_uuid, seen_key, retired = {}, {}, {}, set()
    with io.open(path, encoding="utf-8") as fh:
        for line, row in enumerate(csv.DictReader(fh), start=2):
            key = (row.get("key") or "").strip()
            raw = (row.get("canonical_uuid") or "").strip()
            state = (row.get("state") or "active").strip()
            if not key or not raw:
                raise IdentityError("row %d has no key or uuid" % line)
            try:
                value = uuid.UUID(raw)
            except ValueError:
                raise IdentityError("row %d: %r is not a UUID" % (line, raw))
            if value in seen_uuid:
                raise IdentityError(
                    "canonical_uuid %s is used by both %r and %r - a duplicate "
                    "identity means two things claim to be the same thing"
                    % (value, seen_uuid[value], key))
            seen_uuid[value] = key
            if state == "retired":
                retired.add(value)
                continue
            if key in seen_key:
                raise IdentityError("key %r appears twice (rows %d and %d)"
                                    % (key, seen_key[key], line))
            seen_key[key] = line
            active[key] = value
    return active, retired


def apply_identities(model, key_for, path=REGISTRY, strict=True):
    """Rewrite every `IfcRoot` GlobalId deterministically. Returns a manifest.

    `key_for(entity)` returns the canonical key for a product, or None if the
    entity is not a registered product (relationships, which are derived).

    ⚠️ IT WALKS `IfcRoot`, NOT `IfcProduct`. Types and relationships are
    `IfcRoot` too, and leaving them random was the half of the defect that
    would have kept diffs noisy even after the walls were fixed.
    """
    active, _retired = load_registry(path)
    assigned = {}
    manifest = []

    for entity in model.by_type("IfcRoot"):
        if entity.is_a("IfcRelationship"):
            continue
        if entity.is_a("IfcPropertySet"):
            continue                       # derived below, from its owner
        key = key_for(entity)
        if key is None:
            if strict:
                raise IdentityError(
                    "%s #%d (%r) has no canonical key - every persistent "
                    "element needs authored identity"
                    % (entity.is_a(), entity.id(), getattr(entity, "Name", None)))
            continue
        if key not in active:
            raise IdentityError(
                "%r is not in the identity registry. Mint it once and commit "
                "it; do NOT derive identity from the name" % key)
        value = active[key]
        entity.GlobalId = guid_for(value)
        assigned[entity.id()] = value
        manifest.append((key, entity.is_a(), entity.GlobalId))

    # ⚠️ EXPOSE THE CANONICAL UUID. The GlobalId derives from it, and writing
    # it into the file makes that derivation auditable from the file alone
    # rather than only from the registry beside it.
    import ifcopenshell.api
    for entity_id, value in list(assigned.items()):
        entity = model.by_id(entity_id)
        if not entity.is_a("IfcObject") and not entity.is_a("IfcTypeObject"):
            continue
        pset = ifcopenshell.api.run("pset.add_pset", model, product=entity,
                                    name="Pset_ApartmentIdentity")
        ifcopenshell.api.run("pset.edit_pset", model, pset=pset,
                             properties={"CanonicalId": str(value)})

    # ⚠️ PROPERTY SETS ARE DERIVED, from their owner plus their name - a
    # registry row for them would be a second source of truth for something
    # that has no independent existence.
    owners = {}
    # ⚠️ A TYPE's property sets hang off `HasPropertySets` directly - there is
    # no IfcRelDefinesByProperties for them - so a relationship-only lookup
    # left every type pset ownerless.
    for type_object in model.by_type("IfcTypeObject"):
        if type_object.id() not in assigned:
            continue
        for pset in (type_object.HasPropertySets or []):
            owners.setdefault(pset.id(), []).append(assigned[type_object.id()])
    for rel in model.by_type("IfcRelDefinesByProperties"):
        definition = getattr(rel, "RelatingPropertyDefinition", None)
        if definition is None:
            continue
        for obj in (rel.RelatedObjects or []):
            if obj.id() in assigned:
                owners.setdefault(definition.id(), []).append(assigned[obj.id()])
    for pset in model.by_type("IfcPropertySet"):
        holders = owners.get(pset.id())
        if not holders:
            raise IdentityError(
                "IfcPropertySet #%d (%r) is attached to nothing with a "
                "canonical identity" % (pset.id(), pset.Name))
        value = uuid.uuid5(RELATION_NS, "pset|%s|%s"
                           % ("|".join(sorted(str(h) for h in holders)),
                              pset.Name or ""))
        pset.GlobalId = guid_for(value)
        assigned[pset.id()] = value
        manifest.append(("pset:%s" % (pset.Name or ""), pset.is_a(),
                         pset.GlobalId))

    for entity in model.by_type("IfcRelationship"):
        endpoints = []
        for name in entity.get_info(include_identifier=False):
            if name in ("GlobalId", "OwnerHistory", "Name", "Description",
                        "type"):
                continue
            value = getattr(entity, name, None)
            for item in (value if isinstance(value, (list, tuple)) else [value]):
                if hasattr(item, "id") and item.id() in assigned:
                    endpoints.append(assigned[item.id()])
        if not endpoints:
            raise IdentityError(
                "%s #%d relates nothing with a canonical identity, so its own "
                "identity cannot be derived" % (entity.is_a(), entity.id()))
        value = relationship_uuid(entity.is_a(), endpoints)
        entity.GlobalId = guid_for(value)
        manifest.append(("rel:%s" % entity.is_a(), entity.is_a(),
                         entity.GlobalId))

    manifest.sort()
    return manifest
