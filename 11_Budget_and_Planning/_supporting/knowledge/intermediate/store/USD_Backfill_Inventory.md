# Workstream D USD-backfill inventory

## Widened §6 scope ledger

The stable ledger is grouped by the plan's reference-layer scope, so
aggregate counts cannot be mistaken for complete coverage. Each future price
unit or split claim gets one stable row with a scope group, source-file
anchor, parent ID when split, raw original text, and terminal status.

| Scope group | Required source set | Ledger status | Next action |
| :--- | :--- | :--- | :--- |
| `processed_sources_csv` | `00_Master/processed_sources.csv` price-bearing rows | pending | Inventory source URL, source year, and raw price-bearing field. |
| `numeric_data` | `Numeric_Data.md` | active | Continue unresolved price-bearing entries; `D-ND-060`–`D-ND-064` are tracked. |
| `cross_source` | `Cross_Source_Comparison_Tables.md` | partial | Inventory remaining table cells and split ranges. |
| `guide` | The ten price-bearing guide pages named in plan §6 | pending | Inventory guide-level price claims after Numeric/Cross-Source. |
| `detail` | Each scoped guide's own analysis/detail pages | pending | Inventory price-bearing claims, excluding raw extraction notes. |

The five current Numeric Data rows are not a completion claim for the 338-line
inventory; they are the first widened slice after the prior ten-row ledger.

Current widened Numeric Data rows:

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-ND-063` | `numeric_data` | `Numeric_Data.md` | Real inspection-fee data point, source year 2019 | — | resolved | Appended ≈$150 for ≈10,000 RUB and ≈$3,100+ for ≈200,000 RUB+ at the confirmed 2019 USD/RUB annual average of 64.7. Corrected 2026-08-21 - the originally-merged previously merged figure was an arithmetic error. |
| `D-ND-064` | `numeric_data` | `Numeric_Data.md` | Real emergency-repair steel-strip cost, source year 2023 | — | resolved | Appended ≈$27 for ≈2,300 RUB at the confirmed 2023 USD/RUB annual average of 84.7. |

Stable slice identifiers for the scoped reference-layer price inventory. A
slice ID remains stable if a line is split or later reclassified; status records
the disposition rather than relying only on a changing aggregate count.

## Current Cross-Source 2026/2025 tier slice

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CS-078` | `cross_source` | `Cross_Source_Comparison_Tables.md` | BURO Luxury tier, source year 2026 | — | resolved-uncomputable | Original 1,000,000+ RUB/m² retained; no USD equivalent because 2026 has no complete historical annual rate. |
| `D-CS-079` | `cross_source` | `Cross_Source_Comparison_Tables.md` | BURO Premium tier, source year 2026 | — | resolved-uncomputable | Original 450,000–1,000,000 RUB/m² retained; no USD equivalent because 2026 has no complete historical annual rate. |
| `D-CS-080` | `cross_source` | `Cross_Source_Comparison_Tables.md` | BURO Mid tier, source year 2026 | — | resolved-uncomputable | Original 200,000–450,000 RUB/m² retained; no USD equivalent because 2026 has no complete historical annual rate. |
| `D-CS-081` | `cross_source` | `Cross_Source_Comparison_Tables.md` | Бородатый Прораб full-realization figure, source year 2025 | — | resolved | Appended ≈$1,800+/m² for 150,000+ RUB/m² at the confirmed 2025 USD/RUB annual average of 83.21. |

## Current processed_sources.csv slice

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CSV-001` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260727_10`, Minsk World 2025 benchmark | — | resolved | Original USD figures retained; annotation records USD equivalent as same as original. |
| `D-CSV-002` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260727_12`, unknown-year RUB pricing | — | resolved-uncomputable | Original RUB pricing retained; explicit no-equivalent note because source year is unknown. |
| `D-CSV-003` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260727_13`, Minsk 2025 benchmark | — | resolved | Original USD figures retained; annotation records USD equivalent as same as original. |
| `D-CSV-004` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260730_1`, WITALT 2025 RUB tiers | — | resolved | Appended ≈$1,200–$1,400/m² and ≈$240–$960/m² at 83.21 RUB/USD. |
| `D-CSV-005` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260730_2`, 7komnat.by 2026 USD benchmark | — | resolved | Original USD figures retained; annotation records USD equivalent as same as original. |
| `D-CSV-006` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260730_3`, Prolife Invest 2026 RUB tier | — | resolved-uncomputable | Original RUB pricing retained; explicit no-equivalent note because 2026 has no complete historical annual rate. |

## Current processed_sources.csv slice 2

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CSV-007` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260731_3`, Komanda Masterov 2024 USD framework | — | resolved | Original USD range retained; annotation records USD equivalent as same as original. |
| `D-CSV-008` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260731_5`, Бородатый Прораб 2025 full-realization figure | — | resolved | Appended ≈$1,800/m²+ for 150,000 RUB/m²+ at 83.21 RUB/USD. |
| `D-CSV-009` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260731_7`, Yana Vrublevskaya 2023 BYN discrepancy | — | resolved | Appended ≈$190 for 585 BYN at 3.0091 BYN/USD; stated $10,000 target remains same-as-original USD. |

## Current processed_sources.csv slice 3

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CSV-010` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260814_3`, food-waste-disposer 2022 price | — | resolved | Appended ≈$440 for 30,000 RUB at 67.5 RUB/USD; preserved the source's separate approximate $500 wording. |
| `D-CSV-011` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260814_4`, built-in-refrigerator 2022 labor tiers | — | resolved | Appended 2022 equivalents for comfort 25,000–45,000 RUB/m² and ~32,000 actual, plus business 50,000–85,000 RUB/m². |

## Current processed_sources.csv slice 4

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CSV-012` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260815_17`, Zemstandart design fee 2024 | — | resolved | Appended ≈$40/m² for 4,000 RUB/m² at 92.66 RUB/USD (corrected 2026-08-21 - previously $50, an arithmetic error). |
| `D-CSV-013` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260815_18`, restated Zemstandart design fee 2024 | — | resolved | Appended ≈$40/m² for 4,000 RUB/m² at 92.66 RUB/USD (corrected 2026-08-21 - previously $50, an arithmetic error); restatement is explicitly not treated as independent corroboration. |

## Current Cross-Source audited slice

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CS-075` | `cross_source` | `Cross_Source_Comparison_Tables.md` | Zemstandart bespoke design-tier average, source year 2023 | — | resolved | Appended ≈$3,900 for 331,000 RUB at the confirmed 2023 USD/RUB annual average of 84.7. |
| `D-CS-076` | `cross_source` | `Cross_Source_Comparison_Tables.md` | Бородатый Прораб tile installation, source year 2025 | — | resolved | Appended ≈$50/m² for 4,000 RUB/m² and ≈$100/m² for 8,000 RUB/m² at the confirmed 2025 USD/RUB annual average of 83.21. |
| `D-CS-077` | `cross_source` | `Cross_Source_Comparison_Tables.md` | РемонтХочу tile installation, source year 2024 | — | resolved | Appended ≈$70/m² for 6,500 RUB/m² at the confirmed 2024 USD/RUB annual average of 92.66. |

## Turn 76 — Numeric Data and Cross-Source slice

| Slice ID | File | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-ND-057` | `Numeric_Data.md` | Zemstandart design-project fee, 2022 → 2026 website pair | resolved-partial | 2022 3,000 RUB/m² converted at 67.5; 2026 5,000 RUB/m² explicitly not computable from incomplete annual row |
| `D-ND-058` | `Numeric_Data.md` | Zemstandart company website current 2026 prices | resolved-uncomputable | 2026 prices and 5,000 RUB deposit retained; no historical annual USD/RUB equivalent exists |
| `D-ND-059` | `Numeric_Data.md` | Zemstandart 2022-12-20 fee transition | resolved | 2022 3,000 RUB/m² and effective-2023 4,000 RUB/m² converted with their respective annual rows |
| `D-CS-059` | `Cross_Source_Comparison_Tables.md` | WITALT full project budget tier | resolved | 2025 100,000–120,000 RUB/m² converted |
| `D-CS-068` | `Cross_Source_Comparison_Tables.md` | WITALT brigade tiers | resolved | 2025 20,000–80,000 RUB/m² converted |
| `D-CS-069` | `Cross_Source_Comparison_Tables.md` | Prolife Invest brigade | resolved-uncomputable | 2026 figures retained; incomplete 2026 annual row prevents normalization |
| `D-CS-070` | `Cross_Source_Comparison_Tables.md` | Бородатый Прораб labor rate | resolved | 2025 ≈60,000 RUB/m² converted |
| `D-CS-072` | `Cross_Source_Comparison_Tables.md` | РемонтХочу stages 2–11 | resolved | 2024 ≈48,375 RUB/m² converted |
| `D-CS-073` | `Cross_Source_Comparison_Tables.md` | Zemstandart comfort-class band | resolved | 2022 25,000–45,000 RUB/m² and ≈32,000 RUB/m² converted |
| `D-CS-074` | `Cross_Source_Comparison_Tables.md` | Zemstandart business-class band | resolved | 2022 50,000–85,000 RUB/m² converted |

This slice adds 10 inventory IDs to the tracked ledger. The broader plan
inventory remains open; these IDs must not be counted again in a later batch.

## Turn 82 — Numeric Data initial residual slice

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-ND-060` | `numeric_data` | `Numeric_Data.md` | Real design-deviation regret case, source year 2022 | — | resolved | Appended 15,000 RUB → ≈$220 and 50,000 RUB → ≈$740 at the confirmed 2022 USD/RUB annual average of 67.5. |
| `D-ND-061` | `numeric_data` | `Numeric_Data.md` | Entry-hallway dividing-wall case, source year 2020 | — | resolved | Appended <$28 for <2,000 RUB and >$140–$280 for >10,000–20,000 RUB at the confirmed 2020 USD/RUB annual average of 71.9. |
| `D-ND-062` | `numeric_data` | `Numeric_Data.md` | Re-keying cost after lost key, source year 2019 | — | resolved | Appended ≈$31 for ≈2,000 RUB at the confirmed 2019 USD/RUB annual average of 64.7. |

Raw source text remains in the source file; these stable rows identify the
price-bearing sentence rather than a mutable line number. Parent IDs are
reserved for later splits when one sentence contains independently sourced
figures. The broader §6 inventory remains open.

## Turn 96 — processed_sources.csv slice

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CSV-014` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260817_cidd4YHBJdA`, layout-only design fees, source year 2023 | — | resolved | Appended approximately $50/m² for 4,000 RUB/m² and $65/m² for 5,500 RUB/m² at the confirmed 2023 USD/RUB annual average of 84.7. |
| `D-CSV-015` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260818_WBaKEl5HIzU`, wallpaper prices, source year 2019 | — | resolved | Appended approximately $500 for ~32,000 RUB standard and $2,000 for ~130,000 RUB premium at the confirmed 2019 USD/RUB annual average of 64.7. |

These two stable IDs cover only explicit price-bearing entries with a confirmed
source year; rows with missing years or non-specific amounts remain for later
inventory disposition.

## Turn 98 — processed_sources.csv slice

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CSV-016` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260817_2`, Zemstandart design-fee price history, source years 2025 and 2026 | — | resolved-partial | Appended approximately $50/m² for the 2025 4,000 RUB/m² fee at 83.21 RUB/USD (rounded per the 2026-08-21 no-cents/approximate-precision correction); retained the 2026 5,000 RUB/m² figure with an explicit no-equivalent note because 2026 has no complete historical annual average. |
| `D-CSV-017` | `processed_sources_csv` | `00_Master/processed_sources.csv` | `run_20260817_3`, property-value figure, source year 2024 | — | resolved | Appended approximately $3,800/m² for 350,000 RUB/m² at 92.66 RUB/USD (rounded per the 2026-08-21 no-cents/approximate-precision correction); explicitly retained its separate property-value status rather than treating it as a renovation-cost benchmark. |

## Turn 100 — USD no-cents retrofit: Cross-Source slice

| Retrofit ID | File | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-CS-R-001` | `Cross_Source_Comparison_Tables.md` | Бородатый Прораб full-realization figure, 2025 | resolved | rounded ≈$1,800+/m²; original currency figures retained. |
| `D-CS-R-002` | `Cross_Source_Comparison_Tables.md` | Zemstandart bespoke design-tier average, 2023 | resolved | rounded ≈$3,900 total; original currency figures retained. |
| `D-CS-R-003` | `Cross_Source_Comparison_Tables.md` | Бородатый Прораб tile installation, 2025 | resolved | rounded ≈$50 and ≈$100/m²; original currency figures retained. |
| `D-CS-R-004` | `Cross_Source_Comparison_Tables.md` | РемонтХочу tile installation, 2024 | resolved | rounded ≈$70/m²; original currency figures retained. |
| `D-CS-R-005` | `Cross_Source_Comparison_Tables.md` | 7komnat.by derived per-m² fee | resolved | rounded ≈$34/m²; original $1,750 total retained; original currency figures retained. |
| `D-CS-R-006` | `Cross_Source_Comparison_Tables.md` | Zemstandart video #157, 2021 | resolved | corrected source-year rate to 73.6; rounded ≈$34 and ≈$41–$48/m²; original currency figures retained. |
| `D-CS-R-007` | `Cross_Source_Comparison_Tables.md` | Zemstandart Sergey Saratov video, 2022 | resolved | rounded ≈$40/m²; original currency figures retained. |
| `D-CS-R-008` | `Cross_Source_Comparison_Tables.md` | Zemstandart video #177, 2022 | resolved | rounded ≈$40/m²; original currency figures retained. |
| `D-CS-R-009` | `Cross_Source_Comparison_Tables.md` | Zemstandart livestream, 2022 | resolved | rounded ≈$40 and ≈$60/m²; original currency figures retained. |
| `D-CS-R-010` | `Cross_Source_Comparison_Tables.md` | Zemstandart video #287, 2024 | resolved | rounded ≈$40/m² (corrected 2026-08-21 — previously $50, a copy-paste error from the adjacent 2025 row); original currency figures retained. |
| `D-CS-R-011` | `Cross_Source_Comparison_Tables.md` | Zemstandart video #313, 2025 | resolved | rounded ≈$50/m²; original currency figures retained. |
| `D-CS-R-012` | `Cross_Source_Comparison_Tables.md` | Zemstandart video #256, 2023 | resolved | rounded ≈$50/m²; original currency figures retained. |
| `D-CS-R-013` | `Cross_Source_Comparison_Tables.md` | Unnamed designer relayed in video #256, 2023 | resolved | rounded ≈$65/m² and ≈$4,900 total; original currency figures retained. |
| `D-CS-R-014` | `Cross_Source_Comparison_Tables.md` | WITALT full project tier, 2025 | resolved | rounded ≈$1,200–$1,400/m²; original currency figures retained. |
| `D-CS-R-015` | `Cross_Source_Comparison_Tables.md` | WITALT brigade tiers, 2025 | resolved | rounded ≈$240–$960/m²; original currency figures retained. |
| `D-CS-R-016` | `Cross_Source_Comparison_Tables.md` | Бородатый Прораб labor rate, 2025 | resolved | rounded ≈$720/m²; original currency figures retained. |
| `D-CS-R-017` | `Cross_Source_Comparison_Tables.md` | РемонтХочу stages 2–11, 2024 | resolved | rounded ≈$520/m²; original currency figures retained. |
| `D-CS-R-018` | `Cross_Source_Comparison_Tables.md` | Zemstandart comfort-class band, 2022 | resolved | rounded ≈$370–$670/m² and ≈$470/m²; original currency figures retained. |
| `D-CS-R-019` | `Cross_Source_Comparison_Tables.md` | Zemstandart business-class band, 2022 | resolved | rounded ≈$740–$1,300/m²; original currency figures retained. |
| `D-CS-R-020` | `Cross_Source_Comparison_Tables.md` | Conditional AC BYN interpretation, 2017 | resolved | rounded ≈$80/linear meter; currency ambiguity retained; original currency figures retained. |

This retrofit slice applies the 2026-08-21 approximate-precision rule to 20
Cross-Source USD-equivalent lines. The 2021 video #157 row also corrects its
wrongly carried 58.3 rate to the confirmed 2021 rate of 73.6; its recomputed
values are rounded from the corrected arithmetic. Retrofit IDs are separate
from new-content IDs and do not increase the underlying price-line inventory.

## Turn 102 — USD no-cents retrofit: Numeric Data and CSV slice

| Retrofit ID | File | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-ND-R-001` | `Numeric_Data.md` | Yana Vrublevskaya 2023 rough works totals | resolved | rounded ≈$3,700, ≈$3,500, and ≈$190; original figures and source markers retained. |
| `D-ND-R-002` | `Numeric_Data.md` | Zemstandart 2022 design fee | resolved | rounded ≈$40/m²; original figures and source markers retained. |
| `D-ND-R-003` | `Numeric_Data.md` | Zemstandart 2022→2023 transition fee | resolved | rounded ≈$40/m² and ≈$50/m²; original figures and source markers retained. |
| `D-ND-R-004` | `Numeric_Data.md` | Furniture-dispute case totals, 2020 | resolved | rounded all USD equivalents to whole/approximate values; original figures and source markers retained. |
| `D-ND-R-005` | `Numeric_Data.md` | Comfort-class labor band restated, 2022 | resolved | rounded ≈$370–$670/m²; original figures and source markers retained. |
| `D-ND-R-006` | `Numeric_Data.md` | Design-deviation regret case, 2022 | resolved | rounded ≈$220 and ≈$740; original figures and source markers retained. |
| `D-ND-R-007` | `Numeric_Data.md` | Entry-hallway dividing-wall case, 2020 | resolved | rounded <$28 and >$140–$280; original figures and source markers retained. |
| `D-ND-R-008` | `Numeric_Data.md` | Re-keying cost, 2019 | resolved | rounded ≈$31; original figures and source markers retained. |
| `D-ND-R-009` | `Numeric_Data.md` | Interior door price point, 2019 | resolved | rounded ≈$190–$230/unit; original figures and source markers retained. |
| `D-ND-R-010` | `Numeric_Data.md` | Inspection-fee data point, 2019 | resolved | rounded ≈$150 and ≈$3,100+; removed obsolete decimal error from correction prose; original figures and source markers retained. |
| `D-ND-R-011` | `Numeric_Data.md` | Emergency-repair steel strip, 2023 | resolved | rounded ≈$27; original figures and source markers retained. |
| `D-ND-R-012` | `Numeric_Data.md` | Food-waste disposer, 2022 | resolved | rounded ≈$440; original figures and source markers retained. |
| `D-ND-R-013` | `Numeric_Data.md` | Comfort/business labor bands, 2022 | resolved | rounded ≈$370–$670, ≈$470, and ≈$740–$1,300/m²; original figures and source markers retained. |
| `D-ND-R-014` | `Numeric_Data.md` | Earliest design-fee point, 2021 | resolved | rounded ≈$34 and ≈$41–$48/m²; original figures and source markers retained. |
| `D-ND-R-015` | `Numeric_Data.md` | Restated comfort/business bands, 2022 | resolved | rounded ≈$370–$670 and ≈$740–$1,300/m²; original figures and source markers retained. |
| `D-ND-R-016` | `Numeric_Data.md` | Bespoke design-tier average, 2023 | resolved | rounded ≈$1,300, ≈$2,600, and ≈$3,900/m²; original figures and source markers retained. |
| `D-ND-R-017` | `Numeric_Data.md` | Bespoke-design worthwhile threshold, 2023 | resolved | rounded >$354,000; original figures and source markers retained. |
| `D-ND-R-018` | `Numeric_Data.md` | Exclusive bespoke design fee, 2023 | resolved | rounded ≈$11,800 and ≈$160/m²; original figures and source markers retained. |
| `D-ND-R-019` | `Numeric_Data.md` | December 2025 design fee | resolved | rounded ≈$50/m²; 2026 future rate remains non-computable; original figures and source markers retained. |
| `D-ND-R-020` | `Numeric_Data.md` | Apartment market value, 2024/2025 | resolved | rounded ≈$3,800 and ≈$4,200/m²; original figures and source markers retained. |
| `D-CSV-R-001` | `processed_sources.csv` | run_20260730_1 | resolved | rounded ≈$1,200–$1,400 and ≈$240–$960; original figures and source metadata retained; notes field only changed. |
| `D-CSV-R-002` | `processed_sources.csv` | run_20260731_5 | resolved | rounded ≈$1,800/m²+; original figures and source metadata retained; notes field only changed. |
| `D-CSV-R-003` | `processed_sources.csv` | run_20260731_7 | resolved | rounded ≈$190 for the 585 BYN gap; original figures and source metadata retained; notes field only changed. |
| `D-CSV-R-004` | `processed_sources.csv` | run_20260814_3 | resolved | rounded ≈$440; original figures and source metadata retained; notes field only changed. |
| `D-CSV-R-005` | `processed_sources.csv` | run_20260814_4 | resolved | rounded all 2022 USD equivalents to whole/approximate values; original figures and source metadata retained; notes field only changed. |
| `D-CSV-R-006` | `processed_sources.csv` | run_20260815_17 | resolved | rounded ≈$40/m² (corrected 2026-08-21 - previously $50, an arithmetic error); original figures and source metadata retained; notes field only changed. |
| `D-CSV-R-007` | `processed_sources.csv` | run_20260815_18 | resolved | rounded ≈$40/m² (corrected 2026-08-21 - previously $50, an arithmetic error); original figures and source metadata retained; notes field only changed. |
| `D-CSV-R-008` | `processed_sources.csv` | run_20260817_cidd4YHBJdA | resolved | rounded ≈$50/m² and ≈$65/m²; original figures and source metadata retained; notes field only changed. |
| `D-CSV-R-009` | `processed_sources.csv` | run_20260818_WBaKEl5HIzU | resolved | rounded ≈$500 and ≈$2,000; original figures and source metadata retained; notes field only changed. |

This slice completes the decimal-form retrofit in Numeric Data and the nine
price-bearing CSV rows containing USD decimal forms at the refreshed baseline.

## Turn 104 — guide/detail USD-equivalent audit: Doors detail batch

| Retrofit ID | File | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-GD-R-001` | `Doors_Trim_Cost_and_Buying.md` | interior classic hinged material/hardware set, 10,000–40,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-002` | `Doors_Trim_Cost_and_Buying.md` | sliding-pocket set from ~20,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-003` | `Doors_Trim_Cost_and_Buying.md` | concealed-mount full kit from ~30,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-004` | `Doors_Trim_Cost_and_Buying.md` | cheapest MDF-film ~10,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-005` | `Doors_Trim_Cost_and_Buying.md` | eco-veneer ~15,000–20,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-006` | `Doors_Trim_Cost_and_Buying.md` | solid-wood from ~30,000 RUB / ~25,000 stock average | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-007` | `Doors_Trim_Cost_and_Buying.md` | cheap aluminum-edge concealed from ~12,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-008` | `Doors_Trim_Cost_and_Buying.md` | quality full-aluminum-frame concealed from ~50,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-009` | `Doors_Trim_Cost_and_Buying.md` | hardware set alone ~5,000–7,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-010` | `Doors_Trim_Cost_and_Buying.md` | classic hinged installation ≈5,000 RUB/door | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-011` | `Doors_Trim_Cost_and_Buying.md` | concealed-mount installation ≈30,000 RUB/door | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-012` | `Doors_Trim_Cost_and_Buying.md` | manufacturer entrance-door tier ladder 65,000–380,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-013` | `Doors_Trim_Cost_and_Buying.md` | retailer sufficient entrance tier ≈65,000–95,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-014` | `Doors_Trim_Cost_and_Buying.md` | concealed-door apartment multiplier, hundreds of thousands of RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-015` | `Doors_Trim_Cost_and_Buying.md` | door hardware set ~5,000–7,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-016` | `Door_Anatomy_and_Mount_Types.md` | classic hinged full turnkey ≈5,000 RUB/door | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-017` | `Door_Anatomy_and_Mount_Types.md` | sliding-pocket material/hardware from ~20,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-018` | `Door_Anatomy_and_Mount_Types.md` | concealed-door material/kit floor ≈30,000 RUB | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |
| `D-GD-R-019` | `Door_Anatomy_and_Mount_Types.md` | concealed full installation ≈30,000 RUB/door | resolved-uncomputable | 2026 source figure; no complete historical annual USD/RUB rate; original RUB figure retained with direct exchange-rate policy link. |

This bounded guide/detail batch adds claim-local non-computable handling to 19
2026 price-bearing lines. Remaining guide/detail files require source-year
inventory and conversion or explicit non-computable handling.

## Turn 2 (CODEX) — Numeric Data / Cross-Source trailing-date slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-ND-063` | `numeric_data` | Zemstandart comfort-class labor band, undated source | resolved-uncomputable | Explicit not-computable reason added; no date-anchored conversion guessed. |
| `D-ND-064` | `numeric_data` | RemontХочу 11-stage smeta, 2024-11-14 | resolved | Added ≈$53,200 total and ≈$530/m² using trailing 6-month average 90.98. |
| `D-ND-065` | `numeric_data` | Бородатый Прораб full-realization figure, 2025-01-08 | resolved | Added ≈$1,600/m² and ≈$158,000 total using trailing 6-month average 94.72. |
| `D-ND-066` | `numeric_data` | BURO segment-tier framework, 2026-03-12 | resolved | Added ≈$2,500/≈$5,700/≈$12,600 per m² tier boundaries using trailing 6-month average 79.39; preserved open-ended upper bound. |
| `D-ND-067` | `numeric_data` | BURO HVAC cost-variance bands, 2026-03-12 | resolved | Added date-anchored ≈$2,500–$8,800, ≈$12,600–$37,800, ≈$18,900–$63,000 total and ≈$60–$630/m² equivalents using trailing 6-month average 79.39. |
| `D-ND-068` | `numeric_data` | Бородатый Прораб design tiers, 2025-01-08 | resolved | Added ≈$40/≈$50/≈$70 per m² for 4,000/5,000/7,000 RUB using trailing 6-month average 94.72. |
| `D-CS-075` | `cross_source` | BURO and full-realization rows | resolved | Added date-anchored equivalents for BURO and Бородатый Прораб rows. |
| `D-CS-076` | `cross_source` | Zemstandart bespoke-design average, 2023-01-17 | resolved | Added ≈$4,900 total using trailing 12-month average 68.23. |
| `D-CS-077` | `cross_source` | Tile installation labor rows, 2025-01-08 and 2024-11-14 | resolved | Added ≈$40/≈$85 and ≈$70 per m² using date-anchored trailing 6-month averages. |

This slice applies the post-dialogue precision rule to newly filled units:
trailing 6 months for general renovation work, and 12 months for the longer
bespoke-design history. Original currencies and figures remain unchanged.

## Turn 4 (CODEX) — processed_sources.csv notes-field slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-CSV-018` | `processed_sources_csv` | `run_20260810_19`, 2020-12-01 dividing-wall case | resolved | Added <$27 for the <2,000 RUB figure using the trailing 6-month USD/RUB average of 74.12 (corrected 2026-08-23 - previously <$28, a $1 rounding slip). |
| `D-CSV-019` | `processed_sources_csv` | `run_20260810_22`, 2022-11-13 bathroom regret case | resolved | Added ≈$250 and ≈$840 for 15,000 and 50,000 RUB using the trailing 6-month average of 59.74. |
| `D-CSV-020` | `processed_sources_csv` | `run_20260810_44`, 2019-02-02 inspection-cost case | resolved | Added ≈$150 and ≈$3,000 for ~10,000 and ~200,000 RUB using the trailing 6-month average of 66.64. |

All three changes are confined to the CSV `notes` field; source metadata,
original currencies, and original amounts remain unchanged.

## Turn 6 (CODEX) — Bathroom guide/detail slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-GD-020` | `guide_detail` | `07_Bathroom/Bathroom_Guide.md`, dated towel-warmer and heated-floor estimates | resolved | Added date-anchored equivalents: ≈$30 vs. ≈$130–$190 for 2,500 vs. 10,000–15,000 RUB and ≈$380 for 30,000 RUB, using the 2026-04-17 trailing 6-month average of 78.86. |
| `D-GD-021` | `guide_detail` | `07_Bathroom/Bathroom_Guide.md`, concealed-door finishing estimate | resolved-uncomputable | Added explicit not-computable reason because the cited source date is not independently confirmed. |
| `D-GD-022` | `guide_detail` | `07_Bathroom/analysis/Bathtub_and_Shower.md`, tub/pan material estimates | resolved | Added ≈$160–$210, ≈$420–$520, and ≈$210 equivalents using the 2025-04-04 trailing 6-month average of 95.97. |
| `D-GD-023` | `guide_detail` | `07_Bathroom/analysis/Fixtures_Mixers_and_Sinks.md`, rain-shower assembly | resolved | Added ≈$520–$630 for 50,000–60,000 RUB using the 2025-04-04 trailing 6-month average of 95.97. |
| `D-GD-024` | `guide_detail` | `07_Bathroom/analysis/Planning_and_Layout.md`, comfort-class labor band | resolved-uncomputable | Added explicit not-computable reason because the restated figure has no independently confirmed publish date. |

## Turn 8 (CODEX) — Ceilings guide slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-GD-025` | `guide_detail` | `13_Surfaces_and_Finishes/Ceilings_Guide.md`, L-shaped stretch-ceiling cost delta | resolved | Added approximately >$140–>$270 for the >10,000–>20,000 RUB delta using the 2020-12-01 trailing 6-month average of 74.12. |

## Turn 10 (CODEX) — Doors guide headline slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-GD-026` | `guide_detail` | `13_Surfaces_and_Finishes/Doors_and_Trim.md`, classic-hinged installation and entrance-door tiers | resolved-uncomputable | Added claim-local explanation that exact publish dates are not confirmed; no conversion guessed. |

## Turn 12 (CODEX) — Walls and Paint guide slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-GD-027` | `guide_detail` | `13_Surfaces_and_Finishes/Walls_and_Paint.md`, load-bearing opening cost comparison | resolved | Added ≈$230 DIY and >$760 specialist equivalents using the 2019-01-05 trailing 6-month average of 66.08. |
| `D-GD-028` | `guide_detail` | `13_Surfaces_and_Finishes/Walls_and_Paint.md`, 435,000 RUB designer-fee case | resolved | Added ≈$4,800 using the 2024-05-05 trailing 6-month average of 91.06. |

## Turn 14 (CODEX) — Engineering systems analysis slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-GD-029` | `guide_detail` | `12_Engineering_and_Systems/analysis/AC_Sizing_and_Selection.md`, BURO AC-system cost comparison | resolved | Added date-anchored ≈$2,500, ≈$6,300–$8,800, ≈$12,600–$37,800, ≈$18,900–$63,000, and ≈$60–$630/m² equivalents using trailing 6-month average 79.39. |
| `D-GD-030` | `guide_detail` | `12_Engineering_and_Systems/analysis/Hygienic_Shower_and_Towel_Warmer.md`, towel-warmer/leak-protection costs | resolved | Added date-anchored ≈$100–$160, ≈$30, ≈$310–$520, and <$1/month equivalents using trailing 6-month average 95.97. |

## Turn 20 (CODEX) — Wardrobes guide/detail slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-GD-031` | `guide_detail` | `14_Furniture/Wardrobes_and_Storage.md`, dated dividing-wall cost supporting built-in wardrobe conversion | resolved | Added under ≈$30 for the source's <2,000 RUB cost using the 2020-12-01 trailing six-month USD/RUB average of 74.1231; hand-check: 2,000 ÷ 74.1231 = 26.98, which rounds to $30 in the nearest-$10 bucket. |
| `D-GD-032` | `guide_detail` | `14_Furniture/analysis/Wardrobe_vs_Walkin_Tradeoff.md`, same dated 2.16m dividing-wall case | resolved | Added the same claim-local under ≈$30 equivalent and derivation; this is one source/cost event repeated across guide and detail, not a second independent price. |

## Turn 21 (CODEX) — Plumbing guide/detail slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-GD-033` | `guide_detail` | `12_Engineering_and_Systems/Plumbing_and_Waterproofing.md`, dated water-supply and heating rough-in total | resolved | Added ≈$4,200 for the source's 380,000 RUB / 100 m² construction-only example using the 2024-11-14 trailing six-month USD/RUB average of 90.9774; hand-check: 380,000 ÷ 90.9774 = 4,176.86, which rounds to $4,200 in the nearest-$100 bucket. |
| `D-GD-034` | `guide_detail` | `12_Engineering_and_Systems/analysis/Cost_Drivers_and_Buying_Guidance.md`, same dated rough-in total | resolved | Added the same claim-local ≈$4,200 equivalent and derivation; this is one source/cost event repeated across guide and detail, not a second independent price. |

## Turn 23 (CODEX) — HVAC guide/detail slice

| Slice ID | Scope group | Entry anchor | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- |
| `D-GD-035` | `guide_detail` | `12_Engineering_and_Systems/HVAC_and_Ventilation.md`, dated full-system ventilation cost range and ambiguous breather figure | resolved | Added ≈$19,600–≈$131,000 for the source's 1.5–10 million RUB range using the 2026-07-29 trailing six-month USD/RUB average of 76.4100; hand-checks: 1,500,000 ÷ 76.4100 = 19,630.94 → $19,600 (nearest-$100), and 10,000,000 ÷ 76.4100 = 130,872.92 → $131,000 (nearest-$1,000). Explicitly marked the source's unitless “1,350” breather figure not computable. |
| `D-GD-036` | `guide_detail` | `12_Engineering_and_Systems/analysis/Fresh_Air_Ventilation_and_Ducting.md`, same dated full-system range | resolved | Added the same claim-local range, rate, rounding derivation, and not-computable breather caveat; this is one source event repeated across guide and detail, not a second independent price. |

**History (2026-08-21)**: the original batch claimed 24 lines with generic
"2026 price-bearing line N" labels; a CLAUDE review found 4 were misplaced
(3 appended to Markdown headings instead of price rows, redundant with each
row's own correct annotation; 1 appended to a paragraph with no price figure
at all) and removed them, and a CODEX self-audit then rebuilt this table with
content-specific anchors for the real 19, superseding the earlier generic
version and this note's prior draft.
