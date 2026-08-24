# Pavel Sidorik — Channel Processing Plan (started 2026-08-24)

**Channel**: https://www.youtube.com/@PavelSidorik/videos
**Purpose of this file**: single source of truth for processing this channel across sessions. Read this first when resuming — don't re-derive the video list/clustering from scratch.

## Channel facts

- 336 videos total as of the 2026-08-24 preflight (`_Inbox/planning/preflight_20260824T072533Z.json`). All showed as `fresh` (never processed) — this channel is new to the project.
- Appears to be a genuine individual practitioner (finisher/tiler/plasterer/electrician), not a company-branded channel — titles read as first-hand hands-on tutorials, "mistakes" videos, and tool reviews, not sales pitches.
- **Two complete, numbered, documented renovation case-study series**:
  - "Renovation in a New Building from A to Z" — roughly #1–#42 (apartment renovation, ~60m², real prices mentioned in several titles).
  - "Remaking a Khrushchevka from A to Z" — roughly #1–#36 (older-building renovation).
  - Plus a separate house-construction series (foundation → roof), lower priority for an apartment-focused project but may carry transferable masonry/concrete technique.
- **Belarus signal, worth confirming per-source**: one title states "Sold a house near Minsk and bought one in a Polish village," another visits someone "in Brest," Belarusian brand/material references appear (Керамин tile, "Belarusian hopper bucket"). This channel is a strong candidate for the new `16_Legal_and_Regulations` folder's level-1 evidence bar (Handover/Acceptance in particular) if confirmed.
- **Content mix**: (a) numbered case-study series entries, (b) standalone technique tutorials (screed, plaster, tiling, drywall, waterproofing, electrical, plumbing, soundproofing, painting) with real overlap/redundancy against the series entries, (c) tool/equipment reviews (laser levels, sprayers, workbenches) — lower priority, mostly buying-opinion not technique, (d) a handful of pure filler (New Year greeting, a conference trip, clickbait) — skip these entirely.
- No duplicates flagged against `00_Master/processed_sources.csv` — genuinely new channel.

## Value-filter assessment (per standing rule — trial before full-scale processing)

This channel has not been trialed yet. Per the project's standing rule for a brand-new channel, run a small trial batch (this round) before committing to full-scale processing of all 336 videos, and report the substance-to-promotion ratio honestly.

## Round 1 — Trial batch (5 videos, dispatched 2026-08-24) — COMPLETE

Selected for topic diversity and highest expected signal, not sequential order:

| # | Video ID | Title | Why selected | Outcome | Fact yield | Substance/promotion assessment |
|---|---|---|---|---|---|---|
| 1 | `hpU_xEXmdvE` | Как принять квартиру у застройщика? Ремонт в НОВОСТРОЙКЕ от А до Я. #1 | Directly relevant to the new `16_Legal_and_Regulations/analysis/Handover_Acceptance_and_Defect_Reporting.md` placeholder — first real candidate source if it clears the level-1 Belarus bar | **FULL extraction** | 9 | High substance, low promotion (1 sponsor segment for Ritter laminate, cleanly excluded). Dense, checkable acceptance checklist with real tolerance figures and named developer pressure tactics from personal experience. **Did not clear the level-1 Belarus bar** — see Region Check below. Routed to general budgeting store, not `16_Legal_and_Regulations/`. |
| 2 | `Oh4hGMZ90mw` | Из чего состоит дизайн проект? Нужен или нет? Цена? | Design-process content, relevant to `11_Budget_and_Planning` and potentially `17_Design_and_Ergonomics` | **FULL extraction** | 8 | High substance, zero promotion. Second independent studio's 20-page design-project structure, materially expanding an existing 28-item checklist; independently re-derives an existing junction-detail recommendation (now double-sourced). Real USD pricing tiers, Belarus level 2 (explicit "largest studio in Belarus" statement, but not spoken as this project's own pricing market). |
| 3 | `0sJPlpi8I2U` | How much does the repair cost in Khrushchev? Overview of the finished apartment. Rework from A to Z | Real cost-benchmark candidate for `11_Budget_and_Planning`/`Budgeting_Guide.md` | **FULL extraction — standout of the batch** | 7 | High substance, zero promotion. Real, complete, self-executed 31.2 m² DIY renovation total, **level-1 Belarus confirmation spoken directly** ("this is the average renovation cost for Belarus"). First self-managed case in this whole store with both level-1 region confirmation and a computable $/m² figure (≈$492-507/m²). Built as a new scoped case study and folded into `Budgeting_Guide.md`. |
| 4 | `C0FOWRxqWX4` | How to Waterproof a Bathroom from A to Z? All Steps. Potential Mistakes. | Dense bathroom technique, tests fit against existing `07_Bathroom/analysis/*` pages | **FULL extraction — densest pure-technique source** | 8 | High substance, zero promotion. Named-product (Ceresit CR65 vs CL51) waterproofing comparison and full technique. **Did not route to `07_Bathroom/analysis/*`** — found a better-fitting existing home at `12_Engineering_and_Systems/analysis/Waterproofing_and_Plastering.md` (a dedicated cross-referenced waterproofing page), which it filled a real gap in (roll/membrane-heavy coverage, thin on brush-on/cementitious technique). |
| 5 | `b0FeObtj2bo` | Основные ошибки при капитальном ремонте! Советы для начинающих! | General "mistakes" format, tests this channel's own promotional ratio | **PARTIAL — weakest source in the batch** | 3 | Low-to-moderate substance, zero promotion. Short, generic, auto-captioned "mistakes" listicle (this channel's oldest video in the trial, 2017). Only 3 genuinely new items extracted (neighbor-negotiation soundproofing angle, 20-100% budget-overrun range, in-person contractor vetting); the rest directly duplicates this same channel's video 1 (ventilation A4 test, 90° corner rule) or restates commonplaces already well-covered elsewhere in this store. |

**Round 1 yield**: 5 videos processed, 35 genuinely-new facts (9+8+7+8+3, excluding duplicate/corroborating-only content), yield = 7.0 new facts/video.

### Region check finding for video 1 (`hpU_xEXmdvE`), per this trial's explicit brief

**Does NOT clear the level-1 Belarus bar.** The speaker names Brest directly and specifically ("Когда мы покупали первую квартиру в Бресте...") — but that is a personal anecdote about a **different, earlier, unrelated apartment** (a one-room panel-building unit), not the monolithic-frame apartment that is the subject of this video/series. For *this video's own object*, the speaker instead states he is applying the **Russian** СНиП/СП code specifically "because most viewers are in Russia" ("большинство зрителей в России, я беру российский свод правил") — an explicit choice that, if anything, points away from a Belarus-location claim for this specific project, or at minimum leaves it unresolved. **Conclusion: level 2 at best for this object; routed to the general budgeting store, not `16_Legal_and_Regulations/analysis/Handover_Acceptance_and_Defect_Reporting.md`.**

By contrast, video 3 (`0sJPlpi8I2U`, a different, earlier, already-completed project by the same channel) **does** clear level 1 directly and unambiguously ("это среднестатистическая стоимость ремонта для Беларуси") — showing the region-evidence bar genuinely varies episode-to-episode on this channel, not something to assume holds (or fails) uniformly across the whole "new building A-to-Z" series. **Recommendation for future rounds**: check each episode's own spoken content individually for a direct Belarus/city naming, rather than assuming the whole 42-episode new-build series inherits video 1's outcome or video 3's outcome by default.

## Overall Trial Verdict: RECOMMEND FULL-SCALE PROCESSING (with light title-based filtering)

This channel cleared the value-filter bar decisively — 5 of 5 videos yielded genuinely new, checkable content (4 full extractions, 1 partial), a 7.0 facts/video yield well above the 1.0 floor and comparable to this project's strongest channels to date (e.g. Category 5's best chunks). Zero videos were pure promotion or filler in this trial. Key findings supporting full-scale processing:

- **Zero sponsor/promotional segments in 4 of 5 videos**, and only one clean, easily-excluded segment in the fifth (video 1's Ritter laminate ad) — this channel's promotional ratio is markedly lower than most turnkey-company channels already processed for this project.
- **Genuine individual-practitioner voice** confirmed directly — first-hand technique, named products, own project costs, candid client-driven compromises (e.g. video 4's skipped vertical-corner taping) — not a company self-promotion channel wearing a personal-channel format.
- **At least one video per project-relevant category delivered a standout, store-strengthening result**: a new best-in-class self-managed case study (video 3), a materially-expanded design-project checklist (video 2), a real gap-fill for an existing engineering page (video 4), and a genuine (if unresolved) Belarus-attribution test case (video 1).
- **The one weak video (video 5) was identifiable in advance by title-genericness and channel-chronology** (this channel's oldest upload, a generic "mistakes" listicle format) — suggesting a light title-skim filter (deprioritize generic "top mistakes"/"tips" titles in favor of numbered case-study-series episodes and named-technique titles) can improve the yield further in future rounds, without needing a strict pre-filter.

**Recommended approach for Rounds 2+**: proceed with **full-scale processing, filtered lightly by format** — prioritize the two numbered case-study series ("New Building A-to-Z," ~42 episodes; "Khrushchevka Remake A-to-Z," ~36 episodes) and standalone named-technique tutorials; deprioritize the tool/equipment-review pool (buying-opinion content, lower technique density per this channel's own plan notes) and skip the identified pure-filler videos (New Year greeting, conference trip, clickbait) outright. Process series episodes in narrative order where practical (per the existing plan's Rounds-2+ note) since they form one real, connected project each. Re-run the explicit Belarus level-1-vs-level-2 region check per episode rather than assuming a fixed answer for the whole channel.

## Rounds 2+ (cluster and dispatch per the verdict above)

**Confirmed series structure** (re-derived directly from the manifest's numbered titles): both series are single continuous documented projects, numbered descending in upload order:

- **"Renovation in a New Building from A to Z"** — episodes **#1–#42**, confirmed complete run. #1 (`hpU_xEXmdvE`) already processed in Round 1 (region: level 2 only for this project). Process the rest **in narrative order**.
- **"Remaking a Khrushchevka from A to Z"** — episodes **#1–#36**, confirmed complete run (`xZBBLG8wd5A` = #1 through `z_gp4eGsSCM` = #36). The cost-overview "finale" (`0sJPlpi8I2U`, level-1 Belarus, already processed in Round 1) is a separate summary video, not part of the numbered run — process #1–36 in narrative order once the New Building series is underway.
- **House-construction series** (~15 episodes, foundation → roof) — lower priority for an apartment-focused project.
- **Standalone technique tutorials** (~180 videos) — cluster by topic once the two main series are underway; expect overlap with series content.
- **Tool/equipment reviews** (~40 videos) — deprioritized.
- **Filler** (New Year greeting, WorldSkills trip, clickbait, joke clips) — skip entirely, never fetch.

### Round 2 — New Building A-to-Z, episodes #2–#8 (7 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `_TGU8C0u010` | Life hacks for apartment renovation. Useful tips. #2 | pending |
| 2 | `H6atjh_g1jQ` | Dismantling work in a new building. Everything you need to know #3 | pending |
| 3 | `ZW-dNzbCREI` | Construction of partitions of a bathroom from blocks. All stages. #4 | pending |
| 4 | `HqmQaZ1y1UM` | The main mistakes when erecting partitions from aerated concrete #5 | pending |
| 5 | `9-NjgDLleOw` | Do-it-yourself electrician in a new building. #6 | pending |
| 6 | `IWVPepWlzSs` | Do-it-yourself electrician in a new building. Episode 2 #7 | pending |
| 7 | `7QuzCGvDG_w` | Electrician in a new building. Cable routing with and without corrugation. Episode 3 #8 | pending |

Further rounds (New Building #9–42, then Khrushchevka #1–36, then technique-cluster rounds) will be planned round-by-round as processing proceeds, given the scale (331 videos remaining) — not fully pre-planned in one pass.

## Progress Log

- 2026-08-24 — Channel discovered and preflighted while the Kruglov/Ontario channel's Round 4 was paused on a YouTube rate-limit — switching channels rather than waiting out the cooldown, per explicit user direction. Plan file created, 5-video trial batch dispatched.
- 2026-08-24 — **Round 1 trial batch complete.** All 5 videos fetched serialized with real spacing (no rate-limit encountered), 4 fully extracted + 1 partial extraction, yield 7.0 new facts/video. Region check performed explicitly on video 1 as instructed: does not clear the level-1 Belarus bar (Brest anecdote is about a different, unrelated apartment); video 3 does clear it directly and became this store's first self-managed case study with both level-1 Belarus confirmation and a computable $/m² figure. Video 4 routed to `12_Engineering_and_Systems/analysis/Waterproofing_and_Plastering.md` (better fit than a `07_Bathroom` page). `Budgeting_Guide.md` updated (self-managed benchmarks section, now 3 references). CSV rows logged (`run_20260824_hpU_xEXmdvE` through `run_20260824_b0FeObtj2bo`, all `archived`). Promotion self-check performed for all 5 source notes. **Verdict: recommend full-scale processing, filtered lightly by format** (prioritize the two numbered series and named-technique tutorials, deprioritize tool reviews, skip identified pure filler). See Overall Trial Verdict section above for full reasoning.
