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
[source: [[_Sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]

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
[source: [[_Sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]

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
  **⚠️ A skeptical counterpoint, Round 15 (added 2026-08-28)**: remotely
  starting a kettle from a phone sounds convenient, but if it has no
  water in it the household still has to walk over and fill it before
  remote-start does anything useful — and modern kettles already heat
  water in roughly 30-40 seconds regardless, meaningfully narrowing the
  real-world benefit. General framing: prioritize smart-home tools that
  actually solve a problem for your specific household, not devices
  adopted just because the category exists. Konstantin Kruglov /
  Ontario, `single-account`, `unverified`. [source: [[_Sources/YT_VVxzNTshJCM_kruglov_modern_must_have_solutions|YT_VVxzNTshJCM]]]
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
[source: [[_Sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]

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
[source: [[_Sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]

## Yandex-Ecosystem Starter Kit and Named Scenarios (Kruglov/Ontario, Round 15, added 2026-08-28)

A device/scenario-level companion to the wired-vs-wireless comparison
above, from the same round: `single-account`, `unverified`, upload
2025-07-04. [source: [[_Sources/YT_Y3Xpww54LpU_kruglov_smart_home_2026_starter_kit|YT_Y3Xpww54LpU]]]

**Named hub hardware and compatible brands**: Яндекс Станция 2, Max, and
Lite (with a Zigbee module) as hub-capable speakers; confirmed
compatible device brands include **Xiaomi, Aqara, Redmond**, and
**Roximo** (cameras, with its own cloud storage). Verify Alice
integration before buying any device — the compatible list keeps
growing.

**Full device taxonomy** (extending this page's existing device-level
notes): button (single/long-press/double-press each triggering a
distinct scenario); door/window sensor; **vibration/tilt sensor**
(triggers on an object being flipped, tilted, or vibrated); leak sensor
(two-contact "washer," closes circuit on water contact); motion/light
sensor (dual-purpose); smart bulb (on/off, dimmable, or full RGB); smart
outlet; temperature/humidity sensor; security camera; gas sensor and
smoke sensor (two distinct device types); automatic curtain motors/
electro-cornices; broader climate devices (breathers, ACs, humidifiers,
dehumidifiers).

**⚠️ Leak-sensor cost/architecture recommendation**: a cheap,
Wi-Fi-independent standalone leak sensor costs only **≈500 RUB**; a
Wi-Fi-integrated leak-detection-and-shutoff system costs **5,000-7,000
RUB more**. **Recommendation: buy both** — let the Wi-Fi system handle
the actual shutoff, but add a cheap independent sensor alongside it so
the household gets a separate confirmation notification that the
shutoff actually happened. Also recommends a leak sensor behind a
loggia washing machine even where a leak wouldn't reach a neighbor —
pooling water behind the machine is a real, easily-missed problem on
its own.

**⚠️ Away-mode security scenario, with concrete timing**: a single
button press arms the system after a **~10-second delay** (motion,
door/window, leak, and valuables-vibration sensors all activate
together); on return, the household has **~15-20 seconds** to disarm
before the alarm triggers. Explicitly scoped as protection against
ordinary break-in attempts, not a jam-proof professional system (RF
jammers can defeat it; genuine jam-resistance needs dedicated
servers/professional camera infrastructure).

**Named scenarios**: background push notification on entry-door open/
close for passive child school-departure/arrival monitoring; a
gun-safe vibration sensor triggering both a push notification and a
**custom Alice text-to-speech alert** ("the safe is under guard...");
Aqara gas/smoke sensors also flagged as usable for household
hookah-smoke detection as an off-label side benefit; a smart outlet on
an iron addressing forgotten-appliance anxiety via app-check or an
automated ~15-minute run-time cutoff; night-time bathroom lighting
auto-dimming to **50% brightness**; motorized curtains opening on an
**alarm-clock event**, not just a fixed timer.

**⚠️ Heated-floor smart-relay alternative to a programmable smart
thermostat**: programmable Wi-Fi heated-floor thermostats cost
significantly more, and **some models lose their programmed schedule
after a power interruption** — a real reliability gap. Cheaper, more
robust alternative: an ordinary non-programmable thermostat left
permanently "on," wired through a simple smart relay that switches the
whole circuit on/off on a schedule (e.g. on 6am, off 9am for an 8am
usage window) — scheduled operation without paying for or trusting a
failure-prone smart thermostat.

**Recommended 10-device starter kit for a first-time adopter**: hub
(speaker preferred over a standalone hub device), door-open sensor,
motion sensor, temperature/humidity sensor, leak sensor, smart outlet,
smart bulb, control button, camera, automatic curtains — framed as a
maximal "get acquainted" set, with 3-5 suggested as a smaller starting
point. **Camera guidance**: prefer a brand with its own cloud-storage
service; camera integration into the smart-home app is currently
view-only (no cross-app automation triggers yet).

## Ecosystem Scale Figure and a Water-Vapor "Fireplace" Device (Kruglov/Ontario, Round 15, added 2026-08-28)

**⚠️ Yandex Alice ecosystem scale**: as of this source's 2025-02-28 upload, the Yandex Smart Home app lists **260 registered device-manufacturer companies** compatible with Alice — offered as evidence of the ecosystem's practical maturity for a first-time adopter, complementing this round's own Yandex-ecosystem starter-kit content above.

**Water-vapor "fireplace" humidifier — a new device category for this store**: a decorative unit producing a realistic flame-like visual effect using only water (no real combustion, distinct from a bio-fuel fireplace), can be built into furniture, and can integrate into a smart-home system — offered as a humidifier alternative with a stronger aesthetic payoff than a plain humidifier appliance. `single-account`, `unverified`. [source: [[_Sources/YT_QyF37JEFpfA_kruglov_top12_stylish_solutions|YT_QyF37JEFpfA]]]

## Apartment-Interior Motion Sensors — a Reliability Caution (Kruglov/Ontario, Round 15, added 2026-08-28)

Konstantin Kruglov / Ontario flags motion sensors as **unreliable
specifically for apartment-interior lighting** — even correctly
configured, "you'll never trust that the light will turn on when you
actually need it." He concedes motion sensors genuinely help for
street/entryway/stairwell lighting (exterior/common-area use), but
recommends standard or two-way/crossover switches for interior apartment
rooms instead. `single-account`, `unverified`. [source: [[_Sources/YT_kkE25HmFciU_kruglov_worst_solutions|YT_kkE25HmFciU]]]

## A Turnkey Designer's Reliability Caution (Игорь Краснов, added 2026-09-01, Round 4)

Distinct from the Kruglov/Ontario wired-vs-wireless architecture comparison above — this is a broader adoption caution from a design (not installation) practitioner, and genuinely new for this page's own risk framing. [source: [[_Sources/YT_NO6-2zAJgys_krasnov_19controversial_items|NO6-2zAJgys]]]

- **⚠️ Sensors misfire, companion apps freeze/lag, automations frequently don't behave as configured.** Many users report reverting to basic manual switches/thermostats over time and end up using only a few core functions (lighting on/off, climate control) out of a much larger installed feature set. **Recommends realistically assessing which specific smart-home functions will actually see daily use BEFORE investing in a full system**, rather than installing maximal automation by default. Converges with this page's own existing "prioritize tools that actually solve a problem for your specific household" framing (Kruglov's kettle counterpoint above) — same conclusion, independent channel, applied at the whole-system level rather than one device category.

`single-account`, `unverified`.

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
[source: [[_Sources/YT_om5BbhJDaOo_kodolov_smart_home_pricing|om5BbhJDaOo_kodolov_smart_home_pricing]]]

## ⚠️⚠️ A Designer's Own Flat, One Year In — Four Retrofit Patterns and a Scene That Justifies the Rest

**Unusually good evidence for this page: every item is a device actually in service in the reporter's own Petersburg flat, with the annoyance it was bought to fix and the schedule it runs on. Yandex/Алиса ecosystem, which corroborates the starter-kit section above from an independent practitioner.** [source: [[_Sources/YT_lhikl-7c43c_nsdsgn_own_flat_year_one_fixes|YT_lhikl-7c43c]]]

### ⚠️⚠️ The retrofit pattern worth generalising — leave the fixture ON and put the intelligence upstream

**A 20-year-old vintage floor lamp with a foot switch he found genuinely irritating: «он выключается НОГОЙ, там кнопочка такая — каждый раз подходить, уходить, выключать, забыл, подошёл».**

- **⚠️ THE FIX: «я ЗАЖАЛ ВКЛЮЧЕНИЕ и купил УМНУЮ КНОПКУ»** — a smart button at «тысяч там полторы, может две» (**~1,500-2,000 ₽, 2024**). The lamp's own switch is permanently held on; the button upstream does the switching.
- **Scheduled rather than voice-triggered: «каждый раз, когда я прихожу с работы, ЗА ПОЛЧАСА до моего прихода уже включена лампа, ОНА МЕНЯ ВСТРЕЧАЕТ; и ночью она выключается либо по моей команде, либо сама».** «Дом тебя как будто бы ОБНИМАЕТ и встречает.»
- **→ THE PATTERN: any dumb fixture with an awkward switch can be automated without rewiring and without replacing the fitting. It is the only route available for vintage, second-hand or designer fittings that will never have smart internals — and it sidesteps the reliability concerns recorded above, because the fitting itself is unmodified and the failure mode is simply "the lamp stays on".** Compare the wired-versus-wireless decision on [[12_Engineering_and_Systems/analysis/Smart_Home_Wired_vs_Wireless|Smart Home: Wired vs Wireless]] — this is the cheapest possible wireless retrofit and it requires no rough-stage decision at all.

### Motorised curtains — the drive was swapped, and the percentage function is the favourite

- **He changed the existing electric curtain DRIVE so that it works with Алиса** — so an already-motorised curtain became controllable, rather than a new curtain being bought. **«Наверное САМОЕ КРУТОЕ РЕШЕНИЕ» of everything he did.**
- **Morning by voice, evening on a schedule. ⚠️ And one schedule detail that is a genuine use case rather than a novelty: «они также уже В 11:00 ВСЕГДА ОТКРЫТЫ, чтобы я НЕ ПРОСПАЛ, не дай Бог.»**
- **⚠️ PARTIAL CLOSING, which he singles out: «мне очень нравится функция, когда можно сказать "Алиса, ЗАКРОЙ ШТОРЫ НА 50%", и она закроет шторы не полностью, а только наполовину.»** **→ A percentage-addressable drive is a different product from an open/close one, and it is the difference between a novelty and a daily control.** See [[17_Design_and_Ergonomics/analysis/Curtains_and_Window_Treatments|Curtains and Window Treatments]].
- **⚠️ The composed effect he rates highest is a two-device interaction, not a single function: «когда они вечером ЗАКРЫВАЮТСЯ, у меня СРАЗУ ЖЕ ЗАГОРАЕТСЯ СВЕТИЛЬНИК — то есть шторы закрыты, а в комнате СВЕТЛО.»** «Создаёт прямо нереальный УЮТ… я живу с этим несколько месяцев, но меня КАЖДЫЙ РАЗ этот момент радует.»

### ⚠️⚠️ The "goodnight" scene — and it is what makes a large device count tolerable

- **The problem, stated plainly and it is the one this page's device sections tend to create:** a controlled socket with a night-light in the study, a kitchen floor lamp, wall night-lights, a bedside lamp and motorised curtains. **«Чтобы всё это закрыть, нужно КАК ДУРАК ХОДИТЬ ПО ВСЕЙ КВАРТИРЕ, говорить: Алиса, закрой это; Алиса, выключи это.»**
- **⚠️ «Прописал СЦЕНАРИЙ — когда ты говоришь просто "Алиса, СПОКОЙНОЙ НОЧИ", у тебя выключается ВЕСЬ СВЕТ, который тебе нужно, и ЗАКРЫВАЮТСЯ ШТОРЫ… ОНО ОЧЕНЬ ПРОСТО ДЕЛАЕТСЯ, и я всем его рекомендую.»**
- **→ This is the load-bearing item, not a nice extra: the same practitioner argued four years earlier that light groups should be capped at two or three because hunting for the right switch becomes intolerable. The scene is what removes that ceiling.** Full reconciliation on [[12_Engineering_and_Systems/analysis/Switches_and_Controls|Switches and Controls]].
- **⚠️ And his flat rejection of the alternative input method, which is a dissent from common practice: «я НЕНАВИЖУ ДАТЧИКИ ДВИЖЕНИЯ — вот это всё МАХАНИЕ РУКАМИ, чтобы они включились».** Independent of, and compatible with, the motion-sensor reliability caution recorded above — his objection is to the interaction, not the reliability.

### Scheduled appliances — and the schedules encode a noise decision

| Device | Schedule | The reasoning |
| :--- | :--- | :--- |
| **Air purifier** | On when he leaves for work, off toward evening | **«Весь день она работает, но при этом мне ШУМ НЕ МЕШАЕТ, когда меня нет дома.»** Filter life ~**1 year** |
| **Humidifier** (on a smart plug) | Running in the day, **off at night** | **«Ночью я хочу спать в ТИШИНЕ.»** Power level also settable from the phone |
| **Гирлянда** | Evenings only | **«Я всем конечно рекомендую гирлянды включать именно НА РАСПИСАНИЕ — зачем вам гирлянда днём?»** |
| **Robot vacuum** | 3× a week at a set hour | Scope stated honestly: **«он НЕ ЗАМЕНЯЕТ вам обычную влажную уборку [и] пылесос — но если вы сделали клининг, то, часто запуская его, вы будете ПОДДЕРЖИВАТЬ довольно хороший порядок»** |

**⚠️ The pattern across all four: the schedule exists to move the device's NOISE into hours when nobody is home. That is a scheduling criterion this page did not have — the starter-kit section above schedules for convenience and energy, and this schedules for acoustics.** It also matters because two of these live in rooms where the noise would otherwise force them off entirely: the purifier moved out of the bedroom for exactly this reason, and the humidifier is silenced at night.

**⚠️ A humidity figure worth keeping, since it is the reason the humidifier exists at all: with the radiators running in a Petersburg winter, «это УЖАСНЫЙ СУХОЙ ВОЗДУХ, у меня начинают ЛОПАТЬСЯ СОСУДЫ… там по 10% ВЛАЖНОСТИ показывает». In summer he does not use it — «воздух в Питере и так довольно влажный».** So the device is heating-season-only, which bears on whether it is worth integrating at all. See the humidification note on [[12_Engineering_and_Systems/analysis/Breathers_vs_Mechanical_Ventilation|Breathers vs Mechanical Ventilation]].

## Wired vs. wireless architecture — moved to its own page

See **[[12_Engineering_and_Systems/analysis/Smart_Home_Wired_vs_Wireless|Smart Home — Wired vs. Wireless Architecture]]**. **That decision has to be made at the rough stage**, before the walls close; this page keeps pricing, control methods, devices, sensors and the ecosystem starter kit, which can be revisited later.
