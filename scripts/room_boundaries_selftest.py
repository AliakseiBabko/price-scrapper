#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Guards `tools/layout/room_boundaries.py`.

⚠️⚠️ THE FAILURE THIS MUST PREVENT IS A ROOM THAT LOOKS RIGHT.
A room is four numbers. Four numbers can always be drawn as a rectangle, and the
rectangle will look like a room whether or not any wall actually bounds it. So
the seeds are about refusing a plausible box:

  * a bound naming a wall the compiler does not resolve
  * a bound naming a face that does not exist
  * bounds that enclose nothing, or are inside out
  * a side with a real gap in it

⚠️ AND ONE ABOUT AREA. `AGENTS.md`: areas are never evidence. The 9.36 room
computes to 9.605 m² against a plan figure of 9.360, and that discrepancy must
NOT make the room fail - the linear chain is what closes, and a checker that
rejected on area would be using the one thing the repo forbids as evidence.
"""

import copy
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))
sys.path.insert(0, os.path.join(REPO, "tools", "drawings"))

import resolve_v0_geometry as R                  # noqa: E402
import room_boundaries as RB                     # noqa: E402

PASS, FAIL = [], []


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", name,
                        ("  -- " + str(detail)) if detail and not cond else ""))


def rejects(name, geom, row, expect):
    try:
        RB.boundary(geom, row)
    except RB.BoundaryError as exc:
        ok(name, expect.lower() in str(exc).lower(), "wrong reason: %s" % exc)
        return
    except Exception as exc:                      # noqa: BLE001
        ok(name, False, "raised %s not BoundaryError: %s" % (type(exc).__name__, exc))
        return
    ok(name, False, "ACCEPTED a boundary it must refuse")


def main():
    geom = R.resolve()
    rows = RB.rooms()
    ok("0  there is at least one authored room", len(rows) >= 1)
    real = rows[0]

    # --- 1. THE REAL ROOM MUST RESOLVE, or every seed is vacuous -------------
    b = RB.boundary(geom, real)
    ok("1  the 9.36 room resolves", b["room_id"] == "SM", b["room_id"])
    ok("1a it is 2825.1 x 3400.0", abs(b["width_mm"] - 2825.1) < 0.5
       and abs(b["depth_mm"] - 3400.0) < 0.5,
       (b["width_mm"], b["depth_mm"]))
    ok("1b its south side is MA PLUS the end of R8 - a face is rarely one wall",
       b["sides"]["south"]["elements"] == ["MA", "R8"],
       b["sides"]["south"]["elements"])
    ok("1c its north side closes THROUGH the doorway O6",
       "O6" in b["sides"]["north"]["openings"], b["sides"]["north"])

    # --- 2. AREA MUST NOT BE USED AS EVIDENCE --------------------------------
    # 9.605 computed against a 9.360 plan figure. If a future version starts
    # failing on that, it has adopted the one thing AGENTS.md forbids.
    ok("2  the room passes DESPITE computed area != plan area",
       abs(b["computed_area_m2"] - b["plan_area_m2"]) > 0.2,
       (b["computed_area_m2"], b["plan_area_m2"]))

    # --- 3. A BOUND NAMING A WALL THAT DOES NOT EXIST ------------------------
    bad = copy.deepcopy(real); bad["south_ref"] = "NOPE.face_hi"
    rejects("3  a bound naming an unresolved wall is refused", geom, bad,
            "does not resolve")

    # --- 4. A BOUND NAMING A FACE THAT DOES NOT EXIST ------------------------
    bad = copy.deepcopy(real); bad["south_ref"] = "MA.face_middle"
    rejects("4  a bound naming a nonexistent face is refused", geom, bad,
            "expected one of")

    # --- 5. MALFORMED REFERENCE ----------------------------------------------
    bad = copy.deepcopy(real); bad["south_ref"] = "MA"
    rejects("5  a malformed bound reference is refused", geom, bad,
            "not WALL.face")

    # --- 6. BOUNDS THAT ENCLOSE NOTHING --------------------------------------
    # south and north swapped: an inside-out room, which would otherwise draw
    # perfectly happily as a rectangle with a negative depth.
    bad = copy.deepcopy(real)
    bad["south_ref"], bad["north_ref"] = real["north_ref"], real["south_ref"]
    rejects("6  an inside-out room is refused", geom, bad, "do not enclose")

    # --- 7. A SIDE WITH A REAL GAP -------------------------------------------
    # Push the east bound out past G8 onto a plane nothing reaches.
    bad = copy.deepcopy(real); bad["east_ref"] = "R4.face_hi"
    rejects("7  a side with a gap no wall accounts for is refused", geom, bad,
            "gap")

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
