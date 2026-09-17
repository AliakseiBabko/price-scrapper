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

ADJUDICATION - a judgement about the SOURCE, and nothing else
  accepted      a real service fact, in scope, to be carried forward
  decomposed    this source carries SEVERAL independently adjudicable claims and
                is not adjudicated directly. Its atomic claims are, in the claim
                inventory. ⚠️ A compound block is not simply "old" and "new":
                legacy_comment:6 holds a retracted horizontal DN110 main, an
                accepted two-vertical-stacks reading AND an accepted "there is
                no horizontal main" - three claims, independently judged.
  duplicate     the same fact already carried by another locator
  contradicted  a later source overrides it; the override must be named
  retracted     withdrawn, by the owner or by evidence
  out_of_scope  not a service fact at all - migration policy, drawing-label
                feedback, or a note about the code. Calling those `duplicate`
                would be dishonest.
  unresolved    NOT YET ADJUDICATED - the default, and the only honest starting
                value for anything needing judgement

⚠️ THERE IS NO `migrated` ADJUDICATION, DELIBERATELY. An earlier version had
one, and it meant only "somebody typed the word": the coverage self-test marked
all 72 locators `migrated`, supplied ZERO target records, and passed. The
migration could have been declared complete having produced no data at all.

**Whether a source was actually carried forward is DERIVED** from the target
records that cite it - never authored here. `contradicted` and `retracted`
sources still need targets, because they survive as history; `out_of_scope` is
the only ordinary case needing none.

⚠️ AND NO FAN-OUT LIVES HERE. One locator can target several concepts at once -
an observation, three occurrences, value records and an approval - so a single
`target_concept` column was wrong in kind. The ledger holds SOURCE-LEVEL
JUDGEMENT only; the target records live in their own draft tables, keyed by a
provisional `migration_key` and their `source_locators`.

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

# ⚠️ KEYED BLOCKS ARE DISCOVERED BY SHAPE, NOT ALLOW-LISTED.
# ------------------------------------------------------------------
# There used to be a `KEYED_BLOCKS` tuple naming six variables, and it was a
# GATE-DESIGN DEFECT of exactly the kind this repository keeps finding: an
# allow-listed extractor cannot detect an authored block it was never told
# exists. It silently missed NINE drawn, tagged placement assertions -
#
#   P1SVC     five risers and valves (SW-B-H, SW-B-C, SS-B, SH-B, SS-K2)
#   F1        a fire detector, coded directly with no block at all
#   SV-VT     a transfer opening, likewise standalone
#   V-1, V-2  vent grilles in an INLINE literal with no variable name, and
#             which the generator tags on the sheet but never even adds to
#             its own REVIEW table
#
# - and still reported "TOTAL source locators 105" as though that were the
# inventory. V-1/V-2 are why reconciling against the generator's REVIEW table
# alone would NOT have been enough either: the sheet draws and tags them, and
# the review registry does not contain them.
#
# So discovery is structural (a literal of key-first tuples, iterated by a loop
# that draws), the standalone tags are read directly, and `check_registry()` is
# the backstop that fails on anything drawn but unledgered.
#
# Blocks that are ONE polyline each: their elements are the route's points, not
# separate facts, so ledgering per point would invent facts that do not exist.
# This one stays DECLARED rather than inferred - mistaking a route for a keyed
# block would manufacture a fact per vertex, so it may not be a guess.
POLYLINE_BLOCKS = ("SEWER", "BATH_W", "BATH_S")

# `tagsrc(sheet, px, py, iid, src, col)` - the item id is positional arg 3.
TAGSRC_IID_ARG = 3

# What "this loop PLACES something on the sheet" looks like. ⚠️ This is a
# heuristic and it is allowed to be one ONLY because `check_retained()` refuses
# to let it drop a source: the first version listed `sym_*`, `tagsrc` and
# `REVIEW.append`, and it silently lost all six `ROUTES` - which draw with
# `polyline_rounded` and are never tagged, so the registry check could not see
# them go either. Over-inclusion is cheap: a literal still has to be a list of
# key-first tuples to become a keyed block at all.
DRAW_CALLS = ("tagsrc", "REVIEW.append", "polyline_rounded", "callout", "htag")

DECISION_WORDS = ("ВЛАДЕЛЕЦ", "владелец", "Owner:", "owner ", "OWNER",
                  "owner’s", "OWNER’s")

FIELDS = ["locator", "source_kind", "raw", "carries",
          "multiplicity", "count_min", "count_max",
          "reviewed_multiplicity", "reviewed_multiplicity_note",
          "vertical_kind", "vertical_raw",
          "occurrence_split_count", "expected_target_concepts",
          "adjudication", "adjudication_note", "review_position"]


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
    bands = set(re.findall(r"\b(low|mid|high)\b", low))
    if len(bands) > 1:
        # "low + one mid" describes DIFFERENT heights for DIFFERENT items. It is
        # not one height with uncertainty, so it cannot become a range with a min
        # and a max either - it needs the grouping decision first.
        return "mixed_qualitative", text
    if bands:
        # A single qualitative BAND shared by every item the row describes.
        # "E-MR-SOC, count 2, height low" is two sockets both low - one band, not
        # a mixed description. Treating it as mixed overstated the uncertainty on
        # two of the three rows that carried it.
        return "band", text
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
                # ⚠️ PARSED and REVIEWED multiplicity are different things. The
                # parser reports what the ROW SAYS and never more - service_outlets
                # has no `count` column at all, so every row there parses as
                # `unstated`. Classification may resolve that from the row's
                # complete evidence - "sewer connection, MAIN" plus an observation
                # of one stack is one occurrence - but it does so HERE, with a
                # note, rather than by the parser defaulting to `single`.
                "reviewed_multiplicity": "",
                "reviewed_multiplicity_note": "",
                "vertical_kind": vkind,
                "vertical_raw": vraw,
                "occurrence_split_count": "",
                # A review aid only - a semicolon-separated hint at what this
                # source is expected to produce. It is NOT the fan-out and the
                # gate does not check against it.
                "expected_target_concepts": "",
                "adjudication": "unresolved",
                "adjudication_note": "",
                "review_position": "%s:%d" % (name, index),
            })
    return out


def _dotted(func):
    """`tagsrc` / `REVIEW.append` / `s3.sym_riser` as a flat name."""
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        base = _dotted(func.value)
        return (base + "." + func.attr) if base else func.attr
    return ""


def _is_draw(node):
    """Does this subtree PLACE a tagged item on a sheet?

    That is the signature of an authored placement assertion, and it is what
    replaces the allow-list: a block nobody named is still discovered, because
    the code that draws it looks the same as the code that draws the rest.
    """
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            name = _dotted(sub.func)
            leaf = name.rsplit(".", 1)[-1]
            if (name in DRAW_CALLS or leaf in DRAW_CALLS
                    or leaf.startswith("sym_")):
                return True
    return False


def _keys(literal):
    """The string keys of a list/tuple of key-first tuples, else None.

    A route literal is a list of COORDINATE tuples, so its first element is a
    number and this returns None - which is the honest answer, not a guess.
    """
    if not isinstance(literal, (ast.List, ast.Tuple)) or not literal.elts:
        return None
    keys = []
    for element in literal.elts:
        if not isinstance(element, (ast.Tuple, ast.List)) or not element.elts:
            return None
        first = element.elts[0]
        if not (isinstance(first, ast.Constant) and isinstance(first.value, str)):
            return None
        keys.append(first.value)
    return keys


def _keyed_literals(tree):
    """name -> (literal node, keys, ORIGIN name).

    The origin matters: the switches are AUTHORED in `SWDEF` and drawn from
    `SW`, which a loop assembles from it. The locator must name the source the
    reviewer judges - `legacy_generator:SWDEF:W1` - so the keys propagate
    forward through that loop while the origin name stays put.
    """
    found = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        keys = _keys(node.value)
        if not keys:
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                found[target.id] = (node.value, keys, target.id)

    for node in ast.walk(tree):
        if not isinstance(node, ast.For) or not isinstance(node.iter, ast.Name):
            continue
        source = found.get(node.iter.id)
        if source is None:
            continue
        for sub in ast.walk(node):
            if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute)
                    and sub.func.attr == "append"
                    and isinstance(sub.func.value, ast.Name)):
                found.setdefault(sub.func.value.id, source)
    return found


def _drawn_blocks(tree, literals):
    """(named blocks, inline blocks) that a drawing loop actually iterates."""
    named, inline, seen = {}, [], set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.For) or not _is_draw(node):
            continue
        if isinstance(node.iter, ast.Name):
            entry = literals.get(node.iter.id)
            if entry and entry[2] not in seen:
                seen.add(entry[2])
                named[entry[2]] = entry
        else:
            keys = _keys(node.iter)
            if keys:
                inline.append((node.iter, keys))
    return named, inline


def _standalone_tags(tree):
    """key -> line, for items coded directly with no block at all.

    `F1` and `SV-VT` are each a bare `tagsrc(...)` / `REVIEW.append(...)` in
    module scope. They are placement assertions like any other and they were
    invisible to the block-shaped extractor.
    """
    out = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _dotted(node.func)
        if name == "tagsrc" and len(node.args) > TAGSRC_IID_ARG:
            arg = node.args[TAGSRC_IID_ARG]
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                out.setdefault(arg.value, node.lineno)
        elif name == "REVIEW.append" and node.args:
            first = node.args[0]
            if isinstance(first, ast.Dict):
                for key, value in zip(first.keys, first.values):
                    if (isinstance(key, ast.Constant) and key.value == "item_id"
                            and isinstance(value, ast.Constant)
                            and isinstance(value.value, str)):
                        out.setdefault(value.value, node.lineno)
    return out


def registry(source):
    """EVERY item id the generator draws, tags or reviews - the whole registry.

    This is deliberately derived a SECOND way, independently of extraction, so
    that a discovery miss shows up as a coverage failure instead of as a
    smaller inventory nobody questions.
    """
    tree = ast.parse(source)
    literals = _keyed_literals(tree)
    named, inline = _drawn_blocks(tree, literals)
    ids = {}
    for _node, keys, origin in named.values():
        for key in keys:
            ids.setdefault(key, origin)
    for _node, keys in inline:
        for key in keys:
            ids.setdefault(key, "inline")
    for key in _standalone_tags(tree):
        ids.setdefault(key, "standalone")
    return ids


def check_registry(rows, source):
    """⚠️ THE BACKSTOP. Anything the generator draws must be in the ledger.

    The inventory may not be declared complete while the sheet places a tagged
    item that no locator carries. This is the check that the allow-list version
    could not have had, because it compared the ledger against the same list it
    extracted from.
    """
    carried = set()
    for row in rows:
        locator = row["locator"]
        if locator.startswith("legacy_generator:"):
            carried.add(locator.split(":")[-1])
    problems = []
    for key, origin in sorted(registry(source).items()):
        if key not in carried:
            problems.append(
                "the generator draws and tags %r (%s) but NO ledger locator "
                "carries it - the inventory is not complete" % (key, origin))
    return problems


def check_retained(rows, previous):
    """⚠️ A SOURCE MAY NEVER LEAVE THE INVENTORY SILENTLY.

    `check_registry()` only sees what the generator TAGS, so it cannot notice
    an untagged source disappearing - and one immediately did. Replacing the
    allow-list with structural discovery dropped all six `ROUTES` locators,
    the registry check passed, and the printed total went DOWN while reading
    like an improvement.

    A source leaves this ledger only by someone deleting it from the generator,
    and then the raw text goes too. Anything else is extraction regression.
    """
    produced = set(row["locator"] for row in rows)
    problems = []
    for locator in sorted(set(previous) - produced):
        problems.append(
            "locator %s was in the ledger and the extractor no longer produces "
            "it - a source cannot leave the inventory silently" % locator)
    return problems


def _rows_from_literals(source=None):
    # `source` is an injection point for the self-test: a seeded generator has
    # to reach the extractor without being written into the tree.
    if source is None:
        if not os.path.exists(SHEETS):
            return []
        source = io.open(SHEETS, encoding="utf-8").read()
    lines = source.splitlines()
    tree = ast.parse(source)
    literals = _keyed_literals(tree)
    named, inline = _drawn_blocks(tree, literals)
    out = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.List):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        block = next((n for n in names if n in POLYLINE_BLOCKS), None)
        if block is not None:
            # ONE route, not one fact per vertex. Ledgering each point would
            # invent facts the source does not contain.
            out.append({
                "locator": "legacy_generator:%s" % block,
                "source_kind": "python_literal_route",
                "raw": lines[node.lineno - 1].strip()[:400],
                "carries": "%d-point polyline" % len(node.value.elts),
                "multiplicity": "single", "count_min": "1", "count_max": "1",
                "reviewed_multiplicity": "", "reviewed_multiplicity_note": "",
                "vertical_kind": "unstated", "vertical_raw": "",
                "occurrence_split_count": "", "expected_target_concepts": "",
                "adjudication": "unresolved", "adjudication_note": "",
                "review_position": "make_services_sheets.py:%d" % node.lineno,
            })

    def keyed(block, element, key):
        return {
            "locator": "legacy_generator:%s:%s" % (block, key),
            "source_kind": "python_literal",
            "raw": lines[element.lineno - 1].strip()[:400],
            "carries": block,
            "multiplicity": "single", "count_min": "1", "count_max": "1",
            "reviewed_multiplicity": "", "reviewed_multiplicity_note": "",
            "vertical_kind": "unstated", "vertical_raw": "",
            "occurrence_split_count": "", "expected_target_concepts": "",
            "adjudication": "unresolved", "adjudication_note": "",
            "review_position": "make_services_sheets.py:%d:%d"
                               % (element.lineno, element.col_offset),
        }

    blocks = [(origin, node) for node, _keys, origin in named.values()]
    # An INLINE literal has no variable name to be semantic about, so its items
    # are located by their own id under `tag:` - the id IS the stable key, and
    # a line number would not be stable at all.
    blocks += [("tag", node) for node, _keys in inline]
    for block, node in blocks:
        for element in node.elts:
            first = element.elts[0]
            out.append(keyed(block, element, first.value))

    seen = set(row["locator"].split(":")[-1] for row in out)
    for key, line in sorted(_standalone_tags(ast.parse(source)).items()):
        if key in seen:
            continue
        out.append({
            "locator": "legacy_generator:tag:%s" % key,
            "source_kind": "python_literal_standalone",
            "raw": lines[line - 1].strip()[:400],
            "carries": "tag",
            "multiplicity": "single", "count_min": "1", "count_max": "1",
            "reviewed_multiplicity": "", "reviewed_multiplicity_note": "",
            "vertical_kind": "unstated", "vertical_raw": "",
            "occurrence_split_count": "", "expected_target_concepts": "",
            "adjudication": "unresolved", "adjudication_note": "",
            "review_position": "make_services_sheets.py:%d" % line,
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
            # NOT truncated. A comment block is EVIDENCE, and a reviewer-authored
            # claim must be an exact substring of it - truncation would make a
            # real claim unverifiable against its own parent. Block 6 was cut at
            # 900 characters, mid-word.
            "raw": text,
            "carries": "prose; may be a decision, an observation, a retraction, "
                       "or not a service fact at all",
            "multiplicity": "", "count_min": "", "count_max": "",
            "reviewed_multiplicity": "", "reviewed_multiplicity_note": "",
            "vertical_kind": "", "vertical_raw": "",
            "occurrence_split_count": "", "expected_target_concepts": "",
            "adjudication": "unresolved", "adjudication_note": "",
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

    # NEVER reset an adjudication already decided. Semantic locators are what make
    # this reliable: a positional one would re-attach the reviewer's judgement
    # to the wrong fact after any edit above it.
    existing, kept = {}, 0
    if os.path.exists(a.out):
        with io.open(a.out, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                existing[row["locator"]] = row
    carry = ("adjudication", "adjudication_note", "expected_target_concepts",
             "occurrence_split_count", "reviewed_multiplicity",
             "reviewed_multiplicity_note")
    for row in rows:
        prior = existing.get(row["locator"])
        if prior and (prior.get("adjudication") or "") not in ("", "unresolved"):
            for field in carry:
                if prior.get(field):
                    row[field] = prior[field]
            kept += 1

    # ⚠️ CHECKED BEFORE WRITING. A regressed inventory must not reach the file
    # at all - the previous ledger is the evidence the retention check needs,
    # and overwriting it first would destroy exactly that.
    problems = check_retained(rows, existing)
    problems += check_registry(rows, io.open(SHEETS, encoding="utf-8").read())
    if problems:
        for problem in problems:
            print("FAIL %s" % problem)
        print("REFUSING TO WRITE: %d problem(s); the ledger on disk is "
              "unchanged" % len(problems))
        return 1

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
        ("vertical mixed_qualitative (genuinely)", lambda r: r["vertical_kind"] == "mixed_qualitative"),
        ("vertical band (shared qualitative)", lambda r: r["vertical_kind"] == "band"),
        ("vertical continuous", lambda r: r["vertical_kind"] == "continuous"),
        ("vertical relative", lambda r: r["vertical_kind"] == "relative"),
    ):
        print("   %-34s %3d" % (label, sum(1 for r in rows if test(r))))
    print("   %-34s %3d" % ("adjudications carried over", kept))
    print("   %-34s %3d" % ("TOTAL source locators", len(rows)))

    print("   %-34s %3s" % ("retention + registry checks", "ok"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
