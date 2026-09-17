# Codex review brief — what belongs in the model OUTSIDE the apartment perimeter

**2026-09-17.** Branch point `e50e101` on `main`. This is a **scoping question, not a repair round.** Nothing is broken. The question is what the model is *for* at its edges, and it has just produced its second hand-authored exception in three days.

⚠️ **I have a recommendation and it is at the end. Attack it.** It is the cheap option, and the owner proposed the expensive one; I want to know whether I am choosing it because it is right or because it is cheap.

---

## 1. The trigger — a derivation that cannot be made

`M2` is the wall between our лоджия and the neighbouring flat's. The vault has carried two records about it that looked like a contradiction:

| Record | Says |
| :--- | :--- |
| Owner rule 4 | *"M2 is 200 mm aerated block with NO insulation"* |
| `wall_blocks.csv` | an insulation thickness (150, latterly disputed) |

The owner pointed at `_Inbox/_Visual_Drop/4th_floor_plan.png`. **Both are right about different parts of the same wall.** M2's upper run abuts the neighbour's лоджия; its lower run projects past the neighbour's footprint and faces open air, and the plan draws a stippled insulation band on the outer face of that run only. Evidence crop: `_Drawings/evidence/m2_mixed_exposure_from_4th_floor_plan.png`. Finding recorded at `wall_materials.json → M2_EXPOSURE_IS_MIXED_2026_09_17`; **no value was written**, because `insulation_mm` is one number per wall and every value is wrong somewhere along its length.

**The reason the compiler cannot resolve this is that what decides M2's exposure is what stands on the other side of it, and the model does not carry the other side.**

## 2. ⚠️⚠️ This is the SECOND instance, and the first is already committed as an exception

Two days earlier, `MC`'s insulation end caps were suppressed by owner directive. The note in `wall_blocks.csv` is explicit about *why* the rule could not derive it:

> *"The end-cap rule cannot derive this: nothing east of x 12946.0 exists in our model, so a flood from outside reaches it and it reads as exposed. **Being at the end of OUR drawing is not the same as being outside the BUILDING.**"*

That is the same failure, stated in the same words, about a different wall. **The pattern is now established rather than suspected:** where a property of our geometry depends on adjacency, the compiler reads *absence of neighbour* as *outside*, and a human has to patch it. Two patches exist. Neither is checkable by any gate, because there is nothing to check them against.

**This is the load-bearing observation of the brief.** If you disagree that two instances constitute a pattern, say so — the whole case rests on it.

## 3. The owner's candidates

He proposes admitting, explicitly:

1. **The party walls shared with `2Б/2`** (the in-block neighbour to the left) **and `3А/2`** (the mirrored flat across the block joint, east).
2. **Part of the internal passage carrying the entrance door of `2Г/2`.**
3. **The electrical panel in that passage**, next to `2Б/2`, between entrance area 5.30 and WC 4.43.

### What the vault already asserts about each, without modelling any of it

**Party walls.** `building_spec.json → neighbours_and_adjacency` already carries load-bearing claims that depend on the other side:

- the block-joint wall is *"a GENUINE DECOUPLED DOUBLE WALL, ~400 mm"* — **our leaf is 200–250 mm and the neighbour's block supplies the rest.** The vault's soundproofing advice ("needs no spend at all") is a claim about a composite whose second half is not in the model;
- the **#1 soundproofing priority in the flat** is the left party wall's lower portion, *"where the 9.36 room meets the neighbour's 14.64 habitable room"*;
- the top wall's three-segment split `G2 | R3 | G3` exists **because it has more than one neighbour along its length** — corridor, then `2Г/2`. That is adjacency already driving our own segmentation.

**The passage.** It is the delivery and waste route, and `2Г/2`'s door bounds what our entrance-area work can spill into. `building_spec.json → flat_in_building/access` already records the carry distance from the lift core.

**The panel.** The owner intends to **rewire the flat completely, with the layout derived from appliance and fixture positions** — the case made in the previous brief. A generated cable run needs an origin. Today `wall_materials.json` records only *"a central distribution board near the ENTRANCE"*, which is the flat's own board. The floor panel is where supply actually enters, and it is outside the perimeter.

## 4. The arguments against, stated as strongly as I can

⚠️ **There is no measured geometry for any of this, and the vault has a standing rule about that.**

- **Rule 9 / `Evidence_Reading_Discipline.md`: areas are never evidence.** 5.30, 4.43, 14.64, 18.74 are room labels off a block plan. They cannot become geometry. Everything we would model comes from **one raster screenshot the owner assembled and mirrored**, with no printed dimension on any of it.
- **`_Precedents/` rule 11: undimensioned means undimensioned**, and a confident label on an unlooked-at thing is worse than no label. Admitting neighbour walls means authoring coordinates whose provenance is "read off a screenshot".
- **No oracle exists for it.** `check_dxf_closure.py` and `raster_fidelity.py` both register against the developer PDF **of our flat** and assert its sha256. Neighbour geometry would be the first canonical geometry in the project with **no independent check** — and `Validator_Design_Discipline.md` says a gate nobody has watched fail is not a gate.
- **Every IFC baseline moves.** Wall count (24 after `A_NW_CORNER`), IDS expected-applicability counts, identity minting, connection ledger, closure gate. All are currently green and all are asserted against the flat as it stands.
- **Phase and ownership semantics do not exist for it.** The vocabulary is `existing` / `demolished` / `new`. These elements are none of those in any useful sense — they are *never ours to touch*. And phasing already has **zero practitioner sources across 292 videos**, so there is no convention to borrow.
- **Scope.** The deliverable is a renovation album for one flat. A neighbour's WC is not in it.

## 5. ⚠️ My recommendation, which is the one I most want attacked

**Do not model neighbour geometry. Author an ADJACENCY RECORD instead.**

A table — call it `wall_adjacency.csv` — carrying, per wall and per face, **what is on the other side**: `outside` / `party_flat:2Б/2` / `party_flat:3А/2` / `common_corridor` / `own_loggia` / `neighbour_loggia` / `shaft`, with a provenance column and, where a face changes neighbour along its length, **a run split** — which is precisely what M2 needs and what `G2|R3|G3` already does informally.

**Why I think this is the right shape:**

- it is **exactly the information both patches needed**, and nothing more. MC's end cap and M2's insulation both become *derivable* rather than *directed*;
- it is **the class of statement we can actually evidence.** "The far side of MC's east end is another flat" is a topological claim readable off the block plan without measuring anything. "The neighbour's wall is 200 mm at x=13196" is not;
- it is **gateable**: every wall face accounted for, no face left `unknown` silently, vocabulary closed, a face that changes neighbour must carry a split — the same shape as the locator union and the phase vocabulary, both of which were closed after failing open;
- it keeps `insulation_mm` honest, because the insulated extent becomes a **consequence of the adjacency runs** rather than a number someone picks;
- it does not move a single IFC baseline.

**The panel is the one candidate this does not serve**, and I think it is genuinely different in kind: it is not adjacency, it is **the origin of a network we are about to generate**. My inclination is to admit it as a **located service terminal with a scope marker (`outside_apartment`, never demolished, never new)** rather than as modelled geometry — the services locator schema already has `scope_kind` / `scope_ref` for exactly this reason.

---

## 6. What I want from you

1. **Is "two hand-authored exceptions" a pattern?** §2 is load-bearing. If it is really two unrelated one-offs, most of this collapses.
2. **Rule in or out, per candidate** — party walls, passage, panel — and say *why* each differs from the others, if it does.
3. **Is there an admission rule?** My draft: *an element outside the apartment boundary is admitted only when a derivation INSIDE the boundary is currently wrong or hand-patched without it.* Accept, reject, or sharpen it. In particular: does it wrongly admit or wrongly exclude any of the three?
4. **Attack the adjacency-table recommendation.** Specifically: is there a derivation the owner will want that **topology alone cannot supply** and geometry could — acoustic performance of the ~400 mm composite is my own best counter-example, and I do not know how to price it from topology.
5. **Evidence standard.** If any geometry is admitted, what provenance is acceptable for it, given that every check in this repo registers against a PDF of our flat only? I do not have an answer and would rather admit nothing than invent an unguarded oracle.
6. **Representation, if admitted.** IFC-wise these are neither `existing` nor `new`. Is there a defensible way to carry a *context* element that cannot be confused with scope of work, or does that argue on its own for keeping them out of the model entirely?

**Ground everything in files you have read.** The last four review rounds each found a real defect in the round before, including two that would have produced confidently wrong geometry. Assume the same here — particularly in §5, where I am arguing for the option that costs me least.
