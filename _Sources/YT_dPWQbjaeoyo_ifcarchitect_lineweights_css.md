---
source_type: video transcript (BlenderBIM/IFC specialist channel, styling tutorial)
source_url: https://www.youtube.com/watch?v=dPWQbjaeoyo
video_id: dPWQbjaeoyo
transcript_file: _Archive/processed_sources/20260913_ifcarchitect_lineweights_css_2c32ec23.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2023-01-25 (confirmed via yt-dlp metadata)
channel: Ifc Architect
source_title: "BlenderBim - Beginner Tutorial - Lineweights & more in 16mins"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 12
promotional_ratio: none
corroborates_existing: true
region: south_africa_presenter_states_his_own_lineweights_are_South_African_standard - flagged
delivery_model: n/a - not a renovation source
---

# Source Note - Ifc Architect: ⚠️⚠️ THE STYLING SYSTEM IS LITERALLY CSS - Which Dissolves the "Magic Strings" and Settles the Architecture (YouTube dPWQbjaeoyo)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

**BlenderBim-era (2023-01); read because no Bonsai-era replacement exists.** `promotional_ratio: none`. **UI paths discarded; the file formats and the styling model are the content.**

## ⚠️⚠️ 1. Stated in the first sentence: line weights, line styles and hatch patterns are CSS

> *"Today we're going to be doing **custom line weights, line styles and hatch patterns — USING CSS**. It's not too complicated, but it is tedious."*

**The stylesheet is a real `.css` file**, copied from the add-on's `data/styles/` directory, **placed beside the IFC file** (*"they have to be in the same place"*), and referenced per-drawing:

> *"Select the camera → **`EPset_drawing`** → at the bottom, which is **`stylesheet`** — we're just going to write **`tut.css`**. So this lets **this camera** reference that CSS file."*

> **→ ⚠️⚠️ THE SVG+CSS ARCHITECTURE IS NOW CONFIRMED FROM ALL FOUR SIDES**: drawings open in a browser, sheets are SVG files in a directory, sheet filtering uses a CSS attribute selector, **and the styling is a CSS file the user edits in Notepad.** [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|VgvPk78IU0U]] §4 recorded this as an inference from three indirect tells; **it is no longer an inference.**
>
> **⚠️ And note the scoping, which is the good half: the stylesheet lives WITH THE PROJECT, and the reference is a per-drawing property.** Different sheets can carry different stylesheets. **That is exactly the right shape, and it is trivially git-trackable.**

## ⚠️⚠️ 2. THE CORRECTION: the "undocumented magic strings" are CSS class names

**This retires a characterisation I recorded earlier in this batch.** [[_Sources/YT_QTviOpqz1rw_ifcarchitect_bonsai_2d_detail|QTviOpqz1rw]] §5 and [[_Sources/YT_r0ebxigzM6U_ifcarchitect_bonsai_section_elevation|r0ebxigzM6U]] §4 described `brick`, `concrete`, `earth`, `SEALANT` as *"undocumented, unvalidated, case-sensitive magic-string vocabularies with contradictory conventions."*

**They are CSS classes, defined in a file the user can open and read.** To add a custom line style he appends a rule to the stylesheet and names it `green`, then sets the element's `object type` attribute to `green`:

> *"We're going to change the name for this thing to **green**, and we want the **stroke** to be green lowercase, and we want the **stroke-width** to be two, and then… the **dash-array**."* … *"Where it says **object type**, you want this to just be **whatever you label the predefined type**."*

> **→ THE VOCABULARY IS NOT MAGIC AND IT IS NOT FIXED — IT IS WHATEVER THE STYLESHEET DEFINES, AND IT IS USER-EXTENSIBLE.** The casing inconsistency is not a convention at all; it is just how the shipped default stylesheet happens to be written.
>
> ⚠️ **Two things from the earlier notes survive, and one does not.** **Survives:** nothing validates that a name typed into an attribute matches a class that exists — a typo yields no hatch and no error, **so the IDS argument stands unchanged.** **Survives:** the earlier presenter had to flash the valid list on screen because it is not discoverable *in the UI*. **Does not survive:** calling it undocumented. **It is documented in the stylesheet, which is the file you are meant to edit.**

## ⚠️⚠️ 3. The styling taxonomy, and it is the right one to copy

The stylesheet is organised by **the element's ROLE IN THE DRAWING**, not by element class:

| Category | What it styles |
| :--- | :--- |
| **`cut`** | anything the camera plane passes through |
| **`projection`** | anything seen beyond the cut |
| **`text`** | all text |
| **`annotation`** | drawn 2D annotation |
| **predefined types** | *"purely 2D elements"* — user-extensible classes like his `green` |
| **`material`** | *"a 3D element that references a 2D pattern"* — the hatch binding |

**Demonstrated**: setting text blue and cut red turns wall cut lines red and text blue, **while the window and sanitaryware symbols and the annotations do not change**, because they belong to different categories.

> **→ ⚠️⚠️ CUT vs PROJECTION IS FIRST-CLASS, AND IT IS THE FUNDAMENTAL DISTINCTION IN ARCHITECTURAL DRAWING.** What is cut is heavy and poché'd; what is beyond is light. **Our own SVG generator should be organised the same way** — style by *role in the view*, plus material for fill — rather than by element type. **This is the most directly copyable design in the round**, and it needs no Bonsai.

## ⚠️⚠️ 4. A hatch requires TWO registrations in TWO files, with matching names

To add a finer red brick:

1. **The pattern** — an SVG `<pattern>` in `data/templates/patterns`, each *"starts with a label, it's got a width, it's got a height, this is a rotation, and then this is the actual spacing."* He adds `red brick` at width 2, height 2, `stroke: red`.
2. **The material** — *"we need to create the material in the CSS file"*, copying the existing `brick` material rule and relabelling it `red brick`.
3. Then set the wall's **material layer set name** to `red brick`.

> **→ ⚠️ DEFINE ONE WITHOUT THE OTHER AND YOU GET NOTHING.** A two-file coupling held together by a string, with no check that the halves agree. ⚠️ **A third concrete rule for IDS / a pre-flight check**, and a caution for any styling system we build: **one definition, one place.**

## ⚠️⚠️ 5. The scoping is INCONSISTENT, and it decides how any of this could be adopted here

| Artefact | Where it lives | Consequence |
| :--- | :--- | :--- |
| **Stylesheet (`.css`)** | **beside the IFC**, referenced per drawing | ✅ project-local, git-trackable |
| **Hatch patterns** | **inside the add-on install** | ⚠️ *"that changes every Blender file for this version"* — global, lost on reinstall |
| **Title blocks** | **inside the add-on install** | ⚠️ *"if you reinstall, this file will default to just these three, so you will LOSE your custom title block"* ([[_Sources/YT__vrVETTI5jQ_ifcarchitect_custom_titleblock|_vrVETTI5jQ]]) |
| **Markers, symbols, view titles** | **inside the add-on install** | ⚠️ global |

> **→ ⚠️⚠️ FOUR OF THE FIVE STYLING ARTEFACTS LIVE IN THE APPLICATION INSTALL DIRECTORY, NOT WITH THE PROJECT.** They are version-global, shared across every project, and destroyed by a reinstall.
>
> **For this repository that is close to disqualifying on its own terms, independent of drawing quality.** Every gate here rests on artefacts being committed, hashed and diffable — the frozen ink mask, the committed registration, the archived transcripts, `data/canonical/`. **A deliverable whose appearance depends on files sitting in `AppData/Roaming` is not reproducible**, and a rebuild on another machine would silently produce differently-styled sheets.
>
> **→ If any part of this is adopted, the styling artefacts must be copied into the repo and installed into place by the build**, not edited in situ. **The presenter himself works around it by hand** — *"make sure that you copy this somewhere safe."*

## Convention findings

6. **⚠️⚠️ LINE WEIGHT CONVENTIONS ARE NATIONAL, and he flags his own**: *"I've also made my own more extensive custom line weights, but I think it's good for people to just start with this, because **those are very South African standardy**."*
   > **→ ⚠️ JURISDICTION FLAG FOR THIS ENTIRE CHANNEL.** He is a South African architect — confirmed again in [[_Sources/YT_jTL3a6QwckA_ifcarchitect_custom_wall_type|jTL3a6QwckA]], where he saves *"my South African standard 220 masonry wall."* **Every drawing convention from these five sources carries an unstated national default**, and line weights especially. **Nothing from him is a Belarusian convention, and standing rule 4 applies: no regulatory routing.**
7. **He overrides a national convention on personal preference**: of the default section arrowheads — *"which I don't really like, because they're like Revit arrowheads. **I know this is standard in a lot of countries**, but I just prefer a normal arrow."* **→ Recorded neutrally as an instance of exactly the thing above: a shipped default is somebody's convention, and it is being replaced by somebody else's.**
8. **Dimension tick marks are SVG marker definitions** (`markers` template, `dimension marker start` / `end`), resized by halving every value — *"just makes it a bit more legible if you ask me."*
9. **Section marks are symbol definitions** (`symbols` template: `section arrow`, `section tag`), and **he suppresses the tag by zeroing its values** rather than by any supported means.
10. **⚠️ The view-title marker carries separate size entries PER FONT** — one set for Arial, one for OpenGost — so a size change must be made in both. **→ A maintenance smell, and a hint that the templates are hand-maintained rather than generated.**

## ⚠️ 11. Another hand-finishing admission

> *"**I still don't know how to move these guys away or delete them**, but at the moment **I just delete them afterwards in Inkscape** anyway."*

> **→ Third instance in this round of the final sheet being hand-finished in the vector editor**, after the arrangement ([[_Sources/YT_HEb7fWJduXg_ifcarchitect_page_layout|HEb7fWJduXg]] §2) and the clip workaround (§6 there). **The Bonsai → Inkscape → PDF path is not a pipeline with an optional manual step; the manual step is load-bearing.**

## 12. A comparative claim, recorded not evaluated

> *"It's a lot easier than editing patterns in Revit, for instance, without extra add-ons and stuff."*

⚠️ **No verdict routed** — a vendor comparison from an enthusiast, and this vault discards tool verdicts by default.

## What was deliberately NOT extracted

- **All file paths into the add-on install directory** — dated and machine-specific; only the *fact* of their location is kept, in §5.
- The specific CSS property values, dash arrays and marker coordinates — his worked example, and they encode a South African convention.
- **No prices, no regional claims routed, no regulatory content.**

## Source Notes

*Ifc Architect* (YouTube), 2023-01-25, 16 min, **read in full**. Open-source workflow throughout (Blender, BlenderBim, IfcOpenShell, Inkscape, Notepad); example files given away. **Claims are this presenter's, as opinion.** ⚠️ **Nothing is measured or verified.** ⚠️ **Sixth source from this presenter in the vault** — his agreement with himself is not corroboration. ⚠️⚠️ **He is a South African architect and his conventions are South African** (§6) — **this flag belongs on every convention taken from this channel.** ⚠️ **Dated** — the styling system is architectural and unlikely to have moved, but the directory layout and the shipped default stylesheet certainly have; **confirm against our installed Bonsai 0.8.6-alpha260801 before relying on any path.**
