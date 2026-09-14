# Channel triage — @Сосновскаяфабрикамебели (Сосновская фабрика мебели)

**Date:** 2026-09-14 · **Owner-supplied** · **258 videos** · **Status: CLOSED. Tier 1 (10 videos) processed 2026-09-14; Tier 2 measured and declined**

Owner's steer, verbatim in intent: *reviews and details of materials, appliances, techniques, errors, dos and don'ts, practical advice — not overviews.* Explicitly: **kitchen facade material selection, countertop selection, how to compose a kitchen correctly.** Explicitly **filter out**: representation, and advertising for this vendor's own products whether open or hidden.

---

## ⚠️⚠️ 1. Read this first: EVERY ENGLISH TITLE ON THIS CHANNEL IS A YOUTUBE AUTO-TRANSLATION

The first manifest pull returned titles like *"Tacky Kitchen. Never Do This"* and *"TOP 6 Secrets to Creating the Perfect American-Style Black Kitchen"*. **None of those is the channel's title.** Forcing `--extractor-args "youtube:lang=ru"` returns the real ones:

| What the listing showed | What the channel actually published |
| :--- | :--- |
| "Tacky Kitchen. Never Do This" | **«Колхозная кухня. Никогда так не делай»** |
| "The most useless kitchen hardware…" | **«Самая бесполезная фурнитура для кухни…»** |

**Caption manifest, verified on the top video (`y1XTG_FcbQo`): `ru-orig` (Russian, Original) plus derived `ru` and `en`.** ⚠️⚠️ **So the audio is Russian, the titles are Russian, and YouTube translated the metadata for this machine's locale.**

> **→ CONSEQUENCES, AND THEY ARE PROCEDURAL:**
> - **`--languages ru` is mandatory** (standing rule 1). An `en` fetch here would return a machine translation of a machine transcription.
> - **`source_title` in the CSV must be the RUSSIAN original.** The English string is not a title anyone published and would be unsearchable and unverifiable.
> - **A title-skim triage must be done on the `lang=ru` manifest**, or the skim is reading YouTube's paraphrase. The semantics survived translation here, but that is luck, not method.
> - **This is the FIFTH distinct form of the caption/title-language trap this vault has recorded**, and the first where the *manifest itself* was translated rather than an individual video's captions.

⚠️ **Also note**: the `lang=ru` pull returns **abbreviated view counts** (`66` for 6,600). View figures below come from the English-locale pull; titles from the Russian one, joined on video ID.

---

## 2. What this channel is

**A Russian kitchen factory's own channel** (Сосновская фабрика мебели), running since at least 2018. **Audience scale is an order of magnitude above anything else in this vault's kitchen sources** — the top video has **1.7M views**, eight are above 400k, and the median technical video runs **10–20 minutes**.

**⚠️⚠️ The advertising here has a different shape from the last vendor channel, and the filter has to match it.** CAPPUCCINO was ~85% customer testimonials, trivially excluded by title. **This channel has almost no testimonials.** Its filler is:

- **Project showcases** — «Эта КУХНЯ олицетворение…», «Мы создали идеальный дизайн…», «Обзор кухни в модном цвете года Pantone». A tour of a kitchen they built. **This is the hidden advertising the owner asked to filter**: it is shot as content, not as an ad, and it carries a real material list — but the material list is *their* specification, presented as aspiration rather than as a comparison.
- **Fashion/trend videos** — «Модная КУХНЯ 2020», «Тренды 2021/2022/2023/2024», «Формула идеальной кухни 2023». **44 of 258.** Dated by construction, and the vault has no use for kitchen fashion.

**⚠️ Zero-cost keyword exclusion removes 73 of 258** (44 trend/style, 21 showcase, 20 non-kitchen — wardrobes, closets, bathroom, hallway, a children's room, one house build). **That leaves 185, which is still far too many, because the real duplication is INTERNAL.**

---

## ⚠️⚠️ 3. The real filter is topic saturation, not the titles

Counting the survivors by subject:

| Subject | Videos | Verdict |
| :--- | ---: | :--- |
| **Facade materials** | ~30 | **Heavily saturated.** Film vs plastic vs enamel, acrylic vs plastic, super-matte, gloss, veneer vs LDSP, solid wood, metal, glass, FENIX, ALVIK, CLEAF, AGT, PerfectSense/Mattelux, powder coating, PP vs PVC… **Take the longitudinal ranking and the crash tests; decline the rest.** |
| **Countertops** | ~14 | **Saturated.** Take the head-to-head and the crash test. |
| **Small-kitchen layout** | ~12 | **Near-total overlap with each other** and with existing vault coverage. Take at most one. |
| **Ordering / pricing / scams** | ~11 | **Take three.** ⚠️ All prices are RUB, 2019–2025 — rule 2 blocks every figure; only the STRUCTURE transfers. |
| **Hardware & mechanisms** | ~14 | Take the useless/useful pair plus one on slides and lifts. |
| **Sinks, taps, backsplash** | ~8 | Take two. |
| **Appliances** | ~6 | ⚠️ Mostly covered by existing appliance sources. Take induction-vs-electric at most. |
| **Carcass construction & edging** | ~8 | **⚠️⚠️ NOT saturated and NOT covered elsewhere. Take three.** |

**Grep of the existing vault before triaging**, which is what decides marginal value rather than the titles:

| Term | Files mentioning it in `03_Kitchen/`, `14_Furniture/`, `15_Appliances/` |
| :--- | ---: |
| `постформинг`, `порошковое покрытие`, **`метр погонный`**, `ALVIK`, `PerfectSense`/`Mattelux`, `DEKTON` | **0 each** |
| `компакт-ламинат`, `кварц`, `CLEAF`, `индукцион` | **1 each** |
| `эмаль` | 3 |
| `FENIX`, `шпон` | 4 |

> **⚠️⚠️ THE FACADE AND COUNTERTOP INVENTORY IS THE PART THE VAULT IS LEAST SHORT OF.** The FLAT fabricator series already covers fine-line veneer, массив, the PVC-film refusal, plastics, enamel, glass, LDSP tiering, stone and HPL; the CAPPUCCINO round added painted-vs-laminated MDF with four physical tests, plus quartz, porcelain stoneware, HPL and the styrene refusal on liquid acrylic. **So "another facade overview" is worth almost nothing here.** What is worth something is the **named products with zero coverage** (ALVIK, PerfectSense/Mattelux, DEKTON, compact laminate, postforming, powder coating) and, much more, **the evidence types nothing else in the vault has** — see §4.

---

## ⚠️⚠️ 4. What this channel has that NO other source in this vault has

This is the actual reason to process it, and it is not the material overviews.

1. **⚠️⚠️ LONGITUDINAL FAILURE DATA.** `A9Kef6CvNZ4` — **«Моя первая КУХНЯ. 9 лет эксплуатации. Что с ней стало?»** The maker revisits a kitchen he built nine years earlier. **The CAPPUCCINO acceptance checklist closed by stating its own limit: every front material has a delayed failure mode invisible at handover, and no delivery-day inspection catches any of them. This video is the other end of exactly that gap.** **Nothing else in this vault observes a kitchen after years of use.**
2. **⚠️⚠️ PHYSICAL DESTRUCTIVE TESTING, repeatedly.** `-I97gsh-aek` (**24 hours underwater** — plywood vs LDSP vs MDF), `DEecuW1BjC8` (countertop crash test with real samples), `R3n52O7TmN0` (AGT facade crash test), `QoWW9smxCus` (vandal-proof facades, crash test). **The vault singled out CAPPUCCINO's four-test MDF head-to-head precisely because tested beats asserted. This channel does it as a format.**
3. **⚠️⚠️ A TEN-YEAR RANKING.** `p8cazVnSTc8` — «12 самых лучших фасадов для КУХНИ. **Экспертный рейтинг за 10 лет**», 26:38. **A ranking built on a decade of warranty and return experience is a different claim from a ranking built on a spec sheet.**
4. **⚠️⚠️ THE QUOTING UNIT.** `24DWOdqalc4` — «**Метр погонный кухни. Что это такое**». **Zero coverage in the vault, and it is the unit every kitchen in this market is quoted in.** Directly needed to read a quote, and it is where the comparison between two quotes goes wrong.
5. **⚠️ THE SUPPLY CONTRACT.** `xJNxhohL2OM` — «Грамотный договор купли-продажи мебели. Все нюансы». Pairs with `Contract_Practice.md`, which covers renovation contracts and not furniture supply.
6. **⚠️ CARCASS PRODUCTION AND EDGING.** `Lfvs1XUz53s` (25:39, 13 secrets of a durable carcass) and `iKWdPE1fRY8` (**«Главный показатель качества КУХНИ. 3 способа кромления»**). **The CAPPUCCINO source made edge banding a health item; this one is about how the edge is actually applied and why it fails.**

---

## 5. Proposed Tier 1 — 10 videos, ~2h20m

**Chosen for evidence type and for zero existing coverage, NOT for view count.**

| # | ID | Min | Russian title | Why |
| :-- | :-- | :-- | :--- | :--- |
| 1 | `A9Kef6CvNZ4` | 10:37 | Моя первая КУХНЯ. 9 лет эксплуатации. Что с ней стало? | **⚠️⚠️ The only longitudinal source in the vault. Closes the gap CAPPUCCINO named and could not fill** |
| 2 | `p8cazVnSTc8` | 26:38 | 12 самых лучших фасадов для КУХНИ. Экспертный рейтинг за 10 лет | **A decade of returns, not a spec sheet. The one facade video worth the length** |
| 3 | `-I97gsh-aek` | 13:22 | Теперь ты знаешь самый прочный материал… 24 часа под водой | **A destructive test on the substrate question CAPPUCCINO left open (any MDF front is moisture-limited)** |
| 4 | `Lfvs1XUz53s` | 25:39 | 13 секретов производства прочного корпуса КУХНИ | **Carcass, uncovered. Complements the acceptance checklist from the production side** |
| 5 | `iKWdPE1fRY8` | 11:47 | Главный показатель качества КУХНИ. 3 способа кромления | **⚠️⚠️ How the edge is applied and why it fails — the mechanism behind the health finding** |
| 6 | `24DWOdqalc4` | 8:44 | Метр погонный кухни. Что это такое | **Zero coverage; the unit every quote is written in** |
| 7 | `npaV7FELR9k` | 19:17 | Эпичная битва столешниц: DEKTON, кварц, акрил, компакт | **The countertop head-to-head; DEKTON and compact laminate are near-uncovered** |
| 8 | `0Hao_4VdnNw` | 16:00 | Правильная планировка кухни и грамотное расположение встроенной техники | **The owner's "how to compose a kitchen correctly", and it ties layout to appliance placement** |
| 9 | `cnW4A8uFCDc` | 11:52 | Самая бесполезная фурнитура для кухни | **1.3M views. A vendor naming hardware NOT to buy is an argument against its own upsell** |
| 10 | `xJNxhohL2OM` | 11:26 | Грамотный договор купли-продажи мебели. Все нюансы | **Furniture supply contract; `Contract_Practice.md` covers renovation contracts only** |

**Pairs with #9 if it lands well:** `AIPQ6ZLxTQk` (946k, «Самые полезные решения на КУХНЕ», 19:57) — the positive half of the same argument, and the two are only meaningful together.

---

## ⚠️⚠️ 6. Tier 2 — MEASURED AND DECLINED (2026-09-14, after Tier 1)

**Tier 1 proved the channel, so the Tier 2 question became live. It was decided on counts, not on impression.**

| Tier 2 cluster | Existing coverage | Verdict |
| :--- | :--- | :--- |
| **Mistakes / ordering** (`Vf3pDmkyT1k`, `NfBvQNAxRPA`, `y1XTG_FcbQo`, `Xd8ivbYOYKk`, `4ZM3-MP8D4c`, `c70WzPVSisc`) | `General_Dos_and_Donts.md` carries **13 distinct sources** in 250 lines, plus Kruglov's design-mistakes and 25-ordering-mistakes notes, CAPPUCCINO's ten tells, and now Sosnovskaya's own acceptance and ordering material | **DECLINE** |
| **Countertops** (`DEecuW1BjC8`, `i_yNNRR0-ms`) | `Worktops_and_Backsplash.md` has **37 distinct sources** — the most saturated page in the folder — plus the new fabricator account and the four-material crash test | **DECLINE** |
| **Backsplash** (`5zqdxOdEHZE`) | **17 files** in `03_Kitchen/` already touch it | **DECLINE** |
| **Sink** (`Qdtuk0nRZjw`) | **19 files** | **DECLINE** |
| **Lift mechanisms** (`p1zwa2MkufA`) | `Kitchen_Gadgets_and_Mechanisms.md` carries Aventos **HK / HF / HS**, Servo-Drive and TIP-ON in detail | **DECLINE** |
| **Named facade products** (`kjkuwK2ae_E` ALVIC, `hvkMOC1CgTM` Mattelux/PerfectSense) | Was **zero** before this round. **Tier 1 closed it at category level** — UV-lacquer panels are one construction (MDF + decor paper + UV lacquer), and **the disqualifying defect is already captured**: tea soaks through the lacquer into the paper | **DECLINE** — the finding that mattered is in |
| **ЛДСП health** (`3yZ_JFilgPc`) | **6 files** carry formaldehyde/E1 material, and this round added the спецпропитки disagreement | **DECLINE** |
| **⚠️ Drawer slide SYSTEMS** (`aN9cCdJIKWY`) | TANDEMBOX, LEGRABOX and MOVENTO appear **twice each** in `Storage_and_Hardware.md` — **mentions, not a comparison** | **THE ONLY REAL GAP** |
| **⚠️ Powder coating vs enamel** (`F9SoaAAX9Jo`) | **Literally zero** mentions of «порошковое покрытие» anywhere in `03_Kitchen/` | Uncovered, but **niche** — powder coat on MDF is unusual |

> **⚠️⚠️ AND THE PRINCIPLED REASON, WHICH MATTERS MORE THAN THE COUNTS: TIER 2 IS THE PART OF THIS CHANNEL THAT DOES NOT TEST.**
>
> **Tier 1 earned its place because this presenter runs destructive tests, revisits a nine-year-old kitchen, and ranks on a decade of returns — evidence types nothing else in the vault has.** **The mistakes and ordering videos are assertion-format listicles: the one thing this channel does that a dozen other sources already do.**
>
> **This vault's own value filter already says so**, from the Dude Blender round: *“the value filter should ask ‘does this source say how it could be WRONG’, not only ‘does it cover a new task’.”* **→ Take the part of a channel that does what no one else does; decline the part that does what everyone else does.**

> **VERDICT: TIER 2 DECLINED AS A BATCH.** ⚠️ **Two items remain individually defensible and neither justifies a round on its own** — `aN9cCdJIKWY` (drawer slide systems, the only genuine gap) and `F9SoaAAX9Jo` (powder coating, zero coverage but niche). **Fold them into some future kitchen round if one happens; do not open one for them.**

### The original Tier 2 list, retained for the record



`Vf3pDmkyT1k` (10 способов обмана при заказе) · `NfBvQNAxRPA` (ТОП 18 ошибок) · `y1XTG_FcbQo` (Колхозная кухня, 1.7M) · `Xd8ivbYOYKk` (16 ошибок при выборе фасада) · `DEecuW1BjC8` (столешницы, crash test) · `i_yNNRR0-ms` (ТОП 12 столешниц 2020) · `c70WzPVSisc` (пластик/плёнка/ЛДСП — «самый большой обман») · `3yZ_JFilgPc` (опасна ли ЛДСП для здоровья) · `aN9cCdJIKWY` + `p1zwa2MkufA` (выдвижные и подъёмные механизмы) · `5zqdxOdEHZE` (фартук, 12 идей + секреты установки) · `Qdtuk0nRZjw` (мойка: камень или нержавейка) · `kjkuwK2ae_E` (ALVIK) · `hvkMOC1CgTM` (Mattelux / PerfectSense) · `F9SoaAAX9Jo` (порошковое покрытие или эмаль)

## 7. Declined outright

- **All 44 trend/fashion videos.** Dated by construction.
- **All 21 project showcases.** ⚠️ **This is the hidden advertising** — real content shape, vendor specification as substance.
- **All 20 non-kitchen** (wardrobes, closets, bathroom, hallway, children's room, one house build). ⚠️ **Wardrobes are deferred rather than refused** — `14_Furniture/` exists and there are ~10 of them, but the owner's steer is kitchen.
- **The ~10 small-kitchen-layout videos beyond one**, and **the remaining ~25 facade overviews**, as internally duplicative.
- ⚠️ **Every price figure on the channel.** RUB, 2019–2025, Russian market. **Rule 2: no comparable market.** Only structure transfers — what a погонный метр contains, what drives the 10× spread, what separates a cheap carcass from an expensive one.

---

## ⚠️⚠️ 5b. SPOT-CHECK RESULT — both passed, and the risky one passed hardest

**Two fetched 2026-09-14 (`ru`, serialized, `--fetch-upload-date`), exactly the pair §8 said to check. Read in full. Neither is a factory tour.**

**`Lfvs1XUz53s` — «13 секретов производства прочного корпуса» (25:39, uploaded 2026-07-16).** The risky pick, and **the best single find of this triage.**

- **⚠️⚠️ IT RUNS A LIVE IMMERSION TEST DURING THE VIDEO** — samples dropped in an aquarium at the start, revisited at the end: **EVA-glued edge vs PUR-glued edge, plus an MDF/NTM front.** The destructive-test format is real, not a title.
- **⚠️⚠️ AND IT ATTACKS THE ASSUMPTION THE VAULT CURRENTLY CARRIES.** *«Заблуждение… что качество каркаса зависит исключительно от толщины ЛДСП и его производителя»* — you can take the thickest, most expensive LDSP, band it with thin melamine on EVA glue, **and the edge falls off, the carcass swells, and the hardware pulls out of what is now труха.** → **The CAPPUCCINO round recorded 16-vs-18 mm board as the thing to check. This says the BOARD is the wrong variable and the EDGE TECHNOLOGY is the right one.** **A genuine disagreement between two fabricators, and it is testable.**
- **⚠️⚠️ A CHECKABLE PRE-ORDER ARTEFACT: the ДЕТАЛИРОВКА.** A professional must hand you a printed carcass specification — every part, the fastener schedule (евровинт, эксцентрик, glued joints) and the hardware list. *«Если такого листочка ты не увидел перед заказом… либо ты купил модульную кухню, либо тебе будет её пилить гаражник».* → **A document you can demand BEFORE paying, and the vault has nothing equivalent for furniture.**
- ⚠️ **Promotional content is present and identifiable**: the edge-banding machine is *«сейчас в продаже»* — **he sells equipment as well as kitchens**, which is a second commercial interest to declare. The opening *«90% кухонь России уже полный хлам»* is an unsourced market claim.

**`A9Kef6CvNZ4` — «Моя первая КУХНЯ. 9 лет эксплуатации» (10:37, uploaded 2020-03-27 — so the kitchen dates to ~2011).**

- **It is BOTH the longitudinal record hoped for AND a post-installation acceptance checklist**, delivered by walking a 9-year-old kitchen. **The acceptance half is the larger half**, and it complements CAPPUCCINO's delivery-day list rather than repeating it — **that one is what arrives on a lorry, this one is what to check after the fitters leave.**
- **⚠️⚠️ A VISUAL GEOMETRIC GATE: «крест на фасаде»** — where four fronts meet, the joint must read as a true cross, checked with horizontals and verticals independently. **CAPPUCCINO said “carcass diagonals do not match”; this gives the one-glance test for it.**
- **⚠️⚠️ HARDWARE AUTHENTICATION, MORE SPECIFIC THAN WHAT THE VAULT HOLDS.** CAPPUCCINO said Blum carries a factory engraving. **This adds: hinges are marked INSIDE THE CUP (в чашечке)** — here Hettich — **and lift mechanisms carry branded caps.** → **Where to actually look.**
- **⚠️⚠️ THE FAILURE POINT AFTER 9 YEARS IS NOT WHERE EXPECTED.** Not under the sink (dry, PUR-glued carcass intact) but **the еврозапил — the countertop mitre joint**, showing slight вспучивание. **Real observed degradation with a location and a timescale.**
- **Further checkable items**: a ЛДСП plinth **must** have a silicone seal underneath (an aluminium or plastic one need not); a **термошов plus a metal strip is mandatory above a dishwasher**; **a factory countertop is marked with its producer on the underside** (a provenance check anyone can do); and on a plastic front the tell is the **«строчка»** — a visible seam at the banded edge, which is both a moisture and an aesthetic defect.
- ⚠️ **It is their own kitchen and carries two Instagram plugs.** `promotional_ratio: medium`.

> **⚠️⚠️ VERDICT: PROCESS TIER 1.** Both spot-checks cleared the bar, the destructive-test and longitudinal formats are real, **and the channel already contradicts an existing vault finding on its first contact** — which is the strongest possible argument that it is not a restatement.
>
> ⚠️ **ONE CAVEAT THAT WILL COST TIME: the ASR is noticeably worse than this vault's norm.** Proper nouns are mangled (*Senosan* → «seen as an», *disposer* → «dice poser», торцов → «как усов») and some numerals are unreliable. **Every brand name and every figure needs re-derivation from context, and anything that cannot be re-derived must be dropped rather than guessed.**

## 8. Open risks to check on the first fetch

- **⚠️ `promotional_ratio` is unknown and the format makes it hard to read from a title.** A 25-minute "13 secrets of carcass production" from a factory is *either* the best process source in the vault *or* a factory tour. **Spot-check #4 and #2 before committing to the rest of Tier 1.**
- **⚠️ Nine years of video means the early material claims may be superseded by the later ones**, by the same presenter. **Where two videos disagree, the later one is not automatically right — record both and say which is which**, the way this vault handles a Perspective.
- **⚠️ Serialize the fetches**, 90 s spacing, exit-code-2 circuit breaker (rule 7). **Pass `--upload-date` on every fetch** — the dates are in the manifest already, so it costs nothing.
