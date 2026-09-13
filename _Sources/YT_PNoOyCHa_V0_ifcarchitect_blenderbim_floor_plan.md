---
source_type: video transcript (BlenderBIM/IFC specialist channel, beginner walkthrough)
source_url: https://www.youtube.com/watch?v=PNoOyCHa_V0
video_id: PNoOyCHa_V0
transcript_file: _Archive/processed_sources/20260913_ifcarchitect_blenderbim_floor_plan_0b356feb.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2022-10-18 (confirmed via yt-dlp metadata)
channel: Ifc Architect
source_title: "BlenderBim - Beginner Tutorial - Floor plan - in 20mins"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Drawing and Documentation Conventions`, `Digital Toolchain / AI Workflow`)
fact_yield: 12
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Ifc Architect: The Bonsai/BlenderBIM Route to the Same Drawing - Where the Drawing Is GENERATED, Not Exported (YouTube PNoOyCHa_V0)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## ⚠️ Dating caveat, stated up front

**This is the OLDEST of three recordings of the same tutorial on this channel** — `PNoOyCHa_V0` (2022, "BlenderBim"), `agwK8hbkToM` (2023), `IXRpDka6gLI` (Bonsai era). The add-on has since been **renamed** and its **UI overhauled**. **Every UI path, button name and panel location in this note is therefore discarded as dated.** What is extracted is the **document semantics**, which are IFC-level and do not move with the UI. See [[_Inbox/planning/bonsai_ifc_batch_20260913|the batch triage]] §2.

`promotional_ratio: low` — one free asset library, given away, and a credit to the OSArch community and IfcOpenShell. ⚠️ **That is this project's own ecosystem**: our chain is IfcOpenShell-based, and Bonsai is installed and idle.

## ⚠️⚠️ 1. THE DECISIVE CONTRAST WITH THE MESH ROUTE: the drawing is GENERATED from the model

He states the mental model in one line:

> *"It's **similar to AutoCAD in that you have to print the end result**."*

The model view is not the drawing. A camera is placed, and **`create drawing`** produces the plan. When he then decides the windows sit on the wrong face, he moves them in the model, runs `create drawing` again, *"and you can see the windows have moved — it's as straightforward as that."*

> **→ ⚠️⚠️ THE DRAWING IS A DERIVED ARTEFACT, REGENERATED ON DEMAND, AND IT TRACKS THE MODEL.** **This is exactly what [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|the MeasureIt_ARCH route]] in this same batch cannot do** — there the drawings are *exported meshes*, permanently detached, and a dimension on one cannot know the model changed.
>
> **This is the gap analysis's `Adopt` verdict vindicated on the one axis that matters most**, and it is the same axis as the *placed, not associated* defect that spanned three tools last round ([[_Inbox/planning/astra_modelling_batch_20260913|Astra batch]] §3). **Two routes to an annotated sheet, and only one of them maintains the constraint. The difference is not drawing quality — it is whether anything holds the drawing to the model.**
>
> ⚠️ **It is not fully automatic, and he says so**: *"I like to just **update representation** every now and then to make sure that it's all updating."* **A manual sync step exists.** That is precisely the kind of step that must be a build target, not a habit, if this ever runs headless.

## ⚠️⚠️ 2. The plan cut height is a NAMED CONVENTION with a stated reason

> *"We're going to create a plan — **not at zero, which is our engine, but at my story, which is that ONE METRE STANDARD HIGH CUT, so it CUTS THE WINDOWS AND THE DOORS**."* Later: *"this is cutting it at **1 to 1.2 metres high** roughly."*

> **→ THE PLAN CUT PLANE SITS ~1.0–1.2 m ABOVE STOREY LEVEL, AND THE REASON IS THAT IT MUST PASS THROUGH BOTH WINDOW AND DOOR OPENINGS.** A cut at zero shows a slab; a cut too high misses window sills; a cut too low misses window heads. **This is a real drawing convention with a functional justification, and it answers the gap left open by [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|YYmFMxMV6io]] §9**, where the cut plane was dragged by eye and no height was ever stated.
>
> ⚠️ **Route it to [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]].** It is directly actionable for this project's own plan sheets.

## ⚠️ 3. Plan orientation convention

> *"In architecture **we typically orient plans towards north**, and in Blender when you tab 7 on your numpad it orients **Y — the green line — to north, and X to east and west**."*

> **→ +Y = NORTH, +X = EAST, plan viewed from above.** ⚠️ **Relevant to the open datum question.** The previous round found that unrelated agents silently defaulted to the **bottom-left of the wall** as origin ([[_Inbox/planning/astra_modelling_batch_20260913|Astra batch]] §3.4); this supplies the **axis** half of the same unstated convention. **Together they are the default this project would be silently fighting if it chose otherwise.** Flagged for `residential-bim-geometry-rules` alongside the datum decision.

## ⚠️⚠️ 4. Each object carries a 2D PLAN REPRESENTATION that is a SYMBOL, not a section

The single most transferable finding for our own sheet generation:

> *"If I want to see **how the shower actually looks when it's cut**, I can just go into object properties → geometry → representations and **turn on the plan representation**, so we can see **where the drain is**."*

He then works almost entirely in that 2D view — activating the plan annotation for every fixture and rotating it into place (shower −90°, WC 90°, basin 90°, sink −90°).

> **→ ⚠️⚠️ THE PLAN SYMBOL IS AUTHORED SEPARATELY FROM THE 3D GEOMETRY AND IS NOT DERIVED BY CUTTING IT.** A drain does not appear in a section through a shower tray; it appears because the *symbol* has one. **This is how real architectural documentation works, and it is a capability our hand-rolled SVG pipeline does not have** — it can only draw what it can compute from geometry.
>
> **Route to [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]]**: a fixture on a plan is represented by convention, not by projection. ⚠️ **And it sharpens the Bonsai adopt question again**: this symbol library is a large part of what "adopting the drawings subsystem" would actually buy.

## ⚠️⚠️ 5. Door swing is a TYPE-LEVEL 2D annotation — and editing it has a silent wide blast radius

> *"I'm not liking the direction of the swing, so with the 2D annotation selected I'm going to tab into it, right click, and **mirror along the Y global**… **and you see that's changed ALL the doors, because they're the same type.** If there were different types it would be changed differently."*

For one door he then works at instance level instead: tabs out, selects that door alone, rotates 180° *"because I want him to swing inside."*

> **→ ⚠️⚠️ A TYPE EDIT AND AN INSTANCE EDIT LOOK THE SAME AND DIFFER ONLY IN WHETHER YOU TABBED INTO THE OBJECT.** The type edit silently restyled every door in the building. **He noticed because it was visible; on a large plan it would not be.**
>
> **This is a defect class worth carrying**: *an edit whose scope is implicit in the selection mode*. It belongs alongside the failure classes in `00_Master/Validator_Design_Discipline.md`, and it is an argument for **authoring types programmatically**, where the scope of a change is explicit in the code, rather than through a GUI where it is a modal state. ⚠️ **Supports the gap analysis's "Keep programmatic" verdict on IFC authoring.**
>
> **And the underlying convention is real and useful**: door swing is a property of the **2D representation**, decided per type with per-instance overrides — *"this is just a 2D representation, it's just this view of the wall of the door."*

## ⚠️⚠️ 6. Saving IFC silently discards anything not classified as IFC

> *"You would just name it… and say **export IFC**. **The key difference here is you're only saving the IFC, not the Blender file** — so if you have something in the Blender file that you want to save, **make sure it's classified as an IFC, or just save the Blender file separately**."*

> **→ A SILENT DATA-LOSS TRAP: UNCLASSIFIED OBJECTS DO NOT SURVIVE THE SAVE.** ⚠️⚠️ **Directly corroborated by [[_Sources/YT_tAq0foY2GOY_spbproduction_bonsai_ifc_vs_blend_save|tAq0foY2GOY]] in this same batch**, which is entirely about this question — **two independent sources, one batch.**
>
> ⚠️ **Lower risk for this project than for a GUI user**, because our IFC is authored programmatically and Blender is a *viewer* here — there is nothing in the Blender file to lose. **But it decides how Bonsai could ever be introduced**: any drawing or annotation work done in the Blender session must be IFC-classified, or it is not in the deliverable. **That is a constraint on the "adopt Bonsai for annotated sheets" plan, not a blocker.**

## Authoring semantics worth keeping

7. **Walls are typed objects with a numeric length property**, not traced polygons: he types **10000 mm** and hits refresh; `shift E` extends to a snap, `shift F` flips, `shift G` regenerates position. **→ The dimension is the input, not a measured consequence of mouse work** — the opposite of the three mesh-tracing sources in this batch.
8. **⚠️ A type library QUANTISES wall thickness**: *"we're going to select the **200 wall, because that's similar to a masonry brick wall of 220**."* **→ He accepts a 20 mm type error because the library has no 220.** Worth noting against our model, which carries exact `clear_mm` per wall. **A type-library workflow trades dimensional fidelity for schedulability**; ours currently has the fidelity and not the schedule. Internal walls set to **100**.
9. **Project structure is `project → site → building → storey`**, with units (metric millimetres; square and cubic metres) chosen at project creation. Objects are placed on the active storey.
10. **Window position within the wall thickness is an explicit authored decision** — he moves windows from the inner to the outer face and regenerates. ⚠️ Not a default; something must decide it.
11. **⚠️⚠️ Deliberate 2D-only elements**: the kitchen countertop and the built-in cupboards are **drafting lines**, not modelled objects — *"we're not going to model it per se."* Drawn at **600 mm** counter depth with an **800 mm** fridge gap. **→ ANYTHING DRAFTED-ONLY IS INVISIBLE TO QUANTITY TAKEOFF.** A legitimate documentation shortcut that silently removes an item from every schedule. **Directly relevant to [[18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join|Quantity Takeoff and Cost Join]]: the drawing and the takeoff can disagree, and a 2D-only element is how.** ⚠️ Joinery is exactly the class of item this would hide, and it is not cheap.
12. Fixtures come from a **loadable IFC type library** (`.ifc` file of type products, categorised as building element / furniture / sanitary terminal types) — *"loaded into our types, and we access it the way we access the walls."* **→ A furniture symbol library is itself an IFC file.**

## What was deliberately NOT extracted

- **Every UI path, panel name and button** — dated by two subsequent re-records (see caveat above).
- Keystroke sequences and the furniture-placement section, which is mouse work.
- The 600 mm counter and 800 mm fridge figures are **generic joinery defaults with no jurisdiction stated** — recorded as context, **not routed as figures**.
- **No prices, no regulatory content.**

## Source Notes

*Ifc Architect* (YouTube), 2022-10-18, 17 min, **read in full**. **Claims are this presenter's, as opinion.** ⚠️ **Nothing is measured or verified in this video** — it is a modelling walkthrough, and the wall lengths are inputs he types, not findings. ⚠️ **Dated source**: see the caveat at the top; UI-level content discarded, document semantics retained. ⚠️ **This channel is `@IfcArchitect`, one of the two channels triaged in [[_Inbox/planning/bonsai_ifc_batch_20260913|this batch]]** — 42 videos, assessed there as the highest-relevance channel found so far.
