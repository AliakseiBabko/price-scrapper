---
source_type: video transcript (construction/renovation channel, technical explainer, auto-generated captions)
source_url: https://www.youtube.com/watch?v=RwyPR2RFZYM
video_id: RwyPR2RFZYM
transcript_file: _Archive/processed_sources/20260825_stroy_i_remont_smoke_detectors_general_ae19572a.txt
fetched: 2026-08-25 (anonymous, youtube-transcript-api, ru auto-generated captions)
upload_date: 2020-12-08 (confirmed via yt-dlp metadata)
channel: СТРОИТЕЛЬСТВО И РЕМОНТ (Construction and Repair), channel_id UCtUm-XxECRUHTzou6GrPziQ
source_metadata_location: not stated (no city/region named in transcript)
language: ru
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 13
promotional_ratio: medium
corroborates_existing: false
---

# Extraction Note — "ДАТЧИКИ ДЫМА И ПОЖАРНАЯ СИГНАЛИЗАЦИЯ" (YouTube RwyPR2RFZYM)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

General technical explainer built around a specific branded security-panel
ecosystem ("Ктс control"/"KTS control" — likely a hub/panel product line
this channel sells or installs; exact brand name ASR-uncertain, phonetic
match to "КТС" or similar). Medium promotional ratio: hub-specific
port/wiring/programming detail is brand-tied, but the underlying
mechanism, placement rules, and cabling standards are general
fire-safety technique usable regardless of which hub someone buys. This
is the first fire-safety/smoke-detector source in this vault — no
existing page anywhere covers this topic.

## Electrical / Regulations — New Facts

- **Detector placement rule (ceiling)**: at least 0.5m clearance from
  light fixtures, power cables, or any other source of electromagnetic
  interference, to avoid false triggers.
- **Detector placement rule (wall-mount alternative)**: ~10cm down from
  the ceiling, and at least 0.5m from the nearest wall corner.
- **⚠️ Coverage/quantity rule**: code minimum is one detector per 15-18m²
  of room area, but the source explicitly recommends **at least two
  detectors even in small rooms** — the stated reason is false-alarm
  discrimination: if only one detector exists, a single false trigger
  looks identical to a real fire; if two detectors both trigger, that's
  treated as confirmed alarm requiring immediate action.
- **How an optical smoke detector actually works**: contains an optical
  chamber whose transparency is electronically monitored. Clear chamber =
  normal signal. Smoke, soot particles, or even steam/vapor reduce
  chamber transparency (partially or fully) and the electronics send an
  alarm signal. A wired detector closes its signal loop to alert the
  central panel; a wireless detector sends an equivalent coded signal
  over radio. Many detectors also have a built-in audible alarm.
- **Wired detector spec (this system)**: comes with a 10m cable and plug,
  ~100mm diameter x ~40mm housing, rated -30°C to +55°C at up to 90%
  relative humidity, compatible across this panel line's full version
  range. Cable can be extended up to 50m from the stock 10m run.
- **⚠️ Wiring/cable spec and code-compliance note**: standard cable used
  is КСПВ 4×0.4 or 4×0.5mm² — route it away from light fixtures/power
  cables/EM-interference sources (same reasoning as the ceiling placement
  rule) to avoid false triggers. **For full fire-code compliance, replace
  this cable with fire-resistant-rated cable** instead of standard КСПВ.
  Any splice/extension joint must be **soldered** (solder + rosin flux),
  not just twisted — stated as a real safety requirement, not a nicety
  ("I know most people never do this, but I hope you will — it's your
  own safety").
- **Daisy-chaining multiple detectors per port**: a splitter lets several
  detectors share one signal port (any one triggering signals alarm for
  that port); alternatively, same-color wires from multiple detector
  cables can be joined in parallel (4 solder joints total) without a
  splitter.
- **Alarm reset requires physically disconnecting power**: once tripped,
  a detector's alarm state (lit indicator + closed loop) persists **until
  the detector is de-energized** — disconnect the cable for at least 5
  seconds, or reboot the whole panel via SMS command or app/portal
  button.
- **Non-destructive wired-detector self-test method**: insert a paperclip
  into the small test hole in the detector's cover, ~3cm deep, into the
  smoke chamber, to simulate smoke particles without needing an actual
  smoky room — indicator lights confirm the test passed.
- **Wireless detector spec**: -0°C to +55°C rated (narrower cold range
  than the wired unit), up to 90% RH; runs ~1 year on one 9V "Krona"-type
  battery; battery life drops if operated below -10°C or with unstable
  radio link to the panel; operates on 868 MHz with a built-in antenna.
  Comes with plastic mounting bracket, battery, mounting hardware, and a
  magnet used for programming/testing.
- **Wireless signal-quality test procedure**: hold the programming magnet
  to the same spot used for pairing and hold it there — the detector's
  indicator blinks; **more frequent blinking = better signal** to the
  panel. If it doesn't blink at all, relocate the detector until it gets
  a usable signal — stated as directly affecting battery life (poor
  signal drains the battery faster from repeated retransmission
  attempts).
- **Low-battery warning behavior (code requirement)**: per fire-code
  requirements, a low-battery detector must audibly beep roughly every
  30 seconds and flash a battery-status indicator; the panel can also be
  configured to push SMS/app notifications on low battery.
- **System capacity**: this panel line supports up to 32 wireless
  detectors and up to 100 wired detectors (via port splitters across
  ports D1-D5).
- **⚠️ Reliability comparison, source's own stated opinion**: wired
  detectors are described as **the most reliable type** — not subject to
  battery depletion, radio interference, or signal attenuation through
  reinforced-concrete floor slabs, unlike wireless units.
- **Whole-apartment power cutoff on alarm**: mentioned as a real
  integration option — a power contactor wired to the alarm system can
  cut electricity to the entire dwelling automatically if even one smoke
  detector triggers (used as a fire-safety measure, e.g. to de-energize
  wiring during a fire); referenced as covered in a separate linked video
  (not itself fetched).
- **What else triggers a false/real alarm**: any airborne particulate
  that reduces chamber transparency — cigarette smoke, hookah/vape vapor,
  dust, soot, and even plain steam/water vapor (a real installation
  caveat for detectors placed near kitchens/bathrooms).

## Assumptions / Uncertainties

- The exact hub/panel brand name is ASR-uncertain (transcribed
  phonetically as "кто control"/"кс control" across the auto-generated
  captions) — treated as a specific branded ecosystem, not a generic
  standard, and not adopted as a brand recommendation in the wiki page
  (per the advertising filter, brand/product-tier detail is tagged
  commercial; the underlying mechanism/wiring/placement rules are
  general).
- No city/region stated — not usable for region-specific code citation,
  general technique reference only.
- `single-account`, medium promotional ratio (channel-branded hub
  ecosystem woven through the installation instructions).

## Relevance to This Project's Topic

First fire-safety/smoke-detector source processed for this vault (no
prior coverage anywhere). Routed toward a new
`12_Engineering_and_Systems/analysis/Fire_Safety_and_Smoke_Detection.md`
page once the 3+-source threshold is met (3 more fire-safety candidates
queued in the same batch as of this session).
