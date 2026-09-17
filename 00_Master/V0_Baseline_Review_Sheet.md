# v0 baseline — review sheet for the owner

**This is the review that unblocks layout selection.** `v0_named_walls_placed.json` carries `status: "DRAFT — not owner-reviewed."`, and `tools/cad/PROVISIONAL_MODEL_POLICY.md` forbids promoting draft geometry into the sheet a layout decision is read off. Everything downstream — the single-basis v0/v1 comparison, and which of v1's partitions earn their demolition cost — waits on this page.

> [!IMPORTANT]
> **Nobody but the owner can grant this.** A technical review can say the reconstruction is internally consistent and that the gates pass; it cannot say the reconstruction matches what the owner knows the apartment to be. Those are different claims and only the second one unblocks the decision. Codex reviewed the artifact and said so itself.

> [!CAUTION]
> **⚠️ APPROVING THIS DOES NOT MEAN "AS-BUILT".** What is being accepted is that the **planned** geometry is a faithful reading of the developer's drawings. It stays `planned` and `not field-verified` afterwards, and `data/canonical/dimension_tolerance.json` keeps the ±50 mm build tolerance. Nothing here has been measured on site.

---

## What is being reviewed, exactly

Approval is recorded against these bytes, not against "the drawing". If any of them changes, the approval lapses and this sheet must be re-run.

| Artefact | sha256 (first 16) |
| :--- | :--- |
| `_Drawings/review/v0_dxf_readback.png` — **the picture to look at** | `e43018f8ff3c2227` |
| `data/cad/dxf/v0_developer_layout.dxf` | `7dd218d60c305e17` |
| `data/canonical/v0_named_walls_placed.json` | `98a2d1bdb4eae7ac` |

**Commit:** `82b8c86`. The acceptance record is `data/canonical/v0_baseline_acceptance.json`, `pending_owner_review` until the owner says otherwise.

> [!IMPORTANT]
> **The lapse is ENFORCED, not promised.** `tools/layout/check_baseline_acceptance.py` **recomputes all three hashes on every run** and reports the baseline decision-bearing only when the status is accepted, all five scopes are accepted, and no pinned artefact has changed. `compare_variants.py` calls it and prints a **PROVISIONAL** banner on the sheet otherwise; `--require-accepted` makes it refuse outright. An earlier draft stated the lapse in prose while nothing read the file at all.

---

## 1. Wall and opening arrangement

**25 walls** and **11 openings**. `window_frames.csv` holds **four frame MEMBERS** — three mullions and one transom, across `O2`, `O3` and `O4` — not four window assemblies. There are **three** windows (`O2`, `O3`, `O4a`), one loggia door (`O4b`), five internal doors, one passway and the loggia glazing. The walls are `R1a`–`R9` (reinforced-concrete frame), `G1`–`G8` (aerated-block internal), `MA`/`MB`/`MC` (façade) and `M2`/`M6b` (loggia enclosure).

Openings as recorded, with the widths the plan prints:

| | type | host wall | width mm |
| :--- | :--- | :--- | ---: |
| `O1` | door | `G4C` | 710 |
| `O2` | window | `MB` | 1760 |
| `O3` | window | `MC` | 1763 |
| `O4a` | window | `MA` | 600 ⚠ |
| `O4b` | door | `MA` | 770 ⚠ |
| `O5` | door | `G6` | 910 |
| `O6` | door | `G4d` | 910 |
| `O7` | door | `G4C` | 710 |
| `O8` | door | `G2` | 1010 |
| `O9` | glazing | `M2` → `M6b` | 2939 |
| `O10` | passway | `V2` → `R5` | 1455 |

⚠ `O4a`/`O4b` and `O2`'s sill carry a `?` in the record — they are read, not printed.

**What to check:** is any door or window in the wrong wall, on the wrong side, or missing entirely? Position matters more than width here — a width can be corrected later without moving anything else.

## 2. Ventilation shafts V1 and V2

> [!CAUTION]
> **⚠⚠ THREE DIFFERENT NUMBERS EXIST PER SHAFT AND THEY ARE NOT INTERCHANGEABLE.** An earlier draft of this sheet flattened them into one and would have asked for approval of a figure that is not this floor's. They are separated here because the difference is a whole floor band.

| | shaft proper, **this 4th floor** | modelled obstruction | superseded figure |
| :--- | :--- | :--- | :--- |
| `V2` | **421 × 685 mm**, 0.288 m², 3 channels | 400 × 900 mm at x 8980.8–9380.9, y 15090.3–15990.2 | ~~400 × 1140~~ |
| `V1` | **⚠ NOT ESTABLISHED** | 700 × 400 mm at x 3380.9–4080.9, y 15590.3–15990.3 | ~~1140 × 490~~ |

- **The superseded figures are the floors-10-and-up sub-type**, printed on the detailed plan, with **doubled vent sections**. They are not this flat's. V2 was corrected on 2026-09-04 by removing the 455 mm section this floor does not have.
- **The modelled obstruction is larger than the shaft proper** because it includes the enclosed niche around it. That is deliberate — it is what a layout must keep clear of — but it is not the shaft's own size.
- **⚠⚠ `V1` IS FLAGGED, NOT CORRECTED.** The vault records: *"my basic-plan reading gives ~675 × 362, but that implies a 0.315 m² difference where 0.18 is expected. The reading does not reconcile, so V1 NEEDS A CAREFUL RE-MEASUREMENT."* The owner's own statement — V1 has **one** section on this floor, so its length is *"similar to V2"* — gives 685 arithmetically, but that has not been reconciled with the plan reading.

**What to check:** first, whether both blocks are where you remember them and whether there is a **third anywhere we have not drawn** — a shaft is immovable, so a missing one invalidates any layout running through it. Second, and separately: **`V1`'s size is an open question, and accepting this scope does not settle it.** If you accept, it is the *positions* and V2's 421 × 685 you are accepting.

## 3. Loggia outline and glazing

**7 loggia bays**, with `O9` the glazing at **2939 mm**, and the enclosure closing on a **diagonal** south-west face — not a rectangle. The лоджия is **outside the warm perimeter**, so the thermal boundary is the wall between the flat and the лоджия — **not** the лоджия's own glazing `O9`.

> [!NOTE]
> **⚠ The element carrying that boundary is `O4a` + `O4b` hosted in `MA`** — the window and the full-height glass door, in the façade wall. An earlier draft named `M1` here. **`M1` is NOT one of the 25 model walls**: it belongs to the owner's own marking vocabulary in `wall_materials.json`, and `WALL_IDS_ARE_NOT_ALIGNED_WITH_THE_MODEL_2026_09_17` records that *"MA/MB/MC have no obvious counterpart in M1..M7 at all"* and that **no alias map is being written**, because a wrong pairing would authorise chasing a cable into the RC frame. So the reviewable element is `MA` with `O4a`/`O4b` in it, and `M1` is not being asked about.

**What to check:** the diagonal. It is the single most unusual thing in the outline and everything about the loggia's usable depth depends on it being right.

## 4. M2 and M6b

Both 200 mm aerated block, both loggia enclosure.

- **`M2`** — between our loggia and the neighbour's. Its southern **570 mm** is external and insulated; the rest abuts the neighbour's loggia and is not. Settled on the full floor plan, 2026-09-17.
- **`M6b`** — on the rendered façade plane, insulated for its full length.
- Insulation **120 mm assumed, not measured**, on both. Closed as an assumption on your instruction — it is external, so it moves no internal dimension.

**What to check:** nothing about the insulation. What matters is whether `M2` and `M6b` are in the right places and the right thicknesses, because they bound the loggia and the loggia is a room you may use.

## 5. The four open extent exceptions

These are places where the **drawn** length deliberately differs from the **recorded** length. All four are explained and gated; none is an error. They are listed because approving the baseline means approving these too.

| wall | drawn | recorded | Δ | why |
| :--- | ---: | ---: | ---: | :--- |
| `R8` | 1789.7 | 2090 | **−300.3** | owns two corners, but one already overlapped MB's band, so the clamp correctly added nothing |
| `MA` | 2950.1 | 3025 | **−74.9** | drawn **shorter** than the record after two corrections on 2026-09-15 |
| `M2` | 2073.4 | 1850 | **+223.4** | **your own directive** — *"no gap between M2 and MA"* — extended its north end 70 mm to MA's near face |
| `R1b` | 1345.0 | 1200 | **+145.0** | a rectangular-leg figure carved out of the `A_NW_CORNER` monolithic casting; comparing it to a drawn extent is only approximately meaningful |

**What to check:** the `M2` row is the one to read, because it is the only one that records an instruction you gave rather than a compiler consequence.

---

## How to accept

Say so, naming anything from the five sections above that is **wrong** — a correction is more useful than a blanket yes, and a partial acceptance is legitimate: the record has a slot per section. On acceptance the five scopes flip from `pending` to `accepted` against the hashes above, `planned` and `not_field_verified` stay, and `compare_variants.py` becomes decision-bearing.

> [!IMPORTANT]
> **What happens next is NOT "select v1".** The comparison exists to identify **which of v1's partitions actually earn their demolition and rebuild cost** — measured on one consistent basis for the first time. Some may; some may not. That is the question the baseline unblocks, and it is a different question from which layout is nicer.
