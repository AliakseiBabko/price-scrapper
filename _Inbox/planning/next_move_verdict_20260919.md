# Sequencing verdict — Codex, 2026-09-19, reproduced

Answer to `joint_review_prompt_next_move_20260919.md`. **Every load-bearing claim
below was reproduced before it was accepted.**

---

## The verdict

> **Modified option 3 wins. Option 2 is a GATE INSIDE it, not its predecessor.
> Option 1 is backlog work unless the chosen slice requires those boundaries.**

And, before any of it, an **option 0** I had not offered: the owner reviews v0.

## ⚠️⚠️ The correction that matters most — my answer to the owner was wrong

He asked *"what do you need from me to proceed?"* and I said **"almost nothing."**
That was wrong. The right answer:

> **Review the v0 sheet and either accept or correct the six scopes. I do not need
> another idea yet — your existing transformable-zone intent is enough for the next
> experiment.**

⚠️ **And option 3 was badly phrased by me.** I asked the owner to *describe a layout
idea*. He has already supplied the governing one: **`DI-004`, the transformable
kitchen/living sleeping zone serving both `SC-A` and `SC-B`.** Asking for another is
asking him to repeat himself.

## ⚠️⚠️ Why "rough-in first" is wrong — the third inverting finding

Antigravity's sequencing argument fails, and the reason is one I did not see:
**option 2 would not model constraints, it would silently SELECT them.**

| claim | reproduced |
| :--- | :--- |
| `services_observed.csv` has **zero data rows** | ✅ header only |
| `service_outlets.csv` has **8** | ✅ |
| `v2-model-native.json` has `operations: []` | ✅ `status: draft` |
| `BAND-KL-3` is an unresolved design contradiction | ✅ verbatim |

**Anchors exist; a coordinated routing layer does not.** So building duct routes,
drops and falls now would fix an HVAC and fixture topology *before the layout has
generated the demands that determine it*. Codex names the specific trap: the vault
records decentralised through-wall units as the leading option at 2500 mm, and
**merging the windowless kitchen into the living zone may eliminate the kitchen
supply duct entirely** — so the layout can delete the very route option 2 proposes
to model. Plumbing has the same shape: the WC's DN100 drain routes first, and sinks
are then constrained by slope and distance to the riser, so fixture destinations
must exist first.

## The next unit of work, when the owner has reviewed v0

**One coupled layout / rough-in feasibility slice**, driven by the existing `DI-004`
intent. It answers only:

- can the transformable zone close spatially?
- can `SC-A` and `SC-B` share the same expensive first fix?
- what ventilation architecture does that topology require?
- where, if anywhere, are ceiling drops unavoidable at 2500 mm?
- do drainage, electrical and lighting terminals stay feasible?
- which partition moves earn their demolition and reconstruction?

Not "design all rooms". Not "engineer all services first".

**There is already a concrete conflict for the slice to resolve: `BAND-KL-3`** — the
window band cannot serve both the bed position and the boy's study position in
`SC-B`. Authoring six more baseline rooms will not answer it.

## ⚠️ The boundary on testing an idea without a compiler

**Coherent only as a KILL TEST.** Legitimate: reject an idea because it collides
with an immovable shaft, cannot give a required clearance, or forces an impossible
service route. **A rejected hypothesis is useful and needs no variant.**

Not legitimate: assign new wall coordinates, claim room closure, compare
demolition against new build, generate a plan, or keep the spatial result as though
it were a variant. **At that point the retired builder has been recreated
informally.**

> Test verbally stated intent against existing constraints. If it survives, author
> the minimum model-native variant relations and let that concrete option trigger
> the replacement compiler.

## On the apparatus imbalance

**"A real problem now. It was not necessarily a mistake historically."** Several
hardening commits were justified — the tombstone, the 23-vs-24 check, the acceptance
deadlock, the first room boundary. But `241cc84` already declared the stop
condition, and continuing with all remaining rooms *because they feed nine sheets*
would knowingly continue the imbalance.

⚠️ **And the six-of-nine self-defect figure cuts the other way from how I framed
it**: new code naturally exposes its own defects, which is a reason to **narrow the
surface area, not expand it.**

⚠️ **Author the next room boundary when the design slice needs it — not as a
blanket batch.** `5088f6f` proved one boundary architecture works. It did not prove
the other six are the priority.

## The sequence

1. **Owner reviews v0** ← the only thing blocking, and it is his
2. run one `DI-004` / `SC-A` / `SC-B` design slice
3. author only the room boundaries it touches
4. ventilation, ceiling-void, drainage and electrical feasibility **inside** that slice
5. if it survives, let it trigger the new variant compiler
6. **stop when the option is accepted or rejected — do not roll straight into more tooling**
