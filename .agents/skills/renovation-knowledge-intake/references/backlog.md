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
- Scoped guide/detail pages — only the two Doors pages done (19 lines).
  The rest of the plan's guide/detail scope (`Bathroom_Guide.md`,
  `Budgeting_Guide.md`, `Plumbing_and_Waterproofing.md`,
  `HVAC_and_Ventilation.md`, `Walls_and_Paint.md`, `Ceilings_Guide.md`,
  `Wardrobes_and_Storage.md`, and each of the above's own `analysis/`
  pages) has not been started.

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
