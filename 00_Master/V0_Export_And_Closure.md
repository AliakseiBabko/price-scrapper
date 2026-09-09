# The v0 export, the closure gate, and what each review round fixed

Split out of `V0_Geometry_Status.md` on 2026-09-09, which had reached 454
lines against a 400-line backstop. That page keeps what v0 IS and where it
stands; this one keeps the EXPORT, the gates that check it, and the record of
what each round of the owner's review and the `V0_DXF_RASTER_FIDELITY`
dialogue actually corrected.

> **The gate to run is `tools/layout/check_dxf_closure.py`.** It rasterises the
> wall union and needs no raster plan, so it cannot be circular, and
> `scripts/dxf_closure_selftest.py` proves it rejects six seeded defects.

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

### ✅ The DXF is now CHECKED against the raster, by measurement

`tools/layout/overlay_dxf_on_raster.py` → `_Drawings/review/v0_dxf_over_raster.png`.
Owner, 2026-09-09: *"I want you to check yourself and not come back to me showing
the same result."* Fair, so the check is now a number that can be re-run after
every change.

**Registration matters and two attempts were wrong before this one:**

- ⚠️ `dimension_tolerance.json` records `mm_per_px: 20.6302` for this plan. **It
  cannot be right** — the file is 879 px wide and the flat is ~10.2 m, so ~12–13
  mm/px. Not used.
- ⚠️ Fitting the **ink bounding box** gave **6.61% anisotropy**, because the box
  includes the dimension strings and room labels printed outside the walls.
- ✅ Fitting on **wall lines** — rows and columns whose ink spans ≥30% of the
  drawing, matched against the DXF's own face coordinates — gives **1.96%
  anisotropy**, consistent with the 1.66% aspect error already recorded for this
  raster. **13 of 21 x-faces and 19 of 28 y-faces land on a drawn line.**

⚠️ **And the first metric was flattery.** A hit/miss probe at 90 mm found ink for
23 of 24 walls, while the overlay plainly showed walls off their lines — at
13 mm/px, 90 mm is 7 px and almost everything "passes". Replaced with the
**distance in mm from each sampled edge to the nearest ink**.

**Result: 19 of 24 walls have every sampled edge within 60 mm of drawn ink.**
The five that do not:

| wall | worst | mean |
| :--- | :--- | :--- |
| R9 | 142 mm | 42 mm |
| G2 | 123 mm | 61 mm |
| G4C | 103 mm | 44 mm |
| G4d | 103 mm | 31 mm |
| G8 | 90 mm | 34 mm |

⚠️ The registration's own noise is roughly ±13–26 mm (one to two pixels), so
**60–90 mm is marginal and 90–142 mm is real.**

### ✅ The envelope bug that amputated the лоджия

`clip_to_envelope()` built the flat's box from axis-aligned **faces** only. The
лоджия's south side is the **diagonal glazing**, so no horizontal face existed
down there and the floor came out at y = 7490.4 — above the лоджия, which reaches
about y = 6100. **The flat is an L, and clipping an L to the bounding box of its
main block deletes the other leg.**

Consequences, both now fixed: M2's solid was cut from 1945.7 mm to 1490.2 against
a recorded 1850, and every лоджия wall below the line vanished. The envelope now
takes the glazing's own extent as well — floor **6120.6** — and **M2 moved from
−360 mm to +95.7 mm** against its recorded length.

### ✅ THE OWNER-NAMED GEOMETRY IS CLOSED — 2026-09-09

CODEX, `V0_DXF_RASTER_FIDELITY` round 1: *"Claude did the interesting work
instead of completing the asked work… A better measurement of an unfixed result
does not answer that complaint."* Correct. So this round closed the geometry
first and rebuilt the check second.

**`tools/layout/check_dxf_closure.py` — PASS.** No cavities, no unsanctioned
overlaps, 24 of 25 walls present and the 25th explicitly quarantined.

| what the owner named | now |
| :--- | :--- |
| **R7 × MC** cavity, *"most likely MC"* extends | ✅ closed, MC extends onto R7 |
| **MA × M2** 70 mm gap | ✅ closed, M2 extends onto MA |
| **M6b** *"extension of R8"*, missing | ✅ placed, flush with R8's face at 6131, **quarantined** |
| MB / R2 / R9 *"filled with the insulation"* | ✅ recorded as `insulation_infill` — **never to be closed by lengthening masonry** |

**Two new canonical files**, both companions to generated data rather than
hand-edits that `--write` would wipe:

- `junction_directives.csv` — junctions `classify()` cannot emit, with
  `closure_kind` (`wall_extension` / `insulation_infill` / `unresolved`), who
  extends, source and status. Merged deterministically into the ledger.
- `wall_placement_directives.csv` — M6b, as **quarantined provisional geometry**.
  Its **thickness is still unresolved** (no 200 mm solid exists; the drawing
  shows 300/150/100 there) so it is excluded from quantities, IFC and any
  construction dimension.

### ⚠️ Three of my own errors this round, all caught by the new gate

**1. My closure test was wrong.** It asked *"do the two rectangles overlap in
both axes"* and reported **six of eight corners open** when they were solid — MA
ends exactly on R8's face and R8 spans the corner, so the x-overlap is zero and
the corner is nonetheless filled. **Closure is a coverage question, not a
pairwise-overlap question.** Replaced with a rasterised wall union.

**2. The corner extension over-shot.** Extending by a flat thickness pushed R8
350 mm past MA's far face and into G8. **Now clamped to the other wall's far
face**, so the corner is exactly solid and no more.

**3. `J_G4a_G4b` was wrong and is withdrawn the same day.** The 25 mm gap is
along **y**, and G4b runs EW — extending it along its own axis could never close
it, and the extension drove G4b 250 mm into R1b. **There is no void there at
all: R1b continues above G4a on the same x band.** The row is kept as
`withdrawn` so the mistake is auditable, and G4b's `owns_corners_mm` reverted.

### ✅ And the check is now watched to fail

`scripts/dxf_closure_selftest.py`: the real export must pass, and **six seeded
defects must each be rejected** — three corner voids, an unsanctioned overlap, a
deleted wall, a 500 mm global shift. **All six rejected.**

⚠️ **The flood-fill alone was not enough and the selftest proved it:** pull MC
300 mm off R7 and the void it opens **connects to the room**, so the fill sees
one large empty region and calls it a room. An explicit **per-corner square
coverage** assertion was needed. ⚠️ **And one seed was itself wrong** — shrinking
R1a's *east* end does not touch the R1a/R1b corner at its *west* end, so the gate
was right to accept it. **A negative case has to break the thing it claims to.**

### The raster overlay is now advisory, and says so

CODEX rejected it as flattering and partly circular: it fits the registration on
the DXF's own wall faces, then scores those faces against wall-adjacent ink;
four probes per wall; untyped ink; and it **returned 0 while five walls breached
its own threshold**. All true. It now **exits 1 on a breach and 2 on unusable
registration**, and its header states plainly that
`check_dxf_closure.py` is the gate that decides and this is a displacement smell
test.

⚠️ **Still outstanding from that review**, and not done: a control-point
registration using non-wall features, a frozen wall-only raster mask, per-wall
IoU, and dense boundary distance. Until those exist the raster numbers are a
smell test only.

**Round 2 of `V0_DXF_RASTER_FIDELITY` found five of this page's claims untrue in the committed tree**, and the defect classes the closure gate had been missing are recorded in [V0_Closure_Gate_Failure_Classes.md](V0_Closure_Gate_Failure_Classes.md).
