---
source_type: video transcript (vendor channel, method demonstration - AI agent validating CAD/BIM models against requirements)
source_url: https://www.youtube.com/watch?v=EHCgAi2x8-Q
video_id: EHCgAi2x8-Q
transcript_file: _Archive/processed_sources/20260914_ddc_requirements_three_columns_a735b6aa.txt
fetched: 2026-09-14 via youtube-transcript-api (en)
upload_date: 2026-06-12 (confirmed via yt-dlp metadata)
channel: DataDrivenConstruction
source_title: "AI Agents for BIM Requirements Verification"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / Validation`)
fact_yield: 14
promotional_ratio: high
corroborates_existing: false
contradicts_existing: true
region: not_applicable_method_only
delivery_model: vendor of the free converters demonstrated; a book behind them
---

# Source Note - DataDrivenConstruction: ⚠️⚠️ EVERY REQUIREMENT IS THREE COLUMNS — and the Experiment That Makes the Case (YouTube EHCgAi2x8-Q)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## ⚠️⚠️ Why this one matters: it challenges a commitment this project has already made

[`toolchain_gap_analysis_20260908.md`](../_Inbox/planning/toolchain_gap_analysis_20260908.md) records an **`Adopt`** decision: author a project **`.ids`** ruleset (buildingSMART Information Delivery Specification) and validate the model against it.

> **⚠️⚠️ THIS SOURCE ARGUES, WITH AN EXPERIMENT, THAT THE `.ids` FORMAT IS DOING NO WORK.** Not that validation is unnecessary — the opposite. That **the FORMAT is the accidental part**, and what survives is three columns.

## ⚠️⚠️ 1. The claim

15 requirement files across **eight formats** — a Word execution plan, an Excel matrix, **Solibri Model Checker JSON**, CSV, a nested JSON, **DWS** (AutoCAD standards), **IDS from buildingSMART**, and XML — *"the same 20 validation rules written in eight completely different formats … each with its own structure, its own syntax, its own way of expressing the exact same rules."*

> *"To validate and apply the data in your case study, you only need **three columns. The group or type name, the parameter name, and the boundary conditions for its values.**"*
>
> Restated at the close: ***"ENTITY — what we check. ATTRIBUTE — which parameter. CONSTRAINT — what rule it must follow."***

⚠️ **Two details that make the claim less glib than it sounds.** The Word plan already carried **five** columns — entity, attribute, constraint, **severity, category** — so severity and category are dropped as not load-bearing for the check itself. And the Solibri format costs *"dozens of lines of code"* per rule against IDS's **250 lines of XML for 16 rules** (~15 lines a rule).

## ⚠️⚠️ 2. The experiment — the part worth taking seriously

The same Revit model was validated **twice**, once against the requirements expressed as **JSON** and once against them expressed as **Solibri**:

> **Both dashboards read 76.3%, 1,993 passed, 599 failed. Identical.**
>
> *"It does not matter which format the requirements are written in. If the rules are the same, the result is the same. **The format is unnecessary complexity.**"*

> **→ ⚠️ THE RIGHT SHAPE OF EVIDENCE — hold the rules constant, vary only the notation, and show the outcome does not move.** That is a genuine controlled comparison and it is rarer in this source class than it should be.
>
> **⚠️⚠️ AND THE CAVEAT THAT GUTS HALF OF IT: the SAME AI agent wrote BOTH parsers, in the same run, from the same understanding of the rules.** Two parsers by one author agreeing is **weaker than two independent tools agreeing**. It shows the agent was self-consistent; it does not show that the agent read either format the way its own ecosystem's tool would. ⚠️ **The honest reading: the formats are interchangeable TO THIS AGENT.** ⚠️ **The experiment that would settle it — run the Solibri file through actual Solibri and compare — was not run.**

## ⚠️ 3. The consolidation, and the size of what is left

Second prompt: read every requirement file across every format, extract all rules, deduplicate.

- **16 unique IFC rules, 20 unique Revit rules**, *"all rules correct and found across all seven source formats."*
- Output: **two Excel sheets, three bold columns each, 6 KB each.**
- Final run: **70.7% overall compliance, 3,235 checks passed, 1,343 failed, 36 rules across four projects**, plus a **79-page PDF report** with worst and best performing rules and every failed element.

⚠️ **An arithmetic discrepancy worth recording, because this vault checks totals:** 3,235 + 1,343 = **4,578**, and the narration says **"45,578 total"**. The closing line says *"nearly 5,000 checks"*, which matches 4,578 and not 45,578. **→ The spoken 45,578 is a slip; do not carry it.** ⚠️ **That it went out uncorrected in a video whose subject is VALIDATION is itself the note.**

## ⚠️⚠️ 4. What this means for THIS project

**The gap analysis's `Adopt` of a project `.ids` should be reconsidered, and this is the reason to reconsider it — not to reverse it.**

**The case for dropping `.ids` here:**
- Our rule count is small and will stay small — wall thicknesses, a door clear width, socket heights, a `Pset_<Class>Common.Status` on every demolished element.
- A **CSV of three columns plus a short IfcOpenShell loop** produces the same pass/fail list, **is diffable in git**, and needs **no schema, no editor and no validator binary**. Our toolchain is already exactly this shape — `tools/lib/tabular.py`, strict CSV, a checker per concern.
- `.ids` buys **interoperability with other people's validators**, and **this is a one-person project with no counterparty** that will ever consume our ruleset. ⚠️ **We already declined Speckle on precisely this argument** — *"Git + canonical JSON … is leaner, runs entirely offline."*

**The case for keeping it:**
- ⚠️ `.ids` is an **open buildingSMART standard**, and the vault's standing preference is for open formats over ad-hoc ones. A three-column CSV is a private schema.
- ⚠️ A hand-rolled checker is **apparatus we then have to guard**, and standing rule 10 is unambiguous: **a gate nobody has watched fail is not a gate.** Every rule needs a seeded failure in a selftest. **That cost lands whichever format we choose** — and it is the real cost, not the format.

> **→ RECOMMENDATION, for the owner to decide: write the rules as a three-column CSV first, because that is the part that is actually load-bearing and it can exist this week. Emit `.ids` from it later if a counterparty ever needs it.** The columns are the source of truth either way, **which is the source's actual point and it survives the caveat in §2.**
>
> ⚠️ **Recorded as an OPEN ITEM against the gap analysis, not as a reversal of it.**

## ⚠️ 5. The failing-elements output, which is the transferable half

The run produces *"detailed breakdowns for every project, every rule, **every failed element**"* — and the companion video does the same thing with element identifiers that **paste straight back into the authoring tool**.

> **→ ⚠️⚠️ A CHECK'S OUTPUT IS THE LIST OF THINGS THAT FAILED, ADDRESSED SO YOU CAN GO FIX THEM.** Not a percentage. **This vault's own gates already work this way and `00_Master/Validator_Design_Discipline.md` says why** — *printing is not checking*. **A 70.7% compliance headline is exactly the number that is useless without the list underneath it**, and the source, to its credit, produces both.

⚠️ **The compliance percentage itself should be treated as decorative.** 36 rules of unstated importance, unweighted, over four projects — a model can be 95% compliant and unbuildable, or 70% compliant with every failure trivial.

## ⚠️ What was deliberately NOT extracted

- **Product and tool names as recommendations** — the converter, the book, the specific AI coding agents.
- **The 33 dashboards** (one per project × requirement-format combination) — an artefact of the demonstration, not a method.
- **The "dozens of systems — ERP, 4D, 5D, CAD/BIM, supplier, site software" framing.** Enterprise scale; we have one flat.
- **No prices anywhere in this source.** **No regulatory content.**

## Source Notes

**DataDrivenConstruction** (YouTube), 2026-06-12, ~7 min, **read in full**. `promotional_ratio: high` — it demonstrates the channel's own converters and closes on its own book.

⚠️ **The demonstration is a scripted best case.** Two Revit files and two IFC files, requirement sets the presenter prepared, and no instance shown where the agent misread a format. **The claim that all eight formats reduce to three columns is asserted over ONE curated rule set of 20 rules.** ⚠️ **A production `.ids` also carries cardinality, applicability facets and optional/required distinctions that three columns do not obviously hold** — untested here, and the honest place where the reduction may leak.
