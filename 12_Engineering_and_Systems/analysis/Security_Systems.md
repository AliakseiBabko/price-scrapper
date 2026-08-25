# Security Systems

Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]]. Created 2026-08-25 — the first security-system sources (CCTV cameras, alarms) arrived as part of a dedicated batch targeting this vault's own gap analysis (no prior coverage anywhere), and crossed this project's 3+-source no-page threshold with 3 usable sources (a 4th candidate had no captions available).

> [!NOTE]
> Two of three sources are real hands-on DIY camera-system installations (independent channels, no overlap); the third (Pima Force alarm demo) is a heavily brand-promotional single-installation showcase — its brand-specific claims are excluded here, only the general architecture concepts it demonstrates are carried into this page. Full source list in [[12_Engineering_and_Systems/analysis/Security_Systems_Source_Notes|Source Notes]].

## Camera System Wiring & Assembly

Vasily Tarasov (Ucam / Системы видеонаблюдения) walks through a full coax-based CCTV kit build: **screw the HDD into the DVR chassis, don't just set it in place** — an unsecured drive vibrates against the housing during operation and typically fails within 1-1.5 years. КВК combined cable carries power (two thin +/- leads) and video (one thick coax) together; BNC connector assembly is a real technique with a failure mode worth knowing (**don't over-torque the small screw** — it strips easily). **Prefer WAGO lever connectors over twisted joints for all power splicing** — twisted-only joints are a real, checkable cause of intermittent camera signal/power loss. The same wiring pattern scales to 16 cameras.

Рабочая Молодежь's real personal workshop-CCTV project adds independent, richer technique: an **SD-card-per-camera architecture** (each camera is its own self-contained recorder, no central DVR needed) with **detection-based recording** to conserve storage; a **PoE switch vs. separate 12V power** tradeoff (PoE = one cable per camera for power+data, cheaper non-PoE switch = separate power supply needed at each camera); and a full RJ-45/T568B crimping walkthrough with a cable tester verification step.

→ **[[12_Engineering_and_Systems/analysis/Security_Camera_Installation_Technique|Full detail]]** (multi-format jumper-pin water-ingress caution, structured-cabling slack rule, real 1-workday install-time data point)

## Security-Specific Installation Choices

Рабочая Молодежь's project is the richest source here for security-specific (not just electrical) reasoning: **exterior cable runs should route directly into a junction box, never along an exposed exterior wall** — an exposed run is trivially easy to cut. **Plastic vs. metal junction box is a real, quantified security tradeoff** (~90 RUB plastic vs. a meaningfully pricier metal option that resists tampering and lets a camera mount directly to the box) — the source accepted the cheaper plastic option specifically because these particular cameras self-report a connection-loss/tamper event, a partial mitigation worth weighing against the box choice itself, not a substitute for it.

Vasily Tarasov adds a distinct point: **insulate/tape exposed multi-format jumper wires on a camera's PCB** — if water bridges the contacts, the camera's signal format can change unexpectedly on its own, a real field failure mode independent of the box-security question above.

→ **[[12_Engineering_and_Systems/analysis/Security_Camera_Installation_Technique|Full detail]]** (same page as wiring — installation and security choices are documented together per-source)

## Alarm-System Architecture (General Concepts, Brand Claims Excluded)

The Pima Force installation demo (Винтошпунт, a general-content channel — **high promotional ratio, brand claims excluded per this vault's advertising filter**) still demonstrates real, brand-agnostic alarm-system design patterns worth carrying forward: a **hybrid wired/wireless sensor architecture** (default to wired for reliability, add wireless only where cable routing is genuinely impractical — the source's own reason was a wood-frame house structure); **line-supervision/tamper detection** on wired devices (cutting a keypad wire or opening its housing both trigger a distinct, centrally-reported fault — a real defense against a naive "just cut the wire" attack); **multi-path communication redundancy** (Ethernet primary, Wi-Fi as a fallback when a wired router-to-panel run isn't available, GSM as an independent backup channel with its own SMS alerting); and **alarm-panel-to-camera integration**, where a triggered alarm event pushes a notification containing a direct video-clip link.

→ **[[12_Engineering_and_Systems/analysis/Security_Alarm_Architecture_Concepts|Full detail]]** (UPS backup power for the detector loop, programmable relay outputs for gate-automation integration)

## Fire-Safety Overlap

A power-contactor pattern (cutting all electricity on a fire-alarm trigger) is documented on [[12_Engineering_and_Systems/analysis/Fire_Safety_and_Smoke_Detection|Fire Safety & Smoke Detection]] — the same programmable-relay-output concept used here for gate automation applies there for a safety response instead of a convenience one, worth reading together if planning either system's panel/relay capacity.

## Source Notes

Traceability record moved to its own page — [[12_Engineering_and_Systems/analysis/Security_Systems_Source_Notes|Source Notes]]. Not reader content, kept off this page by design.

## Change Log

Editorial history moved to its own page — [[12_Engineering_and_Systems/analysis/Security_Systems_Change_Log|Change Log]]. Not reader content, kept off this page by design.
