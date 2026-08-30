# Electrical — Rough Electrical: Sequencing & Common Pitfalls

Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]].

- Alexey Zemskov / ZEMS recommends: **Plaster masonry (brick/block) walls before chasing electrical cable slots** — chasing into unplastered walls risks unanchored, loosely-hanging cable runs and typically forces the electrical work into two messy, re-visited phases instead of one clean pass.
- Alexey Zemskov / ZEMS warns: **Do not cut recessed breaker-panel niches into load-bearing monolithic concrete walls** — this violates structural building codes; use a surface-mounted panel instead where the wall is load-bearing.
- **Петришин-Строй refines the monolith-chasing rule above with the real underlying mechanism (added 2026-08-24, Round 8)**: the actual hard limit isn't the monolith material itself, it's the rebar inside it — chasing up to roughly the first rebar layer's cover depth (~2-3cm) is fine, but cutting/damaging the rebar is technologically prohibited outright and will get the building's technical supervision ("технадзор") to fine the contractor and force it re-welded. **A soundproofing side-benefit of routing around exposed monolith instead**: bare monolithic concrete is acoustically resonant (vibration/noise travel readily through it), so covering outlet-box/cable areas with foam block instead of chasing the monolith directly gives incidental extra soundproofing. **Real time-cost data point**: a foam-block outlet-box group + finish took ~10 minutes vs. nearly an hour drilling the equivalent into granite-aggregate monolithic concrete with a core bit — carbide bits wear out fast on this hard aggregate, so a water-cooled diamond core bit at low RPM (manual spray-bottle trickle feed) is used instead. [source: [[_Sources/YT_sqk0Nl8AVYI_petrishin_monolith_electrical|sqk0Nl8AVYI]]]
- **Outlet-box flush-mount discipline and pull-out resistance (Петришин-Строй, added 2026-08-24, Round 8)**: a protruding outlet box causes a visible bump defect once plastered — flush-mount as a courtesy to the plastering/painting crew. In a thin partition wall with weak box fixation, cord-tugging (children or adults) can pull a box out of the wall entirely; enlarging the drilled mounting hole slightly beyond the box's own footprint gives the mounting adhesive/plaster more grip surface and meaningfully improves pull-out resistance — framed as a real shock-risk mitigation, not just a cosmetic fix. [source: [[_Sources/YT_sqk0Nl8AVYI_petrishin_monolith_electrical|sqk0Nl8AVYI]]]
- **Phase-loss/neutral-disconnection protection, a building-shared-infrastructure failure mode (Петришин-Строй, added 2026-08-24, Round 8)**: a client-requested protection unit automatically disconnects (or switches to a backup phase) if a phase is lost. Mechanism: if an electrician elsewhere in the building's shared wiring accidentally disconnects a neutral, the full 380V line-to-line voltage can appear across single-phase 220V loads throughout the building and "seek out" the weakest-consumption device on a circuit (e.g. a TV), destroying it via overvoltage — distinct from ordinary breaker/short-circuit protection, and not previously documented on this page. [source: [[_Sources/YT_sqk0Nl8AVYI_petrishin_monolith_electrical|sqk0Nl8AVYI]]]
- **Leave cable slack when the final fixture location is still genuinely uncertain, and verify multi-conductor cable counts with the fixture supplier before wiring (Петришин-Строй, added 2026-08-24, Round 8)**: a real anecdote of a design-drawing/kitchen-layout coordination gap (under-cabinet lighting position conflicting with an as-installed range hood) was absorbed without a redo specifically because the electrician left visible spare cable length at the outlet — without that slack, a miscoordinated cable gets cut short and hidden as a future problem. Separately: complex dimmable LED under-cabinet lighting needed a 5-conductor cable (only 4 of 5 actually used) — confirmed by calling the fixture supplier directly before installation, rather than assuming a standard conductor count. [source: [[_Sources/YT_sqk0Nl8AVYI_petrishin_monolith_electrical|sqk0Nl8AVYI]]]
- Alexey Zemskov / ZEMS warns: **Do not puncture subfloor soundproofing membranes with mechanical anchors to clip electrical conduit** — this ruptures the acoustic insulation's integrity; use adhesive clips bonded to the soundproofing layer instead.
- Alexey Zemskov / ZEMS recommends: **Price rough electrical work by floor area, not by cable length** — pricing by linear meters is a known vector for "turns out we needed more cable, please pay more" upselling; a floor-area-based quote is harder to inflate after the fact. *(See the smeta-literacy section of [[11_Budget_and_Planning/Budgeting_Guide|Budgeting Guide]], which applies the same logic to plumbing rough-in.)*
- **A window-slope-mounted outlet/switch panel must be glued (foam adhesive) to the slope structure, not merely clipped in** — a loose/wobbly slope outlet when unplugging a cord is a simple, homeowner-testable sign of a bad glue job. The commonly repeated "condensation can short a slope outlet" worry is treated as a myth by this source: the slope cavity sits at the same temperature as the room, so there's no dew-point crossing inside it. `single-account`, physics reasoning not independently verified. [source: [[_Sources/YT_P7_rUkk8clU_outlets_in_window_slopes|P7_rUkk8clU_outlets_in_w]]]

## Furniture-First Planning & Marking Technique (added 2026-08-24, Round 2)

Pavel Sidorik **independently corroborates** the "plan furniture before finalizing socket placement" rule already in [[12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning|Key Concepts & Planning]] (a different practitioner/channel), and adds a concrete method: model the apartment in SketchUp with exact room dimensions, ceiling heights, and furniture drawn to real size/position, then read electrical-point placement directly off that model — especially valuable for built-in kitchen/bathroom furniture. A self-taught non-expert can do this (2 days spent on the model, credited to YouTube tutorials); a prior, hand-drawn-pencil version of the same practice on this channel's earlier khrushchevka project is called a real precision downgrade by comparison.

**Uniform switch-height marking technique**: mount a laser level on a spring-loaded extension pole (распорная штанга) positioned mid-room, and mark every switch location in the room from that single 360°-laser position at once — guarantees a consistent height (this project: 90cm from finished floor) without repositioning the laser per point.

**Floor-base prep specific to electrical rough-in**: after screed demolition and cement-laitance grinding, patch leftover surface pits/divots with cement plaster (applied, then scraped flush) purely to create a smooth-enough base for routing corrugated conduit — cosmetic evenness only, since a new screed will cover it regardless. Real before/after screed-thickness figures for this project: original developer screed 10cm, new total floor buildup (screed + underlayment) reduced to 7-8cm.

**Reusable dust-containment room barrier** ("Blue Dolphin" plastic zip-door, sealed with included double-sided tape): hangs over a doorway, lets the crew chase/drill one room fully sealed off, vacuum it clean, then move tools/belongings there before opening the next room; reusable across future projects. **Material-specific adhesion caveat**: on an aerated-silicate-block wall, the included double-sided tape alone was unreliable (dusty, porous surface) — back it up with ordinary plastering tape as a secondary adhesive. [source: [[_Sources/YT_9-NjgDLleOw_sidorik_electrical_ep6|9-NjgDLleOw_sidorik_electrical_ep6]]]

**Prime freshly-cut chases/holes immediately after cutting and vacuuming, while the room is still sealed and clean — before moving tools/belongings back in.** Extends the dust-barrier sequencing above with the next step: deep-penetrating primer (named: Ceresit CT 17) applied by airless sprayer at low pressure to avoid airborne mist (a garden pump sprayer substitutes if no airless sprayer is available). [source: [[_Sources/YT_IWVPepWlzSs_sidorik_electrical_ep7|IWVPepWlzSs_sidorik_electrical_ep7]]]

**Furniture-maker coordination timing, corroborating with a stated failure
mode (Петришин-Строй, added 2026-08-24, Round 2)**: before rough-electrical
work starts, have the furniture makers (`мебельщики`) come measure and
propose their own outlet/switch placement for built-in cabinetry/appliances
first, folding any changes into the rough-electrical layout — the company's
own stated experience is that furniture installers routinely show up
*after* rough-in is finished and ask for relocated outlets anyway, so
front-loading this avoids the later rework. Independently corroborates the
Zemskov/Sidorik "plan furniture before finalizing socket placement" rule
above with a third, distinct practitioner. [source: [[_Sources/YT_Q6GKMOJuaPc_petrishin_electrical_quality_checklist|Q6GKMOJuaPc]]]

**⚠️ Low-ceiling wiring-layout rule (Петришин-Строй, added 2026-08-24, Round 4, Moscow level-1 case study)**: on a secondary-market apartment with limited ceiling height, keep only lighting circuits routed across the ceiling; run switch/socket cabling along the floor/walls instead. Stated mechanism: if all wiring (not just lighting) ran on the ceiling, cable crossovers would force a bigger ceiling recess/drop than lighting-only wiring needs — a concrete ceiling-height-preservation technique tied directly to a wiring-layout decision. [source: [[_Sources/YT_qFM8NIDIRro_petrishin_case_study_old_apartment|qFM8NIDIRro]]]

**Panel-termination and breaker-labeling discipline (Петришин-Строй, added 2026-08-24, Round 5)**: the breaker panel itself must be fully wired/terminated before the rough-electrical stage is handed over, not left as "we'll finish it in 30 minutes later" — a named real practitioner complaint about crews that route wiring to every outlet box but leave the panel itself unterminated. **Breaker labels should be requested and applied immediately at the moment of paying for the electrical stage**, not deferred — otherwise by the time the apartment is ready to occupy, nobody remembers which breaker controls which circuit. `single-account`. [source: [[_Sources/YT_vKMHNYQYWAI_petrishin_top13_expensive_mistakes|YT_vKMHNYQYWAI]]]

## Project/Smeta Cross-Review, Wire-Labeling Hiring Risk, and a Live-Circuit Damage-Detection Mechanism (Петришин-Строй, added 2026-08-24, Round 7)

- **Cross-review the design project and cost estimate together with an
  experienced electrician before work starts** — specifically to catch
  designer/estimator errors on paper; reworking an outlet/switch
  position or a wired circuit line after installation is far slower and
  costlier than correcting the same error while it's still a drawing.
- **Panel-size decision framework, by client need and budget**: absent a
  formal single-line electrical design, the foreman and electrician
  assess client needs directly and propose a panel size (compact
  12-breaker, or 36/48/72-breaker) plus whether a smart-home system is
  wanted, rather than defaulting to one fixed size.
- **⚠️ Wire-end labeling as a hiring-vetting red flag, not just tidiness**:
  every wire end should be marked (marker or tag) with its destination
  room/device. Unlabeled wires during or after an electrician's work are
  a red flag either way — either the electrician is unskilled, *or* a
  skilled one deliberately skipped labeling to make the client dependent
  on him personally for any future work. **Cost consequence**: bringing
  in a different electrician later on unlabeled work means tracing and
  re-testing every connection from scratch, which the source states
  commands "a large sum."
- **⚠️ Live-circuit-during-drywall-install damage-detection mechanism**:
  after temp outlets/switches/lights are connected and functionally
  tested, **keeping the panel energized through subsequent trades' work
  (e.g. drywall installers screwing metal track to the walls) means a
  screw that hits a live wire trips the breaker immediately** — alerting
  that trade on the spot. Leaving the panel de-energized instead lets
  the same screw-through-wire damage go completely undetected until the
  panel is later connected, by which point it's far more expensive and
  difficult to trace and repair. Distinct from, and a refinement of,
  this project's existing basic temp-outlet functional test.
- **Explicit 4-factor electrical-rough-in cost-driver framework**: (1)
  outlet/switch density; (2) wall material — reinforced-concrete panel
  wall costs more to chase than aerated/gas-block; (3) panel size —
  bigger panel costs more labor to assemble; (4) aesthetics — perfectly
  straight/measured/hidden-back-box trace routing and a primed/painted
  ceiling cost extra time without changing the electrical system's
  actual performance. **Explicit performance-vs-aesthetics admission**:
  neat routing does not improve "electron speed" or any functional
  network parameter — it's a purely cosmetic/serviceability upsell,
  stated candidly by the source rather than framed as technically
  necessary — a useful line item for distinguishing must-pay from
  nice-to-have spend on an electrical quote.

[source: [[_Sources/YT_qnmVK1R3X0k_petrishin_electrical_pricing_mistakes|qnmVK1R3X0k]]]

## Floor vs. Ceiling Wiring Routing — Decision Framework and a Real Worked Cost Comparison (Петришин-Строй, real ЖК Аэробус object, added 2026-08-24, Round 10)

Real 117m², 4-room apartment, ЖК "Аэробус" (region level 2 — named
development, no city spoken). Low promotional ratio.

**Color-coded conduit convention** (this installation's own choice, not
a universal requirement): black = power/outlet circuits, gray = lighting
circuits, orange = low-voltage/data circuits (satellite/cable TV,
internet, CCTV) — makes the rough-in self-documenting for troubleshooting
later.

**Decision framework**: route via **ceiling** when the client accepts a
stretch or drywall-drop ceiling to hide the conduit, when the developer's
existing screed is already flat/good (no reason to repour just to bury
floor wiring), or when the existing floor covering (e.g. expensive
parquet) is staying and won't be opened up. Route via **floor** when the
client wants to preserve every centimeter of ceiling height (a
drywall/stretch ceiling to hide conduit costs 3-5cm regardless), or when
a new screed is being poured anyway (a typical 4-6cm new-build screed
buries the wiring for free).

**⚠️ Structural reason floor routing is usually cheaper for outlets**:
outlets/switches always sit low on a wall regardless of layout, so
floor-routed wiring needs only a short wall chase (~30-50cm) up to the
box; ceiling-routed wiring needs a *full-height* chase down from the
ceiling to the same box — more wire, more chasing labor, more cost,
specifically for outlet/switch circuits (not lighting fixtures, which
are already at ceiling height either way).

**⚠️ Real arithmetic-checkable cost comparison, same object, same fixture
count, two hypothetical full-routing scenarios**: all-floor-routing would
use 2,045m of wire, ≈33,673 RUB in consumables, ≈120,862 RUB total
materials; all-ceiling-routing would use 2,488m of wire, ≈52,710 RUB in
consumables, ≈159,510 RUB total materials — a **38,648 RUB** materials
difference. Adding an illustrative +20% ceiling-routing labor premium (on
a deliberately round 1,000 RUB/m² baseline labor rate, below actual
Moscow market rate) adds a further ≈23,400 RUB. **Combined: full-ceiling
routing would have cost roughly 62,000 RUB more than full-floor routing**
for this specific real object's fixture count — a rare worked real-object
comparison for this exact decision, not a universal percentage.
`single-account`. Not converted to USD (upload date not confirmed).

**Combined/hybrid routing rationale on this object**: the developer
requires whole-apartment Шумонет-100 soundproofing, itself mandating a
≥6cm screed pour — burying the main power/lighting bundle under that pour
is free. Low-voltage cabling was deliberately routed via ceiling instead,
specifically to avoid an overlap-prone floor bundle *and* to avoid
overloading the ceiling with the entire bundle (which would have
complicated the ceiling soundproofing frame's own install) — a deliberate
density-management split.

**Conduit-to-screed fixing over floor soundproofing**: conduits must
never be screw-anchored through a Шумонет soundproofing layer into the
structural screed below — the screw penetration creates a rigid "sound
bridge" defeating the soundproofing's purpose. Instead, conduits are tied
to a wire mesh laid loosely over the soundproofing layer (no fasteners
through the membrane); without soundproofing present, conduits are
perforated-tape-strapped directly to the screed. A separate patch is
applied specifically where a conduit run crosses from floor to wall, to
avoid a rigid screed-to-wall bridge at that transition.

**Junction/splice placement**: avoid hidden/inaccessible junction boxes
behind wallpaper or a wall patch — route lighting-circuit splices into
deepened switch-box recesses at the switch locations instead, so future
troubleshooting only requires removing the switch mechanism.

**⚠️ Counter-intuitive caution, worth checking against other sources**:
this source states directly that a wire cannot realistically be pulled
back out of an already-installed conduit run for replacement, regardless
of floor or ceiling routing — contrary to the common assumption that
conduit exists specifically to enable future wire replacement without
demolition. `single-account`, `unverified`.

[source: [[_Sources/YT_yyW9WaW3Pls_petrishin_electrical_floor_vs_ceiling|yyW9WaW3Pls]]]

## Floor-Routing Detail, a Real Rough-In Walkthrough (ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ / Vladimir Amelchenko, added 2026-08-28, Round 3)

St. Petersburg (channel level 2), low promotional ratio, `8-GD_CEX0Bg` (2025-02-28), 170m² apartment/3 bathrooms. Corroborates this section's existing floor-vs-ceiling routing and never-fasten-through-soundproofing rules, with a distinct fixing-technique variant and new details.

- **⚠️ Conduit-to-Шуманет fixing, a gluing variant**: after leveling the floor and laying two layers of Шуманет (soundproofing + waterproofing), corrugated conduit is **glued directly to the membrane using bitumen tape**, not screw-fastened — the membrane's own bitumen-like surface takes the tape well. This project's existing Petrishin-Stroi source instead ties floor conduit to a wire mesh laid loosely over the membrane; both share the same underlying rule (never fasten a rigid penetration through the membrane) but are two independent, non-identical methods.
- **⚠️ Waterproofing-membrane repair at wall penetrations, a real flood-prevention detail**: where conduit exits the floor membrane into a wall, the membrane is necessarily cut, breaking the "trough" that makes the floor waterproof — two additional membrane layers must be welded/fused back over the cut to restore a sealed penetration. Without this repair only the soundproofing function survives at that point, not the waterproofing — the next screed pour would flood the neighbors below through the unsealed penetration.
- **⚠️ Low-voltage (12-24V) transformer consolidation outside the wet zone**: a bathroom with extensive 12-24V transformer-driven lighting (shelves, mirror, vanity) routes all transformers out to a dedicated cabinet in an adjacent room — housing them in the wet zone itself is "not quite correct," and there's often no physical space there anyway.
- **⚠️ Metal protective sleeve at a floor-conduit doorway-threshold crossing**: floor conduit passing under a door opening is fed through metal tubing so a later trade drilling/screwing in a threshold strip at that spot can't sever the cable.
- **⚠️ Deliberate detour routing to guarantee avoiding a known future fixture-mounting point**: where a wall fixture has a known fixed anchor pattern (an intercom handset, a wall sconce, both anchored on a vertical axis), rough-in conduit is routed in a "U"-shape detour around that axis instead of a straight run — guaranteeing whoever later drills for those anchors (any installer, any care level) can't hit the cable. A deliberate mistake-proofing technique, not an aesthetic/cost choice.

[source: [[_Sources/YT_8-GD_CEX0Bg_sbk_electrical_roughin_basics|8-GD_CEX0Bg]]]

## Locating a Concealed Junction Box, and a Live-Wiring Safety Caution (added 2026-08-25, Квартиранты)

An individual homeowner (not a professional electrician), needing power for
a new light fixture with no visible nearby source: **tapped the wall near
the ceiling above an existing switch and listened for a hollow sound at
several points** — this located a plastered-over, concealed junction box
at the wall/ceiling seam. **A directly reusable diagnostic technique**:
knock-testing along a wall/ceiling seam near an existing switch/outlet to
find a concealed junction box before assuming new wiring must run all the
way from the breaker panel. Once found, he broke open the plastered-over
gap, drilled a short vertical chase from the ceiling down to the new
wire's exit point with a hammer drill and masonry bit, threaded the new
wire through, and filled the chase with **Rotband patching compound that
was past its stated shelf life** — treating expired setting compound as
still usable for a non-critical, purely cosmetic channel fill (not a
structural application).

**⚠️ Explicit, self-identified unsafe practice**: the source performed
this work **live (energized)**, specifically because he wanted to film
the process and needed the light on to do so, and states directly:
"repeating this and working on live electrical wiring is dangerous to
health and life." Recorded here as a documented, self-flagged bad
practice, not a technique to copy — de-energize a circuit before
modifying it, regardless of filming/visibility convenience.
[source: [[_Sources/YT_sAXC1hn8u9A_kvartiranty_hallway_wall_prep_electrical|YT_sAXC1hn8u9A]]]
