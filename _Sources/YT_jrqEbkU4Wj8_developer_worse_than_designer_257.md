---
source_type: video transcript (single-speaker developer-layout critique + detailed replan case study, Russian, manually-created captions)
source_url: https://www.youtube.com/watch?v=jrqEbkU4Wj8
video_id: jrqEbkU4Wj8
transcript_file: _Archive/processed_sources/20260819_developer_worse_than_designer_257_9480a752.txt
fetched: 2026-08-19
upload_date: 2023-12-10 (metadata-confirmed via yt-dlp `upload_date`)
channel: Zemstandart / Zemproekt (Alexey Zemskov)
regional_applicability: not stated in-video — level 2/channel-branding only (Moscow, per this channel's established convention)
currency: not applicable — no specific transaction figures stated (a premium new-build developer layout, not a paid-designer critique)
language: ru (manually-created captions, method=youtube-transcript-api, generated=False)
extraction_taxonomy: custom (renovation planning, per renovation-knowledge-intake wrapper taxonomy)
---

# Extraction Note — Zemstandart/Zemproekt: "When the Developer Is Worse Than the Designer" (#257, YouTube jrqEbkU4Wj8)

## Evidence levels
(1) transcript text — (2) metadata — (3) inference — (4) none.

## Processing status: FULL EXTRACTION

Remainder-pool batch (post-Category-5), video 2 of a small next batch. **New-build apartment** (a premium developer white-box unit) — squarely in scope. Dense worked-example replan with two standout findings that meaningfully extend/nuance existing store content. No named-individual legal-dispute content (a different, unnamed designer is referenced only in passing as similarly bad, not identified).

## Rules / Heuristics — Standout Findings

- **⚠️ A WC/bathroom door's swing direction should be decided by the actual foot-traffic pattern at that specific location, not applied as a fixed rule — a genuinely important nuance to this vault's existing door-swing-direction convention.** This vault's existing rule defaults to WC/bathroom doors swinging outward (for the safety reason that an incapacitated occupant shouldn't be trapped behind their own body blocking an inward door). Here, the source makes the **opposite** choice deliberately: the bathroom sits at a busy corridor junction where traffic from three other rooms converges, so an outward-swinging door risks striking someone walking through *that* corridor unexpectedly — a stranger to the swing, with no way to anticipate it. An inward-swinging door instead only risks striking someone already inside/entering the bathroom itself, who is aware of the door and moving deliberately. **General rule: when a WC/bathroom door opens directly onto a high-traffic junction corridor (multiple rooms' traffic converging at that exact point), weigh striking corridor traffic against the existing safety rationale for outward swings — the safer choice can flip to inward depending on the specific traffic pattern.** This doesn't invalidate the existing default; it's the first documented case in this store of a deliberate, reasoned exception.
- **⚠️ Cut ventilation/airflow openings in built-in furniture (e.g. a custom desk) positioned in front of a window when it blocks a radiator's convection path — a specific, mechanism-explained condensation-prevention technique not previously recorded in this store.** If a desk or other furniture sits between a radiator and a window, blocking the radiator's warm-air convection from reaching the glass, the window can fog/condensate because it's no longer being kept warm by that airflow. Cutting deliberate holes/cutouts in the furniture at the appropriate location restores enough airflow to prevent this. **General rule: whenever furniture is placed between a heat source and a window, verify convection airflow to the glass isn't blocked — add airflow cutouts if it is.**
- **Soundproofing insulation thickness within a wall assembly should be set based on the specific site's actual wall thinness and stated occupant noise levels, not a fixed default.** The source's own stated default is 50-70mm, but this project used 100mm specifically because on-site measurement found the existing walls unusually thin and the client's children were noted as loud — a real example of adjusting a normally-fixed spec based on direct measurement + stated household behavior. **Distinct from this vault's already-well-corroborated 150mm figure** (which is about total partition wall-to-wall spacing between two rooms) — this is about the acoustic-insulation-layer thickness specifically, a related but separate variable. **General rule: survey actual wall thinness and factor in real occupant noise levels before defaulting to a fixed soundproofing-insulation-layer thickness.**

## Mistakes / Warnings — Corroborating Existing Findings

- **A closet/storage niche around a structural column with narrow reveals (here: 54cm wide × 28cm deep, ~25cm usable after door-leaf thickness) is functionally near-useless — even for simple document storage.** Reinforces this vault's now-extensively-corroborated reveal-width-vs-storage-usability finding.
- **A developer leaving structural columns fully exposed/unconcealed by the layout, rather than integrated into a wall, is a recurring developer-layout failure mode**, reinforcing this vault's existing findings on this exact issue from multiple independent sources.
- **A decorative grille niche should be sized 5mm larger than the grille's own dimensions on each measured axis** — reiterated, matching this vault's existing tolerance figure.

## Advertising / Promotional Content Notes

Standard channel framing (implicit endorsement of the source's own process — "what I've shown you is only 10% of the real project," a note that real work happens in the technical-documentation phase after client approval). No price-increase/booking call-out in this segment.

## Target Page(s)

The door-swing-direction traffic-pattern nuance is an important addition to `13_Surfaces_and_Finishes/analysis/Door_Swing_Direction.md` — should be added as an explicit exception case, not just a corroborating note. The furniture-cutout-for-radiator-convection technique is a new addition worth its own line on `13_Surfaces_and_Finishes/Walls_and_Paint.md` or a Windows page. The soundproofing-thickness-should-be-site-verified nuance belongs alongside the existing 150mm partition content.

## Relevance to This Project's Topic

High — the door-swing-direction exception is a genuinely important nuance to an existing safety rule (not a contradiction, but a real scenario this store hadn't yet covered), and the furniture-cutout-for-condensation technique is a specific, checkable, previously-unrecorded mechanism.

## Gaps

- No region confirmed at level 1 (spoken) — channel-convention-only (Moscow).
- No transaction/cost figures stated (a developer white-box layout, not a paid-designer critique).
- No named individual — no legal-dispute exclusion needed.

## Recommended Downstream Routing

`tiered-knowledge-base` — Rules/Heuristics Durable Facts section (the two standout findings), Mistakes/Warnings for the corroborating points. Wiki-route the door-swing exception to `Door_Swing_Direction.md` explicitly, and the furniture-cutout technique to `Walls_and_Paint.md`.

## Promotion self-check

Re-read in full after drafting. All concrete facts/rules/numbers identified during extraction are reflected in the checklist above.
