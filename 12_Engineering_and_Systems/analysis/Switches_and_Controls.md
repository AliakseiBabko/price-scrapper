# Electrical — Switches & Controls

Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]].

**Install a master cut-off switch near the main entrance** — a single button that shuts down all (or most) apartment lighting on the way out, rather than checking room by room. In its fuller version, it also controls the duty/night-light circuit below, giving one action that covers every light in the apartment. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Use two-way ("проходной") switches for a room's main light where it makes sense** — most valuably bedside, so a light can be switched off without getting back up: cheap to install, disproportionately high perceived comfort value. **Extend the same logic across a whole chain of adjoining passage rooms** (e.g. entry → corridor → living room) — every room in the chain shares one switch group controlling the same circuit, switchable from any point, so nobody has to backtrack to turn off a light in a room they've already left. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**A dedicated "duty"/night-light circuit is worth building in**: a separate, always-on low-level light — distinct from the main light — in hallways, entries, and bathrooms, letting someone navigate at night without triggering bright main lighting. Controlled from at least the entry door and typically from multiple points. Belongs in hallways/WCs, never bedrooms — see [[12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning|Key Concepts & Planning]] for the full lighting-category taxonomy this fits into. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Install dimmers as a low-cost upgrade** on primary living/bedroom lighting circuits. **Finalize the actual bulbs being used before buying a dimmer** — dimmer compatibility depends on matching leading-edge vs. trailing-edge dimming to the bulb/driver type, and buying the wrong pairing is a common, avoidable mistake. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Minimize switch/gang count per location** — two gangs for a living room's main controls is commonly enough; six is usually over-specification that adds cost and visual clutter without functional benefit. Prefer several single-gang switches over one crowded multi-gang plate where space allows, and keep every standard toggle switch in the apartment on the **same ON/OFF orientation** — a mixed-orientation install is a common, avoidable annoyance. Never position a switch inside a future door's swing zone, checked against the door leaf's full opening arc, not just its closed position. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Two-way switches work in pairs; a run with three or more control points adds "intermediate" (crossover) switches between the two end switches**, not more two-way switches — a distinct component. Wire joints must terminate in a proper junction box; twisted-and-taped joints left exposed outside a junction box are a common, unsafe jobsite shortcut. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Konstantin Kruglov / Ontario gives the precise general formula for the two-way/crossover pattern above**: keep exactly 2 two-way switches at the two logical "end" locations regardless of how many control points exist, and add one crossover/intermediate switch per additional point beyond those two — 3 points = 2 two-way + 1 crossover; 4 points = 2 two-way + 2 crossover; 10 points = 2 two-way + 8 crossover. Buying two ordinary standard switches and asking an electrician to wire them as two-way does not work — the devices must be two-way switches by construction from the start. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_1dp7alivsLQ_kruglov_safe_sockets_switches|1dp7alivsLQ_kruglov_safe_sockets_switches]]]

**⚠️ Never tie an exhaust-fan/ventilation circuit to the main light switch (Round 13 triage, added 2026-08-28)**: wiring a bathroom's extractor fan to switch on automatically with the main light is a common but avoidable mistake — always give ventilation its own dedicated switch. Konstantin Kruglov / Ontario, `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_0TLDGD8MY1A_kruglov_top_renovation_mistakes_2026|YT_0TLDGD8MY1A]]]

**Konstantin Kruglov / Ontario: two devices worth avoiding, with reasoning** — (1) triple-gang switches: each gang is only ~2cm wide (about one fingertip), making it hard to hit the right gang reliably, especially at night; (2) wiring 3+ crossover control points onto one multi-gang switch instead of using separate crossover switches — the cable run required is disproportionate to the benefit. **Avoid a two-way ("проходной") dimmer specifically**: switch/socket lines are normally bought matched from one manufacturer/collection, and a two-way-capable dimmer often only exists in a different product line, forcing a visible frame/finish mismatch across the installation. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_1dp7alivsLQ_kruglov_safe_sockets_switches|1dp7alivsLQ_kruglov_safe_sockets_switches]]]

**Buy sockets, switches, and cover-frames from one manufacturer and, ideally, one product line/collection, sourced together** — a real documented client case: a client bought round-bodied socket/switch mechanisms with square-shaped cover frames from mismatched sources for a 45-point order (30 sockets, 15 switches); caught and returned before installation, but framed as a routine, easy-to-make mistake worth an explicit warning rather than assuming it's obvious. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_1dp7alivsLQ_kruglov_safe_sockets_switches|1dp7alivsLQ_kruglov_safe_sockets_switches]]]

**Socket mounting-type taxonomy**: surface-mounted (no back-box needed), flush/recessed (back-box + routed cable), pop-out/retractable (spring- or button-actuated, e.g. a kitchen-island pop-up socket), and panel-mounted (clipped to the DIN rail like a breaker — specialized, not detailed further). **Grounding is a hard requirement** — every power socket should be grounded; avoid ungrounded sockets entirely. **Water-protection sockets are visually distinguished only by a hinged cover** — cover present = water-protected (bathrooms, loggia/outdoor); no cover = not. **Child-safety shutter-curtain sockets exist but a correctly-specified breaker/RCD combination plus supervision is the real protection** — even on accidental contact, correctly-specified protective devices should trip before serious harm. Other named sub-types: smart (hub/network-controlled) sockets, lockable-cover (key-actuated) sockets, sockets with an integrated voltage-monitoring relay (very sensitive appliances only, rarely used in apartments), and a decorative illuminated "socket-nightlight" hybrid (explicitly dismissed as a novelty, not a real recommendation). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_1dp7alivsLQ_kruglov_safe_sockets_switches|1dp7alivsLQ_kruglov_safe_sockets_switches]]]

**A bathroom/WC exhaust fan's switch belongs inside the room it serves, not in the adjoining hallway.** Automating a fan is fine for auto-OFF (a timer that shuts it off after a delay) but not for auto-ON (an occupancy/humidity sensor that starts it without warning) — auto-ON is startling for the occupant. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Prefer spring-clamp (screwless, self-clamping) terminals over screw terminals on finish-stage outlets/switches** — screw terminals are more prone to loosening from thermal cycling over time. Evaluate a device by country of manufacture and terminal type rather than by brand name alone. Avoid switches with an integrated LED backlight/indicator — a reported flicker/glow issue with some LED bulb types. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Kitchen counter outlet rule**: every open/free counter zone gets its own outlet; the main cooking zone additionally needs its own task-lighting switch. **Avoid touch/capacitive-sensor controls for standard-tier under-cabinet lighting** — reported as unreliable (doesn't consistently respond to a hand-wave despite marketing claims) and less convenient with wet/dirty hands, which can still press a physical switch but may be reluctant to touch a sensor pad; may be more appropriate for premium-segment kitchens. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8eECI5sWEy4_switch_placement_general_rules|8eECI5sWEy4_switch_place]]]

**Highly granular per-zone lighting circuits are easy to over-specify at design time and commonly go unused in practice — plan for roughly 2 real circuits per room (day/night) as the default, not more, absent a specific documented need.** A real Category 5 case: an as-wired apartment had several independent lighting zones per room (a genuine over-spec), and the owners' own retrospective admission was that the granular zoning went almost entirely unused once installed — smart-switch reprogramming was needed afterward just to consolidate the circuits onto fewer physical controls. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_iEpRx5Pe7to_designer_disaster_20m_277|YT_iEpRx5Pe7to]]]

**⚠️ Smart-switch relay click noise near a bedroom is a real, checkable nuisance worth verifying before installation, not a hypothetical concern.** Some smart-switch relay types click audibly on activation — disruptive specifically in a quiet nighttime bedroom setting. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_iEpRx5Pe7to_designer_disaster_20m_277|YT_iEpRx5Pe7to]]]

**Pre-wire an outlet cluster wherever a future device (e.g. a security camera) is anticipated, even if it isn't being installed yet** — avoids visible surface cabling being added later. A documented case: a pre-installed outlet cluster near a kids'-room ceiling corner meant a camera added afterward required no additional visible wiring. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_iEpRx5Pe7to_designer_disaster_20m_277|YT_iEpRx5Pe7to]]]

**A large open-plan space needs a light switch reachable near every exit path, not just at the main entry** — reiterated across two independent Category 5 defect cases, both requiring a "walk blind" across a dark room to reach the only switch. `single-account` each, `unverified`. [sources: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cWRgenv4B40_full_disaster_30m_274|YT_cWRgenv4B40]], and this vault's existing entry/corridor-chain guidance above]

**Keep safety/reliability-critical controls (a room's main light switch, a WC/bathroom's light control) on physical, non-networked hardware — reserve voice/app/smart-home control for genuinely optional comfort features only.** A real household's stated reasoning: if a basic function (turning on a light to see) depends on an internet connection or a voice-assistant service, an outage means you can't perform an ordinary daily task. A specific real anecdote: a voice-controlled kitchen backsplash light was used "effectively twice — once when it was installed, once when we found someone dumb enough to buy it from us," offered as evidence the novelty didn't survive contact with daily use. Pairs with this vault's existing wired-vs-wireless smart-home reliability finding (`6syO3dTButw`, Category 5 chunk 3). `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_zPR8PGWq5lA_3yr_diy_deviations_case_229|YT_zPR8PGWq5lA]]]

**A voltage relay (реле напряжения) is recommended as a standard electrical-panel component, even in a budget build-out** — protects connected equipment from grid voltage spikes/surges. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_ajtv-urp18I_old_building_crossover_tips_101|YT_ajtv-urp18I]]]

**An exposed electrical panel should be sized to the apartment's actual circuit count, not oversized as a decorative feature** — a documented defect used a panel far larger than any legitimate circuit count for the unit, functioning as an unconcealed wall feature rather than real capacity; the general rule (see the false-wall/panel-concealment guidance elsewhere in this vault) is to plan real circuit count first, then conceal a correctly-sized panel behind a false wall. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_ROv1BuBfECU_designer_disaster_35m_281|YT_ROv1BuBfECU]]]

**Cluster a multi-circuit switch group near the seating/sofa position in a combined kitchen-living room**, controlling separate lighting circuits (e.g. kitchen zone + loggia zone) from one location rather than scattering single switches at each zone's own entry. Pairs with the balcony-door-slope socket guidance below. **A balcony/loggia door slope (откос) should carry at least two sockets** — practical loggia-zone device/lighting need, not just a design flourish. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_WmkOC9uKnCQ_kitchen_living_loggia_layout_lifehack_154|YT_WmkOC9uKnCQ]]]

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
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_QfTqabNW1Lc_kodolov_electrical_rough_install|QfTqabNW1Lc_kodolov_electrical_rough_install]]]

## Electrical-Panel Niche Sizing Formula (added 2026-08-19, remainder-pool Round 2)

**⚠️ Electrical-panel recess: minimum 110mm panel installation depth → build the niche to at least 140mm deep.** If the host wall isn't thick enough to net a structurally sound remainder after recessing, thicken it first — worked example: a 200mm neighbor-shared wall thickened to 250mm specifically to make a 140mm-deep niche viable. **Full coordinate sequence, worked example**: from the floor screed, offset 1200mm up for the niche's bottom edge, then a further 500mm for the niche's height (spanning roughly 1200-1700mm above the floor); horizontally, offset 100mm from the neighbor-shared wall, then 400mm for the niche's width. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_C4lUAfJyyb0_developer_stolen_meters_170|YT_C4lUAfJyyb0]]]

## Precise Switch-Reachability Formula & Window-Reveal Outlet Clearance (added 2026-08-19, remainder-pool Round 2)

**⚠️ Position a switch 90cm from the floor, 15cm from the opening's edge** — demonstrated as the exact figures needed to reliably find and press a switch without looking. **Window-reveal outlet clearance: 10-15cm from the windowsill's own plane**, not flush against it. **Master-switch differentiation, a third independent corroborating instance**: a master switch identical in height/appearance to the regular switch group is a real usability failure. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_eezwcNG-1qI_designer_project_walkthrough_269|YT_eezwcNG-1qI]]]

## Master-Switch Differentiation & Baseboard-Electrical Caution (added 2026-08-19, remainder-pool Round 2)

**⚠️ A "master" switch that cuts power/lighting to the whole unit must be physically set apart from the regular switch group** — a different height/position, and visually distinct in appearance — specifically to prevent it being pressed by accident. **⚠️ Avoid routing outlets, TV coax, or network/twisted-pair cabling through a baseboard channel system as the primary distribution method** — this creates a furniture-placement conflict, since there's no way to know in advance exactly where a TV or other furniture piece should sit if its power/data connections are scattered along a low baseboard run rather than fixed at the wall location the furniture will actually occupy. Plan electrical/data points at their intended furniture-height locations instead. **A real documented extreme failure case**: 5 switches at one bedroom's entry plus 6 more elsewhere (11 total across two adjoining rooms), none clearly labeled by function — a striking real-world instance of violating the single-switch-per-room-exit principle already established in this vault. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_MWDcYHqe-iQ_designer_apartment_walkthrough_288|YT_MWDcYHqe-iQ]]]

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
- **⚠️ Second-household-member usability caveat, Round 15 (added 2026-08-28)**: because the master switch fully cuts the apartment's general lighting circuit, a household member who stays home/sleeps in after another member leaves for work (switching off the master light on the way out) loses light access entirely until they themselves walk to the entry door and reactivate it — a real, easily-overlooked tradeoff in a multi-person household with staggered schedules. Konstantin Kruglov / Ontario, `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_VVxzNTshJCM_kruglov_modern_must_have_solutions|YT_VVxzNTshJCM]]]
- **Vetting heuristic**: if a prospective electrician can't give a
  clear answer about master switches, treat that as a sign they aren't
  fully current on residential electrical practice.
- Also used per-floor in multi-story country houses, not just
  single-apartment installs.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_zuh3k15-STo_petrishin_master_switch|zuh3k15-STo_petrishin_master_switch]]]

**⚠️ Router and security-camera system named explicitly in a fourth independent source's exclusion list (Round 14 triage, added 2026-08-28)**: Konstantin Kruglov / Ontario restates the same master-switch inconvenience case and "vacation mode" scoped-switch alternative already covered above, but names the **Wi-Fi router and a security/surveillance camera system** directly as always-excluded devices, alongside the refrigerator and leak-protection system already on this page's priority-group list. The existing "weak-current panel" category would implicitly cover the router, but this source calls it out by name — a minor but real specificity addition, not a new mechanism. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_86fmWWVXark_kruglov_stop_using_trends|YT_86fmWWVXark]]]

## Multi-Gang Switch Sequencing Should Match Walking Direction (added 2026-08-25, Квартиранты)

A real household's own hallway rewiring: a 3-button switch panel by the
entry door is wired so **button 1 controls the living room, button 2 the
hallway's own light, and button 3 a picture's accent backlight** —
deliberately ordered to match the sequence a person encounters walking
from the entry door inward, rather than an arbitrary left-to-right
assignment. A directly reusable multi-gang-switch layout principle for a
corridor with several independently-lit zones in a row: order the gangs to
match the walking path, not panel geometry. `single-account`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_sAXC1hn8u9A_kvartiranty_hallway_wall_prep_electrical|YT_sAXC1hn8u9A]]]

## Passthrough-Switch Cognitive-Load Caution (Kruglov/Ontario, Round 15, added 2026-08-28)

**⚠️ Distinct from this page's existing cost-based crossover-switch-count formula**: passthrough (проходной) switching only genuinely simplifies life if the household can mentally track which switch controls what from where. Recommendation: apply it selectively (e.g. one bedroom entry-to-bedside pair in a 30m² apartment) rather than wiring every room in a passthrough chain — an apartment fully saturated with passthrough switches becomes a "piano of switches" the household never fully learns to use. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_kkE25HmFciU_kruglov_worst_solutions|YT_kkE25HmFciU]]]

**A complementary cost-justification framing, a second Ontario source (Round 15, added 2026-08-28)**: a passthrough/crossover switch setup costs roughly **2,000-4,000 RUB** more than a standard switch at a given location — framed as clearly worth paying for the daily comfort of not needing to backtrack to a switch. Doesn't conflict with the cognitive-load caution above — this source argues the marginal cost is worth it specifically at locations where passthrough switching is genuinely useful, not that it should be used everywhere. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_VVxzNTshJCM_kruglov_modern_must_have_solutions|YT_VVxzNTshJCM]]]

## Touch/Capacitive Wall Switches — General-Purpose Impracticality (Kruglov/Ontario, Round 15, added 2026-08-28)

**Distinct from this page's existing under-cabinet-lighting-specific touch-sensor caution above**: a touch switch requires visually locating the exact touch point and pressing precisely, and doesn't always register on the first attempt — contrasted with an ordinary toggle/rocker switch, which can be hit anywhere on its face by feel alone with no visual confirmation needed. Recommends touch switches only where already integrated into a smart-home voice-control setup (where the physical switch is rarely the primary control method anyway). `single-account`, `unverified`, Ontario (Nikita Kuznetsov presenting). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_x8cNF81m7-A_kruglov_impractical_solutions|YT_x8cNF81m7-A]]]

## Named Product Line and a Frame-Swap Lifehack (added 2026-08-24, Round 2)

Pavel Sidorik names **EKF-brand outlets/switches, "Valencia" series**, with a direct price/quality assessment: "хороший вариант по соотношению цена и качество" (good price-to-quality ratio). Devices planned for one project: two-gang switch, two-gang pass-through (3-way/traveler) switch, one-gang switch, grounded outlets, outlets with integrated USB charging ports, network/ethernet outlets — a TV antenna outlet was considered and explicitly excluded. **Cosmetic lifehack: swap only the switch/outlet's outer frame (рамка) to a different color while keeping the same white mechanism/base** — frames are sold separately from the mechanism, making this a cheaper way to get a color accent than buying an entirely different product line. `single-account`, region unresolved for this episode (series-level Belarus attribution established elsewhere in this channel's other episodes). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_9-NjgDLleOw_sidorik_electrical_ep6|9-NjgDLleOw_sidorik_electrical_ep6]]]
