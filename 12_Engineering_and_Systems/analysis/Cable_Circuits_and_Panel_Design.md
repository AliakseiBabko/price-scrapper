# Electrical — Cable Sizing, Circuits & Panel Design

Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]].

## Cable Gauge, Breakers & Circuits

**Cable-gauge-by-load table (copper)**: 1.5 mm² for lighting circuits, 2.5 mm² for socket/outlet circuits, 4 mm² for ovens, 6 mm² for cooktops and other high-draw appliances. A 4–6 mm² high-load circuit should never be split or branched partway along its run. [source: [[_Sources/YT_JrClDJb8WTM_cable_sizing_breaker_selection|JrClDJb8WTM_cable_sizing]]]

**Breaker curve selection**: curve B for socket circuits (tolerates appliance inrush current without nuisance-tripping), curve C for lighting and AC circuits. Curve D is not recommended for residential use. Breaker amperage pairs to cable gauge: roughly 10A for 1.5 mm², 16A for 2.5 mm², 20A for 4 mm², 32A for 6 mm² (this practitioner's convention — verify against your local code before treating as a fixed rule). [source: [[_Sources/YT_JrClDJb8WTM_cable_sizing_breaker_selection|JrClDJb8WTM_cable_sizing]]]

**Why the breaker pairing works mechanistically**: a 2.5mm² cable can handle 20-25A continuously but is protected by a 16A breaker, so the breaker trips well before the cable itself would begin to heat up under a fault, given correct installation. The stated design target for rough electrical overall: survive at minimum 5 renovation cycles (at an estimated 5-7 years between renovations), implying a ~30-year minimum lifespan — cable/connection lifespan doesn't depend on user behavior the way a socket/switch's wear does. [source: [[_Sources/YT_NXwfvUwUKLc_rough_electrical_lifespan_testing|NXwfvUwUKLc_rough_electr]]]

**Panel circuit-count formula**: at least 2 circuits per room (one lighting, one sockets), plus 1 dedicated circuit for AC where present; oven and cooktop each get their own dedicated circuit; wet rooms (bathroom, WC, kitchen) require an RCD/differential breaker. [source: [[_Sources/YT_ciXeqvKDKSI_panel_circuit_formula|ciXeqvKDKSI_panel_circui]]]

**Panel/electrical-cabinet location: avoid siting it in a humid technical room, not just a wet room.** Архитектор Виталий Злобин (independent architect, `single-account`, region: Russia level 1 for the general design convention cited) — extracted from a house-scale gas-boiler-room video but the underlying reasoning is general, not gas-specific: an electrical panel is vulnerable to elevated ambient humidity, and any water-treatment/water-preparation technical space runs meaningfully more humid than an ordinary room even without being a "wet room" in the bathroom/kitchen sense. This adds a *location* rule distinct from this page's existing wet-room-circuit-protection content above (which covers RCD/breaker protection for circuits serving a wet room, not panel placement itself). [source: [[_Sources/YT_KXszjTBmfpQ_zlobin_boiler_room_theory_1|KXszjTBmfpQ]]]

**Keep at least 15 cm separation between power cabling and low-voltage/signal cabling** — reduces electromagnetic interference. Note a real capacity constraint worth checking early: a 15kW three-phase panel is cited as insufficient to run two tankless water heaters plus an induction cooktop simultaneously — see [[12_Engineering_and_Systems/analysis/Water_Heaters|Plumbing: Water Heaters]] for the recirculation-pump alternative this drives. [source: [[_Sources/YT_JrClDJb8WTM_cable_sizing_breaker_selection|JrClDJb8WTM_cable_sizing]]]

## Real Jobsite Routing Rules (added 2026-08-24, Round 2)

Konstantin Kruglov / Ontario, real 83 m² jobsite walkthrough, says:

**Floor-vs-ceiling routing decision, with a stated cost tradeoff**: route through the floor (cheaper) only if the screed can still cover the highest point of the run by at least 4cm; otherwise route through the ceiling — which costs roughly **20-30% more** than floor routing for the same job. Ceiling routing is also the default when the ceiling is suspended/false (not plastered) or purely by owner preference, independent of the screed-height constraint.

**Minimum clearance where electrical cabling crosses a water-supply pipe: 5cm, or a code-compliant sleeve.** Hitting both this 5cm clearance and the 4cm minimum screed cover at the same time is often not achievable in a normal floor buildup; when it isn't, the standard practice shown is to flag the shortfall to the client, get explicit informed sign-off to proceed with it (framed as a minor-severity violation), rather than growing the floor buildup to fix it.

**Conduit color/material code**: grey PVC ("ПВХ") conduit only for exposed/ceiling routing; brightly-colored conduit (black/orange/red, a different material — "ПНД") supports combustion and is safe only when fully embedded in poured floor screed — never use colored ПНД conduit on a ceiling run.

**Floor-routed corrugated conduit over acoustic underlayment must be tied to the underlayment's own mesh with cable ties, never nailed/stapled through it** — puncturing a "zero-impact-noise" underlayment defeats its function.

**Plaster the walls before marking/chasing electrical point locations, not the reverse** — real walls are out-of-plane; marking against the raw wall/slab produces visibly crooked sockets/switches once plaster (which adds real thickness) is applied afterward. Plastering first also means less of the actual load-bearing wall gets chased, since more of the channel depth is absorbed by the plaster layer. This is the wall-equivalent of this page's floor-screed-as-datum rule — reference the *finished* surface, not the substrate, for both. A design project's point coordinates are meant to be read against this same finished-floor/finished-wall reference — an electrician marking from the bare slab/wall, ignoring the not-yet-applied screed/plaster, produces misaligned results even from an otherwise-correct drawing.

**Chase deep enough that at least 0.5cm of plaster remains over the buried cable** — plaster only bonds/functions properly from about 0.5cm thickness upward.

**Corrugated conduit is only needed for the floor/ceiling run up to where it enters a wall — inside the wall itself, code-rated cable can be chased and buried without conduit**, since routing several conduited cables inside one wall would need an impractically large chase; this is standard, coded, and safe.

**Floor-embedded socket installation technique**: a floor socket's back-box is much larger/deeper than a standard wall box — before pouring screed, build a temporary foam/rigid-insulation block as disposable formwork in the exact spot/size the floor socket will occupy, remove it once the screed cures, then install the real socket into the resulting cavity.

**Real panel-group example with a concrete client-facing benefit**: main breaker → voltage-monitoring relay → RCBOs on wet-zone circuits → banks of shared RCDs (grouped A/B/C/D), each protecting several ordinary breakers rather than giving every circuit its own RCBO. Concrete payoff shown: a client can switch off just the socket group in a kids' room while the lighting circuit (a different group under a different breaker on the same or a different RCD) stays on — every breaker still keeps leakage protection via its shared RCD even though the breaker itself only covers short-circuit/overload. [source for this section, all items: [[_Sources/YT_gKBzDEllg4M_kruglov_best_wiring_a_to_z|gKBzDEllg4M_kruglov_best_wiring_a_to_z]]]

## Wet-Room Electrical Grounding — Equipotential Bonding (added 2026-08-24, Round 2)

Konstantin Kruglov / Ontario says: **an equipotential-bonding box (коробка уравнивания потенциалов) is a mandatory-by-code wet-room component, distinct from ordinary circuit grounding** — it bonds a room's metal fixtures (plumbing manifold/installation frame, a metal bathtub) to a common ground reference, protecting against stray/leakage current traveling through water or metal fixtures and shocking someone touching a fixture or standing in a metal tub. Low-cost to implement, mandatory to include. [source: [[_Sources/YT_gKBzDEllg4M_kruglov_best_wiring_a_to_z|gKBzDEllg4M_kruglov_best_wiring_a_to_z]]]

## Guiding Principles & Additional Planning Rules (added 2026-08-24, Round 2)

Konstantin Kruglov / Ontario states three governing principles behind this channel's electrical recommendations: **ПУЭ code compliance, convenience/functionality, and "ремонтопригодность" (repairability)** — any vulnerable connection should stay easy to access and fix later.

**Ceiling routing is specifically forbidden (not just discouraged) when the ceiling is a plastered/monolithic finish rather than a suspended one** — chasing into the floor slab above isn't permitted; ceiling routing is only viable under a false/suspended ceiling. **Ceiling-height-driven cost mechanism**: most sockets sit ~30cm above finished floor, so a floor-routed run to that height is shorter (cheaper) than a ceiling-routed run down ~2.7m from a 3m ceiling — at lower ceiling heights (example: 2.65m), floor routing is preferred partly just to avoid dropping the ceiling further. **A concrete case where ceiling routing is chosen anyway**: buying a "whitebox" apartment you like except for its electrical/wall finishes, and wanting to avoid demolishing the existing screed or heating risers — build a false ceiling (drop ~10cm) so all-new wiring can route through the ceiling instead of cutting into the existing floor.

**Panel "modes" — a second named mode beyond vacation/away**: a **"winter" mode** that disconnects air-conditioner circuits specifically to prevent an accidental cold-weather AC startup (which can damage the unit), in addition to the existing vacation-mode exception list (fridge, router, leak-protection, alarm stay live).

**Physical implementation alternative, corroborating the vacation/away-mode concept above (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, added 2026-08-28, Round 7)**: a dedicated "master switch" (мастер-выключатель) — an ordinary wall switch wired through a contactor — cuts all lighting (and optionally selected outlet circuits) with one press on the way out, while fridge/router/AC stay on the same always-on exception logic as the vacation-mode note. **Parts and cost**: switch + contactor + breaker, ≈3,000 RUB (≈$40) total. [source: [[_Sources/YT_3GvLuU2x7wU_sbk_master_switch|YT_3GvLuU2x7wU]]]

**Never use non-original/counterfeit breakers or RCDs to cut panel cost** — the correct lever is optimizing circuit grouping (e.g. combining WC + bathroom lighting onto one shared breaker), not downgrading device authenticity. **RCD+breaker combo vs. 3 separate RCBOs is roughly 3x cheaper** for equivalent protection (sharpens this page's existing shared-RCD-vs-RCBO cost note with a specific multiplier).

**⚠️ Electrical-point density benchmark, from the company's own 30-project design sample: ~0.85 electrical points per m²** (a "point" = any outlet, switch, dimmer, underfloor-heating thermostat, HDMI outlet, or low-voltage/network outlet). Worked example: a 50 m² apartment needs at least 42 points; more is fine, less is not recommended.

**Junction boxes are obsolete in modern rough-in practice** — splicing happens inside a deep back-box at the outlet/switch location itself, not in separate mid-run junction boxes. **Among reliable connector types, Wago spring-clamp connectors are specifically named as the only genuinely serviceable/repairable option.**

**LED-strip transformer placement: two valid options, decided by ease of future access, not aesthetics** — near each strip individually, or centralized in one location (e.g. a closet ceiling near the panel). Centralizing is explicitly favored for maintenance speed, since transformers fail relatively often.

**Smart-home setup sequencing, a 4-step algorithm**: (1) decide which specific devices you want (sockets, switches, smoke/motion/door-open sensors are the most common); (2) choose the hub/"brain" ecosystem before buying more devices; (3) install/wire/configure; (4) build automation scenarios last. Two connectivity methods: Wi-Fi or wired network cable. [source for this section, all items: [[_Sources/YT_8HnZ2m8vkZQ_kruglov_10_best_electrical_solutions|8HnZ2m8vkZQ_kruglov_10_best_electrical_solutions]]]

## Kitchen/Cooktop Rough-In Details and Floor-Routing Mesh Fix (Petrishin-Stroi, added 2026-08-24, Round 2)

Петришин-Строй (Sergey Petrishin), region level 2 (channel-level Moscow
association only, no city named in this source):

- **Built-in-appliance socket placement**: don't place an outlet directly
  behind a built-in kitchen appliance — put it left/right of the
  appliance, or lower in the (usually removable) plinth/kickplate area,
  so the appliance can sit flush against the wall.
- **Cooktop feed-cable length**: leave at least 1.5m of cable at a cooktop
  (`варочная панель`) location — cooktops are usually hard-wired directly
  rather than plugged in, and insufficient length forces a splice/re-solder
  later.
- **Floor-routed cable over an already-installed sound/waterproofing
  membrane — no clips**: secure the cable to a metal mesh (3mm wire,
  50×50mm cell) laid over the membrane using plastic zip ties, never by
  puncturing the membrane itself with clips/staples, which degrades its
  function — the same anti-puncture principle already on this page/
  [[12_Engineering_and_Systems/analysis/Rough_Electrical_Sequencing|Rough Electrical Sequencing]]
  (Zemskov's adhesive-clip rule, Sidorik's hot-glue-clip alternative
  above), applied here via a mesh instead of an adhesive clip.
- **Low-voltage transformer ceiling-avoidance rule**: never mount
  step-down transformers for low-voltage/LED-strip circuits inside the
  ceiling void — they fail more often there. Keep transformer access open;
  with many LED-strip circuits (correspondingly many transformers),
  consider routing them to a separate dedicated distribution point instead
  of scattering them through the ceiling.
- **Leak-sensor shutoff valve ("аквасторож") power-feed reminder**: if the
  apartment will have an automatic water-shutoff/leak-sensor unit, its
  power feed must be run at the rough-electrical stage — flagged as a
  commonly forgotten item.
[source: [[_Sources/YT_Q6GKMOJuaPc_petrishin_electrical_quality_checklist|Q6GKMOJuaPc]]]

## Routing, Documentation & Special Cases

**Route electrical conduit above plumbing runs on the ceiling, not stacked on the floor** — avoids compounding conduit-plus-pipe thickness inside the screed depth near door thresholds, a common cause of an unwanted raised threshold lip. Conduit should clear adjacent walls by 15 cm minimum (20-25 cm preferred). [source: [[_Sources/YT_12o621100MQ_electrical_point_coordinates_in_design_projects|12o621100MQ_electrical_p]]]

**Why "finished floor" specifically means the finished screed surface, and why screed must be poured before rough electrical**: most electric-point heights are referenced to the "zero mark" — the finished screed surface, not the sub-floor or waterproofing beneath it. Wiring before screed is poured risks the crew missing the true zero mark, a documented cause of misaligned outlets/switches above a kitchen backsplash or asymmetric bedroom fixtures. Re-verify room geometry before both screed *and* electrical rough-in — errors are cheap to fix before screed, expensive once electrical points are set against them. [source: [[_Sources/YT_12o621100MQ_electrical_point_coordinates_in_design_projects|12o621100MQ_electrical_p]]]

**Document electrical point coordinates consistently**: heights are measured from finished floor by default, except window-slope outlets (measured from the slope/sill) and ceiling-referenced points like an AC-alignment mark (measured from the ceiling). **A corner-labeling convention worth adopting**: rooms shown top-down, corners labeled alphabetically clockwise from top-left; a point's horizontal reference defaults to the nearest door/window opening or nearest labeled corner. The payoff is concrete — with this convention a client can independently verify any installed point in ~3-5 minutes with just a tape measure and the room's single sheet. [source: [[_Sources/YT_12o621100MQ_electrical_point_coordinates_in_design_projects|12o621100MQ_electrical_p]]]

**Never split a point's content description from its location marker into a separate reference table** — a real cited failure (a table-row mismatch) produced an as-built switch with two outlets specified instead of the intended content, discovered only after the client paid for rework out of pocket. Use a compact abbreviation legend instead (R = outlet, V = switch, ТВ = TV output, УТП = ethernet, leading digit for quantity) kept attached to the location marker. [source: [[_Sources/YT_12o621100MQ_electrical_point_coordinates_in_design_projects|12o621100MQ_electrical_p]]]

**On walls getting frame-mounted soundproofing against a neighbor's wall, add an extra electrical setback before applying standard offsets**: the soundproofing furring-out setback should be 10 cm plus the soundproofing layer's own thickness; from that face, standard offsets apply (15 cm from corner, 90 cm switch height). Electricians must be told about this before starting, or their box work ends up buried inside the eventual furring assembly. [source: [[_Sources/YT_12o621100MQ_electrical_point_coordinates_in_design_projects|12o621100MQ_electrical_p]]]

**A few narrower technique notes worth knowing**: sample only the ground conductor when checking an existing de-energized service-entry cable's gauge, to avoid disturbing live/neutral conductors unnecessarily; extend an undersized service cable with crimp ferrule sleeves and a heat-shrink gel splice kit, not an ad-hoc splice; when extending a high-load cable, use a fire-safety-rated splicing capsule specifically — an incorrect splice on a high-load cable risks overheating and fire; size a specialty appliance's power feed (e.g. a sauna heater) by that appliance's own installer's spec, not the general electrician's assumption; outlet/junction boxes must themselves be sound-rated wherever the surrounding wall has soundproofing, or a standard box lets sound through and defeats the wall; a dedicated non-switchable circuit for a router+camera, wired ahead of the panel's breakers, keeps remote surveillance working even when every breaker is off. [source: [[_Sources/YT_alnV3DYCDlg_extending_service_entry_cable|alnV3DYCDlg_extending_se]]]

## Perspectives: GOST vs. TU, and a Panel-Location/Gofra Nuance (added 2026-08-25, Sergey Kodolov)

- **⚠️ Perspective flagged, not applied to override the existing rule
  below**: this page's existing buying-guidance rule (line 155 below)
  says cable must be certified to ГОСТ, never merely ТУ. Sergey Kodolov
  offers a broader counter-perspective on GOST-vs-TU generally: GOST
  standards are revised very infrequently, while genuinely good new
  products are released under a manufacturer's own ТУ (technical
  specification) far more often — so a ТУ-certified product is not
  automatically inferior. He's speaking about consumer/building products
  broadly, not specifically about cable-insulation safety grade, so this
  doesn't necessarily contradict the narrower existing cable rule — but
  record it as a live perspective disagreement on how strictly to apply
  "GOST-only" as a general buying heuristic, not a resolved question.
- **Distribution-panel placement nuance for larger buildings**: the main
  panel doesn't have to sit in an apartment's entry closet — for a large
  house/multi-unit building, it can be placed mid-building in a dedicated
  small utility/patch room ("кроссовая"), from which wiring fans out more
  efficiently than routing everything back to one entry-point closet.
- **Gofra-type ceiling/floor split, added reasoning**: ПВХ (light,
  flexible, doesn't support combustion, easily damaged) is for ceiling/
  open indoor use; ПНД (combustible, but far more mechanically/moisture/
  chemically resistant) is for floor-under-screed use. This page's
  existing ПНД-for-floor rule was previously reasoned via mechanical
  durability alone — Kodolov adds that ПНД is specifically *not*
  recommended for ceiling runs because it's combustible, a distinct
  reason from ПВХ's ceiling-only use (which is about fragility, not fire).
[source: [[_Sources/YT_QfTqabNW1Lc_kodolov_electrical_rough_install|QfTqabNW1Lc_kodolov_electrical_rough_install]]]

## Real Materials/Cable Spec Worked Example (added 2026-08-24, Round 2)

Pavel Sidorik, real ~61 m² new-build apartment, first episode of a 2-3-part electrical mini-series:

- **Cable-type specification actually used**: socket/power circuits ВВГнг-LS 3×2.5; lighting circuits use ВВГнг-LS 3×1.5 (runs needing a 3rd conductor, e.g. two-way/pass-through switching) or ВВГнг-LS 2×1.5 (simple single-point switching). **Buying-guidance rule: cable must be certified to ГОСТ (state standard), never merely to ТУ (a manufacturer's own internal spec)** — a real, generalizable quality-shortcut red flag distinct from brand name.
- **Named panel components**: EKF-brand "Aeres" and "Proximo" series RCBOs, a voltage-monitoring relay, main incomer breaker, and standard breakers; a built-in "Proximo" 36-module panel enclosure; a separate built-in metal enclosure specifically for low-voltage/data cabling.
- **Back-box drilling technique**: use a **72mm hole saw for a 68mm back-box** (not 68mm) — the extra 4mm clearance lets the box be leveled/adjusted within the hole once set. **Tool choice depends on wall material**: a rotary hammer alone suffices for a soft block wall; solid concrete needs a heavier-duty drill, since a lighter drill's torque-limiting clutch will slip repeatedly on concrete. Groove (штроба) depth sized to fit two 2.5mm² cables side by side.
- **Developer-supplied electrical inventory, real example**: an exterior metal panel with breakers, of which only one was actually wired to anything (the rest decorative/for future circuits per the developer's own labeling); that one breaker fed a single outlet. Incoming service cable: 3-conductor, 10mm² stranded, plus a separate fiber-optic line, expected to need extending (crimped, not soldered) to reach the new panel location.
- Region unresolved for this specific episode (no location/currency named directly) — series-level Belarus attribution already established by this channel's other episodes. No pricing yet (deferred to a later episode). [source: [[_Sources/YT_9-NjgDLleOw_sidorik_electrical_ep6|9-NjgDLleOw_sidorik_electrical_ep6]]]

## Ceiling Wiring, Floor Routing, and a Floor-Routed-Cable Safety FAQ (added 2026-08-24, Round 2, ep.8)

Pavel Sidorik, same project (Belarus level 1 — direct statement that fiber-optic is run into every apartment "in Belarus," plus Minsk named for a tool-rental location):

- **Ceiling lighting-circuit cable-type rule**: 2-conductor (2×1.5) cable for fixtures with no ground terminal (most recessed/spot lights); 3-conductor (3×1.5) reserved for fixtures needing grounding. Standard wiring diagrams: single-pole switch breaks phase to a daisy-chain of fixtures; a two-pole switch for a central fixture splits phase into two independently-switched lines (extends to three-pole for three lines); two-pole pass-through/3-way switches for hallway/living-room shared control from multiple points.
- **Floor conduit under screed: ПНД (high-density polyethylene), never ПВХ** — ПНД doesn't deform underfoot and is meaningfully stronger; conduit color is cosmetic only. **Independently corroborates this page's existing conduit-material rule with an added, compatible mechanical-durability rationale** (previously explained via a combustion-safety distinction).
- **Fast conduit-clip fastening**: a powder-actuated (gas-cartridge) tool is fastest, rentable rather than requiring purchase; cost-per-shot claimed cheaper than a single dowel-nail (qualitative, no figure given). **Where this would puncture an underlying soundproofing membrane, use adhesive-mounted clips instead** — hot-glue-gun adhesive (tested against foam adhesive and sealant) was the most effective: strong, fast-setting, no drilling needed.
- **Long conduit-and-cable pull technique**: for a large job, pull ~100m of conduit + cable together outdoors using the conduit's own built-in steel fish-tape wire; a building's own long shared corridor is a viable substitute for going outside.
- **Network cable spec**: copper, FTP category 5e, shielded (EMI protection).
- **⚠️ A genuine, mechanism-based floor-routed-cable safety FAQ, addressing recurring skeptical viewer comments**: (1) floor-routed cable-in-conduit under screed is ПУЭ-compliant, not a violation, and preferred wherever screed thickness allows; (2) three concrete advantages over ceiling routing — no concealed junction boxes (all connections sit in back-boxes, accessible by removing a plate, unlike a junction box sealed behind drywall/stretch ceiling), shorter cable runs, and a fully freed ceiling (no boxing/dropping needed); (3) a failed embedded cable is not retrieved — a new cable is run and the old one left in place, exactly as with wall- or ceiling-embedded cable, both of which also need demolition to access; (4) **cable meltdown is "practically impossible" given four layers of overcurrent protection in series** — RCBO + apartment main incomer breaker, a separate corridor/riser main breaker, and a building-service-entrance disconnect+fuses — leaving a **connection/junction point, not the cable run itself**, as the one genuinely vulnerable spot, which is exactly why floor-routed cable's back-box-accessible junctions are a real safety/maintainability advantage. [source: [[_Sources/YT_7QuzCGvDG_w_sidorik_electrical_ep8|7QuzCGvDG_w_sidorik_electrical_ep8]]]

## Corrugated-Conduit Fire Behavior and a Self-Conducted Cable Burn Test (Петришин-Строй, added 2026-08-24, Round 11)

2018-vintage source, region unresolved, low promotional ratio:

- **Corrugated-conduit ("гофра") ignition risk clarified as low in
  practice**: a short circuit could theoretically ignite the conduit,
  but in practice the breaker trips first — actually igniting it needs a
  sustained overload of roughly 5 minutes *without* any breaker tripping,
  considered unlikely. Once genuinely burning, fire spreads faster
  through the conduit than through open cable. Black gofra was said to
  support combustion somewhat more than gray gofra, though the
  practitioner's own view (`single-account`, not lab-tested) is that this
  difference doesn't matter much once an apartment is already on fire.
- **Self-conducted comparison burn test, standard cable vs. this page's
  already-standard ВВГнг-LS spec**: the crew held an open flame to ~30cm
  segments of both. Standard cable's insulation failed and slid off the
  conductor after exposure; ВВГнг-LS kept its per-core insulation intact
  and the cable remained apparently functional afterward — the practical,
  hands-on reason (beyond this page's existing GOST-vs-TU buying rule)
  the company moved to ВВГнг-LS specifically, not merely GOST-certified
  cable in general.
[source: [[_Sources/YT_VqrXg-tDRO8_petrishin_plastering_electrical_secrets|YT_VqrXg-tDRO8]]]

## Real-World Circuit-Separation Failure Case, From a Third-Party Flip Teardown (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, added 2026-08-28, Round 7)

Vladimir Amelchenko, reacting to a third-party flipper's own renovation-reveal video, names a concrete real-world illustration of why this page's existing circuit-separation guidance matters in practice, not just in theory:

- **⚠️ Worked failure case: one undersized panel with no circuit separation** — all apartment lighting on a single breaker, no separate breaker for outlets by room, no dedicated breaker for the dishwasher. Named concrete consequence: when the dishwasher fails and trips the breaker it shares with unrelated outlets, everything on that shared breaker stops working — potentially half a kitchen's outlets — until the appliance is fixed or unplugged, not just the appliance's own circuit.
- **⚠️ Standard breaker installed in place of an RCD (УЗО), named safety consequence**: without an RCD, a fault current to a metal appliance casing does not trip protection before a person touching the casing completes the circuit through their body — named explicitly as a potentially lethal risk for a small child.

[source: [[_Sources/YT_jfjW3Jf4hEM_sbk_flipping_teardown|YT_jfjW3Jf4hEM]]]

## The panel itself — moved to its own page

See **[[12_Engineering_and_Systems/analysis/Electrical_Panel_Design_and_Assembly|The Electrical Panel — Device Logic, Sizing, Assembly and Acceptance]]**. This page keeps cable gauge and circuit design, routing rules, grounding, and the fire-behaviour and failure-case evidence.
