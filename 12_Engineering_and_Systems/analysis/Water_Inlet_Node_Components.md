# Plumbing — Water-Inlet Node: Components & Filtration

Covers the mandatory-vs-optional component split at the water-inlet/collector node, the two-tier filtration decision, and the sequencing/tamper-vulnerability rules around the water meter. Part of [[12_Engineering_and_Systems/Plumbing_and_Waterproofing|Plumbing & Waterproofing]].

## Component Sequence and the Mandatory-vs-Optional Split

LAB-REMONT, Знакомые сантехники, Добродушный сантехник, and Стройплощадка × Будни сантехника describe: **Mandatory minimum**, corroborated across all sources that discuss this: main shutoff valve → coarse filter/"грязевик" → water meter → check valve (needed whenever the node feeds both hot and cold risers; can be omitted on a cold-only inlet). One source adds a specific rule for the single joint between the main shutoff valve and any leak-protection valve: **exactly one threaded joint should exist there**, and it should be the *only* threaded joint anywhere upstream of the main shutoff — everything from the riser to the shutoff should otherwise be welded/fused, matching the original riser material. The stated reason: everything downstream of the main shutoff is the resident's own responsibility and can be isolated by the resident alone; everything upstream requires calling the building's management company to shut down the whole riser — so an upstream leak is a much larger liability, and hidden threaded joints there are the classic failure point management companies and codes try to eliminate.

LAB-REMONT, Знакомые сантехники, and Zemstandart/Alexey Zemskov recommend: **Optional but genuinely recommended tier**: pressure reducer + manometer, fine filter, leak-protection system, water-hammer arrestor (see [[12_Engineering_and_Systems/analysis/Pressure_and_Water_Hammer|Pressure & Water Hammer]] and [[12_Engineering_and_Systems/analysis/Leak_Protection_Systems|Leak Protection]]). Add a UPS/battery backup for the leak-protection system specifically, since it's electrically powered and won't trigger during a power outage without one.

Знакомые сантехники and Стройплощадка × Будни сантехника note: **A coarse-filter mesh-size discrepancy exists across sources and isn't reconciled here**: one source states coarse filters "ship standard" with 800/500/300 micron screens; another states the code-correct pre-meter screen should specifically be 600 micron with a tamper-seal lug. These may describe different filter product classes rather than a true contradiction — treat 500 micron as a reasonable default and confirm the specific product's rating.

## Filtration — a Two-Tier, Not One-Tier, Decision

- **Coarse filter (грязевик)**, pre-meter: protects the water meter's impeller/vanes from mechanical debris (weld scale, sand, pipe scale) that would otherwise abrade the vanes and cause inaccurate metering over time. Mesh commonly 500 micron (also cited: 300, 600, 800 depending on source/product). [source: [[_Archive/processed_sources/20260731_plumbing_video_4_7f5e9a77.txt|20260731_plumbing_video_]]]
- **Fine filter**, post-meter, mesh commonly cited 5–110 micron across sources (treat as "roughly two orders of magnitude finer than the coarse filter," not one precise number): protects downstream ceramic-cartridge valves in modern single-lever and thermostatic mixers from fine abrasive particulate — many fixture manufacturers require this level of filtration to preserve their warranty. **Install it after the meter, never before** — a fine filter placed before the meter can, per one source, effectively divert water around metering when the filter is opened/flushed, which is both improper and adjacent to a genuine water-theft/tamper vulnerability (see below). [source: [[_Archive/processed_sources/20260731_plumbing_video_4_7f5e9a77.txt|20260731_plumbing_video_]]]
- **Self-flushing (самопромывные) fine filters, ~50–100 micron, are actively discouraged for residential use by one source** despite their marketing appeal: they need a manual flush roughly twice a year tied to a drain connection, and in practice residents rarely do it — the filter clogs silently, and the first symptom is a low-pressure complaint traced back to a forgotten, clogged filter. A standard, easily-swapped cartridge filter is recommended instead for most apartments; self-flushing filters are only argued to be worth it for larger units with 2+ bathrooms needing higher sustained throughput. [source: [[_Archive/processed_sources/20260731_plumbing_video_4_7f5e9a77.txt|20260731_plumbing_video_]]]
- **If water quality itself is suspect (not just particulate), get a water analysis and install a dedicated mainline filter housing** downstream, with cartridge type chosen per the analysis: polypropylene mechanical (5–10 micron), carbon/charcoal (chlorine taste/odor removal), ion-exchange (softening/anti-scale), or iron/manganese-removal (only if water runs visibly yellowish). **Combining a flush filter and a mainline filter on the same node is called "generally pointless"** — let the water analysis decide which single approach is needed, not both. [source: [[_Archive/processed_sources/20260731_plumbing_video_4_7f5e9a77.txt|20260731_plumbing_video_]]] Petrishin-Stroy corroborates and adds the concrete client-complaint trigger for each branch in practice: a softening cartridge gets added specifically when a client complains about hard water, an iron-removal cartridge specifically when the system shows elevated iron — add-ons are request-driven, not part of a default build. (added 2026-08-24, Round 7) [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_O_2Jji7NAHQ_petrishin_plumbing_cabinet_components|O_2Jji7NAHQ]]]
- **Plastic filter housings aren't recommended on higher-pressure systems**, except the "Big Blue" (BB) type rated to 7 or 15 bar — other plastic housings are fine only where pressure is genuinely low. [source: [[_Archive/processed_sources/20260731_plumbing_video_4_7f5e9a77.txt|20260731_plumbing_video_]]]
- **Don't oversize a filter housing "just in case."** Water sitting stagnant in an oversized bowl goes stale since it isn't circulating properly — match housing size to actual flow. [source: [[_Archive/processed_sources/20260731_plumbing_video_4_7f5e9a77.txt|20260731_plumbing_video_]]]
- **Route a drain valve under each filter housing to the sewage line**, so unscrewing a filter bowl to change its cartridge doesn't spill residual water — a reusable coarse-filter mesh can often be flushed clean directly through this drain valve under pressure, without disassembly. [source: [[_Archive/processed_sources/20260731_plumbing_video_4_7f5e9a77.txt|20260731_plumbing_video_]]]
- **A flush/rinse filter's own periodic waste-water drainage deserves a dedicated dry-trap connection** — these filters need flushing roughly every 6 months; routing that infrequent flush water through a temporary hose each time is awkward, and installing a small dedicated dry-trap-siphon drain is the more convenient, durable solution. Use a **dry-trap** type, not an ordinary water-trap siphon. [source: [[_Archive/processed_sources/20260731_plumbing_video_4_7f5e9a77.txt|20260731_plumbing_video_]]]

## Utility-Cabinet Rough-In Rules and Owner-Facing Labeling (Петришин-Строй, added 2026-08-24, Round 2)

Petrishin-Stroy, region level 2 (channel-level Moscow association only, no
city named this episode): the utility cabinet (`тех.шкаф`) housing the
manifold/collector assembly must be placed exactly where the design
project shows it — an offset placement leaves the whole assembly
misaligned behind the access hatch. Install a light fixture inside the
cabinet (working one-handed while holding a phone flashlight in the other
is explicitly the alternative being avoided). Waterproof the cabinet
interior — a frequent minor-leak location — to protect the surrounding
wall finish even though it doesn't prevent the leak itself. **Label every
piece of equipment at the node with a function sticker**, so the owner
can perform basic actions (isolating a branch, etc.) without calling a
professional for routine tasks. Petrishin-Stroy also requires **ventilation inside the cabinet, called
mandatory rather than optional, specifically to prevent mold/fungus** —
the cabinet's own elevated humidity (open water-bearing components) needs
active air exchange or moisture accumulates; and a **mandatory RCD/
differential-current breaker on the cabinet's own electrical outlet**,
framed as the floor-level minimum electrical protection if water reaches
the socket and grounds out. (added 2026-08-24, Round 7)
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_OgIZhrxD4v4_petrishin_plumbing_quality_checklist|OgIZhrxD4v4]]]

## Cabinet Back-Wall Waterproofing: Coating vs. Rigid Barrier by Substrate Condition, and a Small DIY Tool Fix (Петришин-Строй, added 2026-08-24, Round 7)

Petrishin-Stroy: **normally a waterproofing coating on the cabinet's back
wall is enough**, but on one secondary-market object the masonry riser
shaft behind the cabinet had old cracked brick, holes, and four disused/
abandoned pipes — judged too risky to coat directly, so an **aluminum
sheet was installed as a rigid physical barrier instead**. A concrete
substrate-condition decision rule (coating vs. rigid barrier), not a
universal recommendation to switch away from coating by default.
Separately: the pressure reducer's own adjustment cap uses a small key
not sold separately anywhere this source has found — **3D-printing a
replacement key shaped so it can't be set down and lost** (it stays
attached to/can't easily separate from the cap) solves a real recurring
small-tool-loss problem specific to this fitting. `region: level 2`.
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_O_2Jji7NAHQ_petrishin_plumbing_cabinet_components|O_2Jji7NAHQ]]]

## Manifold, Meter, and Reducer — Additional Rules (added 2026-08-24, Round 2)

Konstantin Kruglov / Ontario says: **the manifold ("коллекторная гребёнка") performs exactly two functions — pressure isolation (flushing a toilet shouldn't cause a scald risk for someone showering elsewhere) and serviceability (a single fixture can be isolated and repaired/replaced without shutting off the whole apartment's water). If a plumbing quote doesn't include a manifold, walk away — no modern layout is built without one.**

Konstantin Kruglov / Ontario says: **a pulse-output water meter transmits its readings automatically (e.g. to the management company), distinct from a standard non-pulse meter.** **Replacing a water meter requires inviting the management company (or ЖЭК) to reseal the new one** — this is management-company-overseen work, not a purely private plumbing decision.

Konstantin Kruglov / Ontario says: **a pressure reducer only ever reduces pressure — it cannot raise a low input pressure.** Beyond protecting fixtures from excess pressure, it's also framed as mitigating pipe noise/gurgling sometimes heard in older buildings' risers, and at very high pressure (6-10 atm) preventing a tap's stream from being uncomfortably "sliced" by excess force.

Konstantin Kruglov / Ontario, real Moscow jobsite, says: **riser soundproofing with clamps is cheap and worth doing** — wrapping/clamping ("хомуты") the shared riser pipe meaningfully reduces the risk of riser noise being audible in the living room. **A pressure reducer can legitimately be omitted at the apartment level if the building already has one at the entry/stairwell riser and the client doesn't want to duplicate it** — a real client decision: no in-unit reducer, since the building's own stairwell-level reducer already regulates supply pressure, even though an in-unit one "could have been added for convenience." **Installation-frame (инсталляция) anchoring**: bolt the frame rigidly to the structural floor slab, not the not-yet-poured screed, before screed is poured; use a chemical anchor specifically where the wall material is weak/aerated-block, since the frame bears substantial load. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_QcYJwQgu67g_kruglov_perfect_plumbing_mistakes|QcYJwQgu67g_kruglov_perfect_plumbing_mistakes]]]

Konstantin Kruglov / Ontario says: **an optional solenoid (electromagnetic) valve, distinct from a leak-protection system's automatic valve, can be wired to a simple switch for a one-button seasonal water-path switchover** — e.g. switching to a storage water heater during a scheduled hot-water outage, instead of manually operating multiple valves or a bypass. [source for this subsection: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_4jAQ526Zy2w_kruglov_perfect_manifold_unit|4jAQ526Zy2w_kruglov_perfect_manifold_unit]]]

## A Fuller Real Installation Sequence, With Named Component Specs (added 2026-08-24, Round 5)

Pavel Sidorik gives a real, granular inlet-node build order — consistent with, and one level more granular than, the "mandatory minimum" sequence above: **вводной кран (main shutoff) → защита от протечки (leak-protection valve) → грязевой фильтр (coarse filter) → счётчик воды (water meter) → самопромывной фильтр с манометром (self-flushing fine filter + gauge) → редуктор давления с манометром (pressure reducer + gauge) → обратный клапан (check valve) → коллектор (manifold) → гаситель гидроударов (water-hammer arrestor).**

- **Main shutoff valve**: never use it to partially throttle flow — only fully open or fully closed. Cracking it partway lets limescale build up on the internal ball and can seize the valve shut, leaving you unable to shut off water in an emergency. **Open and close it fully about once a month** to knock accumulated scale off the ball. A Neptun-brand automated leak-protection valve performs this same monthly cycle automatically.
- **Coarse filter (FAR)**: a concrete data point for this page's existing 300–800 micron mesh-size range — 300 micron, rated to 25 bar, installed with its cleanout access facing down so the mesh can be unscrewed and cleaned in place.
- **Self-flushing fine filter (FAR)**: 100 micron mesh, rated to 25 bar, rotatable body (mountable vertically or horizontally). **A specific mechanistic reason this filter sits *before* the pressure reducer rather than after**: it can withstand the full 25 atm line pressure — if it couldn't, it would have to move to *after* the reducer, which would then leave the reducer itself unprotected from waterborne debris. This is a distinct placement rule from this page's existing "install the fine filter after the meter, never before" rule (that one concerns pre-/post-meter placement to avoid a metering-bypass vulnerability; this one concerns pre-/post-reducer placement and is purely about protecting the reducer from debris).
- **Pressure reducer — static vs. dynamic operation is the key spec to check.** A genuinely important distinguishing feature beyond the general noise/high-pressure mitigation already noted above: **this reducer regulates pressure even with every tap fully closed (static), not only while water is actively flowing (dynamic)** — cheaper reducers work in dynamic mode only, meaning they provide *zero* protection from a static overpressure event. **Why this matters concretely**: a building's water system can be pressure-tested at elevated pressure, including at night, and a resident with only a dynamic-mode reducer would have no protection and would only discover a burst fitting after the fact.
- **Check valve**: backflow (hot water intruding a cold riser, or vice versa) is "not rare" in practice — cited causes include a failed/cheap mixer or simply a missing check valve where one belongs. Positioned after the reducer, before the hot/cold manifolds.
- **⚠️ A specific, named real-world instance of this backflow: a hygienic shower/bidet spray fixture pushing hot water into the cold-water manifold, surfacing as hot water at unrelated cold-only fixtures (dishwasher, kitchen sink, toilet tank/installation)** — stated to account for ~90% of cases of this symptom. **Fix**: check valves on *both* the hot and cold supply lines feeding the hygienic-shower fixture specifically, not elsewhere in the system. **Retrofit difficulty depends on distribution topology**: straightforward on a manifold system (cut into the two supply lines near the manifold); on a tee-branch system, the valve must go directly on the pipe feeding the shower, which is typically wall-concealed — retrofitting can require demolishing bathroom floor/tile to reach it. **Preventive rule**: install both check valves at initial installation time regardless of topology, as cheap insurance against a costly later retrofit. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_v-SdLOVwRS4_sbk_hot_water_in_toilet_tank|v-SdLOVwRS4]]]
- **Manifold — radial vs. tee distribution, with a concrete flow-balancing mechanism.** Radial ("лучевая") distribution through a manifold beats tee/branch ("тройниковая") distribution on every count considered: (1) serviceability — any single branch/valve can be isolated and swapped without affecting the rest; (2) fewer fittings end up embedded in the screed — just one fitting plus the wall outlet per branch, versus more branch fittings under a tee layout; (3) **per-branch flow balancing is the concrete mechanism behind avoiding the classic "shower runs cold/scalds when someone else flushes/runs another tap" complaint** — a manifold lets each branch's flow be individually tuned so drawing water elsewhere doesn't starve/surge the branch in use.
- **Water-hammer arrestor**: ideally one per mixer, but a single shared arrestor at the end of a manifold-fed branch group works fine over short pipe runs (as done here for a bathroom+toilet manifold pair). **Mounting mistake to avoid**: mounting the arrestor on an extension fitting for installation convenience creates a stagnant water pocket where bacteria can grow — mount it directly instead, even if less convenient, or expect to redo the mounting later.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_Cj2U_wVlG-I_sidorik_plumbing_intro_node_errors|Cj2U_wVlG-I_sidorik_plumbing_intro_node_errors]]]

## Dry-Trap Retrofit for a Self-Flushing Filter's Drain (added 2026-08-24, Round 5)

**Current sanitary code requires a "dry break" (сухой разрыв) between a self-flushing filter's drain hose and the sewage line** — direct hose-to-sewage contact isn't compliant. The fix is a **dry trap (сухой сифон)**: an internal rubber flap opens under flowing water and reseals afterward, blocking sewage odor/backflow while still passing drain water through; a funnel (воронка) attached to the dry trap collects the drain hoses. **Real failure mode of the standard funnel setup**: a drain hose can pop out of the funnel under water pressure and flood the area. Pavel Sidorik's fix: insert a forked bracket ("рогатина") into the funnel, drilled with holes sized for the hoses, to hold them in place while preserving the dry-break air gap. Extends this page's existing "use a dry-trap type, not an ordinary water-trap siphon" guidance with a concrete named product and this hose-retention detail. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_N36scNqRwII_sidorik_water_heater_installation_errors|N36scNqRwII_sidorik_water_heater_installation_errors]]]

## Metering/Tamper FAQ — Why Specific Restrictions Exist (added 2026-08-24, Round 5)

Pavel Sidorik answers viewer questions from a prior episode with concrete mechanisms behind rules already on this page:

- **Why the coarse filter can't be used to bypass the meter**: the coarse filter and the water meter are sealed together (пломбируются вместе) — you can't unscrew the filter without breaking the shared tamper seal.
- **Why a pressure reducer can't go before the meter, even though a viewer called it "a good idea"**: the local water utility (водоканал) permits only the main shutoff valve and the sealed coarse-filter/meter pair before the meter — nothing else, including a reducer — specifically because a reducer has a detachable gauge/union fitting ("американка") that could be removed to draw unmetered water. This reframes the page's existing "no union joints before the meter" rule as a code/utility-enforced restriction, not merely a best-practice choice.
- **Meter pressure-rating clarification**: a meter isn't limited to only 1.5 bar as some viewers assumed — it holds well above that because it already operates inside a developer-installed system running around 4 bar, and developers size meters accordingly.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_N36scNqRwII_sidorik_water_heater_installation_errors|N36scNqRwII_sidorik_water_heater_installation_errors]]]

## A Forgotten Leak-Protection Signal Cable, Caught Before Floor Finishing (added 2026-08-24, Round 5)

Pavel Sidorik, episode #27: the signal cable connecting the Neptun leak-protection inlet valves to the control unit was forgotten during the earlier plumbing stage and had to be retrofitted through the corridor screed before the finish floor went down. **Retrofit routing technique**: routed along the screed's perimeter, taking advantage of the 10mm perimeter damper-tape gap already in place from the screed build — only one corner needed chipping out, avoiding a fresh chase cut. **Cable spec**: two multi-strand 0.75mm² conductors, 12V signal, triggers the Neptun valves to close. Routed through corrugated conduit under the screed in the toilet, hidden behind a pipe with cable clamps in the technical cabinet, then through the screed via the toilet to the control unit; the chase was then patched over. A useful cautionary example of a genuinely easy-to-forget rough-in item (a low-voltage signal cable, easy to overlook next to the more visible plumbing components) and a low-disruption way to catch and fix it before the point of no return (floor finishing). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_kXGYTsBTKj8_sidorik_self_leveling_floor_ep27|kXGYTsBTKj8_sidorik_self_leveling_floor_ep27]]]

## Sequencing Rule Between Filters and the Water Meter, Plus a Metering-Bypass Warning

- **Correct code-referenced sequence**: a coarse/angled strainer *with a tamper-seal lug* installed before the meter, then a fine flush filter after the meter — matching the two-tier logic above, with the added detail that the pre-meter component should carry a tamper seal. [source: [[_Archive/processed_sources/20260731_plumbing_video_5_1992d0a4.txt|20260731_plumbing_video_]]]
- **A threaded union joint ("сгонная резьба") placed before the water meter is a specific, named vulnerability, distinct from ordinary joint-corrosion risk**: it lets someone unscrew the union and draw water bypassing the meter entirely — a metering-fraud/water-theft loophole, not a mechanical-failure concern. One source's own job site had exactly this developer shortcut (a union joint before the meter, with the tamper-seal lug and anti-magnet sticker both skipped) — explicitly flagged as improper: **there should be no union/threaded disassembly points at all before the meter, and everything before the meter should be tamper-sealed.** [source: [[_Archive/processed_sources/20260731_plumbing_video_5_1992d0a4.txt|20260731_plumbing_video_]]]
- **Threaded union joints ("сгон") anywhere on the riser side are separately called "a mine of delayed action"** — they corrode/degrade over time and are a classic unexpected-leak point, especially once concealed. On one job these were removed and converted to permanent welded joints specifically to eliminate this failure mode. [source: [[_Archive/processed_sources/20260731_plumbing_video_5_1992d0a4.txt|20260731_plumbing_video_]]]

## Pipe Insulation, Pressure-Spike Magnitude, and Two Placement Notes (Петришин-Строй, added 2026-08-24, Round 8)

- **"Энергофлекс" ("Energoflex") color-coded pipe insulation, a mechanism not previously recorded here**: blue sleeve on the cold-water pipe prevents condensation forming on the pipe from the temperature differential with the warmer cabinet air — without it, condensation leads to dampness/rust and shortens the life of other cabinet components; red sleeve on the hot-water pipe retains the pipe's own heat inside the insulation rather than radiating it into the cabinet, keeping the technical cabinet/bathroom from overheating.
- **Hydraulic-shock magnitude, a concrete figure**: normal central-system pressure runs 6-8 atm, reduced to a comfortable 3-4 atm by a pressure regulator for household use; during a hydraulic-shock event (tied to planned/unplanned water shutoffs and restorations) pressure in the central system can spike as high as **11 atm** without a regulator installed.
- **Fine-filter omission stated to void fixture manufacturer warranty**: per this source, expensive mixer/fixture manufacturers' own installation instructions and warranty documentation condition the warranty on a 100-micron fine filter being installed upstream. Company's own claim, not independently verified against a manufacturer document, but specific enough to record.
- **Coarse/"косой" filter's building-side placement, tied to meter installation**: this filter is installed *outside* the apartment, on the shared building landing/staircase, without a meter attached to it directly — and is a precondition water-utility installers require before they will install the apartment's own water meter (distinct from this page's existing in-cabinet, pre-meter framing of the coarse filter).
- **Check-valve backflow risk framed with an old-building-stock angle**: hot water pushing backward into the cold line (or vice versa) when line pressures differ enough to overwhelm a mixer's internal chamber is called most common in Stalin-era and Khrushchev-era buildings specifically — an age-of-building risk signal extending this page's existing general check-valve-backflow mechanism.
- **Dry-siphon consolidation of AC condensate and filter-flush drainage**: the AC unit's condensate line and the fine filter's periodic flush discharge are routed into a shared dry siphon before joining the sewage line, specifically to keep sewer gas/odor from venting back into the cabinet through either drain path — a routing detail distinct from the dry-trap retrofit above (which addresses only the filter-drain side).

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_D-DFsBMjlxQ_petrishin_faucets_plumbing_cabinet|D-DFsBMjlxQ_petrishin_faucets_plumbing_cabinet]]]

## Backward-Installed Meter as a QC/Handover Red Flag, and Maintenance Cadence (Петришин-Строй, added 2026-08-24, Round 7)

Petrishin-Stroy reports a real repeat callout where a water meter had been
installed **mechanically backward (counting in reverse)** despite already
being tamper-sealed — nobody had checked its flow-direction orientation
before sealing it. Consequence: an unusually low meter reading risks the
utility company suspecting deliberate tampering and issuing a fine, even
when the real cause was an installer's mistake, not fraud. **Add a meter-
direction check to any handover/acceptance checklist**, not just a visual
completeness check. Separately, the same source recommends a **routine
whole-node inspection every 4–6 months**: flush filters (consistent with
this page's existing self-flushing-filter cadence) and check specifically
for leaks at rubber-gasket/threaded-joint connection points on the
manifold and cabinet, not only at the filters themselves. `region: level
2 (channel-only Moscow association)`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_O_2Jji7NAHQ_petrishin_plumbing_cabinet_components|O_2Jji7NAHQ]]]

## Ceiling-to-Corridor-Cabinet Water Rerouting, and Heating-Manifold Consolidation (Петришин-Строй, added 2026-08-24, Round 11)

Real ~80m² new-build object, client Максим (likely the same evolving
project as this round's video-4 running-cost source, per that note's own
cross-reference). Region level 2. Low promotional ratio.

- **Water-supply rerouting from ceiling to a corridor utility cabinet**:
  hot/cold water originally routed under the apartment's ceiling was
  demolished and re-fed instead from the developer's shared corridor
  utility cabinet, tapping the existing heating-riser/water-supply
  penetration at height and dropping down into the unit — a real
  mid-project routing change, not the original plan.
- **Pipe-material upgrade during the same rerouting**: the original
  polypropylene pipes feeding the unit were removed and replaced with
  cross-linked polyethylene ("сшитый полиэтилен," PEX-A) piping.
- **Heating-manifold relocation and consolidation**: the heating
  manifold, previously in a separate location, was moved into the WC/
  bathroom utility area and consolidated alongside the water-supply
  distribution manifolds, pressure reducers, and filters — one
  coordinated utility-cabinet zone instead of two.
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_Tq2IELynaGs_petrishin_nonstandard_electrical_plumbing_pt4|YT_Tq2IELynaGs]]]

## Water-Hammer Compensator Placement — a Real, Openly-Unresolved Internal Dispute (Петришин-Строй, added 2026-08-24, Round 11)

**⚠️ A genuinely candid QC/self-correction case, invited for viewer
feedback rather than presented as settled.** Real object, город Видное
(region level 1). Standard utility-cabinet setup (Rehau PEX-A piping,
manifolds, pressure regulators, a backwash filter system, leak-
protection system, meters, fine filters) included a water-hammer
compensator ("гидрокомпенсатор") mounted on the fine filter — this
specific placement caused a real internal disagreement within the
company. They called the product's official dealer to ask, were told
this placement was incorrect, and redid the work to match the dealer's
own reference photo. The practitioner explicitly invites more
specialized viewers to weigh in with their own opinion in the comments —
a rare instance of a source presenting a real technical dispute as
still open rather than resolved with full confidence. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_QginFVl00Hw_petrishin_nonstandard_bathroom_panoramic_vidnoe|YT_QginFVl00Hw]]]

## Real Two-Bathroom Rough-In Walkthrough — Brand-Specific Filter/Reducer and Frame Details (Петришин-Строй, "ЖК Виноградный" episodic series, added 2026-08-24, Round 12)

Real object, region level 2 (named development, no city spoken), 2015-
vintage source (oldest processed on this channel to date). Low
promotional ratio. **Heavy overlap with the general inlet-node component
sequence already densely recorded above from five other sources
(main shutoff → coarse filter → leak-protection → meter → check valve →
fine filter/reducer → manifold), correctly not double-counted.**
Genuinely new brand-specific and mechanism detail:

- **⚠️ Fine-filter/reducer material distinction by water temperature,
  brand-named**: Honeywell fine filter + pressure reducer used on both
  hot and cold lines, but **the cold-water unit has a glass bowl housing
  while the manufacturer specifically recommends a metal (iron) housing
  for the hot-water unit** — a material/temperature-rating distinction
  not previously recorded here.
- **Leak-protection sensor, real trigger scenarios named directly**: an
  unattended running tap (e.g. answering a phone call), a child playing
  with a tap, or a sink overflow drain unable to keep pace with an open
  tap — any of these lets water rise past the sink's own overflow,
  triggering the under-sink sensor to cut both hot and cold supply
  completely.
- **Geberit installation-frame detail**: a wall-hung-toilet frame's
  mounting angle-bracket was pre-installed and fixed into the wall ahead
  of the frame itself, specifically for anchoring reliability — a
  distinct, earlier-stage anchoring detail from this page's existing
  Kruglov/Ontario chemical-anchor rule for installation frames.
- **Concealed-mixer hygienic-shower plumbing**: a concealed mixer valve
  blends hot/cold internally in the wall before the mixed water reaches
  the hygienic-shower outlet fixture.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_l4bXbwfOlrU_petrishin_vinogradny_ep7_plumbing|YT_l4bXbwfOlrU]]]

## Additional Component-Level Details (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, added 2026-08-28, Round 2)

Real finished-project inlet-node walkthrough; heavy overlap with the sections above, only genuinely new specifics kept:

- **Butterfly-type shutoff valves for light, low-torque operation** — contrasted against standard valves that stiffen/seize with mineral buildup over time, a real risk if a child or rushed adult needs to close one quickly during a leak.
- **FAR pressure reducers ship with an integrated adjustment key stored in the reducer's own cap** — cheaper models expose only a bare hex head requiring a separately-sourced hex key, avoiding a recurring small-tool-loss risk (compare the Round-7/Петришин-Строй note above about 3D-printing a replacement key for a different reducer that lacks this feature).
- **Water meters mounted at eye level specifically for easy visual reading.**
- **"Заяц" fitting as an alternative dry-break connection method** to the standard funnel-plus-dry-siphon setup, via threaded fittings and hoses — same underlying SanPiN air-gap requirement, different hardware.
- **Cold-water manifold built in two physical tiers since it serves more fixtures than the (single-tier) hot-water manifold.**
- **Check valves specifically flagged as commonly missing on hygienic-shower fixture connections.**

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_Zl_fegEg7yY_sbk_water_supply_manifold_install|YT_Zl_fegEg7yY]]]

## Further Component-Level Details, a Second Node Video From the Same Channel (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, added 2026-08-28, Round 5)

A second, later video from this same channel on the same general topic — real finished two-bathroom node walkthrough, checked directly against the Round 2 entry above before writing; heavy overlap confirmed, only genuinely new specifics kept:

- **⚠️ "Duplicating" shutoff valves added downstream of a developer's own existing riser valves, specifically to avoid re-welding/re-soldering the riser connection** — rather than replacing the developer's riser-mounted valve (which would require cutting into and refusing/re-soldering the riser pipe itself), an additional, better-quality, easy-operating shutoff is installed just downstream, leaving the original riser connection untouched entirely. Distinct from the butterfly-valve product recommendation above (Round 2) — this is about *where/how* to add a valve without invasive plumbing work, not which valve product to buy.
- **Manifold ("гребёнка") units include built-in thermometers as a standard component**, alongside the water-hammer compensators already documented on [[12_Engineering_and_Systems/analysis/Pressure_and_Water_Hammer|Pressure & Water Hammer]].
- **Purple low-tack painter's tape used as temporary layout marking directly on an aluminum manifold-cabinet panel during assembly**, to avoid marking the aluminum with pencil (which would need cleaning off afterward) — a minor real site-practice detail.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__U-FV_62gjM_sbk_water_supply_manifold_2|YT__U-FV_62gjM]]]
