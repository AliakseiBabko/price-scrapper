---
source_type: video transcript (turnkey renovation company owner, real site walkthrough, Russian, ASR auto-generated captions — no punctuation)
source_url: https://www.youtube.com/watch?v=8-GD_CEX0Bg
video_id: 8-GD_CEX0Bg
transcript_file: not separately archived — fetched inline via youtube_transcript_api (sha256 312d9f0e51cad406c82b41dccdadc4127ce8a59de7e43dd08d91797cd6d87d16)
fetched: 2026-08-28 (anonymous, youtube-transcript-api, ru auto-generated/ASR captions, is_translated=false)
upload_date: 2025-02-28 (confirmed via yt-dlp metadata)
channel: ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ (Vladimir Amelchenko), business/premium-segment turnkey renovation company — St. Petersburg (channel-level; not spoken directly in this video)
regional_applicability: St. Petersburg (channel-level, level 2 for this video)
currency: n/a (no pricing stated in this video)
language: ru
extraction_taxonomy: custom (renovation planning)
fact_yield: 8
promotional_ratio: low (a real rough-in site walkthrough; single CTA at the end)
corroborates_existing: partial (floor-vs-ceiling routing and the never-fasten-through-soundproofing rule corroborate this store's existing Petrishin-Stroi content on `Rough_Electrical_Sequencing.md`, with a distinct gluing-technique variant; the waterproofing-membrane repair at wall penetrations, low-voltage transformer consolidation, threshold conduit sleeve, and intercom cable-routing detour are new)
---

# Extraction Note — Vladimir Amelchenko (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ): Reliable Electrical Basics — Rough-In Walkthrough (YouTube 8-GD_CEX0Bg)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference.

## Source Metadata / Promotional Context

**Round 3, video 4 of 8.** A short (6-minute) real site walkthrough of rough-in electrical work in a 170 m² apartment with three bathrooms, addressing a specific recurring viewer objection (why so much cable/why not just "two breakers for the whole apartment"). Low promotional ratio — genuine site footage with real technique shown, single CTA at the end. **Value-filter verdict: full extraction** — dense technical content for a short video, several details not previously recorded in this store.

## Engineering / Systems — Floor-Routed Cable Over Soundproofing, a Gluing-Technique Variant

- **⚠️ Why "so much cable" for a single bathroom, stated as the video's own framing**: a design project with many lighting scenarios (shelf lighting, mirror lighting, vanity/cabinet lighting on 12-24V transformers, a heated towel wall in place of an electric towel warmer, ceiling lighting scenarios, a floor-heating thermostat) genuinely requires this much cable per room — presented as a direct rebuttal to the "two breakers for the whole apartment" comment the speaker says he sees regularly.
- **⚠️ Conduit-to-soundproofing-membrane fixing technique, a gluing variant not previously recorded on this store's Rough_Electrical_Sequencing/Soundproofing content**: after leveling the floor and laying two layers of Шуманет (functioning as both waterproofing and soundproofing under the future screed), corrugated conduit is **glued directly to the Шуманет membrane using bitumen tape** rather than screw-fastened — the membrane's own bitumen-like surface takes the tape well, and this avoids putting any fastener holes through the waterproofing/soundproofing layer. (This store's existing Petrishin-Stroi source instead ties floor conduit to a wire mesh laid loosely over the membrane; both techniques share the same underlying rule — never fasten a rigid penetration through the membrane — but are recorded as two independent, non-identical methods.)
- **⚠️ Waterproofing-membrane repair at wall penetrations, a real flood-prevention detail not previously recorded**: where conduit exits the floor membrane into a wall, the membrane is necessarily cut, breaking the "trough" (корыто) that makes the floor waterproof — the crew must weld/fuse two additional membrane layers back over that cut to restore a sealed penetration. **⚠️ Explicit consequence if skipped**: without this repair, only the soundproofing function survives at that point, not the waterproofing — the next screed pour would flood the downstairs neighbors through the unsealed penetration.

## Engineering / Systems — Low-Voltage Consolidation, Threshold Protection, and Obstacle-Avoidance Routing

- **⚠️ Low-voltage (12-24V) transformer consolidation in a dedicated cabinet, not the wet zone**: a bathroom with extensive 12-24V-transformer-driven lighting (shelves, mirror, vanity) routes all of its transformers out of the bathroom into a separate cabinet in an adjacent room — stated reasoning: housing transformers inside the wet zone itself is "not quite correct," and there's often no physical space for them there anyway. A real, visible design detail (a dense cluster of cables in a bedroom corner immediately outside the bathroom) explained by this consolidation, not a wiring mistake.
- **⚠️ Metal protective sleeve at floor-routed conduit crossing a doorway threshold**: where floor conduit passes under a door opening, it's fed through a length of metal tubing specifically so that a future trade (e.g. installing a threshold/transition strip) drilling or screwing into the floor at that exact spot won't sever the cable — a passive, low-cost protection measure for a location where later trades are statistically likely to drill.
- **⚠️ Deliberate non-straight-line conduit routing to guarantee avoiding a known future fixture-mounting point**: where a wall-mounted fixture with a known, fixed mounting pattern will later be installed (the video's own examples: an intercom handset requiring top-and-bottom wall anchors on a vertical axis; a wall sconce with anchor points on a vertical axis), the rough-in conduit is deliberately routed in a "U"/detour shape around that anchor axis instead of a straight vertical run — guaranteeing that whoever later drills for that fixture's anchors (whether the same crew or a different installer entirely) cannot possibly hit the cable, regardless of how carefully or carelessly the drilling is done. Framed directly as a pre-emptive mistake-proofing technique, not an aesthetic or cost-driven routing choice.
- **Clean, capped outlet-box practice during rough-in**: outlet boxes are kept covered with plugs/caps through the rough-in and later finish stages specifically to keep them free of dust/debris — offered as a visible marker of careful execution (a real, checkable acceptance-stage tell — a chronically dust-filled or debris-packed box at handover suggests careless work).

## Assumptions / Uncertainties

- Region: channel-level St. Petersburg only (not spoken directly in this video).
- No pricing/cost figures are stated anywhere in this video — this is a pure technique/process source, no currency conversion applicable.
- The two-layer membrane-repair detail at wall penetrations is described verbally without a shown material spec (thickness, product name) — recorded as a technique, not a product recommendation.

## Target Page(s)

- **`12_Engineering_and_Systems/analysis/Rough_Electrical_Sequencing.md`** — corroborates this page's existing floor-vs-ceiling routing and never-fasten-through-soundproofing content; adds the bitumen-tape gluing variant (vs. the existing wire-mesh-tie method), the waterproofing-membrane-repair-at-penetrations detail, and the deliberate-detour-routing mistake-proofing technique, none of which are currently on this page.
- **`12_Engineering_and_Systems/analysis/Waterproofing_and_Plastering.md`** — the membrane-repair-at-penetrations detail (re-fusing two layers to restore a sealed "trough" after a necessary cut) is directly relevant to this page's existing waterproofing-technique content; not added directly in this pass, flagged for a future consolidation pass.
- **`12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning.md`** — the low-voltage-transformer-consolidation-in-a-separate-cabinet practice is a real planning detail for any design with extensive low-voltage lighting; no existing overlap found.

## Relevance to This Project's Topic

Genuinely dense technical content for a 6-minute video, with several details not previously recorded in this store despite substantial existing electrical rough-in coverage: a distinct conduit-fixing technique variant, a real flood-prevention detail at membrane penetrations, a low-voltage-transformer consolidation practice, and a concrete mistake-proofing routing technique for known future fixture locations — all directly reinforcing this project's own acceptance/QC and rough-in planning conventions.
