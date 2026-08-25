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

## Sheet list of the planning project (16 sheets)

Machine-readable, with per-sheet "can we generate this today?" verdicts, in
[`dolgushev-planirovochny-proekt.json`](../data/deliverable_templates/dolgushev-planirovochny-proekt.json).
Summary of where this repo stands:

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
