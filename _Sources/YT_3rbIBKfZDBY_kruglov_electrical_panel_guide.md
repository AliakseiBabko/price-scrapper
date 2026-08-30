---
source_type: video transcript (self-promotional renovation-company channel, comprehensive electrical-panel-devices guide, Russian, auto-generated captions)
source_url: https://www.youtube.com/watch?v=3rbIBKfZDBY
video_id: 3rbIBKfZDBY
transcript_file: _Archive/processed_sources/20260824_kruglov_electrical_panel_guide_05684af8.txt
fetched: 2026-08-24
upload_date: 2025-07-26 (metadata-confirmed via yt-dlp `upload_date`)
channel: Konstantin Kruglov | Ontario
regional_applicability: level 2 only (channel's established Moscow association; no city named directly in this video's spoken content)
currency: n/a (no pricing content)
language: ru (auto-generated captions, method=youtube-transcript-api, generated=True)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
fact_yield: 11
promotional_ratio: low
corroborates_existing: true
---

# Extraction Note — Konstantin Kruglov/Ontario: Electrical Panel in an Apartment — Most Detailed Guide (YouTube 3rbIBKfZDBY)

## Source classification

Video/topical transcript — a structured device-by-device walkthrough of every component that can appear in a residential electrical panel (main breaker, breaker, disconnect switch, RCD, RCD+breaker combo unit, voltage-monitoring relay, contactor, time/astro relay, surge arrester, meter, smart-home relays, terminal/labeling practice). Dominant purpose: technical education, not a case study or a decision log.

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Dense, systematically organized device-by-device panel guide with real mechanisms explained for each device (why it works, when to use it, cost/space tradeoffs between combining devices). No pricing content. Promotional content confined to a single closing website call-out.

## Electrical

Konstantin Kruglov / Ontario says (all items below, level-1 evidence — spoken directly in the transcript):

- **⚠️ Panel design sequencing is inverted between planning and installation**: planning goes consumer → cable gauge → breaker rating (determine which appliances go on a line, size cable to the load, then pick the breaker to match); physical installation happens in the opposite order — breaker first, then cable, then the consumer is connected last.
- **⚠️ Breaker (автоматический выключатель) has exactly two protective functions, no more**: (1) protects against line overheating/overload — if cable gauge and breaker rating are correctly matched, the breaker trips before the conductor's insulation can overheat or ignite; (2) protects against short-circuit surge current. A disconnect switch (рубильник) by contrast performs no protective function at all — it only manually opens/closes the circuit for a rated current.
- **⚠️ RCD (УЗО) mechanism and sole function**: monitors both the phase and neutral conductor simultaneously and trips the instant the current returning on neutral doesn't match the current sent out on phase (the source's own analogy: two turnstiles counting people in and out — a mismatch means someone/something diverted current, e.g. a shock or a ground fault). Its **only** function is leakage-to-ground protection — it does not protect against overload (will simply burn out) or short-circuit (also just burns out) the way a breaker does.
- **⚠️ RCD+breaker combination math**: a single-pole breaker plus a two-pole RCD together occupy 3 panel slots (RCD=2, breaker=1); a combined differential breaker ("диффавтомат"/RCBO) does all three protective jobs (overload, short-circuit, leakage) in 2 slots. One RCD can protect multiple downstream breakers — e.g. 3 room-socket circuits behind 1 shared RCD uses 5 slots total, versus 6 slots for 3 separate RCBOs — and the shared-RCD combination is noted as meaningfully cheaper than 3 separate RCBOs, though both are valid, correct combinations; the choice is a real cost/space tradeoff, not a correctness question.
- **⚠️ The main incomer (вводной автомат) can be built from several different device types**: a plain breaker, a breaker+RCD combo, a combined RCBO, or (least protective) a bare disconnect switch with no overload/short-circuit protection at all. It commonly lives at the meter location rather than inside the apartment's own panel, in which case a separate disconnect switch inside the apartment panel is a normal, fully-protected combination — the meter-side incomer is already providing the protection.
- **⚠️ Voltage-monitoring relay (реле контроля напряжения / РКН)**: guards against a documented historical failure mode where a grid fault sends 380V instead of 220V into an apartment, destroying an entire stairwell's worth of refrigerators/TVs/appliances at once — cited as a real recurring problem in the 1990s/early 2000s, now largely mitigated at the utility/management-company level in cities but still a live risk in a private house with voltage sag/surge on its own line. Configured with a min/max voltage window; trips outside the window and only re-closes automatically after the voltage stabilizes back inside the window (it does not itself correct/regulate voltage, only disconnects). Most voltage-sensitive listed appliances: refrigerator, washing machine, dishwasher, air conditioner, computers, video-surveillance systems.
- **⚠️ Surge arrester (УЗИП) is distinct from a voltage relay, not a substitute for one**: a voltage relay only disconnects when voltage exits its set range and does not shunt/absorb an impulse; a УЗИП shunts a very large, short-duration surge (its stated example: a lightning strike) into the grounding system fast enough that a voltage relay's disconnect couldn't react in time. Requires a proper grounding system to work at all — the source states it is standard/mandatory practice for private houses and explicitly calls it unnecessary/useless in an apartment.
- **⚠️ Contactor (контактор) use case**: a manually or automatically triggered device that closes/opens a whole downstream group of circuits at once — no protective function of its own. Two named apartment use cases: (1) distributing a single large underfloor-heating load (the source's example: 100 m² of heated floor) across multiple breakers/zones that all still switch together from one contactor; (2) a "master light"/"away/vacation mode" switch that cuts all non-essential circuits with one press, while explicitly keeping a defined exception list live — leak-protection system, router, video-surveillance/alarm, refrigerator, freezer are named as the standard circuits to exclude from the cutoff.
- **⚠️ Time relay / astro-timer**: schedules a circuit by clock time, or (astro-timer specifically) by actual sunrise/sunset via a light-level threshold — cited use case is exterior/landscape lighting or automatic interior navigation lighting at dusk.
- **⚠️ Panel labeling/terminal-block standard**: a modern panel should use professional terminal blocks, comb busbars, and full circuit labeling so that, months after the renovation finishes, anyone opening the panel (including a future contractor who wasn't on the original crew) can identify what each breaker controls without having to dig through old chat history with the original installer.
- Smart-home devices (voice/app-controllable relays, DIN-rail-mounted smart outlets) are named as an additional panel category tied into a smart-home ecosystem, described only at a category level with no specific mechanism or brand claim — kept at `unverified`/generic-category confidence, not a specific rule.

## Mistakes / Warnings

- **⚠️ Aluminum wiring in older ("secondary market") panels is now illegal and actively dangerous**: current code (source cites "ПУЭ" — Russian electrical installation rules) requires copper cable sized to the specific load; aluminum installations are cited as prone to arcing/contact burn-off and a real fire-safety hazard, not just an outdated preference.

## Regulations / Permits / Approvals

- Konstantin Kruglov / Ontario says current Russian electrical-installation code (**ПУЭ**, "Правила устройства электроустановок") mandates copper conductors sized to the specific connected load; this is stated as the reason aluminum wiring in older panels is now non-compliant. — `level 2` regional applicability only (Russia-wide code reference, not city-specific; does not clear this store's stricter regulations-bucket bar for the separate regulations store since no specific jurisdiction beyond "current Russian code" is named).

## Other / Unclassified

- None beyond the above.

## Advertising / Promotional Content Notes

Low promotional ratio. One closing call-out (company website design-project inquiry link for panel-scheme planning, standard channel sign-off asking for likes/subscribes). No mid-video product/brand pushes, no sponsored segment, no tier-steering toward a specific product/brand — the entire body is neutral device-function technique, applicable regardless of which brand of breaker/RCD/relay a reader buys.

## Target Page(s)

- `12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md` — new "Panel Devices — Function & Combination Logic" section: breaker vs. disconnect-switch functions, RCD mechanism, RCD+breaker vs. RCBO slot/cost tradeoff, main-incomer device options, voltage relay, surge arrester (and why it's apartment-irrelevant), contactor use cases (underfloor-heating distribution, away-mode), time/astro relay, panel labeling standard, planning-vs-installation sequencing.
- `12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning.md` — not used; the Cable/Circuits/Panel page is the closer topical match for panel-hardware-specific content.
- Aluminum-wiring code caution → same Cable_Circuits_and_Panel_Design.md page (fits the existing cable-gauge/code content there) rather than a new page.

## Relevance to This Project's Topic

Medium-high — this project's plan is self-managed/itemized, so panel-device selection (RCD vs. RCBO counts, whether a voltage relay/contactor is warranted) is a genuine buying decision the project will face; no pricing given, so it doesn't help budgeting directly, but it is durable planning/technique content.

## Gaps

- Region: level 2 only (channel's established Moscow/Russia association); no city named in this video's own content.
- No pricing content at all — nothing to normalize for this source.
- Smart-home panel devices mentioned only at category level, no specific mechanism — flagged `unverified`/generic, not elevated to a rule.

## Recommended Downstream Routing

Wiki-routed directly to `12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md` (existing matching page found) — no `Durable_Facts.md` entry needed for this source.

## Promotion self-check

Re-read in full after drafting. All concrete, genuinely new device-function facts and combination-logic tradeoffs identified during extraction are reflected in the sections above; the smart-home mention is explicitly flagged as too generic to promote to a rule.
