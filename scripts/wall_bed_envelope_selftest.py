#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Guards `tools/layout/wall_bed_envelope.py`.

⚠️⚠️ THE TRAP HERE IS LIVE AND I ALREADY FELL IN IT ONCE.
This tool answers "how wide can it be", which is a clear-span question, in a
model that also publishes `solid_mm` (clear plus owned corners) and whole
collinear face planes. Every one of those is a larger number sitting right next
to the right one. The owner corrected `solid`-for-`clear` twice, and the first
version of this tool published 6440 mm for R6 - the whole face plane across the
flat - as an available bed width.

So the seeds are mostly about NOT reading the bigger number.
"""

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "layout"))

from lib.tabular import read_csv                     # noqa: E402
import resolve_v0_geometry as R                      # noqa: E402
import wall_bed_envelope as WB                       # noqa: E402

PASS, FAIL = [], []


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", name,
                        ("  -- " + str(detail)) if detail and not cond else ""))


def main():
    geom = R.resolve()
    blocks = {r["wall_id"]: r for r in
              read_csv(os.path.join(REPO, "data", "canonical", "wall_blocks.csv"))}

    e6 = WB.envelope(geom, blocks, "R6")
    e8 = WB.envelope(geom, blocks, "R8")

    # --- 1. THE REAL ANSWER, so every seed below is not vacuous --------------
    ok("1  R6 concrete-only budget is 1670 mm",
       abs(e6["concrete_only_max_mm"] - 1670.0) < 0.5, e6["concrete_only_max_mm"])

    # --- 2. CLEAR, NEVER SOLID -----------------------------------------------
    # R8 is the discriminating case: clear 1490, solid 2090. A tool reading
    # solid would report ~2010 and look plausible.
    ok("2  R8 uses clear 1490, NOT solid 2090",
       abs(e8["own_clear_mm"] - 1490.0) < 0.5, e8["own_clear_mm"])
    ok("2a ...so its budget is 1410, not ~2010",
       abs(e8["concrete_only_max_mm"] - 1410.0) < 0.5, e8["concrete_only_max_mm"])

    # --- 3. THE COLLINEAR RUN IS NEVER PUBLISHED AS A BUDGET -----------------
    ok("3  the with-block-fixing budget is REFUSED, not computed",
       e6["with_block_fixing_max_mm"] is None, e6["with_block_fixing_max_mm"])
    ok("3a ...and the refusal says why",
       "room" in (e6.get("why_not_computed") or "").lower())
    ok("3b the raw run really is much larger - the trap is real",
       e6["raw_collinear_run_mm"] > 3 * e6["own_clear_mm"],
       e6["raw_collinear_run_mm"])

    # --- 4. THE PESSIMISTIC HALF OF THE TOLERANCE ----------------------------
    # +/-50 is uncertainty; for a ceiling only the losing half counts. Using 25
    # gave a figure 25 mm too generous and reached a reviewer on 2026-09-18.
    ok("4  the build tolerance deducted is 50, not 25",
       abs(WB.BUILD_TOLERANCE_MM - 50.0) < 1e-9, WB.BUILD_TOLERANCE_MM)
    ok("4a the deductions actually sum: 1750 - 50 - 20 - 10 = 1670",
       abs(1750.0 - WB.BUILD_TOLERANCE_MM - WB.PLASTER_MM
           - WB.FITTING_CLEARANCE_MM - 1670.0) < 0.5)

    # --- 5. PERPENDICULAR SPAN USES ONLY PARALLEL WALLS ----------------------
    fs = WB.free_span_perpendicular(geom, "R6")
    high = fs["high"]
    ok("5  R6's room side runs 2825.1 mm",
       high["free_mm"] is not None and abs(high["free_mm"] - 2825.1) < 0.5,
       high["free_mm"])
    ok("5a ...and it NAMES what bounds it, rather than returning a bare number",
       high["bounded_by"] == "G8", high["bounded_by"])

    # An EW wall must never bound a NS wall's perpendicular span: it bounds the
    # other axis, and sweeping everything would find one and report nonsense.
    W = {w["wall_id"]: w for w in geom.walls}
    bounders = [v["bounded_by"] for v in fs.values() if v["bounded_by"]]
    ok("5b no perpendicular wall was used as a bound",
       all(W[b]["axis"] == W["R6"]["axis"] for b in bounders), bounders)

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
