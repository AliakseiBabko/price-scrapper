# The drawn block joints — what the vector settles that no raster could

**Established 2026-09-09.** This is the answer to the owner's question *"we have
one dimension, like a segment of a wall of G2, which is adjacent to the R1a, and
the measurement was not clear. Now on this vector drawing… we have this
measurement."*

## The mechanism

`Apartment_Geometry_Sources.md` had already put the limitation exactly: the basic
plan *"draws the same walls without the numbers — so it cannot show where one
block ends and the next begins. That is why `G1` read as one wall from the basic
plan and as two blocks, 250 + 120, to the owner reading the detailed one."*

**The vector plan draws a line right across the wall's full thickness at every
block joint.** So the segmentation is *read*, not inferred — and
`tools/layout/place_named_walls.py` now segments each wall solid on those joints
instead of laying recorded lengths from one end.

> [!IMPORTANT]
> **⚠️ A joint bounds the wall's CLEAR run, not its `solid_mm`.** Matching on
> `solid_mm` made R1a overshoot to the next joint and swallow 500 mm of G2 —
> because `solid_mm` adds the corners a wall owns, which no joint marks. **R1a is
> the proof: drawn 1415.0 against a recorded `clear_mm` of 1416, while its
> `solid_mm` of 1666 is exactly 250 mm more — the corner it owns.**

## ✅ What the joints confirm, to the millimetre

Matching each named wall against its **`clear_mm`**:

| wall | clear_mm | drawn | delta |
| :--- | :--- | :--- | :--- |
| **R2** | 1675 | **1675.1** | **+0.1** |
| **G5** | 4035 | **4034.9** | **−0.1** |
| **R7** | 1750 | **1749.7** | **−0.3** |
| **G8** | 3250 | **3249.7** | **−0.3** |
| **R5** | 1050 | **1050.0** | **+0.0** |
| **G6** | 1915 | **1915.0** | **+0.0** |
| **R1a** | 1666 | **1415.0** | **−1.0** vs clear 1416 |
| **G2** | 2219 | **2220.6** | **+1.6** |
| R6 | 1750 | 1739.7 | −10.3 |
| G4a | 3570 | 3545.0 | −25.0 |

**Median |delta| across all 17 measurable walls: 10.3 mm.**

### ✅ G2 — the measurement the owner asked about

**G2 reads 2220.6 mm between its two drawn joints, against a recorded 2219.**
The joints are at **x = 4645.9** (its boundary with R1a) and **x = 6866.5**.
**The entrance door O8 sits inside it, at 5146.0…6155.9 = 1009.9 mm against a
printed 1010** — which independently confirms `wall_opening_spans.csv` putting O8
in G2 rather than on a boundary.

⚠️ **And it supplies the dimension `wall_blocks.csv` explicitly asked for.** The
R1a note reads: *"Two pixel-only estimates remain and they disagree: 1429 … and
1241 … Needs one printed dimension from the west wall to the entrance door, or a
tape measure."* → **West inner face to the door's west jamb = 3230.9 → 5146.0 =
1915.1 mm**, of which R1a is 1415.0 and G2's first segment 500.1. **1429 was the closer
of the two estimates; 1241 is wrong.**

## ✅ The R3 | G3 indeterminate split — now located

`wall_blocks.csv` records R3 and G3 as an **INDETERMINATE SPLIT**: *"The split
point is not dimensioned on any plan"*, with only bounds — **R3 ≥ 2515**,
**G3 < 3315**, and the pair total **5830**.

**There is a drawn joint at x = 9606.2**, giving **R3 = 6866.5 → 9606.2 =
2739.7 mm**.

Three independent checks that this is the real joint:

1. **2739.7 ≥ 2515** ✅ — inside the recorded lower bound for R3.
2. The G3 note says the printed 3315 *"runs from the VENTING SHAFT to R2, and the
   R3|G3 split lies east of the shaft edge"*. The shaft edge is at
   12695.9 − 3315 = **9380.9**, and **9606.2 is 225 mm east of it** ✅ — exactly
   as the note reasoned.
3. G3 then runs 9606.2 → 12695.9 = **3089.7 < 3315** ✅.

⚠️ **Not yet promoted into `wall_blocks.csv`** — the split has been an explicit
unknown there since 2026-09-04 and changing it is the owner's call. **❓ Confirm
and I will record R3 = 2740, G3 = 3090.**

## ⚠️ R1a + R1b are ONE element — owner, 2026-09-09

*"R1a and R1b is actually one corner element… this corner is one concrete slab
without any joints."*

**The drawing agrees: there is no joint line between them.** The joints found on
the left wall are at y = 9350.6, 11100.3, 13010.5, 14645.3 and 16240.3 — and
**none at the corner itself**, where the top wall's inner face (16240.3) meets
the left wall's.

→ **So `R1a` and `R1b` are two named legs of a single monolithic L-shaped
reinforced-concrete corner, not two walls meeting at a junction.**

**Consequences, and they are not cosmetic:**

- ⚠️ **The corner-ownership question between them is void.** `wall_corners.csv`
  carries `C_R1a_R1b` with `owner = R1a, owner_gains_mm = 250`. That entry
  models a joint that does not exist. **It is arithmetically harmless — one leg
  still has to carry the corner volume so it is counted once — but it is
  describing the wrong thing**, and anyone reading it will think there is a joint.
- ✅ **It explains R1a's `clear_mm` of 1416 versus `solid_mm` 1666.** The 250 is
  not a corner one wall "wins" from another; it is part of the same casting.
- ⚠️ **For the 3D model and any reinforcement or demolition question, it must be
  one solid.** An L cast in one pour behaves differently from two walls butted
  together, and it is the flat's stiffest element.

**❓ Should `wall_blocks.csv` gain a `monolithic_with` column, or should R1a and
R1b be merged into a single L-shaped element with a polyline footprint?** The
second is more honest and worse for every tool that assumes axis-aligned
rectangles.

## What is still wrong, and it is mine not the model's

`G7 +820`, `G4d −671`, `M2 −360`, `MA +225`, `R1b +145`, `G4C −120`,
`G4b +119`. In each the solid's extent or the greedy joint walk is at fault, not
the recorded length. **Owner, 2026-09-09: *"If you see the walls overlapping,
this is not a question for me. This is question for your method."*** Overlap is
already gated to zero; these residuals are the same class of problem.
