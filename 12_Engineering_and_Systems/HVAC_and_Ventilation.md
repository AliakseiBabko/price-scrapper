# HVAC & Ventilation

Covers air conditioning (split systems), condensate drainage, fresh-air/ventilation strategy, and the sizing/buying decisions around them. Format follows [[12_Engineering_and_Systems/_supporting/wiki_page_format|the shared engineering-systems page template]] — narrative sections first, a Quick Reference table at the end.

## 1. Key Concepts

- **Split-system AC** — the standard residential setup: an indoor unit (produces cold air, mounted in the room) and an outdoor unit (rejects heat, mounted on the facade/balcony), connected by pressurized refrigerant lines plus a condensate drain from the indoor unit.
- **Inverter vs. non-inverter (on/off) compressor** — a non-inverter unit cycles fully on and off to hold a target temperature; an inverter unit smoothly modulates compressor power instead, avoiding the on/off cycling. Inverter is the generally preferred modern default.
- **Fresh-air ventilation is a separate system from AC.** AC cools/recirculates existing room air; fresh-air ventilation (a wall-mounted "breather" unit, or a full ducted supply-and-exhaust system) brings in and filters outside air. Don't conflate the two when budgeting or planning — see §5.
- **Ventilation shaft vs. plumbing cladding — the single most important distinction on this page.** A **ventilation shaft** ("venshakhta," identifiable by its grille openings, typically ~60×40 cm) runs as one shared vertical column from the ground floor to the roof, serving every apartment stacked on that riser line — **it must never be touched, damaged, or removed**; doing so cuts ventilation airflow for every unit sharing the column, not just yours. A **plumbing cladding box** ("zashivka," built around water/sewer risers, sometimes oversized "for the developer's convenience") is a different structure entirely and can often be demolished and rebuilt more compactly to reclaim space. Confusing the two is the kind of mistake that affects neighbors, not just your own apartment. *(Source: a Minsk-based interior designer, see §7 Source Notes — not from the AC-specific source below.)*

## 2. Indoor Unit Placement Rules

Three rules, consistently given by an AC installation specialist:

1. **Don't blow cold air directly on occupants** — position the unit so it cools the room evenly instead of aiming a cold stream at where people actually sit/sleep.
2. **Leave clear space above and below the indoor unit** — it needs unobstructed airflow to draw in warm air and release cooled air; boxing it in tightly (e.g. inside a cabinet with no clearance) defeats this.
3. **Position it to be visually unobtrusive** — avoid the center of a wall or a spot that disrupts the room's sightlines/design where a less prominent option exists.

## 3. Condensate Drainage — Why a Simple Trap Isn't Enough

An AC indoor unit produces condensate that has to go somewhere, and the "obvious" options are both wrong:

- **Draining straight into a sewer stack** lets sewer odor and bacteria migrate back up into the room through the drain line.
- **A simple water trap** (P-trap style) seems like the fix, but during periods the AC isn't running, the trap's water **evaporates**, loses its seal, and the same backflow problem returns.

**The correct mechanism is a "dry trap" valve**: condensate flows into a small reservoir; rising water lifts a floating ball; once the water rises high enough, it overflows through a top port into the sewer connection (a standard ~32 mm pipe). When the AC sits idle and the reservoir water evaporates, the floating ball settles and blocks the opening — so there's no path for sewer gas/bacteria to travel back up the drain, even after months of disuse.

**Route AC condensate drainage into the bathroom/WC specifically, not out through the building's exterior facade** — a second source, corroborating the underlying mechanism above, states that venting condensate outdoors on a modern building tends to create real problems (icing, staining, facade-appearance issues) and recommends routing it into the bathroom's own drainage instead. **A dry-trap siphon is specifically required here, not an ordinary water-trap type** — an ordinary trap's water reservoir evaporates over a season the AC isn't used (e.g. winter), and once dry, sewer odor migrates back up through the AC's own drain tubing and spreads through the apartment via the indoor unit — the same seasonal-disuse failure mode described above, restated with the specific fix (route to bathroom + use a dry trap) rather than just the mechanism.

**Practical installation notes:**
- In-wall condensate and refrigerant lines should run at roughly a **2° slope** toward the sewer riser.
- **Photograph the routing during installation** — this meaningfully reduces the risk that later wall work (shelving, drilling) accidentally damages a hidden line.
- Where gravity drainage to a riser isn't feasible (e.g. the nearest riser is too far or wrong elevation), a **condensate pump** is the standard workaround, mounted inside/adjacent to the indoor unit housing.

## 4. Sizing & Selection

**Rough sizing rule of thumb** (explicitly caveated by the source as an *averaged* estimate, not a substitute for a real heat-load calculation): roughly **1 kW of cooling capacity per 10 m²** of room area, with the smallest commonly available unit size being 2 kW, plus a **~20% capacity buffer** as standard practice. Push capacity upward for rooms with strong sun exposure, extra heat-generating equipment, or rooms that share airflow with an adjoining open-plan space (e.g. a living-dining combo needs sizing for the combined area, not just its own footprint).

**Budget vs. premium tiers** (described functionally, not by brand — several sources on this topic are self-promotional retailer/installer channels, so specific brand endorsements are treated as commercial opinion, not neutral fact):
- Functional cooling performance and air filtration are reported as broadly similar between budget and premium inverter units.
- What premium tiers reportedly add: lower noise/sound pressure, more self-diagnostic and safety systems (more relevant to service technicians than day-to-day occupants), and design/finish options (color choices beyond plain white).
- Reported warranty pattern: mainstream mid/premium brands commonly carry ~5-year bundled warranties (equipment + installation) when bought and installed through the same vendor; the cheapest no-name tier may carry a shorter (e.g. 1-year) equipment warranty even when installation warranty stays the same length.
- One installer's own framing: "you're paying mostly for design and quiet operation at the top end, not a different cooling result" — recorded as that source's opinion, not verified independently.

**Why "AC budget" alone doesn't mean much without specifying the approach**: for the same 100 m² apartment, holding cooling function constant, one design studio gives a concrete illustration of just how wide the range is depending on *how* it's done, not just *what brand*:

| Approach | Total Cost (RUB) | Trade-off |
| :--- | :--- | :--- |
| Standard split-system units (budget/economy) | ≈200,000 | Visible indoor units, most affordable |
| Standard split-system units (good quality) | ≈500,000–700,000 | Visible indoor units, reliable |
| Concealed/ducted AC (same cooling function) | ≈1,000,000–3,000,000 | Hidden installation, same functional result |
| Full supply-and-exhaust ventilation with integrated cooling | ≈1,500,000–5,000,000 | Adds fresh-air ventilation on top of cooling |

That's roughly **5,000–50,000 RUB/m²** from this one system category alone — a source's own explicit illustration of why a bare "price per m²" figure is close to meaningless without knowing which of these was assumed. *(Secondary reference, single-source, 2026 — see [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_6Z7uH2_rXsw_buro_segment_pricing_2026|extraction note]] for the full context.)*

**Filtration**: basic units include a washable coarse mesh filter (rinse, dry, reinsert); some add antibacterial/ionic filter inserts. Worth an honest expectation-setting note from the same source: a user is unlikely to *consciously notice* any difference from the added filter — any benefit is framed as subtle/subjective at best, not a dramatic, perceptible change.

## 5. Fresh-Air Ventilation: Breathers vs. Full Mechanical Systems

A separate decision from AC sizing (see §1). One practitioner's framing, worth treating as a reasonable starting heuristic rather than settled fact:

- A **wall-mounted "breather" unit** (a local fresh-air intake/filter device) is reported to handle the majority of typical indoor air-quality needs at a fraction of the cost of a full system.
- **Full ducted supply-and-exhaust mechanical ventilation** is framed as worth the added cost mainly in specific situations — e.g. an apartment on a loud arterial road where windows realistically can't be opened for fresh air.
- The practical recommendation given: default to breathers unless there's a specific reason (noise, air quality, a strong personal preference) pushing toward a full system, since most people reportedly don't perceive a meaningful difference in day-to-day comfort.

### 5.1 Kitchen Extraction Hoods Share the Same Shaft-Capacity Ceiling

The same shared-shaft constraint that governs fresh-air ventilation (§5) applies just as strongly to a kitchen range hood set to extraction mode ("отвод") — a mechanism worth stating explicitly since it's easy to assume a hood's own motor rating determines its real performance. **This is now corroborated across 5 independent sources** (see the full writeup and per-source detail in [[03_Kitchen/Appliances/analysis/Hood_Analysis|Kitchen Hood Analysis]]):

- **A hood vented into a shared apartment-building ventilation shaft cannot move air faster than the shaft/duct itself allows**, regardless of the hood's own rated m³/h — the shaft, not the hood, is the actual bottleneck. This holds whether the hood is on or off.
- **Cited capacity figures vary and are not reconciled**: ~100–120 m³/h (one source's general figure) vs. a more precise, diameter-dependent formula from a second source (100mm duct ≈ 180 m³/h, 130mm ≈ 300 m³/h, 150mm ≈ 400 m³/h, with a recommended +~50% margin over the duct's own capacity when sizing a hood). Treat ~100–180 m³/h as the realistic range for a typical 100mm connection rather than trusting either figure alone, and verify the actual shaft/duct size directly.
- **An oversized hood on an undersized duct doesn't yield more airflow — it causes more noise and can force draft reversal ("опрокидывание тяги"), pushing air backward through the system**, potentially into a neighboring apartment's line. This is now independently corroborated by three unrelated professional sources (a furniture assembler, a repair-shop owner, and a ventilation installer).
- **No hood works without makeup air ("приток")** — if a kitchen has no dedicated fresh-air supply, a window needs cracking for real extraction to occur at all; independently stated by two unrelated sources.
- **Manufacturer-advertised hood capacity figures may be measured at no-load** (free airflow, no duct/filter resistance) and can overstate real installed performance — `single-account`, not yet corroborated by another source.
- **A regulatory claim exists but is explicitly unconfirmed for this project's own location.** Some Russian-language sources describe a Russian building-code restriction (SNiP) on hood-to-shaft connections, tied specifically to whether the apartment has gas equipment — but accounts vary in precision between sources, none name Belarus, and **the user has explicitly stated this cannot currently be confirmed to apply here and is a research item for later, not a settled rule.** See [[03_Kitchen/Appliances/analysis/Hood_Analysis|Kitchen Hood Analysis]] §6 for the full, hedged writeup — do not treat as applicable without independent verification.
- **The practical alternative in a constrained-venting apartment is recirculation mode** (carbon-filtered, air returned to the room) — functionally reliable regardless of shaft capacity, though it doesn't remove humidity and needs a periodic filter, which can be shorter-lived (days to weeks, depending on type/usage) than a generic "periodic replacement" might imply.
- **A tee-fitting-plus-check-valve setup can preserve natural kitchen ventilation alongside a ducted hood** — independently described by three unrelated sources (see full DIY detail in the linked analysis §9), useful engineering practice regardless of how the regulatory question above eventually resolves.

See [[03_Kitchen/Appliances/analysis/Hood_Analysis|Kitchen Hood Analysis]] for the full multi-source breakdown, including a direct conflict this raises with the kitchen's already-selected hood model.

## 5.2 Supply Ventilation Design & Ducting (added 2026-08-04)

`single-account`, one practitioner's stated standing rule — same corroboration caveat as elsewhere on this page.

- **Supply-air ("приточка") ventilation must be designed only by a specialized ventilation contractor**, never a general contractor, architect, or interior designer. Stated sequence: the general design project is completed first, marked only "supply," "supply+exhaust," or "ducted system" as a placeholder; the ventilation contractor then visits, measures, and produces the actual duct/routing design; the general project is updated to add the required electrical feed/breakers; boxing/drywall to conceal ducts is finalized last, after the ventilation design is locked. [source: `90_Archive/processed_sources/20260804_zemskov_premium_class_tips_71691249.txt`]
- **Round-section ducts are preferred over flat/rectangular for lower noise.** Flat ducts are reserved for minimizing ceiling drop specifically; a technique for avoiding a full-room ceiling drop while still using round ducts is to route the supply duct above the kitchen cabinets and box it behind a floor-to-ceiling kitchen facade, rather than dropping the whole room's ceiling to the duct's lowest point — cited as recovering roughly 12–15 cm of ceiling height. [source: `90_Archive/processed_sources/20260804_zemskov_premium_class_tips_71691249.txt`]
- **A breather can be vented through a window reveal/embrasure instead of an exterior wall**, as a workaround where facade penetrations are banned by the building — the intake/exhaust opening is cut into the window's reveal rather than the wall itself. [source: `90_Archive/processed_sources/20260804_what_is_this_60m2_contractor_control_f7ab173e.txt`]

## 6. Common Mistakes

Three recurring buyer/installer mistakes, from an AC retailer's own stated experience:

1. **Undersizing capacity to save money** — the unit then runs constantly at maximum output trying to keep up, and fails prematurely as a result.
2. **Poor indoor-unit placement** — installing it so it blows directly on occupants (see §2, rule 1).
3. **Buying equipment from one vendor and hiring an unrelated installer elsewhere** — when something goes wrong, it becomes difficult to establish whether the equipment or the installation is at fault, and warranty coverage gets murky. Buying and installing through the same company avoids this and typically comes with one bundled warranty.

A fourth, broader caution from the same source: **AC reliability and lifespan are reported to be roughly 80% dependent on installation quality**, not equipment quality — proper installation needs specialized tools (vacuum pumps, flaring tools, manometers/gauges) and training, which is the stated reason DIY installation based on online tutorials alone is discouraged.

**Interfloor exhaust duct/riser inspection (added 2026-08-04, `single-account`)**: before cosmetic work starts, verify the condition of interfloor ventilation ducts/risers and clamp security — if only the surrounding soundproofing (not the duct itself) is damaged, restore it properly rather than leaving it as found. **Replace developer-installed square sheet-metal exhaust ducts with round plastic ducting** to reclaim the cross-section/airflow the square ducts otherwise waste. [source: `90_Archive/processed_sources/20260804_never_take_this_from_masters_70m2_4b3c72b6.txt`]

## 7. Buying Guidance

- **Seasonal timing**: AC units are reported cheapest to buy in winter, when demand (and prices) are lowest.
- **Warranty structure**: buying equipment and installation as one package from a single vendor is the practical way to get a bundled warranty (see §6, mistake 3) — check whether a quoted warranty period covers both equipment and installation, or just one.
- **Long line-run installations**: apartments where the outdoor unit has to be mounted far from the indoor unit (e.g. a building that prohibits facade-mounted units for aesthetic reasons, pushing the outdoor unit to a rear/courtyard facade instead) need a model explicitly rated for the resulting longer refrigerant line run — an undersized-for-the-run-length unit risks compressor overheating and premature failure. Get the actual run length measured on-site before selecting a model; don't assume a standard model's rated maximum will cover a non-standard installation.

## 8. Quick Reference — Do's and Don'ts

### Do's

| Rule | Applies To | Reason | Source |
| :--- | :--- | :--- | :--- |
| Purchase AC and installation services together from one provider | All Rooms with AC | Preserves single-source warranty and clear fault attribution if something goes wrong | `90_Archive/processed_sources/20260727_budget_video_4b421350.txt`, `90_Archive/processed_sources/20260730_flatart_ac_installation_guide_6e8816fb.txt` |
| Build custom shallow cabinetry in front of protruding ventilation shafts | Kitchen | Blends structural duct protrusions seamlessly into countertop line | `90_Archive/processed_sources/20260727_renovation_tips_video_f23c504a.txt` |
| Paint internal ducted AC grilles in wall color instead of buying linear slot diffusers | Living Room, Bedrooms | Reduces ducted AC hardware costs while maintaining clean visual integration | `90_Archive/processed_sources/20260727_apartment_renovation_guide_360f4c7c.txt` |
| Route AC copper refrigerant lines and condensate drains during rough engineering stage | Living Room, Bedrooms | Conceals AC piping inside walls before plastering; split units are mounted after final wall finishes | `90_Archive/processed_sources/20260727_renovation_guide_mistakes_2_61e3a372.txt` |
| Follow the 3 indoor-unit placement rules (§2) and route drainage through a dry-trap valve (§3) | All Rooms with AC | Even cooling, unobstructed airflow, and reliable long-term condensate drainage without sewer backflow | `90_Archive/processed_sources/20260730_flatart_ac_installation_guide_6e8816fb.txt` |
| Size AC capacity using the ~1 kW/10 m² rule of thumb with a ~20% buffer, adjusted for sun/open-plan exposure | All Rooms with AC | Matches unit capacity to actual heat load; avoids the undersizing failure mode | `90_Archive/processed_sources/20260730_flatart_ac_installation_guide_6e8816fb.txt` |
| Default to a wall-mounted breather unit for fresh air unless there's a specific reason (e.g. a loud road) to install full ducted ventilation | Rooms needing fresh-air ventilation | Handles most air-quality needs at a fraction of a full system's cost | `90_Archive/processed_sources/20260730_prolife_invest_moscow_flipping_31c14c27.txt` |
| For a kitchen hood in a constrained-venting apartment, compare models on recirculation-mode filter cost/lifespan, not just extraction-mode m³/h rating | Kitchen | Extraction performance is capped by shared shaft capacity (~100-180 m³/h typical); recirculation mode works reliably regardless of shaft condition | `90_Archive/processed_sources/20260731_roman_che_kitchen_hood_guide_a89bb70d.txt` |
| Compare kitchen hoods by minimum-speed noise level, not maximum-speed spec | Kitchen | A hood runs on speed 1-2 the vast majority of the time; max-speed dB rankings can reverse at minimum speed | `90_Archive/processed_sources/20260731_hood_video_3_ec2042f3.txt` |
| Install a tee fitting with a separate check valve to preserve natural ventilation alongside a ducted kitchen hood | Kitchen | Prevents the hood's own exhaust from blowing back through a passive vent grille, and blocks shaft backdraft/odors from entering when idle | `90_Archive/processed_sources/20260731_hood_video_5_54ec0a93.txt`, `90_Archive/processed_sources/20260731_hood_video_7_a7501bb5.txt` |

### Don'ts

| Rule | Applies To | Risk | Source |
| :--- | :--- | :--- | :--- |
| Do not block natural ventilation shafts | Bathroom, WC, Kitchen | Causes mold growth and poor air quality | `90_Archive/processed_sources/20260727_vid1_transcript_d04723c5.txt` |
| Do not assume a kitchen hood's rated m³/h extraction figure is achievable in a standard apartment | Kitchen | Real throughput is capped by the shared ventilation shaft/duct (~100-180 m³/h typical for a standard 100mm connection), not the hood's own motor rating | `90_Archive/processed_sources/20260731_roman_che_kitchen_hood_guide_a89bb70d.txt`, `90_Archive/processed_sources/20260731_hood_video_3_ec2042f3.txt` |
| Do not oversize a kitchen hood beyond its duct's real capacity to chase "low noise + high power" | Kitchen | Can cause draft reversal ("опрокидывание тяги"), forcing air backward through the system instead of extracting more | `90_Archive/processed_sources/20260731_hood_video_6_f9450975.txt` |
| Do not touch, damage, or attempt to remove a ventilation shaft ("venshakhta") for any reason, including to reclaim space | Bathroom, WC, Kitchen, any shaft-adjacent wall | Cuts ventilation airflow for every apartment sharing that riser column, not just yours — distinct from a plumbing cladding box, which can be rebuilt | `90_Archive/processed_sources/20260731_doma_minska_severny_bereg_ep2_layout_3e31aa05.txt` |
| Do not drain AC condensate straight into a sewer stack or rely on a simple water trap | All Rooms with AC | Sewer odor/bacteria can migrate back into the room; a simple trap's water evaporates during idle periods and loses its seal | `90_Archive/processed_sources/20260730_flatart_ac_installation_guide_6e8816fb.txt` |
| Do not undersize AC capacity to save money | All Rooms with AC | Unit runs constantly at maximum output and fails prematurely | `90_Archive/processed_sources/20260730_flatart_ac_installation_guide_6e8816fb.txt` |
| Do not attempt AC installation without specialized tools (vacuum pumps, flaring tools, manometers) and training | All Rooms with AC | Installation quality accounts for ~80% of AC reliability; poor installation causes early failure | `90_Archive/processed_sources/20260730_flatart_ac_installation_guide_6e8816fb.txt` |
| Do not assume a standard AC model covers a non-standard, long refrigerant-line-run installation | Apartments with restricted outdoor-unit placement (e.g. facade-mount prohibited) | Undersized-for-run-length units risk compressor overheating and premature failure | `90_Archive/processed_sources/20260730_flatart_ac_installation_guide_6e8816fb.txt` |

## 9. Source Notes

- **AC design & installation guide** (FLATART, Minsk-associated, 2017 — technical content treated as durable, pricing treated as historical/not usable for current budgeting) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_H61xa8n2nTk_flatart_ac_installation_guide|full extraction note]].
- **Breathers vs. full ventilation** (Prolife Invest, Moscow, 2026) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_DsdLa87Acz4_prolife_invest_moscow_flipping|full extraction note]].
- **Ventilation shaft vs. plumbing cladding distinction** (Дома Минска Episode 2, designer interview, Minsk, 2026) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_QHl1YEHMfgE_doma_minska_severny_bereg_ep2_layout|full extraction note]].
- **Kitchen hood extraction vs. recirculation, shared-shaft capacity limits** (7 sources cross-referenced: Roman Che TV 2021, Мебель — это просто 4-part series 2019-2020, ЛенРемонт 2019, Argus 2024 — none region-specific) — full multi-source analysis and its direct conflict with the kitchen's selected hood model in [[03_Kitchen/Appliances/analysis/Hood_Analysis|Kitchen Hood Analysis]].
- Pre-existing Do's/Don'ts rows sourced from earlier archived transcripts — see individual table cells above for paths.
