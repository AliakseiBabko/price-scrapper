# Workstream D USD-backfill inventory

Stable slice identifiers for the scoped reference-layer price inventory. A
slice ID remains stable if a line is split or later reclassified; status records
the disposition rather than relying only on a changing aggregate count.

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
