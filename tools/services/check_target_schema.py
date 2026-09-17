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
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib"))
from tabular import finite  # noqa: E402

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
    "value": ("quantity", "value", "value_type", "knowledge_basis",
              "value_state", "scope_kind", "scope_ref"),
}

RELATION_KINDS = {"alias_of", "duplicate_of", "member_of", "connects_to",
                  "supersedes", "contradicts"}

# ⚠️ THE NORMATIVE FOUR. This said `topology_only / routed / as_built`, which
# contradicted the approved design and collapsed the deliberately load-bearing
# distinction between INTENDED, APPROVED and INSTALLED.
ROUTE_STATES = {"topology_only", "design_intent", "construction_approved",
                "as_built"}

# ⚠️ `phase` is the design's OWN vocabulary, and the geometry gate was
# dispatching on `proposed`, which is not in it. A record could say
# `phase=new`, sit on concrete with installation_method=cast_in, and come back
# VALID - authorising exactly the retrofit into cured concrete the rule exists
# to forbid.
PHASES = {"existing", "demolished", "new"}

# Which concept each reference kind may point AT. A globally unique key proves
# uniqueness, not kind: `observation_refs=OCC-W6` passed, and an assertion was
# able to be its own subject.
REFERENCE_CONCEPTS = {
    "observation_refs": {"observation"},
    "parent_assembly_key": {"assembly"},
    "member_keys": {"occurrence", "assembly"},
    "disputed_with": {"assertion"},
    "subject_key": {"occurrence", "assembly", "route", "observation", "value"},
    "target_key": {"occurrence", "assembly", "route", "assertion"},
}

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
              # ⚠️ `appearance` is what something LOOKS like; `function` is
              # what it does. Conflating them is how "this socket looks
              # different" became "this socket is 380 V".
              "appearance",
              # ⚠️ and phase count is NOT voltage. 380 V and three-phase are
              # separately uncertain claims about the same supply.
              "supply_phases",
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
        # ⚠️ `finite()`, NOT `float()`. AGENTS.md says so, and this file called
        # float() anyway: `value_type=mm, value=nan` parsed, reached the
        # geometry gate, and produced "VALID envelope nan-nan clear of every
        # void". A nan does not give a wrong answer, it makes the comparison
        # itself meaningless - and which way it falls depends on whether the
        # test was written positively or negatively.
        return finite(text) is not None
    if value_type == "range":
        parts = text.replace("–", "-").split("-")
        if len(parts) != 2:
            return False
        lo, hi = (finite(p.strip()) for p in parts)
        # ⚠️ A RANGE IS ORDERED. `1105-915` parsed happily as two finite
        # numbers, and a reversed range is empty rather than merely odd -
        # nothing is ever inside it.
        return lo is not None and hi is not None and lo <= hi
    return True   # string / enum carry no parse obligation


class SubjectRegistryUnavailable(Exception):
    """The subject authority could not be read. See `model_elements`."""


def model_elements(path=MATERIALS):
    """Element ids an assertion may be ABOUT: walls, anchors, rooms, pseudo.

    ⚠️ RAISES when the authority cannot be read. It used to return an empty
    set, and the caller only checked membership when the set was NON-EMPTY -
    so a missing or malformed `wall_materials.json` silently DISABLED subject
    validation altogether. Failure to load a registry must fail the gate; a
    check that quietly stops checking is worse than no check.
    """
    out = set(PSEUDO_ELEMENTS)
    try:
        with io.open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise SubjectRegistryUnavailable(
            "cannot read the subject registry %s (%s) - subject validation "
            "must FAIL, never silently switch itself off" % (path, exc))
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
    # ⚠️ key -> CONCEPT. Uniqueness is not kind: `observation_refs=OCC-W6`
    # passed, and an assertion could be its own subject.
    concept_of = {}
    for row in rows:
        k = (row.get("migration_key") or "").strip()
        if k:
            concept_of[k] = (row.get("target_concept") or "").strip()

    def reference(owner, column, ref, allowed_owner=None):
        """Check one reference by KIND, not merely by existence."""
        if not ref:
            return
        if ref == owner:
            problems.append(
                "%s.%s points at ITSELF - a record cannot be its own %s"
                % (owner, column, column))
            return
        if ref not in known:
            problems.append("%s.%s points at %r, which no record declares"
                            % (owner, column, ref))
            return
        allowed = allowed_owner or REFERENCE_CONCEPTS.get(column)
        if allowed and concept_of.get(ref) not in allowed:
            problems.append(
                "%s.%s points at %s, which is a %r - it must be %s"
                % (owner, column, ref, concept_of.get(ref),
                   " or ".join(sorted(allowed))))
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
            phase = (row.get("phase") or "").strip()
            if phase not in PHASES:
                problems.append(
                    "%s has phase %r; the declared vocabulary is %s"
                    % (key, phase, "/".join(sorted(PHASES))))
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
            reference(key, "parent_assembly_key",
                      (row.get("parent_assembly_key") or "").strip())

        if concept == "assembly":
            members = [m.strip() for m in
                       (row.get("member_keys") or "").split(";") if m.strip()]
            for member in members:
                reference(key, "member_keys", member)
            if key in members:
                problems.append(
                    "%s lists ITSELF as a member - an assembly is not one of "
                    "its own components" % key)

        # ⚠️ TYPE AND VOCABULARY APPLY TO EVERY TYPED RECORD, not only
        # assertions. `values.csv` was "typed" in its header alone: a range
        # value of `not-a-range` and a knowledge_basis of `probably` both
        # passed, because these checks sat inside the assertion-only branch.
        if concept in ("assertion", "value"):
            for column, allowed in (("knowledge_basis", BASES),
                                    ("value_state", VALUE_STATES),
                                    ("value_type", VALUE_TYPES)):
                value = (row.get(column) or "").strip()
                if value and value not in allowed:
                    problems.append("%s has %s %r, which is not declared"
                                    % (key, column, value))
            vtype = (row.get("value_type") or "").strip()
            state = (row.get("value_state") or "").strip()
            if not (row.get("value") or "").strip():
                if state != "unknown":
                    problems.append(
                        "%s has no value but value_state is %r - an empty "
                        "value is only meaningful as an explicit `unknown`"
                        % (key, state))
            elif vtype in VALUE_TYPES and not _typed(row.get("value"), vtype):
                problems.append(
                    "%s declares value_type %r but its value %r does not parse "
                    "as one" % (key, vtype, (row.get("value") or "")[:40]))

        if concept == "assertion":
            for column, allowed in (("property", PROPERTIES),
                                    ("polarity", POLARITY)):
                value = (row.get(column) or "").strip()
                if value and value not in allowed:
                    problems.append("%s has %s %r, which is not declared"
                                    % (key, column, value))
            prop = (row.get("property") or "").strip()
            allowed = ENUM_VALUES.get(prop)
            if allowed and (row.get("value") or "").strip() not in allowed:
                problems.append(
                    "%s asserts %s=%r, which is not one of %s"
                    % (key, prop, (row.get("value") or "").strip(),
                       "/".join(sorted(allowed))))
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
            if element and element not in elements:
                problems.append(
                    "%s is about element %r, which is neither a wall, a "
                    "plumbing anchor, a room nor a declared pseudo-element"
                    % (key, element))
            for column in ("subject_key", "disputed_with"):
                reference(key, column, (row.get(column) or "").strip())
            # ⚠️ `observation_refs` carries the observations backing an
            # assertion. It is SEPARATE from source_locators, which must hold
            # LEDGER locators - the earlier laundering check looked for
            # observation keys inside source_locators, where they can never
            # legitimately appear.
            for ref in (row.get("observation_refs") or "").split(";"):
                reference(key, "observation_refs", ref.strip())

        if concept == "relation":
            kind = (row.get("relation_kind") or "").strip()
            if kind and kind not in RELATION_KINDS:
                problems.append("%s has relation_kind %r, which is not declared"
                                % (key, kind))
            target = (row.get("target_key") or "").strip()
            pending = (row.get("target_pending") or "").strip().lower()
            reference(key, "target_key", target)
            if not target and pending != "yes":
                problems.append(
                    "%s has no target_key and is not marked target_pending - "
                    "an alias must either resolve or say why it cannot" % key)

        if concept == "route":
            # ⚠️ ENDPOINTS MUST RESOLVE. Every route had at least one endpoint
            # that was neither a target key nor a model element, and changing
            # one to the typo `SS-K22` passed - so the topology was not
            # topology, it was two strings.
            for column in ("from_ref", "to_ref"):
                ref = (row.get(column) or "").strip()
                if not ref:
                    continue
                if ref.startswith("unresolved:"):
                    continue
                if ref not in known and ref not in elements:
                    problems.append(
                        "%s.%s is %r, which is neither a target record, a "
                        "model element, nor an explicit `unresolved:<reason>` "
                        "- a route between two unresolvable strings is not "
                        "topology" % (key, column, ref))
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

        if concept in ("assertion", "route", "value"):
            phase = (row.get("scope_phase") or "").strip()
            if phase not in PHASES:
                problems.append(
                    "%s has scope_phase %r; it may not be blank and the "
                    "declared vocabulary is %s"
                    % (key, phase, "/".join(sorted(PHASES))))

        if concept in ("observation", "assertion", "route", "value"):
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

    # ⚠️ A DISPUTE IS RECIPROCAL, OR IT IS NOT A DISPUTE.
    # -------------------------------------------------
    # This only checked that `disputed_with`, when supplied, named SOME
    # existing key. Against the live G7 dispute, deleting `disputed_with`
    # passed, pointing it at an unrelated assertion passed, and deleting
    # `device_class` passed - which removes the very fact that one count is
    # outlets and the other switches, i.e. what makes them contradict at all.
    assertions = dict((r.get("migration_key", "").strip(), r) for r in rows
                      if (r.get("target_concept") or "").strip() == "assertion")
    for key, row in assertions.items():
        state = (row.get("value_state") or "").strip()
        other_key = (row.get("disputed_with") or "").strip()
        if state != "disputed":
            if other_key:
                problems.append(
                    "%s is %r but names disputed_with %s - only a disputed "
                    "value has a counterpart" % (key, state, other_key))
            continue
        if not other_key:
            problems.append(
                "%s is `disputed` but names no counterpart. A dispute is "
                "between two claims; one alone is just uncertainty" % key)
            continue
        other = assertions.get(other_key)
        if other is None:
            continue          # the reference check has already said so
        if (other.get("disputed_with") or "").strip() != key:
            problems.append(
                "%s names %s as its dispute, but %s does not name it back - a "
                "one-sided dispute lets one side be quietly resolved"
                % (key, other_key, other_key))
        for column in ("subject_key", "subject_element", "property",
                       "device_class", "scope_kind", "scope_ref",
                       "scope_phase"):
            if (row.get(column) or "").strip() != (other.get(column) or "").strip():
                problems.append(
                    "%s and %s are recorded as disputing each other but differ "
                    "on %s (%r vs %r) - two claims about different things do "
                    "not contradict"
                    % (key, other_key, column, (row.get(column) or "").strip(),
                       (other.get(column) or "").strip()))
        if (row.get("value") or "").strip() == (other.get("value") or "").strip():
            problems.append(
                "%s and %s dispute each other but assert the SAME value %r"
                % (key, other_key, (row.get("value") or "").strip()))
    # ⚠️ A COUNT WITHOUT A DEVICE CLASS IS NOT A COUNT OF ANYTHING.
    for key, row in assertions.items():
        if (row.get("property") or "").strip() == "count" and not (
                row.get("device_class") or "").strip():
            problems.append(
                "%s is a `count` with no device_class - «G7 has 2» and «G7 has "
                "0» only contradict once you know one counts outlets and the "
                "other switches" % key)

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
    # ⚠️ EVERY SCOPED EVIDENTIARY CLAIM, not only assertions. A route scoped
    # to ours with knowledge_basis=observed launders comparable-flat topology
    # exactly as an assertion would - RTE-BATH-S did.
    for row in rows:
        if (row.get("target_concept") or "").strip() not in (
                "assertion", "route", "value"):
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
