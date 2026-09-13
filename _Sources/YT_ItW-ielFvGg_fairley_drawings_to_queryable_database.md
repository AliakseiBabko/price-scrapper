---
source_type: video transcript (consultancy channel, workflow explainer with measured benchmark results and a product funnel)
source_url: https://www.youtube.com/watch?v=ItW-ielFvGg
video_id: ItW-ielFvGg
transcript_file: _Archive/processed_sources/20260913_fairley_drawings_to_queryable_database_bffd2aaf.txt
fetched: 2026-09-13 via youtube-transcript-api (en auto captions — ORIGINAL language, English-spoken source, not a translated track)
upload_date: 2026-06-30 (confirmed via yt-dlp metadata, upload_date=20260630)
channel: Tim Fairley — construction-AI consultancy, sells "Contractor OS"; Australia (stated market)
source_title: "How to Get AI to Read Construction Drawings (50x Less Tokens, 20% More Accurate)"
language: en
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode — buckets `Digital Toolchain / AI Workflow`, `Drawing and Documentation Conventions`)
fact_yield: 12
promotional_ratio: medium
corroborates_existing: true
region: n/a_AU_market_no_jurisdictional_claim
delivery_model: n/a — not a renovation source; a construction-management consultancy
---

# Extraction Note — Tim Fairley: Turning Construction Drawings Into a Queryable Database, With Measured Results (YouTube ItW-ielFvGg)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Why this source matters more than its predecessor

**⚠️⚠️ This closes a gap this vault explicitly recorded and left open.** `YT_3tAYEJTyUFY` (same practitioner, 2026-04-29, processed 2026-09-11) was routed with the complaint, in its own CSV row: *"there is NO ACCURACY MEASUREMENT of any kind — he asserts the condensed store answers much more quickly and effectively with no comparison figure, no error rate and no test."* **This video is that test.** It is the same workflow, two months later, with a 44-question benchmark and token counts.

**Fourth source from this practitioner** (`3tAYEJTyUFY` processed; `_k1jQBS4Nk8` and `S77hdyyjTmA` in this same batch). Per the vault's standing treatment of a single channel, **repeated claims across his videos are one consistent stated position, not independent corroboration.** What is genuinely new *here* is the measurement.

## Numeric Data — The Benchmark

**⚠️⚠️ Method, stated: he wrote 44 question-and-answer pairs himself against real drawing sets, then had Claude answer them under three different pipelines.** He is explicit that he wants to build the testing out further. **`single-account`, self-administered, self-scored, not independently replicated — weight accordingly.** The transcript garbles the count once as "20 44 questions"; **44** is the figure that survives context.

| Pipeline | Accuracy | Tokens per query |
| :--- | :--- | :--- |
| **Raw images / raster PDF** (no vector layer to select text from) | **86%** | **104,000** |
| **Split + extract vector data → markdown**, referring back to the PDF as needed | **98%** | **66,000** |
| **Query the structured database** (his "drawing analyzer" skill, with checks) | **100%** | **1,400** |

- **Stated headline: 46–72× cheaper.** (1,400 against 66,000 and 104,000 gives ~47× and ~74×; the stated range is consistent with his own figures.)
- **⚠️ The caveat he states himself, and it is the one that matters for a single-user project: the first indexing pass "uses a ton of tokens."** His amortisation argument is a *team* — one person runs the index, everyone else queries it cheaply. **For a one-person project the break-even is a number of queries, not a number of people**, and he does not give it.
- **⚠️ The accuracy gain from database-over-markdown is small (98% → 100%) while the token gain is large (66,000 → 1,400).** Worth separating: the *vector extraction* buys the accuracy, the *database* buys the cost.

## Durable Facts — Why Drawings Are a Bad AI Input

- **Cross-sheet references are the core structural problem**: a footing appears on page 4 and its section view on page 10; answering "how much concrete in these footings" requires the layout (count) **and** the section (depth and size). Tracing a conduit across drawings is the electrical equivalent. Trivial for a human reader, unreliable for a model.
- **A tag means nothing in isolation** — "a tag like F6 only means anything if we go to the section view on the back of the drawings."
- **Symbol and line-weight distinctions carry the meaning**: a dashed line versus a thick line, a minor symbol change. Visually near-identical, semantically opposite.
- **File size**: ~12 MB is called a *relatively standard* drawing set.
- **⚠️ He names the clock benchmark as the external evidence** — "just look up the clock benchmark, which measures how accurately AI models can read analog clocks." Stated as the general demonstration that precise image interpretation is the failure mode. *(The companion source `S77hdyyjTmA` gives the figure: 50.6% against a 90% human baseline.)*

## Rules / Heuristics — The Architecture

**⚠️ The organising principle, stated repeatedly and the most transferable single idea: index the drawings by the PHYSICAL OBJECT, not by the drawing page.** "Instead of structuring our drawings by the page numbers of the drawings, we're taking everything in the drawings and structuring them by the objects shown in the drawings" — slabs, footings, pipe runs, cable runs. Each object carries its dimensions, its specifications, and **the source drawing the information came from**.

Three artefacts sit in the workflow:

1. **`drawings.md` — a register/map of the whole set**, one page, listing every drawing and what is on it. **Pulled in before any drawing is read**, so the model has the overall context plus instructions on how to query the rest.
2. **`drawings.db` — the object-indexed database.** Grouped by physical thing, with quantities, specs, source drawing, **and a confidence rating per measurement** (see below).
3. **A structured text wiki for the non-visual content** — general notes, specifications, schedules — grouped by subject (concrete, electrical, QA), not by drawing. **⚠️ He names its origin: the Andrej Karpathy "LLM wiki" approach.**

- **Query behaviour: progressive ingestion.** Read the register, then the database or the wiki; **go back to the original PDF page only when the database entry is low-confidence or the information is missing.** Only that one page is pulled, not the set.
- **⚠️⚠️ A per-measurement RELIABILITY RATING is stored in the database, and the tiers are stated**: a **counted** quantity, or one read off a **schedule** ("this slab is 200 mm thick"), rates high; an **area or scaled measurement** rates medium. **The confidence travels with the number.**

## Rules / Heuristics — Where Accuracy Actually Breaks

- **⚠️⚠️ Counting instances from vector data is stated as 100% accurate** — the model pulls the vector layer and **writes a script to count occurrences of the F6 tag** rather than looking at the image. *(Note this is a script counting text tokens, not vision — which is why it is reliable.)*
- **⚠️⚠️ Measuring a length by scaling is where it fails**, and he names the full chain of assumptions: extract the scale from the drawing set → crop the region → **assume the scale is what it says** → measure. **This is the same failure this vault already records as "a scaled raster is orientation, not measurement" and "type the dimensions, don't click the pixels."**
- **⚠️⚠️ The mitigation is an ORDER-OF-MAGNITUDE CROSS-CHECK against a known whole, and it independently restates this project's own standing rule 9.** Worked example: a cable-tray run measured at 7 m, where the run visibly spans the building and another drawing gives the building as 35 m, is *clearly wrong*; the reasonable estimate is 3 × 25 m for the full-length runs plus the part-length ones. **"That is obviously not going to be 100% accurate, but it's just this order of magnitude check."** → **This is chain closure — "prefer chain closure over judgement wherever a whole is known" — reached independently by a practitioner with no connection to this project.**

## Planning Rules — The BIM Argument, Stated Most Forcefully Here

- **⚠️ His own framing: the entire workflow is reverse-engineering a BIM model from its own printed output.** "This is basically copying this exact same approach that BIM models were... just reverse engineering it to create from a set of PDF drawings." In a BIM model (Revit, Autodesk) every wall and fitting already sits in a structured database, so a model reading it "is just pulling the actual numbers or quantities from it."
- **"This entire process would be redundant if people gave the BIM models."** Stated as an industry criticism: when quoting a job or receiving a design handover **you are always given the drawings and never the model**, even though the model demonstrably exists on someone's computer. He predicts the industry moves toward handing over the model.
- **⚠️ Relevance to this project, and it is the reason to record the argument rather than the workflow: this project is already on the correct side of it.** `data/canonical/` **is** the structured store, and the drawings are **generated from it** rather than parsed back out of it. **The whole pipeline he is building exists to recover what this project never discards.** Recorded as validation of the architecture, not as instruction.

## Advertising / Promotional Content

- **Contractor OS** — his product: "one of the 40 different construction workflows", weekly additions, **unlimited one-on-one setup calls**. A prepackaged Claude skill is linked in the description. **A real sales funnel, and the video is structured to demonstrate the product.**
- **⚠️ The countervailing facts, which is why this is `medium` and not `high`**: the full method is described in enough detail to rebuild without buying anything; **the benchmark numbers are given against his own earlier method, showing his previous approach as inferior** (98% vs 100%, 66k vs 1.4k tokens); and he states the open problems rather than hiding them (needs more testing, database structure unfinished, trade templates unproven).
- **⚠️ Stated future work, recorded as intent not fact**: per-trade template databases; sub-agents on cheaper models (Haiku for some tasks, "Claude Opus 4.8" for visual interpretation); benchmarking models and harnesses against each other. ⚠️ **The model names here date fast and are not routed.**

## Confidence & Evidence Notes

- **ASR quality**: adequate. Observed corruption: "careerable acquirable" for *queryable*, "Kapathy"/"Karpathy", "Claude Co-work" for Claude Code, "20 44 questions", "vic- vector". Product and model names are candidates, not figures.
- **`single-account` throughout.** The benchmark is self-constructed, self-administered and self-scored on his own Q&A set against his own product. **The numbers are the best this vault has on the question and are still one interested party's.**
- **`corroborates_existing: true`** — context rot, the condensed-store pattern, and "a scaled raster is not a measurement" are all already recorded. **New: the measured accuracy and token figures, the object-indexed schema, the per-measurement confidence rating, the progressive-ingestion query rule, the order-of-magnitude cross-check, and the Karpathy-wiki pattern for text content.**
- **No regulatory content** — nothing routed to `16_Legal_and_Regulations/`.

## Recommended Downstream Routing

- **`18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings.md` (NEW PAGE)** — the benchmark table, the three-artefact architecture, the object-indexing rule, confidence ratings, and where accuracy breaks.
- `18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice.md` §7 — cross-reference only; the agent-behaviour material stays there.
- `_Knowledge/store/Rules_Heuristics.md` — the order-of-magnitude cross-check as independent corroboration of standing rule 9.
- `_Knowledge/store/Advertising_Promotional_Notes.md` — Contractor OS, and the self-benchmarking that partly offsets it.
- **5b**: no prices in this source; no conversion owed.
