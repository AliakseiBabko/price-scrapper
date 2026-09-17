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
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))

from check_baseline_acceptance import (  # noqa: E402
    SCOPES, banner, decision_bearing, load, sha256)


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
    ok, reasons = decision_bearing(accepted)
    check("a fully accepted record IS decision-bearing", ok, reasons[:1] or "clean")
    check("...and its banner is empty", banner(accepted) is None, "no banner")

    def refuses(label, mutate, needle):
        nonlocal failures
        record = copy.deepcopy(accepted)
        mutate(record)
        ok, reasons = decision_bearing(record)
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
            lambda r: r.__setitem__("artefacts", {}), "NO artefacts")

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
