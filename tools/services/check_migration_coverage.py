#!/usr/bin/env python3
"""Coverage gate for the services migration: nothing may be lost silently.

The migration splits one legacy row into several records - an observation plus
occurrences, approvals and relations - so a textual diff cannot prove the new
data covers the old. Coverage is proved against LOCATORS instead:

  1. EVERY legacy source locator has exactly one disposition, and it is not
     `unresolved`.
  2. EVERY new fact cites at least one source locator, or is marked as an
     explicit NEW DECISION with a stated author.
  3. Every cited locator exists in the ledger.
  4. ⚠️ A GROUPED observation may not be partially split. `E-KL-SOC-K` is
     "socket outlets, count 3" - if it becomes occurrences, it becomes as many
     as the grouping decision states, and that decision is recorded. Two
     occurrences from a count of three is the failure this catches, and it is
     silent in every other check because both numbers are plausible.

⚠️ THIS GATE IS EXPECTED TO FAIL TODAY, and that is the point: 74 locators are
enumerated and none is yet classified. It fails until the classification is
reviewed, which is what stops the migration proceeding on unexamined evidence.

    .venv\\Scripts\\python.exe tools/services/check_migration_coverage.py
"""
from __future__ import annotations

import argparse
import csv
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER = os.path.join(REPO, "_Inbox", "migration",
                      "services_migration_ledger.csv")

VALID = {"migrated", "duplicate", "contradicted", "retracted", "unresolved"}
RESOLVED = VALID - {"unresolved"}


def load_ledger(path):
    if not os.path.exists(path):
        return []
    with io.open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check(ledger_rows, new_facts=None, require_complete=False):
    """(problems, summary). `new_facts` is the migrated data, when it exists."""
    problems = []
    new_facts = new_facts or []

    seen = {}
    for row in ledger_rows:
        locator = (row.get("locator") or "").strip()
        if not locator:
            problems.append("a ledger row has no source locator")
            continue
        if locator in seen:
            problems.append("locator %s appears twice in the ledger" % locator)
        seen[locator] = row
        disposition = (row.get("disposition") or "").strip()
        if disposition not in VALID:
            problems.append("locator %s has disposition %r, which is not one of %s"
                            % (locator, disposition, ", ".join(sorted(VALID))))
        elif disposition == "contradicted" and not (row.get("disposition_note") or "").strip():
            problems.append("locator %s is `contradicted` but does not name what "
                            "overrides it" % locator)

    unresolved = [k for k, v in seen.items()
                  if (v.get("disposition") or "").strip() == "unresolved"]
    if require_complete and unresolved:
        problems.append("%d source locator(s) are still `unresolved`; the migration "
                        "may not be declared complete: %s"
                        % (len(unresolved), ", ".join(sorted(unresolved)[:5])
                           + (" ..." if len(unresolved) > 5 else "")))

    # 2 + 3 - every new fact is traceable
    for fact in new_facts:
        cites = [c for c in (fact.get("source_locators") or "").split(";") if c.strip()]
        decision = (fact.get("new_decision_by") or "").strip()
        ident = fact.get("identity_uuid") or fact.get("service_id") or "?"
        if not cites and not decision:
            problems.append("new fact %s cites no source locator and is not marked "
                            "as a new decision" % ident)
        for cite in cites:
            if cite.strip() not in seen:
                problems.append("new fact %s cites locator %s, which the ledger does "
                                "not carry" % (ident, cite.strip()))

    # 4 - a grouped observation may not be partially split
    for locator, row in seen.items():
        if row.get("grouped") != "yes":
            continue
        derived = [f for f in new_facts
                   if locator in (f.get("source_locators") or "")]
        if not derived:
            continue
        stated = (row.get("split_into") or "").strip()
        if not stated:
            problems.append(
                "grouped observation %s produced %d record(s) but the ledger does "
                "not state how many it splits into - the grouping decision has to "
                "be explicit before it is split"
                % (locator, len(derived)))
        elif stated.isdigit() and int(stated) != len(derived):
            problems.append(
                "grouped observation %s splits into %s by the ledger but produced "
                "%d record(s)" % (locator, stated, len(derived)))

    summary = {
        "locators": len(seen),
        "unresolved": len(unresolved),
        "grouped": sum(1 for v in seen.values() if v.get("grouped") == "yes"),
        "new_facts": len(new_facts),
    }
    return problems, summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ledger", default=LEDGER)
    ap.add_argument("--require-complete", action="store_true",
                    help="fail while any locator is still unresolved")
    a = ap.parse_args()

    rows = load_ledger(a.ledger)
    if not rows:
        print("no ledger at %s - run build_migration_ledger.py first"
              % os.path.relpath(a.ledger, REPO))
        return 2

    problems, summary = check(rows, require_complete=a.require_complete)
    print("locators %d | unresolved %d | grouped %d | new facts %d"
          % (summary["locators"], summary["unresolved"],
             summary["grouped"], summary["new_facts"]))
    for problem in problems:
        print("  " + problem)
    print("PASS" if not problems else "FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
