# Codex review brief — the spatial reading, and the rules the owner has stated

**2026-09-18.** Commit `134ea36` → head. Read `00_Master/Spatial_Structure_Analysis.md` first; this brief says what I want attacked in it.

⚠️ **The last five reviews each reproduced real defects in my work, including two rule-9 errors in the last two turns alone** — I ranked wall-bed candidates by `solid_mm` when `clear_mm` is the length of record, and then narrowed to one candidate when the scenarios need two. Assume the same rate here.

---

## What changed since the last brief

The owner reclassified `v1-homestyler` as a **sketch, not a variant** — *"just my experiment… no exact dimensions, just general ideas"* — drawn in Homestyler over the **same constructor raster `v0` came from, before any model existed.** You had already said its coordinates should not survive; this is stronger than that, and it means the "rebase v1" work you sequenced is not merely deferred but **wrong in premise**. It is now `reference_only` and the basis gate refuses it permanently.

He then stated a set of rules directly. They are recorded in:

| file | holds |
| :--- | :--- |
| `data/canonical/design_intents.csv` | DI-001…DI-008, with a `status` and a `dimension_state` each |
| `data/canonical/occupancy_scenarios.csv` | `SC-NOW` (built), `SC-A`, `SC-B` (candidates) |
| `data/canonical/design_parameters.csv` | maximise-subject-to-fit parameters, and the substrate constraint |
| `data/canonical/design_envelopes.csv` | furniture envelopes, five still `NOT_ESTABLISHED` |
| `data/canonical/room_depth_bands.csv` | the band ordering, with one cell marked `unresolved` |

## The claims I most want attacked

**1. That `DI-008` is forced by the building rather than chosen.** §1 of the analysis argues that because all three windows and the лоджия glazing are on one façade, every room shares a depth axis and a light gradient, so entrance → storage → bed → window is a description rather than a preference. **If that is overstated, most of §6 goes with it.**

**2. That there are exactly two wall-bed positions and they are structurally symmetric.** `R6` and `R7`, both 1750 clear, each the north continuation of a façade return, one per outer bay — and they map one-to-one onto the two Phase-2 scenarios. I find this too neat and would like it checked. In particular: **is 1750 clear really enough for a 1600 bed once the CABINET is counted?** I have flagged that the cabinet is wider than its mattress and that the figure is not recorded, but I have not proven 1600 fits.

**3. That the middle bay cannot host a wall bed at all.** `R8`/`R9` are 1490 clear and flank the window wall. I conclude the shared children's room must use ordinary beds. Check whether I have missed a position — including against `G7`/`G8`, which are 75 mm block and would need a floor-bearing frame rather than wall fixing.

**4. That `G7` and `G8` are one decision rather than two.** They set all three bay widths and share boundaries, so width taken from one bay is given to another. If true, every width question in the project reduces to where those two walls sit — which would make them the most consequential movable elements in the flat, and nothing currently treats them that way.

**5. ⚠️ That the first-fix problem is halved.** §6.3 claims the middle bay has the same role in both scenarios, so it needs one wiring answer, and only the two outer bays need wiring that serves both an adult and a child. **This is the load-bearing claim for sequencing DI-004 first** and I reached it late and quickly.

## Where I know I am weak

- **No room polygons exist in the v2 schema.** I inferred the three bays from wall positions and divider x-extents. That inference is not gated by anything, and §2's bay table is the least defended part of the page.
- **Areas are deliberately absent** and I have quoted none — but I have quoted bay *widths*, which are differences between wall coordinates and therefore inherit whatever the coordinates carry.
- **`DI-008` versus the owner's own bed placement.** He puts beds *"next to `R4` or `R5`"*, which are at the room's entrance end — the band his own rule assigns to storage. I recorded the tension rather than resolving it; say if that is the wrong call.
- **The living-zone contradiction** (`BAND-KL-3`) is recorded as unresolved. It may instead be evidence that the living zone should not be the transformable bedroom at all, which would overturn `DI-004`'s premise.

## What I am NOT asking

Not asking you to choose between `SC-A` and `SC-B`, or to place anything. The owner chooses; the model says what is feasible. I am asking whether **the constraint reading is right**, because everything downstream is built on it.
