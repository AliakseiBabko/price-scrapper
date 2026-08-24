# RemProektMD — Channel Processing Plan (started 2026-08-24)

**Channel**: https://www.youtube.com/@remproektmd/videos
**Purpose of this file**: single source of truth for processing this channel
across sessions. Read this first when resuming — don't re-derive the video
list/clustering from scratch.

**Context**: pulled from `_Inbox/planning/youtube_channel_queue.md`'s Group A
queue (item #3) as the second active channel, after Petrishin-Stroi's Round 1
trial confirmed the session's earlier IP-wide YouTube rate-limit had lifted.

## Channel facts — important scope flag

- 97 total videos, all `fresh` (per `_Inbox/planning/preflight_20260824T122042Z.json`,
  light mode, no rate-limit on the listing fetch).
- **This channel is based in Chișinău (Kишинёв), Moldova** — a genuinely new
  country/region for this project, distinct from every Group A source
  processed so far (all Russia/Belarus-market). "RemProekt" is a Moldovan
  design-and-build company; titles are bilingual Russian/English, several
  explicitly say "Reparatie apartamente Chisinau" (Romanian for "apartment
  renovation Chisinau").
- **Currency gap, flagged before processing**: `tools/pricing/currency_converter.py`
  only supports `USD/RUB` and `USD/BYN` — there is no Moldovan Leu (MDL) rate
  data in `data/scraper.db` or `00_Master/exchange_rates_reference.md`. Any
  MDL-denominated price figure from this channel is **not computable** for a
  USD-equivalent with current tooling (same treatment as this project's
  existing "missing-year" convention — record the raw figure, note the
  conversion isn't computable, don't fabricate or guess a rate). This doesn't
  block technique/mechanism extraction, only price normalization for prices
  actually stated in MDL. Building real MDL rate support (via NBM — Moldova's
  central bank) would be a separate tooling task, not undertaken here without
  the user's go-ahead.
- **Price comparability note**: even where a price is stated in USD/EUR
  directly (this channel's bilingual framing suggests it may quote in
  multiple currencies), Chisinau is a different national market from every
  existing pricing benchmark in this store (Moscow, Minsk, provincial Russia)
  — per the standing "location AND year" rule, any Moldovan price is not
  comparable to this project's Belarus-focused budgeting figures without
  saying so explicitly. Technique/mechanism content is not affected by this
  caveat — general renovation technique is reusable regardless of market.
- **Content mix, from title-skim**: (a) a heavy cluster of "Ремонт квартир в
  Кишиневе" trend/showcase videos (bilingual RU/EN/RO, often overlapping
  script across years — 2023, 2024, 2025, 2026 versions of similar "what
  renovation looks like this year" content, likely low marginal value per
  video once one is processed), (b) named-technique tutorials (large-format
  tile installation, screed, soundproofing, parquet/laminate, decorative
  plaster, technical design/3D visualization process), (c) client
  project-showcase "обзор ремонта" room-tours, (d) a cost-benchmark video
  (`zBF3iPJfbaw`, cost per m²) and a scam-avoidance video (`OcqynathaX8`),
  (e) an "Архив" tag on two very old videos (`BSuQAzR4PMA`, `uZFUtb3qts4`) —
  likely thin/legacy content, low priority.
- Not yet trialed.

## Round 1 — Trial batch (5 videos, dispatched 2026-08-24)

Selected for topic diversity, deliberately including one cost-benchmark and
one scam-avoidance video to test region-appropriate value despite the
Moldova/Belarus market mismatch, plus real named-technique tutorials:

| # | Video ID | Title | Why selected |
|---|---|---|---|
| 1 | `zBF3iPJfbaw` | Цена ремонта за 1 м2. Сколько стоит ремонт квартиры под ключ. Стоимость ремонта в 2023 году. | Cost-benchmark test — will hit the MDL currency gap if priced in Leu; tests whether the figure is still worth recording as a non-comparable data point |
| 2 | `OP8ALhLynHE` | How to save money on apartment renovation? We will give you 12 tips on how to do it! | Budget/planning tips, tests brand-agnostic technique value |
| 3 | `OcqynathaX8` | 5 фраз и признаков обмана строителями | Contractor-scam signs — tests Mistakes/Warnings-bucket value, likely region-agnostic |
| 4 | `2fLCiWU6U-I` | Why replace pipes in a new building? Polypropylene or Rehau pipes? | Named-technique plumbing tutorial, tests fit against existing `12_Engineering_and_Systems/analysis/` pipe-system content |
| 5 | `Oxv_w9zejsA` | Technical design of an apartment. How to order technical design? What is included in technical design? | Design-process explainer, tests fit against `11_Budget_and_Planning`/technical-design-process content already in the store |

Status: **pending dispatch**.

## Progress Log

- 2026-08-24 — Channel discovered via `preflight_playlist.py` (light mode,
  no rate-limit), title-skimmed (97 titles reviewed), Moldova/MDL scope flag
  recorded, 5-video trial batch selected, this plan file created.
