# Digital Toolchain — Guide

**General, source-derived knowledge about producing and checking construction data digitally**: getting a drawing into geometry, 2D documentation conventions, 3D modelling and visualisation, cost and quantity take-off, and working with AI agents over any of it.

> [!IMPORTANT]
> **This folder is general practitioner and vendor practice. It is NOT this project's own toolchain.**
>
> Same relationship [[17_Design_and_Ergonomics/Design_and_Ergonomics_Guide|17_Design_and_Ergonomics]] has to `00_Master/Design_Concept.md`: general practice lives in the numbered folder, **this apartment's own decisions and status live in `00_Master/`** — `project_decisions.md`, `Model_and_Views.md`, `Planning_Project_Deliverable_Set.md`, `Sheet_Production_Roadmap.md`, `Revit_AutoCAD_Integration_Strategy.md`, `How_To_View_Outputs.md`, and the `V0_*` pages. **A convention recorded here is somebody else's; a convention we have adopted belongs in `00_Master/project_decisions.md` and in `.agents/skills/residential-bim-geometry-rules/`.**
>
> **Created 2026-09-13.** Rationale, and why the 2026-09-08 decision to keep this in `00_Master/` was revisited: [[18_Digital_Toolchain/analysis/Change_Log|Change Log]].

> [!WARNING]
> **Read everything here for CONVENTIONS AND MECHANISMS, never as a tool recommendation.** [`toolchain_gap_analysis_20260908.md`](../_Inbox/planning/toolchain_gap_analysis_20260908.md) concluded *"no new software; three small scripts over data we already hold"*, and nothing processed since has overturned it. **A screencast that is 70% mouse clicks is still worth reading if the other 30% is a convention we have not settled.**
>
> **⚠️ And model-capability verdicts date within months.** The 2026-09-11 round discarded every one of them on purpose. What survives a model generation is the *mechanism* — how a drawing is turned into queryable data, what an agent silently assumes, how a scale reference is established. Record those; let the scores rot.

## What each page holds

### Drawing and documentation conventions

How practitioners dimension, name and compose their own documentation — collected to settle conventions this project has open.

→ **[[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]]** — dimensioning to centre and the `1/2` proportional notation, **the datum an agent silently chooses for you**, element taxonomy (`вывод провода` is not a socket), sheet-level conventions including **the ~1 m plan cut plane and why a fixture's plan symbol is authored rather than cut**, the two-tool split, colour at concept stage, and agents that generate building geometry.

→ **[[18_Digital_Toolchain/analysis/Raster_To_Geometry|Raster to Geometry]]** — **the scale procedure**: register on the LONGEST printed dimension, verify on a SECOND and independent one, and the worked counter-examples of doing neither; **⚠️⚠️ a plan image is not uniformly scaled** — 45 mm of anisotropic format-fitting distortion measured in one sheet, which bears directly on `raster_fidelity.py` and on the variance study; where the line is in blurred ink; and **captured geometry never carries thickness**, now confirmed for tracing, auto-tracing and 3D scans alike. ⚠️⚠️ **Also the geometry-integrity rules**: wall direction is the **face normal**, with a visual gate — blue outside, red toward the thickness; the drawn line is a **wall face, not a centreline**; and **chain closure on a traced plan** — internal dimensions are clear, the overall is gross, and the difference is the walls.

### How a model becomes a sheet

→ **[[18_Digital_Toolchain/analysis/Model_To_Drawing_Pipeline|Model to Drawing Pipeline]]** — **⚠️⚠️ the dividing line: a drawing GENERATED from the model versus one EXPORTED from it**, and why only the first survives an edit; **four places Bonsai's parametric association leaks** and what that means for a headless build; the silent-failure modes of a generated drawing; **the IFC is the master while the `.blend` is a cache**, with the `Ctrl+S` hazard that creates for our own viewing instructions.

> **⚠️⚠️ Extended 2026-09-13 with the `@IfcArchitect` round, which answered four open questions and corrected two conclusions.** **There is no auto-dimension** — placement is manual in every tool read so far, which **corrects the premise behind the gap analysis's `Adopt` verdict**; but **tags are bulk-placed and data-bound** via `{{ }}` templates over model attributes, which is where the value actually sits. **The output is SVG styled by CSS** — our own format, so the "two engines" framing was wrong. **Sheet assembly is manual drag-and-drop in Inkscape**, so adopting it would mean losing a capability we have. **Sheet content is a declarative query**, which is how a demolition plan is generated from one model. **A detail must be MODELLED, not drafted** — a scoping decision for the owner. And **the type library does NOT quantise wall thickness**, correcting an earlier inference.

### Getting AI to read a drawing

Why a PDF drawing set is a bad input to a language model, what measurably fixes it, and where accuracy breaks.

→ **[[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]]** — **the tiling mechanism** (a drawing ≈ 4,000 tokens, and the meaning lives in features smaller than a tile); two vendors' own published limits, both naming **counting**; **a measured benchmark** — 86% / 98% / 100% accuracy at 104,000 / 66,000 / 1,400 tokens; **index by the physical object, not by the sheet**; per-measurement confidence tiers; **counting from vector data is reliable and scaling a raster is not**; and the order-of-magnitude cross-check that independently restates standing rule 9.

### Working with agents as a system

Not how to get an agent to do one task — how to arrange context, skills and multiple agents so the results are reliable enough to rely on.

→ **[[18_Digital_Toolchain/analysis/AI_Workflow_Systems|AI Workflow Systems]]** — **four failure modes of a standalone workflow** (including "the output gets lost in a mountain of slop" and "undocumented process cannot be improved"); **why agentic harnesses break on documents — git works because the unit is a LINE, knowledge work's unit is the whole FILE**; the context ladder and the router-file pattern; and four genuinely new items — **"lost in the middle"**, completeness-checking-needs-a-baseline, the **skeptic step**, and the sub-agent fresh-context mechanism. ⚠️ **One practitioner throughout; mostly validation of an architecture this repo already has.**

### Quantity take-off, and the cost join

How a quantity gets out of a model and becomes a priced line — **the one genuinely absent tool in this project's own toolchain.**

→ **[[18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join|Quantity Take-Off and the Cost Join]]** — **where a cost attaches** (tag, material, object) and what each choice re-prices; the cost line's fields, with **waste and tax as first-class**; **waste is not one number** — nest linear stock and the percentage collapses, tile needs one; the **cable/containment cardinality split** that `ELE-01` needs; and the three independent arrivals at **a cost model earning its keep by killing a bad option early, not by being precise**. ⚠️⚠️ **§8 is the first source in this vault that actually PRICES** — three quantity routes into one BOQ line (elements, a two-point-calibrated PDF take-off, and a pivot table), a line carrying region and currency **but no price DATE**, and the unmeasured step that matters: **an LLM “three-level semantic search” matching elements to catalogue positions, with no error rate**.

### Requirements, and checking the model against them

How a requirement on a model gets written down, and how it gets checked — **including a source that directly challenges this project's `.ids` commitment.**

→ **[[18_Digital_Toolchain/analysis/Requirements_And_Validation|Requirements and Model Validation]]** — **every requirement reduces to ENTITY, ATTRIBUTE, CONSTRAINT**, asserted over 20 rules written in eight formats; **the experiment** — the same model validated against JSON and against Solibri returns identical numbers — **and the caveat that halves it**, since one agent wrote both parsers; the open item on writing our rules as **a three-column CSV first and emitting `.ids` later**; and **a check's output is the list of things that failed, not a percentage**.

### Concept and visualisation

Generating layout concepts and interior imagery, and what the output may safely be used for.

→ **[[18_Digital_Toolchain/analysis/AI_For_Concept_And_Visualisation|AI for Concept and Visualisation]]** — the БТИ-plan-to-visualisation pipeline; **the LLM as your prompt engineer** (corroborated across two unrelated channels) and the interview-me refinement; **the batch's only measured fidelity check** — 610 drawn against 616 modelled; and the distinction that governs all of it: a render is for **agreeing what is wanted**, never for **deriving a number**.

### Agents wired into CAD

→ **[[18_Digital_Toolchain/analysis/Agent_Connected_CAD|Agent-Connected CAD]]** — open-loop file generation versus **closed-loop MCP control** (and why the closed loop's feedback channel is a screenshot, the unreliable one); the **visual-versus-text feedback token trade-off**, and why deterministic gates escape it entirely; and the clean split in what it can do: **transcription succeeds, spatial logic fails** — a modelling accelerator, not a space planner.

## Standing cautions for this source class

These were learned the hard way across the 2026-09-08 and 2026-09-11 rounds, and they apply to every source processed into this folder.

- **⚠️⚠️ A screencast's knowledge is largely ON THE SCREEN, and transcript-only intake is not adequate.** `tools/youtube/extract_layout_frames.py` pairs transcript segments to scene-detected frames and was built for exactly this. Run it on any source whose value is a sheet layout, a dimensioning convention or a cost table — and apply **standing rule 9** (reading a dimension is a procedure, not a glance) to every figure read off a frame.
- **⚠️ Software-subject ASR is measurably worse than this vault's usual sources.** Observed corruption across rounds: «Rimliner» for Remplanner, «Cowerk» for Claude Code, «отвёртки стен» for развёртки. **Program names, product names and numbers heard once are candidates, not figures.**
- **⚠️ The yield metric understates this source class.** A room-and-trade source adds a paragraph to a page; a source here often changes a field, a datum, a sheet or a rule. **Record how many open capability items moved alongside the fact count** — the fact count alone will always rate it too low.
- **⚠️ Nothing here is a norm, and nothing here is Belarusian.** Sources are Russian, US and UK practitioners plus software vendors. **Standing rule 4: no regulatory claim from any of them goes to `16_Legal_and_Regulations/`.**
- **⚠️ Vendors and channels here are selling something** — a subscription, a course, a consulting practice, or their own credibility as an early adopter. Apply the advertising filter exactly as for a renovation company: **extract the mechanism, drop the verdict.**

## Related

- `00_Master/project_decisions.md` — what this project has actually decided.
- `00_Master/Evidence_Reading_Discipline.md` — standing rule 9, and the seven real misreadings behind it.
- `00_Master/Validator_Design_Discipline.md` — how to write a check that can fail.
- [[11_Budget_and_Planning/Budgeting_Guide|Budgeting Guide]] — the renovation's own costs, as distinct from how a cost is *calculated*.

## Source Notes

Traceability record kept on its own page — [[18_Digital_Toolchain/analysis/Source_Notes|Source Notes]].

## Change Log

Editorial history kept on its own page — [[18_Digital_Toolchain/analysis/Change_Log|Change Log]].
