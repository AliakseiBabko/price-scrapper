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

## The exported intermediate layer, and reading it back

**Three artefacts, regenerated 2026-09-09 from current code:**

| artefact | what it is |
| :--- | :--- |
| `data/canonical/v0_named_walls_placed.json` | the intermediate layer — 24 of 25 named walls on vector solids, segmented on drawn joints |
| `data/canonical/v0_elements_extracted.json` | лоджия glazing, decorative slab, suggested furniture |
| `data/cad/dxf/v0_developer_layout.dxf` | the AutoCAD export — 78 entities, extent **10205 × 10051 mm** |

**`tools/layout/render_dxf.py` renders the DXF by READING THE DXF**, not the JSON
it came from — so `_Drawings/review/v0_dxf_readback.png` is evidence about the
exported file rather than about agreement between two of my own scripts. It is
also the read half of the round trip the accepted design calls for.

### ⚠️ What reading it back exposed, that the JSON render hid

**`V0-WALL-LOGGIA` contains ONE polyline, not two, and there are 24 wall labels
for 25 walls** — M6b has no geometry at all, because no 200 mm hatched solid
exists where the model puts it. On a picture drawn from the JSON this was a thin
bar that looked plausible; in the DXF it is simply absent, which is the honest
representation.

**The openings are measurably wrong, and not uniformly.** Measured against each
host wall's own extent:

| | |
| :--- | :--- |
| inside their host wall | O8, O7, O1, O4, O2, O3 — **6 of 8** |
| **outside it** | **O6 by 766 mm**, **O5 by 1156 mm** |

→ ⚠️ **And those two sit on G4d and G6 — the two walls whose own laid length
disagrees most with the model.** So "openings are raster-routed" is not the whole
diagnosis: **where the wall itself is misplaced, its opening cannot land on it
regardless of which transform positioned it.** Fixing the transform alone would
move O5 and O6 onto walls that are themselves wrong.

**The лоджия glazing floats free** of M2 and the absent M6b, bottom-left — three
disconnected pieces where the flat should close.

### ✅ Four corrections from the owner's read of the DXF — 2026-09-09

**1. Corners were VOIDS. Now closed.** Owner: *"if I have this corner, R1b and
R1a, one of this wall should go up to the end of the another one… we need to
factor in the thickness of the wall to have a closed corner, which is actually
the case in reality."* → Walls were being drawn at their **`clear_mm`** run,
which is what a tape inside the room reads, so every L-corner came out an open
square. `solid_mm` = `clear_mm` + the corners a wall **owns**, and
`wall_corners.csv` already said who owns which. Applying that ledger in the
exporter closes **all five** with no double count, because exactly one wall of
each pair is extended:

| corner | extended | by | at |
| :--- | :--- | :--- | :--- |
| C_R1a_R1b | R1a | +250 | its start, over R1b |
| C_G3_R2 | R2 | +250 | its end, over G3 |
| C_MA_R8 | R8 | +300 | its end, over MA |
| C_MB_R8 | R8 | +300 | its start, over MB |
| C_MB_R9 | R9 | +300 | its start, over MB |

**2. The dashed lines are gone.** Owner: the ones in the G3 / kitchen area are
*"not necessary here, absolutely"* — a CAD leftover, not a decision. The
`V0-SUGGESTED-FURN` layer no longer exists in the export. The runs stay in
`v0_elements_extracted.json` if ever wanted.

**3. ✅ O3 and the slab are now aligned exactly — 0.0 mm on both edges.** Owner:
*"these O3 and new slab extension should be aligned… you can check the vector
drawing."* He was right, and checking it corrected my own reading:

> Inside MC's thickness band the near-full-depth reveal lines are at **10235.9
> and 12035.9**. So the **structural opening is 1800**, and the 10286…11986 pair
> I had taken for the reveal is the **1700 window unit sitting 50 mm inside it**.
> The slab is 10235.9…12035.9 — **the same two numbers.** The developer drew the
> slab as exactly the structural opening, and the raster fit had been moving the
> opening 106 mm off it.

**Openings now come from the vector**, via `tools/layout/place_openings.py`,
which snaps each hatch-gap to the drawn reveal lines. Two more confirmations
fell out: **O4 measures 1380.0**, exactly what `wall_openings.csv` records for
the лоджия opening, and O2 measures 1800 against a named 1760.

⚠️ **Five internal doors are now OMITTED rather than drawn wrong** — O1, O5, O6,
O7, O8. Their reveals are drawn differently in 75/120 mm walls, and no drawn gap
matches their recorded widths. **An omission is honest; a plausible position is
not.** This also corrects an earlier diagnosis of mine: O5 and O6 sat 1156 mm and
766 mm outside their host walls, and I attributed that to the transform alone —
but they are on G4d and G6, the two walls whose own laid length disagrees most
with the model, so the wall placement was implicated too.

**4. ⚠️ The лоджия still does not close, and that one needs the owner.** M2 is
drawn axis-aligned where the real wall splays, and **M6b has no geometry at all**
because no 200 mm hatched solid exists where the model puts it — the vector shows
300 / 150 / 100 there. `project_decisions.md` already flags M6b's 200 mm as
provisional and under revision. **❓ Which is it?** Until that is settled the
лоджия is three disconnected pieces: M2, the absent M6b, and the glazing.

### ⚠️ Two defects the owner spotted from the DXF — 2026-09-09, both real

**1. `R8`'s recorded `solid_mm` was arithmetically wrong, and nothing checked
it.** R8 **owns two** corners — `C_MA_R8` and `C_MB_R8`, +300 each — on a 1490
clear run, so `solid_mm` must be **2090**. It recorded **1790**, which is R9's
figure; R9 owns **one** corner and is correctly 1490 + 300 = 1790, and R9's own
note even reads *"see R8"*. **The 1790 was copied and never updated.** Corrected
to 2090.

⚠️ **`build_wall_corners.py` had PRINTED the heading *"solid_mm = clear_mm + the
corners a wall owns"* and the per-wall gains for weeks without ever comparing
them to the file.** It now checks the invariant and fails on a breach. Same class
as everything the adversarial rounds found: **a number reported is not a number
verified.**

**2. My exporter double-counted the corners.** Walls laid from `solid_mm` — which
already includes owned corners — then had them added again by `close_corners()`.
**R8 drew at 2390 against a true 2090; R9 at 2090 against 1790.** The owner saw
the over-extension on the drawing before any check did. Fixed: everything is now
laid at **`clear_mm`**, corners are added once, and **the exporter reports the
invariant `drawn == solid_mm` on every run**.

**Result: 16 of 24 walls now draw to their recorded `solid_mm` within 15 mm**,
including R8 and R9 exactly. The remaining eight are listed by the exporter each
run: G4d −910, M2 −360, G7 +250, MA +225, R1b +145, G4C −120, G4b −120, G4a −25.
⚠️ **G4d and G4b look transposed** — G4d draws 1915 which is G4b's recorded
length, and G4b draws 1795 which is a chain figure from the small room. That is a
matching error in the wet block, not a length error.

### ⚠️ Corners still open, measured

`wall_corners.csv` holds **five** corners. The flat has more, and `classify()`
does not detect these because the two walls are tens of millimetres apart rather
than touching:

| corner | gap |
| :--- | :--- |
| **R7 × MC** | point contact — a 250 × 300 **void**. ⚠️ **Owner: extend MC** |
| **MA × M2** | **70 mm** |
| R1a × G4C | 380 mm |
| G8 × MA | 175 × 50 mm |
| G4a × G4b | 25 mm |

**Owner, 2026-09-09, on the external ones:** the gaps at MB / R2 / R9 *"are filled
with the insulation, another layer which lays on top of the external walls"* — so
those close in reality through the external insulation, not by extending a wall.
**That is a different closure mechanism and must not be modelled as a wall
extension.**

**❓ The ledger needs extending to cover the corners `classify()` misses**, with
MC owning R7 × MC as directed. It is generated by `--write`, so these belong in
an owner-directed companion file, the same pattern `structural_assemblies.csv`
already uses — not hand-edits that the next regeneration wipes.

### ❓ R6, R7, R8, R9 — the owner says all four should be equal

His recollection is that all four are the same and about **1450**, possibly 1490.
**The model and the drawing both disagree with that, and they agree with each
other:**

| | recorded `clear_mm` | drawn from the joints |
| :--- | :--- | :--- |
| R6 | 1750 | **1739.7** |
| R7 | 1750 | **1749.7** |
| R8 | 1490 | no joints found — laid from `clear_mm` |
| R9 | 1490 | no joints found — laid from `clear_mm` |

So the drawing puts R6 and R7 at ~1740–1750, not 1450, and R6/R7 are recorded
*"printed on the plan"*. **Two pairs at 1750 and 1490 — not four equal.**
⚠️ **Not changed.** Four owner-confirmed lengths, two of them printed, should not
move on a recollection the drawing contradicts. **❓ Worth a second look at the
plan, or a tape once the building completes.**

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
