---
source_type: video transcript (single-speaker technical guide, Russian, ASR auto-generated captions — no punctuation, occasional transcription errors)
source_url: https://www.youtube.com/watch?v=JrClDJb8WTM
video_id: JrClDJb8WTM
transcript_file: _Archive/processed_sources/20260804_cable_sizing_breaker_selection_99e7c33b.txt
fetched: 2026-08-04
upload_date: 2019-02-04
channel: Alexey Zemskov / ZEMS group (Zemstandart/Zemsproekt/Zemsremont) — Belarus/Russia-region renovation-design company
regional_applicability: Belarus/Russia region (channel's stated market); not Minsk-primary, secondary reference
currency: n/a (no pricing in this video)
language: ru (ASR auto-generated captions, no punctuation — unclear numbers/words flagged `uncertain`)
extraction_taxonomy: custom (renovation planning)
---

# Extraction Note — Alexey Zemskov: Cable Sizing and Circuit Breaker Selection (Curve B/C/D); Terminal Connections vs. Twisting/Soldering (YouTube JrClDJb8WTM)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external/domain validation (none performed). This video is unusually technical/electrical-code-adjacent for this channel; treat numeric standards as this speaker's stated understanding, not independently checked against an actual electrical code text.

## Source Metadata

- Single-speaker technical deep-dive on wire gauge selection, breaker trip-curve selection, and terminal/connection methods. **Single-account** per this project's corroboration rule. Denser and more numerically specific than most videos in this batch.

## Durable Facts — Cable Sizing

- **General current-carrying rule of thumb cited**: 1 mm² of copper conductor cross-section should carry no more than ~9 A continuous, equating to roughly ≤2 kW of connected load per 1 mm².
- **Per-application cable gauge table (as stated by speaker)**:
  - Lighting circuits (switches, two-way/cross switches): **1.5 mm²**
  - Sockets, balconies/loggias, air conditioners: **2.5 mm²**
  - Built-in electric ovens: **4 mm²**
  - Cooktops / instant water heaters: **6 mm²**
- **1.5 mm² and 2.5 mm² (lighting and socket) circuits may be split, joined, and tapped into branches.** **4 mm² and 6 mm² circuits (ovens, cooktops, instant water heaters) must NOT be split, joined, or branched** — each high-draw appliance gets its own dedicated, unbroken home-run cable from the panel. `unverified`, single-account, but a clear and specific rule worth preserving as stated.

## Durable Facts — Breaker (Circuit Breaker) Selection

- **A breaker's job is to protect the wire, not the connected appliance** — it disconnects before the cable overheats, not in response to voltage spikes affecting devices like a fridge or TV.
- **Breakers have two trip mechanisms**: (1) an instantaneous electromagnetic trip for very high (short-circuit-level) current, and (2) a slower thermal trip for sustained overload below the instantaneous threshold.
- **Trip curve/sensitivity categories (B, C, D)** — the speaker states these are the three practically relevant categories for residential work (K and other specialty curves are described as essentially unused in the speaker's market):
  - **Category B** trips at roughly 3–5× rated current (fast/instant trip) — recommended for **all socket circuits**, because sockets can feed devices with high inrush current (example given: a vacuum motor drawing up to ~5× its steady-state current on startup — e.g., a steady 9 A load spiking to ~45 A momentarily) and category B tolerates that inrush without nuisance-tripping while still cutting a genuine overload quickly.
  - **Category C** trips at roughly 5–10× rated current — recommended for **lighting circuits** (mostly resistive/steady loads, no large inrush) and, per the speaker, also acceptable for **fixed power modules like air conditioners** (no large inrush current) at lower cost than category B.
  - **Category D** trips at roughly 10–20× rated current (least sensitive) — speaker recommends **avoiding category D entirely in residential apartments**; states it's intended for industrial settings with large motors/high inrush loads (factories).
- **Breaker-to-cable-gauge pairing given as the "golden mean" (avoiding both nuisance trips and cable overheating)**: cable gauges 1.5 / 2.5 / 4 / 6 mm² should be protected by breakers rated **10 / 16 / 20 / 32 A** respectively. The speaker explicitly criticizes the common malpractice of oversizing the breaker relative to the cable (e.g., pairing a 2.5 mm² cable, rated ~9 A/mm² ≈ ~22 A continuous, with a 25 A or 32 A breaker) — worked example given: a 16 A breaker will hold sustained current up to ~18 A (1.13× rated) for over an hour before thermally tripping, and won't trip near-instantly until roughly 5× rated (~80 A); an undersized-for-load breaker (e.g. 25 A/32 A on a 2.5 mm² circuit) can let a cable run dangerously hot for extended periods before tripping, which the speaker frames as a fire-risk mechanism, not just a theoretical concern.
- **Underlying reasoning for insulation failure**: sustained overheating first embrittles cable insulation, which eventually crumbles/cracks (typically hidden inside a wall where it isn't visible); at a later high-current event the degraded, flexed conductors can then contact each other, causing a short and/or fire. This is presented as the actual failure mechanism behind "don't undersize the breaker for the cable," not overheating itself.

## Durable Facts — Wire Termination Method

- **Spring-clamp/self-clamping terminal connectors (WAGO-style) are recommended over twisting, soldering, or welding wire joints**, for several stated reasons:
  - A modern spring-clamp connector is rated to withstand far more overcurrent-trip cycles than would ever occur in the connection's real service life — the speaker frames "which lasts longer" tests (twist/solder vs. connector) as largely irrelevant marketing theater, since neither would realistically be pushed anywhere near failure in normal residential use.
  - **Twisted/soldered/welded joints are non-reversible** — adding a new tap-off point later (a very common mid-renovation or future-renovation request, per the speaker) requires cutting into and redoing the joint, whereas a clamp connector can simply be reopened and a new wire added. This reversibility is presented as the connector's main practical advantage over the ~50-year service life of a typical installation, not raw electrical performance.
  - Explicitly calls out on-camera "stress test" videos (by unnamed third parties) that push high current through side-by-side twisted vs. clamped joints to make clamps look inferior, arguing these tests remove the protective breaker from the circuit — a scenario that would never occur in a real, code-compliant installation — and are therefore misleading demonstrations, not evidence. `unverified`, single-account opinion/argument, but internally consistent reasoning (a properly sized breaker would trip long before either joint type reaches the current levels shown in such demos).
  - Cites (without a specific brand) that premium/high-end switchgear/busbar equipment also uses spring-clamp-style connections even at high current-carrying capacity, as supporting evidence spring clamps aren't a "budget" compromise. `unverified`.
- **1.5 mm² and 2.5 mm² cable should be joined only with clamp connectors (per the earlier splitting rule); 4 mm² and 6 mm² cable should never be joined at all** — run as a single continuous home-run cable instead (consistent with the cable-sizing section above).
- **Watch for counterfeit/low-quality connector products** — described generically as "cheap plastic toys with thin metal plates" mimicking genuine spring-clamp connectors, contrasted with more robust German-made equivalents (brand not retained here per house style — functional distinction only: genuine self-clamping connectors use a load-bearing metal clamp mechanism, not a token thin metal strip).

## Assumptions / Uncertainties

- No electrical code/standard is named or cited by document number — all numeric thresholds (9 A/mm², B/C/D multiplier ranges, breaker-to-cable pairing table) are presented as the speaker's stated technical knowledge, not sourced to a specific regulation text in the transcript.
- The "45 A vacuum inrush" and "80 A test" example figures are the speaker's illustrative numbers, not measured data.

## Relevance to This Project's Topic

This is one of the most technically dense and broadly reusable sources in this batch for `12_Engineering_and_Systems/Electrical_and_Lighting.md` — cable gauge selection by circuit type, breaker trip-curve selection logic, the cable/breaker pairing table, and a clear technical argument for spring-clamp terminals over twisting/soldering (reversibility for future additions, not just raw strength) are all durable, checkable rules of thumb suitable for a Quick Reference table. All `unverified`/`single-account`, same channel as the rest of this batch — but internally coherent and consistent with mainstream electrical practice (B-curve for inrush-prone socket loads, C-curve for resistive lighting loads) rather than idiosyncratic.
