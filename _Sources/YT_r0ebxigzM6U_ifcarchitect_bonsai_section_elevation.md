---
source_type: video transcript (BlenderBIM/IFC specialist channel, Bonsai-era project series part 3)
source_url: https://www.youtube.com/watch?v=r0ebxigzM6U
video_id: r0ebxigzM6U
transcript_file: _Archive/processed_sources/20260913_ifcarchitect_bonsai_section_elevation_2e3ac9ed.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2025-05-12 (confirmed via yt-dlp metadata)
channel: Ifc Architect
source_title: "Bonsai Tutorial - Beginner Project - Part 3 - Section & Elevation"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 8
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Ifc Architect: Section and Elevation Are ONE Mechanism With a Different Camera - and Classification Is What Puts an Object in the Drawing (YouTube r0ebxigzM6U)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

**Bonsai-era (2025-05), no dating caveat.** `promotional_ratio: low` — a coffee-page mention in the closing seconds. Part 3 of the series whose Part 2 is [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|VgvPk78IU0U]]; **read that one first — it carries the round's main findings.**

## ⚠️⚠️ 1. Plan, section, elevation and detail are ONE generator, parameterised

He says it outright when moving from section to elevation: ***"Essentially, it's all the same process."*** And the process is: place the 3D cursor, pick a **direction**, add the drawing, set the camera's **width/height**, set its **scale**, adjust annotations, `activate → print → view`.

The only things that differ between the four drawing types are **cut direction, extent and scale**:

| Drawing | How it is specified |
| :--- | :--- |
| **Plan** | cut on the storey, extent 10 × 8 m, 1:50 |
| **Section** | 3D cursor placed, direction `east`, extent 7500, 1:100 |
| **Elevation** | 3D cursor placed, direction `west`, extent 7500, 1:100 |
| **Detail** | direction `east`, extent **1000**, **1:10** — see [[_Sources/YT_QTviOpqz1rw_ifcarchitect_bonsai_2d_detail|QTviOpqz1rw]] |

> **→ ⚠️⚠️ A DRAWING IS A CAMERA WITH (DIRECTION, EXTENT, SCALE). There is no separate section engine, elevation engine or detail engine.**
>
> **This is directly useful to our own sheet generation and it simplifies the problem considerably.** `Sheet_Production_Roadmap.md` treats sheet types as separate products; **this says one parameterised generator covers all four**, and that a "detail" needs no new machinery at all. **The variation lives in the parameters, not the code.**

## ⚠️⚠️ 2. Classification is the switch that puts an object into the drawing — demonstrated, not asserted

He builds a site terrain as **a plain Blender cube**, stretches it past the camera, and then:

> *"This is a normal Blender mesh… we're going to turn this into an **IFC geographic element**… and then it's **terrain**… and we're going to say **assign IFC class**. **And you can see now it's been assigned and IT'S NOW BEING CUT BY THE CAMERA VIEW.**"*

> **→ ⚠️⚠️ BEFORE CLASSIFICATION THE MESH IS INVISIBLE TO THE SECTION; AFTER IT, IT IS CUT.** The vault already holds *an object is in the model because it carries a class, not because it is in the scene* — from [[_Sources/YT_tAq0foY2GOY_spbproduction_bonsai_ifc_vs_blend_save|tAq0foY2GOY]] §5 and [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] §11 — **but both stated it. This DEMONSTRATES it, and it shows the consequence is not merely "absent from the schedule" but "absent from the drawing."**
>
> **Same mechanism, third consequence.** An unclassified object: is not saved to IFC, is not scheduled, **and is not drawn**. ⚠️ **This makes the drafted-only-element trap worse than recorded** — a drafting line still draws, but any *modelled* geometry you forget to classify silently vanishes from every view.
>
> **`IfcGeographicElement` / `terrain` is also just useful to know** if this project ever needs a site or a slab-below datum.

## ⚠️⚠️ 3. A cut element's LINE WEIGHT is automatic; its FILL is not

> *"Because it's a geographic element, there's a default where it's cut. **Now we have a nice thick line there, but it's being cut as a WHITE element.** We want this to look like it is a section. **We want to add in that hatch pattern.**"*

> **→ THE CUT OUTLINE IS GENERATED; THE POCHÉ IS A CONSEQUENCE OF THE MATERIAL.** An element with no material reads as an empty white outline — technically correct and conventionally wrong. **The same is repeated in the detail video**, where every new element arrives unfilled: *"everything's being cut, but these things don't have materials."*
>
> ⚠️ **A rule for our own generator**: heavy cut-line weight can be derived from the cut itself, but **fill must be driven by material — so every element that can be cut needs a material, or the sheet is wrong in a way that looks deliberate.**

## ⚠️⚠️ 4. The hatch vocabulary is project-wide, lowercase, and unvalidated — second confirmation

Two distinct routes appear in this one video:

- **A project-wide IFC material**: *"we don't have an earth material, so we're going to add one in… click on **materials, this is PROJECT-WIDE**… add in a new **lowercase earth** material."*
- **A wall/slab layer-set name**: *"here where it says **layer set name**, we're going to give it the name… type in **concrete lowercase**."*

> **→ Confirms [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|VgvPk78IU0U]] §5 and extends it**: the hatch binding is not one field but **two paths into the same lowercase vocabulary**, one of which (`materials`) is a **project-scoped named object** and the other a per-type string.
>
> ⚠️⚠️ **And the detail video adds a second vocabulary with the OPPOSITE casing** — a fill area's `object type` typed as **`SEALANT`, all caps** ([[_Sources/YT_QTviOpqz1rw_ifcarchitect_bonsai_2d_detail|QTviOpqz1rw]]). **Two vocabularies with contradictory casing, neither discoverable in the UI, neither validated.**
>
> ⚠️ **CORRECTED later the same round: these are CSS CLASS NAMES, not magic strings.** [[_Sources/YT_dPWQbjaeoyo_ifcarchitect_lineweights_css|dPWQbjaeoyo]] shows the stylesheet is a literal `.css` file the user edits, and the vocabulary is **whatever it defines — user-extensible, and documented in the file itself.** The casing inconsistency is not a convention, just how the shipped default happens to be written. **What survives unchanged: nothing validates that a typed name matches a defined class, and a typo yields no hatch and no error** — so this remains a concrete case for the **IDS validation the gap analysis already marked `Adopt`.**

## ⚠️ 5. "Keep them all generally 1 to 100" — consistency over per-sheet optimisation

He tries 1:50 for the section, looks at it, and reverts:

> *"I can see that looks a little bit better, but actually **I'm just going to leave it at 1 to 100. Keep them all generally 1 to 100.**"*

> **→ A DOCUMENTATION CONVENTION WITH A STATED PREFERENCE: a consistent scale across the set beats a better scale on one sheet.** The reader learns one ruler.
>
> ⚠️ **Note the tension with his own Part 2**, where the plan was set to 1:50 *"which I just feel is more appropriate."* **He states a consistency principle and does not follow it across the set** — which is honest about how this actually goes, and worth recording as: **plans and sections routinely differ in scale; the principle is consistency WITHIN a class of sheet, not across the whole album.** ⚠️ That reading is this vault's, not his.

## Section-drawing conventions worth keeping

6. **⚠️ The section MARK on the plan is an editable annotation, and it lives in the plan drawing.** *"In the plan, we can actually even **edit our section line** — select the 2D annotation element… line them up with the grid lines."* **→ The section symbol and the section drawing are related objects, not a drawn symbol plus a separate view.** ⚠️ Consistent with everything else here: the annotation is *of* the model, not *about* it.
7. **Level lines are a first-class annotation type**, placed, extended and named — he creates a **wall-plate height** and a **roof height**, duplicating with `shift D` and offsetting by typed values. **→ The standard section convention, and it is a supported primitive rather than a drawn line.**
8. **⚠️ Annotation lead-out offsets are eyeballed per drawing, not standardised**: grid lines pushed out **750**, level line **1000**, elevation annotations **500** — against the **400** used for dimension rows in Part 2.
   > **⚠️ This refines what Part 2 suggested.** The three-tier dimension *structure* is a real convention; **the offset numbers are per-drawing judgement at a given scale, not a standard.** Anything our generator does with them should treat the spacing as a **scale-dependent parameter**, not a constant.

## What was deliberately NOT extracted

- All keystroke sequences, panel names and UI locations — mouse work.
- The terrain modelling steps (cube, stretch, depth) — **no relevance to a flat**; kept only for the classification finding in §2.
- **No prices, no regional claims, no regulatory content, no dimensional figures of consequence** — the 7500 extent and 750/1000/500 offsets are tutorial values, recorded above as evidence about *how* offsets are chosen, not as figures to adopt.

## Source Notes

*Ifc Architect* (YouTube), 2025-05-12, 11 min, **read in full**. **Claims are this presenter's, as opinion**; tool behaviours are as observed on one version on his machine. ⚠️ **Nothing is measured or verified.** ⚠️ **Third source from this presenter in the vault** — with [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]] and [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|VgvPk78IU0U]]. **Agreement between them is one voice repeating, not corroboration.**
