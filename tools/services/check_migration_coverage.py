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
  4. ⚠️ A source of known multiplicity may not be PARTIALLY split into
     occurrences. `E-KL-SOC-K` is "socket outlets, count 3": if it becomes
     occurrences it becomes as many as `occurrence_split_count` states. Two
     from a count of three is silent in every other check, because both
     numbers are plausible.

     ⚠️ It counts OCCURRENCES ONLY. One source legitimately produces an
     observation, several occurrences, several value records and an approval -
     comparing all of those against "3" would reject the schema's intended
     one-to-many mapping. `target_concept` on each new fact decides what counts.

     ⚠️ And uncertain multiplicity is NOT a split. `E-KL-SOC-W` is "count 2-3,
     low + one mid": it stays an observation, carrying count_min, count_max and
     the raw vertical text, until somebody decides how many terminals there
     are. A range must never be silently resolved to a number.

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

VALID = {"migrated", "duplicate", "contradicted", "retracted", "out_of_scope",
         "unresolved"}
# `out_of_scope` exists because not every captured line is a service fact:
# migration policy, drawing-label feedback and notes about the code all appear
# in the same comment blocks. Calling those `duplicate` would be dishonest.
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
        # Only a source with a KNOWN multiplicity can be checked for a partial
        # split. A `range` is deliberately exempt: it has no right answer yet,
        # and the check that matters for it is that it produced no occurrences
        # at all.
        multiplicity = (row.get("multiplicity") or "").strip()
        if multiplicity not in ("exact_n", "range"):
            continue
        # OCCURRENCES only. An observation, value records and approvals from the
        # same source are expected and must not count against the split.
        derived = [f for f in new_facts
                   if locator in (f.get("source_locators") or "")
                   and (f.get("target_concept") or "") == "occurrence"]
        if not derived:
            continue
        if multiplicity == "range" and derived:
            problems.append(
                "source %s has an UNCERTAIN multiplicity (%s-%s) but produced %d "
                "occurrence(s); a range must be decided before it is split, not "
                "resolved to a number by the migration"
                % (locator, row.get("count_min"), row.get("count_max"), len(derived)))
            continue

        stated = (row.get("occurrence_split_count") or "").strip()
        if not stated:
            problems.append(
                "source %s produced %d occurrence(s) but the ledger does "
                "not state how many it splits into - the grouping decision has to "
                "be explicit before it is split"
                % (locator, len(derived)))
        elif stated.isdigit() and int(stated) != len(derived):
            problems.append(
                "source %s splits into %s occurrence(s) by the ledger but produced "
                "%d record(s)" % (locator, stated, len(derived)))

    summary = {
        "locators": len(seen),
        "unresolved": len(unresolved),
        "exact_n": sum(1 for v in seen.values()
                       if (v.get("multiplicity") or "") == "exact_n"),
        "range": sum(1 for v in seen.values()
                     if (v.get("multiplicity") or "") == "range"),
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
    print("locators %d | unresolved %d | exact_n %d | range %d | new facts %d"
          % (summary["locators"], summary["unresolved"], summary["exact_n"],
             summary["range"], summary["new_facts"]))
    for problem in problems:
        print("  " + problem)
    print("PASS" if not problems else "FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
