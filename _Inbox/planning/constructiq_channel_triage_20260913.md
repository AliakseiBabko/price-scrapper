# @ConstructIQ — channel triage, 2026-09-13

**411 videos. 4 already processed. 407 fresh.** Preflight manifest: [`preflight_20260913T173248Z.json`](preflight_20260913T173248Z.json). **Nothing processed; one transcript spot-checked.**

## 1. ⚠️⚠️ This is not a new channel — it is Tim Fairley's, and the vault is already built on it

**All four duplicates are sources already in the vault**: `3tAYEJTyUFY` (2026-09-11), and `_k1jQBS4Nk8`, `ItW-ielFvGg`, `S77hdyyjTmA` (2026-09-13 Round 1). **@ConstructIQ is the channel behind the single most-cited practitioner in [[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]]** — a page whose own opening warning reads:

> *"The whole of this page's measured content comes from ONE practitioner… Repeated claims across his videos are one consistent stated position, not independent corroboration. His benchmark is self-constructed, self-administered and self-scored against his own product."*

**→ That warning is the governing fact of this triage. 407 more videos from this voice cannot corroborate anything the vault already holds from it.** Processing heavily here deepens a monoculture rather than broadening the evidence base — and the product funnel (Contractor OS, paid Claude skills, one-on-one setup calls) is the same throughout.

**⚠️ Consequence for routing: nothing from this channel may be recorded as confirming anything else from this channel.** Where a Fairley claim needs corroboration, it has to come from somewhere else.

## 2. What the channel actually contains

Keyword counts across all 411 titles: **estimating 69 · contracts 54 · Claude 47 · cost 34 · scheduling 30 · take-off 25 · drawings 19 · skills 18 · quantities 17**.

Three distinct bodies, with very different relevance:

| Body | Size | Relevance to this project |
| :--- | :--- | :--- |
| **A. AI workflow & systems** — Claude Skills, agents, MCP, sub-agents, knowledge bases, context engineering, plugins, Claude Code | ~44 | **⭐ High, and unexpectedly so.** Several describe an architecture close to this repo's own |
| **B. Professional estimating library** — per-trade take-offs (civil, electrical, plumbing, HVAC, concrete/rebar, earthworks, MEP, steel), bidding, overhead recovery, plant costs | ~95 | **⚠️ Low.** A course for commercial estimators. A self-managed single-flat renovation has no plant mobilisation, no preliminaries recovery, no bid, and no tender |
| **C. Career / lecture / soft-skills** — CVs, "Lecture 10/18: The Perfect Construction Project", "top skills" lists | ~40+ | **✗ None** |

### ⚠️⚠️ A severe re-record pattern, which changes the arithmetic

**The channel remakes its own videos.** Counted from titles alone:

- **4×** "How to Build a Construction Project Knowledge Base with Claude" (`jhGMhemMLEI`, `1hnVaybcMfk`, `u_f43RjQftA`, `_3uEZcvUKaA`)
- **5×** "Claude Skills / Cowork for Construction — Estimating, Contracts, Scheduling" (`5iImqMMGjkI`, `DOK999l5Pqg`, `6mKMTs1M7S4`, `qfKpwBaSXFM`, `KjO1q_TyoDc`)
- **4×** "AI for Estimating — what works, what doesn't" (`aSKEdBADarM`, `qzXVm2bXndk`, `tbNNRL6s6j0`, `bd3S_0WZjv0`)
- **3×** "Build your own AI Construction Estimator" (`jCedUrbENnY`, `-ZfwmItC9o0`, `ymWwEZF3RJo`)
- Many "Master X in N minutes" / "Complete Step-by-Step Guide" pairs per trade

**→ The value filter's script-reuse rule applies hard: pick ONE per cluster, the most recent or the longest, and treat the rest as the same video.** The effective fresh count is far below 407.

## 3. ⚠️ The spot-check — and it passed decisively

**`sjcDHXReSNI` — "I've built over 100 AI workflows for Construction — Here's what's actually hard"** was fetched and read, on the reasoning that a *what's-actually-hard retrospective* is the highest-value format available and the cheapest test of whether this channel adds mechanism beyond the four drawings videos already held.

**It does, and in a direction the vault does not yet cover.** Its thesis: prompting and building a single workflow is no longer the hard part — **integrating one into a system is.** Contents include:

- **Four named failure modes of a standalone skill**, of which two land directly on this repo's own concerns: **output is unreliable without a structured way to guarantee input context and to verify output** — *"who's actually checking the results from it and how are they checking it?"* — and **unless the process is documented you cannot work out what went wrong**, so you cannot improve it.
- **⚠️⚠️ "The output will get lost in a mountain of slop."** One prompt produced seven inspection-and-test plans and eight check sheets. *"We could generate a thousand ITPs in a day… What we actually need is ONE high-quality ITP."* **Directly relevant to a vault holding ~813 extraction notes that has already had to repair fragmentation across 29 pages.**
- **A "skeptic" step type — an independent check of a previous step's deliverables, verifying they are comprehensive.** **This is `00_Master/Validator_Design_Discipline.md`'s position arriving from outside** — *printing is not checking*, and *a gate nobody has watched fail is not a gate*.
- **"State" as the one useful term from the buzzword** — context *plus what the system has produced so far*, carried between steps — and **"the state of the system in construction is fundamentally your project folder"**, with the harness opened inside it. **Project context (the folder) versus business context (across projects).**
- He is appropriately sceptical of the jargon he is relaying: *"I don't know why they're calling it graph engineering. It's basically just… how do we build systems that actually produce useful work."*

**Status**: fetched, **not extracted**. Logged in `processed_sources.csv` as `inbox` so it is not re-fetched. **It is Tier 1 item 1 when a round is run.**

## 4. Verdicts

### ⭐ Tier 1 — process in a Round 1 (5 videos)

**All from body A, chosen because they promise FAILURE MODES or ARCHITECTURE rather than capability — and because they bear on how this project itself works.**

| ID | Title | Why |
| :--- | :--- | :--- |
| **`sjcDHXReSNI`** | I've built over 100 AI workflows — here's what's actually hard | ⭐ **Already spot-checked and confirmed.** Four failure modes, the slop problem, the skeptic step, state-as-project-folder |
| **`wgcOBhejKvo`** | I Run Multiple AI Agents at Once — Here's How I Stop Them Colliding | ⭐ **This repo has a recorded incident of exactly this** (a paused subagent self-resuming and two instances writing concurrently). An outside account of the same failure is worth having |
| **`LBN9xF_rs1w`** | Why AI Struggles with Big Construction Documents — And How to Fix It (Claude Sub-Agents) | Extends the context-rot thread already held from `3tAYEJTyUFY`, with a named mechanism this vault does not have |
| **`8aSYNMXk33A`** | Claude Context for Construction — System Prompts, Skills and Structured Data | **The closest title on the channel to this repo's own architecture** — skills plus structured data plus system prompts |
| **`VrSs8mGI8ss`** | How to Estimate a Construction Project with Claude AI — Take-Off to Priced Bid | ⭐ **The quantity→price join end to end — the one genuinely absent tool** per [`toolchain_gap_analysis_20260908.md`](toolchain_gap_analysis_20260908.md) §B |

### Tier 2 — conditional, a Round 2 at most (4)

| ID | Title | Condition |
| :--- | :--- | :--- |
| `IqfrXoiM4bE` | How to Build an AI Quantity Take-Off Tool — Step-by-Step | Only if a take-off tool is actually going to be built. **The gap analysis's verdict is "three small scripts over data we already hold", not a new tool** |
| `rrUqIdAMzbU` | AI Quantity Take-offs — Actually Worth Using? | The sceptical treatment of a claim already held in short form (*"they don't really work that well"*). Read only if that claim is challenged |
| `6wZRV7Nfees` | Self-Improving Construction Knowledge Base (Memory System) | ⚠️ Interesting but **likely overlaps `sjcDHXReSNI` heavily** — read only after it, and only if it did not cover memory |
| `A2ApRlxFezA` | Construction Overhead Costs — Preliminaries, Recurring and Non-Recurring | The one cost-decomposition title with a category this project's budgeting pages may genuinely under-cover. **⚠️ Commercial-contractor framing; expect most of it not to apply** |

### ✗ Tier 3 — skip, and the reasons are structural

- **The entire per-trade estimating library (~95).** Civil, earthworks, plant mobilisation and financing, formwork/rebar, MEP, bidding, overhead recovery, profit protection, tendering. **This project has no bid, no tender, no plant, no preliminaries and no subcontract chain** — and every figure is AU/UK market, uncomparable under standing rule 2. **The take-off METHOD this project needs is already held**, from `S77hdyyjTmA` and from Vasily_Sanuzel's cutting plan.
- **All career, lecture-series and soft-skills content (~40+).** No renovation or toolchain content.
- **All tool roundups and "best software" videos.** Capability verdicts date within months — the standing rule from 2026-09-11.
- **Every re-record beyond the one chosen per cluster** (§2).
- **⚠️ Contract-management content (54 titles) is skipped for an additional reason: it is jurisdiction-specific.** Australian/UK contract practice is a different country's law. **Standing rule 4 — none of it goes to `16_Legal_and_Regulations/`, and this project is self-managed with no main contract to administer.**

## 5. Recommendation

**Run Tier 1 as a 5-video round, and stop there unless it earns more.** Expected shape: the workflow/systems material routes to `18_Digital_Toolchain/`, and `VrSs8mGI8ss` to `Quantity_Takeoff_and_Cost_Join.md`.

**⚠️⚠️ Two standing constraints on whatever gets processed:**

1. **Nothing from this channel corroborates anything else from this channel.** Six sources from one voice is already a concentration worth flagging on every page that cites it.
2. **The product funnel is constant.** Contractor OS, paid Claude skills, unlimited one-on-one calls. **Route mechanisms; discard the tooling verdicts and the model names**, exactly as the four already-processed videos were handled.

**Do not open the estimating library.** It is the largest part of the channel and the smallest part of its value to this project — and that asymmetry is the single most useful output of this triage.
