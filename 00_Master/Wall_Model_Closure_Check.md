# Wall model — closure and connectivity check

**Written 2026-09-04, to answer one question: is the wall-segment stage finished, and can dimensions start?**
The short answer is **yes for the structure, no for one correction the check itself found.**

Model under test: `data/canonical/wall_materials.json`, `wall_blocks.csv`, `wall_openings.csv`.
Drawing: `_assets/wall_segments_v9.png`.

---

## 1. ⚠️⚠️ What the check found, and it corrects my own earlier work

**There is NO WALL between the кухня (5.24) and the living room (19.49).** Verified on the detailed plan at 5×:
the only things on that line are a **dashed zone boundary** and a **dash-dot grid axis**. No hatching, no
thickness, no jambs.

→ **So in `v0` the кухня is not a room. It is a NOMINAL ZONE inside one undivided 24.73 m² space**, and the
5.24 / 19.49 split is the developer's **area accounting**, not a partition.

### That forces me to withdraw two of the four arguments I gave for `v1`'s kitchen move

Earlier in this session I recorded four independent supports for it. Re-tested against this finding:

| argument | status |
| :--- | :--- |
| **Separability** — the zone must be splittable into a real isolated room (the owner's own thesis) | ✅ **Stands.** Unaffected |
| **Acoustics** — the middle room has no party walls, so the children belong there | ✅ **Stands.** A separate question |
| **Daylight** — *"merging the kitchen into the living room is the only way that zone gets daylight"* | ⚠️ **WITHDRAWN.** They are already one space, so the zone already borrows the living room's window. It is *badly* lit, being at the far end from the glazing, but "no daylight" was wrong |
| **Ventilation** — *"supply has no route to the kitchen zone without ducting"* | ⚠️ **WITHDRAWN.** A through-wall unit in the living room serves the whole open space. The zone has no external wall of its own, which is what I checked — but it does not need one |

→ **⚠️ Both withdrawn arguments failed the same way: I checked whether the KITCHEN had an external wall, and
never checked whether it was an enclosed room.** A zone label on a plan is not a room, and I treated it as
one for several rounds.

→ **What survives is enough.** The owner's separability thesis was always the primary reason, and it does not
depend on any of this. But the review's claim that the move "rests on three independent arguments" is now
**one**, plus the acoustics point about a different room.

---

## 2. Enclosure — does every room's boundary close?

**Yes, all eight, once the кухня/living space is treated as one.**

| room | bounded by, clockwise | closes |
| :--- | :--- | :--- |
| **туалет** 1.24 | R1a · G4C *(O7)* · G4b · R1b | ✅ + **V1 shaft standing inside it** |
| **ванная** 3.09 | G4b · G4C *(O1)* · G4d · G4a | ✅ |
| **9.36 room** | G4d *(O6)* · G8 · MA *(O4a, O4b)* · G4a + R6 | ✅ |
| **16.64 middle room** | G6 *(O5)* · R5+G7+R9 · MB *(O2)* · R4+G8+R8 | ✅ |
| **кухня + living, 24.73** | R3 + **divider (V2 · O10 · R5)** · G3 · R2+G5+R7 · MC *(O3)* · G7 | ✅ **as ONE space** |
| **прихожая** 9.79 | R1a+G2 *(O8)* +R3 · **divider** · G6 + G4d · G4C | ✅ |
| **лоджия** 6.05 | MA · M6b · **O9 glazing, full height and full length** · M2 | ✅ |

**No unaccounted gaps.** Every boundary segment is either a wall, a shaft, or a named opening.

---

## 3. Connectivity — the flat is a tree, not a loop

Reading the openings as edges between rooms:

```
        [common corridor]
                │ O8  (entrance door, 1010, in G2)
                ▼
          ┌─ прихожая 9.79 ──────────────────┐
   O7 ────┤                                  ├──── O10  passway ~958, NOT a door
   туалет │  O1 ── ванная 3.09               │
          │  O6 ── 9.36 room ── O4a/O4b ── лоджия 6.05 ── O9 glazing (due south)
          │  O5 ── 16.64 middle room
          └──────────────────────────────────┘
                                              кухня + living 24.73 ── O3 window
```

Three properties fall out, and each one matters:

1. **⚠️⚠️ IT IS A TREE — there is no circulation loop anywhere.** Every room hangs off the прихожая, and the
   прихожая is the only hub. There is no second route between any two rooms. **So the hall is a single point
   of failure for circulation, and every trip between rooms passes through it** — which is what makes its
   9.79 m² worth arguing about, and what makes the corridor-to-room trade a real decision rather than a
   tidy-up.
2. **⚠️⚠️ O10 IS THE ONLY EDGE INTO THE LARGEST SPACE, AND IT IS ~958 mm WIDE AND CANNOT BE WIDENED** (shaft
   one side, RC column the other). **The biggest room in the flat is reached through the narrowest permanent
   gap.** See `wall_materials.json` → `the_prihozhaya_kuhnya_divider`.
3. **The лоджия is a LEAF BEHIND A LEAF.** It is reached only through the 9.36 room — so whoever occupies that
   room controls access to it. **In Phase 1 that is the adults; in Phase 2 it becomes the boy's room.**
   ⚠️ **Since there is no basement store, the лоджия is also the household's only bulk-storage volume — so from
   Phase 2 onward, the family's storage is behind a child's bedroom.** That is a real planning consequence and
   it has not been recorded anywhere else.

---

## 4. So: is the wall-segment stage done?

**Structurally, yes.**

- ✅ **25 walls**, each with a class, a thickness and, where it applies, an insulation thickness. Every
  thickness is either stated by the owner or derived from the plan's printed 175 step. None is my own guess.
- ✅ **2 ventilation shafts**, as their own class — not walls, but carrying finishable surfaces.
- ✅ **1 composed divider** (shaft + passway + column).
- ✅ **11 openings**, every one hosted.
- ✅ **All eight room boundaries close.**
- ✅ Corner rule, thickness-change rule and no-split-at-openings rule applied consistently.

**Dimensionally, no — and that is the next stage, not a defect:**

| | |
| :--- | :--- |
| **Lengths** | 10 of 25 walls carry a printed figure; the rest need reading or the owner's min/max |
| **Sill and head heights** | Unmeasured for O2 and O3. Two numbers unlock every window band, since finish areas are derived |
| **⚠️ Four blob-derived junctions** | G4C's two openings *(not printed at all — least trustworthy)*, MA's O4a/O4b boundary, whether G6's O5 starts at R4, where G4d's O6 begins |
| **Height datum** | Is 2500 mm from the screed or slab to slab? It multiplies every surface area |

---

## 5. The rule this check earned

**⚠️⚠️ A LABEL ON A PLAN IS NOT A ROOM.** The кухня had an area, a name, a printed dimension chain and kitchen
fixtures drawn in it — everything a room has except walls. **Before treating any labelled space as enclosed,
check its boundary for hatching.**

→ And more generally: **this is what the closure check is for.** Four rounds of reasoning rested on the кухня
being a room, and one crop settled it. **The check should have been run when the model was first assembled,
not when it was declared finished.**
