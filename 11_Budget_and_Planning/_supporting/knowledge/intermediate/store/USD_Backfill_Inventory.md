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
| `D-ND-063` | `numeric_data` | `Numeric_Data.md` | Real inspection-fee data point, source year 2019 | — | resolved | Appended ≈$154.6 for ≈10,000 RUB and ≈$3,091.2+ for ≈200,000 RUB+ at the confirmed 2019 USD/RUB annual average of 64.7. Corrected 2026-08-21 - the originally-merged $2,781.6 figure was an arithmetic error. |
| `D-ND-064` | `numeric_data` | `Numeric_Data.md` | Real emergency-repair steel-strip cost, source year 2023 | — | resolved | Appended ≈$27.2 for ≈2,300 RUB at the confirmed 2023 USD/RUB annual average of 84.7. |

Stable slice identifiers for the scoped reference-layer price inventory. A
slice ID remains stable if a line is split or later reclassified; status records
the disposition rather than relying only on a changing aggregate count.

## Current Cross-Source 2026/2025 tier slice

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CS-078` | `cross_source` | `Cross_Source_Comparison_Tables.md` | BURO Luxury tier, source year 2026 | — | resolved-uncomputable | Original 1,000,000+ RUB/m² retained; no USD equivalent because 2026 has no complete historical annual rate. |
| `D-CS-079` | `cross_source` | `Cross_Source_Comparison_Tables.md` | BURO Premium tier, source year 2026 | — | resolved-uncomputable | Original 450,000–1,000,000 RUB/m² retained; no USD equivalent because 2026 has no complete historical annual rate. |
| `D-CS-080` | `cross_source` | `Cross_Source_Comparison_Tables.md` | BURO Mid tier, source year 2026 | — | resolved-uncomputable | Original 200,000–450,000 RUB/m² retained; no USD equivalent because 2026 has no complete historical annual rate. |
| `D-CS-081` | `cross_source` | `Cross_Source_Comparison_Tables.md` | Бородатый Прораб full-realization figure, source year 2025 | — | resolved | Appended ≈$1,802.7+/m² for 150,000+ RUB/m² at the confirmed 2025 USD/RUB annual average of 83.21. |

## Current Cross-Source audited slice

| Slice ID | Scope group | File | Entry anchor | Parent ID | Status | Disposition |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `D-CS-075` | `cross_source` | `Cross_Source_Comparison_Tables.md` | Zemstandart bespoke design-tier average, source year 2023 | — | resolved | Appended ≈$3,907.9 for 331,000 RUB at the confirmed 2023 USD/RUB annual average of 84.7. |
| `D-CS-076` | `cross_source` | `Cross_Source_Comparison_Tables.md` | Бородатый Прораб tile installation, source year 2025 | — | resolved | Appended ≈$48.1/m² for 4,000 RUB/m² and ≈$96.1/m² for 8,000 RUB/m² at the confirmed 2025 USD/RUB annual average of 83.21. |
| `D-CS-077` | `cross_source` | `Cross_Source_Comparison_Tables.md` | РемонтХочу tile installation, source year 2024 | — | resolved | Appended ≈$70.1/m² for 6,500 RUB/m² at the confirmed 2024 USD/RUB annual average of 92.66. |

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
| `D-ND-060` | `numeric_data` | `Numeric_Data.md` | Real design-deviation regret case, source year 2022 | — | resolved | Appended 15,000 RUB → ≈$222.2 and 50,000 RUB → ≈$740.7 at the confirmed 2022 USD/RUB annual average of 67.5. |
| `D-ND-061` | `numeric_data` | `Numeric_Data.md` | Entry-hallway dividing-wall case, source year 2020 | — | resolved | Appended <$27.8 for <2,000 RUB and >$139.1–$278.2 for >10,000–20,000 RUB at the confirmed 2020 USD/RUB annual average of 71.9. |
| `D-ND-062` | `numeric_data` | `Numeric_Data.md` | Re-keying cost after lost key, source year 2019 | — | resolved | Appended ≈$30.9 for ≈2,000 RUB at the confirmed 2019 USD/RUB annual average of 64.7. |

Raw source text remains in the source file; these stable rows identify the
price-bearing sentence rather than a mutable line number. Parent IDs are
reserved for later splits when one sentence contains independently sourced
figures. The broader §6 inventory remains open.
