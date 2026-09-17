# Codex review brief — the model-first approach, its grounding, and the plan

**2026-09-17.** Commits `9b78af0` → `334e6a7` on `main`. Two bodies of work since the last brief: **four adversarial repair rounds** on the services migration apparatus, and **a research pass over 292 practitioner videos plus three Russian MEP sources** that changed a design position.

**What I want reviewed is the POSITION, not the housekeeping.** The gates pass; that is not the question. The question is whether the approach below is grounded or whether I have assembled a confident-sounding case out of sources that do not support it.

⚠️ **Four review rounds have each found real defects in the round before**, including two that would have produced confidently wrong geometry. Assume the same here.

---

## 1. The position, stated so it can be attacked

> **One authored source of truth → a deterministic compiler → a resolved 3D model → every 2D sheet, quantity and render is a DERIVED VIEW of it.**

**The precise form matters**, and an earlier version of this document got it wrong in a way you corrected:

- **The authoring store is canonical data** (`data/canonical/*.csv`, `*.json`), **not the IFC.**
- **The 3D model is GENERATED** by `tools/ifc/model_from_resolved.py` from the compiler's output.
- **IFC is the authoritative *issued* representation**, not the place work is done.
- **2D is a view.** A discipline sheet is a query plus a cut, not a drawing that happens to resemble the model.

⚠️ **The failure mode this exists to prevent is split-brain authority** — the condition where a drawing and a model each partly define reality and neither is wrong enough to notice.

**Why this is being re-examined now:** the owner intends to **replace all wiring**, with the new layout **derived from appliance and fixture positions** rather than drawn. That makes the electrical layout a *generated* artefact for the first time, which is a direct test of the position.

---

## 2. The finding that changed a position, and how it nearly went the other way

**Round 2 of the research concluded that 3D MEP was not viable**, on strong evidence: Lloyd Sark (IfcArchitect), in a live session, states that Bonsai's native MEP is broken —

> *"doing it natively at the moment, there's a few issues with the system flow… when you do pipes, when you do connections, when you do HVAC… it has a lot of misunderstandings when you model it out"*

— and that practitioners therefore cut the architectural plan and **draft 2D overlays**: *"the drawing becomes a stop gap."* I reported that as settling the question.

**The owner rejected the inference**, on this reasoning: *"it sounds like simplification and reduce the amount of work… while we're trying to do automation pipeline it shouldn't be so important."*

**He was right, and the evidence was already in the vault.** Three practitioners model MEP in 3D as ordinary commercial work:

| Source | Practice |
| :--- | :--- |
| Алексей Дубровин (`kxJ9R3gQjKw` +4) | electrics **and plumbing** in 3D; all clients order it; second year; *«все работы выполняют только по 3d проектам»* |
| Алексей Шемчук (`0c-QhBDQMWE` +4, **in the vault since 2026-09-14**) | *«В модели выполняется вся работа так, как она потом будет выполняться на объекте»*; per-cable schedule with start, end and **length** |
| LOFT DIY (`0T97_CA7hgo`) | wiring in SketchUp by layer and group; length read off by selecting the group |

### ⚠️⚠️ The reconciliation, which is the actual finding

> **Sark's complaint is about the SYSTEM layer. Every benefit the others report comes from the GEOMETRY layer.**

*System flow*, port-to-port connectivity, `IfcDistributionPort` — that is the semantic network, and it is what he reports misbehaving. What the others gain needs none of it:

- coordination against other trades, **decided in the model rather than on site**;
- **as-built documents** telling the next trade *«где сверлить можно, где сверлить нельзя»*, transferring cable-strike liability;
- installation schematics;
- ⚠️⚠️ **quantities by selection — including CHASE LENGTH**: *«выделяем штробы — 67 с лишним метров»*. **Chase length is priced LABOUR**, not material.

**→ The 2D-overlay retreat is a labour-saving choice inside a HAND-modelling workflow. A pipeline that generates geometry does not pay that labour, so the reason does not transfer.** What does transfer is the narrower warning: model the runs as geometry, keep circuit membership as authored data, decline the port layer.

⚠️ **Attack this first.** It is the load-bearing inference of the whole brief, and it rests on my reading that Sark's *"system flow"* means port/flow semantics rather than 3D MEP generally.

---

## 3. What the corpus does and does not contain

My own enumeration of all 292 titles across the five sources, independent of the two agent rounds. **13 processed before my pass; 23 now.**

| Bucket | Titles | Read |
| :--- | ---: | :--- |
| file / performance / bugs | 39 | the corpus's own largest topic |
| drawings / sheets | 29 | |
| types / materials | 18 | ⚠️ our known gap lives here |
| spatial / classification | 14 | |
| **MEP / services** | **1** | ⚠️⚠️ **the void** |
| **scripting / `ifcopenshell`** | **1** | ⚠️⚠️ **and it is FreeCAD, not Bonsai** |
| **phasing / 4D** | **0** | ⚠️⚠️ **not one title in 292** |

**Three voids, confirmed by my own count.** Services, scripted authoring, and phasing. ⚠️ **Phasing is the uncomfortable one**: the flat is being completely rewired, so `existing`/`demolished`/`new` is now load-bearing, and the entire corpus is silent. That is a documentation question, not a research one.

---

## 4. What actually changed in the model's design

| # | Finding | Source | Consequence |
| :-: | :--- | :--- | :--- |
| 1 | ⚠️⚠️ **`IfcMaterialLayer.Priority`** (integer 0–100) governs how layers intersect at connections; a joint is a **connection** (mitre/butt, breakable) | Tom, `rSHAf7GBsUE` | **IFC has its own joint rule, and it differs from ours.** `wall_corners.csv` resolves L-corners by *thicker, then longer* at WALL level; IFC resolves at LAYER level by an authored number. No conflict today — our walls are single-material — **but the external perimeter is layered (300 block + 70 wool + render), so this must be reconciled BEFORE layered walls** |
| 2 | A type carries `PredefinedType`, Psets and **geometry**, all inherited; `Name`/`Tag`/`GlobalId` stay per-instance, and **the instance does not carry its type's name** | Tom, `fN9cP6w0DsM` | Explains why schedules group on `Type.Name` — the designation lives nowhere else. **Our generator emits NO types**, so it cannot produce a door or window schedule at all |
| 3 | Wrong spatial containment is a **common** export defect, and the element then **vanishes silently** from viewers | Catargiu, `lQ_t0neAI9M` + `sdNStKd-fqE` | We call `spatial.assign_container`, so we are *probably* right. **Nothing asserts it** |
| 4 | IFC4.3 is infrastructure-oriented with **zero architectural benefit** for a flat; downgrade strips georeferencing | Tom, `XYeasHbyw-U` | **Stay on IFC4.** Closes an open decision |
| 5 | IDS can be **authored** locally (`ifctester.org`), no data egress | Tom, `s94gzyhP3eU` | A validation route for a model we will not upload |
| 6 | Circuit membership is **authored input**, not derived geometry; lighting circuit count is governed by **inrush**, not steady load | Дубровин, `3cw4oSGr4Cw` | An engineering constraint no geometry produces. The circuit list precedes the tracing |
| 7 | Survey comes first, and includes **wall composition** and in-screed heating located by **thermal imaging** | Дубровин, `wbUm7i-nHHk` | ⚠️ **We have never surveyed this flat.** One photograph exists and it is an exterior elevation |

---

## 5. State of the services migration

`f8ba3ad` → `9b78af0`, four adversarial rounds. **114 source locators, 0 unresolved, 102/102 cited, 176 target records, `--require-complete` passes. 159 seeds across five self-tests.**

⚠️ **`--issued` currently rejects all 7 occurrences, which is the correct answer** — nothing in this flat is field-verified, so nothing is issuable.

**Defects found across those rounds, none by me reviewing my own work:** `nan` producing a VALID placement (a standing-rule violation — `finite()` exists and I called `float()`); a misspelled material failing open so a chased accessory on the RC frame read VALID; candidate assertions authorising an issued result; phase-vocabulary drift (`proposed` vs the design's `new`) that bypassed the concrete rule; an envelope tested only against openings and never against the wall; and **a seed of mine that institutionalised a defect** by asserting an out-of-face envelope was valid.

**Cutover, UUID minting and generation remain unapproved.**

---

## 6. The plan, in order

1. **Reconcile `wall_corners.csv` with `IfcMaterialLayer.Priority`.** Prerequisite for layered walls.
2. **Add the spatial-containment assertion** to the IFC check. Cheap; guards a silent, common failure.
3. **Emit types** — `IfcWallType`/`IfcDoorType`/`IfcWindowType` + `IfcMaterialLayerSet`. Now fully specified. Unblocks all schedules.
4. **Author an IDS** and validate the generated model.
5. **Resolve IFC phasing from the documentation**, since the corpus is silent and the rewire needs it.
6. **Then** the services generator: runs as geometry, circuits as authored data, no `IfcDistributionPort`.
7. Services cutover only after a review round that reproduces no defect.

👤 **Blocked on the owner, and no research closes these:** whether and when the flat is surveyed; circuit count; where the board goes; and **supply phase and calculated load** — open since the `S3` adjudication and now blocking circuit sizing.

---

## 7. Where I would attack this

1. **§2's reconciliation.** If *"system flow"* means something broader than ports, the conclusion inverts and we should not model runs at all.
2. **The Russian sources are three practitioners, one of whom sells the service**, with no measured comparison against 2D. Is that enough to overturn a direct statement from an IFC-native practitioner?
3. **§4.1 may be understated.** I claim no conflict today because walls are single-material — but `wall_corners.csv` already decides corner *ownership*, and `IfcMaterialLayerSet` may make that decision twice with different answers even for a single layer.
4. **Emitting types changes GlobalId/identity surface** while a services migration deliberately mints no UUIDs. Is step 3 safe before step 7?
5. **Phasing is unevidenced entirely**, and I am proposing to resolve it from documentation alone — the weakest evidential basis in the plan.
6. **23 of 292 videos processed.** I claim the remaining 269 hold nothing we need. That is a negative claim from a filtered sample.
