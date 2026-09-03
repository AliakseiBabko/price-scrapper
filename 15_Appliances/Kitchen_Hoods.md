# 🌬️ Kitchen Hoods — Category Comparison

Built-in 60cm-class range hoods researched for the kitchen (catalog.onliner.by, prices in BYN). This is the full candidate set behind the selection already made in [[Kitchen_Appliance_Sets]]. For the chosen model's full reasoning and concerns, see [[15_Appliances/models/Kitchen_Bosch_DHL555BL_Hood]].

> [!WARNING]
> Before trusting any hood's rated m³/h spec in this table, read [[15_Appliances/analysis/Kitchen_Hood_Analysis]] — in a standard apartment building, real extraction performance is capped by the shared ventilation shaft (typically ~100-120 m³/h for ex-Soviet-bloc buildings), not by the hood's own motor rating. This affects the already-selected DHL555BL directly.

> [!NOTE]
> Source: local scrape (`scan_brand_hoods.ts` / `scrape_hood_candidates.ts`, Bosch/Electrolux/Gorenje brand-filtered), captured 2026-07-30. Prices are point-in-time and may have moved since. Not currently logged in `00_Master/processed_sources.csv` since it's local repo scraper output, not an external transcript/document source — flagging as an open question rather than backfilling that log myself.

## ✅ Selected

| Model | Price | Max Capacity | Noise (min–max) | Energy | Width | Motors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **[[15_Appliances/models/Kitchen_Bosch_DHL555BL_Hood|Bosch DHL555BL]]** ⭐ | 1,431 BYN | 360 m³/h (618 m³/h per model page, likely boost mode — see note below) | 38–56 dB | C | 53 cm | 2 |

> [!WARNING]
> **Figure mismatch, not resolved here.** The scraped catalog spec (360 m³/h max, 56 dB max noise) differs from the already-written [[15_Appliances/models/Kitchen_Bosch_DHL555BL_Hood]] model page (618 m³/h, 68 dB at max speed). This could be a standard-vs-boost-mode distinction the model page captured from elsewhere (e.g. product manual) that the catalog listing doesn't show, or the two simply reflect different measurement conditions. Not corrected here — the model page's numbers are left as-is since they came with sourced reasoning; this table shows the raw catalog scrape as its own record.

## Bosch (9 models)

| Model | Price | Max Capacity | Min Noise | Max Noise | Energy | Width | Mount | Motors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| DFT63CA20Q | 471 BYN | 300 m³/h | 48 dB | 62 dB | E | 59.8 cm | Built-in | 1 |
| DFT63CA50Q | 509 BYN | 300 m³/h | 48 dB | 62 dB | E | 59.8 cm | Built-in | 1 |
| DLN53AA70 | 521 BYN | 302 m³/h | 46 dB | 62 dB | D | 53.4 cm | Wall/Built-in | 1 |
| DFT63CA60Q | 697 BYN | 300 m³/h | 48 dB | 62 dB | E | 59.8 cm | Built-in | 1 |
| **DHL555BL** ⭐ | 1,431 BYN | 360 m³/h (190 min) | 38 dB | 56 dB | C | 53 cm | Built-in | 2 |
| DLN56AC50 (Serie 6) | 2,110 BYN | 570 m³/h | — | 72 dB | B | 52 cm | Built-in | 1 |
| DFS067A51 (Serie 4) | 2,219 BYN | 210.7 m³/h min | 41 dB | 53 dB | A | 59.8 cm | Built-in | 1 |
| DBB67AM60 | 4,367 BYN | 460 m³/h (264.6 min) | 50 dB | 63 dB | B | 59.7 cm | Wall/Built-in | — |
| DBB97AM60 (Serie 6) | 4,418 BYN | 460 m³/h (264.6 min) | 50 dB | 63 dB | B | 89.7 cm | Built-in | 1 |

## Electrolux (8 models)

| Model | Price | Max Capacity | Min Noise | Max Noise | Energy | Width | Perimetral Suction |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| LFP326S | 770 BYN | 410 m³/h (170 min) | 48 dB | 69 dB | C | 59.8 cm | No |
| LFP326FB | 1,066 BYN | 410 m³/h (170 min) | 48 dB | 69 dB | C | 59.8 cm | No |
| LFP326FW | 1,141 BYN | 410 m³/h (170 min) | 48 dB | 69 dB | C | 59.8 cm | No |
| LFP616X | 1,362 BYN | 600 m³/h (220 min) | 46 dB | 68 dB | A | 59.8 cm | No |
| LFP536X | 1,432 BYN | 600 m³/h (250 min) | 49 dB | 68 dB | C | 59.98 cm | No |
| LFP539X | 1,551 BYN | 600 m³/h (250 min) | 49 dB | 68 dB | C | 89.98 cm | No |
| LFG716R | 1,599 BYN | 580 m³/h (300 min) | 54 dB | 67 dB | A | 54 cm | — |
| EFG716R (Hob2Hood) | 2,117 BYN | 580 m³/h (300 min) | 54 dB | 67 dB | A | 54 cm | Yes |

## Gorenje (5 models)

| Model | Price | Max Capacity | Min Noise | Max Noise | Energy | Width | Mount |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| WHU629EX/M | 273 BYN | 249 m³/h (126 min) | 60 dB | 67 dB | C | 59.6 cm | Wall |
| BHI626E6B | 429 BYN | 677 m³/h | — | 61 dB | — | 60.5 cm | Built-in |
| TH60E7XB | 699 BYN | 750 m³/h (354 min) | — | 52 dB | — | 59.8 cm | Built-in |
| WHC63CLI | 1,433 BYN | 650 m³/h (246 min) | 50 dB | 71 dB | B | 60 cm | Wall |
| DK63MCLI | 1,545 BYN | — | 41 dB | — | — | 60 cm | Wall |

## Reading Notes

- **"—"** means the field wasn't populated in the source listing, not that the spec is zero.
- Capacity is the manufacturer-stated max airflow at a given duct/setting; real-world performance depends heavily on duct diameter and routing (see [[11_Budget_and_Planning/Renovation_Sequence]] for sequencing implications of duct choice).
- Cheapest-per-brand does not necessarily mean lowest quality — several sub-500 BYN Gorenje models (e.g. TH60E7XB at 750 m³/h) outperform pricier Bosch entries on raw capacity, but trade off noise, motor count, or smart features. The already-selected DHL555BL was chosen for dual-motor reliability and manual controls over these, per [[15_Appliances/models/Kitchen_Bosch_DHL555BL_Hood]]'s reasoning.

## ⚠️⚠️ A Concealed Extract Condenses Steam Onto the Door Above It — a Disclosed Defect, Accepted for Appearance (Александр Синчуков, his own kitchen, 2023-11-02)

**An extract built into the cabinet above the hob, occupying that drawer. Extraction performance itself is fine — «тянет она неплохо, даже когда активная готовка, очень много пара — она с этим справляется». The defect is elsewhere:**

**«Если КИПЯТИШЬ ВОДУ, то испарения начинают просто ЗАСТИЛАТЬ вот здесь ДВЕРЦУ — это прямо НЕКРАСИВО. Поэтому вытяжку приходится ВКЛЮЧАТЬ ВСЁ ВРЕМЯ. Если бы вытяжка была ОТДЕЛЬНАЯ, наверное, этой проблемы бы НЕ БЫЛО.»**

- → **⚠️ A concealed extract must be RUN CONTINUOUSLY even for boiling water, or steam condenses on the cabinet door above. That is an operating cost, not a performance one, and it does not appear in any specification.**
- **His reason for keeping it is stated and is purely aesthetic: «чисто ЭСТЕТИЧЕСКИ мне нравится решение с ОТДЕЛЬНОЙ вытяжкой МЕНЬШЕ, именно в таком современном стиле».** → **Record as a knowing trade-off with both sides named, which is how he presents it. Not a mistake — a priced choice.**
- ⚠️ **And the vault now holds the other half of it, from the factory that built the cabinet: the niche is formed at the works, the duct spigot is planned, and the penetration is CUT ON SITE — «по месту вырежем отверстие».** The manufacturer notes he is constantly asked where the extract went: «Она просто СКРЫТА вот в этих верхних шкафах.» [source: [[_Sources/YT_P3O2koqOGp8_nsdsgn_carcass_furniture_production|YT_P3O2koqOGp8]]]
  - **→ The construction and the consequence, from two sources, nine months apart, on the same cabinet.**

[source: [[_Sources/YT_AEJlxbTmQJU_nsdsgn_own_kitchen_review|YT_AEJlxbTmQJU]]]

