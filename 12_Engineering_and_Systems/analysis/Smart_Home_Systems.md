# Smart Home Systems

Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]]. Created 2026-08-25 — this project's own 3+-sources-no-page threshold rule was crossed once a real dedicated smart-home explainer video arrived; prior scattered mentions lived across `Switches_and_Controls.md`, `Lighting_Design.md`, `Fresh_Air_Ventilation_and_Ducting.md`, `Rough_Plumbing_Sequencing.md`, and the AC pages — cross-check those pages for smart-control mentions specific to their own system before assuming this page is the only home for the topic.

## Pricing and Cost Structure (Sergey Kodolov)

- **Three real pricing tiers**: a low-commitment "taste test" starter kit
  (one smart bulb + a small hub/server) from **≈10,000 RUB**, individual
  smart bulbs ≈600-1,400 RUB each — explicitly recommended as a way to
  test whether you'll actually use a smart home before investing further.
  A genuinely multi-functional whole-apartment system starts around
  **≈500,000 RUB**, scaling upward with no fixed ceiling.
- **Cost-delta relative to classic (non-smart) electrical wiring of the
  same project**: **+3%** just from smart-ready wiring/topology alone
  (can even save slightly on cable in some layouts) vs. **+20-35% total**
  once the full smart-device/controller/programming layer is added,
  varying by object and by which functions the client selects.
- **⚠️ Must be planned from the start of the electrical design project,
  not retrofitted after rough-in** — a smart system needs its own
  commissioning/setup phase running in parallel with the whole
  renovation timeline (commissioning finishes around the same time as
  final furniture placement), unlike ordinary lighting which just works
  once wired.
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]

## System Architecture and Control Methods

- **Three core components**: a **controller** (routes information,
  issues commands, aggregates sensor data), **sensors** (leak/motion/
  gas/CO2 detectors etc.), and **actuators** (relays/devices that execute
  the commanded action). Worked example: a motion sensor signal reaches
  the controller over twisted-pair wiring, the controller matches it
  against a stored scenario, then signals a relay to turn on the light.
- **Wired vs. Wi-Fi control backbone**: wired is fast and reliable;
  Wi-Fi is easier to install but less stable — an outage means repeatedly
  re-issuing voice commands that don't register.
- **Four control methods, ranked by the source's own preference**:
  physical push-button switches (a "hatted"/pressable design, not a
  toggle), a phone app, and — the stated favorite — a voice assistant
  (Alice/Siri). **Scenario-based control (one command triggers a whole
  lighting/scene setup) is called the single most valuable feature**,
  over hitting many individual switches.
- **⚠️ Cross-brand compatibility caution**: check which communication
  protocol devices actually share, not just brand names — mixing many
  brands (Yandex, Xiaomi, Google, Redmond, etc.) into one system is
  genuinely difficult to get working reliably. **Recommendation: hire a
  specialized integration company rather than self-assemble** — most
  negative "smart homes are annoying" sentiment is attributed to
  well-intentioned DIY assembly done without protocol-compatibility
  knowledge, not to the technology itself. (Tier-steering flag: this is
  also the source's own paid service — the protocol-compatibility
  reasoning behind it is genuine regardless.)
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]

## Device-Level Notes

- **Smart lock**: unlocks by phone, fingerprint, code, or card. **Runs on
  battery, not mains** — a low-battery warning beeps well before
  failure; an externally-accessible 9V "crown" battery terminal allows
  emergency external power if the internal battery fully dies. Losing a
  physical key (a recurring problem especially with children) motivates
  the non-key unlock options.
- **Motion sensors**: garage auto-lighting (on when entering, off once
  the car leaves); a genuinely concrete bathroom use case (a cat that
  wouldn't use its litter box without light, solved via motion-triggered
  light instead of leaving one on permanently).
- **Smart kettle/coffee maker**: some models hold a specific *target
  temperature* below full boil (e.g. for white/green tea — full-boil
  water scorches delicate leaves and destroys aroma) — a genuine
  functional benefit distinct from pure convenience. Some refuse to heat
  with no water present (child-safety benefit).
- **⚠️ Motorized curtains/blinds — a real physical threshold, not just a
  convenience upgrade**: above roughly **3-3.5m ceiling height**, manual
  pull-cords/rods stop being practical even with pull-rod attachments —
  motorization becomes the only workable option. Heavy curtains are also
  prone to mechanical damage at the fastening points from repeated
  manual pulling, independent of ceiling height.
- **LED strip color**: real installed-base data point — the strong
  majority of clients choose a simple warm-white dimmable strip over
  full RGB; RGB is mainly useful for deliberate accent/attention effects
  (the source's own example: exhibition-booth lighting), not a typical
  residential choice.
- **CO2 sensors**: marketed for air-quality/ventilation triggering
  (elevated CO2 correlates with impaired cognitive function in a
  crowded room) — flagged with a real cautionary anecdote that
  continuous environmental sensing can surface information well beyond
  its intended HVAC-automation purpose (a client's app flagged an
  unexpected bedroom CO2 spike while he was away). Not a technical rule,
  just a privacy-adjacent awareness point.
- **Smart plugs**: make an otherwise "dumb" lamp app/voice-controllable
  by controlling power to it. Real commercial case: a tenant's radiant
  floor heating kept being left on by staff after hours — fixed with a
  temperature-threshold automation (auto-off at a set floor temperature,
  e.g. ~23°C) rather than relying on staff compliance.
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]

## Safety-Critical Sensors — "Basic Safety, Not Optional"

- **Leak sensors + automatic shutoff valve**: closes the water supply
  automatically on contact with water — faster than a person could
  physically get home after being called. First-hand motivation: the
  source personally experienced two real pipe-burst floods (one his own
  fault, one not) before leak sensors were standard practice at his
  company.
- **Gas sensors + automatic shutoff**: standard recommendation
  specifically for elderly-occupant households (forgotten unlit gas
  burners named as the risk case).
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]

## House/Villa-Specific Additions (⚠️ Not This Project's Apartment Scope)

Flagged as outside this project's own apartment-renovation context —
recorded as general reference only:

- Exterior motion-triggered lighting; heated storm drains/steps/
  walkways (ice-safety, always heat-trace storm drains to prevent
  freeze-driven pipe bursts); perimeter security/alarm systems; backup/
  uninterruptible power for whole-house outages (common in Russian
  private-house areas per this source) with automatic SMS alert on power
  loss; automatic gate control, including a fire-truck-access use case
  (gates can auto-open on a fire-alarm trigger with no one home); roof
  anti-icing/heat-trace systems (framed as effectively unmanageable
  manually, real falling ice/snow-load safety concern).
- **⚠️ Explicit warning against DIY roof heat-tracing**: a real Moscow
  residential fire (~400m² roof) was attributed to an improperly
  self-installed roof heating system — used as the reasoning for
  "trust professionals for this specific system."
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]
