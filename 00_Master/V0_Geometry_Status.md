# v0 geometry — where it actually stands

**v0 is the baseline layout: the flat exactly as the developer builds it.**
Everything else is a variant measured against it. Its room schedule and its
dimension chains were always known; **its partition POSITIONS were not**, because
they existed only on a raster. That gap is why `project_decisions.md` calls v0
*"the blocking task"*, and why `Layout_Option_Review.md` had to **withdraw** its
comparison of v1 against v0 — the two were computed on different bases.

**Started 2026-09-08, from the vector plan.** This page records what the first
extraction pass produced and, more usefully, what it did not.

> [!CAUTION]
> **⚠️ NOTHING HERE IS CANONICAL YET.** `data/canonical/v0_wall_runs_extracted.json`
> carries `status: DRAFT — EXTRACTED, NOT REVIEWED`. **Walls are not named,
> corners are not resolved, and the run list is incomplete.** Do not build a
> variant, a quantity or a drawing on it.

## What the extraction does

`tools/layout/extract_v0_walls.py`, run against
`_Inbox/_Visual_Drop/3Б_3+ МН5_287.pdf`:

1. Long axis-aligned lines → candidate **wall faces**, clustered and their spans
   unioned, because a face is drawn in pieces.
2. Faces paired at a plausible thickness. ⚠️ **Pairing alone over-generates
   badly** — it will pair one wall's face with another's across a room. The
   first pass produced 95 candidates for a flat with ~25 walls.
3. **A drawn wall is a SOLID, and the drawing says so by hatching it.** A pair
   survives only if hatch crosses its centre line. That is the filter that took
   95 candidates to 36.
4. **The unhatched stretches of a surviving wall are reported as candidate
   OPENINGS** — the same evidence read the other way round.

**Result: 36 runs, thicknesses landing on 75 / 100 / 120 / 150 / 175 / 200 / 250 /
300 / 400** — the vault's own wall vocabulary, arrived at independently.

**Look at `_Drawings/review/v0_wall_extraction.png` before trusting any of it.**
A run list reads as plausible long after it has stopped being; the overlay does
not.

## ⚠️ The trap in step 3, and what it cost

**The hatch test was first written to accept 45° and 135° strokes, and it
silently deleted the entire SE façade** — the one external wall in the flat, the
one carrying every window. The façade survived pairing and was thrown away by
the filter.

**The cause: the façade is hatched at 50°, not 45°.** The external aerated block
carries a different fill symbol from the internal partitions. Nothing failed
loudly; the wall was simply absent from a list of 28 that otherwise looked
complete. **It was caught by rendering the runs over the plan and noticing a
grey strip with no red on it.**

> [!IMPORTANT]
> **The lesson is the repo's own: a filter that removes evidence must be looked
> at, not just tuned.** Two thresholds in this tool are now deliberately
> permissive for the same reason — `MIN_COVER = 0.35`, because a wall with two
> windows is mostly not hatched, and that is exactly the wall worth having.

⚠️ **The 50° hatch is RECORDED, not interpreted.** It is tempting to read hatch
angle as a material key — 50° for aerated block, 45/135 for the rest. **Do not.**
This repo's standing position, from the owner, is that **the plan does not
distinguish concrete from aerated block**, and that the wall model in
`wall_materials.json` is owner-supplied evidence *precisely because* it is not
derivable from the drawing. One hatch angle on one drawing is not enough to
overturn that. It is a lead, and it is written down as one.

## ⚠️ What is still MISSING — read this before using the output

- **The façade is only partly captured.** The run under the 19,49 room is there;
  **the stretches under the 9,36 and 16,64 rooms are not**, or are broken into
  fragments. The façade is the least complete wall in the extraction and the
  most consequential one.
- **The лоджия's angled glazing is absent entirely.** The tool handles
  axis-aligned faces only, and that wall is diagonal.
- **Some runs are certainly composites.** The longest is 9,309 mm on one pair of
  faces; the flat has no single wall of that length. It spans several walls that
  happen to be collinear and equally thick, and splitting it needs the junctions.
- **Thicknesses of 296 / 298 / 397 / 147 mm appear** alongside the clean ones.
  These are pairs straddling a joint or an insulation line, not real walls, and
  they have not been resolved.
- **No wall is named.** Mapping these runs onto `R1a…R9`, `G1…G5`, `M1…M6` in
  `wall_blocks.csv` is the step that turns an extraction into geometry, and it
  carries judgement — it is where the owner's material model finally binds to
  named walls, which `project_decisions.md` has wanted since 2026-09-04.
- **No corner is resolved.** Ownership lives in `wall_corners.csv` and is
  enforced by `tools/layout/build_wall_corners.py`. Untouched so far.
- **`check_wall_junctions.py` has not been run against this.** It cannot be, yet:
  it needs named walls.

## What it does not change

**⚠️ Precision is not accuracy.** These are the developer's **project**
dimensions, read to ~0.1 mm because the drawing is exact about itself. The
as-built runs **+1.0% to +1.9% SMALLER**, 12 comparisons of 12. **Size nothing
tight from this.** See `dimension_tolerance.json`.

**Coordinates are sheet-relative, not flat-relative.** Differences between runs
are meaningful; the absolute numbers are not a datum, and a flat-local origin
still has to be chosen.

## The order of the remaining work

1. **Finish the façade**, including the лоджия's diagonal. It is the biggest hole.
2. **Split the composite runs** at their junctions.
3. **Name the walls** against `wall_blocks.csv`, and bind `wall_materials.json`.
4. **Build the corner ledger**, then run `check_wall_junctions.py` and
   `build_wall_corners.py` until both pass.
5. Only then promote out of `DRAFT`, and only then re-open the v0-against-v1
   comparison that `Layout_Option_Review.md` withdrew.

⚠️ **Validate by CHAIN CLOSURE, never against a printed area.** v0's computed
areas will not sum to 69.09, and that is expected, not a bug.
