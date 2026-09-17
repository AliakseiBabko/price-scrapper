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
| 12 | Validation / IDS | ⚠️ Running one is understood; **authoring one is not, and 3 unread titles cover it** |
| **13** | ⚠️ **What must an `IfcWallType` + `IfcMaterialLayerSet` carry?** | ⛔ **NEW. `fN9cP6w0DsM`, `9-mkwEI3m8M` address it directly** |
| **14** | ⚠️ **How does IFC express a wall JOINT?** | ⛔ **NEW. `rSHAf7GBsUE`.** Our corner ownership is canonical data; IFC may have its own opinion |
| **15** | **Spatial containment — what breaks, and how is it checked?** | ⛔ **NEW. `lQ_t0neAI9M`** |
| **16** | **Do we need `IfcSpace`, and what does it buy?** | ⛔ **NEW. `9oXWh1spWys`** |
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
