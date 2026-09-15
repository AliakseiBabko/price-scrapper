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
