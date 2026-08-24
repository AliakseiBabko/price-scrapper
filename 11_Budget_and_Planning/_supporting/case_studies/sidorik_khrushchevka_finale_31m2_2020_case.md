# Case Study — Pavel Sidorik's Own Khrushchevka Remake, Finale (2020)

**Source**: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_0sJPlpi8I2U_sidorik_khrushchevka_finale_cost|full extraction note]] — "Переделка хрущевки от А до Я" (finale episode), Pavel Sidorik, YouTube, published 2020-08-07.

## Why this case study exists

Per this project's broadened case-study definition (coherence over "one
single verified real project" as a hard gate): this is a real, complete,
self-executed renovation — 37 episodes covering the entire project,
summarized here with a real final smeta total — documented first-person
by the person who actually did the work. It is the **first self-managed
case in this store with both (a) level-1, directly-spoken Belarus
confirmation and (b) a confirmed m² denominator letting a $/m² figure be
computed** — the existing self-managed references
([[11_Budget_and_Planning/_supporting/case_studies/yana_vrublevskaya_minsk_mir_studio_2023_case|Yana Vrublevskaya Studio Case]],
[[11_Budget_and_Planning/_supporting/case_studies/price_table_screenshot_case|Price Table Screenshot Case]])
each lack one of these two properties.

## 1. Project Basics

- **Region**: Belarus — **level 1**, spoken directly ("это
  среднестатистическая стоимость ремонта для Беларуси," "this is the
  average renovation cost for Belarus"), with Russia/Ukraine/Kazakhstan
  named as roughly comparable markets specifically for *material* cost
  (not labor cost, which the speaker says varies by region/country).
- **Unit type**: one-room "khrushchevka," 31.2 m², 5th floor of a
  1964-built building, sloped ceiling under the roof (280–320 cm).
- **Date**: 2020 (confirmed via `yt-dlp` upload date, 2020-08-07) — an
  older source in this store; treat pricing as historical, do not blend
  with 2024+ figures without inflation adjustment.
- **Delivery model**: **Self-Managed, DIY** — the speaker (a professional
  finisher) executed the entire renovation himself, in his own spare
  time, over roughly one year. The "labor" figure below represents his
  own valuation of his own labor/time across the project, not a
  third-party contractor invoice — a meaningfully different labor-cost
  structure than either the turnkey or hired-crew self-managed cases
  elsewhere in this store.
- **Currency**: USD, stated directly by the speaker as the primary
  figure. A secondary Russian-ruble (not Belarusian ruble) conversion is
  also given — see the Currency Note below.

## 2. Total Cost — the headline numbers

| Category | Amount (USD, stated) |
| :--- | ---: |
| Labor (speaker's own time, accumulated across 37 episodes) | $6,168 |
| Materials | $9,193 |
| **Sum** | **$15,361** |
| Speaker's own stated total, with an explicit "~$300 more, uncounted minor items" caveat | **≈$15,500–15,800** |

**Derived $/m² (this project's own calculation, not stated by the
source)**: $15,361 ÷ 31.2 m² ≈ **$492/m²** (before the "~$300 more"
caveat); **≈$502–507/m²** if that caveat is folded in. Given this
project's own standing rule that a bare $/m² figure needs both location
and year to be comparable — both are resolved here (Belarus, level 1;
2020, metadata-confirmed) — this is one of the stronger $/m² data points
in this store on that specific dimension, even though the total dollar
amount itself is modest (a small 31.2 m² unit).

## 3. Currency Note — RUB figure is a same-source illustrative conversion, not a second payment currency

The speaker also states the totals in **Russian** rubles (not Belarusian
rubles/BYN, despite this being a Belarus-located, Belarus-confirmed
project): $9,193 → 661,896 RUB, and $6,168 → an ASR-garbled digit string
most plausibly ≈440,000 RUB. A sanity check via
`tools/pricing/currency_converter.py --pair USD/RUB --trailing-months 6
--before 2020-08-07` resolves to **71.16 RUB/USD**, giving $9,193 ≈
654,000 RUB (within ~1.2% of the stated 661,896) and $6,168 ≈ 439,000 RUB
(within ~0.2% of the most plausible reading of the garbled figure) —
confirming the RUB figures are a real, roughly-accurate same-source
conversion, not a different underlying payment amount. **Treat the USD
figures as authoritative**; the RUB figures are presented here only
because the source itself gave them, not because the project was
transacted in RUB.

## 4. Comparison to This Store's Existing Self-Managed References

| | This case (Sidorik, 2020) | Yana Vrublevskaya (2023) | 44 m² Minsk смета (labor-only, 2025) |
| :--- | :--- | :--- | :--- |
| Scope | Full project: own labor + materials, complete finished apartment | Rough works + full finish/fixture/appliance/furniture | Labor-only rate card, per work item |
| Region confidence | **Level 1** (spoken: "for Belarus") | Level 2 only (title/tags/metadata) | Level 1 ("по Минску," spoken) |
| m² known? | **Yes, 31.2 m² — $/m² computable** | No (tag-inconsistent, not stated) | Yes, 44 m² |
| Labor cost basis | Speaker's own DIY time valuation | Hired individual specialists per trade | Generic market rate per work item |
| Real vs. generic | Real, single documented project | Real, single documented project | Real, single documented project |

**Not averaged or combined into one figure** — different labor-cost
bases (self-valued DIY time vs. hired-specialist market rates vs. a
generic rate card) make a direct average misleading even where region and
year line up reasonably well. Kept as three separate, clearly-labeled
self-managed reference points. This case's DIY labor-cost basis in
particular means its $492–507/m² figure likely **understates** what a
comparable hired-labor self-managed project would cost, since the
speaker's own time isn't priced at a market labor rate — a caveat worth
carrying forward wherever this figure is cited.
