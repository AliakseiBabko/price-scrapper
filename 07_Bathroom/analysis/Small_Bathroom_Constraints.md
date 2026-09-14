# Bathroom — Small-Bathroom Constraints

Detail page for [[07_Bathroom/Bathroom_Guide|Bathroom Guide]]. Companion to [[07_Bathroom/analysis/Planning_and_Layout|Planning and Layout]], from which this was split on 2026-09-14 when that page reached the size backstop.

**What changes when the room is small: finished-face arithmetic, the dimensional floors each fixture actually has, what can and cannot be moved, and the door.**

---

## ⚠️⚠️ The Layers Arithmetic (Степан Огурцов, added 2026-09-14)

**From a stated 300+ small bathrooms designed. Directly relevant: this project has a small bathroom and a separate WC.**

### ⚠️⚠️ The layers arithmetic, with a worked failure

| Step | Effect |
| :--- | :--- |
| Measured on the ROUGH substrate | **67 cm** for the washing machine — *«место вагон»* |
| Plaster around the perimeter | **~2 cm** |
| Tile adhesive | **5 mm** |
| Tile | **10 mm** |
| **Result** | **the machine no longer fits** |

**And why it cannot be undone: the bath is already bought, and turning the machine sideways fails because its door will not open.**

> **→ ⚠️⚠️ MODEL TO FINISHED FACES, NOT ROUGH ONES.** **This lands on this repo's own wall-dimension work, where `solid_mm` vs `clear_mm` and the ±50 mm build tolerance are already tracked — see [[00_Master/Geometry_Variance_Study|Geometry Variance Study]].** **The rule: an appliance clearance checked against a rough dimension is not checked at all, and in a small wet room the finish build-up is of the same order as the tolerance.**

### ⚠️⚠️ Minimums, and the order in which things get sacrificed

> **Of bath, WC and basin, the BASIN gives way first** — hence the Soviet habit of overlapping the basin onto the bath.

| Fixture | Minimum |
| :--- | :--- |
| **Bath** | **700 mm wide — it cannot shrink further** |
| **WC** | **⚠️⚠️ 700–800 mm, set NOT by the cistern but by the SEATED PERSON** |
| **Basin** | **400 mm standard minimum**, widening in 100 mm steps |
| **Shower** | **⚠️ he would think twice below 90 × 90 cm** |
| Basin + washing machine side by side | **⚠️ 450 mm (40 basin) + 700 mm (60 machine)** — and such items are barely made |

> **⚠️⚠️ Sizing the WC from the SEATED PERSON rather than from the fixture is a different and better test, and this folder did not have it.**
>
> **⚠️ His decision rule: if basin and washing machine will not both fit alongside, prefer the BATH as the more universal fixture** — soaking things, bathing a child or pet, washing hair. **He otherwise favours a shower precisely because it frees a run for basin plus machine.**

### ⚠️⚠️ Only TWO points on a riser are fixed

> **Where it enters the slab and where it leaves it. Everything between can be changed** — so a riser or towel rail left protruding after a replanning can be re-routed: a straight pipe you design around, or pressed tight to the wall, **and (if the management company does not object) taken into the wall or the screed.**
>
> **→ ⚠️ A liberating geometric insight for a tight room.** ⚠️ **The permission clause is Russian practice; the geometry transfers, the permission does not.**

### ⚠️ Fixtures, the washing machine, and the door

- **Prefer a concealed cistern even here** — nearly the same footprint, better appearance, far easier cleaning. **Reasons for a standard WC: total economy, or when a small ROTATION of the pan materially improves the layout.**
- **⚠️ With a washing machine adjacent, a separate bidet is out** — a hygienic spray is far easier to place, **or a BIDET SEAT, which sits on the pan and needs no wall.**
- **⚠️⚠️ THE COST MYTH: smaller does NOT mean cheaper.** You will not lower your comfort requirements, and cramming them into a small area pushes you to **non-standard fittings and appliances, which cost more.**
- **⚠️ Washing-machine options, in his order**: replanning (including **an opening through the wall that also gains hallway storage**); building it into a wardrobe next door; the kitchen if less cramped; **with 1 m of width, beside the basin under a single worktop**; vertical-loading (front preferred); **under the basin — but then the basin is too high for children or the machine must be an expensive non-standard one**; **wall-mounted, including miniature, several times dearer but opening placements nothing else does.**
- **⚠️⚠️ THE DOOR: short walls mean the opening must be pushed as tight to the wall as possible or the WC protrudes into it.** The opening will be lucky to be **70 cm for a 60 door**; **he has had to fit 50 doors**, and there is no room for elaborate junction detailing.
- **⚠️⚠️ AND THE CHEAPEST SEQUENCING TIP IN THE BATCH: carry the BATH into the bathroom BEFORE the door is installed.**

> [!WARNING]
> **⚠️⚠️ RUSSIAN CLAIMS — flagged in place, NOT routed to `16_Legal_and_Regulations/`, which is Belarus-only.** **In Russia a bathroom may be freely EXPANDED only on the first residential floor, and not over a neighbour's kitchen or living room, so expansion is normally only into corridors or store rooms; and rebuilding walls in the SAME position is said to need no БТИ approval.** **Recorded as the shape of the constraint only.**

[source: [[_Sources/YT_5Ojk5tKyil8_ogurtsov_small_bathroom_rules|YT_5Ojk5tKyil8]]]

## Related

- [[07_Bathroom/analysis/Planning_and_Layout|Planning and Layout]] — the general layout page this was split from.
- [[07_Bathroom/analysis/Tile_Selection_and_Layout|Tile Selection & Layout]] — the tile grid that sets services positions.
- [[13_Surfaces_and_Finishes/analysis/Partition_Construction_and_Wall_Erection|Partition Construction & Wall Erection]] — the thin-partition build-ups.
- [[00_Master/Geometry_Variance_Study|Geometry Variance Study]] — why finished-face modelling matters here.

Part of [[07_Bathroom/Bathroom_Guide|Bathroom Guide]].
