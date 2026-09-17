#!/usr/bin/env python3
"""Seed the ways the existing-state covering record could stop being true.

⚠️⚠️ WHAT THIS LAYER IS FOR. `wall_covering_patches.csv` says what the developer
ACTUALLY BUILT, per face and per extent. The boundary table says what SHOULD be
there. Keeping them apart is the whole design, so the seeds come in two groups:

  PARITY      the patches must reproduce the legacy wall_blocks columns exactly
              while both exist - a cutover that moves the source and changes an
              answer at the same time makes it impossible to say which did it.
  MEANING     presence against requirement must land in the right cell, and an
              UNRESOLVED requirement must never overwrite an observed presence.

    .venv-ifc314\\Scripts\\python.exe scripts/covering_patches_selftest.py
"""
from __future__ import annotations

import copy
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))

import covering_patches  # noqa: E402
from check_covering_reconciliation import (  # noqa: E402
    ANOMALY, CONSISTENT, PROPOSED_OR_DEFECT, REVIEW, reconcile)
from lib.tabular import ValidationError  # noqa: E402


def main() -> int:
    failures = 0
    base = covering_patches.load()

    def check(label, ok, detail=""):
        nonlocal failures
        if ok:
            print("PASS %-58s %s" % (label, str(detail)[:24]))
        else:
            print("FAIL %-58s %s" % (label, str(detail)[:60]))
            failures += 1

    def mutate(fn):
        rows = copy.deepcopy(base)
        fn(rows)
        return rows

    def row_for(rows, host, presence=None):
        for r in rows:
            if r["host_id"] == host and (presence is None
                                         or r["presence_state"] == presence):
                return r
        raise SystemExit("no covering row for %s" % host)

    # ── parity ───────────────────────────────────────────────────────────────
    check("the real patches reproduce the legacy columns",
          not covering_patches.check_parity(),
          covering_patches.check_parity()[:1] or "no problems")

    check("...and there is something to reproduce",
          len(covering_patches.resolved()) >= 5,
          "%d wall(s)" % len(covering_patches.resolved()))

    check("a THICKNESS that drifts from the legacy column is caught",
          any("thickness" in p for p in covering_patches.check_parity(
              mutate(lambda rows: row_for(rows, "MA").__setitem__(
                  "thickness_mm", "90")))), "thickness")

    check("a LOST band is caught",
          any("LOSE a band" in p for p in covering_patches.check_parity(
              [r for r in base if r["host_id"] != "R8"])), "lost")

    check("an ADDED band is caught",
          any("ADD a band" in p for p in covering_patches.check_parity(
              mutate(lambda rows: row_for(rows, "MA").update(
                  {"host_id": "G5"})))), "added")

    check("an EXTENT that drifts is caught",
          any("extent" in p for p in covering_patches.check_parity(
              mutate(lambda rows: row_for(rows, "M2", "present").__setitem__(
                  "along_to_mm", "800")))), "extent")

    # ⚠️ a band that quietly becomes full-face loses the partial extent entirely
    check("a partial band silently made FULL-FACE is caught",
          any("extent" in p for p in covering_patches.check_parity(
              mutate(lambda rows: row_for(rows, "M2", "present").__setitem__(
                  "along_to_mm", "2073.4")))), "full-face")

    check("the face decides the SIDE, so a wrong face is caught",
          any("side" in p or "extent" in p for p in covering_patches.check_parity(
              mutate(lambda rows: row_for(rows, "M6b").__setitem__(
                  "face_ref", "cross_lo")))), "side")

    # ── malformed records ────────────────────────────────────────────────────
    def raises(label, rows, needle):
        nonlocal failures
        try:
            covering_patches.resolved(rows)
            print("FAIL %-58s ACCEPTED it" % label)
            failures += 1
        except ValidationError as exc:
            ok = needle in str(exc)
            print("%s %-58s %s" % ("PASS" if ok else "FAIL", label,
                                   str(exc)[:30]))
            failures += 0 if ok else 1

    raises("a PRESENT band with no thickness is refused",
           mutate(lambda rows: row_for(rows, "MA").__setitem__("thickness_mm", "")),
           "has a depth")
    raises("a nan thickness is refused",
           mutate(lambda rows: row_for(rows, "MA").__setitem__("thickness_mm", "nan")),
           "has a depth")
    raises("a presence_state outside its vocabulary is refused",
           mutate(lambda rows: row_for(rows, "MA").__setitem__(
               "presence_state", "probably")),
           "not one of")
    raises("a reversed band is refused",
           mutate(lambda rows: row_for(rows, "MA").update(
               {"along_from_mm": "900", "along_to_mm": "100"})),
           "do not describe a band")

    # ⚠️ the legacy bridge cannot express two bands on one wall, and must SAY
    # so rather than reporting the first
    try:
        extra = copy.deepcopy(row_for(base, "MA"))
        extra["patch_uuid"] = "11111111-2222-3333-4444-555555555555"
        extra["along_from_mm"] = "0"
        extra["along_to_mm"] = "100"
        covering_patches.legacy_equivalent(base + [extra])
        check("a second band on one wall is refused by the bridge", False,
              "accepted")
    except ValidationError as exc:
        check("a second band on one wall is refused by the bridge",
              "must be retired" in str(exc), str(exc)[:30])

    # ── meaning: the reconciliation matrix ───────────────────────────────────
    from check_boundary_patches import (load_assertions, load_decisions,
                                        load_patches)
    bnd, ass, dec = load_patches(), load_assertions(), load_decisions()

    def verdicts(coverings=None, assertions=None):
        rows, problems = reconcile(coverings or covering_patches.active(),
                                   bnd, assertions or ass, dec)
        return {(r[0]["host_id"], r[0]["presence_state"]): r[2]
                for r in rows}, problems

    got, problems = verdicts()
    check("the real records reconcile with no structural problem",
          not problems, problems[:1] or "none")
    check("an evidenced band against a derived requirement is CONSISTENT",
          got.get(("MA", "present")) == CONSISTENT, got.get(("MA", "present")))
    check("MC's absent end cap against INS-PARTY-MASONRY is CONSISTENT",
          got.get(("MC", "absent")) == CONSISTENT, got.get(("MC", "absent")))

    # ⚠️⚠️ THE CASE THAT CAUSED THE CATEGORY ERROR. M2's abutting run has an
    # UNRESOLVED requirement and an OBSERVED absence. It must land in REVIEW -
    # and must NOT block, and must NOT overwrite the observed state.
    check("an unresolved requirement over an observed absence is REVIEW",
          got.get(("M2", "absent")) == REVIEW, got.get(("M2", "absent")))

    check("...and it does not make the reconciliation fail",
          not problems, "no structural problem")

    # present where the rule says not_required -> investigate
    flipped = copy.deepcopy(base)
    row_for(flipped, "MC", "absent")["presence_state"] = "present"
    row_for(flipped, "MC", "present")["thickness_mm"] = "70"
    got2, _p = verdicts([r for r in flipped
                         if (r.get("state") or "") == "active"])
    check("PRESENT where the rule says not_required is an ANOMALY",
          ANOMALY in got2.values(), sorted(set(got2.values())))

    # absent where the rule says required -> proposed work or defect
    stripped = copy.deepcopy(base)
    row_for(stripped, "MA")["presence_state"] = "absent"
    row_for(stripped, "MA")["thickness_mm"] = ""
    got3, _p = verdicts([r for r in stripped
                         if (r.get("state") or "") == "active"])
    check("ABSENT where the rule says required is PROPOSED_OR_DEFECT",
          got3.get(("MA", "absent")) == PROPOSED_OR_DEFECT,
          got3.get(("MA", "absent")))

    # ⚠️ a band built on a face nobody classified is a structural problem, not
    # a verdict - something exists where no boundary condition was ever stated
    orphan = copy.deepcopy(base)
    row_for(orphan, "MA")["face_ref"] = "cross_hi"
    _g, problems4 = verdicts([r for r in orphan
                              if (r.get("state") or "") == "active"])
    check("a band on a face NO boundary patch covers is caught",
          any("NO boundary patch" in p for p in problems4),
          problems4[:1] or "none")

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
