# Zemskov/Zemstandart remainder pool — post-Category-5 continuation

**Created 2026-08-19**, after the full Category 5 batch (37 videos, 2 trials + 4 chunks)
closed out the original full-channel triage (`_Inbox/planning/zemskov_full_channel_triage.md`).
This file tracks further remainder-pool work beyond the original 17-video candidate list
(now fully processed — see "Round 1" below), and a **newly re-derived Round 2 list of 16
candidates** found 2026-08-19 by cross-referencing the full `channel_fresh_titles.txt`
manifest against `00_Master/processed_sources.csv`, revealing IDs never covered by any
prior triage pass (Category 4, Category 5, or the original Round 1 remainder-pool list).

## Scope decision (explicit user direction, 2026-08-19, still in force)

The user's own renovation is a **new-build apartment**, not secondary/old-building
("вторичка"/старый фонд) housing. When a candidate video turns out to be specifically
about secondary/old-building renovation, do a PARTIAL extraction (crossover-relevant
technique points only), not a full skip. See the project's own memory file
(`feedback_check_agents_skills_before_external_fetch` etc.) and prior source notes
(e.g. `YT_ajtv-urp18I_old_building_crossover_tips_101.md`) for the pattern.

## Two permanently-excluded buckets — never fetch these

- **Channel-meta/self-promo (11 videos)**: `WGlKAKn6hQY`, `peyUIi32BpM`, `Y7YU4tKDxfg`,
  `2Ha1CBay93Y`, `SlnTNHiYzUo`, `YDXw0qHMaBI`, `dZ4_TkZmO2M`, `e0jbZYAFT_g`,
  `SUUGeKWlcj4`, `widAQZWdMcU`, `304zZRMZUoQ`.
- **Legal/dispute/named-individual callout (4 videos)**: `oycgnkyYii4` ("Wall of Shame"),
  `sxUZ_TwgMdQ`, `Duyq7P53pH4`, `ayQj0W9rd8o` (middleman lawsuit content).

**Named-individual content within an otherwise-processable video** (not a full exclusion):
per standing convention, extract only the generalizable content and drop the personal/
naming/dispute-specific content — see `YT_ZvyXuUJ__Ag_middleman_scam_mechanism_511.md`
for the worked example.

## Round 1 — COMPLETE (24 videos processed, 2026-08-19 session)

The original 17-video candidate list (drawn from Category 5's own candidate-derivation
pass) is **fully processed**: 13 FULL, 4 PARTIAL (named-individual exclusions or heavy
redundancy), 4 genuine no-captions skips. Full per-video breakdown lives in this file's
git history (see commits `zemskov-remainder-batch2` through `zemskov-remainder-batch5-final`,
2026-08-19) and in the intermediate knowledge store's Change Log.

**Key finding from Round 1**: at least 6 videos (`ZVoExA0t6nI` #223, `1pU60p0Jh3A` #228,
`HVSZh0lH9hk` #230, `W9cCxVQVVes` #232, `8Xy-h8cS_-s` #234, `n7X10oIqugU` #252) belong to
one July-November 2023 narrated-planning-logic production cluster with heavy content
overlap — worth remembering if any further video from this same window surfaces below.

**Round 1 yield**: 24 videos processed, 40 genuinely-new facts (excluding duplicate/corroborating-only outcomes), yield = 1.67 new facts/video. Retrofitted from the round's enumerated store bullets after removing repeated cluster findings.

## Round 2 — COMPLETE (16 of 16 videos, batches 1-4, 2026-08-19 through 2026-08-20)

| Video ID | Title | Outcome |
|---|---|---|
| `DEs8V-mHHDo` | "КУХОННЫЙ ПИ…ДЕЦ 2022! СЕМЬ КОСЯКОВ НА ОДНОЙ КУХНЕ! #169" | ✅ FULL — 7-point kitchen-installer QC checklist |
| `C4lUAfJyyb0` | "НОВЫЙ ПИ…ДЕЦ ОТ ЗАСТРОЙЩИКА ЗА ДЕНЬГИ ЗАКАЗЧИКА #170" | ✅ FULL — electrical-panel-niche formula, Odintsovo level-1 region |
| `Qw2Xi6uPLls` | "DON'T EVER DO THIS IN YOUR HALLWAY! #302" | ✅ FULL — ⚠️⚠️ standout: the "floating dimension" construction-drafting technique |
| `MWDcYHqe-iQ` | "74 JOINTS IN 74 METERS #288" | ✅ FULL — dense designer-critique tour, many new points |

All 16 are logged in `00_Master/processed_sources.csv` (`run_20260819_<video_id>` / `run_20260820_<video_id>`), have source extraction notes under `11_Budget_and_Planning/_supporting/knowledge/sources/` (except the confirmed duplicate and the 2 no-captions skips), are integrated into the intermediate store's Change Log, and were wiki-routed the same session as processed.

**Final tally (Round 2 only, 16 candidates)**: 13 extracted (1 PARTIAL for named-individual exclusion: `pNhM-kKBy6A`), 1 confirmed duplicate (`mhE_5qlJ0KU`, a re-edited remake of already-processed `C4lUAfJyyb0`), 1 genuine no-captions skip (`HE4u2vprC88`). `OnKreLhmLYY` (#299) and `nbrDFET2AXk` (#295) turned out to be parts 2-3 of the same "90 mistakes" series about one apartment — a real same-project overlap case, flagged in both source notes rather than double-counted. `hVFmcw1H2Rk` (#314) delivered this project's **standout finding of Round 2**: a complete, precisely sequenced 12-item bedroom design formula. A real structural gap surfaced during this batch: this vault has no numbered folder for a master/primary bedroom despite 5+ accumulated sources — flagged in the store's Pending Wiki-Page Decisions section for explicit user decision, not resolved unilaterally.

**Round 2 yield**: 16 videos processed, 31 genuinely-new facts (excluding duplicate/corroborating-only outcomes), yield = 1.94 new facts/video. Retrofitted by counting the four batch breakdowns and removing the confirmed duplicate, no-caption skip, and same-project/corroborating-only repeats.

## Round 3 — not yet started

Round 2's 16-video candidate list (re-derived by diffing the full channel manifest
against the processed-sources CSV) is now fully exhausted. A future session wanting to
continue would need to re-scan
`channel_fresh_titles.txt` again (it may itself be stale/incomplete relative to the
channel's true full catalog — it was generated at some earlier point in this triage
project, not necessarily re-fetched from YouTube itself) or pull a fresh channel video
list if the user wants to keep going beyond this file's own candidate pool.
