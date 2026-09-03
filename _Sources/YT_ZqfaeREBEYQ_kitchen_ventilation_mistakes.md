---
source_type: video transcript (technical tips, Russian, manually-created captions via youtube-transcript-api)
source_url: https://www.youtube.com/watch?v=ZqfaeREBEYQ
video_id: ZqfaeREBEYQ
transcript_file: _Archive/processed_sources/20260810_kitchen_ventilation_mistakes_80d8c9ef.txt
fetched: 2026-08-10 (anonymous youtube-transcript-api, zero prior failed attempts this run — confirms the 429/IP-block seen 2026-08-05 had fully cleared by this date)
upload_date: 2022-07-17 (confirmed via yt-dlp metadata, 2026-08-10 — video is ~4 years old as of processing)
channel: Zemstandart / Zemsproekt (Alexey Zemskov, technical content presented by Сергей Саратов, "design and renovation" lead) — Moscow-based per user-confirmed channel identity (see [[00_Master/exchange_rates_reference|Exchange Rates Reference]] memory)
source_metadata_location: Moscow — per prior explicit user statement, and since independently confirmed (2026-08-10) via the company's own website (`zems.pro/about/` — Moscow and Podolsk office addresses, founding history from 2003, expanded beyond Moscow only from 2018+)
language: ru
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
---

# Extraction Note — Zemstandart/Zemsproekt: Three Kitchen Ventilation Mistakes (#168, YouTube ZqfaeREBEYQ)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

- Solo technical-expert video, Sergey Saratov (Zemskov's design/renovation lead) presenting three kitchen-ventilation mistakes, handed off from host Alexey Zemskov. Clean, grammatical manual captions (unlike the companion `HX2pDdILM7U` source from the same original playlist, which was unusually garbled despite the same captions-flag).
- Self-promotional: Sergey directly advertises his own design-project service (see Numeric Data) mid-video.
- **Turnkey/Full-Service** delivery model — company's own design/renovation service.

## Walls / Ceilings — Durable Facts & Rules

- **Duct cross-section is a noise-vs-ceiling-drop tradeoff, not simply "bigger is quieter."** A larger cross-section duct reduces noise, but a box that's merely wider (not thicker) doesn't help — the duct **must be thick**, and a thick duct box lowers the ceiling more than a wide one. Standard cross-section for most systems: **55×110 mm**. A powerful exhaust hood run through a standard 55×110 duct will be very noisy; for a powerful hood, the recommended cross-section is **250×55 mm** (i.e. wider/flatter, not simply "bigger" — same underlying tradeoff). `confirmed`, single-account.
- **Duct length is a separate noise driver from cross-section**: the longer the run from the forced-exhaust point to the shaft, the noisier it gets — illustrated with a real project's 3D model showing a ~4 m run. `confirmed`.
- **Ceiling-drop rule of thumb**: the ceiling typically drops **~40 mm more than the duct box's own thickness**, because electrical cable conduit runs alongside/above the duct in the same concealed space. This additional drop must be pre-calculated in the design project so it isn't discovered as a surprise after the renovation is finished (framed as: "so you don't end up able to touch the ceiling with your hand"). `confirmed`, a concrete, checkable planning rule.
- **Duct boxes should always get added self-adhesive soundproofing**, regardless of how thick/wide the box already is — a duct box is never fully soundproof on its own. Material spec: self-adhesive, **minimum 3 mm thickness**. `confirmed`.

## Kitchen / Plumbing (Ventilation) — Durable Facts & Rules

- **Combining natural (passive) exhaust and forced (powered) ventilation in the same system creates an inevitable conflict unless a check valve (backflow damper) is installed.** Without one, activating forced exhaust pushes air back through the path of least resistance — commonly out through the natural-vent opening — which can spread kitchen odors faster rather than removing them. **This directly corroborates this store's existing check-valve/backflow fact** (from a different, non-Zemstandart kitchen-hood source already in `12_Engineering_and_Systems/HVAC_and_Ventilation.md` — see that page's Do's table) — now a second, independent source for the same mechanism. `confirmed`.

## Numeric Data

- **Design-project fee: 3,000 RUB/m² (as of 2022-07-17, this video's confirmed upload date)**, stated by Sergey as his own service's flat rate, "anywhere in the world" (i.e. remote design service, not tied to a specific city for delivery, though the channel/pricing itself is Moscow-based per this project's established convention). **A fourth distinct design-fee reference point** in this store, alongside the existing Бородатый Прораб three-tier design pricing (4,000/5,000/7,000 RUB/m², Moscow) — this one is markedly cheaper than even that source's basic tier; keep as a separate data point, not blended. **This project's own company website (`zems.pro/development/`, checked 2026-08-10) currently states 5,000 RUB/m² for apartment design projects** — a ~67% rise over the ~4 years since this video, plausible ordinary price inflation for this market (~13.5%/year compounded), not a same-time contradiction; recorded as a price-history pair (2022 → 2026), not an unresolved conflict. See this store's Numeric Data / Cross-Source Comparison entries for the paired figures. `confirmed` as spoken; `single-account`/self-promotional (a direct service advertisement mid-video).
- **Standard duct cross-section**: 55×110 mm (most systems). **Powerful-hood duct cross-section**: 250×55 mm. **Ceiling-drop delta**: ~40 mm beyond the duct box's own thickness (electrical conduit allowance). **Soundproofing material spec**: self-adhesive, ≥3 mm thick.

## Assumptions / Uncertainties

- The "anywhere in the world" framing for the design-project service is the speaker's own marketing claim — treated as a self-promotional service ad, not evidence this figure applies broadly outside this company's own offering.
- No explicit currency/region restatement in this specific passage beyond "рублей" — region/currency (Moscow, RUB) carried forward from this project's established Zemskov/Zemstandart convention, not independently re-verified in this transcript.

## Relevance to This Project's Topic

Second Zemstandart source (after the companion `HX2pDdILM7U`) from the small original playlist processed 2026-08-05/2026-08-10. Complements this store's existing HVAC/ventilation content with concrete duct-sizing/soundproofing numbers and a second independent source for the natural+forced-ventilation check-valve requirement. Also contributes a fourth, notably-cheaper design-fee data point for the Cross-Source Comparison table.
