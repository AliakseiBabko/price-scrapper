# 💧 Kitchen Water Filtering — Category Comparison

Under-sink reverse-osmosis (RO) drinking-water systems researched for the kitchen (catalog.onliner.by, prices in BYN).

> [!WARNING]
> **Partial data — read before using.** Local scratch scraper output for this category is a mix of a broad, unfiltered ~77-item market scan (`scratch/all_ro_filters.txt`) and a handful of models with full specs pulled (`scratch/specs_summary.txt`). Only **7 models** below have both a downloaded product image (in `_assets/`) *and* matching price/spec data — those are the ones actually built out below. No selection has been made yet; nothing here is marked "chosen."

## Corroborated Candidates (image + price + specs all match)

| Model | Price | Cartridges | Flow Rate | Tank Volume | Pump | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| АКВАФОР DWM-101S Морион | 533.00 BYN | 4 | 0.13 L/min | 5 L | — | 371×190×420 mm. Mechanical + RO membrane + carbon + mineralizing stages. |
| БАРЬЕР Профи Осмо 100 | 473.00 BYN | 5 | 1 L/min | 12 L (8 L usable) | No | 355×130×445 mm. 5-stage, includes softening (ion exchange). |
| БАРЬЕР Профи Осмо 100 Boost М (H152P02) | 691.00 BYN | 6 | 0.2 L/min | — | Yes (boost pump) | Same Профи Осмо 100 line, boost-pump variant — spec detail not in `specs_summary.txt`, only basic listing. |
| Аквабрайт АБФ-Осмо-6 | 334.50 BYN | 6 | 0.2 L/min | — | — | 6-stage incl. mineralization block. |
| Гейзер Аллегро М | 331.00 BYN | 6 | 0.14 L/min | 12 L | — | 3-stage pre-filter + mineralization (magnetite/calcite). Rated to 25 atm, 100k+ pressure-shock cycles. |
| Гейзер Престиж ПМ | 708.00 BYN | 6 | — | 12 L | Yes (boost pump) | Basic listing only — no detailed spec pull. |
| Atoll Twist 600 | 876.21 BYN | 2 | 1.8 L/min | — | Yes | Ultra-compact (12.5 cm wide) — "QuickTwist" 2-cartridge system, Smart processor, auto-flush. Notably higher flow rate than the rest of this table. |

## Open Questions

1. **18 more product images with no matching data.** `_assets/` also has images for **Bort** (Alligator, Alligator Control, Alligator Mega, Alligator Plus — 4), **Exiteq** (EX1176, EX1236, EX1246, EX1266, EX1296 — 5), **Status** (Premium 200, Premium 300 — 2), **Teka** (TR550, TR750 — 2), **Tuvio** (KDA25H11 — 1), and **Zorg** (Adel 103060 SGC, Nevada 126060 SGC, Premium FWD Lite, Premium FWD Medium — 4). None of these brand names appear anywhere in `scratch/all_ro_filters.txt`, `search_results.txt`, or `specs_summary.txt` — I have no price or spec data for any of them, and didn't invent any. If you have a source for these (a different scrape run, a screenshot, a memory of where they came from), point me at it and I'll add them properly.
2. **The other ~70 entries in `all_ro_filters.txt`** are a broad, unfiltered category scan (brands like Terwa, Xiaomi, Philips, Zepter, Waterro, Vivasol, Platinum Water, etc.) — I did not include them here because there's no image evidence they were ever actually shortlisted for this kitchen specifically, as opposed to general market research. Say the word if you want the full 77 laid out regardless.
3. **This scrape isn't logged in `00_Master/processed_sources.csv`** the way externally-sourced transcripts are — it's local repo scraper output, not an external document. Not backfilled here since that's a judgment call about the log's intended scope, not something to decide unilaterally.
