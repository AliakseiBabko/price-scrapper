# 2D/3D design-toolchain sources — triage of a 13-item list

**Created 2026-09-08.** The owner supplied 9 individual videos and 4 channels, described as *"mostly about applying 2D and 3D tools for interior design and apartment renovation projects — creative floor plans, creating electricity charts, lighting, plumbing"*, and asked explicitly for a triage before any processing: **is there anything worth taking, in particular a sequence of how to build a 3D model and what matters in it?**

This is **Group C** work, not Group A or B. The channel queue's own Group C note (2026-08-24) already anticipated exactly this list and set the condition:

> *"Before processing this channel, do a small scoping pass: title-skim to separate pure software-tutorial videos from videos that walk through an actual apartment's 2D plan/facade, and **decide explicitly where extracted content should live** before running a trial batch — don't force it into the renovation intake pipeline's existing taxonomy buckets by default."*

That condition is discharged in §5 below.

## Context that decides the verdict

This triage is **not** free-standing. Three planning documents written earlier the same day fix what "valuable" means here:

- [`toolchain_gap_analysis_20260908.md`](toolchain_gap_analysis_20260908.md) — its conclusion is **"no new software; three small scripts over data we already hold"**, plus the owner's own correction that the changes which actually arrive in a renovation are **substitutions and re-quotes, not geometry**.
- [`deep_research_brief_3d_budgeting_toolchain_20260908.md`](deep_research_brief_3d_budgeting_toolchain_20260908.md) and [`deep_research_review_20260908.md`](deep_research_review_20260908.md).

> [!IMPORTANT]
> **The consequence, and it is the single most important line in this file: these sources are being mined for CONVENTIONS AND INFORMATION MODELS, not for tool recommendations.**
>
> Our chain is Homestyler → DXF → IfcOpenShell → Blender/Bonsai. Nothing in this list overturns today's "no new software" conclusion, and **a video that is 70% mouse clicks in a proprietary web app is still worth reading if the remaining 30% is a drawing convention we have not settled.** Conversely, none of these sources is evidence that we should adopt RemPlanner, SketchUp or Планоплан. Judge every extracted fact by "does this change a field, a datum, a sheet or a rule in our own model", not by "does this look like a nicer program".

## 1. Preflight and identity

| Source | Videos | Fresh | Manifest / dump |
| :--- | :--- | :--- | :--- |
| `@k_dmitry` | **328** | **328 (0 duplicates)** | `preflight_20260908T151046Z.json`, [`k_dmitry_titles_dump.txt`](k_dmitry_titles_dump.txt) |
| `@RemPlanner` | 41 | 40 (1 dup: `OfqkRAZUfe0`, kids-room, processed) | [`remplanner_titles_dump.txt`](remplanner_titles_dump.txt) |
| `@Craftelectric` | 9 | 9 | [`craftelectric_titles_dump.txt`](craftelectric_titles_dump.txt) |
| `@АлександрЭлектрик-ц3н` | **3** | 3 | — |
| 9 loose videos | 9 | 9 | see §4 |

**Caption availability, probed on 7 representative videos: no manual subtitles anywhere on this list — auto-ASR only.** `ru-orig` (Russian original) is present on every Russian item, so **standing rule 1 is satisfiable** — force `ru-orig`, never the `ru` re-processed or `en` track.

> [!WARNING]
> **⚠️ The ASR is visibly noisier than this vault's usual sources, because the subject matter is software.** Observed in the two spot-checked transcripts: «Rimliner» / «ремплайнере» for Remplanner, «планоплане» → «кланировки», «потудомочной машины», «полотенсушитель», «канузла», «нейросети Promeai» mangled. **Program names, product names and — critically — NUMBERS must be treated as unconfirmed when heard once.** A height like «105 см» appearing once in ASR is a candidate, not a figure. Cross-check heights against the vault's existing socket-height pages before recording any of them as new.

## 2. ⚠️ The format problem, and why it is already solved here

**Every item on this list is a screencast.** A large fraction of the knowledge is *on the screen* — which tab is open, what the sheet looks like, where the dimension lines terminate — and not in the audio. On a normal channel that would be a reason to decline.

**It is not, because `tools/youtube/extract_layout_frames.py` already exists and was built for precisely this case.** Its own docstring: *"the author talks over a floor plan, and the useful evidence is the plan on screen at that moment, not the words alone"* — transcript segmentation on discourse cues, ffmpeg scene detection, frame-per-segment pairing, `index.md`.

**→ Mandatory for this group: transcript-only intake is not adequate here. Run `extract_layout_frames.py` on any source whose value is a sheet layout or a dimensioning convention.** The yield estimates below assume frames. And standing rule 9 (reading a dimension is a procedure) applies to every figure taken off one of those frames — identify what the extension lines terminate on, and prefer chain closure.

## 3. Verdict by source

### ⭐ Tier 1a — `@k_dmitry`: process, and it is the best find in the list

**Identity**: a practising interior designer, Moscow and Moscow oblast (ЖК Симфония 34, ЖК Баланс, Зеленый Квартет, Фестивальная, Большая Марфинская, Мелитопольская, Алтуфьево П-3, a house in Раменское). **Jurisdiction: Russia** — standing rule 4, nothing to `16_Legal_and_Regulations/`.

**Why it is different from anything already in this vault**: 250-odd wiki pages come from practitioners explaining *decisions*. This channel films the **production pipeline that turns a decision into a document a worker can build from** — the one thing the vault has no source for. His stack, named in the titles: **Планоплан** (concept layout, 3D panoramas, VR tours for client approval) → **Ремпланнер** (the technical part) → **SketchUp** (3D model) → **D5 Render** (photoreal) → **neural nets** (Nano Banana 2, VEO 3.1, Promeai) to animate or vary a render.

**Spot-check evidence — `DI5GAV64mnU`, «Технический дизайн-проект квартиры на Фестивальной в Remplanner», 33:34, 4,028 words.** Read in full-ish. What it actually contains:

| Finding | Why it matters here |
| :--- | :--- |
| **An explicit staged *регламент работы***: stage 1 concept layout + furniture agreed with the client in Планоплан; **stage 2 the technical base in Ремпланнер — deliberately before detailed visualisation**, to *«сформировать целостную картину работ по ремонту»*; stage 3 detailed renders | **This is the literal answer to the owner's question** — the sequence, with the reason for the order, from someone who bills for it |
| He sends the client **a view link to the live model** and narrates the decisions on it | A client/owner review mechanism; compare `_Drawings/review/` (overwritten, git holds the previous state) |
| **Door swing set by switch reachability** — living-room door reversed to open outward, санузел and kitchen swings changed, *«привязываю к тому, чтобы было удобно пользоваться выключателями при входе-выходе»* | **A layout rule with a rationale → `data/layout_rules/rules.jsonl`.** Also a genuine "connect the dots" instance: electrics driving door geometry, not the reverse |
| **Socket-by-socket derivation from named appliances, with heights**: a low row behind the dishwasher/hob/oven at plinth level; fridge; измельчитель; **фартук at 105 cm**; TV; **170 cm** for microwave/kettle on the raised worktop; **30 cm** at room entry; by the dining table | **This is `cap6`→`cap8` performed out loud.** Per the gap analysis it pays twice — design output *and* the `ELE-01` BOM quantity that is currently `unmeasured`. ⚠️ Heights are single-mention ASR: candidates, not figures |
| Wet rooms: **вывод under lighting; two moisture-protected sockets deliberately offset «чтобы вода на них не попадала» yet still within reach**; towel-rail; washer+dryer | Rule with a stated failure mode |
| Corridor: socket for a voice assistant *(client request)*; two at seated height by the shoe bench; **a robot-vacuum parking socket** | **`cap6` daily-scenario data** — the roadmap calls this "a decision-capture task, not a coding task" |
| **The щиток placed in the wardrobe adjoining the entrance**, cable brought in there, автоматы + реле inside | A `cap8` decision with a location rationale |
| **A план кондиционеров as its own sheet**, used to place the A/C вывод, and the unit moved to "one of the recommended positions" above the door | ⚠️ **See §6 — we have no A/C sheet at all** |
| **Ceiling drop of 80–100 mm is affordable when height allows**, and is what buys freedom to route cable and lighting | A tradeoff with a number, against a vault that holds a contested 27 mm drop figure |
| The **демонтажный план is deliberately near-empty** and he says why (no capital changes), rather than omitting the sheet | Deliverable-set discipline: when a sheet is legitimately blank |
| Tab structure = исходный план · замерные планы · демонтажный · перегородки · мебель · развёртки · розетки · освещение · кондиционеры … | **A second, independent instance of a deliverable sheet set** — see §6 |

**Density: comfortably 25–35 facts from this one video**, on subject matter with no prior coverage. That is at the level of the vault's best channels (`@YourInteriorDes` peaked at 36.0), and unlike those it lands on empty pages.

**Format signal for scoping rounds** — the catalogue splits cleanly and yield will track format, not topic (the corrected yield model from `@YourInteriorDes` Round 3):
- **Highest**: «Технический дизайн-проект … в Remplanner» walkthroughs (`DI5GAV64mnU` 33 min, `F0rXrbPDPf4` 18 min, `kD1dFGQh4EU` 17 min, `35sYbsrip14` 11 min) and **«обоснование планировочного решения»** (`YEpfNcwwGoU` 15 min) — the reasoning formats.
- **High**: cross-tool method (`TJVXUCKQ1UU` «Как использовать Планоплан и SketchUp вместе», `FRKr9X3AFfY` choosing doors and partitions), multi-variant comparisons (`_iN973Mjqm4` three staircase options, `MSVoLHapqEU` 3D variants for a family with two children), tool-vs-tool comparison (`25HQWSd3SU4` D5 Render vs Планоплан).
- ⚠️ **Notable**: `z-yMrBi1oKY` — an initial model **built from laser-scan data**. Worth reading against the retracted laser-meter recommendation in the gap analysis, and against the fact that **our flat is not built yet**.
- **Low / skip**: the 35–250 s render-showcase clips («оживление визуализации с помощью нейросетей», «3D-обзор») — output, no reasoning. Dozens of these; they are the channel's bulk and should be skimmed off.

**Proposal: a full preflight → triage → Round 1 pipeline, Round 1 = 5 videos, weighted entirely to the technical-walkthrough and обоснование formats.** This channel deserves its own plan file, as Group A channels get.

### ⭐ Tier 1b — `@RemPlanner`, split in two

**This is the playlist the owner referred to**: «Видеоуроки Remplanner», **13 numbered lessons**, which is the only structured curriculum in the list.

**Spot-check — `OTBw7bCrv-o`, «Урок 4. Электрика и освещение», 18:09, 1,906 words.** Honest reading: **roughly 70% is mouse mechanics** («наведите курсор», «левым кликом», «зажатой левой кнопкой») and is worthless to us. The remaining 30% is **drawing convention with the worker's reason attached, on questions we have open**:

| Convention stated | Bears on |
| :--- | :--- |
| **Dimensions run to the CENTRE of a socket/fixture, never its edge** — *«размеры всех светильников показывают расстояние до их центра, а не до края предмета, что позволяет строителям правильно рассчитать выводы проводов»* | **`cap3` setting-out dimensions**, and §E of the gap analysis (the datum problem). A convention stated *with* the reason it exists |
| ⚠️⚠️ **A centred fixture is dimensioned `1/2`, not in millimetres** — *«указывая строителям на то, что светильник должен быть смонтирован ровно по центру комнаты, независимо от любого расхождения в размерах»*. Rectangular rooms only | **The best single idea in the whole list.** A *relative* dimension that survives as-built variance, where an absolute figure goes wrong. `Geometry_Variance_Study.md` measured **−45 to +30 mm** across three comparables of this layout; this notation makes that variance harmless for every centred fixture instead of a site argument |
| **«Вывод провода» is a distinct element type** from a socket — a cable brought out of the wall for direct connection with no socket: подсветка, wall lights, A/C, ovens | **A taxonomy gap.** A вывод is not a розетка and is not priced like one — it is a `resource_role` the BOM needs, and the model's 13 electrical elements do not distinguish it |
| **A socket group can carry a `vertical` status that changes its representation on развёртки and in 3D but NOT on the plan** | An element property whose rendering is **per sheet type** — a data-model insight for our own sheet pipeline |
| **Floor and ceiling sockets carry two mounting dimensions to the nearest walls**, still to the centre | Dimensioning rule for points not on a wall |
| Grouping is **creation-order dependent** — two already-placed sockets will not merge; one must be deleted and re-placed | A tool quirk, **worth recording only as evidence that grouping is a modelled relation rather than proximity** |

**→ Process 6 of the 13 lessons, as a specification and not a tutorial**: Урок 2 (построение помещений), **4 (электрика и освещение)**, 5 (чистовая отделка → `cap5` finish schedule, designed but unpopulated), **7 (развёртки стен → we have `room_rollouts.csv` and `check_room_rollout.py`)**, 8 (инженерные системы), 12 (рисование плана по картинке → compare the ~2 h manual `v0` trace). Skip 1, 3, 6, 9, 10, 11, 13.

**And separately — the same channel's non-lesson videos are ordinary Group A/B renovation knowledge and go through the normal pipeline:** «Планировка кухни. 12 золотых правил» (24 min) and «Планировка санузлов. 12 золотых правил» (14 min) are **structured rule sets, i.e. direct `rules.jsonl` fodder**; plus «Как разместить розетки на кухне и избежать ошибок», «Как спланировать розетки перед ремонтом», «Ошибки при планировке квартиры», «Как правильно снять замеры квартиры прежде чем начинать ремонт», «Перепланировка — какую планировку можно согласовать» (⚠️ Russian jurisdiction — rule 4), «Приемка стяжки», «Проходные выключатели», «Разводка электрики по полу или по потолку».

⚠️ **Dedup warning before touching those**: this vault is dense on sockets, стяжка and планировка. Apply the two-shapes-of-saturation test (`@YourInteriorDes` Round 5, conclusion 5) — and grep **both** the Russian term and the English page phrasing plus a folder filename listing before calling anything a gap (the `Water_Inlet_Node_Components.md` error, `vasilysanuzel_channel_triage_20260908.md`).

### Tier 2 — process, narrow and small

| Item | Length | Take | Caveat |
| :--- | :--- | :--- | :--- |
| **`A1HxpHxrvv4`** Craftelectric, «Считаем кабель, гофру и штробы в SketchUp» | 5:36 | **Electrical quantity take-off from a 3D model** — cable, conduit and chase lengths. Feeds `ELE-01` BOM quantity, currently `unmeasured` | Plugin-specific; take the *quantity definition*, not the plugin |
| **`9-hQsyWSnm4`** Craftelectric, «Как нарисовать стены по плану в MoonCAD: подложка, масштаб, перегородки» | 18:45 | **Tracing walls over a scaled raster underlay** — the method for the `v0` manual trace, and adjacent to the `cap0` scale desk-check | MoonCAD, not our tool |
| **`BLnfvEmFsm4`** / **`tAng1kRYkOg`** Craftelectric, 3D flat model from a drawing | 11:52 / 9:43 | The "how to build the 3D model" sequence at its simplest | Likely thin next to k_dmitry |
| **`S_swPgeM-XM`** Craftelectric, sockets + lighting in SketchUp | 10:44 | Second instance of the electrics-on-model workflow | |
| **`MZv33G7UE_A`** mind.sight.studios + **`sSnjQJX4-iY`** MasterSketchUp, **Quantifier Pro** cost estimating | 10:30 / 16:54 | ⚠️ **The design of a quantity→price join — the one genuinely absent tool per the gap analysis.** What we want is its *schema thinking*: how a model quantity becomes a priced line, and how it re-prices | **English, US/AU market. Prices are irrelevant; only the mechanism transfers.** Rule 2 makes the figures unusable anyway |
| **`s0TrXB2WQ2Q`** «Как быстро составлять смету с помощью SketchUp и Excel» | 8:39 | Same idea, Russian, **Omsk 2020** | Rule 2: 2020 Omsk RUB is not comparable. Take the *method*, discard every figure |
| **`PVXE79HM0-c`** Стройплощадка, «ТОП программ для ремонта квартир» | 15:06 | One cheap survey of the tool landscape — calibrates what a Russian renovation market actually uses | Probably a listicle; ⚠️ check for sponsorship (advertising filter) |

### ✗ Tier 3 — skip, with the reason

| Item | Why skipped |
| :--- | :--- |
| **`@АлександрЭлектрик-ц3н`** — whole channel | **Only 3 videos, 2:11 / 4:47 / 2:11**, «Электропроводка своими руками». Hobbyist DIY at a fraction of the depth `12_Engineering_and_Systems/` already holds from specialists. Not fetched → no CSV row needed |
| **`ZXv5HK8Lhys`** «Ремпланнер расстановка розеток, сантехники, света» (5:17) and **`9muFQQZsgsU`** «Простой способ создать идеальный план светильников в Ремпланнер» (3:18), Дом с Фишкой | Thin third-party RemPlanner tips, **wholly superseded by RemPlanner's own Урок 4 and 8**, which are 18 and 16 minutes and authoritative. Excluded on title+length skim, never fetched |
| **`YA9y2IwhCMc`** «Смета на ремонт квартиры. Стоимость ремонта» (5:38, Дмитрий Павлов, СПб) | Its entire content is price figures from **2020 St Petersburg**. **Standing rule 2 kills it**: a price without a comparable location and year has minimal value, and we cannot make 2020 SPb RUB comparable to 2026 Minsk. Skipped on the value it *claims*, not on quality |
| **`fuOjlEj4MbU`** «Craftelectric Tools плагин для электрики в SketchUp» (4:06) | A plugin announcement. Its substance is in `A1HxpHxrvv4`, kept above. Skip as a standalone |
| **`PqvvsL625rc`** «Большой проект для реализации в SketchUp», Vasily_Sanuzel (18:01) | ⚠️ **Already triaged today** as a Tier-2 candidate on its own channel — see [`vasilysanuzel_channel_triage_20260908.md`](vasilysanuzel_channel_triage_20260908.md) line 84. **Leave it in that channel's queue; do not double-handle it here.** Its natural next-single-item there is `9aKNikb29FI` |

## 4. Loose-video ledger

| ID | Channel | Date | Len | Tier |
| :--- | :--- | :--- | :--- | :--- |
| `fuOjlEj4MbU` | Craftelectric | 2025-04-24 | 4:06 | ✗ 3 |
| `PqvvsL625rc` | Vasily_Sanuzel | 2025-08-09 | 18:01 | → other channel's queue |
| `s0TrXB2WQ2Q` | Ремонт квартир Омск | 2020-11-22 | 8:39 | 2 |
| `YA9y2IwhCMc` | ЭЛЕКТРОМОНТАЖ и САНТЕХНИКА СПб / Дмитрий Павлов | 2020-02-09 | 5:38 | ✗ 3 |
| `PVXE79HM0-c` | Стройплощадка | 2025-03-27 | 15:06 | 2 |
| `ZXv5HK8Lhys` | Дом с Фишкой | 2025-01-08 | 5:17 | ✗ 3 |
| `9muFQQZsgsU` | Дом с Фишкой | 2025-04-01 | 3:18 | ✗ 3 |
| `MZv33G7UE_A` | mind.sight.studios | 2025-10-16 | 10:30 | 2 (EN) |
| `sSnjQJX4-iY` | MasterSketchUp | 2020-07-20 | 16:54 | 2 (EN) |

**Dates confirmed from `yt-dlp` metadata, not titles** (rule 2). Russian titles obtained only by forcing `--extractor-args youtube:lang=ru` — the now-familiar auto-translated-metadata trap.

## 5. ⚠️ Where this content lives — the Group C decision, made explicitly

Group C's condition was to decide this *before* a trial batch, and not to default into the existing buckets. **Decision: the content splits, and the split is clean.**

**Half of it is ordinary renovation knowledge and routes normally.** Socket heights, door-swing rules, ceiling-drop tradeoffs, the «12 золотых правил» sets, стяжка acceptance — these have existing taxonomy buckets (`Switches / Sockets / Cables`, `Lighting`, `Planning Rules`, `Quantities / Measurements`, `Design Concept`) and existing wiki homes. **No new structure needed; standard pipeline, standard dedup.**

**The other half is about our own production process and has no bucket, because the taxonomy is a taxonomy of the renovation, not of the project's documentation.** Dimension datums, the `1/2` notation, sheet-set composition, the вывод/розетка distinction, the staged workflow, the quantity→price join. Forcing these into `12_Engineering_and_Systems/` would bury a drawing convention inside a page about wiring.

**→ These go to `00_Master/`, which is already where this project's own method lives** (`wiki_page_format.md`, `Model_and_Views.md`, `Evidence_Reading_Discipline.md`, `Revit_AutoCAD_Integration_Strategy.md`, `Planning_Project_Deliverable_Set.md`). Specifically:

| Extracted content | Destination |
| :--- | :--- |
| Dimension datums, the `1/2` centred-fixture notation, per-sheet representation rules, annotation conventions | **A new `00_Master/Drawing_Conventions_From_Practice.md`**, cross-referenced from `Planning_Project_Deliverable_Set.md` and `Sheet_Production_Roadmap.md`. ⚠️ And per §E of the gap analysis, the datum decisions must also land in `.agents/skills/residential-bim-geometry-rules/` **before `cap3` produces dimensions** |
| Sheet-set composition, tab structure, when a sheet is legitimately empty | `00_Master/Planning_Project_Deliverable_Set.md` — whose own line 144 invites it: *"treat the sheet list as a checklist to argue with"* |
| The staged workflow, tool-to-tool handoffs, client-review mechanics | `00_Master/Model_and_Views.md` / `Options_And_Versions.md` |
| Element types and properties the model lacks (вывод провода, vertical group) | `data/canonical/` schema + `Finishes_and_Furniture_Data_Model.md` |
| Machine-readable layout/planning rules with rationale | `data/layout_rules/rules.jsonl` — ⚠️ **note the gap analysis's finding that nothing currently CONSUMES this file**; adding rules to it is still correct, but a rule checker is the cheapest unbuilt tool |
| Quantity definitions and the quantity→price join | `data/procurement/bom.csv` design + the cost-engine build order |

**Source extraction notes still go to `_Sources/` and the store still to `_Knowledge/store/` as always** — this decision is about *wiki routing*, not about changing storage paths. `Rules_Heuristics.md` and `Durable_Facts.md` take the store side.

## 6. Findings this triage produced on its own, before any extraction

Two are worth recording because they are repo facts, not source facts:

1. ⚠️ **There is no A/C plan sheet anywhere in our deliverable set.** `grep "кондиционер"` returns **0** in both `Planning_Project_Deliverable_Set.md` and `Sheet_Production_Roadmap.md`, and no vault page carries a план кондиционеров. k_dmitry ships one as a tab and uses it to place the вывод and to justify moving a unit above a door. **Our 16-sheet set was derived from a single architect's album (Dolgushev); this is the second independent instance of a sheet set, and it immediately shows an omission.** Worth deciding on its own merits — if A/C is in scope for this flat, a sheet is missing.
2. **The vault-wide index drift reported on 2026-09-03 has grown, not been cleared.** `preflight_playlist.py` now reports **581** source notes with no matching flat-index ID (was 565) and 98 indexed IDs with no source note. Unrelated to this list. **`tools/build_knowledge_base_index.py` wants a rebuild as separate work** — and it should happen before a 328-video channel starts adding notes.

## 7. Recommendation

**Process, in this order, and stop after step 1 to check yield:**

1. **Round 1 on `@k_dmitry`, 5 videos**, all reasoning-format: `DI5GAV64mnU` (already fetched and read), `YEpfNcwwGoU` (обоснование планировочного решения), `F0rXrbPDPf4` or `kD1dFGQh4EU` (a second technical walkthrough, to test whether the format repeats or the first one was the good one), `TJVXUCKQ1UU` (Планоплан + SketchUp together), `FRKr9X3AFfY` (doors and partitions as a planning decision). **Run `extract_layout_frames.py` on at least the two walkthroughs.**
2. **RemPlanner lessons 4, 7, 5, 8, 2, 12** — as specification. Lesson 4 is already fetched.
3. **RemPlanner's two «12 золотых правил» + the socket/замеры/ошибки set** — normal pipeline, hard dedup first.
4. **Tier 2 singles**, cheapest last: `A1HxpHxrvv4`, `9-hQsyWSnm4`, the Quantifier Pro pair, `s0TrXB2WQ2Q`, `PVXE79HM0-c`.

**Expected shape of the yield, stated in advance so it can be checked**: **fewer facts per video than a Group A channel, but structurally heavier ones.** A Group A source adds a paragraph to a wiki page; most of what this group yields changes a **field, a datum, a sheet or a rule**. So the standard yield metric will understate it, and the honest measure is *how many of our open `cap` items moved*. Record both.

**Against processing at all — the case, stated fairly:** the gap analysis concluded the remaining work is *"retrieval and building, not research"*, and this list is research. If the goal is a budget number soonest, the cost track needs none of this. **The counter, which is why the recommendation is still "process": three of our open items are blocked on conventions we have not chosen** (the dimension datum, setting-out notation, the вывод/розетка element split), **and `cap6`/`cap8` are blocked on knowing what a derived services plan even contains.** k_dmitry answers all five from practice, and §E's warning stands — these are cheap to choose now and expensive to retrofit after `cap3` emits dimensions.

## Open questions this triage does not settle

- **Whether k_dmitry's yield holds past the first walkthrough.** One video was read. The format-based scoping above is a hypothesis, and `F0rXrbPDPf4`/`kD1dFGQh4EU` in Round 1 are there specifically to test it.
- **Whether an A/C plan sheet is in scope** (§6.1) — an owner decision, not a research one.
- **Whether the `1/2` centred-fixture notation can be expressed in our DXF/SVG pipeline at all**, or whether it needs Bonsai's annotation subsystem. Testable, and it interacts with the open Bonsai-headless question in the gap analysis.
- **Nothing here addresses the owner's re-quoting/substitution axis.** This whole list is geometry-and-documentation. The cost engine's primary axis gains nothing from it except the Quantifier Pro schema thinking.
