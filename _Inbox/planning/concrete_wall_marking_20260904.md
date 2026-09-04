# Wall materials — the owner's colour marking, 2026-09-04

**Status: READ AND ENUMERATED, PENDING CONFIRMATION OF THE READING.** Deliberately **not** yet promoted into
`data/canonical/current_apartment_shell.json`, because `make_variant.py` checks layouts against those
constraints and a wrong entry would either block a valid design or license removing something structural.

**Sources, both on the basic developer plan (3Б/2+, 1061 × 1112):**

| file | what |
| :--- | :--- |
| `_Inbox/_Visual_Drop/floor_plan_basic_concrete_walls.jpg` | first pass — **concrete only**, in red |
| `_Inbox/_Visual_Drop/floor_plan_basic_all_walls.jpg` | **complete pass — all walls**, three colours |
| `_assets/wall_material_regions.png` | **the numbered reading** (R1–9, G1–8, M1–6) |
| `_Inbox/planning/wall_material_regions.json` | the detected bounding boxes |

✅ **Consistency check passed: the red regions in the two independent markups agree to within 2 px.**

The owner's classes, in his words:

- 🟥 **Red — concrete.** Structural walls and columns.
- 🟩 **Green — internal walls, autoclaved aerated block** («air can create… another bubble» — газобетон /
  газосиликат). **Thicknesses: from 75 mm, 120 mm in the bathroom, up to ~200 mm between apartments.**
- 🟪 **Light purple / magenta — the outside walls.** *"Probably they look like a similar material, but they go
  outside. Probably that was the reason to use different [hatch] for them."*
- ⬛ **A third hatch = INSULATION, and the owner is explicit that IT IS NOT A WALL.** Attached to the actual
  wall, adding **~70 to 100+ mm** of thickness.

**The owner states the marking is complete: "I marked all the walls."**

---

## ⚠️⚠️ First, the finding that makes this irreplaceable: the drawing does not encode material

The owner asked whether the hatching inside the wall sections could distinguish these without his help.
**Tested, and the answer is no.**

**The decisive counter-example is R3.** The red-marked run of the top wall and the **green** segments on either
side of it — **G2 to its left and G3 to its right, the same wall** — are drawn with **identical thickness and
identical diagonal hatching**. One wall, one graphic convention, three different materials along its length.

- **What the drawing DOES encode is thickness** (250 structure, 75 partition, 120 wet block) — exactly the
  *"200 mm threshold … not a structural survey"* heuristic the layout skill already warns about.
- **Thickness would have actively misled**: R2/G5/R7 are three segments of the *same* right-hand wall.
- → **This cannot be re-derived, now or later. It is owner-supplied evidence and must be recorded as such.**

## The structural logic, which the marking makes visible

**Every perimeter wall is mixed by SEGMENT, not uniform:**

| wall | reading, in order |
| :--- | :--- |
| **top** (above прихожая / кухня) | **G2 → R3 → G3** — block, then ~3 m of concrete, then block |
| **right** (кухня / living) | **R2 → G5 → R7** — concrete, block, concrete |
| **left** (туалет / ванная / 9.36) | **R1 → G4 → R6** — same pattern |
| **middle room, both side walls** | **R4 → G8 → R8** and **R5 → G7 → R9** — concrete at BOTH ends, block infill |
| **bottom + loggia** | **M1–M6**, the only walls marked as going outside |

→ **⚠️⚠️ THIS ANSWERS THE EARLIER QUESTION ABOUT R8/R9. They are not a separate category: R4, R5, R8 and R9
are the FOUR ENDS of the middle room's two side walls, with G7 and G8 as the block infill between them.** The
two the owner described as *"columns in the middle next to the entrance area"* are **R4 and R5** — the pair at
the прихожая end. R8/R9 are the same thing at the balcony end, and they are longer (≈180 px against ≈110).

→ **The pattern reads as a frame: concrete at wall ends and in discrete runs, aerated block filling between.**
That is consistent with the owner's own note that some walls are *"partially concrete and partially softer
material."*

## The regions

Detected programmatically (connected components ≥120 px), not by eye. **Coordinates are px in the source
image. The mm equivalents are NOT established** — the marker stroke inflates every box by roughly its own
width, and no scale factor for this image has been derived. **For identification, not measurement.**

### 🟥 Concrete — 9 regions

| # | bbox px | px | reads as |
| :--- | :--- | :--- | :--- |
| R1 | 22,40 – 226,172 | 205 × 133, L | outer corner at the туалет |
| R2 | 1010,41 – 1038,237 | 29 × 197 | right wall alongside the кухня |
| R3 | 421,44 – 695,70 | 275 × 27 | **~3 m run of the top wall above the прихожая** |
| **R4** | 335,305 – 364,414 | 30 × **110** | **COLUMN — middle room, прихожая end, left** |
| **R5** | 648,306 – 676,414 | 29 × **109** | **COLUMN — middle room, прихожая end, right** |
| R6 | 23,566 – 54,739 | 32 × 174 | left wall beside the 9.36 room |
| R7 | 1009,650 – 1038,822 | 30 × 173 | right wall beside the living room |
| R8 | 319,741 – 347,921 | 29 × 181 | middle room, left wall, **balcony end** |
| R9 | 646,744 – 675,923 | 30 × 180 | middle room, right wall, **balcony end** |

### 🟩 Aerated block — 8 regions

| # | bbox px | px | reads as |
| :--- | :--- | :--- | :--- |
| G1 | 227,39 – 248,122 | 22 × 84 | short wall between туалет and прихожая |
| G2 | 344,41 – 419,72 | 76 × 32 | top wall, **left of R3** |
| G3 | 697,43 – 1011,69 | 315 × 27 | top wall above the кухня, **right of R3** |
| G4 | 21,173 – 248,565 | 228 × 393, complex | **the whole ванная / туалет block** plus the left wall beside it — the 120 mm walls |
| G5 | 1008,238 – 1037,649 | 30 × 412 | right wall **between R2 and R7** — the long middle span |
| G6 | 451,304 – 649,317 | 199 × 14 | top wall of the middle room's **1915 × 1050 recess** |
| G7 | 644,410 – 660,743 | 17 × 334 | middle room, right side wall, **main span** (75 mm) |
| G8 | 334,411 – 347,743 | 14 × 333 | middle room, left side wall, **main span** (75 mm) |

### 🟪 External — 6 regions

| # | bbox px | px | reads as |
| :--- | :--- | :--- | :--- |
| M1 | 21,740 – 167,775 | 147 × 36 | wall between the 9.36 room and the **лоджия** |
| M2 | 23,778 – 41,982 | 19 × 205 | лоджия, outer left wall |
| M3 | 674,822 – 765,858 | 92 × 37 | living room, bottom wall (left of the window) |
| M4 | 943,823 – 1039,853 | 97 × 31 | living room, bottom wall (right of the window) |
| M5 | 585,890 – 650,921 | 66 × 32 | bottom wall beside the middle room's window |
| M6 | 329,891 – 411,1068 | 83 × 178 | лоджия, right wall including the angled return |

→ **The magenta set is the лоджия enclosure plus the window walls at the bottom** — i.e. the façade runs along
the **bottom** of the plan (windows in the middle room and living room, лоджия bottom-left). **Everything the
owner marked green on the perimeter is therefore probably a party wall or the common-corridor wall, not
external** — which would explain both the colour choice and his *"up to 200 between the apartments"*.
**That inference is mine; question 1 below.**

## ⚠️⚠️ Insulation: a modelling rule, not a wall

**The owner is explicit that the third hatch is insulation attached to the wall, not a wall — adding ~70 to
100+ mm.** That has to be honoured in the model:

- **It is a LAYER on an external wall, never a wall in its own right.** The shell carries walls with position
  and thickness; adding insulation as a wall would corrupt the shell and every area derived from it.
- **He describes it as OUTSIDE insulation**, so on that reading it does **not** eat internal clear
  dimensions — it grows the envelope outward. **⚠️ Worth confirming (question 4), because if any of it is
  internal it comes straight off the room, and 70–100 mm is far outside the ±25 mm band.**
- It is a real input to an **open content gap** the vault already records: no source yet covers a
  three-season glazing/insulation upgrade sized to keep an unjoined лоджия frost-free without heating
  (`00_Master/Family_Requirements.md`, §10). **If the лоджия walls already carry 70–100 mm, that changes the
  starting point of that calculation.**

## ✅ The wall-reading key — `_assets/wall_reading_key.png`

**The owner asked for an image showing my naming and my current understanding of the wall placement, so he can
answer precisely. That is it.** Built on his own three-colour markup so his colours show through, with:

- **my segment IDs** R1–9, G1–8, M1–6 as circles;
- **◇ 1–10 — the MATERIAL JUNCTIONS**, drawn as diamonds so they never read as segments. Each marks where I
  believe the material changes **along one continuous wall**, which is the thing that cannot be read from the
  drawing and therefore the thing worth confirming;
- **what is on the other side of each wall** — neighbour flat, block joint, corridor, façade;
- **the confirmed orientation**, with the лоджия's due-south glazing called out.

### The ten junctions, and the question at each

**For each: is there a real joint there, and is my position about right?**

| ◇ | wall | my reading |
| :--- | :--- | :--- |
| 1 | top | G2 → R3 |
| 2 | top | R3 → G3 |
| 3 | right (block joint) | R2 → G5 |
| 4 | right (block joint) | G5 → R7 |
| 5 | left (in-block party) | R1 → G4 |
| 6 | left (in-block party) | G4 → R6 |
| 7 | middle room, left wall | R4 → G8 |
| 8 | middle room, left wall | G8 → R8 |
| 9 | middle room, right wall | R5 → G7 |
| 10 | middle room, right wall | G7 → R9 |

### ⚠️ Where I am least sure, stated on the image itself

- **R1 and G4 came out L-shaped in the detection**, so **◇ 5 and ◇ 6 may be misplaced.**
- **G4 covers the whole ванная/туалет block as ONE region.** If those walls differ from each other — and the
  plan prints 120 mm there against 75 mm elsewhere — that single region is hiding the difference.
- **And the open question that matters most: is anything I have labelled NOT a wall?** The insulation is
  already excluded by the owner's own instruction, but a короб or a fixture outline could have been caught.

## ⚠️ What still needs the owner, before promotion to a constraint

1. **Is the green perimeter a PARTY WALL rather than an external one?** R2/**G5**/R7 on the right, G2/R3/**G3**
   on top, R1/**G4**/R6 on the left are all perimeter positions marked green — which fits *"up to 200 between
   the apartments"* if they separate flats or face the common corridor. **Confirm, because it decides whether
   they carry the insulation layer and whether they are acoustically party walls** (the vault holds a
   soundproofing stopping rule that applies to party walls specifically).
2. **Which walls are the ~200 mm ones?** Presumably the party walls. ⚠️ **Note a conflict to resolve: the
   detailed plan prints `250` for what it calls party wall or structure, and the owner estimates ~200. One
   of the two is wrong, or they are measuring different things (structure vs finished).**
3. **R3 — is there a real joint** where the ~3 m concrete run meets G2 and G3, or is the boundary approximate?
4. **The insulation: which walls carry it, and is it definitely OUTSIDE only?** See above — an internal layer
   would come off the room.
5. **Exhaustiveness.** The owner states *"I marked all the walls."* Recorded as such. ⚠️ **No automated
   completeness check has been run against the drawing's own wall linework**, so "unmarked" is still treated
   as *unknown* rather than *absent* until either that check runs or the owner reconfirms.

## Recorded conventions

- **Handedness:** both markups are the **same handedness as the detailed plan** (туалет top-left, лоджия
  bottom-left off the 9.36 room, кухня top-right). **No mirroring correction applies.**
- **Which plan:** the markup is on the **basic** plan (3Б/2+), not the dimensioned **detailed** one. They agree
  on layout; their printed areas differ, and **per the standing instruction those areas are not evidence
  anyway.** ⚠️ **But the grid key (`_assets/wall_key_plan.png`) was built on the DETAILED plan, so its
  A–L × 1–12 references do not transfer to these images.** Positions here are px plus words.
- **Per the 2026-09-04 instruction, no area figure from any source is evidence.** Nothing above uses one.
