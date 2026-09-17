# Bonsai / Blender / IFC — open questions, and what the five channels actually contain

**2026-09-17. My own pass over all 292 titles**, after Antigravity's two rounds. Not a re-triage of their verdicts — a survey of the corpus against *our* toolchain questions, to see what practitioners do before we build anything ourselves.

---

## 1. ⚠️ Coverage reality

**13 of 292 videos are processed — 4.5%.** That is a reasonable filter rate for a channel sweep, but the *distribution* of what was taken is skewed, and three areas that matter to us are under-sampled.

| Bucket | Titles | Processed | Read |
| :--- | ---: | ---: | :--- |
| file / performance / bugs | 39 | 4 | the corpus's own largest topic |
| drawings / sheets | 29 | 2 | second largest |
| **types / library / materials** | **18** | **2** | ⚠️ **our E4 gap sits here** |
| **spatial / classification** | **14** | **1** | ⚠️ containment, storeys, spaces |
| openings / voids | 14 | 3 | adequately sampled |
| **validation / IDS** | **11** | **2** | ⚠️ three are about *authoring* IDS |
| export / viewer | 6 | 0 | untouched |
| qto / cost | 6 | 2 | |
| collaboration / BCF | 4 | 0 | untouched |
| **MEP / services** | **1** | 0 | ⚠️⚠️ **the void, confirmed by my own count** |
| **scripting / API** | **1** | 0 | ⚠️⚠️ **and it is about FreeCAD, not Bonsai** |
| **phasing / 4D** | **0** | 0 | ⚠️⚠️ **not one title in 292** |

**The two voids are real and I confirmed them independently**: services and scripted authoring are absent, and **phasing does not appear even once** — so open problem 6 rests entirely on one vault prior (`_hADRIo-ma4`).

---

## 2. ⚠️ What both earlier rounds under-sampled

### 2a. IFC typing and materials — 18 titles, 2 taken

This is where our known gap lives: **our generator emits no types**, and Bonsai's QTO groups by type.

| Id | Title | Why it matters |
| :--- | :--- | :--- |
| `fN9cP6w0DsM` | **Types and Instances in IFC — `IfcElementType` and `IfcElement` Explained** | ⚠️⚠️ Exactly our question, stated as the title. **Free channel (SPB)** |
| `9-mkwEI3m8M` | Wall Layers in Bonsai — **IFC Material Layer Set in Practice** (22 min) | The entity we must emit |
| `rSHAf7GBsUE` | ⚠️ **Wall Joints in Bonsai: Material Layer Connections Explained** | **Wall junctions expressed in IFC** — the nearest thing found to our corner-ownership problem |
| `lR-zcXpnvco` | Windows & Doors in Bonsai — modifiers to **custom types** (45 min) | Round 1 dismissed this whole playlist as *"basic drafting + Inkscape"*. It is 45 minutes on door/window typing |
| `co0lOhmkfH0` | Layered Walls & IFC Materials | |
| `D_-Tta9pffc` | Adding Bonsai project **templates** | |
| `STj9V3Hzk8M` | Loading a **QTO template** | |

### 2b. Spatial structure and containment — 14 titles, 1 taken

| Id | Title | Why it matters |
| :--- | :--- | :--- |
| `lQ_t0neAI9M` | ⚠️⚠️ **"are your IFC elements in the wrong spatial container?"** (15 min) | The silent failure I proposed gating. **A whole video on it** |
| `Y0NUwQNqkKI` | Bonsai **Project Setup**: IFC Project, Levels, Grids, Views (26 min) | Project structure; also from the dismissed playlist |
| `9oXWh1spWys` | **IFC Spaces: what works and what doesn't** | We have rooms; `IfcSpace` drives space boundaries and room QTO |
| `62nQZ7ccz-c` | Extract storey from an IFC project | |
| `Eqtqun9JrWM` | **bSDD** classification | |
| ×5 | georeferencing | ⚠️ Low value for one flat — but `V1VjLOqXuH4` (IFC2X3 is not georeferenced) is schema-relevant |

### 2c. Authoring an IDS — 11 titles, 2 taken

We validate everything and have **no IFC validation at all**. Three videos are about *writing* a specification, not just running one: `s94gzyhP3eU`, `wkdwzTAB8FE`, `Ksz-9552gKY` (a node-based IDS editor). Plus `r2AJe30KUIk`, *Clean and Validate Your IFC Models*.

### 2d. Untouched entirely

`zaqtSQJ_8jw` **BCF in Bonsai** — issue reporting against a model, which is the shape of our own review loop. And six export/viewer titles including `tDOr7p35QUQ` *Export drawings as SVG* and a 34-minute *Bonsai as an IFC viewer*.

---

## 3. The open questions, as they now stand

✅ answered — ⚠️ partial — ⛔ open — 👤 ours to decide.

| # | Question | State |
| :-: | :--- | :--- |
| 1 | Scripted IFC authoring with `ifcopenshell` | ⛔ **Not on YouTube.** 1 title in 292, and it is FreeCAD. Go to documentation instead |
| 2 | Services in IFC — outlets, cable segments, ports | ⛔ **Void confirmed.** No source will answer this |
| 3 | 3D cable routes: modelled run vs zone | ✅ **Answered outside openBIM** — see `00_Master/Model_and_Views.md` |
| 4 | Ceiling-hosted elements | ⛔ Void |
| 5 | Elements in a riser zone | ⛔ Void |
| 6 | IFC phasing — existing / demolished / new | ⛔ **Zero titles.** One vault prior only, and we now need this for a full rewire |
| 7 | 2D discipline sheets from the model | ⚠️ Mechanism known (cut plane → SVG → CSS); **no services sheet exists anywhere** |
| 8 | IFC4 vs 4.3 | ✅ Stay on IFC4 |
| 9 | Bonsai file model, save semantics | ✅ |
| 10 | glTF export and the appearance gap | ✅ settled earlier; 6 unread export titles may add detail |
| 11 | QTO from IFC | ✅ mechanism; ⚠️ **blocked on us emitting types** |
| 12 | Validation / IDS | ✅ **Authoring answered** — `ifctester.org` has an editor and runs **entirely locally, no data egress**. ⛔ We still have no IFC validation at all |
| **13** | ⚠️ **What must an `IfcWallType` + `IfcMaterialLayerSet` carry?** | ✅ **ANSWERED.** Type carries `PredefinedType`, Psets and geometry — all inherited. `Name`/`Tag`/`GlobalId` stay per-instance, and **the type name is the only home of the designation**, which is why schedules group on it |
| **14** | ⚠️ **How does IFC express a wall JOINT?** | ✅ **ANSWERED, AND IT CONFLICTS WITH OURS.** A joint is a **connection** (mitre/butt, breakable), and layer intersection is governed by `IfcMaterialLayer.Priority`, integer 0–100. ⚠️ **Ours is wall-level (thicker, then longer); IFC's is layer-level and authored. Must be reconciled BEFORE layered walls** |
| **15** | **Spatial containment — what breaks, and how is it checked?** | ✅ **ANSWERED.** Wrong containment is a **common** export defect, and the element then vanishes silently from viewers. Our generator calls `spatial.assign_container`; ⛔ **nothing asserts it — gate still to add** |
| **16** | **Do we need `IfcSpace`, and what does it buy?** | ⚠️ **HALF.** Spaces are troublesome and fixable in Bonsai — *"I promise you are going to encounter [problems]"* — but **neither video says what spaces BUY you**. The need is still unevidenced |
| **17** | Is BCF worth adopting for owner review? | ⛔ **NEW. `zaqtSQJ_8jw`** |

---

## 4. What I would take next — 8 videos, ~2.5 hours

In order. All free except where noted.

1. `fN9cP6w0DsM` — **types vs instances** (Q13). The single highest-value title in the corpus for us.
2. `9-mkwEI3m8M` — **material layer sets in practice** (Q13).
3. `lQ_t0neAI9M` — **wrong spatial container** (Q15).
4. `rSHAf7GBsUE` — **wall joints as material layer connections** (Q14).
5. `9oXWh1spWys` — **IFC spaces, what works and what doesn't** (Q16).
6. `lR-zcXpnvco` — **door/window custom types**, 45 min (Q13).
7. `s94gzyhP3eU` — **authoring an IDS** (Q12).
8. `Y0NUwQNqkKI` — **project setup: levels, grids, views** (Q15).

⚠️ **Deliberately NOT taking**: the five georeferencing videos (one flat, no site coordinates), the render/archviz titles (settled), and the CAD-drafting technique titles (we generate geometry).

---

## 5. ⚠️ How to treat what they say

**These are practitioners, not a specification, and they contradict each other and us.** Already recorded: Lloyd Sark says Bonsai MEP is broken while three Russian practitioners model MEP in 3D commercially; openBIM advocacy says Revit can be dropped while Catargiu says two people manage it and Solibri stays.

**The rule this vault already applies** (standing rule 3, and `00_Master/Evidence_Reading_Discipline.md`): **take the mechanism, not the conclusion.** A practitioner explaining *what `IfcMaterialLayerSet` does* is reporting how the schema behaves. The same practitioner saying *you should draw it by hand* is reporting what is efficient **for hand-modelling**, which is the one constraint our pipeline does not have.

> ⚠️ **We reuse their entity choices, their failure modes and their checks. We do not inherit their workarounds**, because most workarounds exist to avoid manual labour we do not pay.

---

## 6. Round 3 — the shortlist, processed (2026-09-17)

**8 of 8 fetched and processed**, all English originals, dates confirmed by `yt-dlp`. Notes: `YT_fN9cP6w0DsM` (SPB ×4), `YT_lQ_t0neAI9M` (BIMvoice ×2), `YT_lR-zcXpnvco` (Dynamite ×2). Findings routed to `18_Digital_Toolchain/analysis/Requirements_And_Validation.md`.

**Questions 12, 13, 14, 15 closed; 16 half-closed.** The one that changed a plan rather than filling a gap is **14**: IFC resolves wall joints by an authored `Priority` on each material layer, which is a *different rule from ours* and must be reconciled before we emit layered walls.

**What is now the top of the list:**

1. ⛔ **Reconcile `wall_corners.csv` with `IfcMaterialLayer.Priority`** — a prerequisite for layered walls, and the external perimeter is layered.
2. ⛔ **Add the containment assertion** to the IFC check. Cheap; guards a silent and demonstrably common failure.
3. ⛔ **Emit types** (`IfcWallType`, `IfcDoorType`, `IfcWindowType` + `IfcMaterialLayerSet`). Now fully specified; blocks all schedules.
4. ⛔ **Author an IDS** for the model. No data leaves the machine.
5. ⚠️ **Phasing has ZERO sources** and we need it for the rewire. Not a YouTube question — go to the IFC documentation.

⚠️ **And a caveat on the corpus itself**, from Christina: Bonsai tutorials pin to a build and *"sometimes very simple features get completely changed"*. **Schema statements and failure modes transfer; click-paths do not.** Every schema claim above should be checked against the IFC documentation before we emit anything — the `Priority` 0–100 range first.

---

## 7. ⚠️⚠️ Review verdict, 2026-09-17 — the plan order was wrong, and a live defect was found

Full verdict recorded in `00_Master/Model_and_Views.md`. Two things change what happens next.

### ⚠️⚠️ THE LIVE DEFECT: IFC identity is not stable across rebuilds

`root.create_entity` is called without supplying an ID, so **every rebuild mints a new `GlobalId` for the same element**. Reproduced 2026-09-17:

```
run1  3ZhvrV1OzFdvQfK9LxCTqv
run2  0iAXyw7RfE2AAXJQL2v2Yp     # same named wall G3, same code, different identity
```

**This is not a future services problem — it is live today for every wall, opening and frame member.** An "authoritative issued representation" that changes every identity on each rebuild **cannot support a durable annotation, a diff, or a review reference**. It also quietly undermines the services migration's own discipline: that migration deliberately mints **no** UUIDs pending review, while the model beside it re-mints all of them on every run.

**Required before types:**

1. assign an **immutable canonical identity** to every persistent element class;
2. derive the IFC `GlobalId` **only** from that identity;
3. give **types their own** immutable identities;
4. ⚠️ **gate identity stability across rebuilds** — build twice, diff the GlobalIds.

⚠️ **And "emit types unblocks all schedules" was overstated.** Types improve standard grouping and inheritance; occurrence-level schedules remain technically possible without them.

### ⚠️ The IDS comes FIRST, not after

The earlier plan emitted types and layer sets, *then* authored an IDS. That is backwards: the IDS would merely describe whatever the generator happened to build. **The IDS states the exchange contract and must FAIL against today's model** — stable identities, correct containment, required type assignment, material-set compatibility, phase/status vocabulary, prohibited proxies, service topology. Implementation then makes the contract pass.

### The corrected order

| # | Step |
| :-: | :--- |
| 1 | Define the resolved intermediate model as geometry **plus topology, phases, decisions, provenance** |
| 2 | ⚠️ **Stabilise identities** for all current occurrences and future types; gate it |
| 3 | ⚠️ **Author the IDS / IFC contract** — before extending the generator |
| 4 | Add containment validation |
| 5 | Emit types and material sets, **compiler polygons staying authoritative**; derive IFC connection semantics from them |
| 6 | Map canonical `existing`/`demolished`/`new` into the chosen IFC4 status representation |
| 7 | Generate terminals, circuits and **minimal port topology** |
| 8 | Generate route geometry **by state only** — none for `topology_only`, provisional for `design_intent`, exact and quantity-bearing for `construction_approved`, site-confirmed for `as_built` |
| 9 | Spatial plans from geometry; **schematics and schedules from the graph** |
| 10 | ⛔ **Do not issue service geometry until the survey and the owner/trade decisions exist** |

### ⚠️ And the honest status of the research

Three practitioners are enough to reject *"3D MEP is inherently unsuitable for residential work."* They are **not** enough to establish automated IFC generation, port-free interoperability, generated service sheets, error rates, or whether exact routing beats route zones before trade approval. Nor does reading 292 titles prove the remaining 269 hold nothing — **two explicitly relevant plumbing videos had no captions at all.**

> **The correct conclusion is: sufficiently supported for a BOUNDED PROTOTYPE and validation exercise — not "the architecture is settled."**
