---
source_type: video transcript (architecture-modelling tutorial channel, short method video)
source_url: https://www.youtube.com/watch?v=mq63GWbgWdM
video_id: mq63GWbgWdM
transcript_file: _Archive/processed_sources/20260913_architecturetopics_inkscape_trace_to_blender_602c3437.txt
transcript_file_pt2: _Archive/processed_sources/20260913_architecturetopics_inkscape_trace_to_blender_pt2_b79ecdaa.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2022-08-11 (confirmed via yt-dlp metadata)
channel: Architecture Topics
source_title: "How To Turn JPG image to 3D Floor Plan - Blender"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 5
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
covers_also: xXmvs0PK_Bg (2025 re-record of this same tutorial, same channel, same title - handled here, see below)
---

# Source Note - Architecture Topics: Raster Plan to Mesh via Inkscape Auto-Trace - and a Practitioner Discarding the Good Scale Reference for a Bad One (YouTube mq63GWbgWdM)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## ⚠️ Pair handling, and why the OLDER recording is the one processed

**`xXmvs0PK_Bg` (2025-07-25) and `mq63GWbgWdM` (2022-08-11) are the same tutorial, same channel, same title, same method**, re-recorded three years apart. **One is processed, per the value filter. The one chosen is the older.**

> **⚠️⚠️ That inverts the supersession rule applied elsewhere in this batch, and deliberately.** The rule that a later recording supersedes an earlier one exists **because capability verdicts date** — it is doing real work on `@IfcArchitect`, where the add-on was renamed and its UI overhauled between takes. **Here nothing about the software changed**: both recordings drive the same Inkscape *Trace Bitmap* dialogue with the same settings. **With the dating reason absent, the rule has no grip, and the decision falls back to which recording says more.** The 2022 take is 5 minutes against 3, and **it contains the single most valuable passage in either** (§2). The 2025 take adds only that the traced background layer is street artwork to delete, and that the simpler of two detail layers is the one to keep — **both folded in here.** `xXmvs0PK_Bg` is recorded `duplicate_skipped`.

## 1. The method, which is genuinely cheap and genuinely free

**Raster plan → Inkscape *Trace Bitmap* → SVG → Blender.** The specific settings are the only part worth keeping, because the defaults do not work:

- **Multi-colour tab with detection mode set to *colours*, not single-scan edge detection.** His reason is generality: *"this way we can get the result from any kind of image."*
- **`Stack` enabled** — *"this way we get each layer separated"*, so each traced colour arrives in Blender as its own object.
- **Scan count started at the minimum** and raised only as needed, watching the preview. For a black-and-white plan he leaves it at 2.
- In Blender: import SVG (curves) → convert to mesh → **`limited dissolve`** to clean it, because *"if we go into edit mode you would notice that this is now a mess"* → grow-selection to isolate the walls → separate → extrude on Z.

> **→ ⚠️ The `limited dissolve` step is the tell: auto-tracing produces dense, redundant vertices, and the output needs cleaning before it is usable geometry.** He also concedes the cleanup is incomplete — *"you will still have some lines like this which you can fix manually."* **Auto-trace gets you most of a polygon, not a polygon.**

## ⚠️⚠️ 2. The passage that matters: he HAD the right scale reference and threw it away

The plan he traces carries printed dimension strings. He notices them, states they would fix the scale, and then does not use them:

> *"Due to this is generated from an image, **the scale is no way near the real thing**. However, we can look for common things like door or steps and just scale it to fit using any known object. … **And the plan have the dimensions with it, so you can easily fix the scale — though those numbers are probably with feats. So I will rescale this plan using the door length.**"*

> **→ ⚠️⚠️ A CORRECT REFERENCE WAS AVAILABLE AND WAS DISCARDED FOR AN ASSUMED ONE, OVER AN UNRESOLVED UNIT.** The printed dimensions are the plan's own statement about itself and would have given **chain closure** — the fourth clause of standing rule 9, and the strongest form of scale evidence there is. The door width is an assumption about a *class* of object, applied to *this* object, over a spread the same channel elsewhere states as **90–100 cm**.
>
> **And the stated reason for discarding it is not that the dimensions are wrong — it is that he is unsure whether they are feet or metric.** *"Probably with feats."* **An unresolved UNIT was treated as grounds to abandon the measurement rather than grounds to resolve it.** Resolving it is one division: any printed overall against any other printed figure fixes the unit immediately, and a plan with several dimension strings over-determines it.
>
> **This is the cleanest worked instance in the vault of the failure standing rule 9 was written for**, and it belongs next to the seven already in `00_Master/Evidence_Reading_Discipline.md`. **Recorded as a counter-example.** It is the same defect as the sibling video's door-width scaling ([[_Sources/YT_Q4rbqUbhYXY_architecturetopics_blender_floor_plan_from_image|Q4rbqUbhYXY]] §1) but worse, because there no better reference existed and here one did.

## ⚠️ 3. "The scale is no way near the real thing" — stated plainly, and it is the honest part

To his credit he does **not** claim the trace is to scale. The output is explicitly a shape that must be scaled afterwards by external reference.

> **→ Corroborates the finding already held from the previous round: TRACING RECOVERS TOPOLOGY, NOT MEASUREMENT.** See [[_Inbox/planning/astra_modelling_batch_20260913|the Astra batch note]] §3.5, where a tracer's own author assigns wall thicknesses by hand afterwards, and where *"automatically up to scale"* from a photo was flagged as a claim to distrust. **Three independent sources now agree: the geometry that comes out of an image carries no dimensional authority of its own.**

## 4. Source provenance is zero, and it is worth naming

Both recordings open by telling the viewer to search Google or Pinterest for a plan image and download one. **The traced result therefore has no known author, no known scale, no known jurisdiction and no known units** — which is exactly how the unit confusion in §2 arose.

> **⚠️ Directly relevant to this project's own discipline.** `_Precedents/` exists because *a role is a claim, so it needs someone to have looked* (standing rule 11), and an unfurnished plan was once filed as a handover state when it was a demolition *after* state. **A plan pulled off an image search and traced has strictly less provenance than that.** Nothing built this way could enter `data/canonical/`.

## 5. Colour-based separation is a real idea, and this project already does the better version

Tracing on **colour** rather than edges, with each colour landing as its own object, is a workable way to get walls apart from furniture and annotation in one pass.

> **→ Noted as the naive counterpart to `tools/layout/render_vector_extraction.py`, which recovers **hatch-validated wall solids** directly from the source PDF's vector content** — 37 recognised, 17 claimed — **with the PDF's sha256 asserted at check time** (`vector_extent_oracle.py`). **Vector-native extraction from an authored PDF beats raster auto-trace on every axis that matters: no resampling, no cleanup pass, and a provenance chain.** The method here is for when you only have a picture. **This project does not only have a picture.**

## What was deliberately NOT extracted

- Inkscape and Blender version details and UI locations — they date, and both recordings differ on them.
- The extrude-to-height step — no height figure is given in this video.
- **No prices, no regional claims, no regulatory content.**

## Source Notes

*Architecture Topics* (YouTube), 2022-08-11, 5 min, with its 2025-07-25 re-record `xXmvs0PK_Bg` folded in. **Claims are this presenter's, as opinion**, and he is candid about his own unfamiliarity with Inkscape (*"I'm as noob as it gets with this program"*). ⚠️ **Third source from this channel in this batch** alongside [[_Sources/YT_Q4rbqUbhYXY_architecturetopics_blender_floor_plan_from_image|Q4rbqUbhYXY]] — concentration noted; **the door-width scale habit is a channel habit, not an independent corroboration.**
