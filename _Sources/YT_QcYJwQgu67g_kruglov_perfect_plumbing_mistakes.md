---
source_type: video transcript (self-promotional renovation-company channel, real jobsite walkthrough of rough plumbing/heating + a finished-bathroom preview, Russian, auto-generated captions)
source_url: https://www.youtube.com/watch?v=QcYJwQgu67g
video_id: QcYJwQgu67g
transcript_file: _Archive/processed_sources/20260824_kruglov_perfect_plumbing_mistakes_a188649c.txt
fetched: 2026-08-24
upload_date: 2023-12-08 (metadata-confirmed via yt-dlp `upload_date`)
channel: Konstantin Kruglov | Ontario (presenter self-identifies as "Куцо Никита," руководитель компании Онтарио — same head-of-company presenter as `gKBzDEllg4M`, spelled slightly differently in the ASR transcript)
regional_applicability: level 1 — city named directly and spoken in the video's own content ("квартира 83 м... Москва") describing this specific real jobsite, the strongest regional evidence of any Round 2 source in this batch
currency: RUB (one price figure: leak-protection system "от 25,000 RUB")
language: ru (auto-generated captions, method=youtube-transcript-api, generated=True)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
fact_yield: 13
promotional_ratio: low
corroborates_existing: true
---

# Extraction Note — Konstantin Kruglov/Ontario: PERFECT PLUMBING in Your Apartment, Don't Make These Mistakes (YouTube QcYJwQgu67g)

## Source classification

Video/topical transcript — a real 83 m² Moscow jobsite walkthrough (rough plumbing + heating), plus a preview of an unusual finished bathroom design on the same project. Dominant purpose: technical education anchored in a real, visible install with a directly-spoken location.

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

## Plumbing

Konstantin Kruglov / Ontario says (level 1, spoken directly, real 83 m² Moscow jobsite unless noted):

- **⚠️ PEX pipe insulation-vs-conduit rule**: if routing PEX ("сшитый полиэтилен") pipe without a manufacturer-approved corrugated conduit, use at least 4mm-thick thermal insulation instead — this specific jobsite's developer-installed heating pipe uses corrugated conduit without insulation, which the source notes may be acceptable under that specific pipe manufacturer's own approval and is also more damage-resistant, but is **not** the rule to follow for self-installed PEX: **if you install the pipe yourself, use insulation; if you use conduit, that's specifically the developer's own choice, not a general recommendation.**
- **⚠️ Radial ("лучевая") heating distribution is explicitly praised as rare good practice from a developer**: each radiator gets its own dedicated supply line run directly from the manifold cabinet (no in-floor joints at all), contrasted with the far more common sequential/tee ("последовательная," through branching tees) distribution, which the source states nearly all developers use instead, typically bringing pipes up out of the floor directly at the radiator rather than routing them inside the wall — producing a hole in the finished floor that complicates baseboard installation and looks poor. **Recommendation for self-installed heating: always use radial distribution with pipes chased into the wall to the radiator, never floor penetrations.**
- **⚠️ Installation-frame (инсталляция) anchoring rule**: bolt the frame rigidly to the structural floor slab, not to the not-yet-poured screed, before screed is poured. **Anchor type must match wall material** — for a weak/aerated-block wall, use a chemical anchor specifically, since the frame bears substantial load pressure in use.
- **⚠️ Sewer-line slope and corner-angle rules, with a specific figure**: for 50mm drain pipe, maintain roughly 3cm of slope per linear meter. **Horizontal-direction corner turns should use 45° angles, not a single 90°** — corroborates this store's existing two-45°s-not-one-90° drain rule with a slightly different framing (this source allows a 90° specifically for a vertical-to-horizontal drop transition, matching the existing page's stated exception).
- **⚠️ Hot-left, cold-right at every collector/valve, stated as universal** ("always and everywhere") — corroborates this store's existing hot-left/cold-right convention.
- **⚠️ Riser soundproofing with clamps is cheap and worth doing** — wrapping/clamping ("хомуты") the shared riser pipe meaningfully reduces the risk of riser noise being audible in the living room, at low cost.
- **⚠️ AC condensate needs a dry-trap siphon**, same as this store's existing dishwasher-dry-trap guidance — if installing an AC unit, provide a siphon for its condensate drain line.
- **⚠️ Sequential (tee-branched) plumbing distribution causes a pressure-drop scald/pressure-loss risk** — corroborates the existing collector/manifold-vs-sequential-distribution mechanism already in this store, adds a real client-facing framing (running water at one fixture causes a pressure drop and potential scalding at another fixture on the same branch).
- **⚠️ Pressure reducer can legitimately be omitted at the apartment level if the building already has one at the entry/stairwell riser and the client doesn't want to duplicate it** — a real client decision shown on this jobsite: no reducer installed in-unit because the building's own stairwell-level reducer already regulates supply pressure; the source notes it "could have been added here for convenience" but the client chose not to duplicate it.
- **⚠️ Leak-protection system price point, with region/date/currency all confirmed**: "от 25,000 RUB" (starting price) cited directly for a leak-protection system, described as trivial next to the potential cost of water damage. **USD normalization**: using the confirmed 2023-12-08 publish date and a trailing 6-month USD/RUB average (92.66 RUB/USD, `tools/pricing/currency_converter.py --trailing-months 6`), 25,000 RUB ≈ **$270** (rounded to the nearest $10, below the $1,000 threshold). This is a floor/starting price, not a fixed transaction total, so kept at standard rounding precision rather than treated as an exact figure.
- **⚠️ Pressure-testing protocol, a variant of this store's existing procedure**: for the water-supply system, pressurize to **8 atm** (explicitly not 10, because the manometer gauge itself may not tolerate 10 reliably) and hold for **30 minutes**, checking for any pressure drop or visible dampness; for the heating system, pressurize to **10 atm** and hold the same 30 minutes. This differs from this store's existing Zemstandart-sourced protocol (10 atm across the board, 10-minute hold) in both the water-side ceiling (8 vs. 10 atm) and the hold duration (30 vs. 10 min) — recorded as a distinct practitioner's own protocol variant, not merged into the existing numbers.

## Mistakes / Warnings

- **⚠️ Developer-installed window-sill convectors, a detailed multi-part critique with a real neighbor anecdote**: (1) poor heat transfer — a convector only warms the air immediately around the window rather than the room generally; (2) this specific unit's height forced the screed above the building's normal floor-transition level, something the developer reportedly knew in advance and installed anyway; (3) no decorative closing/trim plate at the finished-floor transition, leaving an unavoidable exposed cut at the joint; (4) the floor area directly around/under the convector can't be used for furniture. **Real comparison anecdote**: a neighbor on the same project kept the developer's convector (this client's crew removed theirs and installed a radiator instead) and later reported struggling with cold in winter, resorting to portable electric heaters. **Fix recommendation**: replace with a horizontal radiator where space allows, or a vertical radiator on an adjacent wall if not.

## Design Concept

- **A real, unusual finished-bathroom preview on the same jobsite (iBox system)**: water-supply-zone control built into the tub itself; a hand-held shower head stored in/pulled from the tub's own rim/ledge rather than a fixed wall mount; the tub fills via its overflow opening rather than a separate spout/faucet (source states this is a first-time observation for them, not a previously-familiar product); a tropical rain shower is also present in the same room. **Electric underfloor heating specifically placed under/near the tub to dry the shower hose after use** (the hose rests on the floor after being tucked back into the rim) — explicitly framed as mold prevention, not just comfort. **Two bathroom walls will get electric-heating-cable-on-wall under porcelain tile as a towel-warmer substitute** (matches this batch's already-recorded heated-wall technique from `gKBzDEllg4M`, corroborating rather than new) — no separate towel warmer will be installed in this room.

## Advertising / Promotional Content Notes

Low promotional ratio. Presenter self-identifies by name/role (head of Ontario). One closing pitch offering a free measurement, quote, and a comparison against competitor quotes ("покажем и докажем что мы лучшие") — a slightly more overtly comparative sales pitch than this batch's other videos, flagged as such, but the technical content itself is not brand/tier-steered.

## Target Page(s)

- `12_Engineering_and_Systems/analysis/Pipe_Material_Selection.md` — PEX insulation-vs-conduit rule.
- `12_Engineering_and_Systems/analysis/Rough_Plumbing_Sequencing.md` — radial vs. sequential heating distribution, 50mm-pipe slope figure (corroborates + sharpens existing 45°/90° drain rule).
- `12_Engineering_and_Systems/analysis/Water_Inlet_Node_Components.md` — riser soundproofing-with-clamps note, pressure-reducer-omission-when-building-level-reducer-exists real client decision.
- `12_Engineering_and_Systems/analysis/Leak_Protection_Systems.md` — 25,000 RUB starting-price figure with USD normalization.
- `12_Engineering_and_Systems/analysis/Pressure_Testing.md` — 8 atm/30-min water-side protocol variant, recorded alongside (not merged with) the existing 10 atm/10-min protocol.
- `12_Engineering_and_Systems/analysis/AC_Condensate_Drainage.md` — AC condensate dry-trap requirement (check for overlap with existing content; likely corroboration).
- `12_Engineering_and_Systems/analysis/Radiators_and_Convectors.md` — developer window-sill-convector critique with real neighbor anecdote (a distinct convector sub-type from this page's existing in-floor-convector content).
- `07_Bathroom/analysis/Bathtub_and_Shower.md` — iBox tub-integrated water control, overflow-fill mechanism, rim-stored hand shower, heated-floor-for-drying-hose mold-prevention technique.
- Wall-mounted heated-wall towel-warmer substitute: noted as corroborating `gKBzDEllg4M`'s already-recorded technique, not re-added as new.

## Relevance to This Project's Topic

Medium-high — a new, checkable numeric price point (leak-protection system) with the strongest regional evidence of any Round 2 source, plus several concrete rough-in QC rules (installation-frame anchoring, PEX insulation) directly useful for this project's own self-managed QC checklist.

## Gaps

- Region: **level 1**, the strongest of any source in this Round 2 batch (city named directly describing the actual jobsite, not just channel branding).
- Only one price figure in the whole video; normalized above.
- The 8 atm/30 min pressure-test variant is not reconciled with this store's existing 10 atm/10 min protocol — recorded as a distinct practitioner variant per this store's non-blending convention for numeric figures.

## Recommended Downstream Routing

Wiki-routed to 7 existing analysis pages (listed above) — existing matching pages found for every genuinely new fact, no `Durable_Facts.md` entry needed.

## Promotion self-check

Re-read in full after drafting. All concrete rules, the one price figure (normalized), and the bathroom design details identified during extraction are reflected in the sections above; the heated-wall towel-warmer mention is explicitly flagged as corroboration, not new.
