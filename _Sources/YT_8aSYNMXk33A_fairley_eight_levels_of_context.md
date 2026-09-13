---
source_type: video transcript (construction-AI consultancy channel, structured explainer with a product funnel)
source_url: https://www.youtube.com/watch?v=8aSYNMXk33A
video_id: 8aSYNMXk33A
transcript_file: _Archive/processed_sources/20260913_fairley_eight_levels_of_context_f5b23962.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions — ORIGINAL language)
upload_date: 2026 (confirmed via yt-dlp metadata)
channel: Tim Fairley / @ConstructIQ — construction-AI consultancy, sells "Contractor OS"; Australia
source_title: "Claude Context for Construction – System Prompts, Skills and Structured Data"
language: en
extraction_taxonomy: custom (this project's taxonomy, caller-defined mode — bucket `Digital Toolchain / AI Workflow`)
fact_yield: 12
promotional_ratio: medium
corroborates_existing: true
region: n/a_AU_market_no_jurisdictional_claim
delivery_model: n/a — not a renovation source
---

# Source Note — Tim Fairley: Eight Levels of Context, and a Description of This Repo (YouTube 8aSYNMXk33A)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Why this source

**Tier 1 item of the [@ConstructIQ triage](../_Inbox/planning/constructiq_channel_triage_20260913.md), selected as the closest title on a 411-video channel to this repo's own architecture.** It is closer than expected: **by level 8 he is describing a linked markdown wiki with a router file, a skill library and folder-scoped agents — which is this vault.** **Ninth source from this practitioner; nothing here corroborates anything else of his.**

## ⚠️⚠️ The Reframe — a bad review is a context failure, not a model failure

**His opening case: ask AI to review a contract and it flags 30 clauses, half of them useful.** It over-weights liquidated damages when the programme has float, and misses the cash-flow impact of a 15% security requirement.

> *"None of this is an example of AI is bad. It's an example of AI not having the correct context to complete the task."*

- **⚠️ This is the same failure as his battery-project case in [[_Sources/YT_VrSs8mGI8ss_fairley_takeoff_to_priced_bid|VrSs8mGI8ss]]** — ~50 recommendations, mostly already covered elsewhere. **Same speaker, two different diagnoses of one failure, and they are complementary rather than competing: there the fix is ordering (do the first cut yourself, then have it check YOUR work); here the fix is supply (give it what it needs to know).** Worth holding both.
- **The context inventory he lists for ONE task** — writing a trade scope of works — is the useful concreteness: the company template and format, how the company packages and splits trades, the standard procurement register, the background-document list, the head-contract scope and specifications, the drawings, **which items are provisional sums versus lump sum versus schedule of rates**, and standard inclusions and exclusions.
- **His analogy**: asking without that is like hiring a new contracts administrator and then criticising them for not knowing *"that you usually get the civil contractor to do the underground conduits."*
- **⚠️⚠️ And the economics, which is the point of the whole video: "AI has amnesia"** — told once in one chat, it does not know in the next — **so *"it almost becomes easier to do it yourself than to assemble the necessary context to get AI to perform the task well."*** **Every level below exists to amortise the cost of assembling context.**

**⚠️ One free technique worth keeping: end prompts with *"Ask any clarifying questions if you're unsure."*** — explicitly granting the model permission to come back for more information. **The clarify-first pattern again; note that three of its five appearances in this source class are this same channel, so it is roughly three independent voices, not five.**

## The Levels

| Level | What it is | What it buys, and what it does not |
| :--- | :--- | :--- |
| **1. Plain chat** | Ask a question | *"Like an enhanced Google search."* Starts from scratch every time; scaling means ever-larger prompts and attachments |
| **2. Chat inside a project** | Documents uploaded once into a retrieval store; every chat in the project can pull from them | Removes re-uploading. **⚠️ He rates NotebookLM the best retriever he has used — it answers only from citations referencing the source documents, and is multimodal enough to read drawings well** |
| **⚠️ 3. Skills** | *"Projects are great for STATIC DATA but not for WORKFLOWS."* A skill is a set of instructions **with nested examples**, able to store code; you define the exact process, supply many examples of structure, and specify the output format | See below — the two problems it solves |
| **4. Folder-scoped harness** | Open the agent in a desktop folder; read/write every file in it, **with the skill library still available** | **⚠️ Two named costs: a huge token burn — every PDF is converted to text on every read — and *"it decreases the accuracy and speed at which you get results"*** |
| **⚠️⚠️ 5. A `CLAUDE.md` router** | See below | The fix for level 4's cost |
| **6. Harness project with memory** | Static documents in a retrieval store inside the project; **persistent memory between conversations**, which removes the need to hand-update the router; system instructions at project level | **Registers and anything frequently updated stay in the folder** and are read as needed |
| **7–8. "Operating system"** | *"A very fancy way of saying create a library of… a Wikipedia of markdown files"* with links between them, viewed in **Obsidian** — *"a second brain… structured almost Wikipedia pages"* | Personal and business layers above the project |

### ⚠️⚠️ Skills solve two specific problems, and the second is the one that compounds

1. **Output variability** — *"every time you ask it to do the same task, it'll give you a slightly different output, which makes reviewing it and checking it annoying."*
2. **⚠️⚠️ Repeated re-correction** — *"every time you ask it to do that same task, you have to give it the same incremental improvements. With a skill, you do that once, you store those instructions."* And they improve with use: *"the more you use these skills, the more you iterate… the better they get."*

> **→ A skill is the place to put a correction so you only have to make it once.** ⚠️ **That is precisely why this repo's own skill files carry incident-dated rules** — *"added 2026-08-17, after a real dispatch stalled this way"* — rather than generic advice. **The dates are the corrections, accumulated.**

### ⚠️⚠️ Level 5 — the router file, described almost exactly as `AGENTS.md`

**A markdown file at the top of the project directory containing: a project summary and background · a layout of the folders and where to find each kind of file · the current status of the project.**

> *"It's like an AUTO-UPDATING SYSTEM PROMPT — every time it does something new, it documents it in `claude.md`. It keeps up to date with your files, the structure of it."*

**The effect he names**: asked to review a contract, the agent already knows the contract sits in the tender-and-contract documents and what that document contains. **Result: much faster responses and far fewer tokens.** Created by asking the agent to write it when the folder is first set up.

- **⚠️⚠️ This is an independent arrival at the router pattern this repo already uses.** `AGENTS.md` opens *"Read this first. It is a router, not a manual: it tells you what this repo is and where the real instructions live."* **Same artefact, same justification, reached separately.**
- **⚠️ And this project splits the "current status" element out rather than folding it in** — `00_Master/project_decisions.md` and the `V0_*` status pages carry it. **Worth noting as a deliberate divergence: a status section inside a router file goes stale silently; a status page has its own change log.**

## Confidence & Evidence Notes

- **`single-account`**, a structured explainer with no measurement. **`promotional_ratio: medium`** — Contractor OS and its skill library are pitched, **but the whole ladder is given away and the levels are tool-agnostic.**
- **⚠️⚠️ The honest summary of this source's value to this project: it is largely VALIDATION plus VOCABULARY, not new capability.** Levels 3, 5, 7 and 8 describe a skill library with nested examples, a router file, and a linked markdown wiki — **all of which this vault already has, and several of which it has in a stronger form** (deterministic gates rather than human review; a page-size gate; change logs per page).
- **The genuinely new items are small but real**: the two-problems-skills-solve framing, the auto-updating-router idea, the NotebookLM citation-only retrieval note, and the cost argument that assembling context can exceed the cost of doing the task.
- **⚠️ Product and tool names are NOT routed** per the standing dating rule; the levels and the mechanisms are.
- **ASR**: adequate. "Clowd"/"Coda Work"/"Coda X"/"Anti-Gravity" throughout; "clowd.md" for `CLAUDE.md`.
- **No prices; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/AI_Workflow_Systems.md` (NEW PAGE)** — the context-failure reframe, the levels ladder, the two problems skills solve, and the router-file pattern.
- **5b**: no prices; no conversion owed.
