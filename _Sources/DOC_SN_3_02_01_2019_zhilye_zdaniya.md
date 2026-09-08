---
source_type: primary building norm (Строительные нормы Республики Беларусь), preview PDF
source_title: "СН 3.02.01-2019 «Жилые здания» / «Жылыя будынкі» — Строительные нормы Республики Беларусь"
issuer: Министерство архитектуры и строительства Республики Беларусь; developed by РУП «Стройтехнорм»
source_url: https://mapid.by/assets/files/sn-3.02.01-2019.pdf
evidence_file: _Archive/processed_sources/20260908_SN_3.02.01-2019_zhilye_zdaniya_normy_by_preview.pdf
fetched: 2026-09-08
pages: 25
language: ru
region: Belarus_LEVEL1_primary_norm
fact_yield: 9
promotional_ratio: n/a
corroborates_existing: false
---

# Source Note — СН 3.02.01-2019 «Жилые здания» (clause 4.9 and the minimum room dimensions)

**Fetched to verify a quotation in the Gemini Deep Research report** — and the verification
mattered: **the report got the designation, the clause number and the content of the
exception wrong, and omitted the two most useful parts.**

## ⚠️ Provenance caveats, stated first

- **This is a preview copy** watermarked **«Для ознакомления www.normy.by»**. The cover reads **«СН 3.02.01-2019 … Издание официальное … Минск 2020»** — so the norm's designation year is **2019** and its publication year is **2020**, which is the most likely origin of the report's "СН 3.02.01-2020".
- **⚠️ Amendments exist.** A secondary listing (`enp.by`) advertises the norm as a **«ПЕРЕИЗДАНИЕ с Изменениями №1 и №2»**. **The copy read here does not include them, so every figure below must be re-checked against the current consolidated text before it is relied on for a submission.**
- **The norm governs the DESIGN of residential buildings** (§4.1). Its bite on a renovation is indirect, via **№ 164 §4**, which prohibits переустройство/перепланировка «с нарушением строительных… требований». **That is the mechanism; the norm does not address перепланировка itself.**

## ⚠️⚠️ Clause 4.9 — verbatim

> **«4.9 Не допускается размещать санитарные узлы непосредственно над жилыми комнатами и кухнями. Размещение санитарного узла над кухней допускается в многоуровневых квартирах в случае, когда санитарный узел и кухня входят в состав одной квартиры.**
>
> **Частичное размещение одного из помещений санитарного узла (не более 25 % его площади) над жилой комнатой разрешается, если выполнены мероприятия по повышению гидро- и звукоизоляции конструкции пола этого санитарного узла.**
>
> **Размеры в плане ванной комнаты (с учетом отделки) должны быть не менее 1,5×1,7 м, совмещенного санитарного узла — 1,5×2,5 м и должны обеспечивать размещение в них ванны длиной не менее 1,7 м. Размеры в плане туалета без умывальника должны быть не менее 0,8×1,5 м, с умывальником — 1,4×1,5 м»**

### What the norm actually says

| | |
| :--- | :--- |
| **The prohibition** | Sanitary units may **not** sit **directly over living rooms or kitchens** |
| **The only exception** | **Multi-level flats**, over a **kitchen**, **and only where the sanitary unit and that kitchen are in the same flat** |
| **⚠️ The 25 % allowance** | **Partial placement of ONE of the sanitary unit's rooms — not more than 25 % of its area — over a living room IS permitted, if enhanced waterproofing and sound insulation of that unit's floor construction are carried out** |
| **Minimum plan dimensions, «с учётом отделки»** | **ванная комната ≥ 1.5 × 1.7 m** · **совмещённый санузел ≥ 1.5 × 2.5 m** · both must accommodate **a bath ≥ 1.7 m long** · **туалет without washbasin ≥ 0.8 × 1.5 m** · **туалет with washbasin ≥ 1.4 × 1.5 m** |

## ⚠️⚠️ Four corrections to the Gemini report

| Report claim | Actual |
| :--- | :--- |
| «СН 3.02.01-**2020**» | **СН 3.02.01-2019** (published 2020) |
| «Clause **4.11**» | **Clause 4.9** |
| Exception applies «**на верхнем этаже**, а также в двухуровневых квартирах» | **No top-floor exception exists for sanitary units.** Only **multi-level flats, over a kitchen, same flat.** ⚠️ **The report appears to have conflated 4.9 with 4.8**, which does contain a top-floor allowance — but 4.8 is about **a living room over or under a GAS-STOVE kitchen**, a different rule |
| Its quoted text | **Omits the 25 % partial-placement allowance and the minimum dimensions entirely** — the two most useful provisions in the clause |

**And its practical framing was wrong in the other direction too.** It said expansion is permissible «only at the expense of corridors, entrance halls, pantries or vestibules». **The norm's own text is narrower and more generous at once**: the bar is *over living rooms and kitchens of the flat below*, and **up to 25 % of one sanitary room may cross that line** with enhanced insulation.

## ⚠️⚠️ Directly binding on this project

This flat: **ванная 3.09 m²**, **туалет 1.24 m²**, floor **4 of 21** (so no multi-level or top-floor exception is available).

- **ванная**: the minimum is **1.5 × 1.7 m = 2.55 m²**. At 3.09 m² the area passes, **but both plan dimensions must be met after finishes** — so **the 1.5 m minimum width is the figure to check against the model**, not the area. See [[00_Master/Geometry_Variance_Study|Geometry Variance Study]]; and note tile build-up eats into it, since the norm says «с учётом отделки».
- **⚠️ туалет**: the minimum **without** a washbasin is **0.8 × 1.5 m = 1.20 m²** — the 1.24 m² room clears that only just, and again only if both dimensions hold. **With a washbasin the minimum is 1.4 × 1.5 m = 2.10 m², which a 1.24 m² room cannot achieve.**
  > **→ A washbasin in the separate туалет is not compliant at this room's size.** A concrete, checkable constraint the vault did not have, and it settles a design question rather than raising one.
- **The 25 % allowance is a real planning lever** if any wet-room enlargement is ever considered — but it is conditional on enhanced floor waterproofing **and** sound insulation, both of which are «устройство гидро-, паро-, звукоизоляции» and therefore **works requiring согласование in their own right** under № 164 §3.

## Other clauses noted in passing

- **4.7** — kitchen, combined-sanitary-unit, WC and bathroom doors must carry **ventilation grilles or similar of at least 0.02 m²**, positioned so their bottom is **no more than 0.03 m above floor level.** ⚠️ Directly relevant to door selection and to the vault's ventilation pages.
- **4.8** — a living room over or under a **gas-stove** kitchen is allowed only in single-family and blocked houses, or on the **top floor (mansard) of multi-apartment buildings with multi-level flats**, where kitchen and room are in the same flat.
- **3.33** — definition: a **санитарный узел** is the sanitary-hygienic room(s) in a flat containing bath or shower, washbasin, WC (possibly bidet) **and washing machine**. ⚠️ **The washing machine is part of the definition**, which matters for how the room is assessed.
- **3.44** — **квартира-студия** is defined as ≤ 50 m² total with a mandatory WC, bathroom or combined unit, **no partition between kitchen and living room**, and functional zoning by furniture placement.

## Uncertainties

| Item | State |
| :--- | :--- |
| ⚠️ **Amendments №1 and №2** | **Not in the copy read.** Every figure above needs re-checking against the consolidated current text |
| Preview watermark | «Для ознакомления» — not the official distribution copy |
| Whether 4.9's dimensions bind a перепланировка of an existing flat, or only new design | **The norm is a design norm (§4.1).** It binds here through № 164 §4's prohibition on breaching строительные требования — **an indirect route that should be confirmed with the исполком** |
| Whether «размеры в плане» means clear internal dimensions | Text says «с учётом отделки», which implies **finished clear dimensions** — but the norm does not define the measurement convention |
