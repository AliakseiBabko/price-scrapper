# Electrical — Switches & Controls

Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]].

**Install a master cut-off switch near the main entrance** — a single button that shuts down all (or most) apartment lighting on the way out, rather than checking room by room. In its fuller version, it also controls the duty/night-light circuit below, giving one action that covers every light in the apartment. [source: [[_Sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Use two-way ("проходной") switches for a room's main light where it makes sense** — most valuably bedside, so a light can be switched off without getting back up: cheap to install, disproportionately high perceived comfort value. **Extend the same logic across a whole chain of adjoining passage rooms** (e.g. entry → corridor → living room) — every room in the chain shares one switch group controlling the same circuit, switchable from any point, so nobody has to backtrack to turn off a light in a room they've already left. [source: [[_Sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**A dedicated "duty"/night-light circuit is worth building in**: a separate, always-on low-level light — distinct from the main light — in hallways, entries, and bathrooms, letting someone navigate at night without triggering bright main lighting. Controlled from at least the entry door and typically from multiple points. Belongs in hallways/WCs, never bedrooms — see [[12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning|Key Concepts & Planning]] for the full lighting-category taxonomy this fits into. [source: [[_Sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Install dimmers as a low-cost upgrade** on primary living/bedroom lighting circuits. **Finalize the actual bulbs being used before buying a dimmer** — dimmer compatibility depends on matching leading-edge vs. trailing-edge dimming to the bulb/driver type, and buying the wrong pairing is a common, avoidable mistake. [source: [[_Sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Minimize switch/gang count per location** — two gangs for a living room's main controls is commonly enough; six is usually over-specification that adds cost and visual clutter without functional benefit. Prefer several single-gang switches over one crowded multi-gang plate where space allows, and keep every standard toggle switch in the apartment on the **same ON/OFF orientation** — a mixed-orientation install is a common, avoidable annoyance. Never position a switch inside a future door's swing zone, checked against the door leaf's full opening arc, not just its closed position. [source: [[_Sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Two-way switches work in pairs; a run with three or more control points adds "intermediate" (crossover) switches between the two end switches**, not more two-way switches — a distinct component. Wire joints must terminate in a proper junction box; twisted-and-taped joints left exposed outside a junction box are a common, unsafe jobsite shortcut. [source: [[_Sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Konstantin Kruglov / Ontario gives the precise general formula for the two-way/crossover pattern above**: keep exactly 2 two-way switches at the two logical "end" locations regardless of how many control points exist, and add one crossover/intermediate switch per additional point beyond those two — 3 points = 2 two-way + 1 crossover; 4 points = 2 two-way + 2 crossover; 10 points = 2 two-way + 8 crossover. Buying two ordinary standard switches and asking an electrician to wire them as two-way does not work — the devices must be two-way switches by construction from the start. [source: [[_Sources/YT_1dp7alivsLQ_kruglov_safe_sockets_switches|1dp7alivsLQ_kruglov_safe_sockets_switches]]]

**⚠️ Never tie an exhaust-fan/ventilation circuit to the main light switch (Round 13 triage, added 2026-08-28)**: wiring a bathroom's extractor fan to switch on automatically with the main light is a common but avoidable mistake — always give ventilation its own dedicated switch. Konstantin Kruglov / Ontario, `single-account`, `unverified`. [source: [[_Sources/YT_0TLDGD8MY1A_kruglov_top_renovation_mistakes_2026|YT_0TLDGD8MY1A]]]

**Konstantin Kruglov / Ontario: two devices worth avoiding, with reasoning** — (1) triple-gang switches: each gang is only ~2cm wide (about one fingertip), making it hard to hit the right gang reliably, especially at night; (2) wiring 3+ crossover control points onto one multi-gang switch instead of using separate crossover switches — the cable run required is disproportionate to the benefit. **Avoid a two-way ("проходной") dimmer specifically**: switch/socket lines are normally bought matched from one manufacturer/collection, and a two-way-capable dimmer often only exists in a different product line, forcing a visible frame/finish mismatch across the installation. [source: [[_Sources/YT_1dp7alivsLQ_kruglov_safe_sockets_switches|1dp7alivsLQ_kruglov_safe_sockets_switches]]]

**Buy sockets, switches, and cover-frames from one manufacturer and, ideally, one product line/collection, sourced together** — a real documented client case: a client bought round-bodied socket/switch mechanisms with square-shaped cover frames from mismatched sources for a 45-point order (30 sockets, 15 switches); caught and returned before installation, but framed as a routine, easy-to-make mistake worth an explicit warning rather than assuming it's obvious. [source: [[_Sources/YT_1dp7alivsLQ_kruglov_safe_sockets_switches|1dp7alivsLQ_kruglov_safe_sockets_switches]]]

**Socket mounting-type taxonomy**: surface-mounted (no back-box needed), flush/recessed (back-box + routed cable), pop-out/retractable (spring- or button-actuated, e.g. a kitchen-island pop-up socket), and panel-mounted (clipped to the DIN rail like a breaker — specialized, not detailed further). **Grounding is a hard requirement** — every power socket should be grounded; avoid ungrounded sockets entirely. **Water-protection sockets are visually distinguished only by a hinged cover** — cover present = water-protected (bathrooms, loggia/outdoor); no cover = not. **Child-safety shutter-curtain sockets exist but a correctly-specified breaker/RCD combination plus supervision is the real protection** — even on accidental contact, correctly-specified protective devices should trip before serious harm. Other named sub-types: smart (hub/network-controlled) sockets, lockable-cover (key-actuated) sockets, sockets with an integrated voltage-monitoring relay (very sensitive appliances only, rarely used in apartments), and a decorative illuminated "socket-nightlight" hybrid (explicitly dismissed as a novelty, not a real recommendation). [source: [[_Sources/YT_1dp7alivsLQ_kruglov_safe_sockets_switches|1dp7alivsLQ_kruglov_safe_sockets_switches]]]

**A bathroom/WC exhaust fan's switch belongs inside the room it serves, not in the adjoining hallway.** Automating a fan is fine for auto-OFF (a timer that shuts it off after a delay) but not for auto-ON (an occupancy/humidity sensor that starts it without warning) — auto-ON is startling for the occupant. [source: [[_Sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Prefer spring-clamp (screwless, self-clamping) terminals over screw terminals on finish-stage outlets/switches** — screw terminals are more prone to loosening from thermal cycling over time. Evaluate a device by country of manufacture and terminal type rather than by brand name alone. Avoid switches with an integrated LED backlight/indicator — a reported flicker/glow issue with some LED bulb types. [source: [[_Sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Kitchen counter outlet rule**: every open/free counter zone gets its own outlet; the main cooking zone additionally needs its own task-lighting switch. **Avoid touch/capacitive-sensor controls for standard-tier under-cabinet lighting** — reported as unreliable (doesn't consistently respond to a hand-wave despite marketing claims) and less convenient with wet/dirty hands, which can still press a physical switch but may be reluctant to touch a sensor pad; may be more appropriate for premium-segment kitchens. [source: [[_Sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Highly granular per-zone lighting circuits are easy to over-specify at design time and commonly go unused in practice — plan for roughly 2 real circuits per room (day/night) as the default, not more, absent a specific documented need.** A real Category 5 case: an as-wired apartment had several independent lighting zones per room (a genuine over-spec), and the owners' own retrospective admission was that the granular zoning went almost entirely unused once installed — smart-switch reprogramming was needed afterward just to consolidate the circuits onto fewer physical controls. `single-account`, `unverified`. [source: [[_Sources/YT_iEpRx5Pe7to_designer_disaster_20m_277|YT_iEpRx5Pe7to]]]

**⚠️ Smart-switch relay click noise near a bedroom is a real, checkable nuisance worth verifying before installation, not a hypothetical concern.** Some smart-switch relay types click audibly on activation — disruptive specifically in a quiet nighttime bedroom setting. `single-account`, `unverified`. [source: [[_Sources/YT_iEpRx5Pe7to_designer_disaster_20m_277|YT_iEpRx5Pe7to]]]

**Pre-wire an outlet cluster wherever a future device (e.g. a security camera) is anticipated, even if it isn't being installed yet** — avoids visible surface cabling being added later. A documented case: a pre-installed outlet cluster near a kids'-room ceiling corner meant a camera added afterward required no additional visible wiring. `single-account`, `unverified`. [source: [[_Sources/YT_iEpRx5Pe7to_designer_disaster_20m_277|YT_iEpRx5Pe7to]]]

**A large open-plan space needs a light switch reachable near every exit path, not just at the main entry** — reiterated across two independent Category 5 defect cases, both requiring a "walk blind" across a dark room to reach the only switch. `single-account` each, `unverified`. [sources: [[_Sources/YT_cWRgenv4B40_full_disaster_30m_274|YT_cWRgenv4B40]], and this vault's existing entry/corridor-chain guidance above]

**Keep safety/reliability-critical controls (a room's main light switch, a WC/bathroom's light control) on physical, non-networked hardware — reserve voice/app/smart-home control for genuinely optional comfort features only.** A real household's stated reasoning: if a basic function (turning on a light to see) depends on an internet connection or a voice-assistant service, an outage means you can't perform an ordinary daily task. A specific real anecdote: a voice-controlled kitchen backsplash light was used "effectively twice — once when it was installed, once when we found someone dumb enough to buy it from us," offered as evidence the novelty didn't survive contact with daily use. Pairs with this vault's existing wired-vs-wireless smart-home reliability finding (`6syO3dTButw`, Category 5 chunk 3). `single-account`, `unverified`. [source: [[_Sources/YT_zPR8PGWq5lA_3yr_diy_deviations_case_229|YT_zPR8PGWq5lA]]]

**A voltage relay (реле напряжения) is recommended as a standard electrical-panel component, even in a budget build-out** — protects connected equipment from grid voltage spikes/surges. `single-account`, `unverified`. [source: [[_Sources/YT_ajtv-urp18I_old_building_crossover_tips_101|YT_ajtv-urp18I]]]

**An exposed electrical panel should be sized to the apartment's actual circuit count, not oversized as a decorative feature** — a documented defect used a panel far larger than any legitimate circuit count for the unit, functioning as an unconcealed wall feature rather than real capacity; the general rule (see the false-wall/panel-concealment guidance elsewhere in this vault) is to plan real circuit count first, then conceal a correctly-sized panel behind a false wall. `single-account`, `unverified`. [source: [[_Sources/YT_ROv1BuBfECU_designer_disaster_35m_281|YT_ROv1BuBfECU]]]

**Cluster a multi-circuit switch group near the seating/sofa position in a combined kitchen-living room**, controlling separate lighting circuits (e.g. kitchen zone + loggia zone) from one location rather than scattering single switches at each zone's own entry. Pairs with the balcony-door-slope socket guidance below. **A balcony/loggia door slope (откос) should carry at least two sockets** — practical loggia-zone device/lighting need, not just a design flourish. `single-account`, `unverified`. [source: [[_Sources/YT_WmkOC9uKnCQ_kitchen_living_loggia_layout_lifehack_154|YT_WmkOC9uKnCQ]]]

## Switch Side-Placement, Back-Box Alignment, and Rough-Stage Sequencing (added 2026-08-25, Sergey Kodolov)

Sergey Kodolov (turnkey company owner, multi-city Russia + Dubai) adds
detail this vault's existing 90cm-height / 15cm-from-opening-edge switch
rule didn't yet specify:

- **Which side of the door opening a switch goes on**: the same side the
  door opens toward (the handle side) — so it can be found and pressed
  without looking, rather than fumbling on the hinge side.
- **⚠️ Rough-stage back-box (подрозетник) alignment is the real leverage
  point for a clean finish install** — back-boxes must be level-set and
  installed exactly in line during the rough electrical stage; a finish
  electrician then simply clips frames on with no correction needed.
  Sequencing implication: put your most experienced electrician on the
  **rough** stage, not the finish stage — a bad rough alignment can't be
  fixed later by even a skilled finisher snapping on plates.
- **Back-box selection criteria and a real price range**: 15–250 RUB per
  unit; pricier back-boxes install more precisely and hold cable/
  connections more securely. Choose based on wall material/thickness,
  available recess depth, humidity, whether grounding contacts are
  needed, and whether frequent access is needed (a covered/lidded
  back-box variant exists for that case, though rarely actually needed in
  practice).
- **"No junction boxes, one breaker per outlet" flagged as a cost-inflating
  Moscow ultra-premium trend, not a real technical upgrade** — wiring one
  dedicated breaker straight to one single outlet (skipping the standard
  branching junction-box topology) carries no functional benefit per this
  source; watch for it as tier-steering rather than genuine improvement.
- **"When debating a socket count, round up" heuristic**: if unsure
  between e.g. 2 vs. 3 outlets at a location, install 4 instead — framed
  as near-universal experience that occupants end up wanting more outlets
  than originally planned.
- **General living-room socket spacing rule of thumb: roughly every
  2-3m along the walls**, distinct from a room's fixed-point sockets
  (TV, appliances, etc.).
- **Group audio/video/computer-equipment outlets at one location** to
  avoid needing extension cords/power strips later.
- **Reflected wall-elevation drawings (развертки) have a concrete,
  checkable long-term purpose**: with a documented socket/switch layout,
  the wire path from any outlet runs straight up or down at exactly 90° —
  so years later, a homeowner can predict "there's a wire directly above
  this outlet" and avoid drilling into it when hanging a picture or shelf.
[source: [[_Sources/YT_QfTqabNW1Lc_kodolov_electrical_rough_install|QfTqabNW1Lc_kodolov_electrical_rough_install]]]

## Electrical-Panel Niche Sizing Formula (added 2026-08-19, remainder-pool Round 2)

**⚠️ Electrical-panel recess: minimum 110mm panel installation depth → build the niche to at least 140mm deep.** If the host wall isn't thick enough to net a structurally sound remainder after recessing, thicken it first — worked example: a 200mm neighbor-shared wall thickened to 250mm specifically to make a 140mm-deep niche viable. **Full coordinate sequence, worked example**: from the floor screed, offset 1200mm up for the niche's bottom edge, then a further 500mm for the niche's height (spanning roughly 1200-1700mm above the floor); horizontally, offset 100mm from the neighbor-shared wall, then 400mm for the niche's width. `single-account`, `unverified`. [source: [[_Sources/YT_C4lUAfJyyb0_developer_stolen_meters_170|YT_C4lUAfJyyb0]]]

## Precise Switch-Reachability Formula & Window-Reveal Outlet Clearance (added 2026-08-19, remainder-pool Round 2)

**⚠️ Position a switch 90cm from the floor, 15cm from the opening's edge** — demonstrated as the exact figures needed to reliably find and press a switch without looking. **Window-reveal outlet clearance: 10-15cm from the windowsill's own plane**, not flush against it. **Master-switch differentiation, a third independent corroborating instance**: a master switch identical in height/appearance to the regular switch group is a real usability failure. `single-account`, `unverified`. [source: [[_Sources/YT_eezwcNG-1qI_designer_project_walkthrough_269|YT_eezwcNG-1qI]]]

## Master-Switch Differentiation & Baseboard-Electrical Caution (added 2026-08-19, remainder-pool Round 2)

**⚠️ A "master" switch that cuts power/lighting to the whole unit must be physically set apart from the regular switch group** — a different height/position, and visually distinct in appearance — specifically to prevent it being pressed by accident. **⚠️ Avoid routing outlets, TV coax, or network/twisted-pair cabling through a baseboard channel system as the primary distribution method** — this creates a furniture-placement conflict, since there's no way to know in advance exactly where a TV or other furniture piece should sit if its power/data connections are scattered along a low baseboard run rather than fixed at the wall location the furniture will actually occupy. Plan electrical/data points at their intended furniture-height locations instead. **A real documented extreme failure case**: 5 switches at one bedroom's entry plus 6 more elsewhere (11 total across two adjoining rooms), none clearly labeled by function — a striking real-world instance of violating the single-switch-per-room-exit principle already established in this vault. `single-account`, `unverified`. [source: [[_Sources/YT_MWDcYHqe-iQ_designer_apartment_walkthrough_288|YT_MWDcYHqe-iQ]]]

## Master-Switch Deep Dive: Priority Groups, Implementation Methods, Cost (added 2026-08-24, Petrishin-Stroi Round 9)

Sergey Petrishin gives a dedicated master-switch ("мастер кнопка"/"мастер
выключатель") explainer that extends the brief mentions already on this
page (line 5 above, and the physical-differentiation rule below):

- **Priority-group taxonomy**: the refrigerator, heated floors, the
  leak-protection system, the low-voltage/weak-current panel, and any
  server-room-style equipment closet should stay on a priority group
  that the master switch never cuts. Everything else (general lighting
  and most outlets) is switchable from one location, returning to its
  prior on/off state rather than defaulting on.
- **Four implementation methods**: a programmable logic relay, a full
  smart-home system, a contactor wired for general disconnection, or an
  impulse/latching relay paired with a momentary push-button. Petrishin
  most often uses the last two. **A contactor stays permanently
  energized and wears out faster; an impulse relay only draws power
  momentarily to latch/unlatch and lasts longer, but needs a momentary
  push-button rather than a standard toggle** — the more durable
  impulse-relay option costs **≈4,000 RUB (≈$50) more** than a
  contactor-based setup on the same object (2021 pricing).
- **Decide up front whether TVs/major appliances go in the priority
  group or the switched group** — modern electronics commonly lose
  timer/clock/program state in volatile memory when cut, needing
  reprogramming afterward; this is a deliberate tradeoff to make, not
  an oversight to avoid outright.
- **⚠️ Second-household-member usability caveat, Round 15 (added 2026-08-28)**: because the master switch fully cuts the apartment's general lighting circuit, a household member who stays home/sleeps in after another member leaves for work (switching off the master light on the way out) loses light access entirely until they themselves walk to the entry door and reactivate it — a real, easily-overlooked tradeoff in a multi-person household with staggered schedules. Konstantin Kruglov / Ontario, `single-account`, `unverified`. [source: [[_Sources/YT_VVxzNTshJCM_kruglov_modern_must_have_solutions|YT_VVxzNTshJCM]]]
- **Vetting heuristic**: if a prospective electrician can't give a
  clear answer about master switches, treat that as a sign they aren't
  fully current on residential electrical practice.
- Also used per-floor in multi-story country houses, not just
  single-apartment installs.

[source: [[_Sources/YT_zuh3k15-STo_petrishin_master_switch|zuh3k15-STo_petrishin_master_switch]]]

**⚠️ Router and security-camera system named explicitly in a fourth independent source's exclusion list (Round 14 triage, added 2026-08-28)**: Konstantin Kruglov / Ontario restates the same master-switch inconvenience case and "vacation mode" scoped-switch alternative already covered above, but names the **Wi-Fi router and a security/surveillance camera system** directly as always-excluded devices, alongside the refrigerator and leak-protection system already on this page's priority-group list. The existing "weak-current panel" category would implicitly cover the router, but this source calls it out by name — a minor but real specificity addition, not a new mechanism. `single-account`, `unverified`. [source: [[_Sources/YT_86fmWWVXark_kruglov_stop_using_trends|YT_86fmWWVXark]]]

## ⚠️ Perspectives — A Designer Argues AGAINST the Master Switch, and Says the Function Worth Buying Is Water (NSDSGN, 2022-10-25)

**Recorded as a dissent from the two master-switch sections above, and worth its space because it is a designer talking a client OUT of a specifiable extra.** [source: [[_Sources/YT_2vyIWKmrSXM_nsdsgn_twenty_post_occupancy_regrets|YT_2vyIWKmrSXM]]]

**The context is a regrets video built from viewer comments, and his observation is that «о мастер-выключателе вспоминают в самый последний момент, когда ремонт уже закончен».** His analysis:

- **«Вещь конечно полезная, но если задуматься — для выключения бытовых приборов большой нужды нет.»** Two reasons: **you will never switch off the fridge («он просто тупо разморозится»), and other appliances «перегрузятся, вам заново придётся настраивать».**
- **And on the lighting side: «световые приборы сейчас очень маломощные, почти все на диодных лентах, и они потребляют очень мало энергии — если даже вы забыли выключить одну лампочку, то большой счёт за ваше отсутствие вам не придёт».**
- **⚠️ THE REDIRECTION, which is the useful part: «совсем другое дело — уезжая, перекрыть горячую и холодную воду: тут хватит и пары часов отсутствия, чтобы произошло что-то очень страшное.» → The master function actually worth buying is WATER, not electricity.** *(Which is what this vault's [[12_Engineering_and_Systems/analysis/Leak_Protection_Systems|Leak Protection Systems]] page provides, including a first-hand save from the same channel.)*
- **⚠️ AND THE RETROFIT, for a finished flat with no master switch: «если у вас не один автомат в электрощите, то просто ПОДПИШИТЕ ваши автоматы, и уезжая просто вырубите все, кроме холодильника и другой бытовой техники, которую вырубать не надо».** He is candid that «каждый раз, конечно же, вы этим пользоваться не будете» — **but «если вы уезжаете на неделю или даже на месяц, этот лайфхак вам очень поможет, и вы не увидите под холодильником огромную лужу воды».**

**→ How to read this against the sections above: they establish that a master switch can be implemented in priority groups at a stated cost, and this establishes that the domestic benefit is small once lighting is LED and appliances resent being cut. The two are reconcilable — the electrical master switch is a convenience whose value has fallen with the load, while the water shutoff is the one that prevents a catastrophe. If only one is specified, this source says specify the water.**

## Multi-Gang Switch Sequencing Should Match Walking Direction (added 2026-08-25, Квартиранты)

A real household's own hallway rewiring: a 3-button switch panel by the
entry door is wired so **button 1 controls the living room, button 2 the
hallway's own light, and button 3 a picture's accent backlight** —
deliberately ordered to match the sequence a person encounters walking
from the entry door inward, rather than an arbitrary left-to-right
assignment. A directly reusable multi-gang-switch layout principle for a
corridor with several independently-lit zones in a row: order the gangs to
match the walking path, not panel geometry. `single-account`. [source: [[_Sources/YT_sAXC1hn8u9A_kvartiranty_hallway_wall_prep_electrical|YT_sAXC1hn8u9A]]]

## Passthrough-Switch Cognitive-Load Caution (Kruglov/Ontario, Round 15, added 2026-08-28)

**⚠️ Distinct from this page's existing cost-based crossover-switch-count formula**: passthrough (проходной) switching only genuinely simplifies life if the household can mentally track which switch controls what from where. Recommendation: apply it selectively (e.g. one bedroom entry-to-bedside pair in a 30m² apartment) rather than wiring every room in a passthrough chain — an apartment fully saturated with passthrough switches becomes a "piano of switches" the household never fully learns to use. `single-account`, `unverified`. [source: [[_Sources/YT_kkE25HmFciU_kruglov_worst_solutions|YT_kkE25HmFciU]]]

**A complementary cost-justification framing, a second Ontario source (Round 15, added 2026-08-28)**: a passthrough/crossover switch setup costs roughly **2,000-4,000 RUB** more than a standard switch at a given location — framed as clearly worth paying for the daily comfort of not needing to backtrack to a switch. Doesn't conflict with the cognitive-load caution above — this source argues the marginal cost is worth it specifically at locations where passthrough switching is genuinely useful, not that it should be used everywhere. `single-account`, `unverified`. [source: [[_Sources/YT_VVxzNTshJCM_kruglov_modern_must_have_solutions|YT_VVxzNTshJCM]]]

## Touch/Capacitive Wall Switches — General-Purpose Impracticality (Kruglov/Ontario, Round 15, added 2026-08-28)

**Distinct from this page's existing under-cabinet-lighting-specific touch-sensor caution above**: a touch switch requires visually locating the exact touch point and pressing precisely, and doesn't always register on the first attempt — contrasted with an ordinary toggle/rocker switch, which can be hit anywhere on its face by feel alone with no visual confirmation needed. Recommends touch switches only where already integrated into a smart-home voice-control setup (where the physical switch is rarely the primary control method anyway). `single-account`, `unverified`, Ontario (Nikita Kuznetsov presenting). [source: [[_Sources/YT_x8cNF81m7-A_kruglov_impractical_solutions|YT_x8cNF81m7-A]]]

### A Working Alternative to Both — Wall Switch Plus Proximity Sensor (Надежда Кузина, added 2026-08-31)

**This resolves the under-cabinet touch-sensor objection above rather than restating it.** Interior designer Надежда Кузина agrees the "feel along the underside for the touch spot" type is inconvenient, but reports the **combination** as unusually successful in practice: **an ordinary wall switch as the primary control, plus a proximity sensor on the fitting itself** for the case where hands are dirty or full. The switch keeps the hit-it-by-feel property the section above defends; the sensor covers only the exception.

**She draws a distinction worth keeping**: this is a hand-brought-close sensor, **not** room-entry motion detection — it responds to a deliberate gesture at the fitting, not to someone walking in, so it does not produce the spurious triggering that makes motion sensors unsuitable for a work surface. `single-account`, `unverified`, RU. [source: [[_Sources/YT_iHViNm3dESU_kuzina_kitchen_electrics_and_lighting|YT_iHViNm3dESU]]]

**Related placement rule from the same source**: don't scatter the worktop-light switch across the backsplash separately from the outlets — put it in the same frame, on the same line ("не мельтешить по всему фартуку").

### ⚠️ A Designer's Flat Rejection of Motion Sensors, and What He Uses Instead (Александр Синчуков)

**Recorded as a dissent, because motion sensors are usually recommended for exactly the locations he refuses them in** — corridors and bathrooms — and because the Ontario reliability caution already on [[12_Engineering_and_Systems/analysis/Smart_Home_Systems|Smart Home Systems]] is about false triggering, whereas this objection is about the interaction itself:

- **«Я НЕНАВИЖУ ДАТЧИКИ ДВИЖЕНИЯ — вот это всё МАХАНИЕ РУКАМИ, чтобы они включились. А управление голосом очень удобное.»**
- **⚠️ But he states the honest limitation of his own preference in the same breath: «единственное, раздражает, когда много его нужно включать-выключать — и для этого используется СЦЕНАРИЙ.»** So voice control alone does not scale either; it scales only with scenes. See the scene reconciliation below.
- **→ This lines up with Кузина's distinction above rather than contradicting it: a deliberate gesture at a fitting is acceptable, an ambient detector that has to be coaxed is not.** `single-account`. [source: [[_Sources/YT_lhikl-7c43c_nsdsgn_own_flat_year_one_fixes|YT_lhikl-7c43c]]]

### ⚠️⚠️ A Third Practitioner, Two Flats' Experience, and He Rejects the Standard Defence — Route as Settled (Александр Синчуков, his own kitchen, 2023-11-02)

**A touch switch was offered for the worktop lighting by the furniture makers and refused, on the strength of the previous flat:**

**«Мебельщики изначально предлагали… СЕНСОРНОЙ кнопочке. В ПРОШЛОЙ КВАРТИРЕ она у меня была, И ОНА МЕНЯ ПРОСТО БЕСИЛА — она ПОСТОЯННО ГЛЮЧИЛА. Хотя кто-то говорил, что у тебя просто плохая — Я НЕ ВЕРЮ в эти все рассказы. Я сделал… просто с ОБЫЧНОЙ КНОПКИ.»**

- ⚠️⚠️ **This is the THIRD independent practitioner against furniture and task touch switches, and it is the strongest of the three because he explicitly refuses the “you just bought a bad one” defence** — the defence that normally keeps this question open.
- **The other two: the general-purpose impracticality finding recorded above, and the under-cabinet touch-sensor objection recorded from a separate designer.**
- → **Three sources, no dissent anywhere in the vault. Route as SETTLED: use a mechanical button for cabinet and task lighting.** Note the practical point that he did not lose the convenience — an ordinary button in the same position does the same job.

[source: [[_Sources/YT_AEJlxbTmQJU_nsdsgn_own_kitchen_review|YT_AEJlxbTmQJU]]]

### ⚠️⚠️ CORRECTION to the entry above — it is TWO independent practitioners, not three, and the error was mine

**The Round 6 entry above says "the THIRD independent practitioner against furniture and task touch switches… Three sources, no dissent: route as SETTLED." That count is WRONG.**

**Round 7 processed the flat that the Round 6 source calls «в прошлой квартире» — and the touch-switch complaint is already there, in February 2021: «Меня БЕСИТ вот этот СЕНСОР, потому что с ним ВСЁ ВРЕМЯ ПРОБЛЕМЫ… поэтому я рекомендовал бы включать просто с ОБЫЧНОГО ВЫКЛЮЧАТЕЛЯ.»** [source: [[_Sources/YT_hEZntyMcP-A_nsdsgn_own_previous_flat_studio_kitchen|YT_hEZntyMcP-A]]]

- → **So two of the three instances are THE SAME PERSON, reporting the same failure in TWO DIFFERENT FLATS 2.7 years apart. The vault has TWO independent practitioners against these switches, plus one practitioner twice.**
- → **⚠️ The FINDING survives and is arguably stronger — a repeat failure across two installations, with the "you just bought a bad one" defence explicitly refused in 2023 — but the COUNT was inflated and "settled" was overstated. Two sources is good evidence, not a closed question.**
- ⚠️⚠️ **AND THE PROCESS ERROR IS WORTH RECORDING BECAUSE I HAD ALREADY WRITTEN THE RULE THAT PREVENTS IT. Round 5 established: *an established form is only evidence if its instances are INDEPENDENT — count SOURCES, not OCCURRENCES.* I recorded that lesson and then broke it one round later, on the same channel, by counting one practitioner's two flats as two practitioners.**


## ⚠️⚠️ Switch Mechanism Cycle Life — 1,000 vs 20,000 Operations, and a Fire

**The most consequential safety item on this page, and it comes with a diagnostic signature.** Designer Александр Синчуков, 20 years' practice. [source: [[_Sources/YT_WCoqOCofPx4_nsdsgn_durable_interior_ten_rules|YT_WCoqOCofPx4]]]

- **⚠️ THE FIGURES, and the purchasing criterion they imply: «самый дешёвый выключатель выдержит у вас там 1.000 НАЖАТИЙ, а если вы покупаете просто качественный — не самый дорогой, не из мрамора, а из ПЛАСТИКА, но с КАЧЕСТВЕННЫМ МЕХАНИЗМОМ — выдержит 20.000 НАЖАТИЙ и прослужит гораздо дольше.»** A 20× difference.
  **→ The criterion is the MECHANISM, not the faceplate material — which is a genuinely useful separation, because the visible half is what price is usually judged on. This page's plate-colour sections above are about the visible half; this is about the half that fails.** `single-account`, `unverified` figures.
- **⚠️ Where economising IS acceptable, stated precisely: «можно экономить на механизмах, которые находятся ЗА ТЕЛЕВИЗОРОМ, которые не видно — можно купить попроще. Но НЕ надо покупать самые дешёвые.»** So the trade is by operation count and visibility, not a blanket rule.
- **⚠️⚠️ THE FIRE, and the precursor is the part worth memorising: «на прошлой квартире я лежу дома, СПЛЮ, и тут у меня ВКЛЮЧАЕТСЯ СВЕТ. Я такой: что происходит? Через, наверное, 5 СЕКУНД из выключателя начинает идти ЧЁРНЫЙ ДЫМ. Он просто ЗАГОРЕЛСЯ. Много раз, несколько лет на него нажимали, в итоге механизм вышел из строя, там что-то замкнуло и пошёл огонь. То есть СВЕТ ВКЛЮЧИЛСЯ. Это было жутко страшно. Хорошо, что это случилось НОЧЬЮ, когда я был дома — если бы меня не было, чем бы всё это могло закончиться?»**
  **→ A worn switch mechanism failing to a short and igniting, announcing itself by switching the light on unbidden. A light that comes on by itself is therefore not merely a fault to schedule — it is a reason to kill that circuit immediately.** This vault holds no other account of this failure mode.
- **On the protective side he is unambiguous and brief: «то, на чём точно не надо экономить — это АВТОМАТЫ… экономия на одном автомате может спасти вас от такой вещи, как ПОЖАР.»** Consistent with [[12_Engineering_and_Systems/analysis/Electrical_Panel_Design_and_Assembly|Electrical Panel Design and Assembly]].

## ⚠️⚠️ How Many Light Groups? — the Same Practitioner Answers Twice, Four Years Apart, and the Two Answers Reconcile

> [!IMPORTANT]
> **This page and [[12_Engineering_and_Systems/analysis/Lighting_Design|Lighting Design]] both carry a scenario-count debate. Александр Синчуков supplies both sides of it himself, and the reconciliation is a single rule rather than two competing recommendations.**

**2022 — cap the count.** «Изначально все просят: я хочу много световых групп, я хочу разные сценарии. **Но по факту, во время жизни, всё сводится к ДВУМ, максимум ТРЁМ сценариям. Больше световых групп уже просто начинает РАЗДРАЖАТЬ, когда ты стоишь и ИЩЕШЬ выключатель, который тебе нужен.**» His own case, filming in a large house: about a minute standing there selecting the right light. He allows that a permanent resident may memorise it, «но скорее всего вы будете включать просто ОДНИМ ДВИЖЕНИЕМ». **This is the same cognitive-load argument as the "piano of switches" caution above, arrived at independently.** [source: [[_Sources/YT_CSpXvPWpsgQ_nsdsgn_fifteen_post_occupancy_regrets|YT_CSpXvPWpsgQ]]]

**2024 — many devices, one command.** In his own flat he now has a controlled socket with a night-light in the study, a kitchen floor lamp, wall night-lights, a bedside lamp and motorised curtains, and reports exactly the predicted problem: **«чтобы всё это закрыть, нужно КАК ДУРАК ХОДИТЬ ПО ВСЕЙ КВАРТИРЕ, говорить: Алиса, закрой это; Алиса, выключи это.»** The fix: **«прописал СЦЕНАРИЙ — когда ты говоришь просто "Алиса, спокойной ночи", у тебя выключается весь свет, который тебе нужно, и ЗАКРЫВАЮТСЯ ШТОРЫ… оно очень просто делается, и я всем его рекомендую».** [source: [[_Sources/YT_lhikl-7c43c_nsdsgn_own_flat_year_one_fixes|YT_lhikl-7c43c]]]

**→ THE RULE, stated once instead of twice: the tolerable number of light groups is set by whether a SCENE can collapse them into one action. Without scenes, cap at two or three — the 2022 advice stands and the search cost is real. With scenes, the count stops mattering, because the household never enumerates the groups.** The corollary is a specification one: **if a project is being drawn with many groups, the scene layer is not an optional upgrade — it is what makes the group count usable**, and the master-switch dissent above is the same argument in a cruder form (one action beats many).

> [!WARNING]
> **⚠️⚠️ CORRECTION, 2026-09-03 — THE RULE ABOVE IS NOT MY SYNTHESIS. HE STATED IT HIMSELF, IN JANUARY 2022, BEFORE EITHER SOURCE THE SECTION ABOVE IS BUILT FROM.**
>
> An earlier video from the same channel (`CN-Ab_g4CAI`, **2022-01-26**) carries the cap AND its resolution in one sentence: **«когда групп света слишком много, это очень сильно УСЛОЖНЯЕТ вашу жизнь. В ИДЕАЛЕ, ЕСЛИ ВЫ ХОТИТЕ БОЛЬШЕ ТРЁХ ГРУПП ОСВЕЩЕНИЯ, ТО ХОРОШО ЭТИ ГРУППЫ ОБЪЕДИНИТЬ [В] УМНЫЙ ДОМ. В противном случае, если при входе в комнату у вас будет ПИАНИНО ИЗ ВЫКЛЮЧАТЕЛЕЙ, 10 цветовых групп, это будет каждый раз превращаться в ИГРУ "НАЙДИ ВЫКЛЮЧАТЕЛЬ".»**
>
> **I presented the reconciliation above as something I had constructed from a 2022 cap and a 2024 practice. It is the source's own rule, and the vault must credit it as such.** The 2024 own-flat account remains valuable as *evidence that he then followed his own rule*, but it is corroboration, not the other half of a contradiction.
>
> **⚠️ Note also that «ПИАНИНО ИЗ ВЫКЛЮЧАТЕЛЕЙ» is the same image as the "piano of switches" caution recorded on this page from Kruglov/Ontario — and this instance is earlier. Convergent phrasing, possibly a common trade idiom; recorded as convergence rather than as one source citing another.**
>
> **→ The lesson for this vault, which is the same one as the surname correction logged the same day: before crediting a synthesis to the reading, check whether an earlier source in the same channel already made it. A channel's back catalogue can contain the resolution to what looks like its own contradiction.** [source: [[_Sources/YT_CN-Ab_g4CAI_nsdsgn_thirtyfive_beautiful_but_impractical|YT_CN-Ab_g4CAI]]]

**⚠️ And the three combinations he says a household actually needs, from the same January 2022 source — which is where this channel's "the bright fitting is a CLEANING light" framing originates:** **«яркий свет для УБОРКИ или если вы просто любите яркое освещение; СПОКОЙНЫЙ свет для повседневной жизни; и НОЧНОЙ НАВИГАЦИОННЫЙ свет, он помогает перемещаться в тёмное время суток.»** All fittings on **one colour temperature**. **→ That framing was later found in three separate rooms of his own flat (Rounds 4-5), so the vault has the rule and three instances of him living by it.** See [[12_Engineering_and_Systems/analysis/Lighting_Design|Lighting Design]] and [[07_Bathroom/analysis/Lighting_and_Electrical|Bathroom: Lighting and Electrical]].

## Named Product Line and a Frame-Swap Lifehack (added 2026-08-24, Round 2)

Pavel Sidorik names **EKF-brand outlets/switches, "Valencia" series**, with a direct price/quality assessment: "хороший вариант по соотношению цена и качество" (good price-to-quality ratio). Devices planned for one project: two-gang switch, two-gang pass-through (3-way/traveler) switch, one-gang switch, grounded outlets, outlets with integrated USB charging ports, network/ethernet outlets — a TV antenna outlet was considered and explicitly excluded. **Cosmetic lifehack: swap only the switch/outlet's outer frame (рамка) to a different color while keeping the same white mechanism/base** — frames are sold separately from the mechanism, making this a cheaper way to get a color accent than buying an entirely different product line. `single-account`, region unresolved for this episode (series-level Belarus attribution established elsewhere in this channel's other episodes). [source: [[_Sources/YT_9-NjgDLleOw_sidorik_electrical_ep6|9-NjgDLleOw_sidorik_electrical_ep6]]]

### Two Switching Cases Set by Furniture, Not by the Room (Надежда Кузина, added 2026-08-31)

Both from a planning lecture, and both are decided at layout stage rather than by any switch-height rule. [source: [[_Sources/YT_Rcd9gkPC6CI_kuzina_apartment_ergonomics_bedroom_kids_hallway|YT_Rcd9gkPC6CI]]]

- **⚠️ A bunk bed requires a two-way switch at the door, and she found this out by testing it.** The sconce must be reachable from the bed — but without a second switch by the door, a child who falls asleep with the sconce on in the **top** bunk means a parent climbing the ladder past a sleeping child to turn it off. **"Я кстати пробовала, я реально сама просто на этой лестнице не помещаюсь."**
- **Where spouses wake at different times, the bedroom wardrobe zone needs its own lighting and its own control**, so one can dress without waking the other. Both belong in the electrical drawing at the same time the bedroom layout is fixed.

## ⚠️ Two Drawing-Stage Practices That Prevent Electrical Errors (Татьяна Михайловская, added 2026-09-01)

**Both come from a designer walking through her own project package, and both are practices this vault had nothing on.** [source: [[_Sources/YT_MkssMwpyVsI_mikhailovskaya_design_project_composition|MkssMwpyVsI]]]

### 1. Separate black-and-white electrical elevations

**Elevations showing ONLY sockets, switches, electro-outlets and cable channel — in black and white, for every wall of every room including bathroom and WC, with dimensions.**

**She notes she has not seen other designers do it, and gives the argument rather than a preference:**

> **"Многие розетки у нас находятся за мебелью, электровывод можно упустить, который там в потолке находится. Если мы делаем отдельно такие развертки, мы этого не упустим."**

**On a coloured elevation carrying furniture an outlet is legible but easy to overlook. On a bare one it is the only thing there.**

*(Her own self-criticism on the drawing, offered as advice: the hatching overlapped the labels — "либо делайте штриховку светлее, либо подписи немножко смещайте… не делайте так, как я.")*

### 2. ⚠️ Label every outlet, including the ones no switch controls

**On the switch-binding plan she labels every electro-outlet — including those not connected to any switch**, for instance one energised by a door opening.

Her worked labels: *"электровывод, высота такая-то, подсветка шкафа, выключается на открывание двери"*; and for a sconce switched on the fitting itself, *"бра выключается на приборе."*

> **⚠️ The reason is self-checking, not documentation: "часто можно сделать ошибки в этих планах, и для того чтобы себя перепроверить, лучше все выводы взять себе за принцип подписывать."**
>
> **An unlabelled outlet is ambiguous between "deliberately unswitched" and "you forgot to connect it."** Labelling removes the ambiguity — **and reduces questions back to the designer.**

**Also on the sockets-and-switches plan: a table counting sockets, frames and outlets, with every socket and outlet labelled with height and size.**

## ⚠️ Switch/Outlet Plate Colour Should Match the Wall by Default (Игорь Краснов, added 2026-09-01)

**Standard white plastic switches/outlets clash visibly against dark, complex, or saturated wall colours/finishes and read as an unfinished detail.** **Match the plate colour to the wall (or tile) colour** where the palette allows (e.g. dark-grey wall → dark-grey/graphite plate; beige wall → beige/cream plate) so the fixture visually disappears. **Contrasting plates (e.g. black on a light wall) can work as a deliberate accent** — his own studio uses this — but the shade must match the room's palette precisely; even a small mismatch reads as an error rather than a choice, so only use a contrast when confident in the exact tone. `single-account`, `unverified`. [source: [[_Sources/YT_NvHEQ7vnxfI_krasnov_8things_cheap_apartment|NvHEQ7vnxfI]]]

## ⚠️ Plate Colour — White Is the Worst Default, and Rooms May Differ (Татьяна Безверхая, added 2026-09-02)

> [!WARNING]
> **`promotional_ratio: high` — sponsored product review**, structured as an unboxing of a manufacturer's review box, with a verdict, a note that the brand offers special terms to design professionals, and a closing pointer to its authorised partners. **The product verdict, the tactile and colour-range praise, and a claimed 25-year design service life are excluded from this page.** **Brand identity is deliberately not named** — the auto-generated captions render it inconsistently ("НZ" / "КНС" / "CRН" / "КРНс") and, the review being sponsored, its identity is not needed for anything below. Only the brand-independent selection method is recorded. RU, no prices in the source, 2025. [source: [[_Sources/YT_bcHTIHyWiVc_bezverkhaia_socket_switch_selection|bcHTIHyWiVc]]]

### Why the choice is worth making deliberately

- **⚠️ A common mistake among people managing their own renovation: not thinking about electrical accessories at all.** When it comes time to buy, people take the cheapest or the most ordinary thing — **and she means the visible outer parts specifically (клавиши, накладки), not the mechanisms** — so a decent interior ends up with characterless accessories.
- **Her argument for why it shows**: there are always many of them, in every corner and beside every door, **and they are the part of the interior you physically touch every day, many times a day.**

### ⚠️ Colour — this sharpens the existing match-the-wall rule rather than repeating it

**This page already holds Игорь Краснов's rule that plate colour should match the wall by default, with contrast permitted only as a deliberate, exactly-toned accent. She agrees and adds latitude and edge cases:**

- **⚠️ Her headline is counter-intuitive: the worst colour for electrical accessories is white.** Plain white reads cheap and reads plain **"вне зависимости от дизайна."**
- **⚠️ The one case where white is right: a genuinely snow-white interior** — her example is a white modern-classic scheme, where white plates on white walls work precisely because it is white-on-white.
- **⚠️ The failure tolerance is tighter than expected: if the walls have any tint at all** — even slightly milky or slightly greyish, let alone a real colour — **white accessories read "колхозно."**
- **Black works in any interior that already contains some shade of black**, giving graphic accents; she names minimalism, all contemporary styles, loft and Scandinavian.
- **⚠️ The most directly actionable addition to Краснов's rule — greys with a stated latitude: from light grey to dark saturated graphite, chosen either to match the wall colour or one to two shades darker than the wall.**
- **⚠️ Form follows style, which this page did not hold**: **rounded-corner** series suit styles with any classical inflection and eclectic styles (Japandi named); **sharp, pronouncedly rectangular** series suit **only minimalism and ultra-laconic interiors** — not modern classic, not retro, where they read as wrong.
- **⚠️ Different rooms may legitimately use different colours, and she names the opposite assumption as another frequent self-managed-design error**: "никто не заставляет вас делать одинаковые розетки по всей квартире." Her worked example — lighter or grey in a children's room, black in the entrance zone, white in a white bedroom. **This also nuances Pavel Sidorik's frame-swap lifehack above: swapping only the outer frame while keeping one mechanism type is exactly what makes per-room colour variation cheap.**

### Three brand-independent technical facts

- **⚠️ Back boxes differ by country** — "подрозетники во всех странах тоже разные, как и сами розетки." A range built for the Russian market is designed around the **standard round back box** used there. **Consequence: imported accessories are not automatically compatible with back boxes already installed.**
- **⚠️ Frames are sold by post count, and a socket count is not a frame count.** Single-post frames are typically included with the device, so it arrives ready to install — **but multi-gang blocks require separately purchased two-, three- or four-post frames.** A buying-list item that is easy to miss when counting devices off a plan; complements the socket/frame/outlet counting table already recorded above from Татьяна Михайловская.
- **Pass-through / two-way switches (проходные)** — control one fitting or group from several places (on at the start of a corridor, off at the end; on at a bedroom door, off at either side of the bed). She recommends them **"в каждом ролике."**

> [!NOTE]
> **The pass-through recommendation is a third corroborating account and does not disturb this page's existing position.** This page already carries both the cost justification (≈2,000–4,000 RUB extra per location, Kruglov/Ontario) and the cognitive-load caution against saturating an apartment with them. **Her blanket enthusiasm corroborates the usefulness only — she offers no reasoning that engages with the saturation caution, so it is not a counter-argument to it.**
