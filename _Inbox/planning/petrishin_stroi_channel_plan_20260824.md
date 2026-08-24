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

## Round 1 — Trial batch (5 videos, dispatched 2026-08-24)

Selected for topic diversity and highest expected signal (technique +
real-cost case studies), deliberately avoiding the generic "ошибки" clickbait
format for this first pass per the value-filter rule:

| # | Video ID | Title | Why selected |
|---|---|---|---|
| 1 | `D1REgSDwILU` | Basics of COMPETENT plastering | Named-technique tutorial, tests baseline substance |
| 2 | `E7M-bWWSmfw` | Как сделать стяжку. Этапы, советы, ошибки. Полусухая механизированная стяжка. | Screed technique + cost/steps, tests fit against existing `13_Surfaces_and_Finishes` / `Flooring_Guide.md` |
| 3 | `S23VRWxzz08` | Сколько стоит черновой ремонт в 2022? Подробный разбор на реальном примере! | Real cost breakdown case study — tests region/year-resolved pricing value |
| 4 | `caDB-roRasI` | От чего трескаются стены? Приемка кладки, как должно быть? | Masonry defect/acceptance criteria — tests technique + possible handover/acceptance relevance |
| 5 | `8IW762yALfc` | Ремонт в Москве стоимость всех черновых работ. Показываем реальный объект 2024. | Real 2024 rough-work cost object — second cost-benchmark test, most recent of the batch |

Status: **pending dispatch**.

## Progress Log

- 2026-08-24 — Channel discovered via `preflight_playlist.py` (light mode,
  no rate-limit on the listing fetch), title-skimmed (341 titles reviewed),
  5-video trial batch selected and this plan file created. Dispatching
  Round 1 next.
