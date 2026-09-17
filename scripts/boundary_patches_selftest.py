#!/usr/bin/env python3
"""Seed every way the boundary records could quietly stop meaning anything.

⚠️⚠️ THE FAILURE CLASS THIS WHOLE SCHEMA REPLACES is a geometric flood that
read "absent from our model" as "outside". It was wrong twice - MC's east end
and M2's abutting run - and both times a human patched the OUTPUT rather than
the rule. So the seeds here are aimed at the ways the new records could acquire
the same false confidence: a face nobody covered, a gap nothing notices, a
candidate value driving a generator, an identity that moves when a patch
splits, and a status that belongs to a row instead of to a value.

⚠️ `check()` takes its rows INJECTED, so every seed mutates real structures
rather than a fixture that cannot represent the defect.

    .venv-ifc314\\Scripts\\python.exe scripts/boundary_patches_selftest.py
"""
from __future__ import annotations

import copy
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))

from check_boundary_patches import (  # noqa: E402
    NOT_REQUIRED, REQUIRED, UNRESOLVED, check, eligibility, load_assertions,
    load_decisions, load_inventory, load_patches)


def main() -> int:
    failures = 0
    base_inv = load_inventory()
    base_pat = load_patches()
    base_ass = load_assertions()
    base_dec = load_decisions()

    def expect(label, problems, want, needle=""):
        nonlocal failures
        hit = any(needle in p for p in problems) if needle else bool(problems)
        if hit == want:
            print("PASS %-58s %s" % (label, (problems[0][:26] if problems
                                             else "no problems")))
        else:
            print("FAIL %-58s wanted %s, got %d: %s"
                  % (label, want, len(problems), problems[:1]))
            failures += 1

    MISSING = object()

    def run(inv=MISSING, pat=MISSING, ass=MISSING, dec=MISSING):
        # ⚠ A SENTINEL, not `or`. The first version used `dec or base_dec`,
        # so the seed that passes an EMPTY decision table silently got the real
        # one back and tested nothing - a seed that cannot fail is worse than
        # no seed, and this one proved it by passing while broken.
        return check(copy.deepcopy(base_inv if inv is MISSING else inv),
                     copy.deepcopy(base_pat if pat is MISSING else pat),
                     copy.deepcopy(base_ass if ass is MISSING else ass),
                     copy.deepcopy(base_dec if dec is MISSING else dec))

    expect("the real records pass", run(), False)

    # ⚠️ and it must be non-trivial - a check over nothing passes
    expect("there is something to check",
           [] if len(base_pat) >= 5 and len(base_ass) >= 20 else ["too few"],
           False)

    def patches(mutate):
        rows = copy.deepcopy(base_pat)
        mutate(rows)
        return rows

    # ── coverage ─────────────────────────────────────────────────────────────
    def m2(rows):
        return [r for r in rows if r["host_id"] == "M2"]

    expect("a GAP in a face's cover is caught",
           run(pat=patches(lambda rows: m2(rows)[0].__setitem__(
               "along_to_mm", "400.0"))), True, "has a GAP")

    expect("an OVERLAP is caught",
           run(pat=patches(lambda rows: m2(rows)[0].__setitem__(
               "along_to_mm", "900.0"))), True, "OVERLAPPING")

    expect("a face left SHORT at its far end is caught",
           run(pat=patches(lambda rows: m2(rows)[1].__setitem__(
               "along_to_mm", "1500.0"))), True, "is uncovered from")

    expect("an ENVELOPE face with no patch at all is caught",
           run(pat=[r for r in base_pat if r["host_id"] != "MA"]),
           True, "no patch covers it")

    expect("a patch on a face the compiler does not resolve is caught",
           run(pat=patches(lambda rows: rows[0].__setitem__(
               "face_ref", "cross_nonexistent"))),
           True, "does not resolve as a face")

    # ── malformed geometry ───────────────────────────────────────────────────
    for label, value, needle in (
            ("a nan bound is caught", "nan", "non-finite"),
            ("an inf bound is caught", "inf", "non-finite")):
        expect(label, run(pat=patches(
            lambda rows, v=value: rows[0].__setitem__("along_to_mm", v))),
            True, needle)

    expect("a REVERSED patch is caught",
           run(pat=patches(lambda rows: rows[0].update(
               {"along_from_mm": "900.0", "along_to_mm": "100.0"}))),
           True, "empty or reversed")

    expect("a patch running past the end of its face is caught",
           run(pat=patches(lambda rows: m2(rows)[1].__setitem__(
               "along_to_mm", "9999.0"))), True, "on a face")

    # ⚠️ EACH BOUND'S OWN BASIS - the point of splitting them at all
    expect("a bound with no declared basis is caught",
           run(pat=patches(lambda rows: rows[0].__setitem__(
               "along_from_basis", ""))), True, "EACH BOUND carries its own")

    # ── vertical applicability, EXPLICIT ─────────────────────────────────────
    expect("an unstated vertical applicability is caught",
           run(pat=patches(lambda rows: rows[0].__setitem__("vertical", ""))),
           True, "EXPLICITLY")

    expect("an interval claimed without real bounds is caught",
           run(pat=patches(lambda rows: rows[0].__setitem__(
               "vertical", "interval"))), True, "must be real when it is claimed")

    # ── identity ─────────────────────────────────────────────────────────────
    expect("an identity that is not a minted UUID is caught",
           run(pat=patches(lambda rows: rows[0].__setitem__(
               "patch_uuid", "M2_cross_lo_0_570"))),
           True, "never derived from a host id")

    expect("a duplicate patch identity is caught",
           run(pat=patches(lambda rows: rows[1].__setitem__(
               "patch_uuid", rows[0]["patch_uuid"]))), True, "appears twice")

    # ⚠️⚠️ A SPLIT MUST NOT MOVE THE OLD IDENTITY ONTO ONE CHILD.
    def one_successor(rows):
        rows[0]["state"] = "retired"
        rows[0]["successors"] = rows[1]["patch_uuid"]
    expect("a split that keeps the old identity on one child is caught",
           run(pat=patches(one_successor)), True, "must not land on one child")

    def dangling(rows):
        rows[0]["state"] = "retired"
        rows[0]["successors"] = "ffffffff-ffff-4fff-8fff-ffffffffffff;" + rows[1]["patch_uuid"]
    expect("a successor that does not exist is caught",
           run(pat=patches(dangling)), True, "which does not exist")

    # ── epistemics, PER ASSERTION ────────────────────────────────────────────
    def assertions(mutate):
        rows = copy.deepcopy(base_ass)
        mutate(rows)
        return rows

    expect("a missing required axis is caught",
           run(ass=[r for r in base_ass if r["property"] != "contact_kind"]),
           True, "asserts nothing about")

    expect("a value outside its vocabulary is caught",
           run(ass=assertions(lambda rows: rows[0].__setitem__(
               "value", "outside"))), True, "not one of")

    expect("a value_state outside its vocabulary is caught",
           run(ass=assertions(lambda rows: rows[0].__setitem__(
               "value_state", "probably"))), True, "value_state")

    expect("an assertion with no knowledge_basis is caught",
           run(ass=assertions(lambda rows: rows[0].__setitem__(
               "knowledge_basis", ""))), True, "belong to each asserted VALUE")

    expect("a confident assertion nobody can trace is caught",
           run(ass=assertions(lambda rows: rows[0].update(
               {"evidence": "", "raw_text": ""}))), True, "worse than `unknown`")

    # ⚠️ NOT KNOWING SOMETHING IS NOT AN ASSERTION ABOUT IT
    expect("`unknown` dressed as an assertion is caught",
           run(ass=assertions(lambda rows: rows[0].update(
               {"value": "unknown", "value_state": "asserted"}))),
           True, "not an assertion about it")

    expect("an assertion on a patch that does not exist is caught",
           run(ass=assertions(lambda rows: rows[0].__setitem__(
               "patch_uuid", "ffffffff-ffff-4fff-8fff-ffffffffffff"))),
           True, "which does not exist")

    # ⚠️⚠️ DUPLICATE ROWS. Every keyed lookup in the checker was built straight
    # from the rows, so a duplicate silently overwrote its twin and NOTHING
    # reported it - a second contact_kind assertion turned an eligible patch
    # unresolved with zero problems. Three tables, three seeds.
    expect("a duplicate INVENTORY row is caught",
           run(inv=base_inv + [copy.deepcopy(base_inv[0])]),
           True, "DUPLICATE row")
    expect("a duplicate ASSERTION is caught",
           run(ass=base_ass + [copy.deepcopy(base_ass[0])]),
           True, "DUPLICATE row")
    expect("a duplicate decision rule_id is caught",
           run(dec=base_dec + [copy.deepcopy(base_dec[0])]),
           True, "DUPLICATE row")

    # ⚠️⚠️ AND A DUPLICATE MUST NOT BE RESOLVED PAST even by a caller that
    # skipped validation - otherwise file order decides the answer.
    dupe_ass = copy.deepcopy(base_ass)
    target = next(r for r in dupe_ass
                  if r["property"] == "contact_kind")
    twin = copy.deepcopy(target)
    twin["value_state"] = "candidate"
    got = eligibility(target["patch_uuid"], dupe_ass + [twin], base_dec)[0]
    ok = got == UNRESOLVED
    print("%s a duplicated assertion resolves to UNRESOLVED, not to the last row"
          % ("PASS" if ok else "FAIL"))
    failures += 0 if ok else 1

    # ⚠️⚠️ CONFLICTING DECISION RULES. Matching the FIRST rule that fitted made
    # the verdict depend on CSV row order: an opposite rule inserted above
    # INS-EXT-OPEN flipped M2 from insulated to not, silently.
    opposite = dict(copy.deepcopy(base_dec[0]),
                    rule_id="SEED-OPPOSITE", insulation_required="no")
    expect("overlapping rules with opposite verdicts are caught",
           run(dec=[opposite] + base_dec), True, "OVERLAP with opposite")

    conflicted = base_pat[0]["patch_uuid"]
    first = eligibility(conflicted, base_ass, [opposite] + base_dec)[0]
    last = eligibility(conflicted, base_ass, base_dec + [opposite])[0]
    ok = first == UNRESOLVED and last == UNRESOLVED
    print("%s conflicting rules give UNRESOLVED either way round (%s / %s)"
          % ("PASS" if ok else "FAIL", first, last))
    failures += 0 if ok else 1

    # ── eligibility ──────────────────────────────────────────────────────────
    expect("an empty decision table is caught", run(dec=[]), True, "EMPTY")
    expect("a decision rule with no verdict is caught",
           run(dec=[dict(base_dec[0], insulation_required="maybe")]),
           True, "must be yes or no")

    # ⚠️⚠️ THE GUARD THAT MATTERS MOST: a merely CANDIDATE or UNKNOWN value may
    # never drive generation. This is what stops the schema acquiring the false
    # authority the flood heuristic had.
    def verdict_for(pid, ass):
        return eligibility(pid, ass, base_dec)[0]

    insulating = None
    for row in base_pat:
        if verdict_for(row["patch_uuid"], base_ass) == REQUIRED:
            insulating = row["patch_uuid"]
            break
    if insulating is None:
        print("FAIL %-58s no patch is eligible, so the guard is vacuous"
              % "an eligible patch exists to downgrade")
        failures += 1
    else:
        for state in ("candidate", "disputed"):
            downgraded = copy.deepcopy(base_ass)
            for row in downgraded:
                if row["patch_uuid"] == insulating and row["property"] == "contact_kind":
                    row["value_state"] = state
            got = verdict_for(insulating, downgraded)
            ok = got == UNRESOLVED
            print("%s a %-9s value does not drive generation%s"
                  % ("PASS" if ok else "FAIL", state, "" if ok else " -> %r" % got))
            failures += 0 if ok else 1

        unknowned = copy.deepcopy(base_ass)
        for row in unknowned:
            if row["patch_uuid"] == insulating and row["property"] == "contact_kind":
                row["value"], row["value_state"] = "unknown", "unknown"
        got = verdict_for(insulating, unknowned)
        ok = got == UNRESOLVED
        print("%s an `unknown` value does not drive generation%s"
              % ("PASS" if ok else "FAIL", "" if ok else " -> %r" % got))
        failures += 0 if ok else 1

    # ⚠️ AND THE TWO EXCEPTIONS THIS SCHEMA EXISTS TO RETIRE must come out
    # RIGHT, or it has replaced two honest hand-patches with an automated
    # wrong answer.
    def verdict_at(host, face, lo):
        for row in base_pat:
            if (row["host_id"] == host and row["face_ref"] == face
                    and abs(float(row["along_from_mm"]) - lo) < 0.5):
                return eligibility(row["patch_uuid"], base_ass, base_dec)
        return ("no such patch", None, "")

    got, rule, _why = verdict_at("MC", "end_to", 0.0)
    ok = got == NOT_REQUIRED and rule == "INS-PARTY-MASONRY"
    print("%s MC's end cap is DERIVED off, not hand-suppressed  (%s)"
          % ("PASS" if ok else "FAIL", rule))
    failures += 0 if ok else 1

    got, rule, _why = verdict_at("M2", "cross_lo", 0.0)
    ok = got == REQUIRED and rule == "INS-EXT-OPEN"
    print("%s M2's exposed 570 mm is DERIVED insulated             (%s)"
          % ("PASS" if ok else "FAIL", rule))
    failures += 0 if ok else 1

    got, _rule, why = verdict_at("M2", "cross_lo", 570.0)
    ok = got == UNRESOLVED and "candidate" in why
    print("%s M2's abutting run is NOT eligible while contact is candidate"
          % ("PASS" if ok else "FAIL"))
    failures += 0 if ok else 1

    # ⚠️⚠️ THE THREE OUTCOMES ARE DISTINCT. `None` used to mean both "proven
    # no" and "nobody knows", and a generator reading them as one falsy value
    # would turn uncertainty into a silent omission that looks like a decision.
    mc = verdict_at("MC", "end_to", 0.0)[0]
    m2b = verdict_at("M2", "cross_lo", 570.0)[0]
    ok = mc == NOT_REQUIRED and m2b == UNRESOLVED and mc != m2b
    print("%s a PROVEN `no` and an UNRESOLVED are different values (%s vs %s)"
          % ("PASS" if ok else "FAIL", mc, m2b))
    failures += 0 if ok else 1

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
