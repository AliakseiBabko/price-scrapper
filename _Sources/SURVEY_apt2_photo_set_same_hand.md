---
source_type: photo survey of a comparable flat — 6 Realt.by listing photographs plus the owner's own annotated positioning plan
source_url: not applicable (listing photographs supplied by the owner)
evidence_file: _Survey/apartment_2_same_handedness_as_ours/ — 6 .jpg plus positioning_plan.png. Bytes gitignored; sha256 in _Survey/manifest.csv
fetched: 2026-09-07
publish_date: not applicable — a live listing, condition as at photography
channel: Realt.by listing, unit 2 of this building
source_metadata_location: Minsk, ЖК Дубравинский — the same building as the subject flat
language: ru (plan annotations)
extraction_taxonomy: custom (this project's apartment-geometry taxonomy)
---

# Extraction Note — Apartment 2 photo set (SAME HANDEDNESS), 2026-09-07

## Evidence levels

(1) photographs as supplied — (2) the positioning plan, itself a dimensioned survey drawing —
(3) derived measurement — (4) no independent validation of this set specifically.

**✅ The best comparable of the three, for two reasons that decide what may be carried across.** It is
the **same handedness** as the subject flat — no left/right correction — and its **лоджия is 6.0 m²
against our 6.05**, where apartment 109's was 2.5. So unlike 109, this flat's лоджия findings *do*
transfer.

Every room tracks: 25 vs our 24.73, 16.7 vs 16.63, 9.3 vs 9.36, corridor 10.1 vs 9.79, ванная 3.2 vs
3.09.

---

## What this source settled

- **The кухня label, a second time**: «Жилая с кухонным оборудованием, 25 м²». Two independent
  surveyors of two different flats both call it one room with kitchen equipment.
- **A third confirmation of the long axis**: 7440 twice against our derived 7460 — after 109's 7450
  and 7460.
- **The kitchen services corner**, from `9e9b`: the extract grille high on the V2 assembly, and a pipe
  at the wall/floor junction. ⚠️ That pipe is where the worst error of the session happened — below.

## Dimension comparison against our model

| dimension | ours | apt 2 | delta |
| :--- | ---: | ---: | ---: |
| big room long axis | 7460 | 7440, 7440 | −20 |
| middle room width | 3000 | 2970, 2950 | −30, −50 |
| G4d / 9.3 room | 2825 | 2790 | −35 |
| big room width at кухня | 3315 | 3250 | −65 |
| **9.3 room depth** | 3400 | 3290 | **−110** ⚠️ |

The last row is the only figure outside the ±50 build tolerance in any of the three surveys, and it has
not been explained.

## ⚠️⚠️ The error this source caused, recorded because the pattern matters more than the number

From `9e9b` I identified a **110 mm sewer socket** at the kitchen wall base, and wrote that its own
measured diameter of 113 mm *"is the check that the scale is right rather than merely plausible."*
**All of that was wrong:**

- it is **DN50** — the owner produced an Ostendorf DN50 product photo
- I had measured the **plastered blob** around the pipe, not the pipe
- ⚠️ and using the object's own size to validate the scale that produced the measurement is
  **circular**. A wrong number wearing a cross-check is worse than a flagged one
- a **functional** check would have killed it before any pixel: DN110 is for a WC, and there is no WC
  in a kitchen

Its kind is still unresolved — sewer branch, water emerging from the floor, or heating. `930d` from
apartment 53 later showed the real kitchen sewer unambiguously.

Also corrected from this source: the screed stencil reads **ВОДОСНАБЖЕНИЕ**, not ОТОПЛЕНИЕ. Which
means the heating route was never recorded, three times over.

## Downstream

- Store: `data/canonical/service_outlets.csv`, `photo_positions.csv`
- Canonical record: `APARTMENT_2_is_the_real_comparable_2026_09_07`,
  `RETRACTION_the_110_sewer_socket_2026_09_07`,
  `RETRACTION_the_floor_stencil_is_VODOSNABZHENIE_2026_09_07`
- Discipline page: `00_Master/Evidence_Reading_Discipline.md` §2, circular validation
