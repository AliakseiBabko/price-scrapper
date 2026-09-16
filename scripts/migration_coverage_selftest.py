#!/usr/bin/env python3
"""Guard the migration coverage gate by seeding the losses it exists to catch.

`00_Master/Validator_Design_Discipline.md`: a gate nobody has watched fail is
not a gate. The two seeds the reviewer named specifically are the first two
here, because both are silent in every other check:

  * an OMITTED owner statement - a decision recorded only as a Russian comment
    in drawing code, which no schema validator would miss because it was never
    a field;
  * a PARTIALLY SPLIT grouped observation - "count 3" becoming two occurrences,
    where both numbers are individually plausible.

    .venv\\Scripts\\python.exe scripts/migration_coverage_selftest.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools" / "services"))

from check_migration_coverage import check, load_ledger  # noqa: E402

LEDGER = REPO / "_Inbox" / "migration" / "services_migration_ledger.csv"


def main() -> int:
    failures = 0
    rows = load_ledger(LEDGER)
    if not rows:
        print("FAIL no ledger; run tools/services/build_migration_ledger.py")
        return 1

    def expect(label, problems, want_problem, needle=""):
        nonlocal failures
        hit = any(needle in p for p in problems) if needle else bool(problems)
        if hit == want_problem:
            detail = (problems[0][:78] if problems else "no problems")
            print("PASS %-44s %s" % (label, detail))
        else:
            print("FAIL %-44s wanted problem=%s, got %d: %s"
                  % (label, want_problem, len(problems), problems[:1]))
            failures += 1

    # A fully classified ledger is the baseline every seed is measured against.
    clean = []
    for row in rows:
        row = dict(row)
        row["disposition"] = "migrated"
        clean.append(row)

    problems, _ = check(clean, require_complete=True)
    expect("a fully classified ledger passes", problems, False)

    # 1 - an owner statement left unclassified
    seeded = [dict(r) for r in clean]
    owner = next(r for r in seeded
                 if r["source_kind"] == "comment_block")
    owner["disposition"] = "unresolved"
    problems, _ = check(seeded, require_complete=True)
    expect("an omitted owner comment block is caught", problems, True, "unresolved")

    # 2 - a source of EXACT multiplicity split into the wrong number
    seeded = [dict(r) for r in clean]
    exact = next(r for r in seeded if r["multiplicity"] == "exact_n"
                 and r["count_max"] == "3")
    exact["occurrence_split_count"] = "3"
    facts = [{"identity_uuid": "u%d" % i, "target_concept": "occurrence",
              "source_locators": exact["locator"]} for i in range(2)]
    problems, _ = check(seeded, new_facts=facts, require_complete=True)
    expect("a partially split exact-count source is caught",
           problems, True, "splits into 3")

    # 3 - ONE-TO-MANY ACROSS CONCEPTS MUST PASS. The same source legitimately
    # produces an observation, three occurrences, value records and an approval;
    # an earlier gate counted all of them against "3" and would have rejected
    # the schema's own intended mapping.
    seeded = [dict(r) for r in clean]
    exact = next(r for r in seeded if r["multiplicity"] == "exact_n"
                 and r["count_max"] == "3")
    exact["occurrence_split_count"] = "3"
    facts = ([{"identity_uuid": "o%d" % i, "target_concept": "occurrence",
               "source_locators": exact["locator"]} for i in range(3)]
             + [{"identity_uuid": "obs", "target_concept": "observation",
                 "source_locators": exact["locator"]},
                {"identity_uuid": "v1", "target_concept": "value",
                 "source_locators": exact["locator"]},
                {"identity_uuid": "v2", "target_concept": "value",
                 "source_locators": exact["locator"]},
                {"identity_uuid": "a1", "target_concept": "approval",
                 "source_locators": exact["locator"]}])
    problems, _ = check(seeded, new_facts=facts, require_complete=True)
    expect("one-to-many across concepts is allowed", problems, False)

    # 4 - splitting an exact source with no decision recorded
    seeded = [dict(r) for r in clean]
    exact = next(r for r in seeded if r["multiplicity"] == "exact_n")
    facts = [{"identity_uuid": "u1", "target_concept": "occurrence",
              "source_locators": exact["locator"]},
             {"identity_uuid": "u2", "target_concept": "occurrence",
              "source_locators": exact["locator"]}]
    problems, _ = check(seeded, new_facts=facts, require_complete=True)
    expect("splitting with no decision recorded is caught",
           problems, True, "has to be explicit")

    # 5 - ⚠️ an UNCERTAIN multiplicity resolved to a number by the migration
    seeded = [dict(r) for r in clean]
    rng = next(r for r in seeded if r["multiplicity"] == "range")
    facts = [{"identity_uuid": "u%d" % i, "target_concept": "occurrence",
              "source_locators": rng["locator"]} for i in range(2)]
    problems, _ = check(seeded, new_facts=facts, require_complete=True)
    expect("a 2-3 range silently resolved is caught", problems, True,
           "UNCERTAIN multiplicity")

    # 6 - an ASSEMBLY PARENT must not count as one of its components
    seeded = [dict(r) for r in clean]
    exact = next(r for r in seeded if r["multiplicity"] == "exact_n"
                 and r["count_max"] == "3")
    exact["occurrence_split_count"] = "3"
    facts = ([{"identity_uuid": "o%d" % i, "target_concept": "occurrence",
               "source_locators": exact["locator"]} for i in range(3)]
             + [{"identity_uuid": "asm", "target_concept": "assembly",
                 "source_locators": exact["locator"]}])
    problems, _ = check(seeded, new_facts=facts, require_complete=True)
    expect("an assembly parent is not counted as a component",
           problems, False)

    # 7 - a concept outside the model
    problems, _ = check(clean, new_facts=[{"identity_uuid": "x",
                                           "target_concept": "widget",
                                           "source_locators": clean[0]["locator"]}],
                        require_complete=True)
    expect("an unknown target concept is caught", problems, True,
           "not one of")

    # 8 - a new fact with no provenance at all
    problems, _ = check(clean, new_facts=[{"identity_uuid": "orphan"}],
                        require_complete=True)
    expect("an untraceable new fact is caught", problems, True, "cites no source")

    # 9 - a new fact citing a locator that does not exist
    problems, _ = check(clean, new_facts=[{"identity_uuid": "ghost",
                                           "source_locators": "nowhere.csv:1#X"}],
                        require_complete=True)
    expect("a citation to a missing locator is caught", problems, True,
           "does not carry")

    # 10 - `contradicted` without naming what overrides it
    seeded = [dict(r) for r in clean]
    seeded[0]["disposition"] = "contradicted"
    seeded[0]["disposition_note"] = ""
    problems, _ = check(seeded, require_complete=True)
    expect("`contradicted` with no override named is caught", problems, True,
           "does not name what overrides")

    # 11 - the REAL ledger today, which must still be incomplete
    problems, summary = check(rows, require_complete=True)
    expect("the real ledger is still unclassified", problems, True, "unresolved")
    print("     (%d locators, %d unresolved, %d exact_n, %d range)"
          % (summary["locators"], summary["unresolved"],
             summary["exact_n"], summary["range"]))

    print()
    print("failures: %d" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
