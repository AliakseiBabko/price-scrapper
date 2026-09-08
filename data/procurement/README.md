# `data/procurement/` — the bill of materials and the quotes against it

**Created 2026-09-08.** The spine of the money-and-people side. Two files, deliberately separate.

| File | What it is | Who writes it |
| :--- | :--- | :--- |
| **`bom.csv`** | **Our own scope**: what is needed, where, how much, and what we expect it to cost | us |
| **`quotes.csv`** | **Evidence received**: one row per (BOM line × source × date) with the rate actually quoted | copied from what suppliers and trades send |

**Why they are separate**: the BOM is a statement of intent that we control; a quote is an external fact with a provenance and an expiry. Mixing them loses both — you can no longer tell what you asked for from what you were told, and you cannot hold three competing quotes against one line.

## Purpose, decided by the owner 2026-09-08

> **«The estimations are FOR US, for price negotiations and verification.»**

**So this is a negotiation and verification instrument, not a compliance export.** It never has to render as a formal смета (С-29 / КБ-2в) — no Belarusian private contractor expects one, and НРР is unusable by a private owner anyway (see [[../../16_Legal_and_Regulations/Legal_and_Regulations_Guide|the legal folder]] and the research review). Its job is narrower and more useful: **hold our expected quantity and rate next to every quote received, so a number can be checked and argued with.**

## ⚠️ The engagement unit is the WORK TYPE

> **«There will be no one contract. There will be small contracts per each type of work.»**

**Consequences baked into the schema:**

- **`trade` is the primary slice.** Every query, pack and price comparison groups by it, because a trade slice *is* a contract's subject matter.
- **`rate_source` is keyed per trade**, so losing one contractor re-prices one trade rather than every line.
- **⚠️ And the interfaces between trades are the main risk, so they are rows too.** Nobody owns the joins by default — who waterproofs before the tiler arrives, who chases for the electrician, who protects finished work. **№ 164 §16 allocates damage liability to whoever caused it and is silent on how you prove which trade that was**, so an interface has to be assigned in writing before anyone starts. Interface rows carry `trade = IFC` and exist to be argued about, not bought.

## ⚠️ Rate discovery does not wait for quantities

**The insight that makes this file useful today**: you can ask three tilers for a rate per m² **before** knowing the exact m². **So the scope rows and the rate columns are fillable now, while `qty` stays null until the model carries phase and finishes** (`cap2`, `cap5`).

That is why the seeded rows below have **`qty` empty and `qty_source = unmeasured`**. **They are not placeholders to be guessed at — the standing rule that areas are not evidence forbids deriving them from the developer's area figures.** They fill in when the model does.

## `bom.csv` columns

| Column | Meaning |
| :--- | :--- |
| `key` | `TRADE-NN:ROOM:resource` — e.g. `TIL-01:R04:paving_600x600`. Unique |
| `trade` | 3-letter code, see below. The engagement unit |
| `task` | short verb phrase — what is done |
| `room` | room id, or `ALL` |
| `resource_role` | **what the line is FOR** — stable across product changes |
| `product_id` | **what was chosen** — nullable, swappable. ⚠️ A discontinued material is a change to THIS field only |
| `qty`, `unit` | quantity and unit. Empty until measurable |
| `qty_source` | `model_measured` \| `datasheet_derived` \| `manual` \| `unmeasured` |
| `waste_basis` | `pct:N` \| `nested` \| `none`. `nested` only where the research supports it — large-format tile and sheet goods |
| `rate_expected`, `rate_unit` | our own anchor for negotiation, in BYN |
| `rate_expected_source` | ⚠️ **where the anchor came from, and how much to trust it** |
| `stage` | `1`–`5` — demolition/partitions, rough MEP, screed/plaster, tiling, finishes. Do not commit stage 4 rates in stage 1 |
| `lead_time_days` | **nullable and deliberately unpopulated** — out of scope 2026-09-08, «varies significantly per provider and vendor» |
| `notes` | free text |

**Trade codes**: `DEM` demolition · `MAS` masonry · `PLA` plastering · `SCR` screed and levelling · `WAT` waterproofing · `TIL` tiling · `PLU` plumbing · `ELE` electrical · `VEN` ventilation · `PNT` painting and decorating · `DOR` doors and trim · `FUR` furniture and fit-out · `IFC` **a trade interface, not a purchase**

## `quotes.csv` columns

`bom_key` · `source` (contractor or supplier) · `quote_date` · `valid_until` · `rate_material` · `rate_labour` · `rate_unit` · `currency` · `scope_note` (what they said they included) · `status` (`received` \| `shortlisted` \| `rejected` \| `accepted` \| `expired`)

**⚠️ `valid_until` matters as much as the rate.** The research puts a firm private quote at **30–45 days**; a rate past its window is not a price, it is a memory.

## Validation

```
.venv\Scripts\python.exe tools\procurement\validate_bom.py
```

Checks key format and uniqueness, trade and enum values, that every `quotes.bom_key` resolves, that `nested` waste appears only where it is justified, and that a populated `qty` carries a real `qty_source`. **It also reports expired quotes and lines with no quote at all** — which is the actual working view.
