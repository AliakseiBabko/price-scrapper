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

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `qFM8NIDIRro` | Finished renovating an old apartment. Police visits, wall cracks, and other challenges! | Real case study, tests client-review-format value not yet spot-checked on this channel | **FULL extraction** | 12 | English title, confirmed Russian audio. Foreman-interview case-study format (not a client testimonial) — genuinely dense: real police-during-quiet-hours incident, structural-sway stop condition, no-container site logistics, wall-retention engineering sequence, screed-height compensation, low-ceiling wiring rule, riser rework by "жилищник" + drain-noise soundproofing kit, bathroom niche sightline design, magnetic tile access panel, two-tone tile scheme, balcony scope note. **No total cost/area stated — this case study carries no pricing data.** **Region: level 1** — "Олимпийский проспект" (a real Moscow street) named directly. Low promotional ratio. |
| 2 | `IoQiGtso9Vk` | Complex renovations in a historic Arbat apartment. Results, tips, and challenges. | Real case study, historic building | **FULL extraction** | 8 | Second foreman-interview case study, historic pre-revolutionary building near Arbat. 14-container demolition waste volume, adjustable floor system chosen over screed by room load capacity, drywall ceiling over stretch due to structural beams, masonry inspection-hatch dimensions, historic cast-iron radiator preservation, client networking-equipment niche, wardrobe-behind-headboard layout, dark-tone paint coat-count + molding spray technique + skilled-painter differentiator. **No total cost/area stated.** **Region: level 1** — "центр Москвы исторически" named directly. Low promotional ratio. |
| 3 | `rt9R26k6dEM` | КАК ВЫБРАТЬ ПЛИТКУ? ПЛИТКА ИЛИ КЕРАМОГРАНИТ? | Tile-vs-porcelain comparison technique | **FULL extraction** | 13 | Studio explainer, dense general/brand-agnostic tile-quality primer: ceramic-vs-porcelain material/durability difference, domestic-vs-imported market claim, format-size reference ladder, textured-tile fixture-fit risk, quality-factor taxonomy, surface-type placement rule, coloring-method durability rule, two buying-scam cautions. A closing case-study cost figure was shown on-screen but never spoken — not extractable from ASR. Region level 2 (channel branding only). Low promotional ratio. |
| 4 | `66pn-nIOJkg` | КРАСКА, ОБОИ, ИЛИ ОБОИ ПОД ПОКРАСКУ? ЧТО ЛУЧШЕ И ЧТО ВЫБРАТЬ? | Paint-vs-wallpaper comparison technique | **FULL extraction — densest technique video this round** | 16 | Studio explainer, full three-way pros/cons comparison (paint vs. wallpaper vs. paintable wallpaper) — durability figures, cost-driver mechanisms, a building-settlement resilience mechanism, a named hybrid material with a repaint-cycle figure (ASR-uncertain exact number). Region level 2. Low promotional ratio. |
| 5 | `3sRfRiQ8XfE` | Крутые инженерные коммуникации! Сколько это стоит? | Engineering/utilities cost benchmark | **FULL extraction — 3rd Petrishin-Stroi cost-benchmark case** | 10 | Real per-stage turnkey RUB figures converted via trailing-6-month rate: demolition ≈$4,800, walls ≈$1,800, plastering ≈$3,600, plumbing ≈$3,900, electrical ≈$4,800; arithmetic-summed total ≈$18,800 (self-computed, not source-stated). No floor area so no $/m². Also: three-way partition-material cost-tier ranking, mechanized-vs-hand-pulled plaster tradeoff. Region level 2. Medium promotional ratio. |
| 6 | `PBkZQHkjciE` | Как СЭКОНОМИТЬ на РЕМОНТЕ?! Конкретные СОВЕТЫ и ХИТРОСТИ | Budget-saving tips | **FULL extraction — highest yield this round** | 18 | Extremely dense itemized Moscow-market labor-rate ladder across 8 work categories (design tiers, labor tiers, wall materials, plastering, electrical, plumbing, tile, baseboards/doors, ceilings, flooring), all converted to USD, plus a named screed-level-planning lifehack and a self-disclosed quality caution against the company's own cost-ranked material. **Region: level 1** — "в Москве" named directly for the electrical base rate. Low promotional ratio. |
| 7 | `Z1IuJFudcPY` | TOP 10 CRITICAL DEMOLITION MISTAKES! | Second demolition-mistakes source, tests fit against new `Demolition.md` page | **FULL extraction, explicitly cross-checked against `Demolition.md`** | 10 | English title, confirmed Russian audio. Several items are same-channel restatements of `AcNu6CHE7Y4`'s existing content (scope document, dust protection, construction sink, neighbor notification) — correctly not double-counted. New: teach-back verification method, delicate-tape detail, glass-pitting mechanism, white-vs-green debris bags, temp-wiring hiring red flag, downstairs photo-documentation fraud defense, rush-hour debris timing, container-approval new-build-vs-secondary-market distinction, a distinct towel-warmer accident-share statistic, and a standout real 5-6-apartment flooding incident. **Region: level 1** — "Марино" and "шоссе Энтузиастов" (real Moscow locations) named directly in a personal story. Low promotional ratio. |
| 8 | `F0ZHsu4k6JY` | ПРАВИЛА для маленькой квартиры. В ней есть ВСЕ | Small-apartment design/planning rules | **PARTIAL extraction — low-value pass** | 2 | Despite the "Rules"-framed title, this is almost entirely a client-satisfaction testimonial interview with no concrete technical/numeric substance (why the client picked this company, praise for named staff). Per the value-filter rule, only genuinely reusable content was extracted: a bathtub-vs-shower usage-frequency decision heuristic (35m² apartment) and a minor design-to-smeta turnaround note. Region level 2. **Promotional ratio: high.** |

**Status: COMPLETE — all 8 videos fully fetched and processed (7 full extractions, 1 partial low-value pass), zero rate-limit issues.**

**Round 4 yield**: 8 videos, 89 genuinely-new facts (12+8+13+16+10+18+10+2, excluding duplicate/corroborating-only outcomes), yield = 11.1 new facts/video — **125% of Round 3's 8.9 baseline**, the highest per-video yield of any round on this channel so far, well above the 1.0/video floor. No stop-and-ask trigger.

### Case-study/client-review format finding — explicit, per this round's brief

**This round's central format finding: "case study/client interview" is not one format on this channel — it splits sharply into two sub-formats with very different value.**

- **Foreman/practitioner interview case studies** (videos 1-2, `qFM8NIDIRro` and `IoQiGtso9Vk`): dense, low-promotional, genuinely technical — a site foreman walks through real decisions (structural judgment calls, material choices, design compromises) with concrete, checkable detail. Both cleared **level-1 region** directly. **Neither carried a total project cost or floor-area figure**, however — despite being real "case studies," this sub-format did not deliver the price-comparability data (location + year + cost) this project's standing rule specifically wants; it delivered technique/decision substance instead. Fact yields (12, 8) were solid, in line with this round's other strong performers.
- **Client-satisfaction testimonial interviews** (video 8, `F0ZHsu4k6JY`): despite a "Rules for a small apartment" title suggesting technique content, this was almost entirely consumer sentiment about *why the client chose this company* and *how happy they are* — the value-filter's explicit "pure consumer sentiment, no concrete technical/numeric substance" exclusion criterion applied almost in full. Fact yield collapsed to 2 (well below this round's 11.1 average, though this is an individual-video outcome, not a round-level trigger).

**Recommendation for future rounds**: when this channel offers a case-study/interview-format video, check **who is being interviewed** before assuming substance — a foreman/practitioner interview (even a real-object walkthrough) reliably yields dense technique content but often skips pricing; a client-satisfaction interview reliably yields little beyond sentiment regardless of title framing. Both are worth a quick title+opening-line check before committing to full extraction, consistent with this project's standing value-filter guidance that title framing alone isn't a reliable predictor.

### Region-check finding, per this round's explicit brief

Region evidence was unusually strong this round — **4 of 8 videos cleared level 1 directly** (videos 1, 2, 6, 7 — two case-study interviews via named Moscow streets/districts, the budget-tips video via "в Москве" for the electrical rate, and the second demolition-mistakes video via "Марино"/"шоссе Энтузиастов" in a personal story), a notably higher level-1 rate than prior rounds on this channel (Round 1: 1/5, Round 2: 0/8, Round 3: 3/8). The remaining 4 videos (3, 4, 5, 8) stayed at level 2 (channel branding only, no city spoken). Consistent with every prior round's finding: this channel's region evidence varies video to video, not by a fixed channel-wide answer — worth re-checking every round.

### Demolition.md cross-check finding, per this round's explicit brief

Video 7 (`Z1IuJFudcPY`) was explicitly cross-checked against the `11_Budget_and_Planning/analysis/Demolition.md` page created in Round 3. Several items were confirmed same-channel restatements of existing content (written scope-of-work, dust protection, construction sink, neighbor notification) and correctly not double-counted. The remaining content was genuinely new — extending several existing sections (container-negotiation, towel-warmer risk) with new detail and adding several wholly new mechanisms (glass-pitting from grinder sparks, debris-bag material choice, downstairs-neighbor photo-documentation, a hiring red flag) plus a standout real flooding incident. This is a clean example of corroboration-with-extension, not pure duplication — the page grew substantially from this second source without inflating the fact count with restated content.

### Language check

Both English-titled videos this round (1: `qFM8NIDIRro`, 7: `Z1IuJFudcPY`) were individually verified via `youtube-transcript-api` fetch metadata to have Russian spoken audio (`language: ru`) — fetched and cited in Russian throughout, per this project's standing rule. Video 2 (`IoQiGtso9Vk`) also carries an English on-screen title and was likewise confirmed Russian-spoken. All other videos had Russian titles and Russian audio.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 8 videos fetched serialized one at a time with real spacing (achieved by interleaving each video's own full extraction/routing/CSV/archiving work between fetches, never an idle wait), consistent with Rounds 1-3's own clean results. This channel continues to show no distinct access risk beyond the general serialized-fetch discipline. RemProektMD's single-video rate-limit earlier in the session (the reason this round was dispatched on this channel instead) was not repeated here.

## Progress Log

- 2026-08-24 — **Round 4 complete.** All 8 videos fetched serialized one
  at a time with real spacing (interleaved with each video's own full
  extraction/routing/CSV/archiving work), zero rate-limit issues across
  the entire round. 7 full extractions + 1 partial low-value pass. Yield
  89 new facts / 8 videos = 11.1 facts/video — 125% of Round 3's 8.9
  baseline, the highest per-video yield of any round on this channel to
  date, well above the 1.0 floor — no stop-and-ask trigger. Region
  checked explicitly per video: 4 of 8 cleared level 1 directly (a
  notably higher rate than prior rounds), 4 stayed at level 2. **Central
  finding this round**: case-study/client-review format splits sharply
  into foreman-interview case studies (dense, technical, no pricing) vs.
  client-satisfaction testimonials (thin, sentiment-only) — see the
  dedicated finding section above. Video 7 was explicitly cross-checked
  against Round 3's `Demolition.md` page — corroboration-with-extension
  confirmed, several genuinely new mechanisms added without inflating
  the fact count with restated content. Content routed to
  `11_Budget_and_Planning/analysis/Demolition.md` (2 new sections),
  `07_Bathroom/analysis/Tile_Selection_and_Layout.md`,
  `07_Bathroom/analysis/Structure_and_Framing.md`,
  `07_Bathroom/analysis/Planning_and_Layout.md`,
  `12_Engineering_and_Systems/analysis/Rough_Electrical_Sequencing.md`,
  `12_Engineering_and_Systems/analysis/Rough_Plumbing_Sequencing.md`,
  `13_Surfaces_and_Finishes/Flooring_Guide.md`,
  `13_Surfaces_and_Finishes/Ceilings_Guide.md`,
  `13_Surfaces_and_Finishes/Walls_and_Paint.md`,
  `10_Balcony/Balcony_Index.md`, and `11_Budget_and_Planning/Budgeting_Guide.md`
  (a 3rd Petrishin-Stroi cost-benchmark case in §4, plus a dense
  itemized labor-rate ladder in §5 Cost-Saving Strategies). All price
  figures normalized to USD via `tools/pricing/currency_converter.py`'s
  trailing-6-month average anchored to each video's own confirmed
  publish date. `tools/verify_batch.py` run against the round's changes;
  all 8 new CSV rows independently re-verified via Python's `csv` module
  to parse into the correct 15 columns each with `archived` status.
  `batch_status_20260824_petrishin_round4.json` maintained throughout,
  marked `complete`.

## Round 5 — Designer mistakes, cost benchmark, cosmetic-renovation technique (8 videos, dispatched 2026-08-24)

Continues full-scale processing. Mix of a fresh 2026-dated cost benchmark
(extends the year-over-year benchmark series started in Round 1), a cluster
of "designer mistakes"/"plastering mistakes" videos to test whether this
channel's other recurring mistake-format clusters perform as well as the
already-confirmed "Как убить X" and "СРАВНЕНИЕ!" formats, and a dedicated
cosmetic-renovation ("косметический ремонт") technique video.

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `w6_e7nySEXI` | Что скрывают дизайнеры? Самые частые ОШИБКИ В РЕМОНТЕ | СРЫВЫ СРОКОВ, задержки | Designer-mistakes/project-delay format | **FULL extraction** | 10 | Real ~100m² Moscow apartment, foreman/owner walkthrough. **Region: level 1** — apartment described directly as "one of the most complex apartments in Moscow." No cost/area figure. Dense designer/foreman-coordination checklist: site-cleanliness red flag, milled-vs-classic drywall corners, dimensioned-drawing requirement, practicality-over-aesthetics designer-vetting question, glass-block texture open question, material-delivery-vs-spec deviation defect, LED transformer ventilated-storage rule, uncoordinated HVAC sub-trade defect, sub-trade coordination rule, mezzanine-over-HVAC-hatch defect. Low promotional ratio. |
| 2 | `LEsmpI8bWCY` | Сколько РЕАЛЬНО стоит ДИЗАЙНЕРСКИЙ ремонт в 2026 году?! | Fresh 2026 cost benchmark, extends year-over-year series | **FULL extraction, ⚠️ title/date discrepancy** | 8 | Despite the "2026" title, spoken content says "2025" twice and yt-dlp confirms upload date 2025-11-23 — **not** a fresh year-over-year data point; a market segment-tier structure instead (economy <30,000 RUB/m² ≈$370/m²; comfort 30,000-70,000 ≈$370-870/m²; premium 70,000+ ≈$870/m²+). Three named contractor-fraud schemes (lowball-bait-abandon, recalculation-clause area inflation, desperate-crew lowball-extort). Region level 2. Low promotional ratio. |
| 3 | `8B2xnSNEqqs` | НИКОГДА ТАК НЕ ДЕЛАЙ! Глупые ошибки дизайн-проектов. | Design-project mistakes format | **FULL extraction, ⚠️ format spot-check finding** | 11 | Design lead "Клара" comment-response Q&A defending real criticized design choices — **not a mistakes list despite the title**, a distinct sub-format from this channel's other confirmed formats. Concealed-door baseboard rationale, baseboard material/miter comparison, mural age-targeting, windowsill-seat practicality, open-shelving critique, bedroom lighting-by-routine method, night-lighting reversibility ranking, plywood-cost claim disputed (unverified), routine-walkthrough outlet-placement technique, jacuzzi tradeoff. Region level 2. Low promotional ratio. |
| 4 | `mb-2ll0UtTo` | Главные ОШИБКИ штукатурки. НЕ ДЕЛАЙ ТАК! | Plastering-mistakes format, tests against existing dense plastering content | **FULL extraction, explicitly cross-checked** | 5 | Cross-checked against `D1REgSDwILU` (Round 1) and `r1eyXzXNdI0` (Round 2) — several items same-channel restatement (priming, beacon rust-bleed, straightedge check, mesh mid-depth placement) correctly not double-counted. New: +5°C minimum plastering temperature, vapor-barrier-to-wall junction taping technique (first roofing-adjacent content), ventilation protocol, localized-heater forced-drying mold case, real wall-geometry defect example. Region level 2. Low promotional ratio. |
| 5 | `s27qG_Eg3SY` | ТОП ОШИБОК косметического ремонта! НЕ ДЕЛАЙ ТАК! | Cosmetic-renovation mistakes | **FULL extraction, densest video this round** | 15 | Real on-site cosmetic-renovation walkthrough with real hidden-defect discoveries (developer film behind curtains costing 4-5 unplanned hours, baseboard-footprint mismatch, door-frame foam-gap defect, ceiling cornice crack, UV-degraded window hardware) plus a general secondary-housing ("вторичка") risk checklist (door-frame demolition plaster-crack risk, tile tap-test practice, mixed aluminum-copper wiring risk + cosmetic-vs-capital renovation principle, corroded mixer wall-connection failure mode, whitewash-vs-paint ceiling distinction, furniture-packing smeta line item) plus an open design-trend debate (white vs. wall-color window reveals, "8 years in Moscow"). Region level 2. Low promotional ratio. |
| 6 | `vKMHNYQYWAI` | Топ 13 САМЫХ дорогих ОШИБОК ремонта квартиры. | Costly-mistakes format | **FULL extraction, heavy overlap correctly excluded** | 8 | Owner's own 13-mistakes checklist; heavy overlap with Round 2 QC content (raking-light, temp-outlet test, tile tap-test/SVP) correctly not double-counted. New/extended: semi-dry screed conversion story + ingredient checklist, "жираф" pre-filler grinding, stekloholst settlement-crack mechanism (cross-channel corroboration+extension), tub-tile 2mm silicone joint mechanism, acrylic-tub load-testing requirement, shower-pan masonry material spec (company's largest warranty-cost driver), electrical panel full-termination + breaker-label-at-payment rule, drywall screw-depth/paper-tape QC. Region level 2. Low promotional ratio. |
| 7 | `izhaUHRKViw` | Как сделать КАЧЕСТВЕННЫЙ косметический ремонт? Ловушки, технологии, результат | Cosmetic-renovation technique | **FULL extraction** | 9 | Real cosmetic-renovation walkthrough; corroborates and extends video 5's cosmetic-only-if-capital-done principle with an active company policy framing. New: furniture/floor wrap-protection + wood-floor dust-absorption mechanism, ceiling-fixture full-removal vs tape-and-bag, faceplate-removal paint technique, point-repair redefinition of "cosmetic," low-cost-high-impact baseboard/windowsill/door swap heuristic, protective wall panel for chair-scuff zone, parquet-gap sealant budget alternative (150,000-200,000 RUB ≈$1,900-$2,500 min for full refinish), child-safety lockable window handles, mandatory post-renovation cleaning. Region level 2. Low promotional ratio. |
| 8 | `8QBqwydVND8` | Все этапы ремонта квартиры в 2026, пошагово. | All-stages 2026 walkthrough | **FULL extraction, low yield — heavy restatement** | 4 | General rough-renovation sequence explainer, substantially restating already-captured content (design-project-first, plastering priming/mesh/ventilation, electrical temp-outlet safety, plumbing pressure test, screed-differential-height lifehack — now a 3rd+ restatement on this channel). New: two-tier company warranty terms (5yr engineering / 2yr general construction), electrical-plumbing stage-order flexibility, proactive wall-geometry pre-check at wall-building stage (distinct from video 4's reactive discovery), shumonet impact-noise underlayment description. Region level 2. Low promotional ratio. |

**Status: COMPLETE — all 8 videos fully fetched and extracted, zero rate-limit issues.**

**Round 5 yield**: 8 videos, 70 genuinely-new facts (10+8+11+5+15+8+9+4, excluding duplicate/corroborating-only outcomes), yield = 8.75 new facts/video — **79% of Round 4's 11.1 baseline** (within the >50%-drop stop-and-ask threshold, and well above the 1.0/video floor). No stop-and-ask trigger, though video 8's own yield (4) and video 4's own yield (5) were both individually the lowest of any video processed on this channel to date, driven by heavy same-channel restatement — flagged explicitly below, not a round-level concern yet.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 8 videos fetched serialized one at a time with real spacing (achieved by interleaving each video's own full extraction/routing/CSV/archiving work between fetches, never an idle wait), consistent with Rounds 1-4's own clean results.

### Region-check finding, per this round's explicit brief

Region evidence varied video to video again, consistent with every prior round. 7 of 8 videos stayed at level 2 (channel-only Moscow association, no city/street named); 1 of 8 (video 1) cleared level 1 directly via the object itself being described as "one of the most complex apartments in Moscow" in the video's own spoken content. No video this round used a regulatory-body or street-name signature the way Round 3's video 3 or Round 1's video 5 did.

### Language check

All 8 videos had Russian titles and confirmed Russian spoken audio (`youtube-transcript-api` returned `language: ru` for every fetch) — no English-titled video was encountered this round.

### Format spot-check findings — "designer/design-project mistakes" and "top N expensive mistakes" clusters, per this round's explicit brief

- **Video 1 (`w6_e7nySEXI`, "designer mistakes/project delays")**: turned out to be a real, dense foreman/owner walkthrough of an actual complex Moscow apartment — genuinely substantive, consistent with this channel's other "mistakes"-titled formats already confirmed positive (Rounds 2-3).
- **Video 3 (`8B2xnSNEqqs`, "НИКОГДА ТАК НЕ ДЕЛАЙ!")**: **the most interesting format finding this round** — despite the clickbait mistakes-format title, this video turned out to be a comment-response Q&A (design lead "Клара" defending real viewer criticism of past design choices), not a mistakes list at all. Still dense and substantive (fact_yield 11, above this round's own average), but a structurally distinct sub-format worth recognizing for future title-skims on this channel — a "mistakes" title can mean "defensive rationale for choices already made," not just "acceptance checklist" or "clickbait cold-open into real technique."
- **Video 6 (`vKMHNYQYWAI`, "Top 13 most expensive mistakes")**: this format spot-check came back with the round's most heavily-overlapping content — roughly half its 13 named items restated content already captured from this channel's own Round 2 QC videos. Still cleared the 1.0 floor easily (fact_yield 8) once overlap was excluded, but this is the first "top N mistakes" video on this channel to show substantial same-channel restatement rather than being mostly novel.
- **Video 8 (`8QBqwydVND8`, general all-stages 2026 walkthrough)**: **this round's lowest-yield video (4)** — a general step-by-step sequence explainer that restates a large fraction of this channel's already-established rough-renovation content (some points now restated a 3rd or 4th time across rounds). Worth flagging for future rounds: this channel's general "full sequence" or "all stages" explainer format appears to have a much lower marginal-yield ceiling than its named-technique, case-study, or comparison formats, once enough of the channel's other content has already been processed — not a reason to skip the format outright (it still contributes real new items, like this video's warranty-terms benchmark), but not to expect dense yield from it either.

### Cross-check findings, per this round's explicit brief

- **Video 2 (cost benchmark) vs. existing `Budgeting_Guide.md` benchmarks (2022, 2024, engineering-focus 2025)**: this video does **not** extend that year-over-year series despite its "2026" title — its own spoken content confirms "2025," and its content (market segment tiers) is structurally different from the single-real-object itemized totals in the existing series. Recorded explicitly as a separate market-tier benchmark, not blended with the real-object series.
- **Video 4 (plastering mistakes) vs. this channel's own Round 1 (`D1REgSDwILU`) and Round 2 (`r1eyXzXNdI0`) plastering sources**: explicit cross-check performed as instructed. Several items were same-channel restatement (priming importance, beacon rust-bleed, straightedge gap check, and — newly confirmed this round — the material-transition mesh mid-depth-placement detail, now a 3rd-time restatement) and correctly not double-counted; genuinely new content (vapor-barrier junction technique, minimum temperature, ventilation protocol, forced-drying failure case, wall-geometry defect example) still cleared a modest fact_yield of 5.
- **Video 6 vs. Round 2's QC videos, and video 8 vs. multiple prior rounds**: both showed the heaviest same-channel restatement seen on this channel to date — flagged as this channel's technique/QC content base is now large enough that a new video's marginal yield increasingly depends on whether it's a named-technique/case-study/comparison video (still yielding well, per videos 1, 3, 5, 7) versus a general "top N" or "all stages" recap video (videos 6, 8 — where restatement risk is highest).
- **Video 5 vs. Video 7**: both are real cosmetic-renovation walkthroughs from this channel; video 7 explicitly corroborates and extends video 5's own "cosmetic renovation is only genuinely cosmetic if capital renovation was already done" principle with an active company-policy framing — recorded as corroboration-with-extension, not double-counted.

## Progress Log

- 2026-08-24 — **Round 5 complete.** All 8 videos fetched serialized one
  at a time with real spacing (interleaved with each video's own full
  extraction/routing/CSV/archiving work), zero rate-limit issues across
  the entire round. All 8 fully extracted. Yield 70 new facts / 8 videos
  = 8.75 facts/video — 79% of Round 4's 11.1 baseline, well above the 1.0
  floor and not a >50% drop — no stop-and-ask trigger, though videos 4
  and 8 individually posted this channel's lowest-ever per-video yields
  (5 and 4) due to heavy same-channel restatement, flagged explicitly for
  future rounds. Region checked explicitly per video: 7 of 8 stayed at
  level 2, 1 (video 1) cleared level 1 directly via the object itself
  being called "one of the most complex apartments in Moscow." Language
  checked — all 8 confirmed Russian audio, no English titles this round.
  **Key format finding**: video 3's "mistakes"-format title actually
  concealed a comment-response Q&A sub-format (design lead defending
  past choices), distinct from this channel's other confirmed mistakes/
  QC formats — still dense (fact_yield 11). Video 2's "2026" title was
  found to be a discrepancy — spoken content and yt-dlp upload date both
  confirm 2025 — recorded as a market segment-tier benchmark, explicitly
  not blended into the existing year-over-year real-object benchmark
  series. Explicit cross-checks performed: video 4 against Rounds 1-2's
  plastering sources (heavy restatement correctly excluded, yield 5);
  video 6 against Round 2's QC videos (heaviest overlap yet on a "top N"
  video, yield 8 after exclusion); video 7 against video 5's own
  cosmetic-vs-capital-renovation principle (corroboration-with-extension,
  not double-counted). Content routed to `11_Budget_and_Planning/Budgeting_Guide.md`
  (market-tier benchmark, contractor-fraud schemes, designer-coordination
  pointer, secondary-housing risk-checklist pointer, warranty-terms
  benchmark), the general store's `Rules_Heuristics.md` (3 new topic
  areas: Designer/Foreman Coordination & QC, Secondary-Housing
  Renovation-Estimate Risk Checklist, Quality Cosmetic Renovation
  Technique), `12_Engineering_and_Systems/analysis/Waterproofing_and_Plastering.md`
  (2 new sections), `12_Engineering_and_Systems/analysis/Rough_Electrical_Sequencing.md`
  (1 new section), `13_Surfaces_and_Finishes/Flooring_Guide.md` (3 new
  sections), `13_Surfaces_and_Finishes/Walls_and_Paint.md` (1 new
  section), `13_Surfaces_and_Finishes/Ceilings_Guide.md` (2 new
  sections), `13_Surfaces_and_Finishes/analysis/Door_Anatomy_and_Mount_Types.md`,
  `Windows_Slope_Finishing.md`, and `Windows_Acceptance_Checklist.md`
  (1 new section each), `07_Bathroom/analysis/Bathtub_and_Shower.md` (1
  new section), and `17_Design_and_Ergonomics/analysis/Family_Scenario_Driven_Design.md`
  and `Decor_and_Finish_Selection_Technique.md` (1 new section each).
  All price figures normalized to USD via `tools/pricing/currency_converter.py`'s
  trailing-6-month average anchored to each video's own confirmed publish
  date. `tools/youtube/archive_transcripts.py` run (dry-run first, all 8
  matched correctly) — 3 source notes' bottom `[source: ...]` inline
  links needed a manual fix afterward since the archive script renamed
  those 3 transcripts to a different slug than the note's own filename
  (frontmatter `transcript_file:` was updated automatically by the
  script; the bottom link was not, and was corrected by hand for videos
  2, 3, and 7). All 8 new CSV rows independently re-verified via Python's
  `csv` module to parse into the correct 15 columns each with `archived`
  status — 2 rows initially broke due to an unquoted comma inside a
  Russian title field (videos 1 and 7) and were fixed the same session.
  `tools/verify_batch.py` to be run against the pre-round commit before
  finishing.

## Round 6 — Case-study review, per-stage cost benchmarks, market-tier cross-check, finishing/drywall/screed technique (8 videos, dispatched 2026-08-24)

Continues full-scale processing. Deliberately favors case-study/cost-
benchmark and named-technique videos over recap "ТОП-N ошибок" formats
(Round 5 found those recap formats to have this channel's lowest yields
so far). Includes a second 2024-dated market-tier video for an explicit
cross-check against Round 5's 2025 market-tier note, and two videos
(3, 4) explicitly checked for year/area confirmation against the
existing real-object cost-benchmark series.

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `g1b6Hxx-HUk` | DON'T DO THIS! A designer reveals the secrets of remodeling (65 m² apartment review) | Real case-study/review format | **FULL extraction** | 11 | English title, confirmed Russian audio. Design-lead interview (Anastasia/Клара — same "Клара" as Round 5's `8B2xnSNEqqs`), real ~65m² apartment, no total cost/area pricing stated. Pre-purchase-designer-consultation heuristic, drywall-vs-masonry demolition-candidate signal, legalization-aware layout decision, 2-window furniture-placement caution, corridor-sightline caution, laundry-in-hallway placement, towel-warmer placement mitigation, humid-zone facade material rule, entry-tile-matching technique, reversible kids-room decal decor, lighting-preference-conflict resolution via backlit panel, designer-vetting-via-built-photos, in-store material verification, room-by-room budget tracking, remote-supervision fallback, RU illegal-replanning framing (not routed to Legal folder). Region level 2. Low promotional ratio. First real content on the previously-empty `17_Design_and_Ergonomics/analysis/Functional_Zoning_and_Furniture_Arrangement.md` placeholder. |
| 2 | `8dyPTnmOHKs` | 6 МУЛЬТОВ ТОЛЬКО ЗА РАБОТУ?! ЦЕНЫ КАЖДОГО ЭТАПА на реальной квартире | Real per-stage labor-only cost breakdown | **FULL extraction — 4th cost-benchmark case** | 10 | Real 120m² premium turnkey object, labor-only total 6,000,000 RUB ≈$76,400 (≈$640/m²) — explicitly not blended with the existing rough-stage-only 2022/2024 series (different scope). Per-stage costs for plastering/electrical/plumbing/flooring/tile/painting; client off-spec switch substitution real-cost loss (~85,000 RUB ≈$1,100); herringbone install-time/error mechanism; exclusive-material 6-month lead-time/crew-retention caution; proactive raking-light wall-prep discipline. Warranty terms restated from Round 5 video 8, correctly not double-counted. Region level 2. Medium promotional ratio (competitor-dunk framing excluded). |
| 3 | `JLjCveR-ft0` | Ремонт квартиры за 1 300 000! Обзор ремонта | Real cost-benchmark case study, tests fit against existing series | **FULL extraction, ⚠️ attribution nuance** | 10 | **Channel explicitly states this is not its own crew's object** — features another practitioner's ("Александр") real 38m² secondary-market full rough+finish renovation. Total 1,300,000 RUB ≈$14,000 (≈$370/m²) — a **full-scope** (not rough-only) budget benchmark, kept separate from the rough-stage-only series (different scope, per this project's price-comparability rule). New: dual towel-warmer pet-towel storage, under-bed pet nook, compact-footprint exhaust fan for cabinet clearance, custom two-leaf door for tight bathroom clearance, window-portal-to-desk conversion, dual-purpose acoustic panel, concealed stretch-ceiling curtain track, balcony insulation+glazing real-world effectiveness verification, single-chamber-glazing freeze-risk warning. Region level 2 (weaker than usual, object isn't the channel's own execution). Medium promotional ratio. |
| 4 | `7LAB25SCQ1Q` | Сколько стоят этапы ремонта вторички? Ремонт на Арбате, Москва | Secondary-market per-stage cost breakdown, named Moscow district | **FULL extraction — same real object as Round 4's `IoQiGtso9Vk`** | 8 | **Region: level 1 direct** ("Новый Арбат" named). Explicit follow-up video on the **same real object** as Round 4's historic-Arbat case study — supplies the 75m²/Stalin-era-building/secondary-market scope that case was missing. Real per-stage rough-work costs: walls 76,000 RUB ≈$780; plastering 291,000 RUB ≈$3,000; drywall+soundproofing 410,000 RUB ≈$4,200; plumbing 156,000 RUB ≈$1,600; tile 500,000 RUB ≈$5,200. **Demolition and electrical costs ASR-garbled/missing — not extracted**; partial sum (≈1,433,000 RUB ≈$14,800) explicitly **not** added to the year-over-year full-total series (incomplete). Floor-system beam-material criterion refined (metal beams → screed) with an open, unresolved discrepancy flagged against Round 4's timber-beam wording. Low promotional ratio. |
| 5 | `nT0qOcN_nEQ` | Сколько стоит ремонт в Москве в 2024 году? Эконом, комфорт, премиум? | 2024 market-tier pricing, cross-check against Round 5's 2025 video | **FULL extraction, explicit cross-check performed** | 10 | Genuinely 2024-dated (confirmed spoken + `yt-dlp`). **Cross-check finding**: not a clean same-scope year-over-year comparison — 2024's Comfort figure (35,000-40,000 RUB/m²) is labor-only excluding design/furniture, while 2025's Comfort band (30,000-70,000 RUB/m²) is full turnkey including design — similar raw numbers across unequal scope actually suggest a real price increase once equalized, not stability; recorded as an open finding, not a resolved inflation %. New: rough-work floor ~20,000 RUB/m², with-furniture Comfort ~100,000+ RUB/m², premium ventilation/smart-home big-ticket items (1-3 million RUB); White-Box realism caution; partition-material savings tiers; custom-hardware lead-time caution; flip-vs-own-home budget caution; Bentley/VW/Lada client-expectation-calibration technique. Region level 2 (Moscow mention is a service-area sales CTA). Medium promotional ratio. |
| 6 | `Q0sVq_1SIQM` | Финишные работы при ремонте квартиры | Finishing-work technique | **FULL extraction** | 9 | Foreman ("Максим") interview, real object. **Region: level 1 direct** ("улица Челомея" named). Same-material countertop/backsplash rationale, push-to-open cabinet doors, deliberately non-built-in visible fridge, quartz-vinyl-with-wood-veneer vs. engineered-board substrate distinction, ceiling-drop mechanism from low-mounted risers+ventilation with a real client height-tradeoff decision, fixture-install-delay sequencing to protect from a ceiling trade, centralized LED-transformer metal-plate mounting (extends Round 5's rule), heated-wall-panel towel-warmer alternative, wired/wireless leak-sensor placement strategy. Medium promotional ratio. |
| 7 | `gCI2qF34Dss` | Все ошибки гипсокартона! Как принимать работы? | Drywall mistakes + acceptance checklist, named-technique hybrid format | **FULL extraction** | 7 | Comedic-skit cold open (collapsed-ceiling gag) settling into genuine drywall frame/board technique. 45° board-edge bevel prep, 400mm max profile cell spacing, anchor-wedge vs. nail/plastic-dowel fastening (reinforced by a real collapsed-ceiling case), Knauf crab-connector cross-joint technique, perimeter damper tape, staggered two-layer drywall pattern. Screw-depth control and plane-check QC correctly not double-counted (same-channel Round 5 restatement). Region level 2. Medium promotional ratio. |
| 8 | `c4mmaLAsDw4` | Не делайте стяжку без этого! Как спасти соседей и нервы. Самая лучшая шумоизоляция пола | Screed/floor-soundproofing technique, tests against existing content | **FULL extraction, densest video this round** | 11 | Real 120m² object, ЖК Topills. New named product **Шумопласт** (ASTic Group, granular polystyrene-bead, -28dB impact/-7-9dB airborne) — distinct from this store's existing Шумонет, with an explicit product-selection comparison by substrate unevenness. Application technique (compaction sound-QC signal, 48hr real-world cure vs. 24hr spec, no-extend-after-15min rule), sand-quality/frozen-sand caution, fiber additive, rebar-mesh mid-pour-lift technique, 2-3 day water-curing protocol, quantified screed-height cost-trap (~300,000 RUB ≈$3,800 on this real object), cost benchmark ≈6,000-7,000 RUB/m² ≈$80-$90/m² all-in. Region level 2. Low promotional ratio. |

**Status: COMPLETE — all 8 videos fetched and fully extracted, zero rate-limit issues.**

**Round 6 yield**: 8 videos, 76 genuinely-new facts (11+10+10+8+10+9+7+11, excluding duplicate/corroborating-only outcomes), yield = 9.5 new facts/video — **109% of Round 5's 8.75 baseline**, well above the 1.0/video floor. No stop-and-ask trigger.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 8 videos fetched serialized one at a time with real spacing (achieved by interleaving each video's own full extraction/routing/CSV/archiving work between fetches, never an idle wait), consistent with every prior round's clean result on this channel.

### Region-check finding, per this round's explicit brief

Region evidence again varied video to video: 5 of 8 videos stayed at level 2 (channel-only Moscow association); **3 of 8 cleared level 1 directly** (video 4 via "Новый Арбат," video 6 via "улица Челомея," and — per the task brief's own framing — video 4's district naming was the strongest a-priori level-1 candidate of the batch and confirmed as such). Video 3's region was **weaker than usual even at level 2**, since the featured object isn't the channel's own execution (flagged explicitly in that video's note) — this project's per-video region-check discipline held even for that edge case rather than defaulting to the channel's usual association.

### Language check

Videos 1 ( `g1b6Hxx-HUk`), 3 (`JLjCveR-ft0`, English title, confirmed Russian audio implicitly by transcript fetch), and all others were fetched with `language: ru` returned by `youtube-transcript-api`; video 1's English on-screen title was individually verified against Russian spoken audio. No English-audio video was encountered.

### Cross-check findings, per this round's explicit brief

- **Video 3 (1,300,000 RUB, 38m²) and video 4 (New Arbat, 75m²)** were both explicitly checked for confirmed year/area via `yt-dlp` metadata before deciding whether to add them to the existing real-object cost-benchmark series (2022: 1,424,000 RUB/45m²; 2024: 1,122,000 RUB). **Neither was force-fit into that series**: video 3 is full-scope (rough+finish), a different scope from the series' rough-stage-only totals, and is also not the channel's own execution; video 4's total is only partially recoverable (two stage-cost figures ASR-garbled/missing), so no complete comparable total exists for it this round. Both are recorded as their own separate, clearly-scoped data points instead — the same discipline that caught Round 5's mislabeled "2026" video.
- **Video 4 is a direct follow-up on the same real object as Round 4's `IoQiGtso9Vk`** (historic Arbat apartment) — the channel's own spoken content confirms this is a return visit. This closes part of that case's previously-flagged "no total cost or floor-area" gap (75m², Stalin-era building, secondary market) and also surfaced an open, unresolved beam-material discrepancy (timber vs. metal) between the two videos' own wording, flagged rather than silently reconciled.
- **Video 5 (2024 market tiers) vs. Round 5's `LEsmpI8bWCY` (2025 market tiers)**: the explicit cross-check the task brief asked for. Finding: a genuine scope/methodology difference (2024 figure excludes design/furniture, 2025 figure includes them) means the two videos' similar raw RUB/m² numbers do **not** indicate price stability — if anything they suggest a real increase once scope is equalized. Recorded as an open cross-source finding, not a resolved year-over-year percentage.

## Progress Log

- 2026-08-24 — **Round 6 complete.** All 8 videos fetched serialized one
  at a time with real spacing (interleaved with each video's own full
  extraction/routing/CSV/archiving work), zero rate-limit issues across
  the entire round. All 8 fully extracted. Yield 76 new facts / 8 videos
  = 9.5 facts/video — 109% of Round 5's 8.75 baseline, well above the 1.0
  floor — no stop-and-ask trigger. Region checked explicitly per video:
  3 of 8 cleared level 1 directly (videos 4, 6, and video 3's weaker-
  than-usual level 2 due to the attribution nuance), 5 of 8 stayed at
  level 2. Two videos (3, 4) were explicitly checked against the
  existing real-object cost-benchmark series and correctly kept
  separate rather than force-fit (different scope in both cases). Video
  4 was found to be a direct follow-up on the same real object as Round
  4's `IoQiGtso9Vk`, closing part of that case's cost/area gap and
  surfacing an open beam-material wording discrepancy. Video 5 was
  explicitly cross-checked against Round 5's 2025 market-tier video —
  found a genuine scope/methodology difference rather than a clean
  year-over-year comparison. Content routed to
  `11_Budget_and_Planning/Budgeting_Guide.md` (3 new benchmark/cross-
  check entries), `11_Budget_and_Planning/_supporting/knowledge/intermediate/store/Rules_Heuristics.md`
  (5 new topic-area sections), `17_Design_and_Ergonomics/analysis/Functional_Zoning_and_Furniture_Arrangement.md`
  (first real content on this previously-empty placeholder page),
  `17_Design_and_Ergonomics/analysis/Decor_and_Finish_Selection_Technique.md`
  and `Family_Scenario_Driven_Design.md` (new sections each),
  `13_Surfaces_and_Finishes/Flooring_Guide.md` (3 new sections),
  `Ceilings_Guide.md` (2 new sections), `Walls_and_Paint.md` (1 new
  section), `analysis/Soundproofing.md` (1 new named-product section),
  and `10_Balcony/Balcony_Index.md` (1 new section). All price figures
  normalized to USD via `tools/pricing/currency_converter.py`'s
  trailing-6-month average anchored to each video's own confirmed
  publish date. One rounding-bucket fix applied (a $636/m² figure
  corrected to $640/m² in two files) after `tools/verify_batch.py`
  flagged it against the pre-round commit (`4b3eccc`) — re-run passed
  clean afterward. `tools/youtube/archive_transcripts.py` run (dry-run
  first, all 8 matched correctly); all 8 source notes' bottom
  `[source: ...]` inline links needed the same manual fix as Round 5
  (frontmatter `transcript_file:` auto-updated by the script, bottom
  link was not) — corrected by hand for all 8. All 8 new CSV rows
  independently re-verified via Python's `csv` module to parse into the
  correct 15 columns each with `archived` status.

## Round 7 — Plumbing/flood-prevention technique, mechanized putty, window-masking, electrical pricing, wall cracks, real case studies (8 videos, dispatched 2026-08-24)

Continues full-scale processing. Deliberately favors case-study/cost-
benchmark and named-technique content over recap "ТОП-N ошибок" formats
(per Rounds 3-6 findings). Includes two explicit cross-checks requested
for this round: video 3 (mechanized putty) against Rounds 1-3's existing
plastering/wall-squareness content, and video 6 (wall cracks) against
Round 1's masonry acceptance video (`caDB-roRasI`) and the building-
settlement deformation-seam mechanism already flagged twice on this
channel. Videos 7 and 8 were each checked for confirmed year/scope
before deciding whether to add them to the existing real-object cost-
benchmark series.

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `O_2Jji7NAHQ` | Сантехнический шкаф. Зачем каждый элемент? Как сэкономить? Как избежать потопа, плесени и грибка? | Plumbing-cabinet technique/economy, flood/mold-prevention framing | **FULL extraction** | 9 | Interview with Mikhail (engineering-systems specialist, 20+yr experience), secondary-market object. Upload date 2024-04-07 confirmed via yt-dlp. Region level 2. No RUB prices spoken (no conversion applicable). Heavy corroboration of existing dense inlet-node/pressure/leak-protection content, correctly not re-extracted. New: 3D-printed reducer-key tool, cheap-Chinese-analog-substitute economics (works backward / needs annual replacement vs 5-10yr), aluminum-sheet lining alternative for a compromised masonry shaft, ~1yr-minimum DIY-experience heuristic (пакля packing skill), backward-installed-meter QC/fraud-risk red flag, mandatory RCD on cabinet outlet, 4-6mo whole-node maintenance cadence, mandatory cabinet ventilation vs mold, client-complaint-driven water-quality add-on filters. Low promotional ratio. |
| 2 | `YxXfsKoyx6M` | Как предотвратить потоп в квартире? / Монтаж системы отопления в квартире / Ремонт после потопа | Flood-prevention + heating-system installation technique; tests this channel's recurring flooding-incident theme for genuinely new mechanism | **FULL extraction** | 6 | Real flood-damage case study, ЖК "Лучи," leak from upstairs neighbor's own developer heating pipe. Upload date 2023-05-28 confirmed via yt-dlp. Region level 2. **Genuinely new mechanism, not a restatement of the towel-warmer/tee-joint flooding themes already documented**: гофра (corrugated-conduit) hidden-leak-travel mechanism, AC-condensate seasonal-elimination diagnostic heuristic, radiator side-connection to protect the baseboard-drilling path, 24hr water-temperature-equilibration wait before a heating pressure test, real flood-remediation cost benchmark >300,000 RUB ≈$4,100 (a distinct damage-remediation category, not blended with the renovation cost-benchmark series). Replacement-system component list corroborates existing inlet-node sequence, not re-extracted. Low promotional ratio. |
| 3 | `G0vtTswg5Ck` | Как сделать ровные стены в квартире? Механизированная шпатлевка. Все секреты. | Mechanized-putty wall-leveling technique, explicit cross-check against Rounds 1-3 plastering/squareness content | **FULL extraction, cross-check confirmed no overlap** | 9 | Named-technique tutorial, master finisher Eduard. Upload date 2023-07-02 confirmed via yt-dlp. Region unresolved (no city/development named). **Explicitly cross-checked against `D1REgSDwILU` (Round 1), `r1eyXzXNdI0` (Round 2), and `lTeNBUR1u8g` (Round 3) — no overlap found**: this covers the spray-putty-machine equipment/technique itself, a sub-topic none of those sources touched. New: two-whisk mixer, day-split corner-protection sequencing, orbital-vs-eccentric sander tradeoff, wallpaper-vs-paint finish-path branching, real 70m² 6-day-mechanized-vs-2-week-hand speed benchmark, 2-person fatigue-staggered crew composition, trade-specialization speed/quality rationale. Low promotional ratio. |
| 4 | `QtQBGLzS698` | Как заклеить окно правильно? Мастер-класс. Ремонт в ЖК Оранж Парк. | Window-sealing masterclass, tests fit against existing Windows pages | **FULL extraction** | 8 | Real jobsite masterclass — actually a dust-protection **film-masking** technique (not weatherproofing/slope-insulation), foreman Sergey Vasilyevich. Upload date 2021-03-25 confirmed via yt-dlp. **Region: level 2** — "ЖК Оранж Парк" named, no city spoken. **Cross-checked against `Windows_Slope_Finishing.md` and `Windows_Acceptance_Checklist.md` — no overlap** (neither page has masking-film content); also cross-checked against `Demolition.md`'s existing general "wrap windows in film" rule — this is the concrete step-by-step technique behind that rule, not a duplicate. New: film-width preference, overlap-margin technique, top-edge gap for later puttying, static-cling positioning + a tape-type nuance, scratch-avoidance trim technique, operable-sash ventilation-compatible masking, windowsill protection, dark-frame caution, a real 5min-vs-15-20min time-tradeoff benchmark. Low promotional ratio. |
| 5 | `qnmVK1R3X0k` | Электрика в квартире, цена// Как избежать косяков при ремонте квартиры | Electrical pricing + mistakes-avoidance, cross-check against existing electrical content | **FULL extraction** | 7 | Sergey Petrishin's own methodology explainer. Upload date 2023-04-30 confirmed via yt-dlp. Region unresolved. **Despite "цена" in the title, no RUB prices are actually spoken** (on-screen table only, not ASR-extractable). Heavy overlap with existing electrical content correctly excluded (junction-boxes-in-backboxes, temp-outlet test, and a Bentley/Hyundai restatement of Round 6's Bentley/VW/Lada analogy). New: project/smeta cross-review sequencing, panel-size decision framework, wire-labeling hiring-vetting red flag, live-circuit-during-drywall damage-detection mechanism, an explicit 4-factor cost-driver framework, a performance-vs-aesthetics admission, a ceiling-priming client-consent cost item. Low promotional ratio. |
| 6 | `UhE9cOJ35FY` | Как исправить трещины на стенах // Почему трескаются стены в квартире? | Wall-crack repair technique, explicit cross-check against Round 1's masonry/settlement-crack content and the deformation-seam mechanism | **FULL extraction, cross-check confirms a third recurrence** | 6 | Real crack-repair case study. Upload date 2023-05-14 confirmed via yt-dlp. Region unresolved. **Explicitly cross-checked against `caDB-roRasI` and the deformation-seam mechanism already flagged in Round 1 videos 1 and 4 — confirmed this is a third recurrence**; the video's own "root causes" section is a near-complete restatement of the existing masonry-acceptance checklist, correctly not double-counted. The genuinely new content is the *repair* technique itself (first-time application by this company): drill-and-inspect diagnostic, groove-and-soundproof-drywall-strip patch technique, recessed paper-tape seam technique, reapplication on a second crack in the same video, and a real repair cost/time benchmark (~3 days, ≈20,000-30,000 RUB ≈$280-$420 — a distinct defect-repair cost category, not blended with renovation-stage benchmarks). Low promotional ratio. |
| 7 | `FRRT0ZrhjaI` | Ремонт квартиры, цена. Новостройка 54 м2. Обзор готовой квартиры, румтур. | Real new-build case-study/room tour with a stated floor area, candidate for the real-object cost-benchmark series if year/total cost confirmed | **FULL extraction — not added to the cost-benchmark series** | 8 | Real 54m² room tour, client (Marina) present. Upload date 2024-01-14 confirmed via yt-dlp. Region unresolved. **Checked explicitly for a usable total/area per this round's brief — none exists**: every per-room cost is shown on-screen only, never spoken, so nothing is ASR-extractable except one real spoken furniture price (700,000 RUB wardrobe ≈$7,500) and two generic company "starting from" rates at the end (not this apartment's actual spend) — correctly **not** forced into the real-object benchmark series. New: 4-factor wardrobe cost-driver breakdown, a manufacturing-defect free-rework anecdote, a sofa usable-width heuristic, a fixed-distance TV-diagonal workaround, a wood-panel toilet-access-door design, a range-hood-type-change hole-relocation redo, a 3D-panel-integration precision caution, an AC-placement precision caution, and a procurement/price-verification workflow. Heated-wall towel-warmer content correctly excluded as a same-channel Round 6 restatement. Medium promotional ratio. |
| 8 | `tYcH95rlgNw` | Как выглядит ремонт за 5 млн рублей в 2023 году? // С какими трудностями столкнулись при ремонте? | Real 2023 cost-benchmark case study, candidate to extend the multi-year real-object benchmark series if scope is comparable | **FULL extraction — new 7th cost-benchmark case, added to the series** | 9 | Real case study, client Shamil, foreman Yura. **Genuinely confirmed 2023** (spoken "в 2023 году" plus yt-dlp upload date 2023-06-04) — clears the year-confirmation bar. Region unresolved. **Real total spoken cost, full turnkey scope, confirmed 54m² area: 5,250,000 RUB ≈$78,700 (≈$1,500/m², trailing-12-month rate given the project's own ~2yr timeline)** — a genuinely new, distinctly-scoped data point, kept separate from the rough-only/labor-only series per this project's non-blending convention, comparable in kind to Round 6's `JLjCveR-ft0` full-scope case. New: ~2yr multi-stage COVID-delayed timeline, per-room area breakdown for a 54m² 2BR layout, hexagonal-tile/cork-transition entry technique, thin-6mm-tile 45° layout difficulty, a grout-staining-on-light-tile-with-ordinary-cement-grout risk+fix, a client-sourced DIY Instagram accent-panel technique, an aesthetic utility hatch, and a real material-buffer-stock logistics lesson. Low promotional ratio. |

**Status: COMPLETE — all 8 videos fully fetched and extracted, zero rate-limit issues.**

**Round 7 yield**: 8 videos, 62 genuinely-new facts (9+6+9+8+7+6+8+9, excluding duplicate/corroborating-only outcomes), yield = 7.75 new facts/video — **82% of Round 6's 9.5 baseline** (within the >50%-drop stop-and-ask threshold, and well above the 1.0/video floor). No stop-and-ask trigger.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 8 videos fetched serialized one at a time with real spacing (achieved by interleaving each video's own full extraction/routing/CSV/archiving work between fetches — never an idle wait), consistent with every prior round's clean result on this channel.

### Region-check finding, per this round's explicit brief

Region evidence again varied video to video, not a fixed channel answer, consistent with every prior round. Per-video: video 1 (level 2, channel-only Moscow association), video 2 (level 2), video 3 (unresolved — no city/development named), video 4 (level 2 — "ЖК Оранж Парк" named but no city spoken), video 5 (unresolved), video 6 (unresolved), video 7 (unresolved), video 8 (unresolved). **No video this round cleared level 1** — a notably weaker region-evidence round than Round 6 (3 of 8 level-1) or Round 4 (4 of 8 level-1), consistent with this project's standing finding that region evidence varies video to video rather than following a fixed channel pattern; this round's mix (equipment/technique explainers and unbranded case studies) simply didn't happen to include a directly-named city/street/development this time.

### Language check

All 8 videos had Russian titles and confirmed Russian spoken audio (`youtube-transcript-api` returned `language: ru` for every fetch); no English-titled video was encountered this round.

### Mechanized-putty cross-check finding (video 3), per this round's explicit brief

**Explicitly cross-checked against Round 1's `D1REgSDwILU` (base-coat plastering), Round 2's `r1eyXzXNdI0` (same-channel plastering restatement test), and Round 3's `lTeNBUR1u8g` (wall-squareness QC) — confirmed no overlap.** This video covers a distinct sub-stage (mechanized/sprayed putty application, the finishing stage after base-coat plastering) with its own equipment, sequencing, and QC content that none of those three sources touched. Genuinely new material/technique, not a same-channel restatement — one of this round's stronger yields (9) as a direct result.

### Wall-crack cross-check finding (video 6), per this round's explicit brief

**Explicitly cross-checked against Round 1's `caDB-roRasI` (masonry acceptance) and the building-settlement deformation-seam mechanism already flagged twice on this channel (Round 1 videos 1 and 4) — confirmed this is a third recurrence of that mechanism**, not new. The video's own "root causes" section (block stagger/offset, deformation joints at top-course and new-to-existing seams, tie-back reinforcement frequency, flashlight joint-fill check) is a near-complete restatement of `caDB-roRasI`'s existing masonry-acceptance checklist on `07_Bathroom/analysis/Structure_and_Framing.md` — correctly not double-counted, which held this video's yield down to 6 despite a dense repair-technique section. The genuinely new content was isolated to the *repair* technique itself (drill-and-inspect diagnostic, groove-and-drywall-strip patch, recessed paper-tape technique, a second-crack reapplication, and a real cost/time benchmark) rather than the root-cause explainer.

### Cost-benchmark-series findings (videos 7 and 8), per this round's explicit brief

- **Video 7 (54m² room tour) was checked for a usable total/area and found not to clear the bar** — despite the 54m² figure in the title, no total cost is ever spoken (only shown on-screen), so this video contributes technique/mistake content and one real furniture price but is **not** added to the cost-benchmark series, consistent with the discipline that caught Round 5's mislabeled "2026" video and Round 6's partial-Arbat figure.
- **Video 8 (5,000,000 RUB, 2023) was checked and cleared the bar decisively** — the year is confirmed two independent ways (spoken "в 2023 году" and `yt-dlp` upload date), the area is confirmed (54m²), and the total (5,250,000 RUB) is spoken directly and explicitly framed as all-in turnkey scope. Added as this channel's **7th** cost-benchmark data point in `Budgeting_Guide.md` — kept as its own separately-dated/scoped entry, not averaged with the rough-only, labor-only, or other full-scope cases already on that page.

## Progress Log

- 2026-08-24 — **Round 7 complete.** All 8 videos fetched serialized one
  at a time with real spacing (interleaved with each video's own full
  extraction/routing/CSV/archiving work), zero rate-limit issues across
  the entire round. All 8 fully extracted. Yield 62 new facts / 8 videos
  = 7.75 facts/video — 82% of Round 6's 9.5 baseline, well above the 1.0
  floor and not a >50% drop — no stop-and-ask trigger. Region checked
  explicitly per video: no video cleared level 1 this round (a notably
  weaker region-evidence round than Round 4 or 6), 4 stayed at level 2,
  4 unresolved. Two explicit cross-checks performed as instructed: video
  3 (mechanized putty) against Rounds 1-3's plastering/squareness
  content — confirmed no overlap, genuinely new sub-topic; video 6 (wall
  cracks) against Round 1's masonry acceptance video and the
  deformation-seam mechanism — confirmed a third recurrence, root-cause
  section correctly excluded from the fact count, only the repair
  technique itself counted as new. Videos 7 and 8 were both explicitly
  checked against the existing real-object cost-benchmark series before
  deciding: video 7's 54m² figure was **not** force-fit in (no spoken
  total), video 8's 5,250,000 RUB / 54m² / confirmed-2023 total **was**
  added as a 7th, separately-scoped data point. Content routed to
  `12_Engineering_and_Systems/analysis/Water_Inlet_Node_Components.md`,
  `Cost_Drivers_and_Buying_Guidance.md`, `Pressure_Testing.md`,
  `Leak_Protection_Systems.md`, `Radiators_and_Convectors.md`,
  `Rough_Electrical_Sequencing.md`; `13_Surfaces_and_Finishes/Walls_and_Paint.md`;
  `11_Budget_and_Planning/analysis/Demolition.md`;
  `11_Budget_and_Planning/Budgeting_Guide.md` (a flood-remediation cost
  data point plus the new 7th cost-benchmark case);
  `07_Bathroom/analysis/Tile_Selection_and_Layout.md`;
  `14_Furniture/analysis/Wardrobe_Worked_Cases.md`;
  `17_Design_and_Ergonomics/analysis/Functional_Zoning_and_Furniture_Arrangement.md`;
  and the general store's `Rules_Heuristics.md` (3 new topic-area
  sections). All price figures normalized to USD via
  `tools/pricing/currency_converter.py`'s trailing-6-or-12-month average
  anchored to each video's own confirmed publish date.
  `tools/youtube/archive_transcripts.py` run (dry-run first, all 8
  matched correctly, 2 of them renamed by the script to match the note's
  own filename slug); all 8 source notes' bottom `[source: ...]` inline
  links needed the same manual fix as Rounds 5-6 (frontmatter
  `transcript_file:` auto-updated by the script, bottom link was not) —
  corrected by hand for all 8. All 8 new CSV rows independently
  re-verified via Python's `csv` module to parse into the correct 15
  columns each with `archived` status. `tools/verify_batch.py` to be run
  against the pre-round commit before finishing.

## Round 8 — Plumbing cabinet, window selection, client interview, foam-block masterclass, monolith electrical, finishing materials/tips (8 videos, dispatched 2026-08-24)

Continues full-scale processing. A fresh, topic-diverse 8-video selection
from the 341-video manifest (288 fresh/unprocessed at the start of this
round), favoring named-technique and acceptance-checklist content over
recap "ТОП-N ошибок" or pure room-tour formats per this channel's own
established pattern. Includes one Russian-noise-law/quiet-hours video
that hit a genuine no-captions failure (not a rate-limit), and three
explicit cross-checks requested for this round: video 5 (foam-block
masterclass) against Round 1's masonry acceptance video (`caDB-roRasI`);
video 6 (monolith electrical) against existing electrical sequencing
content (Rounds 2, 4, 7); and video 8 (finishing tips) against Round 7's
finishing-works video (`Q0sVq_1SIQM`) and Round 2's wallpaper/paint video
(`VcrYHkDgb0o`).

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `D-DFsBMjlxQ` | Зачем так много кранов? Это не обман? Сердце квартиры - ванная комната. | Bathroom-fixture/faucet technique (English title) | **FULL extraction** | 6 | English title, confirmed Russian audio. Despite the "faucets" framing, this is a plumbing-cabinet/water-inlet-node component walkthrough — heavily overlapping with `Water_Inlet_Node_Components.md` and this channel's own Round 7 `O_2Jji7NAHQ`, correctly not double-counted. New: Energoflex color-coded pipe-insulation mechanism, 6-8atm normal / 11atm hydraulic-shock-spike figure, fine-filter-omission warranty-void claim, coarse-filter landing-placement/meter-install precondition, check-valve old-building-stock risk angle, AC-condensate+filter-drain dry-siphon consolidation. Region level 2. Low promotional ratio. |
| 2 | `4bv7Aa6YLCo` | Как выбрать окна? Основные ошибки и важные детали. | Window-selection technique (English title), cross-check against Windows pages | **FULL extraction** | 9 | English title, confirmed Russian audio. Studio explainer, dense pre-purchase profile/hardware/glazing/gasket/sill selection primer. **Explicitly cross-checked against `Windows_Quality_and_Buying.md`, `Windows_Hardware_Selection.md`, `Windows_Slope_Finishing.md`, `Windows_Acceptance_Checklist.md`, and Round 7's `QtQBGLzS698`** — no overlap found, genuinely new selection-criteria content. **⚠️ Perspectives disagreement flagged**: this source recommends Rehau/Veka/European brands, in direct tension with the existing Zemskov claim that profile brand doesn't affect quality within a tier. New: profile-thickness ladder, chamber-count range, tilt-turn mandatory-even-without-ventilation reasoning, glazing-unit chamber/add-on cost drivers, gasket contour+cross-section longevity rule, windowsill material-by-function guide, drip-cap fastening/length/rattle-fix rule. Region level 2. Low promotional ratio. |
| 3 | `eInWxbd_UiA` | Как принять черновой этап ремонта? Основные ошибки. Технический дизайн. | Rough-stage acceptance checklist (expected, per title) | **PARTIAL extraction — title/format mismatch** | 5 | **⚠️ Despite the acceptance-checklist title, this is a client-satisfaction testimonial interview** (Denis/Ekaterina, 2020, COVID/ruble-crash era spoken directly) — the same low-yield sub-format flagged in Round 4 (`F0ZHsu4k6JY`). Only genuinely reusable content extracted per the value-filter: ventilation-before-walls sequencing rule, structural-column-integration wall-design technique, design-team-vs-construction-team communication-quality independence finding, client material-price self-verification variance band, floor-height-driven leak-sensor investment rationale. Region unresolved. Medium promotional ratio (heavy client-sentiment content correctly excluded). |
| 4 | `tVex6zojJng` | Как не нарушить закон о тишине? Основные правила при ремонте в новостройке. | Moscow noise-law/quiet-hours regulation, expected level-1 regulatory candidate | **SKIPPED — no captions available** | 0 | Both `youtube-transcript-api` (subtitles disabled) and `yt-dlp` (no subtitle tracks for ru/en) failed with exit code 1 — a genuine per-video no-captions failure, `reason_class: null` in both attempts, **not a rate-limit/IP-block signature**. Not fetched, not extracted. The intended noise-law-routing question (general store vs. `16_Legal_and_Regulations/`, which is strictly Belarus-scoped) was never reached since no content was retrieved. |
| 5 | `A4OmiqS6kYo` | Строим стены из пеноблока. Мастер класс. | Foam-block partition masterclass, cross-check against Round 1's masonry acceptance | **FULL extraction, cross-check confirms complementary (not duplicate) content** | 7 | Real jobsite masterclass with a second practitioner (Alexander Mikhalych) — a **builder's-perspective** technique video, distinct in angle from Round 1's `caDB-roRasI` (an **acceptance/QC checklist** for the same material). **Explicitly cross-checked**: offset/stagger rule, corner-toothing, and top-of-wall deformation gap all corroborate `caDB-roRasI` and were correctly not double-counted. New: design-to-raw-dimension plaster-allowance conversion, precision utility-chase layout coordinated with future kitchen-cabinet install, "average-face" leveling method preventing cumulative runaway error, rebar-groove cure-time sequencing rule, working-around-existing-riser-rebar technique, reinforcement-groove cutting detail, wallpaper-paste adhesive-application analogy. Region unresolved. Low promotional ratio. |
| 6 | `sqk0Nl8AVYI` | Электромонтаж в монолите. Советы мастера. | Monolith-specific electrical wiring, cross-check against existing electrical sequencing | **FULL extraction, cross-check confirms genuinely new sub-topic** | 9 | Sergey Petrishin's own practitioner walkthrough. **Explicitly cross-checked against `Rough_Electrical_Sequencing.md` and `Cable_Circuits_and_Panel_Design.md`** — the existing monolith note there only covers breaker-panel niches; no overlap, genuinely new sub-topic. New: monolith chase-depth/rebar-cutting-prohibition mechanism, foam-block-covering soundproofing side-benefit, real 10min-vs-1hr time comparison, diamond-core-bit water-cooling technique for granite-aggregate monolith, outlet-box flush-mount discipline, hole-enlarging pull-out-resistance fix, ⚠️ phase-loss/neutral-disconnection 380V building-shared-infrastructure failure mechanism, cable-slack-for-design-ambiguity heuristic, supplier-verification-before-wiring habit. Region unresolved. Low promotional ratio. |
| 7 | `Rm0aHk4flxc` | Как выбрать отделочные материалы? Основные принципы и секреты. | General finishing-materials comparison/selection (English title) | **FULL extraction** | 10 | English title, confirmed Russian audio. Real client+designer finishing-materials shopping trip (tile/décor showroom + hypermarket). New: two-copy design-project shopping habit, paint fan-deck necessity + trial-can cost tip, scored-large-format-tile small-tile-look technique, grout-color selection rule + mosaic-grout design lever, decorative micro-cement/anti-vandal-plaster durability guidance for high-traffic zones, angled-sample lighting-distortion warning, laminate bevel/wear-class/thickness criteria, composite decking balcony choice + price point, baseboard clip-vs-screw-anchor fixation reality check, real-time foreman shopping-trip consultation habit. Region level 2 (ASR-truncated Moscow location mention, not promoted to level 1). Low promotional ratio. |
| 8 | `KlIQxR3vWU8` | Финишные работы. Советы по лепнине, обоям, плитке. | Finishing-work tips (molding/wallpaper/tile), cross-check against Round 7 and Round 2 finishing/wallpaper videos | **FULL extraction, cross-checks confirm no overlap** | 7 | Montage of several practitioner interviews (wallpaper/paint finisher; 25yr mosaic/pool specialist). **Explicitly cross-checked against Round 7's `Q0sVq_1SIQM` and Round 2's `VcrYHkDgb0o`** — no overlap found on either. This video's monolith-rebar mention restates this round's own video 6 (`sqk0Nl8AVYI`), correctly not double-counted. New: molding two-tone sponge-wipe paint technique, wallpaper-glue toxicity myth debunked, color-indicator glue product feature, floor-level-transition thickness-direction-asymmetry rule, mosaic-vs-tile curved/organic-shape capability distinction, ⚠️ luxury gold-leaf mosaic €5,500/m² reference price point (out of project budget scope, not converted), common-area-quality building-signal heuristic. Region unresolved. Low promotional ratio. |

**Status: COMPLETE — 7 of 8 videos fetched and extracted (1 partial low-value pass on video 3), 1 genuinely skipped for no captions (video 4), zero rate-limit issues.**

**Round 8 yield**: 7 videos processed (video 4 not fetched — no captions, excluded from the denominator per this project's `skipped` convention), 53 genuinely-new facts (6+9+5+7+9+10+7, excluding duplicate/corroborating-only outcomes), yield = 7.6 new facts/video — **98% of Round 7's 7.75 baseline** (comfortably within the >50%-drop stop-and-ask threshold, and well above the 1.0/video floor). No stop-and-ask trigger.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 7 successful fetches were serialized one at a time with real spacing (achieved by interleaving each video's own full extraction/routing/CSV work between fetches — never an idle wait), consistent with every prior round's clean result on this channel. Video 4's failure was independently confirmed as a genuine no-captions case (`youtube-transcript-api`: "Subtitles are disabled for this video"; `yt-dlp`: no subtitle tracks for ru/en) — both attempts carried `"reason_class": null` in the `.FAILED.meta.json` record, not the rate-limit/IP-block signature this project treats as a circuit breaker. Per the standing rule, it was left unlogged/pending in no meaningful sense — instead logged with `status: skipped` and the specific no-captions reason, since it was a genuine per-video failure, not a block requiring a stop.

### Region-check finding, per this round's explicit brief

Region evidence again varied video to video, not a fixed channel answer, consistent with every prior round. Per-video: video 1 (level 2), video 2 (level 2), video 3 (unresolved), video 5 (unresolved), video 6 (unresolved), video 7 (level 2, with an ASR-truncated "в московском..." phrase explicitly not promoted to level 1 given the uncertainty), video 8 (unresolved). **No video this round cleared level 1** — consistent with Round 7's own finding that this channel's region evidence genuinely varies round to round, not a fixed pattern; this round's mix (studio explainers, a masterclass, and older 2019-vintage videos without the newer real-object case-study framing) simply didn't happen to include a directly-named city/street/development this time.

### Language check

Three videos carried English on-screen titles (1: `D-DFsBMjlxQ`, 2: `4bv7Aa6YLCo`, 7: `Rm0aHk4flxc`) — all three individually verified via `youtube-transcript-api` fetch metadata to have Russian spoken audio (`language: ru`), per this project's standing rule that title language is not a reliable signal. No English-audio video was encountered.

### Cross-check findings, per this round's explicit brief

- **Video 2 (window selection) vs. existing `Windows_*` pages and Round 7's `QtQBGLzS698`**: no overlap found — this video's pre-purchase component-selection primer (profile thickness/chamber count, tilt-turn hardware reasoning, glazing-unit add-ons, gasket contour/cross-section, windowsill material, drip-cap fastening) sits at a level of technical detail none of the existing Windows pages previously covered. Surfaced a genuine **Perspectives disagreement**: this source recommends known brands (Rehau, Veka, European hardware) directly contradicting the existing Zemskov claim that profile brand doesn't affect quality within a market tier — recorded as an open disagreement, not resolved.
- **Video 5 (foam-block masterclass) vs. Round 1's `caDB-roRasI`**: confirmed complementary, not duplicate, as anticipated in the round brief — a builder's-perspective masterclass (layout/leveling/reinforcement technique) vs. an acceptance/QC checklist for the same material. The offset/stagger, corner-toothing, and deformation-gap rules corroborate and were correctly excluded from the new-fact count; the layout-precision and leveling-compensation technique content was genuinely new.
- **Video 6 (monolith electrical) vs. existing electrical sequencing content (Rounds 2, 4, 7)**: confirmed genuinely new sub-topic, no overlap — the existing pages' only monolith-specific rule concerned breaker-panel niches; this video's chase-depth/rebar mechanism, drilling technique, and phase-loss failure mode were all new.
- **Video 8 (finishing tips) vs. Round 7's `Q0sVq_1SIQM` and Round 2's `VcrYHkDgb0o`**: no overlap found on either — neither existing source covered the molding two-tone paint technique, the wallpaper-glue myth, or the floor-level-transition thickness-direction asymmetry. This video's own monolith-rebar mention was, however, a same-round restatement of video 6 and was correctly not double-counted.

## Progress Log

- 2026-08-24 — **Round 8 complete.** 7 of 8 videos fetched serialized one
  at a time with real spacing (interleaved with each video's own full
  extraction/routing/CSV/archiving work), zero rate-limit issues. Video 4
  (noise-law/quiet-hours) hit a genuine no-captions failure (confirmed via
  both `youtube-transcript-api` and `yt-dlp` failure reason classes —
  neither was rate-limit-related), logged `status: skipped` with the
  specific reason, not left pending. 6 full extractions + 1 partial
  low-value pass (video 3, a title/format-mismatched client-testimonial
  interview). Yield 53 new facts / 7 processed videos = 7.6 facts/video —
  98% of Round 7's 7.75 baseline, well above the 1.0 floor — no
  stop-and-ask trigger. Region checked explicitly per video: no video
  cleared level 1 this round (2 at level 2, 4 unresolved, 1 skipped),
  consistent with Round 7's own finding that this channel's region
  evidence genuinely varies round to round. Language checked explicitly
  for all three English-titled videos (1, 2, 7) — all three confirmed
  Russian spoken audio. Three explicit cross-checks performed as
  instructed: video 5 (foam-block masterclass) vs. Round 1's masonry
  acceptance video — confirmed complementary, not duplicate; video 6
  (monolith electrical) vs. existing electrical-sequencing content —
  confirmed genuinely new sub-topic; video 8 (finishing tips) vs. Round
  7's and Round 2's finishing/wallpaper videos — confirmed no overlap on
  either, only a same-round internal restatement (video 6's monolith-rebar
  rule) correctly excluded. A genuine **Perspectives disagreement** was
  surfaced and recorded on `Windows_Quality_and_Buying.md` (does profile/
  hardware brand affect quality — this round's video 2 says yes, the
  existing Zemskov source says no). Content routed to
  `12_Engineering_and_Systems/analysis/Water_Inlet_Node_Components.md`,
  `Rough_Electrical_Sequencing.md`;
  `13_Surfaces_and_Finishes/analysis/Windows_Quality_and_Buying.md`,
  `13_Surfaces_and_Finishes/Walls_and_Paint.md`,
  `13_Surfaces_and_Finishes/Flooring_Guide.md`;
  `07_Bathroom/analysis/Structure_and_Framing.md`,
  `07_Bathroom/analysis/Tile_Selection_and_Layout.md`; and the general
  store's `Rules_Heuristics.md` (3 new topic-area sections: design-phase
  vetting/sequencing/structural-obstruction notes, finishing-materials
  shopping-trip habits, common-area quality signal). All 7 processed
  transcripts archived via `tools/youtube/archive_transcripts.py`
  (dry-run first, all 7 matched correctly); all 7 source notes' bottom
  `[source: ...]` inline links needed the same manual fix as Rounds 5-7
  (frontmatter `transcript_file:` auto-updated by the script, bottom link
  was not) — corrected by hand for all 7. All CSV rows (7 `archived` + 1
  `skipped`) independently re-verified via Python's `csv` module to parse
  into the correct 15 columns. `tools/verify_batch.py` run against the
  pre-round commit (`9b25e40`) — passed clean on the first run, no
  rounding-bucket or ID-drift problems found.

## Round 9 — Master switch, ventilation 6-years-later, bathroom tile/ceiling technique, partition materials, tile expo tour, wallpaper Q&A, construction sink (8 videos, dispatched 2026-08-24)

Continues full-scale processing, selected fresh from the 341-video
manifest for topic diversity, favoring named-technique/real-problem-
diagnosis content over recap "ТОП-N ошибок" or pure room-tour formats.
Includes a deliberate cross-check of the channel's own existing
"construction sink" concept mention on `Demolition.md` (video 8) and a
genuinely new-to-this-channel long-term-outcome format (video 2).

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `zuh3k15-STo` | What is a master switch? Electrician masterclass. Master-off switch. | Electrical technique (English title), cross-check against existing electrical content | **FULL extraction** | 6 | English title, confirmed Russian audio, real breaker-panel demo. Extends this channel's existing brief master-switch mentions on `Switches_and_Controls.md` with priority-group taxonomy, 4 implementation methods, contactor-vs-impulse-relay tradeoff + ≈4,000 RUB (≈$50) cost premium, appliance-timer-reset decision, electrician-vetting heuristic. Region level 2 (no city named; generic country-house mention only). Low promotional ratio. |
| 2 | `nhJI_yGjfRU` | Проблемы с вентиляцией/поэтапное решение. Ремонт в новостройке через 6 лет. | Real ventilation-problem diagnosis, 6-years-later revisit — genuinely new format for this channel | **FULL extraction — flagged format** | 6 | **Heavily ASR-garbled transcript**, facts extracted conservatively. A real return visit 6 years after the original renovation to fix a concealed shared-ventilation-valve defect that a new downstairs neighbor's complaint surfaced — a management-company technical-project sign-off did not catch it ("human error"). Forced a tile-color repair compromise. Generalist-vs-specialist labor error-rate heuristic and root-cause-analysis discipline routed to the general store. Region level 2 (residential complex named generically, no city). Low promotional ratio, no prices spoken. |
| 3 | `OperMXnGmXE` | Как класть плитку в ванной? Этапы, советы, ошибки. | Bathroom tile-laying stages/technique, cross-check against `Tile_Selection_and_Layout.md` | **FULL extraction** | 10 | Real object (named development, "Березовые аллеи"), presenter Maxim Kulish. Squareness verification, priming/cure sequencing, wall-before-floor sequencing, decorative-row height-calculation method, tile-lot consistency check, adhesive mechanics, and a genuine refinement to the page's existing "classic layout" centering rule (tile-width-dependent centering choice, worked 400×200mm vs. 500×200mm examples). Region level 2. Low promotional ratio. |
| 4 | `EQW9y4bNea0` | Материал для стен. Из чего лучше строить перегородки? | Partition-wall material comparison, cross-check against Round 5/6/8 partition content | **FULL extraction — corroborates + quantifies existing ranking** | 11 | Comedic cold-open settling into a real 4-material (drywall/tongue-groove gypsum/foam block/brick) comparison with real market-price data and sound-insulation dB figures (53/46/47/43 dB) — quantifies the existing qualitative ranking from Rounds 5/6/8 rather than duplicating it. Company discloses a forward-looking shift toward double-layer drywall for its own future work. Region level 2. Low promotional ratio. |
| 5 | `RfcoPP3dvcQ` | Потолок в ванну. Реечный, натяжной, касетный что лучше? | Bathroom-ceiling type comparison, tests fit against `Ceilings_Guide.md`'s Round 3 comparison | **FULL extraction — densest video this round** | 14 | Unusual dual-host format: builder Sergey Petrishin plus named design blogger Ekaterina Popova. Bathroom-specific comparison (slatted/cassette/glass-mirror/plastic/stretch) — complements, doesn't duplicate, Round 3's general painted/drywall/stretch comparison. Named slatted-ceiling brand tiers with a real 1.7×1.7m cost example (≈6,000-9,000 RUB), fixture-drop-height rules, cassette 30cm grid + tile-layout-parallel centering rule, Armstrong glass ceiling pricing, plastic-panel heat/odor caution, and a stretch-ceiling leak-resistant-not-leak-proof clarification. Region level 2. Low promotional ratio. |
| 6 | `P8GMYTARyNU` | Как выбрать керамическую плитку? Главные принципы. Цена, качество, стиль. | Ceramic-tile selection principles, cross-check against Round 4's tile-vs-porcelain primer | **PARTIAL extraction — title/format mismatch** | 6 | **Actually a trade-show/expo booth tour** (Italon, Kerama Marazzi), not a structured principles explainer — heavily ASR-garbled, brand-showcase-heavy. Per the value-filter rule, only genuinely generalizable heuristics extracted (rectified-tile zero-joint red flag, small-format-for-small-bathroom rule, contrast-grout design lever, metallic-insert accent-only rule, large-slab delivery/access caution); unconfirmed brand-specific prices excluded. No overlap with Round 4's material-science primer. Region unresolved (no location named). **Promotional ratio: high.** |
| 7 | `NyIj6h8hZHw` | Как правильно клеить обои! 17 вопросов мастеру по малярке и обоям! | Wallpaper-hanging Q&A (17 questions), cross-check against Round 2's wallpaper/paint video | **FULL extraction, second-highest yield this round** | 15 | Genuine Q&A with a named finishing specialist (маляр). Explicitly cross-checked against Round 2's `VcrYHkDgb0o` — 2 items corroborate/extend (dry-lay roll check, seam-glue-residue wipe), remainder new: wipeable-paint myth, vinyl door-casing shrinkage rule, glue-open-time skill differentiator, ceiling-vs-wall paint distinction, Benjamin Moore primer anecdote, 2-month full-apartment timeline, self-QC walkthrough discipline, trade-specialization stance (2nd voice), design-project value for the finishing trade, real undocumented-outlet rework case. Region level 2. Low promotional ratio. |
| 8 | `RNiSYvLX6Vc` | Строительная раковина, лайфхак на стройке. Пошаговая инструкция. | Construction-sink build masterclass, explicit cross-check against this channel's existing construction-sink mention on `Demolition.md` | **FULL extraction — cross-check confirms distinct source, new mechanism** | 8 | **Explicitly cross-checked against the existing "construction sink" mention on `Demolition.md`** (from an earlier round) — confirmed this video is **not** that mention's originating source (different upload dates, no cross-reference between the two transcripts), but the same underlying concept from the finishing-stage tool-washing angle rather than the existing flooding-prevention angle. Real build dimensions (80cm height, 12mm plywood shelf, 32mm mixer hole, 45mm drain hole) plus a wholly new tile-adhesion defect mechanism (dirty wet-cut tile bonding to its own dried cutting slurry instead of the wall, often misdiagnosed by installers as bad adhesive) — routed to `Tile_Selection_and_Layout.md`. Region unresolved. Low promotional ratio. |

**Status: COMPLETE — all 8 videos fully fetched and extracted (7 full extractions, 1 partial low-value pass on video 6), zero rate-limit issues.**

**Round 9 yield**: 8 videos, 76 genuinely-new facts (6+6+10+11+14+6+15+8, excluding duplicate/corroborating-only outcomes), yield = 9.5 new facts/video — **125% of Round 8's 7.6 baseline**, well above the 1.0/video floor. No stop-and-ask trigger.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 8 videos fetched serialized one at a time with real spacing (achieved by interleaving each video's own full extraction/routing/CSV/archiving work between fetches — never an idle wait), consistent with every prior round's clean result on this channel.

### Region-check finding, per this round's explicit brief

Region evidence again varied video to video, not a fixed channel answer, consistent with every prior round. Per-video: video 1 (level 2, no city named), video 2 (level 2, residential complex named generically), video 3 (level 2, named development "Березовые аллеи"), video 4 (level 2), video 5 (level 2), video 6 (unresolved — trade-show setting, no location at all), video 7 (level 2), video 8 (unresolved — no location named). **No video this round cleared level 1** — a notably weaker region-evidence round than Round 4 or Round 6, but consistent with this channel's standing finding that region evidence varies round to round rather than following a fixed pattern; this round's mix (studio/expo explainers, an older 2018-2019-vintage technique cluster, and a long-term-revisit case) simply didn't happen to include a directly-named city/street/development this time.

### Language check

Video 1 (`zuh3k15-STo`) carried an English on-screen title ("What is a master switch?...") and was individually verified via `youtube-transcript-api` fetch metadata (`language: ru`) to have Russian spoken audio, per this project's standing rule that title language is not a reliable signal. All other videos had Russian titles and confirmed Russian spoken audio.

### Cross-check findings, per this round's explicit brief

- **Video 3 (bathroom tile stages) vs. the existing "classic layout" centering rule** (Zemstandart/Zemskov, on `Tile_Selection_and_Layout.md`): not a duplicate — this video adds a genuine tile-width-dependent refinement (whether to center on the tile's center or edge depends on the specific tile's width, worked 400×200mm-vs-500×200mm examples), extending rather than restating the existing rule.
- **Video 4 (partition materials) vs. Round 5's `3sRfRiQ8XfE`, Round 6's `nT0qOcN_nEQ`, and Round 4's `PBkZQHkjciE`** (existing partition-material rankings): confirmed corroboration-with-quantification, not duplication — this video's real sound-insulation dB figures (53/46/47/43 dB) and real market unit pricing give numeric backing to a ranking those three sources had already stated qualitatively.
- **Video 5 (bathroom ceilings) vs. Round 3's `lvixGbwo0Ug`** (general painted/drywall/stretch ceiling comparison): confirmed complementary — that source covers general-room ceiling types; this video is bathroom-specific and covers three types (slatted, cassette, glass/mirror) not in that source, with only partial overlap on stretch-ceiling mold/yellowing questions, which this video corroborates and extends with a leak-resistant-not-leak-proof clarification.
- **Video 6 (tile expo tour) vs. Round 4's `rt9R26k6dEM`** (tile-vs-porcelain material/durability primer): confirmed no overlap — that source covers material science and format taxonomy; this one covers brand-showcase design trends and delivery logistics instead, genuinely complementary despite both nominally being about tile selection.
- **Video 7 (wallpaper Q&A) vs. Round 2's `VcrYHkDgb0o`** (wallpaper/paint acceptance checklist): 2 items confirmed as direct corroboration-with-extension (dry-lay roll check gained a sheet-numbering step; seam-glue-residue wipe gained a brand-dependency note) and were not double-counted; the remaining 13 items are genuinely new.
- **Video 8 (construction sink) vs. this channel's own existing "construction sink" mention on `Demolition.md`**: the round brief's explicit ask. **Confirmed this video is not that mention's originating source** — the two videos have different upload dates and neither transcript references the other — but they describe the identical physical fixture from two different life-cycle angles (this video: finishing-stage tool-washing and a tile-adhesion defect mechanism; the existing note: demolition-stage flood prevention). The existing `Demolition.md` entry was extended with a cross-reference to this video's build instructions and the new tile-adhesion mechanism, rather than treated as a duplicate.

## Progress Log

- 2026-08-24 — **Round 9 complete.** All 8 videos fetched serialized one
  at a time with real spacing (interleaved with each video's own full
  extraction/routing/CSV/archiving work), zero rate-limit issues across
  the entire round. 7 full extractions + 1 partial low-value pass (video
  6, a title/format-mismatched trade-show expo tour). Yield 76 new facts
  / 8 videos = 9.5 facts/video — 125% of Round 8's 7.6 baseline, well
  above the 1.0 floor — no stop-and-ask trigger. Region checked
  explicitly per video: no video cleared level 1 this round, 6 stayed at
  level 2, 2 unresolved (a trade-show setting and a build-instructions
  video with no location spoken). Language checked explicitly for the
  one English-titled video (1) — confirmed Russian spoken audio. Five
  explicit cross-checks performed as instructed (see the dedicated
  finding section above): video 3 vs. the existing classic-layout
  centering rule (genuine refinement, not duplicate); video 4 vs. three
  existing partition-material rankings (corroboration-with-
  quantification); video 5 vs. Round 3's general ceiling comparison
  (complementary, bathroom-specific); video 6 vs. Round 4's tile-vs-
  porcelain primer (no overlap); video 7 vs. Round 2's wallpaper/paint
  video (2 items extended, 13 new); and **video 8 vs. this channel's own
  existing construction-sink mention on `Demolition.md`, per the round's
  explicit brief — confirmed a distinct source describing the same
  fixture from a different life-cycle angle, not the originating source**,
  adding a wholly new tile-adhesion defect mechanism in the process.
  Video 2's 6-years-later revisit format was flagged as genuinely new
  for this channel — a real long-term-outcome check, not a same-project
  acceptance checklist, per the round's explicit brief; extracted despite
  a heavily ASR-garbled transcript, with facts kept conservative. Content
  routed to `12_Engineering_and_Systems/analysis/Switches_and_Controls.md`,
  `Fresh_Air_Ventilation_and_Ducting.md`;
  `07_Bathroom/analysis/Tile_Selection_and_Layout.md` (2 new sections);
  `12_Engineering_and_Systems/analysis/Soundproofing.md`,
  `13_Surfaces_and_Finishes/Ceilings_Guide.md`, `Walls_and_Paint.md`;
  `11_Budget_and_Planning/analysis/Demolition.md` (extended, not
  duplicated); and the general store's `Rules_Heuristics.md` (3 new
  topic-area sections: generalist-vs-specialist labor/root-cause
  discipline, partition-tool-competency vetting, trade-specialization/
  undocumented-outlet rework case). All price figures normalized to USD
  via `tools/pricing/currency_converter.py`'s trailing-6-month average
  anchored to each video's own confirmed publish date, except the
  partition-material video's small material-only unit prices, where a
  USD conversion would have collapsed into the same rounding bucket for
  every material and was deliberately omitted in favor of the real RUB
  figures, per this project's own price-comparability rule.
  `tools/youtube/archive_transcripts.py` run (dry-run first, all 8
  matched correctly); all 8 source notes' bottom `[source: ...]` inline
  links needed the same manual fix as Rounds 5-8 (frontmatter
  `transcript_file:` auto-updated by the script, bottom link was not) —
  corrected by hand for all 8. All 8 new CSV rows independently
  re-verified via Python's `csv` module to parse into the correct 15
  columns each with `archived` status. `tools/verify_batch.py` to be run
  against the pre-round commit (`7d0f0d0`) before finishing.

## Round 10 — Bathroom/plumbing product selection, baseboard/flooring, electrical routing decision, radiator flood incident, wall/ceiling soundproofing frame technique (8 videos, dispatched 2026-08-24)

Continues full-scale processing, a fresh 8-video selection from the
341-video manifest (272 fresh/unprocessed at the start of this round),
favoring named-technique, real-problem-diagnosis, and product-selection
content over recap "ТОП-N ошибок," multi-apartment "экспресс-обзор," or
pure room-tour formats. Includes an explicit cross-check of video 2
against Round 8's faucet/plumbing-cabinet video, video 4 against
`Flooring_Guide.md`'s existing 5-material comparison, video 6 against
this channel's other flood incidents (towel-warmer, ventilation-defect),
and videos 7-8 against each other and against existing `Soundproofing.md`
content.

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `zZ_1iOXL_wA` | Как выбрать инсталляцию унитаза, душ, мебель для ванной. | Toilet-installation-frame, shower, bathroom-furniture selection | **PARTIAL extraction — title/format mismatch** | 8 | Single-brand premium trade-show/showroom interview (toilet installation frames, overhead shower systems, vanity furniture, linear drains), not a how-to-choose explainer — same sub-format as Round 9's tile-expo video. High promotional ratio; luxury EUR/RUB list pricing (≈€15,000 shower system, 30,000-400,000+ RUB furniture tiers) excluded per value-filter. Region unresolved (international trade fair). New: installation-frame load distribution independently corroborating the existing 400kg Kruglov/Ontario figure from a second brand, frame repair/warranty terms, tile-to-metal cold-crack risk, corner-mount bracket kit, in-bowl forced-ventilation-fan concept, three-tier linear-drain product ladder. |
| 2 | `fIicREPruVs` | Как выбрать смесители, поддоны, раковины, зеркала. Советы и ошибки. Выставка Mosbuild. | Faucets/shower-trays/sinks/mirrors at Mosbuild; explicit cross-check vs. Round 8 faucet/plumbing-cabinet video | **PARTIAL extraction — heavily ASR-garbled** | 5 | Multi-brand Mosbuild booth-hopping tour, high promotional ratio, several ASR-uncertain numbers deliberately excluded. **Explicitly cross-checked against Round 8's `D-DFsBMjlxQ`** — confirmed no overlap (that source is concealed plumbing-cabinet engineering; this is a retail-fixture showroom tour). Region unresolved. New: pre-sloped factory shower-pan product category, foldable shower seat, decorative radiator cover, heated anti-fog mirror, concealed-valve rough-in depth caution. |
| 3 | `cyV4ePfTtVg` | Как выбрать плинтус? Основные принципы и частые ошибки. | Baseboard/skirting-board selection, likely new sub-topic | **SKIPPED — no captions available** | 0 | Both `youtube-transcript-api` (subtitles disabled) and `yt-dlp` (no subtitle tracks for ru/en) failed, `reason_class: null` for both attempts — a genuine per-video no-captions failure, **not** a rate-limit/IP-block signature. Not fetched, not extracted. |
| 4 | `k9CrEU5RuIE` | Как выбрать напольное покрытие? Частые ошибки и главные принципы. | Flooring-selection principles; explicit cross-check vs. `Flooring_Guide.md`'s Round 3 5-material comparison | **FULL extraction — title/content mismatch, useful gap-filler** | 7 | Another Mosbuild expo tour (same co-host Ekaterina as video 2), brief flooring-material segment pivoting mostly to baseboard/tile-trim selection — **incidentally substitutes for video 3's gap** on baseboard content. Medium promotional ratio (one company-promotion segment excluded). **Explicitly checked against `Flooring_Guide.md`'s 5-material comparison — no overlap.** Region unresolved. New: carpet residential-use exclusion, cable-channel baseboard, Scandinavian white-baseboard product, tile-corner-trim thickness ladder, ⚠️ baseboard-width-to-expansion-gap coordination rule, pipe-riser escutcheon collars, two balcony budget wall-finish options. |
| 5 | `yyW9WaW3Pls` | Электромонтаж по полу или потолку? Как лучше и дешевле. Все за и против. Ремонт ЖК Аэробус. | Electrical wiring routing decision, not yet covered by this channel (Rounds 2/4/7/8/9) | **FULL extraction** | 10 | Real 117m², 4-room apartment, ЖК Аэробус. **Region level 2** (named development, no city spoken). Low promotional ratio. Full floor-vs-ceiling routing decision framework plus a rare real arithmetic-checkable worked cost comparison (≈62,000 RUB more expensive for full-ceiling vs. full-floor routing on this specific object). New: color-coded conduit convention, structural outlet-height reasoning, combined/hybrid routing rationale, conduit-to-screed fixing over floor soundproofing, junction-splice placement rule, flood-safety business-experience claim, counter-intuitive wire-non-replaceability-in-conduit caution. |
| 6 | `GLU9nJYrtbQ` | Потоп от радиатора! Что делать и кто виноват? ЖК Рассказово. | Real radiator-flood incident, liability determination; explicit cross-check vs. towel-warmer/ventilation-defect flood incidents | **FULL extraction — real incident case study** | 11 | Real active flood incident filmed 4 days after the fact, ЖК Рассказово. **Region level 2** (named development, no city spoken). Low promotional ratio. **Explicitly cross-checked against Round 4's towel-warmer demolition-accident incidents and Round 9's concealed-ventilation-valve defect — confirmed a genuinely distinct mechanism** (developer heating-fitting failure during active renovation, not demolition damage or a years-later concealed defect) and a new liability-determination mechanism (upper-vs-lower connection point dispute). New: two-pipe non-radial topology whole-apartment-shutoff flaw, fitting failure point, unbranded-pipe red flag, confirmed same-day multi-leak pattern in the development, structured 4-factor root-cause theory, 7-item preventive checklist. |
| 7 | `rEe5LHWj4fI` | Шумоизоляция стен в квартире. Каркас. Подробная видео инструкция. | Wall-soundproofing frame installation, detailed technique; cross-check vs. `Soundproofing.md` | **FULL extraction — first systematic soundproofing-installation source** | 14 | Detailed step-by-step wall-frame build, named ASTic/Acusti Group system (Vibrostek M, Connect PS, Шуманет Эко, триплекс/Soundline DB, Акулайн). Region unresolved. Medium promotional ratio (disclosed commercial affiliation). **Confirmed: the first genuinely systematic soundproofing-installation technique source on this vault** — existing `Soundproofing.md` content was taxonomy/comparison/case-mentions only. New: full material list, depth-budgeting worked example, hanger/profile spacing, two-screw QC rule, straightedge check, material-quality tell, insulation-density myth correction, board-orientation/staggered-seam rules, finishing technique. |
| 8 | `O4pGx8ESHDU` | Шумоизоляция потолка. Монтаж звукоизолирующего подвесного потолка. | Ceiling-soundproofing companion technique; cross-check vs. video 7 and `Soundproofing.md` | **FULL extraction — 4th level-1 region source** | 12 | Companion build, same system, very likely same real object. **Region level 1 direct** (city "Реутов" plus a specific address named). Medium promotional ratio (same disclosed affiliation, candidly notes premium pricing). **Explicitly cross-checked against video 7** — several steps corroborate/restate (staggered seams, texture tell, eco-wool caution, sealant technique), correctly not double-counted. Genuinely new: laser-level low-point datum procedure, **the decoupling mechanism made concrete (temporary removable perimeter anchors)** — the single most important mechanism-level fact in this pair, fastener substitution for soft walls, two-tier connector system with a real documented fit tradeoff, string-line leveling, hanger-type load differentiation, Акулайн weight spec, elevator-size logistics caution, load-test demo, insulation datasheet composition. |

**Status: COMPLETE — 7 of 8 videos fully fetched and processed (2 partial low-value/ASR-garbled passes on videos 1-2, 5 full extractions), 1 genuinely skipped for no captions (video 3), zero rate-limit issues.**

**Round 10 yield**: 7 videos processed (video 3 not fetched — no captions, excluded from the denominator), 67 genuinely-new facts (8+5+7+10+11+14+12, excluding duplicate/corroborating-only outcomes), yield = 9.6 new facts/video — **101% of Round 9's 9.5 baseline**, well above the 1.0/video floor. No stop-and-ask trigger.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 7 successful fetches were serialized one at a time with real spacing (achieved by interleaving each video's own full extraction/routing/CSV/archiving work between fetches — never an idle wait), consistent with every prior round's clean result on this channel. Video 3's failure was independently confirmed as a genuine no-captions case (`youtube-transcript-api`: "Subtitles are disabled for this video"; `yt-dlp`: no subtitle tracks for ru/en) — both attempts carried `"reason_class": null`, not the rate-limit/IP-block signature this project treats as a circuit breaker. Logged `status: skipped` with the specific reason, per the standing convention (not left pending, since this was a genuine per-video failure, not a block).

### Region-check finding, per this round's explicit brief

Region evidence again varied video to video, not a fixed channel answer, consistent with every prior round. Per-video: video 1 (unresolved — international trade fair), video 2 (unresolved — international trade fair), video 4 (unresolved — international trade fair), video 5 (level 2 — named development ЖК Аэробус, no city spoken), video 6 (level 2 — named development ЖК Рассказово, no city spoken), video 7 (unresolved — no city/development named, though very likely the same object as video 8), video 8 (**level 1 direct** — city "Реутов" plus a specific street address named). This round's trade-show cluster (videos 1, 2, 4) pushed the unresolved count higher than most prior rounds, while video 8 delivered this channel's 4th level-1-confirmed source overall (after Round 1's Нахимовский проспект, Round 3's two Moscow-named sources, Round 4's four level-1 sources, Round 6's two).

### Language check

No English-titled video was encountered this round — all 8 selected videos had Russian titles. All 7 successful fetches confirmed Russian spoken audio (`youtube-transcript-api` returned `language: ru` for every fetch).

### Cross-check findings, per this round's explicit brief

- **Video 2 (Mosbuild faucets/fixtures) vs. Round 8's `D-DFsBMjlxQ` (plumbing-cabinet/water-inlet-node walkthrough)**: explicitly checked, confirmed **no overlap** — that source covers concealed plumbing-cabinet engineering (filters, pressure, meters); this one is a retail-fixture showroom tour (shower pans, seats, mirrors, sinks, radiator covers), a genuinely different sub-topic.
- **Video 4 (flooring/baseboard) vs. `Flooring_Guide.md`'s Round 3 5-material comparison (`96mlkQoczI4`)**: explicitly checked, confirmed **no overlap** on the flooring-material content itself (this video's flooring-material segment is brief and only adds the carpet-exclusion note); the video's real value turned out to be its baseboard/tile-trim content instead, which incidentally, partially fills the gap left by video 3's no-captions failure.
- **Video 6 (radiator flood) vs. Round 4's towel-warmer demolition-accident incidents and Round 9's concealed-ventilation-valve defect**: explicitly checked, confirmed a **genuinely distinct mechanism** — a developer heating-fitting failure during active renovation (not demolition-crew damage or a years-later concealed defect) — and a new liability-determination angle (which specific connection point failed, and was that the one anyone actually worked on) not present in either prior incident.
- **Videos 7-8 (wall/ceiling soundproofing) vs. each other and vs. existing `Soundproofing.md` content**: explicitly cross-checked as instructed. Confirmed the same underlying acoustic principles (perimeter damper tape, vibro-hanger decoupling, staggered seams, named ASTic/Acusti Group materials) applied consistently to two different surfaces, with several steps genuinely restated between them (correctly not double-counted in video 8's tally) and several genuinely surface-specific additions in each (wall: depth-budgeting from the most protruding point; ceiling: laser-level low-point datum, two-tier connector grid). **Confirmed this is the first genuinely systematic soundproofing-installation technique source on this vault**, as opposed to the existing dB-figure/product-comparison content already there — and surfaced the single most important mechanism-level addition of the round: the *temporary, removable* perimeter track anchoring that's the actual construction step behind "vibration-damping hangers interrupt structural noise transfer," a mechanism this page previously described only abstractly.

## Progress Log

- 2026-08-24 — **Round 10 complete.** All 7 fetchable videos fetched
  serialized one at a time with real spacing (interleaved with each
  video's own full extraction/routing/CSV/archiving work), zero
  rate-limit issues across the entire round. Video 3 (baseboard
  selection) hit a genuine no-captions failure (confirmed via both
  `youtube-transcript-api` and `yt-dlp` failure reason classes — neither
  was rate-limit-related), logged `status: skipped` with the specific
  reason. 5 full extractions + 2 partial low-value/ASR-garbled passes
  (videos 1-2, both single-brand/multi-brand trade-show tours). Yield 67
  new facts / 7 processed videos = 9.6 facts/video — 101% of Round 9's
  9.5 baseline, well above the 1.0 floor — no stop-and-ask trigger.
  Region checked explicitly per video: 3 unresolved (the trade-show
  cluster), 2 at level 2 (both named developments), 1 unresolved despite
  being very likely the same object as a level-1 source, and video 8
  cleared level 1 directly (city "Реутов" plus a specific address) — this
  channel's 4th level-1-confirmed round-level source. Language checked —
  no English-titled videos this round, all 7 fetches confirmed Russian
  audio. Four explicit cross-checks performed as instructed (see the
  dedicated finding section above): video 2 vs. Round 8's faucet/
  plumbing-cabinet video (no overlap, different sub-topic); video 4 vs.
  Round 3's 5-material flooring comparison (no overlap; video 4's real
  value was baseboard content instead, incidentally filling video 3's
  gap); video 6 vs. Round 4's towel-warmer incidents and Round 9's
  ventilation-valve defect (genuinely distinct mechanism and a new
  liability-determination angle); and videos 7-8 vs. each other and vs.
  existing `Soundproofing.md` content (confirmed the first genuinely
  systematic soundproofing-installation source on this vault, and
  surfaced the round's single most important mechanism-level finding —
  the temporary/removable perimeter-anchor technique that concretely
  achieves frame-system acoustic decoupling). Content routed to
  `12_Engineering_and_Systems/analysis/Wall_Hung_Toilet_Installation.md`,
  `Rough_Electrical_Sequencing.md`, `Radiators_and_Convectors.md` (2 new
  sections: decorative covers, the real flood incident);
  `07_Bathroom/analysis/Bathtub_and_Shower.md` (2 new sections),
  `Fixtures_Mixers_and_Sinks.md`; `08_WC/WC_Guide.md` (toilet-bowl
  ventilation-fan concept); `13_Surfaces_and_Finishes/Flooring_Guide.md`
  (carpet exclusion, full baseboard-selection section),
  `analysis/Soundproofing.md` (a major new full-installation-technique
  section covering both wall and ceiling builds); `10_Balcony/Balcony_Index.md`
  (2 budget wall-finish options); and `11_Budget_and_Planning/analysis/Demolition.md`
  (a cross-reference to the new radiator-flood incident, distinguishing
  it from the existing towel-warmer mechanism). All 7 processed
  transcripts archived via `tools/youtube/archive_transcripts.py`
  (dry-run first, all 7 matched correctly) — no manual `[source: ...]`
  link fixes were needed this round (all note filenames already matched
  the archived-transcript slugs the script produced). All CSV rows (5
  `archived` + 2 `archived` partial + 1 `skipped`) independently
  re-verified via Python's `csv` module to parse into the correct 15
  columns. `tools/verify_batch.py` run against the pre-round commit
  (`21207c7`) — passed clean on the first run, no mojibake, BOM,
  retired-pattern, ID-drift, rounding-bucket, or arithmetic-plausibility
  problems found.

## Round 11 — Decorative plastering/paint, string-beacon method, combined plastering+electrical, screed QC, ZIPS-panel soundproofing, cork flooring, non-standard case studies (8 videos, dispatched 2026-08-24)

Continues full-scale processing, a fresh 8-video selection from the
341-video manifest, favoring named-technique content over recap
"ТОП-N ошибок," multi-apartment "экспресс-обзор," or pure room-tour
formats. Deliberately excludes the channel's separate "Ремонт по
проекту Алексея Земскова" cluster per this plan's standing note.
Includes an explicit cross-check of video 2 against Rounds 1/2/3/6
beacon/plastering content, and video 5 against Round 10's frame-system
soundproofing mechanism.

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `P55P5i3OFbI` | Как выбрать краску? Мастер-класс по нанесению декоративной штукатурки. | Paint selection + decorative-plaster masterclass | **SKIPPED — no captions available** | 0 | Both `youtube-transcript-api` (subtitles disabled) and `yt-dlp` (no subtitle tracks for ru/en) failed, `reason_class: null` for both attempts — a genuine per-video no-captions failure, **not** a rate-limit/IP-block signature. Not fetched, not extracted. |
| 2 | `xoLGoOIRMlc` | Новый секретный метод быстрой установки маяков своими руками // Штукатурка по струнным маякам. | String-beacon ("струнные маяки") fast-installation method; explicit cross-check vs. Rounds 1/2/3/6 beacon content | **FULL extraction** | 10 | 2018-vintage source. Cross-check confirmed genuinely distinct from every rigid-strip-beacon method already on `Waterproofing_and_Plastering.md` — a tensioned wire between corner brackets, not a physical strip beacon. New: corner-bracket+wire mechanism, tapered-wedge fine adjustment, real measured wall-deviation example, mid-span 40-minute partial-set anchoring, 7cm mesh-reinforcement threshold, explicit scope limitation (short walls/openings still use rigid beacons), laser-level self-verification anecdote, string-mistaken-for-debris site risk. Region level 2. Low promotional ratio. |
| 3 | `VqrXg-tDRO8` | Как штукатурить и делать электромонтаж? Секреты ремонта от мастеров. | Combined plastering + electrical-wiring technique/sequencing secrets | **PARTIAL extraction — heavily ASR-degraded, title/content mismatch** | 6 | 2018-vintage source. A scattered practitioner Q&A, not a structured tutorial as titled. New: гофра black-vs-gray fire-behavior nuance + low real-world ignition-risk clarification, self-conducted burn-test comparing standard cable vs. already-standard ВВГнг-LS, conditional-value long-trowel technique with an explicit don't-use-on-flat-walls warning, post-plastering humidity trade-sequencing bottleneck + dehumidifier mitigation, tool-ownership/no-policing management philosophy. Region unresolved. Low promotional ratio. |
| 4 | `gREGOOA2OHo` | А полы то ровные? Проверяем стяжку и отделку квартиры! | Floor/screed-evenness QC-check technique, real-object inspection | **FULL extraction** | 14 | 2017-vintage source (oldest of the round at fetch time). **Region level 1** — "Новая Рига" highway corridor named directly. Real semi-dry-screed QC finding one month post-pour (doorway-transition-bump generalization), masonry-built shower base + Neptun leak-protection component list, real shower tile dimensions, tile-height convention + tile-to-paint flush-plane drywall-buildup technique, engineered-board no-plywood detail, cost-saving untiled-behind-fridge decision, pre-install-backing-ahead-of-pending-design-decision sequencing lesson, and a real running project-cost-tracking update (680,000 RUB + 208,000 RUB client installment) — explicitly kept separate from this project's completed-object benchmark series as an in-progress total. Low promotional ratio. |
| 5 | `hrhJ6Y8hhPU` | Шумоизоляция стен ЗИПС панелями. Советы от профессионалов. | Wall soundproofing with ZIPS panels; explicit cross-check vs. Round 10's frame-system mechanism | **FULL extraction, densest video this round** | 15 | 2016-vintage source — oldest processed on this channel to date, required a one-time USD/RUB 2016 backfill (`fetch_exchange_rates.py --backfill --start-year 2016`). **Region level 1** — "Одинцовский район, посёлок Ромашково" named directly, plus a residential complex and unit number. **Cross-check confirmed a genuinely distinct installation approach from Round 10's frame system** — a rigid factory panel with silicone-filled fastening nodes screwed directly to the wall, no air-gap hanger frame — sharing only the underlying decoupling principle and the manufacturer (Acoustic Group). New: full panel construction, real 2,500 RUB/m² (≈$40/m²) cost figure, perimeter damper-tape prep, excess-silicone mistake warning, layout/cutting technique, socket-drilling soundproofing-breach warning, foam-block fastener-substitution finding, utility-avoidance marking, fastening-depth QC, 25cm-minimum row-offset rule, counter-intuitive do-not-over-fasten rule, substrate-flatness tolerance, pre-drywall QC pass, practitioner pros/cons summary. Medium promotional ratio (disclosed manufacturer-training relationship). |
| 6 | `4O1UqRqpApw` | Пробковый пол. Технология укладки от профессионалов. | Cork-flooring installation technology, a material not yet covered | **FULL extraction — first cork-specific source on `Flooring_Guide.md`** | 9 | 2016-vintage source. New: real product ID (Maestro Club Ronda), 3m-straightedge/2-3mm flatness spec (a second data point vs. the existing 2m/2mm Zemskov rule), priming dust-sealing rationale, PVC vapor-barrier film step with a cork-specific rough-screed-isolation benefit, last-board-width-under-5cm first-row-split planning rule, 4-5mm minimum thermal-expansion-gap figure (a second data point vs. the existing 8-12mm typically-executed baseboard-coordination figure, not a contradiction), spacer-wedge technique, joint sealant technique, 15-20cm minimum seam-offset rule. Acclimation duration corroborated an existing rule, not re-counted. Region level 2. Low promotional ratio. |
| 7 | `Tq2IELynaGs` | Ремонт в новостройке. Нестандартные решения по электрике и сантехнике. Часть 4. | Non-standard electrical/plumbing solutions, real-object technique | **FULL extraction, likely same real project as video 4** | 11 | 2017-vintage source, ~2 weeks before video 4's own date, same client name (Максим) and a lower running-cost total — flagged as a probable (not certain) earlier installment of the same evolving project. New: wall-thickness value-engineering (28cm→15-16cm via reinforced curved drywall), bathroom partition rebuild freeing space while adding soundproofing (90cm→1.36m), client-driven angled-wall layout tweak, plywood-reinforced-drywall future-mounting technique, work-zone window-addition rationale, ceiling-to-corridor-cabinet water rerouting + PEX-A upgrade, heating-manifold consolidation, window-reveal outlet placement (crew's own stated skepticism), bedroom lighting-circuit plan, and a separate real running-cost update (370,815+38,400 RUB spend, 267,623 RUB act #1, 500,000 RUB client payment, 90,000 RUB foreman balance). Region level 2 for this specific video. Low promotional ratio. |
| 8 | `QginFVl00Hw` | Нестандартный санузел с панорамными окнами. ЖК Видное | Non-standard bathroom with panoramic windows, real-object design/technique case | **FULL extraction, ⚠️ unusually strong region-1 signature** | 11 | 2017-vintage source. **Region level 1** — full address spoken directly ("город Видное, улица Завидная, дом 10"), stronger than this channel's usual single-element level-1 signature. New: large-bathroom-window privacy fixes, a novel curved/radius-wall beacon fabrication technique (bent metal-plastic pipe wired to screws, packed with plaster) genuinely distinct from every straight-wall beacon method on this channel, mosaic-layout precision + named materials, a water-hammer-compensator placement dispute candidly presented as still open (resolved by calling the official dealer), bathtub-podium distance-to-drain rationale, site-protection practice, washer/dryer drain prep, drywall-to-stretch-ceiling L-joint curtain-niche detail. Towel-warmer electric-over-hydronic recommendation corroborated an existing well-sourced stance, not re-counted. Low promotional ratio. |

**Status: COMPLETE — 7 of 8 videos fully fetched and processed (6 full extractions, 1 partial low-value/ASR-degraded pass on video 3), 1 genuinely skipped for no captions (video 1), zero rate-limit issues.**

**Round 11 yield**: 7 videos processed (video 1 not fetched — no captions, excluded from the denominator), 76 genuinely-new facts (10+6+14+15+9+11+11, excluding duplicate/corroborating-only outcomes), yield = 10.9 new facts/video — **114% of Round 10's 9.6 baseline**, well above the 1.0/video floor. No stop-and-ask trigger.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 7 successful fetches were serialized one at a time with real spacing (achieved by interleaving each video's own full extraction/routing/CSV/archiving work between fetches — never an idle wait), consistent with every prior round's clean result on this channel. Video 1's failure was independently confirmed as a genuine no-captions case (`youtube-transcript-api`: "Subtitles are disabled for this video"; `yt-dlp`: no subtitle tracks for ru/en) — both attempts carried `"reason_class": null`, not the rate-limit/IP-block signature this project treats as a circuit breaker. Logged `status: skipped` with the specific reason, per the standing convention.

### An unusually old cluster of sources this round

Three of this round's sources (videos 2, 3: 2018; video 4: 2017; videos 5, 7, 8: 2016-2017) turned out far older than every source processed on this channel in Rounds 1-10 (all 2022+), making video 5 (2016-10-13) the oldest source processed on this channel to date. This required a one-time USD/RUB exchange-rate backfill for calendar year 2016 (`tools/pricing/fetch_exchange_rates.py --backfill --start-year 2016`, then `generate_exchange_rates_reference.py`) before video 5's real cost figure could be converted — done this session per this project's missing-year rule. The regenerated reference table's confirmed-row floor did not pick up a 2016 row (the generator appears to floor at 2017), but the underlying daily-rate database now holds full 2016 coverage, and `currency_converter.py`'s trailing-6-month lookup against that database worked correctly regardless — this project's own guidance already treats direct `currency_converter.py` lookups as the primary path and the reference table as a fallback, so this is not a blocking gap, only noted for anyone who expects to see 2016 listed in the table itself.

### Region-check finding, per this round's explicit brief

Region evidence again varied video to video, not a fixed channel answer, consistent with every prior round. Per-video: video 2 (level 2), video 3 (unresolved — no location named), video 4 (**level 1** — "Новая Рига" highway corridor), video 5 (**level 1** — Одинцовский район/посёлок Ромашково), video 6 (level 2), video 7 (level 2 for this specific video, though likely the same real project as video 4's level-1 object), video 8 (**level 1**, an unusually strong signature — full city+street+house-number address spoken directly). 3 of 7 fetched videos cleared level 1 directly this round, continuing this channel's pattern of level-1 evidence varying substantially round to round rather than following any fixed rule.

### Language check

No English-titled video was encountered this round — all 8 selected videos had Russian titles. All 7 successful fetches confirmed Russian spoken audio (`youtube-transcript-api` returned `language: ru` for every fetch, all `is_generated_captions: true`).

### Beacon-method cross-check (video 2), per this round's explicit brief

**Confirmed genuinely distinct, not a restatement.** Every prior beacon source on this channel (Rounds 1, 2, 3, 6 — `D1REgSDwILU`, `r1eyXzXNdI0`, `mb-2ll0UtTo`, the laser-level rigid-strip content) describes a **physical metal strip beacon** set with plaster dabs. Video 2's "струнные маяки" method instead uses a **tensioned wire strung between two wall-mounted corner brackets** as the plastering reference line — a structurally distinct approach, not a variant of the rigid-beacon technique. The practitioner himself frames it as a complementary method for long, straight wall runs specifically, not a universal replacement — short walls and door-opening returns still use the existing rigid-beacon technique. Recorded on `Waterproofing_and_Plastering.md` as a new, separate section rather than merged into the existing beacon content.

### ZIPS-panel soundproofing cross-check (video 5), per this round's explicit brief

**Confirmed a genuinely distinct installation approach from Round 10's frame system, sharing only the underlying decoupling principle and manufacturer.** Round 10's wall/ceiling frame system (`rEe5LHWj4fI`/`O4pGx8ESHDU`) builds a free-standing metal-profile frame off vibration-damping hangers, decoupled from structure via temporary/removable perimeter anchors, with an air-gap cavity behind the finish board. Video 5's ZIPS panel system is instead a **rigid, factory-made sandwich panel screwed directly to the wall** through silicone-filled fastening nodes built into the panel itself — the decoupling element lives inside each fastening point, not in a separate hanger/bracket assembly, and there's no air-gap cavity. Both use a comparable perimeter damper tape and the same dense finish-drywall product (Акулайн) for mass-loading, and both trace back to the same manufacturer (Acoustic Group) — but they are genuinely two different products/methods, not two applications of one method. Recorded on `Soundproofing.md` as its own section, with the cross-check finding stated explicitly inline.

### Same-project likely-link finding (videos 4 and 7), not explicitly requested but surfaced during extraction

Videos 4 and 7 share a client name (Максим), a running-materials-cost-table format, and upload dates only ~2 weeks apart (video 7: 2017-09-18; video 4: 2017-10-01), with video 7's lower running total (370,815 RUB) consistent with being an earlier installment of the same evolving project video 4 continues. **Not confirmed as certain** — neither video's own transcript names or cross-references the other — but recorded as a probable link in both source notes and both `Budgeting_Guide.md` entries, kept as two separate running-cost data points rather than merged or assumed identical.

## Progress Log

- 2026-08-24 — **Round 11 complete.** All 7 fetchable videos fetched
  serialized one at a time with real spacing (interleaved with each
  video's own full extraction/routing/CSV/archiving work), zero
  rate-limit issues across the entire round. Video 1 (paint/decorative-
  plaster masterclass) hit a genuine no-captions failure (confirmed via
  both `youtube-transcript-api` and `yt-dlp` failure reason classes —
  neither rate-limit-related), logged `status: skipped` with the
  specific reason. 6 full extractions + 1 partial low-value/ASR-degraded
  pass (video 3). Yield 76 new facts / 7 processed videos = 10.9
  facts/video — 114% of Round 10's 9.6 baseline, well above the 1.0
  floor — no stop-and-ask trigger. Region checked explicitly per video:
  3 of 7 cleared level 1 directly (videos 4, 5, 8 — including video 8's
  unusually strong full-address signature), 3 stayed at level 2, 1
  unresolved. Language checked — no English-titled videos this round,
  all 7 fetches confirmed Russian audio. Two explicit cross-checks
  performed as instructed (see the dedicated finding sections above):
  video 2's string-beacon method vs. Rounds 1/2/3/6 rigid-beacon content
  (confirmed genuinely distinct installation approach); video 5's ZIPS
  panel system vs. Round 10's frame system (confirmed genuinely distinct
  approach sharing only the underlying decoupling principle and
  manufacturer). An unrequested but real same-project likely-link was
  also surfaced between videos 4 and 7 (see dedicated section above).
  This round's sources turned out unusually old (2016-2018, vs. 2022+ for
  every prior round on this channel), requiring a one-time 2016 USD/RUB
  exchange-rate backfill. Content routed to
  `12_Engineering_and_Systems/analysis/Waterproofing_and_Plastering.md`
  (string-beacon method, curved-wall beacon technique, trowel technique +
  drying bottleneck), `Cable_Circuits_and_Panel_Design.md` (гофра
  fire-behavior + cable burn test), `Soundproofing.md` (ZIPS panel
  system, a major new section), `Water_Inlet_Node_Components.md` (water
  rerouting/manifold consolidation, water-hammer-compensator dispute);
  `07_Bathroom/analysis/Bathtub_and_Shower.md`, `Tile_Selection_and_
  Layout.md` (2 sections), `Structure_and_Framing.md`, `Planning_and_
  Layout.md`; `13_Surfaces_and_Finishes/Flooring_Guide.md` (first
  cork-specific section), `Ceilings_Guide.md` (curtain-niche detail);
  `11_Budget_and_Planning/Budgeting_Guide.md` (2 new running-cost-
  tracking data points) and the general store's `Rules_Heuristics.md`
  (tool-ownership philosophy, real-project value-engineering/design-
  skepticism notes). All 7 processed transcripts archived via
  `tools/youtube/archive_transcripts.py` (dry-run first, all 7 matched
  correctly) — all 7 source notes' bottom `[source: ...]` inline links
  needed the same manual fix as Rounds 5-10 (frontmatter
  `transcript_file:` auto-updated by the script, bottom link was not) —
  corrected by hand for all 7. All CSV rows (6 `archived` full + 1
  `archived` partial + 1 `skipped`) independently re-verified via
  Python's `csv` module to parse into the correct 15 columns.
  `tools/verify_batch.py` to be run against the pre-round commit
  (`72c434c`) before finishing.

## Round 12 — Short TV-format technique clips, wallpaper/plumbing/soundproofing material specifics, radiator freeze-burst, Виноградный episodic-series spot-check (8 videos, dispatched 2026-08-24)

Continues full-scale processing, a fresh 8-video selection from the
341-video manifest for topic diversity, deliberately avoiding the
"Ремонт по проекту Алексея Земскова" cluster and the "Отзыв №N"
client-testimonial cluster per this plan's standing notes. Includes an
explicit cross-check of video 5 (radiator burst) against this channel's
three other flood incidents, video 7 (Шумопласт) against Round 6's
existing Шумопласт section, and a deliberate first-touch spot-check of
the older numbered "ЖК Виноградный" episodic series (video 8).

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `szIzrJJMm4o` | Как защитить межплиточные швы? Телеканал «Бобёр». | Short TV-format tile-grout-protection technique | **FULL extraction** | 2 | Confirmed via `yt-dlp` uploader metadata to be uploaded directly by the Petrishin-Stroi channel itself, not a third-party "Бобёр" TV re-upload. 2016-04-20 upload date. New grout-joint water/mold-protection sealant technique, genuinely new to `Tile_Selection_and_Layout.md`. Region level 2. Low promotional ratio. |
| 2 | `VZk4615VM6I` | Установка дверного порожка. Телеканал «Бобёр». | Short TV-format door-threshold-installation technique | **FULL extraction** | 4 | Same-day/same-series pair with video 1 (identical 2016-04-20 upload date, same channel uploader). Removable T-molding transition-threshold three-part construction technique — new to `Flooring_Guide.md`. Region level 2. Low promotional ratio. |
| 3 | `MTKwKUx0Nnc` | Как покрасить обои. Секреты от профессионалов. | Painting-over-wallpaper technique | **SKIPPED — no captions available** | 0 | Both `youtube-transcript-api` (subtitles disabled) and `yt-dlp` (no ru/en subtitle tracks) failed, `reason_class: null` for both — a genuine no-captions failure, not a rate-limit signature. Not fetched, not extracted. |
| 4 | `ot7qPVf7XVU` | Как клеить флизелиновые обои | Non-woven ("флизелиновые") wallpaper-hanging technique, explicit cross-check vs. Round 9 wallpaper Q&A | **FULL extraction** | 9 | Real jobsite demo, brand "Patent Decor" named. **Explicitly cross-checked against Round 2's acceptance checklist (`VcrYHkDgb0o`) and Round 9's 17-question Q&A (`NyIj6h8hZHw`) — confirmed no overlap**, first hands-on gluing/hanging-sequence walkthrough for non-woven wallpaper on this page. New: priming-mandatory-but-often-skipped rule, paintable-non-woven-specific 4.5L glue ratio, ⚠️ glue-on-wall-only-vs-vinyl-both-sides material distinction, knife-parallel-to-wall trim technique, waffle-cloth cleanup, seam-over-window/door placement rule, draft warning. Region level 2. Low promotional ratio. |
| 5 | `oA6gABulhJk` | ЧП (чрезвычайное происшествие). Прорвало батарею! | Real radiator-burst emergency incident, explicit cross-check vs. this channel's other flood incidents | **FULL extraction — genuinely distinct 4th mechanism** | 9 | Real incident, filmed on-site day-of/day-after. **Explicitly cross-checked against Round 4's towel-warmer demolition damage, Round 9's concealed-ventilation-valve defect, and Round 10's radiator-fitting failure — confirmed a genuinely distinct 4th mechanism**: a freeze-burst from a management-company multi-unit heating shutoff combined with a window left open for post-plaster drying, not demolition damage, concealment, or a single fitting failure. **Region: level 1** (a real city named directly, ASR-uncertain exact spelling). New: management-company diagnostic-failure pattern, real ~1-1.5L incident scale, diagnostic sequence, and a **positive-case corroboration of Round 10's radial-piping recommendation from the opposite direction** (this apartment's radial wiring let the crew isolate just the one burst radiator). Low promotional ratio. |
| 6 | `vv4Wav4S7dY` | Сантехнические работы полипропиленом | Polypropylene-pipe plumbing technique | **SKIPPED — no captions available** | 0 | Both `youtube-transcript-api` (subtitles disabled) and `yt-dlp` (no ru/en subtitle tracks) failed, `reason_class: null` for both — a genuine no-captions failure, not a rate-limit signature. Not fetched, not extracted. |
| 7 | `ar4HNfWjzh4` | Шумоизоляция пола "Шумопласт". Советы от профессионалов. Петришин Строй | Шумопласт floor-soundproofing deep dive, explicit cross-check vs. Round 6's existing Шумопласт section | **FULL extraction** | 9 | Real object, Одинцовский район/Ромашково — **same district/settlement and same named crew (Валера/Ваня/Коля) as Round 11's ZIPS-panel video**, likely the same real job. **Explicitly cross-checked against Round 6's existing Шумопласт section — confirmed only partial originating-source status**: Round 6's source was already independently detailed (composition, -28dB figure, application technique, all-in cost); this video adds the manufacturer's own engineering-album spec sheet (80mm total buildup), a second product-selection criterion (utility-line density, additive to Round 6's substrate-unevenness criterion), a critical beacon-must-not-penetrate rule, and a material-only cost breakdown distinct from Round 6's all-in figure. Region level 1. Medium promotional ratio. |
| 8 | `l4bXbwfOlrU` | Эпизод 7. Сантехнические работы. ЖК Виноградный. Ремонт квартиры онлайн. | First-touch spot-check of the older numbered "ЖК Виноградный" episodic series (~13 episodes) | **FULL extraction, explicit series-worth verdict recorded** | 10 | Oldest source processed on this channel to date (2015-12-28 confirmed via `yt-dlp`). **Explicitly checked against existing `Water_Inlet_Node_Components.md` — confirmed heavy overlap** on the general inlet-node component sequence (already densely corroborated from 5+ other sources), correctly excluded from the fact count; genuinely new: Honeywell glass-vs-metal filter/reducer material distinction, Geberit frame-anchoring detail, leak-protection trigger scenarios, and a genuinely new **real cable-under-straightedge floor-squeak demonstration mechanism**, routed to `Flooring_Guide.md`. **Verdict: worth a further small spot-check (2-3 later episodes, structural/finishing stages) before committing to the full ~13-episode series** — this episode's plumbing content was more heavily pre-covered ground than a first-touch episode ideally would be. Region level 2. Low promotional ratio. |

**Status: COMPLETE — 6 of 8 videos fully fetched and extracted, 2 genuinely skipped for no captions, zero rate-limit issues.**

**Round 12 yield**: 6 videos processed (videos 3 and 6 not fetched — no captions, excluded from the denominator), 43 genuinely-new facts (2+4+9+9+9+10, excluding duplicate/corroborating-only outcomes), yield = 7.2 new facts/video — **66% of Round 11's 10.9 baseline** (within the >50%-drop stop-and-ask threshold, and well above the 1.0/video floor). No stop-and-ask trigger.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 6 successful fetches were serialized one at a time with real spacing (achieved by interleaving each video's own full extraction/routing/CSV/archiving work between fetches — never an idle wait), consistent with every prior round's clean result on this channel. Both no-captions failures (videos 3, 6) were independently confirmed as genuine per-video failures (`youtube-transcript-api`: "Subtitles are disabled for this video"; `yt-dlp`: no subtitle tracks for ru/en; `reason_class: null` for both attempts in both cases) — not the rate-limit/IP-block signature this project treats as a circuit breaker. Both logged `status: skipped` with the specific reason.

### Region-check finding, per this round's explicit brief

Region evidence again varied video to video, not a fixed channel answer, consistent with every prior round. Per-video: video 1 (level 2), video 2 (level 2), video 4 (level 2), video 5 (**level 1** — a real city named directly, ASR-uncertain exact spelling), video 7 (**level 1** — "Одинцовский район... деревня Ромашково" named directly, same location as Round 11's ZIPS video), video 8 (level 2 — named development, no city spoken). 2 of 6 fetched videos cleared level 1 directly this round.

### Language check

No English-titled video was encountered this round — all 8 selected videos had Russian titles. All 6 successful fetches confirmed Russian spoken audio (`youtube-transcript-api` returned `language: ru` for every fetch).

### Radiator freeze-burst cross-check (video 5), per this round's explicit brief

**Confirmed a genuinely distinct, fourth flood/burst mechanism on this channel.** Round 4's incidents are demolition-crew physical damage to an existing towel-warmer pipe; Round 9's is a years-later concealed shared-ventilation-valve defect; Round 10's is a developer-installed heating-fitting/gasket failure at a specific connection point with a liability dispute. This video's mechanism is environmental/interruption-driven: a management company cut heating to multiple apartments in response to an unrelated leak elsewhere, without diagnosing which unit was actually affected; this apartment's own window had been left cracked for post-plaster drying, and the resulting cold-plus-no-heat condition froze the radiator's water column, bursting both its top and bottom gaskets simultaneously. **A genuinely valuable secondary finding**: this apartment's radial ("лучевая") piping topology let the crew isolate and shut off only the burst radiator, keeping the other three fully functional — a positive-case corroboration, from the opposite direction, of Round 10's implied recommendation that non-radial topology is a liability. Recorded on `Radiators_and_Convectors.md` and cross-referenced from `Demolition.md`'s flood-incident cluster.

### Шумопласт cross-check (video 7), per this round's explicit brief

**Confirmed partial, not full, originating-source status.** Round 6's existing Шумопласт section (`c4mmaLAsDw4`) was already independently detailed — composition, manufacturer dB figures, application technique, cure protocol, and an all-in installed cost. This video adds real manufacturer engineering-album data (an 80mm total floor-buildup spec: 20mm Шумопласт + 60mm minimum screed) plus a second, additive product-selection criterion (utility-line density under the floor, distinct from Round 6's substrate-unevenness criterion), a critical beacon-must-not-penetrate-the-material rule, and a material-only cost breakdown (≈275-300 RUB/m²) kept explicitly separate from Round 6's all-in ≈$80-90/m² figure since the two are non-comparable cost bases. One manufacturer figure (an airborne-noise index ASR-rendered as "79dB") was flagged `ASR-uncertain` and treated as a likely digit-merge of the existing -7-9dB figure rather than adopted as a new, higher number. This video's location (Одинцовский район/Ромашково) and named crew (Валера/Ваня/Коля) match Round 11's ZIPS-panel video exactly, strongly suggesting the same real job across both soundproofing-method sources.

### Виноградный episodic-series spot-check (video 8), per this round's explicit brief

**Explicit verdict: worth a further small spot-check before committing to the full series, not yet a full-round commitment.** This first-touch episode (plumbing rough-in, episode 7 of ~13) delivered one genuinely new, physically-demonstrated mechanism (the cable-under-straightedge floor-squeak demo) and several brand-specific installation details (Honeywell, Geberit), but roughly two-thirds of its inlet-node-component content was a straightforward restatement of the sequence this vault already has densely corroborated from five other sources. The format looks structurally comparable to Kruglov/Sidorik's own numbered episodic series (which performed well on this project), but this specific episode's subject (plumbing) happened to be unusually pre-covered ground for a first-touch episode. **Recommendation for a future round**: sample 2-3 later episodes covering structural/electrical/finishing stages (this episode's own forward reference points to a drywall-construction episode next) before deciding on the full ~13-episode series.

## Progress Log

- 2026-08-24 — **Round 12 complete.** 6 of 8 videos fetched serialized one
  at a time with real spacing (interleaved with each video's own full
  extraction/routing/CSV/archiving work), zero rate-limit issues across
  the entire round. Videos 3 and 6 hit genuine no-captions failures
  (confirmed via both `youtube-transcript-api` and `yt-dlp` failure
  reason classes — neither rate-limit-related), logged `status: skipped`
  with the specific reason. All 6 fetched videos fully extracted. Yield
  43 new facts / 6 processed videos = 7.2 facts/video — 66% of Round 11's
  10.9 baseline, well above the 1.0 floor and not a >50% drop — no
  stop-and-ask trigger. Region checked explicitly per video: 2 of 6
  cleared level 1 directly (videos 5, 7), 4 stayed at level 2. Language
  checked — no English-titled videos this round, all 6 fetches confirmed
  Russian audio. Three explicit cross-checks performed as instructed (see
  the dedicated finding sections above): video 5 (radiator freeze-burst)
  against this channel's three other flood incidents — confirmed a
  genuinely distinct fourth mechanism plus a positive-case radial-piping
  corroboration; video 7 (Шумопласт) against Round 6's existing section —
  confirmed partial (not full) originating-source status, with new
  manufacturer spec-sheet data and a second product-selection criterion;
  and video 8 (Виноградный episode 7) against `Water_Inlet_Node_
  Components.md` — confirmed heavy overlap correctly excluded, with an
  explicit series-worth verdict recorded (spot-check further before
  committing to the full series). Videos 1-2 were also confirmed, via
  `yt-dlp` uploader metadata, to be genuine same-channel same-day content
  rather than third-party "Бобёр" TV re-uploads. Content routed to
  `07_Bathroom/analysis/Tile_Selection_and_Layout.md` (grout-protection
  technique), `13_Surfaces_and_Finishes/Flooring_Guide.md` (T-molding
  threshold technique, cable-under-straightedge demo mechanism),
  `13_Surfaces_and_Finishes/Walls_and_Paint.md` (non-woven wallpaper
  hanging technique), `12_Engineering_and_Systems/analysis/
  Radiators_and_Convectors.md` (freeze-burst incident), `12_Engineering_
  and_Systems/analysis/Soundproofing.md` (Шумопласт spec-sheet
  extension), `12_Engineering_and_Systems/analysis/
  Water_Inlet_Node_Components.md` (brand-specific filter/frame detail),
  and `11_Budget_and_Planning/analysis/Demolition.md` (cross-reference to
  the new freeze-burst mechanism). All 6 processed transcripts archived
  via `tools/youtube/archive_transcripts.py` (dry-run first, all 6
  matched correctly) — 2 of the 6 source notes' bottom `[source: ...]`
  inline links needed the same manual fix as Rounds 5-11 (frontmatter
  `transcript_file:` auto-updated by the script, bottom link was not) —
  corrected by hand for both (`oA6gABulhJk`, `ar4HNfWjzh4`, both renamed
  by the archive script to match their source notes' own filename slugs).
  All CSV rows (6 `archived` + 2 `skipped`) independently re-verified via
  Python's `csv` module to parse into the correct 15 columns.
  `tools/verify_batch.py` run against the pre-round commit (`6ce34d8`) —
  passed clean on the first run, no mojibake, BOM, retired-pattern,
  ID-drift, rounding-bucket, or arithmetic-plausibility problems found.

## Round 13 — Vinogradny series spot-check (3 more episodes), third-party TV segments, kitchen case studies (8 videos, dispatched 2026-08-24)

Deliberately curated to resolve two specific open questions rather than
sample the channel's default mix: (1) whether the older "ЖК Виноградный"
episodic series (2016-17, ~13 episodes, only episode 7 touched so far in
Round 12) is worth committing to as a full series, via 3 more episodes
(5, 8, 11 — electrical/radiators, drywall ceilings, tiling); (2) whether
this channel's third-party TV appearances (Москва 24, НТВ) carry real
technique/case substance or are purely human-interest/format filler. Also
included two real kitchen-renovation case studies (Kozhukhovo, Butovo).

| # | Video ID | Title | Why selected | Status | Fact yield | Notes |
|---|---|---|---|---|---|---|
| 1 | `EWNki2-ZFzQ` | Эпизод 8. Монтаж гипсокартонных потолков. ЖК Виноградный. | Vinogradny spot-check (drywall ceiling) | **Partial extraction — thin, low-value pass** | 1 | Very short progress-update video, mostly CTA/filler. Only new item: metal profile can't be cut for elevator fit, must be hand-carried up stairs (10th floor) when elevator too small — extends existing elevator-sheet-cutting logistics note (`O4pGx8ESHDU`) from soundproofing board to general drywall/profile. Region level 2. Low promotional ratio. |
| 2 | `_GL2t3cdSi8` | Эпизод 5. Электромонтажные работы и замена радиаторов. ЖК Виноградный. | Vinogradny spot-check (electrical + radiators) | **Partial extraction** | 2 | Progress-update video. New: керамзит (expanded-clay) lightweight fill under an unusually thick (7-8cm) screed to reduce slab dead-load; a vague ASR-uncertain "special material" mention to prevent гофра conduit overheating in a wire bundle (flagged, not promoted to a rule). Client-testimonial and "get a technical project done first" advice corroborate existing content, not re-extracted. Region level 2. Low promotional ratio. |
| 3 | `GC2vize3KQ0` | Эпизод 11. Плиточные работы. ЖК Виноградный. | Vinogradny spot-check (tiling) | **FULL extraction, best-yielding Vinogradny episode this round** | 3 | Real jobsite tiling walkthrough. New: installer-specific method of tiling directly onto an exposed heated-floor mat with adhesive alone (no self-leveling/skim pre-coat); paint-swatch-behind-furniture color-decision technique; textured ("с пупырышками") tile grout-cleanup difficulty warning. Region level 2. Low promotional ratio. |
| 4 | `xHOOBcDcJZU` | Москва 24 - Специальный репортаж | Third-party TV special report, tests real substance vs. human-interest framing | **Low-value pass — SKIPPED (fetched, not extracted)** | 0 | Confirmed genuinely about Sergey Petrishin/his crew (named directly on air, Russian audio confirmed) — but content is Moscow-24 labor-market journalism (career mismatches, a researcher trying puttying as a stunt), not renovation technique/budgeting. Only renovation-adjacent mention (prime-then-putty sequence) already well-established. Region unresolved. |
| 5 | `0hjkfIfzkUw` | Бригада Сергея Петришина. Потолок своими руками (НТВ) | Third-party NTV segment, ceiling-plastering technique | **FULL extraction — thin, heavy overlap** | 1 | Confirmed genuinely Sergey Petrishin (named on air), Russian audio confirmed. Short "traditional segment" NTV how-to, heavily restates this channel's own extensive existing beacon-plastering content. Only new: beacon product-line thickness options (6mm/10mm, 3m stock length), >5cm-layer multi-pass rule. Region unresolved. Low promotional ratio. |
| 6 | `I8js5-kLrYI` | Бригада Сергея Петришина. Мозаика своими руками (НТВ) | Third-party NTV segment, mosaic technique | **FULL extraction** | 2 | Confirmed genuinely Sergey Petrishin (named on air), Russian audio confirmed. New: white-tile-adhesive-required-for-glass-mosaic rule (dark adhesive dulls shine); notched-trowel depth scaled to half the mosaic's thickness. Curved-wall mosaic use and epoxy-grout preference corroborate existing content, not re-extracted. Region unresolved. Low promotional ratio. |
| 7 | `7-vbxZceZAM` | Ремонт кухни (Кожухово) | Real kitchen case study, Kozhukhovo | **SKIPPED — no captions available** | 0 | Both `youtube-transcript-api` (subtitles disabled) and `yt-dlp` (no ru/en subtitle tracks) failed, `reason_class: null` for both — a genuine no-captions failure, not a rate-limit signature. Not fetched, not extracted. |
| 8 | `ABniAmT5Dx0` | Ремонт кухни (Бутово) | Real kitchen case study, Butovo | **SKIPPED — no captions available** | 0 | Same failure signature as video 7 — both methods failed, `reason_class: null` for both, genuine no-captions, not rate-limit. Not fetched, not extracted. |

**Status: COMPLETE — 6 of 8 videos fully fetched and (partially or fully) extracted, 2 genuinely skipped for no captions, zero rate-limit issues.**

**Round 13 yield**: 6 videos processed (videos 7 and 8 not fetched — no captions, excluded from the denominator), 9 genuinely-new facts (1+2+3+0+1+2, excluding duplicate/corroborating-only outcomes), yield = 1.5 new facts/video — **21% of Round 12's 7.2 baseline, well below the 1.0-floor-adjacent range and a clear >50%-drop trigger.**

### ⚠️ Stop-and-ask signal triggered — explicit flag, not silently overridden

Per this project's own round-yield rule, a >50% drop from the immediately
preceding round (Round 12's 7.2 → this round's 1.5, an 79% drop) is a
stop-and-ask trigger, and 1.5 also sits close to the 1.0 absolute floor.
**This round's low yield has a clear, identifiable cause, not a mystery
about the channel's remaining pool**: it was deliberately composed
entirely of higher-thinness-risk content — 3 more Vinogradny episodes
(a series already flagged in Round 12 as heavily pre-covered ground), 2
third-party NTV short-format clips (a format this vault hadn't tested
yet, structurally a ~1-minute TV spot, not a full technique video), and
1 third-party human-interest TV report — rather than the channel's own
higher-confidence formats (named-technique tutorials, cost-case studies,
"Как выглядит качественная X"/"Как убить X"/"СРАВНЕНИЕ!" series) that
produced 7.6-11.1 facts/video across Rounds 1-11. Two of the round's
8 slots (real kitchen case studies) also turned out to have no captions
at all, further concentrating this round's yield into its thinnest
categories by chance. **Recommendation, not a silent continuation**: do
not dispatch a further round of this same composition (more Vinogradny
episodes, more third-party TV clips) without checking in with the user
first — see the explicit Vinogradny verdict below. A future round drawn
from the channel's already-confirmed high-yield formats would likely
return to the 7-11 facts/video range this channel has shown consistently
before this round, but that is a recommendation for the user to weigh,
not an automatic license to proceed.

### Explicit Vinogradny series verdict (4 of ~13 episodes now spot-checked, Rounds 12-13)

**Verdict: do not commit to the remaining ~9 episodes as a dedicated
round — deprioritize this series going forward**, reversing Round 12's
tentative "worth 2-3 more episodes" holding position now that those
episodes are in. Combined evidence across all 4 spot-checked episodes
(Round 12's episode 7 plumbing: yield 10, but explicitly flagged as
"heavily pre-covered ground"; this round's episodes 5, 8, 11: yields 2,
1, 3 respectively): **the series' own format — short, informal, on-camera
progress-update videos filmed in 2016-17 with minimal narrated technique
explanation — caps its practical yield regardless of which stage/trade
is sampled**, unlike this channel's later (2020s-era) named-technique
tutorials and comparison series, which are structured explicitly around
technique explanation and consistently yield 7-11 facts/video. Across 4
episodes (7, 5, 8, 11 — spanning plumbing, electrical/heating, drywall
ceilings, and tiling, i.e. a real spread of trades, not a fluke of one
stage), the average yield is (10+2+1+3)/4 = 4.0 facts/video, well below
this channel's non-Vinogradny baseline, and 3 of the 4 episodes (5, 8, 11)
individually fell far below that baseline (1-3 facts/video) once
same-channel/cross-topic corroboration was excluded. The series does
still surface occasional genuinely new logistics/technique details (this
round's elevator-profile-carry detail, expanded-clay slab-load fill,
heated-floor tiling method, paint-swatch technique) — it is not worthless
— but its yield-per-video is low enough, and consistently so across a
real trade spread, that continuing it as a dedicated multi-episode
commitment is not a good use of future round budget relative to this
channel's confirmed higher-yield formats. **Recommendation**: leave the
remaining ~9 Vinogradny episodes unprocessed; if revisited at all, treat
individual episodes as opportunistic single-video fill-ins alongside a
higher-yield-format round, never as a dedicated round of their own.

### Rate-limit outcome

**Zero rate-limit signatures encountered anywhere in this round.** All 6
successful fetches were serialized one at a time with real spacing
(interleaved with each video's own full extraction/routing/CSV/archiving
work between fetches — never an idle wait). Both no-captions failures
(videos 7, 8) were independently confirmed via both fetch methods'
`reason_class: null` — genuine no-captions failures, not the rate-limit
signature this project treats as a circuit breaker.

### Region-check finding, per this round's explicit brief

Region evidence stayed uniformly weaker this round than in prior rounds
— no video cleared level 1. 3 of 6 fetched videos (the Vinogradny
episodes) stayed at level 2 (ЖК Виноградный named, no city spoken); the
3 third-party TV segments (videos 4-6) had **region unresolved** — none
named a specific location for the featured apartment/job, since the
third-party framing (Moscow-24, NTV) foregrounds the practitioner/human-
interest angle over the specific object being worked on.

### Language check, per this round's explicit brief

No English-titled video this round. All 6 fetched videos confirmed
Russian spoken audio (`youtube-transcript-api` returned `language: ru`
for every fetch).

### Third-party TV segment verification, per this round's explicit brief

All 3 third-party videos (Москва 24, and the two НТВ clips) were
individually checked against their own spoken content — **all 3
confirmed genuinely Sergey Petrishin/his crew**, not a different
practitioner: the Москва 24 report names "бригадир Сергей Петришин"
directly and follows "Сергей Викторович" personally on-site; both НТВ
clips have Sergey Petrishin personally demonstrating the technique on
camera, addressed by name by the host. All 3 confirmed Russian spoken
audio. **Substance finding**: the Москва 24 report is genuinely
low-value (human-interest journalism, not technique/budgeting content);
the two НТВ clips are technically legitimate short-format demos but
heavily restate this channel's own already-extensive existing content
(ceiling-plastering, general tiling) — only 2-3 minor new numeric/
technique details total across both. **Recommendation**: this channel's
third-party TV-segment cluster is now reasonably well-characterized as
low-to-thin yield (consistent with Round 12's finding on two other short
TV-format clips, which yielded 2 and 4) — do not prioritize remaining
third-party clips (if any exist on the manifest) over the channel's own
higher-yield uploaded formats.

## Progress Log

- 2026-08-24 — **Round 13 complete.** 6 of 8 videos fetched serialized
  one at a time with real spacing (interleaved with each video's own
  full extraction/routing/CSV/archiving work), zero rate-limit issues
  across the entire round. Videos 7 and 8 (real kitchen case studies,
  Kozhukhovo and Butovo) hit genuine no-captions failures (confirmed via
  both fetch methods' `reason_class: null`), logged `status: skipped`.
  Video 4 (Москва 24 report) was fetched but assessed as a low-value
  pass and logged `status: skipped` with reason, per the value-filter
  rule's own guidance for this case (fetched, not a captions failure,
  but not extracted). The remaining 5 videos were partially or fully
  extracted. Yield 9 new facts / 6 processed videos = 1.5 facts/video —
  a clear >50%-drop stop-and-ask trigger from Round 12's 7.2, explicitly
  flagged above with its identified cause (a round deliberately composed
  of higher-thinness-risk content, not a surprise about the channel's
  remaining pool) rather than silently overridden. **Explicit Vinogradny
  series verdict recorded**: deprioritize the remaining ~9 episodes,
  reversing Round 12's tentative holding position, based on a consistent
  low yield (2, 1, 3 facts/video this round; 10 in Round 12, but flagged
  there as heavily pre-covered) across a real 4-trade spread (plumbing,
  electrical/heating, drywall ceilings, tiling). All 3 third-party TV
  segments (Москва 24, 2× НТВ) were individually confirmed genuinely
  Sergey Petrishin with Russian audio — the Москва 24 report is
  low-value human-interest content; both НТВ clips are legitimate but
  heavily restate existing content. Region checked explicitly per video:
  no video cleared level 1 this round (3 Vinogradny episodes at level 2,
  3 third-party TV segments unresolved). Content routed to
  `13_Surfaces_and_Finishes/Ceilings_Guide.md` (elevator-profile-carry
  logistics detail), `13_Surfaces_and_Finishes/Flooring_Guide.md`
  (керамзит lightweight-fill technique), `07_Bathroom/analysis/
  Tile_Selection_and_Layout.md` (heated-floor tiling method, textured-
  tile grout warning, glass-mosaic adhesive/notch rules),
  `13_Surfaces_and_Finishes/Walls_and_Paint.md` (paint-swatch-behind-
  furniture technique), and `12_Engineering_and_Systems/analysis/
  Waterproofing_and_Plastering.md` (beacon thickness/multi-pass rule).
  All 6 fetched transcripts archived via `tools/youtube/archive_
  transcripts.py` (dry-run first, all 6 matched correctly) — all 6
  source notes' bottom `[source: ...]` inline links needed the same
  manual fix as Rounds 5-12 (frontmatter `transcript_file:`
  auto-updated by the script, bottom link was not) — corrected by hand
  for all 6. All CSV rows (5 `archived` + 3 `skipped`) added via direct
  CSV append, independently re-verified via Python's `csv` module to
  parse into the correct 15 columns. `tools/verify_batch.py` to be run
  against the pre-round commit (`0541eec`) before this round is reported
  complete.
