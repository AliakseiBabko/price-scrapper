# ВАШ ДИЗАЙНЕР ИНТЕРЬЕРА (@YourInteriorDes) — channel triage

**Created** 2026-09-03. Requested directly by the user. This channel is **Group B entry #4** in [[youtube_channel_queue|the YouTube channel queue]] — it was already on the list as "value UNCONFIRMED, trial-only," and had never been preflighted.

- Channel: https://www.youtube.com/@YourInteriorDes/videos
- Channel ID: `UCoJvM19nhHxfplqcO4wDL4A`
- Preflight manifest: `_Inbox/planning/preflight_20260903T072237Z.json` (light mode) — **220 videos, 220 fresh, 0 duplicates.** Nothing from this channel has ever been processed.
- Title dump: `_Inbox/planning/yourinteriordes_titles_dump.txt` (Russian titles, duration, view count) and `yourinteriordes_titles_meta.json`
- Identity: **a St Petersburg premium design-and-build studio's own channel** — NSDSGN (`nsdsgn.ru`), fronted by Senchugov (Instagram `@senchugov`). Channel description: «Дизайн-проекты и ремонт интерьера премиум класса / 400+ реализованных объектов / Берём ответственность за сроки, бюджет и результат».
- Jurisdiction: **Russia (St Petersburg).** Standing rule 4 applies — nothing from this channel goes to `16_Legal_and_Regulations/` (Belarus-only).
- Catalogue spans roughly 2017 → 2026 (newest-first ordering; the bottom ~65 entries are the 2017–2019 vlog/professional-tour era). **Titles carry years (2021, 2024, 2025, 2026) but upload dates are unconfirmed** — light mode does not fetch them. Confirm each from `yt-dlp` metadata at fetch time per the standing rule, especially for the cost videos.

## ⚠️ Two channel-specific traps, both found during triage

### 1. This channel has YouTube multi-language metadata enabled — the auto-translation trap is live

`yt-dlp` returned **English titles by default** ("WHY HOME THEATERS ARE A COLLECTIVE FARM" for «ПОЧЕМУ ДОМАШНИЕ КИНОТЕАТРЫ - ЭТО КОЛХОЗ"). The dump above was only obtained by forcing `--extractor-args youtube:lang=ru`.

**That is direct evidence the channel publishes translated metadata, which means auto-dubbed and auto-translated caption tracks are likely present too.** Standing rule 1 forbids fetching or citing them. **Every fetch from this channel must force `--languages ru` and the resulting transcript must be spot-checked as genuinely Russian, not a translated track.** This is the first channel in this vault where the trap has been *observed* rather than merely guarded against — worth carrying forward as a preflight step for other channels.

### 2. There is no crowd signal to rank by on this channel

View counts are unusually low and near-random relative to length: 72- and 81-minute expert Q&A videos sit at 10–78 views, while a 4-minute Ferrari test drive has 659 and a golf vlog 504. The highest-viewed items (814, 834, 886, 908) are a mix of «уют» listicles, a Spanish-stone showroom clip and an architect interview.

**On other channels view count has been a usable secondary ranking signal. Here it is noise, and following it would systematically deprioritise the long-form technical content — which is the only content worth processing.** Rank by format and subject only.

## Identity read: this is a design-**build** studio, not a design studio

The description commits to «сроки, бюджет и результат» — the studio does the renovation, not just the drawings. That has two consequences:

- **The advertising filter applies at full strength, and the specific tier-steering risk is named in the description: «премиум класса».** Expect the premium option to be characterised favourably. Two videos are the pitch itself rather than advice — `i9n1YI4iaiw` («Почему нельзя начинать ремонт без дизайн проекта?») and `JTyJVpFawpI` («Как выбрать дизайнера интерьера — 5 признаков профессионала») — and are marked accordingly below.
- **But it also means the channel has site access and trades in construction, not only styling** — hence the rough-stage site reviews, engineering-systems videos, and long-form Q&A with its own builders. That is the reason this channel is worth processing at all.

## ⚠️ The main triage finding: this channel breaks the Group B premise, the same way Шеврина/SMBUREAU did

Group B's premise is that a design/room-tour channel may yield nothing transcript-extractable. **The room-tour half of this catalogue fits that premise exactly and should be skipped almost entirely. The other half does not.**

The catalogue splits cleanly:

| Cluster | Approx. count | Verdict |
| :--- | :--- | :--- |
| Room tours / «Обзор квартиры N м²» / «Рум тур» / ЖК reviews | **~75** | **Tier 3** — the studio's own finished objects, narrated, no alternatives compared |
| 2017–2019 vlog era: Spanish/Italian tile-factory showroom tours, exhibitions, travel, Ferrari, golf, football | **~30** | **Tier 3** |
| Commercial interiors (barbershop, dentistry, two offices, culinary salon) | 5 | **Tier 3** — not an apartment vault subject |
| Career/profession content, feng-shui interviews, DIY crafts | ~10 | **Tier 3** |
| Trend-of-the-year videos (2025, 2026, Milan, Italy) | 6 | **Tier 2** — dated by construction, low durability for a one-flat decision vault |
| **Technical, materials, engineering, cost, process and storage content** | **~60** | **Tier 1 — the reason to process this channel** |

**The Tier-1 cluster is also where the long-form content is.** Five videos run over 55 minutes and four of the five are Q&A or podcast formats with a named guest — a builder, a light designer, an architect. Шеврина's finding was that **format predicts yield better than topic**, and the podcast/Q&A format was the richest there. This channel has the same format available and untested.

## Tier 1 — the substantive cluster, grouped by destination

### Engineering systems and services

| ID | Len | Title | Likely destination |
| :--- | :--- | :--- | :--- |
| `ZKAcnh4kKfY` | **81 min** | 10 вопросов о СВЕТЕ В ИНТЕРЬЕРЕ — китайский свет, дизайнерские фейлы, теплота и интенсивность света | `12_Engineering_and_Systems/Electrical_and_Lighting.md` |
| `7DnlE-pl0y4` | 26 min | Ошибки в освещении. 9 советов профессионального светодизайнера | same |
| `P-up1d1Nl2Q` | 13 min | 7 секретов освещения — сценарии, типы светильников | same |
| `xA0pFTLCt5M` | 19 min | ВЕНТИЛЯЦИЯ и КОНДИЦИОНИРОВАНИЕ — типы, стоимость, ошибки | `12_Engineering_and_Systems/HVAC_and_Ventilation.md` |
| `AH1INy0i5lU` | 34 min | Как избавиться от шума соседей — звукоизоляция стен, пола, потолка | soundproofing pages |
| `Z0brwxSe7gQ` | 43 min | Инженерные системы квартиры / обзор стройки 2024 | mixed engineering |
| `EONwZL7d5ck` | 9 min | Трубчатый радиатор — оправдана ли цена | `12_Engineering_and_Systems/Heating.md` |
| `k092OQqUqWU` | 3 min | Как сделать душевую в уровень с полом | `08_WC` / waterproofing |

**Coverage note that shaped the trial pick**: `colour temperature` returns **0** matches across the vault and `Kelvin` only 6, against 200+ files mentioning soundproofing and 150 mentioning stretch ceilings. **Lighting quality — colour temperature, intensity, fixture sourcing — is the thinnest of these subjects and has an 81-minute source available.**

### Surfaces, finishes and partitions

| ID | Len | Title | Likely destination |
| :--- | :--- | :--- | :--- |
| `gTgUJaWKobM` | 27 min | Современный натяжной потолок. Теневое примыкание. Разбор от специалиста | `13_Surfaces_and_Finishes/Ceilings_Guide.md` |
| `3tgHGhY0gXA` | 20 min | Натяжные потолки или гипсокартон? | same |
| `I7QptpZ0bAk` | 17 min | Обзор напольных покрытий 2025 | `13_Surfaces_and_Finishes/Flooring_Guide.md` |
| `ryCn_b9a_bg` | 19 min | Обзор ещё 12 напольных покрытий 2024 | same |
| `7hp4R1K8AQw` | 6 min | Как производят ПАРКЕТ? | same |
| `unfPu3A7MxM` | 22 min | МИКРОЦЕМЕНТ — что с ним не так? | `13_Surfaces_and_Finishes/Walls_and_Paint.md` |
| `cl0LIAVZUjI` | 23 min | 5 трендов оформления стен. Декоративная штукатурка | same |
| `x1ymR0UKm_E` | 14 min | Как безошибочно выбрать ПЛИТКУ? 5 правил | tile pages |
| `8NXiXZDVh7A` | 11 min | Какую ПЛИТКУ купить — как не разочароваться через год | same |
| `pR1t7zlT2Qk` | 19 min | Стеклянные перегородки: дорого или нет? 10 мифов | partitions / layout |
| `M7NXBh0hIo8` | 28 min | Перегородки из стекла, алюминия и стали | same |
| `Tj94jGH6fls` | 28 min | СТЕКЛЯННЫЙ КИРПИЧ ФАЛЬКОНЬЕ | **`Фальконье` = 0 vault matches, `стеклоблок` = 1** |
| `VhL_IrZG2kM` | 12 min | ПОДОКОННИКИ, ОТКОСЫ — все варианты декора | `13_Surfaces_and_Finishes/Windows.md` |
| `wyZcbPK6jnA` | 29 min | НЕ ВЕШАЙТЕ ШТОРЫ, пока не посмотрите ЭТО | curtains/window treatment |
| `_EgOrCroNZ4` | 13 min | Вешаете шторы? 5 ужасных ошибок | same |

**⚠️ `теневое примыкание` (shadow-gap ceiling perimeter) returns 0 matches in the vault**, while `shadow gap` in English returns 10 and `stretch ceiling` 150. The specific detail is thin even though the general subject is dense — which is what makes `gTgUJaWKobM` a useful narrow test rather than a duplicate.

### Kitchen

| ID | Len | Title | Likely destination |
| :--- | :--- | :--- | :--- |
| `-6QKr4HerCQ` | 32 min | Как заказать идеальную кухню? 25 ошибок | `03_Kitchen` |
| `hEZntyMcP-A` | 24 min | Как уместить всё в КУХНЕ 5 кв.м? | `03_Kitchen` (small-kitchen planning) |
| `wvlr2aGDMCc` | 19 min | Эти 5 ОШИБОК испортят ВАШУ кухню | `03_Kitchen` |
| `7vck4_oV2rQ` | 14 min | За что не стоит переплачивать на КУХНЕ? | `03_Kitchen` + budget |
| `AEJlxbTmQJU` | 28 min | Кухня дизайнера — хранение, наполнение, функционал | `03_Kitchen/Kitchen_Furniture.md` |
| `K8bkvE8o7QE` | 6 min | Монтаж фартука — до или после кухни? | sequencing detail |
| `VL_Hq252WEk` | 9 min | Как сделать современную и стильную кухню? | `03_Kitchen` |

### Furniture

| ID | Len | Title | Likely destination |
| :--- | :--- | :--- | :--- |
| `P3O2koqOGp8` | 15 min | Производство корпусной мебели. Почему дорого и как оценить качество | `14_Furniture` |
| `KPRcI_CPpAs` | 16 min | Как выбрать ДИВАН и не прогадать | `14_Furniture` (loose furniture) |
| `dIM5yK5dHNk` | 26 min | Как выбрать диван на заказ правильно? | same |
| `eX1IIwdn6Bk` | 25 min | МЕБЕЛЬ ИЗ КИТАЯ ЛУЧШЕ ЕВРОПЕЙСКОЙ? | `14_Furniture` market structure |
| `RGkLr-GTc6E` | 24 min | Стоит ли покупать мебель из Китая? | same |
| `h-qg_dns-ZU` | 19 min | Мебель из Европы — почему так дорого? | same |
| `SAqwDiuXmhE` | 13 min | ИКЕА под новым брендом? SWED HOUSE ожидание/реальность | same |

**Note**: the China-vs-Europe furniture cluster (three videos) pairs directly with the FLAT channel's «Мебель из Италии ВСЁ?» finding on import substitution, and with Безверхая's paint-side finding on the same phenomenon. **A cross-source comparison is available here, not just an addition.**

### Cost, contracting and process

| ID | Len | Title | Likely destination |
| :--- | :--- | :--- | :--- |
| `M0Wv4SOSUhs` | **72 min** | 15 важных вопросов о ремонте и дизайне. Ответы опытного строителя | mixed technical |
| `SEdNCGA0Ttg` | **70 min** | КАК ВЫБРАТЬ СТРОИТЕЛЕЙ И НЕ ПОЖАЛЕТЬ? Подкаст | `11_Budget_and_Planning` contracting |
| `yaeQr8Q0tCQ` | **63 min** | Стоимость ремонта в 2024? Бюджет стройки. Подкаст | `11_Budget_and_Planning` |
| `HbQHuyokSd0` | 18 min | Как потерять 58 МИЛЛИОНОВ на ремонте — строители в бегах, шантаж, суды | contracting risk |
| `femc1QkWzG8` | 15 min | Сколько сейчас стоит ремонт — почему так дорого | `11_Budget_and_Planning` |
| `AMMIMihB-Mc` | 27 min | Цены на мебель и стройматериалы. Импортозамещение | market/pricing |
| `K2pg-8iGP4s` | 37 min | 20 советов как сэкономить на ремонте | budget tiers |
| `AlUOhFGNvLc` | 14 min | 3 важных этапа ремонта. Последовательность отделки | `11_Budget_and_Planning/Renovation_Sequence.md` |
| `ka0rqfSjO_c` | 15 min | Как подготовиться к ремонту? С чего начать? | same |
| `7zpsZtcTkCM` | 57 min | Все фишки и трудности ремонта — квартира дизайнера 55 м² | mixed, own-flat case |
| `2B67955_Z5I` | 51 min | СЕКРЕТЫ РЕМОНТА ОТ ЭКСПЕРТОВ. Обзор стройки | mixed |
| `bJz8bG_CFSI` | 46 min | Серьёзный ремонт 2024 — окончание чернового этапа | rough-stage sequencing |
| `Kygk24zWv-8` | 12 min | Как выбрать квартиру — 10 советов дизайнера | `11_Budget_and_Planning` |
| `1Dpc8SLJd6M` | 47 min | СТРОИМ ДОМ. Разговор с архитектором Zrobim Architects | ⚠️ see below |
| `i9n1YI4iaiw` | 22 min | Почему нельзя начинать ремонт без дизайн-проекта? | ⚠️ **this is the pitch** |
| `JTyJVpFawpI` | 10 min | Как выбрать дизайнера интерьера — 5 признаков | ⚠️ **this is the pitch** |
| `pwNypmJNTcg` | 10 min | Ремонт 15 комнат БЕЗ ДИЗАЙН-ПРОЕКТА в элитном доме | interesting counterweight to `i9n1YI4iaiw` |

**⚠️ `1Dpc8SLJd6M` is the one Belarus-adjacent item on the channel.** Zrobim Architects is a **Minsk** studio, and this apartment is in Belarus — so a Belarusian practitioner's voice is genuinely scarce and valuable here. **But the subject is building a house, not renovating a flat, and standing rule 4 still governs**: any regulatory claim it makes goes to the relevant technical page with the jurisdiction flagged, never to `16_Legal_and_Regulations/` on the strength of the guest being Belarusian. Worth a deliberate later decision, not in the trial.

### Storage and living-with-it

| ID | Len | Title | Likely destination |
| :--- | :--- | :--- | :--- |
| `9ZwqMKiMgvc` | 35 min | Как хранить вещи в МАЛЕНЬКОЙ квартире с БОЛЬШОЙ семьёй | storage / `17_Design_and_Ergonomics` |
| `cudO-SSdrn0` | 33 min | Вы неправильно храните вещи! Приёмы от дизайнера | same |
| `RtRabYtDxNk` | 29 min | У вас беспорядок? Начните хранить вещи правильно | same |
| `hllO93k4O7Q` | 15 min | Расхламление гардероба | same |
| `Y1lBVJz-ib4` | 20 min | Интерьер, который не придётся часто убирать | maintenance-driven finish selection |

**Four storage videos totalling ~112 minutes is the largest single-subject block on the channel.** Storage is well-represented in the vault by volume (442 files mention it) but mostly as incidental mentions inside room pages; a dedicated multi-source treatment does not exist.

### Design reasoning and mistakes (option-framed — the Group B "genuinely reusable" test)

Per the queue's own criterion, these are the titles that frame **a problem with multiple named solutions** rather than narrating one finished flat:

`ibg1vWH9RF8` (10 приёмов визуально увеличить комнату) · `Nr0fILr9Ck8` (10 приёмов декорирования) · `FImWEXa5qWg` (10 способов сделать интерьер дороже) · `l3GPUc1GJWw` (12 способов создать уют) · `gcXhjK7PyGI` (цвет, ошибки, цветовой круг) · `RxU4L7ce86E` (**69 min**, ошибки родителей в детской, с психологом) · `WCoqOCofPx4` (10 правил неубиваемого интерьера) · `2vyIWKmrSXM` (20 ошибок) · `CSpXvPWpsgQ` (15 вещей) · `CN-Ab_g4CAI` · `lhikl-7c43c` · `34D4bv2dNLw` · `vvf2wcUYaUE` · `-1hfcmvUGjY` · `3y-gA7A6QJ4` (идеальная ванная) · `_nDCLhRUojE` (ванная дизайнера 4 м²) · `3_76xEfI01k` (почему дом это не квартира) · `hOLv4HZqCbI` (культовые предметы дизайна, как отличить подделку) · `QdH15TUctG4` (искусство в интерьере) · `bPNt1L_B4jY` (**89 min**, почему домашние кинотеатры — это колхоз)

**These are Tier 1 by title but Tier 2 by confidence.** The mistakes/regrets format repeats heavily across the channel (at least eight near-identical titles), so expect steep inter-video duplication within this block. **Process one, measure the dedup, then decide — do not batch them.**

## Tier 3 — skip without fetching

- **~75 room tours and object reviews.** Every «Обзор квартиры N м²», «Рум тур», «ЖК …» title. This is the studio's own delivered work, narrated. Per the project's advertising filter and Group B's own criterion, a single showcased result is not a technique.
- **The 2017–2019 vlog era, entries ~155–220.** Thirteen Spanish/Italian tile-and-fixture showroom tours («Проф тур 2019», Porcelanosa, Venis, Grespania, Pamesa, Marazzi, Florim, Antonio Lupi), exhibition walk-throughs (Habitare 2018, Stockholm Furniture Fair, MAISON&OBJET), plus Sochi/football, Ferrari, golf and Paris vlogs. Short-format and promotional.
- **Commercial interiors**: barbershop (`NIM2JM3Mgf0`), dentistry (`ngHlf5AYfQ4`), two offices (`8wlEd0KuLGA`, `4_izi-kIEP8`), culinary salon (`aCOj0C2sPWI`).
- **Career and profession**: marketing for designers (`DyX4TtKQRfI`), how to become a designer (`VQpfwvwNss4`), «кто такой дизайнер» two-parter (`GchKE5JcZXY`, `AExPf1LRrkI`), architect interview (`eSOS17Lb3C8`).
- **Feng shui interviews** (`NHqf-OoLPBM`, `Hvo3k-sFnk4`) — one is explicitly titled «Разрушаем мифы», but this vault has no use for the subject either way.
- **DIY crafts**: plywood console (`lbNCoKOjWno`), two pendant-lamp-from-a-bottle builds (`lVS7X08Bfas`, `YkgFNaAS_kc`).
- **Travel/lifestyle property tours**: Dubai Bentley villa (`ejSKZhGFy24`), Dubai $4M house (`Hysa7p4l7sw`), Tokyo vlog (`Ij2JZoOYSLM`), two Petersburg architecture walks (`9Pz0R8tUrZU`, `bZk8yfe2gAU`), tree house (`d1yrII1Q2vc`), Thailand studio (`UKdhx-vPjhM`).
- **Stunt**: `LlREkap9wio` («поджигаем кухню за 2.000.000»).
- **Trend-of-the-year videos** (`Iw6OQgemnnM`, `wdo7VGRJiH8`, `Vx2nrh29UjA`, `Qzju6MhJsfA`, `NLORI_VY1LE`, `rK_IM8LhL_4`, `kXdbbiBI84A`, `gtOh0FbHqHY`, `mxrm9eau7ZY`) — **Tier 2 rather than a hard skip**, but dated by construction and this vault records decisions for one flat, not fashion cycles. Only worth it if the trial shows the channel puts real material reasoning inside a trend framing.

**⚠️ One Tier-3 borderline worth naming rather than burying**: `Cr2Pq2ig7Ns` — «Купил особняк за 2.000.000 рублей и восстановил его. Дом Никуличева». A priced restoration of a historic building at 50 minutes and the channel's third-highest view count. **Wrong building type for this vault** and that is why it is here, but it is not showcase content and a later decision could go either way.

## Round 1 trial batch — 6 videos, scoped and ready, awaiting go-ahead

Group B's standing instruction is a 2–4 video trial. **I am proposing 6, deliberately, for a reason this vault has already established**: Шеврина/SMBUREAU's three-round finding was that **format predicts yield better than subject does**, and this channel has six materially different formats in its Tier-1 cluster. A 3-video trial would confound format with topic and could not produce the verdict Group B actually asks for.

Each pick tests a different thing rather than maximising expected yield:

| # | ID | Len | What it tests |
| :-- | :-- | :--- | :--- |
| 1 | `M0Wv4SOSUhs` | 72 min | **The expert-guest long-form format**, and a *builder's* voice on a designer's channel — the highest-density bet, and least exposed to the studio's own tier-steering |
| 2 | `ZKAcnh4kKfY` | 81 min | **The thinnest subject in the vault with a long source available** — colour temperature returns 0 matches, Kelvin 6. Also tests whether "10 questions about X" yields numbers |
| 3 | `9ZwqMKiMgvc` | 35 min | **The user's own Group B reusability criterion** verbatim: one specific problem, multiple named solutions. And it is the head of a 4-video, 112-minute block, so its yield decides the block |
| 4 | `-6QKr4HerCQ` | 32 min | **The doubted "N mistakes" list format, against a subject the vault is already rich in** — so the measurement is dedup pressure, not novelty. If this one is thin, ~20 Tier-1 titles collapse to Tier 3 |
| 5 | `gTgUJaWKobM` | 27 min | **The narrow named-technique format**, on a detail that is genuinely absent (`теневое примыкание` = 0) inside a subject that is dense (stretch ceilings = 150 files) |
| 6 | `pR1t7zlT2Qk` | 19 min | **A myth-busting format that promises a price** («дорого или нет? 10 мифов») from a studio whose description says «премиум класса» — the sharpest available test of tier-steering |

**Fetch discipline for this batch**: serialized, one at a time, ~5–6 minute spacing, anonymous, and **`--languages ru` forced with a Russian-content spot-check on each transcript** per trap #1 above. Four of the six are 27–81 minutes, so expect large transcripts.

**⚠️ Caption availability is the main unknown and could end this before it starts.** The channel is small (view counts in the tens), long-form, and has multi-language metadata enabled. Manual Russian captions may not exist on the podcast-format videos at all. If two of the six come back caption-less, that is a finding about the channel, not a fetch failure to retry.

### The verdict this trial must return

Not merely "did it clear the bar," but, per Group B's genuinely-open framing:

1. **Does the long-form expert-guest format on a designer's channel yield mechanism-and-number content?** If yes, this channel is reclassified as Group A presented by a designer — the Шеврина precedent — and gets the normal round pipeline. If the density is in the guest and not the host, that is a sharper and more useful finding.
2. **Can a premium design-**build** studio be trusted on cost and on material tiers it sells?** The FLAT verdict was "yes, on behavioural evidence, with named caveats." This studio has a stronger commercial interest than a furniture maker does, because it sells the whole renovation.
3. **Does the mistakes/regrets block have any content beyond its first instance?** Eight near-identical titles is either a rich seam or one video published eight times.

## Queue position and cross-references

- Group B entry #4, now preflighted. The Group B recommendation in [[youtube_channel_queue]] — "run one small trial across a couple of these channels and let the user decide whether to invest in the group at all" — **is still unspent; six of the eight original Group B channels remain unpreflighted.**
- Closest precedents for how this channel is likely to behave: [[shevrina_smbureau_channel_plan_20260830]] (designer channel that yielded technical content and was reclassified) and [[flat_interio_channel_triage_20260902]] (a seller's own channel, and the trust verdict on one).
- **Unrelated pre-existing issue surfaced by this preflight run, flagged not fixed**: the tool warned that **565 source notes have no matching flat-index ID** and 98 indexed IDs have no source note. That is index drift affecting the whole vault, not this channel, and it predates today. Worth a `tools/build_knowledge_base_index.py` rebuild as separate work.
- **Tooling note**: `preflight_playlist.py` fails under the repo's active `.venv-ifc314` interpreter (no `yt_dlp` module). It runs under `py -3`. Use `py -3 tools/youtube/preflight_playlist.py …` on this machine.

## Round 1 results and verdict (completed 2026-09-03)

**Round 1 yield**: 6 videos processed, 172 new facts, yield = **28.7 new facts per processed video** — **the highest single-round yield recorded for any channel in this vault** (previous high: FLAT Round 3 at 24.0). All 6 fetched serialized with `--languages ru` forced, zero rate-limit signatures. **6/6 clear the value bar; none was skipped or partially processed.** Batch state in `batch_status_20260903_yourinteriordes_round1.json`.

| # | ID | Topic | Len | Uploaded | `fact_yield` | `promotional_ratio` | Outcome |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | `M0Wv4SOSUhs` | Builder Q&A — cost tiers, смета, генподряд | 72 min | 2023-12-15 | **34** | low | Full |
| 3 | `9ZwqMKiMgvc` | Space organiser's own flat — storage | 35 min | 2026-03-25 | **33** | low | Full |
| 5 | `gTgUJaWKobM` | Stretch ceilings, теневое примыкание | 27 min | 2023-01-25 | **31** | medium | Full |
| 4 | `-6QKr4HerCQ` | 25 kitchen ordering mistakes | 32 min | 2025-07-22 | 28 | medium | Full |
| 2 | `ZKAcnh4kKfY` | Lighting podcast — colour temperature, gear | 81 min | 2024-01-09 | 27 | low | Full |
| 6 | `pR1t7zlT2Qk` | Glass partitions, 10 myths | 19 min | 2026-07-14 | 19 | **high** | Full |

**Seventeen pages touched across seven folders**, all in the same session as extraction per standing rule 6. No new pages created — every sub-topic had an existing home. Caption availability was never a problem: **2 manual Russian tracks, 4 Russian ASR, none translated.**

### ⚠️ The verdict on the round's stated question

**Yes — this channel breaks the Group B premise, and it does so for a more specific reason than Шеврина did.** Шеврина turned out to be a designer producing technical content herself. **Here the content is carried by the guests, not the host.** Four of the six are guest formats, and the two highest-yield sources are a contractor of 30+ years and two lighting specialists. **That distinction is the single most important planning output of this round**, because it says which of the ~54 remaining Tier-1 titles are worth anything.

**On whether a premium design-*build* studio can be trusted:** yes, with the caveats below, and the evidence is behavioural rather than tonal. **Twice in six videos the host publishes expert testimony that limits his own professional authority:**

- A space organiser stating that a designer **«вряд ли мог»** have foreseen storage — *could not have*, not merely did not — with her own designer-drawn wardrobe rebuilt afterwards as the example.
- Two lighting specialists describing the designer as **«ключ от всех дверей, но с очень ограниченным функционалом… решение финальное не за ним»**, which he endorses on camera and extends with a medical analogy.

Add to that: the builder podcast opens with an explicit disclaimer of any commercial tie; the ceiling installer **endorses the 250–300 RUB/m² mass-market tier for a rental flat**, steering out of his own segment; the kitchen video's cost-down advice repeatedly steers away from spend, **including away from work a designer would bill for**; and the partition maker **concedes two of his own ten "myths" as true** (monthly dusting, and that painting metal well is genuinely hard).

**The caveats that must stay attached:**

1. **⚠️ `pR1t7zlT2Qk` is a clean failure and the round was designed to catch exactly this.** The title asks «дорого или нет?» and the video **never states a single price** — not for a partition, a door, or a square metre. The expense question is answered entirely with a cost-*structure* argument that justifies the price. **Highest promotional ratio of the round, and the pattern to watch for on the rest of the channel: a partner-showroom episode whose title promises a number.**
2. **Brand preferences from supplier guests are stated practice, not independent comparison** — the ceiling profile line, Blum, Egger-style hardware verdicts, the "phone our supplier for installer recommendations" close.
3. **Only three of six sources carry absolute prices** (Dec 2023, Jan 2023, Jan 2024). Two carry none at all, and the kitchen video is **deliberately all ratios** — which is a strength, not a gap.
4. **The 81-minute lighting podcast is much thinner on hard photometrics than its runtime implies** — no CRI figure, no lumens, no wattage, no pulsation coefficient across 81 minutes. **It is a relationship podcast containing four excellent technical passages.** That is a format warning for the channel's other long-form titles, not a complaint about this one.

### ⚠️ The round's most valuable outputs were two corrections and a divergence, not additions

- **`Ceiling_Type_Comparison_and_Cost.md` carried "does not yellow" on a virgin-pellet material argument. The installer concedes yellowing from smoke over time.** Reconcilable as material ageing versus soiling — but the page can no longer carry the claim unqualified, and now says so.
- **The 27 mm stretch-ceiling drop is measured from the lowest existing obstruction, not from the slab** — extracted on camera by the host pushing back about junction boxes. **The page's existing ceiling-drop ranking is slab-referenced, so the two figures must never be compared.** This is the clearest instance in the vault of a claim arriving *with* its own correction because an interviewer did the work.
- **An unreconciled divergence on fridge top clearance: 300–500 mm here against Кузина's 200 mm** already on the page. Neither source states a derivation, so both stand with a note to take the larger where the cabinetry allows.
- Two smaller ones: **a dB claim corrected inline** (50 dB glossed as "half"; decibels are logarithmic), and **a genuine counter-data-point on ЛДСП and moisture** — a self-built shoe rack in the cheapest board with edges entirely unsealed, wet winter shoes, no swelling — recorded with its informality stated.

### What the trial design got right and wrong

**Right:** picking by format rather than by expected yield. The three formats that produced the highest yields — expert-guest long-form, a practitioner's own home, and a narrow named-technique breakdown — are all guest formats, and that is the finding that scopes the rest of the channel. **Selecting for vault thinness also worked**: `теневое примыкание` and `colour temperature` both returned zero prior matches and both produced page-level additions.

**Wrong, or at least less useful than expected:** the dedup-pressure pick (`-6QKr4HerCQ`) was chosen expecting it to be thin against a well-covered subject, and it came back at 28 — **because it turns out the vault's kitchen coverage is dense in dimensions and thin in costing ratios.** Useful, but it measured something other than what it was aimed at.

### Recommended Round 2 — 5 videos, awaiting go-ahead

**Weighted entirely to guest formats and to the trades, which is where all the yield came from:**

1. `M0Wv4SOSUhs`'s sibling: `SEdNCGA0Ttg` (**70 min**, «Как выбрать строителей и не пожалеть?») — **the direct continuation of the round's best source, on the subject the vault's contracting pages just gained the most from.**
2. `yaeQr8Q0tCQ` (**63 min**, «Стоимость ремонта в 2024? Бюджет стройки») — a second dated cost benchmark from the same podcast format, and 2024 sits in the gap between this round's Dec-2023 ladder and the vault's 2025 tiers.
3. `xA0pFTLCt5M` («Вентиляция и кондиционирование — типы, стоимость, ошибки») — **the ceiling source established that ventilation gates the ceiling; this is the ventilation half, and `12_Engineering_and_Systems/HVAC_and_Ventilation.md` exists.**
4. `cudO-SSdrn0` (**33 min**, «Вы неправильно храните вещи») — **the second of the four-video storage block, whose head returned 33.** Tests whether the block sustains or whether Ксения's own-flat visit was the whole of it.
5. `7DnlE-pl0y4` («Ошибки в освещении — 9 советов профессионального светодизайнера») — **a different lighting guest and a shorter format, to test whether the photometric thinness was the podcast format or the channel.**

**⚠️ Expect below 28.7.** Round 1 deliberately took the strongest guest formats, and the honest expectation is somewhere in the high teens to low twenties — still well above this vault's stop-and-ask floor.

**Deprioritised on the round's own evidence, not on title-skim:** the general-design and trend cluster (`SLTml8mznnI`, `YAq6gvJL6Fc`, `Gr_xR6mdz7M`, `mxrm9eau7ZY`, `kXdbbiBI84A`, and the six trend-of-the-year videos). **The host solo on design is this channel's weakest configuration, and the vault holds far better-sourced design content from designers who specialise in it.** The mistakes/regrets block (eight near-identical titles) remains untested and should be sampled **once**, not batched.

## Round 2 results and verdict (completed 2026-09-03)

**Round 2 yield**: 5 videos processed, 145 new facts, yield = **29.0 new facts per processed video.** All 5 fetched serialized with `--languages ru` forced. **Zero rate-limit signatures across both rounds — 11 transcript fetches and 11 metadata calls, none blocked.** Batch state in `batch_status_20260903_yourinteriordes_round2.json`.

| # | ID | Topic | Len | Uploaded | `fact_yield` | `promotional_ratio` |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | `SEdNCGA0Ttg` | Choosing builders — roundtable, ex-прораб on the panel | 70 min | 2024-08-15 | **33** | low |
| 2 | `yaeQr8Q0tCQ` | Renovation cost roundtable | 63 min | **2023-10-03** ⚠️ | **30** | low |
| 3 | `xA0pFTLCt5M` | Ventilation and AC — types, costs, mistakes | 19 min | 2023-10-17 | **30** | low |
| 4 | `cudO-SSdrn0` | Space organiser audits the designer's flat | 33 min | 2026-02-03 | 28 | low |
| 5 | `7DnlE-pl0y4` | Lighting mistakes — 500lux | 26 min | 2022-06-09 | 24 | low |

**Two rounds: 11 videos, 317 facts, yields 28.7 then 29.0.** **One page created and fifteen updated**, across eight folders.

### ⚠️ My Round 1 prediction was wrong, and the reason is the useful part

**Round 1 predicted "expect below 28.7 — somewhere in the high teens to low twenties." Round 2 came in at 29.0.**

**The prediction rested on the assumption that Round 1 had taken the channel's strongest titles. That was the wrong model of what Round 1 produced.** Round 1's real output was **a better selection rule** — that this channel's value sits in its guest formats and its trades — and Round 2 was composed entirely on that rule. **The channel is simply deeper in guest content than the decay assumption allowed for.**

**→ The transferable lesson: a decay prediction should be conditioned on whether the previous round changed the selection METHOD, not only on what it consumed.** Where a round produces a new discriminator, the next round can plausibly hold or improve.

### One page created, under the 3+-sources threshold

**`11_Budget_and_Planning/analysis/Technical_Supervision.md`.** Технадзор had accumulated passing mentions on four pages — Budget Tiers, Project Duration, Wall Prep, Contract Practice — with no home of its own, and `SEdNCGA0Ttg` then delivered a dense dedicated treatment that both advocates the role and dismantles it. **The page keeps авторский надзор and технадзор explicitly distinct**, which the passing mentions had begun to blur.

### ⚠️ A fragmented page was repaired as part of this round

**`AC_Key_Concepts_and_Placement.md` tripped the FRAGMENTED check after this round's addition** — 10 of 12 top-level headings named a processing batch rather than a topic. **The condition was largely pre-existing; this round's addition took it over the detection threshold, which makes it this round's to fix.**

Repaired with `tools/split_page.py merge`: **12 sections grouped under 5 thematic parents, with all 12 original dated headings demoted to `###` so every attribution and date survives.** `RESULT: CLEAN` — 75 content lines with 0 missing, 11 citation IDs before and after. **Not split, per the standing rule that splitting a fragmented page yields two fragmented pages.**

### ⚠️ Three things this round got wrong, and what they cost

**Recorded because the misses were more instructive than the hits.**

1. **A DATE TRAP that invalidated the pick's stated rationale.** `yaeQr8Q0tCQ` is titled «Стоимость ремонта в **2024**?» and I selected it on the reasoning that 2024 filled the gap between Round 1's Dec-2023 ladder and the vault's 2025 tiers. **Its confirmed upload date is 2023-10-03 — ten weeks BEFORE Round 1's ladder, not after.** Second title-year/upload-year mismatch in this vault. **It turned out more useful than intended**: it became a near-simultaneous cross-check of the same market from the buying side rather than the selling side — **and the cross-check passed**, their ~25,000 RUB/m² SPb labour figure sitting ~25% above Round 1's contractor at ~20,000, in the direction you would predict. **But that was luck, not method.**
2. **⚠️ A SOURCE-IDENTITY MISS: `7DnlE-pl0y4`'s guest was already a vault source.** Сергей Реньжин of 500lux is recorded via Кузина's channel (`9MsEZVjLH2M`, 2022-08-25), and this appearance is **ten weeks earlier**. I selected the video for "a different lighting guest" and got the same one. **Handled by discounting the yield, marking the affected lighting-page claims as one practitioner on two channels rather than independent confirmations, and correcting an attribution — the vault credited Реньжин with the physiology mechanism for the same-scene rule, and here he gives that rule with a different mechanism, so the physiology framing is his later refinement.** **→ A preflight step worth adopting: check a guest's name against `_Sources/` before selecting a video for its guest.**
3. **The test question that source was chosen to answer got a third answer.** I asked whether Round 1's photometric thinness was the podcast format or the channel. **It was neither — it was the guest.** A 26-minute video with a lighting **designer** carries more usable illuminance and colour-temperature figures than Round 1's 81-minute podcast with a lighting **supplier**. **That refines the round's own selection rule: prefer the guest's discipline over the format's length.**

### What the round produced that matters most

- **⚠️ The densest contracting material in this vault**, from a panel containing an ex-прораб: four **green** flags (the vault was rich in red ones), two proposed signals recorded as **contested** because the panel rejects them among themselves, and **an inverted vetting test derived from consent practice rather than workmanship** — a builder who walks anyone onto any site without asking the owner will do the same with yours.
- **⚠️ "We comply with СНиП" is not a quality claim.** СНиП tolerances run to 5 mm per metre and developers hand over on exactly that — so acceptance criteria have to be tighter than СНиП and written down.
- **⚠️ A procurement-commission range with a vault-wide consequence: 2–15%**, volunteered by designers against their own industry. **Any designer-sourced material or supplier recommendation anywhere in this vault may carry one.** Routed to `Advertising_Promotional_Notes.md` as a standing reading rule, with their transparent alternative recorded as the thing to ask for.
- **⚠️ Round 1's ceiling loop closed from the other end.** Round 1's installer said ventilation gates the ceiling; this round's ventilation source supplies the arithmetic that makes it non-negotiable — **ducts take 150–200 mm, machines 300 mm minimum, section grows nearer the machine, and ducts go in first while the lighting arrives after the ceilings.** Plus independent confirmation of the combined ventilation-plus-track slot, from the designer's side.
- **⚠️ A coherence check across unrelated practitioners: Round 1's supplier gave the Kruithof rule; Round 2's designer independently gives 200–300 lux with 2700–3000 K for a children's room.** The rule and its application converging from different people is the strongest internal consistency signal either round produced.
- **A counter-intuitive cost mechanism: a minimalist interior costs MORE, not less**, because it removes the visual noise that hides poor execution — so it raises the minimum acceptable trade quality rather than lowering material cost.

### Recommended Round 3 — and the honest recommendation is to pause, not continue

**Two rounds have not decayed, so there is no yield argument for stopping. There is a different argument.**

**⚠️ The remaining Tier-1 pool no longer matches what made these two rounds work.** Eleven videos are processed and **every long-form guest format on the channel is now done** — both cost roundtables, the builders roundtable, both storage visits, both lighting sources, the ceiling specialist, the ventilation explainer. **What is left in Tier 1 is predominantly the host solo**, which Round 1 identified as this channel's weakest configuration and which Round 2 did nothing to rehabilitate.

**Specifically remaining, with an honest expectation attached:**

1. **`M0Wv4SOSUhs`'s remaining siblings and the site-review cluster** — `2B67955_Z5I` (51 min, «Секреты ремонта от экспертов, обзор стройки»), `Z0brwxSe7gQ` (43 min, engineering systems on site), `bJz8bG_CFSI` (46 min, end of rough stage), `7zpsZtcTkCM` (57 min, all the tricks of his own 55 m² renovation). **These are the only substantial guest-or-site formats left, and they are the strongest remaining candidates.** Expect below 29.0 but plausibly above 20.
2. **The two remaining storage videos** (`RtRabYtDxNk`, `hllO93k4O7Q`) — the block has now returned 33 and 28, but these are the shorter and narrower two, and the method is thoroughly documented. **Diminishing.**
3. **`1Dpc8SLJd6M`** — the Zrobim Architects (Minsk) podcast, **still the one Belarus-adjacent item on the channel and still flagged for a deliberate decision rather than a default skip.** Subject is building a house, not renovating a flat.
4. **The mistakes/regrets block** (eight near-identical titles) — **still untested, and should be sampled ONCE rather than batched.**
5. **The host-solo design and trend cluster — recommend against.** Round 1's scope finding stands and Round 2 reinforced it.

**⚠️ My recommendation: run one final round of the four site-review/own-flat items in (1) plus one probe from (4), then close the channel.** That is where the remaining value is concentrated, and after it the channel is host-solo design content this vault already holds better-sourced elsewhere. **Flagging rather than deciding: `1Dpc8SLJd6M` remains the user's call.**

## Round 3 results and verdict (completed 2026-09-03) — and the closing recommendation is REVISED

**Round 3 yield**: 5 videos, 148 new facts, yield = **29.6 per processed video.** **All five were MANUAL Russian caption tracks. Zero rate-limit signatures across all 16 fetches in three rounds.**

| # | ID | Topic | Len | Uploaded | `fact_yield` | `promotional_ratio` |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | `2vyIWKmrSXM` | **The probe** — 20 post-occupancy regrets | 31 min | 2022-10-25 | **32** | low |
| 2 | `2B67955_Z5I` | Site review, finish details | 51 min | 2025-01-31 | **32** | medium |
| 3 | `Z0brwxSe7gQ` | Engineering systems on site | 43 min | 2023-10-11 | **30** | low |
| 4 | `7zpsZtcTkCM` | His own 55 m² flat, start to finish | 57 min | 2023-06-14 | 29 | low |
| 5 | `bJz8bG_CFSI` | End of rough stage | 46 min | 2024-05-03 | 25 | medium |

**Three rounds: 16 videos, 465 facts, yields 28.7 / 29.0 / 29.6.** **Sixteen pages updated across seven folders; no new page needed.**

### ⚠️ I predicted decay three times and was wrong three times — the corrected model

Round 1 → predicted below 28.7, got **29.0**. Round 2 → predicted below 29.0, got **29.6**. Round 3 → predicted below 29.0 "but plausibly above 20", got **29.6**.

**Each time I modelled yield as a function of TITLES REMAINING. The actual driver is FORMAT.** On this channel yield tracks whether a video is a guest format, a live site review, an own-object retrospective, or crowd-sourced outcomes — and barely tracks how many have already been taken. Round 3 was composed entirely of those formats, so it held.

**→ The transferable correction, and it applies to every channel in the queue: predict decay from the remaining pool's FORMAT MIX, not from its size. And when a round produces a new discriminator rather than merely consuming its best titles, expect the next round to hold rather than fall.**

### ⚠️ The probe reversed its own premise — and that is why the recommendation changes

**`2vyIWKmrSXM` was sent as a single probe to justify dismissing eight near-identical mistakes-and-regrets titles.** Rounds 1 and 2 both deprioritised the block as a likely repetitive listicle.

**It is not a listicle. It is a follow-up built out of the comment section of the first such video** — «выпуск вызвал огромный резонанс, зрители стали писать о своей боли… и я решил записать новый выпуск, где подробно разберу эти ситуации».

**→ The content is CROWD-SOURCED POST-OCCUPANCY REGRET DATA with a practitioner's remedy attached to each item. This vault has almost none of that, because nearly every source in it describes DECISIONS rather than OUTCOMES** — and this is the only kind of source that can say what people regret after living with a choice. **It also yields frequency information no single practitioner can give**: he identifies dark glossy floor tile as the single most-written-about regret in his comments.

**It returned 32, the joint-highest of the round.**

### ⚠️ Guest-identity check — it caught something it could not resolve

**Three of the five feature a contractor named Руслан. Applying the preflight step adopted after Round 2, the check was run and came back inconclusive**, which is recorded in all three notes rather than resolved by assumption:

- **Supports identification with Round 1's builder**: same first name, same role, same channel, same joint-project relationship — and Round 1's source records having already appeared on this channel twice, including on a joint object.
- **Does not confirm it**: no старый фонд reference, no 30-plus-years claim, no Петровская коса, and a company name («esus», ASR-garbled) the earlier source did not give. **The one «30 лет» in the transcript is him quoting other people's complacency, not describing himself.**
- **Treated as probably the same practitioner, with overlapping claims recorded as same-practitioner consistency rather than independent corroboration.** Little turns on it because the content is almost entirely new — **but the honest assessment is that the new step caught a possible duplication it could not settle, which is still an improvement on Round 2, where nothing caught it at all.**

### What Round 3 established that the earlier rounds could not

- **⚠️ A designer regrets self-coordinating his own 55 m² flat, having hired the best specialist in every trade.** «Я очень пожалел о том, что не нанял прораба.» **This recalibrates this channel's own генподряд threshold of ~300 m²: the coordination requirement is driven by the NUMBER OF INDEPENDENT SPECIALISTS to be sequenced, not primarily by area.** **Directly relevant to this project — self-managed, and far below 300 m². Recorded as evidence to weigh, with the actionable form being that the sequencing role must be someone's named job even in a small self-managed flat.**
- **⚠️ A painted-wall ACCEPTANCE PROTOCOL, which the vault did not have at all: «проявочный свет — не для приёмки, а для выполнения работ»; acceptance is with the normal lighting on at 1 metre from the wall; and daylight is unreliable in both directions.** This settles the otherwise unwinnable dispute of a client walking the walls with a torch.
- **⚠️ Three tiers of solution to the as-built problem, from one channel, and the cheapest costs a pencil** — photograph the open chases with pencilled dimensions (and the закладные, and the studs); label every box and wire; or keep an unmodelled 3D point cloud. With the measured cost of doing none of it: two days of an electrician's time on 30 m².
- **⚠️ The tooling asymmetry explaining the plasterboard-versus-block price AND staffing gap at once: 300,000 RUB of tooling against 10,000–30,000.**
- **⚠️ A rough-stage-only figure (22,000–28,000 RUB/m², May 2024) that NESTS correctly inside this channel's two other ladders.** Three figures, three sources, seven months apart, ordering correctly.

### ⚠️ REVISED RECOMMENDATION — do not close the channel yet

**My Round 2 recommendation was to run this round and then close, on the reasoning that every long-form guest format was exhausted and what remained was host-solo design content. Round 3's probe refuted the premise of that reasoning.**

**What is actually left, with honest expectations:**

1. **⚠️ The mistakes-and-regrets block — SEVEN more titles, now reclassified from "dismiss" to "process".** `CSpXvPWpsgQ` (15 things regretted, 27 min), `CN-Ab_g4CAI` (30 min), `lhikl-7c43c` (34 min, «красивые решения, оказавшиеся ошибкой»), `34D4bv2dNLw`, `WCoqOCofPx4` (10 rules of an indestructible interior), `vvf2wcUYaUE`, `-1hfcmvUGjY`. **Expect real inter-video duplication within the block — that risk was always genuine — but the probe returned 32, so the block deserves a proper round rather than a dismissal. Recommend 3–4 of them, longest first, and stop when the dedup ratio turns.**
2. **The two remaining storage videos** (`RtRabYtDxNk`, `hllO93k4O7Q`) — the block has returned 33 and 28; these are the shorter, narrower two. **Diminishing but not exhausted.**
3. **`RxU4L7ce86E`** — 69 min, kids-room design mistakes **with a child psychologist.** ⚠️ A guest format in a category this vault is thin on, and it was never triaged into any round. **On the corrected format model this is the strongest single unprocessed title on the channel.**
4. **`ZKAcnh4kKfY`'s siblings in the technical cluster** — `AH1INy0i5lU` (34 min, soundproofing), `gTgUJaWKobM` done, `3tgHGhY0gXA` (stretch vs plasterboard), the two flooring reviews, microcement, decorative plaster, the tile pair, the partition pair, `Tj94jGH6fls` (Falconnier glass brick, still zero vault matches). **All still unprocessed, all technical, several with named guests.**
5. **`1Dpc8SLJd6M`** — the Zrobim Architects (Minsk) podcast. **⚠️ Still the one Belarus-adjacent item on the channel, still flagged for the user's decision rather than a default skip, and now flagged for the third time.** Subject is building a house, not renovating a flat.
6. **Still recommend against: the host-solo general-design and trend cluster.** That finding has survived all three rounds.

**⚠️ Honest summary: the channel is not exhausted and I was wrong to think it would be. 16 of 220 videos are processed, roughly 45 Tier-1 titles remain, and the formats that produced three non-decaying rounds are still represented in the pool. The decision to continue is now a question of how much of the user's budget this channel deserves relative to the six unpreflighted Group B channels — not a question of whether the yield has run out.**

## Progress log

- 2026-09-03 — Preflight run (220 videos, 220 fresh, 0 duplicates), Russian title dump obtained after discovering the channel serves auto-translated metadata, full title-skim triage completed, vault-coverage probes run for candidate subjects, 6-video Round 1 trial scoped.
- 2026-09-03 — **Round 1 complete: 6/6 processed, 172 new facts, yield 28.7 — the highest single-round yield in this vault.** Zero rate-limit signatures. 17 pages across 7 folders; store, CSV and archive updated; `check_page_sizes.py` clean (no FRAGMENTED, nothing over backstop) and `verify_batch.py` 40 files / 0 problems. **Round 2 scoped above, awaiting go-ahead.**
- 2026-09-03 — **Round 3 complete: 5/5 processed, 148 new facts, yield 29.6 — above Round 2, against my prediction for the third consecutive time.** All five manual Russian caption tracks; zero rate-limit signatures across all 16 fetches. 16 pages across 7 folders; no new page needed; two additions were DISTINCTIONS on pages that already covered the subject (the wall-acceptance light regime, and a designer arguing against the master switch). **⚠️ THE PROBE REFUTED ITS OWN PREMISE: the mistakes-and-regrets block is crowd-sourced POST-OCCUPANCY OUTCOME data, not a listicle, and returned 32 — so my recommendation to close the channel is REVISED to "do not close yet". Corrected yield model recorded: predict decay from the remaining pool's FORMAT MIX, not its size.** `check_page_sizes.py` clean; `verify_batch.py` 0 problems. **`Contract_Practice.md` at 382 lines flagged in Pending Wiki-Page Decisions for a split on the next material addition.**
- 2026-09-03 — **Round 2 complete: 5/5 processed, 145 new facts, yield 29.0 — slightly ABOVE Round 1, against my own prediction of decay.** Reason recorded above: Round 1's real output was a better selection rule, not just consumption of the best titles. **One page created** (`Technical_Supervision.md`, under the 3+-sources threshold) **and fifteen updated across eight folders.** **One pre-existing FRAGMENTED page repaired** (`AC_Key_Concepts_and_Placement.md`, 12 sections → 5 thematic parents, `RESULT: CLEAN`, every attribution preserved). **Three misses recorded honestly: a date trap that invalidated a pick's rationale, a guest already in the vault, and a test question that got a third answer.** Zero rate-limit signatures across all 11 fetches. **Recommendation: one final round of the four site-review/own-flat items, then close.**
