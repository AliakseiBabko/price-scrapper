# Renovation Sequence

Airplane-view guide to renovation sequencing. For trade-off tables and the full 24-step turnkey workflow, see [[11_Budget_and_Planning/case_studies/schedule_analysis_case|Schedule Analysis Case Study]].

## General Order of Events

1. **Design and Layout Ideation** — floor plans, 2D plumbing/electrical/HVAC layouts, initial Bill of Materials.
2. **Demolition and Preparation** — dismantling old walls/floors/finishes, garbage removal.
3. **Rough Works & Structural Changes** — new partition walls, floor leveling, screed.
4. **Engineering and Utilities** — plumbing, electrical, HVAC routing.
5. **Finishing Preparation** — puttying/plastering walls flat, prepping floors.
6. **Finishing Works** — final flooring, wall paint/wallpaper, stretch ceilings.
7. **Installation of Fixtures & Doors** — interior doors, sockets/switches/lighting, sanitary ware.
8. **Furniture and Final Cleaning** — move-in, assembly, professional cleaning.

> [!CAUTION]
> **Don't rush the timeline.** Demanding an artificially fast schedule (e.g. "turnkey in 3 months" for a large project) forces contractors to charge premiums for weekend work and accelerated curing compounds. Let the sequence flow naturally.

## Sequence Depends on What You Choose

The order above is a default, not a fixed rule — several material and design choices change *when* specific steps must happen, sometimes irreversibly:

- **Hidden/concealed doors vs. standard doors** — concealed door frames must be installed during rough wall works, before plastering; standard overlay doors are installed last, after flooring and paint. Choosing hidden doors after rough works have already passed that point makes the concealed option impossible without redoing wall finishes.
- **Concealed vs. surface-mounted baseboards** — concealed baseboard channels need to go in before wall plastering; surface-mounted baseboards are a simple last step after furniture.
- **Large-format tile backsplash vs. standard tile** — large slabs (e.g. 3m runs) must be tiled *before* cabinet installation to leave maneuvering clearance; standard small tiles can go in after cabinets.
- **Drywall-frame vs. block/brick partition walls** — drywall framing allows utility routing inside the cavity before closing (zero wall chasing); block/brick walls require plastering first, then chasing grooves for cables/pipes after a 2–3 week drying wait.

Each of these trade-offs, with sources and full option tables, is documented in the [[11_Budget_and_Planning/case_studies/schedule_analysis_case|Schedule Analysis Case Study]] — decide on these choices *before* the relevant rough-works stage, not after.

## A Concrete Stated Build Order Within "Rough Works & Structural Changes" (added 2026-08-04)

One practitioner's own standing sequence for step 3-4 above, in more granular detail (`single-account`, corroborated across 3 videos from the same channel — see [[12_Engineering_and_Systems/analysis/Waterproofing_and_Plastering|Plumbing: Waterproofing & Plastering]] for the underlying waterproofing/screed technique): **plaster walls → clean off plaster drips → floor waterproofing (single continuous contour) → underfloor heating loop, if not central heating → re-verify room geometry → screed → only then rough electrical.** The stated reasoning: geometry errors are still cheap to fix before screed, but expensive once screed and electrical points are set against uncorrected reference points — and most electrical point heights are referenced to the finished screed surface (the "zero mark"), so wiring before screed risks the crew missing it (see [[12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design|Electrical: Cable, Circuits & Panel Design]]). A related safety-sequencing note from the same batch: before any floor demo/prep near developer-installed temporary heating, close the shared riser shutoff valve first, then open radiator bleed valves to confirm no residual pressure, and only then cut the heating loop — cutting pipes before confirming depressurization is flagged as a common, dangerous shortcut. [source: `_Archive/processed_sources/20260804_pre_screed_waterproofing_acceptance_5b57e2e4.txt`, `_Archive/processed_sources/20260804_floor_soundwaterproofing_technique_3021c8d1.txt`]

## Debris Volume — a Planning Sanity Check (added 2026-08-04)

**Rule of thumb: roughly 300 debris bags and 18–20 removal trips for a 100 m² apartment**, from demolition through rough-in — a useful sanity check when reviewing a contractor's debris-removal line item or planning dumpster/removal logistics. Debris pileup on-site is tolerated during demo/rough-in but should not still be accumulating once finishing work starts. `single-account`, `unverified`. [source: `_Archive/processed_sources/20260804_construction_debris_removal_volume_a83a6846.txt`]

## Flooring-Transition Planning: a Recurring Gap, Consolidated Here (added 2026-08-04)

This theme recurred independently across **4 of the 27 videos** in a single "general renovation tips" playlist batch — every source note that touched it flagged the same thing: this vault has no dedicated Flooring page, so the theme has nowhere clean to live. It's genuinely infrastructure (screed height is a whole-apartment planning constraint, not a per-room styling choice), so it's consolidated here as an interim home rather than left scattered across per-room source notes — **flagging explicitly that a dedicated Flooring page remains an open structural question**, not something decided unilaterally in this pass.

`single-account` throughout — one channel, several videos, not independent corroboration, though the repeated emphasis across otherwise-unrelated videos suggests the practitioner considers it a common, costly mistake worth repeating.

- **Multi-floor-covering screed-height planning must happen at project/design stage, not during construction or procurement.** Quartz-vinyl, engineered board, and porcelain tile all have different thicknesses (engineered board, in particular, is thicker than quartz-vinyl) — a technologist must calculate and document the required screed-height offsets in the project *before* work starts. Discovering the mismatch mid-renovation forces redone screed work. The same principle applies even within one material: e.g. porcelain tile over an underfloor-heating mat needs a different screed height than porcelain tile with no mat plus a tile-adhesive layer — both must be leveled to match, planned in advance. [sources: `_Archive/processed_sources/20260804_zemskov_premium_class_tips_71691249.txt`, `_Archive/processed_sources/20260804_business_class_five_attributes_19385e7a.txt`, `_Archive/processed_sources/20260804_what_is_this_60m2_contractor_control_f7ab173e.txt`]
- **Door-opening and outlet heights must be recalculated whenever screed height is deliberately varied** to compensate for flooring-thickness differences — flagged as a corollary commonly missed even by teams that get the screed differential itself right. [source: `_Archive/processed_sources/20260804_what_is_this_60m2_contractor_control_f7ab173e.txt`]
- **Do not patch a screed differential with self-leveling compound after the fact** — differences between porcelain tile and engineered board (with plywood underlayment) can reach 3–5 cm; self-leveling compound poured that thick will crack, is expensive at that thickness, and raises the finished floor enough to interfere with door clearances. Plan the differential into the screed itself, before flooring is chosen and ordered. [source: `_Archive/processed_sources/20260804_what_is_this_60m2_contractor_control_f7ab173e.txt`]
- **Plywood underlay for engineered board must never be glued onto self-leveling compound** — only onto sub-screed; a reputable installer will refuse or void warranty otherwise. **Engineered board must acclimate on-site** (temperature/humidity) before installation, longer than laminate needs — installing it fresh off a delivery truck is a defect risk. [source: `_Archive/processed_sources/20260804_zemskov_premium_class_tips_71691249.txt`]
- **Even where a full self-leveling-compound patch isn't the plan, deliberately plan a minimum ~1.5 cm screed-height differential between adjacent quartz-vinyl and tile zones**, even when not strictly required by material thickness — preserves flexibility to change the flooring plan later, since removing only 1–1.5 cm of cured screed isn't practical (the alternative, a flush level, forces full demolition of the tiled-zone screed if the plan changes). A shallow (~1 cm) threshold strip is a worse alternative to a deliberate differential: height differences under ~5 cm aren't reliably perceived visually, so a small lip becomes a stubbed-toe/trip hazard rather than a visible, expected step. [source: `_Archive/processed_sources/20260804_never_take_this_from_masters_70m2_4b3c72b6.txt`]
- **Minimize visible cut/trimmed pieces when one flooring material runs through irregularly-shaped connected rooms** — plan cuts to land inside closets or other hidden areas rather than visible traffic areas. [source: `_Archive/processed_sources/20260804_what_is_this_60m2_contractor_control_f7ab173e.txt`]

## Pre-Finish Stage Acceptance Checklist (added 2026-08-04)

A dedicated QC milestone between rough-in and finish work — walls plastered+sanded, tile laid, rough electrical wired and terminated, ready for wallpaper. `single-account`, `confirmed` as the speaker's stated practice, from a source describing ~250 renovation objects/year. [source: `_Archive/processed_sources/20260804_prefinish_stage_acceptance_d34c8e90.txt`]

- **Tile before wallpaper, not after** — tiling is one of the messiest trades, and tiling after wallpaper risks ruining the paper with tile-dust spray. If a skilled tiler isn't available in time and wallpaper must go up first, protect it with plastic film during tiling.
- **Wall-flatness inspection standard, Q1–Q4 tiers**: Q2 finish is sufficient for heavy vinyl or fleece (флизелин) wallpaper; Q3 is generally adequate for most finishes; Q4 (near-mirror flatness) is needed only for glossy paint, Venetian plaster, or silk-screen finishes, and costs meaningfully more (business/premium-segment pricing). Demanding Q4 for standard wallpaper is flagged as unnecessary over-spec — match the tier to the actual finish, not to a blanket "as flat as possible" instinct. *(A second source in the same batch corroborates Q3/Q4 as the business-class-typical range, framed from the contract/spec-verification side rather than the technical-tier side — see [[11_Budget_and_Planning/Budgeting_Guide|Budgeting Guide]] §4.)*
- **Grout timing is flexible**: grouting tile joints doesn't have to happen immediately after laying tile — recommended to do together with joint silicone sealing as one combined step, any time later. White grout left ungrouted for a while during ongoing renovation can discolor/darken in the meantime.
- **Wet-room electric points get one more check specifically at pre-finish**: confirm the tiler cut tile openings correctly for already-placed points (towel warmer cable, mirror-light cable, sink outlets, washer/dryer outlets) — the tiler has a diamond core bit and the homeowner typically doesn't, making this the one point-related check still worth doing this late (contrast with [[12_Engineering_and_Systems/analysis/Cable_Circuits_and_Panel_Design|Electrical: Cable, Circuits & Panel Design]]'s rule that point coordinates should otherwise be verified right after rough wiring, not deferred to pre-finish).
- **Kitchen tile backsplash prep**: if a wall will be tiled for a backsplash, leave that area un-primed (plastered only) — tile adhesive won't bond properly to a primed surface. Mark the area "don't prime" directly on the wall (sometimes twice) to prevent the mistake reaching the painting crew.
- **Self-leveling floor (наливной пол) check**: verify flatness with a straightedge across multiple planes before finish flooring goes down. An undetected defect surfaces later as unmatched seams or a creaking floor, requiring the finish flooring to be pulled up and redone.

## Replanning Approval, Pre-Demolition Packing, and Two Late-Stage Sequencing Rules (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, added 2026-08-28)

Vladimir Amelchenko's own 17-stage sequence checklist, low promotional
ratio. [source: [[_Sources/YT_dSZpq5Z9CEk_sbk_full_renovation_sequence_az|YT_dSZpq5Z9CEk]]]

- **⚠️ Replanning approval must happen before demolition/reconstruction work starts, not after** — many people take a finished design project straight into demolition, only to later discover the layout change may be unregistered, risking a fine and a forced reversal. **Named timeline caution**: the approval process itself varies by district — up to **2 months** in the speaker's own example — budget this as a real planning delay, not a formality alongside other early-stage work.
- **⚠️ Pre-demolition protective packing (windows, doors, elevator, mailboxes) as a default, not just damage-avoidance**: prevents an unresolvable liability dispute — a real worked scenario: an unprotected wall gets scratched, the crew and any delivery company both disclaim responsibility, and without a camera or packing in place the owner either fixes it personally or risks a management-company bill. Even with a camera clearly identifying the responsible party, recovering compensation still requires real effort (determining repair cost, matching the original developer finish) — packing by default is cheaper in time/money/stress than pursuing compensation after the fact, even when liability is provable.
- **⚠️ Finish-plumbing-after-ceiling sequencing rule**: finish electrical and stretch-ceiling installation happen before finish plumbing fixtures (faucets, sinks, glass shower partitions) — ceiling installers working afterward in the same room risk damaging already-installed glass/fixtures.
- **⚠️ Post-furniture wall-defect check ("дефектовка")**: after kitchen/built-in furniture installation (painted-wall, classic-design projects specifically), the crew checks all walls for chips/scratches caused by the furniture installers' own work and corrects them before considering the project complete.
- **Corroborates this page's existing debris-volume note**: debris removal is explicitly named as an overlooked stage — real cost/time components include protective floor/elevator covering before hauling, the haul itself, and (without elevator access) manually carrying every load down plus cleaning the entire stairwell top to bottom.
- **Corroborates this page's existing partition-material-dependent build-order note, restated from the plastering-sequence angle**: drywall partitions get perimeter-plastered first, then built; aerated-block (газобетон) partitions are built first, then the entire perimeter plus new partitions are plastered together as one pass.

## Secondary-Apartment Rough-Stage Construction Techniques (Ontario/Nikita Kuznetsov, added 2026-08-28)

Several concrete construction techniques from a real secondary-apartment
("вторичка") rough-stage sequence walkthrough, `single-account`.
[source: [[_Sources/YT_nd5WfYyjelg_kruglov_rough_reno_stages_old_apartment|YT_nd5WfYyjelg]]]

- **Partition-wall build technique**: aerated/gas-block partitions are
  built up **row by row with a mandated drying wait between each row**
  (never poured/built in one day), on a CSP (cement-particle board)
  footing strip. Before wet construction starts, dry-stack a single test
  row along the entire planned layout to visually confirm room
  proportions and furniture clearances match intent, adjusting before
  committing. Metal embeds are primed against rust before being sealed
  in.
- **Selective 90° plastering rule**: reserve strict 90° corners for
  rooms where it functionally matters for cabinetry fit later (walk-in
  closet, kitchen, bathroom) — forcing 90° everywhere (e.g. a plain wall
  that will only carry curtains) is unnecessary and can be
  counterproductive. **Window-reveal-symmetry technique**: since a
  window unit is frequently installed slightly out of square relative to
  its rough opening, prioritize equal-width reveals on both sides of the
  window over strict wall perpendicularity at that specific wall —
  mismatched reveal widths are a more visible defect than a
  slightly-non-square wall, and also cause windowsill-fit problems.
- **Skip plastering behind frame-based soundproofing** — a wall segment
  that will be covered by a frame soundproofing system doesn't need
  plaster underneath at all, saving that material and labor cost.
- **A sharper reason behind this page's existing electrical-after-
  plastering rule, specific to panel buildings**: chasing cable grooves
  after plastering means the chase cuts mostly through the new plaster
  layer and only minimally into the structural panel wall — important
  because panel-building walls contain load-bearing rebar that cannot be
  cut.
- **Concealed/built-in fixture pre-purchase checklist for rough
  plumbing**: a hydronic towel warmer, any concealed/built-in mixers,
  and a hygienic-shower valve must all be purchased and on-site before
  rough plumbing is routed, since the installer embeds internal
  components at that stage; radiators intended for the heating layout
  are needed at the same stage.
- **Door/window purchase-lead-times**: entry door ≈1 month (install
  planned right after demolition or during rough works, wrapped/sealed
  through screed work); replacement windows ≈2 weeks (installed either
  right after demolition or after rough works complete — either timing
  is fine if protected).
- **⚠️ Stretch-ceiling installation order depends on ceiling type**: for
  a standard (non-shadow-gap) stretch ceiling, install the perimeter
  profile first, finish/paint/wallpaper the walls, and stretch the
  fabric membrane **last** — minimizes risk of ceiling installers
  damaging already-finished walls. **This reversed order is not possible
  for a shadow-gap/floating-profile ceiling**, since painting/papering
  cleanly around an already-installed shadow-gap profile isn't
  practical — a different sequencing is required for that ceiling type.
- **Kitchen backsplash tile timing/cost mechanism, extending this page's
  existing large-format-tile-specific backsplash note to *any*
  backsplash tile**: tiling the backsplash during the main tiling phase
  (using the kitchen design plan's own precise dimensions) is cheaper
  and more precise than tiling after cabinets are installed, which
  requires transporting tile off-site for cutting or an installer
  cutting awkwardly on-site.
- **Consolidated client-vs-contractor purchasing split**: contractor
  typically sources rough materials, tile adhesive/putty/primer/mesh,
  ceiling material, and finish flooring material; the client sources the
  entry door, windows, all concealed/built-in plumbing fixtures, the
  tile itself, and finish-stage plumbing/electrical fixtures.

## New-Build Rough-Stage QC Acceptance Checklist (Ontario/Nikita Kuznetsov, added 2026-08-28)

From a real, itemized new-build rough-renovation case (see the case
study linked from `Budgeting_Guide.md` §6). `single-account`. [source: [[_Sources/YT_suY0GGTOG9E_kruglov_rough_reno_new_build_case|YT_suY0GGTOG9E]]]

- **Partition acceptance**: check tilt/plumb with a laser level, confirm
  opening heights against the apartment's own reference "zero" mark, and
  confirm reinforcement mesh is present where required.
- **Plastering acceptance ("helicopter pass")**: run a straightedge
  diagonally across every plastered surface, re-checking near
  baseboards, ceiling lines, and openings — **and separately re-verify
  flatness with a laser even where the underlying partition was already
  confirmed straight**, since plastering crews set their own leveling
  beacons and can introduce a new tilt independent of the partition
  itself. Follow with a square-check at every corner meant to be 90°,
  and a laser-tape parallelism check on walls meant to stay parallel.
- **⚠️ Humidity/mold-prevention step after plastering**: crack windows
  for ventilation while plastering dries, and actively manage indoor
  humidity by season — in winter, use a dedicated dehumidifier machine,
  since natural apartment exhaust fans alone can't keep up and
  unmanaged humidity risks mold on walls/floors.
- **⚠️ Floor-soundproofing-membrane protection during plumbing/
  electrical rough-in**: secure pipes and floor-routed cable to a net
  laid over the soundproofing membrane using cable ties, rather than
  fastening directly through the membrane, to avoid puncturing its
  waterproofing/soundproofing function.
- **⚠️ Quantified plumbing pressure-test protocol**: pressurize the
  manifold node to **8 atmospheres**, hold for **30 minutes**, confirm no
  pressure drop, before accepting rough plumbing. Separately verify
  sewage slope with a laser level; 45° fittings throughout (not 90°
  bends) reduce flow resistance/clog risk. Confirm check valves on the
  hygienic-shower line and the heated-towel-warmer branch, a water-
  hammer arrestor on the manifold node, and a fine-particle filter
  (near-universal in current renovations).
- **⚠️ Mixed wired/wireless leak-sensor cost-optimization**: wired
  sensors at each individual water-point risk location (cheap, cabling
  is short there), a WiFi-based wireless sensor block for the radiator/
  heating-manifold zone specifically (avoids running sensor cable to a
  more awkward location) — an explicit budget-driven mixed-technology
  choice, not "wireless is simply better."
- **Electrical conduit (гофра) usage rule**: for ceiling-routed cable,
  conduit is used purely for mounting convenience (not a code
  requirement) — but once cable drops into a wall chase, conduit is
  removed, since adding it to an already-cut chase groove would require
  cutting an even wider channel, which panel-building walls (rebar-
  constrained) won't tolerate. Conduit is specifically recommended for
  low-voltage/Ethernet cable, in its own separate chase, to avoid
  electromagnetic interference from power lines.
- **Electrical panel/point handover documentation rule**: every
  rough-wiring drop must be labeled/signed by the electrician at
  handover, and the panel must be clearly labeled matching each breaker
  to its corresponding outlet/circuit.
- **⚠️ Named "vacation mode" wiring trick**: alongside the main
  incoming breaker, wire two circuits (leak-protection system, WiFi
  router, refrigerator) to bypass it entirely — a secondary master
  switch specific to vacation use: flipping off the main breaker before
  leaving still keeps these critical safety/convenience circuits
  powered.
- **Screed acceptance checklist**: laser-level check for consistent
  height everywhere, straightedge flatness check, confirm expansion/
  control joints are cut at every external corner and opening
  (crack-prevention), and confirm a perimeter damper strip is present.
- **A contractor-vetting question**: ask whether a contractor maintains
  documented technical process cards ("техкарты") for its own work and
  request to see them — a genuine signal of whether its quality process
  is systematized versus ad hoc.

## A Five-Macro-Stage Documentation/Preparatory/Completion Checklist (Kruglov/Ontario, added 2026-08-28)

An alternative organizing taxonomy — Documentation → Preparatory →
Rough → Finish → Completion — from a source that, unlike this
channel's other sequencing videos, gives comparable structured detail
to the *bookend* stages (before rough works start, and after the
visible work looks finished) rather than just the rough/finish middle.
`single-account`. [source: [[_Sources/YT_9tScer1xT_E_kruglov_all_stages_2025|YT_9tScer1xT_E]]]

- **Documentation-stage checklist**: layout plan and its feasibility/
  approval status; engineering plans (electrical, plumbing, sewage,
  low-voltage, ventilation/AC); a replanning project and/or design
  project if needed; a contractor-selection pass across five distinct
  specialist categories (main montage contractor, special-installation
  workers, door installers, AC installers, ventilation installers); and
  management-company paperwork (powers of attorney, signed technical
  conditions/regulations).
- **Preparatory-work checklist**, commonly neglected despite being
  genuinely time/effort-consuming: temporary site lighting/electricity;
  temporary water supply and sewage (a toilet and shower pan); assembling
  scaffolding/towers/tool-storage shelving; protectively covering
  windows/doors and, separately, elevators/common areas; and arranging a
  construction-debris container.
- **A specific stage-ordering detail**: demolition, then window
  replacement (entry door can go here too, but must be replaced before
  screed is poured), then partition erection and plastering.
- **A furniture/AC preliminary-measurement timing tip**: once walls are
  plastered, furniture makers and AC installers can start their own
  measurements and planning — even before the floor's "zero point" is
  fixed, since wall geometry is already sufficient for this purpose.
- **A deferred-wiring detail for drywall partitions**: walls that will
  later be built from drywall get only rough electrical stub-outs at
  the main rough-electrical stage — full routing is deferred until the
  drywall structure itself is actually built.
- **⚠️ Post-completion defect-discovery mechanism**: a cleaning crew
  brought in once major work is done routinely surfaces accumulated
  incidental damage from the whole install chain (scuffed floors from
  furniture movers, a dropped tool from an AC installer) — client and
  company jointly document and remediate these before calling the
  project finished.
- **⚠️ Remediation gets structurally harder the later it's found**: a
  wiring or wall-flatness fix mid-rough-works is trivial; the same
  class of fix once furniture, stretch ceilings, and finish fixtures
  are all installed can require calling a ceiling installer back to
  unhook a stretch-ceiling section just to access the problem —
  a concrete argument for catching defects earlier rather than at
  project's end.
- **A named handover-briefing checklist**: alongside the keys, walk
  through how the electrical panel/breaker labels work, how the water
  supply system works, how to operate the hygienic shower, and how to
  switch/operate a water heater (e.g. a tankless unit).

## A Second "All Stages" Video: New-Build/Secondary Demolition Comparison and Two Sharper Rationales (Ontario/Nikita Kuznetsov, added 2026-08-28)

This round's sibling "all stages" video (2024, older than the one
above) restated most of this page's existing content almost verbatim —
correctly identified as the round's thinnest source rather than forced
into a denser extraction — but contributed a few genuinely new or
sharper items. `single-account`. [source: [[_Sources/YT_lLuNbjNXjg0_kruglov_all_stages_2024|YT_lLuNbjNXjg0]]]

- **A concrete new-build-vs-secondary demolition-duration comparison**:
  a new-build unit with no existing partitions needs only its
  developer's temporary heating loop and a single course of blocks
  demolished — a one-day task; a secondary-market apartment on a 5th
  floor with no elevator can take demolition and debris removal **up to
  a full month**.
- **⚠️ A partition-substrate placement rule, distinct from this page's
  existing partition-material-dependent *plastering-order* note above**:
  block-based partitions (aerated concrete, foam block, tongue-and-
  groove gypsum block) mount directly on the floor slab; drywall-framed
  partitions mount on top of the screed instead.
- **A general (type-agnostic) rationale for electrical-after-
  plastering**, complementing this page's existing panel-building/
  rebar-specific version: before plastering, there are no accurate
  final dimensions yet to place outlets/switches correctly — a reason
  applicable regardless of building type.
- **⚠️ A finish-electrical-before-stretch-ceiling testing rationale**,
  distinct from this page's existing finish-plumbing-after-ceiling
  rule: finish electrical (outlets, switches) is installed and tested
  *before* the stretch ceiling goes in, specifically so a wiring problem
  is caught while still easy to access — a different specific claim
  from the fixture-damage-avoidance reasoning behind the existing rule.
- **A general (not ceiling-type-conditional) two-phase stretch-ceiling
  technique**: install the perimeter profile first, finish the walls,
  then stretch the membrane last — presented as a general best-practice
  option for any stretch ceiling, related to but distinct from this
  page's existing ceiling-type-conditional sequencing rule above.

## Wall-Flatness Defects: a Pre-Kitchen/Cabinetry Check Worth Planning For (added 2026-08-04)

A related, currently page-less topic worth a pointer here even though the full technique doesn't have a clean home: developer-delivered walls with several-centimeter depressions (up to 3–5 cm) are a common defect, not "free extra floor area" — an uneven wall should be checked and corrected before finalizing a kitchen or cabinetry layout, since off-the-shelf cabinet modules are standardized in multiples of 10 cm and won't fit a non-standard recessed segment. Three named failure modes exist for the wrong fix (thick gypsum plaster alone, cement-sand under gypsum finish, drywall-on-metal-stud-frame) versus one correct method (aerated-block infill, glued and mechanically dowel-anchored, leveled with plaster guide rails as one continuous plane with the surrounding wall). `single-account`. See the full technique in the source note — this vault has no general walls/plastering-technique page to hold it in full; check delivered walls for flatness during a pre-purchase or pre-renovation walkthrough, and budget the correction if found (see [[11_Budget_and_Planning/Budgeting_Guide|Budgeting Guide]] §4). [source: `_Archive/processed_sources/20260804_wall_depression_aerated_block_fix_a0b9ff14.txt`]
