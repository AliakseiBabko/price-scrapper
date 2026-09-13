---
source_type: video transcript (archviz education channel, DISCLOSED SPONSORED tutorial)
source_url: https://www.youtube.com/watch?v=gq1LIFNxjeI
video_id: gq1LIFNxjeI
transcript_file: _Archive/processed_sources/20260913_upstairs_archviz_ai_workflow_1683d527.txt
fetched: 2026-09-13 via youtube-transcript-api (en manual subtitles — ORIGINAL language)
upload_date: 2026-06-26 (confirmed via yt-dlp metadata)
channel: Upstairs (Oliver)
source_title: "I Finally Found an AI Workflow That Actually Fits Archviz"
language: en
extraction_taxonomy: custom (this project's taxonomy, caller-defined mode — bucket `Digital Toolchain / AI Workflow`)
fact_yield: 8
promotional_ratio: high
corroborates_existing: true
region: n/a_no_jurisdictional_claim
delivery_model: n/a — not a renovation source
---

# Source Note — Upstairs: PARTIALLY PROCESSED — Non-Destructive AI Editing, Against a Conditional That Still Does Not Apply (YouTube gq1LIFNxjeI)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## ⚠️ The conditional, honoured — and a second source from this channel

**The 2026-09-11 triage set a standing condition for archviz content: *"the 2026-09-08 research already advised outsourcing a room render at $40–90 rather than building an asset pipeline. Read it only if that advice is being revisited."*** **It is not being revisited.** Same handling as [[_Sources/YT_tJSS-IWrJoE_sketchupessentials_ai_render_tool_selection|tJSS-IWrJoE]] — **product and model content discarded, transferable technique kept.**

**⚠️ It is richer than that conditional implies, which is why `fact_yield: 8` rather than the near-skip its predecessor earned.** **Second source from this channel** (after [[_Sources/YT_YkHGQPfZEgM_upstairs_plan_presentation_technique|YkHGQPfZEgM]]).

**⚠️⚠️ `promotional_ratio: high` — it is SPONSORED, and he discloses it plainly and early** (*"yes, this video is sponsored"*), explains the timing, and **still closes by saying the hype is wrong**: *"I've been pessimistic about where things were going with AI, and still am… this tool doesn't replace the thinking. That part is still on you."* **The product name, its model line-up and its feature list are NOT routed** — every one of them dates within months, and he says so himself.

## ⚠️⚠️ The Technique Worth Keeping: non-destructive AI editing

**The core workflow, and it is product-independent:**

1. **Send only the CROP you want changed, never the whole render.** Two stated reasons: precision, and **keeping everything else out of reach of the generator.**
2. **Paste the result back into the authored image as a maskable layer**, aligned to the original.
3. **Mask down to just the change** — the people, the weathering, the vegetation.

**⚠️⚠️ The two payoffs he names are the reason to record it:**

> *"The base render will always remain the same… You will avoid making your images go through the many iterations and generations inside an AI model and start losing the details, which is quite common."*

> *"If part of the design changes, a client requests something different, you can always re-render from your software, then just replace the base render, and you're pretty much done."*

- **→ KEEP THE AUTHORED ARTEFACT AS THE BASE AND APPLY GENERATED EDITS AS REPLACEABLE LAYERS ON TOP.** The design can then change without losing the edits, and repeated generation never degrades the original.
- **⚠️ This is the same single-source principle as his own "place LINKED, never embedded"** rule already recorded from `YkHGQPfZEgM`, **arriving one layer further down the pipeline.** Same channel, so a consistent position rather than corroboration — **but it is the render-stage form of a rule this vault holds at the drawing stage.**

## ⚠️ Prompt Phrases That PROTECT — the third instance of a rule this vault holds

**His recommended key phrases are all negative constraints:** *"Don't change the camera angle," "Maintain image proportions," "Keep architecture intact," "Don't change materials."*

- **→ Telling the model what to PROTECT, not only what to change.** **This vault holds the rule abstractly from Urban Decoders and as a tool-selection criterion from `tJSS-IWrJoE` (edit-consistency); here it appears as concrete, copyable prompt text.** Third appearance, and the most directly usable form.
- **Intensity words matter**: use *"subtle"* and *"soft"* for wear and imperfections, or you get something destroyed rather than weathered. For motion, **use "breeze" rather than "wind"** for natural people-and-vegetation movement.
- **⚠️ Overlong prompts hurt**: *"sometimes if you add too long prompts, it confuses the model."*

## ⚠️⚠️ Establish the Geometry-Dependent Facts in the 3D Tool, Delegate Only Appearance

**His preferred method for adding people: place 3D figures in the scene FIRST, then use the generator only to improve their realism.**

> *"That way, I can guarantee SCALE and POSITIONING, and only adjust realism, texture, characteristics… I treat this as something already existing. I'm just improving and not creating from scratch."*

- **→ Scale and position are decided where they can be controlled; appearance is delegated.** **A clean statement of the division of labour in the visual domain, and consistent with "delegate transport, not judgement" from the estimating side.**
- He confirms it from the failure direction too: when characters are placed by the generator instead, *"the scale sometimes is hard to adjust."*

## ⚠️ Two Limits Stated Plainly

- **⚠️⚠️ The occlusion rule: *"whatever it can't see, it's going to just invent."*** Re-framing a render to a new viewpoint works for ultra close-ups, **hallucinates at medium shots**, and invents whatever the source view did not contain. **→ A generator asked for a view containing information absent from the source will fabricate that information.** Worth holding next to the "lost in the middle" and silently-supplied-values rules — **the same failure, in image space.**
- **Video must start from a frame, never from a prompt alone** — *"we're not generating your video from scratch, from a prompt, pretty much ever."* **Start-image plus end-image constrains a transition** (day to night, a shading system opening) and leaves *"less margin for hallucinations."*

## ⚠️ He Applies the Slop Test to His Own Output

Demonstrating empty-lot-to-building and empty-room-to-furnished transitions, he stops and says: *"this already touches a little bit on the slop area… is this really necessary to the story? What's the purpose of this?"*

- **→ An independent, different-domain instance of the failure mode recorded from Fairley — *"the output will get lost in a mountain of slop"*.** **A practitioner applying the test to work he is being paid to promote.**

## Rules / Heuristics — Generation as Ideation, Again

Building twelve lighting scenarios from one render, his stated use is explicit: *"I use this more as a REFERENCE and IDEATION tool, and not so much as a final result"* — **and he then goes back to the rendering software to recreate the chosen atmosphere properly.** Furniture-variant testing is likewise *"better for just quick testing"*, with less control than 3D.

- **⚠️ Third independent arrival in this batch at generation-as-option-exploration** (with [[_Sources/YT_vHWOV5lJudg_melosazemi_floor_plan_generation_as_option_exploration|vHWOV5lJudg]] and the concept material already on the page). **Reusable node-based workflows are the mechanism: build once, swap the base image, re-run.**

## Confidence & Evidence Notes

- **`single-account`**, sponsored, no measurement of anything. **Every product, model and pricing detail deliberately NOT routed.**
- **⚠️ It does NOT reopen the render-pipeline decision**, which stands as the 2026-09-08 research left it: **outsource a room render rather than build an asset pipeline.** Nothing here costs or compares that.
- **Transcript quality excellent** (manual subtitles).
- **No prices carried; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/AI_For_Concept_And_Visualisation.md`** — non-destructive layered editing, protective prompt phrases, scale-in-3D-appearance-in-AI, the occlusion rule, start/end-frame video control, and the self-applied slop test.
- **5b**: no prices; no conversion owed.
