# Review prompt — the apparatus is mature and the flat is not designed. What next?

**2026-09-19.** For Codex. Follows `joint_review_prompt_toolset_20260918.md` and
`joint_review_prompt_eevee_gi_20260918.md`, whose findings drove most of what is
described below.

---

I want your judgement on **what to do next**, not on whether the code is correct.
Be blunt, and **reproduce rather than assert** — name the file, the number or the
commit if you think I have something wrong.

## The situation, stated against myself

Over 2026-09-18/19 this repo produced a long run of green commits. In the same
period **not one design decision was made about the apartment.** `v0-existing` is
the same building it was on 2026-09-17. I recorded that split explicitly in
`00_Master/project_decisions.md` under *APPARATUS vs DELIVERABLE*, because the
commit log otherwise reads as progress.

**What got built (apparatus):**

- a wall-elevation renderer (развёртки), 13 seeds
- textures proven applicable at exact physical scale with **no UV maps** —
  measured 400.0 px against 400.0 expected
- the EEVEE probe-volume defect found (by you) and fixed; probes do carry
  out-of-frame light, EEVEE recovers ~42% of path-traced
- derived views made provenance-bearing; `check_view_freshness.py`, 16 seeds
- `build_variant.py` and `make_variant.py` retired to tombstones, 10 seeds
- the wall manifest contract made coherent — 25 legs / 24 physical / 23 direct + 1
  assembly
- **rooms**: the model resolved walls and never rooms. `room_boundaries.csv` +
  `room_boundaries.py`, first `IfcSpace` this compiler has ever emitted, 11 seeds.
  **1 of 7 rooms authored.**
- wall-bed width answered as a BUDGET rather than waiting on a catalogue: **no
  wider than 1670 mm on R6 or R7**; open footprint leaves 825 mm in front on R6,
  1490 on R7

**What the owner decided (real, and small):** no wider window in the 9.36 room, so
the radiator does not move, so central heating is untouched, so the renovation
stays in the **notification track** under Постановление 164 rather than becoming a
designed project. Two album sheets moved out of scope.

**What has NOT happened:** no layout option authored, no variant built or chosen,
no room laid out. The variant compiler is deliberately unbuilt — it is meant to be
triggered by the first genuinely authored model-native option, and no such option
exists.

## The owner's own framing

> *"the purpose of creating this model is to experiment with different ideas"*

He does not draw and will not learn; chat is the permanent interface. He has just
asked me what I need from him. **My honest answer was "almost nothing"** — I can
author the remaining six rooms, build развёртки, model rough-in envelopes and chase
the browser-lighting problem entirely alone.

## ⚠️ The bias I want you to check

**I keep choosing apparatus work, and apparatus work is the category that does not
require the owner.** That is a suspicious coincidence and I am not well placed to
judge it. Every one of the items above is defensible individually; the pattern may
not be.

## The three options I put to him

1. **Author the five remaining room boundaries** — feeds развёртки (nine album
   sheets), more apparatus, no design.
2. **Build the rough-in envelopes** — duct routes, ceiling drops and drainage falls
   against a **2500 mm** clear ceiling.
3. **He describes one layout idea in words; I test it against the model** and report
   what closes and what does not.

I recommended **3**.

## ⚠️⚠️ And here is the direct conflict I want adjudicated

**Antigravity's answer of 2026-09-18 says option 3 is wrong**, and names it the
biggest unnamed risk — a *critical-path inversion*:

> *"You are planning to spend the coming weeks on Steps 5–7 … while the rough-in
> engineering layers contain zero geometry and zero data in `data/canonical/`. If
> you design the furniture and finishes in 3D first, you will have to throw them
> away the moment the rough-in engineering is confronted."*

I partially refuted that at the time — shafts, plumbing anchors, outlets and
existing electrics **do** exist; what is missing is **horizontal routing** (duct
runs, ceiling drop zones, drainage falls). That correction stands, but its
sequencing argument was never resolved, and **it points at option 2 while I am
recommending option 3.**

Relevant hard constraint: clear ceiling is **2500 mm**, ducts want 150–200 mm, and
**no height is recoverable from the floor** — the screed is already laid with the
heating distribution in it.

## What I want judged

1. **Is my recommendation of option 3 right, or is Antigravity's sequencing right
   and rough-in must precede any layout experiment?** This is the main question.
2. **Is the apparatus/deliverable imbalance a real problem or a false alarm?** Six
   of the last nine defects I found were in my own new code. An argument exists that
   the apparatus needed exactly this hardening before carrying any design. I cannot
   tell whether that is true or a rationalisation.
3. **Is "author one layout in words, test it against the model" even a coherent unit
   of work** given there is no variant compiler? Testing an idea against v0 without
   building a variant may be the right lightweight move, or may be the thing that
   silently recreates the retired builder.
4. **What is the smallest piece of real design work that would be decision-bearing?**
   The v0 baseline is not accepted yet — six scopes pending — so strictly nothing
   read off it is decision-bearing today. Does that change the answer?
5. **What am I still not seeing?** The last two rounds each found a defect that
   inverted a conclusion: the probe volume, and a census that printed a
   contradiction and returned PASS. Assume there is a third.

## What I am not asking

Do not design the apartment. Do not re-litigate canonical-data-first, the variant
builder retirement, or the room-boundary architecture — those are settled and
working. The question is **sequencing and where the next unit of effort should go.**
