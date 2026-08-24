# Repository backlog — deferred maintenance, not active pipeline steps

This is a to-do list for housekeeping/completeness work deliberately
deferred in favor of active channel/content expansion, not a set of rules
the pipeline must follow on every run. Revisit after a period of active
new-channel processing, not continuously. Update this file (add, check off,
or re-scope an item) whenever a deferral decision like this is made, so the
list stays a real record rather than going stale.

## USD currency normalization (Workstream D residual)

As of 2026-08-21, close of the `PRICE_SCRAPPER_ATTRIBUTION_AND_CURRENCY_NORMALIZATION`
dialogue: **105 of 338** price-bearing units in the defined reference layer
carry a cited USD-equivalent (or an explicit not-computable reason). **233
remain**, split roughly by scope group (re-derive exact current counts before
resuming, these will drift as new content is added):

- `Numeric_Data.md` — 46 done, remainder not yet audited.
- `Cross_Source_Comparison_Tables.md` — 23 done, remainder not yet audited.
- `00_Master/processed_sources.csv` — 17 rows done out of ~420, most rows
  not yet audited for price content at all.
- Scoped guide/detail pages — **done as of 2026-08-24** (rounds 3-12 of
  `PRICE_SCRAPPER_USD_BACKFILL_RESIDUAL`): `Bathroom_Guide.md`,
  `Ceilings_Guide.md`, `Doors_and_Trim.md`, `Walls_and_Paint.md`,
  `12_Engineering_and_Systems` (AC/towel-warmer analysis pages,
  `Plumbing_and_Waterproofing.md`, `HVAC_and_Ventilation.md`),
  `Wardrobes_and_Storage.md`, and each's own `analysis/` pages all now
  carry cited USD-equivalents or explicit not-computable reasons for
  their dated price-bearing units. `Budgeting_Guide.md` also picked up
  content incidentally via the Workstream E live intakes (rounds 8-9).
  **If new rooms/pages are added to the vault later, re-check this list
  isn't stale before assuming guide/detail scope is fully closed.**

**When resuming**: use `USD_Backfill_Inventory.md`'s stable-ID ledger and
content-specific-label convention (established turn 106) as the tracking
mechanism, not raw counts. Run `tools/verify_batch.py --json` on every batch
before considering it done — it checks rate-vs-table correctness, no-cents
rounding, and single-value arithmetic plausibility automatically.

## Workstream E — live pipeline demonstration

The USD-normalization and corrected-attribution steps are documented as
standing pipeline steps in this skill (§5, §5b), and the tooling has been
run directly, but the plan's stronger acceptance bar — **2-3 real,
newly-processed sources showing both inline attribution and USD
normalization applied live during intake**, not retrofitted — has never
actually been demonstrated and linked as evidence. The next 2-3 genuinely
new channel/video intakes naturally satisfy this if their extraction notes
and store updates are checked afterward and cited somewhere (e.g. back in
a reopened dialogue, or a short review file) as the demonstration.

## Exchange rate table gaps

- **USD/BYN 2018-2019**: never attempted. `tools/pricing/fetch_exchange_rates.py`
  should be able to pull these directly (same as the successful 2013-2017
  test done 2026-08-21) - just needs doing.
- **USD/BYN 2017, 2020, 2021**: attempted and confirmed unfetchable via the
  methods tried so far (partial/empty API responses) - marked
  `unverified / needs source` in `00_Master/exchange_rates_reference.md`
  with the specific failure noted. Worth a retry with a different
  date-chunking strategy if this ever becomes load-bearing for a real
  source's conversion, not worth chasing speculatively.
- **Pre-2016 BYN redenomination boundary**: see SKILL.md §5b's missing-year
  rule for the caveat; no outstanding action, just a landmine to remember
  if a pre-2016 Belarusian source shows up.

## Legacy rounding-bucket sweep (found 2026-08-23, round 7)

`tools/verify_batch.py` gained a `check_rounding_bucket` check (2026-08-23)
that flags any `≈$` figure not landing on the correct nearest-10/100/1,000
bucket for its magnitude (see SKILL.md §5b's rounding rule). Round 7 found
and fixed 3 instances live (`AC_Sizing_and_Selection.md` + two already-merged
`Numeric_Data.md`/`USD_Backfill_Inventory.md` entries from an earlier
round), but a full-history scan (`--base <root-commit> --head main`) found
**50 pre-existing violations** across the wider repo, including files
outside this dialogue's current scope: `Change_Log.md`,
`Cross_Source_Comparison_Tables.md`, and both case-study files
(`7komnat_novaya_borovaya_52m2_case.md`,
`yana_vrublevskaya_minsk_mir_studio_2023_case.md`). Not swept — this is a
dedicated future round's worth of work, not something to fold into an
in-progress batch. When resuming: run the full-history scan first to
re-derive the current count (new content may have added or fixed more
since), then work through them the same way round 7 did (re-derive the
correct rate/amount from `currency_converter.py` directly, don't just
apply the nearest-bucket formula blind — some may also have a stale rate
or amount, not just a rounding miss).

## Page restructuring backlog

Pages flagged during a housekeeping pass as having crossed the layered-
conversion threshold (see `00_Master/wiki_page_format.md`'s "Layered
convention" section) but not converted on the spot, because the conversion
itself is dedicated-session-sized work (splitting into several `analysis/`
pages, rewriting the compact guide, re-pointing every cross-link) — not
something to squeeze into a housekeeping check between processing rounds.

- **`13_Surfaces_and_Finishes/Walls_and_Paint.md`** (flagged 2026-08-24,
  during the Kruglov/Ontario intake's post-Round-3 housekeeping review): 239
  lines, ~15 distinct sub-topics (substrate compatibility, gas-block wall
  material calculation, partition-layout masonry technique, foam-glue
  masonry, radiator-niche insulation mechanism, load-bearing wall opening
  technique, future-flexible planning, wall-plane offset/tie-in rules,
  partition-thickness defaults, wall-squareness diagnostics, and more) — well
  past the threshold that triggered the Bathroom (397 lines) and Wardrobes
  (141 lines, 6 sub-decisions) conversions. **Not converted yet.** When
  resuming: follow the same shape as those two conversions (compact guide +
  `analysis/` pages, Source Notes and Change Log split to their own pages),
  moving/reorganizing existing prose rather than re-deriving it, and update
  every inbound link that named the old single page.

- **`12_Engineering_and_Systems/analysis/Waterproofing_and_Plastering.md`**
  (flagged 2026-08-24, during the Pavel Sidorik intake's post-Round-4
  housekeeping review): 338 lines and growing fast — this is itself already
  a detail-level `analysis/` page (not a top-level Guide), but it has
  accumulated at least 9 distinct sub-topics (floor waterproofing membrane
  QC, brush-on/cementitious product selection, plaster substrate/crack
  prevention, beacon/laser 90°-corner method, plastering-workflow tricks,
  ceiling plaster without full mesh, bathroom-specific substrate prep,
  rough-stage acceptance checklist, screed expansion joints/soundproofing) —
  arguably dense enough to warrant its own further split into per-sub-topic
  analysis pages under a compact `Waterproofing_and_Plastering` summary,
  the same pattern applied one level up when a top-level Guide gets split.
  **Not converted yet** — still accumulating new Pavel Sidorik plastering
  episodes as of this flag, better to let it settle before deciding the
  final page boundaries.

**When adding a new item here**: note the line count, sub-topic count, and
the date/context it was flagged, same as the entries above, so a future
session doesn't have to re-derive whether it's still overdue.

## Tooling limitations (known, not urgent)

- `tools/verify_batch.py`'s arithmetic-plausibility check only fires on
  unambiguous single-value lines (exactly one dollar figure, exactly one
  RUB/BYN figure, in the whole line before the rate annotation) - it
  deliberately skips ranges and multi-figure lines rather than risk a wrong
  pairing. A more complete range-aware version is possible but wasn't
  worth building speculatively; revisit if a range-line defect actually
  slips through in practice.
- Citation-ID drift detection is file-level (a source ID could theoretically
  move between claims without the set changing) rather than claim-local.
  Same reasoning: real gap, not worth closing until it actually causes a
  missed defect.
- A canonical machine-readable "Workstream D completeness report" (one row
  per inventory unit: file, anchor, original amount/currency, source year,
  rate used, USD result or reason, status) was proposed but never built.
  Would make a future closure turn's audit faster; not blocking.

## Process notes worth re-reading before resuming

- `WORKSTREAM_OWNERSHIP.md` and `CROSS_DIALOGUE_NOTICES.md` (in
  `ai-management`) are the coordination mechanism for concurrent
  agent work - re-read `ai-skills/skills/management-plan-dialogue/SKILL.md`
  before opening a new dialogue for this backlog.
- Open a **new, narrowly-scoped dialogue** for this backlog rather than
  reopening the closed 107-turn `PRICE_SCRAPPER_ATTRIBUTION_AND_CURRENCY_NORMALIZATION`
  one - that was the explicit reason it was closed.
