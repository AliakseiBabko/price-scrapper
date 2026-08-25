---
source_type: video transcript (fire-alarm-systems specialist/trainer channel, technical explainer, auto-generated captions)
source_url: https://www.youtube.com/watch?v=rsTdXaLenEw
video_id: rsTdXaLenEw
transcript_file: _Archive/processed_sources/20260825_nikolai_fire_detector_types_cd7a0563.txt
fetched: 2026-08-25 (anonymous, youtube-transcript-api, ru auto-generated captions)
upload_date: 2024-01-09 (confirmed via yt-dlp metadata)
channel: Системы безопасности и связи АПС, СОУЭ, ОС, СКС, channel_id UCtWbqP5BuuuHh61fvJ0UHsg (presenter identifies himself as Nikolai)
source_metadata_location: Russia (references Russian СП 484 code standard; no specific city named)
language: ru
extraction_taxonomy: custom (this project's renovation-budgeting taxonomy, caller-defined mode)
fact_yield: 15
promotional_ratio: medium
corroborates_existing: false
---

# Extraction Note — "Датчики дыма, пожарные извещатели - какие бывают?" (YouTube rsTdXaLenEw)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference — (4) external validation (none performed).

## Source Metadata / Promotional Context

Fire-alarm-systems trainer/specialist channel (presenter "Nikolai"),
addressed to a somewhat more technical/professional audience than a
consumer renovation video, but the type-selection logic, coverage
geometry, and placement rules are directly usable general reference.
Medium promotional ratio: a mid-video plug for a paid "low-current
systems installer" training course and the presenter's own book, both
excluded from extraction — the surrounding technical content (detector
types, code citations, coverage geometry) is dense and non-promotional.
Cites a real Russian regulatory document (СП 484) by number — this is
Russia-sourced regulatory content, so per this project's standing rule it
stays in the general budgeting store / `12_Engineering_and_Systems`
technique pages, never in `16_Legal_and_Regulations/` (Belarus-only
folder).

## Regulations / Electrical — New Facts

- **⚠️ Addressable vs. non-addressable systems — the core system-design
  choice**: non-addressable systems (threshold-loop panels like
  "Гранит," "Верест," "Сигнал-20М," "Сигнал-20П") let dozens of
  detectors share one loop with no individual detector ID — on
  trigger/fault, the panel only tells you *which loop*, not which exact
  detector, forcing physical search ("low informativity," the source's
  own stated main drawback). Addressable systems (popular Russian
  brands: Болид/Bolid, Стрелец/Strelets) give each detector its own
  address reporting individual status. **⚠️ Cross-brand incompatibility
  warning specific to addressable systems**: unlike non-addressable
  detectors (which work with any threshold-loop-type panel regardless of
  brand), an addressable detector generally cannot be mixed with a
  different manufacturer's addressable panel — no protocol compatibility.
- **Selection guidance by building scale**: for a small object, the
  difference barely matters practically. **For 500m²+ or a separate
  building, an addressable system is recommended** — on trigger, staff
  can pinpoint the exact room instead of physically checking dozens of
  rooms during a panic/evacuation event, and addressable systems
  integrate far more reliably with automated response systems (fire
  water supply, elevator control-on-alarm, smoke-exhaust ventilation)
  that need to both trigger and auto-reset reliably.
- **⚠️ Detector-type selection is code-governed, based on the dominant
  fire factor of what's stored in the room** (cites СП 484 п.62 — a real
  Russian regulatory document/clause): furniture-storage rooms →
  smoke-dominant fire factor → smoke detectors. High-dust environments
  (e.g. production facilities) → smoke detectors cause false triggers
  from dust → use heat detectors instead. This is a general selection
  principle, not tied to one specific room type.
- **Point smoke detectors ("точечные дымовые")**: usable up to 12m
  ceiling height; detection zone is a circle whose radius is set by
  ceiling height per СП 484's own tables (referenced but not itself
  reproduced numerically in the transcript). Commonly installed near
  entry doors and in most habitable rooms.
- **Point heat detectors ("точечные тепловые")**: detection-zone circle
  is **half the radius** of an equivalent point smoke detector; max
  ceiling height rated for is **9m** (vs 12m for smoke). Each model has
  its own trigger temperature threshold — must be matched to the room's
  actual expected temperature range. **Typical placement: kitchens,
  high-humidity rooms, and high-dust environments** (furniture
  production, paint-spray booths) and **unheated spaces where smoke
  detectors would otherwise false-trigger**.
- **Linear detectors ("линейные"/ИПДЛ, beam-type)**: used above 12m
  ceiling height, rated up to **21m**. Detection zone is a rectangle
  independent of ceiling height: **max 4.5m from the beam's central axis
  to a wall, max 9m between adjacent beam detectors.** Typical use:
  large spaces (gyms, warehouses, production floors).
- **⚠️ Linear-detector alarm-reset caveat (non-addressable only)**: after
  a fire signal, resetting requires a full power cycle to the detector —
  in practice done via an intermediate control module (example given:
  "С2000-КПБ") configured during commissioning to auto-cut power on
  reset. **Addressable linear detectors don't have this problem.** A
  real commissioning/design consideration, not a minor detail — without
  planning for it, you literally can't clear the alarm without manually
  de-powering the detector.
- **Non-addressable linear detectors also typically get remote
  indicator lamps (per-detector status) and remote test buttons** — so
  functional testing doesn't require a lift/scaffolding to physically
  reach the detector.
- **⚠️ Linear-detector mounting height rule, with a real physical
  reason**: must be installed **no lower than 60cm below the ceiling**,
  measured to the emitter's central axis — because smoke accumulates at
  roughly that ceiling-adjacent layer; installing lower means the beam
  either won't detect smoke or detects it significantly late.
- **⚠️ Real-world roof-shape exclusions for linear detectors**: a
  double-pitched (gable) roof where the ridge-to-beam-axis distance
  exceeds 60cm may make this detector type unusable in that orientation
  — sometimes solvable by relocating to a different wall, sometimes not.
  A **ribbed ceiling with ribs protruding more than 60cm** also makes
  linear detectors physically unusable (the ribs obstruct the beam).
  **Linear detectors are prohibited on sandwich panels or corrugated
  metal sheeting ("профлист") — must mount only to load-bearing
  structure**; if the wall is sandwich-panel construction, mount around/
  wrapping the underlying metal framework instead.
- **Flame detectors ("извещатели пламени")**: not tied to ceiling
  height at all. Detection zone is a **triangle** (90° angle, ~25m along
  the bisector, per the specific model's manual). Typical use: gas
  combustion, flammable-liquid, and metal-fire environments (industrial
  settings). **Best models combine both infrared and ultraviolet
  sensors** — having both reduces false triggers versus either sensor
  alone. When used for localized detection of a specific piece of
  equipment (rather than whole-room coverage), the "every point of space
  must be covered" requirement doesn't apply the same way as for
  whole-room protection.
- **Linear heat detectors ("линейные тепловые" / heat-sensing cable)**:
  essentially a thermocable whose electrical resistance changes with
  temperature along its full length. Typically used to protect
  concealed spaces — above a suspended ceiling or under a raised/false
  floor.
- **Aspirating detectors ("аспирационные")**: a central processing unit
  connected to PVC sampling tubes (specific configuration/length per
  each model's manual) with small holes drilled along the tube; the unit
  actively draws air through these holes and analyzes it for fire
  indicators. **Each hole in the sampling tube counts as equivalent to
  one point smoke detector** for coverage-requirement purposes.
- **General coverage-geometry principle stated up front**: every point
  in a protected space must be covered by either one addressable
  detector or two non-addressable detectors (redundancy requirement
  specific to non-addressable systems, tying back to the
  low-informativity drawback above).

## Assumptions / Uncertainties

- Russia-sourced regulatory citation (СП 484) — per this project's
  standing rule, usable as general/comparative reference technique in
  the main store and `12_Engineering_and_Systems`, **never** to be routed
  into `16_Legal_and_Regulations/` (Belarus-only, stricter bar).
- `single-account`, medium promotional ratio (course/book plug excluded
  from extraction).
- Numeric coverage-radius tables referenced (СП 484 Table 1/2) are cited
  by name but not reproduced with actual numbers in the transcript — not
  captured as numeric data here, flagged as a real gap if anyone needs
  the exact radius-vs-ceiling-height table later.

## Relevance to This Project's Topic

Third and densest fire-safety/smoke-detector source for this vault —
crosses this project's 3+-source no-page threshold on its own merit
alongside the two prior sources (`YT_RwyPR2RFZYM`, `YT_hHbKJuQth_w`).
Provides the system-level vocabulary (addressable/non-addressable,
detector-type taxonomy, code-driven selection logic) the other two
sources assume but don't explain. New dedicated page created this
session:
`12_Engineering_and_Systems/analysis/Fire_Safety_and_Smoke_Detection.md`.
