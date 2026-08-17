# Price Table Screenshot Analysis — Test Case

> [!NOTE]
> **Dual-purpose document.** This case study contains two distinct kinds of content: (1) renovation-budgeting evidence — the reconstructed labor-cost table below, sourced from real screenshots of a 44 m² Minsk apartment estimate — and (2) screenshot/parser test-fixture guidance ("Test Case Interpretation", "Recommended Automated Test Usage", "Screenshot Mapping Table" sections further down), written to validate a table-parsing/OCR pipeline rather than to document renovation costs. Both are kept together for now; splitting them into separate documents is a possible future cleanup, not done in this pass.

## Source

- **Screenshot folder:** `_Inbox\_Visual_Drop\` (10 PNG files, all named `Screenshot 2026-07-28 0*.png`)
- **YouTube video:** https://www.youtube.com/watch?v=XWmoyTQK1AQ
- **Video title (from page metadata):** "Какая стоимость ремонта квартиры в Новостройке Беларуси. Работа + Материалы в 2025. Минск мир"
  (approx. "What does apartment renovation cost in a new-build in Belarus. Labor + Materials, 2025. Minsk World")
- **Transcript availability status: AVAILABLE (correction from prior version of this file).** The earlier version of this document incorrectly stated the transcript could not be fetched. That conclusion was based only on a generic `WebFetch` of the video's HTML page, which does not retrieve captions — it was not a transcript-specific extraction attempt, so "unavailable" should never have been asserted.
  - **Retrieval method used:** This repository has a dedicated transcript pipeline, `.agents\skills\youtube-to-obsidian\SKILL.md`, which runs `.venv\Scripts\python.exe scripts\get_youtube_transcript.py "<url>" "<slug>"` (uses the `youtube_transcript_api` Python package to pull YouTube's own caption track, not page HTML).
  - Running that script against this video returned: `Error: Transcript already processed! (Duplicate hash: b385361e400f8525dc094ccc3ed55cc0884930c6ca78e846f1fcb459c1b1e046)`. This video had already been transcribed and archived on 2026-07-27, before this analysis file was first created — the transcript existed the whole time and simply wasn't checked with the right tool.
  - **Transcript artifact (pre-existing, not duplicated):** `_Archive\processed_sources\20260727_renovation_guide_mistakes_7_b385361e.txt`, logged in `00_Master\processed_sources.csv` as `run_20260727_13` (title: "How Much Does Apartment Renovation Cost in 2025 (44m2 Minsk Real Breakdown)", source_year 2025, region "Minsk Belarus", status `archived`). Per this repo's evidence-handling convention, that archived file *is* the canonical source artifact for this transcript — no second copy was created for this analysis, to avoid duplicate/conflicting source-of-truth files.
  - As a secondary cross-check, `yt-dlp --write-auto-subs --write-subs --sub-lang ru,en --skip-download` was also run manually (Python `yt-dlp` package, installed on demand) and successfully pulled the same video's auto-generated Russian and English caption tracks — confirming independently that captions do exist and are retrievable; the repo's already-archived transcript (extracted via `youtube_transcript_api`) was used as the citation source below rather than this ad-hoc copy, to stay consistent with the repository's own pipeline and avoid a second untracked transcript file.
  - **Caveat on transcript reliability:** this is an **auto-generated (ASR) caption track**, not a human-written transcript. Spoken numbers in particular are a known weak point for ASR — several stage-subtotal figures mentioned aloud in the video are transcribed as short, likely-truncated numbers (e.g., "14 дол", "12 долларов" for stages that, based on the itemized screenshot rows, plainly total in the hundreds/thousands). These narrated subtotals are cited below as rough spoken context only, never as verified figures, and are never used to override or "correct" any screenshot-observed cell value.

## Evidence Handling Note

- Original screenshots in `_Inbox\_Visual_Drop\` were **not moved, renamed, or deleted**. All 10 files remain in place.
- No cell value, header, or label was guessed. Where a value could not be read with confidence directly from the pixels, it is marked `unclear` rather than inferred.
- No files were overwritten; this is a newly created file.

## What the Screenshots Show

All 10 screenshots are sequential, overlapping crops of a single scrolling Excel worksheet named **"Смета"** (Russian: "Estimate/Quote"), part of a workbook with three tabs: `Смета`, `Материалы`, `Лист3` (only `Смета` is visible in any screenshot). The sheet is a **renovation labor-cost estimate ("смета на работы")**, organized into numbered stages ("Этап 2" through "Этап 13"; Этап 1 was not captured in any screenshot — coverage begins mid-document at Этап 2).

Columns (header row, row 1):

| Col | Header (Russian) | Meaning |
|---|---|---|
| A | Наименование работ | Work item name |
| B | Единица | Unit of measure (шт = piece, м2 = m², м.п. = linear meter, точка = point/fixture, модуль = module) |
| C | Цена | Unit price. **No currency symbol is printed in any screenshot cell** (screenshot-observed fact, unchanged). The presenter states in the transcript that all `смета` prices are denominated in USD, the Minsk construction market's de facto pricing currency, converted to RUB/BYN only when settling with a specific contractor (transcript-derived context — see "Transcript-Derived Context" below; not something visible in the spreadsheet itself). |
| D | Количество | Quantity |
| E | Итог | Line total (= C × D in every row checked) |
| G | Наименование работ | A second, partial/truncated copy of item names — appears to be an adjacent helper/reference column, not distinct data |

Row-by-row coverage across all 10 screenshots spans **rows 1–183 continuously**, with color-coded row bands per stage (blue/pink/green/purple alternating by Этап). No gaps in row coverage were found once all 10 images were assembled in order.

## Transcript-Derived Context

Everything in this section comes from the video's spoken narration (archived transcript, see Source above), **not** from pixels in any screenshot. It is kept separate from the "Reconstructed Table" section on purpose — nothing here should be read as confirming a specific unclear cell value.

- **What the spreadsheet is:** the presenter (a designer/former all-trades builder in Minsk) built this `смета` from a real, already-completed 44 m² apartment renovation in a new-build ("Новостройка"), reusing the same working (non-visual) design project that specified partitions, electrical, and plumbing layouts for that apartment. The video's purpose is to walk through this real project's costs stage by stage.
- **Currency:** prices are explicitly stated to be in **US dollars** — the presenter says the Belarusian construction market (unlike Russia's ruble-denominated market) prices almost everything in USD, and materials purchases are converted from RUB to USD at the end for consistency. This directly informs (but does not overwrite) the "currency not printed" observation from the screenshots.
- **Pricing basis:** the presenter describes the `Цена` column as **average market rate** — not premium/high-end and not the cheapest available — and warns that lower-priced crews can be half the cost but carry real quality risk; supervision ("прораб") is recommended and priced separately from these line items.
- **Why so many `Количество` values are `0`:** the presenter confirms this `смета` reflects what was *actually needed on this specific 44 m² apartment* (e.g., almost no demolition was required because the apartment was a bare new-build shell), not a generic checklist — a `0` quantity means "priced service, not used on this project," consistent with what "safe assertions" already states below.
- **Этап 1 is apparently not a missing screenshot, but simply not an itemized line-item stage:** the presenter refers to "поиск коммуникаций в полу детектором" (the first priced row, screenshot row 3) as being under the stage "labeled Этап 2" in the workbook, implying the spreadsheet's own numbering starts its priced content at Этап 2, not that a screenshot of Этап 1 is missing. This is spoken context only — it does not visually confirm there is no Этап 1 elsewhere in the workbook, but it does soften the earlier assumption that a screenshot was skipped.
- **Loose stage-subtotal figures mentioned aloud** (ASR-transcribed, treat as approximate/context only, not verified): демонтаж/кладка/штукатурка stage ≈ "$1.74" spoken (likely an ASR-garbled figure, presenter himself says he doesn't fully recall the exact number); ventilation + rough plumbing labor ≈ $1,090; rough electrical labor transcribed as "14 дол" (ASR-truncated, plausibly $1,400-class given the line items, not confirmed); GKL + tile labor transcribed as "12 долларов" (same caveat); rough paint/plaster stage ≈ $1,393–$1,400; finish paint/wallpaper/decorative stage ≈ $950 (presenter notes actual cost was higher because fresco/decorative work was added later and isn't reflected in that figure); finish plumbing + electrical + trim stage ≈ $800. **None of these spoken subtotals were cross-checked against a summed total of the screenshot rows** — they are reported here only as narrative context on the video's own framing, and specifically must not be used to "fill in" or validate any individual row's `Итог` value.
- **Materials are tracked separately from labor**, in a second `Материалы` sheet tab (never visible in any screenshot) and were reportedly priced in RUB during purchase, converted to USD afterward for reporting — reinforcing that the `Смета` tab captured in the screenshots is **labor-only**, matching the screenshot-only conclusion already drawn below.

**Confirms, contradicts, or adds context?** The transcript **adds context** and, on structure, **confirms** the screenshot reconstruction (stage names, the "labor-only, real-project-driven" nature of the sheet, average-market pricing, and the meaning of zero-quantity rows). It does **not contradict** any screenshot-observed value. It does **not** independently confirm any specific `Цена`, `Количество`, or `Итог` digit — the ASR-transcribed spoken subtotals are too imprecise (and in at least two cases visibly truncated by the auto-captioning) to serve as verification for row-level numbers.

## Reconstructed Table (by Stage)

**Value-status legend** (applies to every cell below): unless flagged otherwise inline, every `Price`/`Qty`/`Total` value is **screenshot-observed** — read directly from a screenshot rated `clear` or `partial` in the Screenshot Mapping Table below (rows sourced from a `partial`-rated screenshot are still directly read, just from a lower-contrast or overlap-cropped image; see that table for which screenshot backs which row range). Four exceptions exist and are marked inline where they occur:
- **`unclear`** — the digit(s) could not be read with confidence from the pixels; no value is asserted.
- **`calculated` / "by arithmetic"** — a value implied by `Цена × Количество` but not independently confirmed by direct pixel legibility, used only as a cross-check annotation next to an `unclear` cell, never as a silent substitute for it.
- **`missing`** — no screenshot provides row-level detail for this range at all (currently only rows 64–69, see below).
- **Confidence caveat** — rows 88–95 (Этап 7) are legible but printed on a dark-green highlighted band with lower contrast than unhighlighted rows (flagged separately after that table).

`Итог` consistently equals `Цена × Количество` in every row where all three values are legible; this was used only as a cross-check on the reconstruction, never as a substitute for reading the digits.

### Этап 2. Заехали на объект (rows 3–6)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Поиск коммуникаций в полу детектором | 1шт | 50 | 1 | 50 |
| Заклеивание окон, подоконников | 1 м2 | 1,5 | 16,17 | 24,255 |
| Укрывка пола | 1 м2 | 1 | 0 | 0 |
| Снятие и упаковка радиаторов | 1 шт | 5 | 2 | 10 |

### Этап 3. Демонтаж, кладка стен, штукатурка, стяжка (rows 8–39)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Демонтаж старых труб (точка) | 1шт | 2 | 0 | 0 |
| Демонтаж перегородок пустотелый (гипсокартон) | 1 м2 | 4 | 0 | 0 |
| Демонтаж перегородок полнотелых (газоблок, керамзит) | 1 м2 или м.п. | 6 | 0 | 0 |
| Демонтаж перегородок полнотелых (Кирпич) | 1 м2 или м.п. | 10 | 0 | 0 |
| Демонтаж штукатурки | 1 м2 или м.п. | 2 | 0 | 0 |
| Демонтаж межкомнатных дверей | 1 шт | 10 | 0 | 0 |
| Демонтаж Плитки | 1 м2 | 2 | 0 | 0 |
| Демонтаж стяжки (под перенос радиаторов) | 1 м.п. | 5 | 0 | 0 |
| Демонтаж плинтуса | 1 м.п. | 1 | 0 | 0 |
| Демонтаж обоев | 1 м.п. | 0,5 | 0 | 0 |
| Штроба в стяжке под кладку стен | 1 м.п. | 6 | 8,23 | 49,38 |
| Кладка перегородок из кирпича | 1 м2 | 15 | 0 | 0 |
| Кладка блока керамзитобетон | 1 м2 | 9 | 21,79 | 196,11 |
| Кладка блока керамзитобетон погонный метр | 1 м.п. | 9 | 0 | 0 |
| Армировка примыкания к стенам от застройщика (уголок) | 1 шт | 6 | 4 | 24 |
| Армировка примыканий стеклосеткой | 1 м.п. | 1 | 21,8 | 21,8 |
| Армировка стен арматурой внутри стены | 1 м.п. | 3 | 0 | 0 |
| Перемычка на дверью | 1 шт | 10 | 2 | 20 |
| Формирование проёма | 1 шт | 15 | 2 | 30 |
| Заделка пеной примыкания потолка и стены | 1 м.п. | 1 | 9,5 | 9,5 |
| Грунтовка стен или потолка бетонконтактом или адгезионный клеевой слой | 1 м2 | 0,5 | 28,5 | 14,25 |
| Грунтовка универсальным грунтом | 1 м2 | 0,2 | 120 | 24 |
| Обработка противогрибковой Ceresit | 1 шт | 15 | 0 | 0 |
| Чистка стен от штукатурки и загрязнений или бетона шлифмашиной и грунтовка | 1 м2 | 3 | 0 | 0 |
| Монтаж подоконников | 1 м2 | 10 | 2 | 20 |
| Штукатурка по маякам стен | 1 м2 | 6 | 120 | 720 |
| Штукатурка по маякам потолков | 1 м2 | 10 | 0 | 0 |
| Штукатурка узких участков по маякам (менее 50см) или откосы | 1 м.п. | 6 | 33 | 198 |
| Устройство Примыкание скрытых дверей (сетка,грунтовка,штукатурка либо ГКЛ) | 1 м.п. | 6 | 0 | 0 |
| Монтаж теневого плинтуса (штроба+монтаж плинтуса) | 1 м.п. | 8 | 0 | 0 |
| Стяжка пола (до 6см) | 1 м2 | 7 | 0 | 0 |
| Стяжка пола, узкий участок до 50см (до 6см толщиной) | 1 м.п. | 7 | 9 | 63 |

### Этап 4. Вентиляция и кондиционирование (rows 41–45)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Монтаж короба вентиляции | 1 м.п. | 7 | 6 | 42 |
| Устройство вывода точки вентиляции | 1 шт | 5 | 4 | 20 |
| Отверстия в стенах под инженерные коммуникации | 1 шт | 2 | 4 | 8 |
| Демонтаж шахты под короб вентиляции и заделка | 1 шт | 15 | 2 | 30 |
| Монтаж обратного клапана в вентиляции | 1 шт | 2 | 3 | 6 |

### Этап 5. Черновая сантехника (rows 47–70)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Монтаж нового радиатора | 1 точка | 100 | 1 | 100 |
| Перенос радиатора | 1 точка | 50 | 0 | 0 |
| Перенос Радиатора в одной плоскости | 1 точка | 30 | 0 | 0 |
| Шлифовка и покраска радиаторов | 1 точка | 30 | 0 | 0 |
| Штробы под сантехнику в слабых материалах (не более 50x50мм) | 1 м.п. | 1,6 | 0 | 0 |
| Штробы под сантехнику в бетоне (не более 20x20мм) | 1 м.п. | 2,6 | 0 | 0 |
| Штробы под сантехнику в стяжке (под радиатор) | 1 м.п. | 6 | 1 | 6 |
| Сантех точки (Гор и хол вода) | 1 шт | 35 | 6 | 210 |
| Сантех точки (холодная вода) | 1 шт | 25 | 3 | 75 |
| Сантех точки (канализация) | 1 шт | 20 | 6 | 120 |
| Установка внутренней части встроенного смесителя + гнездо под него | 1 шт | 35 | 2 | 70 |
| Отвод на потребителя (*душ, излив) | 1 шт | 15 | 3 | 45 |
| Сборка и монтаж коллектора (гребёнки) | 1 шт | 30 | 2 | 60 |
| Перенос счётчиков воды на удобное место | 1 шт | 20 | 2 | 40 |
| Установка оборудования после счетчика (редуктор, клапан, фильтр и т.д.) | 1 шт | 8 | 8 | 64 |
| Установка Системы от протечки воды (с подключение базы) | 1 шт | 50 | 0 | 0 |
| Работа по установке датчиков утечки воды | 1 шт | 10 | 0 | 0 |
| *(rows 64–69: status = **missing** — not individually resolved to specific line items from any screenshot; the row range falls in the seam between screenshot 082418.png and 082519.png and was not re-verified at row-level granularity; treat as absent data, not as "all zero" or otherwise inferred — see Open Questions #2)* | | | | |
| Шумоизоляция канализации | 1 шт | 25 | 1 | 25 |

### Этап 6. Черновая электрика (rows 72–86)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Гнездо для подрозетников | 1шт | 1 | 63 | 63 |
| Штробы под электрику в слабых материалах (не более 30x30мм) | 1 м.п. | 1,6 | 52 | 83,2 |
| Штробы под электрику в бетоне (не более 20x20мм) | 1 м.п. | 2,6 | 16 | 41,6 |
| Укладка кабеля без гофр | 1 м.п. | 1 | 600 | 600 |
| Монтаж подрозетников | 1шт | 2 | 63 | 126 |
| Монтаж распаечной коробки электрики | 1шт | 2 | 12 | 24 |
| Монтаж коробки силового щита | 1шт | 30 | 2 | 60 |
| Распайка коробок электрики | 1 шт | 10 | 12 | 120 |
| Установка датчика температуры (штроба, Гофра, заделка) | 1 шт | 15 | 3 | 45 |
| Укладка электро тёплых полов в штробу (без штробы. Только укладка и замазка) | 1 м2 | 10 | 4,7 | 47 |
| штроба в стяжке для электро тёплого пола | 1м.п. | 1,5 | 42,3 | 63,45 |
| Заделка штроб | 1м.п. | 0,5 | 68 | 34 |
| Короб под провода ТВ | 1 шт | 15 | 0 | 0 |
| Вводной кабель | 1 шт | 50 | 0 | 0 |
| Сборка силового щита | 1 модуль | 4 | 24 | 96 |

### Этап 7. Монтаж ГКЛ (rows 88–95)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Монтаж гипсокартона (1слой) (Опуск, карниз, второй уровень, полка и т.д.) | 1 м.п. | 10 | 6,4 | 64 |
| Монтаж гипсокартона (1слой) (Ровный потолок,стена) | 1 м2 | 10 | 0,5 | 5 |
| Монтаж гипсокартона (2слоя) (Опуск, карниз, второй уровень и т.д.) | 1 м.п. | 12 | 0 | 0 |
| Монтаж гипсокартона (2слоя) (Ровный потолок,стена) | 1 м2 | 12 | 0 | 0 |
| Монтаж скрытого люка | 1 шт | 30 | 0 | 0 |
| Монтаж в ГКЛ и устройство трекового светильника | 1 м.п. | 12 | 0 | 0 |
| Зашивка инсталяции ГКЛ | 1 шт | 30 | 1 | 30 |
| Шумоизоляция Стен (потолок коэффициент 1.2) | 1 м2 | 14 | 0 | 0 |

*Confidence note: rows 88–95 are printed on a dark-green highlighted band; text/digits are legible but lower-contrast than unhighlighted rows.*

### Этап 8. Гидроизоляция (rows 97–98)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Гидроизоляция мастикой ceresit | 1 м2 | 3 | 14 | 42 |
| Гидроизоляция примыканий лентой ceresit | 1 м.п. | 2 | 14 | 28 |

### Этап 9. Укладка плитки (rows 100–127)
| Item                                                               | Unit   | Price | Qty   | Total  |
| ------------------------------------------------------------------ | ------ | ----- | ----- | ------ |
| Потдон для душа из бетона                                          | 1 шт   | 50    | 0     | 0      |
| Усиление углов плитки для монтажа стекла душевой                   | 1 шт.  | 15    | 0     | 0      |
| Укрепление стяжки под плитку (ремонт трещин)                       | 1 м.п. | 5     | 3     | 15     |
| Укладка мозайки плюс подготовка                                    | 1 м2   | 19    | 0     | 0      |
| Укладка мелкоформатной плитки (кабанчик и т.п.)                    | 1 м2   | 17    | 0     | 0      |
| Укладка керамогранита погонный метр (меньше 30см)                  | 1 м.п. | 15    | 0     | 0      |
| Укладка керамики погонный метр (меньше 30см)                       | 1 м.п. | 13    | 7,5   | 97,5   |
| Укладка керамогранита                                              | 1м2    | 15    | 9,95  | 149,25 |
| Укладка керамики                                                   | 1м2    | 13    | 19,91 | 258,83 |
| Укладка керамогранита широкоформат (до 1500мм)                     | 1м2    | 17    | 0     | 0      |
| Укладка керамогранита широкоформат (свыше 1500мм, цена договорная) | 1м2    | 0     | 0     | 0      |
| Большая раковина со столешницей из плитки                          | 1 шт.  | 400   | 0     | 0      |
| Маленькая раковина из плитки                                       | 1 шт.  | 250   | 0     | 0      |
| Чистовой рез плитки                                                | 1 м.п. | 6     | 26    | 156    |
| Гипсовый кирпич под окраску                                        | 1 м2   | 20    | 0     | 0      |
| Уголок алюминиевый на плитку                                       | 1 м.п. | 5     | 0     | 0      |
| Грунтовка универсальным грунтом                                    | 1 м2   | 0,2   | 0     | 0      |
| Запил плитки под 45                                                | 1 м.п. | 10    | 8,8   | 88     |
| Выложить душевой поддон плиткой с уклоном под трап                 | 1 шт   | 50    | 0     | 0      |
| Затирка плитки цементной фугой                                     | 1 м2   | 2     | 29,6  | 59,2   |
| Затирка плитки эпоксидной фугой                                    | 1 м2   | 5     | 0     | 0      |
| Формирование наружных углов из эпоксидной фуги                     | 1 м.п. | 5     | 0     | 0      |
| Плинтус из плитки на лоджии                                        | 1 м.п. | 10    | 2     | 20     |
| Силикон внутренних углов                                           | 1 м.п. | 2     | 16    | 32     |
| Отверстия в плитке (керамогранит)                                  | 1 шт   | 5     | 0     | 0      |
| Отверстия в плитке (керамика)                                      | 1 шт   | 3     | 23    | 69     |
| Герметизация скрытого люка                                         | 1 шт   | 10    | 0     | 0      |
| Экран из плитки под ванной, ГКЛ с люком на магнитах                | 1 шт   | 70    | 1     | 70     |

### Этап 10. Малярные работы (rows 129–145)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Перетягивание сеткой потолка и стены | 1 м2 | 4 | 15 | 60 |
| Монтаж малярного уголка либо малярной ленты на/в углы | 1 м.п. | 2 | 64 | unclear (screenshot digit partially obscured; 2×64 = 128 by arithmetic, not independently confirmed) |
| Самонивелир смесь на пол | 1 м2 | 6 | 30 | 180 |
| Заделка стыков ГКЛ серпянкой и смесью унифлот | 1 м2 | 0,9 | 0 | 0 |
| Грунтовка ниверсальным грунтом | 1 м2 | 0,2 | 99 | 19,8 |
| Шлифовка оштукатуренной поверхности перед шпаклёвкой | 1 м2 | 0,5 | 99 | 49,5 |
| Шпаклёвка под покраску | 1 м2 | 10 | 28,65 | 286,5 |
| Шпаклёвка Опусков, откосов и коробов под окраску | 1 м.п. | 8 | 28 | 224 |
| Шпаклевка под обои | 1 м2 | 4 | 70,52 | 282,08 |
| Шпаклёвка Опусков и коробов под обои | 1 м.п. | 9,5 | 4 | 38 |
| Плинтус (багет) потолочный (+покраска и заделка стыков) | 1 м.п. | 6 | 0 | 0 |
| Акрил внутренних углов | 1 м.п. | 0,2 | 30 | 6 |
| Перетягивание фасадной сеткой | 1 м2 | 4 | 18,13 | 72,52 |
| Перетягивание фасадной сеткой (до 30см) | 1 м.п. | 4 | 11,7 | 46,8 |
| Монтаж 3D панелей | 1 м2 | 17 | 0 | 0 |
| Монтаж молдига под покраску | 1 м.п. | 0 (unclear — appears blank/0, low contrast) | 0 | 0 |
| Утепление потолка и стен пенопластом | 1 м2 | 6 | 0 | 0 |

### Этап 11. Укладка напольного покрытия (rows 147–154)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Шлифовка паркета | 1 м2 | 6 | 0 | 0 |
| Ламинат | 1 м2 | 5 | 28,99 | 144,95 |
| Ламинат чистовой рез, погонный метр | 1 м.п. | 5 | 1,4 | 7 |
| Кварцвинил | 1 м2 | 5 | 4,9 | 24,5 |
| Кварцвинил чистовой рез, погонный метр | 1 м.п. | 5 | 2,8 | 14 |
| Паркетная доска (цена зависит от материала, может корректироваться) | 1 м2 | 9 | 0 | 0 |
| Ступень под лоджией, приклеевание ламината, паркета или плитки | 1 шт | 15 | 0 | 0 |
| Порожки межкомнатные либо стык без порожка (метр погонный либо штука) | 1 шт, 1 м.п. | 9 | 0 | 0 |

### Этап 12. Чистовая малярка (rows 156–162)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Откосы, опуски, коробы и т.д. покраска 2 слоя | 1 м.п. | 4 | 28 | unclear (cursor icon obscures the total digit in screenshot 082834.png; 4×28 = 112 by arithmetic, not independently confirmed) |
| Грунтовка стен и пола универсальным грунтом | 1 м2 | 0,2 | 99,17 | 19,834 |
| Нанесение декоративной штукатурки | 1 м2 | 12 | 18,13 | 217,56 |
| Нанесение декоративной штукатурки, погонный метр | 1 м.п. | 12 | 11,7 | 140,4 |
| Поклейка обоев (если обои тонкие и деликатные, цена будет выше) | 1 м2 | 4 | 70,52 | 282,08 |
| Поклейка обоев погонный метр | 1 м.п. | 4 | 9,5 | 38 |
| Покраска стен и потолка | 1 м2 | 4 | 28,65 | 114,6 |

### Этап 13. Чистовая сантехника, электрика, плинтус (rows 164–183)
| Item | Unit | Price | Qty | Total |
|---|---|---|---|---|
| Светодиодный профиль, монтаж | 1 м.п. | 5 | 0 | 0 |
| Установка, подключение блока светодиодной подсветки | 1 шт | 10 | 4 | 40 |
| Подключение светодиодной ленты (пайка) | 1 шт | 5 | 6 | 30 |
| Установка унитаза (навесного) | 1 шт | 15 | 1 | 15 |
| Монтаж полотенцесушителя | 1 шт | 30 | 1 | 30 |
| Навеска чистовых компонентов сантехники (изливы, краны, души и т.д.) | 1 шт | 10 | 9 | 90 |
| Установка смесителей (внутреннего и наружного монтажа) | 1 шт | 10 | 2 | 20 |
| Установка смесителей на раковину | 1 шт | 10 | 2 | 20 |
| Монтаж и подключение раковины | 1 шт | 15 | 1 | 15 |
| Монтаж зеркала с подсветкой | 1 шт | 15 | 1 | 15 |
| Монтаж Аксессуаров на плитку (вешалки, держатели и т.д) | 1 шт | 5 | 0 | 0 |
| Установка чистовых розеток и выключателей | 1 шт | 3 | 63 | 189 |
| Монтаж терморегулятора теплого пола | 1 шт | 10 | 3 | 30 |
| Установка точечных светильников и навеска бра | 1 шт | 8 | 6 | 48 |
| Подключение домофона | 1 шт | 15 | 1 | 15 |
| Установка Люстр (если конструкция сложная, оговаривается отдельно) | 1 шт | 20 | 1 | 20 |
| Плинтус полиуретан + покраска | 1 м.п. | 8 | 0 | 0 |
| Плинтус МДФ | 1 м.п. | 5 | 25,7 | 128,5 |
| Плинтус ПВХ | 1 м.п. | 2 | 6,5 | 13 |
| установка батарей | 1 шт | 10 | 0 | 0 |

**Footer note (below row 183, partially cut off at the bottom edge of screenshot 082915.png):**
> "Работы, которые выполняют смежные бригады, тут не учитываются. Такие как: Монтаж окон и дверей, Вывоз мусора, монтаж новых радиаторов, Натяжные потолки, Работы в сфере ЖКХ, Установка кондиционеров, Сборка мебели. Но на вс[а...]" *(text is cut off by the screenshot's lower edge — remainder unclear)*

## Test Case Interpretation

**What pricing scenario this represents:** A **labor-only renovation cost estimate ("смета")** for a full apartment renovation in a new-build ("Новостройка"), broken into 13 sequential construction stages (demolition, wall-building, MEP rough-in, drywall, waterproofing, tiling, painting, flooring, finish plumbing/electrical/trim). Each line item has a unit price and a quantity, and the `Итог` (total) column is a pure arithmetic product of the two (`Итог = Цена × Количество`), confirmed consistently across every row where all three values were legible.

**What data can be used as expected test data:** The `Цена × Количество = Итог` relationship is the one safely verifiable, deterministic rule in this dataset — it held in every row checked, including decimal quantities (e.g. `1,5 × 16,17 = 24,255`; `6 × 21,79 = 130,74`... note: this specific row shows `196,11`, i.e. price×qty = `9 × 21,79 = 196,11` ✓). Rows with quantity `0` reliably total `0`. This arithmetic invariant is a reasonable target for a unit test on a table-parsing/estimate-calculation function (e.g., "given price and quantity, total = price × quantity, rounded/displayed to 2 decimals").

**What assertions are safe to make:**
- Total = Price × Quantity for every row where all three fields are legible (verified spot-checks above hold).
- The sheet has a strict tabular structure: `Наименование работ | Единица | Цена | Количество | Итог`, with stage-header rows (`Этап N. <name>`) that have no numeric data of their own and act as section breaks.
- Row order and stage numbering (Этап 2 → Этап 13) is sequential in the source document as captured.
- Zero-quantity rows are valid "priced but not used" line items, not missing data.

**What assertions are unsafe (evidence incomplete):**
- **Do not treat the 183 captured rows as the complete смета.** Этап 1 was never captured by any screenshot (see Open Questions #1); the transcript offers a weak, unconfirmed hint that priced content may simply start at Этап 2, but that is not proof there is no Этап 1 content elsewhere in the workbook. No test or downstream consumer should assert "this is the full estimate" or rely on item-count totals (e.g., "there are exactly N priced line items") from this document.
- **Do not run strict/exact-match automated checks against any cell flagged `unclear` in this document** (see the legend at the top of "Reconstructed Table") — there are 3 such cells (two `Итог` values obscured by a cursor icon, one `Цена` value on a low-contrast band) plus the fully `missing` rows 64–69. Tests should skip these cells/rows or assert only "value is unknown," never a specific expected number.
- **No screenshot shows a currency symbol printed in the `Цена`/`Итог` cells.** The transcript (see "Transcript-Derived Context") has the presenter stating the smeta is priced in USD — this is now a reasonably-grounded piece of context, but it is *spoken*, not *visible in the spreadsheet*, so it should be cited as "presenter states USD," not asserted as a printed/verified fact of the document itself.
- **Rows 64–69** (within Этап 5) were not individually transcribed with confidence — they fall in an area of overlap between two screenshots where exact line items were not independently re-verified; do not assume this range is empty or use it as complete data. The transcript does not resolve this at row-level granularity either.
- **No grand total / sheet-level sum was ever visible** in any screenshot, and the transcript's spoken stage subtotals are ASR-transcribed, imprecise, and in places apparently truncated — they must not be summed or treated as a substitute for an observed grand total.
- **The `Материалы` (Materials) tab was never visible** in any screenshot — this table covers labor pricing only. The transcript confirms materials were tracked and priced separately (in RUB, converted afterward), but no material cost figures from the transcript should be merged into this labor-only table.
- Two total values (`Монтаж малярного уголка...` row and `Откосы, опуски, коробы... покраска 2 слоя` row) have digits obscured by a cursor/UI icon in the source screenshot; the arithmetic-implied values are noted but are not independently confirmed by direct pixel legibility, and the transcript does not mention these specific rows.
- **Spoken stage-subtotal figures from the transcript are auto-caption (ASR) output** and must not be used as verified numeric data — treat them strictly as narrative framing, per the caveat in the Source section.

## Recommended Automated Test Usage

**Safe — parser/OCR fixture checks:**
- Use the row data in "Reconstructed Table (by Stage)" as a golden fixture for a table-parsing function (Excel-export, screenshot-OCR, or CSV-import parser): given the item name, unit, price, and quantity strings shown, the parser should extract those exact fields for every row **not** flagged `unclear`/`missing`.
- Column-header parsing: `Наименование работ | Единица | Цена | Количество | Итог` is a safe fixed fixture for a header-detection test.
- Stage-header detection: rows containing only an `Этап N. <name>` string with no numeric data are a safe fixture for "section break, not a data row" classification logic.
- Unit-of-measure vocabulary (`шт`, `м2`, `м.п.`, `точка`, `модуль`) is a safe fixture for a unit-normalization function.

**Safe — arithmetic consistency checks:**
- `Итог == round(Цена × Количество, 2)` (allowing for locale decimal-comma formatting) holds for every legible row in this document and is a safe invariant to assert in a calculator/estimator unit test.
- `Количество == 0 ⟹ Итог == 0` is a safe invariant, confirmed across dozens of rows.
- These checks should explicitly **skip** the rows flagged `unclear`/`missing` (see legend) rather than asserting a specific expected value for them.

**Skip until the original Excel/source data is available (do not build tests against this document for these):**
- Any check involving the currency unit (e.g., formatting `$` or `BYN` on output) — this document only has spoken (transcript) evidence for USD, not a printed/verified cell value.
- Any check involving a grand total, stage subtotal, or sum-of-all-rows figure — no grand total was ever visible in any screenshot, and the transcript's spoken subtotals are ASR-imprecise; do not derive an expected total from this document.
- Any check asserting the estimate is "complete" (fixed item count, no missing stages) — Этап 1 and rows 64–69 are gaps in this evidence, not confirmed-absent data.
- Any check involving the `Материалы` (materials/cost-of-goods) tab — it was never visible in any screenshot; nothing here should feed a materials-pricing test.
- The 3 `unclear`-flagged cells and the `missing` row range (64–69) — do not hardcode an expected value for these until the source workbook itself is available.

## Screenshot Mapping Table

| Filename | Role in Reconstruction | Visible Fragment / Table Area | Confidence |
|---|---|---|---|
| Screenshot 2026-07-28 081607.png | Primary source | Rows 1–26 (header, Этап 2, start of Этап 3) | clear |
| Screenshot 2026-07-28 081634.png | Overlap/cross-check | Rows 1, 7–31 (Этап 3, scrolled) | clear |
| Screenshot 2026-07-28 082349.png | Overlap/cross-check | Rows 17–41 (end of Этап 3, start of Этап 4) | clear |
| Screenshot 2026-07-28 082418.png | Primary source | Rows 39–70 (Этап 4, Этап 5) | clear |
| Screenshot 2026-07-28 082519.png | Primary source | Rows 70–98 (Этап 6, Этап 7, start of Этап 8) | partial (rows 88–95 on dark-green highlight, lower contrast) |
| Screenshot 2026-07-28 082624.png | Primary source | Rows 105–129 (Этап 9 continued, start of Этап 10) | clear |
| Screenshot 2026-07-28 082721.png | Overlap/cross-check | Rows ~80–104 (Этап 6 tail, Этап 7, Этап 8, start of Этап 9) | partial (rows 88–95 on dark-green highlight) |
| Screenshot 2026-07-28 082746.png | Primary source | Rows 127–151 (end Этап 9, Этап 10, start Этап 11) | partial (one total digit obscured by cursor icon, row ~130) |
| Screenshot 2026-07-28 082834.png | Primary source | Rows 148–172 (end Этап 11, Этап 12, start Этап 13) | partial (one total digit obscured by cursor icon, row ~156) |
| Screenshot 2026-07-28 082915.png | Primary source | Rows 161–183 + footer note (Этап 13 continued, closing note) | partial (footer note text cut off at image edge) |

**Processed: 10 / 10. Skipped: 0. Cells flagged `unclear`: 3** (one `Итог` in Этап 10, one `Итог` in Этап 12, one `Цена` in Этап 10's "Монтаж молдига под покраску" row). **Rows flagged `missing`: 6** (rows 64–69, Этап 5). **Other partial evidence: 1** footer note truncated at the image edge (Этап 13 exclusion list, tail unreadable).

## Open Questions / Gaps

1. **Этап 1** is not represented in any screenshot. The transcript suggests (but does not prove) that the workbook's priced content may simply start at Этап 2 rather than a screenshot being missing — this is not confirmed either way, since the presenter never explicitly describes an Этап 1.
2. **Rows 64–69** (Этап 5) were not confidently isolated as distinct line items from the two overlapping screenshots covering that range; the transcript does not provide row-level detail for this range either. Revisit with a screenshot centered on that exact range if precise line items are needed.
3. **Currency unit** is not printed anywhere visible in the spreadsheet cells themselves. The transcript now provides spoken context (presenter states USD), but a printed/visual confirmation from the workbook (e.g., a currency-formatted cell, a header note) is still absent.
4. **No grand total row** was captured — unknown whether one exists further down the sheet (row 183 already includes an unmoved-work exclusion note, suggesting the itemized list may end there, but this is not certain from the screenshots alone). The transcript's spoken stage subtotals are too imprecise/ASR-garbled to substitute for this.
5. ~~Transcript unavailable~~ — **corrected**: the transcript was available all along in this repo's archive (`_Archive\processed_sources\20260727_renovation_guide_mistakes_7_b385361e.txt`) and has now been read and cited above under "Transcript-Derived Context." Remaining gap: the transcript's spoken numeric figures are ASR-transcribed and imprecise, so several stage-level dollar amounts mentioned in the video remain only loosely readable, not exact.
6. Two specific total-column digits (Этап 10 "Монтаж малярного уголка..." row, Этап 12 "Откосы, опуски, коробы..." row) are obscured by an on-screen cursor icon in the source screenshots; the values shown in this document for those cells are arithmetic inferences (Цена × Количество), not directly read digits, and are flagged as such in the tables above. The transcript does not mention these specific rows.
7. **New:** exact spoken stage-subtotal figures (Этап 6 electrical "$14??", Этап 7+9 combined "$12??") are ASR-truncated in the archived transcript and could not be confidently reconstructed even from the transcript text itself — if precise figures are needed, they would require re-watching the relevant timestamp with sound, not just the caption track.

---

## Companion Benchmark: Minsk / Belarus 2025 Turnkey Labor & Material Rates

> [!NOTE]
> Appended from the former `11_Budget_and_Planning/analysis/Master_Budgeting_Guide.md` §4 during the 2026-07-30 wiki/case-study reorganization (that file is now archived at `11_Budget_and_Planning/_supporting/legacy/Master_Budgeting_Guide_legacy_pre_reorg.md`). This is a top-level rate-card summary of the **same underlying source** (`b385361e`, the 44 m² Minsk apartment смета) as the row-level reconstruction above — a rollup view rather than the full row-by-row table. Content is unchanged from the original document.

> [!NOTE]
> **Metadata**:
> - **Source class**: Primary local benchmark
> - **Region**: Minsk, Belarus
> - **Source year**: 2025
> - **Currency in source**: USD (labor/design) & BYN (rough materials)
> - **Conversion basis**: Direct local USD / BYN estimates
> - **Comparability**: Direct primary benchmark for Minsk comfort-class renovation projects

| Labor & Service Item | Stated Rate / Cost | Scope / Unit | Notes & Technical Details | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Floor Pipe Detector Scanning** | $50 USD | Flat fee per job | Ultrasonic/magnetic scanning of PEX radiator pipes in raw screed before chasing | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Keramzit-Concrete Block Masonry** | $9 USD / m² | Wall area | Partition wall construction with perimeter expansion joints & bed joints | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Wall Plastering by Guides** | $6 USD / m² | Wall area | Plastering with 90° geometry for kitchen/bathroom walls (market avg $5 USD/m²) | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Ceiling Plastering by Guides** | $10 USD / m² | Ceiling area | Heavy plaster leveling for raw concrete ceilings | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **AC Split-System Installation** | $350 USD | Job total | Labor & line routing by HVAC specialists | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Rough Plumbing & Ventilation Labor** | $1,090 USD | Job total | Riser manifold, counter relocation, leak servo-drives, multizone ventilation | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Rough Electrical Installation Labor** | $1,400 USD | Job total | Cable chasing, panel assembly, temporary switches/sockets | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Ceramic Tile Installation** | $13 USD / m² | Tile area | Wall/floor ceramic tile labor | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Standard Porcelain Tile Installation** | $15 USD / m² | Tile area | Standard porcelain stoneware labor | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Large-Format Porcelain Tile (<1.5m²)** | $17 USD / m² | Tile area | Large-format porcelain stoneware labor | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Rough Surface Prep & Plastering Labor** | $1,400 USD | Job total | Wall putty prep under wallpaper & paint, floor screed grinding | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Final Trim Installation Labor** | $800 USD | Job total | Plumbing fixtures, lighting trim, MDF baseboard installation | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
| **Rough Building Materials (Stage 1)** | 2,000 BYN | Material purchase | Keramzit blocks, Rotband plaster, SM11 tile glue, primers, fasteners | [[_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e\|b385361e]] |
