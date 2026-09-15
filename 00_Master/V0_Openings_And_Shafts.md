# v0 — the openings and the ventilation shafts

How every opening in this flat is FOUND, and the two elements that are not
walls but carry finishable surface. Split out of
[`V0_Geometry_Status.md`](V0_Geometry_Status.md) on 2026-09-15 because that
page had begun to organise itself by the DATE facts arrived rather than by
topic — the fragmentation defect standing rule 8 names — and had reached the
400-line backstop. Nothing here is new; the headings are.

## The openings — the drawing had them all along

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

## The shafts — V1 and V2

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

### ⚠️ V2 carries an ENCLOSED NICHE, and is drawn as one piece

Owner, 2026-09-15: *"this niche is enclosed and flush with the venting shaft —
it looks like a one piece from outside."* The 214.9 mm between the shaft proper
(north face 15775.3) and the top wall's inner face 15990.2 is **an enclosed
niche, not a void**, finishing flush with the shaft.

**The drawn element is therefore 899.9 = 685.0 shaft + 214.9 niche**, running
y 15090.3…15990.2 hard against the top wall. ⚠️ **The two figures are kept apart
because they are different things**: `shaft_proper_mm` is the 4th-floor duct
footprint a services drawing needs, the combined depth is what a FINISH take-off
needs — the niche adds surface and removes floor exactly as the shaft does.

✅ **It also explains the corroboration above**: the 214.9-against-a-printed-200
that helped anchor V2 is the NICHE, not a gap. The anchor is unchanged and O10
still closes at 1440.0 against 1455.

## The window frame subdivision — what part 2 actually needs

`data/canonical/window_frames.csv`, added 2026-09-15 from four photographs the
owner pointed at. **This is the piece the план alone cannot supply**: a plan
gives an opening's width and position, and the 3D model needs to know how the
frame is divided.

| opening | wall | pattern | evidence |
| :--- | :--- | :--- | :--- |
| **O2** | MB | **2 sashes, 1 mullion, NO transom** | `ext1` (**ours**, outside) + `b6f0` (apt 53, inside) |
| **O3** | MC | **2 × 2 — 1 mullion AND 1 transom**, four panes | `ext1` (**ours**, nearly square-on) + `bdc7` (apt 53, inside) |
| **O4** | MA | **window leaf + full-height DOOR leaf**, 1 mullion | `9db4` (apt 53) + the recorded O4a/O4b |

Two of the four photographs are of **this flat**, not a comparable, and they are
the ones that carry the pattern for O2 and O3.

### ⚠️ The pattern is measured. The sizes are not.

**A photograph settles topology and nothing else here.** How many sashes there
are, whether a transom exists, which leaf is the door — those are countable, and
a photo is the right instrument. A member width is not: the visible centre band
scales to ~140 mm off an oblique shot with no scale reference in frame, which is
±100 at best under standing rule 9. **Every member size in the table is a
nominal pending a tape measure, and each row says so.**

The 0.5 splits are the same: the **default** for a two-sash unit, not a
reading. O3's panes measure ~17% apart on the exterior photo — ~40 mm at
1763 — which is inside the reading error, so the default stands rather than
pixels being adopted.

⚠️ **The two photos disagree about O3's transom height and the exterior one
wins.** `ext1`, nearly square-on, puts it within ~3% of mid-height; `bdc7`,
oblique and from inside, reads 57/43. An oblique interior view compresses the
far part of a vertical division, so the near-frontal shot is the better
instrument. **At a 1985 opening the two readings differ by ~140 mm** — worth a
tape measure before anything depends on it.

### ⚠️ Reading a MIRRORED photo: O4's door is on the EAST

`9db4` is apartment 53, which is **mirrored**, so its left and right cannot be
carried across — that is exactly the error the `_Survey` folder names in every
directory. What *can* be carried is a **relationship that survives mirroring**:
in the photo the door leaf sits on the side with the **short wall reveal** and
the window leaf on the side with the long run.

In our flat O4 spans x 4351.0…5731.0, leaving **1120.1 to G4a on the west** and
**325 to G8 on the east** — so the short reveal is east, and the door goes east.
The mullion lands at 4951.0, which is 4351 + the recorded 600 leaf, so its
position comes from the record rather than from the photo.

### In plan, only the vertical members exist

O3's transom is recorded and **deliberately not drawn**: it is horizontal, so it
belongs to elevation, and a plan showing it would be lying about what a plan is.
`check_dxf_closure.py` asserts every vertical member is drawn where recorded and
that nothing extra is, with its own seed — a new drawn class with no seed is a
class nobody has watched fail, and these are DRAFT-grade photo evidence, so they
need the gate more than the walls do.

