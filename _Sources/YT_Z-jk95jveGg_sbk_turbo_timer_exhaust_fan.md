---
source_type: video transcript (turnkey renovation company owner, product/wiring explainer, Russian, ASR auto-generated captions — no punctuation)
source_url: https://www.youtube.com/watch?v=Z-jk95jveGg
video_id: Z-jk95jveGg
transcript_file: not separately archived — fetched inline via youtube_transcript_api (sha256 f0dc35efa59b54f49fee6247e251f91cbbb7ccbe91f2da88f4d6aa9cf32a843a)
fetched: 2026-08-28 (anonymous, youtube-transcript-api, ru auto-generated captions)
upload_date: 2021-01-11 (confirmed via yt-dlp metadata)
channel: ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ (Vladimir Amelchenko), business/premium-segment turnkey renovation company — St. Petersburg
regional_applicability: general technique, not region-specific
currency: n/a (no pricing in this video)
language: ru
extraction_taxonomy: custom (renovation planning)
fact_yield: 5
promotional_ratio: low
corroborates_existing: false (new content — no existing turbo-timer/exhaust-fan wiring content found on Fresh_Air_Ventilation_and_Ducting.md)
---

# Extraction Note — Vladimir Amelchenko (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ): "Choosing a Bathroom/WC/Toilet Exhaust Fan" (YouTube Z-jk95jveGg)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference.

## Source Metadata / Promotional Context

**Round 7, video 6 of 8.** A "useful tips" segment demonstrating the wiring difference between a standard 2-wire bathroom exhaust fan and a 3-wire turbo-timer fan, using two physical units opened on camera. Low promotional ratio — direct hands-on demonstration, single soft CTA.

## Electrical / HVAC — Exhaust Fan Control Modes and a Real Late-Stage Wiring Trap

- **⚠️ Three control modes for a bathroom exhaust fan, named with a real tradeoff each**: (1) **wired to the light switch** — fan runs only while the light is on, so moisture clears slower once the light (and fan) are switched off on exit; (2) **wired to its own separate switch** — fan can keep running after the light is off, but relies on the occupant remembering to switch it off, a real risk of it running unattended for a long time; (3) **turbo-timer fan** — wired so it starts with the light/switch but keeps running for a fixed delay (stated range: roughly 30 seconds up to several minutes, model-dependent) after the light/power is switched off, then shuts off automatically — solves both problems named above.
- **⚠️ Named wiring-scheme difference, the video's core technical point**: a standard fan's terminal block has exactly **2 connections** (neutral/blue, phase/black) — wired the same as a light fixture. A turbo-timer fan's terminal block has a **3rd terminal**, carrying **continuous phase power to the timer circuit itself** (separate from the switched phase that starts the fan) — the timer board needs its own always-on power feed to time out correctly after the switched circuit is cut.
- **⚠️ Real, effectively unfixable-late defect named directly**: because the two fan types need genuinely different wiring at the switch/junction box (2-wire vs. 3-wire feed), a turbo-timer fan **cannot be retrofitted into wiring that was only ever run for a standard fan** once the ceiling is finished (stretch/drop ceiling installed, tiling done) — the wiring decision must be made at the design or rough-in stage, before ceilings/finishes close access to the run.
- **⚠️ Named real-world failure pattern this creates**: clients commonly buy a fan (including upgrading to a turbo-timer model) only at the very end of a renovation, once the ceiling and tile are already finished — by that point an electrician/installer physically cannot correct the wiring without demolition, producing exactly the kind of late, unresolvable defect and client dissatisfaction the source describes as a recurring source of conflict.
- **Practical mitigation stated directly**: decide the specific fan type (standard vs. turbo-timer) during design or, at latest, before ceiling/tile finishing begins — not as a final-stage purchase decision.

## Assumptions / Uncertainties

- General technique, not region-specific; no pricing stated in this video.
- Timer duration range ("30 seconds to a few minutes") is stated as model-dependent, not a fixed spec.

## Target Page(s)

- **`12_Engineering_and_Systems/analysis/Fresh_Air_Ventilation_and_Ducting.md`** — no existing content on exhaust-fan control wiring/timer types; this is a genuinely new addition to that page.

## Relevance to This Project's Topic

A concrete, checkable wiring distinction (2-wire vs. 3-wire fan control) tied directly to a real, sequence-dependent planning trap (the decision must be made before finishes close access) — fills a real gap in this project's ventilation content, not previously covered.
