# Layout Option Review — v0 against v1, read against the closest comparable

**Written 2026-09-03/04, after processing `Phk79uKT7rA` — a 2020 renovation of a ~70 m² flat for a family of four that the owner identified as very close to this project.** This page is a *judgment* review. The generated numeric comparison is `tools/layout/compare_variants.py`; the mechanism for carrying options is `00_Master/Options_And_Versions.md`. Nothing here re-derives a dimension — every figure is quoted from `data/canonical/room_schedules.json` or `data/cad/room_labels.json`.

> [!IMPORTANT]
> **Read `.agents/skills/apartment-layout-modelling/SKILL.md` before acting on anything here.** In particular: every dimension is nominal **±25 mm**, nothing is field-verified, **room outlines in `data/cad/room_polygons.json` are approximate** (7 of 10 rooms are flagged, the worst at −23.6%), and **Homestyler's own label areas are the authoritative figures** — the grown polygons are for placing things, never for measuring them.

> [!CAUTION]
> **⚠️⚠️ READ THIS BEFORE ANY NUMBER BELOW. ADDED 2026-09-04, AND IT PARTLY UNDERCUTS THIS PAGE.**
>
> **The owner's standing instruction: areas are not evidence — including the developer's own — and only
> linear dimensions are a source of truth.** Tested and confirmed: the plan's one plain rectangle closes
> to 0.2%, while the small room is out 2.6% and the middle room 4.4%. See `project_decisions.md` and
> `data/canonical/dimension_tolerance.json`.
>
> **Most of §1–§3 was written from areas, so its numbers are not all of equal standing. Which is which:**
>
> | number | basis | standing |
> | :--- | :--- | :--- |
> | `v1` room areas — 15.28, 13.57, 10.56, 8.32, 1.90 | **Homestyler's own computation of the owner's drawn geometry** (`data/cad/room_labels.json`) | ✅ **Reliable** — a CAD area of a known polygon, and the skill already treats these as authoritative for quantities |
> | `v0` room areas — 19.49, 16.64, 9.36, 9.79, 5.24, 64.85 | **the developer's published figures** | ⚠️ **Not evidence.** Published, not measured |
> | **every Δ in §1**, and the pools table | **mixes the two bases** | ⚠️⚠️ **Unreliable — do not quote the magnitudes** |
> | **the 1.39 m² "lost to partitions"** (§2) | 64.85 developer − 63.46 Homestyler | ⚠️⚠️ **Mixed basis. Withdrawn as a measurement** — the *direction* (new partitions consume floor) is certain, the figure is not |
> | **24.13 m² combined zone** (§3) | 13.57 + 10.56, **both Homestyler** | ✅ **Reliable**, and it is the number the retractable divider must be sized against |
> | **"0.60 m² smaller than v0's 24.73"** (§3) | Homestyler vs developer | ⚠️ **Withdrawn.** No conclusion about `v1` being smaller than `v0` survives |
> | **which room serves which function** (§1) | **label seed coordinates plus the owner's own statements**, not areas | ✅ **Survives intact** — the role-swap reading does not depend on any area |
> | **15.28 m² in the bunk-bed argument** (§6) | Homestyler | ✅ **Survives** — the area argument there still holds |
> | **the вентблок 400 × 1140** (§5) | **printed linear dimensions** | ✅ **Reliable** |
>
> → **What this page still establishes, unchanged: the role swap, the separability requirement (§3a),
> the 24.13 m² the Phase 2 concept has to work inside, the вентблок result, and both blockers.**
> → **What it no longer establishes: any Δ between `v0` and `v1`, and the 1.39 m² partition cost.**
> **Those become answerable — properly, on one consistent basis — once `v0` has geometry built from the
> printed chains.** That is the same task §5 already names as the remaining blocker, and this is a second,
> independent reason to do it.

---

## 1. What v1 actually does — and the role swap that the area diff hides

A role-keyed diff of the two schedules looks dramatic, and it is misleading. Read that way:

| Role | v0 (developer) | v1 (Homestyler) | Δ |
| :--- | ---: | ---: | ---: |
| living | 19.49 | 13.57 | **−5.92** |
| kids | 9.36 | 15.28 | **+5.92** |
| bedroom | 16.64 | 9.29 | **−7.35** |
| kitchen | 5.24 | 10.56 | **+5.32** |
| bathroom | 3.09 | 3.07 | −0.02 |
| wc | 1.24 | 1.47 | +0.23 |
| laundry | — | 1.90 | **+1.90** |
| circulation (прихожая → entrance 2.44 + hallway 5.88) | 9.79 | 8.32 | **−1.47** |
| **sum of deltas** | | | **−1.39** |

**⚠️ Those ±5.92 and ±7.35 figures are not resizings. They are role reassignments between rooms that barely changed size.** Confirmed from the label seeds in `data/cad/room_labels.json` and from the owner's own statements in `00_Master/Family_Requirements.md`:

- **The middle room of the row becomes the kids' room.** `Kids Room` sits at x = 4618, between `Bedroom small` at x = 1599 and `Living and Dining Room` at x = 7779 — it *is* the middle room. It carries 15.28 m² against the 16.64 m² the developer prints for that room: **a −1.36 m² change, not +5.92.**
- **The 9.36 m² room becomes the adults' bedroom.** `Bedroom small` is 9.29 m² and sits at the loggia end. The owner states this directly: *"temporarily, a bedroom for adults will be seated in a smaller room, 9.36 square meters."* **A −0.07 m² change.**
- **The living room is the only room that genuinely shrinks**: 19.49 → 13.57, because the kitchen is taken into it.

**So the honest description of v1 is not "a re-cut flat". It is: the three rooms of the row keep their sizes and swap their functions, and one real move happens — the kitchen expands into the living room.** Read as pools rather than roles:

| Pool | v0 | v1 | Δ |
| :--- | ---: | ---: | ---: |
| **living rooms** (3 жилые) | 45.49 | 38.14 | **−7.35** |
| **service** (kitchen + bath + wc + laundry) | 9.57 | 17.00 | **+7.43** |
| **circulation** | 9.79 | 8.32 | −1.47 |
| **lost to new partitions** | | | **−1.39** |

**⚠️ v1 moves 7.35 m² out of the living-room pool and 1.47 m² out of circulation, and spends 7.43 m² of it on services — a kitchen slightly more than doubled, plus a laundry room the developer plan does not have.**

## 2. The cost of the moves, quantified: 1.39 m² of floor

`v0` rooms sum to **64.85 m²**; `v1` rooms sum to **63.46 m²**. The difference is floor consumed by the 24 partitions v1 adds.

**1.39 m² = 2.0% of the 69.09 m² total, or about a third of the loggia's counted 4.24 m².**

That is not an argument against v1 — the laundry room alone is 1.90 m² of function bought for it, and the owner has a stated reason for each move. **It is the number to hold every further partition against.** It is also the one figure the comparable case study puts real pressure on (§4).

## 3. Phase 2 already works in v1 — and it is close on area

The owner's plan is explicitly phased (`Family_Requirements.md`, clarified 2026-08-20):

- **Phase 1 (now):** adults sleep in the ~9.3 m² room; both children share the 15.28 m² room; the living room is living-only; the dining table lives in the kitchen.
- **Phase 2 (~2029–2030):** adults move into the combined kitchen-living space, split at night by a sliding glass partition, sleeping on a **Murphy bed to be installed during the current build**. The ~9.3 m² room becomes the boy's room; the 15.28 m² room becomes the girl's.

**The arithmetic checks out, and it is tight:**

| | living zone | kitchen zone | combined |
| :--- | ---: | ---: | ---: |
| **v1** | 13.57 | 10.56 | **24.13** |
| v0 (rooms as drawn) | 19.49 | 5.24 | 24.73 |
| owner's stated target | | | ~24–25 |

- ✅ **v1's zone split matches the owner's stated intent**: the bigger zone (13.57) is the living/bedroom zone, the smaller (10.56) is the kitchen zone with the dining table — and the seeds confirm the kitchen sits *behind* the living room (x = 7856, y = 7944 against x = 7779, y = 4230), i.e. away from the row's façade and toward the entrance, which is where the owner said he wanted it.
- ⚠️ **But v1's combined space is 0.60 m² SMALLER than v0's two rooms already are**, and combining v0's kitchen and living would *add* the removed wall's footprint on top of 24.73. **So v1 buys the zone *shape* the Phase 2 concept needs, not extra area — it pays 0.60 m²+ for it.** Worth knowing when the Murphy bed and the sliding partition are sized: the partition's parking width and the bed's swing come out of 24.13, not 24.7.

## 3a. ⚠️⚠️ The thesis behind all of it, stated by the owner 2026-09-04 — ONE bathroom, to fund a real living room

Everything in §1–§3 is *what* `v1` does. This is *why*, and it had not been written down until the owner said it.

**The comparable spent area on a SECOND full sanitary room and got a brief satisfied on paper.** The owner's reading of what that cost them: their combined kitchen-living came out too small to be a living room at all — *"just a small sofa and a screen, a monitor on the wall … that's not a real living room. There is no place of living room."*

**So this project keeps two wet rooms (the single bathing room plus the separate туалет, both near the entrance) and spends the third one's area on the kitchen-living zone.** *"Instead we have bigger area which can be separated into a real isolated room if needed. That was a main idea."*

- → **⚠️⚠️ THAT REFRAMES §3's 24.13 m² FROM A NUMBER INTO A REQUIREMENT.** The zone is not just bigger; it must stay **separable into a genuinely isolated room**, because that is what makes Phase 2 possible. **Any later move that trims that zone spends the thing the whole layout was built to buy** — which is the strongest argument in this document for looking to circulation for area instead (§5).
- → **⚠️ It is a knowing departure from a vault rule, not an oversight.** Zemskov's ideal is three wet rooms (`wc.bathroom_count_minimum_3`); his own area-constrained fallback is two (`wc.budget_fallback_2_wet_rooms`). **This project takes the fallback deliberately, for a reason the rule does not weigh: what the third wet room costs the living zone.** Recorded in `project_decisions.md`.
- → **And it answers the case-study round's open question: THIS is the decision in the comparable that the owner rejects.**
- ⚠️ **The divider is RETRACTABLE, not a sliding door** (owner's correction, same date). That changes the parking width and the head detail, and it has to be sized against 24.13 m², not the developer plan's 24.73.

### Two structural differences from the comparable, and one of them kills a transfer

| | comparable | this project |
| :--- | :--- | :--- |
| **Лоджия attaches to** | the kitchen-living zone | **the 9.36 m² small bedroom** — confirmed on the detailed plan |
| **Sanitary rooms** | master bathroom **+ second full one** | one bathing room + separate туалет |

→ **⚠️ The comparable's balcony-off-the-living-zone content does not transfer.** Here the лоджия is coupled to whoever occupies that room — adults in Phase 1, **the boy** afterwards — which is also why the standing лоджия decision (keep it closed and separate, glazing and insulation only) belongs to that room's brief and not to the living zone's.

## 4. What the comparable case contributes — and what it does not

The case is now a dataset: `data/layout_cases/nsdsgn-70m2-family-two-children.json`, with five rules in `data/layout_rules/rules.jsonl`.

**It is genuinely close.** ~70 m², family of four, two children sharing a room, a standard corridor plan with a row of rooms and a middle room, two sanitary rooms. The owner named the differences himself: the loggia sits differently, that flat's second sanitary room is a full bathroom where this project has a separate WC, and its combined kitchen-living is *smaller* than this project's — so anything achieved there is achievable here with room to spare.

### ⚠️⚠️ The finding, and the one place it must NOT be transferred

A designer with **carte blanche on style** made **exactly one replanning move** — «мы немножко уменьшили КОРИДОР В ПОЛЬЗУ ДЕТСКОЙ КОМНАТЫ, в принципе, это ВСЕ ИЗМЕНЕНИЯ» — because «такая АРХИТЕКТУРА, что ПЕРЕИГРАТЬ это было… НЕВОЗМОЖНО».

- ⚠️⚠️ **That is not a cost argument here, and treating it as one would be wrong.** His was a **finished building with a load-bearing column**. **This flat is unbuilt — `status: design_intent_building_not_finished`, partitions drawn 75 mm and not yet erected.** Moving a wall that does not exist yet costs a drawing revision; moving one that does costs demolition, waste removal, and an approval. **The restraint finding is recorded in the ruleset with that caveat attached** (`replanning.restraint_on_a_standard_corridor_plan`).
- ✅ **What DOES transfer is the direction of the donor.** He took the area from the **corridor**, and that independently corroborates a rule the vault already held from Zemskov — `corridor.is_the_area_donor` is now **`corroborated`** rather than `single_source`: two practitioners, different cities, different professions, same first donor.
- ✅ **And the specific move — corridor into the children's room — is now its own rule** (`corridor.reduce_in_favour_of_kids_room`), because it is exactly the trade this plan type offers.

## 5. ⚠️⚠️ The open question this round was meant to settle, and why it cannot be yet

**Both practitioners in the vault say take from circulation first. v1 takes 1.47 m² from circulation and 7.35 m² from the living-room pool — the opposite emphasis.** After v1's moves, **8.32 m² is still committed to entrance + hallway**, and the geometry says the transfer is available: `Hallway` (x = 4914, y = 7754) lies directly beneath `Kids Room` (x = 4618, y = 4182), so the two share a boundary.

**The question worth answering: could part of the service expansion come from that 8.32 m² instead of from the living-room pool, protecting the 24.13 m² the Phase 2 concept depends on?**

**Two hard limits bound the answer, and one of them is a blocker:**

1. **`corridor.min_clear_width` = 1100 mm in the rough state** (Zemskov). That is the floor under any corridor narrowing, and it is measured *before plaster*. It is also the quantitative content of NSDSGN's «немножко», which he never numbers.
2. **✅ THE SECOND ВЕНТБЛОК IS NOW MEASURED — 400 × 1140 mm = 0.456 m²**, read from the **printed** dimension strings on `fllor_plan_detailed.jpeg` (2026-09-04), and drawn to the same shaded-box-with-rounded-channels convention as the confirmed туалет block. **⚠️ Its long axis runs PERPENDICULAR to the façade wall — the туалет block lies *along* its wall, so the orientation must not be assumed from that one.** It stands at the прихожая/кухня boundary, roughly above the partition between the middle and right-hand rooms.
   - → **⚠️⚠️ AND THE RESULT IS BETTER THAN EXPECTED: it does NOT stand in the way of the corridor-to-kids trade.** That trade takes depth from the прихожая along the **middle** room's north wall, where the plan prints a **1050 mm** band (a 1915 × 1050 recess beside a 910 door opening). The block sits at the **kitchen end** of the прихожая, not that end — and at 1140 mm deep it is deeper than that 1050 band, which is consistent with it belonging to the kitchen boundary rather than to the corridor.
   - → **What it DOES constrain is the кухня/постирочная corner — which is exactly where `v1` puts its 1.90 m² laundry.** That is the adjacency to check next, and it is the same situation the comparable resolved by **building the laundry cupboard against its immovable column rather than around it** (`laundry.ventilated_doors_on_an_enclosed_appliance`, and the case's `m2` move). **The precedent is directly usable.**
   - ⚠️ **Still open on this: the datum of the adjacent `200` dimension is not certain from the raster, so the block's offset from the wall needs field confirmation.** 400 × 1140 are printed figures; the offset is not.
3. **⚠️⚠️ SO ONE BLOCKER REMAINS, AND IT IS THE BIGGER ONE: `v0` HAS NO GEOMETRY.** ⚠️ **The route has changed** — the owner states the plan images are the only source of truth, so a Homestyler export of the *original* layout is probably not available; only the redesign was ever traced. **The remaining route is the skill's fallback: reconstruct v0's partitions from the printed dimension strings on the detailed plan, against the registered raster.** Hand work, and it is now the single task standing between this project and a measured layout comparison.

> [!IMPORTANT]
> **⚠️⚠️ THIS IS THE ROUND'S REAL FINDING: the layout-selection decision is blocked on two cheap measurement tasks, not on more analysis or more sources.**
> 1. **Give `v0` geometry.** The skill already names the cheapest route: *export the original layout from Homestyler as a second DXF, the way the redesign was exported.* Without it there is no baseline to measure a trade against — only two room schedules.
> 2. **Locate the second вентблок on `fllor_plan_detailed.jpeg`**, the way the туалет block was found by zooming (1140 × 490, three channels). It is the immovable that stands where the corridor trade wants to go, and it plays the same role here that the load-bearing column played in the comparable case — which resolved it by *building the laundry cupboard against it* rather than around it.
>
> **Both are hours of work, not a round of research. Everything else in the layout decision is downstream of them.**

## 6. Two live disagreements the owner's own phasing settles

Both were routed to their pages as unresolved Perspectives when the source was processed. `Family_Requirements.md` resolves the deciding variable in each — so they are recorded as *informed*, with the owner's position still the one that closes them.

### The bunk bed

The case study built one and framed it as the children's own wish. The vault's Round 4 clinical source argues **against** bunk beds *where area permits two separate beds*. **Area is the deciding variable, and here it is 15.28 m² for two children aged 3 and 6 — which comfortably permits two separate beds.** The clinical objection therefore applies at full strength.

**And the shared configuration has a known end date:** the children split into two rooms at Phase 2, ~3–4 years out. **So a bunk bed is a temporary fitting with a foreseen obsolescence** — which is the vault's own standing test for children's joinery. ⚠️ Note the corollary the owner already flagged: shared storage should be sized so it still works as one child's storage afterwards.

### The themed mural

Built in the case study. The vault holds that a themed children's scheme has roughly a **one-year** useful life. With a 3-year-old and a 6-year-old, and the room becoming the girl's own room in 3–4 years, **the lifespan finding and the phasing point the same way**: keep the theme in things that are cheap to replace, not in a wall finish that is part of the build.

## 7. Decide-now-use-later items this case study adds to first fix

The Murphy-bed infrastructure is already on this list by the owner's decision. The case study adds two more of the same class, and they share a property: **they are cheap now and expensive or impossible later.**

- **Per-child, locally-switched night lights at two bed heights.** In the case study each boy got his own, switched from his own bed. **The switch heights depend on the bed decision above**, so the bunk-versus-separate choice has to be made before the electrics are chased in — not before the furniture is bought.
- **A cable hatch let into the desktop, with brushes.** Trivial as a joinery instruction, impossible to add cleanly to a finished desk.
- ⚠️ **And one negative lesson worth designing to:** in the case study a socket back-box was set slightly off-line and is **permanent** — nobody looked in time. This flat's first fix is the stage where that class of error becomes irreversible.

## 8. What this review deliberately did not do

- **No variant was created.** Answering §5 needs the two measurements, and a `v2` drawn without them would be a guess wearing a drawing's authority. `process.minimum_two_variants` is already satisfied by v0 and v1.
- **No dimension was re-derived from a plan image**, per the skill.
- **No claim about which physical room v0 intends as "bedroom" versus "kids"** beyond what the label seeds and the owner's statements support. v0 has no geometry; the mapping in §1 rests on the seeds of v1 plus the owner's own words, and would be confirmed outright by the v0 DXF export.

---

## Source Notes

- Case dataset: `data/layout_cases/nsdsgn-70m2-family-two-children.json` (Александр Синчуков / Сенчугов, NSDSGN, 2020-11-03; **manually supplied transcript — no caption track exists**; undimensioned).
- Rules: `corridor.is_the_area_donor` (upgraded to `corroborated`), `corridor.reduce_in_favour_of_kids_room`, `replanning.restraint_on_a_standard_corridor_plan`, `kids.identical_workstations_prevent_conflict`, `laundry.ventilated_doors_on_an_enclosed_appliance`, `process.no_deviation_clause_needs_detection`.
- Areas: `data/canonical/room_schedules.json`. Seeds and label areas: `data/cad/room_labels.json`. Outline confidence: `data/cad/room_polygons.json`.
- Household phasing and every quoted owner statement: `00_Master/Family_Requirements.md`.
- Wiki narrative for the case: [[17_Design_and_Ergonomics/analysis/Replanning_Cases_and_Layout_Selection|Replanning Cases and Layout Selection]], [[05_Kids_Room/analysis/Desks_Beds_and_Shared_Rooms|Desks, Beds and Shared Rooms]].
