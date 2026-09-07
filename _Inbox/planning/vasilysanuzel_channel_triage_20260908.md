# Vasily_Sanuzel «Ремонт Санузлов» (@VasilySanuzel) — channel triage

**Created 2026-09-08.** Requested directly by the user ("triage videos of this youtube channel"). Triage only — **nothing fetched, nothing processed.**

- Channel: https://www.youtube.com/@VasilySanuzel/videos
- Preflight manifest: `_Inbox/planning/preflight_20260907T220550Z.json` (light mode, UTC stamp) — **46 videos, 46 fresh, 0 duplicates.** Nothing from this channel has ever been touched.
- Title dump (Russian, `lang=ru` forced): `_Inbox/planning/vasilysanuzel_titles_dump.txt`; raw metadata `vasilysanuzel_titles_meta.json`
- Identity: **a one-man plumbing/bathroom renovation contractor** — channel name «Vasily_Sanuzel Ремонт Санузлов». He does the work himself on camera («Сделал все сам», «Как это делаю я»), and the whole catalogue is **one trade in one room type**: санузлы and nothing else.
- Geography: **Moscow and Moscow oblast** — ЖК Дивное, ЖК Лыткарино Хит, ЖК Бунинские луга, ЖК Ясеневая, plus ПИК new builds. Housing stock: **П-44, П-44Т, П-3 panel series** and ПИК new builds.
- Jurisdiction: **Russia.** Standing rule 4 applies — nothing from this channel goes to `16_Legal_and_Regulations/` (Belarus-only). Route regulatory-sounding claims to the technical page with the jurisdiction flagged.

## ⚠️ Two channel-specific traps, recorded before any fetch

1. **The channel serves auto-translated English metadata by default.** The preflight manifest came back with titles like *"I Took the Bathroom Apart and Saw What's Hiding Inside"* — the same trap as `@YourInteriorDes` (see `yourinteriordes_channel_triage_20260903.md`). The Russian titles in the dump above were obtained only by forcing yt-dlp's `extractor_args` youtube `lang=ru`. **Standing rule 1: force `--languages ru` on every transcript fetch and spot-check each transcript for translated text.**
2. **No upload dates are available yet.** Flat playlist extraction returns `timestamp: None` for every entry, and per-video probing was deliberately not run (rate-limit protocol, standing rule 7). The list order is reverse-chronological and `WsoF9sW1S4Q` self-dates to 2021, so the tail of the table is roughly 2021 and the head is recent — **but that is inference, not metadata. Confirm each date from `yt-dlp` at fetch time**, and in particular before touching the one price-bearing title (`ahHspdChZZc`, «Ремонт однокомнатной квартиры за 250 тысяч»), where standing rule 2 applies: a figure is meaningless without city and year, and RUB 250k in 2021 Moscow is a different claim from RUB 250k today.

**View counts are noise here and must not be used to rank.** The whole channel runs 3–299 views. That cuts both ways: there is no audience to perform for, so the promotional risk is close to zero and the "here is what it actually cost me" honesty is likely high — but there is also no production discipline forcing structure, so thinness risk sits in the short обзор format rather than in the channel as a whole.

## Why this channel is worth a trial even though the bathroom is the vault's most-covered room

`07_Bathroom/` is 23 pages / ~3,400 lines and `08_WC/` exists; a naive read says the subject is saturated. **Round 4 of `@YourInteriorDes` established the counter-rule that applies exactly here: saturation by file count is not saturation by content — ask what adjacent trade could defeat the existing pages, because vault pages are organised by trade and failures are not.**

This channel is that adjacent trade. Everything the vault holds on bathrooms comes from **designers and general contractors making decisions**; this is a **sanitary specialist executing them**, and the gap check bears it out:

| Subject | `_Sources/` files | Wiki files | Verdict |
| :--- | :--- | :--- | :--- |
| «узел ввода» / apartment water inlet unit, shut-offs, filters | **0** | **1** (English, incidental) | **A real hole.** One whole episode is the assembly of it |
| гидроизоляция as a *rationale* («зачем нужна») | 3 (RU term) | 65 (EN term) | Covered as a rule, thin as a *why*; a specialist's failure reasoning is new |
| трап / linear drain, поддон «за 3 дня» | 5 | 3 | Thin, and this is a whole episode |
| Quantity take-off for a bathroom («как посчитать материал и не ошибиться») | — | — | **Nothing in the vault does this at the material-list level** |
| Post-occupancy outcome («санузел год спустя») | rare | rare | Scarcest content type in the vault |

**And the geometry match is unusually close.** This project's ванная is **3.09 m²** and the туалет **1.24 m²** (`data/canonical/room_schedules.json`). This channel's staples are a 150×200 cm bathroom (**3.0 m²**, `V0T8stClpDE`), «маленькая ванная» detailed projects, and **separate** санузлы in П-44Т — i.e. the same problem class, not a generic one. `00_Master/project_decisions.md` also keeps the single-bathroom-plus-separate-туалет layout as a deliberate decision, so small-wet-room execution is load-bearing for this project, not incidental.

**The honest counter-argument, for the user's decision:** 46 videos of one trade in one room is a narrow channel, ~28 of them are short after-the-fact обзоры that will likely be thin, and the bathroom pages are already the densest in the vault. The upside is concentrated in maybe 12–18 long-form items. This is a **budget question**, and the trial below is scoped to answer it cheaply.

## Title-skim triage

### Tier 1a — the П-44 six-part serialized build (2h 50m total, one bathroom start to finish)

The single strongest asset on the channel: a complete sequenced build by one specialist, in a panel flat, with the numbers stated as he hits them. Process **in series order** if it clears the trial — the sequencing is the content.

| # | ID | Min | Title | Likely destination |
| :-- | :--- | :-- | :--- | :--- |
| 22 | `6x_rmCEyxTE` | 22:55 | Серия 1. Подготовка объекта. Замена труб. Возведение стен | `07_Bathroom/analysis/Structure_and_Framing.md`, `12_Engineering_and_Systems` |
| 21 | `4SZG3yJqtQk` | 23:54 | Серия 2. Выравнивание стен и пола. Штукатурка. Стяжка | `13_Surfaces_and_Finishes`, `07_Bathroom/analysis/Planning_and_Layout.md` |
| 20 | `M8EyOCrm0tw` | 29:20 | Серия 3. Сантехнические работы. **Сборка узла ввода водоснабжения** | `12_Engineering_and_Systems` — **the 0-coverage subject** |
| 19 | `0nJt_VkOxDo` | 25:26 | Серия 4. Монтаж трубопровода. Встроенные смесители. Каркас. Инсталляция | `07_Bathroom/analysis/Fixtures_Mixers_and_Sinks.md`, `Structure_and_Framing.md` |
| 18 | `slpRtjzBN4c` | 21:45 | Серия 5. Монтаж трапа. Душевой поддон за 3 дня. **Зачем нужна гидроизоляция** | `07_Bathroom/analysis/Shower_Enclosures_and_Drainage.md` |
| 17 | `d9MQq-SgH1U` | 34:05 | Серия 6. Укладываю керамогранит. Эпоксидная затирка. **«Попал на деньги»** | `07_Bathroom/analysis/Tile_*`, `Tile_Grout_Selection_and_Protection.md` |
| 26 | `YxNlSJBoaiY` | 9:59 | Обзор после завершения (the series' own closing review) | corroboration only; low priority |

### Tier 1b — the П-3 project set (planning-and-engineering side of the same work)

| # | ID | Min | Title | Note |
| :-- | :--- | :-- | :--- | :--- |
| 14 | `2wxwztd6IGU` | 45:04 | Из мечты в реальность. Ванная в панельном доме П-3 | longest of the set |
| 9 | `UkQpm1LLqxQ` | 27:09 | От идеи до воплощения. Подготовка, стены, **геометрия** | geometry of a small wet room |
| 8 | `eeJFwyXpvDw` | 23:37 | «НИКТО не обращает на это внимания». Водопровод, канализация, электрика, инсталляции | the four services in one pass |
| 15 | `lzExBhaA0xk` | 22:21 | «Это происходит в каждой ванной, во время ремонта». Базовые работы | failure-mode framing |
| 7 | `utSHZcKnq3I` | 20:37 | Была идея сделать ванную и тут понеслось… | scope-creep case, unverified |

### Tier 1c — highest-value standalones

| # | ID | Min | Title | Why it ranks here |
| :-- | :--- | :-- | :--- | :--- |
| 10 | `LDeNqQL7TLQ` | 43:38 | **Производитель ответит! IV Слёт сантехников** | **Expert/guest format — the highest-yield format in every channel this vault has processed**, and the longest video here |
| 12 | `z0hcMY5PYoc` | 30:30 | Попал в новостройку от ПИК. **Ломать санузел?** | The decision format, and the closest analogue to this project's own «под чистовую» handover with the WC pan already fitted |
| 13 | `VaWyCaaFXqk` | 15:39 | **Технический проект санузла. Как посчитать материал и не ошибиться** | Material take-off — nothing in the vault does this |
| 46 | `UJn-cA7ZmRU` | 20:07 | Унитаз: замена, сборка, установка, своими руками | The developer's WC pan is already installed and is a likely replacement — directly actionable |
| 6 | `9aKNikb29FI` | 22:04 | **Маленькая ванная — не повод для расстройств.** Детальный проект в SketchUp | Small-wet-room design at this project's own scale |
| 37 | `h7JYk20m9mQ` | 9:02 | **Санузел год спустя. Что произошло с ремонтом?** | **Post-occupancy outcome** — the vault's scarcest type; cheap at 9 min |
| 25 | `jWgyphJut9o` | 7:43 | ПИК. Ремонт **без сноса кабины**. Что получилось? | The other half of the demolish-or-keep decision |
| 4 | `_qK9TwqwoZ4` | 23:16 | Зашел в БЕТОН, но вышел из ВАННОЙ. Сделал все сам | Full cycle, single operator |
| 5 | `dJB-JUhsBkg` | 24:18 | Была ванная от застройщика, стала от мастера | Developer finish → proper finish, this project's exact starting condition |
| 3 | `PqvvsL625rc` | 18:01 | Большой проект для реализации в SketchUp | Modelling/geometry; cross-check against `apartment-layout-modelling` conventions |
| 28 | `S1WZ8wjorZg` | 9:16 | Водоснабжение в квартире. Что нужно знать | Feeds the узел-ввода gap |
| 31 | `iGbAt9nKWXc` | 8:56 | П-44: как можно выполнить разводку труб | Pipe-routing options — "N ways to X" shape |
| 29 | `PIC8bie1b2Q` | 8:39 | Ванная с душевой **без порога** | Threshold-free shower; vault has this thinly |
| 27 | `V0T8stClpDE` | 10:11 | Как в маленькой ванной сделать ремонт? **Ванная 150×200 см** | 3.0 m² — dimensional twin of this project's 3.09 m² ванная |
| 34 | `naFNNSZaaE8` | 11:14 | Обзор **раздельного** санузла в доме П-44Т | This project keeps a separate туалет (1.24 m²) |
| 44 | `ahHspdChZZc` | 12:29 | Ремонт однокомнатной квартиры за **250 тысяч** | ⚠️ Price-bearing — **resolve city + year first** (rule 2); likely ~2021 Moscow |
| 11 | `qIXG_OC7Y4I` | 17:55 | Попробовал уложить **кварцвинил Ёлочкой**. Это сложно? | Off-topic for санузел but only 2 vault sources on кварцвинил; a fitter's difficulty verdict |
| 1 | `mzqcMe5MQNs` | 5:04 | Разобрал ванную по кусочкам и увидел, что скрывается внутри | Demolition-reveal — what is actually behind a finished wet wall |

### Tier 3 — short after-the-fact обзоры, tool clips and vertical/shorts: expect thin, do not process by default

`3vX37tX87jI` (9:47), `Swxcr10YSfc` (5:47), `3P8Zz0Irzh4` (21:54, **vertical video** — titled «ТЫ НЕ ДОСМОТРИШЬ», self-described unwatchable), `iItCUmIaHwA` (11:04), `1j9aJEXBJpQ` (1:01), `ifJkoRJYpCw` (8:53), `3Xj62Qrtmp4` (6:08), `cG0asKwmHg8` (3:22), `3XujFaZ5FOQ` (6:21), `4-LT2DOCEBQ` (5:33), `dw5KQaYR3Sw` (9:44), `7mvt950qWD8` (5:05), `2gZsD26wyjI` (7:43), `WsoF9sW1S4Q` (4:57, self-dates 2021), `H2ltWLZ1Sbw` (12:26), `qBLoAfx_MtE` (5:10, tool curiosities).

Per the existing filter: **a single showcased result is not a technique.** These are narrated walk-throughs of one finished room with no alternative comparison. `naFNNSZaaE8` and `V0T8stClpDE` were promoted out of this tier **on dimensional relevance to this specific flat, not on format.**

## Proposed Round 1 trial — 4 videos, scoped by FORMAT, not by title count

Per the corrected yield model confirmed at `@YourInteriorDes` Round 4: **scope a round from which formats are left, not how many titles are left.** Each pick below tests a different format, so the round returns a selection rule and not just facts.

| Pick | ID | Min | Format being tested |
| :-- | :--- | :-- | :--- |
| 1 | `M8EyOCrm0tw` | 29:20 | **Serialized execution episode** — and it lands on the 0-coverage узел ввода |
| 2 | `z0hcMY5PYoc` | 30:30 | **On-site decision** (demolish the developer's cabin or not) — this project's own question |
| 3 | `LDeNqQL7TLQ` | 43:38 | **Expert/guest Q&A with manufacturers** — historically the best format in this vault |
| 4 | `h7JYk20m9mQ` | 9:02 | **Post-occupancy outcome** — scarcest type, cheapest pick on the list |

**Fetch serialized, one at a time with spacing, `--languages ru` forced** (rules 1 and 7). Total runtime ~1h 52m.

**What the trial decides:** if the serialized-execution format (pick 1) yields, the П-44 six-part series is worth a dedicated round on its own and this is a Group A channel. If only the guest video (pick 3) yields, take the standalones and skip the series. If the outcome video (pick 4) yields, look for more of that format across the tail before writing the tail off. **If picks 1 and 2 both come back thin, close the channel** — those are the two formats the whole Tier 1 case rests on.

## Open items for the user

1. **Budget question, stated plainly:** this is a narrow single-trade channel against the vault's densest room. Worth the four-video trial? The gap table above is the case for yes; the ~28 thin обзоры are the case for keeping it to one round regardless of outcome.
2. **`ahHspdChZZc` («за 250 тысяч») is the only price-bearing title** and needs its year confirmed before any figure from it is comparable. It is deliberately **not** in the trial batch.
3. Group classification: **provisionally Group A** (construction/renovation technique), not Group B — this is execution content, not design. Queue entry added accordingly.
