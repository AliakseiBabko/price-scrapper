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
