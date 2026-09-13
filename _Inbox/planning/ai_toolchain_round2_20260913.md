# Toolchain Round 2 — the deferred Tier 2 items, processed 2026-09-13

**The owner re-supplied the original 24-item list (20 loose videos + 4 channels) and asked to continue, recalling the earlier batch as having been "trashed."** This file records what was actually outstanding, what was processed, and what remains.

## 1. ⚠️ The premise, corrected — nothing was trashed

**The 2026-09-11 list was tiered, not discarded.** Its own triage sorted 11 items into **Tier 1 (5, processed)**, **Tier 2 ("fetch in a Round 2, not now", 5)** and **Tier 3 (1, skipped with a reason)** — and it named `X1lnTEpy6PQ` **"the single most useful next fetch."** The 2026-09-08 list was handled the same way.

**So Round 2 was already specified. This round executes it** rather than starting over.

| Status | Items |
| :--- | :--- |
| Already processed (2026-09-11 Tier 1) | `f0EU_xbavEA` `9tfvs3XW5qQ` `HOjQiiHJ714` `3tAYEJTyUFY` `althlPj8Tag` |
| **Processed this round** | `MZv33G7UE_A` `sSnjQJX4-iY` `s0TrXB2WQ2Q` `A1HxpHxrvv4` `X1lnTEpy6PQ` `9-hQsyWSnm4` `PVXE79HM0-c` `YkHGQPfZEgM` `BEHlmJCKvTA` `E-ECbD14g_8` `tJSS-IWrJoE` |
| **Still excluded — reasons re-checked and they stand** | `YA9y2IwhCMc` (content is entirely 2020 St Petersburg prices; rule 2 makes them uncomparable), `ZXv5HK8Lhys` + `9muFQQZsgsU` (thin third-party RemPlanner tips, superseded by RemPlanner's own 18-minute lessons), `fuOjlEj4MbU` (a 4-minute plugin announcement whose substance is in `A1HxpHxrvv4`, processed this round), `0T97_CA7hgo` (2020 DIY SketchUp electrical, superseded) |
| Belongs to another queue | `PqvvsL625rc` — triaged on the Vasily_Sanuzel channel queue, flagged "do not double-handle" |

**⚠️ The five exclusions were re-examined against the owner's re-supplied list and left excluded.** They are recoverable in one command if the owner disagrees — **none is a skip on quality, four are skips on supersession or on rule 2.**

## 2. ⚠️⚠️ The finding that should change how triage is done

**Round 2 yield: 11 videos, 77 new facts, 7.0 per video — against Round 1's 5.1.**

**The tier that was deferred outyielded the tier that was read first.** And two of the three lowest-rated items in the batch were among the five richest:

| Item | Prediction | Actual |
| :--- | :--- | :--- |
| `PVXE79HM0-c` | *"One cheap survey of the tool landscape… probably a listicle"* | **Yield 10.** A working electrical shop's complete deliverable set, their layer-by-responsibility convention, and a data-carrying-label schedule mechanism |
| `9-hQsyWSnm4` | *"wall-tracing over a scaled raster underlay"* — i.e. thin | **Yield 9.** Two modelling conventions this project does not state anywhere: register on the longest known distance, and a wall's side is relative to its direction |

> **→ A triage's confidence about a source it has NOT FETCHED is worth much less than it feels. Deferral order should track COST — length, language, fetch risk — not predicted yield.** The cheap items should go first regardless of what the title promises, because the prediction is the unreliable part.

## 3. What this round produced

**New page**: `18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join.md`.
**Extended**: `Drawing_Conventions_From_Practice.md` (§3 and §6), `Agent_Connected_CAD.md` (§4–5), `Bill_of_Quantities_and_Procurement.md` (§5a-quinquies-bis and §5a-sexies), the folder guide.

**The five findings that matter most are recorded in full in [[18_Digital_Toolchain/analysis/Change_Log|the folder's Change Log]].** In brief: a practitioner performing this project's own chain-closure check and discarding the result; a gap in this project's cost-engine design (no waste factor) exposed by an outside tool, with the vault already holding the better half of the answer; a third agent-CAD architecture this project is already on; the two-quantities-per-line schema `ELE-01` needs; and three independent arrivals at *re-derivability, not precision*.

## 4. ⚠️ What was deliberately NOT done, and what remains

- **No frame extraction.** Several of these are screencasts, and `tools/youtube/extract_layout_frames.py` exists for exactly that. **On reading, the value in all eleven was spoken schema and stated conventions rather than on-screen detail** — but ⚠️ **`A1HxpHxrvv4` and `9-hQsyWSnm4` are the two where a frame pass would add most** if their on-screen dialogues and parameter panels are ever wanted verbatim.
- **⚠️⚠️ The four CHANNELS in the owner's list are not done, and they are a much larger job than the loose videos were:**

| Channel | State |
| :--- | :--- |
| **`@RemPlanner`** | **1 of a planned 6 lessons processed** (Урок 4). The 2026-09-08 triage recommended 6 of the 13-lesson «Видеоуроки» series *as a specification, not a tutorial*. **5 outstanding, and it is the highest-value channel remaining** — Урок 4 alone gave the dimensioning datum and the вывод/розетка split |
| **`@k_dmitry`** | **Round 1 of 5 proposed done** (5 videos). **328 videos on the channel**; the triage weighted future rounds to the «технический дизайн-проект» and «обоснование планировочного решения» formats |
| **`@Craftelectric`** | **Both named Tier 2 singles processed this round.** The rest of the channel is unassessed |
| **`@АлександрЭлектрик-ц3н`** | **Assessed as a skip** on 2026-09-08 — three DIY clips of 2–5 minutes, against a folder already far deeper from specialists. **Unchanged** |

- **⚠️ Still nothing on COST CALCULATION as a method.** This round adds the *schema* for a quantity→price join, which is real progress on the gap. **It does not add rates, a rate source, or a costing procedure** — and the cost engine remains the one genuinely absent tool from [`toolchain_gap_analysis_20260908.md`](toolchain_gap_analysis_20260908.md) §B.

## 5. Open items this round raises

- **⚠️⚠️ `waste_pct` is missing from this project's cost-engine design.** Both take-off tools carry it as a first-class field per cost line. **The design should carry it as a per-resource property with a METHOD attached** (nested cut plan vs. flat percentage), per §2 of the new page. **Owner decision; not actioned.**
- **⚠️ A wall-direction convention should be stated explicitly** in `.agents/skills/residential-bim-geometry-rules/` — if a wall carries a direction, traverse the perimeter consistently; if it does not, say so, so nobody assumes one.
- **⚠️ Is the frozen raster registration fitted on the LONGEST available reference?** `raster_fidelity.py` registers from the PDF's hatched wall faces against a committed fit. The rule that a registration's relative error scales inversely with reference length makes this a checkable question about the committed registration.
- **⚠️ `ELE-01` needs two quantities per line** (conductor and containment), and containment rates depend on `wall_materials.json`. Recorded as an input to that BOM line's design.
