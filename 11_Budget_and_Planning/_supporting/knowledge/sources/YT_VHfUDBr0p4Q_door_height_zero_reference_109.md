---
source_type: video transcript (single-speaker technique/explainer, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=VHfUDBr0p4Q
video_id: VHfUDBr0p4Q
transcript_file: _Archive/processed_sources/20260819_door_height_zero_reference_109_df982ae2.txt
fetched: 2026-08-19
upload_date: 2019-11-21 (metadata-confirmed via yt-dlp `upload_date`)
channel: Zemstandart (Alexey Zemskov)
regional_applicability: not stated in-video — level 2/channel-branding only (Moscow, per this channel's established convention)
currency: not applicable — no pricing stated in this source
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemstandart: "How to Correctly Set the Doorway Height at the Beginning of an Apartment Renovation" (#109, YouTube VHfUDBr0p4Q)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Category 4 batch, chunk 2 of ~6. Earliest-dated source in this chunk (2019) and one of the densest, most mechanism-rich sources in the whole Category 4 batch so far — a full explanation of the "zero reference" / "working reference" (нулевая и ходовая отметка) system used throughout this channel's renovation methodology, previously only implicit in other sources' worked examples. Explicitly states the reasoning for a numeric standard already independently present in this store (2.07m door-opening height, from the foam-block masonry sources), closing a gap where that figure was recorded without its own derivation.

## Planning Rules — Zero-Reference System & Door-Opening Height Derivation

- **"Zero reference" (нулевая отметка) definition for apartment renovation, distinct from the construction/geodesy meaning of the same term**: in construction/geodesy, the zero reference can be placed anywhere and is arbitrary per site; in apartment renovation, the zero reference has one fixed, non-arbitrary meaning — **the level of the finished (not rough) common-corridor floor outside the apartment's front door.** Everything below that level is a negative offset, everything above is positive. `confirmed`, explicit mechanism.
- **Why the corridor's finished floor specifically is the zero reference, two stated reasons**: (1) a well-executed renovation should never leave the occupant stepping down into a pit or up over a step when exiting to the corridor — the apartment's finished floor and the corridor's finished floor must be level, which only works if both are referenced from the same zero; (2) the screed plane is present and physically referenceable throughout nearly the entire renovation timeline (from the earliest rough-in work until the very last pre-wallpaper step, when a thin self-leveling correction layer goes down over it) — every measurement in a project (plumbing/electrical stub-out heights, door-opening heights, all layout dimensions) is ultimately taken from the screed, whatever nominal reference point is used, so treating the screed itself as zero avoids compounding conversion errors across every single measurement.
- **"Working reference" (ходовая отметка) definition and role**: a second, elevated virtual reference plane set exactly **1000mm above the zero reference**, projected around the room at roughly chest/eye height with a laser level and marked directly on walls (and, importantly, also on window/door reveals, pipe risers, and ventilation shaft surfaces that won't themselves be plastered — a mark placed only on soon-to-be-plastered walls is later lost). **In construction/geodesy the zero reference is primary and the working reference is a convenience aid; in apartment-renovation practice this is reversed — the working reference is primary and used for essentially all layout, while the zero reference is often never physically marked on-site at all**, existing only as a virtual concept everything else is derived from.
- **Why exactly 1000mm (not an arbitrary convenient height)**: a round 1-metre offset makes mental arithmetic between the two reference systems trivial even for an inexperienced tradesperson (worked example given: "25cm above zero" instantly converts to "75cm below working reference" without a calculator) — explicitly framed as an error-reduction design choice, not a habit or convention without a stated reason.
- **Door-opening height standard, with full stated derivation**: rough screed-referenced opening height must be **exactly 2.07m**, not the older/still commonly-quoted 2.06m figure. Derivation: standard interior door leaf mounts on the *finished* floor at 2.05m clearance height; a finished floor build-up above the rough screed is typically 2cm total (1cm self-leveling correction compound + 1cm finish flooring); 2.05m + 2cm = 2.07m measured from the rough screed. **This is the first source in this store to state the 2.07m figure's own derivation** — the figure itself already appears independently in this store's foam-block masonry sources (`yt_OR0Vk7V6zeo`, corroborated via `13_Surfaces_and_Finishes/Walls_and_Paint.md`), which stated the number as a given without explaining where it comes from; this source supplies the missing mechanism and closes that gap.
- **Consequence of getting opening height wrong, both directions, stated as the reason this matters enough for its own video**: too-low openings are typically only discovered once wallpaper and finish flooring are already installed, requiring chiselling into finished walls (dust, noise, guaranteed wallpaper/flooring damage near the opening) to raise them; too-high openings require either expensive non-standard custom doors or building up the header (again risking finish-surface damage). Both failure modes are framed as expensive and disruptive enough at the finishing stage that the cost of getting the layout right up front is trivial by comparison.
- **Practical marking procedure using the two-reference system**: (1) position a self-leveling laser so its horizontal beam crosses the building entrance door opening and as many other openings as possible in one setup; (2) adjust the laser's height until the beam sits exactly 99cm above the corridor's *finished* floor surface (99cm, not 100cm, because the corridor's own finish-flooring layer is already down and ~1cm thick — the beam is thus exactly 1m above the *rough* screed underneath it, i.e. exactly at the working reference); (3) transfer that laser plane around the apartment with a marker, hitting every wall and every non-plasterable surface; (4) from each working-reference mark, measure down 1m to find/pour screed to, and up 1.07m to mark each door-opening's top.
- **What to use as zero when the building corridor's own floor isn't finished yet (a genuinely common real-world case for a new-build renovation done early)**: explicitly do **not** use the bottom of the developer-installed building entrance door as a stand-in zero — the source states developer installers set that door's position with no regard for the future corridor floor level at all. **Correct substitute**: the building elevator's own threshold height, because developers deliberately set that height so a stroller or a wheeled appliance/cart can cross it without a bump — making it a reliable proxy for the intended future corridor finished-floor level.
- **Worked numeric consequence, stated explicitly**: because of the finish-floor buildup, the apartment's own finished floor level ends up 5-10mm *higher* than the corridor's finished floor level (not perfectly flush) — imperceptible underfoot in normal use, but a deliberate, correct outcome: it's specifically there so that if the corridor or a neighboring unit floods, water is directed away from the apartment's own doorway (toward the elevator lobby) rather than pooling into the unit.

## Advertising / Promotional Content Notes

A closing segment briefly pivots to promoting the company's own "technical design" service (250,000 RUB, claimed to save 500,000+ RUB on a 100m² apartment) — tag as a direct commercial claim/tier-steering, `unverified` savings figure, not adopted as a store-level fact. The entire preceding technical content is free of brand/product endorsement.

## Target Page(s)

`13_Surfaces_and_Finishes/Walls_and_Paint.md` — the existing "Partition Layout & Masonry Technique" and "Foam-Glue Block Masonry" sections already state the 2.07m door-opening figure without derivation; this source should be added as the citation for *why* that number is 2.07m, not 2.06m or another figure — a meaningful gap-closer. Also touches `12_Engineering_and_Systems/analysis/Mounting_Heights_and_Positioning.md` (the zero/working-reference system underlies every stub-out height figure already recorded there) and potentially `13_Surfaces_and_Finishes/Flooring_Guide.md` (corroborates/extends the existing Screed Zero-Reference Lowering Technique section — this source explains the *reference system itself*, the flooring source explains a *cost-saving technique built on top of it*; both belong cross-linked).

## Relevance to This Project's Topic

Very high — this is foundational planning methodology that every other measurement/layout source in this store implicitly depends on, and until now had never been explained end-to-end from a single source. Closes a real gap (the 2.07m figure's own derivation) and gives a general-purpose two-reference measurement system directly applicable to any DIY layout work on this project.

## Gaps

- No region confirmed at level 1 (spoken) — channel-convention-only (Moscow); the elevator-threshold-as-proxy convention is plausibly Russia/CIS new-build-specific and may not transfer to a different country's building-handover practice.
- The 250,000 RUB design-fee/500,000+ RUB savings claim is an unverified company marketing claim — not adopted as fact.
- 5-10mm apartment-vs-corridor floor height differential is stated as a deliberate design outcome; not independently verified against a second source, but the flood-protection mechanism given is internally consistent and plausible.

## Recommended Downstream Routing

`tiered-knowledge-base` — Planning Rules Durable Facts section of the renovation budgeting intermediate store (as a new, foundational subsection), plus wiki routing to `13_Surfaces_and_Finishes/Walls_and_Paint.md` and `12_Engineering_and_Systems/analysis/Mounting_Heights_and_Positioning.md` (see Target Page(s) above).

## Promotion self-check

Re-read in full after drafting. All concrete facts/rules/numbers identified during extraction are reflected in the checklist above.
