# AI for Concept and Visualisation

Detail page for [[18_Digital_Toolchain/Digital_Toolchain_Guide|Digital Toolchain]].

**Generating layout concepts and interior imagery with AI — the prompting technique that makes it work, what the output is safe to be used for, and the one place its dimensional fidelity has actually been measured.**

> [!WARNING]
> **⚠️⚠️ The load-bearing distinction on this page: a generated image is a CONCEPT and COMMUNICATION artefact, not a measurement.** Every source here is selling a course, a tool list or a channel, and none of them checks an output against its input except the one that is measured in §3 — where two dimensions were checked and **one was wrong by 6 mm.** Use these outputs to agree what is wanted; never to derive a number. [[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]] carries the measured reasons why.

## 1. The pipeline — a БТИ plan and a brief, to a visualisation

The fullest description comes from a Russian training-centre masterclass. **It is a course funnel and its headline claim ("what took a week now takes a day") is unverifiable — but its INPUT is exactly this project's own starting material, which is why it is worth recording.** [source: [[_Sources/YT_2eONA-6WVVI_merkulov_bti_to_visualisation_pipeline|YT_2eONA-6WVVI]]]

1. **Brief + БТИ plan into an LLM.** ChatGPT, Claude, Grok, Gemini and DeepSeek are named as interchangeable here — *"все топовые модели одинаково хорошо справляются с этими задачами."*
2. **Give the model a role** (architect, interior designer), **then the task** (study the brief and drawings, consider layout and space-organisation options), **then state the output format explicitly** — e.g. "three prompts for Midjourney v7, aspect 3:4".
3. **An image model produces layout variants against the БТИ plan.**
4. **A schematic 3D project**, from which viewpoints, dimensions and views are taken.
5. **Neural rendering in two passes — a base render, then a refined final.**

**⚠️ The claim that separates this from mood-boarding, and the one worth testing rather than believing: the concept search is constrained by the real room from the start.** *"Отличие нашей концепции от Pinterest в том, что уже на этапе поиска идеи мы учитываем габариты помещения, стили интерьера, виды мебели и общую логику пространства."* Named controls: whether the kitchen has an island, whether the windows are floor-to-ceiling. **Pinterest gives you someone else's beautiful room; this is meant to give you yours.**

## 2. ⚠️⚠️ The technique that actually carries: the LLM is the prompt engineer

**Corroborated across two unrelated channels, on different continents, for different audiences — which is rare in this batch and is why this is the most trustworthy item on the page.**

- **The core move: you do not become a prompt engineer; you delegate prompt-writing to the language model.** *"Дизайнеру сейчас не нужно становиться промт-инженером. Эту задачу мы делегируем чату GPT."* The LLM assembles a prompt the image model will understand, carrying style, materials, mood and constraints. [source: [[_Sources/YT_2eONA-6WVVI_merkulov_bti_to_visualisation_pipeline|YT_2eONA-6WVVI]]]
- **The stated failure it fixes: people are disappointed by image models because they cannot articulate what they want.** The prompt is the instrument; most people write "one long messy sentence and hope for the best."
- **⚠️ The refinement, from the second channel — have the model INTERVIEW you.** Give it the role of prompt engineer for the specific generator, then ask it to question you with a list before it writes anything. A rough idea goes in, a set of elaboration questions comes back (with defaults offered, e.g. aspect ratio), and the answers produce a fully specified prompt. *"Instead of me guessing the format, I can get Claude to interview me."* [source: [[_Sources/YT_la8Ml1fQfOg_urbandecoders_claude_for_architects|YT_la8Ml1fQfOg]]]
- **What a well-built prompt carries, enumerated**: room area, ceiling height, layout type, style, materials, furniture, lighting, atmosphere, **plus the image model's own technical parameters.** *"Это уже не абстрактный запрос: сделай мне красивую кухню."*
- **⚠️ One general prompting rule from the same source, and the non-obvious half is the second one: tell the model what to CHANGE and what to PROTECT**, then iterate conversationally. Most prompt advice covers only the first.
- **Custom instructions are a token-economy measure, not just a convenience** — setting role, tone, audience and format once means not re-explaining context on every turn.

## 3. ⚠️⚠️ The only measured fidelity check in the batch

**Everything above describes a workflow and measures nothing. One source measures.** [source: [[_Sources/YT_sujS9Mgveo4_sketchupgurus_elevation_to_3d_fidelity_check|YT_sujS9Mgveo4]]]

**A 2D kitchen elevation was handed to an image-capable model with the prompt "create a SketchUp 3D model of this kitchen following this drawing". It returned a `.dae` (COLLADA) file in 5–10 minutes.** Measured against the source drawing with SketchUp's dimension tool:

| Drawing states | Model measures | Delta |
| :--- | :--- | :--- |
| **610** | **616** | **+6 mm** |
| **356** (a drawer) | **356** | **0** |

- **Against this project's own ±50 mm nominal band (`00_Master/Geometry_Variance_Study.md`), 6 mm is comfortably inside tolerance.** That is the reassuring reading and it should not be over-read.
- **⚠️⚠️ What this tests is TRANSCRIPTION fidelity, not correctness.** The model is measured against the drawing it was handed, so the result says the generator mostly preserved numbers it was given. **It says nothing about whether those numbers were right** — which is the question `00_Master/Evidence_Reading_Discipline.md` exists for.
- **⚠️ Two dimensions were checked and one was wrong, with no explanation.** An unexplained 6 mm is the concerning kind — not a rounding artefact, not a unit conversion. **On a sample of two, a systematic scale error and a one-off drift are indistinguishable.** The measurement method was itself eyeballed.
- **The title claims "perfect 3D"; the transcript says "almost" five times.**

> **→ How to hold it: a promising single data point that an elevation-to-geometry generator preserves dimensions to roughly the right order — and nowhere near enough to trust one. This project's route is unchanged: model from the printed dimension strings, and let `check_dxf_closure.py` and `raster_fidelity.py` decide.**

## 4. What the output is actually for

**⚠️ The most useful framing on this page comes from the thinnest source in the batch, and it sidesteps the accuracy problem entirely.** AI-generated interior imagery is described as *"отличная база для разговора со строителями, чтобы не тратить недели на объяснения на пальцах"* — **a basis for the conversation with builders, so weeks are not spent explaining by hand-waving.** [source: [[_Sources/YT_QLge-kb_L2I_moydom3d_five_ai_services_roundup|YT_QLge-kb_L2I]]]

> **Two different uses of the same picture, and only one is safe.** A render used to **agree what is wanted** with a contractor needs no dimensional fidelity at all. A render used to **derive a dimension** needs exactly what §3 shows it does not reliably have.

**⚠️ This matters more than usual for this project, which is self-managed** — every trade is briefed separately, so the cost of a specialist misunderstanding the intent is borne directly. A concept image is cheap alignment; it is not a drawing, and it must not be handed over as one. The deliverable that *is* a drawing is defined in `00_Master/Planning_Project_Deliverable_Set.md`.

## Source Notes

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [[_Sources/YT_2eONA-6WVVI_merkulov_bti_to_visualisation_pipeline\|YT_2eONA-6WVVI]] | The БТИ-to-visualisation pipeline; LLM-as-prompt-engineer; the room-constrained-concept claim | 7 |
| [[_Sources/YT_la8Ml1fQfOg_urbandecoders_claude_for_architects\|YT_la8Ml1fQfOg]] | The interview-me refinement; change-versus-protect; custom instructions as token economy | 3 (partial) |
| [[_Sources/YT_sujS9Mgveo4_sketchupgurus_elevation_to_3d_fidelity_check\|YT_sujS9Mgveo4]] | **The only measured fidelity check in the batch** | 2 |
| [[_Sources/YT_QLge-kb_L2I_moydom3d_five_ai_services_roundup\|YT_QLge-kb_L2I]] | The render-as-communication-artefact framing | 1 (near-skip) |

**⚠️ Promotional handling**: a training-centre course funnel, a channel-growth tour, and an affiliate-style tool roundup. **No tool name, model version, ranking or free-tier claim from any of them is routed** — per the standing rule that capability verdicts date within months. See [`_Knowledge/store/Advertising_Promotional_Notes.md`](../../_Knowledge/store/Advertising_Promotional_Notes.md).
