#!/usr/bin/env python3
"""Coverage gate for the services migration: nothing may be lost silently.

The migration splits one legacy row into several records, so a textual diff
cannot prove the new data covers the old. Coverage is proved against LOCATORS,
and it is checked in BOTH DIRECTIONS.

⚠️ WHY BIDIRECTIONAL, AND WHAT IT FIXES
---------------------------------------
An earlier version had a `migrated` disposition, and the self-test marked all
72 locators `migrated`, supplied ZERO target records, and PASSED. `migrated`
meant only "somebody typed the word" - the migration could have been declared
complete having produced no data whatsoever. That defect is why the two
concepts are now separate:

  ADJUDICATION  a judgement about the SOURCE - accepted, duplicate,
                contradicted, retracted, out_of_scope, unresolved. AUTHORED.
  COVERAGE      whether the source was actually carried forward. DERIVED from
                the target records that cite it. NEVER authored.

THE RULES
  1. Every locator has a valid adjudication, and none is `unresolved` when the
     migration is declared complete.
  2. Every TARGET RECORD cites a valid locator, or is an explicit new decision
     with a stated author.
  3. Every target record has a valid, non-empty concept.
  4. ⚠️ Every IN-SCOPE locator is cited by at least one target record.
     `contradicted` and `retracted` sources are in scope: they survive as
     HISTORY, and dropping them silently is exactly the loss this gate exists
     to prevent. `out_of_scope` is the only ordinary case needing no target.
  5. An exact occurrence split matches `occurrence_split_count`, counting
     OCCURRENCES only - an assembly parent is not one of its own components.
  6. An UNCERTAIN multiplicity produces no occurrences at all. A range must be
     decided, never resolved to a number by the migration.

    .venv\\Scripts\\python.exe tools/services/check_migration_coverage.py
"""
from __future__ import annotations

import argparse
import csv
import glob
import io
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MIGRATION = os.path.join(REPO, "_Inbox", "migration")
LEDGER = os.path.join(MIGRATION, "services_migration_ledger.csv")
DRAFTS = os.path.join(MIGRATION, "draft")

ADJUDICATIONS = {"accepted", "duplicate", "contradicted", "retracted",
                 "out_of_scope", "decomposed", "unresolved"}
# `decomposed` is NOT a substantive judgement. It says: this source carries
# several independently adjudicable claims and is judged through them.
SUBSTANTIVE = ADJUDICATIONS - {"decomposed", "unresolved"}
CLAIMS = os.path.join(MIGRATION, "services_claim_inventory.csv")
# In scope means "must be carried forward in some form". A contradicted or
# retracted claim still has to survive as history.
IN_SCOPE = {"accepted", "duplicate", "contradicted", "retracted"}

# The concepts a target record may declare. `assembly` is a NAMED GROUP that is
# itself a thing - SW-K is the hot and cold take-offs - and it is NOT one of its
# own component occurrences.
CONCEPTS = {"occurrence", "assembly", "observation", "assertion", "value",
            "approval", "connectivity", "route", "relation"}


LOCK = os.path.join(MIGRATION, "services_claim_inventory.lock.json")


def load_lock(path=LOCK):
    if not os.path.exists(path):
        return {}
    import json
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_lock(claim_rows, path=LOCK):
    """Freeze the claim set of every parent declared complete."""
    import json
    lock = {}
    for claim in claim_rows:
        if (claim.get("claim_inventory_complete") or "").strip().lower() != "yes":
            continue
        lock.setdefault(claim.get("parent_locator"), []).append(
            claim.get("claim_locator"))
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({k: sorted(v) for k, v in lock.items()},
                            ensure_ascii=False, indent=2) + chr(10))
    return lock


def load_claims(path=CLAIMS):
    if not os.path.exists(path):
        return []
    with io.open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check_claims(ledger_rows, claim_rows):
    """The claim-inventory invariants.

    ⚠️ ONE SOURCE BLOCK -> SEVERAL ATOMIC CLAIMS -> ONE ADJUDICATION PER CLAIM.
    This is ordinary source normalisation, not an exception to one-locator-one-
    adjudication. `legacy_comment:6` holds a RETRACTED horizontal DN110 main, an
    ACCEPTED two-vertical-stacks correction and an ACCEPTED "there is no
    horizontal main" - three claims, independently judged, which is why an
    automatic 6a/6b split would not have been enough either.

    The extractor never authors these: it emits the untouched parent block, and
    a reviewer writes the child claims beneath it.
    """
    problems = []
    by_locator = {r.get("locator"): r for r in ledger_rows}
    children = {}
    slugs = set()

    for claim in claim_rows:
        locator = (claim.get("claim_locator") or "").strip()
        parent = (claim.get("parent_locator") or "").strip()
        text = claim.get("claim_text") or ""
        if not locator or "#" not in locator:
            problems.append("claim %r has no `parent#slug` locator" % locator)
            continue
        if locator in slugs:
            problems.append("claim locator %s appears twice" % locator)
        slugs.add(locator)
        if not locator.startswith(parent + "#"):
            problems.append("claim %s does not sit under its parent %s"
                            % (locator, parent))
        parent_row = by_locator.get(parent)
        if parent_row is None:
            problems.append("claim %s names parent %s, which the ledger does not "
                            "carry" % (locator, parent))
            continue
        children.setdefault(parent, []).append(claim)

        # ⚠️ The claim text must still be IN its parent. If the parent block is
        # edited and a claim no longer matches, that is a loud failure, not a
        # silent drift - the claim would otherwise keep an adjudication for
        # words nobody wrote.
        if text not in (parent_row.get("raw") or ""):
            problems.append(
                "claim %s quotes text that is NOT in its parent block any more - "
                "the source changed and the claim no longer matches: %r"
                % (locator, text[:60]))

        adjudication = (claim.get("adjudication") or "").strip()
        if adjudication not in ADJUDICATIONS or adjudication == "decomposed":
            problems.append("claim %s has adjudication %r; a claim is atomic and "
                            "may not itself be decomposed" % (locator, adjudication))
        elif adjudication == "unresolved":
            problems.append("claim %s is still unresolved" % locator)

    # A decomposed parent may not carry a substantive judgement of its own, and a
    # parent with claims must be declared decomposed.
    for parent, kids in children.items():
        parent_adjudication = (by_locator[parent].get("adjudication") or "").strip()
        if parent_adjudication in SUBSTANTIVE:
            problems.append(
                "parent %s is decomposed into %d claim(s) but also carries a "
                "substantive adjudication %r - it must be judged through its "
                "claims, not alongside them"
                % (parent, len(kids), parent_adjudication))
        elif parent_adjudication != "decomposed":
            problems.append("parent %s has claims but is not marked `decomposed`"
                            % parent)
    for locator, row in by_locator.items():
        if (row.get("adjudication") or "").strip() == "decomposed" and not children.get(locator):
            problems.append("%s is marked `decomposed` but has no claims" % locator)

    return problems, children


def load_ledger(path=LEDGER):
    if not os.path.exists(path):
        return []
    with io.open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_drafts(directory=DRAFTS):
    """Draft target records, keyed by a PROVISIONAL `migration_key`.

    ⚠️ No immutable UUID is minted until these have been reviewed. A UUID is
    forever by construction - the IFC GlobalId derives from it - so minting one
    for a record that may still be split, merged or withdrawn would create
    permanent identity for a provisional judgement.
    """
    out = []
    for path in sorted(glob.glob(os.path.join(directory, "*.csv"))):
        with io.open(path, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                row["_table"] = os.path.basename(path)
                out.append(row)
    return out


def check(ledger_rows, target_records=None, require_complete=False,
          claim_rows=None, lock=None):
    problems = []
    target_records = target_records or []
    claim_rows = claim_rows or []

    claim_problems, children = check_claims(ledger_rows, claim_rows)
    problems.extend(claim_problems)

    # ⚠️ A COMPLETED INVENTORY MAY NOT LOSE A CLAIM. Once a parent is declared
    # `claim_inventory_complete`, its set of claims is fixed: deleting one later
    # would drop an adjudicated fact with no trace, which is precisely the silent
    # loss this whole apparatus exists to prevent. Withdraw a claim by adjudicating
    # it `retracted`, never by removing the row.
    if lock:
        present = {c.get("claim_locator") for c in claim_rows}
        for parent, locked in lock.items():
            missing = [c for c in locked if c not in present]
            if missing:
                problems.append(
                    "%s was declared claim_inventory_complete but %d claim(s) have "
                    "since been REMOVED: %s - withdraw a claim by adjudicating it "
                    "`retracted`, not by deleting it"
                    % (parent, len(missing), ", ".join(sorted(missing))))

    seen = {}
    for row in ledger_rows:
        locator = (row.get("locator") or "").strip()
        if not locator:
            problems.append("a ledger row has no source locator")
            continue
        if locator in seen:
            problems.append("locator %s appears twice in the ledger" % locator)
        seen[locator] = row
        adjudication = (row.get("adjudication") or "").strip()
        if adjudication not in ADJUDICATIONS:
            problems.append("locator %s has adjudication %r, which is not one of %s"
                            % (locator, adjudication, ", ".join(sorted(ADJUDICATIONS))))
        elif (adjudication == "contradicted"
              and not (row.get("adjudication_note") or "").strip()):
            problems.append("locator %s is `contradicted` but does not name what "
                            "overrides it" % locator)

    # ⚠️ REGISTER CLAIM LOCATORS BEFORE CITATIONS ARE CHECKED. Target records
    # cite CHILD claims where a parent is decomposed, never the compound parent -
    # so a claim locator is a citable locator. Registering them after the
    # citation loop rejected every legitimate citation as "the ledger does not
    # carry it", which is how the self-test found this ordering bug.
    for claim in claim_rows:
        locator = (claim.get("claim_locator") or "").strip()
        if locator:
            seen.setdefault(locator, claim)

    unresolved = [k for k, v in seen.items()
                  if (v.get("adjudication") or "").strip() == "unresolved"]
    if require_complete and unresolved:
        problems.append("%d source locator(s) are still `unresolved`; the migration "
                        "may not be declared complete: %s"
                        % (len(unresolved), ", ".join(sorted(unresolved)[:5])
                           + (" ..." if len(unresolved) > 5 else "")))

    # 2 + 3 - every target record is traceable and typed
    cited = {}
    for record in target_records:
        ident = (record.get("migration_key") or record.get("identity_uuid")
                 or record.get("service_id") or "?")
        cites = [c.strip() for c in (record.get("source_locators") or "").split(";")
                 if c.strip()]
        decision = (record.get("new_decision_by") or "").strip()
        concept = (record.get("target_concept") or "").strip()

        if not concept:
            problems.append("target record %s declares no concept" % ident)
        elif concept not in CONCEPTS:
            problems.append("target record %s declares concept %r, which is not one "
                            "of %s" % (ident, concept, ", ".join(sorted(CONCEPTS))))

        if not cites and not decision:
            problems.append("target record %s cites no source locator and is not "
                            "marked as a new decision" % ident)
        for cite in cites:
            if cite not in seen:
                problems.append("target record %s cites locator %s, which the ledger "
                                "does not carry" % (ident, cite))
            else:
                cited.setdefault(cite, []).append(record)

    # 4 - ⚠️ THE DIRECTION THE OLD GATE WAS MISSING.
    if require_complete:
        orphaned = [k for k, v in seen.items()
                    if (v.get("adjudication") or "").strip() in IN_SCOPE
                    and not cited.get(k)]
        if orphaned:
            problems.append(
                "%d in-scope locator(s) are adjudicated but NOT CITED by any target "
                "record - adjudicating a source is not carrying it forward, and a "
                "contradicted or retracted claim still has to survive as history: %s"
                % (len(orphaned), ", ".join(sorted(orphaned)[:5])
                   + (" ..." if len(orphaned) > 5 else "")))

    # 5 + 6 - splits
    for locator, row in seen.items():
        multiplicity = (row.get("multiplicity") or "").strip()
        if multiplicity not in ("exact_n", "range"):
            continue
        occurrences = [r for r in cited.get(locator, [])
                       if (r.get("target_concept") or "") == "occurrence"]
        if not occurrences:
            continue
        if multiplicity == "range":
            problems.append(
                "source %s has an UNCERTAIN multiplicity (%s-%s) but produced %d "
                "occurrence(s); a range must be decided before it is split, not "
                "resolved to a number by the migration"
                % (locator, row.get("count_min"), row.get("count_max"),
                   len(occurrences)))
            continue
        stated = (row.get("occurrence_split_count") or "").strip()
        if not stated:
            problems.append(
                "source %s produced %d occurrence(s) but the ledger does not state "
                "how many it splits into - the decision has to be explicit before "
                "it is split" % (locator, len(occurrences)))
        elif stated.isdigit() and int(stated) != len(occurrences):
            problems.append(
                "source %s splits into %s occurrence(s) by the ledger but produced "
                "%d" % (locator, stated, len(occurrences)))

    summary = {
        "claims": len(claim_rows),
        "locators": len(seen),
        "unresolved": len(unresolved),
        "in_scope": sum(1 for v in seen.values()
                        if (v.get("adjudication") or "").strip() in IN_SCOPE),
        "cited": len(cited),
        "targets": len(target_records),
        "exact_n": sum(1 for v in seen.values()
                       if (v.get("multiplicity") or "") == "exact_n"),
        "range": sum(1 for v in seen.values()
                     if (v.get("multiplicity") or "") == "range"),
    }
    return problems, summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ledger", default=LEDGER)
    ap.add_argument("--drafts", default=DRAFTS)
    ap.add_argument("--lock", action="store_true",
                    help="freeze the claim set of every parent declared complete")
    ap.add_argument("--require-complete", action="store_true",
                    help="fail unless every locator is adjudicated AND carried forward")
    a = ap.parse_args()

    rows = load_ledger(a.ledger)
    if not rows:
        print("no ledger at %s - run build_migration_ledger.py first"
              % os.path.relpath(a.ledger, REPO))
        return 2

    targets = load_drafts(a.drafts)
    claims = load_claims()
    if a.lock:
        frozen = write_lock(claims)
        print("locked %d parent(s): %s" % (len(frozen), ", ".join(sorted(frozen))))
    lock = load_lock()
    problems, summary = check(rows, targets, require_complete=a.require_complete,
                              claim_rows=claims, lock=lock)
    print("locators %d | claims %d | unresolved %d | in scope %d | cited %d "
          "| targets %d | exact_n %d | range %d"
          % (summary["locators"], summary["claims"], summary["unresolved"],
             summary["in_scope"], summary["cited"], summary["targets"],
             summary["exact_n"], summary["range"]))
    for problem in problems:
        print("  " + problem)
    print("PASS" if not problems else "FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
