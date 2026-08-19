---
source_type: video transcript (single-speaker real-project full-replan walkthrough, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=v7UXJ5fJ0H0
video_id: v7UXJ5fJ0H0
transcript_file: _Archive/processed_sources/20260819_worst_apartment_2019_replan_520_0ce7b02e.txt
fetched: 2026-08-19
upload_date: 2020-03-15 (metadata-confirmed via yt-dlp `upload_date`)
channel: Zemstandart / Zemproekt (Alexey Zemskov)
regional_applicability: level 2 only (no city named directly in this video's content) — assume Moscow per this channel's usual default, not level-1-confirmed
currency: RUB (one uncertain aggregate figure, see Gaps)
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemstandart/Zemproekt: "The Worst Apartment of 2019" (#520, YouTube v7UXJ5fJ0H0)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Remainder-pool batch, video 1 of the current small batch. **New-build apartment (111.5 m²), full design + build project (both proект and ремонт by the same channel)** — squarely in scope. **⚠️ Confirmed title/content mismatch**: despite the "worst apartment of 2019" dunk-style title and the #5xx numbering flagged as a caution in the tracking file, this is a substantive, positive full-replan case study — not off-topic, not thin. Metadata upload date (2020-03-15) also confirms the #5xx numbering on this channel doesn't reliably indicate a later/different video series, contrary to the working hypothesis from the earlier `LVerbq1hkxg` (#549) finding — that video's off-topic content was a one-off, not evidence #5xx numbers are systematically riskier.

## Rules / Heuristics — Real Full-Replan Case, Several Techniques

- **⚠️ Developer-built non-perpendicular wall (135° instead of 90°) between kitchen and an adjacent corridor cost the kitchen roughly 1.10m of usable width** — the wall was demolished and rebuilt at a true 90° angle, directly recovering that width without shrinking any other room, since the "lost" area had only been feeding an oversized, functionally useless corridor. **General principle: verify every wall's actual angle before accepting a developer's layout as fixed** — a small angular deviation compounds into a large usable-area loss over a wall's full length, and if left uncorrected (even by a few degrees), causes a visible seam misalignment once kitchen cabinetry is installed against it.
- **⚠️ A door opening positioned on the diagonal corner of a room can leave the door with literally no valid swing direction** — the documented case: a bathroom door, as originally positioned by the developer, would have conflicted with the kitchen entrance, the bedroom exit, the sink, or the towel warmer depending on which way it swung — every option failed. Fix: reposition the opening (not just re-hang the door) so the leaf can open against a clear wall section with none of those conflicts. A general diagnostic: if a door opening can't be swung any direction without a conflict, the fix is almost always relocating the opening itself, not compromising on a "least-bad" swing direction.
- **⚠️ A shower stall's clear space is highly sensitive to small dimensional changes — a mere 10cm of extra width (from moving one wall 10cm) was the specific difference between "usable, if snug" and "genuinely too tight to use without hitting the fixtures with your elbows."** A concrete data point for shower-stall minimum clearance planning: treat 10cm increments near the minimum threshold as meaningfully consequential, not negligible, when space is tight.
- **Loggia upgrade technique, several steps combined**: (1) verify the loggia's existing wall composition/material before joining it (not just visually joining, actually check what's behind the finish); (2) removing a substantial existing insulation layer that turns out to be unnecessary once the loggia is properly warmed can itself recover usable floor area — documented gain: ~10cm on each side, summing to roughly 1 additional m²; (3) replace any cold/wind-only glazing (a sliding aluminum system providing only wind/precipitation protection, no thermal insulation) with warm glazing as part of the same join. A "cold" (holodnaya) loggia the developer only wind-glazed is not automatically a small space once joined and re-insulated correctly — it can end up meaningfully larger than its as-delivered footprint suggests.
- **Wardrobe/closet wall-shift technique**: an L-shaped storage run that doesn't fit in its allotted space (one leg extends into a door opening, the other leg is 50cm too short) can be fixed by shifting the bounding wall outward — documented case: shifted 20cm, which **simultaneously** enlarged the wardrobe to full functional capacity (10-15 hanging garments instead of half that) **and** left the adjoining corridor at a still-generous 1.40m width. Worth noting as a case where a wall move plausibly seemed like a corridor-width tradeoff but wasn't, once actually measured.
- **⚠️ Entrance-vestibule reclamation technique, with an important safety caveat**: a small mudroom/vestibule area (documented: roughly 1-1.5m² in this case) can sometimes be reclaimed from a shared building corridor/stairwell landing space by moving the true apartment entry door outward into what was previously common-area space — described as "always worth it, even at some risk of being required to reverse it" (i.e., not risk-free, a building-management/HOA pushback risk exists). **Critical caveat, stated explicitly**: never let this kind of reclamation block or obstruct anything that must remain accessible to any person (implicitly: emergency personnel, maintenance access, communal utility points) when the occupant isn't home — that boundary should never be crossed regardless of the space gained. This is Moscow-apartment-block-specific in its exact mechanism (multi-unit floor landings), but the general principle (a shared-space reclamation opportunity exists at many entry configurations, bounded by a hard life-safety/access constraint) is broadly transferable.
- **ROI framing for a paid design project**: the speaker's argument is that a design fee (stated elsewhere on this channel as roughly 50,000 RUB) pays for itself many times over through recovered usable area alone — in this case, an estimated 5 m² that would otherwise have been wasted, valued at a stated but ASR-garbled figure (approximately 300,000 RUB, `uncertain` — the exact wording didn't transcribe cleanly). Treat the ratio (design fee vs. recovered-area value) as the durable point; the specific 300,000 RUB figure should not be cited as confirmed.

## Advertising / Promotional Content Notes

Standard channel format — real client project (named only by first name, "Павел," not a full-identity legal-dispute exclusion case), a design-fee ROI pitch at the close, no third-party sponsor content, no named-individual dispute content.

## Target Page(s)

Multi-topic real case: Kitchen/Walls-Ceilings (wall-angle defect), Bathroom/WC (door-swing diagnostic, shower clearance), Balcony/Loggia (insulation-removal + re-glazing technique), Furniture/Built-ins (wardrobe wall-shift), Entrance/Hallway (vestibule-reclamation technique with the safety caveat).

## Relevance to This Project's Topic

High — a dense, positive, new-build full-replan case with several genuinely new, broadly-applicable techniques (wall-angle verification, door-swing-conflict diagnostic, loggia insulation-removal-for-area-gain, entrance-vestibule reclamation with its safety boundary) not previously recorded in this store in this combination.

## Gaps

- Region: level 2 only (no city stated) — default Moscow assumption per channel convention.
- The ~300,000 RUB recovered-area-value figure is ASR-garbled and not confirmed — recorded as `uncertain`, not used for any pricing benchmark.
- No named individual beyond a first name — no legal-dispute exclusion needed.
- The entrance-vestibule-reclamation technique's exact legality/reversibility risk is building-management-specific and not independently verified beyond the source's own framing.

## Recommended Downstream Routing

`tiered-knowledge-base` — multiple Rules/Heuristics entries across Kitchen, WC/Bathroom, Balcony/Loggia, Furniture/Built-ins, Entrance/Hallway. Wiki-route each per the intake skill's 5a step.

## Promotion self-check

Re-read in full after drafting. All concrete facts/rules/numbers identified during extraction are reflected in the checklist above.
