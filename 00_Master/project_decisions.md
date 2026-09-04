<!-- memory-reference: historical - this page describes the 2026-08-31 drain
     out of Claude's machine-local memory. It does not depend on that memory;
     see tools/verify_agent_readiness.py for why the distinction matters. -->

# Project Decisions & Open Items

Decisions taken about **this apartment and this project**, with dates, plus the open items that are not yet resolved.

> [!NOTE]
> **Created 2026-08-31 by draining Claude Code's machine-local memory into the repository** (WS-3 of the `AGENT_KNOWLEDGE_PORTABILITY` plan). Everything here previously existed only in `~/.claude/projects/.../memory/`, readable by one agent on one machine. **One of those notes had already drifted** — it cited `90_Archive/`, a path that stopped existing in the 2026-08-30 restructure. That is the argument for this file.
>
> This page records **decisions and open questions**. It deliberately does *not* duplicate detail that already lives elsewhere; where the substance is in a skill or a data file, this page points at it.

## The apartment

**ZK Dubravinskiy, type 3Б/3+, 69.09 m², 4th floor.** Established 2026-08-26.

- **⚠️⚠️ AREAS ARE NOT EVIDENCE — LINEAR DIMENSIONS ONLY. Owner’s standing instruction, 2026-09-04.** Do not trust any area figure, **including the developer’s own on either drawing**: his own attempt to reconstruct the total from the two plans did not play out, the areas look like a CAD recalculation, and many walls are of complex shape rather than a straight run. **Tested and confirmed: the one plain rectangle on the plan closes to 0.2% (туалет, 1140×1090 = 1.243 vs 1.24), while both rooms with shape complexity are out by 2.6% and 4.4%.** → **Build geometry from linear chains; NEVER validate a reconstruction against a printed area** — when `v0` is built, its computed areas will not sum to 69.09 and **that is expected, not a bug**. Use **chain closure** as the validator (the small room’s two parallel chains both give 2825 exactly). Areas keep their published roles only. Detail: `data/canonical/dimension_tolerance.json`.
- **Two area conventions, never compared across.** Developer plans publish **clear** floor area with service boxing deducted; БТИ-style measured plans publish **gross** area to the wall faces, counting the короб as floor. Verified on the туалет: 1140 × 1090 = 1.24 m² clear, plus a 1140 × 490 riser recess = 0.56 m², giving the 1.80 m² gross that two of three measured comparables print. **Where a developer area and a measured area differ by about a короб footprint, that is the explanation before any construction difference is.**
- **Usable floor in the туалет is ~1.24 m², not 1.8.** The 1140 × 490 block is the **вентблок** (three channels, drawn in section), not a plumbing короб — corrected after zooming the plan. Common property, immovable. A second вентблок sits between the kitchen zone and the laundry/hallway zone; plumbing стояки are also in the wet zone.
- **Ventilation section count depends on the floor; plumbing does not.** Above the 10th floor a flat carries two ventilation sections instead of one, taking extra area. **This flat is on the 4th — single section, larger areas.** That is why kv109 prints туалет 1.6 m² / total 68.3 m²: it is a higher-floor sub-type. **Use kv53 and Минина 6 as comparables; do not average kv109 in.**
- **Tolerance: treat every model dimension as nominal ±25 mm**, and never design a fit needing less than ~30 mm of slack. The building is unfinished and nothing is field-verified; three as-built comparables give wall-to-wall spreads of 0–50 mm, median 20 mm.
- **⚠️⚠️ AND THE RISK IS ASYMMETRIC, established 2026-09-04. The developer plan reads LARGER than all three measured flats on both dimensions testable from printed chains — +1.0% to +1.9%, 9 of 9 comparisons, mean +1.5%.** So ±25 mm is the flat-to-flat scatter, not the whole exposure. **Size for a room up to ~100 mm SHORTER than drawn, never longer**, and specify any fitted run to a post-plaster site measurement rather than to the plan. ⚠️ *Not a settled fact — it does not reconcile with the measured AREAS for the same room, and the tension is recorded in `dimension_tolerance.json` rather than resolved by preference.*
- **⚠️⚠️ The three measured comparables may be MIRRORED** — the series has left- and right-handed variants (owner, 2026-09-04). **Compare a comparable’s named DIMENSION freely; never map its POSITION onto this flat without establishing handedness first.**
- **⚠️ No further geometry exists until the building completes — owner’s estimate 2026-11 to 2026-12.** The five plan images are all there is. Until then nothing is field-verifiable: choose a layout on design intent, but cut no joinery.
- **Source roles**: the developer detailed plan is the base case (v0). The owner's Homestyler design is a **variant, not the existing state**. Partitions are drawn 75 mm on the developer plan.

Data: `data/canonical/room_schedules.json`, `data/canonical/dimension_tolerance.json`. Narrative: `00_Master/Apartment_Geometry_Sources.md`. **Option review — what `v1` actually changes against `v0`, what it costs, and the two measurements the layout decision is blocked on: `00_Master/Layout_Option_Review.md`.** **Full detail is in `.agents/skills/apartment-layout-modelling/SKILL.md` — read that before quoting any dimension or proposing a layout; do not re-derive from the plan images.**

## ⚠️⚠️ The layout thesis — ONE bathroom, bought to fund a real living room

**Owner's decision and reasoning, stated 2026-09-04, in response to the closest comparable in the vault.** This is the argument the whole `v1` layout rests on, and it had not been written down.

**The comparable (`Phk79uKT7rA`, ~70 m², family of four) spent area on a SECOND full sanitary room. The owner rejects that trade, and names its cost in that flat:** their combined kitchen-living came out too small to be a living room at all — *"just a small sofa and a screen, a monitor on the wall … that's not a real living room. There is no place of living room."*

**The decision here:** keep the developer's **single bathing room plus the separate туалет** (two wet rooms, near the entrance), and spend the area that a second bathroom would have taken on the **kitchen + living zone instead** — *"instead we have bigger area which can be separated into a real isolated room if needed. That was a main idea."*

- → **The operative word is SEPARABLE.** The zone is not merely bigger; it is sized so that a part of it can be closed off as a genuinely isolated room. That is what makes the Phase 2 arrangement possible at all, and it is why area in that zone is worth more here than a second shower.
- → **⚠️ This is a deliberate departure from a rule the vault holds, and it should not be read as an oversight.** Zemskov's ideal is **three** wet rooms (`wc.bathroom_count_minimum_3`); his own stated fallback for an area-constrained project is **two** — a separate туалет plus a combined bathroom (`wc.budget_fallback_2_wet_rooms`). **This project takes the fallback knowingly, and for a reason the rule does not consider: what the third wet room would cost the living zone.**
- → **It also answers the question left open by the case-study round: this is the decision in that case study the owner rejects.** The bunk bed and the themed mural remain his to state.

### The retractable glass divider — a correction to how it had been recorded

**Not doors.** *"which can be separated by the … glass divider, not a door's divider, which can be retractable divider."* Earlier notes in `Family_Requirements.md` describe a *sliding glass door*; the owner's intent is a **retractable divider** — which changes the parking-width and head-detail problem, not just the ironmongery. **Size it against the 24.13 m² the zone actually has** (see `00_Master/Layout_Option_Review.md`), not against the developer plan's 24.73.

### Two structural differences from the comparable, stated by the owner

1. **⚠️ The лоджия connects to the SMALL BEDROOM here, not to the kitchen.** In the comparable the balcony is off the kitchen-living zone. **Confirmed on the detailed plan: the лоджия hangs off the 9.36 m² room.** So the comparable's balcony-off-the-living-zone content does not transfer, and the лоджия decision (keep it closed and separate) stays coupled to whichever person occupies that room — adults in Phase 1, the boy afterwards.
2. **Room tenure is phased and already assigned:** лоджия-side 9.36 m² room → adults now, **the boy** later; the middle room (15.28 m² in `v1`) → both children now, **the girl** later; adults move into the separable part of the kitchen-living zone.

**Overall the owner's assessment of the comparable stands: “the general layout is very similar, as the area is very similar”** — which is why the case is kept as a worked example and why the one trade it made differently is worth this much text.

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
| **⚠️⚠️ `v0` HAS NO GEOMETRY, so no layout trade can be measured.** Its room schedule and dimensions are known; its partition positions exist only on the plan image. ⚠️ **ROUTE CHANGED 2026-09-04: the owner states the plan images are the only source of truth, so a Homestyler export of the ORIGINAL layout is probably not available — only the redesign was ever traced. The remaining route is the skill’s fallback: reconstruct the partitions from the PRINTED dimension strings on `fllor_plan_detailed.jpeg`, using the registered raster.** That is now the actual task, and it is hand work. | **Open, and it BLOCKS layout selection** — raised 2026-09-04 |
| **✅ The SECOND вентблок is MEASURED. 400 × 1140 mm = 0.456 m²**, at the прихожая/кухня boundary, **long axis PERPENDICULAR to the façade wall** — unlike the туалет block, which lies along it. Drawn to the same shaded-box-with-channels convention as the confirmed one; both figures are **printed on the plan**, not derived from scale. ⚠️ **The datum of the adjacent `200` dimension is not certain from the raster — confirm the block’s offset from the wall at field measurement.** In `data/canonical/room_schedules.json`. | **Closed 2026-09-04**, with the offset flagged |
| **⚠️ Which layout gets built is not decided, and no option is marked `selected`.** `v0-existing` is `baseline`, `v1-homestyler` is `owner_first_approximation`. The pipeline order names “choose the best layout” as a step; nothing had recorded it as an open decision. **Review and the two blockers: `00_Master/Layout_Option_Review.md`.** | Open since 2026-09-04 |
| **The bunk-bed and themed-mural questions are informed but not answered.** Both turn on facts now established (15.28 m² permits two separate beds; the shared room ends at Phase 2, ~3–4 years out). **The owner’s position is what closes them** — he has said he rejects some of the case study’s decisions without naming which. | Open since 2026-09-04 |

## Conventions recorded elsewhere

Pointers, so this page stays a decision record rather than a second copy:

- **Vault layout** (`_Sources/`, `_Knowledge/` top-level since 2026-08-30) — `.agents/skills/renovation-knowledge-intake/SKILL.md`, storage-paths section. **`00_Master/Bedroom_Design_Principles.md` is deliberately not in a room folder** — this project has no fixed master bedroom, so it applies to whichever room serves that function. Don't "tidy" it into `06_Small_Bedroom`.
- **Page shape, layered convention, Perspectives blocks** — `00_Master/wiki_page_format.md`.
- **Layout case dataset contract** (frames → case JSON → rules JSONL → prose; the wiki is never the system of record for a number) — `.agents/skills/apartment-layout-modelling/SKILL.md`.
- **Budget-tier organising preference** (cheap / optimal / premium per system; user defaults to optimal, premium only where felt daily; flag *technical* cross-system dependencies separately from taste) — `renovation-knowledge-intake/SKILL.md`.
- **Channel queue and group structure** — `_Inbox/planning/youtube_channel_queue.md`.
- **Zemskov full-channel triage, complete as of 2026-08-19** — `_Inbox/planning/zemskov_full_channel_triage.md`. **Do not re-derive the candidate list**; the only reason to revisit is new uploads since that date.
