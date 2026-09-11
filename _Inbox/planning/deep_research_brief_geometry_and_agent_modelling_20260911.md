# Deep Research brief — wall topology, raster→geometry, and agents that drive a modeller

**Created 2026-09-11** at the owner's request: *"we're struggling to draw walls to connect them properly, to avoid overlapping or leaving gaps between walls… I know probably we reinvented a wheel so we can get new tools, new approaches."*

**This file is the brief, not the research.** §1 is a paste-ready prompt. §2 says how to judge what comes back. §3 records what was verified in the repo today, so the prompt's context digest can be trusted and updated rather than re-derived.

**Companion to [`deep_research_brief_3d_budgeting_toolchain_20260908.md`](deep_research_brief_3d_budgeting_toolchain_20260908.md)**, which asked the broad toolchain question. This one is narrow and deliberately so: **geometry correctness, getting a dimensioned raster into geometry, and the agent-driving-a-modeller layer.**

---

## ⚠️⚠️ Read this before sending: the premise in the request is out of date, and one wheel really was reinvented

**Checked in the repo today, 2026-09-11, not recalled:**

| Claim | Verified state |
| :--- | :--- |
| *"struggling to draw walls to connect them properly"* | **`check_wall_junctions.py` → PASS.** 25 wall runs, *"no overlap, no gap, and every L-corner void is owned in `wall_corners.csv`"* |
| *"avoid overlapping or leaving gaps"* | **`check_dxf_closure.py` → PASS.** No unsanctioned overlap, no unexplained near-miss inside the 400 mm band, no wall-union cavity, both delivered review images byte-identical to a fresh render |

**→ Wall junction closure is not currently broken. It is solved, gated, and guarded by 24 seeded defects (`dxf_closure_selftest.py`) plus 7 more on the raster side.** Asking research to solve it would waste the delegation.

> [!IMPORTANT]
> **⚠️⚠️ BUT THE "REINVENTED A WHEEL" INSTINCT IS CORRECT, AND HERE IS THE PROOF — this is the single most useful finding available today.**
>
> `wall_corners.csv` decides which wall owns each L-corner by a home-grown rule: **thicker first, then longer.** That is a hand-rolled priority scheme.
>
> **IFC already standardises exactly this.** Verified against the IFC4 schema via IfcOpenShell today — `IfcRelConnectsPathElements` carries:
> - **`RelatingPriorities` / `RelatedPriorities`** — integer priority lists **per material layer**, which is the standard mechanism for deciding whose layers win at a junction;
> - **`RelatingConnectionType` / `RelatedConnectionType`** — `ATSTART` / `ATEND` / `ATPATH`, making **corner-versus-T-junction a first-class distinction in the schema.**
>
> **And `grep` across the whole repo returns ZERO uses of it.** The corner ledger is a private reimplementation of a standard relationship, in a project whose model is already IFC.
>
> **This does not mean the ledger was wrong** — it passes, and a per-layer priority model is more than a single-owner ledger needs today. **It does mean the research question is "should the ledger become `IfcRelConnectsPathElements`", not "how do we close corners".**

---

## §1 — ⭐ THE PROMPT — paste this

> I maintain the complete drawing and model set for **one apartment renovation in Minsk, Belarus** myself, using **Python + IfcOpenShell + ezdxf + Blender/Bonsai and AI coding agents** rather than a Revit/ArchiCAD/SketchUp seat. The geometry layer works and is gated. I want to know **which parts of it I have hand-rolled that an established formalism or standard already covers**, and what the 2025–2026 agent layer genuinely adds. **Test my approach; do not assume it, and do not sell me a tool.**
>
> **Already built and PASSING — do not propose any of it.** Apartment geometry as canonical CSV/JSON; walls as calculation legs grouped into physical *assemblies*; a corner-ownership ledger deciding which wall owns each L-corner (*thicker, then longer*), so `solid = clear + owned corners`; validators that gate on overlap, gap, unowned L-corner void, unexplained perpendicular near-miss and wall-union cavity; a DXF closure gate asserting wall identity, absolute faces, drawn length and thickness — cross-checked against an independent oracle that re-derives the hatched wall solids from the source PDF at check time; a raster-fidelity gate measuring DXF-edge→ink and ink→DXF-body distances against a *frozen* mask and a *committed* registration; adversarial self-tests (24 seeded DXF defects, 7 raster, 13 tabular) that must each be rejected. IFC model, layout variants as typed patch files, four A3 sheets generating, DXF with existing/demolished/new layers.
>
> **Research these, in this order:**
>
> 1. **Wall junction topology as a SOLVED problem in the literature.** I hand-rolled a corner-ownership ledger. IFC has `IfcRelConnectsPathElements` with per-layer `RelatingPriorities`/`RelatedPriorities` and `ATSTART`/`ATEND`/`ATPATH` connection types, and I use none of it. **How do Revit's and ArchiCAD's wall-join and layer-priority systems actually resolve a junction, what is the underlying formalism (half-edge/BREP topology, straight skeleton, boolean solid operations, polygon offsetting), and what is the open-source equivalent** (OCC/OpenCascade, CGAL, Shapely, FreeCAD's Arch module)? **Should a one-flat model adopt the IFC relationship, or is a private ledger the right scope?** Name the failure modes of each.
>
> 2. **A raster floor plan carrying PRINTED DIMENSION STRINGS → geometry. This is my actual blocker.** My baseline layout exists only as a dimensioned plan image; partition positions must be reconstructed from the printed dimension strings, and it is currently hand work. **What is established practice — vectorisation, OCR plus a constraint solver, scan-to-BIM, commercial plan-to-BIM services? How reliable are 2025–2026 vision-language models at reading dimension strings and their extension-line endpoints, with measured error rates, not vendor claims?** I already require **chain closure** (a run of dimensions must sum to a known whole) as validation — **what else is used to catch a misread dimension, and what does the error distribution look like?**
>
> 3. **Constraints versus absolute coordinates.** My model stores absolute coordinates at a stated **±50 mm nominal** tolerance; a variance study across three as-built flats of the same layout measured **−45 to +30 mm** against the developer's plan. I have also seen a planner tool dimension a centred fixture as **`1/2`** rather than in millimetres, so the intent survives site variance. **Should the layout be a CONSTRAINT SYSTEM (dimension chains that must close, symmetry and centring as relations) rather than fixed coordinates?** What do parametric/constraint solvers (FreeCAD's sketcher, SolveSpace, layout-specific constraint solvers, geometric constraint solving literature) offer a building layout, and where does it break down? **How do drawing standards express a relative or proportional dimension, and can DXF or IFC annotation carry one?**
>
> 4. **AI agents that drive a 3D modeller — what actually works in 2025–2026.** MCP servers and plugin APIs for SketchUp, Blender, FreeCAD, Rhino and Revit; agents that generate geometry *as code* versus manipulating a GUI; the reliability difference. **Is there measured evidence that a GUI-driving or plugin-driving agent beats a programmatic pipeline like mine for building geometry, or is code generation still the more reliable path?** Include honest failure modes and date-stamp every capability claim.
>
> 5. **Automated rule checking against a model.** I have ~50 machine-readable layout rules (minimum clear widths, adjacency, avoid-rules, sequencing) with parameters and rationale, and **nothing consumes them.** What is the established route — **IFC IDS**, model checking (Solibri, BIMcollab Zoom, open-source checkers), BCF for reporting issues back — and what is the cheapest path from a rules file to a gate that fails a variant?
>
> 6. **Where my approach genuinely loses**, naming the task and what buying or outsourcing just that capability costs.
>
> **Also — and this matters as much as the answers: name SOURCES I should follow.** Specific practitioners, YouTube channels, GitHub repositories, papers, standards documents and forums that cover open-source BIM geometry, plan-to-BIM extraction, and agent-driven CAD. I build a knowledge base from named sources, so a named person or repo is worth more to me than a summary.
>
> **Cite everything. Date-stamp anything about AI capability. Prefer standards, source code and practitioner writing over marketing pages. Where you are uncertain, say so rather than smoothing it over.**

---

## §2 — How to judge what comes back

**The previous brief's results were graded in [`deep_research_review_20260908.md`](deep_research_review_20260908.md); the same standard applies. Its lesson: the report's most valuable output was a SCHEMA and a set of CASCADE RULES, and its worst were confident claims about a norm it had misread.** Expect the same split.

| Question | A good answer looks like | Reject if |
| :--- | :--- | :--- |
| 1. Junction topology | Names the formalism and says what each *cannot* express; gives a clear verdict on adopting `IfcRelConnectsPathElements` at one-flat scale | It describes how to draw a wall in a GUI, or restates that corners need resolving |
| 2. Raster→geometry | **Measured** error rates with dates and sources; names validation beyond chain closure | Vendor accuracy claims, or "modern AI can read drawings" with no number |
| 3. Constraints | Engages the ±50 mm / −45…+30 mm reality and says where constraint solving is worth the complexity | It recommends a parametric CAD seat |
| 4. Agents | Dated, sourced capability claims and named failure modes | Undated enthusiasm, or a list of products |
| 5. Rule checking | A concrete path from a rules file to a failing gate, IDS named properly | "Use Solibri" with no route from my data |
| 6. Where it loses | Named tasks with prices | A generic "hire a professional" |

> [!WARNING]
> **⚠️ Three specific ways this research will try to mislead, all of them seen before in this project.**
>
> 1. **It will substitute Russian norms for Belarusian ones.** The last report did this and it had to be corrected — and standing rule 4 exists because of it. **Anything regulatory must be Belarus (СТБ / ТКП) or be flagged as Russian.**
> 2. **It will overstate vision-model drawing comprehension.** `00_Master/Evidence_Reading_Discipline.md` records **seven real failures** of reading a dimension off an image *in this project*. An AI that reads dimension strings confidently and wrongly is the exact failure this vault has already been burned by. **Demand error rates; treat any un-numbered claim as marketing.**
> 3. **It will propose a tool where a formalism was asked for.** The question is what the *concept* is, not what software has a button for it.

**And the standing trap from the last round, worth restating: do not let a recommendation framed for surveying an EXISTING flat land on this one. The flat is not built yet** (`tools/cad/PROVISIONAL_MODEL_POLICY.md`: *"the current model is a planning baseline, not an as-built survey"*). A laser-meter recommendation was retracted for exactly this reason on 2026-09-08.

---

## §3 — What was verified today, so the digest can be trusted

All checked 2026-09-11 in the working tree, not recalled:

- `tools/layout/check_wall_junctions.py` → **PASS**, 25 wall runs, no overlap/gap, every L-corner owned.
- `tools/layout/check_dxf_closure.py` (under `.venv-ifc314`, which has `ezdxf` 1.4.2) → **PASS**, including the delivered-image byte-identity check. ⚠️ **It does not run under `py -3`** — `ezdxf` is absent there, and `AGENTS.md` already warns the venvs are not interchangeable.
- IFC4 schema via IfcOpenShell → `IfcRelConnectsPathElements` confirmed with `RelatingPriorities`, `RelatedPriorities`, and `IfcConnectionTypeEnum` = `(ATPATH, ATSTART, ATEND, NOTDEFINED)`.
- `grep` for `IfcRelConnectsPathElements|RelatingPriorities|ConnectionTypeEnum|ATSTART` across the repo → **zero matches.**
- `00_Master/project_decisions.md` open items → **`v0` still has no geometry and it BLOCKS layout selection**; the recorded route is reconstruction from the printed dimension strings on `fllor_plan_detailed.jpeg` over the registered raster, described there as *"hand work"*. **That is why question 2 is the blocker and not question 1.**
- `data/layout_rules/rules.jsonl` → 50 rules; nothing in `tools/` reads the file (the gap analysis of 2026-09-08 already recorded this and it is still true).

## §4 — Gemini's returned PLAN, reviewed 2026-09-11

**Gemini came back with a 7-step research plan, not results.** Recorded here because the plan is the last cheap moment to correct the research, and because the repo's precedent ([`deep_research_review_20260908.md`](deep_research_review_20260908.md)) is to grade what a model returns rather than accept it.

### Coverage — it maps onto all six questions, and improves on two

| Brief | Gemini's step | Verdict |
| :--- | :--- | :--- |
| Q1 junction topology | **(1)** formalisms in Revit/ArchiCAD, OpenCASCADE, CGAL, Shapely, FreeCAD Arch — BREP, straight skeleton, polygon ops · **(2)** IFC schema *versus* a private ledger, with failure modes | ✅ **Better than asked.** It split the formalism from the adopt-or-not decision, which is the right order — the decision is not answerable until the formalism is |
| Q2 raster + printed dimensions | **(3)** OCR + constraint solving, VLM accuracy, **"benchmarked error rates"**, and **"validation mechanisms for dimension chain closure"** | ✅ It caught the chain-closure ask and the demand for numbers rather than claims |
| Q3 constraints vs coordinates | **(4)** SolveSpace, FreeCAD Sketcher, layout solvers, construction tolerances, relative/proportional dimensions in IFC and DXF | ✅ Complete |
| Q4 agents driving a modeller | **(5)** MCP, plugins, GUI automation vs headless code generation, **"measured reliability and failure modes"** | ✅ Complete |
| Q5 rule checking | **(6)** IDS, **IfcTester**, Solibri, BIMcollab, BCF → a pass/fail gate | ✅ **Names `IfcTester`, which the brief did not.** That is the likely answer to "cheapest path from a rules file to a gate", and it came from the model rather than from us |
| Q6 where it loses | **(7)** cost-benefit of a custom pipeline vs licences vs outsourcing | ✅ |
| The sources ask | **(7)**, second half | 🟡 **Bundled — see below** |

### ⚠️ Three things to put back before it runs

1. **⚠️⚠️ THE DATE-STAMP REQUIREMENT IS GONE.** The brief said *"date-stamp anything about AI capability"*, and nothing in the plan carries it. Steps (3) and (5) do ask for measured reliability, which is most of the value — but **an undated capability figure is worthless within months.** The 2026-09-11 video batch demonstrated this directly: five of eleven sources were model tests whose verdicts were discarded on sight as already stale.
2. **⚠️ THE SOURCES DIRECTORY IS BUNDLED INTO THE COST-BENEFIT STEP, AND IT LOST TWO CATEGORIES.** The brief asked for practitioners, **YouTube channels**, GitHub repos, papers, standards and **forums**; the plan keeps repos, papers, standards and practitioners, and drops YouTube and forums. **That matters more here than it would elsewhere: this vault is built almost entirely from named YouTube practitioners, so a dropped channel is a dropped intake route.** A directory sharing a step with a cost analysis will also come back thinner than one with its own step.
3. **⚠️ THE PLAN READS AS A NEUTRAL LITERATURE SURVEY, NOT AS A TEST OF A THESIS.** The brief said *"test my approach; do not assume it, and do not sell me a tool"*, and listed what is already built and must not be proposed. **None of that framing survives into the plan.** The "already built" block is still in Gemini's context, so this is a risk rather than a defect — but it is the exact failure the 2026-09-08 brief had to guard against, where a report's gap table *"describes, almost line for line, what is already built."*

### ⭐ Paste this back to Gemini before approving the plan

> Approve the plan with three amendments:
>
> 1. **Date-stamp every claim about AI or model capability** — for each, give the month and year it was measured or published, and say explicitly when a figure is a vendor claim rather than an independent measurement. Undated capability numbers are useless to me.
> 2. **Make the source directory its own step, not part of the cost-benefit step**, and include **YouTube channels and practitioner forums** alongside repos, papers, standards and named people. I build a knowledge base from named sources; a channel or a repo is worth more to me than a summary.
> 3. **Frame the whole thing as testing my existing pipeline rather than surveying the field.** For each of the six areas, answer *"is what he already has adequate, and if not, what specifically replaces it?"* — and do not recommend anything in the "already built" list. Where my approach is already the established one, say so plainly; that is as useful to me as a gap.
>
> Also: ignore "PlanNer" in my question 3 — that was my typo. Your reading of it as layout-specific constraint solvers is what I meant.

### On jurisdiction — low risk here, one place to watch

Standing rule 4 and the last brief's Russian-norms substitution make jurisdiction the default worry, but **this brief is deliberately non-regulatory and the plan reflects that.** The one exposure is **Q3/step (4)'s "how do drawing standards express a relative or proportional dimension"** — a standards answer can arrive as ГОСТ 21.501 / СПДС when Belarus uses СТБ / ТКП. **If that question returns a standard, check which country's it is before acting on it.**

## Open items this brief does not settle

- **Whether to adopt `IfcRelConnectsPathElements`** is a real decision with a real cost, and the research is being asked to inform it rather than make it.
- The brief asks nothing about cost, procurement or scheduling — those belong to the 2026-09-08 brief and the BOM work, and mixing them in would blunt both.
- **Nothing here asks Gemini to solve the wall closure**, deliberately. If a future session reuses this brief, re-run the two gates first: if they have gone red, the premise changes and §1's digest must be rewritten.
