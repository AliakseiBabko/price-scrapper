#!/usr/bin/env python3
"""Guard the exchange IDS: each requirement must fail for ITS OWN reason.

⚠️⚠️ THE TWO FAILURES THIS EXISTS TO CATCH

1. `0 of 0`. A specification whose applicability matches nothing REPORTS
   SUCCESS. A suite of them reports total success while checking nothing, and
   the report is green, so nobody looks. Seeded below by running the suite
   against a model with no walls.

2. A SHARED CAUSE. Six specifications failing together might be six
   requirements, or one defect wearing six hats. So each failing requirement is
   satisfied ON ITS OWN in a copy of the model, and the suite must show exactly
   that one specification flipping to pass while the others stay put.

    .venv-ifc314\\Scripts\\python.exe scripts/ids_selftest.py
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "ifc"))

import ifcopenshell  # noqa: E402
import ifcopenshell.api  # noqa: E402

from check_ids import BASELINE_PATH, run  # noqa: E402

GENERATOR = os.path.join(REPO, "tools", "ifc", "model_from_resolved.py")


def build():
    out = os.path.join(tempfile.gettempdir(), "ids_selftest.ifc")
    man = os.path.join(tempfile.gettempdir(), "ids_selftest.json")
    proc = subprocess.run([sys.executable, GENERATOR, "--output", out,
                           "--manifest", man], capture_output=True, cwd=REPO)
    if proc.returncode != 0:
        raise SystemExit("build failed: %s"
                         % proc.stderr.decode("utf-8", "replace")[-300:])
    return out


def failing(model_path):
    rows, problems = run(model_path)
    return set(n for n, _a, f, _w in rows if f), problems


def save(model, tag):
    path = os.path.join(tempfile.gettempdir(), "ids_seed_%s.ifc" % tag)
    model.write(path)
    return path


def main() -> int:
    failures = 0

    def check(label, ok, detail=""):
        nonlocal failures
        if ok:
            print("PASS %-56s %s" % (label, detail[:30]))
        else:
            print("FAIL %-56s %s" % (label, detail[:66]))
            failures += 1

    base_path = build()
    base_failing, base_problems = failing(base_path)
    baseline = json.load(io.open(BASELINE_PATH, encoding="utf-8"))["failures"]

    check("no applicability problems on the real model", not base_problems,
          "; ".join(base_problems)[:60])
    check("today's failures match the recorded baseline",
          base_failing == set(baseline),
          "now %s vs baseline %s" % (sorted(base_failing), sorted(baseline)))
    check("the contract is not vacuously satisfied", len(base_failing) >= 5,
          "%d specifications failing" % len(base_failing))
    check("...and not uniformly failing either",
          len(base_failing) < 8,
          "%d of 8 pass today" % (8 - len(base_failing)))

    # ── ⚠️ THE `0 of 0` GUARD ────────────────────────────────────────────────
    model = ifcopenshell.open(base_path)
    for wall in model.by_type("IfcWall"):
        model.remove(wall)
    empty = save(model, "nowalls")
    _rows, problems = run(empty)
    hit = [p for p in problems if "MATCHED NOTHING" in p]
    check("a specification that matches NOTHING is refused", bool(hit),
          hit[0][:60] if hit else "no applicability problem raised")

    # ── each requirement satisfied ON ITS OWN ────────────────────────────────
    def seeded(tag, mutate):
        m = ifcopenshell.open(base_path)
        mutate(m)
        return failing(save(m, tag))[0]

    def set_object_type(cls, value):
        def go(m):
            for e in m.by_type(cls):
                e.ObjectType = value
        return go

    cases = [
        ("Walls carry a type designation",
         set_object_type("IfcWall", "WALL_GAS_SILICATE_250"), "walltype"),
        ("Doors carry a type designation",
         set_object_type("IfcDoor", "DOOR_D01"), "doortype"),
        ("Windows carry a type designation",
         set_object_type("IfcWindow", "WINDOW_W01"), "wintype"),
        ("No unclassified proxies",
         set_object_type("IfcBuildingElementProxy", "VENT_SHAFT"), "proxy"),
    ]

    def add_identity(m):
        for wall in m.by_type("IfcWall"):
            pset = ifcopenshell.api.run("pset.add_pset", m, product=wall,
                                        name="Pset_ApartmentIdentity")
            ifcopenshell.api.run("pset.edit_pset", m, pset=pset,
                                 properties={"CanonicalId": "seeded"})
    cases.append(("Walls expose their canonical identity", add_identity, "ident"))

    def add_material(m):
        material = ifcopenshell.api.run("material.add_material", m,
                                        name="Aerated block")
        for wall in m.by_type("IfcWall"):
            ifcopenshell.api.run("material.assign_material", m,
                                 products=[wall], material=material)
    cases.append(("Walls carry a material association", add_material, "mat"))

    for name, mutate, tag in cases:
        try:
            after = seeded(tag, mutate)
        except Exception as exc:                       # noqa: BLE001
            check("%s fails for its OWN reason" % name[:34], False,
                  "seed error: %s" % str(exc)[:40])
            continue
        flipped = name not in after
        others_held = (base_failing - {name}) == (after - {name})
        check("%s fails for its OWN reason" % name[:34],
              flipped and others_held,
              "flipped=%s others_unchanged=%s" % (flipped, others_held))

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
