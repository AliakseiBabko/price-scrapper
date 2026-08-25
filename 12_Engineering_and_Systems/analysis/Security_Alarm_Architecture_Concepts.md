# Security Systems — Alarm Architecture Concepts

Detail page for [[12_Engineering_and_Systems/analysis/Security_Systems|Security Systems]]. Source: Винтошпунт, a general "we film everything" content channel — a single-installation showcase of a Pima Force alarm system. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_jNGss4BSnLQ_vintoshpunt_pima_force_alarm_mechanism|jNGss4BSnLQ]]]

> [!WARNING]
> **This source's entire framing is high-promotion for a specific product** — explicitly billed as "one of the best security systems in the world." That superlative claim is the channel's own marketing framing, not verified or extractable as fact, and is not adopted here. **Only the general, brand-agnostic architecture concepts the installation demonstrates are recorded below** — Pima-Force-specific product/model claims are deliberately excluded from this page's prose.

## Hybrid Wired/Wireless Sensor Architecture

This installation (a wood-frame house) used wired 4-conductor infrared motion sensors and wired smoke detectors as the default, adding a wireless expander module **specifically because running cable to some locations in the wood structure proved impractical**. A real, generalizable design principle independent of brand: **default to wired for reliability, use wireless selectively only where cable routing is genuinely difficult** — not a starting assumption that wireless is simpler or preferable.

A distinct **"curtain"-type window motion sensor** is also named, as a category separate from room-interior PIR motion sensors — a real sensor-type distinction worth knowing when comparing window-specific vs. general-room coverage options.

## Line Supervision / Tamper Detection

Demonstrated live: cutting or disconnecting one wire from a wired keypad is detected by the panel as a fault and immediately reported to both the monitoring station and the client's app. Separately, opening the keypad's housing triggers a distinct tamper-switch event, also reported centrally. **This is a general alarm-system design concept worth evaluating on any system, regardless of brand** — a system without line supervision/tamper detection can be defeated by simply cutting a wire with no alert generated at all.

## Multi-Path Communication Redundancy

Primary channel: the home's Ethernet/internet connection. A Wi-Fi module was added when a direct wired run between router and panel wasn't available. A GSM module provides a backup communication channel to the monitoring station independent of the internet-based channel, and sends SMS notifications on its own. **General principle**: relying on a single communication path (internet-only, for example) is a real failure mode a hybrid multi-channel design avoids — worth checking for on any system being considered, not specific to this brand.

## UPS Backup Power for the Detector Loop

A dedicated uninterruptible power supply specifically for the security sensors (separate from any general household backup power) was described as part of the standard setup — worth treating as a baseline expectation for a wired alarm installation, not an optional extra.

## Panel-as-Automation-Controller

Programmable relay outputs (on the main panel board or a separate relay expander) were used in this installation to enable app-controlled gate opening/closing — a real example of an alarm panel doing double duty as a general home-automation controller, not just intrusion detection. Compare with the smart-home controller/sensor/actuator architecture on [[12_Engineering_and_Systems/analysis/Smart_Home_Systems|Smart Home Systems]], which describes the same relay/actuator pattern from a dedicated smart-home-system angle.

## Alarm-to-Camera Integration

The site's CCTV system was integrated with the alarm panel so specific alarm events trigger push notifications containing a direct video-clip link — a real, useful integration pattern (alarm-triggered video snippet delivery) independent of which specific camera/panel brand is chosen. See [[12_Engineering_and_Systems/analysis/Security_Camera_Installation_Technique|Camera Installation Technique]] for the camera-side wiring/assembly detail this would connect to.

## Assumptions / Uncertainties

No city/region stated (private wood-frame house). `single-account`, high promotional ratio, partial extraction only — brand/model-specific claims (panel model, specific sensor brands/countries of manufacture) are recorded in the underlying extraction note for traceability only, never as endorsements on this page.
