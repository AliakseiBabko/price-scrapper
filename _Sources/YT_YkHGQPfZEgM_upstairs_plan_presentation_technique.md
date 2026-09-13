---
source_type: video transcript (architecture-presentation channel, Photoshop/Illustrator craft tutorial)
source_url: https://www.youtube.com/watch?v=YkHGQPfZEgM
video_id: YkHGQPfZEgM
transcript_file: _Archive/processed_sources/20260913_upstairs_plan_presentation_technique_402aca18.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions - ORIGINAL language)
upload_date: 2026 (confirmed via yt-dlp metadata)
channel: Upstairs
source_title: "How I Turn Simple Floor Plans Into Beautiful Architectural Drawings"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Drawing and Documentation Conventions`)
fact_yield: 4
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Upstairs: PARTIALLY PROCESSED - Three Workflow Rules, and a Styling Recipe Deliberately Not Routed (YouTube YkHGQPfZEgM)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## ⚠️ Partial extraction, and the honest reason

**Deferred on 2026-09-11 as "presentation/graphic style of a plan, which is a real open item (our sheets are functional, not handsome) - but it is the least urgent axis."** That assessment holds exactly.

**The bulk of the video is a Photoshop styling recipe** - path-blur long shadows, an off-white base, hand-painted dark and bright areas, blue-tinted shadows, grain, gradients on soft light, colour balance and levels. **It is real craft and it is well explained.** But this project's sheets are a **working deliverable that a contractor builds from**, not a portfolio piece - **so the recipe is recorded as existing and NOT routed as technique.** `fact_yield: 4`, and the number is honest.

**⚠️ If the owner ever decides the album should be presentable as well as correct, this is the source to come back to** - and it names its own references (MNMA Studio; the plan is from Terra e Tuma Arquitetos Associados), with an explicit instruction to credit them and not copy straight.

## ⚠️ Durable Facts - The Three Rules That Do Transfer

**All three are about keeping a rendered presentation honest and re-derivable, which is the part that matters regardless of style.**

1. **⚠️⚠️ Export the CUT ELEMENTS as a separate file.** The walls - everything the section plane cuts - must come out as their own PDF or PNG, separate from the complete plan. **"The only thing that you need to have is a separate document... with the cut elements, like being the walls. Because you need that to apply the shadows and everything else."** → **The cut layer is what carries depth. Any presentation pipeline needs it isolated, which is a requirement on the EXPORT step, upstream of any styling.**
2. **⚠️⚠️ Preserve scale across the vector-to-raster boundary.** Make the raster document the same dimensions and resolution as the source sheet (A4, A3, etc.) **"so that you don't change the scale here in Photoshop. That's very important. We want this to be up to scale at the end of the day."** → **A presentation pass must not silently destroy the drawing's scale**, which is exactly the hazard this vault already records from the other direction in [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §6 - a raster with no established scale is orientation, not measurement.
3. **⚠️⚠️ Place LINKED, never embedded.** Linking the source file means editing it - moving a wall, adding a detail - and saving **updates the presentation automatically.** *"That's linked, updated automatically. This is the best of both worlds."* → **A presentation is a VIEW of the drawing, not a copy of it.** **The same single-source principle this project already enforces far more strongly by generating drawings from `data/canonical/`** - recorded as independent corroboration at the presentation layer, which is the one layer where a copy is most tempting.

**One incidental item worth noting**: the source plan can come from BIM (Archicad, Revit) or 2D drafting (AutoCAD, Rayon), with Illustrator used only for line-weight tidying - **and he states that step is optional.** The pipeline does not depend on it.

## Confidence & Evidence Notes

- **`single-account`**, a craft tutorial; nothing here is a claim requiring verification.
- **ASR**: clean.
- **⚠️ The styling parameters are deliberately NOT routed** (hue ~30, saturation 4-8, taper 70%, and so on). They are aesthetic settings for one reference style, they would date as software changes, and **this project has no presentation deliverable they would serve.** Recorded here only so a future session knows the source covers them.
- **No prices; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice.md` §3** - the three workflow rules: separate cut-elements export, preserve scale across the raster boundary, link rather than embed.
- **5b**: no prices; no conversion owed.
