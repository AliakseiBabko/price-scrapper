# Does the vector plan actually add anything? — the honest accounting

> [!IMPORTANT]
> **Owner, 2026-09-09:** *"Now I'm not sure why we're doing this at all. What it
> will give us… it's kind of a double job. We already have the plan with all the
> walls, all the wall segments with the material… They're already aligned, and
> now you're trying to… it may be useful in the future to extract graphics from
> the vector images, from the CAD files. But for now, what you are doing is just
> trying to reinvent the wheel."*

**He is substantially right, and this page exists so the answer is auditable
rather than defended.** Written 2026-09-09, after three architectures.

## The verdict up front

**Re-deriving the wall inventory from the drawing was reinventing the wheel, and
it should never have been attempted.** `wall_blocks.csv` + `wall_runs.csv` +
`wall_openings.csv` already hold 25 named walls with owner-confirmed classes,
thicknesses and lengths, and 10 openings. The drawing cannot improve on any of
that — **the plan uses the same hatch and the same thickness for concrete and
for aerated block**, so it cannot even distinguish the materials the model's
whole R/G/M scheme is built on.

**What the drawing legitimately supplies is exactly four things**, and only the
first of them was ever missing from the model.

## 1. Coordinates — the one thing the model lacked

The wall list carries **thickness and length but no position in millimetres**.
`wall_runs.csv` is in *basic-plan pixels*, which is why `project_decisions.md`
says the wall ids are *"regions on a raster, not named shell walls"*, and why the
material model *"cannot be enforced yet"*.

→ **The drawing turns the list into geometry.** That is the deliverable the owner
himself named: *"probably it would be nice to have this data in vector form, not
only the list of wall segments with the parameters."*
Output: `data/cad/dxf/v0_developer_layout.dxf`.

## 2. Independent validation of the model's own numbers

This is the part that would justify the exercise even if nothing else did,
because it tests figures nothing had tested:

| check | model | drawing | delta |
| :--- | :--- | :--- | :--- |
| **top wall** R1a + G2 + (R3+G3) | 1666 + 2219 + 5830 = **9715** | merged solid **9715.1** | **0.1 mm** |
| small room, top chain | 1795 + 120 + 910 = 2825 | **2825.0** | 0.0 |
| small room, bottom chain | 1120+1380+150+175 = 2825 | **2825.0** | 0.0 |
| middle room, bottom width | 600 + 1800 + 600 = 3000 | **3000.0** | 0.0 |
| туалет | 1140 × 1090 | **1140.0 × 1090.0** | 0.0 |
| east wall R7 + G5 + R2 | 7710 | 7731 | 21 mm |

**Two independent routes agreeing to a tenth of a millimetre on a 9.7 m chain is
not a double job.** It is the first evidence that the recorded lengths are right.

## 3. Three elements the model did not contain at all

- **The лоджия glazing's real subdivision** — run 2963.9, **four bays 660.0 ·
  680.2 · 679.2 · 659.2**, three 50 mm mullions, 150 mm assembly depth. ⚠️ `O9`
  previously had its four-bay reading from **a photo of flat 109**, and said so:
  *"the PATTERN transfers and the bay count and widths do not."* **The owner
  asked for exactly this for his 3D model.**
- **The decorative slab** at the 19,49 window — 1800 × 370, projecting 320 mm
  beyond MC. The owner identified what it is; **it was recorded nowhere.**
- **The suggested-furniture positions** — the two wardrobes, which the owner had
  not noticed on the raster.

## 4. One genuine disagreement it exposed

**M6b has no 200 mm wall in the drawing.** Where the model puts it, the vector
carries 300 at 5981/6281, 150 at 6131/6281 and 100 at 6181/6281.
`project_decisions.md` already flagged M6b's 200 mm as **provisional, "owner
revising against another plan"** — so the drawing did not create a problem, it
found one the owner had already suspected.

## What this page does NOT claim

- ❌ **It does not claim the drawing improves any wall's thickness, length, class
  or material.** It cannot; the model is authoritative on all four.
- ❌ **It does not claim the extraction is finished.** Residuals of +820 (G7),
  −671 (G4d), −360 (M2) remain, and those are **extraction faults, not questions
  for the owner** — his instruction, and correct: *"If you see the walls
  overlapping, this is not a question for me. This is question for your method
  of extracting the vector graphics."*
- ❌ **It does not claim the three failed architectures were necessary.** They
  were not. The first re-derived walls; the second positioned them through a
  raster fit with 3.3% anisotropy; only the third takes geometry from the vector
  and uses the raster solely to attach names.

## The standing rule that comes out of this

> **The wall model is the source of truth for WHAT a wall is. The drawing is the
> source of truth for WHERE it is, and a check on the model's arithmetic. Neither
> direction may be reversed, and nothing about a wall may be re-derived from the
> drawing.**

Enforced in `tools/layout/place_named_walls.py`, which now also **drives wall
overlap to zero as a gate rather than reporting it** — 8 overlapping pairs
(0.261 m²) down to 0, using `wall_corners.csv` where it has an entry and
thicker-then-longer where it does not.
