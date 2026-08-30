---
source_type: video transcript (turnkey renovation company channel, in-house specialist interview + real project walkthrough)
source_url: https://www.youtube.com/watch?v=7vjW6SzHeWM
video_id: 7vjW6SzHeWM
transcript_file: _Archive/processed_sources/20260825_forcemontage_ventilation_types_cost_7ebcbe3a.txt
fetched: 2026-08-25 via youtube-transcript-api (auto-generated ru captions)
upload_date: 2021-10-06 (confirmed via yt-dlp metadata, upload_date=20211006)
channel: Forcemontage - Design and Build — turnkey renovation company
source_metadata_location: unresolved (no city/country named directly; RUB pricing implies Russia but not stated as a country claim in-transcript)
language: ru
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 9
promotional_ratio: medium
corroborates_existing: true
---

# Extraction Note — Forcemontage: Single-Flow vs. Two-Flow Ventilation, Real Project Ceiling-Zone Planning, AC Placement (YouTube 7vjW6SzHeWM)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

Turnkey renovation company channel, interview with an in-house HVAC specialist ("Евгений") walking a real client project. **`promotional_ratio: medium`** — genuine technical content (ceiling-drop-by-zone breakdown, real duct-routing coordination problem, AC placement mechanics) is presented alongside self-promotional framing (own company's design process, own project as showcase). Company/project-specific branding is present but the underlying technique/mechanism content is extractable per this project's advertising filter.

## Region Check

**Not resolved to level 1.** RUB pricing appears but no city/country is named directly in the transcript. Treat pricing as an unresolved-region data point only (per this project's price-comparability rule) — not comparable without further region confirmation.

## HVAC / Ventilation

- **⚠️ Two fundamental system architectures, cleanly distinguished**: **single-flow ("однопоточная")** = passive supply (via window/wall valves, driven only by the vacuum the mechanical exhaust creates) + mechanical exhaust only; **two-flow ("двухпоточная")** = both supply and exhaust are mechanical, either as separate supply/exhaust units or one combined supply-exhaust unit (optionally with heat recovery). **Single-flow's stated tradeoff**: no ability to mechanically/individually regulate how much air reaches each room (it's purely passive, driven by whatever vacuum the exhaust fan happens to create) — chosen specifically where low ceiling height rules out running full ducting through living spaces. `confirmed`, general system-taxonomy distinction, directly complements this page's existing taxonomy (breathers/heat-recovery/central-ducted) with the supply-vs-exhaust-mechanization axis specifically.
- **⚠️ Real-project ceiling-drop-by-zone breakdown, a genuinely concrete worked example distinct from this page's existing single-number duct-drop figures**: technical zone (walk-in closet housing the ducted-AC air handler, exhaust fan, and supply unit) — **350mm** drop; corridor/hallway transit zone — **150-180mm**; bathroom zone (carries the exhaust grille) — also dropped (figure not stated); **living spaces are deliberately kept duct-free, zero ceiling drop**, by concentrating all routing through technical/transit zones only. `confirmed`, concrete real-project numbers, generalizable planning pattern (route everything through non-living zones first, size technical-zone ceiling drop to whatever the largest equipment/duct run needs).
- **Real coordination problem and its resolution: a structural beam forcing a large kitchen supply duct below the beam, requiring furniture/joinery coordination to box and decorate it** — the practitioner states this required direct collaboration between the ventilation trade and the furniture/finishing trades to box the duct attractively rather than leave it exposed. `single-account`, real example, illustrates a genuine sequencing/coordination risk (duct routing decided before kitchen cabinetry design can create a visible conflict needing custom joinery to resolve).
- **Design process sequence stated explicitly**: pre-project concept phase (preliminary airflow-rate calculation, preliminary equipment placement) → commercial proposal → client approval → installation contract → equipment procurement → rough equipment (ceiling-mounted units) installed first → then full ducting distribution. `confirmed`, generalizable project sequencing, corroborates (with more granularity) the general "ventilation contractor produces the real design after the general project" sequencing already on this page (Zemskov source).
- **⚠️ AC outdoor-unit placement options and constraints, four cases**: (1) a pre-designed facade "basket"/cage — no management-company approval needed since it was already accounted for in the building's own design; (2) direct facade mounting without a pre-designed spot — **requires management-company approval**; (3) balcony placement — technically workable but **makes the balcony unusably hot** during AC operation, a real usability tradeoff; (4) **ventilated-facade cavity recessing** — a real solved case: the outdoor unit was mounted on brackets fixed to the building's monolithic slab and recessed into the ventilated-facade cavity, saving boxing space, with a dedicated serviceable access hatch planned separately for maintenance. `confirmed`, real project example, extends this page's existing AC-placement content (which already covers a different building's own facade-condensate-drainage restriction) with a distinct facade-integration technique.
- **Economy-to-premium system cost range, RUB/m²**: **"economy system, probably from 2,500 to 10,000 rubles per square meter"** — region-unresolved, unit-of-area ambiguous (whether whole-apartment area or affected-room area is not clarified in the transcript). Recorded as a bare, low-confidence data point — **do not treat as directly comparable** to this page's existing Oganyan/BURO 5,000-50,000 RUB/m² range (different unrelated source, ambiguous area basis, region unresolved on both) per this project's price-comparability rule; both ranges are recorded side by side as independent, non-reconciled data points. `single-account`, `unverified`.
- **Acoustic treatment fallback when no dedicated silencer/plenum chamber fits**: box the duct/equipment enclosure with additional acoustic lining material as a substitute noise-control measure. `single-account`, technique note.
- **⚠️ Window-sash-integrated humidity-auto-regulating supply valve — installation technique, genuinely distinct from this page's existing window-reveal-routing (L-shaped duct) content**: valve mounted in the *upper part of the window sash itself* (not the wall/reveal) — the sash's pressure-seal strip area is milled/routered without cutting into the window's internal metal reinforcement core; two ~140mm grooves are cut from the interior side; the valve is fitted into this milled channel entirely during finish-stage work (after all wall/ceiling finishing is complete); the exterior side is also milled with two grooves but concealed under the sash handle's own cover plate, leaving **no visible exterior penetration at all**. The valve is described as humidity-sensing/self-regulating (a mechanical damper that reads ambient humidity and opens/closes automatically), and incoming air is directed up toward the ceiling to mix with warm air from the heating system before it can be felt as a cold draft at occupant level. `confirmed`, detailed, checkable installation technique — new to this page (the existing window-reveal content is a wall-cavity L-duct technique for a facade-restricted building, not a sash-integrated valve).
- **Wall-mounted equivalent of the same humidity-regulated valve**: same auto-regulating mechanism, but the duct is chased into the wall behind finish and the valve body is surface-mounted onto the duct opening after finishing — functionally identical air-delivery behavior (rises to ceiling, mixes with heated air) to the window-sash version. `confirmed`, technique variant.

## Confidence & Evidence Notes

- **ASR quality**: auto-generated Russian captions, no punctuation, several garbled/run-on phrases (e.g. repeated fragments, unclear pronoun references) — numeric content (ceiling drops, cost range) is stated plainly enough to extract with confidence; some connecting narrative is ASR-degraded.
- Real project walkthrough with a named specialist, genuinely coherent single-project case study (clears this project's case-study coherence bar) despite `promotional_ratio: medium`.

## Assumptions / Uncertainties

- Region unresolved — RUB implies Russia but no city/country stated directly; pricing recorded as a bare data point only, not used for cross-source comparison.
- Economy/premium cost range's area basis (whole-apartment vs. affected-zone m²) is ambiguous in the source itself.

## Recommended Downstream Routing

- **`tiered-knowledge-base`** — this project's renovation budgeting knowledge store.
- **`12_Engineering_and_Systems/analysis/Fresh_Air_Ventilation_and_Ducting.md`** — adds the single-flow-vs-two-flow architecture taxonomy, the real-project ceiling-drop-by-zone worked example, and the sash-integrated humidity valve installation technique.
- **`12_Engineering_and_Systems/analysis/AC_Key_Concepts_and_Placement.md`** — adds the ventilated-facade-cavity outdoor-unit-recessing technique and the balcony-placement usability tradeoff, extending this page's existing placement content.
- **5b**: pricing recorded as a bare, region-unresolved data point (not converted/compared) per this project's rule.

## Relevance to This Project's Topic

Adds a third independent voice on whole-system ventilation architecture (single-flow vs. two-flow) plus a genuinely new supply-valve installation technique (sash-integrated) not covered by any prior source on this page — directly useful reference material for evaluating a real contractor's proposed system type and installation method.
