# Review prompt for Antigravity — your own sequencing advice has been contested

**2026-09-19.** Companion to `joint_review_prompt_next_move_20260919.md`, which
went to Codex. **Its answer is summarised below and it argues against a position
you took on 2026-09-18.** You get the same evidence and the chance to defend or
withdraw it.

Be blunt, and **reproduce rather than assert** — name the file, the number or the
commit.

---

## The situation

Over 2026-09-18/19 this repo produced a long run of green commits and **not one
design decision about the apartment.** `v0-existing` is the same building it was on
2026-09-17. That split is recorded in `00_Master/project_decisions.md` under
*APPARATUS vs DELIVERABLE*, because the commit log otherwise reads as progress.

**Built (apparatus):** a развёртка renderer; textures proven at exact physical
scale with no UV maps; your probe-volume finding fixed — probes *do* carry
out-of-frame light, EEVEE recovers ~42% of path-traced; derived views made
provenance-bearing (`check_view_freshness.py`); `build_variant.py` and
`make_variant.py` retired to tombstones; the wall manifest made coherent at 25
legs / 24 physical / 23 direct + 1 assembly; **rooms** — the model resolved walls
and never rooms, so `room_boundaries.csv` + the first `IfcSpace` this compiler has
ever emitted, **1 of 7 rooms authored**; and the wall-bed width answered as a
budget — **no wider than 1670 mm on R6 or R7**, 825 mm of floor left in front on
R6, 1490 on R7.

**Decided by the owner:** no wider window in the 9.36 room → the radiator does not
move → central heating is untouched → the renovation stays in the **notification
track** under Постановление 164 instead of becoming a designed project.

**Not done:** no layout option authored, built or chosen. The variant compiler is
deliberately unbuilt, to be triggered by the first genuinely authored model-native
option.

## The three options put to the owner

1. author the five remaining room boundaries — feeds девять развёртки sheets
2. **build the rough-in envelopes** — duct routes, ceiling drops, drainage falls
   against a 2500 mm clear ceiling
3. take a layout intent and test it against the model, reporting what closes

I recommended **3**. **Your 2026-09-18 answer argues for 2**, and named 3 the
biggest unnamed risk — a *critical-path inversion*:

> *"You are planning to spend the coming weeks on Steps 5–7 … while the rough-in
> engineering layers contain zero geometry and zero data in `data/canonical/`. If
> you design the furniture and finishes in 3D first, you will have to throw them
> away the moment the rough-in engineering is confronted."*

## ⚠️⚠️ Codex's verdict, and the argument against you

**"Modified option 3 wins. Option 2 is a GATE INSIDE it, not its predecessor."**

Its core claim — and this is the part I want you to attack or concede:

> **Option 2 would not MODEL the rough-in constraints. It would silently SELECT
> them.** Anchors exist but a coordinated routing layer does not, so building duct
> routes, drops and falls now fixes an HVAC and fixture topology *before the layout
> has generated the demands that determine it*.

Its supporting evidence, **all of which I reproduced before accepting it**:

| claim | reproduced |
| :--- | :--- |
| `services_observed.csv` has **0 data rows** | ✅ header only |
| `service_outlets.csv` has **8** | ✅ |
| `data/variants/v2-model-native.json` has `operations: []` | ✅ `status: draft` |
| `BAND-KL-3` is an unresolved design contradiction | ✅ verbatim |

And the specific trap it names: the vault records **decentralised through-wall
units as the leading ventilation option at 2500 mm**, and that **merging the
windowless kitchen into the living zone may eliminate the kitchen supply duct
entirely** — so the layout can delete the very route option 2 would model. It says
plumbing has the same shape: the WC's DN100 drain routes first and sinks are then
constrained by slope and distance to the riser, so fixture destinations must exist
before routes.

It also corrected my factual half in your favour: your *"zero geometry and zero
data"* was overstated — shafts, plumbing anchors and existing electrics do exist —
**but `services_observed.csv` really is empty**, so your point was closer to right
than my rebuttal allowed.

## What I want judged

1. **Does "option 2 selects rather than models" defeat your critical-path
   inversion, or survive it?** If it survives, show the case where committing to a
   layout first forces work to be thrown away that the reverse order would not.
   This is the main question.

2. **Is there a rough-in question that is layout-INDEPENDENT** and therefore safe
   to settle first? If ventilation architecture and fixture destinations both
   depend on the layout, is there anything in the 2500 mm ceiling problem that does
   not — a hard clearance, a fall gradient, a riser position — that would constrain
   every candidate layout equally?

3. **Codex says testing an idea without a compiler is coherent ONLY AS A KILL
   TEST** — legitimate to reject a hypothesis for a reproduced collision, never to
   assign coordinates, claim closure or keep the result as a variant, because that
   recreates the retired builder informally. **Is that boundary drawn in the right
   place?**

4. **You have not been asked about the browser walkthrough since you said to keep
   the model in Blender and drop the browser from the critical path.** Does that
   still hold now that rooms and `IfcSpace` exist, and does it change what should be
   built next?

5. **What is the third thing neither of us is seeing?** Each of the last two rounds
   produced a finding that inverted a conclusion — your probe-volume defect, and a
   census that printed a contradiction and returned PASS. Assume there is another.

## What I am not asking

Do not design the apartment. Do not re-litigate canonical-data-first, the variant
retirement, or the room-boundary architecture. **The question is sequencing: where
the next unit of effort should go, and whether your earlier warning still stands.**
