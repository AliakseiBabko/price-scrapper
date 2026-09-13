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

## 5. ⚠️⚠️ Non-destructive editing — keep the authored artefact as the base

**The most transferable technique in this folder for working with a generator on an image, and it is product-independent:**

1. **Send only the CROP you want changed, never the whole render** — for precision, and to keep everything else out of the generator's reach.
2. **Paste the result back into the authored image as a maskable layer**, aligned.
3. **Mask down to just the change.**

> *"The base render will always remain the same… you avoid making your images go through the many iterations and generations inside an AI model and start losing the details, which is quite common."*
>
> *"If part of the design changes, a client requests something different, you can always re-render from your software, then just replace the base render, and you're pretty much done."*

**→ KEEP THE AUTHORED ARTEFACT AS THE BASE; APPLY GENERATED EDITS AS REPLACEABLE LAYERS ON TOP.** The design can change without losing the edits, and repeated generation never degrades the original. **⚠️ The same single-source principle as "place LINKED, never embedded" in §4 of [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] — one layer further down the pipeline.**

- **⚠️ Protective prompt phrases, in copyable form**: *"Don't change the camera angle," "Maintain image proportions," "Keep architecture intact," "Don't change materials."* **The protect-half of the change-versus-protect rule, third appearance and the most usable.**
- **Intensity words decide the result**: *"subtle"* and *"soft"* for wear, or you get something destroyed; **"breeze" rather than "wind"** for natural movement. **Overlong prompts confuse the model.**
- **⚠️⚠️ Establish the geometry-dependent facts in the 3D tool; delegate only appearance.** Place 3D figures first, then use the generator only to improve realism — *"that way I can guarantee SCALE and POSITIONING, and only adjust realism… I'm just improving and not creating from scratch."* Confirmed from the failure side: when the generator places people instead, *"the scale sometimes is hard to adjust."*
- **⚠️⚠️ The occlusion rule: *"whatever it can't see, it's going to just invent."*** Re-framing to a new viewpoint works for ultra close-ups and **hallucinates at medium shots**. **A generator asked for a view containing information absent from the source will fabricate it.**
- **Video must start from a frame, never a prompt alone**; **start-image plus end-image** constrains a transition and leaves *"less margin for hallucinations."*
- **⚠️ He applies the slop test to his own sponsored output** — empty-lot-to-building and empty-room-to-furnished transitions: *"is this really necessary to the story? What's the purpose of this?"* **An independent, different-domain instance of the mountain-of-slop failure mode.** [source: [[_Sources/YT_gq1LIFNxjeI_upstairs_archviz_ai_workflow|YT_gq1LIFNxjeI]]]

## 6. ⚠️ Generation as option exploration — a third arrival

**Plan generation from a boundary plus a prompt, and the framing that makes it safe:**

> *"This is not meant to be like a final generation where you just click send to AI and get the floor plan. **It's meant to be a starting point to get you over the BLANK CANVAS SYNDROME**… and then you can make tweaks as you go, or **generate multiple options and explore stuff much faster.**"*

- **⚠️ What the practitioner actually corrects is telling: DESIGN judgements, not geometry errors** — removing a walk-in closet the bedroom cannot take, widening an entrance, reconsidering a leftover space. **The generated plan was coherent; what it lacked was judgement about that brief.**
- **Twelve lighting scenarios generated from one render are used the same way** — *"more as a REFERENCE and IDEATION tool, not so much as a final result"* — then recreated properly in the rendering software. **Third arrival in this batch at generation-as-option-exploration.**

### ⚠️ Tracing gives topology, not thickness — and "automatically to scale" is a claim to distrust

**An automated sketch-to-CAD tracer returns editable walls and windows in seconds, and its author is honest about the ceiling: *"this is not something where you just click once and it's fully automating your documentation. **This is simply a tracer which allows you to get a conceptual floor plan from a sketch.**"*** Named failure classes: **landscape read as walls**, door orientation wrong, spurious walls, misplaced windows, and *"the results will very much vary in terms of how clear they are to read."*

- **⚠️⚠️ WALL THICKNESS IS NOT RECOVERED — it is assigned afterwards from convention** (he sets 30 cm exterior, 20 cm interior by hand). **→ The trace recovers TOPOLOGY. Thickness arrives from a human.** Directly consistent with why `wall_blocks.csv` treats thickness as a sourced, decided quantity.
- **⚠️⚠️ And a claim to distrust: that skew correction makes a photographed plan *"completely up to scale."*** **Rectification can recover a plane's SHAPE; it cannot recover absolute SCALE without a known real-world dimension — and none is supplied anywhere in the demonstration.** **This vault has established the point twice** — two-point scale verification, and register-on-the-longest-known-distance. **A traced plan with no established reference is a shape, not a measurement.** [sources: [[_Sources/YT_9pDOD_xx2kA_melosazemi_sketch_to_cad_tracing|9pDOD_xx2kA]], [[_Sources/YT_vHWOV5lJudg_melosazemi_floor_plan_generation_as_option_exploration|vHWOV5lJudg]]]

### ⚠️ A manual baseline, and a batch-wide absence of verification

- **A professional's manual pipeline for a CAD-to-Unreal walkthrough: *"just creating the OUTER STRUCTURE of the building manually took close to 4 hours."*** The automated run produced a playable project in ~30 minutes. **⚠️ But not one dimension is checked anywhere in that source** — the output is judged by being walkable.
- **⚠️⚠️ That is the batch-wide pattern: of ten sources, one measures anything.** **This vault's only measured elevation-to-3D fidelity check remains `sujS9Mgveo4`'s 610 drawn against 616 modelled.** **A visual "near-perfect" is not a measurement, and is recorded as the former throughout.**
- **⚠️ None of this reopens the render-pipeline decision**, which stands as the 2026-09-08 research left it: **outsource a room render rather than build an asset pipeline.** [source: [[_Sources/YT_hLslbz8n-1w_sudheendra_cad_to_unreal_walkthrough|hLslbz8n-1w]]]

## Source Notes

| Source | Contribution | Yield |
| :--- | :--- | :--- |
| [[_Sources/YT_2eONA-6WVVI_merkulov_bti_to_visualisation_pipeline\|YT_2eONA-6WVVI]] | The БТИ-to-visualisation pipeline; LLM-as-prompt-engineer; the room-constrained-concept claim | 7 |
| [[_Sources/YT_la8Ml1fQfOg_urbandecoders_claude_for_architects\|YT_la8Ml1fQfOg]] | The interview-me refinement; change-versus-protect; custom instructions as token economy | 3 (partial) |
| [[_Sources/YT_sujS9Mgveo4_sketchupgurus_elevation_to_3d_fidelity_check\|YT_sujS9Mgveo4]] | **The only measured fidelity check in the batch** | 2 |
| [[_Sources/YT_QLge-kb_L2I_moydom3d_five_ai_services_roundup\|YT_QLge-kb_L2I]] | The render-as-communication-artefact framing | 1 (near-skip) |

**⚠️ Promotional handling**: a training-centre course funnel, a channel-growth tour, and an affiliate-style tool roundup. **No tool name, model version, ranking or free-tier claim from any of them is routed** — per the standing rule that capability verdicts date within months. See [`_Knowledge/store/Advertising_Promotional_Notes.md`](../../_Knowledge/store/Advertising_Promotional_Notes.md).
