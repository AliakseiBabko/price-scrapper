# Deep Research brief — the 2D/3D/budgeting toolchain, and whether an agent can replace the stack

**Created 2026-09-08** at the owner's request. **This file is the brief, not the research.** Nothing here has been researched yet — Part 1 is a paste-ready prompt for Gemini Deep Research, Part 2 says how to judge what comes back.

**The question behind the request, stated plainly:** the owner has concluded he can reproduce the functional parts he needs with agents instead of adopting SketchUp / ArchiCAD / Revit / Planner 5D, and wants to check that against established practice before committing — *not* to be sold a tool, and *not* to reinvent what the industry already settled. **So the research must test that thesis, including where it fails.**

---

## ⭐ THE PROMPT — paste this (~370 words, fits a chat box)

> I'm the owner-manager of one apartment renovation in **Minsk, Belarus**. I want to produce and maintain the whole document set myself — 2D plans, a 3D model, quantities, budgets, visualisations — using **Python + Blender + AI agents instead of buying Revit / ArchiCAD / SketchUp / Planner 5D**. Research what professional practice has already settled here, and **test whether my approach is realistic rather than assuming it.**
>
> **Already built — don't propose it:** apartment geometry as canonical JSON/CSV; an IFC model built with IfcOpenShell (walls, spaces, openings, MEP points); layout variants as patch files, built and diffed by one command; geometry validators that gate (wall junctions, corner ownership, room-rollout closure, a QTO gate); four A3 sheets generating from the IFC via SVG→PDF; DXF export with existing/demolished/new layers; Blender + Bonsai plus a headless EEVEE render script; a price database with historical-FX normalisation.
>
> **What I need researched:**
>
> 1. **Quantity take-off from an IFC model, done properly** — what is measured off the model versus off a product datasheet, and whether professionals use waste percentages or nested cutting plans.
> 2. **Quantities → budget, and specifically the automatic cost DELTA between two layout variants** (5D BIM). Include the **Belarusian** estimating basis (НРР) — **do not substitute Russian norms.**
> 3. **Construction-grade 2D from code**: realistic limits of IfcOpenShell / ezdxf / FreeCAD BIM / Bonsai for dimension strings, tags, schedules and title blocks — and what "worker-ready" requires that a coordination drawing lacks.
> 4. **Rendering**: what the step from an EEVEE demonstrator to a presentable image actually costs, and honestly whether AI image tools (ControlNet depth over a clay render) keep enough **geometric fidelity** to be more than mood.
> 5. **Colour and finish selection** — what is systematisable, where a human eye stays required, and what a painter or tiler needs per surface.
> 6. **The 2024–2026 agent layer**: MCP servers for CAD/BIM, agent-driven estimating, raster-plan→vector accuracy, and the review practices that keep agent output trustworthy (IDS, BCF, model checking).
> 7. **Where my approach fails and a paid seat wins** — name the tasks, and what buying *just* that capability costs, including one-off outsourcing.
> 8. Sheet by sheet, what does an established **«планировочный проект»** album contain, and which drawing standards govern it (ГОСТ 21.501 / СПДС versus Belarusian СТБ / ТКП)?
>
> **Output:** a verdict per capability (*replaceable by agents now / with effort / not yet*); a gap table with method + open-source path + failure mode; a build order; a standards list separating mandatory from customary and Belarus from Russia; named tools with maturity and licence; and a **"don't build this — buy or outsource"** list.
>
> **Cite sources. Date-stamp anything about AI capability. Prefer standards, software docs and practitioner writing over marketing pages.**

---

## Part 0 — Why the brief is shaped this way (background, not for pasting)

**The YouTube sources looked outdated because they answer a different question.** They teach *a tool*. This project does not need a tool; it needs **a data model that produces drawings, quantities, budgets and images, and that can be re-run when a decision changes.** That is a different literature — BIM/QTO/5D, open-source IFC tooling, and the 2024–2026 agent layer — and almost none of it is on renovation YouTube.

**⚠️ The brief deliberately tells Gemini what already exists.** Without that it will return a beginner's tool comparison. With it, it has to engage the real gaps. The digest in the prompt is factual and taken from this repo today; **if it drifts, update it before reusing this brief.**

**⚠️ And one honest warning to carry into reading the results.** The owner's thesis is probably right for **2D documentation, quantities and budgeting**, which are data problems. It is least likely to hold for **photoreal rendering and for material/colour judgement**, which are perceptual. Expect the research to split along that line, and be suspicious of an answer that says everything is automatable — or that nothing is.

---

## Part 1 — The long-form version (a fallback, not the prompt)

**Use the short prompt at the top of this file.** This expanded version exists for two cases only: **the short prompt comes back shallow on a specific question** and you want to re-ask that section with its sub-bullets, or **a future session needs the full context digest** without re-deriving it from the repo. Do not paste the whole thing — it reads as a specification, and Deep Research answers a *question* better than it answers a brief.

---

**Role and goal.** You are researching established professional practice and current (2024–2026) tooling for one specific job: **turning a single apartment renovation into a decision-ready, worker-ready document set — 2D plans, a 3D model, quantities, budgets and visualisations — produced and maintained by one person using AI agents and open-source tooling rather than a commercial CAD/BIM seat.**

I am the owner and the project manager of my own renovation. I am not an architect and I am not buying a tool. I already have a working pipeline (described below). **I want to know what professional practice has already settled, what of it I am missing, and which parts of the remaining work are genuinely automatable now versus still requiring a specialist or a paid product.**

**Test my thesis; do not assume it.** My thesis is: *for this scope, a data-model-plus-agents approach can replace SketchUp / ArchiCAD / Revit / Planner 5D at acceptable quality.* Report where that holds, where it breaks, and what the breaking points cost.

### Context — what already exists, so do not propose it

A private repository already implements a substantial part of this flow. **Treat all of this as done and working, and do not recommend rebuilding it:**

- **Canonical data layer.** Apartment geometry as JSON/CSV: wall runs, wall faces, openings and their spans, corner ownership ledger, room schedules, per-room internal elevations ("развёртки"), plumbing anchors, existing electrical points, wall materials, a dimensional tolerance record.
- **A model, in IFC.** Built programmatically with IfcOpenShell: 18 walls, 8 spaces, 11 openings (7 doors, 4 windows), 13 electrical devices, 3 plumbing devices, 7 light fixtures. Ceiling height 2500 mm. Monolithic reinforced-concrete frame, so external walls are non-load-bearing and only the frame and the common shafts/risers are immovable.
- **A variant system.** Layout options are expressed as patch files against a base, built with one command, and diffed against each other programmatically.
- **Validation that actually gates.** Wall-junction checks (no overlaps, gaps or unowned L-corner voids), a corner ledger deciding which wall owns each corner, room-rollout closure checks on both axes, canonical-data validation, a model-quality audit, and a quantity-take-off gate.
- **Drawing production.** Four A3 sheets generate from the IFC (architectural / electrical / plumbing / combined) through an SVG→PDF pipeline, with a per-sheet manifest and placement validation that checks symbols snap to walls, avoid openings and sit inside rooms. Also a DXF export carrying phase layers (existing / demolished / new).
- **3D viewing, and a working render script.** Portable Blender with the Bonsai (ex-BlenderBIM) add-on; the IFC opens with its data intact. There is also a scripted room-by-room demonstrator that builds a Blender scene from the IFC, sets up **per-scenario lighting**, and renders PNGs headlessly — **but on the EEVEE real-time engine, from an older provisional model, with no material library and no photoreal intent.**
- **Source geometry.** The redesign was drawn in Homestyler and exported as DWG/DXF at millimetre precision; room labels (area and perimeter per room) are extracted from the DWG's text layer.
- **A pricing side.** A local SQLite price database with a scraper, plus a historical-FX converter (daily, trailing-N-month and calendar-year bases) so any price can be normalised to USD at the date it was quoted.
- **A safe agent boundary.** A local allowlisted JSON-lines interface exposing validation, IFC generation and design validation to an agent, with no arbitrary shell, code, network or file writes.
- **A knowledge base.** ~250 wiki pages synthesised from ~820 extraction notes taken from practitioner sources, holding trade rules, failure modes and price benchmarks.

**The known gaps, which are what I want researched:** the model carries **no element phase, no finish schedule, no real furniture objects, and no electrical circuits**; the existing sheets are drawn from heuristics rather than from decisions; **quantities are not yet wired to prices**; **the render path is a real-time-engine demonstrator, not a presentable image, and is not connected to the current model**; and **colour/material selection is not systematised**. The target deliverable is a **16-sheet planning-project album** in the Russian/Belarusian «планировочный проект» tradition.

**Jurisdiction:** the apartment is in **Minsk, Belarus**. Practitioner technique from Russian sources is usable; **regulatory, normative and cost-estimating rules are not transferable between the two and must be sourced for Belarus specifically.**

### Research questions

Answer these in order. **Cite sources for every factual claim, and mark clearly where you are inferring rather than citing.**

**Q1 — The deliverable, as a profession defines it.** What does an established Russian/Belarusian «планировочный проект» / «дизайн-проект» album actually contain, sheet by sheet, and what do international equivalents include that it omits (or vice versa)? Which sheets are contractually load-bearing — the ones trades and inspectors actually work from — and which are sales material? **Name the drawing-convention standards that govern them** (СПДС / ГОСТ 21.501 and successors; the Belarusian equivalents, СТБ or ТКП; ISO 128 / ISO 13567 layer conventions for comparison), and say which are mandatory versus customary for a private interior fit-out.

**Q2 — Quantity take-off from a model: the settled method.** How is QTO done properly from a BIM model, at the level of detail a single apartment needs?
- The IFC mechanisms that exist for it — base quantities, `IfcElementQuantity`, `IfcQuantityArea` / `Length` / `Volume`, and how completely IfcOpenShell can compute them versus read them.
- **What must be measured off the model versus what must be measured off a rule** (e.g. plaster area from wall faces, but adhesive consumption from a product datasheet).
- The standard waste/overage allowances by trade, and **whether professionals actually use percentages or nested cutting plans** — I have a practitioner source achieving under 1% waste on framing by nesting cuts, and I want to know whether that is normal practice or exceptional.
- **The classification/coding layer**: is there a real benefit for a single flat in adopting a coded classification (Uniclass, OmniClass, or a national смета basis) to key quantities to prices, or is a flat product list sufficient at this scale?

**Q3 — From quantities to a budget, and to budget *deltas*.** This is my most important question.
- How is **5D BIM** actually practised — the mechanism linking a model element to a unit rate, and how the link survives a design change.
- **What the Belarusian cost-estimating basis is** for renovation work (НРР / нормативы расхода ресурсов, and whatever governs private residential fit-out), how a смета is legitimately built from it, and whether a private owner can use that basis or should price from market quotes instead.
- **How to price a self-managed / itemised renovation as opposed to a turnkey one** — the two produce different $/m² figures for the same work, and I need the itemised path.
- **The specific capability I want: given two layout variants, produce the cost delta between them automatically.** Does established practice support that, what is it called, and what is the minimum data needed to make it honest rather than decorative?
- **How practitioners handle price validity over a long project** — indexation, re-quoting triggers, and contract language that survives material-price movement.

**Q4 — 2D documentation without a CAD seat.** What is the current state of producing construction-grade 2D drawings programmatically?
- The realistic capability of **IfcOpenShell + IfcConvert**, **ezdxf**, **FreeCAD's BIM workbench**, **Bonsai's drawing/annotation system**, and **Speckle**, specifically for plans, elevations, sections, dimension strings, tags, schedules and a title block.
- **Where each one stops** — annotation, dimension-string automation and sheet composition are where I expect the wall, so be concrete about it.
- **What "worker-ready" actually requires** that a coordination drawing does not: tolerances, setting-out dimensions from a stated datum, mark/tag schedules, notes, and revision control. **Name the omissions that most often send a trade back to ask a question.**

**Q5 — 3D and rendering: what is automatable in 2026 and what is not.**
- The current path from IFC to a presentable image: **Blender + Cycles headless scripting**, material libraries, IBL/lighting setup, and what quality is reachable without an artist. **I already render headlessly on EEVEE with scripted lighting scenarios, so the question is specifically what the step up to a presentable image costs** — engine, materials, lighting, camera and post — and whether that step is worth taking at all for an owner-managed project.
- **Where AI image generation genuinely fits**: ControlNet depth/line conditioning from a rendered viewport, img2img over a clay render, and the current honest assessment of **geometric fidelity** — does it preserve real dimensions and openings well enough to show a client, or only well enough for mood?
- **Whether any of the 2024–2026 text/image-to-3D or plan-to-3D systems are accurate enough for construction**, as opposed to visualisation.
- **The reverse direction**: photogrammetry or Gaussian splatting from phone photos of a real flat, and whether it can produce measurable as-built geometry or only appearance. I have a photo survey of three comparable flats and would like to know if it is exploitable.

**Q6 — Colour, material and finish selection, systematised.** What established method exists for deriving a coherent palette and finish schedule for a whole flat, as opposed to picking per room?
- The professional conventions actually used (60/30/10, LRV, undertone matching, sample-under-real-light protocols), and which of them survive contact with evidence.
- **Whether any of it is legitimately automatable** — colour-harmony computation, LRV-driven lighting checks, palette extraction from a reference image — and where a human eye remains non-negotiable.
- **How the palette becomes a schedule**: the data a painter, tiler and fabricator actually need, per surface, and how professionals stop the schedule drifting from the drawings.

**Q7 — The agent layer, which is the part I most need updating on.** What has actually changed in the last 18–24 months that makes this approach viable, and what is hype?
- **MCP servers and agent integrations for CAD/BIM** — for Blender, FreeCAD, Revit, Rhino/Grasshopper, Speckle, IFC — with an honest read on maturity, safety and whether anyone uses them on real work.
- **Agent-driven quantity and estimating workflows**, and any published case of a small project run this way.
- **Vectorising a raster floor plan** — the current state of plan-image-to-geometry (segmentation models, commercial converters, published pipelines) and the accuracy actually achieved, because I have one layout that exists only as a dimensioned image.
- **Parametric/rule-driven layout generation** (Grasshopper, Dynamo, generative-layout research) and whether it is useful for a single flat or only at portfolio scale.
- **The safety and review question**: what practices exist for keeping an agent-produced model trustworthy — validation gates, information-delivery specifications (**IDS**), issue exchange (**BCF**), model-checking rules. I already gate on geometry; I want to know what else is standard.

**Q8 — Where the thesis fails, and what the fallback costs.** Be adversarial here.
- **Name the specific tasks in this scope where a commercial seat (Revit / ArchiCAD / SketchUp+plugins / a Planner-5D-class tool) still wins decisively**, and quantify what it would cost to buy just that capability — including one-off outsourcing rather than a subscription.
- **The failure modes of a self-built pipeline** on a real construction site: drawings the trades won't read, revision drift, a model nobody but the author can open, a quantity error that reaches an order.
- **The hybrid most professionals would actually recommend for my situation**, and why.

### Output format

Produce a structured report with:

1. **An executive verdict on my thesis**, split by capability (documentation / quantities / budgeting / 3D / rendering / colour), each rated **replaceable by agents now / replaceable with effort / not replaceable yet**, with the reason in one sentence each.
2. **A gap table**: for each of my six named gaps (phase, finishes, furniture, circuits, quantities-to-prices, rendering), the established method, the specific open-source or scriptable path, the realistic effort, and the failure mode to watch.
3. **A prioritised sequence** — what to build in what order, with dependencies, given that I want a budget number as early as possible and want to change decisions late.
4. **A standards and conventions list** I should be complying with, separating mandatory from customary, and flagging Belarus-specific items distinctly from Russian ones.
5. **Named tools and libraries**, each with: what it does in this pipeline, maturity, licence, whether it is scriptable/headless, and whether an agent integration exists.
6. **A "do not build this" list** — things I should buy, outsource once, or skip.
7. **Sources**, grouped by question, with a note on the age of each and whether it has been superseded.

### Constraints and exclusions

- **Prefer primary and professional sources**: standards, software documentation, published BIM/QTO methodology, practitioner and industry writing. **Marketing pages and SEO listicles are not evidence.**
- **Say when something has changed recently.** If a 2021 recommendation no longer holds, say what replaced it and when.
- **Date-stamp volatile claims** (model capabilities, product features, prices).
- **Do not recommend a workflow that requires a Windows-only paid seat** without flagging it as exactly that.
- **Do not conflate Russian and Belarusian regulation or cost bases.** If a Belarusian source cannot be found for a point, say so rather than substituting a Russian one.
- **No generic "BIM improves collaboration" content.** Every recommendation must be executable by one person with a laptop, Python, Blender and an LLM agent.

---

## Part 2 — What to do with the result (our side, not Gemini's)

### Acceptance criteria — reject the report if it does not do these

| Test | Why |
| :--- | :--- |
| **Does it distinguish Belarus from Russia on cost basis and regulation?** | Standing rule 4 exists because this failure mode is common and expensive |
| **Does it answer Q3's variant-cost-delta question concretely**, with a named method? | That is the single capability the whole exercise is for |
| **Does it name where the thesis FAILS?** | A report that says everything is automatable has not been researched |
| **Does it date its claims about AI/agent capability?** | The whole reason for asking is that this layer moves quarterly |
| **Does it avoid re-proposing what the context digest says is built?** | If it recommends "start by modelling the walls", the digest was ignored — re-paste and retry |
| **Are quantity rules separated into model-measured vs datasheet-derived?** | Conflating them is how a take-off silently goes wrong |

### Then, in this repo

1. **File the report** under `_Inbox/planning/`, and treat it as a **source**, not as a decision — it gets read against `00_Master/Sheet_Production_Roadmap.md`'s ten capabilities, and the roadmap is amended where the research contradicts it.
2. **Anything about drawing conventions** goes to `00_Master/Planning_Project_Deliverable_Set.md`; anything about the model contract to `.agents/skills/residential-bim-geometry-rules/`; anything about the build chain to `.agents/skills/apartment-layout-modelling/`.
3. **⚠️ Cost-basis findings go to `11_Budget_and_Planning/`, and any regulatory finding must clear the Belarus level-1 bar before it touches `16_Legal_and_Regulations/`.**
4. **Re-scope the ten capabilities** against the report's prioritised sequence, and record what changed and why — the roadmap already says the gap is decisions rather than a drawing engine, and the research may sharpen or overturn that.

### Two things worth watching for in the answer

- **The rendering question may resolve against automation, and that is fine.** If the honest answer is "a clay render plus AI styling is mood-only, and a client-grade image needs an artist or a paid tool", that is a useful, cheap answer — it removes an item from the roadmap rather than adding one. **Note this is the one place the context digest was wrong on the first draft**: `tools/blender/build_apartment_demo.py` already renders scenario-lit PNGs headlessly on EEVEE from the provisional IFC. The gap is *quality and connection to the current model*, not existence — and the digest was corrected before use, because a brief that understates what exists gets a beginner's answer back.
- **The plan-vectorisation answer has a specific consumer waiting.** `v0`, the developer's own layout, exists only as a dimensioned image and is the one blocker standing between this project and a measured like-for-like layout comparison. If Q7 returns a credible path, that is the first thing to try; the current fallback is a second Homestyler export or hand reconstruction from the dimension strings.

---

## Gemini's returned plan — coverage check (2026-09-08)

Gemini answered the short prompt with an 8-step research plan before running. **It maps cleanly onto all eight questions and keeps the jurisdiction guard** — its step (1a) explicitly contrasts Belarusian СТБ/ТКП against Russian СП and interstate ГОСТ/СПДС, and step (2) is scoped to Belarusian НРР. It also added two useful details of its own: **line weights and hatch patterns** under the 2D question.

**Six items from the prompt did not survive into its plan, and were sent back as an amendment:**

| Dropped | Why it matters |
| :--- | :--- |
| **Can a private owner actually use the НРР basis, or must he price from market quotes?** | ⚠️ The practical crux. If the answer is "not usable", half the cost-basis research is academic and the fallback is market quotes plus this repo's own price DB |
| **Self-managed / itemised versus turnkey pricing** | The two give different $/m² for identical work; this project is explicitly self-managed, and the vault already separates the two delivery models |
| **Price validity over a long project** — indexation, re-quoting triggers, contract language | `11_Budget_and_Planning` already holds «never price a long contract at signing-day material prices»; this is the method behind it |
| **A coded classification layer** (Uniclass / OmniClass / смета basis) at single-flat scale | Determines whether quantities can key to prices at all, or whether a flat product list suffices |
| **Speckle, and drawing revision/version control** | Revision drift is a named failure mode of a self-built pipeline — it matters more here than draughting quality |
| **Photogrammetry / Gaussian splatting from phone photos** | ⚠️ Has a consumer waiting: `_Survey/` holds 30 photos of three comparable flats, and `v0` still has no geometry |

**Also reasserted**: the output format (verdict per capability, gap table, build order, standards list separating mandatory from customary and Belarus from Russia, tools with maturity and licence, "don't build this" list) and the date-stamping of AI-capability claims — Gemini's plan restated none of it, and that is what makes the report usable rather than readable.

**And one steer on effort**, sent with the amendment: **do not let steps (1) and (2) consume the budget.** The standards research is the easiest to find and the least likely to have changed; **the highest-value items are the automatic cost delta and the agent layer.**

---

## Amendment 2 — after the primary-law pass (2026-09-08, same day)

**Gemini's revised plan absorbed all six of the dropped items above and is good as written.** What changed underneath it is the **legal** ground: `16_Legal_and_Regulations/` was filled from **Постановление Совмина РБ № 164 of 03.04.2026**, read in full, the same day — see [[_Sources/DOC_postanovlenie_164_2026_pereustroystvo_pereplanirovka|the source note]].

**So research item (1) was rewritten from "identify the standards" to "fetch the six acts № 164 defers to".** The full amendment as sent is below, in brief.

### What is now settled and must not be re-researched

№ 164 repeals № 384 of 2013 in full; it is a Council-of-Ministers постановление under ЖК ст. 5; §3 is a closed list whose final sentence puts finishes, tiling, screed-over-screed, in-place sanitaryware, sockets, lighting and furniture **outside** perепланировка (while insulation is **inside** it); two approval tracks with проект + ТУ only for gas and central heating; §14 permits self-performance; §10 puts waste rules and the acceptance date in the permit; §17's 30-day commission lead; §20's план-схема as the acceptance standard; and Положение 2 §2 covering AC equipment.

### The six acts requested instead, in priority order

1. **Указ № 200** (1.1.21, 1.1.21¹, 1.1.21², 1.15.1, 1.15.3) — the citizen document lists. **Nothing about the application can be stated without them.**
2. **СН 3.02.01-2020** — the wet-zone rule, quoted.
3. **The § 21 registration legislation** — passport vs ведомость, cost, lead time, and what changed on 1 January 2023.
4. **«Правила пользования жилыми помещениями»** — the noise regime for non-перепланировка work, and whether it applies per task.
5. **СН 2.02.05-2020** — fire resistance for new internal partitions.
6. **КоАП** — the penalties § 29 refers to without quantifying.

Plus **one drafting question**: whether абзац первый of части первой пункта 3 is the introductory phrase or the first list item — **it decides whether this project pays for a ведомость технических характеристик.**

### And three findings that re-scope other items

| Item | Change |
| :--- | :--- |
| **(2) cost basis** | **Answer "can a private individual use НРР at all?" EARLY.** If not, the item pivots to market-quote methodology — and this repo's own price DB plus FX normalisation becomes the primary instrument rather than a supplement |
| **(4) documentation** | **§20 makes the submitted план-схема the acceptance standard**, so the documentation must be **deliberately under-specified where decisions are still open** and precise where they are not. Asked whether established practice exists for scoping a permit submission to preserve late flexibility — **which is the legal form of the owner's own "changeable on the fly" requirement.** Also: what belongs in **акты на скрытые работы when the owner performs the work himself** |
| **(8) build order** | **Noisy work is confined to weekdays 09:00–19:00, and acceptance needs 30 days' notice. The binding constraint on this pipeline is calendar, not compute** — and the build order should reflect that |

> **⚠️ The most consequential of those is (4).** The project's stated goal is a model flexible enough to change late; № 164 §20 means **every late change is also a change to the document you are accepted against.** The two requirements are in tension, and the resolution is probably to keep the permitted-works description to what is genuinely decided — which § 3's closed list makes viable, since most late-changing decisions (finishes, fixtures, furniture) are not перепланировка at all. **Research is being asked to confirm or refute that reading.**
