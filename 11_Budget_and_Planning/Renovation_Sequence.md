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

## ⚠️ A Finished-Floor-Level Error Is a Rough-Stage Mistake That Only Appears at Fit-Out (Надежда Кузина, added 2026-09-01)

**The highest-consequence item routed in Round 5, and this vault had nothing on it.** [source: [[_Sources/YT_JOBm37_9iDg_kuzina_practical_vs_good_interior|JOBm37]]]

- **Stairs are the obvious case**: a poured or turning staircase is a difficult job, and **if the builders are not experienced or not expensive it may need re-pouring several times — because the FIRST and LAST tread must come out at the right height, which requires correctly calculating the finished floor level on each storey.**
- **⚠️ But the general case applies to a flat with no stairs at all: a miscalculated finished-floor height makes the interior inconvenient to use.**
- **⚠️ Her worked example is WC height — a pan set so high the user's feet do not comfortably reach the floor. "Ошибка там в 3–4 сантиметра реально делает интерьер адски неудобным."** *(Her illustrative magnitude, not a tolerance.)*
- **⚠️ And the diagnosis is the half that matters: it is NOT that the builders did not know the correct WC height above the floor. It is that the finished-floor height was calculated wrongly.**

> **An arithmetic error at rough stage, invisible until fit-out, and expensive to correct once the screed is down.** Check finished-floor levels against the fixture heights they will carry — not just against each other.

## ⚠️ Acceptance — a Room Can Be Beautifully Designed and Unusable (Надежда Кузина, added 2026-09-01)

Her worked example is a restaurant washroom she admired in detail: **plain small black tile, all the decor on the doors, frosted-glass inserts printed with samurai, and the glass appearing backlit though it was not — purely from correctly distributed ceiling light.**

**Beautiful right up until the latch would not engage its keeper, and she changed cubicle.**

**⚠️ Her point is about acceptance, and it belongs with the snagging stage: at the end of a renovation, do you accept work like that or not — and when something later breaks, do you fix it or decide everything is fine?** [source: [[_Sources/YT_JOBm37_9iDg_kuzina_practical_vs_good_interior|JOBm37]]]

## ⚠️ The Documentation Control for the Finished-Floor-Level Error (Татьяна Михайловская, added 2026-09-01)

**This page already records the highest-consequence rough-stage error found so far: a miscalculated finished-floor level, which makes fixtures unusable and is invisible until fit-out.** [source: [[_Sources/YT_MkssMwpyVsI_mikhailovskaya_design_project_composition|MkssMwpyVsI]]]

**A second, independent channel supplies the control for it — and it is simply documentation.**

**⚠️ Her worked project goes from a 2,800 mm ceiling height on the survey plan to 2,650 mm on the post-replanning plan, because the floor level rose after levelling — and she shows recording that change as normal practice, carried explicitly from one drawing to the next.**

> **The number that later governs every fixture height is written down rather than assumed.** Two independent channels: **one making the error visible, the other showing the practice that prevents it.**

**⚠️ And a related sequencing fact from the same round: the WC installation frame mounts on the CONCRETE floor, before the screed is poured and before tiling** — see [[12_Engineering_and_Systems/analysis/Wall_Hung_Toilet_Installation|Wall-Hung Toilet Installation]]. **So the WC type is fixed at planning stage, and it is fixed against the same finished-floor number.**

## ⚠️ Nine Steps Before the Builders Arrive — an Ordered Start-Up Plan (Татьяна Безверхая, added 2026-09-02)

Moscow designer, **uploaded 2026-08-22, the most recent source in this batch**; 11 years in the field, team credited with 200+ projects. `promotional_ratio: medium` — three own-studio insertions, but **she opens with an explicit disclaimer that the video is aimed at self-managers as much as at clients**, and most steps are given in both a DIY and a hire-it-out form. **This page already covers the on-site build order thoroughly; what it did not hold is the pre-site order.** [source: [[_Sources/YT_eHxsVHIus5Q_bezverkhaia_ten_step_sequence|eHxsVHIus5Q]]]

**⚠️ Her framing thesis: nine of the ten steps happen before any builder walks in.** The archetypal failure is a crew arriving and asking the owner "а делать-то что?" — she treats that question as the error itself. Do the nine, and "вы выдаёте ему список решений."

1. **⚠️ Key handover — do not economise on an acceptance inspector (приёмщик), because this is a one-time window.** It is the only moment defects can be forced back onto the developer. **With the inspector, and using a thermal imager**: that the windows are not losing heat, that frames are properly sealed, that there are no cracks or chips, that they do not leak. **She flags developer windows as a recurring problem on her own projects** — "для меня это такой вечный головняк." **For a whitebox, additionally**: wall flatness, wall geometry, filler quality, screed flatness. **Force remediation before starting.** Her candid note: you have waited a long time and want to begin, but skimping here costs far more later. **Complements this page's existing new-build rough-stage QC checklist by putting a step before it — the developer-handover check, not the crew's own rough-stage check.**
2. **⚠️ Measure, and establish the technical constraints — this second half is the substantive part and is easy to skip.**
   - **Ventilation**: in business/premium buildings there is typically **common-building supply ventilation** — establish where the outdoor units sit, **how air enters the apartment, and what the capacity is.** In budget buildings instead: **where the AC baskets are, how air conditioners may be positioned, whether breathers (бризеры) are permitted.**
   - **Obtain the БТИ plan and identify the wet zones on it** — that is what makes any later replanning possible or not.
   - **⚠️ In the old fund especially: the gas question, and the kilowatts allocated to the apartment. "Возможно, вам банально нужно докупать мощности, потому что текущих не хватит для современной техники."** **A purchasable constraint that has to be discovered before appliances are chosen** — and one this page's sequence did not name.
   - **⚠️ In the very old fund: whether the floor slabs below need reinforcement, where the building has timber slabs.**
3. **The layout solution — with a gate: do not move on until you have a layout you are actually in love with.** She advises against stock layouts except on a genuinely budget job.
4. **⚠️ Storage systems, deliberately a step of its own — with a number.** Storage is among the sharpest issues across all her clients. **Method: audit your actual possessions, work out how you are comfortable storing them, and build in a 20–25% margin above that.** **Two preferences: avoid free-standing wardrobes** (exception: a decorative vitrine acting as decor), **and prefer built-in storage, ideally consolidated into a separate dressing room.** **Read alongside Кузина's retrievability rule on [[17_Design_and_Ergonomics/analysis/Whole_Home_Planning_Method|Whole-Home Planning Method]] — hers is a volume margin, Кузина's is the reason volume alone is not capacity.**
5. **⚠️ Engineering before aesthetics — commission a dedicated engineering project** from a company that specialises in them, and **hire a crew with matching qualifications and permits (допуски).** Items to integrate at this stage in higher segments: ventilation, humidification, ionisation, smart-home and remote climate control.
6. **Only now, design and aesthetics.** **⚠️ Her rationale is the justification for the whole ordering: "красота без планировки, красота без инженерки, красота без технологий — она бесполезна."** She acknowledges the pull to start here and defers it to sixth.
7. **⚠️ Working documentation — and she gives a genuinely low-budget floor for it, which this page lacked.** With budget, a bureau produces it. **Without: use a homeowner-grade program (she names RemPlanner) to at least lay out tile and place sockets crudely — or literally print the layout and draw on it in pen.** **⚠️ The consequence of skipping it: "без планов, без развёрток, без точного технического задания для строителей ваш дальнейший ремонт превратится в аттракцион невиданной щедрости с вашей стороны, потому что вы будете бесконечно платить за переделки."**
8. **⚠️ Budgeting — the DIY method stated concretely.** Take Excel and **list everything in the apartment — porcelain, paint, curtains, radiators, fittings, sockets, even towel hooks — by room, with quantity or area and price**, and autosum. **The purpose is not the total but the sequencing: what you can pay for now and what can be deferred.**
   - **⚠️ The failure mode is specific and worth keeping**: money runs out at the very end, credit cards and limits are exhausted, **and people move into an unfinished flat — sometimes radically unfinished, not merely missing a loose piece of furniture** — or start cutting important things and buy "кухню, сделанную из дров," **purely because the tile bought at the start was far above what the budget allowed.**
9. **Procurement and contractor selection** — tilers, builders, ventilation specialists, replanning-approval agents — and begin purchasing.
10. **Bring the crew on site.**

**⚠️ Gap in this source, worth stating: no costs anywhere** — not for the acceptance inspector, the measurers, the engineering project or the documentation, despite all four being recommended purchases. Any budgeting use needs figures from elsewhere on this folder's pages.

## ⚠️ Furniture Is a Rough-Stage Decision — Blocking, Lighting Power, and the Coordination Chain (FLAT, added 2026-09-02)

A furniture manufacturer's own account of what goes wrong when furniture is commissioned late (Михаил, owner of FLAT, St Petersburg). `promotional_ratio: medium` — **the thesis "come to us early" is also the pitch, and he says so openly** — but the two failure mechanisms are physical and specific, and **he draws an honest scope boundary that excludes most of what a client buys.** RU, 2023. [source: [[_Sources/YT_F7bIf3Pv3X8_flat_when_to_commission_furniture|F7bIf3Pv3X8]]]

**⚠️ His governing premise, and it is why this belongs on a sequencing page: "мебель у клиента должна стоять при любых раскладах."** The furniture gets installed regardless of what was prepared — **so a rough-stage omission does not cancel it, it degrades it or forces a compromise.**

### ⚠️ Failure one — missing blocking/backing (закладные), which he calls problem number one

- **The real case: a ~400 m² house with a great deal of wall-hung furniture — including hung TV units where the television stood *on* the unit rather than being wall-mounted, so the unit carried its own weight plus the TV's, plus small children leaning on it. "Нет ни одной закладной, ничего вообще."**
- **⚠️ The remediation cost is the point: "для того чтобы сделать, тебе надо просто полдома разобрать."** They compromised instead.
- **⚠️ The mechanism, stated numerically, and this is genuinely new to this vault: a 4 m-long wall-hung unit fixed into 12.5 mm plasterboard — which he calls "мел с бумагой" — with only the profile studs behind it.** That is what the load actually hangs on when no blocking was installed. **Bears on any wall-hung furniture, TV mount or floating vanity decision, not only kitchens.**
- **His liability framing explains why the maker cares more than anyone in the chain: "мы же понимаем, что мы эту тумбу привезём, повесим, и она просто упадёт на ногу кому-нибудь."**

### ⚠️ Failure two — under-cabinet lighting missed by the whole chain

- A kitchen arrives already manufactured with integrated lighting, the installers fit it, **and there is no provision to power or switch it.**
- **⚠️ The chain of omission is the finding: the designer missed it first, then the foreman, then the client's instruction was not tracked, then the installers "тоже никуда не смотрят."** He concedes everyone missing it takes real effort — **and reports it happening.** Fixing it afterwards is "очень сложно, больно и дорого."
- **⚠️ His diagnosis is diffusion of responsibility, stated as an ideal-versus-real gap: "в идеальном мире должен смотреть строитель, дизайнер, директор, авторский надзор… но в реальном мире такие ситуации очень часто, и вы за них отвечаете."** **This is the practical case for why author's supervision and independent technical supervision are separate roles — a distinction this vault already holds from three design-side sources; here it arrives from the trade that inherits the failure.**

### ⚠️ When to commission, with the scope boundary that makes the advice usable

- **His answer: think about the furniture at the very beginning, before the renovation starts.**
- **⚠️ But he draws the line himself: a chest of drawers or a bed can be bought at any moment — "я купил, привёз, поставил, с ней не может быть никаких глобальных проблем."**
- **⚠️ Early commissioning matters specifically for: a kitchen, built-in furniture, wall-hung units, and decorative wall panels.** "Чтобы сделать это хорошо, нужна подготовка."
- **⚠️ The named coordination chain: прораб + технолог + конструктор of the furniture production + дизайнер. The технолог visits site, checks, takes the necessary measurements and issues recommendations on socket positions, service routing and blocking/backing.**
- **⚠️ And the cost gradient for delay: "на раннем этапе всё можно сделать… чем дольше ты это всё затянул, тем сложнее эту проблему решать," and once the crew is off site "решать эти вопросы не с кем — это решается просто сложнее и дороже для клиентов."**

**⚠️ Corroborates this page's existing pre-site ordering from the opposite side of the table.** Безверхая's ten-step plan puts technical constraints and engineering ahead of finishes, and her kids-room method turns on placing sockets for furniture that does not yet exist. **This source supplies the physical consequence of skipping that — blocking, and lighting power — from the trade that inherits the problem.**

**⚠️ Gap: no specification for the blocking itself** — no material, thickness, size or fixing pattern, only that it must exist. **And no indication of how early "early" is** in weeks or stages. Anything buildable needs a different source.
