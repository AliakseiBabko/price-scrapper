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
