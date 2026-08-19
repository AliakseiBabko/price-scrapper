# Plumbing & Waterproofing

Overview of water supply/drainage rough-in, pipe material, the water-inlet/collector node, water heaters, waterproofing, and leak protection. Each section states the leading recommendation(s) and *why*, so you can form a view without clicking through — the linked `analysis/` page underneath has the full multi-source breakdown, every number, and every citation. Room-specific application of this content lives on [[07_Bathroom/Bathroom_Guide|Bathroom Guide]] and [[08_WC/WC_Guide|WC Guide]] — this page is the infrastructure layer those pages cross-reference rather than repeat.

> [!NOTE]
> This page draws on a wide source base: several self-promotional Moscow/SPb renovation-company and plumbing-retailer channels, plus a Zemstandart/Alexey Zemskov general-tips playlist added 2026-08-04. Treat brand/product mentions as commercial, general technique as usable. Two genuine cross-source numeric disagreements (coarse-filter mesh size, water-hammer-compensator mechanism) are called out explicitly in their `analysis/` pages rather than silently merged. Full source list in [[12_Engineering_and_Systems/analysis/Plumbing_Source_Notes|Source Notes]].

## Rough-In Sequencing & Wet-Zone Placement

**Place the toilet first, as close to the riser as practical** — it needs the widest, hardest-to-conceal drain pipe (100mm), so everything else should be planned around its fixed position, not the reverse. Keep a relocated sink along a wall, not mid-room — the drain needs a consistent gravity slope to the riser, and a wall run can hide inside the wall without losing that slope; a mid-room sink needs much more screed depth to hide the same slope.

**A prefab plumbing cabin, if present, should almost always be demolished** — it reclaims real ceiling and wall space, and its lightweight panel walls are a poor tiling substrate compared to the structural wall underneath. **Never pour screed or tile over the floor area where the sewage stack penetrates down to the neighbor below** — that gap is a multi-floor leak's safest escape route; sealing it just traps a leak inside your own unit instead of letting it continue down.

Within a plumbing cladding box (zashivka), supply pipes can often be re-routed but the sewage stack generally can't be moved — don't assume "it's in a box, so it's all fair game."

→ **[[12_Engineering_and_Systems/analysis/Rough_Plumbing_Sequencing|Full detail]]** (wet-zone approval rules, zashivka audit technique, dry-fit warning, hot-left/cold-right convention, drain-bend rule)

## Fixture Stub-Out Coordinates (added 2026-08-18)

**A complete, mechanism-explained coordinate reference for where to place every rough-plumbing stub-out**, by fixture type — sink, shower, tub, toilet + hygienic shower, urinal, washing machine, and kitchen sink with/without an adjacent washer. Every rule specifies not just a height/offset but *why* — e.g. a toilet's hygienic-shower outlet sits 300mm right of centerline specifically so a right-handed user's wand hangs to their free (left) hand while washing, mirrored for a Muslim household's religious practice. **A recurring warning across every fixture**: never compress the standard spacing to save space — supply lines tolerate it, but drain lines at this diameter need the full spacing to keep a correct slope and avoid extra elbow bends.

→ **[[12_Engineering_and_Systems/analysis/Fixture_Stubout_Coordinates|Full detail]]** (full coordinate table by fixture, kitchen-with/without-washer layouts)

## Pipe Material Selection

**PEX is now used in ~95% of rough-in work, and the reason is structural, not fashion**: a PEX run from manifold to fixture is one continuous pipe with zero hidden joints — nothing buried under plaster/screed/tile that could fail invisibly. Polypropylene remains viable and cheaper, but its joints do get buried, a real tradeoff against PEX's price premium. Metal-plastic pipe is flagged as flatly obsolete by experienced installers.

**For the manifold node itself, stainless steel is worth the modest premium over PEX** — that node concentrates many device-to-device joints (unlike an open PEX run's two joints total), and the guiding principle across sources is that a system is only as strong as its weakest joint. Running stainless throughout the whole apartment, though, is considered unjustified overkill.

→ **[[12_Engineering_and_Systems/analysis/Pipe_Material_Selection|Full detail]]** (riser-to-shutoff special case, PEX press-fitting technique)

## Water-Inlet Node: Components & Filtration

**A mandatory baseline, corroborated across every source that discusses it**: main shutoff → coarse filter → water meter → check valve. **Everything upstream of the main shutoff is the management company's liability; everything downstream is yours** — which is why one source insists on exactly one threaded joint at that boundary and welded/fused connections everywhere else upstream: a hidden threaded joint there is the classic failure point codes try to eliminate.

Filtration is genuinely a two-tier decision, not one filter doing both jobs: a **coarse filter before the meter** protects the meter's own impeller from mechanical debris; a **fine filter after the meter** protects modern ceramic-cartridge mixer valves from fine particulate (many manufacturers require it for warranty). Installing a fine filter *before* the meter isn't just wrong sequencing — it can effectively divert water around metering, a real tamper vulnerability sources flag explicitly. **Self-flushing fine filters are actively discouraged** for a typical apartment: the twice-yearly manual flush they need rarely happens in practice, so they clog silently and the first symptom is an unexplained pressure drop.

→ **[[12_Engineering_and_Systems/analysis/Water_Inlet_Node_Components|Full detail]]** (mesh-size discrepancy, water-quality-driven mainline filtration, meter-bypass vulnerability)

## Pressure & Water Hammer

**Measure this apartment's own riser pressure directly — don't assume a figure from any source**, since cited riser pressures range from ~5 atm to 11 atm depending on building height and floor. Once measured, **a diaphragm/membrane pressure reducer is worth its premium over a cheaper piston type**: a piston reducer's output sags under simultaneous multi-fixture draw and tends to seize up in typical tap water, usually getting replaced with a diaphragm unit eventually anyway — piston-reducer savings are false economy over the system's lifetime, per two independent sources.

Check valves aren't optional: without one, a single-lever mixer left slightly open lets the higher-pressure line (usually hot) push backward into the lower-pressure line and from there into the **entire shared riser** — an affected apartment's neighbors can wake up to hot water from a cold tap, and metering gets corrupted on both sides. This risk didn't exist under old two-handle fittings; it became a hard requirement specifically once single-lever and thermostatic mixers became standard.

A water-hammer compensator addresses two genuinely different mechanisms (overnight thermal expansion on the cold line; valve-slam shock on any line) — no source can quantify exactly how much longer a system lasts with one installed, but a flexible braided-steel supply hose is repeatedly named as the single weakest, most commonly-failing point in home plumbing, and both mechanisms contribute to that failure.

→ **[[12_Engineering_and_Systems/analysis/Pressure_and_Water_Hammer|Full detail]]** (measurement method, flow-rate sizing, rated-pressure mismatches)

## Leak Protection

**A three-part system (motorized shutoff valve, control module, battery backup) is worth installing, and wired sensors beat wireless on every relevant metric** — a wireless sensor's battery can fail at exactly the worst moment with no advance warning. Sensor placement matters as much as the system itself: a floor-mounted sensor at the lowest point of each wet zone, plus dedicated sensors under the tub, washer, and sinks, triggers at just 1-2mm of standing water. **One easily-missed installation detail**: the control unit's own wireless uplink can't penetrate a metal manifold cabinet door — mount it behind plastic instead, or the whole system is silently disabled even though every sensor and valve are fine.

Buy one kit per riser pair, not per apartment — a second bathroom on a separate riser needs its own kit unless you consolidate both stub-outs to one collector point, a real cost/complexity tradeoff worth deciding deliberately rather than discovering later.

→ **[[12_Engineering_and_Systems/analysis/Leak_Protection_Systems|Full detail]]** (kit cost, common failure scenarios, false-trigger fix)

## Pressure Testing (Опрессовка)

**This is arguably the single highest-stakes QA step in the whole rough-in process** — a missed leak found later means removing screed and opening finished walls. A basic check at normal working pressure only catches gross assembly errors; **real verification means testing to 10 atm**, well above code's 4.5 atm minimum, because the lower figure often isn't enough to reveal a micro-crack or marginal joint. Demand this be done in front of you before accepting rough plumbing, and physically inspect the whole run after the hold regardless of what the gauge showed — a leak too small to register as a pressure drop can still saturate and delaminate screed over time.

→ **[[12_Engineering_and_Systems/analysis/Pressure_Testing|Full detail]]** (full procedure, tooling, what the test does and doesn't validate)

## Water Heaters: Tank vs. Tankless

**The real decision driver is your region's hot-water outage pattern, not a blanket preference** — a tankless heater is a good fit for a short, predictable scheduled outage (~10 days/year is a common cited figure), but "no tankless heater will save you" if outages run longer, where a tank heater becomes the only real fix. For a multi-person household, a tank heater is criticized as impractical regardless of outage length — the first shower depletes the stored hot water for everyone after. Tankless units need meaningfully more instantaneous power (380V/three-phase for genuinely hot, sustained output), so sizing has to be checked against the apartment's actual electrical allocation before committing.

**Provision for a tankless heater during rough-in even if you don't plan to install one** — one real account describes a client skipping it, then hitting an unexpectedly long outage with young children, forcing a retrofit that risked damaging already-finished tile. Cheaper to leave a spare branch off the manifold now than to retrofit later.

→ **[[12_Engineering_and_Systems/analysis/Water_Heaters|Full detail]]** (capacity sizing, placement-flexibility difference, recirculation-pump alternative)

## Waterproofing & Plastering

**Roll/membrane waterproofing under the screed, with an upturn onto the walls, has no exceptions** — it's what separates the screed from direct contact with walls and floor finish. Brush-on wall waterproofing becomes mandatory (not just recommended) specifically when using gypsum-based plaster, since gypsum must be protected from moisture — a real reason some companies brush-waterproof floor-to-ceiling on every bathroom wall even where code would technically exempt them.

**"Single-contour" waterproofing (applied after interior walls exist) is worth insisting on over "single-bowl" (applied to the whole shell before walls go up)** — the single-bowl method looks impressive on camera but has two real failure modes: a single pinhole leaks straight through to the unit below, and membrane installed before walls exist reliably gets punctured multiple times during wall construction. **Never waterproof over the area around a sewage/drain stack** — the same "leave the leak an escape route" logic as the screed rule above, and a mistake crews make out of over-caution often enough that four independent sources flag it explicitly.

→ **[[12_Engineering_and_Systems/analysis/Waterproofing_and_Plastering|Full detail]]** (gypsum-vs-cement tradeoff, membrane installation/QC technique, screed reinforcement rules)

## ⚠️ Relocating a Dry Room Under a Neighbor's Wet Zone (added 2026-08-19, remainder-pool batch)

**Relocating a bedroom (or any dry room) to sit directly below an upstairs neighbor's kitchen — not just a bathroom — carries a real water-damage risk, and should only be done under one of two conditions**: (1) the unit is on the top floor (no neighbor above at all), or (2) a confirmed guarantee has been obtained that the upstairs neighbor has completed full waterproofing on their own kitchen. A kitchen counts as a wet zone the same as a bathroom for this purpose — any layout change that ends up placing a dry room under a wet zone above carries real leak-risk exposure regardless of which specific fixture (sink, dishwasher) is above. `single-account`, `unverified`, but a genuinely important risk-disclosure point worth applying cautiously to any layout change involving room-swapping across floors, not just this project's own building. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_D8t1ADisUE8_odnushka_premium_replan_246|YT_D8t1ADisUE8]]]

## Shower Podium, Freestanding-Tub Drains & Slope

**A freestanding tub generally forces a floor-raise, and the deciding factor is distance to the stack** — one source's rule of thumb puts the cutoff around 5-6 meters, beyond which screed thickness alone can't provide enough drain slope. This is also why most shower installations use a raised podium instead of a flush floor: one source estimates ~95% of their own projects lack enough screed depth for a fully flush floor with a working drain. Weigh a freestanding tub's aesthetic appeal against this real plumbing consequence before committing to floor-buildup plans.

→ **[[12_Engineering_and_Systems/analysis/Shower_Podium_and_Drains|Full detail]]** (mitigation options, drain/trap type comparison)

## Hygienic Shower & Towel Warmer

**A hygienic shower's failure mode is specific and preventable**: leaving the upstream shutoff valve open after use (not just releasing the spray trigger) leaves the hose and mixer under sustained full line pressure — one source states it "100%" eventually fails and floods the unit if left this way for an extended period. A "vent-type" valve design fixes this at the hardware level, making it physically impossible to hang the nozzle back up without closing the shutoff first — worth choosing over relying on habit.

**For towel warmers, default to electric over hydronic** — not a style choice but a cost/risk comparison: a hydronic unit typically isn't covered by your leak-protection system at all (it sits downstream of that system's shutoff), carries a real stray-current corrosion risk from a neighboring unit's wiring fault, and costs more to install to begin with (~10,000-15,000 RUB vs. ~2,500 RUB for electric) despite electric's running cost being trivial (~10-15 RUB/month). One source's own building now goes door-to-door offering free hydronic disconnection — real evidence this isn't a hypothetical risk.

→ **[[12_Engineering_and_Systems/analysis/Hygienic_Shower_and_Towel_Warmer|Full detail]]** (correct usage sequence, hydronic bypass failure mode, pre-fit timing)

## Wall-Hung Toilet Installation

**Weight capacity is commonly underestimated** — even base-tier in-wall frames are rated to 200-250kg, reinforced versions to 400kg, and reinforced isn't significantly pricier, so it's worth defaulting to reinforced if there's any doubt. The one hard requirement: **the frame's feet must rest on a solid, monolithic concrete base only**, never tile or screed, or the installation degrades over time.

→ **[[12_Engineering_and_Systems/analysis/Wall_Hung_Toilet_Installation|Full detail]]** (repairability, a code-enforcement risk worth watching)

## Recovering Doorway Clearance Around a Riser Utility Box (added 2026-08-17)

A real project case (Zemskov/Zemstandart, `single-account`): a load-bearing wall on one side of a doorway and a hot/cold riser utility box on the other left only ~80cm clearance where ≥90cm was needed for a 60cm door (70cm rough opening + 2×10cm door-casing/baseboard returns). Two general-purpose rules recovered the missing ~10cm:

- **Don't hesitate to recess pipes slightly into a wall** — the riser was recessed ~5cm into a rebuilt utility-box wall, directly recovering clearance.
- **Don't hesitate to relocate a shutoff-valve access panel** if its position conflicts with a door swing or corner — move the valve onto a straight run of pipe and drop the access panel from the awkward position entirely, recovering both its own housing depth and the swing-clearance problem it caused.

[source: `11_Budget_and_Planning/_supporting/knowledge/sources/YT_IbV-DC3z8jI_riser_concealment_narrow_doorway_clearance_079.md`]

## Cost Drivers & Buying Guidance

**Price rough plumbing by fixture "points," not linear meters of pipe** — a sink needs 2 points (hot+cold); pricing by pipe length is a known vector for "turns out we needed more pipe" upselling after work starts, and a points-based quote cross-checked against the design's fixture count is much harder to inflate. A standard node runs roughly 3 hot + 5 cold points as a sanity-check baseline.

**Compare fixtures by full installed cost, not sticker price** — the visible price gap between a surface-mounted and built-in fixture is commonly much smaller than the real gap once pipework, fittings, sleeves, and labor are counted. And **never bypass main shutoff valves during modifications** — beyond the obvious flood risk, it crosses a real legal liability boundary: upstream of the main shutoff is the management company's responsibility, downstream is yours.

→ **[[12_Engineering_and_Systems/analysis/Cost_Drivers_and_Buying_Guidance|Full detail]]** (manifold cabinet code issues, multi-riser combining decision, recirculation-system cost)

## Source Notes

Traceability record moved to its own page — [[12_Engineering_and_Systems/analysis/Plumbing_Source_Notes|Source Notes]]. Not reader content, kept off this page by design.

## Change Log

Editorial history moved to its own page — [[12_Engineering_and_Systems/analysis/Plumbing_Change_Log|Change Log]]. Not reader content, kept off this page by design.
