---
source_type: video transcript (construction-AI consultancy channel, systems-design retrospective)
source_url: https://www.youtube.com/watch?v=sjcDHXReSNI
video_id: sjcDHXReSNI
transcript_file: _Archive/processed_sources/20260913_fairley_workflow_systems_failure_modes_680fd79c.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions — ORIGINAL language)
upload_date: 2026 (confirmed via yt-dlp metadata)
channel: Tim Fairley / @ConstructIQ — construction-AI consultancy, sells "Contractor OS"; Australia
source_title: "I've built over 100 AI workflows for Construction - Here's what's actually hard"
language: en
extraction_taxonomy: custom (this project's taxonomy, caller-defined mode — bucket `Digital Toolchain / AI Workflow`)
fact_yield: 11
promotional_ratio: medium
corroborates_existing: true
region: n/a_AU_market_no_jurisdictional_claim
delivery_model: n/a — not a renovation source
---

# Source Note — Tim Fairley: Four Failure Modes of a Standalone Workflow, and the Slop Problem (YouTube sjcDHXReSNI)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Why this source, and the concentration warning that governs it

**Fetched as the single spot-check for the [@ConstructIQ channel triage](../_Inbox/planning/constructiq_channel_triage_20260913.md), on the reasoning that a *what's-actually-hard retrospective* is the highest-value format available and the cheapest test of whether the channel adds mechanism beyond the four drawings videos already held.** It passed, and in a direction the vault did not cover.

> [!WARNING]
> **⚠️⚠️ This is the FIFTH source from this practitioner.** [[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]] is built almost entirely on his other four. **Nothing here corroborates anything there, and nothing there corroborates this** — it is one voice and one product funnel throughout. Where a claim of his needs support, it has to come from elsewhere.

**`promotional_ratio: medium`** — Contractor OS is the backdrop and the whole video is an argument for buying a system rather than assembling prompts, **but the failure modes are given away in full and several of them argue against his own earlier content** (the individual skills and workflows he has spent 100 videos building).

## ⚠️⚠️ Rules / Heuristics — The Four Failure Modes of a Standalone Skill

**His thesis, and the reason the video exists: getting AI to do a single task is no longer hard. Integrating it into a system is.** The worked example is an inspection-and-test plan — one prompt produced seven ITPs — and his question is *"then what?"*: which folder does it go in, who checks it was correct, how do you verify it matches the original requirements, who reviews it, and how do you hand the workflow to a team.

**Even packaged as a named skill, he argues an individual workflow has four failure modes:**

1. **It makes sense to you, not to your team.** You built the prerequisites and the template library into your head; scaling the process requires explaining simply and intuitively how to run it and how to set it up.
2. **⚠️⚠️ The output is fundamentally unreliable, because there is no structured way to guarantee the INPUT CONTEXT or to VERIFY THE OUTPUT.** Stated as the question that exposes it: ***"Who's actually checking the results from it, and how are they checking it?"***
3. **⚠️⚠️ The output gets lost in a mountain of slop.** *"With AI it is easy to generate a lot of information. We could generate a thousand ITPs in a day, but that's probably not going to be useful. What we actually need is ONE high-quality ITP."* **The corollary he draws is the operational one: you need a structured way to check and control what documentation you STORE, or you generate a mass of outputs nobody ever uses.**
4. **⚠️⚠️ Unless the process is documented, you cannot improve it — and this is the one he calls most important.** The first pass at any process is just you working out what the best way might be. **If it is a standalone skill and you never mapped out how it was supposed to run, then when the output is bad it is impossible to work out what went wrong**, so there is nothing to fix and iterate on.

## ⚠️ Durable Facts — Vocabulary, With His Own Scepticism Intact

He is relaying "graph engineering" as an industry buzzword and is openly unconvinced by the name: *"I don't know why they're calling it graph engineering. It's basically just trying to answer the question of how do we build systems that actually produce useful work."* **Recorded with the scepticism, because it is the right attitude to the term.**

- **node = step**, **edge = input** — he prefers the plain words and says so.
- **⚠️⚠️ state = the one term he thinks is genuinely useful.** Not merely context: **context PLUS everything the system has produced so far, carried between steps.** His instance: before the ITPs are generated, the quality lot register and the requirements register already exist, and those form part of the state.
- **⚠️ "The state of the system in construction is fundamentally your project folder."** Open the agent harness inside the project folder; everything the AI knows and everything it has produced lives there.
- **Project context (this project's folder) versus business context (information relevant across projects)** — a two-level split.

**A step taxonomy is given, of which three are worth recording**: an **AI step** (e.g. a skill with an input and an output), a **planning step** (produces the process itself — his example is a quality management plan), and:

- **⚠️⚠️ a "SKEPTIC" step — an INDEPENDENT CHECK of a previous step's deliverables, verifying they are comprehensive.** A named role in the pipeline whose only job is to doubt the previous output.

## ⚠️⚠️ Confidence & Evidence Notes — and why this lands on this project specifically

- **`single-account`**, one practitioner's stated experience over a claimed 100+ workflows. **No measurement anywhere in this source** — unlike his benchmark video, this is entirely argument.
- **`corroborates_existing: true`, and the corroboration is unusually direct and runs BOTH ways:**
  - **Failure mode 2 and the skeptic step are `00_Master/Validator_Design_Discipline.md` arriving from outside.** That page holds that **printing is not checking** and that **a gate nobody has watched fail is not a gate** — reached here as *"who is actually checking the results, and how"*, and answered with a dedicated doubting step. **An outside practitioner independently concluding that a pipeline needs an adversarial checking stage is the strongest external support that discipline has.**
  - **Failure mode 3 — the mountain of slop — lands on a vault holding ~813 extraction notes** that has already had to repair fragmentation across 29 pages. *"One high-quality ITP, not a thousand"* is the same argument as this project's own value filter and its `fact_yield` honesty.
  - **Failure mode 4 — undocumented process cannot be improved — is why `_Inbox/planning/` triage files exist here**, and why the round notes record what was *not* done and why.
  - **State-as-the-project-folder describes this repo's arrangement exactly** — an agent harness opened in a folder whose canonical data, skills and gates are the state.
- **⚠️ The one thing to be careful of: his framing solves the problem by BUYING a system.** This project solves it with deterministic gates and a triage record. **Both answers address the same four failure modes; only one of them is checkable by the person relying on it.**
- **ASR**: good. **No prices; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/AI_Workflow_Systems.md` (NEW PAGE)** — the four failure modes, the state/project-folder definition, and the skeptic step.
- `00_Master/Validator_Design_Discipline.md` — a cross-reference only; the skeptic step as external corroboration.
- **5b**: no prices; no conversion owed.
