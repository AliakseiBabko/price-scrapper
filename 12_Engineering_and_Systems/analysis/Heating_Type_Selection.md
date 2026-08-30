# Heating — Underfloor Heating Type Selection

Part of [[12_Engineering_and_Systems/Heating|Heating]].

> [!NOTE]
> `single-account`, one practitioner's own stated field experience and comparison, not independently cross-verified against manufacturer specs or a second channel. [source: [[_Sources/YT_8RIyq8nZ9EQ_underfloor_heating_type_comparison_097|note]]]

## Naming Clarification

Zemstandart/Zemsproekt (Alexey Zemskov) explains: "Water" underfloor heating is more accurately "liquid" (жидкостной) — the heat-transfer medium is often antifreeze, not pure water. Both "electric" and "film" (infrared) types are technically electric, but have fundamentally different heating mechanisms: direct-heating electric cable/mat resistively heats the element itself; film/infrared heats via radiated waves that warm whatever sits above the film, not the film's own temperature primarily. The two shouldn't be conflated despite both being "electric."

## The Ten-Parameter Comparison

| Parameter | Water | Electric | Film/Infrared |
| :--- | :--- | :--- | :--- |
| Installation complexity | Hardest (historically) — modern push-fit fittings + rentable crimping tool have closed most of the gap; the "hard to install" reputation is argued to be largely a plumber fee-inflation myth as of 2018-2019 | Second | Easiest |
| Durability (rated life) | 50 years | 15 years | 15 years |
| Reliability (% surviving to end of rated life) | ~100% | ~40% | ~70% |
| Repairability (of the heating element specifically) | Low (embedded in screed) | Essentially none (embedded, breaking out required) | High — remove baseboard, lift floating floor, replace section |
| Heat-up time | Slowest (must warm the full screed mass) | Intermediate | Fastest (~5 min under a thin covering like linoleum) |
| Cool-down time | Slowest — best for continuous operation | Intermediate | Fastest — best for intermittent/on-demand use |
| Running cost | Cheapest | Most expensive | Second cheapest |
| Finish-flooring compatibility | Any covering | Any covering | **Never** ceramic tile; **never** metal-backed premium laminate; poor with cork |
| Wet-room compatibility | Unrestricted | Unrestricted | **Categorically prohibited** — exposed electrical connections, real shock risk on any water ingress |
| Legal status in a standard apartment | **Effectively illegal** (see below) | Unrestricted | Unrestricted |
| Noise | Silent (audible noise = trapped air needing bleed; a forced-circulation pump is never fully silent — site it as far from occupied space as practical) | Silent | Silent |

## Why Water Underfloor Heating Is (Almost) Never an Option in an Apartment

Two independent legal restrictions, both applying regardless of one-pipe or two-pipe central-heating scheme:

1. **Cannot be connected to a central-heating system at all.** [source: [[_Sources/YT_8RIyq8nZ9EQ_underfloor_heating_type_comparison_097|8RIyq8nZ9EQ_underfloor_h]]]
2. **Cannot be installed above another unit's living space** — i.e. above a neighbor's ceiling. [source: [[_Sources/YT_8RIyq8nZ9EQ_underfloor_heating_type_comparison_097|8RIyq8nZ9EQ_underfloor_h]]]

The only real exception is an individually-metered, individually-heated ground-floor unit — the source's own estimate puts this under 1% of cases. This single constraint is why water heating, despite ranking best on nearly every other parameter in the table above, is described as "almost never usable in an apartment" — it's realistically a private-house-with-individual-heating option only.

## Film's Two Categorical Incompatibilities, With Mechanism

- Zemstandart/Zemsproekt (Alexey Zemskov) warns: **Ceramic tile**: the film layer physically prevents tile adhesive from bonding to the base beneath it. Perforated film variants exist specifically to address this, but the perforated area is too small in practice — tile still detaches.
- Zemstandart/Zemsproekt (Alexey Zemskov) warns: **Metal-backed premium laminate**: some premium laminate lines include a metal foil layer. Heating a metal-backed laminate on film is functionally equivalent to putting metal in a microwave.

## Furniture Placement

Never place furniture directly over active underfloor heating of any type. For water and electric, this is an efficiency/cost concern (wasted heating under something that doesn't need it) — neither type gets hot enough to actually damage furniture. Film is different: it heats by radiating waves upward, and furniture sitting directly in that radiation path can genuinely overheat and be damaged, not just waste energy.

## ⚠️ Due Diligence When Buying a Unit With Claimed Underfloor Heating (added 2026-08-19)

> [!NOTE]
> A genuine consumer-fraud finding, distinct from the type-selection/technical content above. [source: [[_Sources/YT_o7lGqaUuGm0_fake_renovation_scam_walkthrough_214|note]]]

Zemstandart/Zemsproekt (Alexey Zemskov) documents: **A documented real case of fabricated underfloor heating**: buyers of a "renovated, move-in-ready" unit specifically asked about underfloor heating before purchase (they couldn't tolerate cold tile underfoot) and were shown three apparently-functioning thermostats, one per zone. After moving in, activating the thermostats caused sparking. Investigation found: the thermostats received line power and produced no fault when idle, but their output leads were simply short-circuited together with no heating cable connected anywhere — confirmed with a cable detector swept across the entire tiled area, which found nothing. When contacted, the sellers' own proposed "fix" was to swap the fake thermostats for ordinary wall outlets.

Zemstandart/Zemsproekt (Alexey Zemskov) advises: **Practical takeaway: a visible, apparently-working thermostat is not evidence of a working heating system underneath it.** Before treating claimed underfloor heating as a real, valuable feature of a unit being purchased (new or resale), verify it independently — run a cable/stud detector across the floor, or ask to see the system actually heating the floor to a measurable temperature, rather than accepting a thermostat's presence or a seller's verbal claim.

## Named Film Exception, and Electric Cable Sub-Taxonomy (added 2026-08-24, Round 3)

Konstantin Kruglov / Ontario adds a named-brand exception and a sub-taxonomy within "electric" underfloor heating:

- **⚠️ Named exception to the film-can't-go-under-tile rule above**: manufacturer **Oriental Dream** makes a film/infrared product explicitly rated for tile and other adhesive-set finishes, unlike the ~99% of film products restricted to floating floors. `single-account`, `unverified`.
- **Two distinct electric cable-based products, same underlying twin-conductor cable technology**: **thick bare cable (6.7mm)**, embedded ~3cm into the screed, field-adjustable power density by installation spacing (180-450 W/m²), unconstrained by any fixed mat width — but slower to heat (must pass through the full screed + adhesive + tile stack). **Thin cable pre-mounted on a mesh mat (2.8mm)**, sold pre-sized with its own reinforcing mesh and sensor conduit, easier to install for a standard area, but capped lower (130-300 W/m², brand-dependent) and constrained by the mat's fixed width. **⚠️ A mat-based heating cable must never sit directly under laminate with no screed/adhesive layer above it** — it always needs its floated compound layer regardless of finish type.
- **Power-density selection guide by use case**: 130 W/m² — too weak, not recommended for any use; 180 W/m² — practical minimum for a heated tile-covered room (kitchen, hallway, WC); 210 W/m² — recommended specifically for a heated towel wall (an electric-cable alternative to a standard towel warmer); 300 W/m² — reserved for cold, unheated spaces only (an unglazed/uninsulated loggia or balcony).

[source: [[_Sources/YT_Is76QlotVFE_kruglov_underfloor_heating_hydronic_electric|Is76QlotVFE]]]

## Thermostat Buying Taxonomy (added 2026-08-24, Round 3)

Konstantin Kruglov / Ontario gives four independent classification axes, useful as a buying checklist: control interface (mechanical dial, touchscreen, or buttons); programmability (simple on/off+setpoint vs. a full weekday/weekend schedule); connectivity (smartphone-app control — check per model, since visually-identical units sometimes differ only in this); and **⚠️ sensor dependency, a real failure-mode distinction**: a standard thermostat relies entirely on its own wired floor sensor — if that sensor later becomes embedded/inaccessible and fails (sealed under finished tile with no access), the whole heating system stops working until either the thermostat is replaced for a sensorless-capable model or the flooring is broken open to replace the sensor. Some models include a built-in air-temperature sensor as a fallback — less precise, but keeps heating functional if the floor sensor fails. **Prefer a thermostat with air-sensor fallback as insurance against this failure mode.** [source: [[_Sources/YT_Is76QlotVFE_kruglov_underfloor_heating_hydronic_electric|Is76QlotVFE]]]

## ⚠️ Perspectives — Electric Cable Floor Lifespan Disagreement (added 2026-08-24, Round 3)

Two single-account sources give different service-life figures for
electric-cable underfloor heating specifically — flagged as an open
disagreement, not resolved in favor of either:

- **Konstantin Kruglov / Ontario**: ~15 years.
- **Петришин-Строй**: ~25 years.

Both sources agree on water floor (~50 years) and film floor (~15
years), so the disagreement is specific to the electric-cable figure.
Neither source cites an independent testing standard or manufacturer
spec sheet — treat the true figure as unresolved pending a
manufacturer-sourced or third independent practitioner account, rather
than defaulting to either number. [sources: [[_Sources/YT_Is76QlotVFE_kruglov_underfloor_heating_hydronic_electric|Is76QlotVFE]], [[_Sources/YT_xt_q5SkINT8_petrishin_heated_floor_comparison|xt_q5SkINT8]]]

## New Legality Nuance, Real Payback Economics, and Wood-Covering Thermal Mechanism (Петришин-Строй, added 2026-08-24, Round 3)

Region level 2 (channel-only Moscow association). Low promotional
ratio. Heavy structural overlap with the existing 10-parameter table
above (not re-extracted) — only genuinely new content below.

- **New legality exception for water/liquid underfloor heating**: also
  permitted in a new-build specifically designed with separate
  dedicated risers for underfloor heating — distinct from the existing
  <1%-of-cases individually-metered-ground-floor-unit exception.
  **Sharper mechanism for the illegal-hookup consequence**: connecting
  to a shared central-heating riser without authorization also disrupts
  the hydraulic balance of the entire riser line, not just a paperwork
  violation.
- **⚠️ Install cost vs. running cost, with a real payback figure**: water
  floor is the most expensive to install but, run on mains gas or a
  wood boiler, roughly **5× cheaper to operate** than any electric
  floor (cable or film) — electricity tariffs are the most expensive
  energy source in this comparison. In a permanently-occupied house,
  the higher install cost is recouped in roughly **3 years** via gas
  savings, saving "tens of thousands of RUB" annually thereafter.
  Electric floor is cheaper to install but pricier to run — reasonable
  for a weekend/seasonal dacha, financially poor for permanent
  full-house heating.
- **Bitumen-insulated-contact mechanism for film's wet-room
  prohibition**, more specific than "exposed electrical connections":
  film's electrical contacts are protected only by bitumen insulation —
  water ingress causes a short circuit and real shock risk.
- **Planning-sequence rule**: draw the furniture-placement floor plan
  *before* designing the heated-floor layout, not after.
- **Thermostat energy-saving figure**: using a thermostat instead of a
  fixed constant setting saves **up to 30%** of energy consumption.
- **Room-by-room combination strategy for an apartment**: film floor
  under floating coverings in living spaces (fast, on-demand comfort
  heating); electric cable floor under tile in wet/utility zones
  (bathroom, kitchen, balcony).
- **⚠️ General thermal-conductivity mechanism, broader than the
  existing "film can't go under laminate" rule**: laminate, engineered
  board, and solid wood all conduct heat poorly (heated-nail-vs-lit-
  match analogy) — heating *any* underfloor-heating type under a thick
  wood-based covering is largely pointless regardless of the heating
  technology, since the covering itself blocks most heat from reaching
  the surface. Recommendation: pair heated flooring with tile,
  porcelain tile, quartz-vinyl, or linoleum instead, and always confirm
  the covering manufacturer's own heating-temperature limit first.
- **⚠️ Same-account restatement, not independent corroboration**: this
  source's own quartz-vinyl-over-heated-floor failure account (cupping,
  squeaking, manufacturer denial) is the same incident already recorded
  from this channel's `Qt4uGvGRYT0` (loggia insulation) source — the
  same company retelling the same real case, not a second data point.
  [source: [[_Sources/YT_xt_q5SkINT8_petrishin_heated_floor_comparison|xt_q5SkINT8]]]

## Electric-Floor Operating-Cost Formula, and a Second Independent Water-vs-Electric Cost-Gap Estimate (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, added 2026-08-28, Round 4)

Low promotional ratio, general explainer. [source: [[_Sources/YT_9ndMjQLTF9E_sbk_heated_floor_downsides|YT_9ndMjQLTF9E]]]

- **⚠️ Named operating-cost formula, distinct from this page's existing cost/payback figures**: (area m²) × (mat power density W/m², real examples 130-180 W/m²) × 0.4 (derating for mandatory wall/heat-source/furniture clearance) = draw. Worked example: 30 m² × 180 W/m² × 0.4 ≈ 2 kW; at ~9h/day average active cycling ≈ 20 kWh/day; at 4.5 RUB/kWh ≈ 90 RUB/day, ≈2,500 RUB/month (≈$30) for one 30 m² zone. Scaled: a 100 m² apartment on underfloor heating costs at minimum ≈7,000 RUB/month (≈$80) in electricity.
- **⚠️ A second, independent water-vs-electric primary-heating cost-gap estimate, corroborating this page's existing Petrishin-Stroi ~5x figure with a different worked example**: for a 200 m² house, electric underfloor heating as the *sole/primary* heat source is estimated at ≈35,000-40,000 RUB/month (≈$390-$440), versus ≈3,000-5,000 RUB/month (≈$30-$60) for the equivalent water-based (gas-fired) system — roughly a 7-10x gap, somewhat higher than Petrishin-Stroi's 5x figure but the same conclusion: electric floor heating belongs in supplemental/wet-zone roles, never as a house's primary heat source.
- **A distinct thermostat-wattage area cap** (as opposed to a mat/zone-sizing convention) is documented on [[07_Bathroom/analysis/Heated_Floor_and_Thermostat|Bathroom: Heated Floor & Thermostat]] — a standard thermostat's ≈3.5 kW average power limit caps single-thermostat coverage to ≈20 m² at 180 W/m² mat density.

## Brand Tier Reference (added 2026-08-24, Round 3, self-reported market survey)

Konstantin Kruglov / Ontario, self-described own market survey (multiple retailer/installer calls) — **economy/comfort tiers are explicitly hearsay** from that survey, not the source's own hands-on experience; **premium tier reflects direct hands-on work**: Economy — Warmstat, Teplolux/Tropix (both claimed Russia-made). Comfort — Atom Standart (Russia), ART Basic (claimed Poland). Premium — **Thermo** (Sweden; source disputes a rival retailer's claim that production moved to China) and **DEVI** (considered historically even higher-ranked than Thermo, but reportedly exiting/reducing this market — limited stock or a 2-3 month parallel-import wait); Thermo and DEVI are named the market's two leading premium brands, Thermo currently easier to obtain. Atom Premium and Hertz (Extra line, claimed German manufacture) also mentioned by retail contacts as premium but **explicitly flagged by the source as hearsay, never personally used**. `single-account`, mixed direct/hearsay evidence as noted per brand. [source: [[_Sources/YT_Is76QlotVFE_kruglov_underfloor_heating_hydronic_electric|Is76QlotVFE]]]
