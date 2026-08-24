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

| # | Video ID | Title | Why selected | Outcome | Fact yield | Assessment |
|---|---|---|---|---|---|---|
| 1 | `zBF3iPJfbaw` | Цена ремонта за 1 м2. Сколько стоит ремонт квартиры под ключ. Стоимость ремонта в 2023 году. | Cost-benchmark test — will hit the MDL currency gap if priced in Leu; tests whether the figure is still worth recording as a non-comparable data point | **FULL extraction** | 9 | Upload date 2020-10-20 confirmed via `yt-dlp` (despite on-screen "2023" title). **Currency turned out to be EUR, not MDL** — the anticipated MDL gap did not occur here; USD equivalent still not computable (tool supports neither EUR nor MDL). Region level 2 only. Real cost-driver reasoning (new-build vs. old-fund gap mechanism, small-apartment bathroom-premium mechanism), screed/ceiling QC rules, 10-15% contingency rule. Medium promotional ratio. |
| 2 | `OP8ALhLynHE` | How to save money on apartment renovation? We will give you 12 tips on how to do it! | Budget/planning tips, tests brand-agnostic technique value | **FULL extraction, densest video this round** | 12 | English title, **confirmed fully Russian spoken audio**. Zero absolute price figures — no MDL/currency question at all for this source. 12-tip dense, low-promotional technique list: stretch-ceiling-vs-drywall flood-containment case study, bathtub foam insulation, plastic-baseboard wall-waviness trick, budget kitchen-laminate guidance, tile-trim cost caution, third-channel corroboration of the plastic-vs-plastered window-return crack mechanism, unheated-balcony finish guidance (crossed this store's 3+-source pending-page threshold), and a technical-design deliverables list that turned out to closely duplicate Video 5's own content. |
| 3 | `OcqynathaX8` | 5 фраз и признаков обмана строителями | Contractor-scam signs — tests Mistakes/Warnings-bucket value, likely region-agnostic | **FULL extraction** | 5 | Upload date 2020-07-12. Fully region-agnostic contractor-vetting checklist, zero price figures. 5 concrete red flags (contract refusal, itemized-smeta refusal, false "universal crew" claim, refusal to show past projects, unrealistically short timeline) — cleared the bar for a direct `Budgeting_Guide.md` §4 addition. Low promotional ratio. |
| 4 | `2fLCiWU6U-I` | Why replace pipes in a new building? Polypropylene or Rehau pipes? | Named-technique plumbing tutorial, tests fit against existing `12_Engineering_and_Systems/analysis/` pipe-system content | **FULL extraction** | 6 | English title, **confirmed Russian spoken audio**. **First cross-channel (non-Zemstandart) corroboration** of this store's existing polypropylene joint-narrowing defect, demonstrated on camera with a real cut-open joint comparison — genuinely strengthens an existing claim, not just a new brand mention. Adds a human-factor delayed-failure mechanism and a real leak case (flagged as likely the same incident referenced more briefly in Video 1, not double-counted). Medium promotional ratio (brand repetition). |
| 5 | `Oxv_w9zejsA` | Technical design of an apartment. How to order technical design? What is included in technical design? | Design-process explainer, tests fit against `11_Budget_and_Planning`/technical-design-process content already in the store | **FULL extraction (mostly duplicate)** | 3 | Upload date 2020-10-25. **Confirmed, by direct transcript comparison, the script-overlap flagged when processing Video 2** — same deliverables-list content restated. Not double-counted; only genuinely new content recorded: 90cm switch-height cross-channel corroboration, new 30cm general-outlet-height figure, two additional named deliverable types, a remote/cross-border design-service delivery-model detail. Medium promotional ratio. |

**Round 1 yield**: 5 videos processed, 35 genuinely-new facts (9+12+5+6+3, excluding
duplicate/corroborating-only content), yield = 7.0 new facts/video — well above
the 1.0 floor, roughly in line with this project's other Round 1 baselines
(e.g. Pavel Sidorik's 7.0). No stop-and-ask trigger.

**MDL currency-gap outcome, reported explicitly per the task brief**: no video
in this trial stated a price in MDL. Video 1 stated its two headline prices in
**EUR**, not MDL — a different but equally uncomputable currency for this
project's tooling (`tools/pricing/currency_converter.py` supports only
USD/RUB and USD/BYN). The remaining four videos contained no absolute price
figures at all. The anticipated MDL gap therefore did not materialize in
practice for this specific 5-video sample, though the underlying tooling gap
(no EUR or MDL support) did apply once, exactly as anticipated, just via a
different currency than expected. This doesn't rule out MDL appearing in a
later round from this channel — flagged for the next round's selection to
watch for it.

## Overall Trial Verdict: RECOMMEND FULL-SCALE PROCESSING

This channel cleared the value-filter bar decisively — 5 of 5 videos fully
extracted, zero partial/skipped/failed outcomes, a 7.0 facts/video yield well
above the 1.0 floor and in line with this project's other Round 1 baselines.
Zero videos were pure promotion; the highest promotional-ratio videos (1, 4,
5) were rated "medium," never "high," and every video's checkable technical
content remained separable from its commercial framing. Key findings
supporting full-scale processing:

- **The Moldova/MDL scope flag did not block this trial and, on this
  5-video sample, barely came up in the anticipated form** — one video
  stated EUR prices (not MDL), and USD normalization was equally
  not-computable for that currency; every other video was either
  price-free or, in one case, a real cross-channel corroboration of an
  existing technical fact. **This means the scope flag doesn't change
  the recommendation** — most of this channel's value, at least in this
  sample, is technique/mechanism content, and region-agnostic content
  is fully usable per this project's own existing Russian-source
  precedent, independent of whether a given video's few price points are
  ever normalizable.
- **Genuine cross-channel corroboration, not just more single-account
  content**: Video 4 independently confirmed, with an on-camera
  demonstration, an existing polypropylene-joint-narrowing defect
  previously sourced only from Zemstandart — a real strengthening of an
  existing claim's evidence tier, from a channel with no known
  connection to that one. Video 5 similarly cross-corroborated an
  existing Zemstandart-only mounting-height convention (90cm switch
  height) and added a new figure (30cm general outlet height).
- **A real script-overlap pattern was caught and handled correctly, not
  silently duplicated**: Video 2's tip #12 and Video 5's entire content
  are largely the same deliverables-list script — flagged proactively
  when Video 2 was processed, confirmed by direct comparison when Video
  5 was processed, and only the genuinely incremental content from
  Video 5 was recorded as new fact yield. **Future rounds selecting from
  this channel should actively check for this kind of internal
  script-reuse** (this channel appears to have a recurring
  "core content" segment reused across nominally distinct videos),
  the same discipline already applied to Zemstandart/Zemskov batches.
- **A fully region-agnostic contractor-vetting video (3) cleared the bar
  for a direct `Budgeting_Guide.md` addition** — a useful reminder that
  this channel's value isn't only technique/mechanism content narrowly
  scoped to plumbing/finishes; general renovation-process guidance also
  qualifies.
- **No rate-limiting encountered** — all 5 fetches succeeded on the first
  attempt, spaced by the natural interleaving of full per-video
  extraction/routing work between fetches.

**Recommendation for the next round**: continue processing this channel,
following this project's existing per-round title-skim + spot-check
discipline (per the channel plan's own content-mix notes — the large
"Ремонт квартир в Кишиневе" trend/showcase cluster likely has diminishing
marginal value across near-duplicate years, so prioritize named-technique
tutorials and any remaining cost/scam-adjacent content first). Watch
specifically for (a) an MDL-priced video, to finally exercise that scope
flag in its originally anticipated form, and (b) further instances of this
channel's internal script-reuse pattern.

## Progress Log

- 2026-08-24 — Channel discovered via `preflight_playlist.py` (light mode,
  no rate-limit), title-skimmed (97 titles reviewed), Moldova/MDL scope flag
  recorded, 5-video trial batch selected, this plan file created.
- 2026-08-24 — Round 1 trial batch dispatched and completed: all 5 videos
  fetched (serialized, real spacing via interleaved extraction/routing work),
  no rate-limiting encountered. All 5 fully extracted (35 genuinely-new facts,
  7.0/video yield). Currency scope note: no video stated an MDL price; Video 1
  stated EUR prices instead (also not computable with current tooling); the
  remaining 4 videos had no price figures at all. Wiki-routing performed the
  same session for every source: `13_Surfaces_and_Finishes/Ceilings_Guide.md`,
  `Walls_and_Paint.md`, `Flooring_Guide.md`, `analysis/Windows_Slope_Finishing.md`,
  `analysis/Doors_Trim_Cost_and_Buying.md`, `07_Bathroom/analysis/Tile_Selection_and_Layout.md`,
  `Bathtub_and_Shower.md`, `12_Engineering_and_Systems/analysis/Pipe_Material_Selection.md`
  (first cross-channel corroboration of the polypropylene joint-narrowing
  defect), `11_Budget_and_Planning/Budgeting_Guide.md` §4 (contractor-scam red
  flags). A confirmed script-overlap between Videos 2 and 5 was caught and
  handled without double-counting fact yield. Loggia/Balcony pending-wiki-page
  entry crossed the 3+-source threshold and was flagged (not built this
  session) for a dedicated future pass. Overall trial verdict: **recommend
  full-scale processing** — see verdict section above. `tools/verify_batch.py`
  run against this batch's changes (see verification notes in this session's
  final report).
