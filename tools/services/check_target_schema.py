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
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRAFTS = os.path.join(REPO, "_Inbox", "migration", "draft")

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
    "observation": ("observed_what", "scope_apartment", "observed_via"),
    "assertion": ("property", "value_type", "polarity", "knowledge_basis",
                  "value_state", "scope_apartment"),
    "relation": ("relation_kind", "from_ref", "to_ref"),
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
              "voltage", "route_state", "gang", "arrangement"}
# `ours` or a comparable actually looked at. A blank is what the rule forbids.
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


def check(rows):
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

        if not (row.get("source_locators") or "").strip():
            problems.append("%s cites no source_locators" % key)

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
            vtype = (row.get("value_type") or "").strip()
            if vtype in VALUE_TYPES and not _typed(row.get("value"), vtype):
                problems.append(
                    "%s declares value_type %r but its value %r does not parse "
                    "as one" % (key, vtype, (row.get("value") or "")[:40]))
            for column in ("subject_key", "disputed_with"):
                ref = (row.get(column) or "").strip()
                if ref and ref not in known:
                    problems.append("%s.%s points at %r, which no record "
                                    "declares" % (key, column, ref))

        if concept in ("observation", "assertion"):
            scope = (row.get("scope_apartment") or "").strip()
            if scope and scope not in APARTMENTS:
                problems.append(
                    "%s has scope_apartment %r; it must name `ours` or the "
                    "comparable actually looked at - this column is what makes "
                    "the comparable-flat rule enforceable" % (key, scope))

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
