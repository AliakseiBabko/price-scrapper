# Screed & Subfloor

## Scope

Everything under the floor covering: screed types and thickness rules, crack causes, mechanized and semi-dry methods, curing discipline, acceptance testing against a developer screed, impact-noise underlayment, and screed-vs-walls sequencing

Split out of `Flooring_Guide.md` on 2026-08-31. **Content was moved verbatim** — nothing was rewritten, condensed or re-attributed in the move. The parent guide keeps its summary lists and the shared Source Notes.

**Companion pages:**

- [[13_Surfaces_and_Finishes/analysis/Flooring_Material_Selection|Flooring Material Selection]]
- [[13_Surfaces_and_Finishes/analysis/Flooring_Installation_and_Baseboards|Flooring Installation, Transitions & Baseboards]]
- [[13_Surfaces_and_Finishes/Flooring_Guide|Flooring Guide]] — the parent guide

---

## Screed Type Selection, Thickness Rules, and the Top-3 Crack Causes (Konstantin Kruglov / Ontario, added 2026-08-28, Round 6)

> [!NOTE]
> First Kruglov-channel screed content on this page — cross-checked against this page's existing screed content (Петришин-Строй's semi-mechanized/acceptance-QC sources, Pavel Sidorik's DIY reinforced-screed build, the sbk.remont developer-screed-defect case below) before writing; several mechanisms corroborate rather than duplicate (mandatory fiber/plasticizer, external-corner T-cuts, gradual-drying discipline) and are not re-recorded. Region level 2, with an explicit "99% of Moscow/Moscow-region apartments" statement. Low promotional ratio. [source: [[_Sources/YT_SP3NyXmPafI_kruglov_screed_cracking|YT_SP3NyXmPafI]]]

- **⚠️ Wood-floor-slab buildings are essentially restricted to dry screed only** (GVL sheet-based) — cement-based wet/semi-dry screed risks overloading the wood structure and flooding the unit below. Not every historic "Stalinka" building has wood floor slabs — some (especially older city-center, monument-protected buildings) have had their interior floor slabs rebuilt over time to accommodate modern elevator shafts or underground parking.
- **Dry screed's three real downsides, one counter-intuitive**: can't tolerate uneven point-loading from furniture/appliances (loose fill shifts, deforms the floor); a flood requires full demolition/rebuild (trapped moisture, mold); and **despite being weaker/less durable than wet or semi-dry, dry screed is actually the more expensive of the three options.**
- **Company preference: semi-dry over wet screed, for level accuracy** — wet screed's higher water content shrinks/settles more as it cures, making an exact target floor level harder to hit; semi-dry settles less.
- **⚠️ Wet-screed thickness rule + keramzit-buildup technique**: minimum 3cm; the mortar layer itself should never exceed 6cm (overload risk) — beyond 6cm total, build up the excess with keramzit fill + cement-milk consolidation first, then finish with up to 6cm of mortar on top. Worked example: 10cm total = 4-5cm keramzit + cement milk + 5cm mortar screed.
- **⚠️ Semi-dry screed thickness rule, a distinct threshold**: minimum 4cm; up to 8cm achievable without keramzit; beyond 8cm needs the same keramzit-buildup **plus mandatory mesh reinforcement**.
- **⚠️ Three-tier drying schedule for both screed types**: **walkable** — wet 2-3 days (stepping boards needed before then), semi-dry 12-24 hours. **Tile-layable** — wet screed needs *full* cure first (tiling onto a damp wet screed is explicitly forbidden): 28 calendar days, or 7 days per cm of thickness (5cm → 35 days); semi-dry only needs 10-14 days (moisture mostly out, strength sufficient before full cure). **Final flooring** (laminate/quartz-vinyl/parquet): full cure required either way — semi-dry's own full cure (≈20-21 days) is slightly faster than wet's 28 days.
- **⚠️ No universal drying-time standard**: humid/cold rooms can extend full cure to 35-40 days — judge per-room condition, don't apply the 28-day figure blindly.
- **Top-3 named crack-cause framework**: (1) bad mix composition (too much water/poor mixing → uneven drying, cracking); (2) installation defects (overly thick layer without reinforcement, or missing mandatory fiber+plasticizer in either screed type); (3) missing deformation joints — called out as the single most important cause.
- **⚠️ Perimeter damper-tape minimum thickness spec, first numeric figure for this store: ≥8mm**, alongside deformation cuts at door openings, every 3-4m in long/narrow rooms, and a diagonal "T"-cut at every external corner (this last detail corroborates this page's existing Петришин-Строй content, not new).
- **⚠️ Radiator-adjacent extra-watering technique during cure**: if a radiator can't be switched off while the screed cures, water that specific area more closely/frequently than the rest of the room — its heat accelerates local moisture loss, risking a locally weaker zone if not compensated for.
- **⚠️ Install-time figure, distinct from the drying/cure schedule above (added 2026-08-28, Round 16)**: semi-dry screed installs across a whole apartment in **1-2 days regardless of layout**, and even a full **150-200m² apartment takes only ≈3 days total** — versus wet screed on the same footprint taking roughly **1.5 weeks**. This is the install/pour time itself, not the walkable/tile-layable/full-cure durations already on this page above (which apply after either screed type is poured) — a real-jobsite demonstration (scratch-test of a cured semi-dry screed to show it doesn't crumble) offered as a direct rebuttal to a common client worry that semi-dry screed is "just loose sand" or under-strength. `single-account`, `unverified`. [source: [[_Sources/YT_A16VC0VYjSQ_kruglov_5_site_tour|YT_A16VC0VYjSQ]]]

## Developer Screed Acceptance Testing — Real Instruments and Thresholds (added 2026-08-28)

> [!NOTE]
> Vladimir Amelchenko / ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, with a guest technical-supervision specialist, real on-camera inspection of a subscriber's new-build apartment — live instrument readings shown, not a studio explainer. `single-account` for the specialist's stated thresholds (not cross-checked against a written building code here), but internally consistent and demonstrated live. [source: [[_Sources/YT_l0aR7nQGh4M_sbk_screed_inspection_case|YT_l0aR7nQGh4M]]]

This project's first developer-screed acceptance-testing content — what to actually check before accepting a new-build apartment's floors, and what the numbers mean.

- **Two distinct instruments measure two distinct defects — don't conflate them**: a **склерометр** (rebound/impact hammer, 10 shots averaged) measures the screed's **compressive strength class**; a **rotary laser level** maps **surface flatness/level variation** across multiple points. A screed can fail either test independently of the other.
- **⚠️ Worked example from a real inspection**: rebound-hammer average ≈11.3 ("M100" class) — roughly **1/3 below the code norm for residential floors**. A separate pull-off/adhesion test (50×50mm test tabs glued to the surface, torn off with a calibrated instrument) read **0.35 MPa against a 1 MPa norm** for a base intended for laminate, quartz-vinyl, or tile (**parquet's own norm is stricter still, 0.5 MPa** — this screed fails that threshold too). Level-variation: apartment-wide code tolerance is **≈5mm**; this apartment's single corridor alone measured a 0 to -15mm spread across five points, with a separate 2cm (20mm) corner-to-corner difference found in that same corridor.
- **⚠️ Remediation branches by the *planned finish flooring*, not one verdict for the whole apartment**: planning **parquet** → a screed this weak must be fully demolished (won't survive under a rigid wood floor — cracking, delamination, swelling). Planning **quartz-vinyl** instead → the same screed may be salvageable: grind the surface, reinforce with a strengthening compound or an epoxy primer with sand broadcast, then self-level up to 15-20mm on top — a cheaper remediation path, but only for the more tolerant covering.
- **⚠️ Named failure mode if the strength test is skipped**: pouring an overly strong/rigid leveling material directly onto an already-weak screed doesn't fix it — it **tears the weak layer apart**, since the two layers don't flex/fail together under load. The pull-off test exists specifically to choose a *compatible* leveling material, not just to grade the screed pass/fail.
- **⚠️ Developer semi-dry screed (полусухая стяжка) is characterized as structurally one-time-use**, per the specialist's repeated hands-on experience: when tile bonded to it is later removed, the screed crumbles away in chunks with the tile, unlike a properly mixed "wet" screed, which stays intact even after tile removal a decade later — real implication for anyone who might change flooring later.
- **Stated industry-awareness gap**: per the specialist, roughly 90% of builders (not just buyers) don't know this acceptance test exists, how to perform it, or what the consequences of skipping it are.

### Second Independent Practitioner Doing the Same Pull-Off Test, and a Budget Remedy (Руслан via NSDSGN, 2023-10-11)

**Corroboration rather than new method — recorded because the section above notes that per its own specialist «roughly 90% of builders don't know this acceptance test exists», and this is a second, unrelated contractor doing it as routine.** [source: [[_Sources/YT_Z0brwxSe7gQ_nsdsgn_engineering_systems_site_review|YT_Z0brwxSe7gQ]]]

- **They tested the DEVELOPER's screed on a live object with a pull-off test («на отрыв») using dedicated equipment — «простреливается» — and concluded «в целом стяжка требует улучшения».** No numbers given, so the thresholds above remain the reference.
- **⚠️ The remedy they chose, and it is a third branch the section above does not cover: rather than demolish or fully re-level, they patched it to protect the client's budget — a strengthening primer (укрепляющая грунтовка) plus a finishing levelling compound, with the minor cracks opened out and filled.**
  **⚠️ Read that against the named failure mode above — pouring an overly rigid levelling material onto an already-weak screed tears the weak layer apart. Their sequence puts a CONSOLIDATING primer first, which is the step that makes a light levelling layer defensible. Recorded as their stated approach on one object, not as a general permission to skip the strength test.**
- **And the client-side dynamic worth knowing: «просто клиенты хотят её иногда оставить — мы рекомендуем от себя» otherwise.** So the pressure to accept a developer screed usually comes from the budget, which is exactly why the test is worth its cost.

## Screed-First vs. Walls-First Sequencing — per Zemskov/Zemstandart (added 2026-08-19)

> [!NOTE]
> `single-account`, direct prequel to this vault's existing zero-reference/working-reference content on `13_Surfaces_and_Finishes/Walls_and_Paint.md` and `12_Engineering_and_Systems/analysis/Mounting_Heights_and_Positioning.md` — the two sources form an explicit two-part series (this one uploaded 4 days before the other). [source: [[_Sources/YT_cJLZebMtW7A_screed_or_walls_first_108|note]]]

**The deciding factor is wall construction material, not personal preference or a fixed rule of thumb**: [source: [[_Sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

- **Masonry walls (aerated/foam block) → build walls first, pour screed after.** The floor area under a future wall gets filled with cheap, light block material instead of costly, heavy screed — at just 10cm screed thickness on a 100m² apartment, the "wasted" screed volume filling future wall footprints can reach 1-2m³, a real cost/labor difference given how much cheaper and easier aerated block is to place than the equivalent screed volume. [source: [[_Sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]
- **Drywall-on-metal-frame walls → pour screed first, then build the frame on top.** A metal track profile screwed to an uneven raw subfloor bends to follow that unevenness, producing a visibly bowed wall — screed gives the frame a flat surface to sit on. The same volume-fill economics apply in reverse here too: filling that floor footprint with a stud-and-drywall assembly (especially double-layer with insulation) is more complex/expensive per unit volume than the same footprint filled with ordinary screed. [source: [[_Sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

**One clean exception to the walls-first-for-masonry default**: a genuinely empty, obstruction-free apartment being poured with a concrete pump truck — there, a single-day full-contour screed pour is unambiguously the right call, since the pump truck removes the practical batching constraints that otherwise erode a "pour everything at once" screed's supposed flatness advantage (see below). [source: [[_Sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

**Why "screed poured continuously in one operation is flatter" is significantly overstated in practice**: a genuinely continuous single-pour screed is rare without a pump truck (hand-mixed mortar can't physically place several tonnes in one session, so it ends up poured in batches regardless); a genuinely empty apartment is rare too (tools, material bags, and crew facilities occupy floor space); and — the decisive point — nearly all modern finish flooring needs a thin self-leveling correction layer over the screed anyway, which flattens variation up to ~3-8mm regardless of how the screed itself was sequenced, making the end result effectively identical between the two approaches once that layer goes down. [source: [[_Sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

**Walls-first's own genuine downside, and the fix**: plastering after walls go up inevitably drops mortar onto an already-poured screed, which bonds permanently if not cleaned immediately and later needs jackhammer removal. Build walls, plaster them, *then* pour screed last — this is why the masonry-first sequence above specifically puts screed after plastering, not right after the walls go up. [source: [[_Sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

**Room-to-room level-transfer error, and a pre-marking technique that closes the gap**: transferring a level reference room-by-room (unavoidable once walls exist) accumulates ~3-8mm of real error across a project. Fix: before any walls are built, while the space is fully open, set up a laser level once at the center and mark reference points at ~1m intervals across the *entire* future apartment footprint — every future room then inherits at least one mark from that single original setup, avoiding the accumulated transfer error a room-by-room re-level would introduce. Mark these points not at an arbitrary height but at exactly 99cm above the corridor's own finished floor level, and mark every surface that won't itself be plastered later (window/door reveals, ventilation shafts, pipe risers) — see [[13_Surfaces_and_Finishes/Walls_and_Paint|Walls & Paint]] for the full zero-reference/working-reference system this height derives from.

**Template-stick leveling technique, useful regardless of which sequencing method is chosen**: instead of repeatedly reading a tape measure against a laser-level plane at each beacon, cut a wooden batten, hold it against the beacon at the room's highest point, and mark the laser's crossing point on the rod once — then level every other beacon by matching the laser line to that single mark, rather than re-reading a tape measure each time. Faster (matching a mark beats reading and comparing a number) and more accurate (a tape measure's blade flexes/bows over distance; a rigid rod doesn't). [source: [[_Sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

## Full DIY Reinforced Screed Build with Sub-Screed Sound Insulation — per Pavel Sidorik (added 2026-08-24, Round 4)

Individual practitioner, own new-build apartment, Belarus (level-1 region — see [[16_Legal_and_Regulations/analysis/Renovation_Permits_and_Approvals|Renovation Permits & Approvals]] for the developer-must-deliver-with-screed law this project is built against). Full self-managed build: partitions and electrical rough-in go in *before* the screed (screed must never touch a partition, to avoid transmitting structural noise into it), then a sub-screed noise-insulation membrane, then XPS, then mesh reinforcement and beacons, then the pour.

**Named sub-screed membrane and structural-vs-airborne noise reasoning**: "Стопзвука М" bitumen-polymer membrane (ТехноСонус) — functionally similar to felt-backed roofing membrane, waterproof, torch-fused at overlaps. His own stated reasoning for adding it at all: **structural noise (impacts, footsteps, furniture) is far easier to stop at its source floor than to absorb from the receiving neighbor's ceiling below** — airborne noise (voices, music) is comparatively easier to treat from the receiving side instead. He checked whether cheap linoleum could substitute for the membrane (similar properties) but found even the cheapest linoleum costs more — no reason to substitute. [source: [[_Sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

**XPS layer, named product and reasoning**: Технониколь Carbon Eco, 20mm, rated to 10 tonnes/m² distributed load, rough surface for mortar adhesion. Manufacturer-technologist-confirmed (relayed by the practitioner, `single-account`) compatible with the membrane above, and independently rated to absorb 21dB on its own. Using XPS instead of a thicker plain mortar layer cut roughly 2.5 tonnes of dead weight across the apartment while improving sound absorption at no added screed cost. Screed thickness ended up 7cm total (down from the developer's original 10cm) despite adding the membrane, XPS, and rerouted electrical conduit within it — net finished-floor height rose only ~0.5cm after full substrate cleanup. [source: [[_Sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

**Perimeter damper strip, a genuinely new construction detail**: 15cm strips cut from the same membrane, glued to the wall at final screed height, topped with a second 5mm foamed-polyethylene layer (stapled on) — the extra layer exists because the 5mm membrane alone is thinner than the ~10mm the screed's own linear-expansion movement calls for. Runs the full perimeter of every room getting a screed; trimmed flush and sealed with acoustic sealant after finish work. [source: [[_Sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

**Mesh reinforcement**: needed whenever screed thickness exceeds 3cm (mortar is strong in compression, weak against linear-expansion stress). 10×10cm cell, 4mm wire, one-cell overlap, tied at every second cell, held mid-depth on ~2.5cm risers cut from scrap pipe or XPS offcuts.

**Expanded-clay (керамзит) lightweight fill under an unusually thick screed, per Петришин-Строй (ЖК Виноградный episodic series, added 2026-08-24, Round 13)**: when a screed must run unusually thick (this job: ~7-8cm, driven by the apartment's own leveling needs) filling the full depth with sand-concrete alone risks overloading the structural slab with dead weight — adding a keramzit (expanded-clay) layer as part of the buildup lightens the total load. Distinct from this page's XPS-substitution approach above (that swaps for sound-absorption + weight reduction with a rated product; this is a lower-cost bulk-fill weight-reduction technique for a plain thick screed). Region level 2 (ЖК Виноградный named, no city spoken). `single-account`. [source: [[_Sources/YT__GL2t3cdSi8_petrishin_vinogradny_ep5_electrical_radiators|_GL2t3cdSi8]]]

**⚠️ Beacon technique that avoids sinkage and preserves mesh position**: set beacons on discrete mortar lumps (not a continuous bed) leveled to 1.5cm below the target screed surface (10mm beacon + 5mm mortar allowance) — a continuous thick mortar bed under the beacons would crush the mesh down out of its mid-depth position. Lumps made the evening before, beacons set the next morning once set (avoids wobble/inaccuracy on fresh mortar). Classical laser-level + square method: **~2mm accuracy across the entire apartment footprint** — consistent with this page's existing template-stick technique from an unrelated source, not contradicting it.

**Home-mixed screed recipe and workability technique**: 1 part cement : 2 parts sand by volume, plus a superplasticizer and polypropylene microfiber (60g/100L dosing) mixed in a specific order — water, then plasticizer, then microfiber (into the water, to disperse before dry components), then half the sand (forms a workable "paste" first), mixed once, then the rest of the sand, then rest 5 minutes and mix again. **A demonstrated plasticizer proof**: splitting one stiff, minimal-water batch into two, dosing one half with plasticizer and the other with an equal volume of plain water instead — only the plasticizer half becomes workable, showing the effect isn't just marketing. Home-mixing this way is claimed to cost roughly half of a ready-made bagged screed mix (`single-account`, no absolute figures, not usable for price comparison). Explicitly contrasted with the bad practice of using dish soap or tile adhesive as an improvised plasticizer, or simply over-watering the mix — both degrade final strength. [source: [[_Sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

**Pour/cure practicalities**: cut/trim the still-soft screed to beacon level the *next day* — wait longer and it can only be ground, not cut; wrap all conduit/pipe fittings and crimp rings in corrugated sleeving before the pour so they can move slightly without ever bonding to the screed (same principle already recorded for PEX pipe specifically — see [[12_Engineering_and_Systems/analysis/Radiators_and_Convectors|Radiators & Convectors]]); cure by watering or covering with plastic sheeting regardless of admixture, as extra insurance. Full screed job (excluding the membrane) took about a week with two workers; the membrane itself was installed separately during the electrical stage and took about a day. [source: [[_Sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

## Finish Self-Leveling Layer Over Beacons — Same Project, Episode #27 (added 2026-08-24, Round 5)

Direct continuation of the DIY screed build above (episode #18) — this covers the finish-leveling stage over that same beacon-poured screed, before the beacons themselves are pulled.

**The problem and why self-leveling compound beats tile adhesive for this finish layer**: a thick screed poured between beacons inevitably settles/sags slightly in the strips between them, leaving the beacons protruding above the settled surface — expected, not a mistake, but since floor height is planned to the millimeter it needs a finishing leveling pass before the beacons come out. Tile adhesive can level the floor but leaves it visually rough (coarser aggregate); a **thin-layer self-leveling compound** achieves level *and* smooth, because its aggregate is much finer and the cured material is inherently stronger, using minimal material by volume at this thickness. The speaker states directly he won't go back to tile adhesive for this purpose after trying self-leveling compound. **Named product: Vetonit 3000**, pourable 1-5mm thick, compatible with underfloor heating.

**Priming is not optional before pouring**: a primer film makes the substrate weakly absorbent so the compound spreads/flows properly — skip it and the substrate pulls water out of the fresh mix, risking delamination, cracking, or poor flow. **Named primer, two-coat dilution schedule**: Vetonit MD16 concentrate (≥40% dry residue) — first coat 1:5 (primer:water), second coat 1:3, applied 2 hours after the first, rolled on.

**Mixing and pour technique**: 5.2L water per bag; mix 1 minute; pour, spread with a trowel, drag flat with a straightedge. A whole room: ~30 minutes, 2 bags at this thickness. **Working-window trick**: while still fresh, ridges/bumps can be trimmed with a spatula — once cured, it's too hard to work by hand. **Two-strip pour sequencing for a solo or two-person job**: pour two strips first, skip the edge strip; once those two strips are walkable (~1hr at 3mm thickness), stand on them to pour the remaining edge strip, avoiding an awkward backward crawl while dragging the straightedge toward yourself. Best as a two-person job (one mixes, one screeds). **Pre-pour prep**: grind the cured screed with a diamond cup wheel to remove debris/laitance/protruding aggregate that would catch the straightedge — but never grind down the beacons themselves.

[source: [[_Sources/YT_kXGYTsBTKj8_sidorik_self_leveling_floor_ep27|kXGYTsBTKj8_sidorik_self_leveling_floor_ep27]]]

## Semi-Dry Mechanized Screed: a Real Conversion Story and Quality-Ingredient Checklist (Петришин-Строй, added 2026-08-24, Round 5)

A real practitioner reversal, not a first-time endorsement: the source
states he was originally skeptical of semi-dry mechanized screed after
finding a developer-poured example that crumbled under a fingernail
scratch on a real object — torn out and replaced with classic wet screed
at the time. After later working with competent screed subcontractors, he
now considers semi-dry mechanized screed the best speed/cost option,
**provided it includes**: fiber additive ("фибра"), a perimeter
deformation joint ("демфер"), correct cement grade and quantity, and
correctly graded sand — framed as the difference between the crumbling
example above and a durable result. `single-account`. [source:
[[_Sources/YT_vKMHNYQYWAI_petrishin_top13_expensive_mistakes|YT_vKMHNYQYWAI]]]

## Shumonet (Impact-Noise Underlayment) Material Description (Петришин-Строй, added 2026-08-24, Round 5)

"Шумонет" is a rubberized-top, felt-backed underlayment laid under
flooring specifically to reduce impact/structure-borne noise transmission
to the unit below (dropped objects, footsteps — distinct from airborne
noise); available in "гидро" (waterproof) and "комби" (combined)
variants. `single-account`. [source: [[_Sources/YT_8QBqwydVND8_petrishin_2026_all_stages|YT_8QBqwydVND8]]]

## Semi-Mechanized ("Полуручка") Screed, Cold-Weather/Access Constraints, and a Curing Routine (added 2026-08-24, Petrishin-Stroi trial)

Петришин-Строй (Sergey Petrishin, Moscow-area turnkey company) — object
is a **country house, not an apartment**, and no city/region is named
in this video at all (region: unresolved, weaker than this channel's
usual level-2 Moscow association since the object itself breaks the
channel's normal apartment context). A distinct screed-delivery method
from the fully mechanized pumped screed and the DIY hand-mixed
reinforced screed already on this page:

- **Semi-mechanized ("полу-механизированная," slang "полуручка")
  screed**: the pour truck's pump still delivers the mix via hose over
  distance/height, but the mix itself is batched in the truck's small
  onboard mixer rather than continuously large-batch mixed — slower,
  but usable in situations a full mechanized pour can't handle. **Four
  named reasons to choose it over a full mechanized pour**: apartment
  above the 25th floor (pump can't reach); building management forbids
  bulk sand/cement deliveries; site access won't allow the needed sand
  truck; ambient temperature below +7°C, since a fully mechanized pour's
  mix can freeze inside the delivery hoses in transit at low temperature
  (this job: **-14°C outside**, using bagged premix — "пескобетон" —
  instead of separately-batched sand+cement, since loose sand itself
  freezes at that temperature even though separate sand+cement is
  normally cheaper). A full mechanized pump rig's own purchase cost is
  cited as a practical barrier to owning one: **≈3,000,000 RUB
  (≈$39,700, trailing 6-month USD/RUB average ending 2021-02-14)**.
- **Two concrete tradeoffs**: roughly **2x slower** than a fully
  mechanized pour; somewhat higher material/labor cost when premix
  bagged product is used instead of loose sand+cement, plus more
  airborne dust during mixing. This job: 70 m² floor area, ~7cm
  thickness, 245 bags of premix consumed.
- **Curing routine with concrete numbers, stated as applying to either
  delivery method**: inter-room deformation joints (poured room-by-room
  rather than as one continuous slab) to prevent cracking; cover with
  plastic film starting the day after the pour; every 3-4 days, remove
  the film, wet the whole surface (**≈1-1.5 L water/m²**), and
  re-cover — repeat this cycle until **14 days**, when the film comes
  off for good; avoid significant loads (heavy material staging,
  ladders) for the **first 10 days**, the period when the screed gains
  most of its final strength.
  [source: [[_Sources/YT_E7M-bWWSmfw_petrishin_screed_stages|YT_E7M-bWWSmfw]]]

## Screed Acceptance/QC Checklist — per Петришин-Строй (added 2026-08-24, Round 2)

Same channel as the semi-mechanized-screed video above, but a distinct
general acceptance/QC video, not a delivery-method one — complementary
content, no overlap flagged. Region level 2 (channel-level Moscow
association, slightly reinforced by an explicit "we serve Moscow/Moscow
region" service-area statement in a sales CTA, but that's the company's
own service scope, not a direct statement about this object's location —
does not clear level 1).

- **Staged-payment heuristic**: 50% at start, 50% only after work is
  finished and the result is visible — agree before work starts, not
  mid-job. **A zero-measurement quote is a red flag**: a crew offering to
  show up and pour with no on-site measurement first can't have checked
  pipe/conduit clearances, door-opening height, or whether the target
  thickness will actually work at this site.
- **Screed strength depends on four factors**: sand:cement ratio (some
  crews deliberately under-dose cement to pocket the savings, producing
  cracks), compaction/tamping (skipping it is called the single biggest
  mistake — leaves micro-voids that crack later), target thickness, and
  the drying/curing regimen. **Two field compaction-QC tests**: (1) walk
  the poured screed the next day in rubber "concrete boots" — it should
  not sink or leave footprints; (2) pour water on the surface — on a
  well-compacted screed it sits on top and absorbs gradually rather than
  disappearing quickly into the body.
- **Minimum-thickness recommendation stronger than the nominal
  standard**: the accepted minimum is 4cm, but the company recommends
  **6cm+**, citing a real case of having to demolish a 4cm screed that
  was poured in full technical compliance and still cracked. Where full
  thickness isn't achievable over water/electrical conduits, reinforce
  that section with metal mesh laid over the conduits.
- **A fourth distinct curing-protocol variant for this store, not merged
  with the numbers above (this project's non-blending convention)**:
  cover with damp rags plus heavy watering, then plastic film, for
  **1 week**; check whether the rags have dried out — if so, re-wet and
  re-cover, repeating every **3-5 days** as needed; then let the screed
  dry undisturbed for a further **21 days** to reach full design
  strength.
- **A written-vs-verbal tolerance bait-and-switch warning**: some crews
  verbally quote a generous tolerance (e.g. "2mm per 2m") to win the job,
  then present looser written tolerances once work begins — get the
  tolerance figure in writing before work starts.
- **Final acceptance tooling and tolerances**: 2m straightedge + laser
  level; gap ≤2mm anywhere; a 5-ruble coin pressed into any gap must not
  sink in (same coin-test technique as this channel's plastering-
  acceptance checklist, now applied to floor screed); bubble level on
  the straightedge must read centered everywhere; laser level deviation
  from true horizontal ≤2mm at any point. **Corners are the most common
  defect location**: the power-trowel finishing machine can't reach into
  corners, so they need separate hand-finishing — skipping this leaves a
  detectable level "jump" right at the corner.
- **Deformation-joint detail extending this page's existing screed-joint
  content**: besides perimeter damper tape and joints between rooms, cut
  a **diagonal T-shaped relief cut from every external/outside corner of
  the room** — outside corners concentrate the highest stress in a screed
  slab, and this cut relieves it deliberately.
- **QC-timing rule with a stated cost mechanism**: inspect the screed
  while still fresh/wet — a defect caught then is fixed on the spot; the
  same defect caught the next day (cured) needs a self-leveling top-up
  or grinding, both slower and costlier. Explicitly agree in advance who
  is responsible for watering/covering the screed during curing.
  [source: [[_Sources/YT_Y9PGtPmcMms_petrishin_screed_quality_checklist|Y9PGtPmcMms]]]

## A Physically-Demonstrated Beacon-Precision-to-Floor-Squeak Mechanism (Петришин-Строй, "ЖК Виноградный" episodic series, added 2026-08-24, Round 12)

Real object, 2015-vintage source (oldest processed on this channel to
date). Region level 2. Low promotional ratio. Genuinely new — no prior
source on this page demonstrates this mechanism physically rather than
just asserting it.

- **⚠️ Real cable-under-straightedge demonstration**: to show why beacon-
  setting precision matters, the practitioner places a piece of
  insulated electrical wire (~2.5mm cross-section) under a straightedge
  laid across the finished screed and presses down, visibly showing the
  rocking/flexing gap a 2-3mm beacon-height error would leave under a
  future rigid floor covering (laminate, parquet, solid board) — a
  physical demonstration of the mechanism behind "an uneven screed
  causes floor creaking," not just an assertion of the rule.
- **Real QC result on this object**: a 3-meter straightedge check across
  multiple rooms found deviation under 1mm, credited to the crew's care
  at the beacon-setting stage.
- **⚠️ Hand-poured (non-mechanized), room-by-room screed sequencing
  risk, generalized as a common industry mistake**: pouring screed room
  by room with hand-mixed material (rather than a continuous mechanized
  pour) commonly produces a level mismatch right at the room-to-room/
  corridor threshold, since each room is finished independently. This
  object's execution was praised as an exception (seamless transitions),
  but the underlying risk is stated as common practice generally.
[source: [[_Sources/YT_l4bXbwfOlrU_petrishin_vinogradny_ep7_plumbing|YT_l4bXbwfOlrU]]]

## Finish Build-Up Thicknesses That Set the Screed Level at a Material Change (Надежда Кузина, added 2026-08-31)

**Puts numbers on the qualitative rule already on [[13_Surfaces_and_Finishes/analysis/Flooring_Installation_and_Baseboards|Flooring Installation, Transitions & Baseboards]]** (Петришин-Строй's thickness-direction asymmetry): different finishes have different total build-ups, so the screed reference must be set knowing which finish goes where. Кузина gives the two figures that decision usually turns on. [source: [[_Sources/YT_g252JnMcc3Q_kuzina_flooring_transition_methods|YT_g252JnMcc3Q]]]

- **Tile / porcelain + adhesive ≈ 15 mm total.**
- **Parquet or engineered board + plywood beneath + adhesive between ≈ 30–32 mm.**
- **⚠️ The difference — roughly 15–17 mm — is compensated in the screed**, which is why the sequencing rule bites: *"вы не можете начать укладывать плитку, если вы точно не определились с тем, как у вас будет паркет."* Glued to plywood, glued straight to the screed, or laminate instead — each demands a different screed height on that side of the joint.
- **The decision this forces early**: the flooring transition is bound to three earlier decisions at once — screed level, the finish build-up on *both* sides, and the door swing direction (the joint must land under the leaf). `single-account`, `unverified`, 2020 source; the thicknesses are conventional build-ups rather than a measured project.
