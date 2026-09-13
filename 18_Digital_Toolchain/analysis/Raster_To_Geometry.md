# Getting a dimensioned raster into geometry

**How practitioners turn a plan image into measurable geometry, and how they establish and check the scale.** Extracted from [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] on 2026-09-13, unchanged, when that page reached the 400-line backstop. This is the topic that bears on the open `v0` task: `00_Master/project_decisions.md` records that **`v0` has no geometry and it blocks layout selection**, with the route being reconstruction from the printed dimension strings over the registered raster.

> [!WARNING]
> **Every claim here is a named practitioner's opinion.** ⚠️ The registration findings bear directly on `tools/layout/raster_fidelity.py` and on `00_Master/Geometry_Variance_Study.md` — see the flagged items below. **Nothing here has been checked against our committed registration yet.**

## 6. Getting a dimensioned raster into geometry

**From an English-language batch on AI-agent modelling — triage in [`_Inbox/planning/ai_agent_modelling_sources_triage_20260911.md`](../../_Inbox/planning/ai_agent_modelling_sources_triage_20260911.md).** These bear on the open `v0` task: `project_decisions.md` records that **`v0` has no geometry and it blocks layout selection**, with the route being reconstruction from the printed dimension strings over the registered raster.

### ⚠️⚠️ A scaled raster is for orientation, not measurement — type the dimensions, don't click the pixels

Justin Geis (TheSketchUpEssentials), stated plainly: *"If you're trying to model this building exactly, you shouldn't be coming in here and using visuals in order to figure out where this is going to go… you actually need to model using the dimensions if you want this to be exact. If you're just trying to get it close enough, it doesn't really matter."*

**→ Independent corroboration of the route this project already chose for `v0`.** Aaron Dietzen (Trimble SketchUp) gives the mechanical reason: a raster *"is literally a bunch of dots… that could be scaled to any size"* and **nothing in it can be snapped to** — *"it doesn't know that this is an end point."*

### ⚠️⚠️ Two-point scale verification — register on one printed dimension, verify on a second

**A check we do not currently have, and it is cheap.** Scale off one known printed dimension, preferably a long one; **then measure a different feature elsewhere in the drawing and compare it against its own printed value.** Geis: *"And I always want to check… I like to draw a line somewhere else."* His honest verdict on the residual: *"that's about as close as you're going to get by scaling a document like this."*

**This is not chain closure.** Chain closure asserts that a run of dimensions sums to a known whole. This asserts the **registration itself** against a printed figure that played no part in establishing it — the same independence principle as `tools/layout/vector_extent_oracle.py`. **Add it to the `v0` reconstruction procedure before the hand work starts.**

#### ⚠️⚠️ The worked counter-example: verifying on the SAME dimension proves only that the tool obeyed you (2023)

**The rule above says verify on a SECOND dimension. Here is what happens one dimension short — same presenter, a different video, and he believes he has verified something.**

He sets the image scale by clicking the two endpoints of a printed 5'9" string. Then:

> *"The first thing I like to do is click on the walls button and **just draw a wall along this dimension just to double check that this length got set correctly**. And notice how this length **did indeed get set to five foot nine inches**. So I'm going to undo this."*

**The instinct is right and rare — a disposable probe, drawn, read back, discarded.** ⚠️ **But the probe measures the dimension the registration was built from, so it can only fail if the tool ignored its input.** It cannot detect a misread endpoint, a wrong printed figure, a unit error, or sheet distortion.

> **→ This is the failure class `00_Master/Validator_Design_Discipline.md` already names — *a checker must not share an editable measurement with the thing it checks* — and it is the same defect that retired `overlay_dxf_on_raster.py`, which fitted its registration on the DXF it was scoring.** [source: [[_Sources/YT_xlmbZHIaHJw_cgessentials_homebuilder_floor_plan_from_scan|YT_xlmbZHIaHJw]]] ⚠️ Seventh source from this presenter — treat all of his material as one voice.

### ⚠️⚠️ …and register on the LONGEST known distance — the missing half of the rule above (Craftelectric / MoonCad, 2025)

**The block above says to verify on a second dimension, and notes "preferably a long one" only in passing. A second, unrelated source states the rule properly, with its reason:**

> «Нужно выбрать **самое большое известное расстояние** на вашем плане… Даже 5-6 м уже будет достаточно, но **чем длиннее выбранное расстояние, тем точнее получится масштаб**.»

His own registration uses **18,229 mm** — the full length of the premises.

- **The reasoning is sound and not merely asserted: the relative error of a registration scales inversely with the length of the reference**, so a short reference multiplies its own reading error across the whole drawing. **A 5 mm misread on a 500 mm reference is a 1% scale error; the same misread on a 18,000 mm reference is 0.03%.**
- **→ The two halves combine into one procedure: REGISTER on the longest known dimension, then VERIFY on a second, independent one.**
- **⚠️ Directly checkable here**: `tools/layout/raster_fidelity.py` registers mm→px from the PDF's hatched wall faces against a frozen registration. **Whether that registration uses the longest available reference is a question worth asking of the committed fit.**
- He then **aligns the underlay so the main internal walls sit on the zero axes** — a datum-setting move, and the same concern as the datum question §1 records as still ours to decide. [source: [[_Sources/YT_9-hQsyWSnm4_craftelectric_mooncad_walls_and_scale|YT_9-hQsyWSnm4]]]

### ⚠️⚠️ …but a plan image is NOT UNIFORMLY SCALED, so no single registration fits it everywhere (SFE-Viz, 2025)

**Both rules above assume the raster is a uniform similarity transform of reality. A practitioner who works from low-quality plans says it is not, and gives a measurement.**

> *"The plans on images, **they're fit and scaled to fit onto a certain image format, so they're usually a little bit out of proportion**. And when you scale an image to one room, and then you move on to the next one and that is a little out of proportion, you would have to scale again — **now you're ruining the scale on the first room**."*

**He then demonstrates it.** Having scaled the main room's width to its printed **6096 mm**, he checks the perpendicular and finds **7728 mm against a printed 3480 + 4293 = 7773 mm**:

> **→ A 45 mm ANISOTROPIC ERROR IN THE SAME IMAGE, after a correct scale on the other axis.** The sheet is compressed along one axis to fit a format.

**His solution is piecewise rectification by hand**: import the plan as an **editable mesh plane** rather than a background image, loop-cut it at wall faces, turn on the edge-length overlay as a ruler, scale globally to one printed dimension, then **move sub-regions** until the second printed dimension also reads true. **A local affine correction per region, driven by the drawing's own printed dimensions.**

- **⚠️⚠️ Directly checkable against `tools/layout/raster_fidelity.py`, and it should be.** That gate fits **one global** registration from the PDF's hatched wall faces. **If a source sheet carries format-fitting distortion, a globally-fitted registration is right in the middle and wrong at the edges** — and the residual presents as a real geometry breach, or masks one. **→ Confirm the frozen registration's residuals are ISOTROPIC and SPATIALLY UNIFORM, not merely within tolerance on average.** A passing mean can hide a systematic gradient. ⚠️ **Two mitigations already in place**: we register from the PDF's own *vector* hatch geometry, not a scan, and a born-digital vector PDF escapes the resampling half of this. **But "fit to an image format" is a layout operation and applies to vector content too.**
- **⚠️⚠️ And the sharper question, for the owner.** `00_Master/Geometry_Variance_Study.md` measures deltas of **−45 to +30 mm** between the developer plan and three surveyed flats, and those deltas set this project's **±50 mm** nominal tolerance. **45 mm of pure image-format compression is indistinguishable from that.** If any part of that study read the developer plan through a raster, **some fraction of what was attributed to build variance may be sheet distortion.** The tolerance is still safe — it absorbs both — **but the study measures "plan-to-reality disagreement", not "construction variance", and the two must not be used interchangeably.**
- **⚠️ He also states an EVIDENCE CEILING and stops at it**: *"at this point we have reached the maximum level of precision that we can get out of an image like this"* — after which the bathroom is **eyeballed and labelled as such**. He inventories which rooms have printed dimensions and which do not **before relying on any of them**. [source: [[_Sources/YT_p3Q7jNyRAtI_sfeviz_precise_plan_from_bad_image|YT_p3Q7jNyRAtI]]]

### ⚠️ Where the line IS in a blurred raster: the centre of the gradient

> *"Because we have a little bit of pixel blur I'm going to go **in the middle of the shadow** — there's a darker shadow and a lighter shadow — so I'm going to put my loop cut **right on the center of these two shadows**."*

**→ Take the centre of the blur gradient as the edge.** ⚠️ **Relevant to how the frozen ink mask in `raster_fidelity.py` is thresholded: a threshold biased to either side of the gradient shifts every edge in the same direction — a systematic error that a symmetric two-direction measurement will not reveal.** He also uses **corner features as anchors** — *"this little corner always helps"* — because a corner constrains two axes where an edge constrains one. **This extends the ink-has-width note below: the ink has width AND a soft boundary, and they are different error terms.**

### ⚠️⚠️ Two counter-examples: scaling off an assumed door width, and discarding a good reference over an unresolved unit

**A third source in the same batch does the opposite of everything above, twice, and the second is worse than the first.**

With no scale bar, the practitioner scales a whole plan off a normative door width: *"the door width is **generally between 90 and 100 cm**… you need to choose one known factor and scale accordingly."* **→ An 11% spread, stated by him, propagated across the drawing — and a door leaf is one of the SHORTEST elements on a plan**, which is precisely what the longest-reference rule forbids.

**The sibling video is the sharper failure.** The plan he traces **carries printed dimensions**; he notices them, says they would fix the scale, and discards them:

> *"**The plan have the dimensions with it, so you can easily fix the scale — though those numbers are probably with feats. So I will rescale this plan using the door length.**"*

> **→ ⚠️⚠️ A CORRECT REFERENCE WAS AVAILABLE AND WAS ABANDONED OVER AN UNRESOLVED UNIT.** Resolving it is one division — any printed overall against any other printed figure fixes the unit, and a plan with several dimension strings over-determines it. **An ambiguous unit is grounds to resolve it, never grounds to fall back on an assumption.** **The cleanest instance in this vault of the failure standing rule 9 exists to prevent**, and it belongs beside the seven in `00_Master/Evidence_Reading_Discipline.md`. [sources: [[_Sources/YT_Q4rbqUbhYXY_architecturetopics_blender_floor_plan_from_image|YT_Q4rbqUbhYXY]], [[_Sources/YT_mq63GWbgWdM_architecturetopics_inkscape_trace_to_blender|YT_mq63GWbgWdM]] — same channel, one voice]

### ⚠️⚠️ Captured geometry does not carry THICKNESS — now confirmed for 3D scans too

**Three capture methods, three practitioners, same finding**: hand-tracing (a tracer's author assigns 30/20 cm by hand afterwards), auto-tracing (*"the scale is no way near the real thing"*), and now a **phone photogrammetry scan** of a real interior:

> *"**I'm not necessarily sure Polycam is measuring my walls accurately** — but these seem like they're a little closer to four inches thick."*

> **→ ⚠️ Note the inversion, and it is the interesting part: a scan of an existing building is the one thing that COULD report true thickness, and he replaces its measurement with a NORM because the result looked wrong.** For this project that is exactly backwards — `_Survey/` and the existing-services capture exist to measure an existing building, and `validate_services_observed.py` refuses a millimetre figure with no named scale reference. **A scan's thickness reading is evidence; "these seem like four inches" is not.** Recorded as a caution in both directions: do not trust capture blindly, and **do not silently replace it with a norm.** [source: [[_Sources/YT_xlmbZHIaHJw_cgessentials_homebuilder_floor_plan_from_scan|YT_xlmbZHIaHJw]]]

### ⚠️⚠️ A wall's side is relative to its DIRECTION, not to the screen (same source)

**A wall sits left, centred or right of its base line — and left and right are computed relative to the base line's direction, first point to second, not relative to the view:**

> «Если я нарисую такую же стену в обратную сторону, снизу вверх, то при выборе "слева" стена окажется уже с другой стороны… у каждой стены есть направление.»

**His rule: «лучше идти последовательно в одном направлении по периметру» — traverse the perimeter consistently in one direction, and the wall-to-baseline relationship stays predictable.**

- **⚠️ This project needs this convention and does not state it anywhere.** `data/canonical/wall_blocks.csv` and `tools/layout/build_wall_corners.py` deal with exactly this — which side of a centreline the solid occupies, and which wall owns an L-corner. **A direction-dependent side convention is a live hazard the moment a wall is entered or edited by hand.**
- **→ Candidate rule for `.agents/skills/residential-bim-geometry-rules/`: if a wall carries a direction, traverse consistently; if it does not, say so explicitly so nobody assumes one.**

#### ⚠️⚠️ Independently confirmed, in a different tool and a different language — and the consequence is worse than a mis-sided wall

> *"**You do want to make sure that you're drawing in a CLOCKWISE direction.** If you don't, **walls have an inside and an outside direction** — so if you draw in the wrong direction, **it's going to put all your cabinets and stuff, if you add cabinets, it's going to put those in incorrectly**."*

**Two sources, two languages, two unrelated tools, same rule. That settles whether it is a tool quirk: it is not.**

- **And this source supplies the half the Russian one did not**: the error is **not confined to which side of its baseline the wall solid sits.** It propagates into **every object subsequently hosted on that wall** — and it does so silently.
- ⚠️ **The two sources do NOT agree on WHICH direction**, only that consistency is required. **Clockwise is that tool's convention, not a universal.**
- **→ The evidence is now strong enough to settle the standing open item.** The rule should be stated **affirmatively** in `.agents/skills/residential-bim-geometry-rules/` — traverse the perimeter in one consistent direction, and **name which** — rather than merely flagged as a hazard. [source: [[_Sources/YT_xlmbZHIaHJw_cgessentials_homebuilder_floor_plan_from_scan|YT_xlmbZHIaHJw]]]

##### ⚠️⚠️ A THIRD source gives the mechanism — it is the FACE NORMAL — and a way to CHECK it by eye

> *"Whenever we have walls with more than one segment, we need to make sure that **all of the segments are facing the same way**, and that **the red side is facing the direction to where the wall will gain its thickness**."*

**The procedure is a visual gate.** Turn on the **Face Orientation overlay** — **blue = front, red = back** — and walk the model: *"all of the outer walls should be blue, because we want the walls to go inside of the house."* Anything red on the outside is flipped with `shift + N`. He checks every internal wall and flips three.

> **→ ⚠️⚠️ THE DIRECTION IS THE FACE NORMAL, AND IT IS RENDERED AS A COLOUR.** Three sources now, three tools, three regions, one rule. **And this is the only one that supplies a CORRECTNESS CONDITION you can see: blue outside, red toward the thickness** — a whole-model property with a defined pass state, checkable at a glance. **That is the shape of a validator, reached by a practitioner with no validator vocabulary.** ⚠️ He finds one genuinely ambiguous wall and says so.

##### ⚠️⚠️ …and therefore the drawn line is a WALL FACE, not a centreline

> *"In a later step, we're gonna tell Blender **to what direction will the walls gain their thickness**. So ideally, **you want each vertex to be on either side of the walls**… in a real project where all the measurements are correct, **the vertex would have to be aligned to one of the sides of the wall**."*

> **→ Because thickness grows ONE WAY from the drawn line, the line has to BE a face.** Third independent treatment of the centreline question — with [[_Sources/YT_Q4rbqUbhYXY_architecturetopics_blender_floor_plan_from_image|Q4rbqUbhYXY]] (*use surfaces; the line method generates problems*) and this project's own `clear_mm` plus corner-ownership ledger. **All three land in the same place.** ⚠️ **And he then declines to do it** — *"because I know that there's a lot of rounding errors, I'm not gonna do it"* — **an explicit statement that the tutorial's geometry is not dimensionally sound.** [source: [[_Sources/YT_94kAIpRnhcY_dudeblender_floor_plan_series|YT_94kAIpRnhcY]]]

### ⚠️⚠️ Chain closure on a traced plan: internal dimensions are CLEAR, the overall is GROSS, and the difference is the walls

> *"You'll note that if we add these dimensions, **1.8 + 1.8 + 3.1 results in 6.7, which is not exactly 7**… And the reason here is that **there are walls and they have thickness. And we have to account for the thickness of those walls.**"*

**He runs the sum, sees a ~300 mm mismatch, and reaches the right explanation instead of adjusting a number until it closes.**

> **→ Standing rule 9's chain-closure clause executed on a traced plan — and it is the LINEAR counterpart of a distinction this vault already holds for areas** (*developer plans are clear/net, БТИ are gross*). **Recorded as the clean statement of it for lengths, and it is the most common way a traced plan goes wrong.**
>
> ⚠️ **He also flags that his own unit conversion is a source of error**, and attributes a visible gap in the traced outline to it: *"there is a little bit of mismatch here **because we changed the units**."* **Instructive against [[_Sources/YT_p3Q7jNyRAtI_sfeviz_precise_plan_from_bad_image|p3Q7jNyRAtI]], where the same imperial→metric conversion was delegated to an LLM and never checked. A converted dimension is a DERIVED figure and carries the conversion's error.** ⚠️ Where a dimension is simply missing, his fallback is stated: *"ask the client, or you can just eyeball it. **I usually round to the nearest 10th of a meter**."*

#### ⚠️ And an element has an ANCHOR, which is a datum for one object

Adjusting a door's width: *"I'm going to **adjust my anchor type so that it stays that CENTER width**."* **→ Changing a door's width moves one jamb, both jambs, or neither, depending on an anchor nobody thinks about.** Same family as the bottom-left-of-wall origin two unrelated agents silently chose (§1) — **an anchor is a datum for a single element, and it is equally implicit.**

### ⚠️⚠️ Geometry-integrity rules a practitioner states as invariants

**From the same three-part series. These matter because they are stated in advance and are falsifiable — which is rarer in this material than any modelling technique.**

- **⚠️⚠️ Never extrude along an existing edge.** *"I now have **two overlapping edges** here, and that will cause a bunch of problems in the future."* The correct move is to subdivide (`Ctrl+R`) and slide the new vertex. **→ A duplicate edge is invisible and breaks everything downstream — the same class of defect `tools/layout/check_wall_junctions.py` refuses.**
- **⚠️ Merge-by-distance as the doubled-vertex check — SECOND independent instance**, after [[_Sources/YT_Q4rbqUbhYXY_architecturetopics_blender_floor_plan_from_image|Q4rbqUbhYXY]]: *"select all, M → By Distance. And **it will show here if you deleted any vertices**."* **Two unrelated presenters, same habit: this is community-standard practice.** ⚠️⚠️ **And it carries the same flaw both times — it deduplicates and reports in one operation, so a non-zero result SILENTLY FIXES the defect instead of refusing it.** `00_Master/Validator_Design_Discipline.md` names exactly this: *a collection that deduplicates destroys the defect being checked.* ⚠️ The **Auto Merge** mode he also uses is the preventive form, and is worse on the same axis — it merges as you work, with no report at all.
- **⚠️ Object scale must be applied back to 1** (`Ctrl+A → Scale`), because *"it interacts with a bunch of other things like modifiers and textures."* **→ A non-unit object scale silently corrupts downstream operations. A dimensional hazard, not a cosmetic one.**
- **⚠️ An operation whose scope depends on invisible prior state.** `Select Pattern` *adds* to the existing selection, and *"if you don't notice that you did that, it might cause trouble later that you will have no idea why that happened."* His defensive habit: select-all, deselect-all, then pattern. **→ Third instance of this failure class**, with Bonsai's type-versus-instance modal selection and the active-collection default. **Something always carries state you are not looking at.**
- **The origin is deliberately set to a building corner**, *"to keep everything tidy."* **→ ⚠️ A third independent instance of the corner-as-origin convention**, after the two unrelated agents that silently chose bottom-left-of-wall (§1). **The convention is not an AI artefact — it is what people do.**

[source: [[_Sources/YT_94kAIpRnhcY_dudeblender_floor_plan_series|YT_94kAIpRnhcY]]]

### ⚠️ The ink has width, and the width is an error term

Dietzen, tracing a wall off a raster: *"I could draw an edge from about the middle of this black line to about the middle of this black line… that's probably around 5½ inches. The line itself is maybe an eighth or a quarter inch thick. So you need to take all this with a grain of salt."*

**→ Before reading a thickness off a raster, decide which part of the drawn line you are measuring to — centre, inner face or outer face — and carry the line's own thickness as an error bar.** `Evidence_Reading_Discipline.md` requires identifying the two elements a dimension's extension lines terminate on; **this adds that the terminating element itself has thickness.**

### The oracle principle, stated from the GUI side

Dietzen: *"It doesn't matter how good the information you get, there's always a possibility that there's a difference between what's in the model and the actual dimension it's supposed to represent. So I always recommend double-checking against printed dimensions of some sort."*

**That is exactly why `vector_extent_oracle.py` exists** — the repo learned that asserting the DXF against `wall_blocks.csv` only proves two hand-edited files agree. **Corroboration of the hardest-won lesson in the geometry work, from someone who reached it by hand.**

**And a weaker note worth keeping**: a *vector* CAD import normally leaves non-intersecting near-misses — *"a couple spots where for whatever reason it didn't intersect correctly… a little bit of cleanup"* — which in a GUI are found by eye. Our 400 mm near-miss band finds them automatically.
