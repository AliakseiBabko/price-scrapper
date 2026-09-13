---
source_type: video transcript (construction-AI consultancy channel, feature explainer with a demonstrated failure)
source_url: https://www.youtube.com/watch?v=LBN9xF_rs1w
video_id: LBN9xF_rs1w
transcript_file: _Archive/processed_sources/20260913_fairley_subagents_and_lost_in_the_middle_f5346496.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions - ORIGINAL language)
upload_date: 2026 (confirmed via yt-dlp metadata)
channel: Tim Fairley / @ConstructIQ - construction-AI consultancy, sells "Contractor OS"; Australia
source_title: "Why AI Struggles with Big Construction Documents - And How to Fix It (Claude Sub-Agents)"
language: en
extraction_taxonomy: custom (this project taxonomy, caller-defined mode - bucket `Digital Toolchain / AI Workflow`)
fact_yield: 8
promotional_ratio: medium
corroborates_existing: true
region: n/a_AU_market_no_jurisdictional_claim
delivery_model: n/a - not a renovation source
---

# Source Note - Tim Fairley: Sub-Agents, and "Lost in the Middle" (YouTube LBN9xF_rs1w)

## Evidence levels
(1) transcript text - (2) YouTube metadata - (3) contextual inference - (4) external validation (none performed).

## Why this source

**Tier 1 item of the [@ConstructIQ triage](../_Inbox/planning/constructiq_channel_triage_20260913.md), selected to extend the context-rot thread the vault already holds from `3tAYEJTyUFY`.** It does, and **it supplies one named mechanism the vault did not have.** **Eighth source from this practitioner - nothing here corroborates anything else of his.**

## ⚠️ A Task Category Worth Naming: "Data Reformatting"

**"A lot of construction work is just reading and reformatting information."** His cleanest example is **procurement**: the head contract, drawings and specifications state what must be built and to what requirements; procurement **extracts those requirements and reformats them into scope-of-works packages** per subcontractor. Worked instance: *"for the electrical works we have to install 23 light fittings, we need a defect liability of two years, and we have to provide shop drawings for approval."*

- **⚠️ The consequence he draws is the useful part: on a reformatting task, what decides the result is less the model's intelligence than "giving it all the relevant context in a format that it can read and use practically."**
- **→ Worth holding as a classifier for this project's own delegations**: a task that is *transport plus reformatting* is a good candidate; a task requiring judgement about what is missing is not. **Consistent with the "delegate transport, not judgement" rule from [[_Sources/YT_VrSs8mGI8ss_fairley_takeoff_to_priced_bid|VrSs8mGI8ss]]** - same speaker, so a consistent position rather than corroboration.

## ⚠️⚠️ The Two Mechanisms - and the second one is new to this vault

**He demonstrates the upload failure on camera** (an 11 MB drawing set refused, *"even though it was only a 10 MB file"*) and then makes the point that a folder-scoped harness solves the **upload limit** but not the real problem: **every query re-ingests the entire set.**

1. **Context-window overload** - *"as you increase the amount of information that you send to AI, you drastically decrease the quality and accuracy of the response."* **Already held in this vault as context rot.**
2. **⚠️⚠️ "LOST IN THE MIDDLE" - NEW HERE, and it is a positional failure rather than a volume one.** *"When you have more context, AI can more reliably read the stuff at the start and the finish, but it misses the stuff in the middle."*
   - **→ This is a different claim from context rot and has a different consequence: WHERE something sits in the context affects whether it is used, not just HOW MUCH context there is.**
   - **⚠️ Directly actionable for this project, which maintains long instruction files.** `AGENTS.md`, `CLAUDE.md` and the longer skill files all have middles. **If the effect is real, a critical rule buried mid-file is weaker than the same rule near either end** - which is an argument for the standing rules being numbered and front-loaded, and for the 300-line page target having a second justification nobody had stated.
   - **`single-account` and `unverified` here** - he names it as a known phenomenon without citing a source, and it was not independently checked. **Recorded as a named hypothesis to design against, not as a measured property.**

**Net effect of ignoring both**: *"you're ingesting a ton of tokens, so you're going to spend more, you're going to go through your usage much faster, and you're actually going to get worse results."*

## ⚠️⚠️ Sub-Agents - the Mechanism, Not Just the Practice

**He is explicit that this is COMPLEMENTARY to indexing documents into markdown, not a replacement** - the indexing strategy is already recorded in this vault from his other videos.

**What a sub-agent is: a separate instance with a FRESH CONTEXT WINDOW, given one specific defined task.**

- **⚠️⚠️ The property that matters: it does not pollute the main context window.** Only the prompt and **the returned markdown summary** land in the main thread - none of the retrieval workings, and none of the document it read. **The main thread, where a long-running complex task is being carried out, stays clean.**
- **They run in PARALLEL** - he shows two, then three, running at once - so results come back faster.
- **⚠️ The cost control, and it is the practical half: delegate sub-agents to a CHEAPER MODEL.** Keep the main thread on the strong model and send retrieval to a cheap one - *"searching and retrieving is fine to use a cheaper model for"* - citing roughly a six-to-seven-fold token price difference. His example: searching a 20-page contract for a clause does not need the expensive model.
- Minor friction noted: no slash command for it; you ask for it in the prompt.

**⚠️ This vault already records the practice** - "sub-agents that analyse each individual drawing, using a cheaper model like Haiku instead of Opus" - from `S77hdyyjTmA`. **Same speaker, so this is not corroboration; what is new here is the MECHANISM (fresh context window, no pollution of the parent) rather than the practice.**

## Confidence & Evidence Notes

- **`single-account`.** **Model names and price ratios are deliberately NOT routed** per the standing dating rule; the architecture is.
- **⚠️ Relevance is immediate rather than theoretical: this project's own sessions use sub-agents**, and the fresh-context-window property is the reason a delegated search returns a conclusion rather than a transcript of its reading.
- **ASR**: good. "Cohere"/"Co-work" inconsistent, "Opus 4.8" (`ASR-uncertain`, not routed).
- **No prices carried; no conversion owed. No regulatory content.**

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/AI_Workflow_Systems.md` (NEW PAGE)** - lost-in-the-middle, the sub-agent mechanism, cheap-model delegation, and the data-reformatting task classifier.
- **5b**: no prices; no conversion owed.
