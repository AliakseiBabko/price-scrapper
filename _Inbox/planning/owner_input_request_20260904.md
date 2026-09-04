# What to describe, and how — owner input request, 2026-09-04

The owner offered three additional sources. **This is the worksheet, in priority order.** Answer in whatever
form is easiest — talking it through is fine, the structure below is so nothing gets lost, not a form to fill in.

**Use `_assets/wall_key_plan.png`** — the developer's detailed plan at 3×, with an **A–L × 1–12 grid**. Every
cell is labelled in place, so a wall can be named without ambiguity: *"the wall from **E4** down to **E9**"*,
*"the column at about **H2**"*. That removes the "on the right" problem, where the answer depends on where the
speaker is standing.

Orientation on that image, for reference: туалет ≈ **B2**, ванная ≈ **B4–C4**, small room 9.36 ≈ **B7–C7**,
прихожая 9.79 ≈ **F2**, кухня 5.24 ≈ **J2**, middle room 16.64 ≈ **F7**, living 19.49 ≈ **J7**,
лоджия ≈ **B10–C10**.

---

## 1. ⚠️⚠️ Wall materials and the two columns — the highest-value item

**Why this ranks first:** the layout skill currently says the shell/partition split rests on *"a 200 mm
thickness threshold … **not a structural survey — no wall may be called non-load-bearing on its strength**."*
That is a named gap, and this closes it. **The two concrete columns are not in the model at all** — the shell
carries 14 walls and the immovable services, no columns — and they sit in the entrance area, which is exactly
where `v1` puts its laundry and where the corridor trade would go.

**And the owner's own reason is the strongest one: you can chase a service through aerated block and you
cannot through concrete.** So this map decides where an AC line, a ventilation run or a recessed anything can
physically go — not just what is legal to remove.

- [ ] **The two columns.** Grid cell for each, roughly. Section if known (square/rectangular, and size).
      Are they free-standing, or buried inside a wall line?
- [ ] **Which walls are concrete** — list by grid run, e.g. *"A1→A9 concrete, E4→E9 concrete"*.
- [ ] **Which walls are the softer material** (газобетон / газосиликат — aerated autoclaved block), and
      **its nominal thickness** if known. The plan draws **75 mm** partitions and **250 mm** structure; if the
      real block is 100 mm, that matters.
- [ ] **Any wall that is partly one and partly the other** — the owner mentioned this. Where does it change?
- [ ] **The вентблок construction.** The owner offered "what it consists of". The туалет block is drawn as
      **three channels** (1140 × 490); the second is **400 × 1140** at the прихожая/кухня boundary.
      **Which channel does what?** That decides whether a kitchen extract may join it at all, and it is the
      difference between a legal and an illegal ventilation design.

## 2. The walk-through description — cheap, and it unlocks item 3

**What it adds that the plan cannot: HANDEDNESS.** The series is built in **left- and right-handed variants**
(recorded 2026-09-04), so any comparable plan *or photo* may be the mirror image of this flat, and there is
currently no way to tell. **A single "as you come in the front door, X is on your left" fixes the orientation
of everything else.**

- [ ] **Entering the front door: what is immediately left, immediately right, straight ahead.**
- [ ] Then the natural walk — into the прихожая, to the kitchen, to each room — *"on the left you see…, on the
      right…"*, which is how the owner says he naturally describes it.
- [ ] **Sightlines**, which no plan gives: standing in the kitchen zone, what can you see? This bears directly
      on where the Phase-2 **retractable glass divider** actually works.
- [ ] Anything about door swings as actually built, if it differs from the plan.

## 3. Photos of a real flat of the same layout — as EVIDENCE, not for rendering

> [!IMPORTANT]
> **⚠️ One correction to the stated purpose: renders are NOT in the deliverable.** The agreed end product is a
> Dolgushev-style **планировочный проект** — A3 sheets plus grey 3D massing, *deliberately* without renders,
> ведомости or развёртки (`project_decisions.md`) — and by the owner's own instruction the model carries
> **no finishes, no lighting, no furniture**. **So photos gathered for daylight or rendering reference would be
> effort spent on something the project has ruled out.** Photos are still valuable, for different reasons:

- [ ] **The columns and the wall materials, visually.** Unfinished concrete and aerated block look nothing
      alike — a photo confirms item 1 independently.
- [ ] **The вентблок, opened or in section** if visible — channel count and which is which.
- [ ] **Window openings** — position and clear size against the plan's 1800.
- [ ] **The slab soffit.** The vault holds a finding that the bare-lacquered-concrete ceiling strategy only
      worked because that practitioner **got lucky with his slab**. A photo says whether that option exists
      here at all, and it is a real budget item.

⚠️ **The mirroring caveat applies to photos too.** A photo of another flat of this layout may be the mirror,
so item 2 should come with or before item 3, or the photos will be read backwards.

### ✅⚠️ MARK THE CAMERA — offered by the owner 2026-09-04, and it is what makes a photo usable at all

**Not a nice extra. Without it a photo of another flat is close to unreadable**, because of the mirroring
above: if a frame shows the вентблок on the right-hand wall, there is no way to tell whether that flat is
handed like this one or is its mirror — so **every left/right observation taken from it is a coin flip.**

**A marked camera position plus view direction removes that:** the arrow says what *should* be on the left,
the photo says what *is*, and the discrepancy settles handedness **for the whole set**.

Three further things it buys:

1. **It attaches an observation to a NAMED wall.** *"The wall on the right of this frame is aerated block"*
   becomes *"wall E4–E9 is aerated block"* — so it lands on a specific wall in the model instead of floating.
2. **It makes openings checkable.** A frame looking down the прихожая gives a door sequence that can be
   compared against the drawing directly.
3. **It needs no new convention.** `schemas/layout-case.schema.json` already has `evidence.frame`, and cases
   carry a `frames_dir` — `zemskov-odintsovo-69m2` uses both. Marked frames slot straight in.

**The convention, kept deliberately rough:**

- [ ] **A dot for the camera, a line for the view direction, labelled to match the filename** — `P1`, `P2`, …
- [ ] **Or skip the drawing and just type it against the grid:** *"P1: camera at F5, looking toward A5"*.
      Two cells — from and toward — is equally unambiguous.
- [ ] **±1 cell does not matter. Which way it faces does.**
- [ ] **⚠️ One line for the whole set is worth more than any single arrow:** *"this flat is the same
      handedness as my plan"* or *"it is mirrored"*. The per-frame arrows then only refine it.
- [ ] Drop them in `_Inbox/_Visual_Drop/` as usual, named `P1…Pn`; they get organised and registered here.

→ **This is a MULTIPLIER on item 3, not a promotion of it.** It moves photos from "possibly misleading" to
"usable evidence", which is a real jump — but items 1 and 2 still come first, and **the wall-material map needs
no photos and no camera marks at all: the grid plan alone carries it.**

---

## What this does NOT unblock

**`v0` geometry.** That is built from the **printed linear chains** on the detailed plan and needs nothing from
the owner — it is in progress. None of the three items above is a prerequisite for it. **They constrain what
may be DONE to the geometry** (what can be removed, what can be chased) rather than what the geometry *is*.

**And per the standing instruction of 2026-09-04: no area figure from any source is evidence.** Everything
above is asked in terms of positions, materials and linear sizes for that reason.
