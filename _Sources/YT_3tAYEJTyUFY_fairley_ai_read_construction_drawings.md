---
source_type: video transcript (practitioner demonstrating agent context management over a drawing set — processed for the PATTERN, not the model verdicts)
source_url: https://www.youtube.com/watch?v=3tAYEJTyUFY
video_id: 3tAYEJTyUFY
transcript_file: _Archive/processed_sources/20260911_fairley_get_ai_to_read_construction_drawings_13eb79da.txt
fetched: 2026-09-11 (anonymous, yt-dlp --write-auto-subs --sub-langs en-orig)
upload_date: 2026-04-29 (confirmed via yt-dlp metadata)
duration: 14:43
channel: Tim Fairley
source_metadata_location: not stated; construction-industry context, English-speaking market
jurisdiction: n/a — no regulatory claim
language: en (en-orig auto-generated; heavy product-name corruption, see warning)
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 5
promotional_ratio: low
corroborates_existing: true (validates this repo's canonical-data architecture rather than teaching it)
---

# Extraction Note — Tim Fairley: "How to Get AI to Read Construction Drawings" (YouTube 3tAYEJTyUFY)

## Evidence levels

(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

**Selected as the batch's most promising item, because reading printed dimension strings off a drawing is this project's live blocker.** It turned out **not to be about that at all** — and the mismatch is the most useful thing in it.

> [!WARNING]
> **⚠️ ASR product-name corruption is severe in this transcript and no product or model name from it can be quoted.** It renders "Claude Code" as **"Cowerk"** throughout, and gives a model version that cannot be taken at face value. **Every capability verdict here is also dated 2026-04-29 and was deliberately discarded** — capability claims date faster than anything else this vault handles.

## Value-filter verdict

**Partial extraction — the pattern and the failure demonstrations only.** Model rankings, product names and versions all excluded.

## Design Concept — ⚠️⚠️ what it actually demonstrates: the naive paths fail

He shows three failures on camera rather than asserting them, which is why they are worth recording:

1. **Direct chat upload of a ~10 MB, 25-drawing set fails.** *"Failed to upload drawings. This format may not be supported or the files are corrupted."* His observation is the useful part: *"if you look at the docs, you should be able to upload 10 megabytes… on paper it works, but if you actually try to upload it to the chat, it will not work."*
2. **A project/RAG upload of the same files fails the same way.** *"The chat and projects don't work."*
3. **A folder-scoped desktop agent "works" but at ruinous cost**: it *"will again try to take that whole set of PDF documents and jam it into the context window, and it's going to use around 30 times the number of tokens"* — enough, he says, to exhaust a pro subscription on a single drawing set — **and it answers less accurately for the same reason.**

**His name for the underlying cause: context rot** — *"the more information we give AI, the less likely it is to answer accurately."*

## Design Concept — the pattern, and the analogy that makes it stick

**His fix: summarise each drawing into a row of a structured store, then query the store instead of the drawings.** The analogy is the clearest statement of the principle in either batch:

> *"It's like giving someone a set of 30 or 100 drawings and saying 'what is the height of the retaining wall?' versus giving someone the retaining wall drawing and telling them this is the height of the retaining wall. So it's basically a way of condensing and creating context."*

> [!IMPORTANT]
> **⚠️⚠️ THIS PROJECT ALREADY DOES THIS, AND MORE STRICTLY — so the finding is validation of the architecture, not instruction.**
>
> `data/canonical/*.csv` **is** the condensed queryable store, and this project goes a step further: **the drawings are GENERATED from it rather than queried alongside it**, so there is no second copy to drift. And `00_Master/Evidence_Reading_Discipline.md` plus `tools/layout/vector_extent_oracle.py` demand **provenance for each extracted figure** — which his summary rows do not carry.
>
> **Worth stating plainly given the owner's "are we reinventing the wheel" question: on this axis the project is ahead of the practice in the video, not behind it.**

**What genuinely transfers, and it is small but actionable:**

- **The one-row-per-drawing summary as an explicit artefact**, queried by an agent over MCP. This project has canonical *data* but no per-drawing index of what each sheet carries — which is a different thing, and closer to the album's own contents page.
- ⚠️ **A spreadsheet is a poor store for this because the whole sheet lands in context** — *"when Claude reads Excel, it jams the whole Excel document into the context window"* — whereas a queried database does not. **Relevant to us: our canonical layer is CSV, which has the same property when read whole.** A query interface over it, rather than reading the files, would be the equivalent improvement.
- He built it in **Google Antigravity**, which this project already runs as one of its three agents (see `AGENTS.md`), so the path needs no new tooling.

## Mistakes / Warnings

- **Documented capability ≠ actual capability.** His upload-limit observation is the general lesson: a documented limit and an observed limit differed, and only the observation mattered. **Consistent with this repo's own standing warning that an agent's self-report is not evidence** — verified behaviour is.
- ⚠️ He is explicit that he is mid-experiment: *"I'm still in the early stages of experimenting with exactly how to build this."* **Recorded as a direction, not a finished method.**

## Unclear / Needs Confirmation

- **No accuracy measurement of any kind.** He asserts that the condensed store answers *"much more quickly and effectively"* but gives no comparison figure, no error rate, and no test. **The claim is plausible and unmeasured.**
- **Nothing in this source addresses reading dimension strings off a drawing**, which is what its title implies and what this project actually needs. **The `v0` blocker is untouched by it** — that question went to the Gemini brief instead (`deep_research_brief_geometry_and_agent_modelling_20260911.md`, question 2), where measured error rates are explicitly demanded.
- Whether the per-drawing summaries were produced by a model reading each drawing — and if so, with what verification — is not shown. ⚠️ **If they were, the pattern inherits exactly the misreading risk `Evidence_Reading_Discipline.md` records seven real instances of, and his rows carry no provenance with which to audit it.**
