---
source_type: photo survey of a comparable flat — 13 Realt.by listing photographs plus the owner's own annotated positioning plan (camera dot + view arrow + 4-hex id per photo)
source_url: not applicable (listing photographs supplied by the owner)
evidence_file: _Survey/apartment_109_mirrored/ — 13 .jpg plus positioning_plan.png. Bytes gitignored as third-party watermarked material; sha256 for each in _Survey/manifest.csv
fetched: 2026-09-06 (photos), 2026-09-06 (positioning plan, corrected the same day)
publish_date: not applicable — a live listing, condition as at photography
channel: Realt.by listing, unit 109 of this building
source_metadata_location: Minsk, ЖК Дубравинский — the same building as the subject flat
language: ru (plan annotations)
extraction_taxonomy: custom (this project's apartment-geometry taxonomy)
---

# Extraction Note — Apartment 109 photo set (MIRRORED), 2026-09-06

## Evidence levels

(1) photographs as supplied — (2) the owner's positioning plan, which is itself an annotated survey
drawing carrying printed dimensions — (3) measurements I derived from the photographs — (4) external
validation: the owner's tape readings, supplied 2026-09-07, which confirmed some and falsified others.

**⚠️ This flat is MIRRORED relative to the subject flat.** Its лоджия is bottom-right where ours is
bottom-left. Heights survive mirroring; every left/right reading does not.

**⚠️ And its лоджия is 2.5 m² against our 6.05.** That is not a tolerance difference, so *nothing* about
its лоджия transfers — the glazing findings in this note come from the pattern, never the size.

---

## What this source settled

- **The кухня is a zone, not a room.** The surveyor's own label is
  «109-6 жилая с кухонным оборудованием, 25.1 м²» — one room, one area. This was the first *positive*
  confirmation of a finding previously reached only by cropping our own plan and finding no wall.
- **The лоджия is glazed at handover** — `9711`: floor to ceiling, **no parapet**, dark anthracite
  frames, **four vertical bays split by one horizontal transom**, at least one opening casement.
- **Internal door heads ≈ 2050 ±60**, and **no internal doors are fitted** — `a82a` shows three bare
  plastered openings. Its far wall is frontal, so it measures directly; the two 710 openings came out
  754 and 675, averaging 714 against the printed 710.
- **First-fix electrics are in** — a corridor pendant point, a **pair of switch boxes at ~880**, and
  **two unidentified circular boxes at ~2100**.
- **Two ceiling light points in the 25 m² room** (`add8`) — the developer wires that space as two zones.
- **The ceiling is ~2540, not 2500.** `a82a`'s frontal far wall gives a pure ratio —
  head-to-ceiling / floor-to-head = 58/257 — so with a standard 2071 door opening the ceiling is 2538.
  No ceiling assumption is used anywhere in that derivation.

## Uncertainties and corrections this source caused

| item | outcome |
| :--- | :--- |
| the positioning plan first printed `9cf9` **twice** | owner corrected it the same day; the 109-5 dot is `9be4` |
| the three window close-ups supplied earliest | **byte-identical** to apartment 53's `b6f0`/`bdc7`/`9db4` — caught by the sha256 manifest on 2026-09-07, not by inspection |
| ⚠️ my O3 sill reading of 538 from `living_room_window` | **wrong by 272** — the tape says 266. I read the sill board, not the frame base |
| 10 of its 23 id-tagged photos | **still unmapped** — usable for what exists, not for where it is |

## Downstream

- Store: `data/canonical/wall_openings.csv`, `photo_positions.csv`, `electrical_existing.csv`,
  `service_outlets.csv`
- Master pages: `00_Master/Soundproofing_Where_It_Is_Worth_It.md`,
  `00_Master/Photo_Evidence_Request.md`, `00_Master/Evidence_Reading_Discipline.md`
- Canonical record: `data/canonical/wall_materials.json` →
  `photo_position_map_apartment1_2026_09_06`, `O9_loggia_glazing_ANSWERED_2026_09_06`,
  `internal_door_openings_2026_09_07`, `ceiling_height_TESTED_2026_09_07`
