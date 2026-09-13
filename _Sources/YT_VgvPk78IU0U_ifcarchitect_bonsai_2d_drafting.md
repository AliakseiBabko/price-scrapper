---
source_type: video transcript (BlenderBIM/IFC specialist channel, Bonsai-era project series part 2)
source_url: https://www.youtube.com/watch?v=VgvPk78IU0U
video_id: VgvPk78IU0U
transcript_file: _Archive/processed_sources/20260913_ifcarchitect_bonsai_2d_drafting_c830a7fe.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2025-03-27 (confirmed via yt-dlp metadata)
channel: Ifc Architect
source_title: "Bonsai Tutorial - Beginner Project - Part 2 - 2D drafting"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 17
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Ifc Architect: ⚠️⚠️ THE ANNOTATED-SHEET QUESTION ANSWERED - Dimensions Are Manual, Tags Are Data-Bound, and the Output Is SVG+CSS (YouTube VgvPk78IU0U)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this source is extracted at 17 facts

**It answers three open items at once**, and one of the answers **reverses a conclusion this vault recorded eight hours earlier**. `promotional_ratio: low` — one coffee-page mention in the final ten seconds, no sponsor, no product.

**Bonsai-era (2025-03), so no dating caveat applies** — unlike the five BlenderBim-era sources in this round.

## ⚠️⚠️ 1. THE DECISIVE ANSWER: dimension placement is entirely MANUAL, and there is no auto-dimension at all

The open item was: *"Does Bonsai place dimension text without per-instance intervention? This is what actually decides the annotated-sheet split."*

**The answer is NO, and it is more thoroughly no than expected.** A dimension in Bonsai is **a polyline the user draws and snaps vertex by vertex**:

> *"We're going to select **dimension**… place our 3D cursor… say add. **You can see it adds in as a POLYLINE CURVE**… I'm going to change it to **edit mode**, and this allows me to **edit the vertices directly**. So I'm going to select this bottom one and say `GY`, make sure your snaps are on, `GY` to snap it to the bottom… say `E` to extend this dimension line."*

He then composes the entire dimension set by hand, for some four minutes of the video, in `G`/`E`/`shift D` keystrokes.

> **→ ⚠️⚠️ THERE IS NO "DIMENSION THIS WALL" COMMAND. There is a line primitive that renders as a dimension, and the human snaps its ends to the geometry.**
>
> **⚠️⚠️ THIS SUBSTANTIALLY WEAKENS THE GAP ANALYSIS'S STATED RATIONALE FOR ADOPTING BONSAI.** [`toolchain_gap_analysis_20260908.md`](../_Inbox/planning/toolchain_gap_analysis_20260908.md) §Kind 3 marks the drawings subsystem `Adopt` **because hand-rolling fails exactly on placement**: *"dimension chains collide on dense MEP plans; excessive custom code required to handle text overlaps."*
>
> **Bonsai does not solve that problem. It gives it to the human.** The previous round already found the same in a purpose-built annotation add-on ([[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|YYmFMxMV6io]] §3) and I recorded it as *"adopting a tool relocates the problem"* while noting Bonsai *"may do better."* **It does not do better. It does the same thing, and this is the current-era recording from the channel that specialises in it.**
>
> **→ And the inversion that follows is the point.** Our SVG pipeline generates from `data/canonical/`, where **every wall's length, thickness and position is already a number in a CSV**. A script that emits a three-tier dimension chain at computed offsets is not "excessive custom code" — **it is a loop over data we already have, for one apartment with fixed geometry.** Hand-snapping in a GUI is the thing that does not scale to a re-run. **For dimensions specifically, our generative route is plausibly the better one, and the gap analysis's premise should be corrected.**

## ⚠️⚠️ 2. …but the dimension CHAIN convention he composes is worth taking, and it is concrete

He builds the dimension set in **three parallel tiers, working outward**, and states the order explicitly — *"we're going to do **openings, then rooms, and then we're going to do overalls**"*:

| Tier | Contents |
| :--- | :--- |
| **Innermost** | **Openings** — each window and door width, and the wall segments between them |
| **Middle** | **Rooms / spaces** — internal clear dimensions |
| **Outermost** | **Overalls** — the full extent, plus one for the outside area and one for the building itself |

**The row spacing is `400` mm, typed, and repeated** via `shift D` + `X`/`Y` + `400` for each new tier. Grid lines are later offset a further *"400 or perhaps 500"* to clear the dimensions.

> **→ ⚠️⚠️ THIS IS DIRECTLY IMPLEMENTABLE IN OUR OWN PIPELINE AND IT IS THE MOST ACTIONABLE THING IN THE ROUND.** Three chains, offsets of 400 mm, innermost = openings, outermost = overall. **It is the standard architectural convention, stated with a number**, and combined with §1 it is the whole argument: *we do not need Bonsai to place dimensions, we need this convention and a loop.*
>
> ⚠️ **Route to [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §1.** The 400 mm is one practitioner's working figure on a 1:50 sheet, **not a norm** — the *structure* is the transferable part, the spacing is a starting value.

## ⚠️⚠️ 3. Tags ARE automatic, data-bound, and type-templated — the opposite of dimensions

**This is the half I did not expect, and it is where Bonsai's real value sits.**

**(a) `bulk tag` places one tag per selected object, in one command**, each already related to its object: *"I've got my space tag selected, I click on **bulk tag**, and you can see we've added in a tag for each space that **already has a relationship aligned with that space**. So you can see it's grabbing the names."* Done for spaces, then doors, then windows.

**(b) A tag's text is a TEMPLATE that resolves against the bound object.** Turning a plain leader into a live one:

> *"We can go to **product assignments**, where you can **create a relationship between the 2D text object and a 3D object** — click the pencil, there'll be an **eyedropper**, select the column… And then we want to tell the text object to go look for the information inside of the column. So we add **two squiggly brackets** and say we want to look for the **name**… and **our smart text has updated automatically to say 'column'**."*

**(c) ⚠️⚠️ The TEMPLATE is type-level; the DATA is instance-level.** Appending a unit to one space tag changed both: *"remember **this is also a type**. So these types are shared **even if the information is different**"* — after which one reads *"office / timber / 9.41 m²"* and the other its own values.

> **→ ⚠️⚠️ THIS IS THE CLEANEST INSTANCE OF TYPE-LEVEL SEMANTICS FOUND SO FAR, AND THE ONLY ONE WHERE IT IS AN UNAMBIGUOUS BENEFIT.** The previous round recorded type edits as a hazard — a silent wide blast radius. **Here the blast radius is the feature**: one edit re-templates every tag, and each still renders its own object's data. **The distinction that makes it safe is that the TEMPLATE is shared and the VALUE is not.**
>
> **→ ⚠️⚠️ AND IT ANSWERS THE `1/2` QUESTION AFFIRMATIVELY.** [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §1 records as untested *"whether our own DXF/SVG pipeline can express a proportional dimension at all, or whether it needs Bonsai's annotation subsystem."* **An annotation whose content is a template string over model attributes can trivially carry a literal `1/2`** — and more importantly, **it shows the general mechanism: the annotation is DERIVED from the model, not transcribed alongside it.** That is the association principle arriving at the annotation layer, and it is what our pipeline should copy regardless of which engine draws.
>
> ⚠️ **It also removes the "needs Bonsai" horn of that dilemma.** A template-over-data annotation is a string-formatting operation. **We can do it; we just have not.**

## ⚠️⚠️ 4. THE STRUCTURAL FINDING: the drawing output is SVG, styled by CSS

**Three independent tells in one video:**

1. **It opens in a browser.** *"If this is the first time you're opening the drawing, it's going to ask you **what should we open it with. You can use any browser.**"*
2. **Hatch patterns come from a material name, and the styling system is named**: *"actually editing the walls and hatch patterns and the materials and creating your own types **will be included in a later video where we talk about CSS**."*
3. The channel's title-block video does it **in Inkscape** — an SVG editor.

> **→ ⚠️⚠️ BONSAI'S SHEETS ARE SVG. OUR PIPELINE IS SVG→PDF. THEY ARE THE SAME FORMAT.**
>
> **This bears directly on the gap analysis's proposed architecture**, which concluded: *"keep our SVG pipeline for the diagrammatic sheets it already produces well, and put Bonsai behind the sheets that need dimension chains, tags and schedules. **Two engines, split by whether the sheet is annotated.**"*
>
> **That split was posed as two incompatible engines. It is not — it is one output format produced two ways.** Which means the realistic options are wider than recorded: **a shared stylesheet, shared post-processing to PDF, or lifting Bonsai's CSS conventions into our own generator without running Blender at all.** ⚠️ **Route as a correction to the two-engine framing, not as a decision** — none of this is tested, and the sheet-assembly half is still open (see [[_Sources/YT_HEb7fWJduXg_ifcarchitect_page_layout|the page-layout source]] in this round).

### ⚠️⚠️ 5. And the hatch is driven by a case-sensitive MAGIC STRING with no validation

> *"We need to give the **layer set name a material name**, and that will **indicate what the hatch pattern is** of that material. So there's a few standard ones and one of them is brick. **So it's got to be lowercase letters B-R-I-C-K.**"*

He then names an internal wall's layer `concrete` and it renders as concrete hatch. *"It's done **by type** generally."*

> **→ THE DRAWING'S APPEARANCE IS A FUNCTION OF MODEL DATA — which is the right design — BUT THE BINDING IS AN UNVALIDATED, CASE-SENSITIVE, UNDOCUMENTED STRING.** Type `Brick` and you get nothing, with no error.
>
> ⚠️⚠️ **This is precisely the class of defect the IDS validation already marked `Adopt` exists to catch**, and it is the second concrete rule this batch has produced for it (after the `IfcDoorStyle` survivor). **A rule asserting that every wall's material layer-set name is drawn from a known vocabulary is cheap and would fail loudly instead of silently.** ⚠️ **And note the coupling it creates**: our `data/canonical/wall_materials.json` already names materials for *costing* reasons — **if those names also drove hatch, one vocabulary would serve both, and a typo would be caught by the gate that already exists.**

## Drawing setup, and a third confirmation of the cut plane

6. **Plan created on the storey, not the origin** — *"we're going to select **my story**. So it's **not going to be origin**."* **→ Third independent confirmation** of the storey-referenced cut, after [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] and [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|fxpIg-su-00]]. ⚠️ Same presenter as the first, so **two voices, not three**.
7. **⚠️ Sheet scale is an explicit camera property**: changed *"from 1 to 100 to **1 to 50**, which I just feel is more appropriate."* **→ Scale is set per drawing, by judgement, and it interacts with everything in §2** — a 400 mm dimension offset reads differently at 1:100.
8. **Drawing extent set by hand** to 10 m × 8 m, corroborating the 50 × 50 default found in [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|fxpIg-su-00]] §5. **No fit-to-content.**
9. **Regeneration is `create drawing` / `print`, then `view`** — run repeatedly through the video after every change. **→ Corroborates the generated-not-exported finding**: he checks his work by regenerating, perhaps six times.

## Annotation mechanics

10. **Three annotation primitives**: **dimension**, **line**, **text** — with **leader** as *"basically a text object with a line attached to it."*
11. **⚠️ Line styles are PRESET TYPES loaded from the project template**: *"there are a bunch of **predefined preset lines** that are automatically loaded when you use the IFC4 demo project"* — he uses `fine` for a ramp slope and `dashed` for an overhead roof line. **→ Line style is a named type, not an ad-hoc property.** Consistent with the named-style-set lesson from [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|YYmFMxMV6io]] §4.
12. **⚠️ Text alignment is set by its ORIGIN, and he flags it as counter-intuitive**: *"how this box alignment works is essentially it's **the origin of the text**… **it isn't the side that the text sits on.** So if I want it to be on the left hand side, **the origin has to be on the right**. It's not quite too intuitive."* **→ A third instance of the implicit-anchor theme** — after the bottom-left-of-wall datum and the door width anchor. **An anchor decides what a change does, and it is never the thing you are looking at.**

## ⚠️ 13. Quantity take-off is one button away — with a portability flag

Filling a space tag, he runs it inline: *"we go to **quantity sets**… there is a custom QTO, there's an **IFC4 base quantities**. We're going to change this to **the Blender version just because it works a little bit better right now**… click **perform quantities take off**. And you can see mine is in square meters, **it's 9.41 m² for this area**."*

> **→ `Qto_SpaceBaseQuantities` — exactly what the gap analysis says the screed, waterproofing, skirting and cornice lines need — is a single command, and the tag then displays it live.**
>
> ⚠️⚠️ **But he does NOT use the IFC4 standard quantity set.** He switches to a **Blender-specific variant** because *"it works a little bit better right now"*, with no further explanation. **A Blender-specific quantity set is not guaranteed to survive to any other tool** — and this project's entire premise is that the IFC is the portable master. **Flagged: if quantities are ever taken this way, take them from the IFC4 base set, or know exactly what the difference is.**

## ⚠️ 14. A free-text attribute used as a semantic field by personal convention

> *"And then the last thing where it says none there is **the description**. **I normally use that for a floor surface.**"* — set to `timber` and `tiles`, which the space tag then renders.

> **→ AN UNTYPED IFC ATTRIBUTE REPURPOSED AS A DATA FIELD BY HABIT.** It works, and **nothing validates it** — not the spelling, not the vocabulary, not whether it is populated. ⚠️ **A second concrete case for IDS**, and a caution for our own model: **a convention that lives only in the author's head is the thing that rots first.**

## 15. Grids are model objects, not drawing annotations — and they can be LOCKED

`project overview → spatial → grids → add grids` creates numbered (1, 2, 3) and lettered (A, B, C) axes as **spatial objects**, adjusted by editing vertices, which then *"show a 2D representation of the grids"* in every drawing automatically.

> ⚠️ **He locks them when done** — *"once they're in the correct position, you can lock it again"* — having first had to confirm *"our grids are not locked, so we can still edit them."* **→ A lock affordance on a datum object.** Worth noting beside the `Ctrl+S` hazard from the previous round: **the tool has a concept of "this is settled, protect it", and the vault's frozen-artefact pattern is the same instinct.**

## 16. Type duplication for divergence — fourth confirmation

To add a sliding door alongside a swing door: **duplicate the door type**, rename it, place an instance, then set its operation to `sliding to the left`. **→ With [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|fxpIg-su-00]] §3 and [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] §5.** ⚠️ Two of the four are this presenter — **three voices, four instances.**

## ⚠️ 17. He edits the MODEL to make the DRAWING read better

Door width reduced to **800 mm** — *"this is just my preference, just makes it a bit smaller and more reasonable"* — and the window shrunk likewise, before any drawing work.

> **→ Recorded as a caution, not a technique.** It is harmless in a tutorial and **structurally wrong for a project whose model is the priced master**: a door width is a purchasing decision and a rough-opening dimension, not a graphic one. **In our model that edit would silently change a BOM line.**

## What was deliberately NOT extracted

- **All keystroke sequences, panel names and button locations** — the four minutes of `G`/`E`/`shift D` dimension work is mouse work, and the specific UI dates even within the Bonsai era.
- The sanitary-fixture placement section — corroborates [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] §12 on loadable IFC type libraries with 2D representations and adds nothing.
- **The 800 mm door and 9.41 m² space figures are tutorial values with no jurisdiction and no relevance** — recorded above only as context for §17 and §13.
- **No prices, no regional claims, no regulatory content.**

## Source Notes

*Ifc Architect* (YouTube), 2025-03-27, 24 min, **read in full**. **Claims are this presenter's, as opinion**, and the tool behaviours are as observed on his machine on one version. ⚠️ **Nothing is measured or verified**; every dimension is a value he types or snaps. ⚠️ **Second source from this presenter in the vault** after [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] — where a finding here agrees with that one, it is the same voice repeating. ⚠️⚠️ **CORRECTED 2026-09-13, same round: the SVG+CSS reading in §4 was written as an inference from three indirect tells. It is now CONFIRMED OUTRIGHT** by two further sources in this round — [[_Sources/YT_HEb7fWJduXg_ifcarchitect_page_layout|HEb7fWJduXg]] names the sheets directory of `.svg` files and exports SVG→PDF, and [[_Sources/YT_dPWQbjaeoyo_ifcarchitect_lineweights_css|dPWQbjaeoyo]] opens the stylesheet as a literal `.css` file. **Read §4 as established, not inferred.** ⚠️ **Likewise §5: the lowercase hatch name is not an "undocumented magic string" but a CSS class defined in that stylesheet** — the substance (nothing validates it; a typo yields no hatch and no error) is unchanged, the characterisation is corrected. **The directory layout should still be confirmed against our installed Bonsai 0.8.6-alpha260801.**
