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

## Progress log

- 2026-09-03 — Preflight run (220 videos, 220 fresh, 0 duplicates), Russian title dump obtained after discovering the channel serves auto-translated metadata, full title-skim triage completed, vault-coverage probes run for candidate subjects, 6-video Round 1 trial scoped. **Nothing fetched. Awaiting go-ahead.**
