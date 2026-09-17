#!/usr/bin/env python3
"""Compare what WAS BUILT against what the boundary rule SAYS SHOULD BE.

⚠️⚠️ TWO INDEPENDENT RECORDS, DELIBERATELY
------------------------------------------
    wall_covering_patches.csv     presence — directly evidenced, authoritative
                                  for the EXISTING phase.
    boundary patches + decisions  requirement — derived, an independent
                                  validation and design layer.

Neither is the other's source. That is the point: a comparison between two
records that shared an origin would only ever prove they were copied correctly.

| existing presence | requirement   | meaning                                  |
| :---------------- | :------------ | :--------------------------------------- |
| present           | required      | consistent                               |
| absent            | not_required  | consistent                               |
| present           | not_required  | INVESTIGATE — an existing anomaly        |
| absent            | required      | proposed work, or a defect               |
| either            | unresolved    | REVIEW — and never overwrite what is     |
|                   |               | observed with what is merely unknown     |

⚠️ AN UNRESOLVED REQUIREMENT IS NOT A FINDING ABOUT THE BUILDING. It is a
finding about our knowledge. M2's abutting run is exactly this: its parapet
contact is unknown, so no requirement can be derived — while its ABSENCE of
insulation is evidenced and stays authoritative. Treating the unresolved
requirement as blocking was a category error; this table is what keeps the two
apart.

⚠️ THIS GATE DOES NOT FAIL ON A DISAGREEMENT. A `present` where the rule says
`not_required` is a real thing to look at, not a broken file, and failing the
build would only invite someone to widen a rule until it stopped complaining.
It fails on what is genuinely malformed: a covering patch on a face nobody
classified, or an overlap it cannot reconcile.

    .venv-ifc314\\Scripts\\python.exe tools/layout/check_covering_reconciliation.py
"""
from __future__ import annotations

import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.tabular import finite  # noqa: E402

import covering_patches  # noqa: E402
from check_boundary_patches import (  # noqa: E402
    NOT_REQUIRED, REQUIRED, UNRESOLVED, eligibility, load_assertions,
    load_decisions, load_patches)

CONSISTENT = "consistent"
ANOMALY = "investigate_existing_anomaly"
PROPOSED_OR_DEFECT = "proposed_work_or_defect"
REVIEW = "review_required"

VERDICT = {
    ("present", REQUIRED): CONSISTENT,
    ("absent", NOT_REQUIRED): CONSISTENT,
    ("present", NOT_REQUIRED): ANOMALY,
    ("absent", REQUIRED): PROPOSED_OR_DEFECT,
}


def _overlap(a0, a1, b0, b1):
    return min(a1, b1) - max(a0, b0)


def reconcile(coverings=None, boundaries=None, assertions=None, decisions=None):
    """[(covering_row, requirement, verdict, why)] plus structural problems."""
    coverings = covering_patches.active() if coverings is None else coverings
    boundaries = load_patches() if boundaries is None else boundaries
    assertions = load_assertions() if assertions is None else assertions
    decisions = load_decisions() if decisions is None else decisions

    rows, problems = [], []
    for covering in coverings:
        if (covering.get("phase") or "").strip() != "existing":
            continue
        lo = finite(covering.get("along_from_mm"))
        hi = finite(covering.get("along_to_mm"))
        if lo is None or hi is None:
            problems.append("covering patch %s has non-finite bounds"
                            % covering["patch_uuid"])
            continue
        matches = []
        for boundary in boundaries:
            if (boundary.get("state") or "").strip() != "active":
                continue
            if (boundary["host_id"] != covering["host_id"]
                    or boundary["face_ref"] != covering["face_ref"]):
                continue
            b0, b1 = finite(boundary["along_from_mm"]), finite(boundary["along_to_mm"])
            if b0 is None or b1 is None:
                continue
            if _overlap(lo, hi, b0, b1) > 0.5:
                matches.append(boundary)
        if not matches:
            problems.append(
                "covering patch %s is on %s.%s %.1f..%.1f, which NO boundary "
                "patch covers. Something was built on a face whose boundary "
                "condition nobody has stated"
                % (covering["patch_uuid"], covering["host_id"],
                   covering["face_ref"], lo, hi))
            continue
        if len(matches) > 1:
            problems.append(
                "covering patch %s spans %d boundary patches. Split it so each "
                "band sits inside ONE boundary condition, rather than letting "
                "this pick a winner"
                % (covering["patch_uuid"], len(matches)))
            continue
        requirement, rule, why = eligibility(matches[0]["patch_uuid"],
                                             assertions, decisions)
        presence = (covering.get("presence_state") or "").strip()
        if requirement == UNRESOLVED or presence == "unknown":
            verdict = REVIEW
        else:
            verdict = VERDICT.get((presence, requirement))
            if verdict is None:
                problems.append("covering patch %s: presence %r against "
                                "requirement %r is not a case this table knows"
                                % (covering["patch_uuid"], presence, requirement))
                continue
        rows.append((covering, requirement, verdict, rule or why))
    return rows, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--issued", action="store_true",
                    help="the ISSUED gate: no band may rest on an unresolved "
                         "requirement without an observed presence behind it")
    a = ap.parse_args()

    rows, problems = reconcile()
    for problem in problems:
        print("FAIL %s" % problem)

    counts = {}
    for covering, requirement, verdict, why in rows:
        counts[verdict] = counts.get(verdict, 0) + 1
        print("  %-5s %-9s %8.1f..%-8.1f %-8s -> %-10s %-28s %s"
              % (covering["host_id"], covering["face_ref"],
                 float(covering["along_from_mm"]), float(covering["along_to_mm"]),
                 covering["presence_state"], requirement, verdict, why[:40]))

    print("\n%d band(s): %s" % (len(rows), ", ".join(
        "%s %d" % (k, counts[k]) for k in sorted(counts))))

    # ⚠️⚠️ THE ISSUED RULE, and it is deliberately narrow. A REVIEW row is fine
    # so long as the EXISTING state is observed - that is M2, where presence is
    # evidenced and only the requirement is unknown. What may never be issued
    # is a band that exists because a rule guessed, with nothing observed
    # behind it.
    if a.issued:
        unbacked = [r for r in rows
                    if r[2] == REVIEW
                    and (r[0].get("presence_state") or "") == "unknown"]
        for covering, _req, _verdict, _why in unbacked:
            print("FAIL %s.%s rests on an UNRESOLVED requirement with no "
                  "observed presence - issuing it would turn a gap in our "
                  "knowledge into a construction instruction"
                  % (covering["host_id"], covering["face_ref"]))
        problems.extend(unbacked)

    if problems:
        print("FAILED: %d problem(s)" % len(problems))
        return 1
    print("PASS - every built band sits against a stated boundary condition")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
