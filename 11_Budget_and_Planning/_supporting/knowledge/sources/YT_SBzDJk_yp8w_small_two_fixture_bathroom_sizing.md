---
source_type: video transcript (dense technical how-to with precise dimensions, user-supplied Turboscribe transcription — no caption track via youtube-transcript-api/yt-dlp)
source_url: https://www.youtube.com/watch?v=SBzDJk_yp8w
video_id: SBzDJk_yp8w
transcript_file: _Archive/processed_sources/20260810_small_two_fixture_bathroom_sizing_aa1b3a59.txt
fetched: user-supplied 2026-08-10 (originally attempted 2026-07-31, logged `skipped` — no captions — run_20260731_40, now superseded)
upload_date: 2021-08-22 (confirmed via yt-dlp metadata)
channel: Zemstandart/Zemsproekt (Alexey Zemskov) — Moscow-based
source_metadata_location: Moscow (channel convention)
language: ru
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
---

# Extraction Note — Zemstandart: Minimum-Size "Two-Fixture" Bathroom Sizing Formulas (#145, YouTube SBzDJk_yp8w)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

Solo technical how-to, extremely dense with precise millimeter-level dimensions — the single most numerically rigorous bathroom-sizing source in this store to date. Contains a direct pitch for the practitioner's own remote design service (`zems.pro`, already in this store). Scope explicitly limited to the case where risers/plumbing stacks sit in an *adjacent* room (don't constrain this room's layout). **Turnkey/Full-Service.**

## Key Concepts

- **"Two-fixture" bathroom** (ванная на два предмета) = a room containing a bathtub plus exactly one of: toilet, sink, or washing machine. This source establishes a formal taxonomy: 2/3/4-fixture rooms (4-fixture = tub+sink+toilet+washing machine), each further split by (a) riser location (inside room vs. adjacent), (b) toilet present or not, (c) tub vs. shower cabin as the primary fixture, and (d) whether a structural (load-bearing) wall constrains the achievable dimensions — each combination requires different sizing logic entirely. This video covers only the "risers adjacent, tub-not-shower" branch.

## Bathroom / Plumbing — Durable Facts & Rules

- **Room width formula (no toilet; second fixture is sink or washing machine)**: from the start wall (rough guide flush to communications, placing them outside the room) → +100mm wall thickness → **+915mm** (broken down as: 15mm tile+adhesive + 100mm left door-trim standoff + 700mm for the smallest 60cm door incl. frame and foam joint + 100mm right door-trim standoff) → then + the bathtub's own width. `confirmed`, precise arithmetic derivation.
- **Do not add the 15mm tile+adhesive allowance on the bathtub side of the room-width calculation** — the tub sits flush to the wall, and tile overhangs the tub rim by that 15mm instead, specifically so water can't seep behind the tub past the trim/baseboard. `confirmed`, a critical sign-reversal rule easy to get backwards.
- **Bathtub width**: minimum usable is 700mm (workable but uncomfortable for most people); practical default is 800mm; 900mm for larger-bodied occupants. `confirmed`.
- **The 915mm door-clearance allowance applies regardless of what the second fixture actually is** — even a 600mm-wide washing machine still requires the full 915mm width allocation, because the constraint is the smallest viable door opening, not the fixture's own footprint. `confirmed`, non-obvious/counter-intuitive rule explicitly flagged.
- **Room length (perpendicular dimension) = the bathtub's own length, with no additional tile-allowance gap** — tile overhangs the tub on all three exposed sides, so the room's other dimension is driven directly by tub length. `confirmed`.
- **Bathtub length must be fitted to the occupant's actual height, not a generic default**: the person's feet should reach the far end wall while lying down, or they'll slide under the water. Worked example given: a 178cm-tall person is comfortable in a 180cm tub; the same person in a 190cm tub (only 10cm longer) would find the extra length exactly enough to make them slide under and choke. **General rule: bathtub length ≈ occupant height, or up to 10cm less.** Practical defaults: 1700mm typical, 1800mm for taller occupants. `confirmed`, concrete worked example with real measurements.
- **Resulting standard room footprint** (combining the above): 1715mm × 1700mm or 1815mm × 1800mm, depending on which tub-length/width combination is used.
- **Perimeter wall thickness allowance**: 100mm.
- **Door-opening formation sequence**: offset 115mm from the start wall for the first vertical guide, +700mm for the second guide, opening height 2070mm.
- **Fixture placement**: position the tub with its drain near the shared/neighboring wall; place the mixer/faucet and shower bar on that same wall.
- **Critical mixer-placement mistake, explicitly flagged as the single most common error**: never center the mixer on the *visible* (tile-overhung) portion of the tub — i.e. don't split the remaining width in half after subtracting the ~15mm of tile overhang and center on that reduced figure. **Always center the mixer on the tub's true physical center**, ignoring the tile overhang, because the drain/overflow assembly (визуально видимый ориентир) is centered on the tub's real geometry, and an off-center mixer next to a centered drain/overflow reads as visibly wrong. `confirmed`, real, specific, checkable mistake.
- **Sink plumbing rough-in point (no-toilet variant)**: offset 15mm from the start wall, then +450mm, place the outlet/supply group on that resulting centerline.
- **Toilet variant plumbing/fixture placement**: horizontal guide offset 250mm from the neighboring (shared) wall; separately, offset 15mm from the start wall then +450mm for another guide; center the wall-hung toilet unit (инсталляция/in-wall cistern frame) on the second guide, with its front face set 250mm from the neighboring wall.
- **Cistern-box height decision rule**: if a water-shutoff manifold or a household-chemical storage cabinet will sit above the toilet's cistern box, build the box full floor-to-ceiling height and form a **600mm × 900mm revision/access hatch** in it. If neither applies, build the box to **1250mm height only**, topped with a decorative countertop surface. `confirmed`, a clear either/or decision rule with two specific resulting dimensions.
- **Hygienic shower (bidet spray)** is placed to the right of the toilet in this source's standard layout (no handedness variation discussed in this specific video, unlike other sources already in this store that do vary this by occupant handedness).

## Numeric Data

- Door-clearance allowance: 915mm (15mm tile + 100mm standoff + 700mm door + 100mm standoff).
- Bathtub width: 700mm minimum / 800mm typical / 900mm for larger occupants.
- Bathtub length: ≈ occupant height, or up to 10cm less; 1700mm typical / 1800mm for taller occupants.
- Standard room footprint: 1715×1700mm or 1815×1800mm.
- Door opening: 115mm offset, +700mm width, 2070mm height.
- Sink rough-in centerline: 15mm + 450mm from start wall.
- Toilet cistern-box height: full floor-to-ceiling with a 600×900mm hatch (if a manifold/cabinet sits above) or 1250mm with a decorative countertop (if not).
- Toilet unit placement: front face 250mm from the neighboring wall.

## Assumptions / Uncertainties

- All figures are this practitioner's own stated design convention — `single-account`, `unverified` against any external building code, though internally consistent and arithmetic-checkable throughout.
- Company scale claim repeated ("22 technologists," "several thousand rules," 15+ years of data collection) — `unverified`, self-promotional, consistent with similar claims elsewhere in this store from the same channel.

## Relevance to This Project's Topic

The most numerically rigorous, arithmetic-checkable bathroom-sizing source in this store to date — directly extends `07_Bathroom/Bathroom_Guide.md`'s existing dimension-planning content with a complete, self-consistent minimum-footprint formula for the common "tub + one fixture" case, plus the mixer-centering mistake and the toilet cistern-box decision rule.
