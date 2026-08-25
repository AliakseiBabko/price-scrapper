# Fire Safety & Smoke Detection

Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]]. Created 2026-08-25 — the first fire-safety/smoke-detector source arrived as part of a dedicated 4-video batch targeting this vault's own gap analysis (no prior coverage anywhere), and immediately crossed this project's 3+-source no-page threshold.

> [!NOTE]
> All four sources are single-account (four different channels, no repeats), general Russian-language fire-safety/smoke-detector technique — one source (Nikolai/АПС СОУЭ ОС СКС) cites a real Russian regulatory document (СП 484) by number, kept here as general/comparative reference technique per this project's standing rule, not routed to `16_Legal_and_Regulations/` (Belarus-only, stricter bar — this content isn't Belarus-confirmed). Full source list in [[12_Engineering_and_Systems/analysis/Fire_Safety_Source_Notes|Source Notes]].

## System Types & Detector Taxonomy

Nikolai (Системы безопасности и связи АПС, СОУЭ, ОС, СКС) explains **the core system-design choice: addressable vs. non-addressable**. Non-addressable panels (threshold-loop type — "Гранит," "Верест," "Сигнал-20М/20П") let dozens of detectors share one loop with no individual ID; on trigger you only learn *which loop*, not *which detector* — real practical consequence: a false alarm in a 30-detector non-addressable system means physically checking every room in a panic. Addressable systems (popular brands: Болид/Bolid, Стрелец/Strelets) report each detector's individual status, but **addressable hardware from different manufacturers generally can't be mixed** — no protocol compatibility, unlike non-addressable detectors which work with any compatible threshold-loop panel. **Recommendation: for 500m²+ or a separate building, go addressable** — for a typical apartment the difference barely matters in practice.

**Detector-type selection is code-governed, based on the dominant fire factor in the room** (Nikolai cites СП 484 п.62): furniture/combustibles → smoke-dominant → smoke detectors. High-dust or high-humidity rooms (kitchens, production spaces) → smoke detectors false-trigger on dust/steam → use heat detectors instead. Five detector categories exist beyond the common point smoke/heat types: **linear (beam) detectors** for ceilings above 12m (rectangular detection zone, max 4.5m beam-to-wall / 9m between beams, rated to 21m ceiling height); **flame detectors** for gas/flammable-liquid/metal-fire environments (triangular detection zone, best models combine IR + UV sensors to cut false triggers); **linear heat detectors** (a thermocable whose resistance changes with temperature, used above suspended ceilings/under raised floors); and **aspirating detectors** (a central unit that actively samples air through a perforated PVC tube network — each hole counts as one point-detector-equivalent for coverage purposes).

→ **[[12_Engineering_and_Systems/analysis/Fire_Safety_System_Types_and_Selection|Full detail]]** (point-detector coverage-circle geometry, linear-detector 60cm/roof-shape/sandwich-panel exclusions, addressable-linear reset advantage)

## How a Smoke Detector Actually Works

СТРОИТЕЛЬСТВО И РЕМОНТ and Системы безопасности (a separate hands-on wiring demo, using detector model ИП 212-45) agree on the same underlying mechanism, described two complementary ways: an **optical chamber's transparency** is continuously monitored — smoke, soot, or steam reduce transparency and trip an alarm; and, mechanically, an **infrared emitter reflects off smoke particles onto a photodiode** — once the reflected signal crosses a threshold, the detector's internal resistance drops and it registers fire. **Any airborne particulate that scatters light triggers it** — cigarette/vape smoke, dust, soot, even plain water vapor near a kitchen or bathroom, a real false-trigger risk worth planning placement around.

**Alarm reset requires removing power from the detector/loop** — both a full manual disconnect (≥5 seconds) and a brief loop depower (~0.5 second) via the panel are described across sources, converging on the same underlying principle: the alarm latch only clears once power is actually interrupted, not by any signal-level command alone. Системы безопасности's live smoke-simulator test also surfaced a real practical gotcha: **a detector can re-trigger immediately after reset if residual smoke concentration is still inside the chamber** — ventilate the chamber before assuming a reset "failed."

→ **[[12_Engineering_and_Systems/analysis/Fire_Safety_Detector_Mechanism_and_Wiring|Full detail]]** (2-wire loop terminal convention, end-of-line resistor placement, loop current-budget worked calculation, non-destructive paperclip self-test)

## Placement & Clearance Rules

Both СТРОИТЕЛЬСТВО И РЕМОНТ and ProНатяжной (a stretch-ceiling installer) independently give the same core ceiling-mount clearances: **at least 0.5m from light fixtures, power cables, or any EMI source** (to avoid false triggers), and if wall-mounted, **~10cm down from the ceiling and 0.5m from the nearest corner**. ProНатяжной adds a rule the other sources don't state: **at least 0.5m between adjacent detectors themselves**. Coverage-quantity guidance: code minimum is roughly one detector per 15-18m², but СТРОИТЕЛЬСТВО И РЕМОНТ explicitly recommends **at least two detectors even in a small room**, specifically for false-alarm discrimination — a single detector's trigger is ambiguous, two independent triggers together are treated as a confirmed event.

## Installation on a Stretch Ceiling (Direct Relevance to This Project)

ProНатяжной's real job-site installation is the most directly applicable source here, since this project's own household uses stretch ceilings in several rooms. **The mounting platform (закладная, ~135mm diameter) must go up *before* the stretch-ceiling film is fitted** — secured to the structural ceiling, wired, then the film is stretched over it and only afterward cut open at the platform location. **Use 4 suspension hangers, not 2**, for rigidity — fewer risks the platform sagging inward over time. Once the film is on, a reinforcing ring is glued at the penetration point (35-50mm both work, since the platform itself overlaps the ring) and a cross-slit cut through it to pull the wiring through cleanly. The detector's terminal screws are described as fragile — over-torquing strips them on the first try, so go gently.

→ **[[12_Engineering_and_Systems/analysis/Fire_Safety_Stretch_Ceiling_Installation|Full detail]]** (full sequencing walkthrough, wire-prep technique, final-verification step)

## Whole-Apartment Integration

СТРОИТЕЛЬСТВО И РЕМОНТ mentions (not itself demonstrated) a **power-contactor integration**: wiring a contactor to the alarm system so that even one smoke-detector trigger automatically cuts electricity to the entire dwelling — a real fire-safety measure to de-energize wiring during an active fire, worth considering alongside the security-system relay-output pattern described on [[12_Engineering_and_Systems/analysis/Security_Systems|Security Systems]].

## Source Notes

Traceability record moved to its own page — [[12_Engineering_and_Systems/analysis/Fire_Safety_Source_Notes|Source Notes]]. Not reader content, kept off this page by design.

## Change Log

Editorial history moved to its own page — [[12_Engineering_and_Systems/analysis/Fire_Safety_Change_Log|Change Log]]. Not reader content, kept off this page by design.
