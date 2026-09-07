---
source_type: photo survey of a comparable flat — 8 Realt.by / Квадратный метр listing photographs plus the owner's own annotated positioning plan
source_url: not applicable (listing photographs supplied by the owner)
evidence_file: _Survey/apartment_53_mirrored/ — 8 .jpg plus positioning_plan.png. Bytes gitignored; sha256 in _Survey/manifest.csv
fetched: 2026-09-07 (three of its photographs were supplied earlier, 2026-09-05, before the flat was identified)
publish_date: not applicable — a live listing, condition as at photography
channel: Realt.by / Квадратный метр listing, unit 53 of this building
source_metadata_location: Minsk, ЖК Дубравинский — the same building as the subject flat
language: ru (plan annotations)
extraction_taxonomy: custom (this project's apartment-geometry taxonomy)
---

# Extraction Note — Apartment 53 photo set (MIRRORED), 2026-09-07

## Evidence levels

(1) photographs as supplied — (2) the positioning plan, a dimensioned survey drawing —
(3) derived measurement — (4) external validation: the owner's tape readings of a very similar flat.

**⚠️ MIRRORED relative to the subject flat.** Its лоджия is 4.1(5.9) m² against our 6.05(4.24) — close
on the full figure, so more transferable than 109's, but not identical.

**⚠️ And three of its photographs were in play for two days before the flat was known.** `b6f0`, `bdc7`
and `9db4` are byte-identical to the window close-ups supplied on 2026-09-05 as "flat unknown". The
sha256 manifest caught it on 2026-09-07 — not inspection. Consequence: those earliest window
measurements came from a **mirrored** flat, which nobody knew at the time. Heights are unaffected;
the O4 window and door leaves sit on **opposite sides** in ours.

---

## What this source settled

**`930d` is the single most informative photograph in the whole survey** — close to frontal at the
kitchen wall, carrying every kitchen service at once:

| item | reading |
| :--- | :--- |
| **SS-K sewer** | grey PVC **horizontal at the wall base**, socket facing into the room, **DN50**, on the screed at ~50–60. Confirms the owner's correction against my retracted 110. Low and horizontal, so fall is easy and a dishwasher or washing machine discharges without a pump |
| **SW-K water** | **two pipes rising out of the floor** — red hot, blue cold, insulated, clamped, brass valves at 500–610, ~92–111 apart. This is what "water reaches the kitchen under the floor" means, and where the ВОДОСНАБЖЕНИЕ stencil leads |
| **SV-K grille** | high on the boxed column, corroborating apartment 2's reading in a second flat |
| **electrics** | **three sockets in a row** at above-worktop height, and a **ceiling light point about a third across the wall** rather than centred — consistent with lighting the zone |

**`ade6` locates P1**, the last unlocated service: the **DN110 main stack** floor to ceiling, flanked by
**two water risers each with an isolating valve and a WATER METER** — matching the developer's
«с установкой счетчиков» — plus a **foil-insulated riser** and branch runs at floor level.

**✅ Sanitaryware is part of the handover** — a WC pan is fitted, seat still in factory wrapping with the
label attached. That answers a question raised twice from dimmer photographs, and it is a budget line
the owner may have been carrying as his own cost.

**The лоджия glazing width**: its plan prints **2.93 m** against our derived **2939** — **9 mm apart**,
the best agreement any figure in this model has achieved against an independent measurement. And it
validates the *derived* trapezoid rather than a measured figure, which is what makes it worth more than
another matching number.

## Uncertainties

| item | state |
| :--- | :--- |
| ⚠️ the scale in `930d` | **two candidates 20% apart** — the visible wall top as a 2500 ceiling gives 3.005 mm/px; a standard 81 mm socket faceplate gives 2.492. Under the first, every derived size lands ~20% high and fits no standard. **Not resolved, and deliberately not picked** — ranges are carried instead |
| its plan's `8431` | the file is `8441.jpg`; one of the two is a misread. Assumed the file |
| the insulated riser | **not confirmed** as heating. It almost certainly is, but the heating route is still recorded nowhere — and a stencil was misread as heating once already |

## Downstream

- Store: `data/canonical/service_outlets.csv`, `electrical_existing.csv`, `wall_openings.csv`,
  `photo_positions.csv`
- Sheets: `_assets/sheet_01_sockets.png`, `sheet_02_lighting.png`, `sheet_03_plumbing.png`
- Canonical record: `kitchen_services_LOCATED_2026_09_07`,
  `P1_zone_LOCATED_and_sanitaryware_ANSWERED_2026_09_07`,
  `O9_glazing_width_CONFIRMED_by_measurement_2026_09_07`
