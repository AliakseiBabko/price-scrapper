---
source_type: video transcript (two-speaker technique demo, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=fSEPr5fpfPM
video_id: fSEPr5fpfPM
transcript_file: _Archive/processed_sources/20260819_kitchen_stubouts_ac_fridge_niche_166_ec2a1580.txt
fetched: 2026-08-19
upload_date: 2022-06-26 (metadata-confirmed via yt-dlp `upload_date`)
channel: Zemsproekt/Zemstandart (Alexey Zemskov, guest: Sergey Saratov, in-house design/renovation lead)
regional_applicability: not stated in-video — level 2/channel-branding only (Moscow, per this channel's established convention)
currency: RUB stated once (design-fee mention only, not a construction/materials price)
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemsproekt/Zemstandart: "How Not to Do Kitchen Renovations With Your Own Hands" — 3 Kitchen Tips (#166, YouTube fSEPr5fpfPM)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Category 4 batch, chunk 2 of ~6. Title matches this channel's usual misleading "how not to" pattern (confirmed again — video is a positive 3-tip technique explainer, not a critique). Three unrelated kitchen sub-topics in one short video: plumbing stub-out group placement, AC placement/sizing, and built-in-style niche sizing for a freestanding fridge.

## Plumbing — Kitchen Stub-Out Group Placement (Trash-Bin Clearance)

- **Kitchen sink stub-out group composition, confirmed**: hot + cold water supply plus a 50mm sewage drain for the sink; a separate cold-water supply plus a 32mm sewage drain for the dishwasher — consistent with this store's existing, more precise `yt_ssS7-TdXhu0` coordinate table (that source gives exact heights/offsets; this source doesn't restate heights, adds a placement rule instead).
- **Stub-out group horizontal placement rule, genuinely new for this store**: the whole plumbing stub-out group should be offset left or right from the sink's own centerline — not centered under it — specifically to leave clear floor space directly under the sink cabinet for a floor-standing trash bin. `confirmed`, explained rationale, complements (does not contradict) the existing exact-coordinate table, which doesn't address this centering-vs-offset design choice.

## HVAC — Kitchen AC Unit Placement & Sizing

- **Kitchen AC placement rule: over the entry doorway, not over a sofa (in a kitchen-living combo) and not over the cooking zone.** Reasoning by elimination: over a sofa in an open kitchen-living layout blows directly on whoever is seated with their back to it while cooking; over the cooking zone conflicts with upper cabinets and blows on whoever is seated on a nearby sofa. Placed over the doorway instead, the cold air stream lands on open floor space, mixes with ambient warm air, and cools the room evenly without anyone being in the direct draft. `confirmed`, explicit reasoning by elimination across placement options, genuinely new AC-placement rule for a kitchen specifically (this store's existing AC placement content covers bedroom/living-room/kids-room, not kitchen).
- **Kitchen AC unit coordinates**: centered on the vertical midpoint of the wall segment above the door (not flush to the ceiling), and centered horizontally directly above the doorway's own centerline (not the wall segment's centerline).
- **Common installer mistake called out**: placing the AC unit in the space between the ceiling and the top of the door frame (i.e. flush-high) rather than centered on the remaining wall segment after door framing — a specific, avoidable vertical-positioning error.
- **Kitchen AC sizing formula: multiply the standard room-sizing formula (used for bedrooms/kids' rooms) by 1.5×.** Reasoning: kitchens have meaningfully more heat sources (appliances, cooking) than a bedroom of the same floor area; sizing a kitchen AC with the standard formula runs the unit permanently near its capacity ceiling, causing premature failure. `confirmed`, explicit multiplier with stated mechanism, genuinely new numeric sizing rule for this store's kitchen-specific AC content.
- **Demand context claim**: ~10% of clients request a kitchen AC unit at the design stage, but the source claims ~90% end up wanting one after move-in once they experience kitchen heat in practice. `unverified`, self-reported company-observation statistic, not independently checkable — record as a company claim, not a market fact.

## Furniture / Built-ins — Freestanding-Fridge Niche Sizing

- **Freestanding-fridge-in-cabinetry niche technique**: when a client wants a freestanding (not built-in) fridge to sit flush in line with the rest of the kitchen cabinetry (rather than protruding into the walkway/doorway), build a dedicated niche recessed behind the cabinet face line to absorb the fridge's extra depth. Reasoning: a quality freestanding fridge is typically slightly over 600mm deep (vs. the kitchen cabinet run's standard 600mm depth) and needs 50-70mm of rear clearance for its compressor/heat exchanger — a niche solves both the depth mismatch and the clearance requirement at once.
- **Niche dimensions**: recess depth 70-100mm behind the main cabinet face line; niche width and height each 50mm larger than the fridge's own external dimensions.
- **Niche finishing detail**: all outer/visible corners of the niche opening get a plastic corner bead (малярный уголок) during framing; the niche's side returns (откосы) and back wall are finished with the same wall-finish material as the surrounding walls, not a separate/contrasting material.

## Advertising / Promotional Content Notes

One explicit design-fee mention (~3,000 RUB/m², described as available "anywhere in the world," directing viewers to the company's own project-ordering site) embedded in the plumbing-tip segment — tag as a direct commercial mention/tier-steering, not neutral technical guidance; the stub-out coordinates and placement rule themselves are still extractable as technique. Otherwise the video is entirely technical content with no other pricing or brand endorsement.

## Target Page(s)

- `12_Engineering_and_Systems/analysis/Fixture_Stubout_Coordinates.md` — add the trash-bin-clearance offset rule alongside the existing precise kitchen coordinate table (complementary design consideration, not a numeric contradiction).
- `12_Engineering_and_Systems/analysis/AC_Key_Concepts_and_Placement.md` and/or `AC_Sizing_and_Selection.md` — new kitchen-specific AC placement rule and 1.5× sizing multiplier; check whether a kitchen sub-section already exists before adding.
- `03_Kitchen/Kitchen_Furniture.md` or `03_Kitchen/Kitchen_General.md` — freestanding-fridge niche sizing (single-file page, append normally).

## Relevance to This Project's Topic

High — three independent, concrete, numeric rules (trash-bin clearance placement, kitchen-specific AC sizing/placement, fridge-niche dimensions) all directly actionable for a self-managed kitchen renovation.

## Gaps

- No region confirmed at level 1 (spoken) — channel-convention-only (Moscow).
- The one design-fee price point given is a company service fee, not a construction/materials price — does not meaningfully affect `Budgeting_Guide.md`.
- The "10% vs 90%" AC-demand claim is an unverifiable company-observation statistic — recorded as a tagged company claim, not adopted as a store-level fact.

## Recommended Downstream Routing

`tiered-knowledge-base` — Plumbing, HVAC, and Kitchen/Furniture sections of the renovation budgeting intermediate store, plus the three wiki pages listed under Target Page(s) above.

## Promotion self-check

Re-read in full after drafting. All concrete facts/rules/numbers identified during extraction are reflected in the checklist above.
