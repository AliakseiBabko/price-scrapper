# AI-agent modelling and raster→geometry sources — triage of an 11-item list

**Created 2026-09-11.** The owner supplied 11 videos on *"using AI agents for creating floor layout plans and 3D modeling"*, asked whether any were already processed, and framed the pain as: *"we're struggling to draw walls to connect them properly, to avoid overlapping or leaving gaps between walls… I know probably we reinvented a wheel so we can get new tools, new approaches."*

**All 11 are fresh** — checked against `00_Master/processed_video_ids.txt` (522 ids). **No overlap with the 2026-09-08 design-toolchain list**, which was Russian-language and about a designer's documentation; this batch is **English-language and about AI agents driving CAD**. Companion research brief delegated to Gemini the same day: [`deep_research_brief_geometry_and_agent_modelling_20260911.md`](deep_research_brief_geometry_and_agent_modelling_20260911.md).

---

## ⚠️⚠️ First, the premise — because it changes what this list is for

**Checked in the working tree today, not recalled:**

| The stated pain | Verified state |
| :--- | :--- |
| *"struggling to draw walls to connect them properly"* | **`check_wall_junctions.py` → PASS.** 25 wall runs, *"no overlap, no gap, and every L-corner void is owned in `wall_corners.csv`"* |
| *"avoid overlapping or leaving gaps"* | **`check_dxf_closure.py` → PASS** (under `.venv-ifc314`; `ezdxf` is absent from `py -3`). No unsanctioned overlap, no unexplained near-miss in the 400 mm band, no wall-union cavity, delivered review images byte-identical to a fresh render |

**→ Wall closure is not currently broken. It is solved, gated, and guarded by 24 seeded DXF defects plus 7 raster ones.** So these videos were *not* read as a fix for that.

> [!IMPORTANT]
> **⚠️⚠️ The "reinvented a wheel" instinct is right, but the wheel is not in these videos — it is in the IFC schema, and the finding is verified.**
>
> `wall_corners.csv` resolves each L-corner by a home-grown rule (**thicker, then longer**). **IFC4 already standardises this**: `IfcRelConnectsPathElements` carries per-material-layer **`RelatingPriorities`/`RelatedPriorities`** and an **`ATSTART`/`ATEND`/`ATPATH`** connection type, making corner-versus-T a first-class distinction. Confirmed against the schema via IfcOpenShell today.
>
> **`grep` across the whole repo returns zero uses of it.** That is the real reinvention, and it is question 1 of the Gemini brief.

**What IS actually blocked, and it reframes the whole list**: `project_decisions.md` records that **`v0` has no geometry and it blocks layout selection**, with the recorded route being *"reconstruct the partitions from the PRINTED dimension strings on `fllor_plan_detailed.jpeg`, using the registered raster"* — described there as **hand work**.

**→ So the valuable axis in this list is raster-plan→geometry, not wall joining. And on that axis the list delivers more than expected.**

---

## Verdicts

**Language note**: ten are natively English, one Russian. **`en-orig` / `ru-orig` used throughout — standing rule 1 is about never taking a *translated* track, and the original here is English for the English sources.** No manual subtitles exist on any of the 11; auto-captions only.

⚠️ **Do not use the subscriber counts `yt-dlp` returned** (609, 478, 651, 504, 482 for channels including TheSketchUpEssentials and the official Trimble SketchUp channel). They are implausibly low and near-identical — the same class of error as the flat-playlist view counts corrected in `vasilysanuzel_channel_triage_20260908.md`. **Nothing here is ranked by audience.**

### ⭐ Tier 1 — read, and they contributed findings

| ID | Source | Len | Verdict |
| :--- | :--- | :--- | :--- |
| **`f0EU_xbavEA`** | TheSketchUpEssentials — *The RIGHT Way to Import Reference Images in SketchUp* | **5:12** | ⭐ **Best value-per-minute in the batch, and it answers an open question from the last round.** See §A |
| **`9tfvs3XW5qQ`** | **Trimble SketchUp** (official) — *3 Ways to Convert 2D Floorplans to 3D Walls* | 17:25 | **Partial** — GUI mechanics discarded; two real discipline findings. See §A |
| **`3tAYEJTyUFY`** | Tim Fairley — *How to Get AI to Read Construction Drawings* | 14:43 | **Partial, and not about what its title suggests** — it is about context management, and it **validates this repo's architecture**. See §B |
| **`HOjQiiHJ714`** | **Trimble SketchUp** (official) — *How good is Claude at SketchUp modeling?* | 16:34 | **Partial** — supplies the batch's strongest cautionary rule. See §C |
| `althlPj8Tag` | **Trimble SketchUp** (official) — *CAD Linework to SketchUp Geometry: 3 Methods* | 13:22 | **Corroborating only.** Companion to `9tfvs3XW5qQ`; skimmed, no independent finding. See §A |

### Tier 2 — fetch in a Round 2, not now

| ID | Source | Len | Why it waits |
| :--- | :--- | :--- | :--- |
| `X1lnTEpy6PQ` | *Claude AI Just Got SketchUp Modeling… This Changes Things!* | 11:27 | Same subject as `HOjQiiHJ714`, from a non-vendor angle. **`HOjQiiHJ714` is the official channel testing the same adapter and was read first; expect corroboration rather than new mechanism.** Worth one fetch to check whether it names limits Trimble's own video omits |
| `BEHlmJCKvTA` | *Is AI 3D Modeling FINALLY Here? Testing Claude Fable 5* | 16:45 | A model-capability test. ⚠️ **Capability claims date fastest of anything in this vault** — worth reading only for the *evaluation method*, not the verdict |
| `E-ECbD14g_8` | *I tested GPT Astra for 3D Modeling — This is Getting Serious* | 26:22 | Uploaded **2026-09-10**, i.e. yesterday. Same caveat, different vendor |
| `tJSS-IWrJoE` | *The AI Rendering Tool I Use MOST — and Why* | 20:18 | **Rendering, not geometry.** Bears on the "EEVEE demonstrator → presentable" question, where the 2026-09-08 research already advised **outsourcing a room render at \$40–90 rather than building an asset pipeline**. Read it only if that advice is being revisited |
| `YkHGQPfZEgM` | Upstairs — *How I Turn Simple Floor Plans Into Beautiful Architectural Drawings* | 16:25 | **Presentation/graphic style of a plan**, which is a real open item (our sheets are functional, not handsome) — but it is the least urgent axis and the title promises aesthetics rather than method |

### ✗ Tier 3 — skip

| ID | Source | Why |
| :--- | :--- | :--- |
| `0T97_CA7hgo` | LOFT DIY (RU) — *Схема электропроводки своими руками в SketchUp*, 20:10, **2020** | The only Russian item and the only one off-topic for this batch. **Its subject — drawing an electrical plan in SketchUp — is already covered better by Round 1's `YT_OTBw7bCrv-o` (RemPlanner Урок 4, which gave the dimensioning datum and the вывод/розетка split) and by Craftelectric's `A1HxpHxrvv4`, already triaged Tier 2 on 2026-09-08.** Six years old, DIY-level, and a GUI walkthrough. **Excluded on title+date skim; not fetched, so no CSV row** |

---

## §A — Raster→geometry: three findings, and they all point the same way

**This is the part of the batch that bears on the actual `v0` blocker.**

### ⚠️⚠️ 1. Two-point scale verification — register on one printed dimension, verify on a *second, independent* one

`f0EU_xbavEA` gives a complete procedure: scale the raster off one known printed dimension (he uses a long one, 36′4″), **then draw a separate line elsewhere in the drawing and check its measured length against its own printed value** (7′2″) — *"And I always want to check… sometimes what I like to do is I like to draw a line somewhere else."* His honest verdict on the result: *"it's pretty close — that's about as close as you're going to get by scaling a document like this."*

**→ This is a cheap check we do not currently have, and it is NOT the same as chain closure.** Chain closure validates that a run of dimensions sums to a known whole. **This validates the registration itself** against a printed figure that played no part in establishing it — the same independence principle as `vector_extent_oracle.py`. **Worth adding to the `v0` reconstruction procedure.**

### ⚠️⚠️ 2. A scaled raster is for ORIENTATION, not for measurement — type the dimensions, don't click the pixels

The clearest statement in the batch, from `f0EU_xbavEA`:

> *"If you're trying to model this building exactly, you shouldn't be coming in here and using visuals in order to figure out where this is going to go… What I should be doing instead is I should actually be modeling to these actual dimensions… you actually need to model using the dimensions if you want this to be exact. If you're just trying to get it close enough, it doesn't really matter."*

**→ This is exactly the route `project_decisions.md` already records for `v0`** — reconstruct from the *printed dimension strings* over the registered raster, not by tracing. **Independent practitioner corroboration of a decision this project already took**, which is a direct answer to "are we doing this right": yes.

`althlPj8Tag` supplies the mechanical reason: a raster *"is literally a bunch of dots… that could be scaled to any size"* and **you cannot snap to it** — *"it doesn't know that this is an end point. It just knows that this is where these darker black boxes kind of run."*

### ⚠️ 3. The ink has width, and the width is an error term

From `9tfvs3XW5qQ`, tracing a wall off a raster: *"I could draw an edge from about the middle of this black line to about the middle of this black line and see okay, that's probably around 5½ inches… the line itself is maybe an eighth or a quarter inch thick. So you need to take all this with a grain of salt."*

**→ Reading a wall thickness off a raster requires first deciding which part of the drawn line you measure to — centre, inner or outer face — and the line's own thickness is a genuine error bar.** `00_Master/Evidence_Reading_Discipline.md` requires identifying *"the two elements its extension lines terminate on"*; this adds that **the terminating element itself has thickness.** Directly applicable to the `v0` trace and to the frozen ink mask.

### ⚠️ 4. And the same source states our own oracle principle, independently

> *"It doesn't matter how good the information you get, there's always a possibility that there's a difference between what's in the model and the actual dimension it's supposed to represent. So I always recommend double-checking against printed dimensions of some sort."*

**That is `vector_extent_oracle.py`'s reason for existing, from the GUI side** — the repo built it after learning that *"asserting the DXF against `wall_blocks.csv` only proves that two things a person edits together agree."* **Corroboration of the hardest-won lesson in the geometry work.**

**One more, weaker**: `althlPj8Tag` notes that a *vector* import leaves *"a couple spots where for whatever reason it didn't intersect correctly… I might have to do a little bit of cleanup"* — i.e. **non-intersecting near-misses are the normal outcome of CAD import, and in the GUI they are found by eye.** Our 400 mm near-miss band finds them automatically. A point where this project is ahead, not behind.

---

## §B — `3tAYEJTyUFY` is not about reading drawings, and that is the interesting part

The title promises AI reading construction drawings. **What it actually demonstrates is that the naive paths fail, and that the fix is context management.** He shows, on camera: a ~10 MB drawing set **failing to upload** to chat; the same failure via a project/RAG upload; and a folder-based agent burning *"around 30 times the number of tokens"* and answering less accurately. His term for the underlying problem is **context rot** — *"the more information we give AI, the less likely it is to answer accurately."*

**His fix: summarise each drawing into a row of a structured database, then query the database over MCP instead of the drawings.** His analogy is the best line in the batch:

> *"It's like giving someone a set of 30 or 100 drawings and saying 'what is the height of the retaining wall?' versus giving someone the retaining wall drawing and telling them this is the height of the retaining wall."*

> [!IMPORTANT]
> **⚠️⚠️ This repo already does this, and more strictly — so the finding is validation, not instruction.** `data/canonical/*.csv` **is** the condensed queryable structure; the drawings are generated *from* it rather than queried. And `Evidence_Reading_Discipline.md` plus the vector oracle go further by demanding provenance for each extracted figure, which his Airtable rows do not have.
>
> **The genuinely new item is small but actionable**: the *pattern* of one row per drawing with its key facts, queried by an agent over MCP — and his incidental notes that **Excel is a bad store because the whole sheet lands in context**, while a database or Sheets is not. He built it in **Google Antigravity**, which this project already runs as one of its three agents.

⚠️ **Two reasons to discount parts of it.** Its model-capability claims are dated 2026-04-29 and already stale — and the ASR mangles product names throughout (*"Cowerk"* for Claude Code, and a model version that cannot be taken at face value). **Recorded as a pattern, not as a model recommendation.**

---

## §C — `HOjQiiHJ714`: the batch's strongest cautionary rule

Trimble's own channel testing the Claude↔SketchUp adapter. What it establishes:

- **It is a file generator, not a live modeller.** *"There's not a direct live connection… It won't go in and edit it. It won't do it live."* A persistent session remembers prior context, but each change **emits a new file** rather than editing in place.
  - **→ Architecturally that is what our pipeline already does** — spec → generated model — except ours is deterministic, patch-based, version-controlled and gated. **On reproducibility, diffability and gating this path is behind us; on convenience for one-off geometry it is ahead.**
- **Output is structured**, named components in the Outliner rather than a mesh soup, and triangulated but *"quad ready"* — not the pathological *"212 different diagonal angle cuts"* he says other AI modellers produce. A stated dimension check passed (a 24″ cube measured 2 ft on all three axes).

> [!WARNING]
> **⚠️⚠️ AND THE RULE THAT MATTERS: THE AGENT SILENTLY INVENTS UNSPECIFIED CONSTRUCTION VALUES.**
>
> Given a deliberately vague prompt, it supplied **5-inch wall thickness, a 9-ft ceiling and a "standard" 36×80-in door** — none of which he asked for — *"based on its knowledge of construction."* It also inserts **placeholder furniture** as extruded rectangles unless told not to.
>
> **This is the exact failure class this project has already built apparatus to refuse.** Our walls are 200/250 mm masonry with a **70 mm insulation layer taken from the drawing rather than from a heuristic** — `place_insulation.py` exists because *"a flat-centroid rule gets M6b wrong"*, and **M6b is deliberately left unsettled rather than guessed.** An agent that defaults a wall thickness would sail straight through that judgement.
>
> **The mitigating behaviour is that it reports its assumptions.** So the rule is: **an agent generating building geometry must be required to enumerate every value it supplied that the prompt did not, and a project like this one must treat each as a defect rather than a default.**

---

## What was routed, and where

Per standing rule 6, the transferable findings were routed in the same turn as extraction, to **[`00_Master/Drawing_Conventions_From_Practice.md`](../../00_Master/Drawing_Conventions_From_Practice.md)** — the page created by Round 1 for exactly this class of content (conventions about our own documentation, which the renovation taxonomy has no bucket for). Nothing went to `16_Legal_and_Regulations/`; no source here makes a regulatory claim, and all are US/UK-market anyway.

**Deliberately NOT routed**: every model-capability verdict in the batch. They are dated, vendor-adjacent, and will be wrong within months. The *evaluation methods* and the *cautionary rule* transfer; the scores do not.

## Open items

- **The two-point scale verification (§A.1) should be added to the `v0` reconstruction procedure** before that hand work starts, not after. It is cheap and it is the only registration check in the batch we do not already have.
- **Round 2 of this list is 5 videos** (Tier 2 above) and is a budget question, not a yield question. **`X1lnTEpy6PQ` is the single most useful next fetch** — it may name limits of the SketchUp adapter that the vendor's own video omits.
- **Nothing in this batch touches the `IfcRelConnectsPathElements` question.** That is with Gemini, and it is the more valuable thread of the two.
