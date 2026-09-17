#!/usr/bin/env python3
"""Validate the issued IFC against the exchange IDS — and refuse `0 of 0`.

⚠️⚠️ THE FAILURE THIS EXISTS TO PREVENT
---------------------------------------
An IDS specification whose applicability matches NOTHING reports success. A
whole suite of them reports total success while checking nothing — the same
class of defect as a seeded gate that cannot fail, and harder to notice because
the report is green.

So every specification carries a separately authored EXPECTED APPLICABILITY
COUNT in `data/canonical/ifc_exchange_expectations.json`, and this refuses to
report a pass unless the count matches. If the generator stops producing walls,
the wall specifications do not quietly start passing.

⚠️ IDS IS NOT THE WHOLE MODEL GATE. Geometry parity, identity stability, void
semantics and quantities stay in Python — see `author_ids.py`.

    .venv-ifc314\\Scripts\\python.exe tools/ifc/check_ids.py --model out.ifc
    .venv-ifc314\\Scripts\\python.exe tools/ifc/check_ids.py --model out.ifc --baseline
"""
from __future__ import annotations

import argparse
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDS_PATH = os.path.join(REPO, "data", "canonical", "ifc_exchange.ids")
EXPECT_PATH = os.path.join(REPO, "data", "canonical", "ifc_exchange_expectations.json")
BASELINE_PATH = os.path.join(REPO, "data", "canonical", "ifc_exchange_baseline.json")


def run(model_path, ids_path=IDS_PATH, expect_path=EXPECT_PATH):
    """[(name, applicable, failed, expected, problems)] plus a problem list."""
    import ifcopenshell
    from ifctester import ids as ids_module

    model = ifcopenshell.open(model_path)
    spec_set = ids_module.open(ids_path)
    spec_set.validate(model)

    expected = json.load(io.open(expect_path, encoding="utf-8"))
    rows, problems = [], []
    for spec in spec_set.specifications:
        applicable = len(spec.applicable_entities)
        failed = len(spec.failed_entities)
        want = expected.get(spec.name)

        if want is None:
            problems.append(
                "specification %r has no expected applicability count - an "
                "unanchored specification can pass by matching nothing"
                % spec.name)
        elif applicable != want:
            # ⚠️ THE `0 of 0` GUARD, and it is not only about zero: a count
            # that drifted means the specification is no longer checking what
            # it was written to check.
            problems.append(
                "specification %r applies to %d entities, expected %d%s"
                % (spec.name, applicable, want,
                   " - IT MATCHED NOTHING, so its pass is meaningless"
                   if applicable == 0 else ""))
        rows.append((spec.name, applicable, failed, want))
    return rows, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default=os.path.join(REPO, "data", "outputs",
                                                    "model_from_resolved.ifc"))
    ap.add_argument("--ids", default=IDS_PATH)
    ap.add_argument("--baseline", action="store_true",
                    help="record today's failures as the accepted baseline")
    a = ap.parse_args()

    rows, problems = run(a.model, a.ids)

    print("%-44s %10s %8s %9s" % ("specification", "applies", "fails",
                                  "expected"))
    for name, applicable, failed, want in rows:
        flag = "  " if want == applicable else "⚠ "
        print("%s%-42s %10d %8d %9s"
              % (flag, name[:42], applicable, failed,
                 "-" if want is None else want))

    for problem in problems:
        print("FAIL %s" % problem)

    failing = [(n, f) for n, _a, f, _w in rows if f]
    if a.baseline:
        with io.open(BASELINE_PATH, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(
                {"recorded": "2026-09-17",
                 "note": ("Today's EXACT failures, captured BEFORE implementing "
                          "types or phase, so each requirement can be watched "
                          "failing independently rather than assumed to fail."),
                 "failures": dict(failing)},
                ensure_ascii=False, indent=2) + "\n")
        print("\nbaseline written: %d specification(s) failing"
              % len(failing))
        return 1 if problems else 0

    if problems:
        print("\nAPPLICABILITY PROBLEMS: %d" % len(problems))
        return 2
    if failing:
        print("\n%d specification(s) FAIL the exchange contract: %s"
              % (len(failing), ", ".join(n for n, _f in failing)))
        return 1
    print("\nPASS - the model meets the exchange contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
