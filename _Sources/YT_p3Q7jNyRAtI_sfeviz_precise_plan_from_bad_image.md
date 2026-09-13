---
source_type: video transcript (Blender archviz channel, long-form precision workflow)
source_url: https://www.youtube.com/watch?v=p3Q7jNyRAtI
video_id: p3Q7jNyRAtI
transcript_file: _Archive/processed_sources/20260913_sfeviz_precise_plan_from_bad_image_bf21c0e8.txt
fetched: 2026-09-13 via youtube-transcript-api (en-orig auto captions - ORIGINAL language, verified from the caption manifest)
upload_date: 2025-02-21 (confirmed via yt-dlp metadata)
channel: SFE-Viz
source_title: "Blender House Modeling Part 1: Precise Floor Plans from Bad Images"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Drawing and Documentation Conventions`, `Digital Toolchain / AI Workflow`)
fact_yield: 14
promotional_ratio: low
corroborates_existing: true
region: north_america (2x4/2x6 framing, imperial source plan) - flagged, not transferred
delivery_model: n/a - not a renovation source
---

# Source Note - SFE-Viz: ⚠️⚠️ THE STRONGEST EVIDENCE-READING SOURCE IN THIS VAULT SINCE THE DISCIPLINE WAS WRITTEN (YouTube p3Q7jNyRAtI)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this one is extracted at 14 facts

**Twenty-nine minutes of one practitioner building a dimensionally-defensible model from a low-quality raster plan, narrating his reasoning at every step.** He does, unprompted and by name-free instinct, **all four clauses of this project's standing rule 9** — identifies what each dimension terminates on, questions what an element plausibly is, keeps his scale independent, and closes chains. **And he states an evidence ceiling and stops at it.**

> **⚠️⚠️ He is also the only source in four batches to CONTRADICT a load-bearing assumption in this project's own tooling.** See §1. `promotional_ratio: low` — one asset plug at the end.

## ⚠️⚠️ 1. THE FINDING: a plan image is NOT uniformly scaled, and a single global registration cannot fit it

This is his stated reason for the whole method, given in the first two minutes:

> *"The plans on images, they're fit and scaled to fit onto a certain image format, so **they're usually a little bit out of proportion**. And when you scale an image in Blender to one room, and then you move on to the next one and that is a little out of proportion, **you would have to scale again — now you're ruining the scale on the first room.**"*

**He then demonstrates it with numbers.** Having scaled the main room's width to its printed **6096 mm**, he checks the perpendicular:

> *"What about the length? We're at **7728** and we need — let's double check this, **3480 + 4293** — we need **7773**. And there you can already see that **the plan is a little squished together to fit on the image format**."*

> **→ A 45 mm ANISOTROPIC ERROR IN THE SAME IMAGE, AFTER A CORRECT SCALE ON THE OTHER AXIS.** The raster is not merely mis-scaled; it is scaled **differently along X than along Y**, and by his account the distortion also varies across the sheet.
>
> **⚠️⚠️ THIS BEARS DIRECTLY ON `tools/layout/raster_fidelity.py`, AND IT SHOULD BE CHECKED.** That gate registers mm→px from the source PDF's hatched wall faces against a **frozen** committed registration, then measures DXF edges against the ink mask densely in both directions. **A single global registration assumes the raster is a uniform similarity transform of reality.** If a source sheet carries the format-fitting distortion described here, **a globally-fitted registration is right in the middle of the sheet and wrong at the edges — and the residual would present as a real geometry breach, or worse, mask one.**
>
> **⚠️ Two mitigations already in place, and they matter**: our registration is fitted from the **PDF's own vector hatch geometry**, not from a scan, and a born-digital vector PDF is not subject to the raster-resampling half of this. **But "fit to an image format" is a LAYOUT operation, and it can be applied to vector content too.** **→ Open item raised: confirm the frozen registration's residuals are isotropic and spatially uniform, not just within tolerance on average.** A mean that passes can hide a systematic gradient, and `Validator_Design_Discipline.md` already records that *printing is not checking*.
>
> **⚠️⚠️ And a second, sharper question.** `00_Master/Geometry_Variance_Study.md` measures deltas of **−45 to +30 mm** between the developer plan and three surveyed flats, and those deltas set the **±50 mm nominal tolerance** this whole project builds to. **The magnitude here — 45 mm of pure image-format compression — is indistinguishable from that.** If any part of that study read the developer plan through a raster, **some fraction of what was attributed to build variance may be sheet distortion.** That does not invalidate the tolerance (a tolerance that absorbs both is still safe), but **it does mean the study measures "plan-to-reality disagreement", not "construction variance", and the two should not be used interchangeably.** Flagged for the owner.

## ⚠️⚠️ 2. His solution: make the reference image an EDITABLE MESH, then rectify it locally

Instead of dropping the image in as a background reference, he adds it as **`Shift A → Image → Mesh Plane`**, and views it in textured solid shading.

> *"That gives me the ability to **edit the image just like any other mesh** with loop cuts and pulling vertices etc. — and that's exactly what I want."*

The working loop, repeated perhaps thirty times across the video:

1. **Loop-cut the image plane** at a wall face, sliding with `GG` (edge-slide) — *"if I press just G and move it, that's when I start moving the texture around, and at this moment I don't want that."*
2. **Turn on the edge-length overlay** so every edge reports its own length in millimetres — this is his ruler.
3. **Scale globally to one printed dimension**, then **move the sub-region** (*"select the whole bottom half and G Y move it down, keeping an eye on that long edge"*) until the second printed dimension also reads true.
4. Build the wall mesh as a **separate object** (`P` to separate, renamed `walls`), snapping vertices to the rectified image.

> **→ This is piecewise rubber-sheeting by hand: a local affine correction per region, driven by the drawing's own printed dimensions.** It is the manual equivalent of a **piecewise / non-rigid registration**, and it is the correct response to §1. **Recorded as the method, and as the argument that a global fit is the wrong shape of solution for a distorted sheet.**

## ⚠️⚠️ 3. Standing rule 9, executed four times, unprompted

**This is the part worth reading the source for.** He never states a rule; he just refuses to use a dimension until he knows what it terminates on.

- **Clause 1 — what do the extension lines terminate on?** Three separate refusals:
  - *"We do not have a measurement for this part here, because **the 3454 in the kitchen are the measurement from this wall to the pantry**."*
  - *"For bedroom number two we do not have a full measurement wall to door, because **the 3937 here are from wall to closet**."*
  - **⚠️⚠️ And the best one, which produces a correction:** *"Because **on the porch there is no wall, the measurement here goes to the outside of the beam**, which will line up with the outside of that wall. So once we extrude up to here, **we got to go back 140 mm to have that wall thickness**."*

> **→ A DIMENSION TERMINATING ON A BEAM FACE RATHER THAN A WALL FACE REQUIRES A ONE-WALL-THICKNESS CORRECTION, AND HE CAUGHT IT.** This is the single cleanest positive instance of clause 1 in the vault, against the seven failures recorded in `00_Master/Evidence_Reading_Discipline.md`. **It belongs there as the worked counter-example.**

- **Clause 4 — chain closure over judgement.** `3480 + 4293 = 7773` checked against a measured 7728 (§1). He does this rather than trusting either figure alone. **Where no direct dimension exists he builds a chain from the far side**: *"we do have a measurement from here to here, then we have the inside of the pantry, and we also have the inside of the office, so we can get all the way down here"* — then walks it, wall thickness by wall thickness: `−3454`, `−89`, `−2845`, `−89`, `−3099`, `−140`.
- **Clause 3 — scale independent of the thing measured.** His scale comes from **printed dimensions**, never from an assumed door width. ⚠️ **Direct contrast with the other two image-tracing sources in this same batch**, which both scaled off an assumed 90–100 cm door ([[_Sources/YT_Q4rbqUbhYXY_architecturetopics_blender_floor_plan_from_image|Q4rbqUbhYXY]] §1, [[_Sources/YT_mq63GWbgWdM_architecturetopics_inkscape_trace_to_blender|mq63GWbgWdM]] §2). **Three sources, one batch, same task, opposite discipline.**
- **Clause 2 — could this plausibly be what it looks like?** See §4.

## ⚠️⚠️ 4. Wall thickness read as EVIDENCE OF WHAT IS INSIDE THE WALL

Twice he treats an anomalous thickness as a question rather than a given:

> *"If we look at something like this here, **it's probably a doubled-up wall because there's a dryer here — there's going to be a vent through the wall.** So that is something I will actually change: I will move the dryer over here so you can vent directly outside the wall, **so that way I can keep this a 2x4 wall.**"*

And again on a pocket door, where he reads a 2x6 as not making sense for that function and reduces it.

> **→ AN UNEXPLAINED WALL THICKNESS IS A CONCEALED SERVICE UNTIL PROVEN OTHERWISE.** ⚠️⚠️ **Directly relevant to `00_Master/Existing_Services_Capture_Protocol.md` and `validate_services_observed.py`**, which already refuses an offset with no datum and a wall that does not exist. **This adds the inverse inference: a wall that is thicker than its structural role requires is positive evidence that something runs inside it** — and in this flat, that is exactly the class of thing the survey is trying to find. **Routed as a reading heuristic.**
>
> ⚠️ Note he *changes the design* to avoid the thick wall. **That freedom does not exist here** — this project surveys an existing building. The inference transfers; the remedy does not.

## ⚠️ 5. He states an evidence ceiling, and stops at it

> *"At this point **we have reached the maximum level of precision that we can get out of an image like this.**"*

Beyond that point he is explicit about what is no longer measured: *"I don't have a measurement here for the bathroom, but because by now everything is mostly scaled into place, **I can just eyeball it**"*; and earlier, *"because we don't have any detail measurements on the laundry room, **we have that creative freedom here**."*

> **→ MEASURED AND EYEBALLED ARE KEPT SEPARATE AND LABELLED.** He takes stock mid-video of exactly which rooms have printed dimensions (main room, master bedroom, walk-in closet, bedroom 2, office, pantry, kitchen) and which do not (**both bathrooms, the laundry**). **An explicit inventory of what the evidence covers, made before relying on it.** This is the same instinct as standing rule 11 — *a role is a claim, so it needs someone to have looked* — applied to dimensions.

## Reading a blurred raster edge

6. **⚠️ Where the line IS, in a compressed image**: *"because we have a little bit of pixel blur I'm going to go in the middle of the shadow — there's a darker shadow and a lighter shadow — so I'm going to put my loop cut **right on the center of these two shadows**."* **→ Take the centre of the blur gradient as the edge.** ⚠️ Relevant to how the **frozen ink mask** in `raster_fidelity.py` is thresholded: a threshold biased to either side of the gradient shifts every edge in the same direction, which is a systematic error a symmetric two-direction measurement will not reveal. **Flagged with §1.**
7. **Corner features as alignment anchors**: *"you can also see that little corner here, that's what I'm going to try to line up my loop cuts with — this little corner always helps a little."* A corner constrains two axes where an edge constrains one.

## Conventions and figures

8. **⚠️ Opening heads are NOT aligned to each other**: **door head 2100 mm, window head 2200 mm, window sill 600 mm** — *"the doors are a little lower than the windows."*
   > **⚠️⚠️ DIRECT PRACTITIONER DISAGREEMENT WITH [[_Sources/YT_Q4rbqUbhYXY_architecturetopics_blender_floor_plan_from_image|Q4rbqUbhYXY]] §5 in this same batch**, which aligns window heads *to* door heads at 2.1 m as a coordination convention. **Neither gives a reason.** → Routed as a genuine **Perspectives** disagreement, not resolved here.
9. **Framing thicknesses**: 2x6 = **139.7 mm, used as 140**; 2x4 = **89 mm**. Wall height **2772 mm**. ⚠️ **North American light-frame construction, from an imperial source plan. Recorded as the source's context only — NOT transferable to this project**, which is block-and-masonry in Minsk. No figure routed.
10. **⚠️ His tolerance rationale, which is sound and does transfer**: on rounding 139.7 to 140 — *"this is not 100% precise, but I mean, **this is a house framing, not a detail machine part**. If you can show me a framer that works to a decimal of a millimeter…"* **→ Precision is set by the trade that builds it, not by the tool that draws it.** The same argument underwrites this project's ±50 mm nominal.
11. **Derived figures computed in-field, not pre-rounded**: for the cathedral ceiling he enters `G Z`, then in Blender's advanced numeric mode types **`4804 − 2772`**, letting the field do the arithmetic. **→ The same instinct as this vault's `arithmetic-exact` tag.** (Pitch stated as 8:12 — 8 in rise per 12 in run.)
12. **Pre-processing the reference**: he upscales the image once for clarity, has an LLM convert every printed dimension imperial→metric, and **writes the resulting specs into the image margin** so they are visible in Blender beside the plan. **→ Cheap and good: the reference carries its own resolved key.** ⚠️ The LLM conversion is **unverified** — no spot-check is shown, and a single mis-converted dimension would propagate silently into the chain closures he relies on.
13. **Per-room floor faces** are separated so *"every room individual materials"* can be assigned. **→ This is the geometric precondition for per-room floor quantities** — the same point [[18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join|Quantity Takeoff and Cost Join]] makes about cost-attachment needing individuated faces.

## ⚠️ 14. The one place his own discipline lapses — and it is instructive

> *"I did notice in between that I must have grabbed the wrong edges somewhere along the way, so the walls were a little out of place, so I moved those back. **The measurements are still intact though, so I didn't mess up anything of the precision.**"*

> **→ THE CLAIM THAT PRECISION SURVIVED IS ASSERTED, NOT CHECKED.** He has an edge-length overlay running that could have verified it in seconds, and does not re-run the chain. **This is exactly the seam a gate belongs on** — and it is the honest reason this project's `check_dxf_closure.py` re-asserts every wall's length and thickness after every export rather than trusting that an edit was local. **A manual workflow's weakest moment is the undo it believes was clean.**

## What was deliberately NOT extracted

- All Blender keystroke sequences and UI locations beyond the four steps in §2 — mouse work.
- The cathedral-ceiling, material and archviz-scene material — **no relevance to a flat with slab ceilings**.
- **No prices. No regulatory content. No figure carried across from the North American framing context.**

## Source Notes

SFE-Viz (YouTube), 2025-02-21, 29 min, **read in full**. **Claims are this presenter's, as opinion.** ⚠️ The source plan is a low-resolution imperial plan downloaded from a floor-plan website — **no provenance**, which he states openly. **No verification of the finished model against any independent measurement is performed**, and the 45 mm anisotropy in §1 is his own measurement reported in passing, not an experiment.
