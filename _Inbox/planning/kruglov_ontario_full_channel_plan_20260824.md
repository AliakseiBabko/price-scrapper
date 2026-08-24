# Kruglov/Ontario — Full Channel Processing Plan (started 2026-08-24)

**Channel**: https://www.youtube.com/@konstantin_kruglov_ontario/videos
**Purpose of this file**: single source of truth for processing this entire
channel across many sessions/chats. Read this file first when resuming work
on this channel — do not re-derive the video list or clustering from
scratch. Update the per-round tables and the Progress Log as each round
completes.

## Channel facts

- 119 total videos on the channel as of the 2026-08-24 preflight
  (`_Inbox/planning/preflight_20260824T054611Z.json`).
- 10 already logged in `00_Master/processed_sources.csv` before this plan
  started (4 from the 2026-08-20 batch below, 6 from earlier rounds not
  documented in a dedicated planning file — see CSV directly if needed).
- **109 fresh videos** are the scope of this plan.
- Content is Moscow/CIS-market apartment renovation (titles mix English and
  Russian; explicit Moscow references e.g. `HGN_3WeL0Jk`). Self-promotional
  (Moscow renovation company channel) but historically **technically
  substantive** — see Round 1 below. Still confirm region/year per-source,
  per standing project rule; don't assume from the channel branding alone.
- **Established baseline yield: 11.5 new facts/video** (Round 1, 4 videos).
  Compare later rounds against this; per standing rule, stop-and-ask the
  user if a round's yield falls >50% below the previous round or below the
  absolute floor of 1.0 new fact/video.

## Round 1 (2026-08-20, pre-dates this file — recorded here for continuity)

See full detail in `_Inbox/planning/kruglov_ontario_20260820.md` and
`_Inbox/planning/batch_status_20260820_kruglov_ontario.json`.

| # | Video ID | Title | Outcome |
|---|---|---|---|
| 1 | `9dfEdjOewng` | These Bathroom Mistakes Will Ruin Any Renovation | archived, fact_yield 9 |
| 2 | `dJMsXYUyh7A` | Lighting Your Home Without Mistakes | archived, fact_yield 15 |
| 3 | `ihx8gUDO3vI` | Top Solutions for a Small Kitchen | archived, fact_yield 14 |
| 4 | `09aHjDgl-vk` | 8 Signs of a HORRIBLE Floor Plan | archived, fact_yield 8 |

**Round 1 yield**: 4 videos processed, 46 new facts, yield = 11.5/video.

## Already-logged duplicates (not in scope — listed for reference only)

| Video ID | Title |
|---|---|
| `dJMsXYUyh7A` | Lighting Your Home Without Mistakes (Round 1) |
| `9dfEdjOewng` | These Bathroom Mistakes Will Ruin Any Renovation (Round 1) |
| `ihx8gUDO3vI` | Top Solutions for a Small Kitchen (Round 1) |
| `09aHjDgl-vk` | 8 Signs of a HORRIBLE Floor Plan (Round 1) |
| `P8t_d7J9fm4` | Comprehensive Renovation Cost List for 2026 |
| `6lacLnqpJbM` | The Perfect Bathroom Layout: The Rules They Don't Talk About |
| `gbxv92vD36U` | How to Create the Perfect Bathroom: A Complete A to Z Guide |
| `3vIpdUvgWW0` | Professional repairs vs. private contractors |
| `yHmEQTqduDk` | All about interior doors. How to choose the perfect door? |
| `s1cWUR4l90w` | How to choose plumbing fixtures? |

## Round plan (109 fresh videos, clustered by destination page)

Status vocabulary matches the skill's CSV status field: `pending`,
`fetched`, `extracted`, `integrated`, `archived`, `skipped`, `failed`.
Update the `Status` column as each video moves through the pipeline; add a
one-line **Round N yield** note under each table once a round closes.

### Round 2 — Electrical + Plumbing (7 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `3rbIBKfZDBY` | Electrical Panel in an Apartment: The Most Detailed Guide | archived |
| 2 | `1dp7alivsLQ` | Secrets of safe sockets and switches in an apartment | archived |
| 3 | `gKBzDEllg4M` | THE BEST ELECTRICAL WIRING for modern renovations, from A to Z | archived |
| 4 | `8HnZ2m8vkZQ` | 10 BEST ELECTRICAL SOLUTIONS for your renovation | archived |
| 5 | `4jAQ526Zy2w` | How to assemble the perfect manifold unit in an apartment? | archived |
| 6 | `QcYJwQgu67g` | PERFECT PLUMBING in your apartment. Don't make these MISTAKES | archived |
| 7 | `55zALDsXP2E` | Pinterest Plumbing Review: The Best and Worst Design Choices! | archived |

**Round 2 yield**: 7 videos processed, 72 new facts (11 + 10 + 12 + 9 + 8 + 13 + 9, excluding duplicate/corroborating-only items which were explicitly flagged and not counted), yield = 10.3/video. Compared against the Round 1 baseline of 11.5/video, this is a ~10% drop — well within normal source-to-source variance, not the >50%-drop or <1.0/video stop-and-ask thresholds. No stop-and-ask trigger for Round 3.

### Round 3 — Lighting + Soundproofing + Heating/Ventilation part 1 (7 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `xikuzV80GP4` | The BEST lighting options for your APARTMENT | archived |
| 2 | `1gXYL99mfY4` | Как выбрать освещение в квартире? Главные ошибки! | archived |
| 3 | `2cHetaq1bt0` | All Types of SOUNDPROOFING | archived |
| 4 | `d5a3hti_P8g` | Вся правда об отоплении в квартире: как дурят застройщики | archived |
| 5 | `Is76QlotVFE` | How to choose underfloor heating: hydronic or electric? | archived |
| 6 | `Q1KSHFhLzJo` | All the SECRETS about heating in your apartment! | archived |
| 7 | `uiiggEC7c9M` | Apartments and BREATHERS: what are these air purifiers | archived |

**Round 3 yield**: 7 videos processed, 90 new facts (11 + 10 + 12 + 14 + 10 + 13 + 20, excluding duplicate/corroborating-only outcomes which were explicitly flagged and not counted), yield = 12.9/video. Compared against the Round 1 baseline (11.5/video) and Round 2 (10.3/video), this is the highest-yield round so far — no stop-and-ask trigger. No rate-limiting encountered. **Note**: this round was processed concurrently by two independent agent sessions on the same repo (a real collision, not anticipated at dispatch time) — see the Progress Log entry below for what happened. Both sessions actively reconciled collisions as they were found (duplicate CSV rows removed, duplicate/overlapping wiki sections merged or reverted, duplicate source notes deleted) — as of this update, `git status` and per-video CSV row counts confirm no known duplicates remain (each of the 7 videos has exactly one CSV row); the `uiiggEC7c9M` duplicate source note mentioned in an earlier version of this note was itself deleted during reconciliation and no longer exists.

### Round 4 — Heating/Ventilation part 2 + Bathroom part 1 (7 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `wowlXrlGrEc` | Выкидывай очиститель и увлажнитель! Бризер | pending |
| 2 | `WK-KLd2ssYY` | How to choose an air conditioner: economy vs. premium | pending |
| 3 | `wsomY_6BRqA` | Как выбрать самый лучший кондиционер в 2025? | pending |
| 4 | `sd2XYBZY-K8` | Bathroom Renovation 2026 – Safety, Convenience, and Design | pending |
| 5 | `IFnZxitFeNk` | The Best Bathroom Remodeling Ideas for 2026 | pending |
| 6 | `MOYwhSd8tv4` | Your Tiles Will Crack or Fall Off! Top Rules for Tiling! | pending |
| 7 | `ZlvJE-ncrK8` | Главные ОШИБКИ в ремонте ванной комнаты | pending |

### Round 5 — Bathroom part 2 + Walls/Ceilings part 1 (7 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `1x7srLdq12I` | Все СЕКРЕТЫ создания идеального санузла! | pending |
| 2 | `BDudniuyJ4s` | These are the mistakes everyone makes when renovating a bathroom! | pending |
| 3 | `_XCBMJmosDk` | ИДЕАЛЬНАЯ ВАННАЯ! 10 правил ремонта | pending |
| 4 | `kxr8zFvUTj8` | Bathroom breakdowns from Pinterest. The best and worst! | pending |
| 5 | `W1PKG4tVw_g` | Вся правда о НАТЯЖНЫХ ПОТОЛКАХ — мифы и ошибки | pending |
| 6 | `lhNC30_adGc` | Which Ceiling to Choose? Materials, Cost, and Safety | pending |
| 7 | `qzi1LqwsP5k` | Everything About Decorative Wall Panels | pending |

### Round 6 — Walls/Ceilings part 2 + Flooring part 1 (7 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `xsU4wp9sR8A` | Самые частые ОШИБКИ при поклейке обоев! | pending |
| 2 | `UEy2UN3N3Aw` | Как правильно подготовить стены под покраску | pending |
| 3 | `2it-PLHuJoU` | Краска или обои? Лучшие материал для отделки стен! | pending |
| 4 | `6FbZY6YHrxQ` | ЛУЧШИЕ варианты отделки стен в квартире | pending |
| 5 | `emfnY0TPyaY` | Как не ошибиться в выборе отделки стен в квартире | pending |
| 6 | `SP3NyXmPafI` | Почему трескается стяжка на полу и как этого избежать? | pending |
| 7 | `2Yjg4dAGJI8` | What's the best flooring for a kitchen in 2026? | pending |

### Round 7 — Flooring part 2 + Doors/Windowsills (7 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `I4cUb68iZUg` | The Whole Truth About Laminate! | pending |
| 2 | `puO8alDwL9w` | The Best Flooring Options! | pending |
| 3 | `LNXBHVnP4gs` | Вся правда о кварц-виниловой плитке! | pending |
| 4 | `9f5XxCn2EFM` | The BEST flooring. Parquet, laminate, LVT, or linoleum? | pending |
| 5 | `YvtdjHJhfpU` | How to Choose the Right TILES for Your Home | pending |
| 6 | `a-e5f7yQDRY` | Which baseboards to choose in 2024 | pending |
| 7 | `Tp2VuAaqXgE` | Everything About Windowsills and Window Slopes | pending |

### Round 8 — Kitchen part 1 (5 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `N6UZiZ1-sNI` | Reviewing Stylish Yet Impractical Pinterest Kitchens | pending |
| 2 | `2I77xJIeRwM` | How to build a KITCHEN 10 TIMES CHEAPER? | pending |
| 3 | `SaMpFOPm_4U` | 10 Key Kitchen Trends for 2026 | pending |
| 4 | `f3EI72Nwemk` | The Best Kitchen Ideas of 2026: Top 10 Tricks | pending |
| 5 | `W2KvnHPQdjM` | TOP Best Kitchen Facades 2026 | pending |

### Round 9 — Kitchen part 2 (5 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `e3bHUlP0PMY` | The Most USELESS Kitchen Items! | pending |
| 2 | `A1mvvVObK5M` | Top 10 Kitchen Design Mistakes | pending |
| 3 | `9aVNKzaxGSI` | Топ лучших решений на современной кухне | pending |
| 4 | `FdJLbYEpViU` | ВСЯ ПРАВДА О КУХНЯХ 2026 | pending |
| 5 | `-1HBQkULK4Y` | ТОП 10 популярных ОШИБОК В РЕМОНТЕ КУХНИ! | pending |

### Round 10 — Appliances (5 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `-PfMz_L6pmI` | Which Washing Machine to Buy in 2026? | pending |
| 2 | `AOlNxAlI0So` | How to Choose an Oven in 2026 | pending |
| 3 | `FmGVmt2RH1c` | Which Refrigerator Should You Buy in 2026? | pending |
| 4 | `10sNVkAEATw` | How to Choose a Dishwasher in 2026? | pending |
| 5 | `IuyGPfH85dg` | How to choose a tumble dryer for your home | pending |

### Round 11 — Cost/Budget/Planning part 1 (7 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `rzpkTJYsY0Q` | Repair Estimate! Top Mistakes People Always Make! | pending |
| 2 | `hfJa_QNaN6c` | How consumables eat up 25% of your renovation budget | pending |
| 3 | `zMu1mAFlVPQ` | За что вы переплачиваете при ремонте | pending |
| 4 | `soshw_203eY` | How much does a modern apartment renovation cost? | pending |
| 5 | `nd5WfYyjelg` | All Stages of Rough Renovation in an Older Apartment | pending |
| 6 | `suY0GGTOG9E` | Rough finishes in a new building. All stages and COST | pending |
| 7 | `KNY-XfgbGog` | Как СЭКОНОМИТЬ на ремонте. Топ 8 лучших советов | pending |

### Round 12 — Cost/Budget/Planning part 2 (8 videos)

| # | Video ID | Title | Status |
|---|---|---|---|
| 1 | `Tyl0yPQkO5g` | Cheap vs. Optimal vs. Expensive Repair | pending |
| 2 | `CK7eEeYlLj0` | Как не ошибиться в выборе ПОДРЯДЧИКА для ремонта | pending |
| 3 | `lPmjWTwNVQA` | Top Contractor Scams! Stay Vigilant! | pending |
| 4 | `9lFhda_KDHk` | Вся правда о том СКОЛЬКО времени у вас займет ремонт | pending |
| 5 | `9tScer1xT_E` | Все этапы ремонта квартиры в 2025 году от А до Я | pending |
| 6 | `lLuNbjNXjg0` | Все этапы ремонта квартиры от А до Я в 2024 | pending |
| 7 | `x7wiBaReFN8` | Как сделать качественный ремонт квартиры в 2024 | pending |
| 8 | `dBn4nhn8d9c` | How to Create a Stylish, Budget-Friendly Renovation in 2024 | pending |

### Round 13+ — General decor / "top-N" / apartment-tour cluster (36 videos)

Lowest expected yield — classic thin "top-N tips" / apartment-tour/trend
format for this channel. **Run a title-skim triage pass before dispatching
any sub-batch of this cluster** (per the value-filter rule); expect a
meaningful fraction to be skipped outright rather than fully processed.
Not yet split into rounds — do that at triage time, in chunks of 6-8.

| Video ID | Title |
|---|---|
| `oDHSbp6QRRE` | The Worst and Most Overrated Home Renovation Trends |
| `JIWmxboS-oM` | 16 Things You Will NEVER Find in a DESIGNER'S Home |
| `IXicju8ul1A` | Indestructible Renovation: The Best Materials |
| `xb5pUpTVIJU` | This Interior Looks Cheap! Don't Make These 10 Mistakes! |
| `vm5u5_3v1_U` | How to Choose Curtains? |
| `86fmWWVXark` | Stop Using These Design Trends When Renovating |
| `_pOv1fnV6nM` | 20 Renovation Mistakes That Will Make You Clean Every Day |
| `qt5mQQ6W6Z4` | How to Organize Storage in Your Apartment: 50 Best Ideas |
| `0TLDGD8MY1A` | Top Apartment Renovation Mistakes of 2026 |
| `2rU14i9NqOk` | How to Design the Walk-in Closet of Your Dreams? |
| `a_i8pGVa7-w` | 10 Bedroom Mistakes That Are Keeping You Sleeping Badly |
| `qPi_0cW7aHI` | How to Create an Expensive Interior: 10 Rules |
| `V8c6mwdvpX0` | 13 budget-friendly solutions that make your interior look more expensive |
| `EwI_ZoT3VTQ` | ТОП-11 решений для МАЛЕНЬКОЙ КВАРТИРЫ |
| `A16VC0VYjSQ` | A tour of 5 apartment renovations in 2026 |
| `cHdQtVoFeuo` | Which smart home should you choose? Wired vs. Wireless |
| `zugXvK4CBlM` | How to remove visual noise and create a sense of order |
| `WQhi-AKDPc8` | The Best Home Renovation Apps |
| `Y3Xpww54LpU` | Everything About Smart Homes in 2026 |
| `mJ0uLdys5cE` | The best renovation solutions for 2025 |
| `iEm_mwCJpfA` | Как создать идеальный интерьер, который легко убирать! |
| `Rm4XLdyqj3s` | Тренды в дизайне интерьера 2025 года |
| `BFbNL-DjDh4` | Top 10 Solutions for Your Perfect Bedroom |
| `QyF37JEFpfA` | Топ 12 самых стильных решений в интерьере! |
| `DOJqxZoXCVw` | The top essential tools that every apartment should have |
| `oom96XXQobY` | Все о перегородках в вашей квартире |
| `cM0AndkKdVk` | Топ лучших решений для современной прихожей |
| `kHmUYEX1Lqw` | ОБЗОР стильной двушки |
| `VVxzNTshJCM` | Modern renovation: THESE solutions are a must |
| `kkE25HmFciU` | Худшие решения в ремонте. Не допускайте их! |
| `e0Tp5apV7Ds` | WhiteBox Apartment |
| `xkA8v-0jGqg` | Обзор современной 3-х комнатной квартиры |
| `x8cNF81m7-A` | Топ непрактичных решений в ремонте |
| `N813aS8mI-Y` | TOP 10 Common Home Renovation Mistakes |
| `5mSvRxFJOgE` | The Truth About Sofas: How Manufacturers Rip Off Buyers |
| `HGN_3WeL0Jk` | UNIQUE 1-Bedroom Apartment in MOSCOW CITY 35 sq.m. |

## Progress Log

- **2026-08-24**: Plan created. 109 fresh videos clustered into Rounds
  2–12 (73 videos, topic-dense clusters) plus an unsplit 36-video general
  cluster (Round 13+) pending triage. Round 1 (pre-existing, 2026-08-20)
  folded in as the baseline. Starting Round 2 next.
- **2026-08-24**: Round 2 (Electrical + Plumbing, 7 videos) completed in
  full, no rate-limiting encountered across any of the 7 sequential,
  minutes-spaced fetches. All 7 re-verified fresh against
  `00_Master/processed_sources.csv` and the source-notes folder before
  fetching (no duplicates found). Processed in two topical sub-batches:
  4 electrical videos (`3rbIBKfZDBY` panel-devices guide, `1dp7alivsLQ`
  sockets/switches taxonomy, `gKBzDEllg4M` real jobsite wiring walkthrough,
  `8HnZ2m8vkZQ` "10 best solutions" list — heavy but explicitly-flagged
  overlap between the studio-recorded videos and the real-jobsite one) and
  3 plumbing videos (`4jAQ526Zy2w` manifold-node device guide, `QcYJwQgu67g`
  real Moscow jobsite plumbing/heating walkthrough — the strongest
  regional evidence (level 1, city spoken directly) of any source in this
  round, plus a normalized 25,000 RUB ≈ $270 leak-protection price point,
  `55zALDsXP2E` Pinterest fixture-review format). All 7 routed directly to
  existing `12_Engineering_and_Systems/analysis/` and `07_Bathroom/analysis/`
  pages (14 pages touched total) — no `Durable_Facts.md` entries needed for
  this round. Promotion self-check performed per source. Transcripts
  archived via `archive_transcripts.py` (dry-run then real run, all 7
  matched cleanly). **Round 2 yield: 10.3 facts/video** (72 facts / 7
  videos), a ~10% drop from Round 1's 11.5/video baseline — normal
  variance, does not trigger the stop-and-ask threshold. Next: Round 3
  (Lighting + Soundproofing + Heating/Ventilation part 1, 7 videos).
- **2026-08-24**: Round 3 (Lighting + Soundproofing + Heating/Ventilation
  part 1, 7 videos) completed in full, no rate-limiting encountered.
  All 7 re-verified fresh against `00_Master/processed_sources.csv` and
  the source-notes folder before fetching. **A real concurrent-session
  collision occurred partway through this round**: a second agent
  instance was independently processing this same Round 3 batch on the
  same repo at the same time (not anticipated at dispatch — this wasn't
  a deliberately split chunk). First detected on video 4 (`d5a3hti_P8g`),
  where a complete source note, wiki-routing, and CSV row already existed
  before this session got to it. The collision-safe `run_id` design
  (keyed by video ID, not a counter) meant no CSV row actually collided —
  every video ended with exactly one CSV row, verified by grep count.
  Handling per video: video 3 (`2cHetaq1bt0`) — the other session's
  work fully superseded this session's initial routing with a better
  organization (a new dedicated `13_Surfaces_and_Finishes/analysis/Soundproofing.md`
  page, created once the topic cleared this store's 3+-sources-with-no-page
  threshold); this session's redundant edits to `Durable_Facts.md`,
  `Flooring_Guide.md`, and `Ceilings_Guide.md` were discarded and replaced
  with lightweight pointer links to the new page instead. Videos 4 and 5
  (`d5a3hti_P8g`, `Is76QlotVFE`) — fully completed by the other session
  before this session reached them; only the batch-status file needed
  updating. Video 6 (`Q1KSHFhLzJo`) — both sessions extracted overlapping
  content independently; this session de-duplicated its own wiki edits
  against the other session's (removed a duplicate "Faral" brand mention,
  a duplicate panoramic-glazing-fix section, and a duplicate thermostatic-
  opinion/leak-sensor section from `Radiators_and_Convectors.md`) and kept
  only its own genuinely non-overlapping additions (refined sequential-
  connection count and the 90%-wall-feed statistic on
  `Rough_Plumbing_Sequencing.md`, the loggia speed-caution nuance on
  `Heating_Placement_Rules.md`, a leak-sensor placement nuance on
  `Leak_Protection_Systems.md`, and the presenter's 7-rule checklist on
  `Radiators_and_Convectors.md`). Video 7 (`uiiggEC7c9M`) — **one
  unresolved duplicate remains**: this session wrote its own source note
  (`YT_uiiggEC7c9M_kruglov_breathers_air_purifiers.md`, fact_yield 15) and
  found the other session's independent note
  (`YT_uiiggEC7c9M_kruglov_breathers_podcast_goncharov.md`, fact_yield 20,
  more thorough) already present; this session deleted its own duplicate
  note and deferred to the other session's version and wiki-routing rather
  than reconcile the two, since the other session's CSV row and wiki
  routing (`Fresh_Air_Ventilation_and_Ducting.md`) had already landed by
  the time this session finished reading the transcript. **No content
  loss occurred** — every video has exactly one final source note, one
  CSV row, and consistent wiki routing — but the two sessions' overlapping
  effort was real wasted work, not just a naming collision. **Round 3
  yield: 12.9 facts/video** (90 facts / 7 videos) — the highest-yield
  round to date, no stop-and-ask trigger. **Process note for future
  rounds**: if a round shows signs of concurrent processing again (a
  source note or CSV row appearing that this session didn't write), stop
  and re-check freshness immediately before continuing to the next video,
  rather than assuming the earlier preflight check still holds. Next:
  Round 4 (Heating/Ventilation part 2 + Bathroom part 1, 7 videos).
