# Fire Safety — Detector Mechanism & Wiring

Detail page for [[12_Engineering_and_Systems/analysis/Fire_Safety_and_Smoke_Detection|Fire Safety & Smoke Detection]]. Primary sources: СТРОИТЕЛЬСТВО И РЕМОНТ (branded hub ecosystem demo) and Системы безопасности (hands-on technician wiring demo, detector model ИП 212-45). [source: [[_Sources/YT_RwyPR2RFZYM_stroy_i_remont_smoke_detectors_general|RwyPR2RFZYM]]] [source: [[_Sources/YT_hHbKJuQth_w_sistemy_bezopasnosti_smoke_detector_wiring|hHbKJuQth_w]]]

## How the Detection Mechanism Works

СТРОИТЕЛЬСТВО И РЕМОНТ describes it as an **optical chamber whose transparency is electronically monitored** — a clear chamber reads as normal; smoke, soot particles, or even steam/vapor reduce transparency (partially or fully) and the electronics send an alarm signal. Системы безопасности's technician demo describes the same physical process mechanically: an **infrared emitter's pulses normally don't reach the photodiode receiver**; when smoke particles enter the sensitive zone, emitted infrared reflects off the particles onto the photodiode, and once the resulting signal crosses a threshold, the detector's internal resistance drops and it registers a fire-alarm state. Both descriptions are the same underlying optoelectronic/light-scattering mechanism, described from two angles.

**What else triggers it (false or real)**: any airborne particulate that reduces chamber transparency — cigarette smoke, hookah/vape vapor, dust, soot, and plain steam/water vapor. A real installation caveat for detectors placed near kitchens/bathrooms.

## Loop Wiring — 2-Wire Terminal Convention

Системы безопасности demonstrates a real professional wiring convention on a 2-wire detector (ИП 212-45), powered directly from the alarm loop itself (no separate power wiring needed):

- **Terminal 2 is always the loop "+"**, regardless of whether it's the incoming or outgoing wire. Terminals 3 and 4 are "-" for outgoing/incoming respectively.
- **Convention**: incoming wire from the panel/previous detector lands on terminals 2+4; outgoing wire to the next detector in the daisy-chain leaves from terminals 2+3.
- **⚠️ End-of-line resistor placement matters mechanically, not just by convention**: the terminating resistor must go on terminals 2+3 of the *last* detector in the chain. Demonstrated live: wiring it to 2+4 instead makes the panel report a loop fault, because the loop never "sees" the resistor in the expected position. **Recommendation: keep every detector's incoming/outgoing wiring consistent** (input always the same terminal pair) — makes future maintenance far easier, since a technician can assume one convention across the whole installation rather than checking each detector individually.

## Loop Current Budgeting — A Real Calculation, Not a Guess

Worked example from Системы безопасности: this panel's loop supports up to **3mA total current**; this specific detector draws **45µA each**; 3mA ÷ 45µA ≈ **66 detectors** theoretically fit on one loop. **Always check the specific panel's own datasheet loop-current spec and the specific detector's own current draw** before assuming a detector count per loop — this varies by hardware, not a fixed universal number.

## Cable & Splicing

СТРОИТЕЛЬСТВО И РЕМОНТ's spec: standard cable used is **КСПВ 4×0.4 or 4×0.5mm²**, routed away from light fixtures/power cables/EMI sources (same reasoning as ceiling placement clearances) to avoid false triggers. **⚠️ For full fire-code compliance, replace this cable with fire-resistant-rated cable** instead of standard КСПВ. Any splice/extension joint must be **soldered** (solder + rosin flux), not just twisted — stated as a real safety requirement. Cable can be extended up to 50m from a stock 10m run.

## Concealed-Space Wiring & Remote Indicators

Системы безопасности's demo covers detectors mounted above a suspended/false ceiling ("запотолочное пространство"): a **remote indicator device (УСС)** is wired in alongside them so status is visible without accessing the concealed space. **⚠️ Concealed-space detectors must go on their own dedicated loop, never combined with detectors mounted directly on the visible ceiling** — kept separate specifically so a technician can immediately tell which physical location triggered. Remote-indicator wiring uses a distinct terminal mapping from the main loop wiring above (detector terminal 1 = "+", terminal 2 = "-" on one side; "+"→terminal 4, "-"→terminal 3 on the indicator side) — worth not confusing the two conventions.

## Alarm Reset & Self-Test

- **Alarm reset requires physically removing power** — either a full manual disconnect (СТРОИТЕЛЬСТВО И РЕМОНТ: at least 5 seconds, or a full panel reboot via SMS/app) or a brief loop depower (Системы безопасности: ~0.5 second via the panel's own reset function). Both sources converge on the same underlying principle: the alarm latch clears only once power is actually interrupted, not by a signal-level command alone.
- **⚠️ Real re-trigger gotcha**: Системы безопасности's live smoke-simulator test showed the detector re-triggering immediately after reset because residual smoke concentration was still inside the chamber — the chamber had to be ventilated before the reset would actually stay clear. Worth knowing before assuming a reset "failed" due to a wiring fault.
- **Non-destructive wired-detector self-test (СТРОИТЕЛЬСТВО И РЕМОНТ)**: insert a paperclip into the small test hole in the detector's cover, ~3cm deep into the smoke chamber, simulating smoke particles without needing an actual smoky room — indicator lights confirm the test passed.

## Hardware Specs (Branded Hub Example — СТРОИТЕЛЬСТВО И РЕМОНТ)

- **Wired detector**: 10m stock cable + plug, ~100mm diameter × ~40mm housing, rated -30°C to +55°C at up to 90% RH.
- **Wireless detector**: -0°C to +55°C rated (narrower cold range than wired), up to 90% RH, ~1 year on one 9V "Krona"-type battery (shorter below -10°C or with unstable radio link), 868 MHz with built-in antenna. Signal-quality test: hold the pairing magnet to the same spot used for programming — more frequent indicator blinking means better signal; if it doesn't blink at all, relocate the detector.
- **Low-battery behavior (code requirement)**: beeps roughly every 30 seconds and flashes a battery-status indicator; the panel can push SMS/app notifications too.
- **System capacity**: up to 32 wireless detectors, up to 100 wired detectors (via port splitters).
- **⚠️ Reliability comparison, source's own stated opinion**: wired detectors are described as the most reliable — not subject to battery depletion, radio interference, or signal attenuation through reinforced-concrete floor slabs, unlike wireless units.

## Assumptions / Uncertainties

The exact hub/panel brand in СТРОИТЕЛЬСТВО И РЕМОНТ's video is ASR-uncertain (phonetically transcribed as "кто control"/"кс control") — treated as a specific branded ecosystem, not adopted as a brand recommendation; the underlying mechanism/wiring/placement rules are general. Панель model (Сигнал-20П) and detector model (ИП 212-45) in the Системы безопасности demo are named professional/commercial fire-alarm hardware — the terminal conventions and loop-budgeting method generalize regardless of specific hardware chosen. No city/region stated in either source.
