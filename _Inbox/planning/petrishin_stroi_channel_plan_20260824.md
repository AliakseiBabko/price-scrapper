# Petrishin-Stroi — Channel Processing Plan (started 2026-08-24)

**Channel**: https://www.youtube.com/@Petrishin-Stroi/videos
**Purpose of this file**: single source of truth for processing this channel
across sessions. Read this first when resuming — don't re-derive the video
list/clustering from scratch.

**Context**: pulled from `_Inbox/planning/youtube_channel_queue.md`'s Group A
queue (item #2) as a fresh, untried channel, after Kruglov/Ontario, Pavel
Sidorik, and TimRemont all hit the same rate-limit/IP-block signature earlier
in the session (see that queue's protocol section). Per explicit instruction,
none of those three are being retried yet — this is new-channel work run in
parallel with that cooldown.

## Channel facts

- 341 total videos, all `fresh` (per `_Inbox/planning/preflight_20260824T122033Z.json`,
  light mode, no probing — no rate-limit encountered on the listing fetch
  itself, which is a mild positive signal but not proof the caption-fetch
  IP-block has lifted).
- Run by Сергей Петришин ("Петришин-Строй"), a Moscow-area renovation
  company (mix of English/Russian titles, similar bilingual pattern to
  Kruglov/Ontario and TimRemont). Channel spans 2017-2026.
- **Content mix, from title-skim**: (a) a large recurring "ошибки
  ремонта"/"mistakes" clickbait format (very heavy — probably the single
  largest category on this channel), (b) real named-technique tutorials
  (plastering by beacons, screed, tiling, electrical, waterproofing,
  demolition), (c) client case-study "Отзыв №N" / room-tour videos with
  real apartment sizes and sometimes real total costs, (d) a notable
  cluster of videos explicitly framed as **"Ремонт по проекту Алексея
  Земскова"** (renovation to a design by Alexey Zemskov) — this is the
  same Zemskov already fully triaged as a source channel in this project
  (see [[project_zemskov_channel_triage_complete_20260819]]) — these
  videos are a different contractor's (Petrishin's) execution of a
  Zemskov-designed project, a genuine cross-source corroboration
  opportunity, not a duplicate. (e) equipment/tool reviews and a "Виноградный"
  numbered episodic series (2016-17, ЖК Виноградный, ~13 episodes) similar
  in structure to Sidorik's/Kruglov's numbered series.
- Not yet trialed.

## Round 1 — Trial batch (5 videos, dispatched 2026-08-24) — COMPLETE

Selected for topic diversity and highest expected signal (technique +
real-cost case studies), deliberately avoiding the generic "ошибки"
clickbait format for this first pass per the value-filter rule. This
trial doubled as a live re-test of the IP-wide YouTube rate-limit that
had blocked Kruglov/Ontario, Pavel Sidorik, and TimRemont earlier in
the session:

| # | Video ID | Title | Why selected | Outcome | Fact yield | Substance/promotion assessment |
|---|---|---|---|---|---|---|
| 1 | `D1REgSDwILU` | Basics of COMPETENT plastering | Named-technique tutorial, tests baseline substance | **FULL extraction** | 8 | Low promotional ratio (one Telegram plug, no product pitch). Dense substrate-prep/priming matrix, 3 named betonokontakt failure modes, a building-settlement deformation-seam mechanism, a numeric QC checklist, and a real materials/labor cost split (741,950 RUB total). **Region: level 2 only** — no city named in-video. Also confirmed the rate-limit block had lifted (this was the first fetch attempt of the session's new-channel test). |
| 2 | `E7M-bWWSmfw` | Как сделать стяжку. Этапы, советы, ошибки. Полусухая механизированная стяжка. | Screed technique + cost/steps, tests fit against existing `13_Surfaces_and_Finishes` / `Flooring_Guide.md` | **FULL extraction** | 6 | Low promotional ratio. Object is a **country house**, not an apartment — **region unresolved**, weaker than this channel's usual level-2 Moscow association. Genuinely new screed-delivery method (semi-mechanized "полуручка" pumped screed) not previously in this store, plus a concrete curing routine. |
| 3 | `S23VRWxzz08` | Сколько стоит черновой ремонт в 2022? Подробный разбор на реальном примере! | Real cost breakdown case study — tests region/year-resolved pricing value | **FULL extraction — real case study** | 9 | Low-to-medium promotional ratio. First Petrishin-Stroi cost benchmark for this store: 1,424,000 RUB rough-stage total, 45 m², ≈$430/m² (Turnkey/Full-Service). **Region: level 2** — named ЖК "River Park," city not spoken. Plumbing-stage sub-costs ASR-garbled, deliberately not extracted as numbers. |
| 4 | `caDB-roRasI` | От чего трескаются стены? Приемка кладки, как должно быть? | Masonry defect/acceptance criteria — tests technique + possible handover/acceptance relevance | **FULL extraction — densest technique source in the batch** | 12 | Zero promotional content, filmed on an active job site. Dense foam-block partition masonry acceptance/QC checklist, corroborating and substantially extending existing partition content with several new checkable rules (flashlight joint-check, 7mm plumb tolerance, reinforcement-frequency floor, deformation-joint specs, door-ear/casing rule, lintel spec). **Region: level 2** — no city named. |
| 5 | `8IW762yALfc` | Ремонт в Москве стоимость всех черновых работ. Показываем реальный объект 2024. | Real 2024 rough-work cost object — second cost-benchmark test, most recent of the batch | **FULL extraction — real case study, ⚠️ first level-1 region source on this channel** | 8 | Medium promotional ratio (one direct sales call-to-action, cleanly excluded). Second Petrishin-Stroi cost benchmark: 1,122,000 RUB rough-stage total (full-gut demolition, no floor area stated so no $/m²). **Region: level 1 — clears the bar directly** (a specific Moscow street, "Нахимовский проспект," named in the source). |

**Round 1 yield**: 5 videos processed, 43 genuinely-new facts (8+6+9+12+8, excluding duplicate/corroborating-only outcomes), yield = 8.6 new facts/video.

### Rate-limit re-test outcome

Video 1 fetched successfully on the very first attempt of this trial —
confirms the IP-wide block that hit Kruglov/Ontario, Pavel Sidorik, and
TimRemont earlier in the session has lifted. All 5 videos in this batch
fetched cleanly, serialized one at a time with real spacing (achieved
by interleaving each video's own full extraction/routing work between
fetches, never an idle wait), zero rate-limit signatures encountered
anywhere in the batch. This clears the way to resume the three paused
channels in a future session, in addition to continuing this one.

### Region-check finding, per this trial's explicit brief

Consistent with every other Group A channel processed so far: this
channel's own level-1-vs-level-2 region evidence **varies video to
video**, not a fixed channel-wide answer. 3 of 5 videos in this trial
stayed at level 2 (channel-level Moscow association only — no city
named in the video's own spoken content); 1 of 5 (video 2) didn't even
clear level 2, since its object is explicitly a country house, breaking
the channel's normal apartment/Moscow context; and video 5 became the
**first source on this channel to clear level 1 directly**, via a
specific named Moscow street ("Нахимовский проспект"). **Recommendation
for future rounds**: check each video's own spoken content
individually for a direct city/street/district naming, exactly as
already established for Pavel Sidorik's channel — don't assume a fixed
region outcome for this channel as a whole.

### Zemskov-cluster cross-check

None of the 5 videos in this trial referenced or overlapped with the
channel's separate "Ремонт по проекту Алексея Земскова" cluster (per
the channel plan's own note above) — no cross-check was triggered.
That cluster remains untouched, to be picked up deliberately in a
future round if it's prioritized.

## Overall Trial Verdict: RECOMMEND FULL-SCALE PROCESSING (with light title-based filtering)

This channel cleared the value-filter bar decisively — 5 of 5 videos
fully extracted, zero partial/skipped/failed outcomes, an 8.6
facts/video yield well above the 1.0 floor and above Pavel Sidorik's
own Round 1 baseline (7.0). Zero videos were pure promotion; the two
videos with any commercial content at all (videos 3 and 5) each
carried exactly one cleanly-excludable sales/CTA segment, with the
remainder of both videos being dense, checkable technical/cost content.
Key findings supporting full-scale processing:

- **Deliberately avoiding this channel's heavy "ошибки"/mistakes
  clickbait format for the trial selection worked as intended** — all
  5 selected videos (named-technique tutorials + real cost-breakdown
  case studies) turned out genuinely substantive, not thin dunk-style
  content. This doesn't yet tell us how the "ошибки" format itself
  performs — that's still untested and should get its own small
  spot-check in an early future round before assuming it's low-value
  (per the value-filter rule's own warning that title sentiment alone
  isn't a reliable filter).
- **Two independent real cost-benchmark case studies** (2022 and 2024)
  were captured in one trial, one of which (video 5) delivered this
  channel's first level-1-confirmed region — a genuinely useful,
  rare combination (real numbers + resolved location) this project's
  price-comparability rule specifically asks for.
- **Dense, checkable technique content with several genuinely new
  mechanisms**, not just corroboration: a building-settlement
  deformation-seam concept that recurred at two different construction
  stages (plastering in video 1, masonry in video 4) — a real
  cross-video mechanism, not a duplicate, since it's the same
  underlying principle applied at two different stages of the same
  kind of project.
- **This company channel's promotional ratio is markedly lower than
  the trial's own prior expectation** for a turnkey-company channel —
  only 2 of 5 videos carried any commercial framing at all, and both
  were still majority-technical.
- **The rate-limit re-test succeeded cleanly**, meaning this channel
  imposes no distinct access risk beyond the general serialized-fetch/
  real-spacing discipline already standard for every channel.

**Recommended approach for Rounds 2+**: proceed with **full-scale
processing, filtered lightly by format** — prioritize named-technique
tutorials and real-object cost-breakdown videos (this channel has
several more of both visible on the manifest, including 2025/2026-dated
cost-breakdown videos that would extend the two-point year-over-year
benchmark started this round); do an early small spot-check of the
"ошибки"/mistakes format specifically (title-genericness alone
shouldn't be trusted as a filter per the value-filter rule, and this
project has been burned both ways — Zemskov's misleadingly-generic
"how not to" titles turned out positive, Kruglov's genuinely
low-substance "$X wasted" dunk videos turned out negative); re-run the
explicit per-video region check every round rather than assuming a
fixed channel-wide outcome; and leave the "Ремонт по проекту Алексея
Земскова" cluster for a deliberate, separately-scoped future round
rather than folding it into ordinary technique/cost rounds.

## Progress Log

- 2026-08-24 — Channel discovered via `preflight_playlist.py` (light mode,
  no rate-limit on the listing fetch), title-skimmed (341 titles reviewed),
  5-video trial batch selected and this plan file created. Dispatching
  Round 1 next.
- 2026-08-24 — **Round 1 trial batch complete.** All 5 videos fetched
  serialized one at a time with real spacing (interleaved with each
  video's own full extraction/routing work, never idle waiting), zero
  rate-limit issues — this also confirmed the IP-wide YouTube block that
  had earlier stopped Kruglov/Ontario, Pavel Sidorik, and TimRemont in
  this same session has lifted (video 1 succeeded on the first attempt).
  All 5 fully extracted. Yield 43 new facts / 5 videos = 8.6 facts/video,
  above the 1.0 floor and above Pavel Sidorik's own Round 1 baseline
  (7.0). Per-video region check performed explicitly: 3 of 5 stayed at
  level 2 (channel-only Moscow association), video 2's object (a country
  house) didn't clear even level 2, and **video 5 became this channel's
  first source to clear level 1 directly** (a named Moscow street,
  "Нахимовский проспект"). Two independent real cost-benchmark case
  studies (2022: 1,424,000 RUB / 45 m² / ≈$430/m²; 2024: 1,122,000 RUB,
  no area given) were added to `Budgeting_Guide.md` as new live-intake
  benchmarks, explicitly not averaged together (different scopes, no
  shared area basis) and explicitly distinguished from Kruglov/Ontario's
  rough-materials-only figures already on that page. Technique content
  routed the same session to `12_Engineering_and_Systems/analysis/
  Waterproofing_and_Plastering.md` (substrate-prep/priming matrix,
  betonokontakt troubleshooting, a building-settlement deformation-seam
  mechanism), `13_Surfaces_and_Finishes/Flooring_Guide.md` (a genuinely
  new semi-mechanized screed method), and `07_Bathroom/analysis/
  Structure_and_Framing.md` (a dense foam-block partition masonry
  acceptance/QC checklist). A real cross-video mechanism echo (the
  building-settlement deformation seam recurring at both the plastering
  stage, video 1, and the masonry stage, video 4) was flagged explicitly,
  not double-counted. None of the 5 videos overlapped with the channel's
  separate Zemskov-project cluster, so no cross-check was triggered.
  `tools/verify_batch.py` run against the pre-round commit; all 5 new
  CSV rows independently re-verified via Python's `csv` module to parse
  into the correct 15 columns each with `archived` status. **Verdict:
  recommend full-scale processing, filtered lightly by format** — see
  the Overall Trial Verdict section above for full reasoning and the
  Rounds 2+ recommendation.

## Round 2 — Technique cluster + "ошибки" format spot-check (8 videos, dispatched 2026-08-24)

Continues full-scale processing per the Round 1 verdict. Prioritizes this
channel's own "Как выглядит качественная X? Материалы, лайфхаки и главные
ошибки" comparison-format series (electrical, plumbing, plastering, screed,
demolition — a structured technique+mistakes hybrid, distinct from the pure
dunk-style clickbait), plus a deliberate 2-video spot-check of the "Как
УБИТЬ X" clickbait format per the Round 1 recommendation to test it early
rather than assume either way.

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `Q6GKMOJuaPc` | Как выглядит качественная электрика? Материалы, лайфхаки и главные ошибки. | Electrical technique+QC series | **FULL extraction** | 9 | Substantial overlap with existing Kruglov/Sidorik electrical content (not re-extracted). New: built-in-appliance socket placement, cooktop cable length, floor-mesh-over-membrane fix, low-voltage transformer ceiling avoidance, aquastop power feed, outlet-box flush-fit QC, underfloor sensor conduit, furniture-maker coordination (3rd-practitioner corroboration). Region level 2. Low promotional ratio. |
| 2 | `OgIZhrxD4v4` | Как выглядит качественная сантехника? Материалы, лайфхаки и главные ошибки. | Plumbing technique+QC series | **FULL extraction** | 9 | Substantial overlap with existing plumbing sequencing/pressure-test content (not re-extracted). New: utility-cabinet rough-in rules, radiator sill-alignment check, pre-closure pipe photo-documentation, towel-warmer sustained-run test, shower-valve-height mistake, tile-thickness mixer-centering mistake. Region level 2. Low promotional ratio. |
| 3 | `r1eyXzXNdI0` | What Does Quality Plastering Look Like? Materials, Hacks, and Common Mistakes. | Plastering technique+QC series (English title) | **FULL extraction** | 5 | English title, **confirmed Russian spoken audio**. Heavy overlap with this same channel's own Round 1 plastering video (`D1REgSDwILU`) — same-channel restatement, not independent corroboration, not re-extracted. New: beacon rust-bleed-through mechanism, corner-mesh mid-depth detail, scoped 90°-corner rule, coin-press QC test, plaster-thickness photo-documentation. Region level 2. |
| 4 | `Y9PGtPmcMms` | What Does Quality Floor Screed Look Like? Materials, Life Hacks, and Major Mistakes. | Screed technique+QC series, tests against Round 1's new screed method | **FULL extraction** | 11 | English title, **confirmed Russian spoken audio**. **No overlap with Round 1's semi-mechanized screed method** — complementary QC-checklist angle. Staged-payment heuristic, 4-factor strength model + 2 compaction tests, 6cm+ thickness recommendation, a 4th distinct curing-protocol variant, tolerance bait-and-switch warning, coin test applied to screed, corner-defect mechanism, T-cut deformation joint, QC-timing rule. Region level 2 (Moscow named only as company service area). Medium promotional ratio. |
| 5 | `zxTbtAbuXFs` | Как выглядит качественный демонтаж? Лайфхаки и главные ошибки. | Demolition technique+QC series | **FULL extraction, densest video this round** | 14 | Second source in the store's "Demolition" topic area (still below 3-source page threshold), zero overlap with the first (Sidorik). Written scope-of-work, furniture/window/door protection, temp lighting/sink, 3-tactic neighbor-relations practice, debris-disposal negotiation, pre-priming dedusting, flooring-to-substrate removal, panel-ceiling-joint/exterior-corner treatment, developer-insulation replacement, ⚠️ named 7-apartment flooding incident, ventilation-shaft resize lifehack. Region level 2. Low promotional ratio. |
| 6 | `NjOkuREH8lI` | Как выбрать затирку? Основные ошибки и главные секреты. | Grout-selection technique, tests fit against `Tile_Selection_and_Layout.md` | **FULL extraction** | 5 | ⚠️ Different framing — Sergey Petrishin's own personal-project video (his own house), not a company case study; region does not clear even level 2. Internal-corner-silicone/epoxy-wet-zone rules corroborate existing Zemskov content (not re-extracted). New: tile-sample shopping tip, monolithic-vs-contrast color rule, ⚠️ photographically-demonstrated white/light-grout floor-traffic discoloration warning, brand-texture comparison, matching-silicone tip. Low promotional ratio. |
| 7 | `xd1xP2FuN40` | Как УБИТЬ ПЛИТКУ. Все ОШИБКИ укладки. Советы и лайфхаки | "Как убить X" clickbait-format spot-check #1 (tiling) | **FULL extraction** | 11 | **Format spot-check: dense, substantive, NOT thin dunk-style filler** — structurally identical to the positively-titled series. Layout/centerline technique, two tile-detachment mechanisms, internal-corner grout-washout mechanism, SVP leveling clips, grout-finish check, fixture-penetration hole-saw technique, acceptance electrical check, floor-protection practice, cost-risk labor pricing. Region level 2. Medium promotional ratio. |
| 8 | `VcrYHkDgb0o` | Как УБИТЬ СТЕНЫ. Все ОШИБКИ малярных работ. Советы и лайфхаки | "Как убить X" clickbait-format spot-check #2 (painting) | **FULL extraction, second-highest yield this round** | 12 | **Format spot-check confirmed a second time: dense wallpaper/paint acceptance checklist, not thin filler.** First wallpaper/paint QC content on `Walls_and_Paint.md`. Wallpaper seam/corner/pattern checklist, ⚠️ raking-light inspection-lamp technique with a pricing implication, painted-wall defect checklist, dark-wallpaper installer lifehack, ceiling-molding checklist, finish-protection rule. Region level 2. Medium promotional ratio. |

**Round 2 yield**: 8 videos processed, 76 genuinely-new facts (9+9+5+11+14+5+11+12, excluding duplicate/corroborating-only outcomes), yield = 9.5 new facts/video — **above Round 1's 8.6 baseline**, well above the 1.0 floor, no stop-and-ask trigger.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 8
videos fetched serialized one at a time with real spacing (achieved by
interleaving each video's own full extraction/routing/CSV/archiving work
between fetches — never an idle wait), consistent with Round 1's own
clean result. This further confirms the IP-wide block from earlier in
the session remains lifted.

### "Как убить X" format spot-check — explicit finding

Both spot-checked videos (7 and 8) turned out to be **structurally
identical to this round's positively-titled "Как выглядит качественная
X?" acceptance-checklist series** — each opens with only a brief
clickbait cold-open (a few seconds) before settling into the same
substantive substrate-prep → technique → acceptance-checklist format as
the rest of the round. Both delivered yields (11 and 12) at or above the
round's own average (9.5), and above 6 of the other 6 videos. **This
channel's "Как убить X" title format is demonstrably not a negative-value
signal** — consistent with, and reinforcing, this project's standing
value-filter warning that title sentiment alone is not a reliable
predictor (title-genericness cuts both ways across channels: Zemskov's
"how not to X" turned out uniformly positive, Kruglov's "$X wasted"
dunk-format turned out genuinely thin, and this channel's "Как убить X"
now joins the positive column). **Recommendation for future rounds on
this channel**: include the "Как убить X" format on equal footing with
the channel's other technique/QC series — do not deprioritize it by
title alone.

### Region-check finding, per this round's explicit brief

Consistent with Round 1's own finding: region evidence varied video to
video, not a fixed channel answer. 6 of 8 videos stayed at level 2
(channel-only Moscow association); video 4 had one sales CTA naming
Moscow/Moscow-region as the company's own *service area* (not the
object's location), correctly kept at level 2 rather than promoted to
level 1; video 6 (personal-project video, Sergey Petrishin's own house)
did not clear even level 2, since it's not necessarily located in/near
Moscow the way the company's client projects are. No video in this round
cleared level 1 directly (unlike Round 1's video 5).

### Language check, per this round's explicit brief

Videos 3 and 4 both carry English on-screen titles; both were
individually verified via the `youtube-transcript-api` fetch metadata to
have Russian spoken audio (`language: ru`) — fetched and cited in
Russian throughout, per this project's standing rule. No English-audio
video was encountered in this round.

### Cross-check findings, per this round's explicit brief

- **Video 4 (screed) vs. Round 1's semi-mechanized ("полуручка") screed
  method**: no overlap — video 4 is a general acceptance/QC checklist,
  not a delivery-method video. Genuinely complementary, not corroborating
  or contradicting.
- **Videos 1 (electrical) and 2 (plumbing) vs. existing Kruglov/Sidorik
  content in `12_Engineering_and_Systems/analysis/`**: substantial
  overlap found and correctly **not** re-extracted (junction-box-open-
  for-fault-test, temp-outlet test, equipotential bonding, white-cable
  red flag, 2-breakers/room heuristic, plumbing-after-plastering
  sequencing, hot-left/cold-right, two-45° elbows, 10-atm pressure test).
  Both videos still yielded 9 genuinely new items each once the overlap
  was set aside.
- **Video 3 (plastering) vs. this same channel's own Round 1 plastering
  video**: heavy same-channel restatement of the acceptance-checklist
  numbers (2mm gap, 1mm/1m plumb tolerance, door-jamb matching) —
  correctly treated as same-channel restatement, not independent
  corroboration, per this project's own same-channel-≠-independent-
  source rule. Lowest yield of the round (5) as a direct consequence.

## Progress Log

- 2026-08-24 — **Round 2 complete.** All 8 videos fetched serialized one
  at a time with real spacing (interleaved with each video's own full
  extraction/routing/logging work), zero rate-limit issues across the
  entire round. All 8 fully extracted. Yield 76 new facts / 8 videos =
  9.5 facts/video, above Round 1's 8.6 baseline and well above the 1.0
  floor — no stop-and-ask trigger. Region checked explicitly per video:
  6 of 8 stayed at level 2, 1 (video 4) had a service-area-only Moscow
  mention correctly not promoted to level 1, 1 (video 6, a personal-
  project video) didn't clear level 2 at all. Language checked explicitly
  for both English-titled videos (3, 4) — both confirmed Russian spoken
  audio. Cross-checks performed as instructed: video 4 vs. Round 1's
  полуручка screed method (no overlap, complementary), videos 1-2 vs.
  existing Kruglov/Sidorik electrical/plumbing content (substantial
  overlap correctly excluded from re-extraction), video 3 vs. this same
  channel's own Round 1 plastering video (same-channel restatement,
  correctly not double-counted as corroboration — lowest yield of the
  round as a result). The two "Как убить X" format spot-check videos (7,
  8) delivered the round's 2nd- and among-highest yields (11, 12) and
  were found structurally identical to the positively-titled series —
  explicit finding: this format is not a negative-value signal for this
  channel, recommend including it in future rounds. Content routed to
  `12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md`,
  `Rough_Electrical_Sequencing.md`, `Heating_Placement_Rules.md`,
  `Water_Inlet_Node_Components.md`, `Radiators_and_Convectors.md`,
  `Rough_Plumbing_Sequencing.md`, `Hygienic_Shower_and_Towel_Warmer.md`,
  `Shower_Podium_and_Drains.md`, `Waterproofing_and_Plastering.md`;
  `13_Surfaces_and_Finishes/Flooring_Guide.md` and `Walls_and_Paint.md`;
  `07_Bathroom/analysis/Tile_Selection_and_Layout.md`; and the general
  store's `Rules_Heuristics.md` (second Demolition-topic-area source,
  `Pending_Wiki_Page_Decisions.md` updated, still below the 3+-source
  page-creation threshold). `tools/verify_batch.py` run against the
  pre-round commit; all 8 new CSV rows independently re-verified via
  Python's `csv` module to parse into the correct 15 columns each with
  `archived` status.

## Round 3 — Wall/paint prep, demolition mistakes, tile/balcony/heated-floor comparisons (8 videos, dispatched 2026-08-24)

Continues full-scale processing. Named-technique tutorials plus this
channel's 2026-dated "СРАВНЕНИЕ!" (comparison) format, testing whether
that format performs similarly to the already-confirmed "Как выглядит
качественная X" and "Как убить X" series formats.

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `d8WzpxSSX8k` | Идеальные стены под покраску | Wall-prep-for-paint technique | **FULL extraction** | 9 | Painter-interview format (subcontractor Mikhail, first of its kind on this channel). Wall-prep-for-paint staged sequence, Пуфас/Унифлот filler comparison, raking-light bump check, 2-3wk prep/1-2day paint timeline, 24hr per-stage cure rule, edge/corner defect QC, cross-trade reveal-damage risk. Region level 2. Low promotional ratio. |
| 2 | `lTeNBUR1u8g` | Идеальные стены в 90 градусов? В чем секрет? Как проверить? | Wall-squareness technique/QC | **FULL extraction** | 7 | Real ~96m² object. German reveal-guide-profile technique, first-course 10mm-adhesive-cap mechanism (independently corroborates existing Zemskov first-course rule), whole-apartment pre-wall squaring principle (independent 2nd-company corroboration), client/inspector QC-verification marks, 2-week/96m² crew-speed data point, ASR-uncertain 50dB noise-limit citation. Cross-checked against Round 1 masonry acceptance (`caDB-roRasI`) and existing plastering QC content — genuinely new detail, not duplicate. Region level 2. Medium promotional ratio. |
| 3 | `AcNu6CHE7Y4` | Как начать ремонт? ТОП 4 ошибки демонтажа. | Demolition mistakes | **FULL extraction — triggered new wiki page** | 7 | Top-4-mistakes format. Dust protection, waste-volume/skip-cost planning, dishonest-contractor underquoting practice, hidden-utility damage risk, towel-rail flood-risk 3-4/10 incidence, load-bearing-wall demolition + Мосжилинспекция approval mechanism. **Rare level-1 Moscow regulatory-body naming** in this video's own spoken content (kept out of `16_Legal_and_Regulations/` per the Russia-vs-Belarus routing rule). This was the 3rd Demolition-topic source in the intermediate store — triggered creation of `11_Budget_and_Planning/analysis/Demolition.md` this session, linked from `Budgeting_Guide.md`. Medium promotional ratio. |
| 4 | `ah3StuP2TZE` | Самая сложная плитка! Крупный формат или мозаика? Что выбрать? | Tile-format comparison technique | **FULL extraction** | 9 | Real object ЖК "Фестиваль Парк," 70m², on-site tiler interview. Custom sloped shower-pan tile fitting, client-driven 45° mitred corner, box pre-sized for whole-tile miter landing, deliberate 1.5mm-vs-2mm grout-joint layout-correction, access-hatch reorder+box-widening, triangular-tile seam complexity, cost-driver mid-project smeta revision, 1-day-per-wall+1-day-grout-cleanup data point. Also yielded ceiling content (cornice/stretch-ceiling incompatibility mechanism, named TZI soundproofing product) routed to `Ceilings_Guide.md`. Region level 2 (named development, no city spoken). Medium promotional ratio. |
| 5 | `Qt4uGvGRYT0` | Как правильно утеплить балкон / лоджию | Balcony/loggia insulation technique | **FULL extraction — 2nd level-1 region source** | 11 | **Region level 1 direct** — Moscow named directly in spoken content. Heat-conservation-not-generation principle, hydronic-radiator-illegal-on-balcony corroboration, glazing prerequisite, пеноплекс/mineral-wool/пенофол comparison, thickness rules, heated-floor-over-insulation stack w/ mandatory aquapanel layer, real quartz-vinyl-on-heated-floor failure case, ceramic/porcelain-tile recommendation, plastic-not-metal anchor rule, 30-50cm merge-zone extension rule, real cost benchmark 38,000 RUB/3.6m² ≈ $460 (~$130/m²). Not applicable to this project's own unheated-balcony plan but retained as reference. Low promotional ratio. |
| 6 | `xt_q5SkINT8` | Как выбрать тёплый пол? СРАВНЕНИЕ! | Heated-floor comparison ("СРАВНЕНИЕ!" format spot-check 1/3) | **FULL extraction** | 8 | Heavy structural overlap with existing `Heating_Type_Selection.md` 10-parameter table, not re-extracted. **Cross-source disagreement flagged**: this source's 25yr electric-cable lifespan vs. existing Kruglov 15yr figure — added as a Perspectives block. New-build dedicated-riser water-floor legality exception, 5x running-cost/3yr-payback economics, bitumen-insulated-contact mechanism, furniture-plan-first sequencing rule, 30% thermostat-savings figure, room-by-room combo strategy, general wood-covering thermal-conductivity mechanism. Flagged same-account restatement of the `Qt4uGvGRYT0` quartz-vinyl failure case, not double-counted. Region level 2. Low promotional ratio. |
| 7 | `96mlkQoczI4` | Какой ПОЛ выбрать в 2026? СРАВНЕНИЕ! | Flooring comparison 2026 ("СРАВНЕНИЕ!" format spot-check 2/3) | **FULL extraction** | 10 | **First general 5-material (laminate/quartz-vinyl/linoleum/tile/solid-wood) pros-cons comparison** on `Flooring_Guide.md` — genuinely new structural content, not overlap. Real named cost-driver mechanism (uncoordinated screed level vs. finish-buildup, 150-300k RUB/≈$1,900-3,700 cost trap; self-leveling compound from 1,000 RUB/≈$10 per bag), company expert's personal solid-oak-floor preference w/ 3 named reasons. Region level 2. Low promotional ratio. |
| 8 | `lvixGbwo0Ug` | Какой ПОТОЛОК выбрать в 2026? СРАВНЕНИЕ! | Ceiling comparison 2026 ("СРАВНЕНИЕ!" format spot-check 3/3) | **FULL extraction — 3rd level-1 region source** | 10 | **Region level 1 direct** — "мы живём в Москве... в Московской области" spoken directly. Painted-ceiling misconception correction w/ chase-prohibition + single-fixture-only mechanism, ceiling-specific raking-light QC + 3m flatness standard, panel-seam paint-prep sequence, drywall-ceiling 2+2wk timeline + catastrophic-flood-outcome flag, expert drywall-vs-stretch ranking, stretch-ceiling flood-recoverability detail (extends existing RemProektMD finding), two named stretch techniques, new practically-free loft-exposed-slab ceiling option. Low promotional ratio. |

**Status: COMPLETE — all 8 videos fully extracted, zero rate-limit issues.**

**Round 3 yield**: 8 videos, 71 genuinely-new facts (9+7+7+9+11+8+10+10, excluding duplicate/corroborating-only outcomes), yield = 8.9 new facts/video — **93% of Round 2's 9.5 baseline** (well within the >50%-drop stop-and-ask threshold, and well above the 1.0/video floor). No stop-and-ask trigger.

### "СРАВНЕНИЕ!" format spot-check — explicit finding

All three spot-checked "СРАВНЕНИЕ!" videos (6, 7, 8) turned out **dense
and substantive, not thin filler** — yields of 8, 10, and 10
respectively, all at or above this round's own average (8.9). Two of
the three (videos 7 and 8) added genuinely new structural content this
project's existing wiki pages didn't have yet (a first general
five-material flooring comparison; a first general three-way ceiling-
type comparison plus a "practically free" loft-ceiling option) rather
than merely restating existing per-material/per-type content — the
"СРАВНЕНИЕ!" format's structured side-by-side framing turned out to be
a genuine synthesis exercise, not just a repackaging of already-known
facts. The one video with heavier overlap (video 6, heated-floor
comparison) still surfaced a real cross-source disagreement (electric-
cable-floor lifespan: 25 years per this source vs. 15 years per the
existing Kruglov/Ontario figure) worth recording as an open Perspectives
item, plus several genuinely new economics/mechanism facts once the
overlapping structural framework was set aside. **Explicit finding: the
"СРАВНЕНИЕ!" format performs comparably to this channel's other
already-confirmed formats** ("Как выглядит качественная X," "Как убить
X") — **recommend including it in future rounds on equal footing**,
consistent with this project's standing value-filter warning that title
format/framing alone is not a reliable predictor of substance.

### Region-check finding, per this round's explicit brief

Region evidence again varied video to video, not a fixed channel
answer — consistent with every prior round. 6 of 8 videos stayed at
level 2 (channel-only Moscow association, no city/street/regulatory
body named). **2 of 8 cleared level 1 directly** (videos 5 and 8, both
via Moscow named outright in spoken content) — this channel's 2nd and
3rd level-1 sources after Round 1's "Нахимовский проспект." **1 of 8
(video 3) cleared level 1 via an unusual signature**: a Moscow-specific
regulatory body (Мосжилинспекция) named directly rather than a city or
street — treated as level-1 evidence for that source specifically, but
its content stayed in the general budgeting store rather than being
mirrored into `16_Legal_and_Regulations/`, which is strictly
Belarus-scoped per this project's own stricter-bar convention for that
folder (a Russian regulatory body/process is a different country's law,
not just weaker evidence).

### Cross-check findings, per this round's explicit brief

- **Video 2 (wall squareness) vs. Round 1's masonry acceptance
  (`caDB-roRasI`) and existing plastering-QC content**: no duplication
  found — video 2 contributed a distinct German reveal-guide-profile
  technique, a new numeric mechanism (10mm adhesive-thickness cap) for
  an already-corroborated first-course rule, and a whole-apartment
  pre-wall squaring principle independently corroborated from a second,
  unrelated company.
- **Video 6 (heated floor) vs. existing Kruglov/Ontario heated-floor
  content in `12_Engineering_and_Systems/analysis/`**: heavy structural
  overlap correctly not re-extracted, but a genuine numeric
  disagreement was found (electric-cable floor lifespan) and recorded
  as an explicit Perspectives block rather than silently adopting
  either figure.
- **Videos 7-8 (flooring/ceiling 2026 comparisons) vs.
  `Flooring_Guide.md`/`Ceilings_Guide.md`**: both pages lacked a
  general material/type-vs-type comparison before this round — both
  videos added genuinely new structural content rather than
  overlapping with the existing technique-heavy entries on those pages.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All
8 videos fetched serialized one at a time with real spacing (achieved
by interleaving each video's own full extraction/routing/logging work
between fetches — never an idle wait), consistent with Rounds 1-2's own
clean results.

### Language check

All 8 videos confirmed Russian spoken audio (`youtube-transcript-api`
returned `language: ru` for every fetch); no English-titled video was
encountered this round.

## Progress Log

- 2026-08-24 — **Round 3 complete.** All 8 videos fetched serialized one
  at a time with real spacing (interleaved with each video's own full
  extraction/routing/CSV/archiving work), zero rate-limit issues across
  the entire round. All 8 fully extracted. Yield 71 new facts / 8
  videos = 8.9 facts/video — 93% of Round 2's 9.5 baseline, well above
  the 1.0 floor and not a >50% drop — no stop-and-ask trigger. Region
  checked explicitly per video: 6 of 8 stayed at level 2, 2 (videos 5,
  8) cleared level 1 directly via Moscow named outright in spoken
  content, and 1 (video 3) cleared level 1 via an unusual signature — a
  Moscow-specific regulatory body (Мосжилинспекция) named directly —
  kept out of `16_Legal_and_Regulations/` per this project's
  Russia-vs-Belarus stricter-bar convention for that folder. The
  channel's own 3rd Demolition-topic source (video 3) crossed this
  project's 3+-source page-creation threshold — created
  `11_Budget_and_Planning/analysis/Demolition.md` this session, linked
  from `Budgeting_Guide.md` §4, and marked the corresponding Pending
  Wiki-Page Decisions entry resolved. The three "СРАВНЕНИЕ!" format
  spot-check videos (6, 7, 8) were found dense and substantive
  throughout — explicit finding: this format performs comparably to
  the channel's other already-confirmed formats, recommend including it
  on equal footing in future rounds (see the dedicated finding section
  above). One genuine cross-source disagreement was found and recorded
  explicitly rather than silently resolved: electric-cable
  underfloor-heating lifespan (this round's video 6 states ~25 years,
  vs. the existing Kruglov/Ontario figure of ~15 years) — added as a
  Perspectives block to `Heating_Type_Selection.md`. Content routed to
  `13_Surfaces_and_Finishes/Walls_and_Paint.md` (wall-prep-for-paint
  sequence, reveal-guide-profile technique, first-course mechanism,
  whole-apartment squaring), `Flooring_Guide.md` (first general
  5-material comparison, screed-buildup cost-trap mechanism),
  `Ceilings_Guide.md` (cornice/stretch-ceiling incompatibility, TZI
  soundproofing product, full painted/drywall/stretch comparison, loft
  option); `07_Bathroom/analysis/Tile_Selection_and_Layout.md` (complex
  small-format tile technique/economics); `10_Balcony/Balcony_Index.md`
  (insulation material/technique/cost reference, not applicable to this
  project's own unheated plan); `12_Engineering_and_Systems/analysis/Heating_Type_Selection.md`
  (legality nuance, payback economics, Perspectives disagreement block);
  and the new `11_Budget_and_Planning/analysis/Demolition.md` page.
  `tools/verify_batch.py` run against the pre-round commit (`c52f96f`) —
  passed clean after one ID-cross-reference fix in
  `Pending_Wiki_Page_Decisions.md`. All 8 new CSV rows independently
  re-verified via Python's `csv` module to parse into the correct 15
  columns each with `archived` status.

## Round 4 — Case studies, comparisons, demolition, cost/budget tips (8 videos, dispatched 2026-08-24)

Continues full-scale processing. Picked up while RemProektMD is paused on
a single-video rate-limit (per the queue's channel-switching protocol —
switch to the other active channel rather than idle-wait or retry
immediately). Mix of real case studies (tests the client-review/case-study
format not yet spot-checked on this channel), technique comparisons, a
second demolition-mistakes video (tests fit against the new `Demolition.md`
page from Round 3), and cost-saving tips.

| # | Video ID | Title | Why selected | Status |
|---|---|---|---|---|
| 1 | `qFM8NIDIRro` | Finished renovating an old apartment. Police visits, wall cracks, and other challenges! | Real case study, tests client-review-format value not yet spot-checked on this channel | pending |
| 2 | `IoQiGtso9Vk` | Complex renovations in a historic Arbat apartment. Results, tips, and challenges. | Real case study, historic building | pending |
| 3 | `rt9R26k6dEM` | КАК ВЫБРАТЬ ПЛИТКУ? ПЛИТКА ИЛИ КЕРАМОГРАНИТ? | Tile-vs-porcelain comparison technique | pending |
| 4 | `66pn-nIOJkg` | КРАСКА, ОБОИ, ИЛИ ОБОИ ПОД ПОКРАСКУ? ЧТО ЛУЧШЕ И ЧТО ВЫБРАТЬ? | Paint-vs-wallpaper comparison technique | pending |
| 5 | `3sRfRiQ8XfE` | Крутые инженерные коммуникации! Сколько это стоит? | Engineering/utilities cost benchmark | pending |
| 6 | `PBkZQHkjciE` | Как СЭКОНОМИТЬ на РЕМОНТЕ?! Конкретные СОВЕТЫ и ХИТРОСТИ | Budget-saving tips | pending |
| 7 | `Z1IuJFudcPY` | TOP 10 CRITICAL DEMOLITION MISTAKES! | Second demolition-mistakes source, tests fit against new `Demolition.md` page | pending |
| 8 | `F0ZHsu4k6JY` | ПРАВИЛА для маленькой квартиры. В ней есть ВСЕ | Small-apartment design/planning rules | pending |

Status: **pending dispatch**.
