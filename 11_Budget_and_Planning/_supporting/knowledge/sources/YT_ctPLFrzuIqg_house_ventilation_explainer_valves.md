---
source_type: video transcript (private-house construction/ventilation contracting channel, technical explainer)
source_url: https://www.youtube.com/watch?v=ctPLFrzuIqg
video_id: ctPLFrzuIqg
transcript_file: _Archive/processed_sources/20260825_house_ventilation_explainer_valves_021d8884.txt
fetched: 2026-08-25 via youtube-transcript-api (manual ru captions)
upload_date: 2023-03-07 (confirmed via yt-dlp metadata, upload_date=20230307)
channel: "Строительство, проектирование, бизнес-обучение" — private-house construction/ventilation contracting company
source_metadata_location: Russia — level 1, directly stated ("если мы возьмём Россию", "у нас в России", RUB pricing throughout); no specific city named
language: ru
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 11
promotional_ratio: medium
corroborates_existing: false
---

# Extraction Note — Private-House Ventilation: Passive Supply Valves + Mechanical Exhaust, Trial-and-Error Design Rationale (YouTube ctPLFrzuIqg)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

A private-house construction/ventilation installer explaining its own standard system design, with named products/brands throughout (Vents "Optima"/"Классика"/"Norvent Pro" supply valves, an unnamed French exhaust-fan brand, "ДЕК"/DEC insulated Dutch ducting, "Остеон" breathers) and its own installation pricing quoted directly. **`promotional_ratio: medium`** — real technical reasoning is present throughout (condensate mechanism, fan-curve-under-load comparison, valve placement physics), but company-own-brand steering is explicit (e.g. dismissing cheaper Chinese valves as not worth the savings, favoring its chosen fan brand's turbine design). Apply this project's tier-steering filter: the mechanism claims (why natural exhaust fails seasonally, why centrifugal turbine fans hold rated output better under duct resistance) are usable market/technique data; the specific brand endorsements are commercial mentions.

**Scope note**: this is a **private house**, not an apartment — several details (attic-mounted fan box, boiler-room ventilation, roof-mounted exterior caps) are house-specific and not directly transferable to an apartment. The core airflow-balance concepts (passive supply valve + mechanical exhaust combination, kitchen-hood-vs-general-exhaust separation, valve/fan sizing logic) generalize to apartments.

## Region Check

**Clears level 1 for Russia** — explicit country-level statements ("если мы возьмём Россию", "у нас в России") plus consistent RUB pricing throughout. No specific city/region named.

## HVAC / Ventilation

- **⚠️ Combined system found empirically superior through trial and error: passive supply valves in "clean" rooms + mechanical (fan-driven) exhaust in "dirty" rooms** — the company states it originally installed fully passive/natural exhaust ventilation but moved away from it after recurring problems (below). `confirmed`, practitioner's own before/after comparison, `single-account`.
- **⚠️ Natural (passive) exhaust ventilation failure mechanism, with seasonal detail**: draft depends entirely on the indoor/outdoor temperature differential and wind — **in summer it effectively stops working entirely** (no meaningful temperature differential to drive stack effect). Only reasonably effective on 2-3 story buildings where the vertical shaft run is long enough (5-7m) to generate real draft; **on single-story houses it's described as "practically ineffective."** [Corroborates and extends the existing "bottle-cap"/stack-effect mechanism already on `Fresh_Air_Ventilation_and_Ducting.md` from the Kruglov/Goncharov source, with a new seasonal-failure and building-height detail.] `confirmed`, mechanism, generalizable.
- **⚠️ Multi-story apartment-building shared exhaust shafts are also unstable across floors, not just in houses**: even a tall shared shaft produces uneven draft by floor — lower floors get excess draft ("гипертяга"), middle floors work normally, **upper floors are described as having no usable draft at all**. `single-account`, `unverified` mechanism claim, but directly relevant to this project's own apartment context (floor position affects natural-exhaust reliability).
- **⚠️ Fan-curve-under-real-load comparison, a concrete example distinct from video 1's abstract fan-curve concept**: a centrifugal-turbine fan design holds its rated output much better under real duct+grille resistance (stable ~100 m³/h at speed 1 in this practitioner's own testing across multiple installs) than a typical screw/vane ("лопастной") duct fan, whose nameplate rating (e.g. 230 m³/h) can drop **30-40%** once real ducting and grilles are attached. `single-account`, concrete comparative claim, self-interested (favors the brand this company sells) but the underlying mechanism (centrifugal turbine vs. vane fan performance-under-load difference) is a checkable engineering claim worth recording with that caveat.
- **Continuous-run requirement for mechanical exhaust, with the specific failure mode if turned off**: even briefly turning off a mechanical exhaust fan lets the duct cool, and warm moist indoor air continuing to rise into the (now static) duct condenses — described as not freezing solid but producing standing water inside the duct/fan housing. Practical mitigation: low power draw (18W) makes continuous operation cheap enough not to matter for the client's electric bill. `confirmed`, mechanism + practical framing.
- **⚠️ Balancing airflow between duct runs of different lengths via inline restrictors, not just end-grille dampers**: named accessory — inline flow restrictors rated at fixed values (15 m³/h and 30 m³/h cited) inserted on the *shorter* duct run specifically, so it doesn't draw disproportionately more air than a longer run off the same fan (air takes the path of least resistance). Restrictors add some noise, so used selectively rather than universally. `confirmed`, technique distinct from (and complementary to) the manual-damper-balancing step in video 1's extraction note — this is a fixed-restrictor approach vs. adjustable-damper balancing.
- **⚠️ Kitchen-hood exhaust must be a fully separate system from the general bathroom/toilet/kitchen background exhaust fan** — corroborating video 1's code-based rule with a mechanistic, non-code reason: grease-laden kitchen air fouls fan blades over time, and accumulated dust building up in that grease film risks fan imbalance. Kitchen hood exhaust is either vented directly outside right above the hood, or routed through the attic to a soffit/eave outlet — never merged into the shared mechanical exhaust duct network. `confirmed`, mechanism distinct from and complementary to video 1's code-citation-based version of the same rule.
- **Supply valve mounting height and placement comfort radius**: standard mounting height 210-220cm from floor (lower when paired with underfloor heating; radiator-integrated valve types mount at radiator height instead, which the source states gives better incoming-air pre-warming since air lands directly on the radiator). **Draft is reported as not perceptible beyond roughly 0.5m from the valve** when correctly positioned away from seating/sleeping zones — a specific placement-clearance figure. `single-account`, practitioner's own field observation.
- **⚠️ Kitchen-hood makeup-air compensation via a dedicated opposite-wall supply valve, distinct from bedroom valves alone**: named product-tier hood airflow figures — 250 m³/h at speed 1, ~300-400 at speed 2, up to 500 at speed 3 — enough to draw down bedroom valves' intended supply if not separately compensated; the fix is a dedicated supply valve placed in the kitchen/living zone roughly opposite the hood, so the hood draws primarily from that valve (with some contribution from bedroom valves) rather than starving the bedrooms' own airflow. `confirmed`, sizing/placement technique, directly extends video 1's balance-table methodology with a hood-specific compensation case.
- **Heat-recovery unit (рекуператор) skepticism, an opinionated single-source claim**: this practitioner considers compact cyclical heat-recovery units (~40-second push-pull cycle) of limited practical value except in a single isolated room with no other supply/exhaust path; cites a **-10°C to -15°C practical low-temperature limit** before internal condensate freezes and supplemental heating becomes necessary, calling the units "a gimmick" in his opinion. `single-account`, `unverified`, opinionated — flag as one practitioner's dismissive view, not a neutral technical consensus (contrasts with the more neutral heat-recovery taxonomy entry already on `Fresh_Air_Ventilation_and_Ducting.md` from the Goncharov source).
- **Breather (бризер) heating-capacity tiering, with named temperature thresholds**: budget-segment breathers with ceramic heating elements are reported to maintain a set temperature only down to about **-20°C**, then shut off heating once unable to keep up; a named premium tier ("Остеон") is reported to work down to **-30°C**. Heater power draw is variable/uncapped by the fan itself, cited range **700W to 1.5kW** depending on outdoor temperature. `single-account`, product-tier claim with specific numbers, `unverified`.

## Material Prices / Labor Prices

Russia, level 1 (country only, no city), 2023-03-07 publish date. Trailing-6-month USD/RUB average used per this project's pricing-precision rule.

- **Exhaust fan + installation**: fan retail **~35,000 RUB**, installation (full ducting, insulated attic-box fabrication) **~30,000 RUB** — combined **~65,000 RUB ≈ $700** (trailing-6-month USD/RUB average to 2023-03-07: ~$693, rounded to nearest 100).
- **Supply valve, installed**: **~5,000-5,500 RUB** per valve including installation labor (~2,500 RUB of that is installation alone) ≈ **$50-$60** per valve.
- **Full small-house system example** (2-3 supply valves + exhaust fan/ducting, kitchen hood ducting included in the fan installation cost, no dedicated recuperator): **~80,000-95,000 RUB ≈ $800-$960** total, i.e. roughly **≈$800-$1,000** in the nearest-$100 bucket.
- **Delivery model**: **Labor-Only-adjacent / small-installer turnkey** — a single specialist company quoting parts + installation as one package for a private house; not comparable to a full-service design-through-furnishing renovation company's overhead structure.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_ctPLFrzuIqg_house_ventilation_explainer_valves|ctPLFrzuIqg]]]

## Confidence & Evidence Notes

- **ASR quality**: manual Russian captions, generally clear, occasional run-on sentence structure typical of unscripted narration — no material ambiguity in the numeric content.
- Single narrator, first-person company explainer format — moderate promotional lean (brand endorsements) but genuine mechanism reasoning throughout, clearing the value filter as **partial**: extract the generalizable mechanisms/technique, flag brand endorsements and single-account opinions (especially the heat-recovery dismissal) explicitly rather than adopting them as neutral fact.

## Assumptions / Uncertainties

- This is a **private house** context by default; house-specific details (attic fan box, boiler-room ventilation, roof vent caps) are recorded for completeness but flagged as not directly apartment-applicable.
- The heat-recovery skepticism and the "30-40% real-world derating" fan comparison are both single-account, somewhat self-interested claims (the second favors the practitioner's preferred fan brand) — recorded with appropriate hedging, not adopted as a neutral engineering consensus.

## Recommended Downstream Routing

- **`tiered-knowledge-base`** — this project's renovation budgeting knowledge store.
- **`12_Engineering_and_Systems/analysis/Fresh_Air_Ventilation_and_Ducting.md`** — adds: natural-exhaust seasonal/height-dependent failure mechanism (extends existing "bottle-cap" content), multi-floor apartment-shaft draft instability, inline-restrictor balancing (distinct from video 1's manual-damper balancing), kitchen-hood makeup-air compensation via a dedicated valve, and a second, more skeptical voice on heat-recovery units (flagged as opinion, contrasting the page's existing more neutral Goncharov taxonomy).
- **5b price normalization complete**: fan+install ≈$700, per-valve ≈$50-60, full small system ≈$800-$1,000 (trailing-6-month USD/RUB average to 2023-03-07).

## Relevance to This Project's Topic

Complements video 1 (bZTJv6aZevw) as a second, independent voice on whole-system airflow balance — where video 1 gave abstract design-engineering methodology, this source gives real installed pricing, a second (partially conflicting/opinionated) view on heat-recovery units, and a concrete kitchen-hood makeup-air compensation case. The private-house framing limits direct applicability but the underlying balance/compensation logic transfers to an apartment context.
