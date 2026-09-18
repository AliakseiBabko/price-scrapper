# What the flat permits — four layers, kept apart on purpose

**2026-09-18, rewritten the same day after review.** Measured against the compiled model (`v0-existing/spec.json`, 25 walls, schema v2).

> [!CAUTION]
> **⚠️⚠️ THE FIRST VERSION OF THIS PAGE PROMOTED DESIGN RULES AND UNPROVEN FEASIBILITY INTO STRUCTURAL FACTS.** Seven defects were reproduced against it, including a second rule-9 endpoint error of the same family as the two the owner caught. **The fix is not better wording — it is that the four layers below must never be stated in the same voice.**
>
> | layer | what it is | how certain |
> | ---: | :--- | :--- |
> | **1** | compiled geometry | measured, gated |
> | **2** | owner-authored allocation rules | **chosen**, not derived |
> | **3** | candidate feasibility | **conditional** on layer 4 |
> | **4** | unresolved manufacturer / layout inputs | **unknown** |

---

## Layer 1 — compiled geometry. What the building is.

### 1.1 All daylight arrives from one side

Three windows and the лоджия glazing, every one on the **south** façade, which steps northward as it runs west. The entrance `O8` is at **y 15990**, the far north.

| opening | host | x extent |
| :--- | :--- | :--- |
| `O3` living-room window | `MC` | 9381 … 12946 |
| `O2` middle-room window | `MB` | 6131 … 9131 |
| `O4a`/`O4b` window + лоджия door | `MA` | 2931 … 5881 |
| `O9` лоджия glazing | `M2 → M6b` | the mitred south-west corner |

**What this proves: every habitable room shares one depth axis — entered from the north, lit from the south — and therefore one light gradient.** That is all it proves. See layer 2.

### 1.2 The flat is a comb

A north service spine (y 12600 … 16240) carries the entrance, both ventilation shafts, both plumbing anchors and both wet rooms. Three habitable bays hang south off it, separated by the 75 mm dividers `G8` and `G7`.

⚠️⚠️ **The bay widths below are CLEAR, face to face.** The first version of this page mixed envelope coordinates with clear dimensions and reported 3125 / 3000 / 3740 — and then drew a conclusion from the comparison, which was the error.

| bay | clear span | between | concrete return |
| :--- | ---: | :--- | :--- |
| **west** | **2825.1** | `R6` east face 3230.9 → `G8` west face 6056.0 | `R6`, 1750 clear |
| **middle** | **3000.0** | `G8` east 6131.0 → `G7` west 9131.0 | `R8`/`R9`, 1490 each |
| **east** | **3489.9** | `G7` east 9206.0 → `R7` west 12695.9 | `R7`, 1750 clear |

> **⚠️ THE WEST BAY IS THE TIGHTEST, AT 2825 — NOT THE MIDDLE.** The first version said the middle at 3000 was tightest, which inverted the answer. The east bay narrows further at the façade return, so even 3489.9 is not uniform down its depth.

### 1.3 `R6` and `R7` are the same element mirrored

Each is the north continuation of a façade return, one per **outer** bay: `R6` at x 2981…3231 / y 9350…11100, north of `MA`; `R7` at x 12696…12946 / y 8531…10280, north of `MC`. Both 250 mm concrete, both **1750 mm clear**.

### 1.4 The wet zone cannot move

`P1` (туалет, beside `V1`) carries hot and cold water — **the flat's only water source** — the main sewer stack and the capped towel-rail tails. `P2` (between `R3` and `V2`, 400 × 200) is **sewer only, no water**; kitchen water arrives from `P1` under the floor. `T1`'s tails cross `G4b` and their emergence point fixes where the rail can go.

### 1.5 Concrete spans, all of them

`R3` 2740 · `R6` 1750 · `R7` 1750 · `R2` 1675 · `R8` 1490 · `R9` 1490 · `R4`/`R5` 1050. Plus `G7` and `G8` at **3250 each**, block.

---

## Layer 2 — owner-authored rules. What he has chosen.

⚠️⚠️ **THESE ARE DESIGN DECISIONS. THE BUILDING DOES NOT IMPOSE THEM AND THIS PAGE MUST NOT SAY IT DOES.**

- **`DI-007`** — daylight is allocated to study positions first; the window wall takes the desk.
- **`DI-008`** — each room bands entrance → storage → bed → window.

**The earlier claim that single-sided daylight *forces* `DI-008` was false.** A common light gradient does not assign *storage, bed and study* to successive bands — that assignment is the owner's, and it is a good one. **The counterexample is already canonical:** `PAR-KIDS-BED-PLACEMENT` puts beds beside `R4`/`R5`, at the entrance end — the very band `DI-008` gives to storage. A derived rule could not contradict itself that way; an authored one can, and this one does.

What layer 1 *does* contribute: because there is only one depth axis, `DI-008` is **checkable** — a placement can be tested against the ordering. That is a property of the rule's shape, not evidence for its content.

---

## Layer 3 — candidate feasibility. Conditional, every line of it.

### 3.1 Wall-bed positions

> **`R6` and `R7` are the two currently eligible, unconditional concrete candidates in intended sleeping zones.** They are **not** the only physically possible positions.

- `R3` (2740) and `R2` (1675) are excluded **by present use** — entrance end and kitchen — not by structure. A zoning change re-opens them.
- `R8`/`R9` (1490) are excluded **by `DI-007`**, a design decision, not by geometry.
- `G7`/`G8` (3250 each) are block, and `PAR-BED-SUBSTRATE` **explicitly permits** non-concrete support via chemical anchors or a floor-bearing frame. **So the middle bay is not prohibited.** The earlier claim that it "cannot host a wall bed at all" was false; it is *unattractive* — the frame eats floor depth, and `DI-007` wants that wall for a desk.

### 3.2 Bed width

**Proven:** an 1800 mattress cannot fit `R6`/`R7` — it misses 1750 by 50 mm before any cabinet is counted.

**Not proven:** that 1600 fits. `design_envelopes.csv` says it correctly and the earlier version of this page contradicted its own canonical record: **the cabinet is the object that must fit, not the mattress**, and its external width is a manufacturer figure nobody has. 1600 remains conditional on cabinet width, fitting clearance and open-bed clearance.

### 3.3 `G7` and `G8` are two coupled variables — not one decision

Two divider coordinates with a fixed total give **two degrees of freedom**, not one. And `R8`/`R9` fix the façade-side boundaries of the middle bay, so **moving `G7` or `G8` changes only the deeper portion** unless a jog is introduced. The earlier claim that either "re-proportions an entire façade bay" was wrong.

---

## Layer 4 — unresolved inputs. Nothing downstream may assume these.

| | what is missing | what it blocks |
| :--- | :--- | :--- |
| **cabinet external width** | manufacturer figure, any bed | whether 1600 fits `R6`/`R7` at all |
| **mattress thickness** | manufacturer figure | the cabinet depth, and so the floor depth it costs |
| **`ENV-DINING`, `ENV-KITCHEN-RUN`** | clearances | whether the kitchen/living zone survives being closed |
| **partition parked depth** | leaf count × leaf width | where the glass divider goes when open |
| **`V1` footprint** | unestablished, needs re-measurement | any clearance question around it |
| **`BAND-KL-3`** | desk or no desk at the living-zone window | `SC-A` and `SC-B` want different answers |

---

## What the first-fix finding actually is

**The earlier claim that the first-fix problem is "halved" was false, because it ignored `SC-NOW` — which is the only scenario being built.** The middle room holds **both children now** and one girl later, so its rough wiring must serve two beds and shared use *and* later single-child use. That is not one answer.

The accurate statement is narrower and still useful:

> **The Phase-2 differences between `SC-A` and `SC-B` are confined to the two outer bays.** The middle bay's *Phase-2* role does not branch. Its *Phase-1 to Phase-2* change still does.

⚠️ **And a related record was wrong:** `SC-NOW` had the small bedroom `unassigned`, contradicting `Family_Requirements.md` — in Phase 1 **the adults occupy it**, the living zone has no bedroom function at all, and the wall bed is installed now for activation in 3–4 years. Corrected 2026-09-18.
