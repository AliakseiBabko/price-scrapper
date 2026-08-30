---
video_id: zuh3k15-STo
channel: Петришин-Строй (Sergey Petrishin / Сергей Петришин)
source_type: youtube
source_title: "Что такое мастер кнопка? Мастер-класс электрика. Мастер-выключатель."
source_url: https://www.youtube.com/watch?v=zuh3k15-STo
transcript_file: _Archive/processed_sources/20260824_petrishin_master_switch_8357e42c.txt
upload_date: 2021-01-24
fetched: 2026-08-24
fact_yield: 6
promotional_ratio: low
corroborates_existing: false
region: unresolved_level2_channel_only
---

# Source Note — Петришин-Строй, "Что такое мастер кнопка? Мастер-класс электрика."

English on-screen title ("What is a master switch? Electrician
masterclass. Master-off switch.") — **confirmed Russian spoken audio**
(`youtube-transcript-api` returned `language: ru`), consistent with this
project's standing rule that title language is not a reliable signal.
Short, single-topic explainer video, filmed with a real on-object
breaker-panel demonstration (a Maxim/foreman toggles the breakers and
confirms nothing resets). No city/street named — **region stays level 2**
(channel-level Moscow association only; the video does generically
mention "загородных домах" / country houses as a common install context,
but names no specific location). Low promotional ratio — a subscribe/like
call-out at the end, no product/company pitch. This channel already has
two existing, more general master-switch notes on
`12_Engineering_and_Systems/analysis/Switches_and_Controls.md` (a basic
mention, and a physical-differentiation rule from a different source's
remainder-pool round) — this video is a dedicated deep-dive that adds
substantially more implementation/mechanism detail than either existing
mention, not a duplicate.

## Electrical — Master Switch ("мастер кнопка" / "мастер выключатель")

1. **Named concept and priority-group taxonomy**: a "мастер кнопка"
   (master button) or "мастер выключатель" (master switch) is a single
   switch, usually near the entrance, that cuts all lighting and most
   outlets in the apartment from one place — except a defined set of
   "priority groups" that must stay powered: the refrigerator, heated
   floors ("тёплые полы"), the leak-protection system, the low-voltage/
   weak-current panel, and a server-room-style equipment closet if
   present. The switch itself looks and operates like an ordinary
   toggle (down = off, up = on), and lighting returns to whatever state
   it was in when it was switched off, not a default-on state.
2. **Four implementation methods, ranked by how this channel actually
   deploys it**: (1) a programmable logic relay (ПЛК), (2) a full
   smart-home system, (3) a contactor wired for general disconnection,
   (4) an impulse/latching relay ("импульсное реле") paired with a
   momentary push-button switch (like a doorbell button) — the channel
   states methods 3 and 4 (contactor or impulse relay) are what they
   actually use most often; the object shown in this video uses a
   contactor.
3. **Contactor vs. impulse relay tradeoff, with a stated cost premium**:
   a contactor is permanently energized whenever the circuit is live,
   so it fails/wears out faster than an impulse relay; an impulse relay
   only draws power momentarily to latch/unlatch, so it lasts longer,
   but it must be paired with a momentary push-button rather than a
   standard toggle switch, and the impulse-relay-plus-button combination
   costs **≈4,000 RUB (≈$50, trailing-6-month rate before this video's
   2021-01-24 publish date) more** than a contactor-based setup on the
   same object. Both installation types are described as simple for
   "practically any electrician" to wire correctly.
4. **Appliance-timer-reset consequence, framed as a decision the
   homeowner should make deliberately**: modern household electronics
   (the video specifically calls out TVs) commonly hold timer/clock/
   setting state in volatile memory — cutting their power via the
   master-switch group resets that state, requiring reprogramming on
   return. Explicit recommendation: **decide up front whether to
   include TVs/major appliances in the master-switch's priority
   (always-on) group** rather than the switched group, specifically to
   avoid this reset-and-reconfigure annoyance (illustrated with a joke
   about a smart oven mid-way through cooking Peking duck losing its
   program).
5. **Electrician-competency vetting heuristic**: if you ask a
   prospective electrician about a master switch/button and they can't
   give you a clear answer, treat that as a signal the electrician
   isn't fully competent in modern residential electrical practice —
   framed as a specific, checkable question a homeowner can use during
   vetting, not just general advice to "ask questions."
6. **Multi-story-house use case**: master switches are also commonly
   installed per-floor in multi-level country houses, not just as a
   single whole-apartment control — a distinct use case from the
   single-apartment framing that dominates the rest of the video.

[source: [[_Archive/processed_sources/20260824_petrishin_master_switch_8357e42c.txt|20260824_petrishin_master_switch]]]
