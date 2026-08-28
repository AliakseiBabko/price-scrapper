---
source_type: video transcript (solo explainer, channel owner, Russian, ASR auto-generated captions — ru language, not translated)
source_url: https://www.youtube.com/watch?v=9ndMjQLTF9E
video_id: 9ndMjQLTF9E
transcript_file: not separately archived — fetched inline via youtube_transcript_api (sha256 c17b6e3ab1eca4d2103ba735d1c2eb3393735426109176c275c7c84499fbb0f7)
fetched: 2026-08-28 (anonymous, youtube-transcript-api, ru auto-generated/ASR captions, is_translated=false, language_code=ru)
upload_date: 2024-11-07 (confirmed via yt-dlp metadata)
channel: ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ (Vladimir Amelchenko), business/premium-segment turnkey renovation — St. Petersburg/Moscow
regional_applicability: national/unspecified — general electric underfloor-heating cost mechanics, no region-specific claim
currency: RUB, converted at trailing-6-month USD/RUB mean before 2024-11-07 (90.7161 RUB/USD, via tools/pricing/currency_converter.py)
language: ru
extraction_taxonomy: custom (renovation planning)
fact_yield: 9
promotional_ratio: low (a genuine downsides-focused explainer, no active project shown, brief closing plug)
corroborates_existing: partial — heavily overlapping topic area (`07_Bathroom/analysis/Heated_Floor_and_Thermostat.md` already covers area-cap/sensor-redundancy/sensor-embedding-failure-mode content in depth); this source's operating-cost formula, mat-wattage-vs-achievable-temperature point, thermostat-wattage-cap (as distinct from the existing per-mat-area cap), electric-vs-water-heating-as-primary-source cost gap, and repair-triggers-full-floor-redo point are all genuinely new to this vault; note this project has already decided against underfloor heating (see project memory), so this is background/comparative knowledge, not an active planning input
---

# Extraction Note — Vladimir Amelchenko (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ): "The Main Downsides Nobody Talks About | Is Underfloor Heating Worth It?" (YouTube 9ndMjQLTF9E)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference.

## Source Metadata / Promotional Context

**Round 4, video 7 of 8.** A general downsides-focused explainer on electric underfloor heating, no active project shown. **Low promotional ratio.** **Value-filter verdict: full extraction** — genuinely dense with a reusable cost formula and several numeric claims, despite this vault's `07_Bathroom/analysis/Heated_Floor_and_Thermostat.md` page already covering adjacent underfloor-heating territory in depth (checked directly before extracting — several items below are confirmed new, not duplicates). **Project-context note**: this project has already decided against underfloor heating (per this project's own memory), so this source is recorded as comparative/background knowledge, not an active input to this project's own plan.

## Engineering / Systems — Mat Wattage Determines Achievable Floor Temperature

- **⚠️ Named mechanism**: heating mats/cables come in different power densities (real examples given: 130 and 180 W/m²) — a mat too weak for the specific floor buildup (screed thickness, porcelain tile, or self-leveling compound above it) simply cannot reach the temperature the client expects, a common source of the "why isn't my floor heating" complaint. **A hard physical ceiling is stated directly**: underfloor heating cannot reach arbitrarily high temperatures regardless of mat power — there is a real thermal limit above which the floor surface itself cannot get hotter, ruled out by basic thermal physics, not a product-quality issue.

## Engineering / Systems / Budget — Electric Underfloor-Heating Operating-Cost Formula, a Genuinely New Reusable Method

- **⚠️ Named worked formula, distinct from this vault's existing installation-cost figures (~30,000 RUB setup, `Heated_Floor_and_Thermostat.md`) — this is an *operating*-cost method**: (room area in m²) × (mat power density in W/m²) × **0.4** (a stated derating coefficient accounting for the mandatory wall/heat-source/furniture clearance a mat can't cover) = instantaneous power draw. **Worked example**: 30 m² room × 180 W/m² × 0.4 ≈ **2 kW** draw. The floor doesn't run continuously — it heats the covering initially, then cycles periodically to maintain temperature, averaging (per the speaker) **≈9 hours/day active**. 2 kW × 9h ≈ **20 kWh/day**; at an example tariff of **4.5 RUB/kWh**, that's **≈90 RUB/day (≈$1/day)**, **≈2,500 RUB/month (≈$30/month)** for this one 30 m² zone. **Scaled claim**: a 100 m² apartment on underfloor heating is stated to cost **at minimum ≈7,000 RUB/month (≈$80/month)** in electricity — presented as a real, commonly-overlooked ongoing cost most buyers never calculate before installing.
- **⚠️ Named electric-vs-water-heating cost gap when used as a *primary* heat source, not supplemental**: for a 200 m² house, using electric underfloor heating as the sole/primary heat source is estimated at **≈35,000-40,000 RUB/month (≈$390-$440/month)** in electricity, versus **≈3,000-5,000 RUB/month (≈$30-$60/month)** for the equivalent water-based (gas-fired) underfloor heating — roughly a **7-10x** cost gap. **Stated conclusion**: electric underfloor heating should be treated as a supplemental comfort feature (e.g. bathroom floor), never as a house's primary heating source, given this gap.

## Engineering / Systems — A Second, Distinct Thermostat Area-Cap Mechanism

- **⚠️ Named thermostat power limit, a different constraint from this vault's existing ~12 m²-per-mat cap (`Heated_Floor_and_Thermostat.md`, a mat/zone-sizing convention)**: a standard thermostat has its own average power-handling limit of **≈3.5 kW** — at a mat power density of 180 W/m², this caps the maximum area **one thermostat** can control to roughly **≈20 m²**, independent of the mat-sizing convention already documented on this vault's dedicated page. A lower-power mat can cover a larger area on the same thermostat, but the cap always exists.
- **⚠️ Named real design-coordination failure, distinct from — though thematically adjacent to — this vault's existing "multi-mat rooms need a multi-loop plan" fact**: a large open kitchen-living room (the speaker's own recurring example: >40 m²) is sometimes drawn in a design project as one single continuous heating loop/contour, without checking whether a single thermostat can actually support that area — the mismatch surfaces only during installation, forcing a late project correction (splitting into multiple loops/thermostats) and a scramble to find wall space for the additional thermostat(s) not originally planned for. The speaker states this is a recurring problem he now teaches at seminars for designers, and that his own company's designers are trained to check this at the design stage specifically to avoid it.

## Mistakes / Warnings — Repair Consequences Specific to Underfloor Heating

- **⚠️ Named repair-compounding mechanism, genuinely new to this vault**: repairing an underfloor-heating system installed under tile several years earlier (the speaker's example: **3+ years**) commonly runs into a real problem — the original tile is very often discontinued/unavailable by the time a repair is needed, meaning even a small, localized heating-element repair can force a **full floor demolition and re-tile**, since a single replacement tile can't be sourced to match.
- **⚠️ Named specialist-scarcity claim**: locating the exact point to open a floor for an underfloor-heating repair (as opposed to simply replacing an accessible sensor, already covered on this vault's dedicated page) requires a genuine specialist skill, and **very few such specialists exist in the market** — the speaker's own framing: be prepared for a long search and high labor cost if this kind of repair is ever needed.

## Assumptions / Uncertainties

- The 0.4 derating coefficient, the ≈9-hours/day average active-cycling assumption, and the 4.5 RUB/kWh tariff are all the speaker's own stated inputs for a worked example — not independently verified, and the true figures will vary by room layout, climate, insulation, and local electricity tariff.
- The 35,000-40,000 RUB/month (electric) vs. 3,000-5,000 RUB/month (water/gas) house-heating comparison is a single-account estimate for one stated house size (200 m²) — not an audited comparison.
- This project has already decided against underfloor heating; this note is recorded for the knowledge base's general completeness and possible future reference, not because it changes this project's own plan.

## Target Page(s)

- **`07_Bathroom/analysis/Heated_Floor_and_Thermostat.md`** — candidate for the operating-cost formula (distinct from the page's existing installation-cost figure), the mat-wattage-vs-achievable-temperature point, and the distinct thermostat-wattage area cap (as opposed to the existing per-mat-area cap).
- **`12_Engineering_and_Systems/Heating.md` / `analysis/Heating_Type_Selection.md`** — candidate for the electric-vs-water-as-primary-heat-source cost-gap figure, a whole-house heating-strategy consideration beyond the bathroom-specific page's scope.
- **`11_Budget_and_Planning/_supporting/knowledge/intermediate/store/Durable_Facts.md`** — the repair-compounding (tile-unavailability) and specialist-scarcity points, general cross-cutting mistakes-and-warnings content.

## Relevance to This Project's Topic

Although this project has already ruled out underfloor heating, this source contributes a genuinely reusable operating-cost estimation formula and several specific numeric data points (thermostat wattage cap, electric-vs-water primary-heating cost gap, repair-driven full-floor-redo risk) that round out this vault's already-substantial underfloor-heating coverage without duplicating it — useful as reference material should the decision ever be revisited, or for any future source-processing pass on this same topic.
