---
source_type: video transcript (SketchUp channel, 1-minute single-test demonstration)
source_url: https://www.youtube.com/watch?v=sujS9Mgveo4
video_id: sujS9Mgveo4
transcript_file: _Archive/processed_sources/20260913_sketchupgurus_elevation_to_3d_fidelity_check_0e2200b9.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions — ORIGINAL language)
upload_date: 2026-09-06 (confirmed via yt-dlp metadata, upload_date=20260906)
channel: Sketchup Gurus
source_title: "image to 3D kitchen model with accuracy, gemini 3.8 model can create image elevation to perfect 3D"
language: en
extraction_taxonomy: custom (this project's taxonomy, caller-defined mode — bucket `Digital Toolchain / AI Workflow`)
fact_yield: 2
promotional_ratio: low
corroborates_existing: false
region: n/a_no_jurisdictional_claim
delivery_model: n/a — not a renovation source
---

# Source Note — Sketchup Gurus: A 2D Elevation Into a 3D Model, With the Batch's Only Measured Fidelity Check (YouTube sujS9Mgveo4)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## ⚠️ A triage correction worth recording

**This was flagged as a likely skip on the title-skim — a 1-minute clip with a hype-shaped title ("perfect 3D").** It was fetched anyway because the batch was small enough to fetch whole. **It turned out to contain the only *measured* dimensional-fidelity check in the entire eleven-video batch**, and it answers the open question left hanging by the two concept-visualisation sources.

**→ The triage lesson, and it is a real one: a runtime of one minute predicts low *volume*, not low *value*. A single spot-check measured on camera can outrank a 35-minute masterclass that measures nothing.** `fact_yield: 2`, and both facts matter.

## Durable Facts — The Test

- **Input**: a **2D elevation drawing of a kitchen**. **Model**: Gemini 3.8 Flash (`ASR-uncertain`, and a version that will date fast). **Prompt**: *"Create a SketchUp 3D model of this kitchen following this drawing. Can you do it?"*
- **Output**: a **`.dae` (COLLADA) file**, generated in a stated **5–10 minutes**, imported into SketchUp through the normal import dialogue.
- **⚠️ The architecture is worth noting alongside [[_Sources/YT_6trAkQY5_kc_makeform_claude_freecad_mcp|6trAkQY5_kc]]'s closed loop: this is the OPEN-LOOP, file-generating pattern** — a model emits a geometry file with no connection to a running application and no feedback from it. **Same pattern [[_Sources/YT_HOjQiiHJ714_trimble_how_good_is_claude_at_modeling|YT_HOjQiiHJ714]] already records for the SketchUp adapter.**

## ⚠️⚠️ Numeric Data — The Fidelity Measurements

**He measures the generated model against the source drawing on camera with SketchUp's dimension tool. Two checks are legible:**

| Drawing states | Model measures | Delta |
| :--- | :--- | :--- |
| **610** | **616** | **+6 mm** |
| **356** (a drawer) | **356** | **0** |

Height is claimed to match, unquantified. His own verdict is "almost matching" and "almost similar", repeated — **he does not claim exactness despite the title's "perfect 3D".**

- **⚠️ Against this project's own tolerance, 6 mm is comfortably inside the ±50 mm nominal band established by `00_Master/Geometry_Variance_Study.md`.** That sounds reassuring and should not be over-read (below).
- **⚠️⚠️ What this actually tests is TRANSCRIPTION fidelity, not correctness.** The model is measured against the drawing it was handed — so the test says the generator mostly preserved the numbers it was given. **It says nothing about whether a drawing's dimensions are right**, which is the question `Evidence_Reading_Discipline.md` exists for.

## Mistakes / Warnings — Why This Is Not Evidence of Reliability

- **Two dimensions checked, out of a whole kitchen. One of the two was wrong.** A 1-in-2 observed error rate on a sample of two supports no conclusion about the rest of the model.
- **⚠️ No error is explained, and an unexplained 6 mm is the concerning kind.** It is not a rounding artefact and not a unit conversion; it is a number the generator moved for no stated reason. **A systematic scale error and a one-off drift look identical on a sample of two.**
- **The measurement method is itself eyeballed** — he places the dimension tool by hand and says "almost 610 from this point", which is standing rule 9's exact warning: a dimension read without establishing what its endpoints terminate on.
- **⚠️ The title claims "perfect 3D" and "accuracy"; the transcript says "almost" five times.** Recorded as the gap between the claim and the demonstration.

> **→ How to hold this: it is a promising single data point that an elevation-to-geometry generator preserves dimensions to roughly the right order, and it is nowhere near enough to trust one. For this project the route remains unchanged — model from the printed dimension strings, and let `check_dxf_closure.py` and `raster_fidelity.py` decide, rather than accepting generated geometry on a two-point spot check.**

## Confidence & Evidence Notes

- **`single-account`, single test, single operator, no repetition, self-reported.**
- **ASR**: clean but the model version ("Gemini 3.8 flash") is `ASR-uncertain` and dates fast; **the version is not routed, the measurement is.**
- **`corroborates_existing: false`** — this is new ground for the vault; no existing page holds a measured elevation-to-3D fidelity figure.
- **No regulatory content.**

## Recommended Downstream Routing

- `18_Digital_Toolchain/analysis/AI_For_Concept_And_Visualisation.md` (NEW PAGE) — the measurement, and the transcription-versus-correctness distinction.
- `_Inbox/planning/` triage note — the "one minute predicts low volume, not low value" lesson.
- **5b**: no prices; no conversion owed.
