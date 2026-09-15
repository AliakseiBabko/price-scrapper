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

**Updated 2026-09-15 against the gates' own output.** Everything below this
heading used to describe round-4 state and had drifted badly: it claimed 12
junction gaps when there are none, said `check_wall_junctions.py` and
`build_wall_corners.py` "have not been run" when both run and pass, listed
out-by figures (G7 +820, G4d −671, M2 −360) the exception ledger had long since
superseded, and still called M6b's 200 mm provisional five days after the owner
confirmed it. **This page is the one a person reads to learn where v0 stands, so
a stale page here is the same defect class as a stale caption on the review
drawing** — which is gated, precisely because it drifted twice. This section is
now written from `check_dxf_closure.py` and `wall_extent_exceptions.csv`.

### The extent exceptions — 8 rows, 6 open

| wall | drawn | recorded solid | delta | state |
| :--- | ---: | ---: | ---: | :--- |
| R8 | 1789.7 | 2090 | **−300.3** | open — `clear + owned corners` over-counts; 1490 off the vector is not a face-to-face inner dimension |
| R9 | 1540.0 | 1790 | **−250.0** | open — R9 laid at `clear_mm` inside its own 1740 solid |
| G7 | 3499.7 | 3250 | **+249.7** | open — **the same defect as R9**, one error showing as two rows: G7 filled the 250 R9 left behind |
| MA | 3050.1 | 2825 | **+225.1** | open — drawn correct at both ends; the record is 225 short |
| M2 | 2373.1 | 2150 | **+223.1** | open — 57.7 is the deliberate лоджия closure; the remaining 165.4 is not accounted |
| R1b | 1345.0 | 1200 | **+145.0** | open — a rectangular leg carved out of a continuous casting; use the assembly footprint |
| M6b | 1439.9 | 1170 | +269.9 | **accounted** — every term is a deliberate recorded move |
| G4a | 3545.0 | 3570 | −25.0 | **accounted** — inside the ±50 build tolerance |

**R9 + G7 is one fix, and the arithmetic is already done:** butting G7 on R9's
real face at 9350.6 gives R9 1790 exactly and G7 3249.7 against 3250. It also
restores this project's own rule — a ≤120 mm partition meeting a frame member
butts it, and the frame does not yield. **It is a change to the placement lay,
not to a table, and it is the next piece of deliverable work.**

### Resolved since this section was last written

- **✅ Junctions: zero.** `check_wall_junctions.py` passes on 25 runs — no
  overlap, no gap, every L-corner owned in `wall_corners.csv`.
- **✅ M6b's 200 mm is owner-confirmed** (2026-09-10), no longer provisional and
  no longer quarantined. The drawing still disagrees and that is *recorded*
  rather than reconciled — `wall_placement_directives.csv` (P_M6b).
- **✅ The two ventilation shafts are in the model** (2026-09-15), below.
- **✅ All ten openings are hosted** (2026-09-15), below.

## The 2026-09-15 round: the shafts and the six missing openings

The owner compared the DXF readback against the approved wall model
(`_Drawings/review/wall_model.png`, v24) and found the walls aligned and
everything else not. `wall_materials.json` states the approved inventory as
**"25 walls + 2 ventilation shafts, 10 openings, ALL TEN HOSTED"**; the DXF held
**25 walls, 0 shafts, 4 openings**.

### The openings — the drawing had them all along

`place_openings.py` reported five doors as *"no drawn gap inside &lt;wall&gt;
matches its width"*. That message was true of what the code looked at and false
about the drawing. It read one span source; there are three.

| source | what it is | supplies |
| :--- | :--- | :--- |
| `candidate_openings` | an unhatched stretch WITHIN one solid | **empty for every internal door in this flat** |
| `bridged_openings_mm` | a doorway that splits its wall into TWO solids, recorded by the merge | O8 (1009.9 vs 1010), O1 and O7 (710.0, 710.0 vs 710) |
| an **inter-wall gap** | the doorway is not in a wall at all — it is the space BETWEEN two walls on one line | O6 (910.0), O5 (910.1), both vs a recorded 910 |

⚠️ **The middle row is the uncomfortable one.** `raster_fidelity.py` already
consumed `bridged_openings_mm` to exclude opening spans from its metric, and
`render_vector_extraction.py` already drew those same gaps in red captioned
"NO OPENING PLACED". **Two consumers could see the doorway and the placer could
not** — and `wall_blocks.csv`'s own G4C note had already written the two 710
spans down by coordinate. Nothing was missing; nothing was even unmeasured.

⚠️ **Width alone cannot tell O1 from O7** — both are 710 mm in G4C and both gaps
are drawn, so width ties and whichever came first used to win. Width is now a
filter and POSITION is the ranking key, using the basic-plan px span through the
identification fit. That fit is unfit for geometry (3.3% anisotropy, 93 mm
residuals) and entirely adequate for choosing between two gaps 710 mm apart.
**No geometry comes from it** — exactly the role it already has for walls.

**O10 was worse than missing — it was invisible.** It had no span row, so the
placer's loop never visited it, so it never landed in `unplaced`, so it never
reached the review drawing's "still open" caption, which counts only `unplaced`.
Absent from the model *and* absent from the list of what is absent. It is placed
now from its two immovable flanks: R5's top face 13650.3 to V2's south face
15090.3 = **1440.0** against a recorded 1455.

### The shafts — V1 and V2

They are **not walls** and must never be counted as walls. Owner: *"we need to
include the ventilation shaft, which is next between R3 and R5. This is not a
wall, but it is a structural element [that] will surface a wall."* They **add
finishable surface inside a room and subtract floor**, so a take-off that
iterates walls under-counts. Own layer `V0-VENT-SHAFT`, own table
`data/canonical/ventilation_shafts.csv`, grey on the review drawing.

⚠️ **Their footprints are the ONLY geometry in v0 not taken from the vector
plan**, and deliberately so: the vector is the DETAILED plan, which draws the
floors-10-and-up variant with **doubled** vent sections. `room_schedules.json`
is explicit — *"USE THE BASIC PLAN for the vent shafts"*.

- **V1 = 700 × 400**, x 3380.9…4080.9, y 15590.3…15990.3.
  `wall_materials.json` had flagged V1 as *needing a careful re-measurement*;
  the approved wall model is that re-measurement. **Position is a chain, not a
  pixel reading**: the printed chain across the туалет is 150 | 700 | 290 = 1140
  from R1b's east face 3230.9, and 3230.9 + 1140 = 4370.9 lands on hatched solid
  S20's west face at **4370.9 — a 0.0 mm closure against an element the chain
  never touched**. The 150 is printed on the plan, not invented.
- **V2 = 400.1 × 685**, x 8980.8…9380.9, y 15090.3…15775.3. x is hatched solid
  S11's own extent; the 685 is the 4th-floor sub-type from the basic plan.
  Anchored on S11's hatch-validated south face and **corroborated two
  independent ways**: the gap left to the top wall is 214.9 against a printed
  200, and O10 comes out 1440.0 against a recorded 1455. Both agree to 15 mm,
  and the alternative anchor — an exact 200 offset — moves it 14.9 mm, inside
  the ±25 nominal tolerance, so the choice does not matter at this grade.

### The gates that now cover this

**A gate nobody has watched fail is not a gate**, so all of it is seeded.
`check_dxf_closure.py` gained a non-wall element section that reads the DXF back
and asserts every shaft and every placed opening is drawn on its recorded
footprint, plus the roster check that would have caught O10 — *a named opening
in no list at all*. `dxf_closure_selftest.py` is **28 seeded defects**, up from
24: a deleted V1, a V2 slid 400 mm, a deleted O10, and an opening named but in
no list. Each was watched failing, and each fails with its own finding kind.

### ⚠️ A false FAIL, fixed — the gate cried wolf

Run on a default Windows console, `check_dxf_closure.py` **exited 1 with the
finding `stale_review_drawing`** while the drawing was byte-identical and the
line immediately above said so. A bare `except Exception` was catching a
`UnicodeEncodeError` raised by its own SUCCESS print — cp1252 cannot encode
`лоджия` — and filing the crash under the name of the defect it had been looking
for. The verdict depended on which terminal ran it.

Both halves are fixed: `tools/lib/console.py` reconfigures stdout to UTF-8 in
every layout tool's `main()`, and the catch-all now reports
`review_drawing_check_errored` and says in words that it is not a finding about
the drawing. **A checker that cannot run must say that, and must never borrow
the name of the defect it was hunting.** The same crash was taking down
`structural_assembly_selftest.py`.

### The review drawing now sits ON the plan

Owner, 2026-09-15: *"I want the base image like a raster image as a basis to
show the difference."* `v0_dxf_readback.png` now draws the model over the
developer's own drawing in pale grey, so a wall in the wrong place is visible
rather than merely measurable.

⚠️ **The underlay uses the FROZEN, HASHED registration** that
`raster_fidelity.py` measures against — fitted between the PDF's hatched wall
faces and the raster's own wall lines, **with the DXF deliberately not
consulted**. Fitting a fresh transform here would rebuild exactly the
circularity CODEX rejected in the old `overlay_dxf_on_raster.py`: a picture that
makes the model look right because it was aligned *to* the model. If the frozen
evidence is missing the drawing falls back to a white ground rather than showing
an unregistered overlay.

**Outlines, not fills.** Owner, 2026-09-15: *"do not fill in the polygons of
the wall segments, because in this case I won't see the wall overlapping —
assign a colour just for the contour, not for the filling."* Right, and it
matters more than it looks: **a filled polygon drawn later paints over an
earlier one, so an overlap is precisely the thing a fill hides.** The corner
overlaps this model deliberately sanctions — a wall extending over its
neighbour to own the corner, all eight of them in `wall_corners.csv` — were
invisible in the filled version. Contours also let the plan's own hatching read
through, so a wall can be checked against the solid it sits on.

**What the picture makes visible that a number did not:** MA's **+225.1** open
exception is now something you can see — its magenta bar runs past the plan's
external corner at the лоджия. The exception ledger has always said so; the
drawing never showed it.

**V2's anchor, checked because the picture raised it.** On the detailed plan the
shaft is drawn 1140 long — the floors-10-and-up variant with two sections — and
our 685 covers only part of it, which makes the eye ask which part. Ink density
cannot answer: 0.559 for our placement against 0.561 for the opposite anchor and
0.541 centred, because the whole area is dense with channel linework and
dimension text (a solid wall measures 0.368 by the same test). **The chains
answer decisively.** Anchored on S11's south face, extending north: the gap to
the top wall is 214.9 against a printed 200, and O10 is 1440.0 against a
recorded 1455 — both within 15 mm. Anchored the other way: **+299.9 and −300.0**.
Two independent chains, both off by exactly 300 for the alternative.

## The 2026-09-15 owner review of the contour overlay

Seven comments drawn on `v0_dxf_readback_commented.png`. All seven are applied.

| what he marked | what it was | outcome |
| :--- | :--- | :--- |
| *"missing segment of the R9. It should be aligned with R8"* | the known R9/G7 pair — R9 laid at `clear_mm` from the LOW end of its own solid, so its corner gain had nowhere to land and G7 swallowed the 250 | **both exceptions closed**; R9 1790.0 vs 1790, G7 3249.7 vs 3250 |
| *"external insulation should not cover all the wall, just the exposed segment"* | R8's band ran 0.045 m² through MA's body, R9's 0.045 m² through MC's, plus three band-on-band overlaps | occlusion rule: a face another wall abuts carries no external layer |
| *"missing pieces of insulation"* ×3 | every arrow was at a wall END, where the band stopped instead of turning the corner | the layer is carried around any end no other wall abuts |
| *"this niche is enclosed and flush with the venting shaft"* | a 214.9 mm void above V2 that is actually an enclosed niche | V2 draws 899.9 hard against the top wall; 685 shaft + 214.9 niche kept as separate figures |
| *"draw it as another opening"* | O9 was exported as frame + bays + mullions only | drawn on `V0-OPENING`; the only non-axis-aligned opening, matched on a bbox |
| *"we don't need these small segments outside of MA M2 and R6"* | MA had inherited the extraction's ENVELOPE CLIP at x 2830.9 as its west face | trimmed to M2's face; exception +225.1 → **+125.1** |
| *"M2 should touch MA, insulation between them is most likely an error"* | reverses the 2026-09-10 instruction at this junction only | confirmed by the owner; the occlusion rule already produced it |

### Two that needed the owner, and why

**Where MA/M2/R6 should align.** The three west faces were 2830.9 / 2930.9 /
2980.8. ⚠️ **MA's was the extraction's envelope clip — where reading the
neighbour's structure stops — not a wall face**, and the frozen ink mask carries
**zero ink** in the 120 mm strip west of 2930.9 across y 6100..9100, so MA's
western 100 mm was drawn over blank paper. M2 is the alignment target because it
is the outermost of the two; R6 sits 49.9 inboard and protrudes past nothing.

**M2's west face.** Insulated over its **southern 570 mm only** (y 6977.2…7547.2,
150 mm on the low face) — our лоджия projects past the neighbour's there to meet
the glazing; the rest of that face is shared. ⚠️ **The drawing cannot corroborate
any of this**: there is no ink west of M2 at all, so the owner is the sole source
for both the extent and the fact of exposure, the same standing as M6b's 200 mm.
⚠️ **The 150 mm thickness is BY ANALOGY with M6b — same class, same thickness,
the лоджия's other external wall — and is NOT measured. It could as easily be
the 70 mm the MA/MB/MC façade carries.** The same answer suppresses MA's west end
cap, because MA's end and M2's face are the same plane.

`wall_blocks.csv` gained `insulation_from_mm` / `insulation_to_mm` /
`insulation_end_caps` so both are recorded data rather than code.

### ⚠️ An export that crashed AFTER its own report

The exporter hit `KeyError: 'face_lo_mm'` on O9 — the diagonal opening falling
through to the rectangle branch — and the crash lands **after** the wall report
prints. So a run showed a correct `MA drawn 2950.1` on screen while the DXF on
disk was still the previous export, and every downstream tool read a stale file.
**Found because `check_dxf_closure.py` compared the exception ledger against the
DXF and got 3050.1 where the exporter had just said 2950.1** — two independent
sources disagreeing, which is the whole reason the ledger is checked against the
drawing rather than against itself.

## Still missing

- **The лоджия's M2 / M6b are exported as axis-aligned bars** — the real
  enclosure is splayed. The glazing itself is correct and diagonal; its two
  flanking walls are not.
- **Window frame subdivision for MA / MB / MC** is not extracted. The geometry
  is on the drawing (the 19,49 window shows jamb frames and a central mullion
  pair) and **part 2, the owner's 3D model, needs it** — real openings with sill
  and head, not plan outlines.
- **The blue fixtures** — sanitaryware, kitchen — are in the owner's markup and
  not in the export.
- **The R9 / G7 250 mm**, above: one fix, arithmetic already done.
- **P1 and P2**, the wet riser group and the second sewer, are drawn on the
  approved wall model and absent from the DXF. They are immovable and recorded
  in `plumbing_anchors.csv`, but they are not part of the "25 + 2 + 10"
  inventory, so they are a separate later item.

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

## The export and its gates

The DXF export, the closure gate that proves the joints are clean, the raster
overlay and its limits, and the record of what each review round fixed:
[`V0_Export_And_Closure.md`](V0_Export_And_Closure.md).
