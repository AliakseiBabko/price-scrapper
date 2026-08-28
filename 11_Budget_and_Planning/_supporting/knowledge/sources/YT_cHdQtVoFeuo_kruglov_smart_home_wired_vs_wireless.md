---
source_type: video transcript (turnkey renovation company, structured "wired vs. wireless smart home" comparison, Russian, ASR auto-generated captions — no punctuation)
source_url: https://www.youtube.com/watch?v=cHdQtVoFeuo
video_id: cHdQtVoFeuo
transcript_file: not separately archived — fetched inline via youtube_transcript_api (sha256 d81d9b456c8d8ffa28d87e0e8e83cd54d6d553c2602429d582da2acc57d6be69)
fetched: 2026-08-28 (anonymous, youtube-transcript-api, ru auto-generated captions, language_code=ru)
upload_date: 2025-10-17 (confirmed via yt-dlp metadata; duration 1085s / ~18 min)
channel: Константин Круглов | Ontario (Konstantin Kruglov, Ontario — Moscow/Moscow-region turnkey renovation company)
regional_applicability: Moscow / Moscow region (channel's stated general market; not re-confirmed spoken specifically in this video, though Zigbee wall-penetration caution is framed generically, not Russia-specific)
currency: RUB figures stated (wired installation ≥200,000 RUB; wired commissioning ≈200,000 RUB; wireless installation from 0-20,000+ RUB); trailing-6-month USD/RUB rate before 2025-10-17 used for conversion
language: ru
extraction_taxonomy: routed to Smart_Home_Systems.md as a major new architecture-comparison section
fact_yield: 18 (full — Round 15, smart-home pair, member 1/2; genuinely fresh ground as anticipated — this channel had no prior dedicated smart-home content, and this store's only existing smart-home source, Kodolov, covers pricing/devices at a much lighter level of architectural detail)
promotional_ratio: low (one CTA near the end, plus a free Telegram-channel guide offer)
corroborates_existing: light — this store's existing Smart_Home_Systems.md content (Kodolov) has a one-line "wired is fast/reliable; Wi-Fi easier to install but less stable" note that this video substantially deepens and systematizes; no direct conflict found
---

# Extraction Note — Konstantin Kruglov (Ontario): "Какой умный дом выбрать? Проводной vs беспроводной" (YouTube cHdQtVoFeuo)

## Evidence levels
(1) transcript text — (2) YouTube metadata — (3) contextual inference.

## Source Metadata / Promotional Context

Konstantin Kruglov, owner of Ontario. **Smart-home pair, member 1/2** —
this channel's first dedicated smart-home explainer, and it delivers on
the dispatch note's "genuinely fresh ground" expectation. A structured,
~18-minute wired-vs-wireless architecture comparison across 12 concrete
criteria, distinct in both depth and framing from this store's only
existing smart-home source (Sergey Kodolov, a device/pricing-level
overview). Low promotional ratio; the comparison reads as genuinely
even-handed (recommends wired for large/complex installs, wireless for
budget/already-finished apartments, not a one-sided pitch for either).

## Genuinely New Content

**Decision triggers — when only one option is actually viable, not a
preference call:**

- **Wireless-only cases**: (1) the renovation is already finished or at
  the finish-works stage — running new low-voltage/electrical cable is
  no longer possible; (2) the whole-project smart-home budget is under
  **~1,000,000 RUB**; (3) the household genuinely enjoys tinkering with
  settings and wants to be able to re-pair sensors, adjust automations,
  and change scenarios themselves going forward.
- **Wired-only cases**: (1) the property is large — an apartment **100m²+**,
  a plot **10+ соток (~1,000m²+)**, or a house **200m²+**; (2) the
  household wants to integrate complex equipment — boilers, hydronic
  heated-floor thermostatic heads, supply/exhaust ventilation systems —
  which physically cannot connect to a wireless system; (3) the
  household doesn't want to understand the underlying mechanism at all
  and wants full turnkey handling (design documentation, installation,
  and years of warranty support all handled by one contractor).

**Wired system architecture and build stages**:

- All core control modules/controllers live in **one dedicated
  smart-home electrical cabinet**, with cables radiating out to devices
  from there. A wired system doesn't exclude wireless-protocol devices
  entirely — it can still incorporate some.
- **Four-stage build sequence**: (1) design documentation development;
  (2) installation work (physical module/sensor/device connection,
  commissioning); (3) remote-control app configuration and handover to
  the client; (4) scenario/automation configuration.

**Wireless system architecture and mesh protocols — new vocabulary for
this store**:

- A **hub** is the "brain" of a wireless system — can be a dedicated hub
  device, a smart speaker, or a Wi-Fi router with built-in hub
  functionality. All device signals route either directly to the hub, or
  — if a device is out of the hub's direct range — relay through other
  devices in sequence (this relay behavior is what makes it a **mesh**
  network); a smart outlet, for instance, can double as a signal
  repeater for other devices.
- **Three full "mesh" protocols compared, a first for this store**:
  **Zigbee** — the most widespread and cheapest, huge device ecosystem,
  but **poor at penetrating thick walls**; **Z-Wave** — pricier, but
  penetrates thick walls better than Zigbee, with the caution that
  devices designed for the US market may not work correctly in Europe
  or Russia; **Thread** — positioned as the future Matter-standard
  protocol, modern/fast/energy-efficient, but far fewer devices support
  it currently than Zigbee.

**Structured 12-criteria wired-vs-wireless comparison table, this
store's first this systematic**:

1. **Design requirement**: wired needs professional design documentation
   in 100% of cases; wireless generally doesn't (a household can plan it
   in notes, more elaborate software, or just mentally, depending on
   system complexity).
2. **Installation cost**: wired **from ≈200,000 RUB (≈$2,500)**, scaling
   with room area and device count (cable pulling, module installation);
   wireless can be **≈0 RUB** for full self-installation, or **from
   ≈20,000 RUB (≈$250)** if hiring a specialist for something like
   installing a smart relay inside a back-box.
3. **Commissioning/setup cost**: wired's commissioning is performed by
   the same specialized company that did design+installation, at
   roughly the same **≈200,000 RUB** order of magnitude; wireless
   systems are typically self-installed or handled by an independent
   wireless-specialist freelancer — **large smart-home installation
   companies typically don't offer wireless-system installation
   services at all**.
4. **Device cost, "subjective" framing**: a single wired controller
   costs more than a single wireless controller in isolation, but a
   wired controller can drive **~6 lighting circuits** vs. a wireless
   controller's **~1-2**, so like-for-like functional cost is roughly
   comparable; wired-only devices (boiler control, hydronic heated-floor
   thermostatic heads, ventilation control) command a real cost premium
   for their added functional scope, not brand markup.
5. **Device type range**: both systems can do lighting, sockets, and
   leak-protection; only wired can add the "complex" device category
   above (boilers, hydronic floor heating, ventilation).
6. **Aesthetics**: wireless devices are described as more miniature and
   stylish, blending into any interior style (classic, hi-tech, modern
   minimalism); many wired devices/sensors are visually bulkier and
   harder to integrate — expected to improve as wired-device
   manufacturers respond to demand, but currently a real wired
   disadvantage.
7. **Power-outage autonomy**: both systems fail completely with no grid
   power at all; with a UPS, only priority circuits (alarm, security,
   leak protection) are kept alive in either system — wireless devices
   run on batteries so are inherently unaffected by grid loss, but
   powered wireless devices (smart AC, smart kettle, smart outlet) still
   won't function without power regardless.
8. **Internet-outage behavior — a real wired advantage**: wired-system
   devices connected by direct cable keep functioning normally (alarm,
   leak protection, cable-based scenarios) with no internet; wireless
   **voice control specifically stops working** (hub/speaker both need
   connectivity), though battery-powered wireless gas/smoke detectors
   still function and alert without internet.
9. **Radio interference/jamming resistance**: a wired system's signal
   cannot be jammed by an RF jammer, and room/house size or wall
   thickness has zero effect on it. A wireless mesh network is
   vulnerable to jamming and to protocol-specific wall-penetration
   limits — **Zigbee specifically struggles in monolithic-partition
   buildings or houses over roughly 150-300m²**, producing regular
   interference and device dropouts.
10. **Control-method flexibility**: wired supports any control method
    simultaneously, including a **permanently wall-mounted static
    control panel**; wireless substitutes a tablet/smartphone, physical
    switches, or voice control instead of a fixed wall panel.
11. **Scalability during use — a sharp, quantified contrast**: wireless
    scales near-infinitely post-installation (the source's own figure:
    up to **1,000 devices**) — add or remove sensors/scenarios instantly.
    Wired scalability is **near zero after installation**: new cable
    runs can't be pulled into an already-finished wall, each controller
    has a hard-fixed number of physical connection points (worked
    example: 6 lighting circuits per controller, no more), and any
    change needs the original specialist company called back out.
12. **Reliability/failure rate — the source's sharpest stated
    preference**: a wired system is described as far more stable, with
    sensor failures roughly **once every several years** based on the
    company's own installation history. A wireless system is described
    as chronically unstable — devices randomly disconnect/de-pair for
    unclear reasons, requiring manual re-pairing/re-integration into
    automations. **Concrete personal anecdote**: two identical Yandex
    Alice smart speakers, equidistant from the router in a **40m²**
    apartment, show meaningfully different signal stability, and either
    one randomly drops connectivity at unpredictable times — offered as
    evidence that even a small, simple wireless setup isn't immune, let
    alone a 30-50-device household system.

**Client-involvement framing, a distinct business-reasoning point**: a
wired system's client involvement is limited to approving planned
scenarios at the design stage and calling a specialist for any later
fix. A wireless system puts near-total ongoing involvement on the
household itself (self-programming, or paying per-visit for a
freelance specialist each time something needs re-pairing) — **stated
as the specific reason large smart-home installation companies
generally avoid offering wireless-system installation as a service at
all**: the failure/de-pairing rate makes it an unattractive service
line for a company staking its reputation on reliability.

## Assumptions / Uncertainties

- Region: channel's stated general market (Moscow/Moscow region); the
  Z-Wave US-vs-Europe/Russia compatibility caution and the Zigbee
  wall-penetration caution both read as general technical claims, not
  Russia-specific regulatory facts.
- All comparison-table figures are `single-account`, `unverified` — this
  source's own company sells both wired-system installation and
  turnkey renovation services, so the wired-system framing (reliability,
  full-service value) carries a structural interest, flagged per this
  project's standing promotional-content caution, though the specific
  mechanisms described (mesh relay behavior, protocol wall-penetration
  differences, controller circuit limits) are concrete and checkable,
  not vague marketing claims.
- Not cross-checked against non-Russian/international smart-home
  sources — this store currently has one other smart-home source
  (Kodolov, also Russian-market) for comparison.

## Target Page(s)

- **`12_Engineering_and_Systems/analysis/Smart_Home_Systems.md`** — new
  major section: wired-vs-wireless decision framework, protocol
  taxonomy, and the 12-criteria comparison table.

## Relevance to This Project's Topic (Cluster Verdict)

**Smart-home pair, member 1/2.** Confirms the dispatch note's "genuinely
fresh ground" prediction — 18 new facts, by far the highest yield of
any video in this round, and a substantial architectural deepening of
this store's previously thin smart-home coverage. The companion video
(`Y3Xpww54LpU`) should be checked directly against this note for overlap
before extraction, since both are dedicated smart-home explainers from
the same channel likely covering some of the same ground (hub concept,
protocol names).
