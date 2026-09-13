---
source_type: video transcript (construction-AI consultancy channel, openly provisional architecture revision)
source_url: https://www.youtube.com/watch?v=wgcOBhejKvo
video_id: wgcOBhejKvo
transcript_file: _Archive/processed_sources/20260913_fairley_agent_collision_and_git_for_knowledge_work_78af7feb.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions - ORIGINAL language)
upload_date: 2026 (confirmed via yt-dlp metadata)
channel: Tim Fairley / @ConstructIQ - construction-AI consultancy, sells "Contractor OS"; Australia
source_title: "I Run Multiple AI Agents at Once for Construction - Here's How I Stop Them Colliding"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 12
promotional_ratio: low
corroborates_existing: true
region: n/a_AU_market_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Tim Fairley: Why Agentic Harnesses Break on Knowledge Work, and Git as the Answer (YouTube wgcOBhejKvo)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this source, and an unusual amount of intellectual honesty

**Tier 1 item of the [@ConstructIQ triage](../_Inbox/planning/constructiq_channel_triage_20260913.md), chosen because this repo has its OWN recorded incident of exactly this failure** - a paused sub-agent self-resuming so that two instances wrote concurrently.

**`promotional_ratio: low`, and unusually so for this channel.** Almost nothing is sold. **He states the video is provisional, invites correction, and publicly revises his own earlier recommendation**: *"exploring some of these problems has made me rethink my ideas around how to set up an AI operating system for construction. Some of the recommendations I've made haven't properly addressed this question."* **A practitioner retracting his own published architecture is the strongest form this channel offers.**

**⚠️ Seventh source from this practitioner. Nothing here corroborates anything else of his.**

## ⚠️⚠️ The Root Cause - Why These Tools Break on Documents

**The best analysis in the source, and it is a mechanism rather than a complaint.**

**Agentic harnesses - he names Claude Code, Cowork, Cursor, Antigravity - all grew out of software engineering. "They weren't designed for knowledge work."** Pointing them at folders of Word documents, Excel files and PDF drawings is using them against their design.

**What code looks like, and why git works on it:**

- Many **small plain-text files**, a couple of hundred lines each, **deliberately structured** - *"software engineers actually put in a lot of time and effort into organising their code base for this exact reason."*
- **A change touches a few lines.**
- Git is **"30 years of knowledge and principles of how two people can change and manage things in the same way, track revisions and solve these workflow orchestration problems"** - diffs, branches, pull requests, per-line attribution, history.

**⚠️⚠️ THE KEY INSIGHT: git works because THE UNIT IS A LINE. In knowledge work THE UNIT IS THE WHOLE FILE.**

> To read one quality lot, the model must ingest **the entire Excel workbook**. To change one status from "NCR raised" to "NCR closed", it must **rewrite the entire document.**

**Three consequences follow directly:**

1. **Concurrent writes collide.** Two agents - or an agent and a person with the file open - both write, and you get two versions of the same register with no way to tell which is correct.
2. **Folders fill with duplicates** and stray markdown files.
3. **⚠️ It is not token-efficient either** - every read is the whole file.

- **⚠️ He is careful that this is not an AI problem**: *"If you've used Microsoft SharePoint on construction projects, everyone runs into this problem. It is an absolute nightmare."* **Agents make an existing problem acute rather than creating a new one.**
- **⚠️ And he scopes it honestly: "If you have a very small company, you've only got two people working in the same folder, it's probably not a big issue."**

## ⚠️ Why the Obvious Architecture Fails - his own earlier advice, retracted

**The naive setup** - shared SharePoint/Drive folder, synced locally, agent harness opened in it - **fails for two reasons he names from experience:**

- **Cloud files are not actually on your computer.** They are hydrated on demand. Forcing always-local sync produced *"all these weird file errors and I would create a file and then it suddenly wouldn't exist."* He turned it off and the problems went away. **"I don't think the local file streaming is as clean as Google Drive and SharePoint make it out to be."**
- **⚠️⚠️ It does nothing about scope of access**: *"If you open Claude in the root of your project folder, you're basically giving Claude access to absolutely everything."*

## ⚠️⚠️ His Proposed Architecture - explicitly provisional

**He says twice that he has not stress-tested it.** Recorded as a proposal, not a finding:

1. **Each person opens the agent harness in a LOCAL folder** containing only what their task needs.
2. **⚠️⚠️ The shared project context lives in a GIT REPOSITORY**, reached through the GitHub MCP rather than through a synced drive. His stated reason beyond version control: **"GitHub... it's a very token efficient way for AI to read and access information."**
3. **⚠️⚠️ Registers and live data go in a DATABASE, not a spreadsheet** - variation register, RFI register, payment claims, cost tracking, production and quality data - in Airtable, Supabase or similar, connected to the agent, **optionally read-only so it cannot write.** *"Databases have solved this problem of how to access information and for different people to update at the same time."*
4. **Static documents** (head contract, drawings, specifications) are copied into the local folder.
5. **⚠️ The human is the gatekeeper**: the agent produces the artefact, **the person is the quality control**, and the person uploads it; the sync then refreshes the markdown representations in the repository.

## ⚠️⚠️ Confidence & Evidence Notes - and why this lands hard here

- **`single-account`**, self-described as in-progress, with an open request for better ideas.
- **⚠️⚠️ THE STRIKING THING IS THAT THIS PROJECT IS ALREADY ON THE ARCHITECTURE HE IS REACHING FOR, AND ARRIVED THERE BY DEFAULT RATHER THAN BY DECISION.** Point by point:
  - **Shared context in a git repository** - this vault is one.
  - **Plain text and CSV rather than Excel** - `data/canonical/` is CSV, so **changes are line-level diffs and git IS the concurrency control**, which is exactly the property he identifies as missing from knowledge work.
  - **Human gatekeeping** - and stronger than his, because this project has **deterministic gates** (`check_dxf_closure.py`, `verify_batch.py`) rather than a person eyeballing the output.
  - **Agent scoped to a folder** rather than to an entire drive.
- **⚠️ Where the advice DIVERGES and the divergence is defensible: he routes live registers to a DATABASE; this project keeps them as CSV in git.** For many concurrent writers a database is right. **For one person with version control, CSV-in-git is better** - it diffs, it reviews, it reverts, and it needs no second system. **Worth recording as a fork in the road rather than as advice to follow.**
- **⚠️ The scale caveat applies directly: this project is one person, so the collision problem is small here** - but **not zero**, since a real two-instance collision is already recorded in this vault's own agent-behaviour memory. **This source supplies the root-cause analysis for that incident.**
- **ASR**: good. "anti-gravity" for Antigravity, "githubs", "Cohere" for Cowork.
- **No prices; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/AI_Workflow_Systems.md` (NEW PAGE)** - the file-versus-line root cause, the failure of the synced-folder architecture, the proposed architecture, and the CSV-in-git versus database fork.
- **5b**: no prices; no conversion owed.
