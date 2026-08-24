---
source_type: video transcript (single-speaker practitioner explainer, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=S4fOYedAruE
video_id: S4fOYedAruE
transcript_file: _Archive/processed_sources/20260824_sidorik_sewer_installation_ep24_d6433db6.txt
fetched: 2026-08-24
upload_date: 2021-07-17 (metadata-confirmed via yt-dlp `upload_date`)
channel: Pavel Sidorik (individual finisher/plasterer/tiler/electrician practitioner) — `single-account`
regional_applicability: Belarus level 1 — two independent direct statements: (1) the pipe-cutting knife's price is stated in Belarusian rubles ("70-80 белорусских рублей"); (2) the sewage-pipe brand's cheapest dealer is named directly ("самая низкая цена в Минске в компании Архитерм... официальные диллеры этой канализационной системы в Беларуси"), located in Боровляны
currency: BYN — one price point (pipe-cutting knife, 70-80 BYN ≈ $27-$31 → rounded to ≈$30 at the trailing-6-month USD/BYN average of 2.5717 BYN/USD before the 2021-07-17 publish date, via `tools/pricing/currency_converter.py --pair USD/BYN --trailing-months 6 --before 2021-07-17`)
language: ru (clean, manually-created captions)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
fact_yield: 16
promotional_ratio: low (one named-dealer mention with a description link, presented as a genuine sourcing tip rather than a sponsor pitch)
corroborates_existing: true (extends Rough_Plumbing_Sequencing.md's drain-slope and two-45s rules with concrete worked numbers; extends Fixture_Stubout_Coordinates.md with a full new set of coordinates; extends the kitchen-outlet-count rule to the sewage/drain side)
---

# Extraction Note — Pavel Sidorik: New-Building Renovation A-to-Z, Episode #24 "Do-it-yourself sewer installation. Errors and solutions." (YouTube S4fOYedAruE)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Source Metadata

Confirmed numbered episode #24 (per the plan's channel manifest), continuing
the plumbing/sewer thread from the two unlabeled plumbing episodes
processed earlier this round. Upload date 2021-07-17, 17 days after the
second plumbing episode (2021-06-30) — consistent sequencing. Covers:
full fixture stub-out marking/heights for the bathroom+toilet, chase
(штроба) sizing rules, cutting-tool technique across two different wall
materials, a named German sewage-pipe brand and its Belarus dealer, the
core slope/corner assembly rules with worked numeric examples, pipe-
cutting/deburring/lubrication technique, and a full room-by-room walk of
the assembled sewage system (washing machine, sink, tub, toilet-node,
installation-frame 90mm transition).

### Region note (checked explicitly per this round's brief)

**Clears level 1 via two independent signals**: a pipe-cutting knife's
price is stated directly in Belarusian rubles ("70-80 белорусских
рублей"), and the sewage-pipe brand's cheapest dealer is named with its
location ("самая низкая цена в Минске в компании Архитерм... они
находятся в Боровлянах... официальные диллеры этой канализационной
системы в Беларуси" — "the lowest price is in Minsk at the Architerm
company... they're located in Borovlyany... they're the official dealers
of this sewage system in Belarus"). Both statements are about this
project's own sourcing/purchasing, not incidental channel branding.

## Quantities / Measurements — Fixture Stub-Out Heights (New Coordinate Set)

A full, concrete stub-out coordinate set for this bathroom+toilet layout
(heights from finished floor, accounting for future screed+tile
thickness even though no screed exists yet at marking time):

- **Washing machine**: drain 72 cm, water supply 60 cm.
- **Under-countertop sink with wall cabinet**: water supply 57 cm, sewage
  54 cm.
- **Shower mixer**: 20 cm above the tub rim, centered.
- **Toilet-room sink**: water supply 66 cm, sewage 61 cm.
- **Hygienic shower**: 65 cm.
- **Towel warmer**: relocated into the bathroom, centered on the future
  tub's position.
- **Electrical outlets placed above the water/sewage lines** at this
  cluster, specifically so a leak can't reach them from below.
- **General lookup heuristic for standard fixture placement figures**:
  search "сантехника, разметка, размер" (image search) for widely-shared
  reference diagrams, and always cross-check against the actual
  equipment's own installation manual before finalizing. `single-account`
  but a reusable planning-research method.

This set is a genuinely new, independent coordinate reference — extends
`12_Engineering_and_Systems/analysis/Fixture_Stubout_Coordinates.md`
rather than duplicating it (different fixture heights/positions than the
page's existing reference, useful as a second real-world data point).

## Rough Plumbing / Mistakes — Chase (Штроба) Sizing

- **Size a chase to the connector/fitting's outer diameter, not the
  pipe's own diameter** — fittings are meaningfully wider/deeper than the
  pipe itself. Concrete worked numbers: 50mm pipe needs a chase sized for
  ~70mm connector clearance; a 20mm PP (polypropylene) pipe's fitting is
  roughly 40mm, so the chase should be at least 45mm, not 20mm; a 32mm
  pipe's fitting is roughly 45mm. **A genuinely reusable sizing rule**
  distinct from this store's existing chase-sizing content (which covers
  zashivka/duct-box clearance, not chase-vs-fitting sizing specifically).
- **Cut the chase with the correct slope built in, and it becomes a
  self-guiding jig for the pipe** — once the pipe sits in a correctly
  sloped chase, it physically can't shift out of that slope. Leave margin
  in both width and depth rather than cutting tight to the pipe/fitting's
  exact size.
- **Cutting tool and a real material-hardness surprise**: a concrete saw
  (бетонорез — essentially a large angle grinder with dust extraction, 6
  cm cut depth) was used throughout. Silicate block (the bathroom
  partition material) cut and chipped out easily — "practically the ideal
  material for bathroom partitions" for this purpose. **Red brick in an
  existing false wall was unexpectedly difficult** — described as
  fired/hardened, "as strong as concrete" — a self-inflicted problem
  since the practitioner had built that false wall himself earlier in
  the project. `single-account`.

## Materials — Named Sewage Pipe Brand, and a Buy-With-Margin Rule

- **Always buy sewage fittings with margin (extra), planning to return
  unused pieces** — especially important when connecting to an
  installation frame, where the exact fittings needed are hard to
  predict in advance.
- **German Ostendorf sewage-pipe system used throughout**: priced
  comparably to a Russian-brand equivalent but with better stated
  quality. Cheapest source found in Minsk at "Архитерм," the brand's
  official Belarus dealer (Borovlyany). **90mm sewage pipe is specifically
  useful for connecting to an installation frame** (matching the 90mm
  frame-outlet spec from the prior episode) but isn't always easy to
  find, since the market default is 110mm.

## Rough Plumbing — Core Slope & Corner Rules, With Worked Numbers

- **Drain slope rule, with a concrete worked example**: maintain 2 cm of
  drop per 1 linear meter of horizontal run. Worked example given
  directly: a washing-machine drain 3 meters from the toilet's sewage
  riser needs 6 cm of total slope over that run (2m → 4cm; 3m → 6cm, and
  so on). **A simple on-site slope-check technique**: cut a short spacer
  piece of pipe to the exact target drop (e.g. a 2cm piece for a 1m run)
  and hold it under the pipe's far end to verify the slope visually.
  Extends this store's existing drain-slope figures (previously only a
  Kruglov-sourced "~3cm per meter for 50mm pipe" figure) with an
  independent, differently-cited number — treat as two sources giving
  different but not necessarily contradictory slope figures (possibly
  reflecting different acceptable ranges or pipe diameters); don't average
  them without checking whether they're describing the same pipe size.
- **Corner rule reaffirmed, with an honest caveat**: prefer two 45°
  elbows over a single 90° for the lowest flow resistance — but explicitly
  "unfortunately not always possible," corroborating this page's existing
  two-45s rule while adding that the ideal isn't always achievable in a
  real build (see the washing-machine and sink worked examples below for
  concrete cases where 90° was used anyway, with a stated reason each
  time).
- **Kitchen (or any multi-fixture zone) sewage-outlet count: at least 2,
  ideally 3+ separate drain outlets** — a real worked example gives 4
  outlets (sink, dishwasher, air conditioner, reverse-osmosis filter) —
  an unused outlet can simply be capped later, so oversizing this is low-
  risk. **Extends this store's existing kitchen-outlet rule (previously
  documented for water-supply outlets specifically) to the sewage/drain
  side of the same wall.**

## Rough Plumbing — Pipe Cutting, Deburring, Lubrication

- **A dedicated rotary pipe-cutting blade tool costs 70-80 BYN (≈$30)** (a real,
  region-resolved price point, Belarus level 1) — described as "a bit
  pricey," especially since two separate blade sizes are needed for 50mm
  and 32mm pipe; **most plumbers instead just use an angle grinder** for
  this reason.
- **After cutting any pipe, always chamfer (fask) the outer edge and
  remove internal burrs** — skipping this leaves burrs that obstruct
  smooth flow and accumulate silt/sediment over time, eventually
  requiring the pipe to be cleaned out.
- **Use dedicated silicone lubricant for sewage-pipe joint assembly, never
  a substitute** — the speaker explicitly and directly pre-empts common
  substitute suggestions (liquid soap, petroleum jelly/vaseline,
  "grandma's homemade jam") as inadequate; the correct silicone lubricant
  is inexpensive ("costs literally nothing") and makes assembly
  meaningfully easier, especially for larger-diameter joints that can be
  physically impossible to seat dry. Corroborates and adds explicit
  substitute-rejection detail to this store's existing lubricant-choice
  content on `Rough_Plumbing_Sequencing.md`.

## Rough Plumbing — Worked Fixture-by-Fixture Routing Examples

- **Washing machine drain**: routed in 32mm pipe, not 50mm, because the
  washer's own drain hose is thinner than 50mm pipe would require and the
  machine has its own drain pump (gravity slope matters less here than
  for a gravity-only fixture). **A single 90° elbow is used here
  deliberately**, not two 45s, because achieving two 45s would require a
  wall/chase roughly twice as thick — an explicit, reasoned exception to
  the corner rule above, justified by the pump doing the work rather than
  gravity.
- **Sink drain**: transitions 32mm→50mm with the transition fitting
  turned *upward* so falling drain water doesn't splash back out; uses a
  45° elbow (not 90°) at the direction change so falling water is guided
  smoothly to the side.
- **Wall-protrusion cosmetic rule**: where a diameter transition happens
  right at the wall face, route the *smaller*-diameter pipe (32mm) through
  the wall face rather than the larger one (50mm) — the smaller pipe
  protrudes less from the finished wall.
- **Tub drain height-control warning**: don't set a tub's sewage stub-out
  too high — it must account for the screed and tile buildup still to
  come; setting it based on the current (unfinished) floor level risks
  needing an unnecessarily raised tub with no working drain slope once
  the floor is actually finished.
- **Toilet-room node**: carries two separate sewage lines — a 50mm line
  to the tub, and a 50mm-to-32mm transition line to the toilet-room sink
  — plus a 90mm line specifically for the installation-frame connection,
  which itself transitions to 110mm to join the main riser (matching the
  90mm installation-frame outlet spec noted in the prior episode).

## Advertising / Promotional Content

- The Ostendorf sewage-pipe dealer ("Архитерм," Minsk/Borovlyany) is named
  with a description-box link — presented as a genuine sourcing
  recommendation with a stated reason (lowest price found for this
  system), not a disclosed sponsor segment or affiliate-discount pitch
  (contrast with the prior episode's explicit Neptun promo-code call-out).
  Recorded as a commercial mention per this project's standing filter,
  but the underlying technical content (brand comparison to Russian
  equivalents, the 90mm-availability tip) is extracted as real market
  information above.

## Target Page(s)

- `12_Engineering_and_Systems/analysis/Fixture_Stubout_Coordinates.md` —
  the full new stub-out coordinate set.
- `12_Engineering_and_Systems/analysis/Rough_Plumbing_Sequencing.md` — the
  chase-sizing rule, the worked drain-slope example and slope-check
  technique, the corner-rule caveat, the extended kitchen-outlet rule, the
  pipe-cutting/deburring/lubrication technique, and all worked
  fixture-routing examples (washing machine, sink, tub, toilet node).
- General budgeting store (`Rules_Heuristics.md`) — the fixture-placement
  image-search research method.

## Relevance to This Project's Topic

Very high value — the densest single source this round: a full
independent stub-out coordinate set, several concrete worked numbers
(chase clearances, slope-per-meter with a spacer-gauge technique, outlet
counts), and multiple fixture-specific routing examples with explicit,
reasoned exceptions to the general corner rule (a meaningfully more
useful pattern than a flat rule with no exceptions noted). Belarus level 1
confirmed via two independent signals (currency, named dealer+location).

## Promotion self-check

Re-read in full after drafting. The full stub-out coordinate set, the
chase-sizing rule and self-guiding-jig observation, the cutting-tool/
material-hardness note, the buy-with-margin rule, the named pipe brand
and dealer, the worked slope example and spacer-gauge technique, the
corner-rule caveat, the extended kitchen-outlet rule, the pipe-cutting/
deburring/lubrication technique (including the explicit substitute-
rejection detail), and all four worked fixture-routing examples are
reflected in the target-page routing above. The named-dealer mention is
flagged as commercial per the Advertising section but its factual content
(brand comparison, 90mm availability) is retained.
