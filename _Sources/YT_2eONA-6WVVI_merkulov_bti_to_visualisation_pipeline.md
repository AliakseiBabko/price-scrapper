---
source_type: video transcript (training-centre masterclass, workflow walkthrough with a heavy course funnel)
source_url: https://www.youtube.com/watch?v=2eONA-6WVVI
video_id: 2eONA-6WVVI
transcript_file: _Archive/processed_sources/20260913_merkulov_bti_to_visualisation_pipeline_f93e0965.txt
fetched: 2026-09-13 via youtube-transcript-api (ru auto captions - ORIGINAL language)
upload_date: 2026-03-25 (confirmed via yt-dlp metadata, upload_date=20260325)
channel: Алексей Меркулов - head of the AMC training centre (учебный центр АМС)
source_title: "Мастер-класс: AI для дизайна интерьера"
language: ru
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - buckets `Digital Toolchain / AI Workflow`, `Design Concept`)
fact_yield: 7
promotional_ratio: high
corroborates_existing: true
region: unresolved_level2_channel_only
delivery_model: n/a - a training provider, not a renovation contractor
---

# Source Note - Меркулов / АМС: A БТИ Plan and a Brief Into Concept and Visualisation, Without 3ds Max (YouTube 2eONA-6WVVI)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Source Metadata / Promotional Context

`promotional_ratio: high`. **A masterclass run by the head of a training centre, and structured as a webinar funnel** - the portfolio is framed as "вход в воронку ваших продаж" (the entry to your sales funnel), the promise is that "what you used to do in a week you can now do in a day", and the closing pitch is the course. **The capability claims are the product.**

**But the pipeline itself is described concretely enough to evaluate, and its INPUT is exactly this project own starting material - a БТИ plan plus a brief.** That is why it was processed rather than filtered out.

## Rules / Heuristics - The Stated Pipeline

**Input: a brief plus a БТИ plan of a real object. Output claimed: a full planning concept and a final visualisation with real furniture and finishes, with no 3ds Max and no heavy visualisation software - "ноутбук и интернет".**

1. **Brief plus БТИ plan into an LLM.** He names ChatGPT, Claude, Grok, Gemini and DeepSeek as interchangeable for this - "все топовые модели одинаково хорошо справляются с этими задачами."
2. **Give the model a role** (architect, interior designer), **then the task** (study the brief and the drawings, consider layout and space-organisation options), **then specify the output format explicitly** - e.g. "give me three prompts for Midjourney v7, image format 3:4".
3. **⚠️⚠️ The organising idea, and the most transferable one: the designer does not become a prompt engineer - the LLM IS the prompt engineer.** "Дизайнеру сейчас не нужно становиться промт-инженером. Эту задачу мы делегируем чату GPT." The LLM assembles a prompt the image model will understand, carrying style, materials, mood and constraints.
4. **A good generated prompt has many parameters baked in, and he enumerates them**: room area, ceiling height, layout type, style, materials, furniture, lighting, atmosphere, **plus the image model own technical parameters.** "Это уже не абстрактный запрос: сделай мне красивую кухню."
5. Image model (Nano Banana / Google Gemini image, `ASR-uncertain`) for **layout variants against the БТИ plan**.
6. A **schematic 3D project**, from which the needed viewpoints, dimensions and views are taken.
7. **Neural rendering in two passes - a base render, then a refined final.**

- **⚠️ The claim that distinguishes this from mood-boarding, and the one worth testing: the concept search is CONSTRAINED BY THE REAL ROOM from the start.** "Отличие нашей концепции от Pinterest в том, что уже на этапе поиска идеи мы учитываем габариты помещения, стили интерьера, виды мебели и общую логику пространства." Worked controls he names: whether the kitchen has an island, whether windows are floor-to-ceiling. **Pinterest gives you someone else beautiful room; this is meant to give you yours.**
- **⚠️ Stated failure mode, and it is the reason the pipeline is built this way: people are disappointed by image models because they cannot formulate what they want.** The prompt is named as the main instrument, and delegating its construction is the fix.

## Confidence & Evidence Notes

- **⚠️⚠️ Nothing here is verified, and the strongest claims are unverifiable by construction.** "A week becomes a day" is a sales claim from a training provider. **No output is checked against the БТИ plan for dimensional fidelity anywhere in the masterclass** - which is precisely the check this project cares about most. **Recorded as a described workflow, not as a validated one.**
- **⚠️ The dimensional-fidelity question is the open one this source does not answer**: whether an image model that has been *told* the room is 3.2 m wide produces an image *of* a 3.2 m room. Everything this vault already holds - the tiling mechanism, the 86% raster accuracy, "a scaled raster is orientation, not measurement" - says to assume it does not until measured. **Use it for concept and communication; do not read a dimension off the output.**
- **ASR quality: poor on product names**, as expected for this subject. Observed: "Джорne"/"жорни"/"мир" for Midjourney, "нанобана" for Nano Banana, "чат Шпити"/"чат GBT" for ChatGPT, "Грог" for Grok, "ДПСК" for DeepSeek, "Neocосика" for неоклассика, "3 кд" for the 3:4 aspect ratio, "Moury"/"Journey" for Midjourney. **Every tool name is a candidate.**
- **`corroborates_existing: true`** - the LLM-as-prompt-engineer pattern is independently described by Urban Decoders in this same batch ([[_Sources/YT_la8Ml1fQfOg_urbandecoders_claude_for_architects|la8Ml1fQfOg]]), on a different continent and for a different audience. **Two unrelated channels, same technique - that is real corroboration.**
- **No regulatory content.**

## Recommended Downstream Routing

- `18_Digital_Toolchain/analysis/AI_For_Concept_And_Visualisation.md` (NEW PAGE) - the pipeline, the LLM-as-prompt-engineer pattern, the room-constrained-concept claim, and the unanswered dimensional-fidelity question.
- **5b**: no prices stated; no conversion owed.
