# Codex review brief — services migration completion, and the electrical wiring rules

**2026-09-17.** Two connected pieces of work, both wanting adversarial review. Commits `ab732f5` → `a503df8` on `main`.

The first is apparatus: the services migration finished, with the validators built around real records. The second is domain: two owner statements about electrical wiring that became model constraints, one of which **disproved a placement built earlier the same day**.

**What I want from you is not confirmation.** The prior review rounds have each found a structural error in my own work, and the pattern held again here — four separate defects below were caught by gates or by the owner, not by me. Assume more remain.

---

## Part 1 — The services migration is complete

### Where it ended

| | |
| :--- | :--- |
| Source locators | **114** (81 ledger rows + 33 reviewer-authored claims) |
| Unresolved | **0** |
| In scope | **102** |
| Cited by a target | **102** — bidirectional coverage satisfied, `--require-complete` passes |
| Target records | **166** across 6 tables |

Concepts: 108 assertion, 32 observation, 10 relation, 7 occurrence, 6 route, 3 assembly.

**No `identity_uuid` is minted anywhere.** Keys are provisional `migration_key`s. A UUID is forever by construction — the IFC `GlobalId` derives from it — so minting one for a record that may still be split or withdrawn would give permanent identity to a provisional judgement.

### The sequencing that was imposed on me, and why it mattered

I proposed building the locator validator first. That was rejected: the validator had **no target-record schema to consume**, so writing it then would have made every typed-column decision silently, inside validator code, where nobody reviews a schema. The imposed order was: draft schemas + a small representative slice → record-schema validator → geometry validator → the remaining targets.

**That ordering found a live gate defect that an empty-input validator could not have.** The split rules read the *parsed* `multiplicity` column. `service_outlets.csv` has no `count` column at all, so every row in it parses as `unstated` and `continue`s past the split check — including `SW-B`, which review decided splits into exactly 2. I deleted one of its two occurrences and **the gate passed**. The existing seed used an `electrical_existing` row that happens to parse as `exact_n`, so the gate looked guarded while the real records went unchecked. Reviewed multiplicity now wins; an override with no stated reason fails.

### The rules the adjudication ran under

Set by the owner, now normative in `_Inbox/planning/services_data_model_design_20260916.md` §3.0f–§3.0g:

1. Comparable-flat photo → asserted observation **there**; candidate projection **here**.
2. **Unambiguous** owner testimony about this apartment **may** establish target existence.
3. Geometry may **constrain or disprove** a placement; it **cannot prove an element exists**.
4. A drawing ID that **displays** a canonical concept is an **alias**, not another occurrence.
5. Literal coordinates stay `candidate`/`derived` unless independently established.
6. Owner-described routing does **not** become `as_built`.

**The fact that makes rule 1 bite:** there is no interior photograph of this apartment. `photo_positions.csv` holds one photo of the owner's unit and it is an **exterior elevation**. Nothing in the flat is field-verified, so **nothing currently qualifies as `resolved_present` on observation**. Only **six** sources mint a target-apartment occurrence, and every one rests on owner testimony: `SS-B`, `SW-B` (assembly of two), `SV-T`, `SV-VT`, `W6`, `SS-K2`.

Assertion states: 57 candidate, 38 asserted, 9 retracted, 4 unknown. Bases: 48 derived, 41 stated, 13 assumed, 3 observed, 3 unknown. Observations are scoped 16 to flat 53, 15 to 109, 1 to flat 2 — **none to ours**, which is the correct and slightly uncomfortable answer.

### What the gates enforce structurally

- `scope_kind` / `scope_ref` — typed, because an apartment enumeration could not express a **developer document governing this unit type**, which §3.0f explicitly allows as a route to established existence.
- **The laundering rule:** an assertion scoped `apartment`/`ours` with `knowledge_basis=observed` is refused unless an observation *also scoped to ours* backs it. The failure mode is not writing a false row — it is a projection quietly claiming observed basis while every observation behind it is of somebody else's flat. **This gate refused one of my own records mid-session.**
- Locator union as columns with **required and forbidden** sets: a `wall_face` carrying `u_mm` is two incompatible placements in one row.
- Terminal envelope as *assertions*, not occurrence columns, so each part carries its own basis. **The validator invents no default device dimensions.** Three-state verdict: centre in a void → invalid; centre clear, extent unknown → **incomplete, not valid**; full asserted envelope clear → valid.

### Things I did not close, deliberately

- **`zone_local` is not built.** `contained_in_zone=P1` and `zone_local(P1,u,v)` are different claims; the compiler publishes neither zone footprints nor local frames, so promoting one into the other would invent precision. P1/P2 occurrences are `unlocated` plus containment assertions.
- **`surface_local` is recognised but not resolvable.** The compiler publishes `FACE_ROLES` and `locate_on_face` — the `wall_face` half only. Production validation reports **"support geometry unavailable"**, never a pass. I had previously claimed the whole contract was "IMPLEMENTED"; that was false and is corrected.
- **`S3` was carried unresolved** until the owner answered it (see Part 2).

---

## Part 2 — Electrical wiring: two owner statements, two model constraints

### 2.1 The substrate rule, and the correction to it

**Owner, first statement:** wiring runs through aerated blocks (G3, G5, G7), not concrete (R2, R7), because significant cavities may not be cut into the monolithic RC frame.

I encoded this as a blanket refusal of any `concrete` host. **The owner then corrected it the same day:** a constructor can lay wiring inside concrete *while pouring it*, and that is exactly how the existing ceiling cable outlets sit inside the slabs. So the prohibition is on **cutting a cavity into cured concrete**, not on wiring in concrete.

`installation_method` (`cast_in` | `chased` | `surface_mounted`) is now the axis:

| phase + method | verdict |
| :--- | :--- |
| `proposed` + concrete | **invalid**, no exception — a retrofit cannot cast into concrete already poured |
| `existing` + `cast_in` | allowed — the ceiling points depend on this |
| `existing` + `chased` | **invalid** |
| `existing` + method unstated | **incomplete** — unevidenced, not impossible |

**My blanket version would have rejected the ceiling outlets**, which are legitimately in concrete.

### 2.2 What it disproved, including my own work from the same session

- **`W6`** — the living-room switch was *inferred* onto `R5` on 2026-09-07 because O10 is the room's only entrance. R5 is concrete. **I had built the entire step-3 geometry seed set around `W6` on R5.** `OCC-W6` is now `unlocated` with `anchor_ref=O10` retained: the owner's claim survives, the wall does not.
- **`S4`** on R2 and **`S9`** on R6 — likewise withdrawn.

**Reason corrected after the cast-in clarification:** all three stay withdrawn but on a **weaker** basis — not structurally impossible, merely **unsupported**. Nothing evidences cast-in for them, every accessory visible in `a89d`/`add8` is in aerated block, and all three were inferred rather than observed.

**Where the constraint points:** O10's south edge is touched by `G6 cross_hi`, `R4 end_to` and `R5 end_to`. `G6` is the only aerated block of the three, so it is the only chase-able jamb there. Recorded as a **candidate**, not asserted — eliminating two of three options is still not an observation.

### 2.3 What the photographs settled, and what they did not

`_Drawings/evidence/a89d_highlighted.png` and `add8_highlighted.png`, owner-annotated, apartment 109.

- **MC (the window wall) carries nothing** — both flanks of O3 are clean in `add8`. This **corroborates the owner's statement about our flat**.
- **⚠️ I kept this deliberately separate from the substrate rule.** MC is block and *could* be chased; it is empty as a matter of **fact**, not prohibition. Conflating an observed absence with a structural rule would put the right answer on the wrong reasoning.
- The gate then **refused my own MC record**: I scoped it to ours with `knowledge_basis=observed` while the photograph is apartment 109. Split into an owner-`stated` assertion plus an observation scoped to 109.

**Relevant history:** `wall_materials.json` → `WALL_MAPPING_WAS_WRONG_TWICE_2026_09_07` records that wall assignment is the axis I could not read off photographs at all, having got it wrong twice while sounding confident both times. The substrate rule matters mainly because it lets the **model** refute an assignment instead of the owner noticing again.

### 2.4 `S3` — answered, and the answer was "neither"

Asked whether *«не 220 В, вероятно 380 В»* described the outlet in his own flat or corrected the drawing, the owner answered that it is **inference**: *"this is my guess"*, *"my guess and speculations"*. His reasoning: the outlet is visibly larger and differently shaped, it sits where the designer places the stove, a stove draws more power.

Sound reasoning — but reasoning from a comparable-flat photograph is **not unambiguous testimony about this apartment**, so S3 does not get the §3.0f exemption. Four separate claims:

| | basis | state | scope |
| :--- | :--- | :--- | :--- |
| outlet is larger / different shape | observed | asserted | **apartment 53** |
| **not** 220 V (`polarity=negate`) | derived | candidate | ours |
| 380 V | derived | candidate | ours |
| three-phase | derived | **unknown** | ours |

No occurrence, no asserted 380 V, no three-phase supply.

### 2.5 The rewire, which changes the standing of everything above

**Owner:** *"the current plan is to replace all the existing wiring. This is the current placement… just for reference, for testing how to construct electric wiring."*

Everything migrated is the **`existing` phase — reference, not design**. No existing position constrains the new layout. The planned topology is fixed: central board **near the entrance** → distribution through the **ceiling** → **drop down the wall** to each accessory → drops **exclusively in aerated block**, chased and covered by the finish.

**This makes the layout generatable for the first time** — derived from appliance and fixture placement plus the topology, rather than drawn by hand.

**⚠️ Flagged rather than left implicit:** `project_decisions.md` records that the handover includes electrics, sockets and switches **already fitted and priced into the flat**, and warns that moving a socket wall throws away paid work. A full rewire discards it deliberately. The owner's call, made — but it now sits in the budget as a **known write-off**.

---

## Gates

| | |
| :--- | :--- |
| `build_migration_ledger` | structural discovery + retention + registry, **11 seeds** |
| `check_migration_coverage --require-complete` | **23 seeds**, PASS at 102/102 |
| `check_target_schema` | **23 seeds**, 166 records |
| `check_locator_geometry` | **21 seeds**, run on `.venv-ifc314` |
| `check_dxf_closure`, `verify_batch`, `check_page_sizes` | all PASS |

Every geometry seed asserts its **expected diagnostic**, not merely a non-zero exit — a validator that rejects the right case for the wrong reason passes an exit-code test.

---

## Defects found this round, and by whom

**None of these were found by me reasoning about my own work.**

| Defect | Found by |
| :--- | :--- |
| Split rules ignored *reviewed* multiplicity; deleting an SW-B occurrence passed | testing the gate against real records |
| Key slug stripped non-ASCII — `ГВС`, `ХВС`, `DN50-в` collapsed onto one key | the uniqueness gate |
| `host_ref=P1` on two risers — **P1 is a plumbing anchor, not a wall** | the geometry gate |
| MC record scoped `ours` with `observed` basis | the §3.0f laundering gate |
| Substrate rule too absolute — would have rejected the cast-in ceiling outlets | the owner |
| `W6` built on a concrete host | the owner's substrate rule |

---

## Where I would attack this if I were you

1. **The three-state verdict may be too generous.** `incomplete` is not a failure by default; only `--strict` makes it one. With extent unknown on nearly everything, is `incomplete` doing any work, or is it a way of never failing?
2. **`prop_for()` in the target generator guesses a `property` from keyword hints** for the 40 claim-derived assertions, defaulting to `arrangement`. That is the least defensible thing in the migration and I flag it as such.
3. **Six model walls have no material class** — `MA`, `MB`, `MC`, `G4C`, `R1a`, `R1b` — and ten classified ids are absent from the model. `G4C`/`G4c` is case; `R1a`+`R1b` are the model's split of `R1`, which `wall_materials.json` says must **not** be split. I refused to guess an alias map, because a wrong pairing would silently authorise chasing the RC frame. Is refusing right, or is it leaving the substrate check unenforceable over the whole external perimeter?
4. **The alias adjudications (12 locators) removed elements from the count.** If any one of them is wrong, an element silently ceases to exist. They are the least reviewed decisions here.
5. **`existence_readiness` / `placement_readiness` / `classification_readiness` are specified but not implemented** as derived outputs.
6. **The frozen generator has not been retired** and the legacy CSVs are still under `data/canonical/`. The one-way cutover is unstarted, so two authorities currently coexist.
