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
                 if r["source_kind"] == "owner_statement_in_comment")
    owner["disposition"] = "unresolved"
    problems, _ = check(seeded, require_complete=True)
    expect("an omitted owner statement is caught", problems, True, "unresolved")

    # 2 - a grouped observation split into the wrong number
    seeded = [dict(r) for r in clean]
    grouped = next(r for r in seeded if r["grouped"] == "yes"
                   and "count=3" in (r["carries"] or ""))
    grouped["split_into"] = "3"
    facts = [{"identity_uuid": "u%d" % i,
              "source_locators": grouped["locator"]} for i in range(2)]
    problems, _ = check(seeded, new_facts=facts, require_complete=True)
    expect("a partially split grouped observation is caught",
           problems, True, "splits into 3")

    # 3 - the same split with no grouping decision recorded at all
    seeded = [dict(r) for r in clean]
    grouped = next(r for r in seeded if r["grouped"] == "yes")
    facts = [{"identity_uuid": "u1", "source_locators": grouped["locator"]},
             {"identity_uuid": "u2", "source_locators": grouped["locator"]}]
    problems, _ = check(seeded, new_facts=facts, require_complete=True)
    expect("splitting with no grouping decision is caught",
           problems, True, "has to be explicit")

    # 4 - a new fact with no provenance at all
    problems, _ = check(clean, new_facts=[{"identity_uuid": "orphan"}],
                        require_complete=True)
    expect("an untraceable new fact is caught", problems, True, "cites no source")

    # 5 - a new fact citing a locator that does not exist
    problems, _ = check(clean, new_facts=[{"identity_uuid": "ghost",
                                           "source_locators": "nowhere.csv:1#X"}],
                        require_complete=True)
    expect("a citation to a missing locator is caught", problems, True,
           "does not carry")

    # 6 - `contradicted` without naming what overrides it
    seeded = [dict(r) for r in clean]
    seeded[0]["disposition"] = "contradicted"
    seeded[0]["disposition_note"] = ""
    problems, _ = check(seeded, require_complete=True)
    expect("`contradicted` with no override named is caught", problems, True,
           "does not name what overrides")

    # 7 - the REAL ledger today, which must still be incomplete
    problems, summary = check(rows, require_complete=True)
    expect("the real ledger is still unclassified", problems, True, "unresolved")
    print("     (%d locators, %d unresolved, %d grouped)"
          % (summary["locators"], summary["unresolved"], summary["grouped"]))

    print()
    print("failures: %d" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
