# Планировочный проект — the target deliverable set

## Purpose

This page describes what the end product of this whole project should look like:
the document set you hand a contractor to start the renovation. It is written
from one real, delivered album, so the target is an observed artefact rather
than a wish list — and it names the gap between that target and what this repo
can currently generate.

The pipeline it sits at the end of: **wiki pages → layout dataset → CAD/BIM
model → this document set**.

## The reference product

Architect **Sergey Dolgushev** (ARCHIDOLGUSHEV, Moscow) sells a *планировочный
проект* explicitly positioned as an alternative to a full дизайн-проект. In his
own words it is "индивидуальная рациональная планировка и альбом всех
необходимых для ремонта чертежей — без визуализации, спецификации и ведомости и
прочих дополнительных материалов, которые влияют на стоимость проекта в сторону
его удорожания" ([video](https://www.youtube.com/watch?v=DQLaOE_A-NA), 01:40).

Two tiers of his own product are on record here, which makes the scope decision
legible:

| | Планировочный проект | Дизайн-проект |
|---|---|---|
| Sheets | 16 + 3D макет | 30 |
| Scale | scale bar only | M 1:50 printed |
| Dimensioned plan | on survey/setting-out sheets | separate размерный план sheet |
| Wall elevations (развёртки) | ✗ | ✓ 6 sheets |
| Schedules (ведомости) | ✗ | ✓ 3 sheets |
| Air-conditioning layout | ✗ | ✓ |
| Visualisation | 3D массинг в том же сером стиле | photoreal renders |
| Machine-readable spec | [`dolgushev-planirovochny-proekt`](../data/deliverable_templates/dolgushev-planirovochny-proekt.json) | [`dolgushev-dizayn-proekt`](../data/deliverable_templates/dolgushev-dizayn-proekt.json) |

Dolgushev's stated reason for the 3D макет rather than renders is worth keeping:
"не все обладают достаточным воображением, чтобы представлять, как планировка
выглядит в объёме — макет в этом поможет". It sells understanding of volume, not
a picture of a finished interior. That is a cheaper promise to keep, and it is
the one this repo is actually equipped to make (`tools/blender/`, `tools/ifc/`).

## How the set is arrived at, not just what is in it

The album is the *last* step. Dolgushev's process, from the same source:

1. **Inputs**: исходный план + план обмеров + a stated brief. Nothing starts
   without measurements.
2. **Options, never one answer** — "вариантов всегда было минимум два, в среднем
   три". For Новая Рига: four variants, each a complete furnished plan plus an
   axonometric, on one A3 sheet.
3. **One room held constant.** Across all four variants the детская stays 10,2 м²;
   what varies is прихожая, кухня, спальня and санузел. Observed from the sheets
   rather than stated — it makes the variants comparable and shrinks the search.
4. **Client assembles the final from parts**: "из 4 варианта мы взяли блок
   прихожей, кухни-гостиной и ванной комнаты, из 3 — спальни с гардеробом и
   расстановку мебели в детской". The variants are deliberately separable into
   blocks (входная группа / кухня-гостиная / санузел / спальня).
5. **Then, and only then**, the drawing set is produced from the agreed plan,
   sent for approval, corrected, and reissued as the final album.
6. **3D макет last**, built from the final album.

Steps 2–4 are the part this repo's `variants[]` structure exists to hold — see
[`data/layout_cases/dolgushev-novaya-riga.json`](../data/layout_cases/dolgushev-novaya-riga.json).

## Our own target set (scope decision 2026-08-26)

Underfloor heating is **not being installed**, so that sheet is dropped: our
target is **11 sheets**, recorded with per-sheet scope and capability status in
[`price-scrapper-target-set.json`](../data/deliverable_templates/price-scrapper-target-set.json),
with the work to get there in [Sheet_Production_Roadmap.md](Sheet_Production_Roadmap.md).

## Sheet list of the planning project (16 sheets)

Machine-readable, with per-sheet "can we generate this today?" verdicts, in
[`dolgushev-planirovochny-proekt.json`](../data/deliverable_templates/dolgushev-planirovochny-proekt.json).
Summary of where this repo stands:

> [!NOTE]
> Corrected 2026-08-26 after inspecting `data/outputs/current_apartment/sheets/`:
> four A3 sheets **already generate** from the IFC seed (architectural, floor plan,
> electrical/lighting, plumbing), with symbol-placement validation. The verdicts
> below were written before that check and understated what exists; the current
> per-sheet status lives in the target set and the roadmap.

- **Producible from the model we already build** (4 sheets): furniture plan,
  survey/demolition plan, new-partitions plan, door-opening marking plan —
  via `tools/ifc/current_apartment_layout.py` and `tools/drawings/floor_plan_svg.py`.
  Blocked on the same thing in every case: the DXF control dimension is still
  unapproved (`tools/cad/PROVISIONAL_MODEL_POLICY.md`).
- **Producible with a schedule layer** (1 sheet): floor finishes with areas —
  `tools/ifc/calculate_wall_finishes.py` does the equivalent for walls.
- **Not yet modelled at all** (5 sheets): underfloor heating, lighting +
  switch grouping, reflected ceiling, sockets/switches, sanitary equipment.
  These need an engineering-systems layer that does not exist yet, and the
  lighting and socket sheets additionally need the *daily scenarios* to be
  written down as data, not prose.
- **3D массинг** (5 sheets): `tools/blender/` can produce geometry; what is
  missing is a consistent grey monochrome output style.

## Graphical conventions worth copying

Observed across both albums — these are cheap to imitate and carry real meaning:

- **Dashed lines show the original partitions** on every variant sheet, so a
  reader sees what changed without a second drawing.
- **Wet zones filled pale blue** (kitchen, bathrooms) — the constraint that
  drives most layout decisions is visible at a glance.
- **Red hatch = demolished**, with its own legend on the demolition sheet.
- **Экспликация block** on every plan sheet: numbered rooms with areas, plus a
  key explaining "номер по экспликации / площадь помещения".
- **Scale bar and north/entry arrow on every sheet**, even where a scale ratio
  is printed.
- **The final variant sheet is flagged by a coloured background** — the album
  tells you which one won without words.
- In the catalogue album, every object is a **before | after pair on one
  landscape page**, numbered, with "?" marks on rooms whose use is unknown in
  the "before" state. Honest about what is not known.

## A caution taken from the same source

Dolgushev deliberately does **not** dimension the free schemes: "как только на
схемах появятся размеры, за них придётся отвечать — а мы работаем с теми
материалами, которые присылаете нам вы". He gives a scale bar and draws to
scale instead. For us this cuts both ways: it is a sound rule for anything drawn
from someone else's measurements, and it means **no number taken from that
catalogue may be treated as a dimension** — recorded as
`dimension_policy: scale_bar_only` on the case.

## Source Notes

- [`data/layout_cases/dolgushev-novaya-riga.json`](../data/layout_cases/dolgushev-novaya-riga.json) —
  full case: 4 variants + final, dimensions read off the album, moves and trade-offs.
  Video [DQLaOE_A-NA](https://www.youtube.com/watch?v=DQLaOE_A-NA) + `00_Master/DQLaOE_A-NA_Новая_Рига_Планировочный_проект.pdf` (28 pp, Москва 2021).
- [`data/layout_cases/dolgushev-100-album-survey.json`](../data/layout_cases/dolgushev-100-album-survey.json) —
  30 apartments from the first hundred objects, each linked to its album page.
  Video [dQq6CxBC7VI](https://www.youtube.com/watch?v=dQq6CxBC7VI) + `00_Master/DQLaOE_A-NA_альбом_100_кв.pdf` (104 pp).
- `00_Master/dQq6CxBC7VI_albom_pr.pdf` (30 pp, 2018) — full design-project album
  for the apartment that appears as object #71 in the catalogue album. Confirmed
  the same object: the room schedule matches exactly (прихожая 11,7 / санузел-постирочная 5,8 /
  кухня 13,9 / гостиная 14,5 / спальня 15,9 / санузел 4,8 / гардероб 4,0 / гостевая 15,5 м²).
  It is the worked example of a free variant becoming a delivered project.
- Everything above is one practitioner's commercial product and his opinion of
  what a renovation needs. Treat the sheet list as a checklist to argue with,
  not a standard.

## ⚠️ A second, independent sheet set — and it exposes an omission (2026-09-08)

**The invitation above was taken up.** Everything on this page to this point derives from **one** practitioner, architect Sergey Dolgushev. Round 1 of the design-toolchain intake produced a second sheet set from a different designer, in a different tool, on two different flats — **Дизайнер Дмитрий К** (Moscow, [`YT_F0rXrbPDPf4`](../_Sources/YT_F0rXrbPDPf4_kdmitry_technical_project_remplanner_review.md), corroborated by [`YT_DI5GAV64mnU`](../_Sources/YT_DI5GAV64mnU_kdmitry_technical_project_remplanner_festivalnaya.md)).

**His tab set, as walked on camera** (18 tabs): исходная планировка · демонтаж · перегородки *(with every partition dimensioned)* · экспликация · **расположение радиаторов** · мебель · привязки сантехники *(drawn in green)* · водоснабжение *(осевые привязки)* · розетки *(heights, plus a per-socket note saying what it serves)* · освещение · **выключатели** *(which switch drives which group, groups colour-coded, lines drawn from switch to group)* · тёплые полы *(+ thermostat)* · **кондиционеры** · напольные покрытия *(material and laying pattern)* · схема отделки *(tile in brick-red, wallpaper elsewhere)* · схема потолков *(material + за-карнизные niches)* · **схема гидроизоляции** · развёртки стен *(carrying electrics AND finishes, so heights read off them)*.

> [!WARNING]
> **⚠️⚠️ WE HAVE NO A/C SHEET AT ALL.** `grep "кондиционер"` returns **0** in this file and **0** in [`Sheet_Production_Roadmap.md`](Sheet_Production_Roadmap.md), and no vault page carries a план кондиционеров. **Both of his projects ship one, and on one of them it is what records the unit being moved to above a door with a вывод rather than a socket serving it.**
>
> **This is exactly what a second opinion is for, and it is an owner decision rather than a research one: if air conditioning is in scope for this flat, a sheet is missing from the target set.**

**Three further points where his set differs from ours, each worth arguing with:**

1. ⚠️ **The finish scheme is explicitly a costing input, not only a drawing** — *«эта схема отделки… также поможет в расчёте стоимости ремонта»*. **That is the practitioner stating the `cap5` finish-schedule → BOM link that [`toolchain_gap_analysis_20260908.md`](../_Inbox/planning/toolchain_gap_analysis_20260908.md) identified as designed-but-unpopulated.** It argues the finish sheet is worth more than its position in our roadmap suggests, because it pays into the budget as well as the drawings.
2. **A dedicated radiator-position sheet and a dedicated waterproofing scheme**, neither of which we carry separately.
3. ⚠️ **He states outright that the строительные plans are NOT the designer's deliverable** — *«эти строительные планы меня не интересуют, дизайнер их не отрабатывают»*. Relevant when deciding which of our sheets a self-managed project with no designer engaged actually needs.

**And one convention of ours that he independently corroborates**: variants are presented over the original layout as a visible underlay ([`YT_FRKr9X3AFfY`](../_Sources/YT_FRKr9X3AFfY_kdmitry_doors_partitions_planning.md): *«показываю изначальную планировку, чтобы была видна разница, в виде подложки»*), which is our own dashed-original-partitions rule reached separately.

**Drawing and annotation conventions from the same round — dimensioning to element centres, the `1/2` proportional notation for a centred fixture, «вывод провода» as an element distinct from a socket, and per-sheet layer states — are collected in [Drawing_Conventions_From_Practice.md](../18_Digital_Toolchain/analysis/Drawing_Conventions_From_Practice.md) rather than here.** That page also records why our grey-massing 3D convention is worth revisiting.

⚠️ **Caveat on all of the above**: auto-generated Russian captions on software subject matter, with observable ASR corruption and one transcript carrying no punctuation at all. The tab list is read from narration, so **the order is reliable and a couple of tab names may be imprecise.** Nothing here has been checked against a Belarusian requirement.


## ⚠️⚠️ A SECOND observed album — and it is the engineering half this page lacked (Алексей Шемчук, added 2026-09-14)

**This page was written from one album (Долгушев) and names its own gap: five sheets "not yet modelled at all" — underfloor heating, lighting + switch grouping, reflected ceiling, sockets/switches, sanitary equipment.** **Долгушев's cheaper tier explicitly OMITS the engineering sections. Шемчук's album is mostly engineering, shown sheet by sheet across five videos.** **The two are complementary: Долгушев gives the scope tiers and sheet counts, Шемчук gives what is on an engineering sheet and why.**

⚠️ **2021, one practitioner, his own conventions — not a standard.**

### ⚠️⚠️ The method: «модель, альбом, объект»

**Build it full-size in a 3D model → derive the album from the model → execute on site.** His stated goal:

> ***«Я задачей своих проектов ставлю стопроцентную реализуемость — отсутствие необходимости в каких-либо дополнительных размышлениях и переделках уже во время выполнения работ.»***

- **⚠️⚠️ FULL-SIZE MEANS FULL-SIZE**: plumbing modelled down to the **mounting plates**; plasterboard modelled as real profiles **AND actual 2 m boards, with the sheet layout chosen so the quantity can be counted exactly.** **→ Take-off falls out of the model as a by-product — which is what [[18_Digital_Toolchain/analysis/Quantity_Takeoff_and_Cost_Join|Quantity Take-off & Cost Join]] is reaching for, arrived at by modelling real parts rather than by a separate estimating step.**
- **⚠️ THE ORDERING PRINCIPLE:** *«Все работы в проекте показаны в той последовательности, в которой они выполняются на объекте.»* **The album's sheet order IS the construction sequence**, which is why it ends with furniture.
- **⚠️ Inside every discipline the sequence is the same: plan the rooms and place ALL the furniture first, then run the services to suit.**

### ⚠️⚠️ The structure: initial state → final state → the path between

1. **Title sheet** — address, short description, and **the people RESPONSIBLE for the project and the works, with phone numbers**, because *«альбом всегда находится на объекте»* — **a tradesman's question is resolved without involving the client.**
2. **Contents sheet** with page numbers.
3. **Survey plan** with dimensions **plus a 3D view for comprehension**, risers, radiators, levels, as handed over.
4. **Post-replanning dimensions** and the final state.
5. **Per-room sheets** with every finish, decor element and furniture item. **⚠️ Where something is unchosen it is fixed by TYPE and left open by model** — "track light" without a fitting. **→ The sheet records the decision made and is honest about the one that is not.**
6. **Order-of-works sheet(s)** — stages down, detail across.
7. Then the disciplines in build order, ending with furniture.

### ⚠️⚠️ The datum rule — pick a mark that cannot move

> **The clean-floor datum is a point that WILL NOT CHANGE during the works — he uses a point on the STAIRWELL LANDING, on the door-handle side, drawn in the project and marked in red on site.**
>
> **The reasoning transfers: marks get knocked out and contractors get replaced, and then nobody knows what anything was measured from.** *«Они открывают проект, видят эту метку, меряют всё от неё, и в конечном итоге все сходятся в одном едином горизонте.»*
>
> **→ ⚠️⚠️ The same idea as this repo's own standing rule that a scale must be INDEPENDENT of the thing being measured ([[00_Master/Evidence_Reading_Discipline|Evidence Reading Discipline]]), applied to a building site: the datum must be outside the work.**

### ⚠️⚠️ THE ORGANISING INSIGHT — every sheet is detachable

**Said repeatedly about different sheets: the demolition sheet carries work VOLUMES so a contractor can price it without the designer recalculating; the plastering sheet carries areas and linear metres for the same reason; the stretch-ceiling sheet can be sent to several ceiling firms for quotes; the internal-door sheet carries leaf sizes AND the wall thicknesses they go into, so the client can walk into a shop with it; the kitchen sheet numbers every module against a decoding table.**

> **→ ⚠️⚠️ EACH SHEET IS BUILT TO BE DETACHED AND HANDED TO ONE TRADE OR SUPPLIER, priced and executed without the designer mediating.** **That is a different design goal from "a complete set of drawings", it explains most of his conventions, and it is the property this repo's own target set should be judged against.**
>
> **⚠️ A scope data point for planning: his complete, buildable VENTILATION section came to THREE sheets.**

[source: [[_Sources/YT_0c-QhBDQMWE_shemchuk_technical_design_album_series|YT_0c-QhBDQMWE]] (+ZkdKiLQKJIc, oibpAA8OL_Y, vwM08Vu31Gc, bsX-42_S_Uc)]

## ⚠️⚠️ A THIRD observed album — and it is the one the owner has named as his target (lab|remont, added 2026-09-18)

**`_Inbox/_Visual_Drop/Инструкция_по_ремонту_#7317795_Для_портфолио_15.pdf`, 45 pages / 37 sheets.** Technical expert *Олег*, lab|remont; live planner at `labremont.floorplan.tools/planner/oid7317795`.

> **The owner supplied it to say what he wants OUT of this project**: *"I want something closer, the set of drawings… I need something like 2D plan, to inquire for plumbing, for ventilation and so on."* So this is not another comparison album — **it is the specification for our own output.**

### The full sheet list, as observed

| | sheet | | sheet |
| ---: | :--- | ---: | :--- |
| 1 | Этапы работ | 20 | Электропроводка |
| 2 | Исходный план | 21 | Напольные покрытия |
| 3 | Демонтаж | 22 | Отделка стен |
| 4 | Перегородки | 23 | Потолки |
| 5 | Помещения | 24 | Гидроизоляция |
| 6 | Окна, откосы, подоконники | 25 | Штукатурка |
| 7 | Радиаторы | 26 | Стяжка |
| 8 | Мебель | 27 | Развертки стен (index) |
| 9 | Сантехника | 28–29 | Развертки — Кухня-гостиная (1–6) |
| 10 | Водоснабжение | 30 | Развертки — Детская (1–11) |
| 11 | **Штатная электрика от застройщика** | 31 | Развертки — Спальня (1–6) |
| 12 | Розетки | 32 | Развертки — Прихожая-коридор (1–6) |
| 13 | Освещение | 33 | Развертки — Кабинет (1–4) |
| 14 | Выключатели | 34 | Развертки — СУ 2 (1–6) |
| 15 | Теплые полы | 35 | Развертки — Гардеробная (1–4) |
| 16 | Кондиционеры | 36 | Развертки — СУ 1 (1–6) |
| 17 | Электрощиток | 37 | Развертки — Помещение без названия (1–4) |
| 18 | Безопасность (датчики протечки) | | |
| 19 | Вентиляция | | |

### ⚠️ What it settles, and what it validates in work already done

- **`Лист 11` is «ШТАТНАЯ ЭЛЕКТРИКА ОТ ЗАСТРОЙЩИКА» — the developer's as-supplied electrics, as its own sheet.** That is precisely what `electrical_existing.csv` and the services-observed capture have been building, and **this album confirms it is a deliverable in its own right, not merely an input.** The migration apparatus was right to treat the existing sweep as first-class.
- **Sockets, lighting and switches are THREE SEPARATE SHEETS** (12, 13, 14), not one electrical sheet. Our services model already separates outlets from luminaires from switches; this says the *drawings* must stay separated too.
- **The set is ordered by TRADE SEQUENCE, not by discipline grouping** — demolition, partitions, then rooms, then services, then finishes, then elevations — and it opens with `Этапы работ`, a work-stages sheet. That matches the «initial state → final state → the path between» structure already recorded from Шемчук.
- **Развёртки are per room and numbered per wall** — `Детская (1–11)` means eleven wall faces in one room. `room_rollouts.csv` already models exactly this, and `check_room_rollout.py` already checks the loop closes.

### ⚠️ What it has that our 16-sheet planning set does not

`Гидроизоляция`, `Штукатурка`, `Стяжка`, `Теплые полы`, `Кондиционеры`, `Безопасность`, `Электрощиток` and `Электропроводка` are all separate sheets here. **That is the gap between a планировочный проект and the full album the owner is asking for** — and it is roughly a doubling of the sheet count, not a refinement of it.

> **⚠️ SCOPE CONSEQUENCE, STATED PLAINLY:** the owner's stated workflow is *experiment with the layout → settle on two or three preferred variants → place things and engineering systems in the 3D model → produce this set per final variant.* **At 37 sheets, producing this set for three variants is 111 sheets.** The set must therefore be GENERATED from the model, not drawn — which is the architecture already chosen, and this album is the strongest evidence yet that the choice was right.

## ⚠️ OWNER SHEET DECISIONS, 2026-09-18 — four of the five lab|remont additions

The lab|remont album (37 sheets) was compared against our own target album
(`zk-dubravinskiy-full-album.json`, 32 sheets, owner-decided 2026-09-07). **The 37
is NOT an adoptable number**: it is an observed album for a DIFFERENT flat, whose
room list includes `Кабинет`, `Гардеробная` and two `СУ` — so a large part of its
count is that flat's room count, and its 11 развёртки sheets do not transfer. The
answerable question was which **sheet TYPES** it has that ours lacks. Five. The
owner ruled on them:

| sheet | decision | the owner's reason |
| :--- | :--- | :--- |
| **`Этапы работ`** | ✅ **IN** | *"first to plan and then to keep track of the actual progress — that's why we need this sheet."* Order of work, volume, approximate timeframe. **He expects it to change on the way and says so** — it depends on external factors. So it is a LIVING sheet, not a fixed programme. Content belongs with `11_Budget_and_Planning/` |
| **`Штатная электрика от застройщика`** | ✅ **IN** | *"existing electric wiring — yeah, it's already built, that's correct."* Already modelled: `electrical_existing.csv` and the services-observed capture |
| **`Электрощиток`** | ✅ **IN** | *"a good sheet to plan beforehand… we will need this panel, we will need switches, and it's better to understand its appearance."* ⚠️ Note **«appearance»** — he wants the panel's COMPOSITION laid out, not just its position. This is the same panel he asked about in the internal passage on 2026-09-16 |
| **`Окна, откосы, подоконники`** | ⚠️ **PROBABLY IN, not settled** | *"frankly, I'm not sure… it could be thought of as a part of finishing work of the walls."* What tipped him toward yes: **the лоджия glazing replacement is already in scope**, and a possible window change in the 9.36 room (below) |
| **`Радиаторы`** | **NOT RULED ON** | Ours folds radiators into `Отопление`. ⚠️ It became live anyway — see the open item below |

> **⚠️ The stale 11-sheet target is a separate problem, not a third option.**
> `price-scrapper-target-set.json` (11 sheets) carries **no supersession marker of its
> own** — only the full album's free-text `supersedes` field records the replacement,
> and `validate_layout_data.py` globs every template equally. `Sheet_Production_Roadmap.md`
> still plans against those 11. **Supersession recorded in one direction only** is the
> same shape as every other defect this project has found.
