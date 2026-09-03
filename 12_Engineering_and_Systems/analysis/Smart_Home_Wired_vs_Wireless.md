# Smart Home — Wired vs. Wireless Architecture

The full architecture comparison between wired and wireless smart-home systems. **Split out on 2026-09-02 under the vault's 300-line page ceiling, verbatim.**

> [!IMPORTANT]
> **This is a rough-stage decision.** Wired architecture has to be committed to before the walls close, which is why it sits apart from the device-level choices that can be made later.

## Wired vs. Wireless — a Full Architecture Comparison (Kruglov/Ontario, Round 15, added 2026-08-28)

This channel's first dedicated smart-home explainer — a structured,
~18-minute comparison substantially deeper than this page's existing
Kodolov content on the specific wired-vs-wireless question. `single-
account`, `unverified`, upload 2025-10-17. [source: [[_Sources/YT_cHdQtVoFeuo_kruglov_smart_home_wired_vs_wireless|YT_cHdQtVoFeuo]]]

**Decision triggers — when only one option is actually viable**:

- **Wireless-only**: renovation already finished/at finish-stage (no
  cable pulling possible); whole-project budget under **~1,000,000
  RUB**; household enjoys tinkering with settings/re-pairing/automation
  themselves.
- **Wired-only**: apartment **100m²+**, plot **10+ соток**, or house
  **200m²+**; needs to integrate boilers, hydronic heated-floor
  thermostatic heads, or supply/exhaust ventilation (physically can't
  connect wirelessly); household wants full turnkey handling with no
  interest in the underlying mechanism.

**Wired architecture**: all controllers/modules live in one dedicated
smart-home cabinet, cables radiate out (can still incorporate some
wireless-protocol devices). **Four-stage build**: design documentation →
installation/commissioning → remote-control app setup/handover →
scenario/automation configuration.

**Wireless architecture and mesh protocols**: a **hub** (dedicated
device, smart speaker, or hub-capable Wi-Fi router) is the network's
"brain" — device signals route to the hub directly or relay through
other devices (a **mesh** network; smart outlets can double as
repeaters). **Three protocols compared**: **Zigbee** (cheapest, widest
ecosystem, poor at penetrating thick walls), **Z-Wave** (pricier, better
wall penetration, US-market devices may not work correctly in Europe/
Russia), **Thread** (future Matter-standard, modern/fast/efficient, far
fewer supporting devices currently).

**12-criteria wired vs. wireless comparison**:

1. **Design requirement**: wired needs professional documentation 100%
   of the time; wireless generally doesn't.
2. **Installation cost**: wired from **≈200,000 RUB (≈$2,500)**, scaling
   with area/device count; wireless **≈0 RUB** self-install, or **from
   ≈20,000 RUB (≈$250)** for a hired specialist (e.g. a smart relay in a
   back-box).
3. **Commissioning cost**: wired ≈**200,000 RUB** by the same
   installation company; wireless is typically self-done or by an
   independent freelancer — **large smart-home companies typically
   don't offer wireless installation as a service at all**.
4. **Device cost**: a single wired controller costs more but drives
   **~6 lighting circuits** vs. a wireless controller's **~1-2** — like-
   for-like functional cost is roughly comparable; wired-only complex
   devices (boiler/heated-floor/ventilation control) carry a real
   premium for genuinely added scope.
5. **Device-type range**: both do lighting/sockets/leak-protection; only
   wired reaches boilers/hydronic floor heating/ventilation control.
6. **Aesthetics**: wireless devices are more miniature/stylish and blend
   into any interior; many wired devices are visually bulkier and harder
   to integrate (expected to improve as demand grows).
7. **Power-outage autonomy**: both fail completely with no grid power;
   with a UPS, only priority circuits (alarm/security/leak-protection)
   stay up either way — wireless devices on batteries are inherently
   power-loss-immune, but powered wireless devices (AC, kettle, outlet)
   still need power regardless.
8. **Internet-outage behavior**: wired cable-connected devices (alarm,
   leak protection, cable-based scenarios) keep working with no
   internet; wireless **voice control specifically stops working**,
   though battery-powered wireless gas/smoke detectors still alert.
9. **Interference/jamming resistance**: wired can't be jammed and is
   unaffected by room/house size or wall thickness; wireless mesh is
   jammable and protocol-limited — **Zigbee specifically struggles in
   monolithic-partition buildings or houses over ~150-300m²**.
10. **Control-method flexibility**: wired supports any method
    simultaneously, including a **permanently wall-mounted static
    panel**; wireless substitutes tablet/smartphone/physical switch/
    voice instead of a fixed panel.
11. **Scalability**: wireless scales near-infinitely post-install (cited
    up to **1,000 devices**); wired scalability is **near zero after
    installation** — no new cable runs into finished walls, and each
    controller has a hard-fixed connection-point limit (6 circuits/
    controller in the worked example).
12. **Reliability**: wired sensor failures cited at roughly **once every
    several years**; wireless devices randomly disconnect/de-pair for
    unclear reasons, needing manual re-integration — **anecdote: two
    identical Yandex Alice speakers, equidistant from the router in a
    40m² apartment, show different signal stability and either can drop
    connectivity unpredictably**, offered as evidence even a small
    simple setup isn't immune.

**Client-involvement framing**: a wired system's client involvement ends
at approving scenarios at design stage; a wireless system puts
near-total ongoing involvement on the household (self-programming, or
paying per-visit for a freelance re-pairing fix) — **stated as the
specific reason large smart-home companies generally avoid offering
wireless installation as a service at all**.

---

Part of [[12_Engineering_and_Systems/analysis/Smart_Home_Systems|Smart Home Systems]].
