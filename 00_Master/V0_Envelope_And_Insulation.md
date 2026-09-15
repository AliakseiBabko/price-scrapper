# v0 — the envelope: what is outside, and the insulation that follows

The insulation layer is a CONSEQUENCE of what lies on the other side of each
face, so the two belong on one page. Split out of
[`V0_Geometry_Status.md`](V0_Geometry_Status.md) on 2026-09-15 for the reason
given in [`V0_Openings_And_Shafts.md`](V0_Openings_And_Shafts.md).

> [!IMPORTANT]
> **A face at the edge of our DRAWING is not a face on the outside of the
> BUILDING.** Every mistake on this page reduces to that one sentence.

## What is outside this flat

The owner supplied `_Inbox/_Visual_Drop/4th_floor_plan.png` on 2026-09-15, and
it settles questions the flat's own plan cannot, because **a face at the edge of
our drawing is not the same as a face on the outside of the building.**

- **This flat is `3Б/2+`, 45,48 / 69,44**, in the middle of a two-section house.
  ⚠️ That is the BASIC plan's identity, **not** the detailed vector plan's — the
  vector is `3Б/3+`, 45,49 / **69,09**, a different sub-type. This is the same
  split `room_schedules.json` already records: *"USE THE BASIC PLAN for the vent
  shafts, the туалет and прихожая areas, and the total — it is this flat. USE
  THE DETAILED PLAN for every dimension, because it is still the ONLY dimensioned
  source."*
- **East: `3А/2`, the mirror**, sharing a party wall. So **MC's east end is a
  party face, not an exposed one** — the end cap there is removed. The rule
  cannot derive this: nothing exists east of x 12946.0 in our model, so a flood
  from outside reaches it and it reads as exposed.
- **West: the neighbour's balcony `4,20(2,94)`**, and it is **shallower than our
  лоджия** `6,05(4,24)` — their parapet stops short and our enclosure carries on
  south to the glazing. ✅ **This independently corroborates the owner's ~570 mm**
  for M2's exposed stretch: scaling off M2's own recorded 1850 interior puts the
  projection at **~590 mm**, about 20 mm apart on a 787-px plan. Note theirs is an
  OPEN balcony with a parapet, not a glazed лоджия.

### ⚠️ "External insulation should not be inside the room"

R9 was the case and **occlusion could not catch it**. R9 sits on the step between
MB's façade line and MC's, so its east face is outdoors below MC and is the 19,49
room's interior above it — and nothing abuts that upper part, so the
abutting-wall test found it clear and insulated a face looking into a bedroom.

The test is now reachability: **a band must lie where a flood from outside the
flat can reach, crossing no wall.** ⚠️ **Only wall bodies are rasterised, never
the glazing** — that is what makes the лоджия come out as *exterior*, which is
correct, because a buffer is not a heated space and its flat-facing walls
*should* carry insulation. The heated rooms stay sealed because a wall is drawn
continuous **through** its own doors and windows; the openings are overlay
entities, not gaps in the rectangle.

⚠️ **The flood's 50 mm cell became a 50 mm NOTCH at every junction** — MB's band
started at 6181.0 where R8's face is 6131.0, MC's at 9430.9 where R9's is
9380.9. Owner: *"one surface interrupted by M6b + insulation layer."* **A surface
broken by a grid artefact is worse than one broken by a real element, because
nothing in the model explains it.** So the flood decides *whether* a stretch is
interior and the wall faces decide *where* it starts and stops: every span end is
snapped onto a coordinate the geometry already contains.

## The MA / M2 corner, reversed

Owner: *"overlap of MA and M2 — let MA go through; cut the M2 block which
overlaps with MA."* `C_M2_MA` now belongs to **MA**, and M2 is cut on MA's near
face 9050.6. **The old reasoning was spent rather than wrong**: J_MA_M2 argued in
2026-09-09 that *"the gap is along y and MA runs EW, so extending MA cannot close
it"* — true while MA's west end was still the envelope clip at 2830.9. Since
`P_MA_west` trimmed MA to M2's west face, **MA spans M2's full 200 mm**, so MA
running through closes the corner by itself.

Both deltas improved: **MA +125.1 → −74.9** (and the sign flipped — MA is now
drawn *shorter* than the record, so the open question is squarely whether its
recorded 2825 clear is right), **M2 +223.1 → +153.4**.

## ⚠️ The insulation is ONE SURFACE, and the photos settle it

Two exterior photos of the real building arrived on 2026-09-15, owner-marked
with our own segment ids — `ext1` (our flat, bare block) and `ext2` (another
flat of the same wall configuration, **caught mid-insulation**). Both are
indexed in `data/canonical/photo_positions.csv`; bytes gitignored, identity by
sha256 in `_Survey/manifest.csv`.

**`ext2` is the decisive one**, because it catches the system half-built:
mineral-wool boards going on over bare aerated block on M6b, render already
finished on MB. It shows, unambiguously:

1. **The layer WRAPS the corner as one continuous skin.** The boards turn from
   M6b's face onto MB's **without a break**, and the render closes over them.
   In the finished building the wall boundary underneath is invisible.
2. **The corner is REAL** — M6b does project and is perpendicular to MB. So the
   photo **confirms** v0's wall topology rather than contradicting it. The
   question was never where the walls are.
3. The build-up is mineral wool over block, rendered — exactly
   `building_spec.json`'s *300 block + 70 wool + render*.

Owner: *"one surface means literally one surface — currently you model M6b as a
wall extruding from the surface."* **The fix belongs to the LAYER, not the
walls.** The exporter drew one rectangle per wall, so a take-off iterating
surfaces saw four where the builder sees one, and every corner carried a seam
that exists in our data and not in the building.

`tools/lib/rectunion.py` now unions the bands into **connected runs and emits
each as a single closed polyline**. The grid is built from the rectangles' own
coordinates — every distinct x and y becomes a grid line — so a cell is wholly
inside or wholly outside and there is **no sampling error at any scale**. Six
surfaces result:

| surface | what it wraps |
| :--- | :--- |
| M6b + MB | **the corner the photo shows** |
| MB + MC + R9 | the south façade including R9's step return |
| MA + R8 | the лоджия's north face turning onto R8 |
| MA · MB · MC · M2 | the stretches a window or the лоджия cuts off |

⚠️ **A 19.9 mm "interior" stretch was cutting M6b's band short of MB's** —
the flood's own 50 mm grid speaking, not a finding, and it left a seam exactly
where the photo shows the wool turning unbroken. Interior spans shorter than
three flood cells are now discarded: **below its own resolution the method
cannot tell a genuine interior stretch from its quantisation, so it must not
claim one.** The stretch this test exists for, R9's, is 870 mm.

### ❓ Raised by the photos and NOT resolved

The model carries **70 mm on MA/MB/MC and 150 mm on M6b/R8/R9**. The photo shows
one continuous wrap and the spec says **70 mm throughout**; a step from 70 to
150 at a corner would show in the render, and it does not. The 150 came from the
owner on 2026-09-11 and the 70 from the spec, so **two owner-grade sources
disagree** and the photo cannot measure thickness. Recorded, not reconciled.

