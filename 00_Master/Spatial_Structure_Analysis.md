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

⚠️⚠️ **The x extents below are the OPENINGS. An earlier version printed the HOST WALL bounds instead** — the fourth error of one family in three days: quoting a container's bounds as the contained thing's. `O2` is 1800 wide, not the 3000 of `MB`.

| opening | host | **opening** x extent | width |
| :--- | :--- | :--- | ---: |
| `O3` living-room window | `MC` | 10235.9 … 12035.9 | 1800 |
| `O2` middle-room window | `MB` | 6731.0 … 8531.0 | 1800 |
| `O4` window + лоджия door | `MA` | 4351.0 … 5731.0 | 1380 |
| `O9` лоджия glazing | `M2 → M6b` | 3130.9 … 6022.1 | 2891 |

> [!WARNING]
> **⚠️ THE COMPILED WIDTH AND THE MEASURED WIDTH DISAGREE, and a consumer must know which it is using.** The compiler places `O2` and `O3` at **1800** — the developer plan's figure. `wall_openings.csv` records **1760** and **1763**.
>
> ⚠️⚠️ **THOSE MEASUREMENTS ARE FROM COMPARABLE FLATS, NOT THIS ONE.** An earlier version said *"use 1760 for any fit"*, which was too broad — it promoted another flat's measurement into this flat's dimension. Correctly:
>
> - **1800 stays the planned nominal.**
> - **1760 is a conservative design allowance**, useful because the developer plan reads 1.0–1.9% larger than every as-built comparable.
> - **Anything fabricated to the opening — a blind, a curtain track, a fitted worktop — needs THIS FLAT measured.** Neither figure is good enough for that.
>
> ⚠️ `O2` also leaves exactly **two 600 mm masonry piers** either side — 6131…6731 and 8531…9131 — at the 1800 figure. At 1760 they are 620.

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
- `G7`/`G8` (3250 each) are block, and `PAR-BED-SUBSTRATE` **explicitly permits** non-concrete support via chemical anchors or a floor-bearing frame. **So the middle bay is not prohibited.** The earlier claim that it "cannot host a wall bed at all" was false; it is *less attractive* — the frame eats floor depth, and `DI-007` wants the window wall for a desk.

> [!IMPORTANT]
> **⚠️⚠️ AND I APPLIED ADULT BED WIDTHS TO A CHILDREN'S ROOM, WHICH IS THE PLAINEST ERROR ON THIS PAGE.** The middle bay is the children's room — both children now, the daughter later. **Children use single beds.** A 900 mm wall-bed cabinet is roughly 1000–1040 external and a 1200 mm one roughly 1300–1340 (trade figures, not vault-sourced). **Both sit comfortably inside `R8`/`R9`'s 1490 mm clear**, with room to spare even after tolerance and plaster.
>
> So `R8`/`R9` are not merely "unresolved for 1400": on **wall length** they are credible candidates for a child's wall bed, which is a genuinely different situation from the one this page described.
>
> ⚠️ **But "comfortable" was still too strong, and an earlier version said it.** Those cabinet ranges are unsourced trade rules of thumb. What is established is **wall-length compatibility**; full feasibility still needs the manufacturer's width, the cabinet depth against the room, circulation, and whatever else wants that wall. `DI-007` is the only *policy* exclusion on the table — it is not necessarily the only remaining *feasibility* check.

### 3.2 Bed width

**Proven:** an 1800 mattress cannot fit `R6`/`R7` — it misses 1750 by 50 mm before any cabinet is counted.

**⚠️⚠️ AND 1600 NOW LOOKS DOUBTFUL TOO, WHICH REVERSES THE WORKING ASSUMPTION.** The cabinet is the object that must fit, and the clear span is not all available:

```
R6/R7 clear                                    1750
less build tolerance, AGENTS.md ±50             -50  →  1700
less plaster on the perpendicular façade wall   -20  →  1680 usable
```

A 1600 wall-bed cabinet is **typically 1690–1740 mm external** — a trade figure, **not vault-sourced**, and it must be replaced by a manufacturer's number before anyone relies on it.

> **⚠️ THE DEFENSIBLE VERDICT IS NARROWER THAN "MAY NOT FIT AT ALL", WHICH IS WHAT AN EARLIER VERSION SAID.** The 1680 figure is a *conservative design envelope*, not a measurement: the ±50 is **uncertainty**, not 50 mm known to be lost. The plaster deduction is real; the tolerance may or may not land against us. So:
>
> **1600 CANNOT BE RELIED UPON at `R6`/`R7`, and a sofa version is especially unlikely to fit.** It is unresolved — not proven impossible. A specific cabinet's external width and fitting clearance settles it either way.

⚠️ Both columns form an internal corner with masonry at their south end — `R6` meets `MA` at y 9350.3, `R7` meets `MC` at y 8530.6 — so the plaster deduction is real, not hypothetical.

⚠️ **And a living-room wall bed is often a `шкаф-кровать-диван`**, whose armrests routinely push the assembly past 1800. If the `R7` unit is to include a sofa, it is very unlikely to fit at all.

### 3.3 `G7` and `G8` are grid-aligned partitions with a HIGH RELOCATION PENALTY

The first version called them *"close to the only real freedom in the plan."* **Both are structural infill locked between 250 mm concrete columns, flush on both ends:**

| divider | x | south end | north end |
| :--- | :--- | :--- | :--- |
| `G8` | 6056.0 … 6131.0 | meets `R8` (5881…6131) — **east faces flush at 6131** | meets `R4` (6056…6306) — **west faces flush at 6056** |
| `G7` | 9131.0 … 9206.0 | meets `R9` (9131…9381) — **west faces flush at 9131** | meets `R5` (9131…9381) — **west faces flush at 9131** |

⚠️ `G8` is pinned to *two different faces*, 75 mm apart — exactly its own thickness. **Moving either divider off its axis detaches it from the columns and leaves 250 mm of concrete projecting into a room as a raw pier**, and on the `G8` side it also eats into `O2`'s 600 mm window jamb.

> **⚠️ THE DEGREE OF FREEDOM IS NOT REMOVED — IT IS EXPENSIVE.** An earlier version called these "PINNED", which was an over-correction in the opposite direction from "the only real freedom in the plan", and it contradicted the owner's own `DI-006`: *"even the room dividers… most likely we're not going to destroy them completely, probably move just a little bit."* **That is his authority to give, and calling the dividers immovable overrides it.**
>
> The accurate statement: **moving `G7` or `G8` costs the flush column junction and creates a pier or a jog that must be deliberately resolved**, and on the `G8` side it also eats into `O2`'s window jamb. A real consequence, and a reason to move them only on purpose — not a prohibition.

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

⚠️⚠️ **And the living/kitchen zone has THREE states, not two** — `SC-NOW` open with no bedroom function, `SC-A` with adults behind the partition, `SC-B` with a schoolboy who needs a desk at the window. It also carries the kitchen's dedicated high-load circuits, the partition track, multi-zone lighting either side of it, the wall-bed power and media, and the `P1`/`P2` plumbing. **Treating the three bays as equal thirds was wrong in the other direction too: this zone is the larger part of the first-fix problem, not a third of it.**

⚠️ **And a related record was wrong:** `SC-NOW` had the small bedroom `unassigned`, contradicting `Family_Requirements.md` — in Phase 1 **the adults occupy it**, the living zone has no bedroom function at all, and the wall bed is installed now for activation in 3–4 years. Corrected 2026-09-18.
