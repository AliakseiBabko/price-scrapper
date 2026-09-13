---
source_type: video transcript (amateur CAD tutorial channel)
source_url: https://www.youtube.com/watch?v=EibFZPrtAp0
video_id: EibFZPrtAp0
transcript_file: _Archive/processed_sources/20260913_civilengineering_chatgpt_dimensions_antipattern_03ebaf5c.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions - ORIGINAL language)
upload_date: 2026-03-31 (confirmed via yt-dlp metadata, upload_date=20260331)
channel: Civil engineering
source_title: "Stop Typing Dimensions! Use This ChatGPT + AutoCAD Trick"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 2
promotional_ratio: low
corroborates_existing: false
region: n/a_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Civil engineering: A DOCUMENTED ANTI-PATTERN, Recorded as What Not To Do (YouTube EibFZPrtAp0)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## ⚠️⚠️ Why this is recorded at all

**This source is routed as a NEGATIVE example, not as technique.** It is a short amateur tutorial - the presenter says twice that he is himself still learning AutoCAD - and its headline "trick" is **precisely the failure mode that every other source in this batch measures, warns against, or designs around.** It is kept because a concrete instance of the wrong thing, performed confidently on camera, is a stronger teaching artefact than another restatement of the rule. **Same treatment this vault already gives a self-flagged live-wiring demonstration: recorded as a documented bad practice, never as a recommendation.**

## ⚠️⚠️ Mistakes / Warnings - The Anti-Pattern

**What he does**: uploads an image of a floor plan to ChatGPT with the prompt **"give me all the dimensions and their respective names as copy-paste format for AutoCAD"**, then **pastes the returned numbers straight into the drawing as text.** His stated motive is that typing them out by hand "takes very time."

**What is wrong with it, and this vault can now be specific rather than general:**

- **It is vision-reading dimensions off a raster image, which is the single least reliable operation in this whole subject.** [[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]] measures raw-image pipelines at **86% accuracy**; both Anthropic and OpenAI publish warnings naming small text, spatial relationships and exact counting; and the clock benchmark puts precise diagram reading near a coin-flip.
- **⚠️⚠️ There is NO verification step of any kind.** He never checks a single returned dimension against the drawing. The numbers go from an image, through a model, into the drawing, and become the drawing.
- **⚠️ It violates this project standing rule 9 completely** - a dimension is read without identifying the two elements its extension lines terminate on, without any independent scale, and without chain closure. **And it is worse than a careless human reading, because the output arrives pre-formatted and confident.**
- **Compare the disciplined version of the same goal**: extract the **vector text layer** and count or read from that (stated as 100% accurate for counting), never from the pixels. **The goal is fine; the method is the one thing that cannot be done this way.**

## Durable Facts - The One Benign Item

- **Raster underlay for tracing**: `insert -> raster image`, place the plan, and draw over it. **Legitimate as ORIENTATION**, and already recorded in this vault as such.
- **⚠️ But note how he handles scale, because it is the same carelessness**: he rescales the underlay by eye to taste ("we can make this image more big or small... all according to how we like it") and, when the pasted text lands at the wrong size, says **"I have not put a proper scale over here... do not worry that I have done something wrong."** **A raster underlay with no established scale is exactly the "orientation, not measurement" case - and he is measuring from it.**

## Confidence & Evidence Notes

- **`single-account`.** Amateur source, explicitly self-described as still learning; **no claim here is treated as authoritative.**
- **ASR**: good; the video content is simply thin.
- **⚠️ `corroborates_existing: false` deliberately - it contradicts existing vault findings rather than supporting them, and is filed on that basis.**
- **No regulatory content.**

## Recommended Downstream Routing

- `18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings.md` - as a named anti-pattern in the accuracy section.
- **5b**: no prices; no conversion owed.
