# Flooring Guide - Do's and Don'ts

See [[12_Engineering_and_Systems/analysis/Soundproofing|Soundproofing]] for floor impact-noise soundproofing (named Shumanet products, wall-perimeter isolation technique, floor-vs-ceiling cost asymmetry) and the general soundproofing decision framework.

## Screed Type Selection, Thickness Rules, and the Top-3 Crack Causes (Konstantin Kruglov / Ontario, added 2026-08-28, Round 6)

> [!NOTE]
> First Kruglov-channel screed content on this page — cross-checked against this page's existing screed content (Петришин-Строй's semi-mechanized/acceptance-QC sources, Pavel Sidorik's DIY reinforced-screed build, the sbk.remont developer-screed-defect case below) before writing; several mechanisms corroborate rather than duplicate (mandatory fiber/plasticizer, external-corner T-cuts, gradual-drying discipline) and are not re-recorded. Region level 2, with an explicit "99% of Moscow/Moscow-region apartments" statement. Low promotional ratio. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_SP3NyXmPafI_kruglov_screed_cracking|YT_SP3NyXmPafI]]]

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

## Developer Screed Acceptance Testing — Real Instruments and Thresholds (added 2026-08-28)

> [!NOTE]
> Vladimir Amelchenko / ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, with a guest technical-supervision specialist, real on-camera inspection of a subscriber's new-build apartment — live instrument readings shown, not a studio explainer. `single-account` for the specialist's stated thresholds (not cross-checked against a written building code here), but internally consistent and demonstrated live. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_l0aR7nQGh4M_sbk_screed_inspection_case|YT_l0aR7nQGh4M]]]

This project's first developer-screed acceptance-testing content — what to actually check before accepting a new-build apartment's floors, and what the numbers mean.

- **Two distinct instruments measure two distinct defects — don't conflate them**: a **склерометр** (rebound/impact hammer, 10 shots averaged) measures the screed's **compressive strength class**; a **rotary laser level** maps **surface flatness/level variation** across multiple points. A screed can fail either test independently of the other.
- **⚠️ Worked example from a real inspection**: rebound-hammer average ≈11.3 ("M100" class) — roughly **1/3 below the code norm for residential floors**. A separate pull-off/adhesion test (50×50mm test tabs glued to the surface, torn off with a calibrated instrument) read **0.35 MPa against a 1 MPa norm** for a base intended for laminate, quartz-vinyl, or tile (**parquet's own norm is stricter still, 0.5 MPa** — this screed fails that threshold too). Level-variation: apartment-wide code tolerance is **≈5mm**; this apartment's single corridor alone measured a 0 to -15mm spread across five points, with a separate 2cm (20mm) corner-to-corner difference found in that same corridor.
- **⚠️ Remediation branches by the *planned finish flooring*, not one verdict for the whole apartment**: planning **parquet** → a screed this weak must be fully demolished (won't survive under a rigid wood floor — cracking, delamination, swelling). Planning **quartz-vinyl** instead → the same screed may be salvageable: grind the surface, reinforce with a strengthening compound or an epoxy primer with sand broadcast, then self-level up to 15-20mm on top — a cheaper remediation path, but only for the more tolerant covering.
- **⚠️ Named failure mode if the strength test is skipped**: pouring an overly strong/rigid leveling material directly onto an already-weak screed doesn't fix it — it **tears the weak layer apart**, since the two layers don't flex/fail together under load. The pull-off test exists specifically to choose a *compatible* leveling material, not just to grade the screed pass/fail.
- **⚠️ Developer semi-dry screed (полусухая стяжка) is characterized as structurally one-time-use**, per the specialist's repeated hands-on experience: when tile bonded to it is later removed, the screed crumbles away in chunks with the tile, unlike a properly mixed "wet" screed, which stays intact even after tile removal a decade later — real implication for anyone who might change flooring later.
- **Stated industry-awareness gap**: per the specialist, roughly 90% of builders (not just buyers) don't know this acceptance test exists, how to perform it, or what the consequences of skipping it are.

## Ten-Material Comparison: Selection Framework and Per-Material Mechanisms (added 2026-08-28)

> [!NOTE]
> Vladimir Amelchenko / ДЕЛАТЬ НЕ ПЕРЕДЕЛАТЬ, structured 15-minute comparison of 10 flooring types. Low promotional ratio. `single-account` for the two flagged opinion items (engineered-board scratch dislike, microcement skepticism) — the speaker names these as his own opinion in the transcript. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_DE-4uFYXJQ4_sbk_flooring_types_compared|YT_DE-4uFYXJQ4]]]

- **⚠️ Three-factor selection framework, apply before comparing materials**: (1) **room purpose** — a real cited case: porcelain tile in a budget hotel's guest corridors (chosen by a price-selected designer for "100-year durability") caused audible heel-click noise all night; carpet is the standard choice there specifically for footstep-noise damping, a separate axis from durability. **Commercial-grade vs. residential-grade carpet is a real, distinct product tier**, not marketing — residential-grade in genuinely high-traffic use shows bald patches within 1-2 months. (2) **operating conditions** — e.g. laminate becomes "a house of cards" (warps) under hydronic underfloor heating, while porcelain tile and quartz-vinyl are compatible with it. (3) **budget-segment coherence** — linoleum in a premium-tier renovation, or expensive imported wood in a bare rental unit, are both called internally incoherent regardless of ability to pay.
- **⚠️ Linoleum's subfloor tolerance is a hidden-cost trap**: it's famous for lying over almost any base, but an uneven subfloor's bumps telegraph straight through and can never be hidden afterward — cheap linoleum over a bad subfloor is not real savings once the necessary subfloor work is counted. Must be allowed to "relax"/flatten after unrolling before being fixed at the baseboards, or permanent waves lock in. Genuinely a two-person installation job for any real room size (one person alone struggles physically and risks wall damage), so real installed cost runs roughly double a naive one-person estimate despite a cheap-looking per-unit labor rate. Shrinks over time — trimmed tight at install, it can visibly pull out from under the baseboards after 1-2 years, not restorable.
- **Laminate considered obsolete by this speaker**: cheaper materials (linoleum, quartz-vinyl) have since matched its wood-imitation textures at lower cost and better water tolerance; genuinely expensive laminate price points are better spent on real solid wood instead, per this speaker.
- **⚠️ Quartz-vinyl / porcelain-tile transition cost mechanism**: laminate-on-underlay sits close to porcelain-tile height (often no leveling correction needed at the transition), but quartz-vinyl is thin enough that matching its height to adjacent porcelain tile (e.g. to avoid a bathroom-doorway threshold) can force a **full-apartment self-leveling pour** — a real, non-obvious cost driven by a height mismatch between two otherwise-compatible materials. Dark/monochrome quartz-vinyl shows longitudinal scratches clearly and can't hide them (needs professional restoration) — nuances this store's existing quartz-vinyl material note (`YT_KXmidtaUNxI`), which didn't cover color-dependent scratch visibility. Cheap quartz-vinyl over an imperfect substrate develops loose/creaking locks over time — consistent with this page's own screed-acceptance-testing section above.
- **⚠️ Porcelain tile / ceramic — a real regulatory prohibition, not a design preference**: wall-to-wall porcelain tile across an *entire* apartment is prohibited by soundproofing/impact-noise building code, except on the ground floor with no neighbors below, or in a private (detached) house. Secondary cons: cold underfoot without underfloor heating; glossy finishes are slippery; **installation labor is called the single most expensive of all materials compared**, and a wrong tile color/texture choice is called capable of "ruining a renovation" more than a mistake with any other flooring material.
- **Engineered/parquet board is business/premium-segment only** (price + delicate handling); the speaker's own stated dislike: newly finished boards can show small scratches within a month or two, even before occupancy — flagged explicitly as his personal opinion, not a universal defect claim.
- **Carpet dampens sound and suits young children playing on the floor; small rooms can loose-lay it, larger areas must be glued to avoid wrinkling/trip hazards**; requires regular vacuuming and can harbor dust mites/allergens — a specific caution for allergy-sensitive households.
- **⚠️ Microcement cannot bridge or reinforce substrate micro-cracks**: any hairline crack in the self-leveling layer or screed beneath telegraphs straight through the finished microcement surface and is very difficult to remediate afterward — ironically makes microcement's substrate-prep requirement the most demanding (and expensive) of all materials compared, despite its minimal visual appearance.
- **⚠️ Developer screed defect rate quantified at ≈95%**, failing all applicable code norms — corroborates this page's own screed-acceptance-testing section above; some Moscow developers reportedly skip pouring any screed at all, per this same speaker.

## Transitions, Grain Direction, and Material Cautions — per Zemskov/Zemstandart (added 2026-08-10)

> [!NOTE]
> New topic angle for this page. Two separate Zemskov/Zemstandart sources, `single-account`/`single-account` throughout — one a real 88.5m² project (cited durability/cost claims are his own account, not independently verified against a materials supplier or another installer), the other a general planning livestream with one real cited client case. [sources: `_Archive/processed_sources/20260810_entry_hallway_dividing_wall_case_8963951b.txt`, `_Archive/processed_sources/20260810_never_do_project_in_pieces_873e1532.txt`]

- Zemstandart/Alexey Zemskov reports: an entry-zone floor wears out faster than the rest of an apartment even when water-resistant, because it's a "dirty zone" (tracked-in grit, moisture) — being able to replace flooring in just that zone independently has real value to the source speaker. Without a dividing wall creating a proper door opening, a transition/seam in an L-shaped or irregular zone has to run diagonally or awkwardly, producing a seam that's long, visually prominent, and (the speaker's claim) fails faster the longer it is. **The fix in the cited project**: route the transition through a door opening, terminating at a short (80cm in that case) transition molding anchored to the door frame rather than the baseboard — a texture/seam this short holds firmly and reads as intentional. **General rule stated by the speaker**: the shorter a flooring transition seam, the better it holds and looks — route transitions through door openings rather than across open floor whenever possible.
- Zemstandart/Alexey Zemskov explains: solid/engineered wood flooring (массив) wears unevenly depending on the direction of foot traffic relative to the grain — per the speaker's account it holds up well when boards run parallel to the main direction of movement, and wears unusually fast laid across that direction. In an L-shaped corridor, this means the two legs of the L often need flooring run in genuinely different directions to match their own traffic pattern, which — without a dividing wall — forces an awkward, long diagonal seam where the two directions meet. The speaker's fix: a dividing wall with a door opening lets each leg have its own grain direction, meeting cleanly at the opening's center.
- **Zemskov's cork-flooring-vs-large-dog caution (real cited case)**: a client wanted both a soft cork floor and a large dog; Zemskov told them to choose one, since a large dog's claws would (per his account) shred a cork floor within roughly a week of normal use. The client chose the dog and dropped the cork-floor plan; per Zemskov, the client later thanked him after seeing a friend's cork floor (installed alongside a large dog) reduced to confetti-like debris requiring constant vacuuming. **Treat the "within a week" figure as a single vivid account (`single-account`)**, not a benchmarked test result — the underlying claim (cork is soft relative to dog claws) is plausible but not independently verified here.

## Buying Sequence and Color-Matching — per Zemskov/Zemstandart (added 2026-08-10)

> [!NOTE]
> `single-account`, delivered confidently but not independently benchmarked against a flooring-industry source or another installer in this project's knowledge base. [source: `_Archive/processed_sources/20260810_laminate_selection_and_matching_a51f8dca.txt`]

- **Zemskov's sequencing rule: choose interior doors first, then laminate — never the reverse.** His estimate: the pool of doors that are both visually appealing and within budget is roughly 100× smaller than the pool of acceptable laminate — fitting laminate to an already-chosen door is easy; the reverse is, per Zemskov, practically impossible.
- **Zemskov's baseboard rule**: choose the baseboard immediately after the doors, matched to the **door** color (ideally the same manufacturer/collection), not the floor color — the baseboard should read as a continuation of the door casing.
- **Zemskov's three reasons floor color is now commonly chosen in deliberate contrast to doors rather than matched**: a true color match is harder to find than a pleasing contrast; even a good color match still shows a texture mismatch (different manufacturers, and laminate lies horizontal under different light than a vertical door); and matching three separate categories (floor, door, furniture) across three different manufacturers to one exact color is, per Zemskov, essentially guaranteed to fail somewhere.
- **Zemskov's saturation-matching rule**: keep the saturation/vividness level roughly consistent across an interior's main components — pairing a natural/saturated tone (e.g. "gold oak") with an artificial/muted one (e.g. "bleached oak") is, per Zemskov, an almost-guaranteed visual clash.
- **Zemskov's board-sizing preference**: laminate milled closer to genuine solid-wood board dimensions (smaller than a typical laminate default — his cited classic laminate size ~130×19cm vs. solid wood ~1.5× smaller) reads as more convincingly premium, since laminate exists specifically to imitate solid wood's look.
- **Zemskov's chamfered-edge requirement — flagged as safety-relevant, not just cosmetic.** Any laminate eventually develops small gaps between boards; a chamfered (beveled) edge hides this, while a square edge leaves it visible, catches cloths/socks, and — per Zemskov — can lift slightly at a crack, a real trip/cut risk for a barefoot walker. He states genuinely premium flooring always has a perimeter bevel, and explicitly debunks the "dirt collects in the bevel groove" objection as a myth invented by manufacturers of non-chamfered product.

## Laying Direction, Row-Offset Pattern, and Continuous-vs-Separated Runs — per Zemskov/Zemstandart (added 2026-08-10)

> [!NOTE]
> `single-account`, own stated practice — explicitly contradicts a "standard trade recommendation" this source itself cites regarding laminate. [source: `_Archive/processed_sources/20260810_flooring_layout_and_orientation_rules_4ef67e84.txt`]

- **Zemskov's material-specific continuous-run-vs-separated-per-room rule**: solid wood and engineered/parquet board must **always** be laid separately per room — continuous laying across room boundaries, per Zemskov, guarantees buckling. Ceramic tile (including wood-look) should **always** be laid as one continuous run (doesn't expand with humidity), except across genuinely different tile types/colors. **Laminate is the ambiguous case, and Zemskov explicitly departs from the standard trade advice here** — the usual guidance is cheap-laminate-separate / premium-laminate-continuous (premium is assumed more moisture-stable); Zemskov's own counter-experience: cheap laminate laid continuously across 150m² with zero issues, and a costly premium laminate that had to be split into rooms after installation — "hundreds" of times in his practice, not a rare exception. **His conclusion: any laminate has roughly even odds of buckling regardless of price tier — the real deciding factor is whether the installing crew is reliable and offers an enforceable warranty**, not the laminate's price.
- **Zemskov's laying-direction priority**: along the light (evenly illuminates the pattern, seams read less distracting) or along the traffic direction (wear happens along, not across, seams) — never diagonal, which he calls unjustified (conflicts with both light and traffic direction, wastes material, produces poor doorway offcuts). When one continuous run spans a whole apartment, prioritize light direction overall (window-facing rooms have more total area than corridors), accepting faster corridor wear — modern laminate still takes roughly 7 years to show visible seam wear there under ordinary use. In a genuinely high-traffic space, lay along the traffic direction instead.
- **Zemskov's row-offset pattern, changed on his own projects since 2015**: offset each row by exactly **1/3 of board length** — not the more common 1/2-length "classic"/brick-bond offset, which he stopped using because it produces a visually repetitive dotted cross-joint line every other row; the 1/3 pattern spaces cross-joints two rows apart, breaking up the repetition, while still meeting manufacturers' typical ≥1.5×-width cross-joint-separation requirement. (Offsetting by exactly one board *width* — a third, worse pattern — fails that requirement entirely and produces an unwanted diagonal visual line.) This offset rule does not apply to ceramic tile, which has no structural interlock between pieces.

## Glue-Down Quartz-Vinyl Installation — per Zemskov/Zemstandart (added 2026-08-10)

> [!NOTE]
> The most detailed glue-down flooring installation-technique source in this store to date — 22 specific rules from a livestream, `single-account` throughout, not cross-checked against a manufacturer installation guide. [source: `_Archive/processed_sources/20260810_glue_down_quartz_vinyl_top_15_mistakes_8efd6760.txt`]

- **Acclimation**: let the product sit in the target room a minimum of 2 days (ideally 3) **at the room's actual future operating temperature**, not just "indoors" — Zemskov cites a real case of material acclimated at a weakly-heated 16°C site later buckling once the occupied apartment was heated to a normal 20-23°C, since glued planks (unlike floating floors) have nowhere to expand.
- **Storage**: always flat, never on edge or standing — edge-storage reliably bows planks lengthwise or widthwise.
- **Substrate**: never glue to a gypsum-based self-leveling floor (floating installation only there); clean all paint/plaster debris first; prime even if visually dust-free (2 coats for a two-component primer — Zemskov's claim: no vacuum fully removes bonding-relevant dust); verify moisture ≤5% after the primer dries; verify flatness with a 2m straightedge, max 2mm deviation (a 3mm deviation will show through the finished floor).
- **Temperature**: install at 18-21°C, never above 24°C — installing warm/soft material at a comfortable-feeling high temperature produces guaranteed perimeter gaps once the room later cools to its normal operating temperature. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__VvT9FcNbKY_glue_down_quartz_vinyl_top_15_mistakes|_VvT9FcNbKY_glue_down_qu]]]
- **Direction and open/closed wall**: follow the design project's floor-plan arrows (see the light/traffic-direction rule above); lay full-length planks along the room's "open" wall (visible, no furniture) and hide narrow cut pieces (minimum 50mm) along the "closed" (furniture-blocked) wall. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__VvT9FcNbKY_glue_down_quartz_vinyl_top_15_mistakes|_VvT9FcNbKY_glue_down_qu]]]
- **Sequencing**: strike a centerline from the door opening to the opposite wall; lay the first 3 rows toward the window; work outward, walking only on already-laid rows; within each 3-row block, lay the longest plank on the centerline, cut the next to 1/3 length, the next to 1/2 length (staggers joints per the row-offset logic above), laying row 2 before row 3 for practical reachability. Tape down the first laid planks so subsequent walking doesn't shift them. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__VvT9FcNbKY_glue_down_quartz_vinyl_top_15_mistakes|_VvT9FcNbKY_glue_down_qu]]]
- **Adhesive timing**: wait ~1 hour after spreading before laying (check tackiness by touch, not the package's stated time — humidity/temperature/sun all shift real open time); spread evenly (an uneven thick patch won't cure correctly); never lay onto fully dried adhesive (small areas only can be reactivated with a heat gun; never double-layer). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__VvT9FcNbKY_glue_down_quartz_vinyl_top_15_mistakes|_VvT9FcNbKY_glue_down_qu]]]
- **Plank handling**: shuffle planks across multiple boxes before laying (batch-to-batch color variation causes visible blotches if laid box-by-box); inspect every plank on both faces and all corners before gluing (shipping damage and dust-preventing-adhesion are both common and invisible until checked); never try to slide a pressed plank into position — it bonds instantly, so sight it precisely before lowering. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__VvT9FcNbKY_glue_down_quartz_vinyl_top_15_mistakes|_VvT9FcNbKY_glue_down_qu]]]
- **Tools and waste**: never set tools directly on freshly laid vinyl (scratches) — keep the shipping packaging as a protected surface instead. Save every offcut (glue-down, unlike click-lock, can be flipped/rotated and reused from any edge) — retailers typically sell by exact room area with no waste buffer, so discarding offcuts risks running short of full planks near the end. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__VvT9FcNbKY_glue_down_quartz_vinyl_top_15_mistakes|_VvT9FcNbKY_glue_down_qu]]]
- **Cure**: no foot traffic or use for a minimum of 48 hours after installation. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__VvT9FcNbKY_glue_down_quartz_vinyl_top_15_mistakes|_VvT9FcNbKY_glue_down_qu]]]

## Chain-Hypermarket Spec-Downgrade Scam — per Zemskov/Zemstandart (added 2026-08-10)

> [!NOTE]
> `single-account`, plausible given known general retail-tier-differentiation practices but not independently verified for this specific claim; the source's own recommended alternative (his "Zems Baza" vetted-supplier directory) is self-promotional and flagged, not adopted as neutral guidance. [source: `_Archive/processed_sources/20260810_flooring_hypermarket_spec_downgrade_scam_6f860ac8.txt`]

- **Zemskov's four-channel buying taxonomy**: market-stall vendors (nearly extinct, actually pricier — just resellers); online-only stores with no physical presence (can rebrand overnight to dodge accountability — avoid regardless of price); specialized flooring retailers (highest prices, most aggressive upselling, but real installers + combined product-and-install warranty, and reputation-dependent so unlikely to sell a spec-downgraded product); large chain hypermarkets (**the warning below**).
- **Zemskov's central warning**: a chain hypermarket can sell flooring identical in packaging/branding/name to a specialized-retailer product at 1.5-2× lower price — because manufacturers produce a **"special series"** specifically for that chain, under the same packaging but a deliberately lower spec (his example: wear-class 31 vs. a standard-channel 33), sometimes undisclosed on the packaging and only detectable by close side-by-side spec comparison. Real cited consequences: laminate swelling from two drops of water, quartz vinyl developing odor and wearing fast even without underfloor heating, engineered board warping at a 1.2% humidity swing. **Buying rule**: when a hypermarket price is dramatically below the same-branded specialized-retailer price, treat that gap as the signal to compare wear-class/water-resistance specs line by line rather than assume identical branding means identical product.

## Real Consumer-Dispute Case: Underlayment Mismatch — per Zemskov/Zemstandart (added 2026-08-10)

> [!NOTE]
> Real client case, `single-account` at two removes (client's own account of an independent manufacturer inspector's finding, relayed through Zemskov). [source: `_Archive/processed_sources/20260810_quartz_vinyl_underlayment_dispute_621b3f51.txt`]

- **A client's flooring (recommended by a retail salesperson alongside a matching underlayment, also salesperson-recommended) developed end-joint separation across ~60-70% of its joints within about 3 months of occupancy.** The retailer initially blamed the installation method (claiming a continuous, threshold-free run was the cause) — a claim the client states directly contradicted what he'd been told pre-purchase. After escalating to the distributor and finally the manufacturer directly, an independent manufacturer inspector found the real cause: **the underlayment was too soft (3mm) for this specific flooring type, which required a firmer, thinner (≤2mm) product.** **Buying rule this case supports**: don't accept an underlayment recommendation from a general retail salesperson without confirming it matches the specific flooring product's own spec — an underlayment mismatch can cause visible structural joint separation, not just a comfort difference. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_0mrBnaOU3I0_quartz_vinyl_underlayment_dispute|0mrBnaOU3I0_quartz_vinyl]]]

## Screed-First vs. Walls-First Sequencing — per Zemskov/Zemstandart (added 2026-08-19)

> [!NOTE]
> `single-account`, direct prequel to this vault's existing zero-reference/working-reference content on `13_Surfaces_and_Finishes/Walls_and_Paint.md` and `12_Engineering_and_Systems/analysis/Mounting_Heights_and_Positioning.md` — the two sources form an explicit two-part series (this one uploaded 4 days before the other). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cJLZebMtW7A_screed_or_walls_first_108|note]]]

**The deciding factor is wall construction material, not personal preference or a fixed rule of thumb**: [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

- **Masonry walls (aerated/foam block) → build walls first, pour screed after.** The floor area under a future wall gets filled with cheap, light block material instead of costly, heavy screed — at just 10cm screed thickness on a 100m² apartment, the "wasted" screed volume filling future wall footprints can reach 1-2m³, a real cost/labor difference given how much cheaper and easier aerated block is to place than the equivalent screed volume. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]
- **Drywall-on-metal-frame walls → pour screed first, then build the frame on top.** A metal track profile screwed to an uneven raw subfloor bends to follow that unevenness, producing a visibly bowed wall — screed gives the frame a flat surface to sit on. The same volume-fill economics apply in reverse here too: filling that floor footprint with a stud-and-drywall assembly (especially double-layer with insulation) is more complex/expensive per unit volume than the same footprint filled with ordinary screed. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

**One clean exception to the walls-first-for-masonry default**: a genuinely empty, obstruction-free apartment being poured with a concrete pump truck — there, a single-day full-contour screed pour is unambiguously the right call, since the pump truck removes the practical batching constraints that otherwise erode a "pour everything at once" screed's supposed flatness advantage (see below). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

**Why "screed poured continuously in one operation is flatter" is significantly overstated in practice**: a genuinely continuous single-pour screed is rare without a pump truck (hand-mixed mortar can't physically place several tonnes in one session, so it ends up poured in batches regardless); a genuinely empty apartment is rare too (tools, material bags, and crew facilities occupy floor space); and — the decisive point — nearly all modern finish flooring needs a thin self-leveling correction layer over the screed anyway, which flattens variation up to ~3-8mm regardless of how the screed itself was sequenced, making the end result effectively identical between the two approaches once that layer goes down. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

**Walls-first's own genuine downside, and the fix**: plastering after walls go up inevitably drops mortar onto an already-poured screed, which bonds permanently if not cleaned immediately and later needs jackhammer removal. Build walls, plaster them, *then* pour screed last — this is why the masonry-first sequence above specifically puts screed after plastering, not right after the walls go up. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

**Room-to-room level-transfer error, and a pre-marking technique that closes the gap**: transferring a level reference room-by-room (unavoidable once walls exist) accumulates ~3-8mm of real error across a project. Fix: before any walls are built, while the space is fully open, set up a laser level once at the center and mark reference points at ~1m intervals across the *entire* future apartment footprint — every future room then inherits at least one mark from that single original setup, avoiding the accumulated transfer error a room-by-room re-level would introduce. Mark these points not at an arbitrary height but at exactly 99cm above the corridor's own finished floor level, and mark every surface that won't itself be plastered later (window/door reveals, ventilation shafts, pipe risers) — see [[13_Surfaces_and_Finishes/Walls_and_Paint|Walls & Paint]] for the full zero-reference/working-reference system this height derives from.

**Template-stick leveling technique, useful regardless of which sequencing method is chosen**: instead of repeatedly reading a tape measure against a laser-level plane at each beacon, cut a wooden batten, hold it against the beacon at the room's highest point, and mark the laser's crossing point on the rod once — then level every other beacon by matching the laser line to that single mark, rather than re-reading a tape measure each time. Faster (matching a mark beats reading and comparing a number) and more accurate (a tape measure's blade flexes/bows over distance; a rigid rod doesn't). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cJLZebMtW7A_screed_or_walls_first_108|cJLZebMtW7A_screed_or_wa]]]

## Full DIY Reinforced Screed Build with Sub-Screed Sound Insulation — per Pavel Sidorik (added 2026-08-24, Round 4)

Individual practitioner, own new-build apartment, Belarus (level-1 region — see [[16_Legal_and_Regulations/analysis/Renovation_Permits_and_Approvals|Renovation Permits & Approvals]] for the developer-must-deliver-with-screed law this project is built against). Full self-managed build: partitions and electrical rough-in go in *before* the screed (screed must never touch a partition, to avoid transmitting structural noise into it), then a sub-screed noise-insulation membrane, then XPS, then mesh reinforcement and beacons, then the pour.

**Named sub-screed membrane and structural-vs-airborne noise reasoning**: "Стопзвука М" bitumen-polymer membrane (ТехноСонус) — functionally similar to felt-backed roofing membrane, waterproof, torch-fused at overlaps. His own stated reasoning for adding it at all: **structural noise (impacts, footsteps, furniture) is far easier to stop at its source floor than to absorb from the receiving neighbor's ceiling below** — airborne noise (voices, music) is comparatively easier to treat from the receiving side instead. He checked whether cheap linoleum could substitute for the membrane (similar properties) but found even the cheapest linoleum costs more — no reason to substitute. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

**XPS layer, named product and reasoning**: Технониколь Carbon Eco, 20mm, rated to 10 tonnes/m² distributed load, rough surface for mortar adhesion. Manufacturer-technologist-confirmed (relayed by the practitioner, `single-account`) compatible with the membrane above, and independently rated to absorb 21dB on its own. Using XPS instead of a thicker plain mortar layer cut roughly 2.5 tonnes of dead weight across the apartment while improving sound absorption at no added screed cost. Screed thickness ended up 7cm total (down from the developer's original 10cm) despite adding the membrane, XPS, and rerouted electrical conduit within it — net finished-floor height rose only ~0.5cm after full substrate cleanup. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

**Perimeter damper strip, a genuinely new construction detail**: 15cm strips cut from the same membrane, glued to the wall at final screed height, topped with a second 5mm foamed-polyethylene layer (stapled on) — the extra layer exists because the 5mm membrane alone is thinner than the ~10mm the screed's own linear-expansion movement calls for. Runs the full perimeter of every room getting a screed; trimmed flush and sealed with acoustic sealant after finish work. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

**Mesh reinforcement**: needed whenever screed thickness exceeds 3cm (mortar is strong in compression, weak against linear-expansion stress). 10×10cm cell, 4mm wire, one-cell overlap, tied at every second cell, held mid-depth on ~2.5cm risers cut from scrap pipe or XPS offcuts.

**Expanded-clay (керамзит) lightweight fill under an unusually thick screed, per Петришин-Строй (ЖК Виноградный episodic series, added 2026-08-24, Round 13)**: when a screed must run unusually thick (this job: ~7-8cm, driven by the apartment's own leveling needs) filling the full depth with sand-concrete alone risks overloading the structural slab with dead weight — adding a keramzit (expanded-clay) layer as part of the buildup lightens the total load. Distinct from this page's XPS-substitution approach above (that swaps for sound-absorption + weight reduction with a rated product; this is a lower-cost bulk-fill weight-reduction technique for a plain thick screed). Region level 2 (ЖК Виноградный named, no city spoken). `single-account`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__GL2t3cdSi8_petrishin_vinogradny_ep5_electrical_radiators|_GL2t3cdSi8]]]

**⚠️ Beacon technique that avoids sinkage and preserves mesh position**: set beacons on discrete mortar lumps (not a continuous bed) leveled to 1.5cm below the target screed surface (10mm beacon + 5mm mortar allowance) — a continuous thick mortar bed under the beacons would crush the mesh down out of its mid-depth position. Lumps made the evening before, beacons set the next morning once set (avoids wobble/inaccuracy on fresh mortar). Classical laser-level + square method: **~2mm accuracy across the entire apartment footprint** — consistent with this page's existing template-stick technique from an unrelated source, not contradicting it.

**Home-mixed screed recipe and workability technique**: 1 part cement : 2 parts sand by volume, plus a superplasticizer and polypropylene microfiber (60g/100L dosing) mixed in a specific order — water, then plasticizer, then microfiber (into the water, to disperse before dry components), then half the sand (forms a workable "paste" first), mixed once, then the rest of the sand, then rest 5 minutes and mix again. **A demonstrated plasticizer proof**: splitting one stiff, minimal-water batch into two, dosing one half with plasticizer and the other with an equal volume of plain water instead — only the plasticizer half becomes workable, showing the effect isn't just marketing. Home-mixing this way is claimed to cost roughly half of a ready-made bagged screed mix (`single-account`, no absolute figures, not usable for price comparison). Explicitly contrasted with the bad practice of using dish soap or tile adhesive as an improvised plasticizer, or simply over-watering the mix — both degrade final strength. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

**Pour/cure practicalities**: cut/trim the still-soft screed to beacon level the *next day* — wait longer and it can only be ground, not cut; wrap all conduit/pipe fittings and crimp rings in corrugated sleeving before the pour so they can move slightly without ever bonding to the screed (same principle already recorded for PEX pipe specifically — see [[12_Engineering_and_Systems/analysis/Radiators_and_Convectors|Radiators & Convectors]]); cure by watering or covering with plastic sheeting regardless of admixture, as extra insurance. Full screed job (excluding the membrane) took about a week with two workers; the membrane itself was installed separately during the electrical stage and took about a day. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|hN7szX2re2c]]]

## Finish Self-Leveling Layer Over Beacons — Same Project, Episode #27 (added 2026-08-24, Round 5)

Direct continuation of the DIY screed build above (episode #18) — this covers the finish-leveling stage over that same beacon-poured screed, before the beacons themselves are pulled.

**The problem and why self-leveling compound beats tile adhesive for this finish layer**: a thick screed poured between beacons inevitably settles/sags slightly in the strips between them, leaving the beacons protruding above the settled surface — expected, not a mistake, but since floor height is planned to the millimeter it needs a finishing leveling pass before the beacons come out. Tile adhesive can level the floor but leaves it visually rough (coarser aggregate); a **thin-layer self-leveling compound** achieves level *and* smooth, because its aggregate is much finer and the cured material is inherently stronger, using minimal material by volume at this thickness. The speaker states directly he won't go back to tile adhesive for this purpose after trying self-leveling compound. **Named product: Vetonit 3000**, pourable 1-5mm thick, compatible with underfloor heating.

**Priming is not optional before pouring**: a primer film makes the substrate weakly absorbent so the compound spreads/flows properly — skip it and the substrate pulls water out of the fresh mix, risking delamination, cracking, or poor flow. **Named primer, two-coat dilution schedule**: Vetonit MD16 concentrate (≥40% dry residue) — first coat 1:5 (primer:water), second coat 1:3, applied 2 hours after the first, rolled on.

**Mixing and pour technique**: 5.2L water per bag; mix 1 minute; pour, spread with a trowel, drag flat with a straightedge. A whole room: ~30 minutes, 2 bags at this thickness. **Working-window trick**: while still fresh, ridges/bumps can be trimmed with a spatula — once cured, it's too hard to work by hand. **Two-strip pour sequencing for a solo or two-person job**: pour two strips first, skip the edge strip; once those two strips are walkable (~1hr at 3mm thickness), stand on them to pour the remaining edge strip, avoiding an awkward backward crawl while dragging the straightedge toward yourself. Best as a two-person job (one mixes, one screeds). **Pre-pour prep**: grind the cured screed with a diamond cup wheel to remove debris/laitance/protruding aggregate that would catch the straightedge — but never grind down the beacons themselves.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_kXGYTsBTKj8_sidorik_self_leveling_floor_ep27|kXGYTsBTKj8_sidorik_self_leveling_floor_ep27]]]

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
[[11_Budget_and_Planning/_supporting/knowledge/sources/YT_vKMHNYQYWAI_petrishin_top13_expensive_mistakes|YT_vKMHNYQYWAI]]]

## Shumonet (Impact-Noise Underlayment) Material Description (Петришин-Строй, added 2026-08-24, Round 5)

"Шумонет" is a rubberized-top, felt-backed underlayment laid under
flooring specifically to reduce impact/structure-borne noise transmission
to the unit below (dropped objects, footsteps — distinct from airborne
noise); available in "гидро" (waterproof) and "комби" (combined)
variants. `single-account`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8QBqwydVND8_petrishin_2026_all_stages|YT_8QBqwydVND8]]]

## Parquet-Gap Sealant as a Budget Alternative to Full Refinishing (Петришин-Строй, added 2026-08-24, Round 5)

For an old parquet floor with gaps/squeaks but not genuinely worn-out
finish: full refinishing (sanding + lacquer or oil recoat) costs
**150,000-200,000 RUB minimum (≈$1,900-$2,500, trailing-six-month
USD/RUB average 80.0023 ending 2026-02-08)** plus several days of dust
and noise. A flexible, wood-tone-matched parquet gap sealant/caulk fills
board gaps (stopping dust accumulation) without sanding the boards
themselves, at a fraction of the cost — described as "80% of the result
for 20% of the price" specifically for gap/squeak complaints, not a
substitute for genuinely worn-out flooring finish. `single-account`.
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_izhaUHRKViw_petrishin_quality_cosmetic_reno|YT_izhaUHRKViw]]]

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
  [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_E7M-bWWSmfw_petrishin_screed_stages|YT_E7M-bWWSmfw]]]

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
  [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_Y9PGtPmcMms_petrishin_screed_quality_checklist|Y9PGtPmcMms]]]

## Five-Material Flooring Comparison and a Real Screed-Buildup Cost Trap (Петришин-Строй, added 2026-08-24, Round 3)

Region level 2 (channel-only Moscow association). Low promotional
ratio. **First general five-material pros/cons comparison on this
page** — prior content here is technique-heavy (glue-down installation,
layout, screed sequencing), not a structured material-vs-material
overview.

- **Laminate**: fast/clean click install, budget-friendly, comfortable/
  less injury-prone than tile. Badly water-intolerant (unwiped water
  swells it within 2-3 days, unrepairable except replacing panels — not
  practical for kitchen/bathroom/hallway); needs a flat substrate;
  **poor thermal conductivity, not suitable for heated floors**;
  temperature swings can dry it out and open plank gaps; cheap budget
  product can delaminate over time.
- **Quartz-vinyl / SPC**: water-resistant (hallway/kitchen/bathroom-safe,
  doesn't swell); continuous threshold-free runs (no thermal "tenting");
  wide modern design range; **⚠️ most manufacturers claim heated-floor
  compatibility, but always verify the exact rated max temperature on
  that specific manufacturer's own spec sheet, not the general claim**;
  simple to install correctly, available at every budget. Thin material —
  transitioning to tile needs a self-leveling pour or stepped screed;
  more substrate-flatness-sensitive than laminate (click-lock failures
  on an uneven subfloor).
- **Linoleum**: modern "comfort segment" product looks good despite the
  material's old-Khrushchevka association; water-resistant, cheaper than
  quartz-vinyl, soft/comfortable barefoot, stays warm-feeling even
  unheated; tolerates a less-than-perfect subfloor. "Photocopies" every
  subfloor bump/dip visibly if laid over an uneven base; heavy/bulky
  roll genuinely needs two installers; shrinks/pulls from under
  baseboards with temperature swings; **cannot be laid as one
  continuous threshold-free run** — always needs transition thresholds.
- **Tile**: durable (minimum 20-year cited service life), fully water-
  resistant, best thermal conductivity of the five when paired with a
  heated floor. Cold/injury-risk underfoot without heating; tiling
  labor is one of the most expensive renovation line items, and
  installation is dusty/messy/slow.
- **Solid/engineered wood board or parquet**: an emotional/tactile
  choice over a practical one — beautiful, eco-friendly, high-status,
  no imitation matches real wood's feel. Expensive material and
  install; temperamental (scratches, water-sensitive, needs care);
  temperature/humidity swings can cause localized warping.

## Kitchen-Specific Worst-to-Best 8-Material Flooring Ranking (Konstantin Kruglov / Ontario, added 2026-08-28, Round 6)

> [!NOTE]
> Cross-checked against this page's existing Kodolov comparison directly below (laminate/engineered board/quartz-parquet, composition/formaldehyde/price/heated-floor) — largely new ground: a structured worst-to-best kitchen-specific ranking across quartz-parquet, engineered board, parquet board, porcelain tile, MSPC composite, LVT, SPC, and moisture-/water-resistant laminate, with hardness ordering and chip-vs-scratch differentiation not previously on this page. See also [[03_Kitchen/Kitchen_General]] for the kitchen-context pointer. Region level 2 only. Low promotional ratio. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_2Yjg4dAGJI8_kruglov_best_kitchen_flooring_2026|YT_2Yjg4dAGJI8]]]

- **Hardness ordering, softest to hardest underfoot**: LVT → SPC → MSPC → laminate → porcelain tile — underlies the rest of this ranking's breakage-risk and comfort judgments.
- **⚠️ Quartz-parquet ranked worst (8th) for kitchen use**: thin natural-wood veneer scratches quickly regardless of claimed protective lacquer, especially in a kitchen's harsher environment. **New concern**: the SPC base has minimal linear-expansion while the glued-on wood veneer has a meaningfully higher expansion coefficient — how the two bonded layers perform together long-term is an unknown, the material being too new for a track record.
- **Engineered board (7th) and parquet board (6th)**: most barefoot-comfortable of all, but scratches/dents easily and is **the single worst material for staining** (wine/borscht/pomegranate juice absorb readily if not wiped within minutes). No locking mechanism (glue-down only) — extra install cost, but glue-down lets heavy cabinetry sit on it safely, unlike a floating installation. Engineered board ranks below parquet board specifically because its typically larger board format makes warping more visually obvious.
- **⚠️ Parquet board's floating-installation furniture prohibition**: parquet board can install glued or floating; when floating, manufacturers explicitly prohibit heavy furniture/cabinetry — insufficient expansion clearance under a fixed load risks tenting, seam separation, or lock breakage.
- **Porcelain tile ranked surprisingly low (5th/worst-category) despite being 2nd-most-popular by usage**: cold underfoot (no underfloor heating assumed), highest hardness → most breakage risk and most dangerous to fall on, uncomfortable for long standing (flat-foot/plantar strain), slip risk (most porcelain tile lacks anti-slip finish). **Subjective criterion explicitly stated**: doesn't convey coziness — a real tension with the open-plan kitchen-living trend, since a continuous tile floor reads cold/commercial while zoning it creates a dated-looking transition seam.
- **⚠️ MSPC composite flooring, first mention on this page**: mineral-stone base + iron-ore additive, topped with a melamine-paper wear layer (same family as laminate's, not the polyurethane layer typical of LVT/SPC) — most scratch-resistant of the quartz-vinyl-adjacent family, though its rigid base can chip at an impact point (repairable with wood filler). 100% waterproof. **⚠️ Named-brand exception**: the "STN" brand maintains warranty even with heavy furniture on a floating-installed MSPC floor — the only such case found among floating-floor products surveyed. Visual caveat: noticeably smaller edge chamfer than standard laminate/SPC.
- **⚠️ Universal quartz-vinyl-family deformation-gap rule**: every variant (LVT/SPC/MSPC) still requires a manufacturer-specified wall expansion gap despite "insignificant" linear expansion. **Correct-but-rarely-followed sequencing**: install cabinetry first, then run flooring only to the cabinet toe-kick, concealing the gap there — in practice almost all installers instead lay the floor continuously and ignore this.
- **LVT (10-20% stone chip+polymer, 75-90% PVC+additives)**: softest/most comfortable of all, 100% waterproof, needs a genuinely flat substrate (uneven base chips the lock). **Scratch-vs-chip tradeoff**: least scratch-resistant of the family (polyurethane layer scratches easily) but essentially no chip risk (soft PVC) — the inverse of MSPC.
- **SPC (≈70% mineral, ≈30% PVC+additives)**: harder than LVT, softer than MSPC; 100% waterproof; chip risk between LVT and MSPC; scratches more easily than laminate but less than any real-wood-veneer product.
- **Cross-material visual-realism claim**: modern SPC/LVT rarely distinguishable visually from genuine wood-veneer parquet/engineered board even by a specialist — tactile inspection can reveal the difference to a professional, an ordinary homeowner likely can't tell even by touch.
- **⚠️ Water-resistant laminate's rated water-contact window**: manufacturer-claimed continuous tolerance of **24-72 hours** for genuinely water-resistant (not merely moisture-resistant) laminate.
- **⚠️ Laminate's de jure vs. de facto conflict, named explicitly**: laminate is floating-installed and manufacturers prohibit heavy cabinetry loading on it (voids warranty), but real-world field practice shows it performs fine under kitchen units anyway — the presenter's stated reason for ranking laminate his overall #1 "de facto" pick despite being technically disqualified "de jure" by the same rule every quartz-vinyl variant is held to.
- **Laminate scratch/chip verdict**: almost impossible to scratch vs. any quartz-vinyl variant, but more scratch-prone than porcelain tile.
- **⚠️ Presenter's own top-pick recommendation, distinct from the "de facto winner"**: MSPC composite is his personally stated most objectively optimal kitchen-flooring choice, flagged as currently underappreciated only because it's new to market, not for any performance shortfall found in this comparison.

## Laminate vs. Engineered Board vs. Quartz-Parquet: Composition, Health, and Heated-Floor Comparison (added 2026-08-25, Sergey Kodolov)

A dedicated three-way comparison, scored across several dimensions with
explicit reasoning (not just a verdict) — Kodolov, multi-city Russia +
Dubai company, RUB pricing, 2024:

- **Composition**: laminate = wood-fiber particle board + printed image
  layer + lamination, no real wood. Engineered/parquet board = plywood
  base + genuine natural-wood veneer top + protective coat. Quartz-
  parquet = **75% stone (SPC) + 25% PVC** base + genuine natural-wood
  veneer top + protective coat.
- **⚠️ Formaldehyde emission — a real cross-material comparison,
  counter-intuitive result**: laminate's tested emission was **~26×
  higher** than quartz-parquet's; engineered board — despite looking
  "most natural" — can legally emit *more* than laminate, because its
  plywood base's adhesive is rated on the same E1/E2 system as laminate,
  not automatically cleaner. Ranking (all three legally compliant):
  quartz-parquet lowest, laminate 2nd, engineered board highest.
  Emission increases when underfloor heating is added beneath a
  material (heat accelerates outgassing) — most relevant to laminate.
- **⚠️ Water-damage recovery, a real mechanism**: laminate swells and
  breaks apart when flooded — not repairable, forces full replacement
  plus collateral baseboard/wallpaper demolition. Engineered board
  "tents" (buckles upward) rather than disintegrating — repairable in
  place (relief kerfs + relay + adhesive injection). Quartz-parquet's
  SPC/stone base isn't water-absorbent at all. Ranking: quartz-parquet
  1st, engineered board 2nd, laminate 3rd.
- **Price ranges (RUB/m², 2024)**: laminate ≈1,000-3,000; engineered
  board ≈4,000-7,000 (up to ~10,000 still not "ultra-premium"); quartz-
  parquet ≈4,000-6,000, exotic veneers (walnut, wenge) to ~7,000.
- **Seamless installation area, a specific number**: SPC-based quartz-
  parquet can run continuous up to **144m², max 12m per side**, before
  needing an expansion break — second only to porcelain tile. Laminate
  and engineered board should stay per-room (differential expansion is
  proportional to run length — a long and a short room sharing one
  continuous run expand by different absolute amounts regardless of
  material).
- **⚠️ Heated-floor suitability — disagrees with this page's existing
  laminate verdict above, flagged as a live disagreement**: this page's
  existing five-material comparison states laminate has "poor thermal
  conductivity, not suitable for heated floors." Kodolov's direct
  counter-claim: laminate actually transmits heat *well* and is
  technically well-suited to heated floors — but he personally avoids
  it under a heated floor for a **different** reason: heat measurably
  increases its formaldehyde emission, a tradeoff he wouldn't accept for
  a household with children/elderly residents (calls it a reasonable
  individual choice for an adult-only household otherwise). Both
  laminate claims can't be true as stated ("poor conductivity" vs.
  "transmits heat well") — recorded as an unresolved cross-source
  conflict rather than silently picking one; the formaldehyde-under-
  heat caveat is new information either way. Engineered board's wood
  layer insulates, reducing heated-floor efficiency (usually not
  installed under it for this reason). Quartz-parquet's stone base has
  the best heat transfer of the three.
- **⚠️ Wear-layer/finish maintenance — new distinction**: engineered
  board's visible "wood" is never actually touched underfoot — a
  coating on top wears unevenly by traffic pattern. Four named coating
  types in two tiers: water-based lacquer and synthetic-oil-resin
  lacquer (thinner, closer feel to real wood, need re-coating roughly
  every ~6 months); solvent-free polyurethane lacquer and acid-curing
  lacquer (thicker, far more durable — cited up to ~50 years — but fully
  seal the wood under a film). Quartz-parquet ships with 7 protective
  layers and no refinishable variant ("unkillable, no choice"). Laminate
  has no wood to maintain at all.
- **Quick facts**: density ≈1 tonne/m³ (laminate, engineered board) vs.
  **≈2 tonnes/m³ (quartz-parquet)**; engineered board and quartz-parquet
  can be custom-painted any color (real wood veneer surface); laminate
  cannot. **Quartz-parquet is explicitly usable in a bathroom/wet
  installation; the other two are not.**
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_lYVb5LwixM0_kodolov_flooring_comparison|lYVb5LwixM0_kodolov_flooring_comparison]]]

**⚠️ Real named cost-driver: uncoordinated screed level vs. finish-
flooring buildup, cited as costing a client 150,000-300,000 RUB
(≈$1,900-$3,700) unnecessarily**: pouring the whole screed to one flat
level without accounting for each zone's different finish-flooring
buildup (worked example: porcelain tile ~1.3-1.5cm total buildup vs.
quartz-vinyl at only 3-5mm) leaves a real height mismatch once both
finishes are laid. Two after-the-fact fixes, both worse than avoiding
the problem: a transition threshold (a real trip/annoyance point people
remember as a sign of poor renovation), or raising the thinner zone
with self-leveling compound across its whole area (real cited price
**from 1,000 RUB/bag, ≈$10**, cost scaling directly with area — easily
150,000-200,000 RUB/≈$1,900-$2,500 in material alone for one zone,
before labor). **The actual fix**: at the screed-pouring stage, tell the
crew each zone's exact planned finish-flooring buildup so some rooms
are deliberately poured lower than others from the start — solves the
problem for free instead of costing thousands of dollars later.

**Company expert's own solid-wood preference, with reasoning distinct
from the general comparison above**: despite professionally working
mostly with laminate/quartz-vinyl in recent years, chose solid oak
board for his own home (12-13 years in use). Three named reasons: (1)
glued installation (to plywood or screed, quality two-component
adhesive) creates a genuinely monolithic feel that even the best
floating laminate/quartz-vinyl never fully achieves; (2) personal
preference for how solid wood feels barefoot; (3) **refinishing
("циклёвка") capability** — after ~5-10 years, the top ~2-3mm worn
layer can be sanded off and fully recolored, producing a "whole new
renovation" feeling without demolition. Engineered-board price scales
with the thickness of its real-wood top veneer, which is what
determines how many refinish cycles it can tolerate.
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_96mlkQoczI4_petrishin_flooring_2026_comparison|96mlkQoczI4]]]

## Laminate Selection Criteria, In-Store Sample Distortion, and a Baseboard-Fixation Reality Check (Петришин-Строй, added 2026-08-24, Round 8)

- **Laminate selection criteria stated explicitly**: bevel type (4-sided
  beveled edge on every plank vs. 2-sided or none — check before buying,
  it changes the finished look), wear class (example: class 33), and
  thickness (8-10mm examples compared against 12mm). A textured
  "artificially aged" wood-grain finish was rejected in favor of a
  smoother matte-oil-look finish once compared as a real flat sample.
- **In-store angled display samples distort how a floor will actually
  look**: a plank shown tilted under a showroom's directional lighting
  reads differently once installed flat under real room lighting —
  lay a sample flat (ideally bring a real plank home to test in-room)
  rather than trusting an angled display.
- **Wood-plastic composite decking ("терасная доска") for a balcony,
  chosen for weather-durability across non-summer seasons**, and noted
  as usable cost-effectively for general balcony flooring, not just
  deck-edge trim. Real price point: ≈968 RUB per 3m plank (2019).
- **Baseboard fixation reality-check, a repeated real-world finding**:
  manufacturer-recommended plastic mounting clips underperform in
  practice; installers instead secure baseboards with dedicated screw
  anchors ("шпильки") plus adhesive for a genuinely secure mount.
- [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_Rm0aHk4flxc_petrishin_finishing_materials_shopping|Rm0aHk4flxc]]]

## Floor-Level-Transition Planning and a Thickness-Direction Asymmetry (Петришин-Строй, added 2026-08-24, Round 8)

Floor-level-transition planning must account for finish-covering
thickness at the rough/leveling stage, not after: parquet, tile, marble,
and PVC flooring all have different thicknesses, so the rough-floor
leveling reference must be set knowing which finish covering goes where,
planned from the very start of the leveling stage. **A stated direction
asymmetry**: going from a thicker to a thinner finish material is easy
(the rough level can simply be built up higher without issue); going the
other direction (needing the level to drop) is much harder — it requires
demolition/grinding of already-placed material, genuinely difficult
regardless of dust-control measures taken.
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_KlIQxR3vWU8_petrishin_finishing_tips_montage|KlIQxR3vWU8]]]

## Carpet (Ковролин) — Rarely Used in Residential Apartments (Петришин-Строй/Mosbuild expo, added 2026-08-24, Round 10)

`single-account`, trade-fair source, region unresolved. **Carpet is
rarely chosen for a Russian apartment**, mainly relegated to hotels:
high foot traffic soils it quickly, installation quality is
inconsistent, and bacteria/insects can colonize it over time — more
durable alternatives (quartz-vinyl, laminate, parquet, engineered board)
are chosen instead for residential use, with carpet staying more common
in bedrooms/children's rooms in a hospitality setting than in a typical
apartment. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_k9CrEU5RuIE_petrishin_flooring_baseboard_mosbuild_expo|k9CrEU5RuIE]]]

## Baseboard Selection — Cable Channel, Tile-Corner Trim, and a Width/Expansion-Gap Coordination Rule (Петришин-Строй/Mosbuild expo, added 2026-08-24, Round 10)

`single-account`, trade-fair source, medium promotional ratio, region
unresolved.

- **Cable-channel baseboard**: a baseboard with a **built-in cable
  raceway**, distinct from a plain plastic baseboard's incidental
  wall-gap routing (see the RemProektMD note on [[13_Surfaces_and_Finishes/analysis/Doors_Trim_Cost_and_Buying|Doors, Trim: Cost & Buying]]) — lets a budget renovation add
  low-voltage wiring (network, phone, TV) into a room later without
  chasing/cutting into the wall.
- **White plastic baseboard (~8cm rectangular profile)** recommended for
  Scandinavian-style interiors: doesn't yellow/darken over time (8-10
  year no-yellowing warranty cited on a Polish import product), corner
  caps don't detach, paint finish resists cleaning chemicals, and can be
  repainted if desired.
- **Tile external-corner trim, a thickness ladder matched to tile
  format**: profile thickness options (~8mm/10mm/12mm) correspond to
  different tile thicknesses/formats. Material choice is a cost/
  aesthetic tradeoff: thin aluminum (cheaper) vs. thicker galvanized
  metal, and unplated color-matched aluminum (blends into the tile) vs.
  chrome/brass-plated trim (a deliberate shiny accent, pricier).
- **⚠️ Baseboard-width-to-expansion-gap coordination rule**: a laminate/
  engineered-board floor's thermal expansion gap ("термошов") at the
  perimeter/pipe penetrations typically runs 8-12mm but varies
  installer-to-installer by several millimeters — a too-thin baseboard
  sole can leave that gap visible if execution isn't perfectly even.
  **Specify the exact baseboard width and foot depth in the design
  project itself**, so the flooring crew knows in advance how much
  irregularity the baseboard will actually cover (a ~30-32mm-wide
  baseboard with adequate foot depth comfortably covers even a sloppy
  ±1cm gap variance) — rather than both trades separately assuming "the
  baseboard will cover it" with no shared number.
- **Decorative pipe/riser escutcheon collars ("гребёнки")**: trim rings
  in multiple colors specifically to close the expansion-gap/cosmetic
  seam around a heating-pipe riser passing through laminate,
  quartz-vinyl, or parquet — matched to the flooring finish color.

[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_k9CrEU5RuIE_petrishin_flooring_baseboard_mosbuild_expo|k9CrEU5RuIE]]]

## Seven-Baseboard-Type Comparison: Cost, Concealed-Door Compatibility, Wear, and Cleaning (Konstantin Kruglov / Ontario, added 2026-08-28, Round 7)

> [!NOTE]
> First structured, comprehensive baseboard-type comparison for this store — cross-checked against this page's existing Petrishin-Строй/Mosbuild baseboard content (cable-channel baseboard, white plastic Scandinavian recommendation, tile-corner-trim ladder, expansion-gap coordination rule) and `13_Surfaces_and_Finishes/analysis/Concealed_Door_Considerations.md`'s existing shadow-gap-baseboard cost/schedule content — no direct overlap; this comparison is new in both breadth and structure. Region level 2 only. Low promotional ratio. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_a-e5f7yQDRY_kruglov_baseboard_types_2024|YT_a-e5f7yQDRY]]]

- **Three-function framework**: (1) cover the flooring-to-wall gap (some flooring types leave none at all); (2) protect that junction zone from mechanical damage during ordinary use — otherwise the fastest-damaged part of any wall; (3) for **floating** flooring specifically, the baseboard's weight/pressure holds the floor's edge down against the substrate through its thermal expansion/contraction cycle. A fourth, purely visual function (perceived floor/wall boundary) is explicitly called secondary/non-essential.
- **⚠️ Seven-baseboard-type taxonomy**: PVC/plastic (often with integrated cable channel); rigid pre-finished family — MDF, veneer, duropolymer, polyurethane foam (~90% of all baseboards installed, per the source); tile baseboard (cut from the floor tile itself); concealed-mount baseboard (flush with the wall, still functionally a baseboard); **shadow baseboard/profile — stated to not actually perform the baseboard function at all**, more a stylistic reveal/gap; aluminum baseboard (rare); micro-baseboard/corner strip (simple L-angle profile).
- **⚠️ Install-cost ranking**: cheapest — PVC. Mid — aluminum, the rigid pre-finished family, micro-baseboard/corner. Next tier — tile baseboard (factory-mitred top edge, more skill/labor). **Most expensive by far — shadow baseboard and concealed-mount baseboard** — both need a wall niche cut first, internal support installed, and a perfectly straight finished edge along the entire room perimeter; concealed-mount additionally needs its insert painted before final mount.
- **Material-cost ranking**: cheapest — PVC. Mid — tile baseboard (extra tile + mitre waste), the rigid pre-finished family (cheap, most popular), micro-baseboard/corner. Most expensive — concealed-mount, shadow, and aluminum baseboard (pricier materials to manufacture).
- **⚠️ Concealed (flush-mount) door compatibility, extends this project's existing Concealed-Door content** (see [[13_Surfaces_and_Finishes/analysis/Concealed_Door_Considerations|Concealed-Door Considerations]]): compatible types must be thin or flush — shadow baseboard, concealed-mount baseboard, aluminum (only a few mm proud), micro-baseboard/corner. **Incompatible**: PVC, the rigid pre-finished family, and tile baseboard — these protrude far enough to catch the door leaf during opening; can be notched around but never allow full swing.
- **⚠️ Wall-prep-quality-needed ranking**: least demanding — tile baseboard and PVC (flexes to hide even a semicircular curve). Middle — the rigid pre-finished family and micro-baseboard/corner. Also demanding — shadow and concealed-mount baseboard (a long, straight rigid ~3m bar shows any wall waviness through the puttied joint). **Most demanding — aluminum baseboard**: an 8-10cm-tall plate glued directly to the wall with no recess to hide behind; any irregularity shows through and can never be puttied away afterward.
- **⚠️ Wear-resistance ranking**: most durable — plastic/PVC (with quality corner fittings — cheap caps can pop off from a single kick) and tile baseboard (both effectively indestructible over decades). Mid-tier — the rigid pre-finished family (wear/dulling after ~10-15 years, typically beyond a renovation's expected lifespan), micro-baseboard/corner. Least durable — concealed-mount (its painted insert visibly wears/dulls from repeated light contact, uncleanable back to original) and aluminum (scratches from the slightest sharp contact). Shadow profile scores as not really applicable to this criterion at all, per the source's own framing.
- **⚠️ Ease-of-cleaning criterion, exists specifically because of shadow profile/baseboard**: no robot vacuum, ordinary vacuum, or hand can effectively reach into its narrow recessed gap — dust accumulates heavily and is extremely difficult to remove even by hand.
- **Presenter's own recommendation, extends this project's existing shadow-gap-baseboard skepticism (Concealed_Door_Considerations.md) with an independent critique**: personal top pick is the rigid pre-finished (MDF/duropolymer) family; PVC only for a rental/flip or tight budget; tile baseboard called outdated; aluminum "not needed"; concealed-mount "costs like an airplane wing" and still wears quickly; shadow profile draws the harshest framing of all seven.

## Cork Flooring — Prep and Installation Technique (Петришин-Строй, added 2026-08-24, Round 11)

**First cork-flooring-specific source on this page.** Real product
identified: Maestro Club brand, "Ronda" collection, ≈90cm × 29.5cm
planks. Most content below is presented by the practitioner as a
universal floating/click-lock flooring rule (equally applicable to
laminate and engineered board), with cork-specific rationale called out
separately. 2016-vintage source, region level 2 (no city/development
named).

- **Sub-floor flatness spec, a second data point distinct from this
  page's existing Zemskov rule**: verified with a **3-meter straightedge**,
  max deviation **2-3mm** — the existing laminate/engineered-board rule
  elsewhere on this page uses a shorter 2m straightedge with a stricter
  2mm maximum; recorded as a second real-world spec, not merged with the
  existing one (different check span).
- **Priming rationale**: primer is applied after cleaning specifically
  because it seals in the micro-dust particles a vacuum or broom can't
  fully remove — the primer layer is the actual dust-control step.
- **PVC vapor-barrier film step**: rolled out across the whole floor
  after the primer cures and before the impact-noise underlayment —
  per most manufacturers' own instructions, and so any residual
  construction moisture in the screed escapes toward the room's
  perimeter instead of being trapped under the flooring. **Cork-specific
  benefit**: also isolates cork from a rough cement-sand screed's
  texture, extending service life.
- **Last-board-width planning rule**: if the final board at the far wall
  would come out narrower than ~5cm (too narrow for its click-lock
  mechanism to engage cleanly), the *first* row is cut roughly in half
  instead, producing symmetric partial boards at both ends of the room.
- **⚠️ Thermal expansion gap, a second numeric figure**: minimum **4-5mm**
  around the entire perimeter — skipping it risks visible buckling
  within days to ~1.5 months. This page's existing Round 10 baseboard
  note cites a typically-*executed* gap of 8-12mm (installer variance,
  covered by baseboard width) — a stated minimum spec vs. a typically-
  executed range, not a contradiction, but recorded as a second data
  point.
- **Spacer-wedge technique**: cut pieces of the same flooring material
  as spacers for straight, true walls; tapered wedges of varying
  thickness for walls with real deviation, to keep the perimeter gap
  consistent either way.
- **Joint sealant technique**: applied to board joints to block moisture
  ingress; excess cures in ~7-10 minutes and peels off cleanly like a
  film, leaving no residue.
- **⚠️ Seam-offset rule, numeric**: stagger between adjacent rows' end
  joints must be **at least 15-20cm**, or the joint risks squeaking and
  gap development over time.
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_4O1UqRqpApw_petrishin_cork_flooring|YT_4O1UqRqpApw]]]

## Laminate Deep-Dive: Composition, Lock-Type Taxonomy, and Buying Vocabulary (Konstantin Kruglov / Ontario, added 2026-08-28, Round 7)

> [!NOTE]
> Cross-checked against this page's existing Zemskov (buying sequence, chamfer, board sizing) and Kodolov (composition/formaldehyde/heated-floor comparison) laminate content before writing — largely new buying vocabulary neither source covered (lock-mechanism types, HDF density, wear-class-series taxonomy, embossing, named brand tiers). Region level 2 only. Low promotional ratio. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_I4cUb68iZUg_kruglov_laminate_whole_truth|YT_I4cUb68iZUg]]]

- **⚠️ Named regulatory code citation for subfloor flatness before laminate, first for this store**: СП 71.13330 ("Изоляционные и отделочные покрытия," п.8.7) sets a legal maximum subfloor deviation of **2mm per 2 running meters**; laminate manufacturers themselves recommend going further, to **1mm per 2m** — legally compliant and manufacturer-recommended are two different bars.
- **Self-leveling layer over screed also protects the laminate itself, a mechanism distinct from height-matching**: laminate is a "living floor" that moves slightly during use; without a leveling layer, the screed's own coarse sand-concrete aggregate can gradually abrade the laminate's underlayment from below.
- **Four-layer composition, more granular than this page's existing Kodolov entry**: top wear layer (acrylic/melamine resin, the main durability driver) → decorative print layer (pattern only) → HDF core (governs lock durability and load resistance) → bottom stabilizing layer (paraffin-impregnated cardboard/plastic/melamine film, moisture/mold protection from below).
- **⚠️ HDF core density range and a real comfort-vs-durability tradeoff, first numeric figure for this store**: 700-1,200 kg/m³ market range, most common quality product at **850-950 kg/m³**. Denser HDF = stronger locks, better moisture resistance, less sag under furniture — but also a more "resonant"/hollow-sounding floor underfoot; higher density is not an unconditional win.
- **Formaldehyde-label reliability caveat**: E1/E0 are the safe classes, E2/E3 unsuitable for residential — but only **European manufacturers** reliably disclose the class at all; cheap Chinese/Turkish/unbranded product may omit it entirely, making the claim unverifiable even when the box says E1.
- **⚠️ Water-damage mechanism, more specific than this page's general laminate water-intolerance warning**: an isolated spill on one board (3-5 drops, left indefinitely) does no damage — the top layer itself is water-resistant. **The real failure point is the board-to-board lock joint**: a pooled spill left across an installed floor for an extended period (worked example: a week's vacation) has, per the source, roughly a 99.9% chance of swelling/destroying the whole floor once water reaches the joints. "Water-resistant laminate" should be judged by **joint performance**, not the box label.
- **⚠️ Embossing ("тиснение") benefits, new to this page**: a textured, wood-grain-matching finish vs. a flat smooth surface — reads more expensive/premium (a non-professional reportedly can't tell it from real wood by sight), meaningfully less slippery underfoot (a real safety factor), and hides surface scratches better than a smooth finish (which shows scratches more visibly under raking light).
- **⚠️ Wear-class 20-series-vs-30-series taxonomy, extends this page's existing class-33 content**: the 20-series (21-23) is the technically correct residential tier by design intent, but Russian market preference has made only the 30-series standard even in homes — **class 32** (low-traffic commercial) and **class 33** (high-traffic commercial) are both more than sufficient for an apartment. **"Class 34" does not exist as a real standard — a marketing invention**, mostly by budget Chinese manufacturers.
- **⚠️ Four-type lock-mechanism taxonomy, genuinely new buying vocabulary**: **Click** (oldest/simplest — most reliable, but boards must be joined into a long "snake" before angling into the long edge, real breakage risk on large areas); **Lock/tongue-groove** (hammered or overlaid; some laminates combine Click long-edge + Lock short-edge, allowing one-board-at-a-time installation regardless of room length — source states he wouldn't use pure Lock); **5G** (an enhanced Click, easier/faster to install, but extremely dust-intolerant — a single trapped speck can start the floor squeaking almost immediately, with no fix short of pulling up and redoing that section); **UniClick** (hammered or clicked, the most balanced option for reliability vs. install difficulty). Source's own ranking: Click most reliable/simplest, 5G reliable-but-risky, UniClick a good balance, plain Lock avoided.
- **⚠️ Thickness range, lock-strength independence, and a specific tile-transition height-match**: practical range 8/10/12/14mm (6mm categorically excluded). **Thickness has no effect on lock/joint durability** — that's governed by HDF quality, not thickness; thickness affects only soundproofing/thermal performance (thicker = quieter, slower to warm). **14mm is excessive under a heated floor** — it either never fully warms through or takes impractically long. **⚠️ 12mm laminate plus its underlayment lands at roughly the same combined height as tile plus tile adhesive** — a 12mm-laminate-to-tile transition can line up almost 1:1 without a compensating self-leveling pour.
- **⚠️ Named laminate brand tier ladder, first laminate-specific brand taxonomy for this store (2025)**: **Economy** — Eger, AGT. **Optimal** — Alpine Floor, Classen, Kronospol. **Premium** (five named, no ranking) — MyStep, MyFloor, "Nofloor"/нотекс (`ASR-uncertain`), Ro, Berry Alloc (`ASR-uncertain` on exact rendering). No prices given — price is stated to depend on the buyer's combined criteria selections, not a fixed per-tier figure.
- **⚠️ Comparative durability claim, flagged as a live disagreement with this page's own sbk.remont content above**: this source states any laminate outlasts engineered/parquet board, quartz-vinyl, and other "natural" flooring — only tile is more durable. This directly conflicts with sbk.remont's `DE-4uFYXJQ4` speaker calling laminate "obsolete" and recommending genuinely expensive laminate spend be redirected to solid wood instead — both are single-speaker opinions, recorded as an unresolved cross-source conflict rather than silently picked.

## Seven-Material Comparison: Shadow-Baseboard Compatibility, Heated-Floor Nuances, and Repairability Framework (Konstantin Kruglov / Ontario, added 2026-08-28, Round 7)

> [!NOTE]
> Cross-checked against this page's existing five-material (Петришин-Строй) and 10-material (sbk.remont, today) comparisons, plus this round's own laminate deep-dive (video 1) — wear-resistance and cost-tier rankings all corroborate existing content and are not re-recorded; only genuinely new items (mostly the source's own two "controversial" criteria — shadow-baseboard and heated-floor compatibility) are below. Region level 2 only. Low promotional ratio. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_puO8alDwL9w_kruglov_best_flooring_options|YT_puO8alDwL9w]]]

- **⚠️ Stated regulatory constraint, `unverified` (no code cited)**: apartments in Russia can only use **electric** underfloor heating — hydronic (water-circulated) underfloor heating is stated as available only in a private/detached house, not an apartment.
- **⚠️ Shadow-baseboard/profile vs. concealed-mount-baseboard compatibility, new baseboard vocabulary for this page**: a "теневой профиль/плинтус" (recessed into the wall, only partially or not at all covering the floor's own perimeter deformation gap) is functionally different from a concealed-mount baseboard (which fully covers the gap despite its hidden look) — the shadow variant's floor compatibility genuinely depends on installation method. **Compatible** (glued installs, negligible real gap): glued engineered board, glued parquet board, glued LVT quartz-vinyl, any tile. **Not recommended** (floating installs needing a real gap): laminate, floating parquet-on-underlayment, floating quartz-vinyl-on-underlayment — even quartz-vinyl's minor linear expansion doesn't exempt it. Newer spring-loaded shadow-baseboard systems exist for floating floors but are treated as unproven over time, not yet recommended.
- **⚠️ Heated-floor-under-floating-materials nuance**: some manufacturers permit laminate/floating-parquet/floating-quartz-vinyl over a heated floor, but only when the heating element is embedded *within the base* (screed or self-leveling layer), not installed directly beneath the floating floor's own underlayment.
- **⚠️ Real field-experience reversal on quartz-vinyl-plus-heated-floor marketing claims**: despite marketing that quartz-vinyl has negligible linear expansion and is heated-floor-safe, this company's own field experience shows most **floating** quartz-vinyl-on-underlayment installed over a heated floor does buckle/tent in practice, with unpredictable recovery once cooled. **Current company practice**: pair a heated floor confidently only with tile or **glued** LVT quartz-vinyl, not floating quartz-vinyl.
- **Local-repairability framework by installation method**: floating installations (laminate, parquet-on-underlayment, quartz-vinyl-on-underlayment) are hard to locally repair — replacing one damaged board means disassembling back to the nearest room edge and reassembling, with a real risk of damaging adjacent locks. Glued installations (any tile, glued parquet/engineered board, glued LVT) allow an individual piece to be swapped without disturbing the rest of the floor.
- **⚠️ Subfloor-prep-cost tiering across 7 compared materials**: simplest prep (plain level screed) — any tile, laminate, parquet-on-underlayment, quartz-vinyl-on-underlayment. More demanding — glued engineered board and glued parquet board. **Most demanding of all — glued LVT quartz-vinyl**: thin and soft like "cut linoleum," so it fully telegraphs any substrate imperfection under raking light.

## Quartz-Vinyl Family Deep-Dive: 11-Criteria Comparison Across Four Subtypes (Konstantin Kruglov / Ontario, added 2026-08-28, Round 7)

> [!NOTE]
> Densest video of this round's flooring cluster. Cross-checked against this page's existing quartz-vinyl-family content (hardness ordering, MSPC first-mention, universal deformation-gap rule, LVT/SPC chip-vs-scratch tradeoff from the round-6 kitchen video) — those generalities corroborate and aren't re-recorded; this video's per-criterion, per-subtype granularity across four subtypes (glue-down LVT, floating SPC, floating click-lock LVT, and a floating "rigid multilayer"/"регит/ABA" type, `ASR-uncertain` on the exact name and kept distinct from this page's existing MSPC content) is almost entirely new. Region level 2 only. Low promotional ratio. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_LNXBHVnP4gs_kruglov_quartz_vinyl_truth|YT_LNXBHVnP4gs]]]

- **Two-camp taxonomy**: **Camp 1** — glue-down LVT (one member). **Camp 2** — SPC, click-lock LVT, and rigid multilayer — all floating/lock-jointed, but with **no universal cross-manufacturer standard**; each brand sets its own area limits, thickness minimums, and heated-floor rules independently.
- **⚠️ Heated-floor compatibility, per subtype**: **Glue LVT** best of all (no locks to separate) — one real limit: don't exceed **27°C** surface temperature (health, not material-failure, reasoning). **SPC** worst — real, significant linear expansion (directly contradicting "quartz-vinyl doesn't expand" marketing); some manufacturers forbid heated floors outright, others require the element embedded **in the screed** plus the same 27°C ceiling, with warranty denial risk if that's not followed. **Click-LVT** more heat-resistant than SPC, combinable under the same embedded/≤27°C rules, less expansion thanks to greater elasticity. **Rigid multilayer** technically compatible but functionally pointless — thickest of the four, slow to warm through, already the warmest-feeling underfoot unheated; also intolerant of partial-room heating, same mechanism as SPC.
- **⚠️ Continuous-run capability, per subtype, extends this page's existing seamless-run figures**: **Glue LVT** best (no locks — effectively unlimited continuous area). **SPC** worst — most manufacturers cap around 10-12m² or an equivalent length limit, comparable to laminate's own per-room separation need, and poorly suited to shadow-baseboard installs (see this round's video-2 note above). **Rigid multilayer** second-best but highly collection-dependent (some lines permit 250m² continuous, others cap at 10-15-20m²). **Click-LVT** locks more break-resistant than SPC's; manufacturers nominally recommend SPC-like limits, but 2-3-room continuous runs commonly work in practice (a lock may tent temporarily under thermal stress, typically returning flat).
- **Installation-difficulty ranking**: **glue LVT hardest of the four** — every plank individually glued, excess adhesive cleaned off without damaging the material. The three floating types install like laminate; **SPC is actually easier than laminate** (cuttable with just a utility knife). Main risk across all floating types: breaking a lock during fitting.
- **⚠️ Substrate-flatness requirement, per subtype**: **glue LVT least forgiving** — thin enough to telegraph any screed imperfection, near-mirror flatness ideal. **SPC and click-LVT** need laminate-grade flatness (the lock is the vulnerable point — a repeated-walked-on bump can break it). **Rigid multilayer most forgiving** of substrate irregularity, though still recommended to meet a SNiP-compliant screed at minimum.
- **⚠️ Heavy-furniture-load tolerance, per subtype**: **glue LVT most tolerant** — load distributed only on the individual glued plank; furniture guide rails can be screwed straight through it. **SPC least tolerant** — its large linear expansion means a heavy sofa "locking" several planks in place while the surrounding floor keeps expanding/contracting creates real internal stress (same mechanism as laminate's furniture caution, worse if installed as one long continuous run). **Click-LVT and rigid multilayer** sit in the middle — click-LVT's base/lock elasticity is more forgiving; rigid multilayer's tolerance scales with its number of fiberglass reinforcement layers.
- **⚠️ Scratch-resistance quality-variance warning**: any quartz-vinyl scratches more easily than quality laminate — an inherent property of its softer UV-lacquer top coat. Real-world scratching mostly happens during renovation/move-in (dragging unpadded metal furniture legs), rarely in ordinary living. **Lacquer quality is entirely manufacturer-dependent and invisible in a showroom** — a real cited client complaint (cheap no-name SPC scratched within a month) illustrates why a wide per-m² price spread among visually similar SPC products often reflects exactly this hidden quality gap; buy from large, established manufacturers with real QC.
- **⚠️ Thickness specs and thickness-quality relationships, per subtype, first numeric figures for this family**: **Glue LVT** 2-3mm (thickness barely affects comfort, marginally affects perceived warmth). **SPC** 3.5-5mm, available with integrated or non-integrated underlayment — **recommend non-integrated**: integrated underlayment covers only the plank body, not the lock joints, leaving joints unsupported; thicker SPC is unconditionally more reliable. **Click-LVT**: practical minimum **>4mm** (below that, too little material for the lock to form properly) — thicker is always safer for lock durability. **Rigid multilayer**: integrated underlayment is *not* a problem here (unlike SPC, thanks to its inherently stronger construction) — reliability instead tracks the number of reinforcement fiberglass ("стеклохолст") layers (2-3 layers = very reliable).
- **⚠️ Moisture-resistance/wet-room suitability, per subtype**: **Glue LVT** best — usable in wet zones/loggias without restriction, steam-cleaner-safe; seal joints with extra UV lacquer in constant-water-contact areas. **SPC** — avoid in wet rooms categorically (joints, not the material, fail on water ingress); steam generators absolutely prohibited. **Click-LVT** — doesn't fear moisture at the material level; the source states he'd still glue it down in a bathroom/WC despite manufacturers not recommending or prohibiting this, an off-label practice he's seen work in small rooms; steam generators still prohibited regardless. **Rigid multilayer** — doesn't fear moisture, usable in bathrooms with proper perimeter waterproofing (still a floating floor); many manufacturers of this type do permit steam-generator use, unlike SPC.
- **Comfort ranking, per subtype**: glue LVT — quiet, modest shock absorption, fairly warm, "semi-commercial" feel. SPC — colder/noisier/harder than glue LVT, though still warmer than average laminate. Click-LVT — noticeably more comfortable than glue LVT (thickness + underlayment, real cushioning). **Rigid multilayer (thick variants) ranks best of all four for comfort** — most cushioned, warmest, most pleasant; thin variants land just ahead of click-LVT.
- **Repairability ranking, per subtype**: easiest — glue LVT, especially with thermally-reactivatable adhesive (heat-gun lift, fresh adhesive, reinstall). Hardest — SPC, click-LVT, and rigid multilayer share the same floating-floor problem: repairing one plank means disassembling back to the nearest room edge, risking damage to previously-intact locks.
- **Eco-friendliness has no category-level ranking** — unlike the other 10 criteria, emission safety depends entirely on the specific manufacturer's raw-material sourcing, not which quartz-vinyl subtype is chosen.

## Heated-Floor-Under-Tile Repair Technique, T-Molding Mechanism, and a Glue-Staining Defect (Ontario/Nikita Kuznetsov, added 2026-08-28, Round 7)

> [!NOTE]
> Fourth and final video of this round's flooring cluster (a real material-sample walkthrough, different presenter than Kruglov — same channel precedent as Round 6's `6FbZY6YHrxQ`). Heavy overlap with this round's videos 1-3 confirmed and not re-recorded (continuous-run/threshold framing, general composition, moisture tiering). Region level 2 only. Low promotional ratio. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_9f5XxCn2EFM_kruglov_best_flooring_kuznetsov|YT_9f5XxCn2EFM]]]

- **⚠️ Heated-floor-under-tile repairability technique, new mechanism**: if an electric heated-floor cable/mat sits directly under tile, removing a damaged tile later risks cutting the cable during demolition. **Fix**: pour a protective cement/self-leveling layer *over* the heating element before tiling — buries and protects it, so tiles can be replaced later without risking the (now-buried) cable.
- **⚠️ T-molding-threshold mechanism at a laminate-to-tile junction, extends this page's existing T-molding content with the "why"**: neither a rigid glue bond nor sealant alone works there — laminate keeps moving with temperature/humidity, so a rigid bond eventually separates and a sealant-only joint cracks from the same ongoing movement. **A T-shaped threshold strip is the only viable solution for this specific material pairing**, not just an aesthetic default.
- **Laminate expansion-gap minimum, a second data point**: **5mm** minimum perimeter damper gap for laminate specifically — distinct from this page's existing cork-flooring 4-5mm minimum and the typically-executed 8-12mm baseboard-covered range.
- **⚠️ Real glue-staining-under-finish defect and its mitigation, new for this store**: adhesive that gets onto a glue-down parquet/engineered-board face during installation and is wiped off can still etch/stain the underlying lacquer or oil finish invisibly — only becoming visible later at a raking angle against light, requiring a full re-lacquer of the entire floor. **Mitigation**: only let dedicated parquet specialists ("паркетчики"), not general flooring installers, handle glue-down parquet/engineered-board installation.
- **Oil-finish vs. lacquer-finish distinction, extends this page's existing Kodolov lacquer-subtype taxonomy**: a true oil finish feels noticeably better underfoot than any lacquer finish, but needs ongoing maintenance (periodic reapplication) — cited as the reason oil finish is comparatively rare in practice despite the superior feel.
- **Discrete-plywood-pad leveling technique for solid-wood (массив) installation**: solid wood has no plywood backing of its own (unlike engineered/parquet board) — plywood pads are cut into pieces, laid discretely with damper gaps between each on the screed, ground flat, and only then is the solid-wood board installed on top.
- **Quartz-vinyl thickness-as-damper tactile-detection nuance**: thicker quartz-vinyl gives real extra cushioning, but it's not detectable by finger-press — only perceptible while actually walking on it; thicker also improves heat retention, more relevant to a house than an apartment.

## Do's

| Rule | Applies To | Reason | Source |
| :--- | :--- | :--- | :--- |
| Buy 10% extra tile volume above net area | Bathroom, WC, Kitchen, Hallway | Account for cuts, waste, and future repairs | `_Archive/processed_sources/20260727_vid1_transcript_d04723c5.txt` |
| Lay sub-screed acoustic soundproofing mats before pouring screed | All Living Rooms | Reduces impact noise transmission to lower floors | `_Archive/processed_sources/20260727_renovation_tips_video_f23c504a.txt` |
| Pour self-leveling compound to equalize tile and laminate/SPC thickness height differences | Living Room, Bedrooms, Corridors | Achieves a single flush floor transition across rooms | `_Archive/processed_sources/20260727_renovation_mistakes_video_21ade3f6.txt` |
| Select SPC quartz vinyl with integrated underlayment for high-wear areas | Living Room, Bedrooms, Corridors | Provides a water-resistant practical finish and eliminates separate underlayment errors | `_Archive/processed_sources/20260727_apartment_renovation_guide_360f4c7c.txt` |
| Select surface-mounted PVC or duropolymer baseboards over concealed flush baseboards on tight budgets | All Living Rooms | Saves premium wall preparation labor costs required for flush baseboard channels | `_Archive/processed_sources/20260727_renovation_guide_mistakes_a8e90887.txt` |
| Mount aluminum tracks for concealed or shadow baseboards during rough wall prep | All Living Rooms | Integrates tracks into wall base before plastering/puttying; decorative inserts are installed after flooring | `_Archive/processed_sources/20260727_renovation_guide_mistakes_2_61e3a372.txt` |
| Leave 3-5 cm un-cut baseboard extension past wall corners at custom cabinet niche locations | Living Room, Bedrooms | Allows custom furniture installers to trim baseboard flush against cabinet panels without joint gaps | `_Archive/processed_sources/20260727_renovation_guide_mistakes_3_a0e895b1.txt` |
| Select exact finishing floor material types before starting rough renovation works | All Rooms | Enables contractors to calculate precise subfloor screed and self-leveling compound depths to create single flush floor transitions | `_Archive/processed_sources/20260727_renovation_guide_mistakes_4_21a6e3c1.txt` |
| Grind high spots on concrete sub-floors when matching thick quartz-vinyl or laminate with porcelain tile | Wood-to-Tile Transitions | Achieves a seamless, zero-threshold floor transition without needing self-leveling compound | `_Archive/processed_sources/20260727_renovation_guide_mistakes_7_b385361e.txt` |
| Route flooring transitions through a door opening rather than across open floor, per Zemskov/Zemstandart | Irregular/L-shaped rooms, multi-direction-traffic zones | A short seam anchored at a door frame holds better and reads as intentional; a long diagonal seam fails faster and looks accidental | `_Archive/processed_sources/20260810_entry_hallway_dividing_wall_case_8963951b.txt` |
| Choose doors, then baseboard (matched to doors), then flooring, per Zemskov/Zemstandart | All rooms | Reverses a much harder problem (fitting doors to an already-chosen floor) into an easy one | `_Archive/processed_sources/20260810_laminate_selection_and_matching_a51f8dca.txt` |
| Only buy laminate/board with a chamfered edge, per Zemskov/Zemstandart | All rooms | Hides inevitable gaps; a square edge can lift at a crack, a real trip/cut risk barefoot | `_Archive/processed_sources/20260810_laminate_selection_and_matching_a51f8dca.txt` |
| Lay solid wood/engineered board separately per room; lay ceramic tile continuously, per Zemskov/Zemstandart | Solid wood, engineered board, tile | Continuous solid-wood/board runs guarantee buckling; tile doesn't expand with humidity | `_Archive/processed_sources/20260810_flooring_layout_and_orientation_rules_4ef67e84.txt` |
| Acclimate glue-down quartz vinyl 2-3 days at the room's actual future operating temperature before installing, per Zemskov/Zemstandart | Glue-down quartz vinyl | Installing before temperature normalizes guarantees gaps or buckling days later | `_Archive/processed_sources/20260810_glue_down_quartz_vinyl_top_15_mistakes_8efd6760.txt` |
| Compare wear-class/water-resistance specs line by line when a hypermarket price is dramatically below a specialized retailer's, per Zemskov/Zemstandart | Any flooring purchase | Chain hypermarkets may sell an identically-branded but spec-downgraded "special series" | `_Archive/processed_sources/20260810_flooring_hypermarket_spec_downgrade_scam_6f860ac8.txt` |
| Use class-33 beveled-edge laminate as a budget kitchen-floor alternative to tile, per RemProektMD | Kitchen | Class 33 (commercial-rated) survived 4 years with no issues in the source's own kitchen; the bevel hides thermal-expansion seam gaps | [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_OP8ALhLynHE_remproektmd_12_money_saving_tips\|OP8ALhLynHE]] |

## Don'ts

| Rule | Applies To | Risk | Source |
| :--- | :--- | :--- | :--- |
| Do not lay laminate directly in wet areas | Bathroom, WC | Swelling and water damage | `_Archive/processed_sources/20260727_vid1_transcript_d04723c5.txt` |
| Do not install under-floor heating in entryway mudroom tile zones if household has large pets | Entrance Hallway | De-icing salts brought in on shoes melt and dry rapidly on heated tile; pets lick paws and risk chemical poisoning | `_Archive/processed_sources/20260727_renovation_guide_mistakes_3_a0e895b1.txt` |
| Do not combine cork flooring with a large dog in the household, per Zemskov/Zemstandart | Households with large dogs | Claws reportedly shred cork flooring within roughly a week of normal use (single cited account) | `_Archive/processed_sources/20260810_never_do_project_in_pieces_873e1532.txt` |
| Do not accept an underlayment recommendation without confirming it matches the flooring product's own spec, per Zemskov/Zemstandart | Any glued/floating flooring | A mismatched underlayment (real case: too-soft 3mm vs. required ≤2mm) can cause structural joint separation | `_Archive/processed_sources/20260810_quartz_vinyl_underlayment_dispute_621b3f51.txt` |
| Do not default to a 1/2-length ("classic") row-offset pattern, per Zemskov/Zemstandart | Laminate, solid wood, engineered board | Produces a visually repetitive dotted cross-joint line; 1/3-length offset avoids it | `_Archive/processed_sources/20260810_flooring_layout_and_orientation_rules_4ef67e84.txt` |
| Do not lay diagonally, per Zemskov/Zemstandart | Long-format flooring | Conflicts with both light and traffic direction, wastes material, produces poor doorway offcuts | `_Archive/processed_sources/20260810_flooring_layout_and_orientation_rules_4ef67e84.txt` |

## Source Notes

- Tile-waste buffer, acoustic underlayment, self-leveling compound, SPC selection, baseboard type/mounting, screed depth planning, tile-to-floor grinding technique — sources as cited inline above (region/channel not yet cross-referenced against the rest of this vault's source-attribution conventions; flagged for future cleanup).
- **Short-transition-at-door-opening rule, grain-direction wear mechanism** (Alexey Zemskov / Zemstandart-Zemsproekt, Moscow, real 88.5m² project, user-supplied Turboscribe transcript after both automated caption-fetch methods failed, added 2026-08-10) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_UfmUC4-T3jY_entry_hallway_dividing_wall_case|extraction note]] (#138, 2020-12-01).
- **Cork-flooring-vs-large-dog caution, real cited client case** (same practitioner, livestream, user-supplied Turboscribe transcript, added 2026-08-10) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_z3xJeVPL6n4_never_do_project_in_pieces|extraction note]] (#705, 2022-12-13).
- **Real underlayment-mismatch consumer-dispute case** (Alexey Zemskov / Zemstandart-Zemsproekt, Moscow, fetched via anonymous `youtube-transcript-api`, added 2026-08-10) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_0mrBnaOU3I0_quartz_vinyl_underlayment_dispute|extraction note]] (#005, 2018-12-13).
- **Laminate buying sequence, color-matching, chamfered-edge safety requirement** (same channel, added 2026-08-10) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_PwJsksBs4Ek_laminate_selection_and_matching|extraction note]] (#058, 2019-02-20).
- **Continuous-vs-separated laying rules, laying direction, row-offset pattern** (same channel, added 2026-08-10) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_lOMxNoyW_NE_flooring_layout_and_orientation_rules|extraction note]] (#060, 2019-02-23).
- **Glue-down quartz-vinyl installation, 22 detailed rules** (same channel, livestream, added 2026-08-10) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT__VvT9FcNbKY_glue_down_quartz_vinyl_top_15_mistakes|extraction note]] (2021-05-21).
- **Chain-hypermarket flooring spec-downgrade scam** (same channel, added 2026-08-10) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_XFhz1NXlln8_flooring_hypermarket_spec_downgrade_scam|extraction note]] (#546, 2023-10-19).
- **Screed-first vs. walls-first sequencing decision, template-stick leveling technique, pre-marking technique** (same channel, #108, 2019-11-17, added 2026-08-19) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_cJLZebMtW7A_screed_or_walls_first_108|extraction note]].
- **Full DIY reinforced screed build with sub-screed noise insulation, beacon/mesh technique, home-mixed screed recipe** (Pavel Sidorik, individual practitioner, own apartment, Belarus level-1 region, "New Building A-to-Z" #18, 2021-04-29, added 2026-08-24) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_hN7szX2re2c_sidorik_screed_noise_insulation_ep18|extraction note]].
- **Class-33 beveled-edge laminate as a budget kitchen-floor alternative to tile, 4-year real-world durability account** (RemProektMD/Andrei, Chișinău/Moldova channel, region level 2 only, added 2026-08-24) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_OP8ALhLynHE_remproektmd_12_money_saving_tips|extraction note]] (2020-09-24).
- **Finish self-leveling layer over that same beacon-poured screed** (same practitioner/project, "New Building A-to-Z" #27, 2021-09-02, added 2026-08-24, Round 5) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_kXGYTsBTKj8_sidorik_self_leveling_floor_ep27|extraction note]].
- **Five-material flooring comparison (laminate/quartz-vinyl/linoleum/tile/solid-wood), real screed-buildup cost-trap mechanism, company expert's solid-wood preference** (Петришин-Строй, "СРАВНЕНИЕ!" format, added 2026-08-24, Round 3) — [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_96mlkQoczI4_petrishin_flooring_2026_comparison|extraction note]] (2025-10-03).
- **Screed-height compensation technique for a level mismatch at a finish-transition point** (Петришин-Строй, real case study, added 2026-08-24, Round 4): pour the new screed slightly higher than the original floor, calculating the exact level needed in advance, to land a clean, flush transition seam between quartz-vinyl and tile at a room boundary — a concrete example of planning a screed pour around a known finish-transition point rather than a fixed generic height. Moscow level-1 region. [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_qFM8NIDIRro_petrishin_case_study_old_apartment|extraction note]] (2025-02-16).
- **⚠️ Adjustable/leveling floor system chosen instead of screed for a historic timber-beam building, room-by-room load-capacity decision** (Петришин-Строй, real Arbat-area case study, Moscow level-1 region, added 2026-08-24, Round 4): most rooms got a "regulated floor" (an adjustable-pedestal floor system) rather than a poured screed; screed was poured only in the corridor, over the existing structural timber beams, specifically because that location's load capacity allowed the extra weight. A concrete example of choosing a floor system per-room based on an old structure's actual load capacity rather than a blanket apartment-wide choice. [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_IoQiGtso9Vk_petrishin_case_study_arbat_historic|extraction note]] (2025-06-15).
  - **Follow-up on the same real object, added 2026-08-24 Round 6** (`7LAB25SCQ1Q`, a cost-summary video for this same 75m² New Arbat apartment — same channel confirms it's a return visit): states the screed section specifically as "the front part of the apartment, where the beams were metal" — the rest of the apartment got the adjustable floor. **⚠️ Open question, not resolved**: this describes the screed-eligible section's beams as *metal*, while the Round 4 note (above) describes the corridor's exposed beams as *timber* — possibly two different beam systems in the same old building (e.g. floor-support beams vs. visible ceiling beams) rather than a real contradiction, but not confirmed either way from the transcripts alone. Flagged as `uncertain` rather than silently reconciled.
- **Quartz-vinyl flooring with a real wood-veneer top layer, distinguished from engineered/parquet board** (Петришин-Строй, real Chelomei St. object, Moscow level-1 region, added 2026-08-24, Round 6): both product types use a genuine wood top layer, but engineered/parquet board's substrate is plywood, while this quartz-vinyl variant's substrate is not — a material-category distinction not previously recorded on this page. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_Q0sVq_1SIQM_petrishin_finishing_works|YT_Q0sVq_1SIQM]]]
- **Screed QC and curing detail, real ЖК Topills object** (Петришин-Строй, region level 2, added 2026-08-24, Round 6): real sand-quality caution (must be washed river sand, never frozen — a real winter-delivery risk); fiber additive ("фибра") mixed into the screed mix for crack-resistance via micro-fiber reinforcement; reinforcement mesh must be physically lifted mid-pour so it ends up embedded within the screed body rather than settling uselessly at the bottom (an unembedded mesh "doesn't work at all," wasting its cost); explicit 2-3 day curing protocol — cover with plastic film immediately after pouring, then periodically uncover and thoroughly water the screed for 2-3 days before re-covering, to prevent rapid moisture loss that would otherwise stop the screed reaching full rated strength (skipping this is common and causes later cracking/warping even on an otherwise well-executed pour). **Quantified screed-height-planning cost trap on this real 120m² object**: not deciding finish-flooring materials (tile vs. quartz-vinyl by room) before the screed pour required a later self-leveling compensation layer costing a minimum additional ≈300,000 RUB ≈$3,800 — a concrete real-object number for this store's existing general 150,000-300,000 RUB cost-trap range. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_c4mmaLAsDw4_petrishin_screed_soundproofing|YT_c4mmaLAsDw4]]]
- **Herringbone (`ёлочкой`) install-time and error-tolerance mechanism, plus exclusive-material lead-time/crew-retention caution** (Петришин-Строй, real 120m² premium case, region level 2, added 2026-08-24, Round 6): a herringbone pattern install takes roughly 2-3× a standard flooring install, and a placement error as small as half a millimeter compounds to a ~1.5cm misalignment by the far end of a run — a concrete precision/time-cost mechanism for this layout. Separately: an exclusive-collection quartz-parquet color took 6 months to arrive after ordering; independently-hired private crews (not a company's salaried staff) may not return to finish a project after a gap that long, since crew members often pick up other, closer jobs during an extended wait — build known long lead times for bespoke/exclusive materials into the project schedule up front. Labor-only install cost for this case: 204,000 RUB ≈$2,600 (trailing-6-month USD/RUB average ending 2026-04-26). [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_8dyPTnmOHKs_petrishin_6mln_labor_per_stage|extraction note]] (2026-04-26).
- **Real semi-dry-screed QC finding, one month post-pour, and an engineered-board no-plywood installation detail** (Петришин-Строй, real object on the "Новая Рига" highway corridor, Moscow region — region level 1, 2017-vintage source, added 2026-08-24, Round 11): a third-party-poured semi-dry mechanized screed, examined more than a month after pour and after the prescribed 10-day plastic-film curing period, came out generally well-planed with only minor deviations. **The one real defect found, and where it occurs**: a ~3mm bump specifically at a room-to-room threshold/doorway transition — flagged as the single most common evenness mistake across builders generally (a plane mismatch between adjacent rooms right at the doorway junction), distinct from flatness within one room. Semi-dry screed is explicitly framed as a legitimate cost-saving choice if minimizing spend is the priority — tap-tested with no hollow sound anywhere, some minor surface cracking within normal tolerance, but measurably less robust than a mechanized/reinforced alternative. Separately: engineered wood board on this object was glued directly to the screed with two-component adhesive, no plywood underlayment used; each box contained ~4-5 different plank lengths specifically to avoid a repeating pattern once laid; porcelain tile elsewhere on the same object was noted as very difficult to drill/cut. [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_gREGOOA2OHo_petrishin_screed_evenness_check|extraction note]] (2017-10-01).

## Removable T-Molding Transition-Threshold Installation Technique (Петришин-Строй, added 2026-08-24, Round 12)

Short TV-style tip clip, confirmed uploaded by the Petrishin-Stroi channel
itself (same upload day, 2016-04-20, as this round's grout-protection
clip — a same-series pair). Region level 2. Low promotional ratio.
Genuinely new installation-mechanism content — distinct from this page's
existing threshold *avoidance* guidance and from `Door_Anatomy_and_Mount_
Types.md`'s "no visible threshold strip" preference (this is what to do
when a transition strip is actually needed).

- **What the threshold hides and secures**: a transition threshold at a
  material-to-material junction (here: tile-to-laminate) both conceals an
  otherwise-visible unevenness at the seam (up to ~1-1.5mm, which even a
  skilled installer can leave) and physically holds down the floating
  laminate edge, which can lift slightly over time without it.
- **Three-part removable T-molding construction**: (1) a base channel
  piece installed under/against the tile, fixed and static; (2) a
  decorative metal T-shaped profile ("Т-образная," "тэшка") sized and
  cut to the run length; (3) a rubber gasket strip, also pre-cut to
  length, that slides over the T-profile's stem before it's pressed into
  the base channel — the rubber's friction fit is what holds the whole
  assembly snug and non-rattling against the tile/laminate surfaces on
  either side.
- **⚠️ No visible fasteners**: unlike some threshold types that are
  screwed directly to the floor, this rubber-gasket friction-fit design
  needs no visible screws through the finish surface — cited as a real
  aesthetic advantage over a screwed-down threshold.
- **Serviceability advantage**: because the T-profile is held only by
  the rubber gasket's friction fit (not glued or screwed), a scratched or
  worn threshold strip can be pulled out and replaced later with no
  special tools or effort — a genuine maintenance/longevity benefit over
  a permanently fixed threshold.
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_VZk4615VM6I_petrishin_door_threshold|YT_VZk4615VM6I]]]

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
[source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_l4bXbwfOlrU_petrishin_vinogradny_ep7_plumbing|YT_l4bXbwfOlrU]]]

## French Herringbone Pattern — Real Cost Premium and QC Standard (Olga Kachanova channel, added 2026-08-25)

Real 2025 Moscow household case, RUB: **French herringbone ("французская
ёлка") parquet installation costs ~15% more than standard "deck"/
plank-run installation** for the same engineered-wood material —
attributed specifically to installation labor complexity, not the wood
itself. This household's installer required subfloor/screed flatness
within **2mm** before accepting the job, and needed several re-grinding
passes to meet that standard — worth budgeting installer callback/QC
time for a herringbone floor specifically, beyond the direct material/
labor price premium. `single-account`. [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_1amhehTMxcg_kachanova_ideal_2room_family_child|YT_1amhehTMxcg]]]
