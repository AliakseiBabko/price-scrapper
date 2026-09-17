#!/usr/bin/env python3
"""Seed the ways a two-variant comparison could stop being single-basis.

⚠️⚠️ THE DEFECT CLASS. `v0` was a retired schematic and `v1` is built on its own
shell, so every number in the old comparison mixed a LAYOUT decision with two
independent reconstructions of the same building. Rebuilding `v0` alone would
have repaired the visible half and left "single-basis" false - so the seeds here
aim at the invisible half: a shell that has quietly moved, a mitre that has been
squared, a shaft that has gone missing, and a partition that claims to be
retained when it is not.

⚠️ THE POSITIVE CONTROL IS SYNTHETIC. v1 cannot pass today - it has not been
rebased - so a guard that waited for a real passing pair would never run. The
control is v0 with one partition removed and one added, which is exactly what a
rebased variant will look like.

    .venv-ifc314\\Scripts\\python.exe scripts/variant_basis_selftest.py
"""
from __future__ import annotations

import copy
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))

from build_variant_spec import build, is_mitred, shell_signature  # noqa: E402
from check_variant_basis import (  # noqa: E402
    DEMOLISHED, NEW, RETAINED, area_comparable, basis_problems, classify, load)


def main() -> int:
    failures = 0

    def check(label, ok, detail=""):
        nonlocal failures
        if ok:
            print("PASS %-58s %s" % (label, str(detail)[:24]))
        else:
            print("FAIL %-58s %s" % (label, str(detail)[:64]))
            failures += 1

    v0 = build()

    # ── the compiled baseline meets the acceptance criteria ──────────────────
    counts = v0["counts"]
    check("v0 has 25 walls", counts["walls"] == 25, counts["walls"])
    check("v0 has 11 opening leaves in 10 units",
          (counts["opening_leaves"], counts["opening_units"]) == (11, 10),
          (counts["opening_leaves"], counts["opening_units"]))
    check("v0 has both ventilation shafts", counts["shafts"] == 2,
          counts["shafts"])
    check("v0 keeps the mitred walls mitred",
          counts["mitred_walls"] == ["M2", "M6b"], counts["mitred_walls"])
    check("v0 carries the diagonal loggia glazing",
          any(o["id"] == "O9" for o in v0["openings"])
          and counts["loggia_bays"] == 7, counts["loggia_bays"])
    check("v0 is not retired and is schema v2",
          "_retired" not in v0 and v0["schema_version"] == 2,
          v0["schema_version"])

    # ⚠️ and NOTHING in the dependency chain may be retired
    on_disk = load("v0-existing")
    check("the spec ON DISK is the compiled one, not the schematic",
          "_retired" not in on_disk and len(on_disk["walls"]) == 25,
          "%d walls" % len(on_disk["walls"]))

    # ── the positive control: a properly rebased proposal ────────────────────
    rebased = copy.deepcopy(v0)
    rebased["spec_id"] = "v1-rebased-SEED"
    partitions = [w for w in rebased["walls"] if not w["structural"]]
    demolished_id = partitions[0]["id"]
    rebased["walls"] = [w for w in rebased["walls"] if w["id"] != demolished_id]
    added = copy.deepcopy(partitions[1])
    added["id"] = "W_NEW_SEED"
    added["polygon_mm"] = [[x + 3000.0, y] for x, y in added["polygon_mm"]]
    rebased["walls"].append(added)

    problems = basis_problems(v0, rebased)
    check("a properly rebased proposal shares the basis", not problems,
          problems[:1] or "one basis")

    verdicts = classify(v0, rebased)
    states = dict((vid or bid, state) for state, vid, bid in verdicts)
    check("the removed partition is DEMOLISHED",
          states.get(demolished_id) == DEMOLISHED, states.get(demolished_id))
    check("the added partition is NEW", states.get("W_NEW_SEED") == NEW,
          states.get("W_NEW_SEED"))
    check("every other wall is RETAINED",
          sum(1 for s, _v, _b in verdicts if s == RETAINED) == len(v0["walls"]) - 1,
          sum(1 for s, _v, _b in verdicts if s == RETAINED))

    def refuses(label, mutate, needle):
        nonlocal failures
        proposal = copy.deepcopy(rebased)
        mutate(proposal)
        proposal["shell_signature"] = shell_signature(proposal)
        problems = basis_problems(v0, proposal)
        hit = any(needle in p for p in problems)
        if hit:
            print("PASS %-58s %s" % (label, problems[0][:24]))
        else:
            print("FAIL %-58s %s" % (label, problems[:1] or "ACCEPTED"))
            failures += 1

    # ⚠️⚠️ THE SHELL HAS MOVED. 50 mm is inside the BUILD tolerance and would
    # never look wrong on a drawing - but these are two compiled descriptions
    # of one building, not two measurements, so any movement at all means the
    # shells are not the same shell.
    def translate(proposal):
        for wall in proposal["walls"]:
            if wall["structural"]:
                wall["polygon_mm"] = [[x + 50.0, y]
                                      for x, y in wall["polygon_mm"]]
    refuses("a 50 mm SHELL TRANSLATION is caught", translate,
            "STRUCTURAL SHELLS differ")

    # ⚠️⚠️ THE MITRE SQUARED. This is what the old rectangle schema did
    # silently, and the лоджия's whole outline depends on it.
    def square_mitre(proposal):
        for wall in proposal["walls"]:
            if wall["id"] != "M2":
                continue
            xs = [p[0] for p in wall["polygon_mm"]]
            ys = [p[1] for p in wall["polygon_mm"]]
            wall["polygon_mm"] = [[min(xs), min(ys)], [max(xs), min(ys)],
                                  [max(xs), max(ys)], [min(xs), max(ys)]]
    refuses("a SQUARED MITRE on M2 is caught", square_mitre,
            "STRUCTURAL SHELLS differ")

    squared = copy.deepcopy(rebased)
    square_mitre(squared)
    check("...and the squared wall no longer reads as mitred",
          not is_mitred(next(w["polygon_mm"] for w in squared["walls"]
                             if w["id"] == "M2")), "squared")

    # ⚠️⚠️ A SHAFT HAS GONE MISSING. A shaft is immovable common property, so
    # its absence is never a layout choice.
    refuses("a MISSING ventilation shaft is caught",
            lambda p: p["shafts"].pop(), "STRUCTURAL SHELLS differ")

    # ── a partition that FALSELY claims to be retained ───────────────────────
    # ⚠️⚠️ THE QUESTION THE OLD TOOL COULD NOT ANSWER. v1's operations add
    # partitions with `phase: existing`, so a moved partition looked retained
    # and its demolition cost vanished. Classification is a RELATION to the
    # baseline, never a phase label carried in the file.
    liar = copy.deepcopy(rebased)
    victim = next(w for w in liar["walls"]
                  if not w["structural"] and w["id"] != "W_NEW_SEED")
    victim["phase"] = "existing"
    victim["polygon_mm"] = [[x, y + 400.0] for x, y in victim["polygon_mm"]]
    liar["shell_signature"] = shell_signature(liar)
    verdicts = classify(v0, liar)
    moved = [(s, v, b) for s, v, b in verdicts
             if v == victim["id"] or b == victim["id"]]
    states = set(s for s, _v, _b in moved)
    check("a MOVED partition claiming `phase: existing` is not RETAINED",
          states == {NEW, DEMOLISHED}, sorted(states))

    # ── room areas stay withdrawn ────────────────────────────────────────────
    ok, why = area_comparable(v0, rebased)
    check("room-area deltas stay WITHHELD while no method is stated",
          not ok, why[:40])
    ok, _why = area_comparable(dict(v0, area_method="compiler_polygon"),
                               dict(rebased, area_method="compiler_polygon"))
    check("...and become comparable only when BOTH state the same method", ok,
          "same method")
    ok, why = area_comparable(dict(v0, area_method="developer_published"),
                              dict(rebased, area_method="homestyler_cad"))
    check("...and two DIFFERENT methods stay withheld", not ok, why[:30])

    # ── a retired or legacy file anywhere in the chain ───────────────────────
    for label, mutate, needle in (
            ("a RETIRED spec anywhere is caught",
             lambda p: p.__setitem__("_retired", "seeded"), "RETIRED"),
            ("a schema v1 spec is caught",
             lambda p: p.__setitem__("schema_version", "0.1.0"), "schema v"),
            ("a spec with no coordinate frame is caught",
             lambda p: p.__setitem__("frame", {}), "no coordinate frame")):
        proposal = copy.deepcopy(rebased)
        mutate(proposal)
        problems = basis_problems(v0, proposal)
        hit = any(needle in p for p in problems)
        check(label, hit, problems[:1] or "ACCEPTED")

    # ⚠️ and classification must REFUSE rather than guess when the basis fails
    try:
        classify(v0, load("v1-homestyler"))
        check("classify REFUSES an unrebased variant", False, "it computed one")
    except ValueError as exc:
        check("classify REFUSES an unrebased variant", True, str(exc)[:24])

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
