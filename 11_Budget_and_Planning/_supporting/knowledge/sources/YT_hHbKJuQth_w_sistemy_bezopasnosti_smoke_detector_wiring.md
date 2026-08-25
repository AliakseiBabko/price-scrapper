---
source_type: video transcript (security-systems technician channel, hands-on wiring demo, auto-generated captions)
source_url: https://www.youtube.com/watch?v=hHbKJuQth_w
video_id: hHbKJuQth_w
transcript_file: _Archive/processed_sources/20260825_sistemy_bezopasnosti_smoke_detector_wiring_71a691a1.txt
fetched: 2026-08-25 (anonymous, youtube-transcript-api, ru auto-generated captions)
upload_date: 2024-11-12 (confirmed via yt-dlp metadata)
channel: Системы безопасности (Security Systems), channel_id UCi-z-pYwyVrUSesCo0ST_Cw
source_metadata_location: not stated (no city/region named in transcript)
language: ru
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 10
promotional_ratio: low
corroborates_existing: false
---

# Extraction Note — "Дымовые пожарные датчики (подключение, устройство, принцип работы)" (YouTube hHbKJuQth_w)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

Hands-on technician demo, low promotional ratio — no product upsell, uses
a generic professional fire panel ("Сигнал-20П" / Signal-20P) purely as a
worked wiring example and a named detector model (ИП 212-45, a real
2-wire optoelectronic smoke detector) for teaching the general terminal
convention. Genuinely technical: terminal-by-terminal wiring, loop
current budgeting, and detector internals with a live smoke-simulator
demonstration.

## Electrical / Regulations — New Facts

- **2-wire loop wiring convention (fire loop)**: this detector type (ИП
  212-45) is powered directly from the alarm loop itself — no separate
  power wiring needed. On the panel side, each loop terminal has a
  standard "+"/"-". On the detector, **terminal 2 is always the loop "+"
  regardless of whether it's the incoming or outgoing wire**; terminals 3
  and 4 are the "-" for outgoing/incoming respectively. Per-instruction
  convention: incoming wire from the panel/previous detector lands on
  terminals 2+4; outgoing wire to the next detector in the daisy-chain
  leaves from terminals 2+3.
- **⚠️ End-of-line resistor placement matters mechanically, not just by
  convention**: the terminating resistor must go on terminals 2+3 of the
  *last* detector in the chain. Demonstrated live: wiring the resistor to
  2+4 instead makes the panel report a loop fault, because the loop
  never "sees" the resistor in the expected position. The source
  deliberately wired one detector backwards on camera to prove the loop
  still physically works either way electrically, but recommends **never
  doing it that way in practice** — keeping every detector's incoming/
  outgoing wiring consistent (input always same terminal pair) makes
  future maintenance/troubleshooting far easier, since a technician can
  assume a consistent convention across the whole installation instead
  of checking each detector individually.
- **Loop capacity is a real current-budget calculation, not a guess**:
  worked example — this panel's loop supports up to 3mA total current;
  this specific detector draws 45µA each; 3mA ÷ 45µA ≈ 66 detectors
  theoretically fit on one loop. **Always check the specific panel's own
  datasheet loop-current spec and the specific detector's own current
  draw** before assuming a detector count per loop — this varies by
  hardware, not a fixed universal number.
- **Remote signal-repeater device for concealed/above-ceiling
  installations (УСС / "устройство сигнализации" — remote loop-status
  indicator)**: when detectors are mounted in a concealed space (above a
  suspended/false ceiling, "запотолочное пространство"), a visible remote
  indicator is wired in alongside them so a technician/occupant can see
  alarm/fault status without accessing the concealed space directly.
  **⚠️ Concealed-space detectors must go on their own dedicated loop,
  never combined with detectors mounted directly on the visible ceiling**
  — kept separate specifically so a technician can immediately tell
  which physical location triggered.
- **Remote indicator wiring convention**: "+" from the detector's
  terminal 1, "-" from terminal 2 on one side; on the detector itself,
  "+" lands on terminal 4, "-" on terminal 3 — a distinct terminal
  mapping from the main loop wiring above, worth not confusing the two.
- **Detector internals and operating mechanism (optoelectronic/infrared
  reflection type)**: contains a smoke chamber with an infrared emitter
  (optopair) and a photodiode receiver. Normally the emitter's pulses
  don't reach the receiver. When smoke particles enter the sensitive
  zone, the emitted infrared reflects off the particles onto the
  photodiode; once the resulting signal crosses a threshold, the
  detector's internal resistance drops and it registers a fire-alarm
  state. **Alarm reset requires removing power from the loop for about
  half a second** (via the panel's loop-reset function), matching the
  disconnection principle in the companion smoke-detector source
  (`YT_RwyPR2RFZYM`).
- **Live smoke-simulator test confirms mechanism, including a re-trigger
  caveat**: using an aerosol smoke simulator sprayed into the chamber,
  the detector and the remote indicator both correctly signaled alarm on
  the panel. **After resetting, the detector re-triggered a second time**
  because residual smoke concentration was still inside the chamber —
  the source ventilated the chamber before it would stay clear, a
  practical real-world note that a reset can appear to "fail" simply
  because the chamber hasn't actually cleared yet, not because of a
  wiring fault.

## Assumptions / Uncertainties

- No city/region stated.
- Panel model (Сигнал-20П) and detector model (ИП 212-45) are named
  professional/commercial fire-alarm hardware, not consumer smart-home
  products — flagged as reference-grade professional installation
  practice, still generally applicable technique (terminal conventions,
  loop-budgeting method, concealed-space separation rule) regardless of
  specific hardware chosen.
- `single-account`, low promotional ratio.

## Relevance to This Project's Topic

Second fire-safety/smoke-detector source for this vault. Independently
corroborates the alarm-reset-via-depowering mechanism from
`YT_RwyPR2RFZYM` (a different channel/practitioner) and adds real wiring/
loop-budgeting technique not covered there. Routed toward
`12_Engineering_and_Systems/analysis/Fire_Safety_and_Smoke_Detection.md`
once the 3+-source threshold is met.
