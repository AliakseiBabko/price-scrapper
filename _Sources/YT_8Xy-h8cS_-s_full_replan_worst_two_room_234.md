---
source_type: video transcript (single-speaker real-project full-replan walkthrough, detailed numeric planning-logic masterclass, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=8Xy-h8cS_-s
video_id: 8Xy-h8cS_-s
transcript_file: _Archive/processed_sources/20260819_full_replan_worst_two_room_234_708bf8d9.txt
fetched: 2026-08-19
upload_date: 2023-09-05 (metadata-confirmed via yt-dlp `upload_date`)
channel: Zemstandart / Zemproekt (Alexey Zemskov)
regional_applicability: level 2 only (no city named directly in this video's content) — assume Moscow per this channel's usual default, not level-1-confirmed
currency: not applicable — no transaction figures stated
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemstandart/Zemproekt: "The Worst Two-Room Apartment I've Ever Seen!" (#234, YouTube 8Xy-h8cS_-s)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Remainder-pool batch, video 4 of the current small batch. **New-build, free-plan apartment — an unusually detailed numeric planning-logic masterclass**, one of the densest and most methodical sources in this remainder pool (the speaker narrates his own wall-by-wall reasoning sequence, including self-corrections). **⚠️ Title-similarity duplicate-risk check performed**: the tracking file flagged this video's title as very close to `1pU60p0Jh3A` ("The worst two-room apartment I've ever seen!!!" #228) — **not yet processed in this session**, so the duplicate/reused-script check against it is still outstanding; do not assume independent value from that pairing until both are compared.

## Rules / Heuristics — Developer Defects Documented

- **⚠️ A single continuous wall plane built from two materially different constructions**: one documented wall combined a 200mm-thick aerated-concrete-block section with a 100mm-thick aerated-concrete section *in the same plane* — and a second wall combined brick with aerated concrete block, again in one continuous plane. **General red flag distinct from the already-documented wall-plane-offset problem**: verify not just that a wall's plane is flat, but that its actual material/construction is consistent along its full run — a materially inconsistent wall can carry different structural/thermal/acoustic properties from one end to the other even where it looks visually flat.
- **A WC opening's raw clear width can look adequate but leave almost no usable space once finished**: documented case — 65.9cm clear width *before* plastering/leveling/tiling, built from 60cm-wide aerated-concrete block, described as leaving barely enough room to sit on the toilet without hitting your elbows once finish layers are added. Corroborates this store's existing WC-too-narrow findings with a fully worked before/after-finish numeric example.

## Rules / Heuristics — Redesign Technique, Detailed Numeric Sequence

- **⚠️ Sequencing exception**: screed is formed and leveled across the general apartment floor early in the process, but **explicitly skipped on the loggia**, where a podium will be built instead to provide insulation — a screed-vs-podium sequencing distinction not previously recorded this specifically in this store.
- **⚠️ Asymmetric tile+adhesive compensation technique, fully worked**: when sizing a raw (pre-finish) wall-to-wall opening that will be tiled on both sides, add tile+adhesive buildup **per wall, not a flat blanket number** — a freshly rebuilt, flat wall needs only ~15mm compensation per side, but an existing, uneven surface that can't be demolished (e.g. a crooked ventilation shaft face) needs closer to 25mm to also absorb its own unevenness. Worked example: target net clear width 1000mm → raw dimension set to 1040mm (15mm for the flat rebuilt wall + 25mm for the crooked shaft face), not a naive flat 1030mm (15mm+15mm) that would leave the finished space narrower than intended on the crooked side. **General rule: don't assume symmetric tile-buildup compensation — check each bounding surface's own flatness and compensate accordingly.**
- **Sink-to-future-tiled-wall clearance: minimum 15mm** — leave this gap when placing a sink/plumbing point near a wall that will later be tiled, verified *before* finalizing plumbing rough-in points, not after.
- **⚠️ Default partition-thickness matrix, with an explicit infrastructure-priority override**: **150mm between two habitable rooms** (bedroom-to-living-room, etc.); **100mm for all other walls** (bathroom/WC dividers, closet dividers) as the default. **Explicit override**: even a wall separating two closet/storage zones — where a thinner wall would obviously yield more storage space on the surface — should still be built to 150mm if that wall needs to house mandatory infrastructure (a water-supply manifold, an electrical distribution panel). **General prioritization rule, stated explicitly**: infrastructure-housing need outranks incremental storage-space gain, even when the "obvious" critique (thinner wall = more storage) looks correct at first glance.
- **⚠️ Door-opening-width-is-fixed, reveal-width-is-flexible planning priority**: when sizing a door opening, the **opening width itself is the fixed, non-negotiable number** (worked examples throughout this video: 800mm for habitable-room doors, 900mm for the entrance door, 700mm for a pantry/closet door) — the **reveal/return on either side simply absorbs whatever space is left over from the available wall run, as long as neither return drops below a 100mm floor** (a return under 100mm forces the door casing/trim to be notched or trimmed to fit, an avoidable complication). Reveals do not need to match a specific target number themselves, only stay ≥100mm and (where both sides are visible together) look visually balanced.
- **⚠️ Counterintuitive passage-opening-width rule**: a wider opening between a kitchen-living room and an adjoining hallway/foyer **does not "cost nothing" for the sake of comfortable passage** — opening width and its flanking reveals both subtract directly from the adjoining room's own footprint (here, a bedroom). **General planning priority, stated explicitly**: don't oversize a passage opening beyond its true functional minimum "to feel more generous," because every extra millimeter of opening/reveal width comes directly out of the floor area of the room people actually spend time in — keep passage openings at their functional minimum (here: 800mm) rather than a feel-good wider default.
- **Closet-behind-a-door depth-maximizing placement technique**: positioning a closet directly behind a door opening (rather than beside it) and pushing the opening itself to one extreme edge of the available wall run (here: offset 100mm from one edge) maximizes the closet's own depth, since the entire remaining wall run beyond the opening's reveal goes to the closet. Worked result: 700mm maximum closet depth from this technique on a wall run that would have yielded much less with the opening centered.
- **Kitchen-module cost-neutral filler-strip technique**: kitchen cabinet modules should be sized to a standard 600mm width; any leftover gap in the available run should be filled with non-standard-width filler strips (вставки), not non-standard-width modules — **filler-strip width doesn't affect price, but non-standard module width does.** A directly actionable kitchen-budgeting tip: always keep the actual cabinet modules at standard widths and absorb layout irregularity in the (free-width, cost-neutral) filler strips instead.
- **Washing-machine/dryer stack concealed inside a hallway closet rather than the kitchen** — an explicit acoustic-comfort decision (keeping appliance noise out of the living/entertainment space) rather than a utility-convenience one. **⚠️ Regulatory-compliance caveat**: the speaker is deliberately evasive when asked directly whether this placement is fully code-compliant ("legal, if you know what you're doing" — non-answer), which reads as an acknowledged gray area, not a confirmed-compliant technique. Do not extract this specific placement as an endorsed, code-clean practice — record only as a real, if legally ambiguous, design choice this practitioner made.
- **Toilet-cistern/sewer-bend concealment box sizing**: a drywall boxing built flush with a ventilation-shaft face was sized deep enough to conceal both the in-wall cistern (инсталляция) *and* the sewer pipe's bend as it curves to meet the riser — reinforces this store's existing "size a concealment box for the full manifold/bend requirement, not the minimum pipe diameter" heuristic with an independent worked example.
- **Bedroom acoustic layer against a neighbor-shared (party) wall: 50mm sound-insulation buildup** — a distinct figure from the well-established 150mm interior-partition soundproofing default; this is an added acoustic layer on an *exterior/neighbor-facing* wall, not an interior partition between two of this apartment's own rooms.
- **⚠️ Deliberate top-down design self-review practice, demonstrated on camera**: after completing a first-pass layout that otherwise looked "done," the speaker explicitly reviews the whole plan from above and catches two real problems that weren't visible while designing each zone individually — (1) a wardrobe/nightstand furniture conflict forcing an awkward, unevenly-sized door-panel mechanism, and (2) an actual storage gap (insufficient quick-access coat storage near the entrance despite a makeup zone and some hanging space already being present) — then redesigns that entire zone from scratch rather than patching around the conflict. **General practice worth adopting**: after a first-draft room-by-room layout is complete, do one deliberate top-down pass specifically hunting for cross-zone furniture conflicts and secondary storage gaps that don't surface until the whole plan is viewed together.

## Advertising / Promotional Content Notes

Explicit, repeated self-promotion for the speaker's own design-service website (zems.pro), framed candidly at the start ("watch this, then go order a professional project") — more directly promotional than most sources in this remainder pool, though the underlying numeric content itself is genuinely instructive and independent of the pitch. No named-individual dispute content.

## Target Page(s)

Extremely multi-topic dense source: Walls/Ceilings (material-inconsistency red flag, partition-thickness matrix, tile-buildup compensation technique, acoustic-layer figure), Doors/Trim (opening-width-fixed/reveal-flexible rule, passage-opening-vs-room-area tradeoff), Kitchen (module/filler-strip cost technique), Furniture/Built-ins (closet-behind-door depth-maximizing technique), Plumbing (sink clearance, cistern/bend concealment sizing), Planning Rules (deliberate self-review practice — a process discipline, not a numeric rule).

## Relevance to This Project's Topic

High — an unusually rich and methodical numeric-planning-logic source with several genuinely reusable formulas and one valuable process-discipline practice (the deliberate top-down self-review pass) that applies to any DIY layout planning, independent of whether the specific dimensions match this project's own apartment.

## Gaps

- Region: level 2 only (no city stated) — default Moscow assumption per channel convention.
- No cost figures — pure planning/technique content, aside from the module-vs-filler-strip pricing note (relative, not absolute).
- No named individual — no legal-dispute exclusion needed.
- The washing-machine-in-hallway-closet placement's code-compliance status is genuinely ambiguous per the source's own evasive framing — flagged `uncertain`, not to be cited as an endorsed compliant practice.
- **Outstanding duplicate-risk check**: this video's title is very close to the still-unprocessed `1pU60p0Jh3A` — compare both once that video is processed, per this project's standing practice for near-duplicate titles.

## Recommended Downstream Routing

`tiered-knowledge-base` — multiple Rules/Heuristics entries across Walls/Ceilings, Doors/Trim, Kitchen, Furniture/Built-ins, Plumbing, and a Planning Rules process-discipline note. Wiki-route per the intake skill's 5a step.

## Promotion self-check

Re-read in full after drafting. All concrete facts/rules/numbers identified during extraction are reflected in the checklist above.
