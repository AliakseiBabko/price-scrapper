#!/usr/bin/env python3
"""Seed every way an acceptance could be honoured when it should have lapsed.

⚠️⚠️ THE DEFECT THIS GUARDS IS THAT THE RULE WAS PROSE. The acceptance record
said approval "lapses" if an artefact changes, and NOTHING read the file - so
an artefact could be regenerated while the record still said `accepted` and the
comparison sheet would go on looking decision-bearing. The hashes provided none
of the protection they were described as providing.

⚠️ The seeds drive `decision_bearing()` over INJECTED records, because the real
one is correctly `pending` today - a guard that could only be exercised by the
owner accepting first would be no guard at all.

    .venv-ifc314\\Scripts\\python.exe scripts/baseline_acceptance_selftest.py
"""
from __future__ import annotations

import copy
import io
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))

from check_baseline_acceptance import (  # noqa: E402
    REQUIRED_ARTEFACTS, SCOPES, VARIANT_SPECS, banner, blocked_topics,
    decision_bearing, load, sha256)


def main() -> int:
    failures = 0

    def check(label, ok, detail=""):
        nonlocal failures
        if ok:
            print("PASS %-58s %s" % (label, str(detail)[:26]))
        else:
            print("FAIL %-58s %s" % (label, str(detail)[:64]))
            failures += 1

    real = load()

    # ── the real record is correctly PENDING ─────────────────────────────────
    ok, reasons = decision_bearing(real)
    check("the real record is NOT decision-bearing today", not ok,
          "%d reason(s)" % len(reasons))
    check("...and it says so in a banner a consumer can print",
          banner(real) is not None, banner(real))

    # ⚠️ AN ACCEPTED RECORD MUST ACTUALLY PASS, or every seed below is
    # vacuously green and the gate is just a refusal.
    accepted = copy.deepcopy(real)
    accepted["status"] = "accepted"
    for name in SCOPES:
        accepted["scopes"][name] = {"state": "accepted",
                                    "accepted_on": "2026-09-17", "notes": ""}
    # ⚠ The positive control must ISOLATE the retired-spec finding, or it
    # would report the gate broken when the gate is right. It injects a spec
    # path that is not retired; the retired one is asserted separately below.
    import json as _json
    import tempfile as _tmp
    live_dir = _tmp.mkdtemp()
    live_spec = os.path.join(live_dir, "spec.json")
    io.open(live_spec, "w", encoding="utf-8").write(_json.dumps({"walls": []}))
    LIVE = (os.path.relpath(live_spec, REPO),)

    ok, reasons = decision_bearing(accepted, LIVE)
    check("a fully accepted record IS decision-bearing", ok, reasons[:1] or "clean")
    check("...and its banner is empty",
          banner(accepted, LIVE) is None, "no banner")

    def refuses(label, mutate, needle):
        nonlocal failures
        record = copy.deepcopy(accepted)
        mutate(record)
        ok, reasons = decision_bearing(record, LIVE)
        hit = (not ok) and any(needle in r for r in reasons)
        if hit:
            print("PASS %-58s %s" % (label, reasons[0][:26]))
        else:
            print("FAIL %-58s ok=%s %s" % (label, ok, reasons[:1]))
            failures += 1

    # ── the hash lapse, which is the whole point ─────────────────────────────
    refuses("an artefact CHANGED since acceptance is caught",
            lambda r: r["artefacts"].__setitem__(
                sorted(r["artefacts"])[0], "0" * 64), "has CHANGED")

    # ⚠️ every pinned artefact, not just the first - a loop that checked one
    # would look identical on a passing run
    for index in range(len(real.get("artefacts") or {})):
        refuses("...for pinned artefact %d as well" % index,
                lambda r, i=index: r["artefacts"].__setitem__(
                    sorted(r["artefacts"])[i], "1" * 64), "has CHANGED")

    refuses("a pinned artefact that no longer exists is caught",
            lambda r: r["artefacts"].update({"data/canonical/gone.json": "x" * 64}),
            "does not exist")

    refuses("a record pinning NO artefacts is caught",
            lambda r: r.__setitem__("artefacts", {}), "does not pin")

    # ── status and scopes ────────────────────────────────────────────────────
    refuses("a record that is not `accepted` is caught",
            lambda r: r.__setitem__("status", "pending_owner_review"),
            "status is")

    for name in SCOPES:
        refuses("one scope left pending is caught (%s)" % name[:22],
                lambda r, n=name: r["scopes"][n].__setitem__("state", "pending"),
                "scope %s" % name)

    # ⚠️ A SCOPE THAT IS ABSENT HAS NOT BEEN ACCEPTED, IT HAS BEEN FORGOTTEN -
    # and deleting a key is how a scope would quietly stop being asked about.
    refuses("a scope DELETED from the record is caught",
            lambda r: r["scopes"].pop(SCOPES[0]), "has no scope")

    # ── acceptance never means as-built ──────────────────────────────────────
    refuses("a record claiming field_verified is caught",
            lambda r: r.__setitem__("field_verified", True), "cannot confer")
    refuses("provenance other than `planned` is caught",
            lambda r: r.__setitem__("provenance", "as_built"), "provenance is")

    # ⚠️⚠️ THE ARTEFACT SET IS EXACT. Removing one pin from an otherwise
    # accepted record returned `(True, [])` - the loop only checked what was
    # still listed, so dropping an artefact silently removed it from the scope
    # of the approval. A pin you can shrink is not a pin. Each one separately.
    for relative in REQUIRED_ARTEFACTS:
        refuses("dropping the pin on %-28s is caught" % os.path.basename(relative),
                lambda r, a=relative: r["artefacts"].pop(a), "does not pin")

    refuses("pinning something OUTSIDE the required set is caught",
            lambda r: r["artefacts"].update({"README.md": "0" * 64}),
            "not in the required set")

    # ⚠️ THE REVIEW SHEET IS ONE OF THEM, because it defines what the scopes
    # MEAN - above all that the shaft scopes do not settle V1.
    check("the review sheet is a pinned artefact",
          "00_Master/V0_Baseline_Review_Sheet.md" in REQUIRED_ARTEFACTS,
          "pinned")

    # ⚠️⚠️ ACCEPTANCE MUST UNBLOCK WHAT IT CLAIMS TO. The comparison reads the
    # VARIANT SPEC, not the DXF, and today that spec is a retired schematic -
    # 18 walls against 25, no shafts, a rectangular loggia. An acceptance that
    # unblocked a sheet built from it would be worse than no acceptance.
    # ⚠⚠ THE RETIRED SPEC IS INJECTED, NOT BORROWED. This seed asserted that
    # the REAL v0 spec was retired - and it was, until the compiler-backed
    # rebuild on 2026-09-17 fixed exactly that. The seed then failed while the
    # repair was correct. A guard must carry its own defect.
    retired_path = os.path.join(live_dir, "retired.json")
    io.open(retired_path, "w", encoding="utf-8").write(
        _json.dumps({"_retired": "seeded", "walls": []}))
    RETIRED = (os.path.relpath(retired_path, REPO),)
    ok, reasons = decision_bearing(accepted, RETIRED)
    check("a RETIRED variant spec keeps the baseline provisional",
          (not ok) and any("RETIRED" in r for r in reasons),
          [r for r in reasons if "RETIRED" in r][:1] or reasons[:1])

    # ⚠ ...and the REAL spec is no longer one, which is the repair recorded
    real_specs_ok, real_reasons = decision_bearing(accepted, VARIANT_SPECS)
    check("the real v0 spec is no longer retired",
          not any("RETIRED" in r for r in real_reasons),
          [r for r in real_reasons if "RETIRED" in r][:1] or "compiled")

    check("...and the spec it checks is the one the comparison loads",
          VARIANT_SPECS == ("data/outputs/variants/v0-existing/spec.json",),
          VARIANT_SPECS)

    # ⚠️ V1 STAYS BLOCKED whatever the overall state says.
    topics = blocked_topics(real)
    check("V1's footprint is a blocked topic in its own right",
          any("v1_footprint" in t for t in topics), topics[:1] or "none")
    check("...and it is a scope of its own, not swept into `the shafts`",
          "ventilation_shaft_v1_footprint" in SCOPES
          and "ventilation_shafts_v1_v2" not in SCOPES, "split")

    # ⚠️ and the hashes in the committed record must be the REAL ones, or the
    # pin is against bytes that never existed
    stale = []
    for relative, pinned in sorted((real.get("artefacts") or {}).items()):
        path = os.path.join(REPO, relative)
        if os.path.exists(path) and sha256(path) != pinned:
            stale.append(relative)
    check("the committed record pins the CURRENT bytes", not stale,
          ", ".join(stale) if stale else "all three match")

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
