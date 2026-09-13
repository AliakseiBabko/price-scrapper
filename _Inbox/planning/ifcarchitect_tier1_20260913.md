# @IfcArchitect Tier 1 — the annotated-sheet spine, 2026-09-13

**Eight videos from the 42-video channel triaged in [`bonsai_ifc_batch_20260913.md`](bonsai_ifc_batch_20260913.md) §2**, which assessed it as **the highest-relevance channel found so far** — a Bonsai/BlenderBIM channel and nothing else, whose spine is exactly the annotated-sheet chain the gap analysis marks `Adopt`.

## 1. ⚠️⚠️ This round is answering NAMED QUESTIONS, not extracting openly

**That is the difference from every previous round in this folder**, and it should set the filter. `Model_To_Drawing_Pipeline.md` and `Drawing_Conventions_From_Practice.md` closed with specific open items, and the reason this channel was ranked first is that its content maps onto them almost item-for-item.

| Question left open | Which video should bear on it |
| :--- | :--- |
| **⚠️⚠️ Does Bonsai place dimension text WITHOUT per-instance intervention?** *"This is what actually decides the annotated-sheet split."* | `VgvPk78IU0U` (2D drafting), `QTviOpqz1rw` (2D detail) |
| **⚠️⚠️ Is sheet assembly a GUI step, or scriptable?** — the gap analysis's own stated limit was *"requires Blender's graphical interface for practical sheet assembly unless driving headless Python API scripts with rigid layout rules"* | `HEb7fWJduXg` (page layout) |
| **⚠️ Can the annotation subsystem express a PROPORTIONAL dimension (`1/2`)?** Recorded as untested, and it decides whether the best convention in the vault is adoptable at all | `VgvPk78IU0U`, `QTviOpqz1rw` |
| **⚠️ Can a wall type be authored at an exact thickness?** — three sources showed the library QUANTISES (200 accepted for a 220 masonry wall), and our model carries exact `clear_mm` | `jTL3a6QwckA` (custom wall type) |
| **⚠️ How is line weight decided** — per layer, per element, per type? Our SVG pipeline has to decide this too | `dPWQbjaeoyo` (lineweights) |
| **⚠️ Phases**: we carry existing / demolished / new as **DXF layers**. IFC has a native concept | `_hADRIo-ma4` (custom phases) |
| **Section and elevation generation** — the two sheet types after plan | `r0ebxigzM6U` |
| **Title block** ⚠️⚠️ **and note what the title says: "with Inkscape".** If Bonsai's sheets are SVG under the hood, our SVG→PDF pipeline and Bonsai's may be far more compatible than the gap analysis's two-engine split assumed | `_vrVETTI5jQ` |

> **⚠️ A question a source does not answer is a result too, and will be recorded as one.** The previous round's most useful outcome was discovering that *text collision is manual in a purpose-built tool too* — a negative that qualified an adopt decision.

## 2. The eight, and why these eight

**All `en-orig`, verified per video from the caption manifest before fetching.**

| ID | Date | Len | Title | Era |
| :--- | :--- | :--- | :--- | :--- |
| `VgvPk78IU0U` | 2025-03-27 | 24m | Bonsai Beginner Project Pt 2 — **2D drafting** | **Bonsai** |
| `r0ebxigzM6U` | 2025-05-12 | 11m | Bonsai Beginner Project Pt 3 — **Section & Elevation** | **Bonsai** |
| `QTviOpqz1rw` | 2025-05-20 | 18m | Bonsai Beginner Project Pt 4 — **2D detail** | **Bonsai** |
| `HEb7fWJduXg` | 2022-12-13 | 17m | Step by Step Pt 5 — **Page Layout** | BlenderBim |
| `_vrVETTI5jQ` | 2023-03-27 | 8m | **Custom Titleblock** with Inkscape | BlenderBim |
| `dPWQbjaeoyo` | 2023-01-25 | 16m | **Lineweights** & more | BlenderBim |
| `jTL3a6QwckA` | 2022-11-02 | 5m | **Custom Wall Type** | BlenderBim |
| `_hADRIo-ma4` | 2024-02-12 | 20m | **Custom Phases** | BlenderBim |

**⚠️ Five of eight are BlenderBim-era, and that is deliberate, not sloppy.** The rule set last round is *the Bonsai-era recording supersedes the BlenderBim-era one **wherever both exist**, because capability verdicts date* — and **for these five no Bonsai-era re-record exists on the channel.** The Bonsai series is only four parts and **has no page-layout instalment**; titleblock, lineweights, custom wall type and phases were each recorded once. **Read the old one only where no new one exists** is exactly the condition here.

> ⚠️ **The dating caveat therefore applies with full force to the five**: UI paths, panel names and button locations are discarded on sight. **Only document semantics and IFC-level behaviour are extracted**, which is what was done for `PNoOyCHa_V0` last round.

**Deliberately NOT in Tier 1:**

- **`Jc896Sob2bU` (Bonsai Pt 1 — Modelling).** It is the current-era replacement for `PNoOyCHa_V0`, **but modelling is not the open question** — the vault now holds three modelling walkthroughs and the marginal fact yield would be low. **Queued, not processed.**
- **All 8 version-update videos, 3 install videos, the course trailer, the features reel and the channel-recommendation video** — release-note content is the purest form of the dating problem, a diff against a version we do not run.
- **The superseded BlenderBim 5-part series** (`kF2k_VW-yrQ`, `xWPLZK_WoS8`, `khGbssjtpeM`, `MH9MSI7FgVA`) and the two superseded floor-plan re-records — their Bonsai-era equivalents are in this round. **`HEb7fWJduXg` is taken from that series only because Part 5 has no successor.**

Outcome recorded below after processing.

---

## 3. Outcome

**All 8 fetched (zero failures) and read in full. 89 new facts, yield 11.1 per video.** No new page — `Model_To_Drawing_Pipeline.md` was the right home and grew from 181 to 345 lines, still under the 400 backstop with topical headings.

### The question-map, answered

| Question | Answer |
| :--- | :--- |
| **Does Bonsai place dimension text without per-instance intervention?** | **⚠️⚠️ NO — there is no auto-dimension at all.** A dimension is a polyline snapped by hand. **Corrects the premise behind the `Adopt` verdict.** |
| **Is sheet assembly a GUI step or scriptable?** | **Manual drag-and-drop in Inkscape — but the artefact is plain SVG, so a script can write it, which is what we already do.** |
| **Can the annotation subsystem express a proportional `1/2`?** | **⚠️⚠️ YES, and it needs nothing from Bonsai** — annotation text is `{{ }}` templating over model data. |
| **Can a wall type be authored at an exact thickness?** | **⚠️⚠️ YES, in five minutes — and the worked example is literally 220.** Corrects the earlier quantisation inference. |
| **How is line weight decided?** | **By CSS**, on a `cut` / `projection` / `text` / `annotation` / `material` taxonomy. ⚠️ And the conventions are **national** — his are South African. |
| **Phases vs our DXF layers?** | **`Pset_<Class>Common.Status`** — the same three values, as standard model data. **A demolition plan is a filter.** ⚠️ Do not copy his type-per-phase pattern. |
| **Section and elevation** | **One camera primitive parameterised by (direction, extent, scale)** — four sheet types, one generator. |
| **Title block** — "with Inkscape" | **⚠️⚠️ The hypothesis was right: it is an SVG template**, with the same `{{ }}` binding as the tags. |

### Handling and exclusions

- **⚠️⚠️ ALL EIGHT ARE ONE PRESENTER**, bringing the vault to **nine of his videos**. **A concentration warning is carried on every note and on both wiki pages**, alongside the **South African** jurisdiction flag he states twice himself.
- **Five of eight are BlenderBim-era, read deliberately** because no Bonsai-era re-record exists for page layout, title block, lineweights, wall type or phases. **All UI paths discarded; only document semantics and file formats retained.** ⚠️ The phases video carries the hardest dating caveat — he says the feature was *"not possible a year ago"* and his method will likely be superseded.
- **Three earlier notes CORRECTED IN PLACE** where this round overturned them: the "undocumented magic strings" are CSS class names, and the SVG+CSS reading is now confirmed rather than inferred.
- **No prices. No regulatory content.** The 220 mm, the roof-construction figures and the phase colours are all recorded as this practitioner's context and **none is transferred as a figure or a rule.**

## 4. What is left

1. **⚠️⚠️ Reproduce before relying** — the SVG/CSS directory layout, the phase workflow, the four re-sync steps and the `Ctrl+S` linkage, all against our installed **Bonsai 0.8.6-alpha260801**. **This is now the highest-value next action on this thread, and it is a LOCAL TEST rather than more sources.**
2. **⚠️ `Jc896Sob2bU` (Bonsai Pt 1 — Modelling)** — queued, still not processed. The current-era replacement for `PNoOyCHa_V0`; **low marginal yield**, since the vault holds three modelling walkthroughs and modelling is not an open question.
3. **The remaining `@IfcArchitect` items are low priority**: `2Q_wtBKa8Dc` (parametric doors & windows), `0wR5uAUwn8Y` (custom window), `dmWjQqyKL3U` (merge IFC libraries), `ClS-6taDO1M`, `ewvlodE1Nxg`, `50Skxd4ByN4`. **The 8 version-update videos, 3 install videos, course trailer, features reel and channel-recommendation video stay skipped.**
4. **`@blender3darchitect`'s named minority** is still unprocessed — **`tDOr7p35QUQ` (export drawings as SVG) first**, since it is our own output format from the other engine.
5. **Unchanged from earlier rounds**: `@RemPlanner` 5 of 6 lessons; `@k_dmitry` rounds 2–5; `@ConstructIQ` Tier 2.
