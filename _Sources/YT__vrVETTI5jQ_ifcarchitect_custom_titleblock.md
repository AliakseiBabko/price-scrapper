---
source_type: video transcript (BlenderBIM/IFC specialist channel, short how-to)
source_url: https://www.youtube.com/watch?v=_vrVETTI5jQ
video_id: _vrVETTI5jQ
transcript_file: _Archive/processed_sources/20260913_ifcarchitect_custom_titleblock_382d3189.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2023-03-27 (confirmed via yt-dlp metadata)
channel: Ifc Architect
source_title: "Beginner Tutorial - Custom Titleblock in BlenderBim - with Inkscape - in 9mins"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Drawing and Documentation Conventions`)
fact_yield: 8
promotional_ratio: none
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Ifc Architect: A Title Block Is an SVG Template With `{{ }}` Placeholders - the Same Binding as the Tags (YouTube _vrVETTI5jQ)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

**BlenderBim-era (2023-03); read because no Bonsai-era replacement exists.** `promotional_ratio: none`.

## ⚠️⚠️ 1. THE FINDING: title blocks and tags share one data-binding mechanism

Opening the shipped A1 template in Inkscape, he points at the placeholders:

> *"You can see it does some smart stuff. **You see these little squiggly brackets — those are REFERENCES.** So where **drawing title** is, **it'll actually look at the drawing title.**"*

> **→ ⚠️⚠️ THE SAME `{{ field }}` TEMPLATE SYNTAX AS THE SMART TAGS** in [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|VgvPk78IU0U]] §3, where a leader was bound to a column and `{{name}}` resolved to *"column"*.
>
> **So the whole annotation-and-titling system is ONE mechanism: an SVG document with placeholders resolved against model and drawing data.** Tags, leaders, view titles and title blocks are all the same thing at different scales.
>
> **⚠️⚠️ This is the strongest "we can simply do this" finding of the round.** A template-substitution pass over an SVG is a string operation — **our generator already produces the SVG and already holds the data.** Nothing about it requires Bonsai, Blender or IFC. **It is the mechanism, not the tool, that is worth adopting**, and it directly answers the standing question of whether our pipeline can carry derived annotation: **yes, and cheaply.**

## ⚠️⚠️ 2. Custom title blocks live in the APPLICATION INSTALL and are destroyed by a reinstall

> *"I just want to make sure that you **copy this somewhere safe**, because **if you reinstall BlenderBim this file will default to just these three, so you will LOSE your custom title block.**"*

> **→ THE TITLE BLOCK IS PART OF THE DELIVERABLE AND IT IS NOT STORED WITH THE PROJECT.** ⚠️ **Together with the hatch patterns, markers, symbols and view titles** — all in the same install directory — **this is the scoping problem set out in [[_Sources/YT_dPWQbjaeoyo_ifcarchitect_lineweights_css|dPWQbjaeoyo]] §5**, and it is the concrete constraint on adopting any of this here: **anything we depend on must live in the repo and be installed by the build, never edited in place.**
>
> ⚠️ Note the inconsistency once more: **the stylesheet is project-local; the title block is not.**

## 3. An existing title block from any CAD imports as vector, via PDF

His stated route: take the title block you already have — *"it could be AutoCAD, it could be Revit, ArchiCAD, anything"* — **print it empty to PDF**, open the PDF in Inkscape, select all, and paste it onto Bonsai's template with the template's own layers **locked** so they are not disturbed.

> **→ A PDF TITLE BLOCK IS A VECTOR IMPORT PATH.** Practical, and it means an existing sheet identity is not lost when the drawing engine changes. **Only the shipped rectangle border is kept from the original template; everything else is replaced.**

## ⚠️ 4. Inkscape specifically — the file does not survive Illustrator

> *"You're going to want to do this **in Inkscape and not Illustrator** or something else — **for some reason it doesn't actually work in Illustrator.**"*

> **→ AN SVG DIALECT DEPENDENCY.** ⚠️ Recorded as a caution about the format's portability in practice: **"it is SVG" does not mean "any SVG tool round-trips it."** Relevant if our pipeline ever reads or writes these files — the safe assumption is that Bonsai's SVG carries structure (layers, ids, placeholders) that a different editor will rewrite or discard.

## ⚠️ 5. He raster-traces a logo that was already vector, and loses information doing it

> *"We're going to go to **path → trace bitmap**… the default should work fine for a black and white drawing… **and it turns it into a vector drawing — and it was initially a vector drawing, so I'm doing a lot of nonsense**, but yeah, that worked out nicely. **Unfortunately I think I lost my grey there.**"*

> **→ A LOSSY CONVERSION APPLIED TO CONTENT THAT DID NOT NEED IT, WITH THE LOSS NOTICED AND ACCEPTED.** He is candid about both halves.
>
> ⚠️ **Recorded because the vault has a cluster of findings on exactly this**: auto-tracing recovers shape and discards measurement ([[_Sources/YT_mq63GWbgWdM_architecturetopics_inkscape_trace_to_blender|mq63GWbgWdM]]), and *a presentation pass must not silently destroy the drawing's scale*. **Here the same reflex is applied to a logo and costs only a grey. Applied to a drawing it costs the drawing.** **The rule generalises: never raster-trace something you already have as vector.**

## Mechanics

6. **Three title-block sizes ship by default**, A1 among them; a custom one is saved alongside them and is then **offered automatically** by the sheets tool — *"because it's in that templates folder, it is available there."*
7. **Naming carries the sheet size and orientation**: he saves as `A1-IFC Arc-horizontal`, *"because it's landscape."* **→ Size and orientation in the filename, which is how the tool distinguishes them.**
8. **A title block is a sheet-level object**: create a sheet from the template, add drawings to it, `create sheets`. Corroborates [[_Sources/YT_HEb7fWJduXg_ifcarchitect_page_layout|HEb7fWJduXg]].

## What was deliberately NOT extracted

- **The install-directory path** — dated and machine-specific; only the fact of its location is kept (§2).
- The Inkscape copy-paste and text-editing steps — mouse work.
- His own title-block content and logo.
- **No prices, no regional claims, no regulatory content, no dimensional figures.**

## Source Notes

*Ifc Architect* (YouTube), 2023-03-27, 8 min, **read in full**. Entirely free and open-source tooling; OSArch community. **Claims are this presenter's, as opinion.** ⚠️ **Nothing is measured or verified.** ⚠️ **Seventh source from this presenter in the vault**, and ⚠️ **he is a South African architect** — see [[_Sources/YT_dPWQbjaeoyo_ifcarchitect_lineweights_css|dPWQbjaeoyo]] §6; **his drawing conventions carry an unstated national default.** ⚠️ **Dated**: the `{{ }}` binding and the SVG template format are architectural and are corroborated by the Bonsai-era [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|VgvPk78IU0U]]; **the directory layout and shipped templates have almost certainly changed.**
