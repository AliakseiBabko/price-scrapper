# Electrical — Rough Electrical: Sequencing & Common Pitfalls

Part of [[12_Engineering_and_Systems/Electrical_and_Lighting|Electrical & Lighting]].

- Alexey Zemskov / ZEMS recommends: **Plaster masonry (brick/block) walls before chasing electrical cable slots** — chasing into unplastered walls risks unanchored, loosely-hanging cable runs and typically forces the electrical work into two messy, re-visited phases instead of one clean pass.
- Alexey Zemskov / ZEMS warns: **Do not cut recessed breaker-panel niches into load-bearing monolithic concrete walls** — this violates structural building codes; use a surface-mounted panel instead where the wall is load-bearing.
- **Петришин-Строй refines the monolith-chasing rule above with the real underlying mechanism (added 2026-08-24, Round 8)**: the actual hard limit isn't the monolith material itself, it's the rebar inside it — chasing up to roughly the first rebar layer's cover depth (~2-3cm) is fine, but cutting/damaging the rebar is technologically prohibited outright and will get the building's technical supervision ("технадзор") to fine the contractor and force it re-welded. **A soundproofing side-benefit of routing around exposed monolith instead**: bare monolithic concrete is acoustically resonant (vibration/noise travel readily through it), so covering outlet-box/cable areas with foam block instead of chasing the monolith directly gives incidental extra soundproofing. **Real time-cost data point**: a foam-block outlet-box group + finish took ~10 minutes vs. nearly an hour drilling the equivalent into granite-aggregate monolithic concrete with a core bit — carbide bits wear out fast on this hard aggregate, so a water-cooled diamond core bit at low RPM (manual spray-bottle trickle feed) is used instead. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_sqk0Nl8AVYI_petrishin_monolith_electrical|sqk0Nl8AVYI]]]
- **Outlet-box flush-mount discipline and pull-out resistance (Петришин-Строй, added 2026-08-24, Round 8)**: a protruding outlet box causes a visible bump defect once plastered — flush-mount as a courtesy to the plastering/painting crew. In a thin partition wall with weak box fixation, cord-tugging (children or adults) can pull a box out of the wall entirely; enlarging the drilled mounting hole slightly beyond the box's own footprint gives the mounting adhesive/plaster more grip surface and meaningfully improves pull-out resistance — framed as a real shock-risk mitigation, not just a cosmetic fix. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_sqk0Nl8AVYI_petrishin_monolith_electrical|sqk0Nl8AVYI]]]
- **Phase-loss/neutral-disconnection protection, a building-shared-infrastructure failure mode (Петришин-Строй, added 2026-08-24, Round 8)**: a client-requested protection unit automatically disconnects (or switches to a backup phase) if a phase is lost. Mechanism: if an electrician elsewhere in the building's shared wiring accidentally disconnects a neutral, the full 380V line-to-line voltage can appear across single-phase 220V loads throughout the building and "seek out" the weakest-consumption device on a circuit (e.g. a TV), destroying it via overvoltage — distinct from ordinary breaker/short-circuit protection, and not previously documented on this page. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_sqk0Nl8AVYI_petrishin_monolith_electrical|sqk0Nl8AVYI]]]
- **Leave cable slack when the final fixture location is still genuinely uncertain, and verify multi-conductor cable counts with the fixture supplier before wiring (Петришин-Строй, added 2026-08-24, Round 8)**: a real anecdote of a design-drawing/kitchen-layout coordination gap (under-cabinet lighting position conflicting with an as-installed range hood) was absorbed without a redo specifically because the electrician left visible spare cable length at the outlet — without that slack, a miscoordinated cable gets cut short and hidden as a future problem. Separately: complex dimmable LED under-cabinet lighting needed a 5-conductor cable (only 4 of 5 actually used) — confirmed by calling the fixture supplier directly before installation, rather than assuming a standard conductor count. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_sqk0Nl8AVYI_petrishin_monolith_electrical|sqk0Nl8AVYI]]]
- Alexey Zemskov / ZEMS warns: **Do not puncture subfloor soundproofing membranes with mechanical anchors to clip electrical conduit** — this ruptures the acoustic insulation's integrity; use adhesive clips bonded to the soundproofing layer instead.
- Alexey Zemskov / ZEMS recommends: **Price rough electrical work by floor area, not by cable length** — pricing by linear meters is a known vector for "turns out we needed more cable, please pay more" upselling; a floor-area-based quote is harder to inflate after the fact. *(See the smeta-literacy section of [[11_Budget_and_Planning/Budgeting_Guide|Budgeting Guide]], which applies the same logic to plumbing rough-in.)*
- **A window-slope-mounted outlet/switch panel must be glued (foam adhesive) to the slope structure, not merely clipped in** — a loose/wobbly slope outlet when unplugging a cord is a simple, homeowner-testable sign of a bad glue job. The commonly repeated "condensation can short a slope outlet" worry is treated as a myth by this source: the slope cavity sits at the same temperature as the room, so there's no dew-point crossing inside it. `single-account`, physics reasoning not independently verified. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_P7_rUkk8clU_outlets_in_window_slopes|P7_rUkk8clU_outlets_in_w]]]

## Furniture-First Planning & Marking Technique (added 2026-08-24, Round 2)

Pavel Sidorik **independently corroborates** the "plan furniture before finalizing socket placement" rule already in [[12_Engineering_and_Systems/analysis/Electrical_Key_Concepts_and_Planning|Key Concepts & Planning]] (a different practitioner/channel), and adds a concrete method: model the apartment in SketchUp with exact room dimensions, ceiling heights, and furniture drawn to real size/position, then read electrical-point placement directly off that model — especially valuable for built-in kitchen/bathroom furniture. A self-taught non-expert can do this (2 days spent on the model, credited to YouTube tutorials); a prior, hand-drawn-pencil version of the same practice on this channel's earlier khrushchevka project is called a real precision downgrade by comparison.

**Uniform switch-height marking technique**: mount a laser level on a spring-loaded extension pole (распорная штанга) positioned mid-room, and mark every switch location in the room from that single 360°-laser position at once — guarantees a consistent height (this project: 90cm from finished floor) without repositioning the laser per point.

**Floor-base prep specific to electrical rough-in**: after screed demolition and cement-laitance grinding, patch leftover surface pits/divots with cement plaster (applied, then scraped flush) purely to create a smooth-enough base for routing corrugated conduit — cosmetic evenness only, since a new screed will cover it regardless. Real before/after screed-thickness figures for this project: original developer screed 10cm, new total floor buildup (screed + underlayment) reduced to 7-8cm.

**Reusable dust-containment room barrier** ("Blue Dolphin" plastic zip-door, sealed with included double-sided tape): hangs over a doorway, lets the crew chase/drill one room fully sealed off, vacuum it clean, then move tools/belongings there before opening the next room; reusable across future projects. **Material-specific adhesion caveat**: on an aerated-silicate-block wall, the included double-sided tape alone was unreliable (dusty, porous surface) — back it up with ordinary plastering tape as a secondary adhesive. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_9-NjgDLleOw_sidorik_electrical_ep6|9-NjgDLleOw_sidorik_electrical_ep6]]]

**Prime freshly-cut chases/holes immediately after cutting and vacuuming, while the room is still sealed and clean — before moving tools/belongings back in.** Extends the dust-barrier sequencing above with the next step: deep-penetrating primer (named: Ceresit CT 17) applied by airless sprayer at low pressure to avoid airborne mist (a garden pump sprayer substitutes if no airless sprayer is available). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_IWVPepWlzSs_sidorik_electrical_ep7|IWVPepWlzSs_sidorik_electrical_ep7]]]

**Furniture-maker coordination timing, corroborating with a stated failure
mode (Петришин-Строй, added 2026-08-24, Round 2)**: before rough-electrical
work starts, have the furniture makers (`мебельщики`) come measure and
propose their own outlet/switch placement for built-in cabinetry/appliances
first, folding any changes into the rough-electrical layout — the company's
own stated experience is that furniture installers routinely show up
*after* rough-in is finished and ask for relocated outlets anyway, so
front-loading this avoids the later rework. Independently corroborates the
Zemskov/Sidorik "plan furniture before finalizing socket placement" rule
above with a third, distinct practitioner. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_Q6GKMOJuaPc_petrishin_electrical_quality_checklist|Q6GKMOJuaPc]]]

**⚠️ Low-ceiling wiring-layout rule (Петришин-Строй, added 2026-08-24, Round 4, Moscow level-1 case study)**: on a secondary-market apartment with limited ceiling height, keep only lighting circuits routed across the ceiling; run switch/socket cabling along the floor/walls instead. Stated mechanism: if all wiring (not just lighting) ran on the ceiling, cable crossovers would force a bigger ceiling recess/drop than lighting-only wiring needs — a concrete ceiling-height-preservation technique tied directly to a wiring-layout decision. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_qFM8NIDIRro_petrishin_case_study_old_apartment|qFM8NIDIRro]]]

**Panel-termination and breaker-labeling discipline (Петришин-Строй, added 2026-08-24, Round 5)**: the breaker panel itself must be fully wired/terminated before the rough-electrical stage is handed over, not left as "we'll finish it in 30 minutes later" — a named real practitioner complaint about crews that route wiring to every outlet box but leave the panel itself unterminated. **Breaker labels should be requested and applied immediately at the moment of paying for the electrical stage**, not deferred — otherwise by the time the apartment is ready to occupy, nobody remembers which breaker controls which circuit. `single-account`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_vKMHNYQYWAI_petrishin_top13_expensive_mistakes|YT_vKMHNYQYWAI]]]

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

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_qnmVK1R3X0k_petrishin_electrical_pricing_mistakes|qnmVK1R3X0k]]]
