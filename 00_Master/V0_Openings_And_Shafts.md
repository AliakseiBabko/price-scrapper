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

`data/canonical/window_frames.csv`.

> [!CAUTION]
> ⚠️ **REBUILT 2026-09-15 FROM THE RECORD, after the owner pointed out that
> these measurements were already made and I had gone off and re-derived them
> from photographs.** He was right, and it is the same failure this project
> already names on its own front page: *"re-deriving the wall inventory was
> reinventing the wheel and should never have been attempted."* The rule is not
> "photos are bad" — it is **search the record before reaching for an
> instrument.**

### What the record already settled, and I should have read first

| | figure | grade |
| :--- | :--- | :--- |
| O3 | sill **266**, height **1985**, width **1763**, head **2251** | **TAPE**, 2026-09-07 |
| O2 | width **1760** | **TAPE** |
| O4a | sill **735** | **TAPE**, and `bc18` agreed to **1 mm** by an independent method |
| all | a head standard at **~2240–2250**, ~250 below the ceiling | derived, consistent across O3 and O4b |

None of that is re-derived here. **`FLAG_O3_window_proportions_do_not_fit` was
opened on 2026-09-06 and closed by that tape on the 7th** — and the tape
vindicated `9902` exactly: measured aspect 1985/1763 = **1.126** against 9902's
square-on 1.11–1.16.

### The patterns

| opening | pattern | agreeing photos |
| :--- | :--- | :--- |
| **O2** | 2 sashes, 1 mullion, **no transom** | `b6f0`, `ext1` (ours) |
| **O3** | **2 × 2** — mullion *and* transom | `9902`, `bdc7`, `ext1` (ours) |
| **O4** | window leaf + full-height **door** leaf | `bc18`, `9db4` |

### Positions come from `9902`, and only as RATIOS

⚠️ **The record already states what 9902 can and cannot do**: *"it carries NO
SCALE — nothing of known length lies in the window's plane"*, but it is the one
square-on shot in the survey, so **its proportions are sound where every oblique
shot's are not.** So it supplies fractions, never millimetres:

- **mullion at mid-width** — the two sashes measure 277 and 282 px, **1.8%
  apart**
- **member ≈ 195 mm** — 78 px of a 705 px frame, ×1763; two sash frames plus the
  mullion profile, a normal PVC centre band

### ⚠️⚠️ O3's transom is the LEAST settled figure in the set

| reading | from top | instrument |
| :--- | ---: | :--- |
| `9902` | **0.56** | square-on, planar — upper pane taller |
| `bdc7` | 0.57 | oblique interior — agrees |
| `ext1` (ours) | **0.457** | oblique, partly behind foliage, against blockwork — **opposite way round** |

Two against one, and the two are the better instruments, so **0.44 above the
sill** is recorded — about 874 above a 266 sill, **~1140 above the floor**.
⚠️ **But the spread is ~0.10 of 1985 ≈ 200 mm, far too coarse for a joinery
order.** A tape settles it outright and nothing should be ordered against it
until one does.

### O4's split was already resolved — and the door is EAST

Three readings agree on the *pair* of numbers: the owner's survey (600), my
2026-09-05 photo split (620/760), and `bc18` corrected for perspective
(583/772). **The dispute was never the widths, only which leaf is which** — and
`bc18` settled it, because there the door stands **open**, so its aperture is
unambiguous: **door ~770, window ~600.**

⚠️ `bc18` and `9db4` are both **mirrored** flats. What survives mirroring is that
the door sits on the side with the **short wall reveal**; our O4 leaves 1120.1
to G4a west and **325 to G8 east**, so the door is east and the mullion lands at
4351 + 600 = **4951.0**.

**A constraint `bc18` gives free:** the door opens **inward, into the 9.36
room**, so a ~770 mm swing must stay clear in front of it — a layout fact, not a
geometry one.

### In plan, only the vertical members exist

O3's transom is recorded and **deliberately not drawn**: it is horizontal, so it
belongs to elevation, and a plan showing it would be lying about what a plan is.
`check_dxf_closure.py` asserts every vertical member is drawn where recorded and
that nothing extra is, with its own seed.

⚠️ That seed initially pinned the mullion's left **edge**, so raising the member
from 120 to 195 mm made it find nothing — **its own assert caught that**, which
is what a seed is for, but a seed that depends on a figure it does not own will
keep going stale. It now locates by the mullion's **centre**, which is the thing
that means something.
