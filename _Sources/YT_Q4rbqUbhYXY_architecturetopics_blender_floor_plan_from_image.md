---
source_type: video transcript (architecture-modelling tutorial channel, step-by-step)
source_url: https://www.youtube.com/watch?v=Q4rbqUbhYXY
video_id: Q4rbqUbhYXY
transcript_file: _Archive/processed_sources/20260913_architecturetopics_blender_floor_plan_from_image_392ce0dc.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2024-05-24 (confirmed via yt-dlp metadata)
channel: Architecture Topics
source_title: "How to Make 3d Floor Plan in Blender"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 9
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Architecture Topics: Tracing a Plan into Blender by Hand - and Three Findings That Land on Gated Questions (YouTube Q4rbqUbhYXY)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## What this is

**A 25-minute, entirely manual mesh-modelling tutorial: a raster plan image is scaled, traced as wall surfaces, extruded to height, and fitted with parametric doors and windows from Blender's bundled `ArchiMesh` add-on.** No AI, no IFC, no Bonsai. `promotional_ratio: low` — one free asset-kit link, no sponsor.

> **⚠️ It is extracted at 9 facts despite being about mouse work, because three of its steps are the practitioner's own solution to problems this project has gated in code.** That is the value filter working as intended: judged on *"does this change a field, a datum or a rule in our own model"*, not on whether the software is one we use.

## ⚠️⚠️ 1. The scale reference is a DOOR — and this is a worked counter-example to our own rule

With no scale bar on the image, he scales the whole plan off an assumed functional dimension:

> *"The numbers on the plan can go with Imperial or metric… I usually fix the scale depending on universal norms. For example, **the door width is generally between 90 and 100 cm**, the steps width for the staircase are 30. So **you need to choose one known factor and scale accordingly**."*

The method is careful in itself — he places a 1×1 m plane, snaps the 3D cursor to the door corner, switches the pivot to the 3D cursor so the image scales *from* that corner, then cross-checks with the measure tool on the door and stair.

> **→ ⚠️⚠️ BUT THE REFERENCE IS BOTH SHORT AND ASSUMED, AND THAT IS THE DEFECT.** *"Generally between 90 and 100 cm"* is an **11% spread stated by the practitioner himself**, and he then propagates it across the entire plan. **This is precisely what the longest-reference scale rule in [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] exists to prevent**: scale off the longest available reference, because the relative error of the reference becomes the relative error of everything. **A door leaf is one of the shortest elements on a plan, and a normative door width is not a measurement of THIS door.**
>
> **Standing rule 9 is engaged on two of its four clauses at once**: the scale is not independent of an assumption about the thing being measured, and no chain closure is attempted where an overall building dimension would have served. **Recorded as a counter-example, not as practice to adopt.**

## ⚠️⚠️ 2. Wall SURFACES, not centrelines — and his reason is ours

Offered as an explicit fork with a recommendation:

> *"There's two main ways to do that: either draw with surface or with lines. **Surface is the method I go by** — simply adding a plane and tracing it along the image walls. **The line method is just a vertex traced along the same walls, then at the end you add thickness to it, but that can generate problems** at the end, so stick with the surface one."*

> **→ Independent practitioner support for representing a wall as a SOLID rather than a centreline plus an offset.** This project reached the same place structurally: walls carry `clear_mm`, corner ownership is an explicit ledger (`wall_corners.csv`, thicker-then-longer), and `solid_mm = clear_mm + the corners a wall owns`. **He does not say what the "problems" are; the vault already knows, because it built a gate for them** — `check_wall_junctions.py` fails on an overlap, a gap, or an L-corner void that nothing owns. **A centreline model defers exactly those three decisions to whatever the thickening operation happens to do at a corner.**

## ⚠️⚠️ 3. A junction between two DIFFERENT wall thicknesses is a deliberate operation

The most directly transferable passage in the video. Reaching a point where a thin interior wall meets a thicker exterior one:

> *"The wall on the right is an **exterior wall with bigger width**, and **a cut is needed to match it with the inner wall while keeping it editable**."*

He adds an explicit loop cut, snaps it to the inner wall's face, then bridges the edge loops.

> **→ THE DIFFERING-THICKNESS JUNCTION DOES NOT RESOLVE ITSELF — IT IS AUTHORED.** *"While keeping it editable"* is the operative phrase: he is deliberately not collapsing the junction into fixed geometry. **This corroborates the design behind `build_wall_corners.py` and the corner ledger: something must decide which wall owns the shared solid, and the answer cannot be left implicit.** ⚠️ And it lands on the finding recorded last round — *generated geometry is placed, not associated* — from the opposite direction: **a human doing it by hand also has to place it, and he knows it, which is why he preserves editability.**

## ⚠️ 4. A geometry self-check that a practitioner actually runs

Before extruding, he selects everything and runs **merge-by-distance** — and then reads the result as a test:

> *"This way you can delete any overlap vertices that you might have made while working. **It's just for checking**, and **since we have zero vertices removed we are good to go**."*

> **→ This is a validator, run by hand, with a pass condition stated in advance: ZERO.** It is the same shape as the duplicate-key checks in `check_dxf_closure.py`. ⚠️ **And it carries the flaw this vault has already named**: `00_Master/Validator_Design_Discipline.md` records that *a collection that deduplicates destroys the defect being checked* — **his check deduplicates and reports in the same operation**, so a non-zero result silently fixes the problem rather than refusing it. **Worth recording as a cheap check with a known trap, not as a model gate.**

## Modelling conventions worth keeping

5. **⚠️ Window heads are aligned to door heads.** Doors are set to **2.1 m** head height and he then cuts and bridges *"on the same height 2.1 m"* for the windows too: *"I will align the top of the windows with the doors as in 2.1 m."* **→ A presentation and coordination convention — a single head datum across all openings on a storey** — and it is the kind of rule that makes a drawn elevation read as deliberate. ⚠️ Not yet a decision for this project; **flagged for `residential-bim-geometry-rules` alongside the open datum question.**
6. **Wall height taken as 2.7 m**, offered as *"the norm"*. ⚠️ **No jurisdiction is named and none can be inferred** — recorded as this practitioner's default only, and **not routed anywhere as a figure**. Rule 4 is not engaged (no regulatory claim is made), but the figure has no authority.
7. **Door swing direction is read off the source drawing**, not invented: *"you can check with the drawing image for the door opening direction."* Corroborates the swing-direction convention.
8. **Openings are cut by a boolean**: the add-on's door object carries *"a wireframe cube around it… to cut the walls."* **→ The void is an object the opening owns.** Worth noting against Bonsai's void management, where the same relationship is IFC-native rather than a mesh boolean.

## ⚠️ 9. The contrast that matters most: this produces a SHAPE with no DATA

`ArchiMesh` doors and windows are parametric — model, opening side, width, height — and he calls the parameters out. **But the output is mesh.** There is no type, no material layer set, no property set, no classification, and therefore **nothing to schedule and nothing to price.**

> **→ This is the clean statement of what Bonsai adds over Blender-plus-add-ons, and why the gap analysis marked the drawings and Qto subsystems `Adopt`** ([[_Inbox/planning/toolchain_gap_analysis_20260908|gap analysis]] §Kind 3). **A 25-minute workflow that ends in a correct-looking 3D plan carrying zero queryable data is exactly the trap this project's programmatic IFC route avoids.**

## What was deliberately NOT extracted

- The repetitive extrude/copy keystroke sequence — mouse work, and the presenter says so himself (*"I won't be commenting on repetitive process"*).
- Add-on and Blender version details — they date.
- **No prices, no regional claims, no regulatory content.**

## Source Notes

*Architecture Topics* (YouTube), 2024-05-24, 25 min. **Claims are this presenter's, as opinion.** ⚠️ Nothing in the video is verified against a measured drawing; the 2.7 m and 90–100 cm figures are the presenter's working defaults and carry no jurisdictional authority. ⚠️ **Same channel as [[_Sources/YT_mq63GWbgWdM_architecturetopics_inkscape_trace_to_blender|mq63GWbgWdM, which also covers xXmvs0PK_Bg]]** — concentration noted.
