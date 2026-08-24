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

## Round 1 — Trial batch (5 videos, dispatched 2026-08-24)

Selected for topic diversity and highest expected signal, not sequential order:

| # | Video ID | Title | Why selected |
|---|---|---|---|
| 1 | `hpU_xEXmdvE` | Как принять квартиру у застройщика? Ремонт в НОВОСТРОЙКЕ от А до Я. #1 | Directly relevant to the new `16_Legal_and_Regulations/analysis/Handover_Acceptance_and_Defect_Reporting.md` placeholder — first real candidate source if it clears the level-1 Belarus bar |
| 2 | `Oh4hGMZ90mw` | Из чего состоит дизайн проект? Нужен или нет? Цена? | Design-process content, relevant to `11_Budget_and_Planning` and potentially `17_Design_and_Ergonomics` |
| 3 | `0sJPlpi8I2U` | How much does the repair cost in Khrushchev? Overview of the finished apartment. Rework from A to Z | Real cost-benchmark candidate for `11_Budget_and_Planning`/`Budgeting_Guide.md` |
| 4 | `C0FOWRxqWX4` | How to Waterproof a Bathroom from A to Z? All Steps. Potential Mistakes. | Dense bathroom technique, tests fit against existing `07_Bathroom/analysis/*` pages |
| 5 | `b0FeObtj2bo` | Основные ошибки при капитальном ремонте! Советы для начинающих! | General "mistakes" format, tests this channel's own promotional ratio |

## Rounds 2+ (not yet planned)

Deferred until the trial batch reports back. If the channel clears the value bar, next steps: cluster the two numbered series and the standalone-technique pool by destination page (same approach as the Kruglov/Ontario plan), decide whether to process series entries in narrative order (recommended — they're a real sequential project) vs. by topic, and explicitly deprioritize/skip the tool-review and pure-filler videos identified above.

## Progress Log

- 2026-08-24 — Channel discovered and preflighted while the Kruglov/Ontario channel's Round 4 was paused on a YouTube rate-limit — switching channels rather than waiting out the cooldown, per explicit user direction. Plan file created, 5-video trial batch dispatched.
