#!/usr/bin/env python3
"""Seed the ways the existing-state covering record could stop being true.

⚠️⚠️ WHAT THIS LAYER IS FOR. `wall_covering_patches.csv` says what the developer
ACTUALLY BUILT, per face and per extent. The boundary table says what SHOULD be
there. Keeping them apart is the whole design, so the seeds come in two groups:

  CUTOVER     the four wall-wide columns are RETIRED, and neither the file
              header nor any consumer may bring them back. The cutover was done
              as a parity build - identical bands, identical IFC - so a later
              difference can only come from the data, never from the move.
  MEANING     presence against requirement must land in the right cell, and an
              UNRESOLVED requirement must never overwrite an observed presence.

    .venv-ifc314\\Scripts\\python.exe scripts/covering_patches_selftest.py
"""
from __future__ import annotations

import copy
import io
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))

import covering_patches  # noqa: E402
from check_covering_reconciliation import (  # noqa: E402
    ANOMALY, CONSISTENT, PROPOSED_OR_DEFECT, REVIEW, issued_problems,
    reconcile)
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

    # ⚠️⚠️ THE RETIRED HEADERS MUST NOT COME BACK. `insulation_mm`,
    # `insulation_side`, `insulation_from_mm` and `insulation_to_mm` were
    # removed from wall_blocks.csv on 2026-09-17 once the covering patches
    # reproduced them exactly. Re-adding any of them would recreate the
    # split-brain the patches exist to close - two records of one fact, read
    # differently by the drawing and the model - and it would do so silently,
    # because nothing would be wrong with the file itself.
    import csv as _csv
    BLOCKS = os.path.join(REPO, "data", "canonical", "wall_blocks.csv")
    RETIRED = ("insulation_mm", "insulation_side", "insulation_from_mm",
               "insulation_to_mm")
    header = _csv.DictReader(io.open(BLOCKS, encoding="utf-8")).fieldnames or []
    back = [c for c in RETIRED if c in header]
    check("the retired insulation columns have not come back", not back,
          "found again: %s" % ", ".join(back) if back else "none of the four")

    # ⚠️ and the check must be able to see them - a name typo would make it
    # vacuous, so assert the header is the one we think it is
    check("...and the header being read is the real one",
          "wall_id" in header and "thickness_mm" in header,
          "%d column(s)" % len(header))

    # ⚠️ nor may any consumer read them again
    offenders = []
    for folder in ("tools", "scripts"):
        for root, _dirs, files in os.walk(os.path.join(REPO, folder)):
            for name in files:
                if not name.endswith(".py"):
                    continue
                path = os.path.join(root, name)
                if os.path.abspath(path) == os.path.abspath(__file__):
                    continue
                body = io.open(path, encoding="utf-8").read()
                for column in RETIRED:
                    if ('"%s"' % column) in body or ("'%s'" % column) in body:
                        offenders.append("%s reads %s" % (name, column))
    check("no consumer reads a retired column", not offenders,
          "; ".join(offenders[:2]) if offenders else "none")

    check("there is something to reproduce",
          len(covering_patches.resolved()) >= 5,
          "%d wall(s)" % len(covering_patches.resolved()))

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
        covering_patches.resolved_bands(base + [extra])
        check("a second band on one wall is refused by the bridge", False,
              "accepted")
    except ValidationError as exc:
        check("a second band on one wall is refused by the bridge",
              "must be retired" in str(exc), str(exc)[:30])

    # ⚠⚠ THE STRICT-CSV SHAPE, seeded over the real file. These moved here
    # from types_materials_selftest.py when the wall-wide columns retired:
    # DictReader drops a stray cell and turns a missing one into None, and
    # float("nan") parses and then defeats every comparison it reaches.
    import tempfile

    def with_line(extra):
        raw = io.open(covering_patches.PATCHES, encoding="utf-8").read()
        lines = raw.rstrip(chr(10)).split(chr(10))
        handle, path = tempfile.mkstemp(suffix=".csv")
        os.close(handle)
        io.open(path, "w", encoding="utf-8", newline="").write(
            chr(10).join(lines[:2] + [extra] + lines[2:]) + chr(10))
        return path

    for label, line in (
            ("a STRAY extra cell is refused", "SEED," * 30 + "SEED"),
            ("a MISSING cell is refused", "SEED,SEED")):
        path = with_line(line)
        try:
            covering_patches.load(path)
            check(label, False, "ACCEPTED it")
        except ValidationError as exc:
            check(label, True, str(exc)[:24])
        finally:
            os.unlink(path)

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

    # ⚠⚠ THE ISSUED BOUNDARY. "review_required blocks nothing" is true only
    # of REPRESENTING the existing state. It must block an issued quantity or a
    # proposed-work decision that depends on that band, and the only way past
    # is a RECORDED DISPOSITION - a person, a date and a reason. Changing a
    # rule until the verdict disappears is not a disposition.
    issued_rows, _p = reconcile(covering_patches.active(), bnd, ass, dec)
    open_rows = [r for r in issued_rows if r[2] != CONSISTENT]
    check("there IS a non-consistent band, so the guard is not vacuous",
          open_rows, "%d row(s)" % len(open_rows))

    check("an undisposed review_required BLOCKS issue",
          any("NO recorded disposition" in p
              for p in issued_problems(issued_rows, {})), "blocked")

    check("...while consistent bands alone do not block issue",
          not issued_problems([r for r in issued_rows if r[2] == CONSISTENT], {}),
          "clear")

    pid = open_rows[0][0]["patch_uuid"]
    full = {pid: {"patch_uuid": pid, "verdict": open_rows[0][2],
                  "disposition": "accept_as_existing", "rationale": "seed",
                  "decided_by": "seed", "decided_on": "2026-09-17"}}
    check("a complete disposition releases it",
          not issued_problems(issued_rows, full), "released")

    stale = {pid: dict(full[pid], verdict="consistent")}
    check("a disposition recorded against a DIFFERENT verdict is caught",
          any("situation has changed" in p
              for p in issued_problems(issued_rows, stale)), "stale")

    for column in ("disposition", "rationale", "decided_by", "decided_on"):
        gap = {pid: dict(full[pid], **{column: ""})}
        check("a disposition with no %-11s is caught" % column,
              any("is not one" in p for p in issued_problems(issued_rows, gap)),
              "unattributed")

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
