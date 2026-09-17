#!/usr/bin/env python3
"""Strict schema gate for the draft TARGET records. Step 2 of pass 2.

The coverage gate answers *"was every source carried forward?"*. It says
nothing about whether a target record is well formed, so a row could cite a
real locator, declare a real concept, and still be meaningless.

⚠️ THE SCHEMA IS DECLARED IN `_Inbox/migration/draft/README.md`, NOT HERE.
------------------------------------------------------------------------
This file ENFORCES that document; it does not get to invent it. The order
matters and was nearly got wrong: building the validator before any target
records existed would have made every typed-column decision silently, inside
validator code, where nobody reviews a schema. The records came first, and
this checks them.

WHAT IT CHECKS
  1. `migration_key` is present and UNIQUE ACROSS EVERY TABLE - it is the
     handle other records point at, so a collision silently merges two things.
  2. `target_concept` is valid AND matches the table it is in.
  3. Required columns are present and non-empty, per concept.
  4. ⚠️ FORBIDDEN columns are EMPTY, per locator kind. A `surface_local`
     occurrence carrying `face_ref` is not a harmless extra field: it is two
     incompatible placements in one row, and whichever the generator reads
     first wins.
  5. Every internal reference (`subject_key`, `member_keys`,
     `parent_assembly_key`, `disputed_with`) resolves to a real key.
  6. Typed assertion values parse as their declared `value_type`.
  7. ⚠️ `scope_apartment` is present on every observation and assertion. This
     is the column that makes the comparable-flat rule (design §3.0f)
     ENFORCEABLE rather than a convention in a notes field.
  8. An unknown `locator_kind` FAILS. It is never skipped.

    .venv\\Scripts\\python.exe tools/services/check_target_schema.py
"""
from __future__ import annotations

import argparse
import csv
import glob
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRAFTS = os.path.join(REPO, "_Inbox", "migration", "draft")

MATERIALS = os.path.join(REPO, "data", "canonical", "wall_materials.json")

# Not walls, but legitimate subjects: the shafts the model carries, the rooms
# a CSV row is scoped to, the slab set a ceiling point sits in, and the flat
# itself for a claim about the whole installation.
PSEUDO_ELEMENTS = {
    "flat", "slabs", "V1", "V2", "P1", "P2", "T1",
    "corridor", "kitchen_living", "middle_room", "small_bedroom", "toilet",
    "bathroom", "loggia", "horizontal_main", "SH-B",
}

CONCEPTS = {"occurrence", "assembly", "observation", "assertion", "value",
            "approval", "connectivity", "route", "relation"}

# Which concept each table carries. A row in the wrong file is a real defect:
# the typed columns around it do not apply to it.
TABLE_CONCEPT = {
    "occurrences.csv": "occurrence", "assemblies.csv": "assembly",
    "observations.csv": "observation", "assertions.csv": "assertion",
    "relations.csv": "relation", "routes.csv": "route",
    "values.csv": "value", "approvals.csv": "approval",
    "connectivity.csv": "connectivity",
}

REQUIRED = {
    "occurrence": ("service_kind", "phase", "locator_kind", "placement_state"),
    "assembly": ("assembly_kind", "member_keys"),
    "observation": ("observed_what", "scope_kind", "scope_ref", "observed_via"),
    "assertion": ("property", "value_type", "polarity", "knowledge_basis",
                  "value_state", "scope_kind", "scope_ref"),
    "relation": ("relation_kind", "legacy_id"),
    # ⚠️ `route` had NO contract at all, so a blank route row would have
    # passed, and routes carried no phase, basis or state.
    "route": ("route_kind", "route_state", "from_ref", "to_ref",
              "knowledge_basis", "value_state", "scope_kind", "scope_ref",
              "scope_phase"),
}

RELATION_KINDS = {"alias_of", "duplicate_of", "member_of", "connects_to",
                  "supersedes", "contradicts"}
ROUTE_STATES = {"topology_only", "routed", "as_built"}

WALL_COLS = ("host_ref", "face_ref", "along_face_mm", "vertical_mm")
SURFACE_COLS = ("support_ref", "surface_role", "u_mm", "v_mm",
                "normal_offset_mm")

# ⚠️ `unlocated` is a REAL value, not a missing one. SV-T exists and its
# position is unknown; recording it as a wall_face with blank fields would make
# "unknown" indistinguishable from "not filled in yet".
LOCATOR_KINDS = {
    "wall_face": (("host_ref", "face_ref"), SURFACE_COLS),
    "surface_local": (("support_ref", "surface_role"), WALL_COLS),
    "unlocated": ((), WALL_COLS + SURFACE_COLS),
}

PLACEMENT_STATES = {"asserted", "candidate", "partial", "unknown"}
POLARITY = {"affirm", "negate"}
BASES = {"observed", "derived", "assumed", "stated", "unknown"}
VALUE_STATES = {"asserted", "candidate", "disputed", "unknown", "retracted"}
VALUE_TYPES = {"bool", "int", "mm", "string", "enum", "range"}
PROPERTIES = {"existence", "count", "position_along", "vertical", "function",
              "voltage", "route_state", "gang", "arrangement",
              # ⚠️ THE TERMINAL ENVELOPE, and it lives HERE rather than as
              # occurrence columns so that each part carries its OWN basis and
              # state. An occurrence has an anchor POINT; a point cannot
              # collide with anything. Without these the extent check has
              # nothing to read, and the validator would have had to invent
              # default device dimensions internally - which is exactly how an
              # assumption becomes invisible.
              "extent_along_mm", "extent_vertical_mm", "anchor_mode",
              "host_interaction",
              # ⚠️ cast-in is not chasing, and the difference decides whether a
              # concrete host is legitimate at all.
              "installation_method"}

# Enum properties whose values are closed. An open string here would let
# `host_interaction` drift into meaninglessness.
ENUM_VALUES = {
    "anchor_mode": {"centre", "lower_centre", "upper_centre", "start", "end"},
    # ⚠️ `creates_penetration` is why a blanket "a service may not overlap a
    # void" rule is wrong: SV-VT IS a hole through G4b, and such a rule would
    # eventually reject the one element whose purpose is to be one.
    "host_interaction": {"avoid_void", "creates_penetration", "fills_opening"},
    "installation_method": {"cast_in", "chased", "surface_mounted"},
}

# ⚠️ SCOPE IS TYPED, NOT AN APARTMENT ENUMERATION. The first version allowed
# only `ours`/`53`/`109`/`2`, which cannot express the thing §3.0f explicitly
# permits as a route to established existence: a developer document governing
# this UNIT TYPE. That is not an apartment.
SCOPE_KINDS = {"apartment", "unit_type", "building"}
APARTMENTS = {"ours", "53", "109", "2"}


def load(directory=DRAFTS):
    rows = []
    for path in sorted(glob.glob(os.path.join(directory, "*.csv"))):
        with io.open(path, encoding="utf-8") as fh:
            for index, row in enumerate(csv.DictReader(fh), start=2):
                row["_table"] = os.path.basename(path)
                row["_line"] = index
                rows.append(row)
    return rows


def _typed(value, value_type):
    """Does `value` parse as `value_type`? Never a guess, never a coercion."""
    text = (value or "").strip()
    if not text:
        return False
    if value_type == "bool":
        return text in ("true", "false")
    if value_type == "int":
        return text.isdigit()
    if value_type == "mm":
        try:
            float(text)
        except ValueError:
            return False
        return True
    if value_type == "range":
        parts = text.replace("–", "-").split("-")
        return len(parts) == 2 and all(p.strip().isdigit() for p in parts)
    return True   # string / enum carry no parse obligation


def model_elements(path=MATERIALS):
    """Element ids an assertion may be ABOUT: walls, anchors, rooms, pseudo."""
    out = set(PSEUDO_ELEMENTS)
    try:
        with io.open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return set()
    for wall in data.get("walls", []):
        out.add(wall.get("id"))
    out.update(data.get("plumbing_anchors", {}).keys())
    anchors = os.path.join(os.path.dirname(path), "plumbing_anchors.csv")
    if os.path.exists(anchors):
        with io.open(anchors, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                out.add(row.get("anchor_id"))
    return out


def check(rows, elements=None):
    if elements is None:
        elements = model_elements()
    problems = []
    keys = {}
    for row in rows:
        where = "%s:%s" % (row.get("_table"), row.get("_line"))
        key = (row.get("migration_key") or "").strip()
        if not key:
            problems.append("%s has no migration_key" % where)
            continue
        if key in keys:
            problems.append(
                "migration_key %s appears twice (%s and %s) - it is the handle "
                "other records point at, so a collision silently merges two "
                "different things" % (key, keys[key], where))
        keys[key] = where

    known = set(keys)
    for row in rows:
        key = (row.get("migration_key") or "").strip() or "<no key>"
        table = row.get("_table")
        concept = (row.get("target_concept") or "").strip()

        if concept not in CONCEPTS:
            problems.append("%s declares concept %r, which is not one of the "
                            "declared concepts" % (key, concept))
            continue
        expected = TABLE_CONCEPT.get(table)
        if expected and concept != expected:
            problems.append(
                "%s is a %r in %s, which carries %r - the typed columns around "
                "it do not apply to it" % (key, concept, table, expected))

        # ⚠️ A NEW OWNER DECISION IS NOT A LEGACY SOURCE. The coverage gate
        # already accepts `new_decision_by` as an alternative to a locator, and
        # this must match it - otherwise a genuinely new decision gets a
        # borrowed locator stapled on purely to pass, which is exactly the
        # false provenance the review found on the rewire and cast-in rows.
        if not (row.get("source_locators") or "").strip() and not (
                row.get("new_decision_by") or "").strip():
            problems.append("%s cites no source_locators and is not marked as "
                            "a new decision with a stated author" % key)

        for column in REQUIRED.get(concept, ()):
            if not (row.get(column) or "").strip():
                problems.append("%s (%s) is missing required column %r"
                                % (key, concept, column))

        if concept == "occurrence":
            kind = (row.get("locator_kind") or "").strip()
            if kind not in LOCATOR_KINDS:
                # ⚠️ NEVER a skip. An unrecognised kind is a hard error.
                problems.append(
                    "%s has locator_kind %r, which is not a member of the "
                    "union - an unknown kind must FAIL, never be skipped"
                    % (key, kind))
            else:
                need, forbid = LOCATOR_KINDS[kind]
                for column in need:
                    if not (row.get(column) or "").strip():
                        problems.append("%s is %s but has no %r"
                                        % (key, kind, column))
                for column in forbid:
                    if (row.get(column) or "").strip():
                        problems.append(
                            "%s is %s but carries %r - that is two "
                            "incompatible placements in one row, and whichever "
                            "the generator reads first would win"
                            % (key, kind, column))
            state = (row.get("placement_state") or "").strip()
            if state and state not in PLACEMENT_STATES:
                problems.append("%s has placement_state %r" % (key, state))
            for column in ("parent_assembly_key",):
                ref = (row.get(column) or "").strip()
                if ref and ref not in known:
                    problems.append("%s.%s points at %r, which no record "
                                    "declares" % (key, column, ref))

        if concept == "assembly":
            members = [m.strip() for m in
                       (row.get("member_keys") or "").split(";") if m.strip()]
            for member in members:
                if member not in known:
                    problems.append("%s lists member %r, which no record "
                                    "declares" % (key, member))
            if key in members:
                problems.append(
                    "%s lists ITSELF as a member - an assembly is not one of "
                    "its own components" % key)

        if concept == "assertion":
            for column, allowed in (("property", PROPERTIES),
                                    ("polarity", POLARITY),
                                    ("knowledge_basis", BASES),
                                    ("value_state", VALUE_STATES),
                                    ("value_type", VALUE_TYPES)):
                value = (row.get(column) or "").strip()
                if value and value not in allowed:
                    problems.append("%s has %s %r, which is not declared"
                                    % (key, column, value))
            prop = (row.get("property") or "").strip()
            state = (row.get("value_state") or "").strip()
            allowed = ENUM_VALUES.get(prop)
            if allowed and (row.get("value") or "").strip() not in allowed:
                problems.append(
                    "%s asserts %s=%r, which is not one of %s"
                    % (key, prop, (row.get("value") or "").strip(),
                       "/".join(sorted(allowed))))
            vtype = (row.get("value_type") or "").strip()
            # ⚠️ AN EMPTY VALUE IS LEGITIMATE ONLY AS AN EXPLICIT UNKNOWN.
            # "extent is unknown" has to be a RECORD, because the validator
            # treats unknown extent as INCOMPLETE rather than valid - but an
            # empty value with any other state is a row nobody finished.
            if not (row.get("value") or "").strip():
                if state != "unknown":
                    problems.append(
                        "%s has no value but value_state is %r - an empty value "
                        "is only meaningful as an explicit `unknown`"
                        % (key, state))
            elif vtype in VALUE_TYPES and not _typed(row.get("value"), vtype):
                problems.append(
                    "%s declares value_type %r but its value %r does not parse "
                    "as one" % (key, vtype, (row.get("value") or "")[:40]))
            # ⚠️ EVERY PROPERTY ASSERTION NAMES ITS SUBJECT. 90 of 108 named
            # nothing, and an assertion about nothing cannot be checked,
            # contradicted or generated from. Exactly one of the two: a target
            # record, or a model element.
            subject = (row.get("subject_key") or "").strip()
            element = (row.get("subject_element") or "").strip()
            if subject and element:
                problems.append(
                    "%s names BOTH subject_key %r and subject_element %r - a "
                    "claim is about one thing" % (key, subject, element))
            elif not subject and not element:
                problems.append(
                    "%s names no subject. Every property assertion must say "
                    "what it is about - a target record (subject_key) or a "
                    "model element (subject_element)" % key)
            if element and elements and element not in elements:
                problems.append(
                    "%s is about element %r, which is neither a wall, a "
                    "plumbing anchor, a room nor a declared pseudo-element"
                    % (key, element))
            for column in ("subject_key", "disputed_with"):
                ref = (row.get(column) or "").strip()
                if ref and ref not in known:
                    problems.append("%s.%s points at %r, which no record "
                                    "declares" % (key, column, ref))
            # ⚠️ `observation_refs` carries the observations backing an
            # assertion. It is SEPARATE from source_locators, which must hold
            # LEDGER locators - the earlier laundering check looked for
            # observation keys inside source_locators, where they can never
            # legitimately appear.
            for ref in (row.get("observation_refs") or "").split(";"):
                ref = ref.strip()
                if ref and ref not in known:
                    problems.append("%s.observation_refs names %r, which no "
                                    "record declares" % (key, ref))

        if concept == "relation":
            kind = (row.get("relation_kind") or "").strip()
            if kind and kind not in RELATION_KINDS:
                problems.append("%s has relation_kind %r, which is not declared"
                                % (key, kind))
            target = (row.get("target_key") or "").strip()
            pending = (row.get("target_pending") or "").strip().lower()
            if target and target not in known:
                problems.append(
                    "%s points at target_key %r, which no record declares - an "
                    "alias that does not resolve preserves no identity"
                    % (key, target))
            if not target and pending != "yes":
                problems.append(
                    "%s has no target_key and is not marked target_pending - "
                    "an alias must either resolve or say why it cannot" % key)

        if concept == "route":
            state = (row.get("route_state") or "").strip()
            if state and state not in ROUTE_STATES:
                problems.append("%s has route_state %r, which is not declared"
                                % (key, state))
            basis = (row.get("knowledge_basis") or "").strip()
            if basis and basis not in BASES:
                problems.append("%s has knowledge_basis %r" % (key, basis))
            vstate = (row.get("value_state") or "").strip()
            if vstate and vstate not in VALUE_STATES:
                problems.append("%s has value_state %r" % (key, vstate))
            if state == "as_built" and basis != "observed":
                problems.append(
                    "%s claims route_state=as_built with knowledge_basis %r - "
                    "as_built is RECORDED FROM SITE and never derived"
                    % (key, basis))

        if concept in ("observation", "assertion"):
            kind = (row.get("scope_kind") or "").strip()
            ref = (row.get("scope_ref") or "").strip()
            if kind and kind not in SCOPE_KINDS:
                problems.append("%s has scope_kind %r, which is not declared"
                                % (key, kind))
            elif kind == "apartment" and ref and ref not in APARTMENTS:
                problems.append(
                    "%s is scoped to apartment %r, which nobody surveyed - an "
                    "apartment scope must name `ours` or a comparable actually "
                    "looked at" % (key, ref))

    # ⚠️ THE COMPARABLE-FLAT RULE, ENFORCED STRUCTURALLY (design §3.0f).
    # -----------------------------------------------------------------
    # An observation in another flat and a projection onto ours must stay
    # SEPARATE RECORDS. The violation is not writing a false row - it is an
    # `ours` assertion quietly claiming `observed` basis while every
    # observation behind it is of somebody else's flat.
    #
    # ⚠️ IT NOW READS `observation_refs`, NOT `source_locators`. The first
    # version searched for observation MIGRATION KEYS inside source_locators,
    # where they can never legitimately appear - that column holds LEDGER
    # locators. So it had NO VALID POSITIVE PATH: it rejected `ours + observed`
    # correctly today only because no observation of ours exists, and after a
    # real survey it still could not have expressed legitimate support.
    observed_scopes = {}
    for row in rows:
        if (row.get("target_concept") or "").strip() != "observation":
            continue
        observed_scopes[(row.get("migration_key") or "").strip()] = (
            (row.get("scope_kind") or "").strip(),
            (row.get("scope_ref") or "").strip())
    for row in rows:
        if (row.get("target_concept") or "").strip() != "assertion":
            continue
        key = (row.get("migration_key") or "").strip()
        if ((row.get("scope_kind") or "").strip() != "apartment"
                or (row.get("scope_ref") or "").strip() != "ours"
                or (row.get("knowledge_basis") or "").strip() != "observed"):
            continue
        refs = [r.strip() for r in
                (row.get("observation_refs") or "").split(";") if r.strip()]
        if not [r for r in refs
                if observed_scopes.get(r) == ("apartment", "ours")]:
            problems.append(
                "%s is scoped to OUR apartment with knowledge_basis=observed, "
                "but `observation_refs` names no observation scoped to ours - "
                "evidence from a comparable flat is an observation of THAT "
                "flat and a CANDIDATE, DERIVED projection onto this one "
                "(design 3.0f). Use knowledge_basis=derived with "
                "value_state=candidate, as a separate record." % key)

    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--drafts", default=DRAFTS)
    a = ap.parse_args()

    rows = load(a.drafts)
    problems = check(rows)
    for problem in problems:
        print("FAIL %s" % problem)
    print("%d target record(s) across %d table(s)"
          % (len(rows), len(set(r["_table"] for r in rows))))
    if problems:
        print("SCHEMA FAILED: %d problem(s)" % len(problems))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
