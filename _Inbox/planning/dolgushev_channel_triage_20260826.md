# Channel triage — @SergeyDolgushev (ARCHIDOLGUSHEV)

Date: 2026-08-26. Channel: <https://www.youtube.com/@SergeyDolgushev>
Author: Sergey Dolgushev, architect / interior designer, Moscow. Sells free
layout variants as lead generation and a paid "планировочный проект".

Whole channel is **12 videos**, all 3–8 minutes. Transcripts fetched and skimmed
for all 12 (auto-generated Russian captions; the two processed videos have
manual ones). Small enough that no sampling was needed.

## Verdict summary

| Video | Length | Verdict | Why |
|---|---|---|---|
| [DQLaOE_A-NA](https://www.youtube.com/watch?v=DQLaOE_A-NA) — ПЛАНИРОВОЧНЫЙ ПРОЕКТ как альтернатива дизайн-проекту | 6:06 | **PROCESSED** | Full case + the deliverable-set spec. Album PDF matched sheet-by-sheet. |
| [dQq6CxBC7VI](https://www.youtube.com/watch?v=dQq6CxBC7VI) — 30 разных квартир | 7:46 | **PROCESSED** | 30 sub-cases, each linked to its album page. |
| [YE8QsC54yK4](https://www.youtube.com/watch?v=YE8QsC54yK4) — Планировка квартиры бесплатно, обзор | 6:37 | **HIGH — process next** | The only video that states the intake method: план обмеров + ТЗ with состав и назначение помещений **и состав семьи**; records orientation (юго-восток), noise (проезжая часть), fixed wet zones, window count. Three principled variants. This is the closest thing on the channel to a repeatable method. |
| [SuPsziP2K4w](https://www.youtube.com/watch?v=SuPsziP2K4w) — Как выбрать планировку при покупке | 5:27 | **HIGH** | Gas-stove constraint forces a closed kitchen in every variant ("возможно объединить кухню-гостиную, но тогда нужно отказаться от газовой плиты в пользу электрической") — a hard constraint rule we do not have yet. Also pre-purchase evaluation as a use case. |
| [G2BYWG7WlCE](https://www.youtube.com/watch?v=G2BYWG7WlCE) — Планировочные решения, краткий обзор | 5:09 | **HIGH** | Explicit pros/cons per variant, including a genuine daily-life scenario argument: private zone placed deep in the flat means a teenager cannot reach their bedroom without crossing the living room. Exactly the scenario-driven reasoning you asked for. |
| [OFad5vcmuVs](https://www.youtube.com/watch?v=OFad5vcmuVs) — Выбираем квартиру для покупки | 4:18 | **MEDIUM-HIGH** | Four separate bedrooms demanded; the whole video is the trade-off "windowless 4th bedroom vs. smaller bedroom with a window vs. wardrobe instead" — a clean worked example of `daylight.third_room_costs_a_window`. |
| [oux5xZwOz3I](https://www.youtube.com/watch?v=oux5xZwOz3I) — Перепланировка, бесплатные варианты | 6:33 | **MEDIUM** | One 3-room ~90 m² case, "сделать две…"; long channel-anniversary preamble eats a third of the runtime. |
| [SOGErWGW1FA](https://www.youtube.com/watch?v=SOGErWGW1FA) — Краткий обзор планировок от подписчиков | 4:44 | **MEDIUM** | Two small apartments; useful mainly for the zone checklist he applies (кухня / обеденная / мягкая / спальная / рабочие места). Heavy self-promotion. |
| FaoAV6ZiqvI, FBWoVVkwPZk, 8qG82Yv3I4s, 16bT2azTj3o, 1Wey5HAhzZI — «Пуки творчества» #1–#5 | 3:00–4:00 each | **SKIP for layout** | Spot-checked #5: it is a reference/mood-board diary about designing his own flat, not layout analysis. #4 ("Дизайнер проектирует интерьер для себя") may hold taste/method material for `17_Design_and_Ergonomics`, but nothing for the layout dataset. |

## Recommended next batch

Process **YE8QsC54yK4 → SuPsziP2K4w → G2BYWG7WlCE → OFad5vcmuVs** as one batch of
four. Each is a `single_apartment` case with real `variants[]`; together they
should also corroborate or contest these existing single-source rules:

- `daylight.third_room_costs_a_window` (OFad5vcmuVs is a second instance)
- `process.minimum_two_variants` (all four)
- `corridor.is_the_area_donor` (G2BYWG7WlCE removes a long corridor into a wardrobe)

and are likely to add at least: a gas-stove/kitchen-merge constraint rule, an
orientation/noise-driven room-assignment rule, and a
privacy-route/daily-scenario rule.

No companion PDFs for those four, so they will be transcript+frame only — the
plans are shown on screen but the album is not published. Use
`--mode speech`; these are narrated case studies, not catalogues.

## Notes for the next run

- All four are short, so `--per-seg 2 --min-seg 20` is a better fit than the
  defaults tuned for Zemskov's longer format.
- Fetching all 12 transcripts back to back at ~20 s spacing did not trip a rate
  limit today.
