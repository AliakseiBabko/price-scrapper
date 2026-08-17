---
source_type: video transcript (technical how-to, Russian, clean/manual-style captions via youtube-transcript-api)
source_url: https://www.youtube.com/watch?v=ludvy76HGSU
video_id: ludvy76HGSU
transcript_file: _Inbox/transcripts/20260731_zems_b025_interiordoors_286a8d88.txt
fetched: 2026-07-31
upload_date: not independently confirmed by metadata; video is titled "...#025" — consistent with this channel's other playlist entries (#028, #141, #142, #146-197 etc.), all previously logged as 2019 in this repo's CSV. Kept as `inferred` 2019 by numbering-consistency, not `confirmed`.
channel: Zemstandart / Alexey Zemskov (Moscow-area renovation company, self-identified on camera as "Алексей Земсков")
source_metadata_location: not stated in transcript or checked metadata; region carried forward from this channel's established CSV convention ("not stated (Moscow-area renovation company)")
language: ru
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
---

# Extraction Note — Zemstandart: Interior Door Sizing, Openings & Reveals (#025, YouTube ludvy76HGSU)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

- Solo host video, Alexey Zemskov speaking directly to camera/narrating over footage of unspecified project(s) ("на своих объектах" = "on my own projects"). Self-promotional business channel — Alexey runs a renovation company and is describing his own standard practice, not a neutral third-party study. References his own earlier video ("как выбрать дверь") as a companion piece.
- No pricing content in this source — purely technical/sizing/planning.

## Doors / Trim — Durable Facts & Rules

- **Door unit (дверной блок) has five components**: leaf (полотно), frame/box (коробка), jamb extensions (доборы), casing/trim (наличники), hardware (фурнитура). `confirmed`.
- **Standard leaf height**: 2.0 m. **Standard leaf widths**: 60 / 70 / 80 / 90 cm; anything else is non-standard. `confirmed`.
- **Leaf-width selection rule of thumb (speaker's own standard, stated as his general practice)**:
  - Bathroom/WC: speaker states two slightly different versions in the same video — early in the video he says 60 cm is the conventional/typical choice (smallest footprint inside a small wet room); in his own closing summary he revises this to "70 cm preferred, 60 cm only if space is very tight." Recorded as an **internal nuance/evolution within the same video, not a contradiction to silently resolve** — both statements given. `confirmed` as spoken, for each version.
  - Living spaces (bedroom, living room, etc.): 80 cm is his stated optimal default. 70 cm only if 80 cm doesn't physically fit (e.g. narrow corridor). **90 cm leaf explicitly not recommended** ("никогда и никому") — described as unwieldy, prone to sagging/warping from its own width, no real advantage over 70 cm.
- **A 60 cm-wide leaf will NOT pass a 60 cm-wide appliance (e.g. washing machine)** through a 60 cm door, even though the leaf and appliance share a nominal width — mechanism: the door frame (коробка) profile isn't rectangular; one side has a ~1 cm-wide rebate/stop (прихлоп) that (a) lets the door close in only one direction and adds soundproofing, and (b) reduces the actual clear/light opening by roughly that rebate width on top of the standard 2–3 mm perimeter installation gap. `confirmed`, concrete non-obvious mechanism.
- **Rebate (прихлоп) rejected embellishment**: some clients request an additional threshold-side rebate/lip (порог с прихлопом) to fully close the sound-transmission gap at the bottom of the door (the weakest point acoustically). Speaker explicitly **advises against this** — modern interior door soundproofing is "already sufficient," the audible gain is imperceptible, and a ~3 cm threshold becomes a trip/stubbing hazard used for the life of the door. `confirmed` as the speaker's stated recommendation.
- **Rough-opening sizing rule**: the **opening (проём) should be 10 cm wider than the leaf** (e.g. 60 cm leaf → 70 cm opening; 80 cm leaf → 90 cm opening), leaving ~5 cm clearance on each side inside the opening for the door frame (which itself occupies ~2–3 cm per side) plus a foam installation joint. `confirmed`, concrete and checkable.
- **Casing standoff rule**: the finished door frame/casing should never sit flush against an adjacent wall/corner — leave a minimum standoff gap (speaker states this passage with a likely ASR/transcription gap around "3-4 cm," recorded as `uncertain` for that specific sub-number) so the casing isn't cut/butted awkwardly and so a small additional baseboard segment can terminate cleanly between the casing and the corner. A flush casing looks poor and produces an ugly baseboard-to-wall or baseboard-to-casing seam. Speaker's overall practical minimum for a full 80 cm door installation incl. both the 10 cm opening allowance and 10 cm casing standoff on each side is **~110 cm of total wall run** ("метр десять"). `confirmed`, concrete number for the total-run case.
- **Standoff also serves a swing/handle-safety purpose**: the ~10 cm standoff lets the door open to 90-95°, moving the door handle physically out of the direct walking path through the opening — a protruding handle at hip/head height is called out as a real injury risk (adults hitting hip, children hitting head/eye). `confirmed`.
- **Corridor-width trade-off**: if a corridor/opening approach is only ~1 m wide, using an 80 cm door forces the casing to encroach onto the adjacent wall — speaker's stated fallback is to downsize to a 70 cm door in that situation rather than accept a bad casing junction. `confirmed`, a concrete decision rule.
- **Wider door leaf ↔ narrower adjacent built-in wardrobe** — a direct trade-off the speaker flags: a larger door consumes more of the wall run that would otherwise go to an adjacent closet/wardrobe on the room side. `confirmed`.
- **Wall thickness vs. door frame — jamb extensions (доборы) are structurally necessary**: standard door frame (коробка) depth is ~7 cm; even the thinnest wall offering any real soundproofing is ~10 cm, and after plastering typically reaches ~15 cm — i.e. the wall is essentially always thicker than the frame, requiring доборы (jamb extension panels) to close the gap and cover the reveals (откосы). `confirmed`.
- **Two доборы types**: standard flat board (simple, cut to fit, one edge against the frame, other trimmed to meet the casing) vs. telescopic (slides into a channel machined into the frame itself). **Telescopic is described as clearly superior** — it self-adjusts to an uneven wall or a slightly twisted frame during installation, producing better junctions. `confirmed` as speaker's stated preference/recommendation — flag as a technique recommendation, not independently benchmarked against cost.
- **Installation-plane offset rule**: an interior door only opens one direction (its rebate prevents the reverse). The frame's installation plane should be offset toward the room the door swings INTO, with the frame flush to the wall on the swing side (allowing a clean foam joint under a flat casing) and the visible foam joint + full reveal treatment on the opposite (non-swing) side. **Getting this backwards is a real hazard**: if the frame is offset the wrong way, the open door strikes/"splits" the corner of the opening, and the leaf can only reach ~90° instead of the intended ~95°, which the speaker links to more serious injuries (presumably from the reduced swing forcing awkward passage/collisions). `confirmed`, safety-relevant mechanism.

## Relevance to This Project's Topic

First formal-pipeline source in this store covering interior door leaf/frame sizing, rough-opening formation, and installation-plane offset as a connected, internally consistent technical system — a genuinely new "Doors / Trim" content area for this store (previously untouched by any formally-processed source). No pricing content; purely durable, brand-agnostic technique.
