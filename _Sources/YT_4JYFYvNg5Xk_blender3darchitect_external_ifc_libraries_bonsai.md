---
source_type: video transcript (Blender-for-architecture channel, short how-to)
source_url: https://www.youtube.com/watch?v=4JYFYvNg5Xk
video_id: 4JYFYvNg5Xk
transcript_file: _Archive/processed_sources/20260913_blender3darchitect_external_ifc_libraries_bonsai_ec083355.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2026-05-27 (confirmed via yt-dlp metadata)
channel: Blender 3D Architect (Alan Rito)
source_title: "Blender Just Got Unlimited Doors & Windows - From a Revit Library, For Free (Bonsai BIM)"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 5
promotional_ratio: medium
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Alan Rito: External IFC Libraries into Bonsai - and ⚠️⚠️ a Schema Upgrade That Leaves a Deprecated Entity Behind (YouTube 4JYFYvNg5Xk)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## What it is

**A five-minute how-to on importing third-party IFC assets into Bonsai**, to escape the single door the demo template ships with. `promotional_ratio: medium` — the tutorial itself is clean, but **the last ninety seconds are a sales block**: two paid workshops, a 300-page rendering book, and a channel-membership pitch. **No product verdict is routed from it.**

⚠️ **This is `@blender3darchitect`, one of the two channels triaged in [[_Inbox/planning/bonsai_ifc_batch_20260913|this batch]]** — 151 videos, assessed there as **mostly not relevant** to a programmatic pipeline, with a named minority that is. **This video is in that minority.**

## ⚠️⚠️ 1. THE FINDING: the schema upgrade fixes the file version and leaves a deprecated ENTITY

He downloads a door from a manufacturer-asset aggregator, and Bonsai flags the file:

> *"**This file is using an old IFC schema.** You will see that Bonsai will highlight this here. **It's using IFC 2x3. We actually need an IFC 4.** But luckily for us, Bonsai will be nice enough to upgrade the file for us. So click this button here, **upgrade to IFC 4**."*

The upgrade runs and produces a new file. **Then the asset does not appear where a door should appear:**

> *"And here's something new. If you never did this before, **you will probably try to look for this new door type under here — and it won't show up as a door type.** Remember, when we browsed here on this object, **it's under DOOR STYLE, not DOOR TYPE.** So to access this object, you actually have to use here this **multi-object tool**."*

> **→ ⚠️⚠️ `IfcDoorStyle` IS THE IFC2x3 ENTITY; `IfcDoorType` IS ITS IFC4 REPLACEMENT. THE FILE-LEVEL UPGRADE DID NOT MIGRATE THE ENTITY CLASS.** The header says IFC4; the contents still carry a deprecated IFC2x3 entity. **The result is an object that is semantically a door and is invisible to every tool that handles doors.**
>
> **This is a precise, checkable defect class, and it is exactly what the gap analysis's `Adopt` verdict on IDS VALIDATION is for.** `_Inbox/planning/toolchain_gap_analysis_20260908.md` marks IDS validation **Adopt**, ahead of our geometry gate, against *"Nothing"* today. **Here is a concrete rule it would have caught at import: assert that every element resolves to an IFC4 type entity, and refuse a deprecated `*Style` survivor.**
>
> ⚠️ **And note the general principle, which is worth more than the specific case: A FORMAT CONVERSION THAT REPORTS SUCCESS HAS NOT NECESSARILY CONVERTED THE CONTENT.** The presenter's own framing — *"Bonsai will be nice enough to upgrade the file for us"* — is the trap. **The upgrade succeeded and the model is wrong.** This belongs with the silent-failure modes collected from [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|YYmFMxMV6io]] §2 in this same batch.

## 2. Third-party IFC assets are real, free, and Revit-shaped

- Manufacturer and aggregator libraries publish real product geometry; **some offer an IFC download alongside their Revit families**, reachable by filtering on file type.
- His recommendation is to **use published assets rather than model your own** — *"you would have a lot of work if you decided to go designing this door here from scratch"* — and specifically to fetch **the model of the door actually being ordered**: *"if you are designing a house, you will order a specific model for a door. You can get this model… in many free online libraries."*

> **→ ⚠️ The second half of that is the genuinely useful idea, and it is a COST idea, not a modelling one.** An asset that *is* the specified product carries the product identity, which is what a schedule needs to price. **It is the `resource_role` / `product_id` split the BOM already uses** — see [[18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join|Quantity Takeoff and Cost Join]].
>
> ⚠️ **But the flag matters for us**: these libraries are **Revit-first**, IFC is their secondary export, and the export is what produced the defect in §1. **Treat a downloaded IFC asset as an untrusted import that must be validated, not as a component.**

## 3. Import mechanics worth keeping

An external library is attached at **project level** (`project overview → project library → open an IFC file`), then individual types are imported from it into the project. **The library is itself an IFC file of type products** — corroborating [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] §12, where a custom furniture library was distributed the same way.

> **→ A TYPE LIBRARY IS AN IFC FILE, AND ATTACHING ONE IS A PROJECT-LEVEL ACT.** ⚠️ Relevant if this project ever needs a fixture or appliance library: the artefact would be an `.ifc` under version control, which is a shape that suits us — **diffable, hashable, and gated like anything else.**

## 4. The thin default library, confirmed a third time

> *"You will notice… that **this single door is not enough**. You need more assets."*

> **→ Third source in this batch on the same point** — with [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|fxpIg-su-00]] §9 (*"the only door that is loaded here, it's a single one"*, slabs only 200/300) and [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] §8 (a 200 wall type accepted for a 220 masonry wall). **The demo template is a teaching aid, not a starting point for real work**, and every practitioner hits this immediately.
>
> ⚠️ **Low relevance to this project as such** — we author types programmatically, so a thin GUI library costs us nothing. **It matters only as context for what "adopting Bonsai" would involve for anyone working in the GUI.**

## 5. The two paths, and which one this project is already on

He frames the choice as: **design your own assets, or import published ones** — and recommends the second *"for most people."*

> **→ This project is on neither path as stated.** Our elements are **generated from `data/canonical/`**, which is a third option his framing does not contain: **author the type from the project's own data.** ⚠️ Recorded because the omission is informative — **the GUI-centred view of BIM assumes a type is either drawn or downloaded, never computed.** That assumption is what the gap analysis's *"Keep programmatic"* verdict quietly rejects.

## What was deliberately NOT extracted

- The asset library's name and UI, and all Bonsai UI paths — they date.
- **The entire closing sales block** — two workshops, a book, channel membership. No recommendation is routed from a source selling the thing it recommends learning.
- **No prices** (none given), **no regional claims, no regulatory content.**

## Source Notes

Alan Rito, *Blender 3D Architect* (YouTube), 2026-05-27, 7 min, **read in full**. He identifies himself as an architect. **Claims are this presenter's, as opinion.** ⚠️ **Nothing is measured or verified.** ⚠️ **The `IfcDoorStyle` / `IfcDoorType` reading in §1 is this vault's interpretation of what he observed**, not a claim he makes — he reports only that the object appears under "door style" and is not reachable from the door tool. **The inference that the schema upgrade left a deprecated entity in place should be reproduced locally before it is relied on.**
