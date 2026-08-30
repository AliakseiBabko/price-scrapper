---
source_type: video transcript (single-speaker methodology/tooling walkthrough, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=3PJJTDkppUg
video_id: 3PJJTDkppUg
transcript_file: _Archive/processed_sources/20260819_expense_tracking_methodology_504_32e14bcd.txt
fetched: 2026-08-19
upload_date: 2018-12-17 (metadata-confirmed via yt-dlp `upload_date`)
channel: Zemstandart / Zemproekt (Alexey Zemskov)
regional_applicability: level 2 only (no city named directly in this video's content) — assume Moscow per this channel's usual default, not level-1-confirmed
currency: not applicable — no transaction figures, purely a tracking methodology
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemstandart/Zemproekt: "Don't Let Yourself Be Fooled on Your Renovation!" (#504, YouTube 3PJJTDkppUg)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Remainder-pool batch, video 1 of the current small batch. **⚠️ Confirmed title/content mismatch** — despite the "don't let yourself be fooled" #5xx-style title (previously flagged as a caution bucket), this is a **pure expense-tracking-methodology video**, not a defect critique. Directly high-value for this project's own **self-managed** delivery model — the video explicitly ranks tracking methods by their applicability to exactly this scenario (owner directly managing/paying for materials and labor, not a single turnkey contractor).

## Rules / Heuristics — Renovation Expense-Tracking Methods, Ranked

- **Five distinct expense-tracking approaches, ranked worst to best, each with a specific documented failure mode**:
  1. **Do nothing during the renovation, reconstruct expenses from memory at the end** — worst method; most information (especially rough-material purchases, which can run to dozens of line items) is simply forgotten.
  2. **Collect every receipt as you go, tally them at the very end** — better than nothing, but has three real problems: (a) hard to analyze *during* the project (you only learn a category breakdown — rough/finish/plumbing/electrical — after the fact, not mid-project when you'd want to course-correct); (b) can't answer "how much have I spent so far" at any point mid-project, only "I have half a sack of receipts"; (c) **critically, it misses every cash payment that never generated a receipt** — informal/cheap demolition labor, movers, market-stall delivery fees, and similar off-the-books payments are invisible to this method entirely.
  3. **⚠️ Delegate expense tracking to the crew/contractor doing the work** — flagged as the riskiest method: whoever controls both the money and the record-keeping has a direct incentive to buy at one price and report a different (higher) price on the receipts handed back, pocketing the difference. **And even when done honestly, this method degrades back into method 2** — at reporting time, the contractor just hands the owner the same "sack of receipts" to sort out themselves.
  4. **⚠️ Negotiate a fixed price for rough materials with the contractor, track only finish materials yourself** — reduces analysis granularity (same downsides as methods 2-3), and creates a direct incentive problem: if a contractor agrees to a fixed rough-materials budget (worked example: 10,000 RUB/m² × 70m² = 700,000 RUB total), they're financially incentivized to source *cheaper* materials than budgeted and pocket the difference, not to spend the full amount on quality. **Only viable with a highly trusted, established company that backs the work with a long warranty** (giving them their own incentive not to cut corners that would trigger warranty claims later) — **never use a fixed-rough-materials-price arrangement with an unverified company or a directly-hired informal crew.**
  5. **⚠️ A dedicated spreadsheet-based expense-tracking system (the speaker's own template, described in full structural detail)** — the recommended method, and the one directly applicable to a self-managed renovation:
     - **Summary sheet** aggregating data from every other sheet, organized into 4 blocks: **Primary Expenses** (rough materials, finish materials, electrical, plumbing, windows/balconies, doors — costs without which the renovation can't be completed and the unit can't be used), **Secondary Expenses** (purchases that could be deferred up to a year post-handover: AC indoor units, built-in kitchen, furniture, appliances, light fixtures, accessories/shelving/mirrors/curtains — plus category-dependent items like a full heating-system replacement, which may legitimately be zero on some projects), **Works** (total contracted work cost, amount already paid to the crew, remaining balance), and **Balance** (total handed to the crew for materials, how much of that the crew has actually spent, how much cash remains in the crew's hands).
     - **Per-purchase-category sheets**: each is a simple table — date, item name, quantity, unit price (total auto-calculated), plus a free-text notes column. A closing "delivery" and "loading/unloading" line is added to each completed purchase batch.
     - **Usability features worth replicating in any DIY tracking spreadsheet**: typing "delivery" or "loading" in the item-name column auto-highlights that row (visual separation of logistics costs from material costs); the header row stays frozen/visible when scrolling; a single marked cell in the top-left corner disappears when data has scrolled under the frozen header, serving as a visual "scroll back up" cue; all formula cells are protected/locked so accidental edits can only happen in data-entry cells (protects against a data-entry mistake silently destroying a formula and losing a large tracked sum); each sheet's own subtotal (materials, delivery/loading, and combined total) is pinned near the top rather than requiring a scroll to the bottom of a long list; every sheet has a one-click link back to the summary sheet, and the summary sheet's own row labels link forward to their respective detail sheets.
     - **A dedicated "Payments" sheet**: date, amount-for-materials column, amount-for-work column, running totals per column and combined — **and a notes column tying every payment to a specific memorable event** (documented practice: "we handed over 200,000 RUB when we came to the site to inspect the tub installation") — explicitly recommended as a dispute-prevention practice: an event-anchored note makes it much easier to recall exactly what a payment was for months later, reducing payment-related disputes.
     - **A dedicated "Overrun" (перерасход) sheet**: for any planned-vs-actual substitution (e.g. buying engineered/solid-wood parquet instead of the originally budgeted laminate), record the originally planned item's price and the actual item's price side by side — the difference is the isolated, attributable overrun for that specific decision, rather than a vague "we're over budget somewhere" feeling.
     - **A simplified second template variant** also described: fewer categories (2 primary, 3 secondary, plus the same organizational-expenses/payments/overrun sheets), trading analytical granularity for a spreadsheet that's easier to read chronologically (rough-material purchases naturally cluster early, finish-material purchases cluster later, so a date-ordered flat list reads coherently without needing category-jumping).

## Advertising / Promotional Content Notes

The speaker points to their own website (referenced only as a URL, "3208.ru," in a materials-purchasing section) as where the described spreadsheet templates can be downloaded — a mild self-promotional pointer, but the templates themselves are framed as free downloads, not a paid product being sold in this video. No named-individual dispute content.

## Target Page(s)

Project-management/budgeting-process content — most relevant to `11_Budget_and_Planning` general workflow guidance. This is a genuinely new topic area for this store (no prior source has covered expense-tracking tooling/methodology in this much structural detail).

## Relevance to This Project's Topic

**High** — this project's own delivery model is explicitly self-managed/itemized (hiring individual trades, sourcing materials directly), which is exactly the scenario methods 3 and 4 above warn against relying on, and exactly the scenario method 5's spreadsheet structure is built for. The block breakdown (primary/secondary/works/balance), the payment-event-anchoring practice, and the overrun-isolation sheet are all directly actionable regardless of which specific tool (spreadsheet software) is used to implement them.

## Gaps

- Region: level 2 only (no city stated) — default Moscow assumption per channel convention.
- No cost figures beyond one illustrative worked example (10,000 RUB/m² × 70m² = 700,000 RUB) used purely to demonstrate the fixed-price-incentive problem, not a real project's actual cost.
- No named individual — no legal-dispute exclusion needed.

## Recommended Downstream Routing

`tiered-knowledge-base` — a new Durable Facts subsection (Project Management / Expense Tracking) covering the 5-method ranking and the spreadsheet structure. Given the depth and self-managed-project relevance, also worth a `Budgeting_Guide.md` mention under "What to Check Before Estimating" or a new tracking-practices subsection.

## Promotion self-check

Re-read in full after drafting. All concrete facts/rules/numbers identified during extraction are reflected in the checklist above.
