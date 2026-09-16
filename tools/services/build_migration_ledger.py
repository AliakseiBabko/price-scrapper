#!/usr/bin/env python3
"""Enumerate every legacy services fact, with a SOURCE LOCATOR and a disposition.

STEP 1 OF THE SERVICE MIGRATION, and deliberately the only step that runs
before anything is classified. It writes OUTSIDE `data/canonical/` - this is a
working ledger, not authored data, and it must not become a second authority
while the migration is in flight.

WHY A LEDGER AND NOT A CONVERSION
---------------------------------
This is not a schema change. One legacy row can become an observation plus
several occurrences, approvals and relations - `E-KL-SOC-K` is "socket outlets,
count 3, height 915-1105" from one photo. A textual diff cannot prove semantic
coverage across that split, so coverage is proved against LOCATORS instead:
every legacy fact must end up with exactly one disposition, and every new fact
must cite a locator or an explicit new decision.

DISPOSITIONS
  migrated      carried into the new canonical files
  duplicate     the same fact already carried by another locator
  contradicted  a later source overrides it; the override is named
  retracted     withdrawn, by the owner or by evidence
  unresolved    NOT YET CLASSIFIED - the default, and the only honest starting
                value for anything needing judgement

⚠️ EVERYTHING STARTS `unresolved`. A disposition is a decision about evidence
and the tool must not invent one. In particular a GROUPED observation - the
existing data says `"low + one mid"` and `"2-3"` - must not be split into
physical occurrences until the grouping decision is explicit and recorded.

    .venv\\Scripts\\python.exe tools/services/build_migration_ledger.py
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEETS = os.path.join(REPO, "tools", "layout", "sheets", "make_services_sheets.py")
CANON = os.path.join(REPO, "data", "canonical")
# ⚠️ TRACKED, and deliberately NOT under data/ - everything there is
# gitignored as generated output, and a disposition is a DECISION about
# evidence. Losing it to .gitignore would make the classification
# unreviewable and unrepeatable. Outside data/canonical/ all the same:
# this is a working ledger, not authored data, and it must not become a
# second authority while the migration is in flight.
OUT = os.path.join(REPO, "_Inbox", "migration")

LEGACY_CSVS = ("electrical_existing.csv", "service_outlets.csv",
               "plumbing_anchors.csv", "services_observed.csv")

# Literal blocks in the frozen generator that carry AUTHORED facts.
LITERAL_BLOCKS = ("SOCK", "POWER", "SWDEF", "LIGHT", "PIPES",
                  "ROUTES", "SEWER", "BATH_W", "BATH_S")

# Prose that states a decision or an observation rather than explaining code.
# Matched on the Russian and English words the file actually uses.
DECISION_WORDS = ("ВЛАДЕЛЕЦ", "владелец", "Owner:", "owner ", "OWNER")

FIELDS = ["locator", "source_kind", "raw", "carries", "disposition",
          "disposition_note", "grouped", "target_concept"]


def _rows_from_csv(name):
    path = os.path.join(CANON, name)
    if not os.path.exists(path):
        return []
    out = []
    with io.open(path, encoding="utf-8") as fh:
        for index, row in enumerate(csv.DictReader(fh), start=2):  # 1 = header
            ident = (row.get("item_id") or row.get("outlet_id")
                     or row.get("anchor_id") or row.get("obs_id") or "?")
            # A grouped record describes SEVERAL things, or a height that is not
            # a point. Flagged, never silently split.
            count = (row.get("count") or "").strip()
            height = (row.get("height_mm") or row.get("centre_height_mm") or "").strip()
            grouped = bool(
                re.search(r"[-+]|\bto\b|,", count)
                or (count and count not in ("1", ""))
                or re.search(r"[-–]|\+|~|ceiling|floor|low|mid", height, re.I))
            out.append({
                "locator": "%s:%d#%s" % (name, index, ident),
                "source_kind": "canonical_csv",
                "raw": json.dumps({k: v for k, v in row.items() if v},
                                  ensure_ascii=False)[:400],
                "carries": "count=%s height=%s" % (count or "-", height or "-"),
                "disposition": "unresolved",
                "disposition_note": "",
                "grouped": "yes" if grouped else "no",
                "target_concept": "",
            })
    return out


def _rows_from_literals():
    """Real tuple literals, via the AST.

    ⚠️ A regex over "everything between the block's brackets" was tried and was
    badly wrong: the bracket-depth arithmetic never closed, so the FIRST block
    swallowed the rest of the file and 32 real rows came out as 224 - including
    parentheses inside comments and unrelated expressions. Parsing the syntax
    gives exact rows with exact line numbers and cannot drift.
    """
    if not os.path.exists(SHEETS):
        return []
    import ast

    source = io.open(SHEETS, encoding="utf-8").read()
    tree = ast.parse(source)
    lines = source.splitlines()
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        block = next((n for n in names if n in LITERAL_BLOCKS), None)
        if block is None or not isinstance(node.value, ast.List):
            continue
        for element in node.value.elts:
            if not isinstance(element, (ast.Tuple, ast.List)):
                continue
            text = lines[element.lineno - 1].strip()
            # ⚠️ LINE AND COLUMN. Several blocks put two tuples on one line -
            # SEWER, BATH_W, BATH_S and ROUTES all do - so a line-only locator
            # COLLIDES, and six facts shared three locators. A colliding
            # locator is worse than a missing one: two different facts become
            # indistinguishable, and a disposition applied to one silently
            # claims to cover the other. Caught by the coverage selftest's own
            # baseline, which is what a baseline is for.
            out.append({
                "locator": "make_services_sheets.py:%d:%d#%s"
                           % (element.lineno, element.col_offset, block),
                "source_kind": "python_literal",
                "raw": text[:400],
                "carries": block,
                "disposition": "unresolved",
                "disposition_note": "",
                "grouped": "no",
                "target_concept": "",
            })
    return out


def _rows_from_owner_comments():
    if not os.path.exists(SHEETS):
        return []
    out = []
    for number, line in enumerate(io.open(SHEETS, encoding="utf-8").read().splitlines(), 1):
        text = line.strip()
        if not text.startswith("#"):
            continue
        if not any(word in text for word in DECISION_WORDS):
            continue
        out.append({
            "locator": "make_services_sheets.py:%d#comment" % number,
            "source_kind": "owner_statement_in_comment",
            "raw": text.lstrip("# ")[:400],
            "carries": "a decision recorded as PROSE, not as data",
            "disposition": "unresolved",
            "disposition_note": "",
            "grouped": "no",
            "target_concept": "",
        })
    return out


def build():
    rows = []
    for name in LEGACY_CSVS:
        rows.extend(_rows_from_csv(name))
    rows.extend(_rows_from_literals())
    rows.extend(_rows_from_owner_comments())
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=os.path.join(OUT, "services_migration_ledger.csv"))
    a = ap.parse_args()

    rows = build()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)

    # NEVER overwrite dispositions already decided. The ledger is worked on by
    # hand between runs, and regenerating it must not silently reset judgement
    # back to `unresolved` - which is the migration's own version of the defect
    # this whole exercise exists to fix.
    existing = {}
    if os.path.exists(a.out):
        with io.open(a.out, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                existing[row["locator"]] = row
    kept = 0
    for row in rows:
        prior = existing.get(row["locator"])
        if prior and prior.get("disposition") not in ("", "unresolved"):
            row["disposition"] = prior["disposition"]
            row["disposition_note"] = prior.get("disposition_note", "")
            row["target_concept"] = prior.get("target_concept", "")
            kept += 1

    with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    by_kind = {}
    for row in rows:
        by_kind[row["source_kind"]] = by_kind.get(row["source_kind"], 0) + 1
    print("wrote %s" % os.path.relpath(a.out, REPO))
    for kind, count in sorted(by_kind.items()):
        print("   %-32s %3d" % (kind, count))
    grouped = sum(1 for r in rows if r["grouped"] == "yes")
    print("   %-32s %3d" % ("of which GROUPED (do not split yet)", grouped))
    print("   %-32s %3d" % ("dispositions carried over", kept))
    print("   %-32s %3d" % ("TOTAL source locators", len(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
