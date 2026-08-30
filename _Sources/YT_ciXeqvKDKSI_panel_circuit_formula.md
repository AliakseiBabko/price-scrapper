---
source_type: video transcript (single-speaker technical explainer, Russian, ASR auto-generated captions, no punctuation)
source_url: https://www.youtube.com/watch?v=ciXeqvKDKSI
video_id: ciXeqvKDKSI
transcript_file: _Archive/processed_sources/20260804_panel_circuit_formula_31314f45.txt
fetched: 2026-08-04
upload_date: 2019-01-22
channel: Alexey Zemskov / ZEMS group (Zemstandart/Zemsproekt/Zemsremont)
regional_applicability: Belarus/Russia region (channel's usual market); no specific city, code, or standard named — secondary reference, unverified against any electrical code
currency: N/A (no pricing stated)
language: ru (ASR auto-generated, no punctuation)
extraction_taxonomy: custom (renovation planning)
---

# Extraction Note — How Many Circuits an Apartment Electrical Panel Should Have

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference. No electrical code or standard is cited anywhere in this source — all technical figures below are the speaker's stated practice, not verified against a regulatory document.

## Source Metadata

- Single-speaker technical explainer responding directly to a stated pattern of confusion he's observed on construction forums, where people give wildly different answers (from "4" to "30") for how many breaker circuits an apartment needs. Sign-off confirms channel ("на сегодня у меня все с вами был алексей земсков").
- No pricing stated.

## Durable Facts

- No single fixed circuit count exists per apartment size; instead, a **rule/formula** is proposed: every room needs a **minimum of 2 separate circuits** — lighting and outlets. If the room has an AC unit, that's a **3rd** dedicated circuit just for the AC. `unverified`, single-account, but a standard-sounding electrical design principle.
- Electric oven and electric cooktop/hob, where present, each get their **own dedicated circuit/breaker** — not shared with each other or with kitchen outlets.
- A loggia/balcony — whether treated as a separate space or merged into the apartment — gets **one single dedicated circuit**, not split into separate lighting/outlet sub-circuits (treated as one circuit regardless of function).
- Bathroom and WC/toilet outlet circuits should use a **differential breaker (RCD/RCBO — trips on overcurrent AND on earth-leakage current)**, not a plain circuit breaker — stated reasoning: protects against electric shock from leakage current (e.g. from a washing machine) or from water ingress reaching the circuit after a leak from a unit above. `unverified` but consistent with general electrical safety practice, though no code/region is cited.
- The panel should have both a **main isolator/input breaker** (cuts all power to the apartment in one action) and a **main differential/RCD device** (auto-cuts power on a leak or ground fault) — described as standard for "any panel worth its salt."
- The apartment's internal main breaker rating should be set **lower** than the main breaker in the building's riser/floor distribution panel — example given: if the building/riser breaker is 63A, the in-apartment main breaker should be around 50A. `unverified`, stated as the speaker's own example, not a universal figure.
- Counter-argument to "too many circuits is excessive": splitting outlets/lighting/AC per room (rather than e.g. all outlets on one whole-apartment circuit, all lights on another) lets you isolate just one room's outlets — e.g., to childproof a room — without losing that room's lighting or AC; it also prevents a single faulted/flooded room's lighting circuit from cutting lighting to the entire apartment. `unverified`, argued via worked hypothetical examples rather than data.
- **Panel construction/QC checklist**: a good panel should be pre-assembled professionally in a factory/assembly shop (not built on-site), come with a product passport and certificate of conformity, and connect breakers to each other via rigid bus bars rather than loose jumper wires/cable stubs. `unverified`, checkable QC criterion.
- Explicit rule: never fit a higher-amperage breaker than the wire gauge supports (e.g., don't put a 20A breaker on 1.5 mm² wire) — a breaker's job is to trip before the wire overheats from overload; oversizing the breaker relative to the wire lets the wire overheat/ignite before the breaker trips.
- Recommends avoiding oven/cooktop appliances with combined draw above roughly **6 kW** for a typical apartment circuit, even though appliances rated 8 kW+ exist on the market — reasoning: running two such high-draw appliances simultaneously risks tripping the main breaker if wired correctly, or an electrical fire if wired incorrectly. `unverified`, no code citation.

## Numeric Data

Wire gauge / breaker amperage pairing stated by the speaker (Level 1, no code/standard cited — treat as one practitioner's stated practice, not a verified regulatory requirement):

| Circuit type | Cable | Breaker |
|---|---|---|
| Outlets & AC | 3-core, 2.5 mm² per core | 16 A |
| Lighting | cable, 1.5 mm² per core | 10 A |
| Oven/cooktop (single-phase) | 3-core, min. 4 mm² per core | 20 A |

Building riser breaker vs. in-apartment main breaker example: riser 63A → apartment main ~50A (speaker's own example, not claimed universal). `unverified`

## Assumptions / Uncertainties

- No national/regional electrical code is named anywhere in this source; all amperage/gauge figures are presented as the speaker's professional practice, not sourced to a standard. Should not be treated as code-compliant guidance for any specific jurisdiction without independent verification.

## Relevance to This Project's Topic

The most technically dense and directly reusable source in this batch — gives a checkable circuit-count formula, a wire-gauge/breaker-amperage reference table, and a panel-QC checklist, all suitable for the Quick Reference / Key Concepts sections of the Electrical_and_Lighting wiki page. Still `single-account`/`unverified` per the corroboration rule (same channel as the rest of the batch), and explicitly not code-verified.
