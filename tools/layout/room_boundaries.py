#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Room boundaries — the thing this model did not have.

⚠️⚠️ WHY THIS EXISTS, AND WHAT IT UNBLOCKS
The compiler resolves WALLS. It has never resolved ROOMS, and that absence was
being felt in three unrelated places before anyone named it:

  * `model_from_resolved.py` emits **zero** `IfcSpace` - it has no room to emit.
    (⚠ NOT a regression: the 8 spaces in the 2026-09-16 artefacts came from
    `current_apartment_layout.py`, a different generator that built rooms as
    plain rectangles from a schedule. Nothing broke; the capability was never in
    this path.)
  * `wall_bed_envelope.py` had to REFUSE a "with block fixing" width because it
    could not clip a collinear wall run to the room the bed stands in.
  * `room_rollouts.csv` covers **1 of 7 rooms**, and развёртки are nine sheets of
    the target album.

⚠️ AUTHORED BOUNDS, COMPILED COORDINATES - the repo's standing pattern. A room
names the four wall FACES that bound it; this resolves them. No coordinate is
typed, so if the compiler moves a wall the room moves with it.

⚠️⚠️ CLOSURE IS CHECKED SEGMENT BY SEGMENT, NOT BY AREA. Each side must be fully
made of walls and openings the compiler actually resolves. `AGENTS.md` is
explicit that **areas are never evidence**, so the plan area is carried for
reference and never compared against - the linear chain is what has to close.

⚠️ A ROOM BOUNDARY RUNS THROUGH ITS OPENINGS. The 9.36 room's north side is G4d
for 1915.1 mm and then the doorway O6 for 910.0 mm. A checker that demanded solid
wall on every side would refuse every room in this flat.

⚠️ RECTANGLES ONLY, AND IT SAYS SO. Four bounding planes cannot express the
trapezoid лоджия or a room with a re-entrant corner. Such a room is REFUSED
rather than squared off - the same reason a rectangle cannot express the mitred
M2 and `build_variant.py` was retired for pretending otherwise.
"""

import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))
sys.path.insert(0, os.path.join(REPO, "tools", "drawings"))

from lib.tabular import read_csv, finite          # noqa: E402
import resolve_v0_geometry as R                   # noqa: E402
import wall_elevation as WE                       # noqa: E402

CANON = os.path.join(REPO, "data", "canonical")
BOUNDARIES = os.path.join(CANON, "room_boundaries.csv")

CLOSURE_MM = 0.5
FACE_KEYS = {"face_lo": "face_lo_mm", "face_hi": "face_hi_mm"}


class BoundaryError(Exception):
    pass


def resolve_ref(geom, ref):
    """'MA.face_hi' -> the coordinate of that wall's face.

    ⚠ Returns the WALL too, so a caller can say which element a bound came from.
    A bare number with no stated terminations is the rule-9 failure.
    """
    if "." not in ref:
        raise BoundaryError("bound %r is not WALL.face_lo / WALL.face_hi" % ref)
    wall_id, face = ref.rsplit(".", 1)
    if face not in FACE_KEYS:
        raise BoundaryError("bound %r names face %r; expected one of %s"
                            % (ref, face, ", ".join(sorted(FACE_KEYS))))
    w = geom.wall(wall_id)
    if w is None:
        raise BoundaryError("bound %r names wall %r, which the compiler does not "
                            "resolve" % (ref, wall_id))
    return w[FACE_KEYS[face]], w


def rooms():
    return read_csv(BOUNDARIES)


def boundary(geom, row):
    """Resolve one room, and verify each side is really made of walls."""
    rid = (row.get("room_id") or "").strip()
    south, w_s = resolve_ref(geom, (row.get("south_ref") or "").strip())
    north, w_n = resolve_ref(geom, (row.get("north_ref") or "").strip())
    west, w_w = resolve_ref(geom, (row.get("west_ref") or "").strip())
    east, w_e = resolve_ref(geom, (row.get("east_ref") or "").strip())

    if north - south <= CLOSURE_MM or east - west <= CLOSURE_MM:
        raise BoundaryError(
            "%s: bounds do not enclose anything - south %.1f north %.1f, "
            "west %.1f east %.1f. Check the face roles: for an EW wall face_lo/hi "
            "are Y, for a NS wall they are X." % (rid, south, north, west, east))

    sides = {}
    # ⚠ REUSE THE ELEVATION'S SEGMENT WALK rather than write a second one. It is
    # already guarded by 13 seeds and already knows that a face is rarely one
    # wall - the 9.36 room's south side is MA plus the END of R8, and R8 is
    # concrete where MA is block.
    for name, axis, coord, a, b in (
            ("south", "EW", south, west, east),
            ("north", "EW", north, west, east),
            ("west", "NS", west, south, north),
            ("east", "NS", east, south, north)):
        segs = WE.segments_along(geom, axis, coord, a, b)
        ops = WE.openings_along(geom, axis, coord, a, b)
        covered = sum(s["length_mm"] for s in segs)
        span = b - a
        # A boundary runs THROUGH its openings, so an opening counts as covered.
        op_len = 0.0
        for o in ops:
            lo, hi = max(o["x0"], a), min(o["x1"], b)
            if hi - lo > CLOSURE_MM:
                op_len += hi - lo
        if covered + 1e-6 < span - CLOSURE_MM:
            # openings sit INSIDE host walls, so they are already inside
            # `covered` when the host reaches this face; only a genuine gap
            # matters.
            if covered + op_len + CLOSURE_MM < span:
                raise BoundaryError(
                    "%s %s side: walls and openings cover %.1f of %.1f mm - a "
                    "%.1f mm gap that nothing the compiler resolves accounts for."
                    % (rid, name, covered + op_len, span, span - covered - op_len))
        sides[name] = {
            "coord_mm": coord,
            "span_mm": span,
            "elements": [s["wall_id"] for s in segs],
            "openings": [o["opening_id"] for o in ops],
        }

    polygon = [(west, south), (east, south), (east, north), (west, north)]
    return {
        "room_id": rid,
        "room_ru": (row.get("room_ru") or "").strip(),
        "bounds_mm": {"south": south, "north": north, "west": west, "east": east},
        "bounded_by": {"south": w_s["wall_id"], "north": w_n["wall_id"],
                       "west": w_w["wall_id"], "east": w_e["wall_id"]},
        "width_mm": east - west,
        "depth_mm": north - south,
        "polygon": polygon,
        "sides": sides,
        # ⚠ COMPUTED, REPORTED, AND NEVER COMPARED AGAINST. Areas are not
        # evidence; the linear chain is.
        "computed_area_m2": round((east - west) * (north - south) / 1e6, 3),
        "plan_area_m2": finite((row.get("plan_area_m2") or "nan")),
    }


def resolve_all(geom=None):
    geom = R.resolve() if geom is None else geom
    out, problems = {}, []
    for row in rooms():
        try:
            out[(row.get("room_id") or "").strip()] = boundary(geom, row)
        except BoundaryError as exc:
            problems.append(str(exc))
    return out, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    geom = R.resolve()
    built, problems = resolve_all(geom)

    if a.json:
        import json
        print(json.dumps(built, ensure_ascii=False, indent=2))
        return 1 if problems else 0

    for rid, b in sorted(built.items()):
        print("%-4s %-14s %7.1f x %7.1f mm   bounds S:%s N:%s W:%s E:%s"
              % (rid, b["room_ru"], b["width_mm"], b["depth_mm"],
                 b["bounded_by"]["south"], b["bounded_by"]["north"],
                 b["bounded_by"]["west"], b["bounded_by"]["east"]))
        for name in ("south", "north", "west", "east"):
            sd = b["sides"][name]
            bits = "+".join(sd["elements"]) or "-"
            ops = (" through " + "+".join(sd["openings"])) if sd["openings"] else ""
            print("      %-6s %7.1f mm = %s%s" % (name, sd["span_mm"], bits, ops))
        print("      area computed %.3f m2 vs plan %.3f - REPORTED, NOT CHECKED "
              "(areas are never evidence)"
              % (b["computed_area_m2"], b["plan_area_m2"]))
    for p in problems:
        print("  PROBLEM %s" % p)

    total = len(rooms())
    print("\n%d of %d authored room(s) resolved." % (len(built), total))
    print("⚠ The flat has 7 rooms plus the лоджия. Rooms not authored here simply "
          "DO NOT EXIST to the model - they are not defaulted to anything.")
    if problems:
        print("FAIL - %d room boundary problem(s)" % len(problems))
        return 1
    print("PASS - every authored room boundary closes on walls the compiler resolves")
    return 0


if __name__ == "__main__":
    sys.exit(main())
