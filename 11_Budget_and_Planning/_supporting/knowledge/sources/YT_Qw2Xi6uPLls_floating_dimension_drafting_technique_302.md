---
source_type: video transcript (real-project hallway full-replan + construction-drafting methodology, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=Qw2Xi6uPLls
video_id: Qw2Xi6uPLls
transcript_file: _Archive/processed_sources/20260819_floating_dimension_drafting_technique_302_275c81e1.txt
fetched: 2026-08-19
upload_date: 2025-04-13 (metadata-confirmed via yt-dlp `upload_date`) — significantly more recent than most sources processed from this channel to date
channel: Zemstandart / Zemproekt (Alexey Zemskov)
regional_applicability: level 2 only (no city named directly in this video's content) — assume Moscow per this channel's usual default, not level-1-confirmed
currency: not applicable — no transaction figures stated
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemstandart/Zemproekt: "Don't Ever Do This In Your Hallway!" (#302, YouTube Qw2Xi6uPLls)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION — standout drafting technique

Remainder-pool Round 2, video 3. **New-build apartment (64m² "euro-3-room")** — squarely in scope. **⚠️ Contains one of the most valuable general planning-documentation techniques found across this entire triage project to date**: a "floating dimension" construction-drawing convention that isn't specific to this hallway, but broadly applicable to any DIY construction-drawing plan.

## Rules / Heuristics — The "Floating Dimension" Drafting Technique (Standout Finding)

- **⚠️⚠️ Major technique: deliberately omit one non-critical dimension from a construction drawing so all cumulative construction tolerance/error lands there, not on a genuinely critical dimension.** The problem this solves: if every segment in a run is separately dimensioned (a reveal, then an opening width, then another reveal, then a wall thickness, then a final segment), an installation crew will start building from whatever reference point is easiest for them (typically a load-bearing wall, working outward once they've decided where the plaster layer will sit) — and by the time they reach the *last* dimensioned segment in the chain, accumulated small construction/plastering tolerance errors will have eaten into exactly the dimension the designer most needed to hold (worked example: a wardrobe's depth, intended to be a firm 600mm, ends up smaller than planned once tolerance has compounded through every other dimension in the chain ahead of it). **The fix**: on the construction drawing, specify only the small number of dimensions that are actually load-bearing/critical (worked example: just "600mm offset from this corner" and "150mm wall thickness" on one sheet; then, on a separate openings sheet, "500mm reveal" and "800mm opening width") — and deliberately leave one specific segment's width *unlabeled*. Because the crew has no dimension to build that segment to, they're forced to build outward strictly from the specified anchor points, and whatever tolerance error exists automatically lands in the one unlabeled ("floating") segment instead of consuming the critical dimension. **The only implicit requirement on the floating segment is that it be wide enough for its own minimum function** (here: just wide enough to fit a standard interior-door casing) — everything else about its exact width is deliberately left to chance. **This is a general construction-documentation principle applicable to any DIY project plan, not specific to this room or channel** — identify which dimensions in a run are truly load-bearing/functionally fixed, dimension only those, and consciously choose one non-critical segment to absorb whatever tolerance error the real-world build introduces.

## Rules / Heuristics — Supporting Case Content

- **Natural-light-path caution for an oversized foyer/hall**: a large, "impressive-looking" entrance hall/foyer can still be a real livability defect if it blocks natural light from reaching it from an adjacent bright room (documented case: a kitchen-living room with two large, low-sill windows sat immediately adjacent to a hall that stayed dark and gloomy anyway, because a wall fully blocked the light path through only a small doorway). **General principle: evaluate a hall/entry wall not just for floor-area efficiency, but for whether it blocks a light path from an adjacent window-rich room** — demolishing/opening such a wall can meaningfully brighten a previously dark zone with no window of its own.
- **80mm paz-greben (tongue-and-groove gypsum-block) partition thickness reconfirmed as inadequate for soundproofing** — a further independent instance of this store's existing 80mm-inadequate finding, demonstrated on camera (visibly flexing/audibly transmitting sound under hand pressure, cracking even through reinforcing fabric).
- **A full entrance-zone functional program, worked as a real client requirement checklist**: coat closet, quick-access changing area, an additional general storage zone, storage for 2 bicycles, a stroller, a water-supply manifold, and an electrical panel — all needing simultaneous placement in one zone. A useful reference checklist for planning any similarly multi-function entrance/storage zone from scratch.
- **Stroller/bike passage clearance**: an 800mm door-opening width was chosen specifically so a stroller and bikes can be moved through comfortably without needing to be walked through sideways or backward — consistent with, and reinforcing, this store's existing minimum habitable-room opening-width figures, but framed here around a specific real access need (stroller/bike passage) rather than a generic "door" requirement.
- **Reveal sized to a specific stored item**: a 500mm reveal next to a storage-zone opening was sized specifically so a stroller fits fully into that space without protruding excessively into the adjacent passage opening — a concrete example of deriving a reveal's width from a real stored-item's footprint, not an arbitrary number.

## Advertising / Promotional Content Notes

Standard channel format, more informal/comedic in tone (a running gag involving someone repeatedly wandering into a toilet during filming), no explicit self-promotional pitch in this particular video (no design-fee or booking-calendar mention). No named-individual dispute content.

## Target Page(s)

The floating-dimension drafting technique is broadly applicable and worth prominent placement — likely a new Planning Rules / Documentation subsection in the intermediate store, and potentially a mention in `Renovation_Sequence.md` (flagged for the user's own manual folding decision, per this wrapper's guardrails, not auto-edited). Supporting content routes to Entrance/Hallway (store-only, per the existing Pending Wiki-Page Decisions entry) and Doors/Trim.

## Relevance to This Project's Topic

**High** — the floating-dimension technique is a genuinely valuable, broadly reusable construction-documentation principle for this project's own self-managed renovation, directly applicable to any DIY plan drawing this project produces for its own crew, regardless of which specific room or dimension is involved.

## Gaps

- Region: level 2 only (no city stated) — default Moscow assumption per channel convention.
- No cost figures — pure planning/technique content.
- No named individual — no legal-dispute exclusion needed.
- Notably more recent upload date (2025-04-13) than most sources processed from this channel — worth noting this channel is still active and producing content well past this project's earlier-processed date ranges.

## Recommended Downstream Routing

`tiered-knowledge-base` — a new, prominently-flagged Durable Facts entry for the floating-dimension technique (Planning Rules bucket). Supporting content to Entrance/Hallway (store-only) and Doors/Trim.

## Promotion self-check

Re-read in full after drafting. All concrete facts/rules/numbers identified during extraction are reflected in the checklist above.
