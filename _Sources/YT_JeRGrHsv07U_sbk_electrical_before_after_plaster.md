---
source_type: video transcript (turnkey renovation company owner, sequencing-decision explainer, Russian, ASR-cleaned captions with punctuation)
source_url: https://www.youtube.com/watch?v=JeRGrHsv07U
video_id: JeRGrHsv07U
transcript_file: not separately archived — fetched inline via youtube_transcript_api (sha256 cf357504ecd06c07aeacfe707327eae0d9acef42f5a195674fcf1611bdedee26)
fetched: 2026-08-28 (anonymous, youtube-transcript-api, ru captions, is_translated=false)
upload_date: 2021-01-29 (confirmed via yt-dlp metadata)
channel: ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ (Vladimir Amelchenko), business/premium-segment turnkey renovation company — St. Petersburg (channel-level; not spoken directly in this video)
regional_applicability: not city-specific — a general sequencing/technique caution
currency: n/a (no pricing stated; only a qualitative "you'll spend more fixing it than you saved" framing)
language: ru
extraction_taxonomy: custom (renovation planning)
fact_yield: 4
promotional_ratio: low (a genuine sequencing-decision explainer directly answering a stated recurring viewer question; no service pitch)
corroborates_existing: false (checked directly against Round 3's `8-GD_CEX0Bg`, this channel's own electrical rough-in walkthrough — that source covers floor-routed conduit/soundproofing-membrane technique and low-voltage consolidation, not electrical-vs-plastering sequencing; also checked against the existing "back-box installation sequencing rule" on `12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md` — that rule is about mortaring an individual back-box before threading cable through it, a narrower and distinct question from this video's whole-wall electrical-before-or-after-plastering sequencing decision)
---

# Extraction Note — Vladimir Amelchenko (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ): "Electrical Before or After Plastering?" (YouTube JeRGrHsv07U)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference.

## Source Metadata / Promotional Context

**Round 6, video 7 of 8.** Directly answers a stated recurring client question about whether to run electrical wiring before or after wall plastering, with a clear final recommendation and two named mechanisms explaining why the seemingly cost-saving "before" sequence usually backfires. Low promotional ratio — a direct technical explainer, no service pitch. **Checked against Round 3's `8-GD_CEX0Bg`** (this channel's own electrical rough-in walkthrough) — no overlap: that source covers floor-conduit/soundproofing-membrane technique and low-voltage transformer consolidation, not this specific sequencing question. **Also checked against the existing "back-box installation sequencing rule"** on `12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md` (mortar an individual back-box in first, then thread cable) — a narrower, distinct question from this video's whole-wall-plastering-timing decision.

## Planning Rules / Mistakes / Warnings — Electrical-Before-Plastering Cost Trap, Two Named Mechanisms

- **⚠️ The naive cost-saving logic, stated directly then debunked**: running cable on top of already-plastered walls means chasing (cutting a channel) into finished plaster, requiring paid remedial patching afterward; running cable *before* plastering lets the wet plaster simply bury the cable with no chasing/patching labor needed. **Explicit verdict: this logic is correct in principle, but has real nuances that usually erase the savings** — the video's core content is those nuances.
- **⚠️ Named mechanism 1 — socket-box (подрозетник) cable-slack shortfall on uneven walls**: a socket box installed before plastering must be set flush to the *final* (post-plaster) wall plane, but the eventual plaster thickness (which varies by how uneven the original wall/construction is) isn't always precisely known in advance. **Concrete rule of thumb stated directly**: always leave at least a palm-width of cable slack reserve inside the box. **Named real-world failure case**: developer-installed electrical work is typically left with almost no cable slack reserve at all — when a wall needs 3-4-5cm of plaster buildup to flatten, pulling the existing developer cable out to reach the box after plastering can literally run out of usable cable length, making a proper socket installation physically impossible without re-pulling new cable.
- **⚠️ Named mechanism 2 — room geometry shift after plastering, moving pre-marked fixture positions out of alignment**: once walls are plastered, their thickness increases (potentially by different amounts across different walls in the same room — 12cm vs 5cm vs 10cm in the video's own comparison, depending on how uneven/poorly-built the original walls were) — this shifts the *effective* interior geometry of the room, meaning outlet/switch/light-fixture positions carefully marked and wired before plastering can end up **misaligned relative to the finished wall surface** (the video's own visual example: a plastered wall edge encroaching over a light switch). **Two named remaining options once this happens, both bad**: accept the fixture positions being off from the original plan, or redo the affected wiring/positions entirely — in either case, the video states the rework cost typically exceeds whatever was originally saved by skipping post-plaster chasing.
- **Final recommendation stated directly**: electrical *can* be done before plastering, but is not recommended unless the installer has deep, specific expertise in managing exactly these two nuances — the default, safer sequencing recommended by the speaker is to run electrical **after** plastering.

## Assumptions / Uncertainties

- No pricing or region-specific content; the "you'll spend more fixing it than you saved" framing is qualitative, not a quantified cost comparison.
- `single-account` — one company's own stated sequencing recommendation and reasoning, not cross-checked against a written electrical code/standard in this transcript.

## Target Page(s)

- **`12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design.md`** — the existing "back-box installation sequencing rule" section is the closest existing home for this content; this video's whole-wall electrical-vs-plastering sequencing question is added as a distinct, related entry in the same section rather than merged into the existing narrower rule.
- **`_Knowledge/store/Durable_Facts.md`** — mirrored here too for this store's standard cross-source traceability.

## Relevance to This Project's Topic

A genuinely new sequencing-decision topic for this store — distinct from both this channel's existing rough-in technique source and the existing narrower back-box mortaring rule — directly useful for this project's own self-managed trade-sequencing planning, where getting electrical-vs-plastering order wrong risks a real, avoidable rework cost.
