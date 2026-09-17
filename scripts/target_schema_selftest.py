#!/usr/bin/env python3
"""Guard the target-record schema gate by seeding the defects it exists to catch.

`00_Master/Validator_Design_Discipline.md`: a gate nobody has watched fail is
not a gate.

⚠️ THE SLICE IS THE FIXTURE. These seeds mutate the REAL vertical slice rather
than a synthetic table, because a fixture the real records cannot reach reads as
covered while covering nothing.

    .venv\\Scripts\\python.exe scripts/target_schema_selftest.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import os  # noqa: E402
sys.path.insert(0, str(REPO / "tools" / "services"))

from check_target_schema import check, load  # noqa: E402


def main() -> int:
    failures = 0
    rows = load()
    if not rows:
        print("FAIL no draft records to check")
        return 1

    def expect(label, problems, want_problem, needle=""):
        nonlocal failures
        hit = any(needle in p for p in problems) if needle else bool(problems)
        if hit == want_problem:
            print("PASS %-54s %s" % (label, (problems[0][:58] if problems
                                             else "no problems")))
        else:
            print("FAIL %-54s wanted problem=%s, got %d: %s"
                  % (label, want_problem, len(problems), problems[:1]))
            failures += 1

    def seed(key, **changes):
        """⚠️ RAISES on an unknown key. Two seeds silently mutated NOTHING
        after a record was renamed, so they asserted a defect was caught while
        testing an empty change - a seed that cannot fail is worse than no
        seed."""
        out, hit = [], 0
        for row in rows:
            copy = dict(row)
            if copy.get("migration_key") == key:
                copy.update(changes)
                hit += 1
            out.append(copy)
        if hit != 1:
            raise KeyError("seed target %r matched %d records" % (key, hit))
        return out

    def find(key):
        return next(r for r in rows if r["migration_key"] == key)

    # 1 - the real slice is well formed
    expect("the real slice passes", check(rows), False)

    # 2 - a duplicate key silently merges two records
    dupe = rows + [dict(find("OCC-SV-T"), migration_key="OCC-W6",
                        _table="occurrences.csv", _line=99)]
    expect("a duplicate migration_key is caught", check(dupe), True,
           "appears twice")

    # ⚠️ 3 - THE ONE THAT MATTERS MOST. A wall_face occurrence carrying ceiling
    # columns: two incompatible placements in one row.
    expect("wall_face carrying surface_local columns is caught",
           check(seed("OCC-SV-VT", support_ref="SLAB-1", u_mm="1200")), True,
           "two incompatible placements")

    # 4 - and the mirror: surface_local carrying wall columns
    expect("surface_local carrying wall columns is caught",
           check(seed("OCC-SV-VT", locator_kind="surface_local",
                      support_ref="SLAB-1", surface_role="finished_ceiling")),
           True, "two incompatible placements")

    # 5 - a well-formed surface_local is ACCEPTED BY THE SCHEMA. ⚠️ That is all
    # it means: the compiler publishes no support geometry, so nothing has been
    # validated against reality here. See the geometry gate.
    expect("a clean surface_local is accepted by the SCHEMA only",
           check(seed("OCC-SV-VT", locator_kind="surface_local",
                      host_ref="", face_ref="", support_ref="SLAB-1",
                      surface_role="finished_ceiling")), False)

    # ⚠️ 6 - an unknown locator kind must FAIL, never be skipped
    expect("an unknown locator_kind FAILS rather than skipping",
           check(seed("OCC-SV-T", locator_kind="ceiling_ish")), True,
           "must FAIL, never be skipped")

    # 7 - `unlocated` is a real value, and carrying a position contradicts it
    expect("unlocated carrying a host is caught",
           check(seed("OCC-SV-T", host_ref="G4b")), True,
           "two incompatible placements")

    # 8 - a reference to a record nobody declares
    expect("a dangling subject_key is caught",
           check(seed("ASR-W6-VERT", subject_key="OCC-NOWHERE")), True,
           "which no record declares")

    # 9 - an assembly listing itself
    expect("an assembly listing ITSELF as a member is caught",
           check(seed("ASM-SW-B", member_keys="OCC-SW-B-H;ASM-SW-B")), True,
           "not one of its own components")

    # 10 - a declared type its value cannot be
    expect("a value that does not parse as its type is caught",
           check(seed("ASR-W6-GANG", value="two")), True, "does not parse")

    # ⚠️ 11 - THE COMPARABLE-FLAT RULE, MADE ENFORCEABLE. A blank scope is
    # exactly how a comparable-flat observation would quietly become a fact
    # about this apartment.
    expect("an observation with no scope_ref is caught",
           check(seed("OBS-CORRIDOR-LIGHT-109", scope_ref="")), True,
           "missing required column")
    expect("a scope naming a flat nobody surveyed is caught",
           check(seed("ASR-EC-LIGHT-OURS", scope_ref="77")), True,
           "nobody surveyed")
    # ⚠️ THE LAUNDERING SEED. A projection quietly claiming observed basis for
    # our flat is how comparable-flat evidence becomes a field-verified fact.
    expect("an `ours` observed assertion with no `ours` observation is caught",
           check(seed("ASR-EC-LIGHT-OURS", knowledge_basis="observed")), True,
           "names no observation scoped to ours")
    # and the typed scope can express what the enumeration could not
    expect("a unit_type scope is accepted",
           check(seed("ASR-EC-LIGHT-OURS", scope_kind="unit_type",
                      scope_ref="3B/2+")), False)
    expect("an undeclared scope_kind is caught",
           check(seed("OBS-CORRIDOR-LIGHT-109", scope_kind="floor")), True,
           "not declared")

    # ⚠️ THE ENVELOPE SEEDS. Without these properties the extent check has
    # nothing to read and the validator would have to invent device sizes.
    expect("an unknown extent is legitimate as an explicit unknown",
           check(rows), False)
    expect("an empty value that is NOT an explicit unknown is caught",
           check(seed("ASR-W6-EXT-A", value_state="candidate")), True,
           "only meaningful as an explicit `unknown`")
    expect("an undeclared host_interaction is caught",
           check(seed("ASR-SV-VT-HOSTINT", value="ignore_void")), True,
           "which is not one of")
    expect("an undeclared anchor_mode is caught",
           check(seed("ASR-W6-ANCHOR", value="middle-ish")), True,
           "which is not one of")

    # 12 - a row in the wrong table
    expect("a concept in the wrong table is caught",
           check(seed("REL-V-2", target_concept="occurrence")), True,
           "do not apply to it")

    # 13 - an undeclared vocabulary value
    expect("an undeclared knowledge_basis is caught",
           check(seed("ASR-W6-VERT", knowledge_basis="probably")), True,
           "which is not declared")

    # 14 - a target with no provenance
    expect("a record citing no source is caught",
           check(seed("OCC-W6", source_locators="")), True,
           "cites no source_locators")

    # 15 - a required column blanked
    expect("a missing required column is caught",
           check(seed("OCC-W6", placement_state="")), True,
           "missing required column")

    # REVIEW ROUND: the rules added after the Codex review

    # EVERY ASSERTION NAMES ITS SUBJECT. 90 of 108 named nothing.
    expect("an assertion with no subject is caught",
           check(seed("ASR-W6-VERT", subject_key="", subject_element="")),
           True, "names no subject")
    expect("an assertion naming BOTH subjects is caught",
           check(seed("ASR-W6-VERT", subject_element="G7")), True,
           "about one thing")
    expect("a subject_element nothing declares is caught",
           check(seed("ASR-3-zero-outlets-on-mc", subject_element="G99")),
           True, "neither a wall")

    # AN ALIAS MUST RESOLVE, OR SAY WHY IT CANNOT.
    expect("an alias pointing at nothing is caught",
           check(seed("REL-V-1", target_key="OCC-NOWHERE")), True,
           "which no record declares")
    expect("an alias with neither target nor pending is caught",
           check(seed("REL-V-2", target_pending="")), True,
           "must either resolve or say why")

    # ROUTES HAD NO CONTRACT AT ALL.
    expect("a route missing a required field is caught",
           check(seed("RTE-SEWER", route_kind="")), True,
           "missing required column")
    expect("an undeclared route_state is caught",
           check(seed("RTE-SEWER", route_state="probably")), True,
           "not declared")
    expect("as_built claimed on a derived basis is caught",
           check(seed("RTE-SEWER", route_state="as_built")), True,
           "never derived")

    # THE LAUNDERING GATE NOW HAS A VALID POSITIVE PATH, which the previous
    # version did not: it searched for observation keys inside
    # `source_locators`, where they can never legitimately appear.
    ours_obs = dict(find("OBS-MC-EMPTY-109"), migration_key="OBS-OURS-SEED",
                    scope_ref="ours")
    rows_ok = seed("ASR-3-zero-outlets-on-mc", knowledge_basis="observed",
                   observation_refs="OBS-OURS-SEED") + [ours_obs]
    expect("an observation scoped to OURS legitimises `observed`",
           check(rows_ok), False)


    # THE nan FAMILY. `value_type=mm, value=nan` parsed, reached the geometry
    # gate and produced "VALID envelope nan-nan clear of every void". Every
    # comparison a nan touches is false, so it passes containment rather than
    # failing it.
    for bad in ("nan", "inf", "-inf", "NaN"):
        expect("a %s measurement is rejected" % bad,
               check(seed("ASR-W6-VERT", value=bad)), True,
               "does not parse")
    expect("a non-finite RANGE bound is rejected",
           check(seed("VAL-E-KL-SOC-K-HEIGHT", value="915-nan")), True,
           "does not parse")

    # VALUES ARE TYPED BY ENFORCEMENT, NOT BY THEIR HEADER.
    expect("a malformed range value is caught",
           check(seed("VAL-E-KL-SOC-K-HEIGHT", value="not-a-range")), True,
           "does not parse")
    expect("an undeclared knowledge_basis on a VALUE is caught",
           check(seed("VAL-E-KL-SOC-K-HEIGHT", knowledge_basis="probably")),
           True, "not declared")
    expect("an undeclared scope_kind on a VALUE is caught",
           check(seed("VAL-E-KL-SOC-K-HEIGHT", scope_kind="floor")), True,
           "not declared")
    # ...and the route/value positive path exists, which it did not when those
    # tables had no `observation_refs` column at all.
    ours_rte = dict(find("OBS-BATH-S-53"), migration_key="OBS-OURS-RTE",
                    scope_ref="ours")
    expect("an OURS observation legitimises an `observed` ROUTE",
           check(seed("RTE-BATH-S", knowledge_basis="observed",
                      scope_ref="ours",
                      observation_refs="OBS-OURS-RTE") + [ours_rte]), False)

    expect("an undeclared scope_kind on a ROUTE is caught",
           check(seed("RTE-SEWER", scope_kind="floor")), True, "not declared")

    # THE SUBJECT REGISTRY MUST FAIL, NOT SWITCH ITSELF OFF. With an empty
    # element set the membership check used to be skipped entirely.
    from check_target_schema import SubjectRegistryUnavailable, model_elements
    try:
        model_elements(os.path.join(REPO, "no", "such", "file.json"))
        print("FAIL %-54s a missing registry was tolerated" % "subject registry")
        failures += 1
    except SubjectRegistryUnavailable:
        print("PASS %-54s %s" % ("a missing subject registry FAILS the gate",
                                 "never silently disabled"))
    expect("an unknown element is caught even with an empty registry",
           check(seed("ASR-3-zero-outlets-on-mc", subject_element="G99"),
                 elements=set()), True, "neither a wall")


    # ROUND FOUR
    expect("an undeclared occurrence phase is caught",
           check(seed("OCC-W6", phase="future")), True, "declared vocabulary")
    expect("a blank scope_phase is caught",
           check(seed("ASR-W6-VERT", scope_phase="")), True,
           "may not be blank")
    expect("a reference of the WRONG CONCEPT is caught",
           check(seed("ASR-3-zero-outlets-on-mc",
                      observation_refs="OCC-W6")), True, "it must be")
    expect("an assertion that is its own subject is caught",
           check(seed("ASR-W6-VERT", subject_key="ASR-W6-VERT")), True,
           "points at ITSELF")
    expect("a REVERSED range is caught",
           check(seed("VAL-E-KL-SOC-K-HEIGHT", value="1105-915")), True,
           "does not parse")
    expect("a disputed value with no counterpart is caught",
           check(seed("ASR-2-two-outlets-on-g7", disputed_with="")), True,
           "names no counterpart")
    expect("a dispute pointing at an unrelated claim is caught",
           check(seed("ASR-2-two-outlets-on-g7",
                      disputed_with="ASR-W6-VERT")), True,
           "does not name it back")
    expect("a dispute over different device classes is caught",
           check(seed("ASR-2-two-outlets-on-g7", device_class="")), True,
           "differ on device_class")
    expect("`disputed_with` on a NON-disputed value is caught",
           check(seed("ASR-W6-VERT", disputed_with="ASR-W6-EXIST")), True,
           "only a disputed value has a counterpart")
    expect("a count with no device_class is caught",
           check(seed("ASR-6-two-vertical-dn110-stacks", device_class="")),
           True, "no device_class")
    expect("an unresolvable route endpoint is caught",
           check(seed("RTE-SEWER", to_ref="SS-K22")), True,
           "neither a target record")
    expect("the retired `routed` state is caught",
           check(seed("RTE-SEWER", route_state="routed")), True,
           "not declared")
    expect("the normative `design_intent` state is accepted",
           check(seed("RTE-SEWER", route_state="design_intent")), False)
    expect("`construction_approved` is accepted",
           check(seed("RTE-SEWER", route_state="construction_approved")), False)


    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
