# HVAC — Key Concepts & Indoor Unit Placement

Part of [[12_Engineering_and_Systems/HVAC_and_Ventilation|HVAC & Ventilation]].

## Key Concepts

FLATART VIDEOS / Yuri Kokichev describes **split-system AC** as the standard residential setup: an indoor unit (produces cold air, mounted in the room) and an outdoor unit (rejects heat, mounted on the facade/balcony), connected by pressurized refrigerant lines plus a condensate drain from the indoor unit.

FLATART VIDEOS / Yuri Kokichev explains **inverter vs. non-inverter (on/off) compressor** — a non-inverter unit cycles fully on and off to hold a target temperature; an inverter unit smoothly modulates compressor power instead, avoiding the on/off cycling. Inverter is the generally preferred modern default.

FLATART VIDEOS / Yuri Kokichev says **fresh-air ventilation is a separate system from AC, and budgeting them together is a common conflation to avoid.** AC cools/recirculates existing room air; fresh-air ventilation (a wall-mounted "breather" unit, or a full ducted supply-and-exhaust system) brings in and filters outside air — see [[12_Engineering_and_Systems/analysis/Fresh_Air_Ventilation_and_Ducting|Fresh-Air Ventilation & Ducting]].

Дома Минска says **ventilation shaft vs. plumbing cladding is the single most important distinction in this whole system.** A **ventilation shaft** ("venshakhta," identifiable by its grille openings, typically ~60×40 cm) runs as one shared vertical column from the ground floor to the roof, serving every apartment stacked on that riser line — **it must never be touched, damaged, or removed**; doing so cuts ventilation airflow for every unit sharing the column, not just yours. A **plumbing cladding box** ("zashivka," built around water/sewer risers) is a different structure entirely and can often be demolished and rebuilt more compactly to reclaim space — see [[12_Engineering_and_Systems/analysis/Rough_Plumbing_Sequencing|Plumbing: Rough-In Sequencing & Wet-Zone Placement]]. Confusing the two is the kind of mistake that affects neighbors, not just your own apartment.

## Indoor Unit Device Taxonomy (added 2026-08-24, Round 4)

Konstantin Kruglov/Ontario gives a four-way taxonomy of devices that can fill a split system's
indoor-unit role, all wired to the same outdoor unit: (1) **standard wall-mounted unit**; (2)
**floor-ceiling/column unit** — a large freestanding column, mostly commercial/large-house use;
(3) **cassette unit** — ceiling-mounted, blows in four directions at once, common in
restaurants/offices/concert halls; flagged as "the bane of every office worker" since a shared
four-direction blow pattern in an open-plan space inevitably over-cools some occupants and
under-cools others; (4) **ducted/channel unit** — concealed above the ceiling, feeding several
rooms from one unit via ducting, with individually-controllable electronic dampers per room
(manual or smart-home-integrated). Ducted units need ceiling depth, condensate routing, and
access-panel planning, and are described as most common in higher-end, high-ceiling renovations
specifically because of that added design complexity. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_wsomY_6BRqA_kruglov_best_ac_2025|wsomY_6BRqA]]]

## Multi-Split: Hard Limit and Failure-Mode Downside (added 2026-08-24, Round 4)

**⚠️ A multi-split system (multiple indoor units on one shared outdoor unit) has a hard limit of 6
indoor units per outdoor unit.** Key downside vs. independent single split systems: if the shared
outdoor unit fails, every room it serves loses AC simultaneously during repair — an independent
split-system failure only takes out one room. A multi-split serving 2 rooms can cost *more* than
two fully independent split systems, despite serving the same room count. The one scenario that
forces multi-split regardless of this trade-off: the facade only has physical space for one
outdoor unit, but AC is needed in more than one room. `single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_wsomY_6BRqA_kruglov_best_ac_2025|wsomY_6BRqA]]]

## Portable/Mobile AC: Quantified Ineffectiveness (added 2026-08-24, Round 4)

**⚠️ A portable/mobile AC (no outdoor unit, exhaust vented via a window hose) is described as
barely effective** — roughly 4 hours to drop room temperature by just 1°C, compounded by the
window needing to stay cracked for the exhaust hose (which independently reduces any AC's
efficiency) and by real noise. The source frames the real-world benefit as closer to a "placebo
effect," with the only meaningfully cool spot directly in front of the unit's outlet.
`single-account`, `unverified`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_wsomY_6BRqA_kruglov_best_ac_2025|wsomY_6BRqA]]]

## Outdoor Unit Placement — Full Taxonomy (added 2026-08-24, Round 4, extends the single restriction below)

Konstantin Kruglov/Ontario gives four outdoor-unit placement scenarios, extending the single
"elite development bans exterior hardware" case already below: (1) **facade-mounted** — typical,
unrestricted secondary-market case; (2) **enclosed loggia box** — where facade mounting is banned,
an insulated enclosure built inside the loggia, vented to the exterior, functionally "outside"
while physically inside the loggia envelope; (3) **developer-designated shared per-floor zone** —
some new-builds provide one dedicated space per floor for every unit's outdoor hardware; (4)
**centralized rooftop system** — a developer installs one large shared outdoor unit on the roof
and every apartment connects to it, removing outdoor-placement choice entirely (cited example:
a Moscow-City-area development, name transcribed uncertainly as "ЖК Nivers в Сити" —
`ASR-uncertain`). `single-account`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_wsomY_6BRqA_kruglov_best_ac_2025|wsomY_6BRqA]]]

## Ventilated-Facade-Cavity Outdoor Unit Recessing, and Balcony-Placement Usability Tradeoff (added 2026-08-25)

Forcemontage (turnkey renovation company, real project, region unresolved) extends this page's existing outdoor-unit-placement taxonomy with two real-case items: **balcony placement is technically workable but makes the balcony unusably hot while the AC runs** — a real usability tradeoff distinct from the building-restriction/serviceability rationales already above. A real solved case for a facade with no pre-designed basket and a ban on standard facade mounting: the outdoor unit was **recessed into a ventilated-facade cavity**, mounted on brackets fixed to the building's own monolithic structural slab, saving the boxing space a standard surface mount would need, with a dedicated serviceable access hatch planned separately for maintenance. `single-account`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_7vjW6SzHeWM_forcemontage_ventilation_types_cost|7vjW6SzHeWM]]]

## Indoor Unit Placement Rules

Three rules, consistently given by an AC installation specialist:

Zemstandart/Alexey Zemskov recommends: 1. **Don't blow cold air directly on occupants** — position the unit so it cools the room evenly instead of aiming a cold stream at where people actually sit/sleep.
Zemstandart/Alexey Zemskov recommends: 2. **Leave clear space above and below the indoor unit** — it needs unobstructed airflow to draw in warm air and release cooled air; boxing it in tightly (e.g. inside a cabinet with no clearance) defeats this.
Zemstandart/Alexey Zemskov recommends: 3. **Position it to be visually unobtrusive** — avoid the center of a wall or a spot that disrupts the room's sightlines/design where a less prominent option exists.

Zemstandart / Alexey Zemskov reports **a fourth constraint, added 2026-08-18 — building-level exterior restrictions**: default to placing the indoor unit wherever the condensate drain and outdoor condenser unit can be routed to the building exterior, letting incoming air mix and reach the room comfortably. **But some developments (real example: an "elite" new-build) categorically prohibit any exterior condenser or condensate-drain hardware** — in that case, place the indoor unit above the entrance door instead (or anywhere else that avoids blowing directly onto a seating/sleeping occupant, per rule 1 above). Check the building's own rules before finalizing AC placement, not just the room-level rules above. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_wFUUakbL5O8_90_regrets_designer_renovation_233|extraction note]]]

## Outdoor-Unit Placement for Serviceability, and DIY/Hired Scope Split (added 2026-08-24, Sidorik Round 4)

Pavel Sidorik, individual practitioner, own apartment: mounted the outdoor condenser **directly below the bedroom window specifically so it can be serviced without hiring industrial rope-access climbers** — a serviceability-driven placement rationale distinct from this page's existing comfort/sightline/building-restriction rules above. **DIY-vs-hired scope boundary, a generalizable heuristic for a self-managed project**: wall-chasing (refrigerant-line and condensate chases) and electrical-feed routing are reasonable DIY scope; connecting/charging the refrigerant lines and outdoor-unit hookup are best left to hired specialists with proper tools — doing that specific part yourself is "not sensible" without them. Chase spec: 7cm wide × 4cm deep for the line-set chase; condensate-drain chase sloped 1cm per meter. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_C-3BcpXDRnk_sidorik_ventilation_ac_ep19|C-3BcpXDRnk]]]

## Kitchen-Specific AC Placement (added 2026-08-19)

> [!NOTE]
> The first kitchen-specific AC placement rule recorded for this store — the three general rules above were given for bedroom/living-room/kids-room contexts. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_fSEPr5fpfPM_kitchen_stubouts_ac_fridge_niche_166|note]]]

Zemsproekt / Zemstandart (Alexey Zemskov, with Sergey Saratov identified in the note) recommends **mounting over the entry doorway, never over a sofa (in a kitchen-living combo) and never over the cooking zone.** Reasoning by elimination across both alternatives: over a sofa in an open kitchen-living layout blows directly on whoever sits with their back to it while cooking; over the cooking zone conflicts with upper cabinets and blows on whoever sits on a nearby sofa. Over the doorway instead, the cold stream lands on open floor space, mixes with ambient warm air, and cools the room evenly with no one in the direct draft — independently the same doorway-placement outcome as the building-restriction fallback above, but reached here for a comfort reason specific to a kitchen's own layout, not an exterior-hardware restriction. **Coordinates**: centered on the vertical midpoint of the wall segment above the door (not flush to the ceiling — a named common installer mistake), centered horizontally on the doorway's own centerline (not the wall segment's centerline).
