#!/usr/bin/env python3
"""Guard the migration EXTRACTOR by seeding the omissions it failed to detect.

`00_Master/Validator_Design_Discipline.md`: a gate nobody has watched fail is
not a gate. The coverage gate is guarded by `migration_coverage_selftest.py`,
but coverage is measured against the inventory - so an inventory that is
missing a source is coverage that proves nothing, and NOTHING was watching the
inventory itself.

⚠️ WHAT ACTUALLY WENT WRONG, AND WHY THESE SEEDS EXIST
------------------------------------------------------
The extractor took its keyed blocks from an ALLOW-LIST of six variable names.
An allow-listed extractor cannot detect an authored block it was never told
exists, so it reported a complete inventory of 105 locators while the generator
was drawing and tagging NINE sources it had never seen:

  P1SVC          a whole keyed block of five risers and valves
  F1, SV-VT      services coded directly, with no block at all
  V-1, V-2       an INLINE literal with no variable name - and these two are
                 not in the generator's own REVIEW table either, so
                 reconciling against that registry alone would still have
                 missed them

Seeds 2-4 are those three shapes. Seed 5 is the regression the repair itself
caused: replacing the allow-list with structural discovery silently dropped all
six `ROUTES` locators, and the registry check could not see it, because routes
are drawn as polylines and never tagged.

    .venv\\Scripts\\python.exe scripts/migration_ledger_selftest.py
"""
from __future__ import annotations

import ast
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools" / "services"))

from build_migration_ledger import (  # noqa: E402
    _rows_from_literals, check_registry, check_retained, registry)

SHEETS = REPO / "tools" / "layout" / "sheets" / "make_services_sheets.py"


def main() -> int:
    failures = 0
    source = io.open(SHEETS, encoding="utf-8").read()
    rows = _rows_from_literals(source)

    def expect(label, problems, want_problem, needle=""):
        nonlocal failures
        hit = any(needle in p for p in problems) if needle else bool(problems)
        if hit == want_problem:
            print("PASS %-52s %s" % (label, (problems[0][:60] if problems
                                             else "no problems")))
        else:
            print("FAIL %-52s wanted problem=%s, got %d: %s"
                  % (label, want_problem, len(problems), problems[:1]))
            failures += 1

    # 1 - the real generator, fully ledgered
    expect("the real generator reconciles", check_registry(rows, source), False)

    # ⚠️ 2 - THE P1SVC SHAPE. A keyed block the extractor was never told about.
    # This is the one the allow-list could not possibly have caught.
    seeded = source + (
        "\nNEWBLOCK = [('NB-1', 10, 20, 'a'), ('NB-2', 30, 40, 'b')]\n"
        "for iid, bx, by, src in NEWBLOCK:\n"
        "    px, py = s3.P((bx, by))\n"
        "    s3.sym_riser(px, py, MG)\n"
        "    tagsrc(s3, px, py, iid, src, MG)\n")
    expect("an unknown keyed block is discovered and demanded",
           check_registry(rows, seeded), True, "'NB-1'")
    seeded_rows = _rows_from_literals(seeded)
    expect("...and the extractor actually ledgers it",
           [] if any(r["locator"] == "legacy_generator:NEWBLOCK:NB-1"
                     for r in seeded_rows) else ["NEWBLOCK not extracted"],
           False)

    # 3 - the F1 shape: a service coded directly, with no block at all
    seeded = source + ("\npx, py = s3.P((500, 500))\n"
                       "s3.sym_detector(px, py, R)\n"
                       "tagsrc(s3, px, py, 'F9', 'seed', R)\n")
    expect("a standalone tagged service is demanded",
           check_registry(rows, seeded), True, "'F9'")
    expect("...and the extractor ledgers it as a tag",
           [] if any(r["locator"] == "legacy_generator:tag:F9"
                     for r in _rows_from_literals(seeded))
           else ["F9 not extracted"], False)

    # 4 - the V-1/V-2 shape: an INLINE literal with no variable name. ⚠️ These
    # are tagged on the sheet but absent from REVIEW, so a check written
    # against the generator's own review registry would NOT catch this one.
    seeded = source + (
        "\nfor iid, bx, by in (('Z-1', 1, 2), ('Z-2', 3, 4)):\n"
        "    px, py = s3.P((bx, by))\n"
        "    s3.sym_riser(px, py, OR)\n"
        "    tagsrc(s3, px, py, iid, 'seed', OR)\n")
    expect("an inline unnamed literal is demanded",
           check_registry(rows, seeded), True, "'Z-1'")
    # ...and the LIVE proof of why the review registry is not enough on its
    # own: V-1 and V-2 are real, drawn, tagged, ledgered - and no
    # `REVIEW.append` anywhere in the generator mentions them.
    reviewed = set()
    for node in ast.walk(ast.parse(source)):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "append"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "REVIEW"):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    reviewed.add(sub.value)
    vents = {"V-1", "V-2"}
    expect("V-1/V-2 are ledgered but absent from REVIEW",
           ([] if vents <= set(registry(source)) else ["V-1/V-2 not in registry"])
           + (["REVIEW does mention %s" % (vents & reviewed)]
              if vents & reviewed else []),
           False)

    # ⚠️ 5 - THE REGRESSION THE REPAIR CAUSED. A source that leaves the
    # inventory silently. The registry check cannot see this: ROUTES are drawn
    # as polylines and never tagged, so nothing else was watching.
    previous = set(r["locator"] for r in rows)
    dropped = [r for r in rows if not r["locator"].startswith("legacy_generator:ROUTES")]
    expect("a silently dropped ROUTES locator is caught",
           check_retained(dropped, previous), True, "cannot leave the inventory")

    # 6 - and retention passes when nothing was lost
    expect("retention passes when nothing is lost",
           check_retained(rows, previous), False)

    # 7 - a route may NOT become one fact per vertex
    route_rows = [r for r in rows if r["source_kind"] == "python_literal_route"]
    expect("routes stay one locator each, not one per point",
           [] if len(route_rows) == 3 else
           ["%d route locators, expected 3" % len(route_rows)], False)

    # 8 - the registry is the SECOND derivation, and it must be non-trivial: a
    # check that finds nothing to check is not a check.
    expect("the registry is non-empty",
           [] if len(registry(source)) >= 30 else
           ["registry has only %d ids" % len(registry(source))], False)

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
