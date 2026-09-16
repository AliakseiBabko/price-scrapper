#!/usr/bin/env python3
"""Guard the migration coverage gate by seeding the losses it exists to catch.

`00_Master/Validator_Design_Discipline.md`: a gate nobody has watched fail is
not a gate.

⚠️ THE FIRST SEED IS THE ONE THAT EXPOSED THE OLD GATE. Its previous baseline
marked every locator `migrated`, supplied ZERO target records and expected a
PASS - so `migrated` meant only "somebody typed the word", and the migration
could have been declared complete having produced no data at all. That exact
arrangement must now FAIL.
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
            print("PASS %-48s %s" % (label, (problems[0][:72] if problems
                                             else "no problems")))
        else:
            print("FAIL %-48s wanted problem=%s, got %d: %s"
                  % (label, want_problem, len(problems), problems[:1]))
            failures += 1

    accepted = [dict(r, adjudication="accepted") for r in rows]

    def target(key, locator, concept="observation"):
        return {"migration_key": key, "source_locators": locator,
                "target_concept": concept}

    # ⚠️ 1 - THE DECISIVE SEED. Everything adjudicated, nothing produced.
    problems, _ = check(accepted, target_records=[], require_complete=True)
    expect("all adjudicated with ZERO targets must FAIL", problems, True,
           "NOT CITED by any target record")

    # 2 - the same ledger, now actually carried forward
    covered = [target("k%d" % i, r["locator"]) for i, r in enumerate(accepted)]
    problems, _ = check(accepted, target_records=covered, require_complete=True)
    expect("adjudicated AND carried forward passes", problems, False)

    # 3 - a contradicted claim dropped instead of kept as history
    seeded = [dict(r) for r in accepted]
    seeded[0]["adjudication"] = "contradicted"
    seeded[0]["adjudication_note"] = "superseded by the 2026-09-07 owner statement"
    partial = [t for t in covered if t["source_locators"] != seeded[0]["locator"]]
    problems, _ = check(seeded, target_records=partial, require_complete=True)
    expect("a dropped contradicted claim is caught", problems, True, "NOT CITED")

    # 4 - out_of_scope legitimately needs no target
    seeded = [dict(r) for r in accepted]
    seeded[0]["adjudication"] = "out_of_scope"
    partial = [t for t in covered if t["source_locators"] != seeded[0]["locator"]]
    problems, _ = check(seeded, target_records=partial, require_complete=True)
    expect("out_of_scope needs no target", problems, False)

    # 5 - an exact source split into the wrong number of occurrences
    seeded = [dict(r) for r in accepted]
    exact = next(r for r in seeded if r["multiplicity"] == "exact_n"
                 and r["count_max"] == "3")
    exact["occurrence_split_count"] = "3"
    extra = covered + [target("o%d" % i, exact["locator"], "occurrence")
                       for i in range(2)]
    problems, _ = check(seeded, target_records=extra, require_complete=True)
    expect("a partially split exact source is caught", problems, True,
           "splits into 3")

    # 6 - one-to-many across concepts, with an assembly parent, must PASS
    seeded = [dict(r) for r in accepted]
    exact = next(r for r in seeded if r["multiplicity"] == "exact_n"
                 and r["count_max"] == "3")
    exact["occurrence_split_count"] = "3"
    extra = covered + (
        [target("o%d" % i, exact["locator"], "occurrence") for i in range(3)]
        + [target("asm", exact["locator"], "assembly"),
           target("v1", exact["locator"], "value"),
           target("ap1", exact["locator"], "approval")])
    problems, _ = check(seeded, target_records=extra, require_complete=True)
    expect("one-to-many plus an assembly parent passes", problems, False)

    # 7 - ⚠️ an uncertain range resolved to a number by the migration
    seeded = [dict(r) for r in accepted]
    rng = next(r for r in seeded if r["multiplicity"] == "range")
    extra = covered + [target("r%d" % i, rng["locator"], "occurrence")
                       for i in range(2)]
    problems, _ = check(seeded, target_records=extra, require_complete=True)
    expect("a 2-3 range silently resolved is caught", problems, True,
           "UNCERTAIN multiplicity")

    # 8 - a target record with no concept
    problems, _ = check(accepted,
                        target_records=covered + [{"migration_key": "x",
                                                   "source_locators": rows[0]["locator"]}],
                        require_complete=True)
    expect("a target with no concept is caught", problems, True, "declares no concept")

    # 9 - a target citing a locator that does not exist
    problems, _ = check(accepted,
                        target_records=covered + [target("ghost", "nowhere.csv:1#X")],
                        require_complete=True)
    expect("a citation to a missing locator is caught", problems, True,
           "does not carry")

    # 10 - a target with no provenance at all
    problems, _ = check(accepted,
                        target_records=covered + [{"migration_key": "orphan",
                                                   "target_concept": "observation"}],
                        require_complete=True)
    expect("an untraceable target is caught", problems, True, "cites no source")

    # 11 - `contradicted` without naming what overrides it
    seeded = [dict(r) for r in accepted]
    seeded[0]["adjudication"] = "contradicted"
    seeded[0]["adjudication_note"] = ""
    problems, _ = check(seeded, target_records=covered, require_complete=True)
    expect("`contradicted` with no override named is caught", problems, True,
           "does not name what overrides")

    # 12 - the REAL ledger today
    problems, summary = check(rows, require_complete=True)
    expect("the real ledger is still unadjudicated", problems, True, "unresolved")
    print("     (%d locators, %d unresolved, %d in scope, %d targets)"
          % (summary["locators"], summary["unresolved"],
             summary["in_scope"], summary["targets"]))

    print()
    print("failures: %d" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
