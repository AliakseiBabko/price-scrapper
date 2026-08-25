# Fire Safety — System Types & Selection

Detail page for [[12_Engineering_and_Systems/analysis/Fire_Safety_and_Smoke_Detection|Fire Safety & Smoke Detection]]. Primary source: Nikolai (Системы безопасности и связи АПС, СОУЭ, ОС, СКС), a fire-alarm-systems trainer/specialist channel. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_rsTdXaLenEw_nikolai_fire_detector_types|rsTdXaLenEw]]]

## Addressable vs. Non-Addressable Systems

- **Non-addressable ("threshold-loop") panels** — examples named: Гранит, Верест, Сигнал-20М, Сигнал-20П. Dozens of detectors can share one loop with no individual detector ID. On trigger or fault, the panel only reports *which loop*, not *which detector* — Nikolai's own stated main drawback, "low informativity." **Coverage-redundancy consequence**: since a single detector's trigger is ambiguous on this kind of system, the code requires every point of protected space to be covered by *two* non-addressable detectors (vs. one addressable detector) — direct false-alarm mitigation.
- **Addressable systems** — popular Russian brands named: Болид/Bolid, Стрелец/Strelets. Each detector reports its own individual address/status to the panel. **⚠️ Cross-brand incompatibility**: unlike non-addressable detectors (which work with any compatible threshold-loop panel regardless of brand), addressable detectors generally cannot be mixed with a different manufacturer's addressable panel — no protocol compatibility between ecosystems.
- **Selection guidance by scale**: for a small object (an apartment), the practical difference is minor. **For 500m²+ floor area or a separate building, addressable is recommended** — pinpointing the exact triggered room during a panic/evacuation beats physically checking dozens of rooms, and addressable systems integrate far more reliably with automated response systems (fire water supply, elevator control-on-alarm, smoke-exhaust ventilation) that need to trigger *and* auto-reset correctly.

## Code-Governed Selection Logic

Nikolai cites СП 484 п.62 (a real Russian regulatory clause) for the underlying principle: **choose detector type by the room's dominant fire factor**, with false-trigger avoidance as a secondary filter.

- Furniture-storage/combustible-material rooms → smoke is the dominant fire factor → smoke detectors.
- High-dust environments (production facilities, workshops) → smoke detectors cause false triggers from ambient dust → substitute heat detectors.
- High-humidity/unheated spaces → same logic applies (smoke detectors false-trigger on steam/condensation) → heat detectors instead.

## Detector-Type Reference

| Type | Detection zone shape | Height limit | Typical use |
|---|---|---|---|
| Point smoke ("точечные дымовые") | Circle, radius set by ceiling height (СП 484 tables — not numerically reproduced in this source) | Up to 12m | Most habitable rooms, near entries |
| Point heat ("точечные тепловые") | Circle, **half the radius** of an equivalent smoke detector | Up to 9m | Kitchens, high-humidity/high-dust rooms, unheated spaces |
| Linear/beam ("линейные"/ИПДЛ) | Rectangle, independent of ceiling height — max 4.5m axis-to-wall, max 9m between adjacent beams | Up to 21m | Large spaces: gyms, warehouses, production floors |
| Flame ("извещатели пламени") | Triangle, 90° angle, ~25m along the bisector (per specific model manual) | Not tied to ceiling height | Gas/flammable-liquid/metal-fire industrial environments |
| Linear heat (thermocable) | Continuous cable, resistance changes with temperature along its length | N/A | Concealed spaces: above suspended ceilings, under raised floors |
| Aspirating | Each perforated-tube hole counts as one point-detector-equivalent | N/A | Where sampling-based early detection is needed |

- **Point heat detectors** — each model has its own trigger-temperature threshold; must be matched to the room's actual expected temperature range, not assumed universal.
- **Flame detectors** — best models combine **both infrared and ultraviolet sensors**, since having both reduces false triggers versus either sensor alone. When used for localized detection of a specific piece of equipment rather than whole-room coverage, the "every point of space must be covered" requirement doesn't apply the same way.

## Linear-Detector-Specific Constraints

- **⚠️ Mounting height rule with a real physical reason**: must be installed **no lower than 60cm below the ceiling**, measured to the emitter's central axis — smoke accumulates at roughly that ceiling-adjacent layer, so installing lower means the beam either won't detect smoke or detects it significantly late.
- **⚠️ Roof-shape exclusions**: on a double-pitched (gable) roof where the ridge-to-beam-axis distance exceeds 60cm, this detector type may be unusable in that orientation — sometimes solvable by relocating to a different wall, sometimes not. A ribbed ceiling with ribs protruding more than 60cm also makes linear detectors physically unusable (the ribs obstruct the beam path).
- **⚠️ Mounting-surface prohibition**: linear detectors are **prohibited on sandwich panels or corrugated metal sheeting ("профлист")** — must mount only to load-bearing structure. If the wall is sandwich-panel construction, mount around/wrapping the underlying metal framework instead.
- **⚠️ Alarm-reset caveat (non-addressable linear only)**: after a fire signal, resetting requires a full power cycle to the detector — in practice done via an intermediate control module (example: "С2000-КПБ") configured during commissioning to auto-cut power on reset. **Addressable linear detectors don't have this problem.** A real commissioning consideration: without planning for it, the alarm can't be cleared without manually de-powering the detector. Non-addressable linear installations also typically get remote indicator lamps and remote test buttons, so functional testing doesn't require a lift/scaffolding to physically reach the detector.

## Assumptions / Uncertainties

Russia-sourced regulatory citation (СП 484) — used here as general/comparative reference technique per this project's standing rule, never routed to `16_Legal_and_Regulations/` (Belarus-only, stricter bar). Numeric coverage-radius tables are cited by name (СП 484 Tables 1/2) but not reproduced with actual numbers in the source transcript — a real gap if the exact radius-vs-height table is needed later.
