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

### ✅ The 70 / 150 split is CORRECT — closed 2026-09-15

I raised this as an open disagreement and **it was not one.** The reasoning that
produced it: the spec says 70 mm mineral wool for the building's external walls,
and `ext2` shows the layer wrapping the M6b/MB corner as one unbroken skin —
from which I inferred a single thickness throughout.

⚠️ **That inference does not follow. A continuous wrap says nothing about
thickness**, and the photo cannot measure one — the same limit already recorded
for every other figure these photos touch. The owner confirmed the recorded
split the same day: **70 mm on the main façade walls MA/MB/MC** (300 block + 70,
per the spec) and **150 mm on M6b/R8/R9**.

Worth keeping as a failure class: a photo that settles TOPOLOGY decisively can
look like it settles DIMENSION, and it does not. `ext2` genuinely proved the
layer is one surface; it proved nothing at all about how thick that surface is.

## The 2026-09-15 second markup: angles, the M2 contact, and R9's recess

### ⚠️ The лоджия face is DIAGONAL, so its ends are mitres, not squares

Owner: *"the angle between glazing and M6b is a sharp angle… this angle should
be really sharp, not like a rectangle like you draw. And for M2 is the same.
Check the original image. This is angled. This is not rectangular."*

Everything in this model is built from axis-aligned rectangles, and a rectangle
running into a diagonal overshoots it by a triangle — **about 200 × 55 mm at
M2's south-west corner and the same at M6b's**. Squaring that off draws a stub
through the glass.

`tools/lib/rectunion.clip_halfplane()` now cuts every insulation run on the
glazing's **own outer plane**. Because it is one plane for both ends, the
finished surface stays continuous across the corner instead of gaining a step
of its own.

### ✅ The WALLS are mitred too — one cut, one angle, one surface

Owner, 2026-09-15: *"M2 and M6b are indeed not squared but inclined — the
surface is flush with the glazing and the insulation, this is the cut under one
angle and we have one surface."* Mitring only the layer left the block sticking
through the glass underneath it, so the wall entities are now cut on the **same
plane** as the insulation: **M2 loses 5710 mm², M6b 5707 mm²** — near-identical,
as a symmetric splay should be.

⚠️ **That required relaxing the strictest invariant in the model**, so it was
done narrowly and proved. `dxf_wall_entities.py` refused anything that was not a
rectangle, and that rule exists because *both* gates once reduced a polyline to
its bounding box — **a triangle on three of a rectangle's corners passed both.**

The relaxation is **not** "allow five corners". A wall may now carry **at most
one** skew edge, that edge must lie on the лоджия glazing's **own plane** — read
from `v0_elements_extracted.json`, never accepted from the entity — and the
polygon area must equal **the result of clipping the entity's own bounding box
on that plane**, recomputed here by shoelace. With no mitre the clip is a no-op
and the original bbox test is unchanged.

Three seeds prove it can still fail, each for its own reason:

| seeded defect | rejected because |
| :--- | :--- |
| the original **triangle on three corners** (CODEX r4) | area is half the box, and no plane passes where its diagonal does |
| a mitre at **45°** instead of the glazing angle | *"the skew edge is off the glazing plane — a wall may be mitred on THAT plane and on no other"* |
| a mitre at the **right angle, wrong offset** — parallel, 400 mm inboard | the plane test is an **offset** test, not an angle test: both ends must lie ON the plane, not merely along it |

The third exists because direction alone would have passed a wall that was
simply too short — the failure an angle-only check invites.

### M2 touches MA — the third time of asking

Owner: *"no gap between M2 and MA. This piece should be part of M2."* He had
said it before and **I twice reported it done when it was not.** The occlusion
rule had removed MA's *band* over M2's width, which deletes the insulation but
leaves a 70 mm **void** — removing the filler is not the same as making contact.
Directive `P_M2_north` now sets M2's north end to MA's near face 9050.6.

⚠️ That needed a new relation: `trim_*` only ever shortens, and M2 had to
**grow** 70 mm. `align_start` / `align_end` set an end either way.

### R9 is 1750 and RECESSED from MB

Owner: *"the length of R7 and R9 are similar, so it should be 1750, because it
is not flush with the MB as you can see it on the photo."* `_Survey` `ext1`
supports him — R9's concrete strip sits back from the block panels either side,
with a shadow line at both edges.

✅ **The printed `clear_mm` 1490 is untouched.** There were two routes to 1750:
clear 1450 + 300, which overrides a printed dimension with a recollection, and
clear **1490 + 260**, which says R9 claims only part of MB's thickness. The
second is what a recessed end *means*, and it costs no printed figure. Directive
`P_R9_south` pins the south face at 7600.6; 9350.6 − 7600.6 = **1750.0**,
against R7's 1749.7.

Three tools had to learn what a pinned end implies, each narrowly:

- **`close_corners`** must not undo it. A derived closure may fill what a stated
  fact leaves open; it may not overwrite the fact.
- **`build_wall_corners`** accepts the ledger's gain for a pinned owner. Its own
  rule — the owner gains the other wall's whole thickness — *assumes the owner
  runs through*, and a pin says it does not. Ownership, pair and kind are still
  asserted, so a flipped owner still fails.
- **`check_dxf_closure`** re-tests a pinned corner against walls **plus the
  insulation layer**. C_MB_R9 is closed by two materials: 650 cells of masonry
  and **100 of insulation**. It is not a void — nothing could cross it — but it
  is not solid block either. Seeded: delete the cap and the corner must fail.

### The end caps: a threshold was answering the wrong question

Owner: *"you forgot this small piece of insulation for the R8 corner from its
edge, similar to what we have for R9."* The old test asked *"does a neighbour
cover at least 25% of this end?"* and emitted nothing when the answer was yes.
⚠️ **R8's south end is 250 wide and M6b covers 200 of it** — so it read as
ABUTTED and the whole end was dropped, including the 50 mm strip M6b does not
reach and the 150 mm of R8's own band beside it. **An end is not abutted or
exposed; it is partly each.** Every uncovered sub-span now gets its own cap.

And a cap's outer face is pulled onto the plane of the layer it joins, so R9's
recess is closed by a **110 mm** cap — not R9's own 150 — which is what makes
the façade read as one plane rather than stepping 40 mm proud of it.

⚠️ `_Drawings/evidence/v0_raster_registration.json` — **S01's baseline was
raised 0.153 → 0.182, deliberately**. Less masonry covers that hatched band
because R9 moved back, which is the intended consequence of a recorded change.
Only that entry changed: `--refit` would have re-derived the whole fit to absorb
one intended move, and the fit is frozen precisely so that cannot happen quietly.

### ⚠️ The façade is ONE plane — R8's cap was standing 80 mm proud of it

Owner, 2026-09-15, with two arrows drawn along MB's south side: *"the surface
plane of MB should be in one level… the insulation adjacent to the лоджия
extends a little bit more than it should. R9's part with external insulation
should look exactly like R8's, except for R8 we have M6b touching it — the
thickness."*

He was right and the numbers were unambiguous:

| element | outer face |
| :--- | ---: |
| **R8's end cap** | **7410.6** ← 80 mm proud |
| MB's bands | 7490.6 |
| MB's end cap | 7490.6 |
| R9's end cap | 7490.6 |

**The cause was a too-strict adjacency test.** `flush_end_caps` pulled a cap
onto its neighbour's plane only when the two OVERLAPPED along the cap's run.
R8's cap runs x 5731…5931 and MB's band starts at 6131, because **M6b's 200 mm
sits between them** — so the cap found no neighbour at all, kept its own 150 mm
depth, and stood proud.

⚠️ **A wall standing between two stretches of the layer does not stop them being
the same surface — the layer wraps it.** What matters is that they are near
enough to be one plane, not that they touch. The test now allows a gap of up to
`CORNER_REACH_MM` (400, the thickest wall in the model). Every element along
MB's south face now reads **7490.6**, and R8's cap becomes 70 deep against R9's
110 — *exactly like R8 except for the thickness*, which is the difference R9's
40 mm recess creates and what the owner described.

⚠️⚠️ **THIS DEFECT CLASS HAS NOW OCCURRED TWICE AND IS NOT GATED.** First the
flood's 50 mm grid notched the layer at every junction; now a 80 mm step at a
cap. Both were caught by the owner reading a drawing, not by a check. **A step
in the finished plane is exactly the kind of thing a gate should catch and
nothing asserts it.** Adding one means measuring the drawn insulation loops back
out of the DXF and asserting that edges facing the same way within a corner's
reach are coplanar — real work with its own seeds, and worth doing before the
surface model is built on top of this.

