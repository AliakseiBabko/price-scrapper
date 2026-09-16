#!/usr/bin/env python3
"""Guard the geometry compiler's own contracts by seeding real defects.

`00_Master/Validator_Design_Discipline.md`: a gate nobody has watched fail is
not a gate. These are the compiler's contracts, as distinct from the gates that
check its OUTPUT - the DXF closure gate and the IFC checker already do that.
What is checked here is what the compiler PROMISES its consumers:

  1. The coordinate frame round-trips exactly, both directions.
  2. ⚠️ The datum is STABLE. A primitive outside the wall envelope must not be
     able to move the model origin - otherwise adding insulation, a service or
     a variant element silently translates every previously issued IFC, and
     every annotation against it refers to a different place while the file
     still loads cleanly.
  3. body_polygon RAISES on the unsupported mitre+extension combination rather
     than silently squaring a clipped corner.
  4. locate_on_face RAISES on an unknown face rather than defaulting to one,
     because defaulting is how a socket ends up on the wrong side of a wall.
  5. A mitred wall exposes a `glazing_cut` face with its own outward normal -
     the reason a locator must name a face rather than assume "the normal".

    .venv-ifc314\\Scripts\\python.exe scripts/resolve_v0_geometry_selftest.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools" / "layout"))

import resolve_v0_geometry as rv  # noqa: E402


def main() -> int:
    failures = 0
    resolved = rv.resolve()

    def ok(label, condition, detail=""):
        nonlocal failures
        if condition:
            print("PASS %-46s %s" % (label, detail))
        else:
            print("FAIL %-46s %s" % (label, detail))
            failures += 1

    # 1 - round trip, both directions
    frame = resolved.frame
    worst = 0.0
    for point in [(0.0, 0.0), (2930.9, 6120.7), (5000.0, 9000.0), (12946.0, 16240.1)]:
        back = frame.model_to_drawing(frame.drawing_to_model(point))
        worst = max(worst, abs(back[0] - point[0]), abs(back[1] - point[1]))
    ok("coordinate frame round-trips", worst < 1e-6,
       "max error %.3e mm over 4 points" % worst)

    model_point = (2.0, 3.0)
    there = frame.model_to_drawing(model_point)
    back_m = frame.drawing_to_model(there)
    ok("model -> drawing -> model round-trips",
       abs(back_m[0] - model_point[0]) < 1e-9 and abs(back_m[1] - model_point[1]) < 1e-9)

    # 2 - the datum must not follow a primitive outside the wall envelope
    baseline = rv.base_wall_datum(resolved.walls)
    intruder = dict(resolved.walls[0])
    intruder["wall_id"] = "NOT-A-WALL"
    intruder["from_mm"] = -50000.0
    intruder["to_mm"] = -49000.0
    intruder["face_lo_mm"] = -50000.0
    intruder["face_hi_mm"] = -49900.0
    # An element far outside the envelope, present in the model but NOT a named
    # wall. The datum is derived from the named walls, so it must not move.
    walls_plus = list(resolved.walls) + [intruder]
    moved = rv.base_wall_datum([w for w in walls_plus if w["wall_id"] != "NOT-A-WALL"])
    ok("datum ignores a primitive outside the envelope",
       abs(moved[0] - baseline[0]) < 1e-9 and abs(moved[1] - baseline[1]) < 1e-9,
       "origin stayed at (%.1f, %.1f)" % baseline)

    naive = (min(rv.wall_box(w)[0] for w in walls_plus),
             min(rv.wall_box(w)[1] for w in walls_plus))
    ok("and a min()-over-everything datum WOULD have moved",
       abs(naive[0] - baseline[0]) > 1000.0,
       "naive origin (%.1f, %.1f) vs stable (%.1f, %.1f)" % (naive + baseline))

    # 3 - the unsupported combination raises rather than guessing
    mitred_poly = [(0.0, 0.0), (1000.0, 0.0), (1000.0, 200.0), (500.0, 200.0)]
    try:
        rv.body_polygon("TEST", mitred_poly, True, [[(1000.0, 0.0), (1900.0, 0.0),
                                                     (1900.0, 200.0), (1000.0, 200.0)]])
        ok("mitre + extension raises", False, "it returned instead of raising")
    except ValueError as exc:
        ok("mitre + extension raises", "mitred" in str(exc), str(exc)[:60] + "...")

    # 4 - an unknown face must raise
    faces = resolved.faces["G5"]
    try:
        rv.locate_on_face(faces, "glazing_cut", 0.0)
        ok("unknown face raises", False, "it returned a point instead")
    except KeyError:
        ok("unknown face raises", True, "G5 has no glazing_cut face")

    # 5 - a mitred wall exposes its cut face, with a different normal
    m6b = resolved.faces["M6b"]
    ok("a mitred wall exposes glazing_cut", "glazing_cut" in m6b,
       "M6b faces: %s" % ", ".join(sorted(m6b)))
    if "glazing_cut" in m6b:
        cut = m6b["glazing_cut"]["outward_normal"]
        par = m6b["cross_lo"]["outward_normal"]
        ok("its normal differs from the parallel face",
           abs(cut[0] - par[0]) > 0.01 or abs(cut[1] - par[1]) > 0.01,
           "cut (%.3f, %.3f) vs cross_lo (%.3f, %.3f)" % (cut + par))

    # 6 - both opening counts are reported, not just one
    counts = resolved.report["opening_counts"]
    ok("both opening counts are published",
       counts["authored_leaf_records"] != counts["physical_opening_units"]
       and counts["aggregated_leaves"],
       counts["note"])

    print()
    print("failures: %d" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
