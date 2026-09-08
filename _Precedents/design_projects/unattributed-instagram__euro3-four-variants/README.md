# `unattributed-instagram__euro3-four-variants`

**Class: `design_project` · `same_type_as_ours: yes` · status `analysed`**

Six sheets by one unidentified interior designer, published on Instagram (media ids
18423775762184885–18423775801184885) and supplied by the owner on 2026-09-08 to answer a question he
asked directly: *"I would like to show existing works for similar apartment with a similar layout. I mean,
exact same layout."*

**This is that material. It is not a similar layout — it is our type, and the set says so itself.**

**The analysis lives in `data/layout_cases/dubravinsky-euro3-designer-variants.json`.** This folder is
only the evidence behind it.

---

## Why we are confident it is our type

The cover sheet captions itself **«Евротрехкомнатная квартира в ЖК Дубравинский ~ 70 м.кв.»** — our
development by name, and ~70 m² against our 69.09. The topology corroborates it independently: same
handedness, туалет top-left with ванная below it, kitchen services top-right, and the distinctive
**angled лоджия** bottom-left.

⚠️ **«Евротрёхкомнатная» describes the RESULT, not the type as sold.** Ours is sold as **3Б/3+** with
three жилые комнаты and a separate 5.24 m² кухня. These sheets show **two** enclosed bedrooms plus an
L-shaped кухня-гостиная — so the euro-3 is what the merge *produces*.

## The six sheets

| role | file | what it is |
| :--- | :--- | :--- |
| `rendering_3d_axonometric` | `renderings/631615996_…` | the 3D cutaway cover that names the development and the area |
| `layout_plan_furnished` | `plans/IMG_20260610_091242_382.jpg` | **variant A** — bath vertical on the left wall · СММ in the ванная · hob in the wall run |
| `layout_plan_furnished` | `plans/631867090_…` | **variant B** — ванная re-proportioned, bath horizontal · **hob on a peninsula** |
| `layout_plan_furnished` | `plans/632197311_…` | **variant C** — **oval 6-seat table** · one appliance run · no workspace anywhere |
| `layout_plan_furnished` | `plans/631647771_…` | **variant D** — **СММ moved out of the ванная** into a laundry closet off the прихожая |
| `structural_scheme` | `plans/632035567_…` | unfurnished partition plan — **see trap 1** |

All six are `examined: yes`.

---

## What this set settles

- **Every one of the four variants starts by removing the кухня partition.** A professional working on
  our type left himself no choice on that move and varied everything else around it. Our 3Б/3+ becomes a
  euro-3, and the market accepts the result — that is what the cover sheet sells it as. ✅ **And the move
  is legal here: the building has no gas** (owner, 2026-09-08), so СН 3.02.01-2019 §4.8 cannot bite and
  it is a согласование question rather than a prohibition.
- **The open variable was storage** — all four place the wardrobes differently: прихожая wall in A and C,
  two runs flanking the middle room in B, inside the left bedroom in D. He did not find one right answer,
  which tells us that decision is genuinely ours.
- **A separate laundry fits.** Variant D moves the СММ out of the ванная into a closet off the прихожая.
  We held that as a hypothesis with no precedent behind it; now it has one.
- **Wet zones are never re-played.** Not one variant merges туалет with ванная — which agrees with our own
  decision.
- **All four put a washbasin in the туалет**, though the room is well under the 1.4 × 1.5 m that
  СН 3.02.01-2019 §4.9 requires once a basin is present. Practice resolves that conflict in favour of
  ergonomics. See [[08_WC/WC_Guide|WC Guide]] §1a, which already records the tension.

## ⚠️ Three traps in this material

**1. The "unfurnished" sheet is not the handover state.** It is tempting to use it as a clean topology
cross-check for `v0`. **It cannot be used that way.** It shows *no кухня partition*, whereas our own
developer schedule lists кухня as a separate **5.24 m²** room. So it is the **after** state of the merge,
drawn without furniture — not the shell. Recorded on the manifest row itself so the mistake cannot be
made twice, and it is the reason `role` now requires `examined: yes`.

**2. No dimension may be taken from any sheet.** Not one dimension string appears anywhere in the set.
`dimension_policy` is `undimensioned`; every figure in the case file comes from our own developer
schedule, none from these images.

**3. Hatching was deliberately not interpreted.** It appears identically on the outer envelope and on
internal partitions across every sheet, so it most likely distinguishes monolithic from block construction
rather than new from existing. That is unconfirmed — so **no wall here is called "new" on the strength of
its hatch**, tempting as it was.

## What the set does not give

**No dimensions, no prices, and no evidence that any of it was built.** These are proposals. As a
precedent for composition it is strong; as a source of geometry it is unusable, and as evidence of outcome
it is silent.
