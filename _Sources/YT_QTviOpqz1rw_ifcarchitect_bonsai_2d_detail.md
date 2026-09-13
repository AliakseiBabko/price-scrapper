---
source_type: video transcript (BlenderBIM/IFC specialist channel, Bonsai-era project series part 4)
source_url: https://www.youtube.com/watch?v=QTviOpqz1rw
video_id: QTviOpqz1rw
transcript_file: _Archive/processed_sources/20260913_ifcarchitect_bonsai_2d_detail_3e86eafd.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2025-05-20 (confirmed via yt-dlp metadata)
channel: Ifc Architect
source_title: "Bonsai Tutorial - Beginner Project - Part 4 - 2D detail"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Drawing and Documentation Conventions`, `Digital Toolchain / AI Workflow`)
fact_yield: 11
promotional_ratio: low
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Ifc Architect: ⚠️⚠️ A CONSTRUCTION DETAIL IS MODELLED, NOT DRAFTED - and What That Costs (YouTube QTviOpqz1rw)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

**Bonsai-era (2025-05), no dating caveat.** Part 4 of the series; read [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|Part 2]] first.

## ⚠️⚠️ 1. THE SCOPING FACT OF THE ROUND: to draw a detail, you must MODEL the construction at detail resolution

**To produce one roof-eaves detail, he does not draft a single line of the construction. He models it:**

- an **`IfcBeam` batten** on a project-wide **50×50 rectangular profile**, rotated 5° to the roof pitch;
- **arrayed at 300 mm spacing** via a parametric array modifier — *"if you were doing the entire structure, you would want the battens to go all the way to the end, it'll probably be about 12"*;
- the **roof slab moved down onto the battens**, then given a **50 mm overhang** by pulling one edge;
- a **fascia board** as a second beam on a new **20×300** profile, rotated 5° and snapped to the roof edge;
- a **ceiling** as an **`IfcCovering`**, sized to the room, angled to the roof.

> **→ ⚠️⚠️ A DETAIL SHEET IS NOT A DRAWING TASK. IT IS A MODELLING TASK AT A FINER RESOLUTION THAN THE REST OF THE MODEL, AND THE DRAWING FALLS OUT OF IT.**
>
> **This is the most consequential scoping fact in the round for this project, and it is a cost, not a benefit.** Our model is **nominal ±50 mm**, walls as solids from `data/canonical/`, with no battens, no layers within a build-up, no fixings. **Nothing in it can produce a construction detail**, and closing that gap means modelling the construction — a different resolution, a different data set, and a different maintenance burden from everything `check_dxf_closure.py` currently gates.
>
> **→ It sharpens the choice for `Sheet_Production_Roadmap.md` into three honest options**, none of which is free:
> 1. **Model at detail resolution** where a detail is genuinely needed — expensive, and the gated geometry chain would have to extend to cover it.
> 2. **Draft details in 2D** — cheap, and it inherits the known trap: **a drafted-only element is invisible to take-off** ([[18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join|Quantity Take-Off]] §5) **and, per [[_Sources/YT_r0ebxigzM6U_ifcarchitect_bonsai_section_elevation|Part 3]] §2, an unclassified modelled object is not even drawn.**
> 3. **Do not issue details at all** — legitimate for a fit-out where the trades own their own build-ups, and it should be a stated scope decision rather than a silent omission. ⚠️ **The vault already has the principle for this**: *a sheet may legitimately be blank, and the album should say so.*
>
> ⚠️ **This is flagged for the owner as a decision, not resolved here.**

## ⚠️⚠️ 2. A DETAIL IS A SECTION WITH A SMALL EXTENT AND A BIG SCALE — no new machinery

> *"We're going to select **section**. We're going to select **east**… **rename this detail one**… adjust the **width and height to be about 1,000**… change the scale from 1 to 100 to **1 to 10**."*

> **→ There is no "callout" or "detail" drawing type. A detail is the section generator with extent 1000 and scale 1:10**, against the section's 7500 at 1:100. **Confirms [[_Sources/YT_r0ebxigzM6U_ifcarchitect_bonsai_section_elevation|Part 3]] §1 from the fourth corner: one camera primitive, four sheet types.**

## ⚠️⚠️ 3. …but even a fully modelled detail still needs 2D drafting ON TOP

**This is the honest complication, and it undercuts the tidy version of §1.** After modelling everything, he still adds:

- **`batting` annotation for insulation** — a dedicated primitive, 150 thick, ***"the length is AUTO-CALCULATED, so you don't have to do the spacing like we used to before"***, then nudged 75 mm (half its thickness) to sit centred on the ceiling;
- a **`fill area`** for sealant;
- **fine lines drawn by hand over the battens** *"just so I know it's been cut"* — **manual 2D linework over geometry that is already modelled and already cut.**

> **→ THE DETAIL IS A HYBRID: MODELLED CONSTRUCTION PLUS DRAWN CONVENTION.** Insulation is not modelled because nobody models insulation; a sealant bead is not modelled because it is a bead. **And some of the drawn linework exists purely to make the cut legible** — the drawing needs marks the model cannot supply.
>
> ⚠️ **So option 2 in §1 is not really an alternative to option 1 — every detail is some of both.** The question is where the line sits.
>
> **`batting`'s auto-calculated length is the one piece of genuine automation found anywhere in Bonsai's annotation system**, and it is worth naming as the counter-example to §4: **it CAN be done, it just mostly is not.**

## ⚠️⚠️ 4. Text overflow, fixed by shrinking the font — the third independent instance

The long specification leader overruns:

> *"And you can see **IT IS OVERLAPPING**. So maybe I want to make this a bit smaller. I'm going to select the text, say edit, **adjust the font size to 1.5**… And there it all fits in perfectly."*

> **→ THIRD INDEPENDENT INSTANCE IN THIS VAULT OF MANUAL TEXT-COLLISION FIXING** — after [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|MeasureIt_ARCH]] §3 and the dimension work in [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|Part 2]] §1.
>
> **The open item *"does Bonsai place dimension text without per-instance intervention?"* is now answered three times over: it does not, and neither does anything else in this material.** The gap analysis's premise — that hand-rolling fails *specifically* on text collision and a tool would fix it — **does not survive.** Nothing on offer solves it. **Which makes our generative route, where offsets are computed from data we already hold, no worse and probably better.**

## ⚠️⚠️ 5. A second styling vocabulary — with the OPPOSITE casing

The sealant fill's appearance is set by typing into `object type`:

> *"Here where it says **object type**, you're just going to type in **SEALANT all caps**. So this is a default material type."*

> **→ HATCH MATERIALS ARE LOWERCASE (`brick`, `concrete`, `earth`, `sand`); FILL-AREA OBJECT TYPES ARE ALL CAPS (`SEALANT`).** Two unvalidated, case-sensitive vocabularies **with contradictory conventions**, and in this video the only way to learn either is to watch someone type it — he flashes the valid list on screen, *"which again I'll put on the screen so you can see"*, i.e. **it is not discoverable in the UI.**
>
> ⚠️ **CORRECTED later the same round: these are CSS CLASS NAMES.** [[_Sources/YT_dPWQbjaeoyo_ifcarchitect_lineweights_css|dPWQbjaeoyo]] shows the stylesheet is a literal `.css` file, so the vocabulary is **user-extensible and documented in that file** — not magic, just not surfaced in the UI. **The casing inconsistency is an artefact of the shipped default stylesheet, not a convention.**
>
> ⚠️⚠️ **Together with [[_Sources/YT_r0ebxigzM6U_ifcarchitect_bonsai_section_elevation|Part 3]] §4, this is the strongest concrete case the vault holds for adopting IDS validation.** A rule asserting that every material name and every annotation object type comes from a known vocabulary is cheap, and **the failure mode without it is silent: you get no hatch and no error.**

## ⚠️ 6. The preview is not the drawing — you must print to see the truth

Stated twice, unprompted:

> *"There is a preview, but you're going to see just now that **it's not too accurate. But when it prints, it's perfect.**"* … *"It's previewing the text over that space. **It's not always exactly perfect.**"*

> **→ THE VIEWPORT IS INDICATIVE; THE PRINTED SVG IS AUTHORITATIVE.** He regenerates and re-views after nearly every change.
>
> ⚠️ **This is mildly ENCOURAGING for the headless question**, and worth recording as such: **the authoritative render is already the batch/print path, not the interactive viewport.** A pipeline that never opens the viewport is not missing a more accurate view — it is using the accurate one. ⚠️ It also means **a GUI user cannot trust what they see while placing annotations**, which is part of why placement takes so long.

## 7. ⚠️ The anatomy of a specification note — worth copying as a shape

His leader text, read out in full:

> *"**50 mm roof sheeting** fixed to **timber battens at 300 centres**, installed **per manufacturer's instructions**, on **200×3 mm steel C channels at 1200 centre to centres**, at **5° slope**, **per engineer spec**."*

> **→ The structure is: MATERIAL + SIZE → FIXING → SPACING → deferral to the MANUFACTURER → SUBSTRATE + SIZE → its SPACING → GEOMETRY → deferral to ANOTHER PARTY.**
>
> ⚠️⚠️ **The two deferrals are the transferable part.** *"Per manufacturer's instructions"* and *"per engineer spec"* are the note **naming who owns the decisions it deliberately does not state.** That is the responsibility-seam principle already in [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §3 — *layer along the seam where responsibility changes hands* — **arriving at the annotation level instead of the layer level.** A note that states everything is claiming authority it may not have; a note that defers is scoping itself.
>
> ⚠️ **The construction described is a pitched timber-and-steel roof and is irrelevant to this flat** — the figures are not routed.

## Project-scoped named objects

8. **A profile is a project-wide named object**, like a material and a type: he creates `50x50` and `20x300` rectangular profiles, then assigns each to a beam's material. **→ Bonsai's model is consistently `types + profiles + materials`, all project-scoped, all named, all reusable.** ⚠️ **This is a good shape and our own data already resembles it** — `wall_materials.json` is the same idea. **A named, project-scoped, reusable definition is the unit; an instance references it.**
9. **`IfcCovering` is the class for a ceiling**, created from a duplicated `cover 30` type renamed `cover 20`. ⚠️ **Directly relevant** — this project will need ceilings and surface finishes, and `IfcCovering` is the correct class for them.
10. **⚠️ Array direction is chosen by trial and error**: *"let's just check which direction it goes… **you can see that is the wrong direction**… we probably want the X."* Local or global space is an option and he picks by looking. **→ A fourth instance of the implicit-direction/anchor theme** — after the wall-direction convention, the bottom-left-of-wall datum, and text alignment by origin. **Something always chooses an axis, and it is rarely stated.**
11. A newline in annotation text is `\n`, *"or you can add a literal."*

## What was deliberately NOT extracted

- All keystroke sequences and UI paths — much of this video is mouse work, and the ASR renders long `G Y` snap sequences as runs of "Y".
- **The roof construction figures** (50×50 battens at 300, 20×300 fascia, 5° pitch, 50 mm overhang, 200×3 C channels at 1200) — **a pitched timber roof, no jurisdiction stated, no relevance to a flat with a concrete slab.** Recorded only as evidence for §1 and §7.
- The spelling correction and re-print sequence.
- **No prices, no regional claims, no regulatory content.**

## Source Notes

*Ifc Architect* (YouTube), 2025-05-20, 18 min, **read in full**. `promotional_ratio: low` — a coffee-page mention at the end. **Claims are this presenter's, as opinion**; tool behaviours observed on one version on his machine. ⚠️ **Nothing is measured or verified.** ⚠️ **Fourth source from this presenter** — agreement with [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|PNoOyCHa_V0]], [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|VgvPk78IU0U]] or [[_Sources/YT_r0ebxigzM6U_ifcarchitect_bonsai_section_elevation|r0ebxigzM6U]] is one voice repeating, not corroboration. **The three-instance text-collision finding in §4 is the exception — it spans two unrelated presenters and two different tools.**
