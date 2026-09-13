# AI Workflow Systems

Detail page for [[18_Digital_Toolchain/Digital_Toolchain_Guide|Digital Toolchain]].

**Not how to get an agent to do one task — how to arrange context, skills and multiple agents so the results are reliable enough to rely on.** General practice, read against this project's own arrangement.

> [!WARNING]
> **⚠️⚠️ EVERY SOURCE ON THIS PAGE IS ONE PRACTITIONER** — Tim Fairley / @ConstructIQ, whose channel also supplied most of [[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]]. **Nine of his videos are now in this vault. Nothing here corroborates anything else of his, and his repeated claims across videos are one consistent position, not independent support.** The product funnel (Contractor OS, a paid skills library, one-on-one calls) is constant.
>
> **⚠️ Read the whole page with the concentration in mind.** Where a claim here matters, it needs a second, unrelated voice — and this page does not have one.

> [!IMPORTANT]
> **⚠️⚠️ The honest summary: most of this is VALIDATION AND VOCABULARY, not new capability.** A router file, a skill library with nested examples, a linked markdown wiki, sub-agents, git-backed shared context, human gatekeeping — **this repo already has all of it, several in a stronger form.** **Read it for the four genuinely new items, flagged ⚠️⚠️ below, and for the reassurance that the architecture was not accidental.**

## 1. ⚠️⚠️ Four failure modes of a standalone workflow

**The thesis: prompting is no longer the hard part. *"The true challenge… isn't getting AI to do a specific task. It's how do you integrate AI into an overall workflow."*** His worked case is an inspection-and-test plan — one prompt produced seven — and the question that follows is *"then what?"*: which folder, who checks it, how is it verified against the requirements, who reviews it.

**Even packaged as a named skill, a standalone workflow fails four ways:**

1. **It makes sense to you, not to your team.** The prerequisites and the template library live in your head.
2. **⚠️⚠️ The output is unreliable because nothing guarantees the INPUT CONTEXT or VERIFIES THE OUTPUT.** The question that exposes it: ***"Who's actually checking the results from it, and how are they checking it?"***
3. **⚠️⚠️ The output gets lost in a mountain of slop.** *"We could generate a thousand ITPs in a day, but that's probably not going to be useful. What we actually need is ONE high-quality ITP."* **You need a structured way to control what you STORE**, or you accumulate outputs nobody uses.
4. **⚠️⚠️ Undocumented process cannot be improved — he calls this the most important.** If the workflow was never mapped, then when the output is bad **it is impossible to work out what went wrong**, so there is nothing to fix.

> **⚠️⚠️ Failure mode 2 is `00_Master/Validator_Design_Discipline.md` arriving from outside** — that page holds that **printing is not checking** and **a gate nobody has watched fail is not a gate.** He reaches the same place and answers it with a dedicated step (§4).
>
> **⚠️ Failure mode 3 lands on a vault of ~813 extraction notes that has already repaired fragmentation across 29 pages.** *"One high-quality ITP, not a thousand"* is this project's own value filter and its `fact_yield` honesty, stated by someone else.
>
> **⚠️ Failure mode 4 is why `_Inbox/planning/` triage files exist here** — and why the round notes record what was *not* done, and why.

[source: [[_Sources/YT_sjcDHXReSNI_fairley_workflow_systems_failure_modes|YT_sjcDHXReSNI]]]

## 2. ⚠️⚠️ Why agentic harnesses break on documents — file versus line

**The best mechanism on this page.** Agentic harnesses — Claude Code, Cowork, Cursor, Antigravity — **all grew out of software engineering and were not designed for knowledge work.** Pointing them at folders of Word documents, spreadsheets and PDFs uses them against their design.

**Why git works on code:** many small plain-text files, deliberately structured, where **a change touches a few lines** — and thirty years of tooling built on that: diffs, branches, pull requests, per-line attribution, history.

> **⚠️⚠️ THE KEY INSIGHT: git works because THE UNIT IS A LINE. In knowledge work THE UNIT IS THE WHOLE FILE.** To read one row of a register the model ingests the entire workbook; to change one cell it must **rewrite the entire document.**

**Three consequences follow:** concurrent writes collide and you get two versions of one register with no way to tell which is right; folders fill with duplicates and stray files; **and every read is the whole file, so it is not token-efficient either.**

- **⚠️ He is careful that this predates agents** — *"if you've used SharePoint on construction projects, everyone runs into this."* Agents make an existing problem acute. **And he scopes it: *"if you've only got two people working in the same folder, it's probably not a big issue."***
- **⚠️ The naive fix fails twice**: cloud files are hydrated on demand, and forcing local sync produced *"weird file errors… I would create a file and then it suddenly wouldn't exist"*; and it does nothing about scope — *"if you open Claude in the root of your project folder, you're basically giving it access to absolutely everything."*

**His proposed architecture — stated as provisional, and he publicly retracts his own earlier advice**: each person's harness open in a **local folder** with only what the task needs · **shared context in a GIT REPOSITORY** reached over MCP, because *"it's a very token efficient way for AI to read and access information"* · **live registers in a DATABASE, not a spreadsheet**, optionally read-only · static documents copied locally · **the human as gatekeeper** of what gets published.

> [!IMPORTANT]
> **⚠️⚠️ THIS PROJECT IS ALREADY ON THAT ARCHITECTURE, AND LARGELY BY DEFAULT RATHER THAN BY DECISION — which is worth knowing.** Shared context in a git repository ✓. **Plain-text and CSV rather than Excel ✓ — so changes ARE line-level diffs and git IS the concurrency control**, the exact property he identifies as missing from knowledge work. Human gatekeeping ✓, and **stronger than his: deterministic gates (`check_dxf_closure.py`, `verify_batch.py`) rather than a person eyeballing output.**
>
> **⚠️ One deliberate divergence worth recording rather than following: he routes live registers to a DATABASE; this project keeps them as CSV in git.** For many concurrent writers a database is right. **For one person with version control, CSV-in-git diffs, reviews and reverts, and needs no second system.** A fork in the road, not a correction.
>
> **⚠️ And the scale caveat applies: this project is one person, so the collision problem is small — but not zero.** A real two-instance collision is already recorded in this vault's agent-behaviour memory. **This source is the root-cause analysis for it.**

[source: [[_Sources/YT_wgcOBhejKvo_fairley_agent_collision_and_git_for_knowledge_work|YT_wgcOBhejKvo]]]

## 3. Context, in levels — and the two that matter here

**The organising economics: *"AI has amnesia"*, so context must be re-supplied every time — and *"it almost becomes easier to do it yourself than to assemble the necessary context to get AI to perform the task well."* Every level exists to amortise that.**

- **⚠️ A bad review is a context failure, not a model failure.** Ask for a contract review and it flags 30 clauses, half useful — over-weighting liquidated damages where the programme has float, missing a security requirement's cash-flow impact. *"This is not an example of AI is bad. It's an example of AI not having the correct context."*
- **Chat → project with a retrieval store → skills → folder-scoped harness → router file → project memory → a linked markdown wiki.** He names the top layers *"a very fancy way of saying create a library of a Wikipedia of markdown files"*, viewed in Obsidian.

### ⚠️⚠️ Skills solve two problems, and the second compounds

1. **Output variability** — the same task gives a slightly different answer each time, *"which makes reviewing it and checking it annoying."*
2. **⚠️⚠️ Repeated re-correction** — *"every time you ask it to do that same task, you have to give it the same incremental improvements. With a skill, you do that once."*

> **→ A skill is the place to put a correction so you only make it once.** ⚠️ **That is exactly why this repo's skill files carry incident-dated rules** — *"added 2026-08-17, after a real dispatch stalled this way"*. **The dates are the corrections, accumulated.**

### ⚠️ The router file, described almost exactly as `AGENTS.md`

A markdown file at the top of the directory carrying **a project summary, a map of the folders and where each kind of file lives, and the current status** — *"like an auto-updating system prompt."* Effect: asked to review a contract, the agent already knows where the contract is. **Result: faster responses, far fewer tokens.**

- **⚠️ An independent arrival at the pattern this repo already uses.** `AGENTS.md` opens *"Read this first. It is a router, not a manual."*
- **⚠️ But this project splits the "current status" element OUT, and that looks like the better call: a status section inside a router goes stale silently; `project_decisions.md` and the `V0_*` pages have their own change logs.**

[source: [[_Sources/YT_8aSYNMXk33A_fairley_eight_levels_of_context|YT_8aSYNMXk33A]]]

## 4. ⚠️⚠️ The four genuinely new items

**Everything above is largely confirmatory. These four are not.**

1. **⚠️⚠️ "Lost in the middle" — a positional failure, distinct from context rot.** *"When you have more context, AI can more reliably read the stuff at the start and the finish, but it misses the stuff in the middle."*
   **→ WHERE something sits in the context affects whether it is used, not just HOW MUCH context there is.** **Directly actionable here**: `AGENTS.md`, `CLAUDE.md` and the longer skill files all have middles. **If the effect is real, a critical rule buried mid-file is weaker than the same rule near either end** — an argument for numbered, front-loaded standing rules, and **a second justification for the 300-line page target that nobody had stated.** `single-account`, `unverified`, named without a citation — **treat as a hypothesis to design against, not a measured property.**
2. **⚠️⚠️ Completeness checking works against a baseline and fails without one.** Asked cold whether anything was missing from a commissioning estimate, it returned **~50 recommendations, mostly items already covered elsewhere** — false positives at scale, because it could not model what was already handled. **The same task with the human's first cut supplied — "it's actually checking what I've already done" — works, because the comparison is bounded.**
   **→ Open-ended "is anything missing?" is unreliable; "check MY draft against the source" is not.** *(Independent instance of the failure [[_Sources/YT_VcBohP2LbNM_aicontractor_flag_not_verify|VcBohP2LbNM]]'s prompt rule guards against — and that one IS a different practitioner.)*
3. **⚠️⚠️ A "skeptic" step — an independent check of a previous step's deliverables, verifying they are comprehensive.** A named role in the pipeline whose only job is to doubt the previous output. **This project's deterministic gates are the stronger form of the same idea.**
4. **⚠️ Sub-agents, with the mechanism rather than the practice: a separate instance with a FRESH context window, whose retrieval workings never enter the parent thread** — only the prompt and the returned summary do. **They run in parallel**, and **retrieval can be delegated to a cheaper model** while the main thread stays on the strong one. *(The practice was already recorded; the no-pollution mechanism is what is new.)*

[sources: [[_Sources/YT_LBN9xF_rs1w_fairley_subagents_and_lost_in_the_middle|YT_LBN9xF_rs1w]], [[_Sources/YT_VrSs8mGI8ss_fairley_takeoff_to_priced_bid|YT_VrSs8mGI8ss]], [[_Sources/YT_sjcDHXReSNI_fairley_workflow_systems_failure_modes|YT_sjcDHXReSNI]]]

## 5. What to delegate

- **⚠️⚠️ "Delegate transport, not judgement."** *"We're simply using it to do the time-consuming moving of data from one spreadsheet into another… we're not relying on it to do complex judgment and reasoning. It's always just moving information around."*
- **A task classifier that follows: "data reformatting"** — reading information and re-expressing it in another format — is a good delegation. **A task requiring judgement about what is ABSENT is not** (§4.2).
- **You can only delegate a process you could perform yourself.** *"The only way you can actually do that is by having a deep understanding of the project and the process yourself"* — and the payoff is instrumental: *"once you build that knowledge for yourself, it is going to be a thousand times easier to STEER it."*
- **The four-part instruction**: narrowly define the task · supply the background it needs · define the process to follow · specify the output template.
- **⚠️ End prompts with *"ask any clarifying questions if you're unsure."*** Explicitly granting permission to come back. **The clarify-first pattern — note three of its five appearances in this source class are this same channel, so roughly three independent voices, not five.**

## Related

- [[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]] — the same practitioner on drawings specifically, with the measured benchmark.
- [[18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join|Quantity Take-Off and the Cost Join]] — his estimating workflow's rate-flagging gate and assembly-library method.
- [[18_Digital_Toolchain/analysis/Agent_Connected_CAD|Agent-Connected CAD]] — session-scoped execution permission and the silently-supplied-values rule.
- `00_Master/Validator_Design_Discipline.md` — this project's own answer to §1's failure mode 2.
