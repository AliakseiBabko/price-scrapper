# Apartment Renovation Knowledge Base

A personal planning vault for one apartment renovation, built from ~813 source
extraction notes — mostly Russian-language YouTube practitioner sources —
routed into ~243 wiki pages across room and topic folders.

It also contains the marketplace price scraper the project started as, which
now serves it as one component. **Those docs are at the bottom of this file.**

> [!IMPORTANT]
> **If you are an AI agent, read [AGENTS.md](./AGENTS.md) instead of this file.**
> It is the shared entry point for Claude Code, Codex and Antigravity, and it
> carries the standing rules, the tool list and the skill map. This README is
> orientation for a human.

## Layout

| Path | Contents |
| :--- | :--- |
| `_Sources/` | Extraction notes, one per source — raw evidence |
| `_Knowledge/store/` | Intermediate store: durable facts, heuristics, numeric data, source index, change log |
| `00_Master/` | Project docs, deliverable roadmap, processed-source ledger, FX reference, page-format convention |
| `01_`–`17_` | Room and topic wiki folders: a compact guide page plus `analysis/` detail pages |
| `_Archive/` | Archived transcripts, hashed for provenance |
| `_Inbox/planning/` | Channel triage plans and backlogs |
| `.agents/skills/` | Project-specific agent skills |
| `tools/` | Python tooling for intake, verification, pricing and drawings |
| `src/`, `data/` | The price scraper (below) |

## Working on the vault

```bash
python tools/youtube/preflight_playlist.py <url>   # dedup before fetching
python tools/verify_batch.py --base <ref>          # run before every commit
python tools/check_page_sizes.py                   # page split / fragmentation check
python tools/build_knowledge_base_index.py         # rebuild the numeric index
```

The intake pipeline is documented in
`.agents/skills/renovation-knowledge-intake/SKILL.md`; page shape in
`00_Master/wiki_page_format.md`.

---

# Component: Smart Home Appliance Scraper

A modular scraping tool and data comparison engine built with **Node.js
(TypeScript)**, **Playwright** and **SQLite**, fetching prices, specifications
and reviews from marketplaces (initially `catalog.onliner.by`). It supplies the
appliance pricing used by `15_Appliances/` and the budgeting pages.

## 🛠️ Project Setup

### Prerequisites
- Node.js (version 18 or higher)
- Playwright Chromium browser

### Installation
1. Clone or open the workspace.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Install the Playwright Chromium browser instance:
   ```bash
   npx playwright install chromium
   ```

---

## 🚀 Running the Scraper

The orchestrator script is located at `src/run.ts`. You can run it directly using `tsx`:

```bash
# General Syntax
npx tsx src/run.ts --site=[site] --category=[category] --filter="[query_string]" --limit=[number]
```

### Important: PowerShell / Windows Escaping
When running commands in **PowerShell**, characters like `&` must be escaped or enclosed in single quotes so they aren't interpreted as background process operators. 

**Example (PowerShell):**
```powershell
npx tsx src/run.ts --site=onliner --category=oven_cooker --filter='mfr[0]=bosch&cleanup_cooker[0]=pyrolytic&thermoprobe=1' --limit=5
```

---

## 📊 Database Schema (SQLite)

The database file is created automatically at `data/scraper.db` when the scraper runs.

- **`categories`**: Stores catalog category metadata (slug, name, URL).
- **`products`**: Stores the canonical product models with technical specifications in `specs_json` (JSON). Products from different stores are grouped under their brand and core model identifier (e.g. `bosch:hbg7764b1`).
- **`offers`**: Stores store-specific listings (pricing, stock availability, listing URLs, images).
- **`reviews`**: Stores customer reviews including rating, author, publication date, advantages (`pros`), and disadvantages (`cons`).
- **`price_history`**: Tracks changes in price points and offer counts over time.

---

## 🔍 Analytical SQL Query Examples

Below are SQL queries you can use to extract data or **ask me (Antigravity)** to run in this chat. The outputs are formatted in markdown tables, perfect for copying directly into **Obsidian** notes.

### 1. Technology & Specs Comparison (e.g., Bosch Pyrolysis & Display)
```sql
SELECT 
  title,
  json_extract(specs_json, '$."Очистка духового шкафа"') AS cleaning_type,
  json_extract(specs_json, '$."Управление"') AS controls,
  json_extract(specs_json, '$."Объём духового шкафа"') AS volume,
  rating,
  reviews_count
FROM products
WHERE brand = 'Bosch' 
  AND specs_json LIKE '%пиролит%';
```

### 2. Reality Check (Review & Sentiment Analysis)
Find customer reviews mentioning specific design elements (like the touch ring on Bosch Serie 8) or technology issues:
```sql
SELECT 
  p.title,
  r.author,
  r.rating,
  r.pros,
  r.cons,
  r.text
FROM reviews r
JOIN products p ON r.product_id = p.id
WHERE r.text LIKE '%кольцо%' OR r.cons LIKE '%кольцо%'
ORDER BY r.rating ASC;
```

### 3. Price & Offers Comparison
Find the current local price ranges and the number of active marketplace offers:
```sql
SELECT 
  p.title,
  o.price_min,
  o.price_max,
  o.offers_count,
  o.url
FROM offers o
JOIN products p ON o.product_id = p.id
ORDER BY o.price_min ASC;
```
