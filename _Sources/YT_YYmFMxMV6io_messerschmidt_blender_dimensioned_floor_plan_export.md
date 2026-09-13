---
source_type: video transcript (Blender workflow channel, add-on pipeline tutorial)
source_url: https://www.youtube.com/watch?v=YYmFMxMV6io
video_id: YYmFMxMV6io
transcript_file: _Archive/processed_sources/20260913_messerschmidt_blender_dimensioned_floor_plan_export_3ca641d8.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2024-04-23 (confirmed via yt-dlp metadata)
channel: Ruben Messerschmidt
source_title: "How to create a FLOOR PLAN with Dimensions in Blender"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 9
promotional_ratio: medium
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Ruben Messerschmidt: A Model-to-Annotated-SVG Pipeline Outside Bonsai - and Its THREE Silent-Failure Modes (YouTube YYmFMxMV6io)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this source matters here

**It is the only source in this batch that runs a complete model → cut → annotate → paper-size → vector-export pipeline, and it does it in plain Blender with add-ons rather than in Bonsai.** That makes it **a direct comparator for the decision already recorded in [[_Inbox/planning/toolchain_gap_analysis_20260908|the gap analysis]] §Kind 3** — adopt Bonsai's drawings subsystem for annotated sheets, against our hand-rolled SVG→PDF.

> **⚠️⚠️ And it complicates that decision rather than confirming it. See §3.**

`promotional_ratio: medium` — three add-on links, two of them free tools he credits by author name (MeasureIt_ARCH, by Kevin Crest and Antonio Vasquez), one a product of his own channel's ecosystem.

## 1. The pipeline, in four stages

1. **Section box** — a bounding box around the model, whose face handles are dragged to set the cut plane. *"Bring it down where you want the cut."*
2. **Generate cross-section and elevation drawings** from that box.
3. **Export those drawings as meshes** (DXF also offered), with a *clean up* option *"to remove any unnecessary vertices"*, into their own collection.
4. **Dimension them with MeasureIt_ARCH**, then set a camera, a **paper size (A3) and orientation**, an output path, and run the `render vector` operator to emit **SVG**.

> **→ Structurally identical to what this project already does**: cut the model, extract 2D, annotate, place on a sheet, emit vector. **The difference is only which engine performs each stage.** Recorded as confirmation that the stage decomposition itself is standard, not a local invention.

## ⚠️⚠️ 2. THREE WAYS THIS PIPELINE SILENTLY PRODUCES A WRONG DRAWING

**This is the extraction's main content.** Each is a case where the export *succeeds* and the sheet is *wrong*, and in each case the presenter only knows because he has hit it before.

**(a) Edges below an angle threshold are silently dropped.**
> *"As you notice, **it didn't take all the edges into account**, which you can see here for example — because **these edges have a very low angle**. Simply increase the crease angle, so in our case **175°** should be fine, then remove the elevation and recreate it."*

> **→ A GENERATED DRAWING CAN OMIT REAL GEOMETRY AND STILL LOOK FINISHED.** The omission is a function of a threshold parameter, so it is systematic: **every edge below the crease angle disappears from every sheet**. Near-coplanar surfaces — a shallow ramp, a slight level change, a chamfer — are exactly the geometry a renovation drawing must show. ⚠️ **Raising the threshold costs time and he says so** (*"this takes even longer because more edges means more calculations"*), which is the pressure that keeps people on a lossy default.

**(b) The drawing's own lines are not exported unless a line group is created.**
> *"If we would export everything now, **we would only see the dimensions** — this because we have to add a line group to our mesh… this adds lines in place of all edges in our mesh which will be visible in the final export. **Actually it looks like nothing happened**, but if you go into the object properties…"*

> **→ ⚠️⚠️ THE DEFAULT EXPORT YIELDS THE ANNOTATIONS WITHOUT THE GEOMETRY.** A sheet of dimension strings floating over nothing. **It is a total, silent omission whose enabling step gives no visible feedback when performed** — *"it looks like nothing happened."* **This is the purest example in the batch of a step you can only get right by already knowing about it.**

**(c) DXF export has acknowledged scaling issues.**
> *"You can bring up the search menu again and search for `render to dxf` and execute this one — **but be aware of some scaling issues that might happen**, and therefore check out the documentation of the MeasureIt_ARCH add-on where they go in detail about how to fix these issues."*

> **→ ⚠️⚠️ AN EXPORT PATH WITH KNOWN, UNQUANTIFIED SCALE DEFECTS IS DISQUALIFYING FOR THIS PROJECT.** Every gate here is dimensional — `check_dxf_closure.py` asserts drawn length and thickness against the record *and* against the PDF's hatched solids. **A route whose own documentation has a section on fixing its scaling is not a route we can put a deliverable through**, whatever its annotation quality. Recorded as a hard exclusion, not a caution.

⚠️ A fourth, smaller one: the `render vector` operator is reachable only through the F3 search menu. *"There actually should be a button somewhere to do this, but to be honest **I didn't find it**."*

## ⚠️⚠️ 3. Text collision is handled MANUALLY here too — which qualifies the adopt decision

The gap analysis's stated reason for adopting Bonsai's drawings subsystem is that hand-rolling *"fails exactly here: dimension chains collide on dense MEP plans; excessive custom code required to handle text overlaps."*

**This source shows the same failure inside a purpose-built annotation add-on, fixed one dimension at a time by hand:**

- A dimension whose arrows point inwards: found by hiding entries one by one in a list to identify it, then set `tweak distance` to **−1** to flip it outward.
- A dimension too narrow for its own text: *"this is way too narrow to fit the text in here, **it gets blind outside**"* — fixed by setting that dimension's alignment to left.
- Defaults unusable at architectural scale: font size raised to **30**, line weight to **2**, arrow size to **30**, because *"it's way too thin and the font is way too small."*

> **→ ⚠️⚠️ ADOPTING A TOOL DOES NOT SOLVE THE TEXT-COLLISION PROBLEM; IT RELOCATES IT.** The add-on has a **named style set** (a real advantage — one edit restyles every dimension using it), **but per-dimension placement remains a manual override.**
>
> **This does not overturn the gap analysis's `Adopt` verdict — Bonsai is a different tool and may do better — but it removes the assumption underneath it.** The honest form of the open question becomes: *does Bonsai's drawing subsystem place dimension text without per-instance intervention, and is that placement reachable headless?* **Placement, not annotation capability, is what decides whether an annotated sheet can be generated by `make`.** ⚠️ **The gap analysis's open item should be sharpened to that.**

## Mechanism worth keeping

4. **A named style set is the right abstraction for annotation.** Dimension style and line style are separate, both scene-level, and every annotation references one. **→ This is what our SVG pipeline should have if it keeps the annotated sheets**: a single style object, not per-element attributes.
5. **Annotation defaults are authored for object scale, not building scale** — every figure needed multiplying by roughly an order of magnitude. **→ Any generated sheet needs an explicit style pass; there is no usable default.**
6. **Background set to white before annotating**, *"that we can see all the black lines much better."* Trivial, but it is the same presentation-pass instinct already recorded in [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]].
7. **Sheet setup is camera + view + paper size + orientation + output path**, with the path testable before export by a button that opens the browser. **→ Verify the output location before running a long export.**
8. **Drawings live in their own collection**, with the source model and section boxes disabled. **→ The drawing is a separate artefact from the model, not a view of it.** ⚠️ That is the weakness of this whole route: **once exported as meshes, the drawings no longer track the model.** It is the *placed, not associated* defect recorded across three tools in [[_Inbox/planning/astra_modelling_batch_20260913|the Astra batch]] §3, arriving now in the drawing layer rather than the geometry layer. **A dimension on an exported mesh cannot know its model changed.**
9. Cut plane is set by dragging a box handle by eye — **no cut height is stated or entered numerically anywhere in the video.** ⚠️ For a plan cut, the height is a convention with consequences (which openings appear, which are dashed above). **An unstated cut height is an unstated drawing convention.**

## What was deliberately NOT extracted

- Add-on version details and UI paths — they date.
- The presenter's own section-box product pitch and the two link-outs.
- **No prices, no regional claims, no regulatory content, no dimensional figures** — every number in the video is a font or arrow size.

## Source Notes

Ruben Messerschmidt (YouTube), 2024-04-23, 14 min, **read in full**. ⚠️ This video carries **author-supplied manual English subtitles in addition to the `en-orig` track** — the transcript quality is above this batch's norm. **Claims are this presenter's, as opinion.** ⚠️ **No output is verified against a measurement**: the word "precise" appears in the title and the opening line, and **nothing in the video measures anything.** The scaling defect in §2(c) is acknowledged and left unquantified.
