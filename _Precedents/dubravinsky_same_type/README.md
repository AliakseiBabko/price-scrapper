# `_Precedents/dubravinsky_same_type/` — design precedent for our own apartment type

**Supplied by the owner on 2026-09-08** to answer a question he had asked directly: *"I would like to show
existing works for similar apartment with a similar layout. I mean, exact same layout."*

This is that material. It is not a similar layout — **it is our type, named as such on the cover sheet.**

---

## Why this is a separate folder from `_Survey/`

They look alike — both are third-party images, both gitignored, both indexed by a `manifest.csv` with
sha256. The difference is what they are evidence **of**, and it matters enough to keep them apart:

| | `_Survey/` | `_Precedents/` |
| :--- | :--- | :--- |
| what it is | **measurement evidence** — 30 photos of three built flats, each tied to a camera position | **design precedent** — what somebody *proposed* for this type |
| what it settles | geometry, services positions, what the developer actually hands over | compositional options, and which of them a professional treats as settled |
| the model **is built from** it | yes — sills, heads, riser zones, the 2540 ceiling | **no. Never.** |
| dimensions may be taken from it | yes, that is the point | **no — there is not one dimension string in the whole set** |

Mixing the two would be the exact failure `00_Master/Evidence_Reading_Discipline.md` exists to prevent:
a furnished presentation plan *looks* like a drawing you can scale, and it is not.

---

## What is here

### `designer_variants/` — six sheets, one designer, our type

The cover sheet captions itself **«Евротрехкомнатная квартира в ЖК Дубравинский ~ 70 м.кв.»** — our
development by name, and ~70 m² against our 69.09. The topology corroborates it independently: same
handedness, туалет top-left with ванная below it, kitchen services top-right, and the distinctive
**angled лоджия** bottom-left.

| role | what it is |
| :--- | :--- |
| `cover_3d_axonometric` | the 3D cutaway that names the development and the area |
| `designer_variant_A` | bath vertical on the left wall · СММ in the ванная · hob in the wall run |
| `designer_variant_B` | ванная re-proportioned, bath horizontal · **hob on a peninsula** at the table |
| `designer_variant_C` | **oval 6-seat table** · all appliances in one run · no workspace anywhere |
| `designer_variant_D` | **СММ moved out of the ванная** into a laundry closet off the прихожая |
| `structural_scheme_after` | unfurnished partition plan — **see the warning below** |

### `minina_3_renderings/` — 12 realt.by-watermarked renderings, same development, ул. Минина 3

Marketing images from a listing. **They are not renderings of the four variant plans above** and must not
be read as such. Only one has been examined so far (a WC with a wall-hung pan, hygienic shower, wall
cabinet and open shelving) — the other eleven are unexamined.

---

## ⚠️ Three traps in this material

**1. The "unfurnished" sheet is not the handover state.** It is tempting to use it as a clean topology
cross-check for `v0`. **It cannot be used that way.** It shows *no кухня partition*, whereas our own
developer schedule lists кухня as a separate **5.24 m²** room. So it is the **after** state of the merge,
drawn without furniture — not the shell. Recorded on the row itself so the mistake cannot be made twice.

**2. No dimension may be taken from any sheet.** Not one dimension string appears anywhere in the set.
Every figure in the case file comes from our own developer schedule; none is read off these images.

**3. Hatching was deliberately not interpreted.** It appears identically on the outer envelope and on
internal partitions across every sheet, so it most likely distinguishes monolithic from block
construction rather than new from existing. That is unconfirmed — so **no wall here is called "new" on
the strength of its hatch**, tempting as it was.

---

## Why the bytes are gitignored, and what is in git instead

Same treatment as `_Survey/` and the album PDFs, for the same reason — third-party material:

- the **bytes** stay out of git — `.gitignore` excludes `_Precedents/**/*.jpg|jpeg|png|webp`
- the **identity** goes into git — `manifest.csv` carries path, set, role, description, byte size and
  **sha256** for all 18 files, and the case file repeats the sha256 of each of the six sheets it cites

> [!IMPORTANT]
> **Gitignored means this machine only — it is not a backup.** Unlike `_Survey/`, losing these would cost
> analysis rather than geometry: the conclusions are already written down in the case file, which *is* in
> git. That is the argument for leaving it as it stands.

---

## What this collection has already settled

The reason it earns a folder:

- **Every one of the four variants starts by removing the кухня partition.** A professional working on our
  type left himself no choice on that move — he varied everything else around it. Our 3Б/3+ becomes an
  euro-3, and the market accepts the result, because that is what the cover sheet sells it as.
- **The open variable was storage** — all four place the wardrobes differently. He did not find one right
  answer, which tells us that decision is genuinely ours.
- **A separate laundry fits.** Variant D moves the СММ out of the ванная into a closet off the прихожая.
  We had that as a hypothesis with no precedent behind it; now it has one.
- **Wet zones are not re-played.** Not one variant merges туалет with ванная — which agrees with our own
  decision.
- **All four put a washbasin in the туалет**, though the room is well under the 1.4 × 1.5 m that
  СН 3.02.01-2019 §4.9 requires once a basin is present. Practice resolves that conflict in favour of
  ergonomics. See `08_WC/WC_Guide.md`, which already records the tension.

**The analysis lives in `data/layout_cases/dubravinsky-euro3-designer-variants.json`.** This folder is
only the evidence behind it.
