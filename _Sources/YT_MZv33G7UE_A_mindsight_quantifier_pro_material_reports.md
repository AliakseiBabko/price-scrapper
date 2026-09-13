---
source_type: video transcript (SketchUp-education channel, vendor-extension tutorial with an affiliate link)
source_url: https://www.youtube.com/watch?v=MZv33G7UE_A
video_id: MZv33G7UE_A
transcript_file: _Archive/processed_sources/20260913_mindsight_quantifier_pro_material_reports_9e64c473.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions - ORIGINAL language)
upload_date: 2025-10-16 (confirmed via yt-dlp metadata)
channel: mind.sight.studios
source_title: "Quantifier Pro - estimate materials and budget inside SketchUp (for interior designers)"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Quantities / Measurements`)
fact_yield: 8
promotional_ratio: high
corroborates_existing: true
region: n/a_US_market_no_jurisdictional_claim
delivery_model: n/a - a software tutorial, not a renovation source
---

# Source Note - mind.sight.studios: Quantifier Pro, and Where a Cost Attaches in a Model (YouTube MZv33G7UE_A)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this was processed

**Flagged on 2026-09-08 as a Tier 2 single and left for a later round, on the grounds that it bears on THE ONE GENUINELY ABSENT TOOL in this project toolchain - a quantity-to-price join.** The [gap analysis](../_Inbox/planning/toolchain_gap_analysis_20260908.md) §B Kind 2 verified by grep that **no quantity-to-price join exists anywhere in this repo.** The batch processed earlier today closed with that gap still open. **This source is read purely for its SCHEMA THINKING** - how a model quantity becomes a priced line - and every figure in it is discarded as US 2025 retail under standing rule 2.

`promotional_ratio: high`: it is a vendor-extension tutorial with the purchase link given twice. **The schema is visible on screen throughout, which is why the promotional frame does not prevent extraction.**

## ⚠️⚠️ Durable Facts - Where a Cost Attaches, Which Is the Design Question

**Cost is not attached per line. It is attached to one of four ENTITY CLASSES: tags, materials, objects, and models.** That is the single most useful structural fact in the source, because it decides what a price change re-prices.

**The per-entry fields, enumerated from the dialogue**: a **code** (his example `TL` for tile), a **description**, a **unit basis** (e.g. square footage), a **factor** (shown as 1), a **unit cost**, a **waste percentage**, a **tax percentage**, and a free **comment**.

- **⚠️⚠️ WASTE AND TAX ARE FIRST-CLASS FIELDS ON EVERY COST LINE, NOT AN AFTERTHOUGHT.** Worked example: a 12x12 tile at **$7** per square foot, **7% waste**, **13% tax**. **This project cost-engine design does not mention a waste factor anywhere** - see the routing note below. **That is a genuine gap this source exposes in our own design, and it is the most actionable thing here.**
- **⚠️ Cost data must be entered by hand and the tool says so** - "because this information can vary, this is something that you have to add manually." **The extension derives QUANTITIES automatically and prices NOTHING automatically.** That division is exactly the one the gap analysis already assumes (rates come from market quotes via `data/scraper.db`, not from the model).

## ⚠️ Rules / Heuristics - Material-Keyed Cost Is a Partial Substitution Axis

**A material report lists every material in the model with its total surface area, aggregated wherever that material appears** - "wherever this material is applied in your model, this is the combined surface area for that specific material." Named instances: wall paint scattered across different walls, bathroom tile, bedroom carpet, wallpaper, wooden floor.

- **⚠️⚠️ Because cost attaches to the NAMED MATERIAL, changing one unit price re-prices every surface carrying that material in a single edit.** → **That is a partial implementation of the substitution axis the owner defined as this cost engine PRIMARY requirement**: a discontinued tile should be a one-line swap that re-prices, not a re-modelling exercise. **Partial, because it keys on the material rather than on a ROLE** ("the floor tile in room 04") - so it cannot express two different products serving the same role, nor re-point a role at a new product while keeping history.
- **Quantities update automatically when the model changes**, demonstrated: wallpaper went from **182 sq ft to 148 sq ft** on a model edit and the report followed.

## Rules / Heuristics - The Prerequisite Discipline

**Stated up front as a precondition, before any quantity is trustworthy: the model must be ORGANISED.** Three specific requirements:

1. **Geometry separated into groups**, per surface type.
2. **Tags assigned and used** - floors, 3D objects, furniture, decor each on their own tag, switchable.
3. **⚠️ Materials PROPERLY NAMED** - "this is going to make it easy for Quantifier Pro to recognize the objects and materials in your model and also extract information."

- **→ The general form, and it is the part that transfers to a project using no SketchUp at all: a take-off is only as good as the naming and grouping discipline applied while modelling. The quantity engine does not impose structure; it exposes whether you had any.** ⚠️ **Directly relevant to `data/canonical/`, where the equivalent discipline is the element taxonomy and the `structural_element_id` scheme.**
- **Units and precision are configurable per report** (length, area, volume, weight), set before reporting rather than per line.

## Numeric Data - Recorded, Then Discarded

- Total worked example project: **~$14,411**, of which **~$1,600 tax**; floor tile line **~$1,400**; dining chairs **$90 each**; combined floor area **1,071 sq ft**.
- **⚠️ ALL FIGURES DISCARDED FOR COMPARATIVE USE under standing rule 2** - US market, 2025, no city named, and a demonstration model rather than a real project. **They are recorded only to show what the report OUTPUTS, not what anything costs.**

## Confidence & Evidence Notes

- **`single-account`, vendor tutorial.** No claim is independently verified and none needs to be - the schema is observable.
- **ASR**: good. Repeated "[music]" artefacts and "furnitureures" for furniture.
- **`corroborates_existing: true`** - the vault already holds a model-derived take-off from a Russian practitioner (`Bill_of_Quantities_and_Procurement.md` §5a-quinquies). **This is the commercial-tool version of the same move, and the two disagree productively about waste - see that page and the new toolchain page.**
- **No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join.md` (NEW PAGE)** - the attachment-point model, the cost-line fields, waste/tax as first-class, the naming prerequisite.
- `11_Budget_and_Planning/analysis/Bill_of_Quantities_and_Procurement.md` - a cross-reference only; that page keeps the practitioner take-off.
- `_Inbox/planning/toolchain_gap_analysis_20260908.md` - **⚠️ the waste-factor omission in our own design, flagged for the owner.**
- **5b**: every figure is US 2025 and deliberately not converted; no comparable figure is carried.
