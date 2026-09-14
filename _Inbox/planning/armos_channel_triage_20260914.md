# Channel triage — @ARMOS-MARKET (ARMOS, mattress & furniture manufacturer, Vichuga/Ivanovo)

**Date:** 2026-09-14 · **Owner-supplied** · **248 videos** · **Status: triaged; 2 spot-checked and read; Tier 1 proposed, not yet processed**

**Owner's steer:** *mattresses, pillows, beds, and bedroom dos and don'ts.*

---

## ⚠️⚠️ 1. This is the first genuinely UNCOVERED domain a channel has hit

**A grep before triaging, across `_Sources/`, `14_Furniture/` and every room folder:**

| Term | Files in the vault |
| :--- | ---: |
| **`независимые пружины` / `боннель` / `пружинный блок`** | **0** |
| **`латекс` / `кокосовая койра` / `memory foam` / `пенополиуретан`** | **0** |
| **`наматрасник` / `топпер`** | **0** |
| `матрас` | **1** |
| `ортопедический` / `анатомический` | 2 |
| `подушка` | 4 |
| `кровать` | 23 |
| `спальня` | 31 |

> **⚠️⚠️ THE VAULT HAS A `06_Small_Bedroom/` FOLDER AND ESSENTIALLY NOTHING ON WHAT GOES IN IT.** Bed and bedroom coverage is layout and design; **the sleeping surface itself — the single most-used object in the flat — is absent.** **This is the opposite of the last two channels, where every topic was saturated.**

**Language check (now routine, and it paid off again): the default-locale manifest returns titles PARTLY translated** — `GUugqt3EvGI` came back as *"Learn to SLEEP FAST!"* while its neighbours stayed Russian. **Captions on the flagship: `ru-orig` present.** **→ `--languages ru` and a `lang=ru` manifest are both required.**

**Dedup: 0 of 248 already processed.**

---

## ⚠️⚠️ 2. The channel is 77% catalogue advertising, and the filter is trivial

| Category | Count | Verdict |
| :--- | ---: | :--- |
| **ARMOS-branded product and factory videos** — individual bed models (ЭМИЛИЯ, Siena, HELEN, Montana…), individual mattress models (Адель, Роксана, Ника, Агат…), "технология HoneyComb / 3D Air System / Steel Edge / HL zone", factory tours, the franchise pitch | **~190** | **DECLINE.** ⚠️ **Below roughly row 55 by views the channel is almost pure catalogue**, 1–3 minutes each, a few hundred views |
| **Sleep-wellness / health** — yoga before bed, insomnia cures, *«как выспаться всего за 4 часа»*, *«в этих позах спать опасно»*, pyjama yoga | **~22** | **⚠️⚠️ DECLINE, AND FIRMLY.** **Health claims from a mattress seller, with no named clinician in the titles.** *«Выспаться за 4 часа»* is the shape of a claim that is wrong and confident. **Out of scope and out of competence** |
| **Sofas** (top-5 for daily sleeping, cheap vs dear, choosing errors) | **~46** | **DEFER.** ⚠️ **The owner asked for mattresses, pillows, beds and bedroom** — a sofa-bed is adjacent and `04_Living_and_Dining_Room/` exists, but it is not the brief |
| **Mattresses, pillows, toppers, bases, bedroom dos/don'ts** | **~35 distinct** | **THE BRIEF.** Tier 1 below |

---

## ⚠️⚠️ 3. Spot-check — both passed, and one is better than its title

**Two fetched 2026-09-14 (`ru`, serialized, `--fetch-upload-date`), chosen to test the evidence type and the flagship.**

**`83N581Eu3BY` — «Разобрали матрас. Что внутри матраса с независимыми пружинами?»** (3:27, 2023-01-12)

**The structural model, which is the thing the vault most needs and has nowhere:**

- **A mattress is THREE cost-and-quality determinants: the cover (чехол), the comfort layers (настилочные слои), and the spring unit (пружинный блок).**
- **⚠️⚠️ THE SPRING UNIT CANNOT DO THE FINE WORK, AND HE SAYS WHY:** *«Сколько бы ни было пружин на квадратный метр, всё равно каждая из них ДИСКРЕТНА — они не обеспечивают плавной подстройки, высокой точечной эластичности.»* **The springs do coarse adjustment to body contours; the comfort layers do the fine adjustment and distribute load down into the springs.**
- **⚠️ A good cover is itself *«своеобразный маленький тонкий матрасик»*** — quilted onto soft foam, and its stated job is that **soft tissue is not compressed and microcirculation is not disturbed, so you turn over less during the night.**
- ⚠️ **It dissects LESS than the title promises** — an explanation over a cutaway rather than a teardown with findings — **and it closes on a discount promo code.**

**`ReYeU-jEINY` — «Как выбрать идеальный матрас? 8 советов эксперта»** (8:37, 2022-01-11, **374k views, the channel's flagship**)

**Substantive, and several items are checkable and vendor-independent:**

- **⚠️⚠️ MEASURE THE BED'S INTERNAL OPENING, AND ROUND DOWN.** Measure 162 cm → buy a **160 cm** mattress. The gap is needed to tuck bedding, fit a protector, and — **on a bed with a lift mechanism — to stop the mattress catching the sides.** Same for length: 202 → 200.
- **⚠️⚠️ OPTIMAL COMBINED BED + MATTRESS HEIGHT = THE BEND OF YOUR KNEE, ± a palm's width.** **A low bed with a low mattress is hard for older people to get out of.** ⚠️ **And a decorative headboard element caps mattress height** — measure from the base to its lower edge.
- **⚠️⚠️ LAMELLA SPACING MUST NOT EXCEED 8 cm**, on a base that is firm, flat and free of protruding or sharp elements.
- **⚠️⚠️ FIRMNESS IS SUBJECTIVE AND THERE IS NO STANDARD.** *«Нет никаких единых норм, правил и стандартов… матрас средней жёсткости одного производителя будет вам казаться мягким, а жёсткий другого — средней жёсткости.»* **→ Firmness labels are NOT comparable between makers. That is a cross-vendor warning from a vendor, and it is the single most useful sentence in the video.**
- **⚠️⚠️ THE IN-STORE TEST, with a duration**: lie in your usual sleeping position for **10 minutes**. *«Если глазки стали закрываться, если не появилось желания перевернуться, не появилось болевых ощущений — это ваш матрас.»* **If discomfort appears in the shop it will be the same at home.**
- **⚠️ "Do not chase the number of springs"** — what matters is the pocket material and its wear, how the springs are joined (by hand or machine), and the wire. ⚠️ **He then says ARMOS makes its own spring blocks, which is where the argument turns into a pitch.**
- **Firmness heuristics**: middle-aged and back sleepers → medium; young and stomach sleepers → firmer; older people and side sleepers → soft or memory foam; heavy build → firm.
- **Load capacity per sleeping place** depends on construction, spring type and **wire thickness**; choose with a margin if above average weight.

> **⚠️⚠️ VERDICT: PROCESS TIER 1.** **The domain is nearly empty in this vault, the two spot-checks both carry checkable mechanisms, and several of the strongest claims work AGAINST an easy upsell** — do not chase spring count, firmness labels are not comparable, go and lie on it for ten minutes.
>
> ⚠️ **The bias to carry throughout: this is a MANUFACTURER. Every "how to choose" is an argument for a construction they sell, and both spot-checks end in a site link, a salon visit or a promo code.** **`promotional_ratio: medium_to_high` across the technical videos.**

---

## 4. Proposed Tier 1 — 10 videos, ~50 min

| # | ID | Min | Title | Why |
| :-- | :-- | :-- | :--- | :--- |
| 1 | `ReYeU-jEINY` | 8:37 | Как выбрать идеальный матрас? 8 советов | **Already read.** The flagship and the spine of the topic |
| 2 | `83N581Eu3BY` | 3:27 | Разобрали матрас. Что внутри | **Already read.** The three-part structural model |
| 3 | `mNRiCwPNBNA` | 5:00 | Пружинный или беспружинный? | **The primary fork, and zero vault coverage** |
| 4 | `Wf8DKZiIJEQ` | 6:52 | Как выбрать беспружинный. Состав. Латекс | **Materials — latex, coir, foam — all at zero** |
| 5 | `k2DeXNYNwYk` | 4:38 | Сколько пружин должно быть? Разбираем на пружины | **Tests the "more springs is better" claim they themselves reject** |
| 6 | `Lgi46kpCQ3A` | 3:41 | Сравнили дешёвый и дорогой матрас | **A comparison, not an assertion** |
| 7 | `I3Fyh_mWiyQ` | 6:26 | Как подобрать подушку. Советы ОСТЕОПАТА | **185k, and the advice is attributed to a third-party clinician rather than the seller** |
| 8 | `LtVT9TxHdtM` | 5:03 | Что такое топпер | **136k. Toppers are at ZERO files** |
| 9 | `O3UWHF8eCVs` | 2:59 | Правильное основание под матрас. Ламели и доски | **The 8 cm rule in full, and a base can be built rather than bought** |
| 10 | `ZLPknlB-3XI` | 4:31 | Ваша идеальная кровать. Лайфхаки и ОШИБКИ | **The bed half of the brief** |

**Add if Tier 1 lands well:** `6NOvooyMOOA` (матрас для пары с разницей в весе — **a specific real problem**), `Ddk2mkGIE8g` (**why a new mattress smells** — possibly an emission/health item, cf. the ЛДСП formaldehyde finding), `Y8J4GZkdApo` + `eJlOn5DhxxQ` (bedroom anti-trends and the main interior mistake — **the dos-and-don'ts the owner asked for**), `ImSFRdmNMFI` (orthopaedic pillow / memory foam), `G_ep--_GrB4` (mattress on the floor), `CnPrbUgTa7s` (**bed for a small bedroom — `06_Small_Bedroom/` is a live folder**), `eCxYOIIDd-A` (3 myths about orthopaedic mattresses), `WzPN61NdTNg` (waterproof protector), `bm5BJ8XI_is` (mattress height), `HNm4dwN4u7g` (in-shop selection errors).

## 5. Declined outright

- **~190 catalogue and factory videos.** ⚠️ **This is the advertising, and unlike the last vendor channel it is not disguised** — individual product names in the titles make it a one-line filter.
- **⚠️⚠️ All ~22 sleep-wellness/health videos.** **A mattress seller on insomnia, sleeping positions and how to be rested on four hours' sleep is outside both scope and competence, and this vault has no way to check it.**
- **~46 sofa videos** — deferred as adjacent, not refused.
- **Model-ranking videos** (`CkxBzWFBylY` "Топ-7 матрасов, рейтинг 2022", `WmTvwcbqxfo` "Топ 5 подушек", `gUY1BE4b_eA` "ТОП-5 кроватей с подъёмным механизмом", `u7lcc46MV48`, `fuUgPZHFKfc`) — **⚠️ a manufacturer ranking mattresses is a catalogue with an ordinal on it.** **Declined unless a Tier 1 video shows the rankings carry reasoning.**
- ⚠️ **Every price on the channel.** RUB, Russia, 2022–2023. **Rule 2. Only ratios and structural relationships can transfer.**

## 6. Risks to carry into processing

- **⚠️⚠️ A manufacturer explaining what makes a good mattress will describe its own construction.** **Keep the mechanism, drop the verdict** — the same discipline applied to the Сосновская facade ranking.
- **⚠️ No test, no measurement so far.** Neither spot-check measured anything; the "dissection" is a cutaway explanation. **If nothing in Tier 1 shows rather than asserts, this channel is one voice on a topic with no second voice in the vault** — which is a real weakness, since **there is no existing coverage to cross-check against.**
- **⚠️⚠️ AND THAT IS THE SHARPEST RISK HERE: on the last two channels the vault could check a claim against 14 existing files. On this one it cannot.** **→ A second, independent mattress source should be sought before any of this becomes a purchasing decision.**
