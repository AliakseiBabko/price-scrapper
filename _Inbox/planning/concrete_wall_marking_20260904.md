# Concrete walls and columns — owner's red marking, 2026-09-04

**Status: READ AND ENUMERATED, PENDING THE OWNER'S CONFIRMATION.** Deliberately **not** promoted into
`data/canonical/current_apartment_shell.json` yet — four questions below have to be answered first, and the
most important of them is whether the marking is exhaustive. Once confirmed this becomes shell `constraints`,
which is what `make_variant.py` checks a layout against.

**Source:** `_Inbox/_Visual_Drop/floor_plan_basic_concrete_walls.jpg` (1061 × 1112) — the owner marked the
concrete walls and columns in red on the **basic** developer plan (3Б/2+, 69.44).
**Numbered reading:** `_assets/concrete_marking_regions.png`.

---

## ⚠️⚠️ First: the drawing does NOT encode the material. The marking is genuinely new information.

The owner asked whether the hatching inside the wall sections could be used to tell concrete from the softer
material without his help. **Tested, and the answer is no.**

**The decisive counter-example is region 3.** The red-marked run of the top wall above the прихожая and the
**unmarked** segment of that same wall immediately to its left are drawn with **identical thickness and
identical diagonal hatching**. Same wall, same graphics, different material.

- **What the drawing DOES encode is THICKNESS** — 250 mm structure, 75 mm partitions, 120 mm in the wet
  block — and that is exactly the *"200 mm thickness threshold … not a structural survey"* heuristic the
  layout skill already warns about.
- **And thickness would have actively misled here**, because only **parts** of the thick façade walls are
  marked: regions 2, 6 and 7 are segments of façade walls whose remainder is not red.
- *Some* hatch variety does exist on the plan (the outer wall at the balcony end carries a stipple/cross-hatch,
  probably insulation), but it does not correlate with the red marking.

→ **So this cannot be re-derived, and it cannot be re-derived later either. It has to be recorded as
owner-supplied evidence.**

## The nine marked regions

Detected programmatically rather than by eye (`>=150 px` connected red components). Coordinates are px in the
source image; **the mm figures are approximate** — the red stroke inflates each box by roughly its own width,
and no scale factor for this image has been established. **They are for identification, not measurement.**

| # | bbox px | px size | reads as |
| :--- | :--- | :--- | :--- |
| **1** | 22,40 – 230,178 | 209 × 139, **L-shaped** | The outer **corner at the туалет** — top wall stub plus the left wall beside it |
| **2** | 1009,41 – 1038,241 | 30 × 201 | **Right façade wall alongside the кухня** (5.24) |
| **3** | 420,44 – 696,70 | 277 × 27 | **A ~3 m run of the top wall above the прихожая.** The segment to its left is NOT marked |
| **4** | 335,305 – 364,414 | 30 × **110** | **COLUMN — middle room's top-left corner**, at the прихожая end |
| **5** | 647,306 – 676,414 | 30 × **109** | **COLUMN — middle room's top-right corner**, at the прихожая end |
| **6** | 23,564 – 54,743 | 32 × 180 | **Left façade wall beside the 9.36 room** |
| **7** | 1008,648 – 1038,829 | 31 × 182 | **Right façade wall beside the living room** (19.49) |
| **8** | 319,742 – 347,922 | 29 × **181** | Middle room's **left wall at the balcony end** |
| **9** | 646,744 – 675,923 | 30 × **180** | Middle room's **right wall at the balcony end** |

### ⚠️ The two "columns next to the entrance area" are almost certainly 4 and 5

The owner described **two** concrete columns *"in the middle next to the entrance area"*. **Regions 4 and 5 fit
exactly:** they flank the opening from the прихожая into the middle room, they are short and isolated (≈110 px
against 180 px for regions 8/9 of the same width), and their length corresponds closely to the **1050 mm** band
the *detailed* plan prints at the middle room's top.

**Regions 8 and 9 are the same thickness but ~65% longer, at the balcony end** — so they read as wall segments
or pilasters rather than as the two columns he meant. **That distinction is question 2 below.**

## ⚠️⚠️ Why this matters more than a materials note

1. **It is a hard legality constraint.** Nothing in the model currently carries a column at all; the shell has
   14 walls and the immovable services. Regions 4 and 5 sit in the **entrance area — where `v1` puts its
   1.90 m² laundry and where the corridor-to-kids trade would go.**
2. **The owner's own reason is the sharper one: a service can be chased through aerated block and cannot
   through concrete.** So this map decides where an AC line, a ventilation run or a recessed anything can
   physically go — not merely what may be demolished.
3. **It is the same situation the closest comparable in the vault resolved well:** that flat had a
   load-bearing column that could not be removed, and the designer **built the laundry cupboard against it**
   rather than around it (`nsdsgn-70m2-family-two-children`, move `m2`). **If region 4 or 5 lands where the
   laundry wants to be, that precedent is directly usable.**

## ⚠️ Four questions before this is promoted to a constraint

1. **⚠️⚠️ IS THE MARKING EXHAUSTIVE?** Is everything **not** red confirmed *non*-concrete, or are these only
   the ones the owner is sure about? **Treating a partial marking as exhaustive would be the dangerous
   error** — it would license removing something structural. Until answered, this file records the red as
   *"concrete, confirmed"* and the rest as **unknown**, not as *"not concrete"*.
2. **Are regions 8 and 9 also columns, or wall segments?** Same thickness as 4/5, ~65% longer, at the opposite
   (balcony) end of the same two walls.
3. **Region 3:** roughly 3 m of the top wall above the прихожая is concrete while the segment to its left is
   not. Is that right, and is there a real joint at that boundary?
4. **The non-red walls: material and nominal thickness.** The owner named a *"vaporized concrete"* — i.e.
   **газобетон / газосиликат**, autoclaved aerated block. The plan draws **75 mm** partitions; **if the real
   block is 100 mm, every partition position shifts** and it matters for the reconstruction in progress.

## Handedness — resolved for this image

**The marked plan is the same handedness as the detailed plan** (туалет top-left, лоджия bottom-left off the
9.36 room, кухня top-right). **So no mirroring correction applies to this markup.** That check exists because
the series is built in left- and right-handed variants and any comparable *may* be flipped — see
`00_Master/Apartment_Geometry_Sources.md`.

## Note on which plan this is

The markup is on the **basic** plan (3Б/2+), not the dimensioned **detailed** one (3Б/3+). The two agree on
layout and differ slightly on printed areas — and **per the standing instruction of 2026-09-04 those areas are
not evidence anyway**, so nothing is lost. **But the grid key plan (`_assets/wall_key_plan.png`) was built on
the DETAILED plan, so its A–L × 1–12 references do not transfer to this image.** Positions here are given as
px and in words instead.
