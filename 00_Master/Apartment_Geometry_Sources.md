# Where the apartment's geometry comes from

## The correction that matters

The Homestyler export is **the owner's modified layout, not the existing
state.** I had been treating it as the as-designed flat.

It is provable rather than a guess: the two rooms the CAD segmentation did
recover cleanly measure 13.06 and 10.16 m², and the Homestyler schedule lists
*Living and Dining 13.57* and *Kitchen 10.56*. The developer's plan has no room
of either size — its kitchen is 5.24 m². So the DXF draws the redesign.

That means the pipeline's `v0` should be the **developer's plan**, and the
Homestyler design is already a **variant** — the first real one, replacing the
two illustrative drafts.

## The five sources and what each is good for

| Source | File | Authoritative for |
|---|---|---|
| Developer's detailed plan | `_Inbox/_Visual_Drop/fllor_plan_detailed.jpeg` | **The base case.** Room areas, dimension strings, opening widths of the flat as sold |
| Developer's simplified plan | `_assets/floor_plan_initial.jpg`, `_Inbox/_Visual_Drop/floor_plan_basic.jpg` | Same layout, fewer dimensions — a cross-check |
| Owner's Homestyler design | `_assets/floor_plan_modified.png` | **Room names and areas of the redesign** |
| Homestyler CAD export | `data/cad/dxf/20260727-ZK Dubravinskiy.dxf` | **Wall geometry of the redesign** at millimetre precision |
| Three as-built comparables | `_Inbox/_Visual_Drop/floor plan_1..3.jpg` | **How much the built flat will differ** |

Schedules extracted into
[`data/canonical/room_schedules.json`](../data/canonical/room_schedules.json).

## The base case checks out exactly

Developer plan, type 3Б/3+ — rooms sum to 64.85 m², plus the loggia counted at
its coefficient (6.05 → 4.24) gives **69.09 m², the printed total.** The
arithmetic closing to the centimetre is good evidence the areas were read
correctly.

| Room | m² |
|---|---|
| жилая комната | 19.49 |
| жилая комната | 16.64 |
| жилая комната | 9.36 |
| прихожая | 9.79 |
| кухня | 5.24 |
| ванная | 3.09 |
| туалет | 1.24 |
| лоджия | 6.05 (4.24 counted) |

One number to note: the plan draws **75 mm partitions**, thinner than the 150 mm
the hand-built model assumed throughout.

The owner's redesign moves 1.39 m² into partitions and circulation — 63.46 m² of
rooms against the developer's 64.85 — buying a laundry room, a separate
entrance, and a kitchen at 10.56 m² instead of 5.24 m².

## How much the real flat will differ

The building is not finished, so nothing is field-verified. Three as-built plans
of the same layout give a measured answer instead of a guess
([`dimension_tolerance.json`](../data/canonical/dimension_tolerance.json)):

**Wall-to-wall dimensions differ by 0–50 mm between flats, median 20 mm.** The
overall depth of the living bay reads 7460 / 7440 / 7450 mm across the three.

So: **treat every dimension in the model as nominal ±25 mm, and never design a
fit that depends on less than about 30 mm of slack.** That rules out, for
example, a built-in that spans a whole wall with no scribe.

Room areas are tighter — 0.1–0.3 m² apart:

| Room | Developer | Measured range | Δ |
|---|---|---|---|
| коридор | 9.79 | 10.0–10.2 | +0.31 |
| ванная | 3.09 | 3.2 | +0.11 |
| жилая (малая) | 9.36 | 9.2–9.3 | −0.09 |
| жилая (средняя) | 16.64 | 16.7–16.8 | +0.09 |
| жилая + кухня | 24.73 | 25.0–25.2 | +0.37 |
| **туалет** | **1.24** | **1.6–1.9** | **+0.53** |

Two cautions in that table:

- **The туалет is the outlier.** Every measured flat has it half a square metre
  bigger than the developer's plan. Worth resolving before anything is designed
  to fit in it.
- The measured plans record living and kitchen as **one room** ("жилая с
  кухонным оборудованием"), so that row is only comparable summed.

Totals differ by 2.4 m² (68.3 to 70.7), but that is dominated by how each plan
counts the loggia, not by the rooms. `kv109`'s loggia is materially smaller and
may be a different sub-type.

## What this changes in the pipeline

1. `v0` becomes the developer's plan — the existing state, with the areas above.
2. The Homestyler CAD becomes a real variant, with wall geometry already
   extracted and non-overlapping, and its room schedule known.
3. The two illustrative drafts (`v1-kitchen-living`, `v2-combined-bath`) can go;
   they were only there to exercise the mechanism.
4. Every rule check that compares a dimension should carry the ±25 mm band
   rather than pretending to millimetre certainty.
