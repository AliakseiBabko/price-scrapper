---
source_type: video transcript (turnkey company channel, self-calculation smeta walkthrough, Russian, ASR auto-generated captions)
source_url: https://www.youtube.com/watch?v=Y08zvnbxdM0
video_id: Y08zvnbxdM0
transcript_file: _Archive/processed_sources/20260825_anatolich_smeta_selfcalc_methodology_bd44d55a.txt
fetched: 2026-08-25
upload_date: 2020-06-20 (metadata-confirmed)
channel: "Ремонт и Строительство Anatolich Group" (as-group.pro)
source_metadata_location: .pro domain, no city named in description (level 2 at most)
spoken_project_location: none — no city/region named anywhere in the transcript
regional_applicability: unresolved — do not cite as Minsk/Belarus- or any specific-city-equivalent
currency: RUB (inferred from channel context; no explicit currency figures are spoken in this particular video — it demonstrates the spreadsheet mechanics, not worked prices)
language: ru (auto-generated captions)
extraction_taxonomy: custom (renovation planning)
fact_yield: 3
promotional_ratio: high
corroborates_existing: false
---

# Extraction Note — Anatolich Group: How to Calculate Your Own Renovation Estimate (YouTube Y08zvnbxdM0)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external/domain validation (none performed, no numbers to cross-check).

## Advertising / Promotional Content Flag

**Turnkey company's own channel** (Anatolich Group, as-group.pro). The entire video is a walkthrough of the company's own downloadable Excel/Bitrix-based smeta spreadsheet template, offered as a free lead-magnet download (link in description) alongside a direct pitch to hire the company for the actual renovation. No genuinely independent/neutral demonstration — this is product marketing for the company's own estimating tool. **High promotional ratio, thin content** — under 3 minutes of narration, most of it walking through UI mechanics rather than substantive renovation knowledge. Cleared the value-filter only `partial` (methodology, not the actual template file itself, since the download link was not fetched — see Gaps below).

## Renovation Delivery Model & Scope

**Self-Managed / Itemized-relevant tooling** — despite being a turnkey company's own product, the spreadsheet's structure (per-room, per-line-item price catalog with quantities driven by measured dimensions) is exactly the shape a self-managed buyer would want for their own smeta, not a bundled turnkey quote. The tool itself is delivery-model-agnostic; only its *origin* (a turnkey company's marketing funnel) is turnkey-flavored.

## Durable, Reusable Content — Self-Service Smeta Spreadsheet Structure (Level 1)

- **Room-by-room tab structure**: each room ("комната 1, 2, 3", "ванная," "туалет") gets its own set of dimension inputs (length, width, height, and each opening — door/window — width×height) feeding into that room's own line-item price list. **Bathroom and WC rooms carry an expanded/longer price list specifically for sanitary/plumbing-related work items**, not present on the standard room tabs — a structural distinction worth replicating in any self-built smeta template.
- **Auto-calculated geometry from raw room dimensions** (worked example: 2m × 3m room, 3m ceiling height, one door opening ~2m² + one window opening ~1.5m²): perimeter = (length + width) × 2 (worked: (2+3)×2 = 10m); floor area = length × width (worked: 2×3 = 6m²); **wall area = perimeter × height, minus the total area of door/window openings** — deriving the actual paintable/tileable wall surface automatically from four numbers (length, width, height, opening dimensions) rather than requiring the user to compute wall area by hand for every room. `confirmed`, directly demonstrated on camera.
- **Filterable master price list drives the summary total**: a filter view surfaces the full catalog of priced work items (organized by trade/stage — demolition, wall finishing, flooring, ceiling); the user checks off which items apply to a given room (worked example: demolition of baseboard, laminate/parquet flooring, wallpaper removal, plastic window-reveal/sandwich-panel removal, ceiling baseboard removal, ceiling-panel removal) and the spreadsheet multiplies each checked item's unit rate by the room's auto-calculated or manually-entered quantity (most quantities auto-fill from the geometry above; a few line items — e.g. window-reveal linear length — require a manual quantity entry per the worked example, ~2 linear meters). All checked/quantified line items roll up into a single running grand total ("сводная") across every room. `confirmed`, directly demonstrated.

## Gaps

- The actual downloadable smeta template file itself (linked from the video description, `as-group.pro/smeta`) was **not fetched or examined** — per this project's standing web-source rules, a company's own lead-magnet download would need the same rendered-fetch/evidence-preservation treatment as any other company-website source before being cited as a template artifact in its own right. This extraction note only captures the *structure/mechanics* demonstrated verbally and on-screen in the video, not the file's actual formulas/content.
- No prices, currency figures, or $/m² data are spoken anywhere in this video — it is pure spreadsheet-mechanics demonstration, not a pricing source.

## Relevance to This Project's Topic

Directly relevant to the "self-calculate a smeta" gap this batch targets: the room-by-room dimension-driven, filterable-price-list, auto-totaling structure is a concrete, reusable *template shape* a self-managed buyer could replicate in their own spreadsheet, independent of this specific company's product. Thin on its own (single short video, no real numbers), but complements `YT_cdNwbqsLUK4_remonthochu_smeta_methodology.md`'s smeta-literacy rules (what to verify in a smeta) with a concrete answer to "how is a smeta spreadsheet actually built/calculated."
