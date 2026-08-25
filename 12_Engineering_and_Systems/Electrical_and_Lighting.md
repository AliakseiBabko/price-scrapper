# Electrical & Lighting

Overview of electrical planning and rough-in, cable/circuit/panel design, mounting-height standards, switches and controls, and lighting design. Each section states the leading recommendation(s) and *why*, so you can form a view without clicking through — the linked `analysis/` page underneath has the full multi-source breakdown, every number, and every citation.

> [!NOTE]
> Most of this page's technical detail comes from a single 29-video Zemstandart / Alexey Zemskov YouTube playlist (a Belarus/Russia-region renovation-design company channel used elsewhere in this project). **Because it's all one practitioner/channel, treat repeated claims as one consistent stated convention, not independent corroboration** — even where a number (e.g. the 90 cm switch height) repeats across several of the channel's own videos, it's still a single source. Cross-check against an applicable electrical code before treating any spacing/gauge/height figure as load-bearing. Earlier content (WITALT, Prolife Invest, BURO, Minsk World) predates that playlist. Full source list in [[12_Engineering_and_Systems/analysis/Electrical_Source_Notes|Source Notes]].

## Key Concepts & Planning

Alexey Zemskov / ZEMS recommends: **Plan furniture layout before finalizing socket placement** — a socket blocked by a bed headboard or cabinet is a common, avoidable mistake. **Four lighting categories, each with its own recommended color temperature**: main/task light (~4000K, neutral-white) and decorative/night light (~2700-3000K, warm) — and **night light belongs in hallways/WCs but never a bedroom**, since it disrupts sleep.

Alexey Zemskov / ZEMS recommends: **Electric-point layout via centerline referencing beats corner-only dimensioning for anything symmetric** — define a virtual centerline (e.g. centered on a future bed), then dimension every point from it. Bed-relative asymmetry (5cm off-center one side, 11cm the other) is far more visually noticeable than corner-relative precision, even when the corner numbers look cleaner on paper.

→ **[[12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning|Full detail]]** (rough-vs-finish distinction, technical-vs-decorative lighting budgets, future-proofing provisioning)

## Cable Sizing, Circuits & Panel Design

Alexey Zemskov / ZEMS gives **a cable-gauge-by-load table worth committing to memory**: 1.5mm² lighting, 2.5mm² sockets, 4mm² ovens, 6mm² cooktops — paired with breaker curve B for sockets (tolerates inrush current) and curve C for lighting/AC. **The reason a 16A breaker pairs with 2.5mm² cable rated to 20-25A isn't arbitrary** — the breaker is sized to trip well before the cable itself would begin to heat up under a fault, the actual safety mechanism behind the pairing.

Alexey Zemskov / ZEMS says **panel acceptance comes down to three checkable things**: every load isolable on its own circuit, every breaker labeled, and **selectivity** — a downstream fault should trip only the smallest relevant breaker, never the main incomer. **Test every outlet and switch, and verify point coordinates, immediately after rough wiring — not deferred to a pre-finish inspection.** A defect caught before plastering is fast to fix; the same defect caught at pre-finish is slow, painful, and expensive.

Alexey Zemskov / ZEMS explains **why screed has to go down before rough electrical**: most point heights are referenced to the finished screed surface (the "zero mark"), not the sub-floor. Wiring before screed risks the crew missing that reference entirely — a documented cause of misaligned outlets above a kitchen backsplash or asymmetric bedroom fixtures.

→ **[[12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design|Full detail]]** (point-documentation convention, soundproofing setback rule, splicing/extension technique)

## Mounting Heights & Positioning

Alexey Zemskov / ZEMS says **switch height is a fixed constant, not something to scale per-occupant** — a repeated on-camera demonstration across four people (150-185cm tall) found the resting hand-drop height essentially constant across adults. Default: **switches 90cm from floor, 15cm from the door-opening edge** (moving to 10cm was shown causing casing conflicts). Countertop outlets default to 110cm, shifting by the same delta as any non-standard countertop height. The one real exception: video-intercom monitors and thermostats should track eye level instead, since they're read visually, not operated by feel.

→ **[[12_Engineering_and_Systems/analysis/Mounting_Heights_and_Positioning|Full detail]]** (bedside-point formula)

## Rough Electrical: Sequencing & Common Pitfalls

Alexey Zemskov / ZEMS recommends **plastering masonry walls before chasing cable slots** — chasing into unplastered walls risks unanchored cable runs and typically forces the work into two messy phases instead of one. **Price rough electrical by floor area, not cable length** — length-based pricing is a known upselling vector ("turns out we needed more cable"), and a floor-area quote is much harder to inflate after work starts. **Never cut recessed panel niches into load-bearing concrete** — a structural code violation, not a style choice; use a surface-mounted panel instead.

→ **[[12_Engineering_and_Systems/analysis/Rough_Electrical_Sequencing|Full detail]]** (window-slope outlet gluing, soundproofing-membrane conduit-clip rule)

## Temporary / Construction-Stage Electrical

Alexey Zemskov / ZEMS describes **site power during renovation as using a deliberately simpler spec than finish wiring**: 2×2.5mm² ungrounded temporary vs. 3×1.5/2.5mm² grounded permanent — grounding is treated as unnecessary at this stage. **Retail extension cords are commonly undersized for job-site draw** (conductors as thin as 0.75mm² are cited) — build a proper 2.5mm² job-site extension instead.

→ **[[12_Engineering_and_Systems/analysis/Temporary_Construction_Electrical|Full detail]]** (a real same-practitioner tension on 0.75mm² wire worth reading before assuming it's simply "undersized")

## Switches & Controls

Alexey Zemskov / ZEMS recommends **a master cut-off switch near the entrance as a small, high-value addition** — one button shuts down all or most apartment lighting on the way out, instead of checking room by room. **Two-way switches are worth the modest cost, especially bedside**, and the same logic extends across a whole chain of adjoining rooms (entry → corridor → living room) so nobody has to backtrack to turn off a light in a room already left.

Alexey Zemskov / ZEMS recommends **keeping every toggle switch in the apartment on the same ON/OFF orientation** — a mixed-orientation install is a common, entirely avoidable annoyance, and **never position a switch inside a door's swing zone**, checked against the door's full opening arc.

→ **[[12_Engineering_and_Systems/analysis/Switches_and_Controls|Full detail]]** (duty/night-light circuit, dimmer-bulb compatibility, kitchen counter-zone outlet rule)

## Lighting Design

Alexey Zemskov / ZEMS says **a handful of well-placed, well-diffused fixtures usually beats installing far more than a space needs** — roughly 4 fixtures adequately light a ~30m² room in one cited example. **For bedrooms, perimeter spot lighting beats a central pendant over the bed** — a central overhead fixture creates glare when lying down looking up.

Alexey Zemskov / ZEMS presents **a detailed, live-demonstrated case against recessed spotlights specifically**: aggregate bulb-failure rate scales with fixture count (40 fixtures = 40× a single fixture's failure rate, not a comparable rate), narrow cones create uneven "bumpy wall" illumination on textured wallpaper, reclined glare is a real nuisance, and total cost (each fixture needs its own run plus a step-down transformer) can exceed a single premium chandelier for worse actual room fill. Worth weighing against the popularity of spotlight-heavy designs before defaulting to them.

→ **[[12_Engineering_and_Systems/analysis/Lighting_Design|Full detail]]** (ceiling light-source type comparison, the full 5-argument case with a real live bulb-failure count)

## Buying, Installation Quality, Hiring Red Flags & Cottage-Specific Content

Alexey Zemskov / ZEMS says **sourcing lighting fixtures directly from overseas factories cuts hardware cost roughly 2-3×** versus local resellers — a meaningful lever specifically for lighting, which carries high retail markup. **A hired electrician's tool kit is a real, checkable vetting signal**: no dust-extraction vacuum on the drill during wall-chasing is a red flag (means masonry dust is being spread through the unit's cavities); round, cleanly drilled socket holes indicate competence, hacked square holes don't.

Alexey Zemskov / ZEMS recommends **buying finish-stage devices about a week before installation, not months ahead** — and recount actual point needs room-by-room after rough-in, since kitchen counts especially shift once cabinetry is finalized.

→ **[[12_Engineering_and_Systems/analysis/Electrical_Buying_and_Hiring|Full detail]]** (cable-stripping tool rule, cottage-specific intercom/outdoor-cable content)

## Smart Home Systems

Sergey Kodolov gives a comprehensive smart-home explainer: **real
pricing tiers (a ≈10,000 RUB starter kit up to ≈500,000 RUB+ for a
full system, +3% wiring-only premium vs. +20-35% for a full smart
layer)**, system architecture (controller/sensors/actuators),
device-level notes (smart locks, curtain motorization above 3-3.5m
ceilings, leak/gas safety shutoffs), and house-specific additions
distinct from an apartment's own scope.

→ **[[12_Engineering_and_Systems/analysis/Smart_Home_Systems|Full detail]]** (pricing structure, cross-brand compatibility caution, safety-critical sensor case studies)

## Source Notes

Traceability record moved to its own page — [[12_Engineering_and_Systems/analysis/Electrical_Source_Notes|Source Notes]]. Not reader content, kept off this page by design.

## Change Log

Editorial history moved to its own page — [[12_Engineering_and_Systems/analysis/Electrical_Change_Log|Change Log]]. Not reader content, kept off this page by design.
