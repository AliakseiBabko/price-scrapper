#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Guards `tools/drawings/wall_elevation.py`.

⚠️⚠️ THE FIRST CLOSURE CHECK IN THAT TOOL COULD NOT FAIL. It summed the gaps
between successive marks and compared the total to the span - a TELESCOPING sum,
equal to the span for any marks whatever. It would have reported a closed chain
on every possible input, including a broken one. That is the exact class
`Validator_Design_Discipline.md` names: a seed that cannot fail is worse than no
seed, because it buys confidence without providing any.

So this file exists to WATCH each check fail. Seed 1 asserts the real face
passes - without it every other seed could be vacuously green, which is the
same defect one level up.
"""

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))
sys.path.insert(0, os.path.join(REPO, "tools", "drawings"))

import resolve_v0_geometry as R          # noqa: E402
import wall_elevation as WE              # noqa: E402

PASS, FAIL = [], []


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", name,
                        ("  -- " + detail) if detail and not cond else ""))


def rejects(name, fn, expect):
    """The tool must REFUSE, and refuse for the stated reason."""
    try:
        fn()
    except WE.ClosureError as exc:
        got = str(exc)
        ok(name, expect.lower() in got.lower(),
           "refused, but for the wrong reason: %s" % got)
        return
    except Exception as exc:                       # noqa: BLE001
        ok(name, False, "raised %s, not ClosureError: %s" % (type(exc).__name__, exc))
        return
    ok(name, False, "ACCEPTED a defect it must refuse")


def main():
    geom = R.resolve()
    W = {w["wall_id"]: w for w in geom.walls}
    plane = W["MA"]["face_hi_mm"]
    west = W["R6"]["face_hi_mm"]
    east = W["G8"]["face_lo_mm"]

    # --- 1. THE REAL FACE MUST PASS, or every seed below is vacuous ----------
    elev = WE.room_936_south(geom)
    ok("1  the real 9.36 south face builds", elev is not None)
    ok("1a chain closes to 2825.1 clear", abs(elev["span_mm"] - 2825.1) < 0.5,
       "span %.1f" % elev["span_mm"])
    ok("1b face is MA + R8, two segments", [s["wall_id"] for s in elev["segments"]] == ["MA", "R8"],
       str([s["wall_id"] for s in elev["segments"]]))
    ok("1c the EAST end is CONCRETE, not block",
       elev["segments"][-1]["class"] == "concrete", elev["segments"][-1]["class"])
    ok("1d exactly one opening, 1380.0 wide",
       len(elev["openings"]) == 1 and abs(elev["openings"][0]["width_mm"] - 1380.0) < 0.5)

    # The three numbers the owner's question turns on. If the compiler moves a
    # wall these change, and this seed is what notices.
    o = elev["openings"][0]
    ok("1e west solid 1120.1", abs((o["x0"] - elev["x0"]) - 1120.1) < 0.5,
       "%.1f" % (o["x0"] - elev["x0"]))
    ok("1f east solid 325.0", abs((elev["x1"] - o["x1"]) - 325.0) < 0.5,
       "%.1f" % (elev["x1"] - o["x1"]))

    # --- 2. A SPAN THAT OVERRUNS THE WALLS ----------------------------------
    # Push the east boundary 400 mm past G8. Nothing presents a face there, so
    # the face is no longer made of walls. The telescoping check passed this.
    rejects("2  span overrunning the resolved walls is refused",
            lambda: WE.build(geom, "EW", plane, west, east + 400.0),
            "not fully made of walls")

    # --- 3. A SPAN THAT STARTS IN OPEN AIR ----------------------------------
    # MA begins at x 2930.9; starting the face at 2700 leaves a gap at the west
    # end that no wall fills.
    rejects("3  span starting before any wall is refused",
            lambda: WE.build(geom, "EW", plane, 2700.0, east),
            "gap in the face")

    # --- 4. A FACE PLANE NO WALL LIES ON ------------------------------------
    # It refuses with "not fully made of walls" rather than "gap": with NO
    # segments at all the cursor never advances, so the end-of-span check is
    # what fires. Refusing for the right reason matters, so the seed states the
    # reason the tool actually gives rather than the one I first guessed.
    rejects("4  a face plane with no walls on it is refused",
            lambda: WE.build(geom, "EW", plane + 250.0, west, east),
            "not fully made of walls")

    # --- 5. OVERLAPPING OPENINGS --------------------------------------------
    # Two voids claiming the same hole. The telescoping sum was blind to this:
    # marks still ran monotonically and still summed to the span.
    class _G(object):
        pass

    g2 = _G()
    g2.walls = geom.walls
    dup = dict(geom.openings[0])
    real = [x for x in geom.openings if x["opening_id"] == "O4"][0]
    shifted = dict(real)
    shifted["opening_id"] = "O4_DUP"
    shifted["polygon"] = [[p[0] - 300.0, p[1]] for p in real["polygon"]]
    g2.openings = list(geom.openings) + [shifted]
    rejects("5  overlapping openings are refused",
            lambda: WE.build(g2, "EW", plane, west, east), "overlap")

    # --- 6. AN OPENING CROSSING THE ROOM BOUNDARY ---------------------------
    # ⚠ This seed found a DEAD CHECK. `openings_along` used to clip each
    # opening to the span before returning it, so the bounds test in `build()`
    # compared a clipped value against the very bounds it had been clipped to
    # and could never fire. The clip is gone; an opening that runs past the
    # boundary now reaches the check and is refused.
    g3 = _G()
    g3.walls = geom.walls
    g3.openings = [dict(real, opening_id="O4",
                        polygon=[[p[0] + 500.0, p[1]] for p in real["polygon"]])]
    rejects("6  an opening crossing the room boundary is refused",
            lambda: WE.build(g3, "EW", plane, west, east), "outside the clear span")

    # --- 7. THE TELESCOPING TRAP ITSELF -------------------------------------
    # Assert the property that made the old check useless, so nobody restores
    # it: the sum of gaps between sorted marks ALWAYS equals the span.
    marks = [0.0, 10.0, 999.0, 1234.5, 2825.1]
    telescoped = sum(b - a for a, b in zip(marks, marks[1:]))
    ok("7  the old check was provably vacuous (sum telescopes to the span)",
       abs(telescoped - (marks[-1] - marks[0])) < 1e-9)

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
