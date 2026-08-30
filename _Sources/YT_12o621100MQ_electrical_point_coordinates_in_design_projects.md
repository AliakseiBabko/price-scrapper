---
source_type: video transcript (single-speaker practical guide, Russian, ASR auto-generated captions — no punctuation, occasional transcription errors)
source_url: https://www.youtube.com/watch?v=12o621100MQ
video_id: 12o621100MQ
transcript_file: _Archive/processed_sources/20260804_electrical_point_coordinates_in_design_projects_2dc422a9.txt
fetched: 2026-08-04
upload_date: 2020-06-14
channel: Alexey Zemskov / ZEMS group of companies (Zemstandart/Zemsproekt/Zemsremont) — confirmed by sign-off "с вами как всегда был алексей земсков" at end of transcript
regional_applicability: Belarus/Russia region (Minsk-adjacent renovation-design company)
currency: none stated
language: ru (ASR auto-generated, no punctuation)
extraction_taxonomy: custom (renovation planning)
---

# Extraction Note — Zemskov: How Electrical Point Coordinates Should Be Documented in a Design Project (YouTube 12o621100MQ)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference.

## Note on title vs. supplied hint

The batch hint for this video was "How not to do electricity, DIY installation" — the actual content (verified against the transcript) is about **how electrical-point coordinates should be specified and documented in a design/electrical plan** (a documentation/standards video, aimed partly at self-promotion for the speaker's own design service, but containing a genuinely reusable documentation convention), not a DIY installation mistakes video. Retitled accordingly.

## Source Metadata

Video #126. Contains an explicit pitch for the speaker's own paid design service partway through (skipped per task instructions) but the surrounding documentation-convention content is retained as durable. Single-account (Zemskov/ZEMS), consistent with the rest of this playlist.

## Durable Facts

- **Coordinate system for electrical points**: every electrical point in a plan should have two coordinates, labeled with two letters — "В" (height) and "Д" (length/horizontal distance) — each measured in centimeters from an explicitly stated reference point, with a legend/explanatory note in the project stating what the reference point is. Reasoning given: this lets both installer and homeowner read the same drawing unambiguously without needing drafting/technical training.
- **Default height reference point = finished floor level**, not the screed and not the raw/zero elevation — reasoning: all decorative elements and furniture that could conflict with an electrical point are themselves positioned relative to the finished floor, so measuring from anything else introduces mismatch risk.
- **Exception — window slope/reveal (откос) outlets**: height must NOT be measured from the finished floor for outlets mounted in window slopes, because the resulting distance-to-windowsill would vary significantly and inconsistently between the two slopes of the same window; instead these are measured from the slope/windowsill surface itself.
- **Exception — kitchen countertop outlets**: despite being an above-a-surface case similar to the window-slope exception, kitchen backsplash/countertop-area outlets are still measured **from the finished floor**, not from the countertop — reasoning given: at the time electrical coordinates are set, the kitchen countertop/cabinetry is not yet installed (and won't be for a long time), so the countertop can't serve as a usable reference point yet.
- **Ceiling as an alternative height reference point**: permitted specifically when a point needs to align with something ceiling-relative — e.g. positioning an AC unit at a fixed distance below the ceiling to align with a decorative wallpaper stripe, or positioning a cluster of low-voltage/network points inside a closet mezzanine (антресоль) for a home server setup, or centering an AC unit above a doorway — in these cases ceiling reference is described as faster and more accurate than floor reference.
- **Horizontal ("Д") reference point = nearest corner or nearest opening (door/window) reveal**, whichever is closer; when a point falls in a genuinely ambiguous zone between two possible references, the reference actually used must be stated explicitly in the drawing rather than left implicit.
- **Room corners must be individually labeled** (unique letters within the sheet, assigned alphabetically starting from the top-left corner, going clockwise) specifically to remove ambiguity about which corner a "Д" measurement is taken from.
- **Each room's plan should be on its own separate sheet**, drawn top-down, showing true shape plus all door/window openings and other features (recesses, niches, alcoves) — reasoning given: improves installer readability, allows multiple rooms to be worked in parallel, and makes electrical points located over recesses/window returns possible to dimension at all.
- **Worked example of the resulting installer workflow**: with this convention, an installer needs only two tape-measure readings per point (e.g., "90 cm from corner B, 15 cm from the opening edge") to place a switch — described as fast for the installer and equally fast for the customer to independently verify with the same tape measure and the same two readings, eliminating rework/disputes from ambiguous coordinates.

## Assumptions / Uncertainties

- This is a documentation/process convention advocated by one design company, not an industry-wide code requirement — presented and recorded here as `unverified`, single-account best-practice guidance, not a standard.

## Relevance to This Project's Topic

Useful less as a "rule for the wall" and more as a **template for how this project's own renovation plans should document electrical-point coordinates** — the floor-vs-ceiling-vs-slope reference-point logic and the corner-labeling convention are directly reusable for planning/communicating with an electrician regardless of region. Worth flagging to whoever maintains `Electrical_and_Lighting.md` as a possible "Buying/Practical Guidance" or planning-documentation note, distinct from the room-by-room placement content in the companion video `iBPJimtw7k0`.
