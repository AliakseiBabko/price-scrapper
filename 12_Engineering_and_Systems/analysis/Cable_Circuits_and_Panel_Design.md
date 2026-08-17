# Electrical — Cable Sizing, Circuits & Panel Design

Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]].

## Cable Gauge, Breakers & Circuits

**Cable-gauge-by-load table (copper)**: 1.5 mm² for lighting circuits, 2.5 mm² for socket/outlet circuits, 4 mm² for ovens, 6 mm² for cooktops and other high-draw appliances. A 4–6 mm² high-load circuit should never be split or branched partway along its run.

**Breaker curve selection**: curve B for socket circuits (tolerates appliance inrush current without nuisance-tripping), curve C for lighting and AC circuits. Curve D is not recommended for residential use. Breaker amperage pairs to cable gauge: roughly 10A for 1.5 mm², 16A for 2.5 mm², 20A for 4 mm², 32A for 6 mm² (this practitioner's convention — verify against your local code before treating as a fixed rule).

**Why the breaker pairing works mechanistically**: a 2.5mm² cable can handle 20-25A continuously but is protected by a 16A breaker, so the breaker trips well before the cable itself would begin to heat up under a fault, given correct installation. The stated design target for rough electrical overall: survive at minimum 5 renovation cycles (at an estimated 5-7 years between renovations), implying a ~30-year minimum lifespan — cable/connection lifespan doesn't depend on user behavior the way a socket/switch's wear does.

**Panel circuit-count formula**: at least 2 circuits per room (one lighting, one sockets), plus 1 dedicated circuit for AC where present; oven and cooktop each get their own dedicated circuit; wet rooms (bathroom, WC, kitchen) require an RCD/differential breaker.

**Keep at least 15 cm separation between power cabling and low-voltage/signal cabling** — reduces electromagnetic interference. Note a real capacity constraint worth checking early: a 15kW three-phase panel is cited as insufficient to run two tankless water heaters plus an induction cooktop simultaneously — see [[12_Engineering_and_Systems/analysis/Water_Heaters|Plumbing: Water Heaters]] for the recirculation-pump alternative this drives.

## Panel Acceptance

**Three checkable "cornerstones" for accepting a finished panel**: (1) every eventual load is accounted for and split into separate circuits per room/function, so any area can be isolated independently; (2) every breaker is labeled/marked; (3) **selectivity** — breakers sized/coordinated so a downstream fault trips only the smallest relevant breaker, never the main incomer or the building's own riser breaker. **Test every outlet and switch before accepting rough electrical** — protects against a later trade puncturing a cable and the customer wrongly blaming the original electrician.

**Load-test the panel and verify every point's coordinates right after rough wiring finishes — not deferred to a later pre-finish inspection.** Catching a defective cable or misplaced point before plastering/tiling closes the wall is fast; catching it at pre-finish is slow, painful, and expensive. A supervisor who only checks point coordinates at pre-finish is a sign of inadequate on-site QC.

## Routing, Documentation & Special Cases

**Route electrical conduit above plumbing runs on the ceiling, not stacked on the floor** — avoids compounding conduit-plus-pipe thickness inside the screed depth near door thresholds, a common cause of an unwanted raised threshold lip. Conduit should clear adjacent walls by 15 cm minimum (20-25 cm preferred).

**Why "finished floor" specifically means the finished screed surface, and why screed must be poured before rough electrical**: most electric-point heights are referenced to the "zero mark" — the finished screed surface, not the sub-floor or waterproofing beneath it. Wiring before screed is poured risks the crew missing the true zero mark, a documented cause of misaligned outlets/switches above a kitchen backsplash or asymmetric bedroom fixtures. Re-verify room geometry before both screed *and* electrical rough-in — errors are cheap to fix before screed, expensive once electrical points are set against them.

**Document electrical point coordinates consistently**: heights are measured from finished floor by default, except window-slope outlets (measured from the slope/sill) and ceiling-referenced points like an AC-alignment mark (measured from the ceiling). **A corner-labeling convention worth adopting**: rooms shown top-down, corners labeled alphabetically clockwise from top-left; a point's horizontal reference defaults to the nearest door/window opening or nearest labeled corner. The payoff is concrete — with this convention a client can independently verify any installed point in ~3-5 minutes with just a tape measure and the room's single sheet.

**Never split a point's content description from its location marker into a separate reference table** — a real cited failure (a table-row mismatch) produced an as-built switch with two outlets specified instead of the intended content, discovered only after the client paid for rework out of pocket. Use a compact abbreviation legend instead (R = outlet, V = switch, ТВ = TV output, УТП = ethernet, leading digit for quantity) kept attached to the location marker.

**On walls getting frame-mounted soundproofing against a neighbor's wall, add an extra electrical setback before applying standard offsets**: the soundproofing furring-out setback should be 10 cm plus the soundproofing layer's own thickness; from that face, standard offsets apply (15 cm from corner, 90 cm switch height). Electricians must be told about this before starting, or their box work ends up buried inside the eventual furring assembly.

**A few narrower technique notes worth knowing**: sample only the ground conductor when checking an existing de-energized service-entry cable's gauge, to avoid disturbing live/neutral conductors unnecessarily; extend an undersized service cable with crimp ferrule sleeves and a heat-shrink gel splice kit, not an ad-hoc splice; when extending a high-load cable, use a fire-safety-rated splicing capsule specifically — an incorrect splice on a high-load cable risks overheating and fire; size a specialty appliance's power feed (e.g. a sauna heater) by that appliance's own installer's spec, not the general electrician's assumption; outlet/junction boxes must themselves be sound-rated wherever the surrounding wall has soundproofing, or a standard box lets sound through and defeats the wall; a dedicated non-switchable circuit for a router+camera, wired ahead of the panel's breakers, keeps remote surveillance working even when every breaker is off.
