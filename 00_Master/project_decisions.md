# Project Decisions & Open Items

Decisions taken about **this apartment and this project**, with dates, plus the open items that are not yet resolved.

> [!NOTE]
> **Created 2026-08-31 by draining Claude Code's machine-local memory into the repository** (WS-3 of the `AGENT_KNOWLEDGE_PORTABILITY` plan). Everything here previously existed only in `~/.claude/projects/.../memory/`, readable by one agent on one machine. **One of those notes had already drifted** — it cited `90_Archive/`, a path that stopped existing in the 2026-08-30 restructure. That is the argument for this file.
>
> This page records **decisions and open questions**. It deliberately does *not* duplicate detail that already lives elsewhere; where the substance is in a skill or a data file, this page points at it.

## The apartment

**ZK Dubravinskiy, type 3Б/3+, 69.09 m², 4th floor.** Established 2026-08-26.

- **Two area conventions, never compared across.** Developer plans publish **clear** floor area with service boxing deducted; БТИ-style measured plans publish **gross** area to the wall faces, counting the короб as floor. Verified on the туалет: 1140 × 1090 = 1.24 m² clear, plus a 1140 × 490 riser recess = 0.56 m², giving the 1.80 m² gross that two of three measured comparables print. **Where a developer area and a measured area differ by about a короб footprint, that is the explanation before any construction difference is.**
- **Usable floor in the туалет is ~1.24 m², not 1.8.** The 1140 × 490 block is the **вентблок** (three channels, drawn in section), not a plumbing короб — corrected after zooming the plan. Common property, immovable. A second вентблок sits between the kitchen zone and the laundry/hallway zone; plumbing стояки are also in the wet zone.
- **Ventilation section count depends on the floor; plumbing does not.** Above the 10th floor a flat carries two ventilation sections instead of one, taking extra area. **This flat is on the 4th — single section, larger areas.** That is why kv109 prints туалет 1.6 m² / total 68.3 m²: it is a higher-floor sub-type. **Use kv53 and Минина 6 as comparables; do not average kv109 in.**
- **Tolerance: treat every model dimension as nominal ±25 mm**, and never design a fit needing less than ~30 mm of slack. The building is unfinished and nothing is field-verified; three as-built comparables give wall-to-wall spreads of 0–50 mm, median 20 mm.
- **Source roles**: the developer detailed plan is the base case (v0). The owner's Homestyler design is a **variant, not the existing state**. Partitions are drawn 75 mm on the developer plan.

Data: `data/canonical/room_schedules.json`, `data/canonical/dimension_tolerance.json`. Narrative: `00_Master/Apartment_Geometry_Sources.md`. **Full detail is in `.agents/skills/apartment-layout-modelling/SKILL.md` — read that before quoting any dimension or proposing a layout; do not re-derive from the plan images.**

## Scope decisions

**No underfloor heating** — user decision, 2026-08-26. Recorded as `our_scope: out_of_scope` in `data/deliverable_templates/price-scrapper-target-set.json`, which drops the target album from 16 sheets to **11**.

Respect this elsewhere: do not cost, spec or sequence тёплый пол in budget pages or the renovation sequence. The floors sheet (план полов) stays in scope and is unaffected. If the decision is ever reversed, bring it back as a *layer* of the floors sheet rather than a separate sheet.

## The deliverable

**The end product for the whole repo is a document set like architect Sergey Dolgushev's *планировочный проект*** — A3 sheets plus a grey 3D massing, deliberately without renders, ведомости or развёртки. Established 2026-08-26.

**Pipeline order as stated by the user**: wiki pages → drawings / real layout → choose the best layout → produce the document set → start the renovation.

Readable spec: `00_Master/Planning_Project_Deliverable_Set.md`. Machine-readable, sheet-by-sheet with "can we generate this today" verdicts: `data/deliverable_templates/dolgushev-planirovochny-proekt.json`. Work needed for the remaining 11 sheets: `00_Master/Sheet_Production_Roadmap.md`.

The three album PDFs in `00_Master/*.pdf` are **gitignored** — third-party watermarked client documents; identity is kept via sha256 in the case files.

## Modelling approach

**One model, many views. 2D is generated *from* the 3D model, never drawn separately.** Asked and answered directly. Spec + variant patch → one IFC per variant → A3 sheets, DXF, Blender/glb, quantities. **If two outputs disagree it is a generator bug — never fix a drawing by hand.** Annotation (dimension chains, hatches, экспликация) lives in the drawing layer, not the model.

- **Variants are patches, not copies.** Base geometry in `data/canonical/current_apartment_base.json`; a variant is a typed patch in `data/variants/<id>.json` using the same op vocabulary as the layout cases (`wall.remove`, `zone.merge`, `opening.create`, `furniture.place`, `finish.set`, `circuit.assign`). Every wall/opening/fill carries `phase` (existing / demolished / new / modified).
- **Furniture and appliances are *objects*; finishes are *properties of surfaces*.** Products belong in a catalogue with dated, regional prices — which is where the price-scraping half of the repo plugs in. **CAD "layers" are a drawing-time concept generated from this data; never organise the data as layers.**
- **Viewers the user actually has: Blender (3D) and Autodesk DWG TrueView (2D).** TrueView opens only DWG/DXF — not IFC, SVG or PDF — so any 2D output meant for the user must also be exported via `tools/drawings/export_variant_dxf.py`.
- **Venvs are not interchangeable**: `.venv-ifc314` has ifcopenshell/ezdxf/Blender tooling; `.venv` has the scraping/PDF stack and no ifcopenshell. Pick per script.
- **The user is not experienced with CAD.** Explain in terms of what they choose — products, rooms — and let the tooling own drawing conventions.

Detail: `00_Master/Model_and_Views.md`, `00_Master/Finishes_and_Furniture_Data_Model.md`, and the `apartment-layout-modelling` skill.

## Source conventions

**Zemskov / Zemstandart is Moscow-based, prices in RUB.** Per the user's explicit statement, then independently confirmed 2026-08-10 from the company's own `zems.pro/about/` (office addresses in Moscow and Podolsk; business in Moscow since 2003).

> [!IMPORTANT]
> **Nuance that changes how a source is read**: the business expanded beyond Moscow — St. Petersburg, Tula, Ryazan, Kaluga — from **2018 onward**. Treat a Zemstandart source from 2018 or later as **"Moscow-based, multi-region"** rather than pure-Moscow. Check the specific video's upload date.

**When comparing prices across Zemstandart sources from different years, account for inflation before calling it a contradiction.** Worked example: a 2022 video states a 3,000 RUB/m² design fee; the company's 2026 website states 5,000 RUB/m² for the same service — ~67% over ~4 years, roughly 13.5%/year compounded. Ordinary inflation, not a conflict.

*(`zemstandart.pro` and `земстандарт.рф` are JS-heavy SPAs that yield nothing to a plain fetch; `zems.pro` is the one that works.)*

## ⚠️ Open items

Real, scoped work that is **not** done. None of these are trivial.

| Item | Status |
| :--- | :--- |
| **Zemskov region/currency not applied retroactively.** The Moscow/RUB convention above was applied to the 2026-08-05 batch but **not** to the ~15+ earlier Zemstandart entries already in the store. | Open since 2026-08-10 |
| **Budget-tier page never reconciled against its own channel.** `11_Budget_and_Planning/analysis/Budget_Tiers_Cheap_Optimal_Premium.md` was seeded from one Kruglov/Ontario source (`Tyl0yPQkO5g`), but ~20 other sources from that same channel are already in the store and were **not** cross-checked for figure conflicts or tier-boundary disagreements. **Check `YT_P8t_d7J9fm4` (2026 cost list) and `YT_WK-KLd2ssYY` (AC economy vs premium) first** — most likely to overlap. Do this before treating the page's figures as settled. | Open since 2026-08-28 |
| **Numeric Data entries predating the location+year rule.** Many entries don't pair year and location at the individual-entry level. A real audit, not a sweep. | Open since 2026-08-10 |
| **USD backfill.** 233 of 338 price-bearing units still lack a USD equivalent. | Tracked in `_Knowledge/store/USD_Backfill_Inventory.md` |
| **Page-splitting backlog.** 20 oversized pages plus one fragmented. | Tracked in `_Inbox/planning/page_splitting_backlog_20260831.md` |

## Conventions recorded elsewhere

Pointers, so this page stays a decision record rather than a second copy:

- **Vault layout** (`_Sources/`, `_Knowledge/` top-level since 2026-08-30) — `.agents/skills/renovation-knowledge-intake/SKILL.md`, storage-paths section. **`00_Master/Bedroom_Design_Principles.md` is deliberately not in a room folder** — this project has no fixed master bedroom, so it applies to whichever room serves that function. Don't "tidy" it into `06_Small_Bedroom`.
- **Page shape, layered convention, Perspectives blocks** — `00_Master/wiki_page_format.md`.
- **Layout case dataset contract** (frames → case JSON → rules JSONL → prose; the wiki is never the system of record for a number) — `.agents/skills/apartment-layout-modelling/SKILL.md`.
- **Budget-tier organising preference** (cheap / optimal / premium per system; user defaults to optimal, premium only where felt daily; flag *technical* cross-system dependencies separately from taste) — `renovation-knowledge-intake/SKILL.md`.
- **Channel queue and group structure** — `_Inbox/planning/youtube_channel_queue.md`.
- **Zemskov full-channel triage, complete as of 2026-08-19** — `_Inbox/planning/zemskov_full_channel_triage.md`. **Do not re-derive the candidate list**; the only reason to revisit is new uploads since that date.
