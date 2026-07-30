# Renovation Budgeting — Intermediate Knowledge Store

> [!NOTE]
> Initialized 2026-07-30 during the wiki/case-study reorganization. This store is a scaffold, not a completed extraction pass — no source has yet been run through the `renovation-knowledge-intake` skill's formal intake pipeline (`meeting-transcript-extract` → this store → `tiered-knowledge-base` synthesis). The sections below link to the case studies that already existed before this reorg; they are pointers, not upserted structured facts. No numeric fact in this file has been independently re-verified here — see each linked case study or archived source for provenance.

## Source Index

Formal intake pending. Sources already referenced by existing case studies (see `00_Master/processed_sources.csv` for the full registry):

- `dfc91747` / `26bc9c25` — Minsk World 60 m² turnkey project (cost + companion design). See [[11_Budget_and_Planning/_supporting/case_studies/minsk_world_60m2_design_cost_case|Minsk World 60m² Case]].
- `b385361e` — 44 m² Minsk apartment labor смета (screenshots + transcript). See [[11_Budget_and_Planning/_supporting/case_studies/price_table_screenshot_case|Price Table Screenshot Case]].
- `21a6e3c1`, `21ade3f6`, `f23c504a`, `61e3a372`, `a8e90887` — sequencing/workflow sources. See [[11_Budget_and_Planning/_supporting/case_studies/schedule_analysis_case|Schedule Analysis Case]] and [[11_Budget_and_Planning/Renovation_Sequence|Renovation Sequence]].
- `360f4c7c`, `371bd212`, `7617b523` — cost-saving strategy sources. Now integrated as [[11_Budget_and_Planning/Budgeting_Guide|Budgeting Guide]] §5, full detail in [[11_Budget_and_Planning/_supporting/analysis/cost_saving_strategies_full|cost_saving_strategies_full]].
- `4b421350` — Russia/RUB secondary reference pricing (not yet linked to a case study).

## Durable Facts

*Not yet extracted into this store. Pending formal intake.*

## Numeric Data / Measurements

*Not yet extracted into this store — numeric data currently lives only inside the case studies listed above. Pending formal intake would upsert specific figures here with per-fact source/confidence tags.*

## Cases / Examples

- Minsk World 60 m² turnkey ($54,000 / $900 per m², 2025, primary Minsk benchmark).
- 44 m² Minsk labor-only смета (row-level, 2025, primary Minsk benchmark).
- 24-step turnkey workflow (cross-sourced, multiple 2024 Russia transcripts).

## Rules / Heuristics

*Not yet extracted into this store. The wiki pages already contain synthesized heuristics (buffer %, rough/finish material split, labor-vs-total ratio) — formal intake would trace each back to its source here.*

## Risks / Gaps

- No source yet establishes a min/max price distribution across projects — the case study for this is planned but not created (see [[11_Budget_and_Planning/Budgeting_Guide|Budgeting Guide]] §6).
- `price_table_screenshot_case.md` mixes budgeting evidence with unrelated screenshot/parser test-fixture content; not yet split.
- `11_Budget_and_Planning/_supporting/legacy/Master_Budgeting_Guide_legacy_pre_reorg.md` (legacy, pre-reorg) still contains a short Russia/RUB secondary-reference subsection that was not carried into any case study or this store during this pass — flagged, not lost (original file untouched).

## Open Questions

- Should the Russia/RUB secondary reference bullets (source `4b421350`, `7617b523`) get their own case study, or fold into an existing one?
- When should formal `meeting-transcript-extract` → `tiered-knowledge-base` intake actually run against the already-archived sources in `90_Archive/processed_sources/`, versus continuing to treat the hand-written case studies as sufficient?

## Change Log

- 2026-07-30 — Store created (scaffold only) as part of the `11_Budget_and_Planning` wiki/case_studies/knowledge reorganization. No facts extracted yet.
- 2026-07-30 — Moved to `_supporting/knowledge/intermediate/` as part of the visibility-focused top-level reorganization (`Budgeting_Guide.md` and `Renovation_Sequence.md` are now the only top-level pages; `cost_saving_strategies.md` was integrated into `Budgeting_Guide.md` §5, full text preserved at `_supporting/analysis/cost_saving_strategies_full.md`). Links above updated accordingly; no facts extracted yet.
