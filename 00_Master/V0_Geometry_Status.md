# v0 geometry — where it actually stands

**v0 is the baseline layout: the flat exactly as the developer builds it.**
Everything else is a variant measured against it. Its absence is why
`project_decisions.md` calls v0 *"the blocking task"* and why
`Layout_Option_Review.md` had to **withdraw** its v0-against-v1 comparison.

> [!CAUTION]
> **⚠️ NOT CANONICAL YET.** Every dataset here carries `status: DRAFT`.

> [!IMPORTANT]
> **Is this exercise worth doing at all?** The owner asked that directly on
> 2026-09-09 and the answer is audited on its own page:
> [`V0_Why_The_Vector_Plan_Earns_Its_Place.md`](V0_Why_The_Vector_Plan_Earns_Its_Place.md).
> **Short version: re-deriving the wall inventory was reinventing the wheel and
> should never have been attempted.** What the drawing legitimately supplies is
> coordinates, an independent check on the recorded lengths, three elements the
> model never contained, and one genuine disagreement.

**✅ Wall overlap is now ZERO** — 8 overlapping pairs (0.261 m²) driven to 0 by
`place_named_walls.py`, as a gate rather than a report. Owner, 2026-09-09:
*"If you see the walls overlapping, this is not a question for me. This is
question for your method of extracting the vector graphics."* Correct, so
overlap is measured and resolved in the tool: `wall_corners.csv` decides the
owner where it has an entry, thicker-then-longer where it does not, and a
same-axis overlap is treated as what it is — a thin face pair nested inside a
thick one, an extraction artefact.

## The two deliverables

Owner, 2026-09-08: *"I would spread the job into two parts. I would like to have
something which could be exported into AutoCAD format. And also I would like
something I can use for my own model."*

| part | state |
| :--- | :--- |
| **1 — AutoCAD** | ✅ `data/cad/dxf/v0_developer_layout.dxf`, via `tools/layout/export_v0_dxf.py` |
| **2 — his own 3D model** | ❌ **not started.** Needs the glazing and window frames as real openings with sill/head, not plan outlines |

**The DXF, read back and checked:** 25 walls (10 concrete, 10 aerated, 3
external, 2 лоджия), 8 openings, 4 glazing bays + 3 mullions, the slab
extension, 5 suggested-furniture lines, 25 id labels. **Extent 10115 × 10227 mm**
— which is also an independent check that the scale is right.

**Layer colours are the owner's own key**, from
`_Inbox/_Visual_Drop/floor_plan_basic_all_walls.jpg`: red RC frame, green
internal aerated block, magenta external and лоджия.
**`V0-SUGGESTED-FURN` is dashed, orange, and on its own layer so it can be
frozen or deleted in one action.**

## ⚠️⚠️ THE THIRD ARCHITECTURE — geometry from the VECTOR, names from the raster

**Owner, 2026-09-09:** *"It looks like this is interpretation of the vector image,
not the real displacement... build a processed image where I overlay this PDF
document, everything is aligned. For example R4, G8 and R8 — they completely off
the line... they randomly scattered."*

**He was right, and the diagnosis was more precise than mine.** Every POSITION
was being routed through an affine fit of basic-plan pixels — a fit with **3.3%
anisotropy between its axes and per-wall residuals to 93 mm** — so it scattered
walls the drawing had drawn perfectly aligned. **Proof on his own example**, in
the vector:

| wall | t | faces | along |
| :--- | :--- | :--- | :--- |
| R8 | 250 | 5881.0 / **6131.0** | 7610.6 … **9350.6** |
| G8 | 75 | **6056.0** / **6131.0** | **9350.6** … **12600.3** |
| R4 | 250 | **6056.0** / 6305.9 | **12600.3** … 13650.3 |

**R8 and G8 share the face 6131.0; G8 and R4 share 6056.0; and their ends meet
exactly.** The drawing already contained touching, aligned walls. **The old code
placed G8 at 5981/6056 — out by 75 mm, exactly one wall thickness.**

→ **The rule now: GEOMETRY comes from the vector's hatch-validated solids. The
pixel fit decides only WHICH named wall belongs to WHICH solid, and positions
nothing.** 24 of 25 walls matched onto 17 solids.

### Two further fixes the same insight forced

**A wall continues through its door.** An opening carries no hatch, so a wall
with a doorway arrived as two solids and pulled its names to the wrong side of
the gap. Collinear solids sharing a face pair are now merged across gaps up to
1500 mm. **✅ And that produced the best validation this model has: the top wall's
merged solid measures 9715.1 mm against a recorded R1a 1666 + G2 2219 + (R3+G3)
5830 = 9715 — a residual of 0.1 mm**, from two entirely independent directions.

**The drawing continues the neighbour's structure past this flat.** The SE façade
solid ran 1680.9…5881.0, some 1300 mm of it beyond the party wall. Solids are now
clipped to the flat's own envelope — **x 2830.9…12993.5, y 7490.4…16261.6**. MA's
residual fell from +1375 to +225, and the east chain's from +1600 to **+21**.

## ⚠️ What still needs attention

| out by | walls | most likely cause |
| :--- | :--- | :--- |
| **+820** | G7 | solid longer than the recorded 3250; the 75 mm partition's true extent |
| **−671** | G4d | solid shorter than the recorded 2825 |
| **−360** | M2 | лоджия wall drawn axis-aligned when the real one splays |
| **+279** | R5 | |
| **+250** | MC | |
| **+225** | MA | still slightly over after clipping |
| −120 | G4C | |
| +119 | G4b | |
| +110 | R6, G4a, R1b | |

**⚠️ M6b is UNMATCHED — there is no 200 mm hatched solid where it should be.**
The vector shows 300 at 5981/6281, 150 at 6131/6281 and 100 at 6181/6281 in that
position. `project_decisions.md` already flags **M6b's 200 mm as provisional,
"owner revising against another plan"** — so this is the model and the drawing
disagreeing about a wall the owner already doubted, not a placement failure.
**❓ Worth resolving from the drawing rather than the other plan.**

**12 junction gaps remain**, the largest 239 mm (G4d's end) — down from 17 with
the worst at 394 mm. These are now small enough to be corner-ownership
questions, which is what `wall_corners.csv` and `build_wall_corners.py` exist to
settle.

## Still missing

- **The лоджия's M2 / M6b are exported as axis-aligned bars** — the real
  enclosure is splayed. The glazing itself is correct and diagonal; its two
  flanking walls are not.
- **Window frame subdivision for MA / MB / MC** is not extracted. The geometry
  is on the drawing (the 19,49 window shows jamb frames and a central mullion
  pair) and **part 2 needs it**.
- **The blue fixtures** — sanitaryware, kitchen — are in the owner's markup and
  not in the export.
- **No corner ownership**, so `check_wall_junctions.py` and
  `build_wall_corners.py` have not been run.
- **O10, the прихожая-to-кухня passway**, has no span row and is absent.

## What none of this changes

**⚠️ Precision is not accuracy.** These are the developer's **project**
dimensions; the as-built runs **+1.0% to +1.9% SMALLER**, 12 of 12. Size nothing
tight from this drawing.

⚠️ **Validate by CHAIN CLOSURE, never against a printed area.**

## The лоджия glazing and the slab — the two elements that are settled

**Glazing** (`extract_v0_elements.py`): run **2963.9 mm**, bearing 164.05°,
assembly depth **150 mm**, **four bays 660.0 · 680.2 · 679.2 · 659.2** with
**three 50 mm mullions** — the owner's *"one block but in four segments"*,
measured. **This upgrades `O9` from a pattern read off a photo of flat 109 to a
measurement off this type's own drawing**, and the width now triangulates three
ways (derived 2939, flat 53's printed 2930, this 2963.9) inside 34 mm.

**Slab extension**: a closed rectangle **1800 × 370 mm**, projecting **320 mm
beyond MC's outer face**, 50 mm wider than the window opening each side. ⚠️ **Not
a wall; never a quantity.** It appears at this window only — MB's carries a 70 mm
line in the same place, and whether that asymmetry is real is unresolved.

**Suggested furniture**: five dashed runs, orange, dashed, own layer. ⚠️ **The
source drawing has NO PDF dash operator at all** — the dashes are exploded into
short segments, so furniture is graphically identical to fabric and only its
~90 mm gap rhythm tells them apart. **❓ Which two are the wardrobes, and is
"drifted to the right" a fault in the developer's suggestion or the reason to
ignore it?**
