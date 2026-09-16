#!/usr/bin/env python3
"""Enumerate every legacy services fact, with a STABLE locator and a disposition.

STEP 1 OF THE SERVICE MIGRATION. It writes to `_Inbox/migration/`, outside
`data/canonical/` - a working ledger must not become a second authority while
the migration is in flight - and outside `data/`, everything under which is
gitignored as generated output. A disposition is a DECISION about evidence, so
it has to be reviewable and version-controlled.

WHY A LEDGER AND NOT A CONVERSION
---------------------------------
One legacy row can become an observation PLUS several occurrences, value
records, approvals and relations. A textual diff cannot prove coverage across
that split, so coverage is proved against LOCATORS: every legacy fact ends with
exactly one disposition, and every new fact cites a locator or an explicit new
decision.

⚠️ LOCATORS ARE SEMANTIC, NOT POSITIONAL
----------------------------------------
`legacy_generator:SOCK:S17`, not `make_services_sheets.py:63:1#SOCK`. Line and
column are unique but NOT STABLE: a harmless comment or reformat above a
literal shifts every later locator, which silently defeats the preservation of
dispositions already decided - the reviewer's judgement would re-attach to the
wrong fact, or be dropped. Position is kept as review metadata only.

⚠️ MULTIPLICITY, VERTICAL UNCERTAINTY AND EXTENT ARE DIFFERENT THINGS
---------------------------------------------------------------------
An earlier version had a single `grouped` flag, and it conflated all three:

  E-KL-SOC-K   count exactly 3            -> eligible for 3 occurrences, once
                                             each is matched to a placement
  E-KL-SOC-W   count 2-3, "low + one mid" -> OBSERVATION ONLY. Keep count_min=2,
                                             count_max=3 and the raw vertical
                                             text. Do NOT mint an arbitrary
                                             number of terminals.
  SS-B         "floor to ceiling"         -> ONE continuous occurrence. Not
                                             grouped: that is an extent, not a
                                             multiplicity.
  E-C-LIGHT    height "ceiling"           -> ONE occurrence with a RELATIVE
                                             vertical measurement. Not grouped.

So `multiplicity` / `count_min` / `count_max` are separate from `vertical_kind`
/ `vertical_raw`, and `occurrence_split_count` is decided by review rather than
inferred. It counts OCCURRENCES only - an observation, value records and
approvals derived from the same source must not affect it.

DISPOSITIONS
  migrated      carried into the new canonical files
  duplicate     the same fact already carried by another locator
  contradicted  a later source overrides it; the override must be named
  retracted     withdrawn, by the owner or by evidence
  out_of_scope  not a service fact at all - migration policy, drawing-label
                feedback, or a note about the code. Calling those `duplicate`
                would be dishonest.
  unresolved    NOT YET CLASSIFIED - the default, and the only honest starting
                value for anything needing judgement

    .venv\\Scripts\\python.exe tools/services/build_migration_ledger.py
"""
from __future__ import annotations

import argparse
import ast
import csv
import io
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEETS = os.path.join(REPO, "tools", "layout", "sheets", "make_services_sheets.py")
CANON = os.path.join(REPO, "data", "canonical")
OUT = os.path.join(REPO, "_Inbox", "migration")

LEGACY_CSVS = ("electrical_existing.csv", "service_outlets.csv",
               "plumbing_anchors.csv", "services_observed.csv")

# Blocks whose elements are SEPARATE facts, each with a semantic key.
KEYED_BLOCKS = ("SOCK", "POWER", "SWDEF", "LIGHT", "PIPES", "ROUTES")
# Blocks that are ONE polyline each: their elements are the route's points, not
# separate facts, so ledgering per point would invent facts that do not exist.
POLYLINE_BLOCKS = ("SEWER", "BATH_W", "BATH_S")

DECISION_WORDS = ("ВЛАДЕЛЕЦ", "владелец", "Owner:", "owner ", "OWNER",
                  "owner’s", "OWNER’s")

FIELDS = ["locator", "source_kind", "raw", "carries",
          "multiplicity", "count_min", "count_max",
          "vertical_kind", "vertical_raw",
          "occurrence_split_count", "target_concept",
          "disposition", "disposition_note", "review_position"]


def _multiplicity(count_raw):
    """(multiplicity, count_min, count_max) - never a guess.

    `2-3` is a RANGE and stays one. Turning it into two or three terminals
    would manufacture a decision nobody made.
    """
    text = (count_raw or "").strip()
    if not text:
        return "unstated", "", ""
    span = re.match(r"^(\d+)\s*[-–]\s*(\d+)", text)
    if span:
        return "range", span.group(1), span.group(2)
    exact = re.match(r"^(\d+)", text)
    if exact:
        n = exact.group(1)
        return ("single" if n == "1" else "exact_n"), n, n
    return "unknown", "", ""


def _vertical(height_raw):
    """The KIND of vertical description, with the raw text always preserved."""
    text = (height_raw or "").strip()
    if not text:
        return "unstated", ""
    low = text.lower()
    if "floor to ceiling" in low:
        return "continuous", text
    if low.startswith(("ceiling", "floor")):
        return "relative", text
    if re.search(r"\d\s*[-–]\s*\d", text):
        return "range", text
    if "~" in text:
        return "approximate", text
    if re.search(r"\b(low|mid|high)\b", low):
        # "low + one mid" describes DIFFERENT heights for different items - a
        # mixed description, not one height. It must not collapse to a number.
        return "mixed_qualitative", text
    if re.match(r"^\d+(\.\d+)?$", text):
        return "point", text
    return "unknown", text


def _rows_from_csv(name):
    path = os.path.join(CANON, name)
    if not os.path.exists(path):
        return []
    stem = os.path.splitext(name)[0]
    out = []
    with io.open(path, encoding="utf-8") as fh:
        for index, row in enumerate(csv.DictReader(fh), start=2):
            ident = (row.get("item_id") or row.get("outlet_id")
                     or row.get("anchor_id") or row.get("obs_id")
                     or "row%d" % index)
            multiplicity, cmin, cmax = _multiplicity(row.get("count"))
            vkind, vraw = _vertical(row.get("height_mm")
                                    or row.get("centre_height_mm"))
            out.append({
                "locator": "legacy_csv:%s:%s" % (stem, ident),
                "source_kind": "canonical_csv",
                "raw": json.dumps({k: v for k, v in row.items() if v},
                                  ensure_ascii=False)[:400],
                "carries": (row.get("kind") or row.get("type") or "").strip(),
                "multiplicity": multiplicity,
                "count_min": cmin,
                "count_max": cmax,
                "vertical_kind": vkind,
                "vertical_raw": vraw,
                "occurrence_split_count": "",
                "target_concept": "",
                "disposition": "unresolved",
                "disposition_note": "",
                "review_position": "%s:%d" % (name, index),
            })
    return out


def _rows_from_literals():
    if not os.path.exists(SHEETS):
        return []
    source = io.open(SHEETS, encoding="utf-8").read()
    lines = source.splitlines()
    out = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.List):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        block = next((n for n in names if n in KEYED_BLOCKS + POLYLINE_BLOCKS), None)
        if block is None:
            continue

        if block in POLYLINE_BLOCKS:
            # ONE route, not one fact per vertex. Ledgering each point would
            # invent facts the source does not contain.
            out.append({
                "locator": "legacy_generator:%s" % block,
                "source_kind": "python_literal_route",
                "raw": lines[node.lineno - 1].strip()[:400],
                "carries": "%d-point polyline" % len(node.value.elts),
                "multiplicity": "single", "count_min": "1", "count_max": "1",
                "vertical_kind": "unstated", "vertical_raw": "",
                "occurrence_split_count": "", "target_concept": "",
                "disposition": "unresolved", "disposition_note": "",
                "review_position": "make_services_sheets.py:%d" % node.lineno,
            })
            continue

        for ordinal, element in enumerate(node.value.elts, start=1):
            if not isinstance(element, (ast.Tuple, ast.List)) or not element.elts:
                continue
            first = element.elts[0]
            key = (first.value if isinstance(first, ast.Constant)
                   and isinstance(first.value, str) else "n%d" % ordinal)
            out.append({
                "locator": "legacy_generator:%s:%s" % (block, key),
                "source_kind": "python_literal",
                "raw": lines[element.lineno - 1].strip()[:400],
                "carries": block,
                "multiplicity": "single", "count_min": "1", "count_max": "1",
                "vertical_kind": "unstated", "vertical_raw": "",
                "occurrence_split_count": "", "target_concept": "",
                "disposition": "unresolved", "disposition_note": "",
                "review_position": "make_services_sheets.py:%d:%d"
                                   % (element.lineno, element.col_offset),
            })
    return out


def _rows_from_comment_blocks():
    """COMPLETE contiguous comment blocks, not keyword-bearing lines.

    ⚠️ Line-by-line capture truncated real statements mid-sentence - *"Owner:
    'there are no outlets on the wall with the"* - and several blocks carry a
    retracted interpretation AND its correction, which have to stay together so
    the correction is not read as the original claim.
    """
    if not os.path.exists(SHEETS):
        return []
    lines = io.open(SHEETS, encoding="utf-8").read().splitlines()
    blocks, current, start = [], [], None
    for number, line in enumerate(lines, start=1):
        if line.strip().startswith("#"):
            if start is None:
                start = number
            current.append(line.strip().lstrip("#").strip())
        else:
            if current:
                blocks.append((start, current))
            current, start = [], None
    if current:
        blocks.append((start, current))

    out = []
    ordinal = 0
    for start_line, body in blocks:
        text = " ".join(part for part in body if part).strip()
        if not any(word in text for word in DECISION_WORDS):
            continue
        ordinal += 1
        out.append({
            "locator": "legacy_comment:%d" % ordinal,
            "source_kind": "comment_block",
            "raw": text[:900],
            "carries": "prose; may be a decision, an observation, a retraction, "
                       "or not a service fact at all",
            "multiplicity": "", "count_min": "", "count_max": "",
            "vertical_kind": "", "vertical_raw": "",
            "occurrence_split_count": "", "target_concept": "",
            "disposition": "unresolved", "disposition_note": "",
            "review_position": "make_services_sheets.py:%d" % start_line,
        })
    return out


def build():
    rows = []
    for name in LEGACY_CSVS:
        rows.extend(_rows_from_csv(name))
    rows.extend(_rows_from_literals())
    rows.extend(_rows_from_comment_blocks())
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=os.path.join(OUT, "services_migration_ledger.csv"))
    a = ap.parse_args()

    rows = build()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)

    # NEVER reset a disposition already decided. Semantic locators are what make
    # this reliable: a positional one would re-attach the reviewer's judgement
    # to the wrong fact after any edit above it.
    existing, kept = {}, 0
    if os.path.exists(a.out):
        with io.open(a.out, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                existing[row["locator"]] = row
    carry = ("disposition", "disposition_note", "target_concept",
             "occurrence_split_count")
    for row in rows:
        prior = existing.get(row["locator"])
        if prior and (prior.get("disposition") or "") not in ("", "unresolved"):
            for field in carry:
                if prior.get(field):
                    row[field] = prior[field]
            kept += 1

    with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    kinds = {}
    for row in rows:
        kinds[row["source_kind"]] = kinds.get(row["source_kind"], 0) + 1
    print("wrote %s" % os.path.relpath(a.out, REPO))
    for kind, count in sorted(kinds.items()):
        print("   %-34s %3d" % (kind, count))
    for label, test in (
        ("multiplicity range (observation only)", lambda r: r["multiplicity"] == "range"),
        ("multiplicity exact_n (may split)", lambda r: r["multiplicity"] == "exact_n"),
        ("vertical mixed_qualitative", lambda r: r["vertical_kind"] == "mixed_qualitative"),
        ("vertical continuous", lambda r: r["vertical_kind"] == "continuous"),
        ("vertical relative", lambda r: r["vertical_kind"] == "relative"),
    ):
        print("   %-34s %3d" % (label, sum(1 for r in rows if test(r))))
    print("   %-34s %3d" % ("dispositions carried over", kept))
    print("   %-34s %3d" % ("TOTAL source locators", len(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
