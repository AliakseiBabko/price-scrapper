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
