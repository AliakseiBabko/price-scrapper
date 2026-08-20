# Kruglov/Ontario Batch — 2026-08-20

4-video batch from the "Konstantin Kruglov | Ontario" channel (Moscow renovation company, self-promotional per this store's existing notes; 4 prior sources already processed as of this batch's start). All 4 videos were pre-confirmed fresh (never processed) by the user before this batch started; each was also double-checked against `00_Master/processed_sources.csv` before fetching, per standing practice.

This batch was explicitly a process-convention test, not routine processing — three specific things were exercised and verified: (1) the 2026-08-20 routing-default convention (prefer an existing room/domain wiki `analysis/` page over `Durable_Facts.md`), (2) the round-yield stopping-signal convention, (3) the batch-status JSON convention (`_Inbox/planning/batch_status_20260820_kruglov_ontario.json`).

## Videos processed

| # | Video ID | Title | Outcome | fact_yield |
|---|---|---|---|---|
| 1 | `9dfEdjOewng` | These Bathroom Mistakes Will Ruin Any Renovation | Full extraction | 9 |
| 2 | `dJMsXYUyh7A` | Lighting Your Home Without Mistakes | Full extraction | 15 |
| 3 | `ihx8gUDO3vI` | Top Solutions for a Small Kitchen | Full extraction | 14 |
| 4 | `09aHjDgl-vk` | 8 Signs of a HORRIBLE Floor Plan | Full extraction | 8 |

All 4 fetched cleanly (no rate-limiting, no no-captions failures), all 4 cleared the value-filter spot-check (dense, checklist-style technical content, low promotional ratio throughout — consistent with this channel's already-established substantive style from its 4 prior sources).

## Routing outcome (the actual point of this batch)

- **Video 1 (Bathroom Mistakes)**: 100% routed to existing `07_Bathroom/analysis/*` pages (`Bathtub_and_Shower.md`, `Fixtures_Mixers_and_Sinks.md`, `Tile_Selection_and_Layout.md`, `Shelving_and_Furniture.md`, `Lighting_and_Electrical.md`). Zero `Durable_Facts.md` entries — every fact had a matching existing bathroom page.
- **Video 2 (Lighting Guide)**: 100% routed to 4 existing analysis pages across 3 different folders (`12_Engineering_and_Systems/analysis/Lighting_Design.md`, `07_Bathroom/analysis/Lighting_and_Electrical.md`, `11_Budget_and_Planning/_supporting/analysis/Bedroom_Design_Principles.md`, `03_Kitchen/Kitchen_Furniture.md`). Zero `Durable_Facts.md` entries, despite the source spanning 4+ rooms.
- **Video 3 (Small Kitchen)**: 100% routed to 3 existing `03_Kitchen/*` pages, including populating a previously-empty page (`analysis/Furniture_Facade_Materials.md`) with its first real content. Zero `Durable_Facts.md` entries.
- **Video 4 (Floor Plan Red Flags)**: 100% routed to `Durable_Facts.md` — this is the expected exception anticipated in the task itself: apartment-purchase-stage criteria (curved walls, corridor width, insolation orientation, load-bearing constraints, sewer-riser placement, kitchen-niche sizing) are genuinely cross-cutting with no matching single room/domain wiki page, consistent with this store's existing large "Planning Rules" backlog (no dedicated Planning Rules wiki page exists yet, confirmed by checking `store/Planning_Rules.md`'s own routing note before deciding).

**Net result: 3 of 4 videos landed 100% on existing wiki pages, 1 of 4 legitimately landed in `Durable_Facts.md`** — the routing-default convention worked as intended and was not defaulted-to out of laziness; each Durable_Facts.md placement was a deliberate, checked decision (confirmed no matching page exists), not the fallback path.

## Round yield

**Round 1 yield** (first round for this channel/list — no prior round to compare against, no stop-signal decision applicable): 4 videos processed, 46 genuinely-new facts (9 + 15 + 14 + 8, each counted once even where a fact was routed to multiple pages), yield = 46 / 4 = **11.5 new facts per video**.

This is a very high yield relative to other channels/batches processed in this store (most other batches in `Durable_Facts.md`'s Change Log run in the low single digits per video) — consistent with this channel's already-established reputation (per its 4 prior sources) as technically substantive despite being self-promotional. No stop-signal applies on a first round; if a future round processes more of this channel, compare against this 11.5/video baseline.

## Batch-status JSON

`_Inbox/planning/batch_status_20260820_kruglov_ontario.json` was created at batch start (all 4 videos `pending`) and updated at every transition (`pending` → `fetched` → `extracted` → `archived`) as each video moved through the pipeline. Final state: all 4 videos `archived`. See that file for the exact JSON.

## Process notes / things worth flagging for later

- The "Planning Rules" sub-topic in `Durable_Facts.md` has been past its own 3+-source page-creation threshold for a long time (dozens of batches since 2026-08-05) with no dedicated top-level wiki page ever created. This batch's video 4 added one more batch to that backlog rather than resolving it — flagged explicitly in the store entry and here, since building a new top-level "Planning Rules"/floor-plan-selection wiki page is a real decision (page shape, scope, what to pull from ~15 years of accumulated batches) that's out of scope for a 4-video batch task and deserves its own explicit session.
- Video 3 (Small Kitchen) surfaced a mild, flagged (not resolved) tension: its "use the full vertical height including the mezzanine tier" rule for small kitchens sits against this store's existing medium/large-kitchen "mezzanine tier is skippable" guidance — not a contradiction (different kitchen sizes), but worth a reader's attention.
