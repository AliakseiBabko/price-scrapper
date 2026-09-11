#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove the variant-comparison checks still fail, and still pass, for their own reasons.

Why this exists
---------------
`compare_variants.py` is the sheet the layout decision gets read off, and on
2026-09-11 it was found asserting two things it had not measured:

  1. `daylight.third_room_costs_a_window` reported, for `v1-homestyler`,
     "no window: Kids Room, Living and Dining Room, Kitchen, Bedroom small" -
     four rooms including the kitchen and the living room. The cause was that
     v1 ships `space_boundaries == {}`, so `rooms_touching()` returned nothing
     for every wall and NO room could be found lit. **The check answered with
     total confidence off no input at all.**

  2. `walls_demolished` / `walls_new` printed `0 / 0` for both variants. No wall
     in either spec carries a phase other than "existing" - cap2 is unbuilt - so
     0 was not a measurement, it was the absence of one, printed beside figures
     that are real. `Validator_Design_Discipline.md`, "printing is not checking",
     3 recurrences.

The fix makes the daylight rule report `ok=None` (not evaluable) when an unmapped
window could account for a room it would otherwise call dark, and makes the phase
counts `None` with an explicit `phase_modelled` flag.

**A fix that turns a false failure into "not evaluable" is one step away from a
check that can never fail again.** That is what these seeds are for: each one
breaks the subject on purpose and asserts the tool reacts the way it names.

The seeds
---------
  A  v1 + a space_boundaries entry for its windows  -> check becomes EVALUABLE
     (guards against the not-evaluable branch swallowing every input)
  B  v0 - one window, boundaries intact             -> ok=False, names the room
     (guards against the false branch being unreachable)
  C  v0 with a window whose host wall is unmapped   -> ok=None
     (the defect itself, on a spec that otherwise works)
  D  v0 with one wall marked phase=new              -> phase_modelled True, counts appear
     (guards against the phase branch being stuck at "not modelled")
  E  v0 untouched                                    -> ok=True, all rooms lit
     (guards against the whole check having been broken by the fix)

Usage
-----
    py -3 scripts/compare_variants_selftest.py
"""
from __future__ import print_function

import copy
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools" / "layout"))

import compare_variants as cv  # noqa: E402

SPECS = REPO / "data" / "outputs" / "variants"
DAYLIGHT = "daylight.third_room_costs_a_window"


def load(variant_id):
    return json.loads((SPECS / variant_id / "spec.json").read_text(encoding="utf-8"))


def daylight_of(spec, rules):
    for c in cv.check_rules(spec, rules):
        if c["rule"] == DAYLIGHT:
            return c
    return None


def main():
    rules = cv.load_rules()
    if DAYLIGHT not in rules:
        print("FAIL  %s is not in rules.jsonl - the seeds below test nothing" % DAYLIGHT)
        return 1

    failures = []

    def check(name, condition, detail):
        print("%-5s %-46s %s" % ("PASS" if condition else "FAIL", name, detail))
        if not condition:
            failures.append(name)

    # ---- E: the working case must still work -----------------------------
    v0 = load("v0-existing")
    got = daylight_of(v0, rules)
    check("E untouched v0 stays evaluable and lit",
          got is not None and got["ok"] is True,
          "ok=%s %s" % (got and got["ok"], (got or {}).get("detail", "")[:60]))

    # ---- C: the real defect, reproduced on a spec that otherwise works ----
    seeded = copy.deepcopy(v0)
    windows = [o for o in seeded["openings"] if o["kind"] == "window"]
    if not windows:
        print("FAIL  v0-existing has no window to seed with")
        return 1
    seeded["space_boundaries"] = {}
    got = daylight_of(seeded, rules)
    check("C unmapped windows -> not evaluable",
          got is not None and got["ok"] is None and "not evaluable" in got["detail"],
          "ok=%s %s" % (got and got["ok"], (got or {}).get("detail", "")[:60]))

    # ---- B: a genuinely dark room must still FAIL ------------------------
    seeded = copy.deepcopy(v0)
    boundaries = seeded.get("space_boundaries") or {}
    # Drop every window whose host wall IS mapped, so the remaining evidence is
    # complete and the darkness is real rather than unknown.
    seeded["openings"] = [o for o in seeded["openings"]
                          if not (o["kind"] == "window" and boundaries.get(o["host_wall"]))]
    got = daylight_of(seeded, rules)
    check("B real darkness still fails and names rooms",
          got is not None and got["ok"] is False and "no window:" in got["detail"],
          "ok=%s %s" % (got and got["ok"], (got or {}).get("detail", "")[:60]))

    # ---- A: mapping the windows must make v1 evaluable again -------------
    v1 = load("v1-homestyler")
    got_before = daylight_of(v1, rules)
    check("A1 v1 as shipped is not evaluable",
          got_before is not None and got_before["ok"] is None,
          "ok=%s %s" % (got_before and got_before["ok"], (got_before or {}).get("detail", "")[:60]))

    seeded = copy.deepcopy(v1)
    room_names = [r["name"] for r in seeded["rooms"] if r.get("role") in cv.HABITABLE]
    seeded["space_boundaries"] = {
        o["host_wall"]: room_names[:1]
        for o in seeded["openings"] if o["kind"] == "window"
    }
    got = daylight_of(seeded, rules)
    check("A2 mapped windows -> evaluable again",
          got is not None and got["ok"] is not None,
          "ok=%s %s" % (got and got["ok"], (got or {}).get("detail", "")[:60]))

    # ---- D: phase must appear the moment any wall carries one ------------
    # .get() rather than [] on purpose: against the pre-fix tool this seed raised
    # KeyError, which is an ACCIDENTAL rejection - the suite went red because the
    # code crashed, not because the property it names was violated.
    # Validator_Design_Discipline: "every negative case must fail for the reason
    # it names". Caught by running this selftest against the reverted tool.
    m = cv.metrics(v0)
    check("D1 unphased spec reports phase not modelled",
          m.get("phase_modelled") is False and m.get("walls_new", 0) is None
          and m.get("walls_demolished", 0) is None,
          "phase_modelled=%s new=%s demolished=%s"
          % (m.get("phase_modelled"), m.get("walls_new", "<absent>"),
             m.get("walls_demolished", "<absent>")))

    seeded = copy.deepcopy(v0)
    seeded["walls"][0]["phase"] = "new"
    seeded["walls"][1]["phase"] = "demolished"
    m = cv.metrics(seeded)
    check("D2 one phased wall -> counts appear",
          m.get("phase_modelled") is True and m.get("walls_new") == 1
          and m.get("walls_demolished") == 1,
          "phase_modelled=%s new=%s demolished=%s"
          % (m.get("phase_modelled"), m.get("walls_new", "<absent>"),
             m.get("walls_demolished", "<absent>")))

    print()
    print("failures: %d" % len(failures))
    if failures:
        for f in failures:
            print("  -", f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
