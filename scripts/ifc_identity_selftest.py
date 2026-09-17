#!/usr/bin/env python3
"""Gate IFC identity stability, and seed every way it can break.

⚠️ NOT BYTE-IDENTICAL FILES. OwnerHistory timestamps, entity ordering and STEP
line numbers differ harmlessly between builds. What is gated is the SEMANTIC
MAPPING - `canonical identity -> IFC class -> GlobalId` - which is the thing a
durable annotation, a diff or a review reference actually depends on.

⚠️ THE EASILY-MISSED HALF IS RELATIONSHIPS. Stabilising walls while
`IfcRelVoidsElement`, containment and type assignment re-mint themselves leaves
diffs just as noisy. `IfcRoot` covers relationships and property sets too, and
the seeds below check them explicitly.

    .venv-ifc314\\Scripts\\python.exe scripts/ifc_identity_selftest.py
"""
from __future__ import annotations

import io
import os
import subprocess
import sys
import tempfile
import uuid

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "ifc"))

import ifcopenshell  # noqa: E402

from identity import (  # noqa: E402
    IdentityError, guid_for, load_registry, relationship_uuid)

GENERATOR = os.path.join(REPO, "tools", "ifc", "model_from_resolved.py")
REGISTRY = os.path.join(REPO, "data", "canonical", "ifc_identity.csv")


def build(tag):
    out = os.path.join(tempfile.gettempdir(), "identity_%s.ifc" % tag)
    man = os.path.join(tempfile.gettempdir(), "identity_%s.json" % tag)
    proc = subprocess.run([sys.executable, GENERATOR, "--output", out,
                           "--manifest", man], capture_output=True, cwd=REPO)
    if proc.returncode != 0:
        raise SystemExit("build failed: %s"
                         % proc.stderr.decode("utf-8", "replace")[-400:])
    return out


def manifest_of(path):
    """`canonical identity -> class -> GlobalId`, for every IfcRoot."""
    model = ifcopenshell.open(path)
    rows = []
    for entity in model.by_type("IfcRoot"):
        name = getattr(entity, "Name", None)
        rows.append(("%s:%s" % (entity.is_a(), name or ""), entity.GlobalId))
    rows.sort()
    return rows


def main() -> int:
    failures = 0

    def check(label, ok, detail=""):
        nonlocal failures
        if ok:
            print("PASS %-54s %s" % (label, detail[:34]))
        else:
            print("FAIL %-54s %s" % (label, detail[:70]))
            failures += 1

    # ── 1 ─ TWO BUILDS, IDENTICAL SEMANTIC MANIFEST ──────────────────────────
    first = manifest_of(build("a"))
    second = manifest_of(build("b"))
    same = first == second
    detail = ""
    if not same:
        drifted = [a for a, b in zip(first, second) if a != b][:1]
        detail = "first drift: %s" % (drifted[0] if drifted else "length differs")
    check("two builds give an identical identity manifest", same,
          detail or "%d IfcRoot entries" % len(first))

    # ⚠️ and it must be non-trivial - a check that compares nothing passes
    check("the manifest is non-trivial", len(first) >= 150,
          "%d entries" % len(first))

    # ── 2 ─ RELATIONSHIPS ARE COVERED, not just products ─────────────────────
    model = ifcopenshell.open(build("c"))
    rels = model.by_type("IfcRelationship")
    psets = model.by_type("IfcPropertySet")
    check("relationships are present to be gated", len(rels) >= 50,
          "%d relationships" % len(rels))
    registry, _retired = load_registry(REGISTRY)
    lines = io.open(REGISTRY, encoding="utf-8").read().splitlines()
    minted = set(guid_for(v) for v in registry.values())
    rel_guids = set(r.GlobalId for r in rels) | set(p.GlobalId for p in psets)
    check("no relationship or pset reuses a MINTED product identity",
          not (rel_guids & minted),
          "%d overlaps" % len(rel_guids & minted))
    check("every relationship GlobalId is unique",
          len(rel_guids) == len(rels) + len(psets),
          "%d ids for %d entities" % (len(rel_guids), len(rels) + len(psets)))

    # ── 3 ─ GlobalId DERIVES ONLY FROM THE UUID ──────────────────────────────
    value = uuid.UUID("11111111-2222-3333-4444-555555555555")
    check("the same uuid always gives the same GlobalId",
          guid_for(value) == guid_for(str(value)), guid_for(value))
    check("a different uuid gives a different GlobalId",
          guid_for(value) != guid_for(uuid.uuid4()))

    # ⚠️ RENAMING MUST NOT MOVE IDENTITY. The uuid is what is immutable; the
    # key is a label on it, so a rename edits the key and keeps the uuid.
    # ⚠️ The first version of this seed compared guid_for(x) to guid_for(x) -
    # trivially true, and so a seed that COULD NOT FAIL. It now really renames
    # a row in a copy of the registry and re-reads it.
    any_key = sorted(registry)[0]
    before = guid_for(registry[any_key])
    renamed = []
    for line in lines:
        parts = line.split(",")
        if len(parts) > 1 and parts[1] == any_key:
            parts[1] = "IfcWall:RENAMED-BY-SEED"
            line = ",".join(parts)
        renamed.append(line)
    handle, path = tempfile.mkstemp(suffix=".csv")
    os.close(handle)
    try:
        io.open(path, "w", encoding="utf-8").write(
            chr(10).join(renamed) + chr(10))
        reloaded, _r = load_registry(path)
        after = guid_for(reloaded["IfcWall:RENAMED-BY-SEED"])
        check("RENAMING a key leaves its GlobalId untouched", before == after,
              "%s vs %s" % (before, after))
        check("...and the old key is gone, so the rename really happened",
              any_key not in reloaded, "old key absent")
    finally:
        os.unlink(path)

    # ── 4 ─ RELATIONSHIP DERIVATION ──────────────────────────────────────────
    a, b = uuid.uuid4(), uuid.uuid4()
    check("an UNORDERED relationship canonicalises endpoint order",
          relationship_uuid("IfcRelAggregates", [a, b])
          == relationship_uuid("IfcRelAggregates", [b, a]))
    # ⚠️ and an ORDERED one must NOT, or two different relationships collide
    check("an ORDERED relationship keeps its endpoint order",
          relationship_uuid("IfcRelVoidsElement", [a, b])
          != relationship_uuid("IfcRelVoidsElement", [b, a]))
    check("relationship kind participates in the identity",
          relationship_uuid("IfcRelAggregates", [a, b])
          != relationship_uuid("IfcRelContainedInSpatialStructure", [a, b]))

    # ── 5 ─ THE REGISTRY REFUSES WHAT IT MUST ────────────────────────────────
    dup = lines[:2] + [lines[1]] + lines[2:]          # same uuid twice
    handle, path = tempfile.mkstemp(suffix=".csv")
    os.close(handle)
    try:
        io.open(path, "w", encoding="utf-8").write("\n".join(dup) + "\n")
        try:
            load_registry(path)
            check("a duplicate canonical uuid is refused", False, "accepted")
        except IdentityError as exc:
            check("a duplicate canonical uuid is refused", True, str(exc)[:34])
    finally:
        os.unlink(path)

    # ⚠️ A RETIRED IDENTITY IS NEVER REUSED: retired rows still occupy their
    # uuid, so handing it to a new key must fail.
    retired_row = lines[1].split(",")
    retired_row[3] = "retired"
    seeded = lines[:1] + [",".join(retired_row)] + [
        ",".join([retired_row[0], "IfcWall:NEW", "IfcWall", "active", "", ""])]
    handle, path = tempfile.mkstemp(suffix=".csv")
    os.close(handle)
    try:
        io.open(path, "w", encoding="utf-8").write("\n".join(seeded) + "\n")
        try:
            load_registry(path)
            check("a RETIRED uuid cannot be reused", False, "accepted")
        except IdentityError as exc:
            check("a RETIRED uuid cannot be reused", True, str(exc)[:34])
    finally:
        os.unlink(path)

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
