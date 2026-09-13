---
source_type: video transcript (architecture channel, beta-product walkthrough)
source_url: https://www.youtube.com/watch?v=9pDOD_xx2kA
video_id: 9pDOD_xx2kA
transcript_file: _Archive/processed_sources/20260913_melosazemi_sketch_to_cad_tracing_c80e9042.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions - ORIGINAL language)
upload_date: 2026-07-21 (confirmed via yt-dlp metadata)
channel: Melos Azemi
source_title: "From sketch to CAD : automated floor plan tracing"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 6
promotional_ratio: high
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Melos Azemi: Automated Floor-Plan Tracing, and a Scale Claim to Distrust (YouTube 9pDOD_xx2kA)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this source, and what it actually is

**Selected because "sketch to CAD, automated floor plan tracing" sits directly on this project's live `v0` blocker** - reconstructing geometry from a raster plan.

**⚠️ It is a product walkthrough for a named beta tool for architecture studios**, with a free-account call to action and an explicit recommendation to try it. **`promotional_ratio: high`.** The tool is not this project's toolchain and **no product verdict is routed** - what is extracted is the shape of the capability and one claim worth distrusting.

## Durable Facts - What Automated Tracing Actually Delivers

**The flow**: photograph a hand sketch, drag the image onto the canvas, and the tool offers *"floor plan detected - trace it into editable walls, or keep it as an image."* It **detects multiple floor plans separately** within one image or PDF. Tracing takes seconds and returns **walls and windows placed as editable objects.**

**⚠️⚠️ His own scope statement is the most important line in the source, and it is honest:**

> *"I just want to set the expectations straight... this is not something where you just click once and it's fully automating your documentation. **This is simply a tracer which allows you to get a conceptual floor plan from a sketch.**"*

**→ A tracer produces a CONCEPTUAL plan, not documentation.** That is exactly this vault's own position - a raster is orientation and concept, not measurement - stated by a vendor demo that had every incentive to claim more.

**Named failure classes, all of which he fixes by hand on camera:**

- **Parts of the LANDSCAPE detected as walls**, deleted.
- **Door orientation wrong**; doors re-dragged and re-oriented, some duplicated and moved because *"because of the presentation of some of the doors, it did not get them exactly as they should."*
- **A wall added that should not be there**; missing walls drawn manually to close a kitchen corner.
- **Windows misplaced**, needing to be moved onto the wall line.
- **⚠️ And the honest caveat: *"the results will very much vary in terms of how clear they are to read and detect."*** **Legibility of the source governs the result.**

## ⚠️⚠️ The Finding: Wall Thickness Is NOT Recovered - It Is Assigned Afterwards

**After tracing, he sets wall thicknesses HIMSELF: exterior walls "at least 30 cm", interior walls "20 cm".**

> **→ The trace recovers TOPOLOGY, not THICKNESS. Thickness arrives from convention, applied by a human after the fact.**
>
> **⚠️ This matters directly here.** This project's `data/canonical/wall_blocks.csv`, `wall_corners.csv` and the `solid_mm = clear_mm + owned corners` rule exist precisely because **wall thickness is a decided, sourced quantity rather than something read off a picture.** **An automated tracer confirms the split from the other side: it gives you the lines and leaves the thickness to you.**

## ⚠️⚠️ A Claim To Distrust - "automatically up to scale" from a skewed photo

> *"You don't have to have the floor plan taken in a picture which is completely parallel to it. So even if there's some skewed perspective, [it] will automatically fix it for you. **That way it is completely up to scale.**"*

**⚠️⚠️ The first half is plausible and the second does not follow.** Perspective rectification can recover a plane's SHAPE. **It cannot recover absolute SCALE, because scale requires a known real-world dimension somewhere in the image - and none is supplied, identified or entered anywhere in the demonstration.**

- **This vault has established the point twice from opposite directions**: `f0EU_xbavEA`'s **two-point scale verification** (register on one printed dimension, verify on a second), and `9-hQsyWSnm4`'s **register on the LONGEST known distance** - both of which exist because **a registration needs a reference.**
- **→ Recorded as an unverified vendor claim that contradicts an established finding.** *"Completely up to scale"* with no stated reference is the same failure class as the AutoCAD tutorial that rescaled its underlay by eye ([[_Sources/YT_EibFZPrtAp0_civilengineering_chatgpt_dimensions_antipattern|EibFZPrtAp0]]). **A traced plan with no established scale is a shape, not a measurement.**

## Durable Facts - The Rest, Briefly

- A **hatch library** (searchable - he applies a towel hatch to bathrooms and scales it), an **asset library of furniture blocks by category**, fills, and simple draw tools for things like rugs.
- Rooms and zone labels are generated with the trace and are resized and repositioned by hand for legibility.

## Confidence & Evidence Notes

- **`single-account`**, a vendor demonstration by an enthusiast. **No measurement of any kind is performed** - no dimension is checked against the sketch at any point.
- **⚠️ `promotional_ratio: high`; the product name and its feature set are deliberately not routed** - a beta tool's capabilities date fast. **The scope statement, the failure classes, the thickness finding and the scale claim are what transfer.**
- **ASR**: good. **No prices; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice.md` §6** - tracing gives topology and not thickness; and the "automatically up to scale" claim as one to distrust, against the two established registration rules.
- **5b**: no prices; no conversion owed.
