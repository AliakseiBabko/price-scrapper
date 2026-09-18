---
source_id: YT_FAJubzpKPEI
title: "I Tested ChatGPT on a Real Architecture Project—The Results Surprised Me!"
channel: "AI for Architects"
url: https://www.youtube.com/watch?v=FAJubzpKPEI
video_id: FAJubzpKPEI
upload_date: 2026-08-24
duration: "6:43"
language: en
region: not_region_specific
processed: 2026-09-18
transcript_file: _Archive/processed_sources/FAJubzpKPEI.en.txt
---

# ChatGPT given a real brief, one shot, no coaching — and it failed on closure

A 2,200 sq ft family home on a narrow urban lot 35 ft wide, long axis north–south, neighbours tight both sides. One prompt, no follow-ups, "act as a licensed architect."

## What it got RIGHT — and it is not trivial

- **Site strategy with genuine spatial logic**: main living spaces north, **services and office on the noisy street-facing south side**, bedrooms in the quiet zone. *"A first-year student might get that wrong. ChatGPT didn't."*
- **Code language**: circulation widths, minimum room dimensions, natural-light requirements — and it **raised fire egress and ventilation as design drivers**, *"which most people never even think about until a plans examiner rejects their drawing."*
- **Three massing options with stated trade-offs** — cost, daylight, privacy — in about 90 seconds. Called *"a legitimately strong schematic phase brainstorm."*

## ⚠️⚠️ What it got WRONG — and every failure is a CLOSURE failure

> *"When I stopped asking for ideas and started asking for dimensions, for things you could actually build, the wheels came off."*

- A bedroom **10 ft × 4 ft** beside a bathroom claimed 8 ft deep.
- ⚠️⚠️ **The room widths on one side of the corridor totalled MORE THAN THE WIDTH OF THE SITE.** *"The plan physically could not fit in the lot it had just designed for."*
- A stair: 8 ft 10 in floor-to-floor over **11 risers ≈ 9.65 in each**, against a residential code cap near 8 in. *"Not just uncomfortable — illegal and borderline unusable."*
- Structure: *"appropriate structural systems to be determined by an engineer"*, which the author translates as *"I don't know."*

His conclusion:

> *"ChatGPT can talk about design fluently, but it doesn't actually understand space. It has no spatial model in its head."*

## ⚠️⚠️ THE INVERSE OF THE ОГУРЦОВ FINDING — and together they are a complete picture

| | input | what came out RIGHT | what came out WRONG |
| :--- | :--- | :--- | :--- |
| **Огурцов** (`YT_1WakaBxLkVg`, `YT_KTvihMIPFVk`) | a drawing **with dimensions** | the **geometry** — spot-checks matched exactly | the **identity** — a лоджия read as a duct, taps modelled as glasses, a kitchen mirrored |
| **this test** | a brief with **no geometry** | the **strategy** — orientation, zoning, code drivers | the **geometry** — rooms that do not fit the site, a stair that cannot be built |

> **The model reasons well about RELATIONSHIPS and holds GEOMETRY badly.** Given geometry it transcribes it faithfully but mislabels what things are; given none, it invents geometry that does not close.

⚠️ **AND EVERY DIMENSIONAL FAILURE HERE IS A CHAIN THAT DOES NOT CLOSE** — rooms against site width, risers against floor height. **That is precisely the class `check_dxf_closure.py`, `check_room_rollout.py` and the corner ledger were built to catch**, and standing rule 9 already says to prefer chain closure over judgement wherever a whole is known. This source is outside confirmation that the rule catches the failure that actually occurs.

## What it implies for this project

**Use the model where it is strong and gate it where it is not.** Schematic reasoning — which room should face where, what drives the design, what the trade-offs are — is where it performed. Dimensions, fit and buildability are where it produced confident nonsense, and those are exactly the things this project holds in `data/canonical` and checks with gates rather than asking any model to remember.

## Source Notes

- Promotional: low. The author is explicit that he is not cherry-picking and reports the strong half first.
- No prices. Not region-specific; US code assumptions (riser limits, sq ft).
