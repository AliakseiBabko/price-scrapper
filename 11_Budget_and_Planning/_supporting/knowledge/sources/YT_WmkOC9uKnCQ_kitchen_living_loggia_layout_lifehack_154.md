---
source_type: video transcript (single-speaker technical-design planning walkthrough, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=WmkOC9uKnCQ
video_id: WmkOC9uKnCQ
transcript_file: _Archive/processed_sources/20260819_kitchen_living_loggia_layout_lifehack_154_3d53c22f.txt
fetched: 2026-08-19
upload_date: 2021-10-31 (metadata-confirmed via yt-dlp `upload_date`)
channel: Zemstandart / Zemproekt (Alexey Zemskov)
regional_applicability: level 2 only (no city named directly in this video's content) — assume Moscow per this channel's usual default, not level-1-confirmed
currency: not applicable — no transaction figures stated
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemstandart/Zemproekt: "Best Kitchen-Living Room Life Hack" (#154, YouTube WmkOC9uKnCQ)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Remainder-pool batch, video 3 of the current small batch. **New-build apartment, free-plan layout ("свободная планировка"), 79.5 m²** — squarely in scope. Dense, numeric-heavy technical-design walkthrough, exactly the "technique-format, likely dense" profile flagged in the tracking file. High-value: a full worked planning sequence with many concrete measurements.

**⚠️ Same-project overlap detected**: this video's radiator-niche formula (850mm clearance, niche = grille back-mount dims + 5mm, 1000×600mm→1005×605mm worked example) and its "+800mm opening width" figure are **near-identical to `yt_CHCB4KPupyc`** (#156, same channel, same 79.5m² apartment, already in this store — see `14_Furniture/analysis/Wardrobe_Worked_Cases.md`). This is almost certainly the same real project documented across two different videos (a bedroom/wardrobe video and this kitchen-living-room video), not two independent sources. **Treated as corroboration of an existing store entry, not a new independent data point** — flagged accordingly below and in the store Change Log.

## Rules / Heuristics — Kitchen-Living Room Combined Layout, With Numeric Sequence

- **Structural-survey-before-demo practice**: the design team physically opens shafts/ducts/boxes with hammers/rotary hammers during measurement to determine what can actually be removed, rather than trusting drawings alone — framed as a differentiator ("unfortunately, nobody else does this") and worth noting as a general due-diligence practice for any pre-demo survey, self-managed included.
- **Partition wall between a kitchen-living room and adjacent rooms**: minimum **150mm thick** for adequate soundproofing.
- **Door/opening in a perpendicular wall segment**: **900mm** opening width, with **100mm returns** on each side (so the wall segment housing it needs at least 1100mm total run).
- **Kitchen cabinet run depth**: **600mm**.
- **Plumbing rough-in coordinate sequence for a kitchen sink + dishwasher wall** (a reusable ordering rule, not just this project's specific coordinates): hot water outlet for the sink first; cold water outlet for the same sink placed to its right; cold **drinking** water outlet placed below that; cold water outlet for the dishwasher placed below that. Two drain (slив) outlets on the same wall: one for the sink, one for the dishwasher.
- **Sofa placement clearance sequence**: measure **1250mm** from the neighbor-adjacent wall to define the sofa's zone, then a further **800mm** beyond that to define an opening/door width.
- **Rough floor threshold height**: **100mm** (raised рough-floor level at a threshold/doorway transition in this project).
- **Radiator niche formula**: from the finished floor, minimum **850mm** clearance before the niche starts; the niche itself begins **100mm** down from its own top edge; niche dimensions should be **exactly 5mm larger** than the radiator grille's mounting (rear-seat) dimensions, **not** the grille's visible/decorative face dimensions — explicit warning that grille size specs are always given by rear-seat dimensions, not the decorative overhang. Worked example: a 1000×600mm grille needs a 1005×605mm niche.
- **Balcony-block door-opening design rule**: never shrink the sofa clearance zone (back+seat depth) to enlarge the window/light opening next to a balcony door — the clearance zone is a fixed minimum (sofa back here, seat there), and shrinking it either forces the sofa into the door's swing path or blocks the balcony door leaf's own opening direction (context: this door could only swing one direction).
- **Loggia zoning fix, general pattern**: when a loggia's entry-door position forces the closet/storage to be reached only by walking the loggia's full length (or crawling under drying laundry when a ceiling drying rack is in use), relocate the loggia access point so a large closet on one side and an additional storage zone on the other are both directly reachable — result stated: went from 0 usable storage zones on the loggia to 2, without the walk/crawl-through problem.
- **Loggia lighting placement**: centered on the balcony block (not offset).
- **Switch group placement**: cluster switches near the sofa, controlling two separate lighting circuits (kitchen zone, loggia zone) from one location.
- **Balcony-door-slope (откос) socket rule**: at least two sockets on the balcony door slope — stated with a joking "channel-signature" framing but consistent with genuine practical need (loggia-zone devices/lighting).

## Advertising / Promotional Content Notes

Standard technical-design teaching framing, no company/brand promotion beyond the channel's own persona, no sponsor mentions, no named-individual dispute content. The "two sockets on the slope, or nobody will believe you're watching an Alexey Zemskov video" line is a self-aware channel-signature joke, not a factual claim — noted, not extracted as a rule beyond the underlying practical socket-count recommendation.

## Target Page(s)

Dense numeric planning-rule source spanning several buckets: Kitchen (depth, plumbing sequence), Walls/Ceilings (partition thickness), Doors/Trim (opening width/returns), Electrical (switch clustering, socket placement), Plumbing (rough-in coordinate order), Balcony/Loggia (zoning fix, lighting), Living/Dining (sofa clearance, radiator niche formula). Route each numeric rule to its matching existing wiki page/analysis file; the radiator-niche formula and plumbing-rough-in-order rules in particular look like genuinely new, previously-unrecorded numeric data worth their own Numeric Data store lines.

## Relevance to This Project's Topic

High — this project is a new-build, self-managed renovation, and this source is a genuinely dense, numeric, checkable planning walkthrough of exactly the kind of combined kitchen-living-room-plus-loggia layout this project may need to plan itself. Several formulas (radiator niche sizing, plumbing rough-in order, partition thickness) are directly actionable regardless of the specific apartment's layout.

## Gaps

- Region: level 2 only (no city stated) — default Moscow assumption per channel convention.
- No cost figures — pure planning/technique content.
- No named individual — no legal-dispute exclusion needed.
- Some measurements (1250mm sofa clearance, 900mm door opening) are specific to this apartment's exact furniture/dimensions rather than universal constants — flag as "example values from this project" rather than hard rules, except where explicitly framed as a minimum/formula (150mm partition min, 600mm depth, radiator niche +5mm formula, 100mm returns).

## Recommended Downstream Routing

`tiered-knowledge-base` — multiple Rules/Heuristics and Numeric Data entries across Kitchen, Plumbing, Electrical, Balcony/Loggia, and Doors/Trim buckets. Wiki-route each to its matching page/analysis file per the intake skill's 5a step — this is a genuinely multi-page-touching source given the room-combining scope.

## Promotion self-check

Re-read in full after drafting. All concrete facts/rules/numbers identified during extraction are reflected in the checklist above.
