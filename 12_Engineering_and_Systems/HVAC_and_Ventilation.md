# HVAC & Ventilation

Overview of air conditioning (split systems), condensate drainage, fresh-air/ventilation strategy, and the sizing/buying decisions around them. Each section states the leading recommendation(s) and *why*, so you can form a view without clicking through — the linked `analysis/` page underneath has the full multi-source breakdown, every number, and every citation. Full source list in [[12_Engineering_and_Systems/analysis/HVAC_Source_Notes|Source Notes]].

## Key Concepts & Indoor Unit Placement

**The single most important distinction on this page**: a **ventilation shaft** (venshakhta, shared floor-to-roof, serves every apartment on that riser) must never be touched, damaged, or removed — doing so cuts airflow for every unit sharing the column, not just yours. A **plumbing cladding box** (zashivka, built around water/sewer risers) is a completely different structure and can often be rebuilt more compactly. Confusing the two is the kind of mistake that affects neighbors, not just your own apartment.

**Inverter is the right modern default over non-inverter** — it modulates compressor power smoothly instead of cycling fully on/off, avoiding the temperature swings and extra wear that come with cycling. For indoor-unit placement: don't blow cold air directly on occupants, leave clear space above/below for airflow, and keep it visually unobtrusive where a less prominent option exists.

→ **[[12_Engineering_and_Systems/analysis/AC_Key_Concepts_and_Placement|Full detail]]**

## AC Condensate Drainage

**A simple water trap isn't enough, and the reason is mechanistic, not just "better safe than sorry"**: a trap's water evaporates during any period the AC isn't running, loses its seal, and lets sewer odor/bacteria migrate back into the room. **A "dry trap" valve solves this properly** — a floating ball settles and blocks the opening once the reservoir evaporates, so there's no path back up the drain even after months of disuse. **Route condensate into the bathroom/WC, not out through the exterior facade** — venting outdoors on a modern building tends to cause icing and facade staining, and a dry-trap siphon (not an ordinary water trap) is what actually needs to sit at that connection.

→ **[[12_Engineering_and_Systems/analysis/AC_Condensate_Drainage|Full detail]]** (slope requirement, condensate-pump workaround)

## AC Sizing & Selection

**A workable rule of thumb: ~1 kW cooling per 10 m², plus a 20% buffer** — explicitly caveated as an averaged estimate, not a substitute for a real heat-load calculation, and pushed upward for sun exposure or open-plan spaces sharing airflow. **Budget and premium inverter units perform similarly on core cooling function** — what premium tiers actually buy is lower noise, more self-diagnostics, and finish options, not a meaningfully different cooling result, per one installer's own framing.

**A useful reality check on "AC budget" as a concept**: for the same apartment, holding cooling function constant, going from basic split units to a full ducted supply-and-exhaust system with integrated cooling spans roughly 5,000-50,000 RUB/m² — a bare price-per-m² figure is close to meaningless without knowing which approach was assumed.

→ **[[12_Engineering_and_Systems/analysis/AC_Sizing_and_Selection|Full detail]]** (warranty patterns, filtration expectations, the full cost-by-approach table)

## Fresh-Air Ventilation & Ducting

**Default to a wall-mounted breather unit unless there's a specific reason not to** — it handles most typical indoor air-quality needs at a fraction of a full system's cost; full ducted ventilation earns its premium mainly where windows genuinely can't be opened (a loud arterial road, for instance).

**Kitchen hoods run into the exact same shared-shaft ceiling as fresh-air ventilation, corroborated across 5 independent sources**: a hood vented into a shared shaft cannot move air faster than the shaft itself allows, regardless of the hood's own rated m³/h — oversizing the hood on an undersized duct just adds noise and risks draft reversal into a neighbor's line. See [[15_Appliances/Kitchen/analysis/Hood_Analysis|Kitchen Hood Analysis]] for the full breakdown.

**Supply-air ("приточка") ventilation must be designed by a specialized ventilation contractor, not a general contractor or designer** — the stated sequence has the general project marked only as a placeholder until the ventilation contractor visits and produces the real duct routing. **Duct cross-section trades noise against ceiling drop, and bigger isn't automatically quieter**: a duct needs to be thick, not just wide, to actually cut noise.

→ **[[12_Engineering_and_Systems/analysis/Fresh_Air_Ventilation_and_Ducting|Full detail]]** (window-reveal breather workaround, duct sizing/soundproofing specs, an ASR-uncertain hallway-concealment technique)

## Common Mistakes & Buying Guidance

**Three recurring mistakes, from an AC retailer's own stated experience**: undersizing capacity to save money (the unit then runs constantly and fails prematurely), poor indoor-unit placement, and buying equipment from one vendor while hiring an unrelated installer (murky warranty coverage when something goes wrong). **A broader, striking claim worth taking seriously**: AC reliability and lifespan are reported to be roughly 80% dependent on installation quality, not equipment quality — the real reason DIY installation based on online tutorials is discouraged.

**Buy in winter for the best price**, and if the outdoor unit needs a long refrigerant line run (e.g. facade-mount is prohibited, pushing it to a rear courtyard), get a model explicitly rated for that run length — an undersized unit risks compressor overheating.

→ **[[12_Engineering_and_Systems/analysis/HVAC_Common_Mistakes_and_Buying|Full detail]]**

## Source Notes

Traceability record moved to its own page — [[12_Engineering_and_Systems/analysis/HVAC_Source_Notes|Source Notes]]. Not reader content, kept off this page by design.

## Change Log

Editorial history moved to its own page — [[12_Engineering_and_Systems/analysis/HVAC_Change_Log|Change Log]]. Not reader content, kept off this page by design.
