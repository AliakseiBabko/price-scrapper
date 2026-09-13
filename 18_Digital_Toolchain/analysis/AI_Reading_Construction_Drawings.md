# Getting AI to Read Construction Drawings

Detail page for [[18_Digital_Toolchain/Digital_Toolchain_Guide|Digital Toolchain]].

**Why a PDF drawing set is a bad input to a language model, what measurably fixes it, and where the accuracy actually breaks.** General practice from named practitioners — **not this project's own pipeline**, which is described in `00_Master/` and whose relationship to all of this is set out in the last section.

> [!IMPORTANT]
> **The whole of this page's measured content comes from ONE practitioner (Tim Fairley, construction-AI consultancy, Australia) across four videos.** Repeated claims across his videos are **one consistent stated position, not independent corroboration.** Where a second, unrelated channel reaches the same place it is marked. **His benchmark is self-constructed, self-administered and self-scored against his own product.** It is the best evidence this vault has on the question and it is still one interested party's.

## 1. Why a drawing is a bad input — the mechanism, not the complaint

**⚠️⚠️ A vision model does not read an image; it tiles it.** The image is cut into patches — stated as 16×16 pixels — each patch is converted to tokens, and those tokens are processed the same way as text. A single drawing lands at **roughly 4,000 tokens**.

**The consequence is the entire problem: "the fundamental meaning of construction drawings lives in these tiny features."** Recognising a cat survives tiling, because a cat is spread across many patches. These do not:

- **A semi-dashed line is cold water; a double-dashed line is hot water.** Visually near-identical, semantically opposite, and consequential for estimating and scheduling.
- **`TD7` is meaningless** until you know it is on the sanitary drainage sheet and corresponds to a trench-drain type in a schedule.
- **An `F6` footing** only has dimensions if you know to go to the section view later in the set.

> [!NOTE]
> ⚠️ **The 16×16 figure is an implementation detail that varies by model — treat it as illustrative of the mechanism, not as a specification.** The mechanism is what is durable.

**→ This supplies the MECHANISM under a conclusion this vault already held from an unrelated channel.** [[18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice|Drawing Conventions From Practice]] §6 records, from Trimble's Aaron Dietzen, that a raster is *"literally a bunch of dots"* with nothing to snap to, and from Justin Geis that a scaled raster is orientation rather than measurement. **Those say what a raster lacks. This says why the model cannot recover it.** [source: [[_Sources/YT__k1jQBS4Nk8_fairley_why_ai_fails_on_drawings|YT__k1jQBS4Nk8]]]

### The vendor's own stated limits, and a benchmark

- **⚠️ Anthropic's documentation is cited for three limits, all directly on point**: hallucination; **spatial reasoning is limited** — *"may struggle with tasks requiring precise localization or layout"*, with Anthropic's own examples being **reading an analog clock and describing exact positions of chess pieces**; and **counting — "approximate counts", explicitly not accurate ones.**
  - **⚠️⚠️ The counting limit is the one to carry, because it reframes a whole class of task: a count taken off a drawing by vision is an estimate BY DESIGN, not a bug to prompt around.** Its resolution is in §3.
- **The clock benchmark, quantified**: the top model reads an analog clock at **50.6%** accuracy against a **90%** human baseline. ⚠️ **Single mention, model name `ASR-uncertain` ("GPT-5.4"), and model scores date within months — the durable shape is that precise reading of a simple diagram is near a coin-flip while object recognition is near-solved.** [source: [[_Sources/YT_S77hdyyjTmA_fairley_three_layer_vector_takeoff|YT_S77hdyyjTmA]]]
- **A named academic pointer, not a verified result**: a Florida International University benchmark for LLMs in construction estimating (`ASR-uncertain` on title and authors, **not checked**). Its stated findings: general-purpose models do not know how to process drawings; **they identify drawing elements poorly** — the scale, the title block, whether a sheet is a layout, section or schedule; **they do not know the standard organisation of a drawing set** or how its parts cross-reference; and their construction knowledge is no better than a web search.
  - **→ The operational answer to those middle two is the reusable part: put drawing-type-specific instructions into the pipeline, so it TELLS the model what kind of sheet it is looking at rather than hoping it infers it.**

### The other three failure modes

- **File size.** ~6 MB for 10–15 civil drawings; ~12 MB called a standard set. A harness opened on the folder re-ingests the set on every query — **60,000–70,000 tokens per question**.
- **Context rot** — more context, less reliable output. Already recorded in this vault from the same practitioner's earlier video.
- **Drawings are organised for human scrolling, not for querying.** The layout plan and the section that gives the slab depth sit pages apart. **Splitting the set into individual PDFs does not fix this**, because the grouping is still by sheet rather than by the thing being asked about.

## 2. What fixes it — index by the OBJECT, not by the sheet

**⚠️⚠️ The organising idea, and the most transferable single thing on this page: structure the data by the physical thing being built, not by the page it is drawn on.** Slabs, footings, pipe runs, cable runs — each carrying its dimensions, specifications, **and the source drawing the information came from**.

Three artefacts:

| Artefact | What it is | Why |
| :--- | :--- | :--- |
| **`drawings.md`** | A one-page register of every drawing and what is on it | **Pulled in before any drawing is read**, so the model has whole-set context and instructions on how to query the rest |
| **`drawings.db`** | The object-indexed database — quantities, specs, source drawing, **and a confidence rating per measurement** | The cheap thing to read. This is what queries hit |
| **A structured text wiki** | General notes, specifications, schedules — grouped by **subject** (concrete, electrical, QA), not by drawing | Much drawing content is text, not geometry, and needs no visual pass at all. ⚠️ Origin named: the **Andrej Karpathy "LLM wiki"** pattern |

- **Query rule: progressive ingestion.** Read the register, then the database or the wiki; **return to the original PDF only when an entry is low-confidence or missing — and then pull only that one page.**
- **⚠️⚠️ A reliability rating is stored WITH each measurement, and the tiers are stated**: **counted**, or **read off a schedule** ("this slab is 200 mm thick") → high; an **area or scaled measurement** → medium. **The confidence travels with the number.**

### The three data layers that feed it

Three *independent* sources, each covering a different weakness — **vector data alone "doesn't really mean anything"**, being a mass of coordinates with no concept attached:

1. **The image layer** — gives the conceptual read (*this is a hydraulics layout*). What models are good at.
2. **The vector layer** — text, symbols, geometry. **Supplies the precision the image cannot.**
3. **The exported quantity take-off** — **supplies verified quantities and the assembly structure.**

**⚠️⚠️ The take-off layer is deliberately MANUAL, and the justification is economic rather than technical.** *"Everyone wants AI quantity take-off tools. Unfortunately, from what I've seen, they don't really work that well."* But a take-off must be produced anyway to prepare an estimate — **so the marginal cost of exporting it as structured data is near zero.**

> **→ The general form, worth keeping even where nobody is estimating: where a human is already producing a structured artefact for another reason, exporting it is the cheapest possible high-confidence data layer.**

### The element schema, and where it came from

**element · category · trade · location · measurements/quantities · specifications · comments and tags · relationships with other elements.**

**⚠️⚠️ He names the origin twice and unprompted: the schema is copied from BIM's IFC model format.** *"This is actually an idea I copied from BIM, which actually has the IFC model format that uses this exact strategy."* → **So the schema to copy is IFC's, not his.** Directly relevant here: the 2026-09-11 round found `IfcRelConnectsPathElements` unused anywhere in this repo. **A practitioner reverse-engineering IFC by hand out of PDFs is an argument for reading the standard rather than inventing fields.**

## 3. Where accuracy actually breaks — counting versus measuring

**⚠️⚠️ The distinction that organises everything else: classifying a drawing is easy, and measuring from it is hard.** *"You can upload a picture of a cat and AI can say, yes, that's a cat"* — and equally *"this is a plumbing drawing."* That is categorically different from *"that is 20.7 m of hot water line."*

- **⚠️ Counting instances from the vector layer is stated as 100% accurate** — the model pulls the vector text and **writes a script to count occurrences of the `F6` tag**. **Note why this works: it is a script counting text tokens, not a model looking at a picture.** It routes around the vendor-stated counting limit entirely rather than mitigating it.
- **⚠️⚠️ Measuring a length by scaling is where it fails**, and the chain of assumptions is named: extract the scale from the set → crop the region → **assume the scale is what it says** → measure. **This is exactly the failure this vault already records as "a scaled raster is orientation, not measurement" and "type the dimensions, don't click the pixels."**
- **A clean demonstration of the split**: querying the raw drawing set returned the number and type of ground beams but **could not return their lengths** — *"obviously hasn't been able to precisely measure that."* Retrieval worked; measurement did not.
- **A measured instance of the counting limit**: asked how many footings were on the foundation drawings, a harness reading the raw folder answered **141 — an overcount**. The pre-processed pipeline returned the correct count broken down by type, **with a stated confidence and the source drawings cited.**

### ⚠️⚠️ The mitigation independently restates this project's own standing rule 9

**The order-of-magnitude cross-check against a known whole.** Worked example: a cable-tray run measured at **7 m**, where the run visibly spans the building and another drawing gives the building as **35 m**, is *clearly wrong*; the reasonable figure is 3 × 25 m for the full-length runs plus the part-length ones. *"That is obviously not going to be 100% accurate, but it's just this order of magnitude check."*

> **→ This is chain closure — `Evidence_Reading_Discipline.md`'s "prefer chain closure over judgement wherever a whole is known" — reached independently by a practitioner with no connection to this project, and reached as a way of catching a MACHINE's misreading rather than a human's.** The strongest available external validation of that rule.

## 4. The measured benchmark

**⚠️ Method: 44 self-written question-and-answer pairs against real drawing sets, answered by Claude under three pipelines. Self-constructed, self-administered, self-scored, against his own product, not independently replicated.** He states he wants to build the testing out further. The transcript garbles the count once as "20 44 questions"; **44** survives context.

| Pipeline | Accuracy | Tokens per query |
| :--- | :--- | :--- |
| Raw images / raster PDF (no selectable vector layer) | **86%** | **104,000** |
| Split + extract vector data → markdown, returning to the PDF as needed | **98%** | **66,000** |
| Query the object-indexed database, with checks | **100%** | **1,400** |

- **Stated headline: 46–72× cheaper.** Consistent with his own figures (1,400 against 66,000 and 104,000 ≈ 47× and 74×).
- **⚠️⚠️ Read the two columns separately, because they are bought by different steps.** The **vector extraction** buys nearly all the accuracy (86 → 98%); the **database** buys nearly all the cost reduction (66,000 → 1,400) and only 2 points of accuracy. **If you can only do one, which one depends on whether your problem is being wrong or being expensive.**
- **⚠️ The caveat he states himself: the first indexing pass "uses a ton of tokens."** His amortisation argument is a *team* — one person indexes, everyone queries. **For a single-user project the break-even is a number of queries, not a number of people, and he does not give it.**
- **⚠️ A self-criticism worth keeping as a design lesson**: his own store "is all sitting as one text file. What you should actually have is some sort of database structure like an SQL database." **A flat file must be read whole into context — the same objection this vault already records against reading its own CSVs whole.**

## 5. Division of labour — scripts versus judgement

**⚠️⚠️ The most actionable rule here, and it cuts against how a coding agent behaves by default.**

- **Use scripts for the cheap deterministic work** — splitting the PDF, extracting the vector layer, cropping. **Use the model for categorisation and understanding** — what this drawing is and what is on it.
- **⚠️⚠️ The counter-warning: Claude Code *always wants to write a script for the classification too*, and it should not be allowed to.** A generated classifier does **pattern matching** — *"if the title says electrical, this is an electrical drawing"* — and **"this just doesn't work reliably"**, because titling and formatting conventions vary too much between issuers.

> **→ The general form: automate what is deterministic, and refuse to automate what is a judgement about a document's own idiosyncratic conventions. An agent's eagerness to write a script is not evidence that the task is scriptable.**
>
> ⚠️ **Directly relevant to this project's own extraction pipeline, and it cuts in our favour**: `tools/layout/parse_vector_plan.py` parses **one issuer's** drawings, and a per-issuer parser is legitimate *precisely because* the issuer is fixed. The rule explains why that must not be generalised into a universal drawing parser.

## 6. The BIM argument — and why this project is already on the right side of it

**The claim, stated in all three videos and most forcefully in the second: the entire workflow is reverse-engineering a BIM model out of its own printed output.** In a BIM model every wall and fitting already sits in a structured database, so an agent reading it "is just pulling the actual numbers or quantities from it". Drawings are a 2D *representation*; the cross-references, section views and schedules exist only to compensate for that.

- **"This entire process would be redundant if people gave the BIM models."** His industry criticism: when quoting a job or receiving a design handover **you are given the drawings and never the model**, though the model demonstrably exists on someone's computer. He expects the industry to move.

> [!IMPORTANT]
> **⚠️⚠️ This is validation of this project's architecture, not instruction for it — and the direction matters.**
>
> **`data/canonical/` IS the structured store, and the drawings are GENERATED from it rather than parsed back out of it.** The elaborate pipeline on this page exists to recover, imperfectly and with confidence ratings, exactly what this project never discards. Two further places where this project is ahead of the practice described here:
>
> - **Every figure carries provenance** (`Evidence_Reading_Discipline.md`, `vector_extent_oracle.py`), where his database carries a three-tier confidence rating and no source audit beyond the drawing number.
> - **The gates are automated.** His order-of-magnitude check is a prompt instruction; `check_dxf_closure.py` and `check_wall_junctions.py` fail the build.
>
> **What genuinely transfers, and it is not nothing:** the **per-measurement confidence tier** as an explicit stored field; the **progressive-ingestion query rule**; the **subject-grouped wiki** for text content that needs no geometry; and the **measured argument** that vector extraction buys accuracy while an index buys cost — useful whenever this project decides how much to invest in either.

## Source Notes

| Source | Contribution |
| :--- | :--- |
| [[_Sources/YT__k1jQBS4Nk8_fairley_why_ai_fails_on_drawings\|YT__k1jQBS4Nk8]] (2026-05-13) | The tiling mechanism; Anthropic's stated limits; the FIU benchmark pointer; the 141 overcount; scripts-versus-judgement |
| [[_Sources/YT_ItW-ielFvGg_fairley_drawings_to_queryable_database\|YT_ItW-ielFvGg]] (2026-06-30) | The 44-question benchmark; the three artefacts; confidence tiers; progressive ingestion; the order-of-magnitude cross-check; the Karpathy wiki pattern |
| [[_Sources/YT_S77hdyyjTmA_fairley_three_layer_vector_takeoff\|YT_S77hdyyjTmA]] (2026-07-25) | The three data layers; take-off as a data layer; the element schema and its IFC origin; the clock-benchmark figure; classify-versus-measure |
| [[_Sources/YT_3tAYEJTyUFY_fairley_ai_read_construction_drawings\|YT_3tAYEJTyUFY]] (2026-04-29, processed 2026-09-11) | Context rot; the condensed-store pattern. **Its recorded gap — no accuracy measurement — is closed by `ItW-ielFvGg` above.** |

**⚠️ All four are the same practitioner and the same product funnel (Contractor OS, a paid Claude skill, and a ZZ Takeoff endorsement).** Promotional handling: [`_Knowledge/store/Advertising_Promotional_Notes.md`](../../_Knowledge/store/Advertising_Promotional_Notes.md).
