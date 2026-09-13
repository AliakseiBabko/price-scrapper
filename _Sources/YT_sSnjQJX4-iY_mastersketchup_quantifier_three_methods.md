---
source_type: video transcript (SketchUp-education channel, vendor-extension walkthrough built around a real personal decision)
source_url: https://www.youtube.com/watch?v=sSnjQJX4-iY
video_id: sSnjQJX4-iY
transcript_file: _Archive/processed_sources/20260913_mastersketchup_quantifier_three_methods_f0297189.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions - ORIGINAL language)
upload_date: 2020-07-20 (confirmed via yt-dlp metadata)
channel: MasterSketchUp (Matt Donley)
source_title: "Create an accurate material take-off with costs using Quantifier Pro"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Quantities / Measurements`, `Cost Drivers`)
fact_yield: 9
promotional_ratio: medium
corroborates_existing: true
region: n/a_US_market_no_jurisdictional_claim
delivery_model: n/a - a software walkthrough, not a renovation source
---

# Source Note - MasterSketchUp: Three Cost-Attachment Methods, and a Build Cancelled by a Partial Estimate (YouTube sSnjQJX4-iY)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this was processed, and what makes it better than its companion

Same Tier 2 justification as [[_Sources/YT_MZv33G7UE_A_mindsight_quantifier_pro_material_reports|MZv33G7UE_A]] - read for schema thinking against this project absent quantity-to-price join. **What makes this the stronger of the pair: it is not a demonstration model. It is his own build, and the estimate CHANGED HIS DECISION.** `promotional_ratio: medium` rather than high for the same reason - the extension is the instrument, not the subject.

**⚠️ 2020, US, COVID-era** (he notes 3D Basecamp was cancelled). **Every price is discarded under standing rule 2.**

## ⚠️⚠️ Durable Facts - Three Cost-Attachment Methods, and What Each Is For

**This is the schema detail the companion video only implies.** Cost can be attached three ways, and **the choice determines what a change re-prices**:

1. **⚠️ The OBJECT method - a flat cost on a selected object.** Critically: **applied to a component, every copy of that component inherits the cost.** For one-offs and for repeated identical items. His instances: an **$800** trailer, a **$2,000** sandblasting-and-paint job.
2. **⚠️⚠️ The LAYER/TAG method - cost attached to a tag, and it supports FOUR calculation bases: LENGTH, AREA, VOLUME, or WEIGHT.** So one tag priced per-metre handles all studs; another priced per-square-foot handles siding, paint or roofing; volume handles concrete or insulation; weight requires a density input.
   - **⚠️ How LENGTH is derived, and it is a real gotcha: the extension takes the LONGEST AXIS of the group or component bounding box.** He demonstrates it on a joist, noting the geometry is axis-oriented. **→ A group whose longest bounding-box edge is not the member length will be mis-measured.** This is the same class of hazard as this vault own rule that a bounding box is not the shape - see `dxf_wall_entities.py`, which exists because two gates each reduced a polyline to its bounding box.
3. **The MATERIAL method** - covered in the companion note; prices by named material across the model.

**Cost-line fields, consistent with the companion**: a **cost code** (he notes you can follow your own cost-code template or system), description, calculation basis, unit cost, **waste %**, **tax %**.

## ⚠️⚠️ Rules / Heuristics - Waste Percentage, and the Sharp Disagreement With This Vault

**He states precisely when a waste percentage is the right instrument**: *"the waste percentage comes in handy when you're calculating materials like studs where you know you're going to have some cut off and you can estimate a certain percentage of waste that you want to factor in."*

**⚠️⚠️ And that is exactly the case this vault already holds a BETTER answer for.** `Bill_of_Quantities_and_Procurement.md` §5a-quinquies records Vasily_Sanuzel deriving a **cutting plan** from his model: a spreadsheet takes each required piece length and count and returns both the stock lengths to order and **how to cut each one**. Result on a large framing package: **38 x 3 m lengths ordered = 114 m, ~113 m consumed, 86 cm total offcut waste - under 1%.** That page already says so in terms: *"the concrete answer to the waste-allowance question that every material line on this page otherwise handles with a percentage."*

> **→ The synthesis neither source states, and it is the finding: WASTE ALLOWANCE IS NOT ONE NUMBER - it is a function of whether the material NESTS and whether you control the cutting.**
>
> - **Linear stock you cut yourself** (profiles, studs, skirting, pipe) - **nest it and the percentage collapses toward zero.** A flat 7-10% here is money left on the table.
> - **Tile, sheet goods, anything with breakage, edge cuts or pattern matching** - **a percentage is unavoidable**, because you cannot nest ceramic the way you nest 3 m profiles.
>
> **So a cost engine needs waste as a per-resource property with a METHOD attached, not a single global rate.**

## ⚠️⚠️ The Finding That Is Not About Software

**He modelled a tiny office he intended to build. The running cost reached $5,300 with NO SIDING, NO ROOFING, NO INTERIOR SURFACES AND NO ROOF.** He concluded it would land near **$10,000**, decided it was not worth it, and **abandoned the build** - renting an existing office instead. The sandblasting quote (**$2,000** minimum, against **$2,800** for a ready-to-go trailer) is what he names as pushing him over the edge.

- **⚠️⚠️ A DECISION WAS CHANGED BY A DELIBERATELY INCOMPLETE ESTIMATE, AND THAT IS THE POINT.** The model was a work in progress and the estimate was missing its most expensive remaining items - **and it was still decisive, precisely because it was already over budget before those were added.**
- **→ The rule worth carrying: a cost model earns its keep by KILLING A BAD OPTION EARLY, not by producing a precise final number.** An estimate that is incomplete in a known direction is actionable; it only has to be good enough to cross a threshold.
- ⚠️ **Directly relevant to this project own framing.** The gap analysis already concluded that the model job *"is not to be dimensionally exact - it is to hold quantities stable enough that a substitution re-prices correctly."* **This is the same conclusion reached from the other end: precision is not what makes an estimate useful.**

## Durable Facts - The Native Capability, and Why It Is Not Enough

- **SketchUp Pro has native "advanced attributes" including a PRICE field, plus File -> Generate Report with customisable reports.** He confirms it works - *"you can use this feature"* - but calls it **"really limited... not nearly as flexible."**
- **→ Worth recording as a general caution rather than a product verdict: a native price field that cannot aggregate by tag, material, length, area, volume and weight is a price field, not a cost engine.**
- **⚠️ A practical naming convention worth stealing: he prefixes pricing tags with `PR`** (e.g. `PR 2x6 spruce`) **so pricing tags are distinguishable from modelling tags at a glance**, and the tool itself shows a `$` prefix against any tag carrying a cost. **A cheap, legible way to keep a costing layer separate from a geometry layer in a shared namespace.**

## Numeric Data - Recorded, Then Discarded

$800 trailer; $2,000 sandblasting; $2,800 comparable ready trailer; $5,300 partial running total; ~$10,000 projected; ~$120 on a floor-joist group. **All US 2020 retail, no city named. Discarded for comparative use under standing rule 2; recorded only because the RATIO between $2,000 to refurbish and $2,800 to replace is what carried the decision, and that ratio is the transferable part.**

## Confidence & Evidence Notes

- **`single-account`.** ASR is poor on punctuation (lower-case throughout, no sentence breaks) and mangles the product as "quanah fry"/"quantifier"; "coven" for COVID. **Figures heard once are candidates.**
- **`corroborates_existing: true`** for model-derived take-off; **the waste disagreement with §5a-quinquies is the productive part and is routed as a synthesis, not as a conflict to resolve.**
- **⚠️ 2020 software behaviour** - he notes layers had already been renamed tags and the extension had not caught up. **UI specifics are not routed.**
- **No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join.md` (NEW PAGE)** - the three attachment methods, the four calculation bases, the longest-axis gotcha, the `PR` tag convention, and the native-versus-extension caution.
- **`11_Budget_and_Planning/analysis/Bill_of_Quantities_and_Procurement.md`** - the waste-is-not-one-number synthesis, placed against §5a-quinquies which already holds the nesting half.
- `_Knowledge/store/Rules_Heuristics.md` - "a cost model earns its keep by killing a bad option early, not by producing a precise final number."
- **5b**: every figure is US 2020 and deliberately not converted.
