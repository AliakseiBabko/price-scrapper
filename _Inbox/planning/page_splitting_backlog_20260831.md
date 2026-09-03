# Layered-page splitting backlog (opened 2026-08-31)

## What was done

Three of the vault's largest pages were split, and the checker that flags them was recalibrated — after the splits themselves proved the old thresholds wrong.

| Page | Was | Became |
| :--- | :--- | :--- |
| `13_Surfaces_and_Finishes/Walls_and_Paint.md` | 921 lines, 48 sections | Guide (83) + Partition Construction & Wall Erection (189) + Wall Prep & Plastering (246) + Wallpaper & Paint Application (297) + Decorative & Specialty Finishes (190) |
| `13_Surfaces_and_Finishes/Flooring_Guide.md` | 865 lines, 42 sections | Guide (76) + Screed & Subfloor (252) + Flooring Material Selection (336) + Installation, Transitions & Baseboards (262) |
| `12_Engineering_and_Systems/analysis/Waterproofing_and_Plastering.md` | 815 lines, 23 sections | Parent (40) + Waterproofing Application & QC (180) + Plastering: Substrate Prep & Priming (258), Beacons & Geometry (187), Application & Drying (234) |

**Every section was moved verbatim, and that was verified mechanically per split**: 0 of 224 wikilinks lost, 0 of 113 headings lost, 0 of 2,209 non-empty content lines dropped. **A verbatim split cannot change a fact, a figure or an attribution** — so the only reviewable question left is whether a section landed on the right page, never whether the content survived.

**The Waterproofing page turned out to be two trades in one file** — waterproofing and plastering, joined only by both being wet-stage work. That is why it grew faster than any other detail page and why nothing on it was findable.

## ⚠️ Two findings that matter more than the splits

**1. The old thresholds punished a correct split.** After splitting, the flagged count went **up — 31 to 35**. Seven correctly-sized, single-topic result pages (234–336 lines) tripped the same 220-line rule their 900-line parents had tripped. A rule like that gives an author no achievable target short of atomising every page into stubs.

Recalibrated to **400/260 for detail pages, 500/350 for guides, with the cluster signal at 12+ sections rather than 3+**. At 3 sections the "clustered" threshold applied to essentially every real page, so the tool was a flat 220-line limit wearing a heuristic's clothes. Flagged count: **31 → 21**.

**2. The checker was structurally blind to the opposite failure.** `12_Engineering_and_Systems/analysis/Lighting_Design.md` has **26 top-level sections in 242 lines — 9 lines each**. It is not too long; it is **fragmented**, because every processing batch appended its own dated heading instead of adding to an existing section. It had been flagged "too long, split it" for weeks, and **splitting it would have made it strictly worse.** A FRAGMENTED check now names that case and says to merge.

**The two failure modes generate each other**: a threshold that forbids reasonably-sized pages pushes authors toward exactly the stub-per-batch habit that produces fragmentation. Both are now documented in `00_Master/wiki_page_format.md`.

## Remaining backlog — 20 pages

Ordered by size. **Section count is the better signal**: a page with 30+ sections carries that many independent topics regardless of its length.

| Lines | Sections | Page |
| ---: | ---: | :--- |
| 632 | 9 | `11_Budget_and_Planning/Budgeting_Guide.md` |
| 629 | 35 | `07_Bathroom/analysis/Tile_Selection_and_Layout.md` |
| 591 | 17 | `17_Design_and_Ergonomics/analysis/Sliding_Partition_Mechanisms.md` |
| 564 | 33 | `17_Design_and_Ergonomics/analysis/Decor_and_Finish_Selection_Technique.md` |
| 537 | 37 | `03_Kitchen/Kitchen_Furniture.md` |
| 527 | 18 | `17_Design_and_Ergonomics/analysis/Functional_Zoning_and_Furniture_Arrangement.md` |
| 483 | 17 | `12_Engineering_and_Systems/analysis/Soundproofing.md` |
| 442 | 20 | `13_Surfaces_and_Finishes/Ceilings_Guide.md` |
| 412 | 19 | `11_Budget_and_Planning/analysis/Budget_Tiers_Cheap_Optimal_Premium.md` |
| 388 | 15 | `09_Laundry_Room/analysis/Essential_Components_and_Layout.md` |
| 356 | 18 | `17_Design_and_Ergonomics/analysis/Curtains_and_Window_Treatments.md` |
| 344 | 26 | `07_Bathroom/analysis/Bathtub_and_Shower.md` |
| 336 | 16 | `13_Surfaces_and_Finishes/analysis/Flooring_Material_Selection.md` |
| 308 | 22 | `12_Engineering_and_Systems/analysis/Radiators_and_Convectors.md` |
| 297 | 12 | `13_Surfaces_and_Finishes/analysis/Wallpaper_and_Paint_Application.md` |
| 285 | 16 | `12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md` |
| 270 | 13 | `17_Design_and_Ergonomics/analysis/Neutrals_and_Earth_Tone_Palettes.md` |
| 267 | 12 | `12_Engineering_and_Systems/analysis/Fresh_Air_Ventilation_and_Ducting.md` |
| 265 | 16 | `17_Design_and_Ergonomics/analysis/Color_Selection_Process_and_Testing.md` |
| 262 | 15 | `13_Surfaces_and_Finishes/analysis/Flooring_Installation_and_Baseboards.md` |

Plus one FRAGMENTED page, which is a different job: `12_Engineering_and_Systems/analysis/Lighting_Design.md`.

## Priority for the next pass

**Split next — worst by section count, which is the signal that matters:**

1. `03_Kitchen/Kitchen_Furniture.md` (37 sections, 537 lines) — a guide page carrying detail it should have delegated long ago.
2. `07_Bathroom/analysis/Tile_Selection_and_Layout.md` (35 sections, 629 lines) — the largest remaining detail page.
3. `17_Design_and_Ergonomics/analysis/Decor_and_Finish_Selection_Technique.md` (33 sections, 564 lines).

All three should split cleanly along the same verbatim-move pattern, with the same mechanical link/heading/line verification afterwards.

**⚠️ Merge, don't split — and do it by hand:** `Lighting_Design.md`. Merging 26 stub sections means *rewriting prose*, which is the one operation in this whole area that can actually lose or distort a fact. It must be done deliberately and checked against the source notes, not scripted the way the splits were.

**Probably fine as they are:** most of the 262–300 band, several of which are the freshly-split pages above. If a review agrees they are coherent single-topic pages, record them in `tools/page_size_exceptions.json` with the reason rather than splitting them further. **Do not add exceptions to make the number go down** — the count is only useful while every entry in it is a real judgement.

## Note on `Budgeting_Guide.md`

632 lines but only **9 sections** — the one page in the list where the line count is high and the topic count is not. It may genuinely be one long thing rather than nine, so it needs reading before any split is designed. Do not treat it as mechanical.

## Update after Кузина Round 1 (2026-08-31, same day)

Three of this backlog's pages were touched by the Кузина Round 1 intake. **Net effect on the fragmentation count: slightly better, deliberately.**

- **`Lighting_Design.md` — the merge-don't-split page above.** Round 1 added three sources' worth of lighting content (dining-pendant sizing, the chandelier-as-decor convergence, and the Реньжин mechanisms). **Rather than appending three more dated top-level headings — exactly the behaviour that produced this page's problem — they were consolidated into one top-level section with `###` subsections, and the page went from 28 to 27 top-level sections while gaining content.** The underlying merge job is untouched and still owed by hand.
- **`Kitchen_Furniture.md`** (#1 to split) gained two sections and one subsection. **The subsection was deliberately nested under the existing fridge-niche section** rather than added at top level, but the two new top-level sections do make the split job marginally larger. They are self-contained and will move cleanly.
- **`Functional_Zoning_and_Furniture_Arrangement.md`** gained one top-level section with `###` subsections, and is now newly flagged for splitting.
- **`Flooring_Installation_and_Baseboards.md`** gained content as a **`###` subsection nested under the existing threshold-sealing section**, adding no top-level heading — that page's flag is unchanged by this round.

**Convention worth generalising from this round**: when a batch adds several sources to an already-fragmented page, give the whole batch one top-level heading and nest per-source content beneath it. It keeps the section count flat and it groups material that a future merge pass would want together anyway.

## Update after Кузина Round 2 (2026-09-01)

Round 2 added substantial content to three pages already on this backlog, and created a fourth candidate. **Fragmentation was avoided — every addition went under one top-level heading per source with `###` subsections, per the convention adopted after Round 1 — but the *size* problem got worse on two pages.**

- **`17_Design_and_Ergonomics/analysis/Decor_and_Finish_Selection_Technique.md`** — was #3 on the split list at 33 sections / 564 lines; **now 36 sections / 636 lines.** It gained the ornament scale-hierarchy rules, the wood-finish rules and the metal-finish rules. **This is now the most urgent split on the list, and it has an obvious seam: pattern/ornament combination, wood finishes, and metal finishes are three coherent topics that arrived together and would separate cleanly.**
- **`17_Design_and_Ergonomics/analysis/Functional_Zoning_and_Furniture_Arrangement.md`** — **now 23 sections / 664 lines**, the longest detail page in this folder. It absorbed the Round 1 planning method, the low-ceiling furniture rules, the irregular-geometry material and the small-apartment box technique. **Newly flagged; a plausible seam is planning *method* versus room-shape *remedies*.**
- **`13_Surfaces_and_Finishes/Ceilings_Guide.md`** — **now 486 lines / 21 sections**, over the 350-line guide threshold. The low-ceiling section is self-contained and is the natural first `analysis/` page to carve out.
- **`Neutrals_and_Earth_Tone_Palettes.md`** and **`Doors_and_Trim.md`** also grew but remain coherent single topics.

**⚠️ Neither round attempted a split.** Splitting is the deliberate, verify-afterwards operation this file already describes, and doing it mid-intake would have mixed two kinds of change in one commit. **Recorded here rather than silently deferred.**

## Split pass 2, 2026-09-01 — the three pages Кузина Rounds 1–3 had pushed over

The three worst pages on the list were split, and **for the first time the flagged count went down as a result of splitting**: **23 → 21**, across 209 → 219 pages. That is the recalibrated thresholds doing exactly what they were recalibrated for — none of the ten pages created here trips the checker.

| Page | Was | Became |
| :--- | :--- | :--- |
| `17_Design_and_Ergonomics/analysis/Decor_and_Finish_Selection_Technique.md` | 691 lines, 38 sections | Parent (333) + Combining Finishes — Wood, Metal and Gloss (97) + Accent Walls & Pattern Combination (98), with furniture content moved into `14_Furniture/analysis/Loose_Furniture_Selection_Principles.md`, panel content into `13_Surfaces_and_Finishes/analysis/Decorative_Wall_Panels.md`, and a full curtain rule set into the curtains page |
| `17_Design_and_Ergonomics/analysis/Curtains_and_Window_Treatments.md` | 439 lines, 22 sections *(after receiving the above)* | Parent (118) + Curtain Fabric, Colour & Pattern (117) + Curtain Sizing, Mounting & Hardware (217) |
| `17_Design_and_Ergonomics/analysis/Functional_Zoning_and_Furniture_Arrangement.md` | 696 lines, 24 sections | Parent (280) + Whole-Home Planning Method (220) + Difficult Room Shapes & Proportion Remedies (143) + `14_Furniture/analysis/Household_Storage_and_Decluttering_Method.md` (74) |
| `07_Bathroom/analysis/Tile_Selection_and_Layout.md` | 690 lines, 36 sections | Parent (231) + Tile Installation, Sequencing & Acceptance (228) + Tile Cutting, Handling & Special Formats (160) + Tile Grout Selection & Protection (88) |

**Every section moved verbatim, verified mechanically per split: 0 non-empty content lines lost across all four** (532, 376, 560 and 547 original lines respectively, each checked line-by-line against the union of the resulting files). A verbatim split cannot change a fact, a figure or an attribution — the only reviewable question left is whether a section landed on the right page.

### ⚠️ Two filing errors surfaced by the split, both fixed

**1. A full curtain rule set was living on a finishes page.** `Decor_and_Finish_Selection_Technique.md` carried 52 lines of Kodolov's curtain-rod, length, fullness-coefficient and fabric-print rules under its own heading, while `Curtains_and_Window_Treatments.md` existed and did not have them. Moved. **This is the failure mode the splits keep exposing: content is filed where the batch that produced it happened to be working, not where a reader would look for it.**

**2. Four unrelated Anuta Vlady rules had been wedged beneath that curtain heading** since 2026-08-25 — mixing classic and contemporary at the piece level, sourcing upholstery colour from a rug's full palette, a venetian-blind maintenance comparison, and combining two small decor pieces into one frame. They were under a curtain heading, on a finishes page, and none of them is about curtains. Moved to the furniture page with the blind point cross-referenced from the curtains page.

### What is still flagged, and the judgement on each

**Deliberately left flagged rather than excepted:**

- **`Decor_and_Finish_Selection_Technique.md` (333 lines, 21 sections)** — much improved, but 21 sections is still a real topic count. A future pass could carve out the refinishing/disguise material (the Dubai case is 47 lines on its own) and the Petrishin practicality rationale (48). **Not done here because the page is now coherent and the marginal gain is small** — this is the point past which splitting starts producing stubs.
- **`Functional_Zoning_and_Furniture_Arrangement.md` (280 lines, 12 sections)** — sits exactly on the cluster threshold. Its largest remaining block is the 77-line partition inventory, which overlaps [[17_Design_and_Ergonomics/analysis/Sliding_Partition_Mechanisms|Sliding Partition Mechanisms]] (591 lines, still #1 on the remaining list). **Those two should be reconciled together, not split apart separately** — that is a merge-and-redistribute job, not a split.

**No exceptions were added to `tools/page_size_exceptions.json`.** The count is only useful while every entry in it is a real judgement, and neither of the two above is settled enough to record as "fine forever."

### Remaining backlog — 21 pages, updated priority

**Split next:**

1. `03_Kitchen/Kitchen_Furniture.md` (568 lines, **38 sections**) — now the worst page in the vault by section count, and a *guide* page carrying detail it should have delegated long ago. It was #1 on the previous pass's list and is still untouched.
2. `12_Engineering_and_Systems/analysis/Soundproofing.md` (483, 17) and `13_Surfaces_and_Finishes/Ceilings_Guide.md` (486, 21) — the two largest remaining after that.
3. `17_Design_and_Ergonomics/analysis/Sliding_Partition_Mechanisms.md` (591, 17) — **but see the note above: reconcile with the zoning page's partition inventory rather than splitting in isolation.**

**⚠️ Still owed by hand, still not done:** the `Lighting_Design.md` merge. It is now **390 lines / 31 sections** — it has grown in both dimensions since it was first identified as the fragmented case, because three intake rounds each added content to it. **Merging 31 stub sections means rewriting prose, which is the one operation in this area that can lose a fact**, so it must be done deliberately and checked against the source notes. It is the oldest unpaid debt on this list.

**Convention confirmed again**: the batch-appends-its-own-dated-heading habit is what produces both failure modes. The one-top-level-heading-per-source-with-`###`-subsections rule adopted after Кузина Round 1 held through Rounds 2 and 3 and is why these three pages were *oversized* rather than *fragmented* — which is the tractable problem of the two.

## ⚠️ The Lighting_Design merge — done, 2026-09-01. The oldest debt on this list is paid.

**This was a merge, not a split, and it is the one operation here that can actually lose a fact** — it means rewriting prose rather than moving it. It was identified as owed on 2026-08-31 and deferred three times.

`12_Engineering_and_Systems/analysis/Lighting_Design.md` went from **390 lines / 31 top-level sections** (12 lines apiece — the fragmentation signature) to **385 lines / 9 sections**, organised by *decision* rather than by the batch that happened to produce each fact:

1. Planning the scheme — scenarios, layers, sequence · 2. Colour temperature · 3. Fixture types and buying checks · 4. Chandeliers and pendants · 5. Glare, shadow, and where light must not go · 6. LED strip and linear lighting · 7. Switching and controls · 8. Room by room · 9. (Daylight — moved out, see below)

### How it was verified, given that prose was rewritten

A verbatim check is impossible here, so three mechanical checks plus a manual pass:

- **All 33 wikilinks preserved, one for one — zero lost.** Every source citation still resolves.
- **All numeric tokens preserved**, with the only diffs being formatting normalisations verified by hand (`12V` → `12 V`, `2700-3500K` → `2700–3500 K`, hyphens to en-dashes).
- **A Russian-phrase diff** to catch dropped quotations, which is what actually found the omissions below.

**⚠️ The check earned its keep — the first draft of the merge dropped three things, and they were restored before commit:**

1. **The `promotional_ratio: medium` flag on the Реньжин podcast.** He plugs his own studio with a promo code and argues throughout for hiring a lighting designer, which is his business. The merged draft cited him heavily and lost the disclosure. **This is the most serious kind of loss possible in this operation** — the facts survived, the reader's ability to weight them did not. Restored as a warning callout in the page header.
2. The gloss «коэффициент цветопередачи» on CRI.
3. The words *"по физиологии"* inside a direct quotation.

**The lesson for the next merge: diff the quotations and the promotional/confidence flags specifically.** A link-count check would have passed all three of those.

### What the merge revealed that fragmentation had hidden

- **A coloured/RGB strip section existed twice, near-verbatim, from the same source** — once under its own heading and once as a trailing paragraph beneath an unrelated track-switching section. Neither knew about the other. Now recorded once.
- **The equal-pendant-heights rule, the worktop-shadow mechanism and the bedside-reading-light guidance each appeared in three to five places**, cross-referencing each other in circles. Now stated once each, with the genuinely different angles nested underneath.
- **Two real disagreements were surfaced that the dated-heading layout had kept apart**: Kruglov's "minimum three scenarios" against Реньжин's *"в 45 м² это называется выключатель"*, and the same 60° beam angle treated as a *defect* in the kitchen source and a *virtue* in the bedroom source. Both are now recorded as disagreements rather than as adjacent unrelated entries.

### And a filing correction the merge forced

**Daylight was moved off the page entirely**, to `17_Design_and_Ergonomics/analysis/Daylight_and_Natural_Light.md` (34 lines). It had been routed onto Lighting Design earlier the same day, correctly flagged as "the first content on this page that is not artificial light" — **and that flag was the argument against it.** Daylight involves no circuits, no fixtures and no electrical planning, and the page lives in `12_Engineering_and_Systems`. A pointer section remains.

**Flagged count: 21 → 20.** Neither Lighting Design nor the new daylight page is flagged.

### What is still owed

Nothing on the *merge* side — this was the only page identified as fragmented. The remaining backlog is all splits, unchanged from the pass above, with `03_Kitchen/Kitchen_Furniture.md` (568 lines / 38 sections) as the clear next target.

## Update after Кузина Round 4 (2026-09-01)

**Flagged count 20 → 21.** `17_Design_and_Ergonomics/analysis/Color_Harmony_and_Combination_Rules.md` crossed the threshold (185 → **299 lines, 13 sections**) by absorbing the round's colour-theory material. **One page in, none out.**

> [!NOTE]
> **⚠️ A correction to the Round 4 commit message, which claimed the flagged count was "unchanged at 20." It went to 21.** The count was checked after the commit was written and the discrepancy is recorded here rather than left standing. Nothing else in that message is affected.

**The routing convention held**, which is the thing worth measuring: twelve pages received content and **section counts stayed flat**, because the whole batch went under one top-level heading per page with `###` per source. **No page became more fragmented.** The four pages now in the 299–349 band grew in *depth*, not in topic count.

| Page | Was | Now | Note |
| :--- | ---: | ---: | :--- |
| `Color_Harmony_and_Combination_Rules.md` | 185 / 12 | **299 / 13** | **Newly flagged.** One new heading for the whole batch |
| `Color_Selection_Process_and_Testing.md` | 265 / 16 | **349 / 17** | Already flagged. **Now the vault's main paint-selection procedure** |
| `Neutrals_and_Earth_Tone_Palettes.md` | 288 / 13 | **348 / 14** | Already flagged |
| `Wallpaper_and_Paint_Application.md` | 297 / 12 | **340 / 13** | Already flagged |

### Judgement on the four — do not split yet

**All four are coherent single-topic pages that grew because a good round landed on them, which is the case this backlog explicitly says not to atomise.** Specifically:

- **⚠️ `Color_Harmony_and_Combination_Rules.md` should be watched, not split.** At 13 sections it is at the cluster threshold, and its new content is one argument — how much of each colour — spanning a Perspectives block, a replacement model and a flagged error. **Splitting the dispute from the model it produced would make both harder to read.** Revisit if it takes another round's worth.
- **`Color_Selection_Process_and_Testing.md` at 349/17 is the one to watch hardest.** It is now carrying two distinct things: **a paint-selection procedure** and **a general colour-decision process**. **That is a real seam and a future split should follow it** — but the procedure only just landed and splitting it in the same pass would mix two kinds of change in one commit, which is the mistake this file already warns against.

**No exceptions added.** Same reasoning as the 2026-09-01 split pass: the count is only useful while every entry in it is a real judgement, and none of these four is settled enough to record as fine forever.

### Still owed

Unchanged from the split pass, and **the merge debt is now clear** — `Lighting_Design.md` was merged on 2026-09-01 and no other page has been identified as fragmented. The remaining backlog is all splits, with **`03_Kitchen/Kitchen_Furniture.md` (568 lines / 38 sections) still the worst page in the vault by section count** and still untouched across three passes.

## Update after Кузина Round 5 (2026-09-01)

**Flagged count 21 → 22, then back to 21 with the first exception in this file's history.**

**⚠️ The page that crossed is `12_Engineering_and_Systems/analysis/Lighting_Design.md` — the one merged earlier the same day.** It went **385 → 410 lines** when Round 5 added three dissents (dimmers as an *interface* rather than as a function; a **third distinct** cove-lighting objection, that the channel is unreachable and never cleaned; and a too-much-light-versus-too-little ranking) plus two pendant items from the focal-point source.

**It is 10 lines over a flat 400-line threshold, with 11 top-level sections — below the 12-section cluster trigger.**

### ⚠️ An exception was added, and this is the first entry in `tools/page_size_exceptions.json`

**The reasoning, recorded because a first precedent sets how the file gets used:**

- **The page's section structure was the deliverable of a deliberate merge** performed section by section hours earlier, taking it from 31 fragmented sections to 9. **Splitting it now would undo work done to fix the opposite failure.**
- **It cannot shrink without losing content**, and the content added was corrections to material already on the page, which is exactly where it belongs.
- **`00_Master/wiki_page_format.md` states that line count is the weakest of the available signals.** A 410-line, 11-section page organised by decision is not the problem this checker exists to catch.
- **⚠️ The exception names the condition for revisiting: if the section count reaches 12, review again — that would mean fragmentation is returning, and for this page that is the signal that matters, not the line count.**

**This does not soften the standing rule.** The four pages left flagged in the Round 4 update remain flagged and un-excepted, because none of them is settled the way this one is. **An exception is for a page whose shape has been deliberately decided and reviewed — not for a page that is merely inconvenient to split.**

### Otherwise unchanged

**18 pages received Round 5 content and section counts stayed flat**, one top-level heading per page for the whole batch. **`13_Surfaces_and_Finishes/analysis/Material_and_Finish_Tiers.md` more than doubled (47 → 105) and is still well clear of the threshold** — it was the natural host for the practical-versus-good table and had the room.

**Still owed and still untouched across four passes: `03_Kitchen/Kitchen_Furniture.md` (568 lines / 38 sections), the worst page in the vault by section count.**

## Update after the Михайловская mini-round (2026-09-01)

**Flagged count 21 → 22.** `07_Bathroom/analysis/Planning_and_Layout.md` crossed at **274 lines / 19 sections**.

**⚠️ No exception added, and the contrast with the Lighting_Design entry is the point.** That page was excepted at 410 lines / **11** sections — over a flat line threshold with a topic count below the cluster trigger, on a structure that had just been deliberately designed. **This one is at 19 sections, which is a genuine topic count and exactly the signal the checker exists to catch.** An exception here would be using the file to make a number go down.

**It is now a real split candidate**, and the seam is visible: the page carries **(a) approvals and expansion direction, (b) layout method and dimensions, (c) fixture placement and clearances, and (d) access for servicing** — the last of which arrived in this round and is a distinct decision from the rest.

**Priority: below `03_Kitchen/Kitchen_Furniture.md` (568 lines / 38 sections), which remains the worst page in the vault by section count and is now untouched across five passes.**

**Otherwise unchanged.** Twelve pages received content and section counts stayed proportionate; `12_Engineering_and_Systems/analysis/Wall_Hung_Toilet_Installation.md` grew from 21 to 57 lines and is nowhere near the threshold.

## 2026-09-02 pass — Безверхая Round 1 (6 videos, 10 pages touched)

**One page crossed the threshold for the first time in this round, and it is a genuine new entry rather than drift:**

- **`13_Surfaces_and_Finishes/analysis/Decorative_and_Specialty_Wall_Finishes.md` — now 292 lines / 21 top-level sections**, newly over the 260-line detail-page threshold. This round added the polyurethane-moulding shrinkage mechanism and the natural-vs-acrylic lime distinction. **The visible seam: the page now mixes (a) decorative plaster and microcement, (b) moulded decor and mouldings, (c) accent-wall and trend critique, and (d) specific wall-material identification.** Moulded decor (лепнина) is the cleanest candidate to lift out — it is a distinct product family with its own materials, failure modes and installation economics, and it is currently split across this page and `Wallpaper_and_Paint_Application.md`'s two-tone painting technique.

**Already-listed pages that grew this round and remain listed, unchanged in priority**: `13_Surfaces_and_Finishes/analysis/Flooring_Material_Selection.md` (now carries six multi-material comparisons plus three Perspectives blocks — **the strongest split candidate of the three, and the Perspectives blocks are a natural seam**), `.../Wallpaper_and_Paint_Application.md`, and `12_Engineering_and_Systems/analysis/Lighting_Design.md`.

**`03_Kitchen/Kitchen_Furniture.md` (627 lines / 42 sections) remains the worst page in the vault and is now untouched across six passes.**

## 2026-09-02 second pass — Безверхая Round 2 (8 videos, 16 pages touched)

**Flagged-page count went 28 → 29. One page crossed the threshold in this round, and one already-flagged page was never entered in this file.**

- **⚠️ NEW: `11_Budget_and_Planning/Renovation_Sequence.md` — now 351 lines against the 350-line guide-page threshold**, crossed by this round's nine-steps-before-the-builders block. **It is one line over, so this is a watch item rather than an action item.** **The seam, if it is ever split, is clean and worth recording now while it is obvious: the page holds (a) the pre-site order — acceptance, constraints, layout, storage, engineering, design, documentation, budgeting, procurement — and (b) the on-site build order, rough-stage QC and acceptance checklists.** Those are two different audiences at two different times; the pre-site half arrived whole in this round and did not exist before it.
- **⚠️ Already flagged by the tool but never listed here: `03_Kitchen/analysis/General_Dos_and_Donts.md` — now 290 lines / 23 sections** (was 266 / 21 before this round). Added this round: the RUSSIAN kitchen-legality block and the cooking-habits specification rule. **Recording it now so the omission does not persist.** Its own seam: kitchen *legality and planning constraints* versus kitchen *use and specification advice*.

**Already-listed pages that grew this round and remain listed, priority unchanged**: `07_Bathroom/analysis/Planning_and_Layout.md` (now 355 lines — **this round added the largest single block on the page, and it is the strongest split candidate of the group; the natural seam is dimensional ergonomics versus approvals versus servicing access**), `07_Bathroom/analysis/Tile_Selection_and_Layout.md` (290), `11_Budget_and_Planning/analysis/Budget_Tiers_Cheap_Optimal_Premium.md` (440), `12_Engineering_and_Systems/analysis/Soundproofing.md` (493 — **the largest flagged page touched this round**), `12_Engineering_and_Systems/analysis/Radiators_and_Convectors.md` (319).

**⚠️ `08_WC/analysis/Dos_and_Donts.md` is the opposite problem and worth noting here for balance**: this round gave that folder its first dimensional content, and the page is still well short of any threshold. **The folder remains the thinnest room folder in the vault** — one analysis page against `07_Bathroom`'s sixteen.

**`03_Kitchen/Kitchen_Furniture.md` (627 lines / 42 sections) remains the worst page in the vault and is now untouched across seven passes.**

## 2026-09-02 third pass — FLAT / @flat_interio Round 1 (6 videos, 5 pages touched)

**Flagged-page count unchanged at 29 — no page crossed a threshold in this round.** Two already-flagged pages grew materially and their seams are now clearer:

- **⚠️ `03_Kitchen/analysis/General_Dos_and_Donts.md` — 290 → 351 lines in one day**, having taken both Безверхая's RUSSIAN kitchen-legality block (Round 2) and FLAT's ten-mistakes block. **It is now carrying three distinct things and the seam is obvious: (a) kitchen legality and planning constraints, (b) working dimensions and specification minima, (c) use-and-taste advice.** **This is the page to split next after the two named below** — it went from "flagged but proportionate" to genuinely mixed in a single session.
- **`11_Budget_and_Planning/Renovation_Sequence.md` — 351 → 382 lines.** The pre-site/on-site seam recorded in this file earlier today is now more pronounced, because FLAT's furniture-coordination block belongs firmly on the pre-site side.
- **`11_Budget_and_Planning/analysis/Budget_Tiers_Cheap_Optimal_Premium.md` — 440 → 472 lines**, but the growth is the page's own Furniture section finally acquiring absolute figures, which is a gap being filled rather than drift.

**⚠️ Worth recording as the opposite of a problem: `14_Furniture/analysis/Furniture_Dispute_Legal_Recourse.md` was 12 lines and is now 47** — the prevention half (contract, specification, verification, prepayment) added upstream of the existing recourse content. **`14_Furniture/` remains thin relative to its importance to this project**, and this round was the first substantial addition to it in some time.

**`03_Kitchen/Kitchen_Furniture.md` (627 lines / 42 sections) remains the worst page in the vault and is now untouched across eight passes** — notably, this round added kitchen-furniture material to two *other* pages rather than to it, which is the right call for now but widens the gap between where the content is and where a reader would look for it.

## 2026-09-02 fourth pass — FLAT Round 2 (5 videos, 7 pages touched)

**Page-size check after this round: no page crossed a threshold that had not already.** Two notes:

- **⚠️ `03_Kitchen/analysis/Furniture_Facade_Materials.md` has taken two large blocks in one day** (FLAT Round 1's substrate/facing taxonomy and Round 2's part-2 additions) and is now the vault's densest single-topic materials page. **It is still under the detail-page threshold and the content is genuinely one topic, so this is a watch item rather than a split candidate** — but if it takes another facade source it should be split by **substrate / facing / hardware-interaction**, which is how both FLAT videos are themselves organised.
- **`11_Budget_and_Planning/Budgeting_Guide.md` (already the second-worst page in the vault by line count) took the three-way allocation split.** That page's problem is unchanged in kind — a long tail of appended live-intake benchmarks — and this addition is a framing section rather than another benchmark, so it does not worsen the seam. **The seam remains: framing and categories, versus the benchmark ledger.**

**`03_Kitchen/analysis/General_Dos_and_Donts.md` — flagged in the previous pass as having gone from proportionate to genuinely mixed in a single session — took a third block this round and remains the page to split next after the two named earlier.** It now carries kitchen legality, working dimensions, use-and-taste advice, and hardware/mechanism scepticism.

**`03_Kitchen/Kitchen_Furniture.md` (627 lines / 42 sections) remains the worst page in the vault and is now untouched across nine passes** — and the gap noted last pass has widened: this session added substantial kitchen-furniture material to three other pages while leaving it alone.

## 2026-09-02 fifth pass — FLAT Round 3 (3 videos, 7 pages touched), channel closed

**Page-size check: the flagged count went 29 to 31 — TWO pages crossed the detail-page threshold in this round**, both of them ones this round wrote to: **`03_Kitchen/analysis/Furniture_Facade_Materials.md` (now 314 lines) and `07_Bathroom/analysis/Fixtures_Mixers_and_Sinks.md` (now 274 lines).** Four notes:

- **⚠️ `03_Kitchen/analysis/Furniture_Facade_Materials.md` has now taken THREE large blocks from one channel in a single day** (Round 1's substrate/facing taxonomy, Round 2's part-2 additions, Round 3's four-year field evidence). **It is now the vault's densest single-topic materials page and the previous pass's watch item has matured into a real split candidate.** **The seam is unchanged and still obvious: substrate / facing / hardware-interaction — which is how the source videos are themselves organised.** **Split this before it takes another source.**
- **⚠️ The opposite result, and it is the round's point: `02_Hallway/analysis/Common_Mistakes.md` went from a 54-line single-entry stub to a page with real content.** **`02_Hallway` and `01_Entrance` were named as under-served rooms when Round 3 was scoped, and selecting a source for them worked.** Neither is near a threshold; **`02_Hallway` remains thin in absolute terms (three analysis pages) and is still worth feeding.**
- **⚠️ NEW: `07_Bathroom/analysis/Fixtures_Mixers_and_Sinks.md` — now 274 lines, newly over the threshold**, crossed by this round's four-year vanity-top failure finding. **The page is coherent by subject (mixers, toilet, sinks) but has accumulated a Perspectives block, finish/marking content, sizing rules and now a durability case.** **Lower priority than the facade page above — it is barely over and the content is genuinely one topic — but worth watching.**
- **`11_Budget_and_Planning/Budgeting_Guide.md` took a second addition today** (the 56 m² priced case, after Round 2's allocation split). **Its seam is unchanged — framing and categories versus the benchmark ledger — and this addition belongs to the ledger half, so it does worsen the imbalance slightly.** Still second-worst in the vault by line count.

**`03_Kitchen/Kitchen_Furniture.md` (627 lines / 42 sections) remains the worst page in the vault and is now untouched across ten passes.** **Three separate sessions today added kitchen-furniture material to other pages while leaving it alone — the content-versus-location gap is now the largest it has been.**

## 2026-09-02 — ⚠️ RESOLVED: `03_Kitchen/Kitchen_Furniture.md`, the vault's worst page, converted to the layered shape

**The page named in this file across ten consecutive passes as "the worst page in the vault, untouched" is done.** Converted at the user's explicit direction after it was flagged to them at the end of the FLAT Round 3 report.

**Before**: 627 lines, 43 top-level sections. **After**: an 80-line guide plus seven detail pages.

| | Lines |
| :--- | :--- |
| `Kitchen_Furniture.md` (guide) | **80** (was 627) |
| `analysis/Layout_Sizing_and_Ergonomics.md` | 173 |
| `analysis/Storage_and_Hardware.md` | 135 |
| `analysis/Worktops_and_Backsplash.md` | 98 |
| `analysis/Appliance_Integration.md` | 70 |
| `analysis/Cabinet_Assembly_Technique.md` | 66 |
| `analysis/Kitchen_Cost_and_Priorities.md` | 59 |
| `analysis/Kitchen_Lighting.md` | 54 |
| `analysis/Kitchen_Furniture_Source_Notes.md` | 30 |
| `analysis/Kitchen_Furniture_Change_Log.md` | 12 |

**⚠️ The diagnosis that justified splitting rather than merging.** This file's own 2026-08-31 lesson is that a page can fail by being *fragmented* — many dated headings with little under each — and that splitting such a page makes it worse. **This was the other failure mode.** The tell: **`## Source Notes` sat at line 512 and `## Change Log` at 539, with ten further content sections below them** — every batch had appended beneath the page's own footer, and the 43 headings were genuinely distinct sub-decisions (sizing, appliance integration, assembly technique, storage hardware, worktops, lighting, cost) rather than one decision sliced up.

**⚠️ The split was mechanical, and verified.** All content was moved **by line range, byte-for-byte** — the convention's requirement is "move/reorganize existing prose rather than re-deriving, so no fact gets lost or silently altered," and a line-range extraction guarantees that literally. **A coverage assertion confirmed every source line was assigned to exactly one destination, and an independent check confirmed all 456 non-blank content lines arrived, none duplicated.** Only seven lines were deliberately dropped: the old title, two blanks, one composite heading whose two bullets went to different pages (each given a new heading in its destination), and the now-duplicate `## Source Notes` / `## Change Log` headings on the two footer pages, whose new H1 titles say the same thing. **The only newly-written prose is the guide itself, the per-page headers and the cross-references.**

**⚠️ The checker's own recalibration held up.** This file's 2026-08-31 entry records that three correct splits *raised* the flagged count 31→35, because well-sized results tripped the same threshold their oversized parents had, and that the thresholds were recalibrated as a result. **This split took the count 31→30, and none of the seven new pages is flagged.** First confirmation that the recalibrated thresholds reward a correct split rather than punishing it.

**Inbound links**: 66 files reference the page. **13 live wiki cross-references that named specific moved content were repointed** at the correct detail page — including five that named a section by title ("Budget Kitchen: What to Cut vs. Never Cut", "2026-Trends section"), exactly the fragile pattern this convention warns about. **No `§N` anchors existed, so nothing was silently broken.** **`_Sources/` notes, `processed_sources.csv` `target_docs`, `_Inbox/planning/` files, the knowledge-store Change_Log and two page-level Change Log entries were deliberately left as written** — historical records of what was true when written, per the precedent set by the 2026-08-30 `_supporting` dissolution. `03_Kitchen/Kitchen_Index.md` gained a page list.

**One deviation from the shape presented to the user, stated plainly**: the illustration showed six detail pages; **seven were created**, because the cost/priorities content (three sections, ~50 lines: cost tricks, what-to-cut-vs-never-cut, priced add-ons) is a genuinely distinct sub-decision and folding it into a topical page would have buried it. Per this convention's own test — decompose by sub-decision, not line count — it earns its own page.

### ⚠️ What is now the worst page in the vault

With Kitchen Furniture resolved, the standing list re-orders:

1. **`11_Budget_and_Planning/Budgeting_Guide.md` — 878 lines.** Now the clear worst by line count, and it grew twice on 2026-09-02. **Its seam is different in kind and has been stable across five passes: framing and cost categories versus an indefinitely-growing ledger of live-intake benchmarks.** The benchmarks are the half that should move.
2. **`03_Kitchen/analysis/General_Dos_and_Donts.md` — 380 lines / 25 sections.** Took three separate blocks on 2026-09-02 and is genuinely mixed (kitchen legality, working dimensions, use-and-taste advice, hardware scepticism). **Now the most mixed page in the vault, and the natural next conversion** — note it already sits in an `analysis/` folder alongside a working layered structure, so it can be split without a guide-page conversion.
3. **`03_Kitchen/analysis/Furniture_Facade_Materials.md` — 314 lines.** Took three blocks from one channel today. **Seam: substrate / facing / hardware-interaction**, which is how the source videos are themselves organised.
4. `12_Engineering_and_Systems/analysis/Soundproofing.md` — 493 lines, coherent by topic.
5. `07_Bathroom/analysis/Planning_and_Layout.md` — 355 lines, seam is dimensional ergonomics versus approvals versus servicing access.

## 2026-09-02 (second pass, same day) — the rest of the worst-page list

Continuation of the Kitchen Furniture conversion, at the user's direction. **Flagged count 30 → 27; three of the five targets cleared the threshold; no new page is flagged.**

| Page | Before | After | Outcome |
| :--- | ---: | ---: | :--- |
| `11_Budget_and_Planning/Budgeting_Guide.md` | 878 | **495** | ⚠️ still flagged — see below |
| `03_Kitchen/analysis/General_Dos_and_Donts.md` | 380 / 25 sections | **250 / 6** | cleared |
| `12_Engineering_and_Systems/analysis/Soundproofing.md` | 493 | **216** | cleared |
| `07_Bathroom/analysis/Planning_and_Layout.md` | 355 | **245** | cleared |
| `03_Kitchen/analysis/Furniture_Facade_Materials.md` | 314 | **314** | ⚠️ deliberately left — see below |

**New pages**: `Cost_Benchmarks_Live_Intake.md` (311) · `Design_Services_and_Fees.md` (120) · `Kitchen_Materials_and_Finish_Critiques.md` (107) · `Kitchen_Gadgets_and_Mechanisms.md` (64) · `Bathroom_Design_and_Palette.md` (70) · `Bathroom_Regulation_and_Wet_Zone_Limits.md` (62) · `Soundproofing_Installation_Technique.md` (293).

**Every move was verified the same way as the Kitchen Furniture split**: content extracted by line range byte-for-byte, coverage asserted, then an independent content-line and citation-ID parity check per operation. **Zero content lines lost, zero citations lost, across all four operations.**

### ⚠️ Budgeting_Guide — the numbering had collapsed, which was the worse defect

Length was not the main problem. **The page had TWO `## 5b.` sections and TWO `## 5c.` sections, with `## 6` sitting *before* 5b–5j** — precisely the failure `00_Master/wiki_page_format.md` predicts for integer numbering on an open-ended page. Separately, **sixteen `### Live intake benchmark` subsections (294 lines) had accumulated under "4. What to Check Before Estimating," which is not what they are** — they landed under the nearest available heading.

Fixed by extracting the benchmark ledger and the design-services cluster. **The extraction resolved the duplicate numbering by itself** (the second 5b/5c *were* the design cluster), after which 5f–5j were renumbered into the vacated 5d–5i slots and §6 moved to the end. **Sequence is now clean: 1, 2, 3, 4, 5, 5a–5j, 6.**

**⚠️ Still flagged at 495 against the 350-line guide threshold, and that is recorded rather than hidden.** What remains is the guide's own framing content, and `11_Budget_and_Planning` was explicitly declared "out of scope" for the 2026-08-17 layered rollout on the grounds that it already has its own tiered structure. **Taking it further would mean a full layered conversion of the folder's master guide — a larger decision than a defect fix, and one worth taking deliberately rather than as a side effect.** The named next step if it is wanted: extract the §5–5c cost-saving/bill-of-quantities cluster (~150 lines).

### ⚠️ General_Dos_and_Donts was the FRAGMENTATION mode — so it was merged, not split

**18 of its 25 top-level sections were dated per-batch headings from a single channel, 8–17 lines apiece.** That is the pattern this file recorded on 2026-08-31 from `Lighting_Design.md`, where the lesson was that **splitting such a page makes it strictly worse and the fix is merging.**

So the sections were **grouped under five thematic parents with the original dated headings demoted rather than deleted — no prose changed** — and only then were two coherent groups (materials/finish critiques, gadgets/mechanisms) moved to their own pages. **25 top-level sections → 6.** This is the first time this vault has applied that lesson deliberately rather than learning it retrospectively.

### ⚠️ Furniture_Facade_Materials — deliberately NOT split, and the reasoning matters

314 lines across 12 sections, averaging 26 lines each: **substantial sections, not fragments.** Every candidate seam — substrate / facing / hardware — **cuts through individual sourced blocks rather than between them.** The tier ladder covers all three facings in one source's comparison; the "Whole Truth 2026" block covers facade types *and* hardware cycle ratings *and* carcass tiers as one source's account.

**Splitting it would fragment single-source blocks a reader compares side by side, which the convention's "move existing prose, don't re-derive" rule exists to prevent.** It is 54 lines over a threshold the convention itself calls "the weakest of the available signals." **Left as one page on purpose. The condition that would change that: if it takes another facade source, split at substrate / facing / hardware — the way the source videos are themselves organised.**

### The two clean splits

- **Soundproofing (493 → 216)** had a genuine seam on whole sections: **deciding *which* system to build versus *how* to build it.** Selection keeps the noise taxonomy, system types, four-factor framework, worked per-wall case, floor-vs-ceiling asymmetry, measured decibel comparisons and the room-adjacency audit; technique took floor membrane, the frame system, ZIPS, frameless, sewer-riser wrap and the door-sill gasket. **⚠️ Шумопласт was deliberately kept on the selection page — it is a material alternative, not a technique**, and the first draft had it in the wrong place.
- **Bathroom Planning & Layout (355 → 245)** shed two clusters: design/palette/spa programming, and RUSSIAN regulation (steam rooms, the threshold). **⚠️ Безверхая's wet-zone replanning limits stayed put, because that block also carries her dimensional ergonomics and cutting it would have split one source's account.**

### Cross-reference handling

**Eight `§N` references pointed into Budgeting_Guide.** §2.1, §4 and the first §5c survived the restructure and still resolve. **The §5e reference from `Furniture_Facade_Materials.md` was repointed** at the new design-services page, and **the two internal §5b/§5d references that travelled with the moved cluster were rewritten to name their sections instead of numbering them**, per the convention's preference for names over `§N`. The legacy 5b–5e numbers were stripped from that page's headings, since they are meaningless on a standalone page.

## 2026-09-02 (third pass) — a 300-line hard ceiling, and the whole vault brought under it

The owner's instruction was to stop wiki pages growing out of control, restructure the dependent
pages rather than only the two named ones, verify the structure, and **keep pages under 300 lines**.
All four parts are done. **Every page in the vault is now under 300 lines**, and the rule is enforced
by a tool rather than by remembering.

### The rule, and where it lives

**No wiki page may reach 300 lines.** `tools/check_page_sizes.py` now **exits non-zero** on a breach,
and the advisory exceptions file **cannot waive it** — the ceiling is checked before that file is
consulted. Below the ceiling the checker warns (detail pages at 260 lines, or 220 with 12+ sections;
guide pages at 280, or 240 clustered), so a page is caught while it is still growing.

The four old thresholds (400/260 detail, 500/350 guide) were **deleted, not kept alongside**: under a
300-line ceiling none of them is reachable, so leaving them in would have been dead code pretending
to be policy.

⚠️ **This does not overturn the 2026-08-31 finding that line count is the weakest signal, and the
convention now says so explicitly.** Line count still tells you nothing about *how* to fix a page.
What a ceiling adds is a moment at which action is forced — the pages that reached 500, 700 and 878
lines got there by twenty batches each appending a little, never by a decision.

Recorded in `00_Master/wiki_page_format.md` (new section), `AGENTS.md` (new standing rule 8), and the
tool's own constants block.

### The tooling that did the work

`tools/split_page.py` gained a **`merge`** subcommand alongside `analyse` and `apply`, because
fragmentation had now been fixed by hand three times. It groups sections under thematic parents and
**demotes the original dated headings from `##` to `###` rather than deleting them**, so every
attribution and date survives; its parity check normalises that one permitted change and requires
everything else to match byte for byte.

### What was restructured

**Twenty pages were over the ceiling. All twenty are under it.** No page was rewritten — sections
were moved whole, by line range, byte for byte.

| Page | Before | After |
| :--- | ---: | ---: |
| `17_.../Decor_and_Finish_Selection_Technique.md` | 739 / 53 sections | **185** |
| `00_Master/Bedroom_Design_Principles.md` | 695 | **255** |
| `17_.../Sliding_Partition_Mechanisms.md` | 591 | **179** |
| `12_.../Lighting_Design.md` | 568 | **268** |
| `13_.../Ceilings_Guide.md` | 503 | **259** |
| `07_.../Bathtub_and_Shower.md` | 489 / 35 sections | **207** |
| `13_.../Wallpaper_and_Paint_Application.md` | 446 | **287** |
| `13_.../Flooring_Material_Selection.md` | 415 | **253** |
| `17_.../Color_Harmony_and_Combination_Rules.md` | 407 | **227** |
| `09_.../Essential_Components_and_Layout.md` | 401 | **223** |
| `17_.../Neutrals_and_Earth_Tone_Palettes.md` | 393 | **270** |
| `17_.../Color_Selection_Process_and_Testing.md` | 393 | **247** |
| `17_.../Functional_Zoning_and_Furniture_Arrangement.md` | 361 | **288** |
| `12_.../Smart_Home_Systems.md` | 329 | **239** |
| `12_.../Radiators_and_Convectors.md` | 319 | **227** |
| `14_.../Loose_Furniture_Selection_Principles.md` | 312 | **236** |
| `12_.../Fresh_Air_Ventilation_and_Ducting.md` | 310 | **231** |
| `17_.../Color_Palette_and_Material_Direction.md` | 309 | **244** |
| `17_.../Whole_Home_Planning_Method.md` | 306 | **232** |
| `01_Entrance/analysis/Storage.md` | 306 | **199** |
| `13_.../Flooring_Installation_and_Baseboards.md` | 300 | **184** |

Plus the two pages the owner named first, done earlier the same day: `Budgeting_Guide.md` 495 → 182
and `Furniture_Facade_Materials.md` 314 → 171.

*(Line counts are `wc -l`; `check_page_sizes.py` reports one more for a file whose last line lacks a trailing newline.)*

**Every operation reported RESULT: CLEAN — zero content lines lost, zero citation IDs lost, across
all thirty-two split and merge operations in this commit.**

### ⚠️ Two findings worth keeping

**1. `Flooring_Installation_and_Baseboards.md` sat at exactly 300 and a manual sweep missed it.**
The sweep used `> 300`; the rule is `>= 300`. **The tool found it; the hand-written check did not.**
This is the case for having the ceiling in a tool at all.

**2. Splitting can EXPOSE fragmentation that was hidden underneath.** `Radiators_and_Convectors.md`
(22 sections in 215 lines) and `Loose_Furniture_Selection_Principles.md` (21 in 225) were not
flagged as fragmented before this pass — their large sections were masking the average. Moving those
sections out revealed the underlying shape, and both then needed **merging**, not further splitting.
Radiators went 22 sections → 7, Loose Furniture 21 → 12. **Re-run the checker after a split rather
than assuming the job is finished** — this is now written into the convention.

### Cross-references

**Twelve `§N` references were broken by the moves and all twelve were repointed to page names**, per the
convention's preference for names over section numbers:

- `Lighting_Design.md` — three internal refs (§3, §4, §8) whose targets left the page.
- The two new lighting pages — three refs: one to §5 (glare) and two to §2 (colour temperature, which stayed behind on the parent).
- `Planning_and_Layout.md` — the Bathtub "§Length Ergonomics" ref, now on the materials page.
- `Budgeting_Guide.md` — a §2 ref, and **a §5e ref that had silently become wrong**: 5e is now
  Krasnov material-selection content, not the Кузина design-fee material it claimed to cite.
- `Estimate_and_Contract_Templates.md` (two §5c refs) and `Decor_Art_and_Composition.md` (one §5e).

### The exceptions file

The single entry — `Lighting_Design.md`, added 2026-09-01 — **was retired**. Its own stated review
condition was "REVIEW AGAIN if the section count reaches 12"; after this pass the page is 268 lines
across 10 sections, below both the ceiling and the cluster trigger. **The reasoning it carried was
kept in the file as a retired-entry note rather than silently deleted**, because the point it made
(that a split can undo a deliberate merge) is still worth knowing.

### Verification

`tools/verify_batch.py --base main` reported **two citation-ID drifts, both self-identified by the
tool as moves** into `Cost_Benchmarks_Real_Object_Cases.md`. Both were confirmed by hand — one
occurrence before, one after, in the page the tool named — and proceeded with per the tool's own
instruction. `tools/check_page_sizes.py` exits 0: **no breaches, 31 advisory warnings**, which is the
early-warning band working as designed rather than a backlog. One of the 31 is `Lighting_Design.md`
itself at 268 lines — it warns now only because its exception was retired, which is the honest
outcome rather than a regression.

## 2026-09-02 (fourth pass) — the other direction: 29 fragmented pages merged

The owner's instruction: *"let's merge in when it's needed and split in when it's needed… a well
balanced repository with articles per topic. It should work both ways."* The 300-line ceiling was
only half the shape rule. **This pass did the other half: 29 pages were organised by intake date
rather than by topic, and all 29 were merged. Zero fragmented pages remain, and zero breaches.**

### ⚠️ The detector was wrong, and it was wrong in a way that mattered

The old test was "20+ top-level sections averaging under 12 lines". Run across all 273 pages it
fired on **two** — and both only *after* a split had removed the large sections masking their
average. Fragmentation had been accumulating for weeks, invisible.

**Two faults, and the second is the important one:**

1. **Average section length also describes the target shape.** `03_Kitchen/Kitchen_Furniture.md` —
   the compact guide built two days earlier as the reference example — is 11 thematic sections in
   80 lines, 7.3 lines each. **The old detector would have condemned exactly the structure
   `wiki_page_format.md` asks authors to produce.** A rule that cannot tell the target from the
   defect is worse than no rule.
2. **It measured arithmetic when the defect is written in the text.** A heading reading
   *"⚠️ Wall Art Framing… (Игорь Краснов, added 2026-09-01, Round 3)"* records **when a fact
   arrived instead of what it is about**. That *is* the fragmentation, stated outright.

**The test is now the proportion of headings that name a processing batch** — 12+ sections, at
least half dated, under 17 lines each. Same vault, same day: **29 pages, against the old rule's
two.**

### What was done

**29 merges, in six batches.** Section counts collapsed hard, which is the measure that matters:

| Page | Sections before → after |
| :--- | :--- |
| `Decorative_and_Specialty_Wall_Finishes.md` | 21 → 6 |
| `Fixtures_Mixers_and_Sinks.md` | 20 → 5 |
| `Planning_and_Layout.md` (bathroom) | 19 → 6 |
| `Tile_Selection_and_Layout.md`, `Bathtub_and_Shower.md`, `Decor_Color_and_Lighting_Technique.md`, `Rough_Plumbing_Sequencing.md`, `Ceilings_Guide.md` | 18 → 5–10 |
| `Material_and_Finish_Technique.md`, `Functional_Zoning…`, `Living_Room_Layout…`, `Water_Inlet_Node_Components.md`, `Family_Scenario_Driven_Design.md` | 17 → 5–9 |
| …and 16 more, all 12–16 sections → 4–9 |

**Nine splits alongside them**, because size and shape are independent problems and several pages
had both.

**Every one of the 38 operations reported RESULT: CLEAN.** `verify_batch.py --base main` returned a
clean PASS with **no citation drift at all** — not even a move to confirm by hand. The knowledge-base
index rebuilt to **16,107 numeric claims, identical to before the pass**: content conserved exactly,
only its arrangement changed.

### ⚠️ Merging is not deleting, and the tool enforces that

`tools/split_page.py merge` groups sections under a thematic parent and **demotes the original dated
heading from `##` to `###` rather than removing it**. Every practitioner name, attribution and date
survives one level down. **The parity check treats that single demotion as the only permitted change
and requires every other line to match byte for byte** — which is why 38 operations could run without
a manual read of each result.

### ⚠️ Order matters, and it looks alarming halfway through

**Merge first, then extract.** Splitting a fragmented page distributes the fragments across two pages
and leaves two fragmented pages.

Four pages were both fragmented *and* near the ceiling. Merging them pushed three **over** the
ceiling — 293 → 304, 291 → 302 — because **a merge adds group headings and therefore lines, typically
10–30 of them.** The follow-up split then brought them back under. That sequence is correct and
expected; the intermediate breach is not a mistake. This is now written into the convention, because
an agent seeing a merge increase a line count would otherwise reasonably conclude it had done the
wrong thing.

### Final state

**279 pages. 0 breaches. 0 fragmented. 19 advisory near-ceiling warnings**, all between 223 and 280
lines with topic-shaped headings — sizeable, not defective. The four pages within fifteen lines of
the ceiling were split for headroom so the next intake batch cannot breach them.

Recorded in `00_Master/wiki_page_format.md` (a new "Both directions" section with the
read-the-headings diagnosis table) and `AGENTS.md` (standing rule 8 rewritten to cover both modes).

## 2026-09-02 (fifth pass) — ⚠️ correcting the hard ceiling: it was the wrong rule

**The two entries above describe a hard 300-line ceiling. That rule was wrong and lasted a few
hours.** It is corrected here rather than edited out of them, per this vault's standing practice of
not rewriting its own records.

### What the owner actually asked for

> *"I don't want a strict three hundred lines rule. The question is not the exact number of lines.
> The question is the approximate size and the integrity. If its structure is logical and requires,
> for example, three hundred and ten lines, that's okay. Not a problem."*

### Why the hard ceiling was wrong

**It made "310 lines and perfectly coherent" fail in exactly the same way "878 lines of twenty
appended batches" failed.** Those are not the same defect and should not produce the same signal. A
gate that cannot tell them apart tells an author nothing useful, and its only available remedy —
split something — is actively harmful applied to a page that is coherent.

**This is the same mistake the 2026-08-31 recalibration had already caught once**, recorded a few
paragraphs up this same file: *"a rule that punishes a correct split gives an author no achievable
target short of atomising every page into stubs."* Making 300 a hard gate reintroduced it in a new
form. Worth noticing that the failure recurred despite being written down — **the written lesson was
about thresholds being too low, and it did not transfer to a threshold being too rigid.**

### What replaced it

| Signal | Lines | Effect |
| :--- | :--- | :--- |
| **Soft target** | ~300 | **Informational. Not a defect.** A prompt to look at the page and ask whether it still holds one subject |
| **Backstop** | 400 | The only failing condition. **Waivable by a reviewed exception** |
| **FRAGMENTED** | any | The defect that actually matters — merge, never split |

**The order of questions is now: are the headings topics or dates? → does the page hold one coherent
subject? → and only then, how long is it.** Length is a prompt for the first two questions, not a
finding on its own.

**The exceptions file can waive things again.** During the hard-ceiling hours it could waive nothing,
which was the point of a ceiling and is not the point of a soft target.

### ⚠️ What the hard ceiling nevertheless got right

**Nobody noticed the 878-, 740- and 696-line pages until someone looked.** None of them got there by
a decision. **The soft target survives because making someone look is its entire job** — the looking,
not the enforcing. Removing the number altogether would restore the original failure mode.

### ⚠️ Two things done under the wrong rule, disclosed

1. **Four pages were split purely for headroom** — `Age_Staged_Planning`, `Soundproofing_Installation_Technique`,
   `Wallpaper_and_Paint_Application`, `Cable_Circuits_and_Panel_Design`, all within fifteen lines of
   the ceiling at the time. **They were defensible splits on topic grounds** (developmental age
   bands, ZIPS/frameless as alternative systems, paint spec versus paint application, the panel as
   its own object) **but none was needed for size.** They have been left in place because the
   resulting pages are coherent, not because the reason for making them was sound.
2. **`Cable_Circuits_and_Panel_Design.md` was split without being merged first**, which is the exact
   ordering error the convention warns about. Splitting it dropped it from 16 sections to 12 and
   pushed its dated-heading ratio to 75%, so **the relaxed checker immediately flagged it as
   fragmented on its first run.** Now merged, 12 sections → 6. **The tool caught its author's own
   mistake within minutes of the rule being loosened**, which is a better argument for the
   integrity test than anything asserted about it above.

### Final state

**283 pages. 0 over the backstop, 0 fragmented, 15 growing toward the soft target** (223–280 lines,
all topic-shaped, all fine). `verify_batch.py` PASS.

## 2026-09-02 (sixth pass) — housekeeping audit: link integrity and the regression guard

Asked whether other housekeeping was due, and specifically whether the skill set, page structure and
YouTube/transcript/triage process needed revising. **Audited rather than guessed. One finding was
important, several were small, and two of my own alarms turned out to be false.**

### ⚠️ The important one: the intake skill did not know about any of the page-shape work

`renovation-knowledge-intake/SKILL.md` is 1038 lines and well maintained on fetching, language,
pacing, taxonomy and price comparability. But it contained **zero mentions** of `split_page.py`,
`check_page_sizes.py`, FRAGMENTED, the soft target, or dated headings.

**That is the regression guard, missing.** Step 5a said "route to wiki pages, follow the page-shape
convention" — and the specific mechanism by which all 29 pages fragmented is *appending*
`## <Topic> (<Practitioner>, added <date>, Round N)`, which the skill neither forbade nor mentioned.
**Left alone, the next few intake batches would have rebuilt exactly what three passes had just
removed.**

Patched: step 5a now carries the no-dated-heading rule with the cost asymmetry stated plainly (one
extra read of the page's headings, versus a vault-wide repair), a new **step 5b** for the end-of-batch
`check_page_sizes.py` run with how to read each of its three signals, and a tooling table near the top
so the two tools are discoverable without reading to line 700. **Including the counter-intuitive
part: a merge makes a page longer, so don't reverse the merge-then-extract order because the number
moved the wrong way.**

### Link integrity — 66 of 69 broken links repaired

An audit of every wiki link across 1342 files found 69 unresolvable instances. Repaired:

- **35 appliance links missing their filename prefix** — a link to `Bosch_DHL555BL_Hood` where the
  file is `15_Appliances/models/Kitchen_Bosch_DHL555BL_Hood.md`; same for the oven, cooktop,
  microwave, dishwasher, four washers, four dryers, and the `Hood` / `FlexZone` /
  `Filtration_Systems` analysis pages. **These were dead links on three index pages** — the main
  navigation into the appliance model pages.
- **8 archive transcript links** citing a path built from the note's own slug plus the video id,
  which is not how `archive_transcripts.py` named the file. **Repaired by matching the 8-hex content
  hash**, which is the stable key. The frozen archive was not touched.
- **9 links into the machine-local memory store**, dangling since it was drained into the repo on
  2026-08-31. Repointed at the durable locations that replaced them.
- **1 link to `12_Engineering_and_Systems/Engineering_and_Systems_Index`**, a page that does not
  exist — that folder has no index.

**The 3 remaining are correct as written**: ellipsis placeholders inside example prose in
`wiki_page_format.md`, plus one genuinely unfinished pointer in a source note, left alone because
`_Sources/` is raw evidence.

### ⚠️ Two false alarms of my own, recorded because the checks were worth having

1. **"359 broken links."** My first checker only indexed `.md`, so every `_Archive/**.txt` provenance
   link looked broken, and it also mis-parsed escaped pipes inside markdown tables. **Real number:
   69.** A link checker that does not understand the repo's own file types and table escaping will
   manufacture a crisis.
2. **"125 broken transcript pointers."** Those notes read
   `transcript_file: not separately archived — fetched inline via youtube_transcript_api (sha256 …)`.
   **That is a deliberate, hash-bearing provenance record, and my check was treating prose as a
   filename.** Provenance is intact.

### Reported, not changed — needs a decision

- **16 `processed_sources.csv` rows carry unexpanded shell brace notation** in `target_docs`, e.g.
  `07_Bathroom/analysis/{Bathtub_and_Shower,Fixtures_Mixers_and_Sinks}.md`. Human-readable, but not
  machine-resolvable, so tooling cannot verify those rows. **Left alone: standing practice names CSV
  `target_docs` as never rewritten.** Expanding them is lossless and would make the ledger checkable
  — worth doing only as a deliberate decision.
- **12 source notes appear uncited by any wiki page** (of 961) — extracted but seemingly never routed,
  the residue of the step-5a-deferral failure recorded on 2026-08-18. Needs a per-note look: some may
  be deliberate (a rejected source), others a real routing gap.
- **`_Inbox/planning/` has 24 files and no index**, two of them over 1500 lines. Working documents,
  out of scope for the page rules, but there is no way to tell which channel queues are still live.
