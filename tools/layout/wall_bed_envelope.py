#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""How wide can a wall-bed cabinet be? Answered from geometry, not from a catalogue.

⚠️⚠️ THIS INVERTS A BLOCKER THAT HAD BEEN SITTING FOR DAYS.
The record said the wall bed was blocked until the owner obtained a
MANUFACTURER'S cabinet width. Owner, 2026-09-19: *"I don't have exact the
wall-bed cabinet external width. This is exploration. I want to get from the
model answer like «wall-bed can be installed ... and its width can be no more
than ...»"*

He is right, and the old framing had it backwards. The model cannot know what a
maker sells, but it knows exactly how much room there is - so it should issue a
BUDGET and let him shop inside it, rather than wait for a number to check.

⚠️ WHAT THIS REPORTS IS A CEILING, NOT A FIT. It answers "no wider than X". It
does NOT say a cabinet of width X exists, nor that the room works with it open -
the open footprint and its walking clearance are a separate question, and so is
whatever else wants that wall.

⚠️⚠️ THE SUBSTRATE DECIDES WHICH RUN COUNTS, AND IT IS A ROUGH-STAGE DECISION.
The maker (Freedom, `YT_qMGSfO-glvc`) is explicit: *«надёжное крепление кровати
возможно ТОЛЬКО К БЕТОННОЙ СТЕНЕ»*. A second maker allows aerated block with
CHEMICAL ANCHORS and six-point fixing.

⚠️⚠️ ONLY THE CONCRETE-ONLY BUDGET IS PUBLISHED. A first version also printed a
"with block fixing" figure and it was WRONG in a familiar way: it summed the whole
collinear face plane and produced 6440 mm for R6 and 7380 for R7 - lengths that
cross rooms, which no bed can. That is a container's extent quoted as the
contained thing's, the same error as solid-for-clear and host-wall-for-opening.
Bounding it needs a room boundary this tool does not resolve, so it is REFUSED
rather than guessed.

⚠ The criterion is the MATERIAL, not the structural role. The vault corrected its
own "load-bearing" paraphrase on 2026-09-15: a load-bearing block wall is still
not concrete.
"""

import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))

from lib.tabular import read_csv, finite          # noqa: E402
import resolve_v0_geometry as R                   # noqa: E402

CANON = os.path.join(REPO, "data", "canonical")

# ⚠ AGENTS.md: dimensions are nominal ±50 mm, measured not assumed, evidenced by
# `Geometry_Variance_Study.md` against three surveyed flats. For a "no wider
# than" answer only the PESSIMISTIC half matters: the wall may be built 50 mm
# SHORTER than the plan says. Using ±25 here would give a figure 25 mm too
# generous, which is the exact error that reached a reviewer on 2026-09-18.
BUILD_TOLERANCE_MM = 50.0

# Plaster/render on a masonry face the cabinet butts against. Deducted ONCE per
# such end.
PLASTER_MM = 20.0

# Installation clearance a carcass needs to be got into the opening at all.
# Trade practice, not a vault-sourced figure, and flagged as such in the output.
FITTING_CLEARANCE_MM = 10.0

CONCRETE = "concrete"
SAME_PLANE_MM = 5.0


def collinear_run(geom, wall_id):
    """Every wall sharing this wall's face plane and axis, contiguous with it.

    A cabinet does not stop where a wall RECORD stops. R6 and G4a present one
    continuous face - R6 concrete for 1750, then G4a aerated block - so the
    physical run a carcass could occupy is longer than R6's own length. That is
    only USABLE with block fixing, which is why the two answers are separate.
    """
    W = {w["wall_id"]: w for w in geom.walls}
    seed = W[wall_id]
    same = [w for w in geom.walls
            if w["axis"] == seed["axis"]
            and abs(w["face_lo_mm"] - seed["face_lo_mm"]) <= SAME_PLANE_MM
            and abs(w["face_hi_mm"] - seed["face_hi_mm"]) <= SAME_PLANE_MM]
    same.sort(key=lambda w: w["from_mm"])
    run = [seed]
    # walk outward while the next wall touches the run
    changed = True
    while changed:
        changed = False
        lo = min(w["from_mm"] for w in run)
        hi = max(w["to_mm"] for w in run)
        for w in same:
            if w in run:
                continue
            if abs(w["to_mm"] - lo) <= SAME_PLANE_MM or abs(w["from_mm"] - hi) <= SAME_PLANE_MM:
                run.append(w)
                changed = True
    run.sort(key=lambda w: w["from_mm"])
    return run


def clear_mm(blocks, wall_id):
    row = blocks.get(wall_id) or {}
    return finite((row.get("clear_mm") or "nan"))


def envelope(geom, blocks, wall_id):
    seed = {w["wall_id"]: w for w in geom.walls}[wall_id]
    own_clear = clear_mm(blocks, wall_id)
    run = collinear_run(geom, wall_id)
    run_ids = [w["wall_id"] for w in run]

    # Concrete-only: the candidate's own CLEAR length. `clear_mm` is the length
    # of record; `solid_mm` includes owned corners and is NOT what a bed attaches
    # to. Quoting solid here is the rule-9 error the owner corrected twice.
    concrete_span = own_clear

    # With block fixing: the contiguous run on the same plane, using each
    # member's clear length.
    run_span = 0.0
    for w in run:
        c = clear_mm(blocks, w["wall_id"])
        run_span += c if c == c else 0.0

    def budget(span, plastered_ends):
        if span != span:
            return float("nan")
        return span - BUILD_TOLERANCE_MM - plastered_ends * PLASTER_MM - FITTING_CLEARANCE_MM

    return {
        "wall": wall_id,
        "class": seed["class"],
        "own_clear_mm": own_clear,
        "collinear_run": run_ids,
        "run_clear_mm": run_span,
        "concrete_only_max_mm": budget(concrete_span, 1),
        # ⚠⚠ NOT PUBLISHED AS A BUDGET, DELIBERATELY.
        # The first version printed budget(run_span) and produced 6440 mm for R6
        # and 7380 for R7 - the length of the whole collinear FACE PLANE across
        # the flat, crossing rooms. That is a container's extent quoted as the
        # contained thing's: the same rule-9 error as solid-for-clear, envelope
        # for bay, host wall for opening. A bed cannot span two rooms, so the
        # run must be clipped to the room the bed stands in - and this tool does
        # not know room boundaries. Reporting the raw run is left as evidence of
        # what the face offers; the BUDGET is refused until it is bounded.
        "raw_collinear_run_mm": run_span,
        "with_block_fixing_max_mm": None,
        "why_not_computed": ("the collinear run crosses rooms; a bed cannot. "
                             "Clipping it to the room needs the room boundary, "
                             "which this tool does not resolve."),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--walls", default="R6,R7,R8,R9",
                    help="candidate walls, comma separated")
    a = ap.parse_args()

    geom = R.resolve()
    blocks = {r["wall_id"]: r for r in read_csv(os.path.join(CANON, "wall_blocks.csv"))}
    have = {w["wall_id"] for w in geom.walls}

    print("WALL-BED CABINET WIDTH BUDGET")
    print("  a CEILING, not a fit. Deductions per candidate:")
    print("    -%.0f mm  build tolerance (AGENTS.md nominal +/-%.0f, pessimistic half)"
          % (BUILD_TOLERANCE_MM, BUILD_TOLERANCE_MM))
    print("    -%.0f mm  plaster on the masonry end it butts against" % PLASTER_MM)
    print("    -%.0f mm  fitting clearance (trade practice, NOT vault-sourced)"
          % FITTING_CLEARANCE_MM)
    print()
    print("  %-5s %-9s %9s  %12s   %-26s"
          % ("wall", "material", "clear", "CONCRETE", "same face plane continues as"))
    print("  %-5s %-9s %9s  %12s   %-26s"
          % ("", "", "mm", "ONLY max", "(NOT a bed budget - see below)"))
    rows = []
    for wid in [x.strip() for x in a.walls.split(",") if x.strip()]:
        if wid not in have:
            print("  %-5s NOT RESOLVED BY THE COMPILER - skipped" % wid)
            continue
        e = envelope(geom, blocks, wid)
        rows.append(e)
        print("  %-5s %-9s %9.1f  %12.0f   %-26s"
              % (e["wall"], e["class"], e["own_clear_mm"], e["concrete_only_max_mm"],
                 "+".join(e["collinear_run"])))

    print()
    conc = [r for r in rows if r["class"] == CONCRETE]
    if conc:
        best = max(conc, key=lambda r: r["concrete_only_max_mm"])
        print("  CONCRETE-ONLY ANSWER: a cabinet fixed straight into concrete must be")
        print("    NO WIDER THAN %.0f mm, on %s."
              % (best["concrete_only_max_mm"],
                 " or ".join(sorted(r["wall"] for r in conc
                                    if abs(r["concrete_only_max_mm"]
                                           - best["concrete_only_max_mm"]) < 1))))
    print()
    print("  ⚠ NOT ANSWERED HERE: whether the room still works with the bed OPEN,")
    print("    what else wants that wall, and whether a cabinet of this width exists.")
    print("  ⚠ Block fixing is a ROUGH-STAGE decision - chemical anchors or a")
    print("    floor-bearing frame must be specified BEFORE the walls are closed.")
    print()
    print("  ⚠⚠ NO 'WITH BLOCK FIXING' BUDGET IS PUBLISHED. The collinear face")
    print("     plane continues across ROOMS - R6 runs on as G4a and R1b - and a")
    print("     bed cannot span two rooms. Printing that length as an available")
    print("     width would be a container's extent quoted as the contained")
    print("     thing's. Clipping it to the room needs a room boundary this tool")
    print("     does not resolve, so the figure is REFUSED rather than guessed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
