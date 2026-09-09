# v0 geometry — where it actually stands

**v0 is the baseline layout: the flat exactly as the developer builds it.**
Everything else is a variant measured against it. Its absence is why
`project_decisions.md` calls v0 *"the blocking task"* and why
`Layout_Option_Review.md` had to **withdraw** its v0-against-v1 comparison.

> [!CAUTION]
> **⚠️ NOT CANONICAL YET.** Every dataset here carries `status: DRAFT`.

## The two deliverables

Owner, 2026-09-08: *"I would spread the job into two parts. I would like to have
something which could be exported into AutoCAD format. And also I would like
something I can use for my own model."*

| part | state |
| :--- | :--- |
| **1 — AutoCAD** | ✅ `data/cad/dxf/v0_developer_layout.dxf`, via `tools/layout/export_v0_dxf.py` |
| **2 — his own 3D model** | ❌ **not started.** Needs the glazing and window frames as real openings with sill/head, not plan outlines |

**The DXF, read back and checked:** 25 walls (10 concrete, 10 aerated, 3
external, 2 лоджия), 8 openings, 4 glazing bays + 3 mullions, the slab
extension, 5 suggested-furniture lines, 25 id labels. **Extent 10115 × 10227 mm**
— which is also an independent check that the scale is right.

**Layer colours are the owner's own key**, from
`_Inbox/_Visual_Drop/floor_plan_basic_all_walls.jpg`: red RC frame, green
internal aerated block, magenta external and лоджия.
**`V0-SUGGESTED-FURN` is dashed, orange, and on its own layer so it can be
frozen or deleted in one action.**

## ⚠️⚠️ Two corrections that shaped this — both from the owner

### 1. Stop re-deriving what the model already has

*"We already have all the wall segments. We determine the thickness, the length.
So you're kind of doing double job."* — `wall_blocks.csv` holds 25 named walls
with owner-confirmed classes, thicknesses and lengths; `wall_openings.csv` holds
10 openings. **The only thing missing was POSITION**, because `wall_runs.csv` is
in basic-plan pixels. → **v0 is a REGISTRATION problem.**
`extract_v0_walls.py` is marked SUPERSEDED as a wall inventory.

### 2. The CHAIN is the unit, not the wall

*"There shouldn't be any overlapping in boxes or voids between the wall. They
should touch each other... I did it deliberately, like, without any gap... This
should be, like, one straight segment."* — and precisely: *"junction between G3
and R3 ... there is a gap and R3 extends beyond the line of external wall created
by G2, R3, G3"*, plus *"R1a extends beyond the line created by R1b, G4a, R6"*.

**Both faults had ONE cause: each wall was snapped SEPARATELY** to whichever
vector face pair was nearest, so walls the model deliberately built as one
straight run drifted off each other and grew steps and gaps.

→ **Walls sharing a pixel coordinate and a thickness are now one CHAIN, snapped
once, and laid end to end.** A chain is straight by construction and contiguous
by construction — **a gap or overlap inside one is now impossible, not merely
unlikely.** 18 chains from 25 walls.

## Three traps caught on the way

**⚠️ MC was on the decorative slab, not on the wall.** Owner: *"it's displaced.
You should move it upward... it's overlapped with that external element... but
actual wall is above."* The slab projects outward and **its own edges are
perfectly good face lines**, so a nearest-pair snap preferred it. → **The snap
now requires HATCH between the two faces.** A wall is a hatched solid; the slab
is not. MC moved from 7960/8253 to **8230.6/8530.6**, and every one of the 18
chains now reports `on_hatched_solid: yes`.

**⚠️ Collinear is not contiguous.** R5 and R9 sit on the same line with the
**3.4 m middle room between them**. Grouped as one chain, the contiguity rule
cheerfully closed that "gap" and invented a wall across the room. → **A chain
splits where its members are more than 300 mm apart.**

**⚠️ The pixel runs are NOT wall lengths.** **G6's pixel run measures 3076 mm
against a recorded 1915** — it was traced along the whole partition line
including its door. → **`solid_mm` is the length of record and is what gets
laid.** The drawing supplies the chain's position; the model supplies its parts.
For the one wall pair with no recorded split — **R3 | G3, whose pair total is
5830 mm** from the owner's top-edge chain — the total is used and split evenly,
flagged as undimensioned.

**⚠️ Insulation is not a layer.** Owner: it may be removed or left in place.
External walls export at their recorded **300 mm** and nothing more.

## ⚠️ What is still unreconciled — the residual list

Each chain's laid length is compared against the drawing's own span for it. **13
of 18 chains differ by more than 60 mm**, and those differences are the honest
remaining work, not something to tune away:

| chain | walls | residual |
| :--- | :--- | :--- |
| chain_10 | **G6** | **+1125** |
| chain_03 | R7, G5, R2 | +347 |
| chain_12 | G8 | +340 |
| chain_14 | M2 | +324 |
| chain_17 | M6b | +312 |
| chain_16 | MC | +250 |
| chain_02 | R6, G4a, R1b | +240 |
| chain_11 | G7 | +190 |
| chain_13 | MA | +130 |
| chain_05 | R9 | −120 |
| chain_01 | R1a, G2, R3, G3 | +95 |
| chain_07 | G4b | −90 |
| chain_06 | R8 | +70 |

**The pattern is one-directional: the drawing's span is almost always LONGER
than the sum of recorded lengths.** That is worth reading against the standing
finding that the developer plan reads 1.0–1.9% larger than every measured flat —
but ⚠️ **it is not the same comparison** and must not be conflated with it: this
one is span-versus-recorded-parts inside a single drawing, and the likelier
cause is that a chain's END is still anchored off raster pixel runs.

**Anchoring chain ends properly is the next job**, and it is what would close
most of this table.

## Still missing

- **The лоджия's M2 / M6b are exported as axis-aligned bars** — the real
  enclosure is splayed. The glazing itself is correct and diagonal; its two
  flanking walls are not.
- **Window frame subdivision for MA / MB / MC** is not extracted. The geometry
  is on the drawing (the 19,49 window shows jamb frames and a central mullion
  pair) and **part 2 needs it**.
- **The blue fixtures** — sanitaryware, kitchen — are in the owner's markup and
  not in the export.
- **No corner ownership**, so `check_wall_junctions.py` and
  `build_wall_corners.py` have not been run.
- **O10, the прихожая-to-кухня passway**, has no span row and is absent.

## What none of this changes

**⚠️ Precision is not accuracy.** These are the developer's **project**
dimensions; the as-built runs **+1.0% to +1.9% SMALLER**, 12 of 12. Size nothing
tight from this drawing.

⚠️ **Validate by CHAIN CLOSURE, never against a printed area.**

## The лоджия glazing and the slab — the two elements that are settled

**Glazing** (`extract_v0_elements.py`): run **2963.9 mm**, bearing 164.05°,
assembly depth **150 mm**, **four bays 660.0 · 680.2 · 679.2 · 659.2** with
**three 50 mm mullions** — the owner's *"one block but in four segments"*,
measured. **This upgrades `O9` from a pattern read off a photo of flat 109 to a
measurement off this type's own drawing**, and the width now triangulates three
ways (derived 2939, flat 53's printed 2930, this 2963.9) inside 34 mm.

**Slab extension**: a closed rectangle **1800 × 370 mm**, projecting **320 mm
beyond MC's outer face**, 50 mm wider than the window opening each side. ⚠️ **Not
a wall; never a quantity.** It appears at this window only — MB's carries a 70 mm
line in the same place, and whether that asymmetry is real is unresolved.

**Suggested furniture**: five dashed runs, orange, dashed, own layer. ⚠️ **The
source drawing has NO PDF dash operator at all** — the dashes are exploded into
short segments, so furniture is graphically identical to fabric and only its
~90 mm gap rhythm tells them apart. **❓ Which two are the wardrobes, and is
"drifted to the right" a fault in the developer's suggestion or the reason to
ignore it?**
