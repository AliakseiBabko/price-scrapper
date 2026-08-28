---
source_type: video transcript (turnkey renovation company owner, project-duration-estimation explainer, Russian, ASR auto-generated captions — no punctuation)
source_url: https://www.youtube.com/watch?v=9lFhda_KDHk
video_id: 9lFhda_KDHk
transcript_file: not separately archived — fetched inline via youtube_transcript_api (sha256 11695044e9238a272eaa686c3fd0a9e7689af38ff0c88f6b4f77edfeb88c2fa5)
fetched: 2026-08-28 (anonymous, youtube_transcript_api, ru auto-generated captions, is_generated=true, language_code=ru)
upload_date: 2024-10-28 (confirmed via yt-dlp metadata)
channel: Константин Круглов | Ontario (Moscow/Moscow-region turnkey renovation company)
regional_applicability: level 2 (Moscow/Moscow-region channel context; not re-confirmed spoken in this specific video)
currency: RUB, converted at trailing-6-month USD/RUB mean before 2024-10-28 (90.3098 RUB/USD, via tools/pricing/currency_converter.py)
language: ru
extraction_taxonomy: custom (renovation planning)
fact_yield: 12
promotional_ratio: low-medium (built around this company's own internal 60-object dataset and smeta-review service, but the underlying throughput methodology and the two named timeline-scam schemes are concrete and reusable regardless of who executes them)
corroborates_existing: false — genuinely new content, no meaningful overlap found
---

# Extraction Note — Konstantin Kruglov (Ontario): "Вся правда о том СКОЛЬКО времени у вас займет ремонт!" (YouTube 9lFhda_KDHk)

## Round 12 context

Video 3 of 7 in this round. Checked against this vault's existing
`11_Budget_and_Planning/analysis/Project_Duration_and_Scheduling.md`
(MaxDar, ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, Forcemontage, VitionGroup — all turnkey-
company duration sources converging on a 6-9-month floor) and this
channel's own prior cost content (`P8t_d7J9fm4`, `soshw_203eY`,
Round 11's cluster) — **no meaningful overlap found with either**. This
video is the first source in this store to attempt an explicit,
falsifiable *duration-estimation methodology* (as opposed to a
headline range or a stage-by-stage schedule) and the first to document
timeline-specific (rather than smeta-wording-specific) contractor-scam
mechanisms. Full extraction — dense, genuinely new content throughout.

## Planning Rules — Two Failed Duration Heuristics, Explicitly Falsified by the Source's Own Data

- **⚠️ The naive room-count heuristic fails, tested against real data**:
  the common assumption ("1-room ≈ 1.5 months, 2-room ≈ 2 months,
  3-room ≈ 3 months...") was this speaker's own starting assumption
  before he began seriously analyzing renovation duration roughly 2
  years before this video — at the time, "every second object" at his
  own company was missing its deadline. Explicitly abandoned once
  tested against real completed-object data.
- **⚠️ A three-tier "complexity coefficient" heuristic was tried next,
  and also failed once tested against real data** — worth recording as
  a genuine negative finding, not just the working method that replaced
  it:
  - **Coefficient 1 (simplest)**: stretch ceiling, wallpaper, laminate,
    ordinary MDF baseboards, no painting or concealed-mount work, a
    small number of outlets/switches.
  - **Coefficient 2**: paint-ready walls, parquet board, still-rigid
    (surface-mounted) baseboards, more outlets/switches, some
    large-format tile.
  - **Coefficient 3** (nicknamed "golden toilets," a stock phrase not
    meant literally): multi-level drywall ceilings, paint-ready walls
    or decorative plaster, concealed-mount doors, a large number of
    built-in linear lighting fixtures on ceiling/walls, concealed or
    shadow-gap baseboards, glued engineered board (e.g. herringbone).
  - **Why it failed**: even mapping this coefficient against floor
    area, results were inconsistent across the source's own completed
    objects (e.g. a 40 m² apartment and a 100 m² apartment didn't scale
    proportionally under the same coefficient) — abandoned as a
    predictive formula once tested against a real dataset, not merely
    theorized to be imprecise.

## Planning Rules — The Metric That Actually Works: "Выработка" (Monthly Throughput Rate)

- **⚠️ A named, data-derived monthly-throughput benchmark, based on an
  internal analysis of 60+ completed objects**: this company's own
  average labor-only monthly throughput ("выработка") is **≈250,000
  RUB/month per object (≈$2,800/month)** — individual objects in the
  underlying dataset ranged 300,000-350,000 RUB/month (≈$3,300-
  $3,900/month), with 250,000 RUB/month being the dataset-wide average,
  not a single project's figure. **Duration formula, worked examples
  given directly**: duration in months = labor-only smeta total ÷
  250,000 RUB — a 1,000,000 RUB (≈$11,100) smeta implies **4 months**; a
  2,000,000 RUB (≈$22,100) smeta implies **8 months**; a 3,000,000 RUB
  (≈$33,200) smeta implies **12 months**. **Explicitly framed as only
  statistically meaningful at this dataset size**: the speaker states
  directly that comparing 1, 2, 3, 5, or even 10 objects would not be
  "statistics" one could actually plan against — 60 objects is where it
  becomes a real planning input.
- **⚠️ A named, genuinely new planning consideration: two annual
  "dead zones" must be added on top of the throughput-based duration
  estimate, not absorbed into it**: the week before New Year (clients
  stop wanting to accept completed work, crews are mentally checked out
  buying gifts, productivity effectively drops to zero) and the same
  pattern around the May holidays — both must be explicitly budgeted as
  calendar time that doesn't count toward the throughput rate, not
  silently assumed away.
- **Complexity still matters, but through cost, not as an independent
  variable**: the three complexity coefficients above do genuinely
  change both the smeta total and the duration, but only *because* they
  change the total labor-only cost being divided by the fixed monthly
  throughput rate — not as a separate multiplier. **Two worked
  same-area comparisons**: a 50 m² apartment with wallpaper + stretch
  ceiling ("simple but stylish, without overdoing it") might run 4-5
  months; the identical 50 m² footprint finished throughout in
  decorative plaster + glued herringbone engineered board + concealed
  doors + concealed baseboards could take "a year, maybe not even
  enough" — 2-3× the cost and correspondingly more than 2-3× the
  duration on the same throughput formula, since concealed/decorative
  work sits in the highest complexity tier.

## Mistakes / Warnings — Why You Can't Simply "Add More Workers" to Go Faster

- **⚠️ A real crowding-out mechanism specific to small apartments, not
  previously documented in this store**: an electrician and a plumber
  each need to route their own trade's work across the *entire*
  apartment, not one room each — in a small apartment, adding more
  workers from the same trade (or running multiple trades
  simultaneously) causes real physical crowding, materially reducing
  each worker's own individual throughput; every worker ends up taking
  longer and earning less per hour, while the client gets **no** actual
  speed benefit. In larger apartments (100-150 m²), staggering two
  electrical crews (not simultaneously, in sequence) can work, but
  running many trades at once in one confined space still isn't
  feasible for the same crowding reason, plus incompatible working
  conditions (e.g. dust from grinding/plastering directly conflicting
  with a painter's need for a clean, dust-free environment nearby).
- **A stated tradeoff between narrow-specialist quality control and
  raw speed**: this company deliberately uses narrowly-specialized
  trade workers (electricians only do electrical, plumbers only
  plumbing, tilers only tile) plus a multi-level QC chain — foreman
  sign-off, then an independent technical-supervisor inspection, then
  client acceptance and payment (**no prepayment used at all**) —
  before the next trade enters. **This chain itself adds real time**
  compared to a "universal" 3-4-person crew working several trades in
  parallel with no unified quality standard between them — the
  explicit tradeoff stated: faster, but with materially weaker,
  inconsistent quality control. A real client anecdote is given
  directly: a client complained a previous company completed their
  100 m² apartment in 2 months five years earlier, versus this
  company's own 4-month quote for a 50 m² apartment (double the time
  for half the area) — explained by this standardization/QC-chain
  tradeoff, not denied as implausible.
- **A named, previously-undocumented equipment-based throughput
  driver**: this company's stated productivity relies partly on
  professional equipment (mechanized plastering, mechanized screed
  pumps, professional dehumidifiers, professional rotary
  hammers/demolition hammers, wall-chasers, tile cutters) that
  materially compresses labor time versus manual-tool execution —
  framed as a real, equipment-driven throughput lever distinct from
  crew-count or specialization.

## Mistakes / Warnings — Two Named Timeline-Specific Contractor-Scam Mechanisms

- **⚠️ Scheme 1 — the "sunk-cost illusion of choice" deadline trap, a
  genuinely new mechanism distinct from this channel's own Round 11
  scam catalog**: a company quotes an artificially short headline
  timeline (worked example: 3 months) specifically because by the time
  that deadline arrives, 65-70% of the *most profitable* work (rough
  stages: plastering, electrical, plumbing, screed, tile) is already
  complete — the company is genuinely comfortable if the client fires
  them at that point, since the remaining, least-profitable finish work
  is exactly what they'd rather not do anyway (the same underlying
  economics as Round 11's rough/finish bait-and-switch, but expressed
  through *timeline* pressure rather than *pricing* structure). The
  client is left facing only two options — extend the contract by
  (typically) another 2 months, or fire the contractor and start over
  with someone else who inherits an unappealing, half-finished,
  already-picked-over object — an "illusion of choice," not a real one.
- **⚠️ Scheme 2 — inflated day-counts on small change-order items,
  compounding Scheme 1**: additional/change-order work ("допы") is
  deliberately quoted with a day-count disproportionate to its actual
  cost/complexity (worked example: a single additional outlet costing
  only ≈1,000 RUB ≈$10 is quoted as requiring **2 full working days**)
  — accumulating enough of these inflated day-counts lets a company
  attribute a further 2-3 months of schedule slip entirely to "допы"
  the client themselves requested. **⚠️ A named legal-recourse
  limitation, not previously recorded in this store**: once a company
  has stated a day-count for a change order (even an inflated one) and
  the client accepted the change, courts are stated to generally side
  with the company that quoted a number in writing — a client isn't
  considered a qualified expert able to dispute the day-count after the
  fact, and disputing it (proving 2 days should have been 1) is
  described as expensive, slow, and unlikely to succeed even when the
  client is probably right.
- **⚠️ A concrete accuracy benchmark for this company's own smeta
  practice, distinct from the general smeta-review-service mentions in
  Round 11**: this company's own carefully-computed smetas grow by up
  to **≈10%** (commonly 5-7%) over a project's real course due to
  unavoidable additions — contrasted directly with a real worked
  comparison from its free one-time competitive smeta-review service: a
  competing company's smeta for the same underlying ≈1,000,000-1,100,000
  RUB (≈$11,100-$12,200) scope of work was quoted at **800,000 RUB
  (≈$8,900)**, already ≈30% under-counted *before work even started*,
  and grew a further ≈1.5× in practice to **1,200,000-1,300,000 RUB
  (≈$13,300-$14,400)** once real допы accumulated — a concrete numeric
  illustration of the scale gap between a properly-itemized smeta's
  natural growth and a deliberately lowballed one's eventual real cost.

## Assumptions / Uncertainties

- All figures (the 250,000 RUB/month throughput average, the 60-object
  dataset, the worked scam examples) are this speaker's own stated
  internal analysis, `single-account`/`unverified` — not independently
  audited.
- Currency conversions use the trailing-6-month USD/RUB mean before the
  confirmed 2024-10-28 upload date (90.3098 RUB/USD), rounded per this
  project's bucket convention (nearest $10 below $1,000, nearest $100
  from $1,000-$99,999).
- Region: level 2 (Moscow/Moscow-region channel context), not
  independently re-confirmed spoken in this specific video.
- Checked directly against this vault's existing
  `Project_Duration_and_Scheduling.md` (four turnkey-company duration
  sources, all converging on a 6-9-month headline range for a
  design-project renovation) — **no direct numeric overlap or
  disagreement found**: this video doesn't state its own headline
  month-range for a "typical" apartment, instead offering a *formula*
  (throughput ÷ smeta total) that a reader would need their own smeta
  total to apply — genuinely complementary to, not duplicative of, the
  existing page's headline-range sources.

## Target Page(s)

- **`11_Budget_and_Planning/analysis/Project_Duration_and_Scheduling.md`**
  — the two failed heuristics (room-count, complexity-coefficient), the
  throughput-based duration formula and its 250,000 RUB/month
  benchmark, the two annual dead-zone periods, and the crowding-out/
  narrow-specialist-QC tradeoff mechanism.
- **`11_Budget_and_Planning/Budgeting_Guide.md`** §4 or
  `analysis/Estimate_and_Contract_Templates.md` — the two named
  timeline-specific scam schemes (sunk-cost illusion-of-choice deadline
  trap, inflated change-order day-counts) and the courts-favor-the-
  quoting-company legal-recourse limitation.

## Relevance to This Project's Topic

High — the first source in this store to propose (and honestly report
testing and rejecting two alternative approaches before arriving at) a
concrete, data-derived duration-estimation *method*, directly usable
once this project has its own labor-only smeta total, plus two
genuinely new timeline-specific contractor-scam mechanisms distinct
from this channel's existing smeta-wording-fraud catalog.
