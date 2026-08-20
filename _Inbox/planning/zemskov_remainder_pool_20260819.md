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

## Round 2 — processed so far (8 videos, batches 1-2, 2026-08-19)

| Video ID | Title | Outcome |
|---|---|---|
| `DEs8V-mHHDo` | "КУХОННЫЙ ПИ…ДЕЦ 2022! СЕМЬ КОСЯКОВ НА ОДНОЙ КУХНЕ! #169" | ✅ FULL — 7-point kitchen-installer QC checklist |
| `C4lUAfJyyb0` | "НОВЫЙ ПИ…ДЕЦ ОТ ЗАСТРОЙЩИКА ЗА ДЕНЬГИ ЗАКАЗЧИКА #170" | ✅ FULL — electrical-panel-niche formula, Odintsovo level-1 region |
| `Qw2Xi6uPLls` | "DON'T EVER DO THIS IN YOUR HALLWAY! #302" | ✅ FULL — ⚠️⚠️ standout: the "floating dimension" construction-drafting technique |
| `MWDcYHqe-iQ` | "74 JOINTS IN 74 METERS #288" | ✅ FULL — dense designer-critique tour, many new points |

All 4 are logged in `00_Master/processed_sources.csv` (`run_20260819_<video_id>`), have source extraction notes under `11_Budget_and_Planning/_supporting/knowledge/sources/`, are integrated into the intermediate store's Change Log, and were wiki-routed the same session.

## Round 2 — 4 remaining candidates (not yet touched)

Found by diffing `_Inbox/transcripts/channel_fresh_titles.txt` (158-row full-channel
manifest) against every `watch?v=` URL in `00_Master/processed_sources.csv`, then
removing the two permanently-excluded buckets above. **None of these 16 IDs appear in
any prior triage file's candidate or exclusion list** — a genuine gap in every previous
pass. Cross-reference each against the CSV again before fetching (a fresh session should
re-verify, not just trust this table):

**Update (batches 1-3 complete, 11 of 16 videos)**: 10 extracted (2 partial for named-individual exclusions), 1 confirmed duplicate (`mhE_5qlJ0KU`, a re-edited remake of already-processed `C4lUAfJyyb0`), no genuine no-captions skips in Round 2 so far. `OnKreLhmLYY` (#299) and `nbrDFET2AXk` (#295) turned out to be parts 3 and 2 of the same "90 mistakes" series about one apartment — a real same-project overlap case, flagged in both source notes. `eezwcNG-1qI` (#269) confirmed on-topic, resolving the spot-check caution below.

| Video ID | Title | Notes |
|---|---|---|
| `4omxjEA7LaI` | "DESIGN DISASTER IN 60 SQUARE METERS #283" | dunk-format |
| `hVFmcw1H2Rk` | "A TOTAL DESIGN MESS IN YOUR BEDROOM! #314" | dunk-format, close in number to already-processed Category 5 videos — check for duplicate/reused-script risk against `Rlyx2F7Aaxg` #315 (already processed) |
| `GtOQ7h1p5qc` | "70 m2 OF PURE DESIGN MADNESS! #303" | dunk-format, same #296-315 numbering cluster as several already-processed Category 5 videos — check content independence |
| `HE4u2vprC88` | "РЕМОНТ КВАРТИРЫ В БЕЛЫХ ТОНАХ. ОТЗЫВ ЗАКАЗЧИКА #514" | positive client-testimonial format, #5xx (no longer treated as inherently risky per Round 1's finding) |

## Suggested next step

Continue in small batches (3-4 videos), same pipeline as Round 1: verify unprocessed
against the CSV → fetch serialized with real spacing → extract (applying the new-build
scoping rule) → integrate into the intermediate store → wiki-route the same session →
CSV log → archive transcripts → branch → commit → push → merge to `main` → delete branch.
Update this file's Round 2 table (move rows to a new "Round 2 — processed" section) as
each batch completes.

After Round 2 is exhausted, a Round 3 re-derivation would need to re-scan
`channel_fresh_titles.txt` again (it may itself be stale/incomplete relative to the
channel's true full catalog — it was generated at some earlier point in this triage
project, not necessarily re-fetched from YouTube itself) or pull a fresh channel video
list if the user wants to keep going beyond this file's own candidate pool.
