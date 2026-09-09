# v0 geometry — where it actually stands

**v0 is the baseline layout: the flat exactly as the developer builds it.**
Everything else is a variant measured against it. That gap is why
`project_decisions.md` calls v0 *"the blocking task"*, and why
`Layout_Option_Review.md` had to **withdraw** its comparison of v1 against v0.

> [!CAUTION]
> **⚠️ NOTHING HERE IS CANONICAL YET.** Both datasets carry `status: DRAFT`.
> Do not build a variant, a quantity or a drawing on them.

## ⚠️⚠️ THE CORRECTION THAT DEFINES THIS PAGE — 2026-09-08

**Owner:** *"We already have all the wall segments. We determine the thickness,
the length. So you're kind of doing double job right now. Try to sort out the
polygons in the vector image just to create overlay and include all of the wall
segments we already marked and with their parameters."*

**He is right, and the first pass was the wrong job.** `wall_blocks.csv` already
holds **25 named walls** with owner-confirmed classes, thicknesses and lengths;
`wall_openings.csv` holds **10 openings** with widths, sills, heads and host
walls. None of it needed re-deriving, and re-deriving it invited a second,
conflicting inventory of the same flat.

**The one thing the model actually lacked was POSITION.** `wall_runs.csv` carries
coordinates in **basic-plan pixels** — which is precisely why
`project_decisions.md` says the wall ids are *"regions on a raster, not named
shell walls"*. → **So v0 is a REGISTRATION problem, not an extraction problem.**

## ✅ The named walls now have millimetre positions

`tools/layout/place_named_walls.py` fits basic-plan pixels to the vector plan's
millimetres and places the existing walls. **The recorded parameters pass through
untouched; nothing about a wall is re-measured.**

| | result |
| :--- | :--- |
| walls placed | **25 of 25** |
| x fit | `mm = 9.8598 × basic_px + 2609.3`, 15/15 walls on a face line |
| y fit | `mm = −10.1934 × basic_px + 16816.2`, 10/10 walls on a face line |
| snap residual | under 20 mm for 21 walls; **worst G7 +93, MA +49** |

**Drawing: `_Drawings/review/v0_named_walls.png`**, coloured by class and
labelled by id — grey concrete frame, green aerated block, blue external, orange
лоджия enclosure.

**Two independent checks that the fit is right**, neither of them used to make
it: **G4d's drawn span comes out 2822 against its recorded 2825**, and **G2's
2218 against 2219**. A wrong scale could not do that.

> [!CAUTION]
> **⚠️ A DEGENERATE FIT GOT THROUGH FIRST, AND IT SCORED PERFECTLY.** At a 60 mm
> matching tolerance the x axis fitted at **5.56 mm/px — almost exactly half the
> true 9.86 — with 15 of 15 walls "on a face line".** With 117 face lines over
> ~30 m the mean spacing is ~250 mm, so at 60 mm a wall lands on *some* line by
> chance about half the time, and **inlier count cannot tell a scale from a
> submultiple of it.** It is the same aliasing that earlier put this drawing at
> 1:150 instead of 1:75 — the second time in two days.
>
> **Fixed by making the two axes check each other:** they describe one drawing,
> so their scales must agree. Tolerance is now 25 mm, and the x fit is
> constrained to within 6% of the y fit's scale — generous next to the raster's
> own ~1.7% aspect error, and far too tight for a submultiple. **The tool exits
> loudly if they disagree.**

## The elements that are not walls

`tools/layout/extract_v0_elements.py` → `data/canonical/v0_elements_extracted.json`.

### ✅ The лоджия glazing — four bays, from OUR OWN drawing

**Owner, 2026-09-08: *"it could be still one block but in four segments"*. The
drawing agrees, and now gives the numbers.**

| | |
| :--- | :--- |
| run along the glazing | **2963.9 mm** |
| bearing | 164.05° — the splay that makes the лоджия non-rectangular |
| assembly depth | **150 mm** |
| **bays** | **660.0 · 680.2 · 679.2 · 659.2** |
| **mullions** | **50 · 50 · 50** |

> [!IMPORTANT]
> **This upgrades `O9` in `wall_openings.csv` from pattern to measurement.** That
> entry got its four-bay reading from **9711.jpg, a photo of flat 109**, and said
> so honestly: *"the PATTERN transfers and the bay count and widths do not"*.
> **Now the bay count and widths come from this type's own drawing.**
>
> **And the width triangulates three ways.** O9 *derived* 2939 from the splay
> geometry; **apartment 53's plan prints 2.93 m**; this drawing measures
> **2963.9**. Three independent routes inside 34 mm, ~1%. ⚠️ **The 2939 stays as
> the model's figure** — it is the one built from this flat's own chain — but it
> is now corroborated rather than merely self-consistent.

### ✅ The slab extension at the 19,49 window — the owner's own reading

**Owner, 2026-09-08:** an *"extension of a floor concrete slab for decorative
purposes"*, marked on his screenshot at the bigger room's window.

**It is a closed rectangle, 1800 mm wide × 370 mm deep**, x 10235.9–12035.9,
y 7910.6–8280.6. It projects **320 mm beyond MC's outer face** (8230.6) and laps
50 mm into the wall. **It is 50 mm wider than the window opening on each side.**

⚠️ **It is NOT a wall and must never be counted as one.** ⚠️ **And it appears at
this window only** — MB's window carries a much shallower 70 mm line in the same
position, not a 370 mm solid. Whether that asymmetry is real or a drafting
difference is unresolved.

### ⚠️ The dashed lines — SUGGESTED FURNITURE, not fabric

**Owner, 2026-09-08:** dashed lines by the main entrance and the middle room are
**suggested wardrobe positioning**, and *"drifted to the right"*.

Five dashed runs are found. **Their identity is deliberately NOT assigned** —
after reading `ПР` as *правая* when it meant *проём*, a role guessed off a
drawing is not worth having:

| axis | line | span | extent |
| :--- | :--- | :--- | :--- |
| EW | 7490.6 | 5692 | x 2788.7 – 8480.9 |
| EW | 14350.3 | 2863 | x 10130.9 – 12993.5 |
| NS | 10130.9 | 2840 | y 13150.3 – 15990.3 |
| EW | 7860.6 | 1699 | x 6782.0 – 8480.9 |
| NS | 9730.8 | 1374 | y 14650.3 – 16024.4 |

**❓ For the owner: which of these are the two wardrobes, and is "drifted to the
right" a defect in the developer's suggestion or the reason to ignore it?**

> [!WARNING]
> **⚠️ THE DRAWING CONTAINS NO PDF DASH OPERATOR AT ALL.** Every dashed line is
> **exploded into short segments**, so dashed and solid are graphically
> identical and a dashed line can only be found by its **gap rhythm** (here a
> regular ~90 mm). **Anything that treats collinear short segments as one line
> will silently promote suggested furniture into built fabric.** Dash-state
> tracking was added to `parse_vector_plan.py` anyway — it is correct PDF
> handling and reports zero on this file, which is itself the finding.

## ⚠️ What is still missing

- **Wall EXTENTS come from the pixel runs, not from the model.** A wall's
  position is now exact across its thickness but its ends are still raster-
  derived, and `clear_mm` / `solid_mm` remain the length of record. **G6 is the
  loud case: recorded 1915, drawn span 3076.** Not reconciled.
- **Runs are not clipped to the flat**, so the façade reaches into the
  neighbour's flat where the drawing continues it.
- **Window frame subdivision** inside MA / MB / MC is not extracted. The
  geometry is there — the 19,49 window shows jamb frames and a central mullion
  pair as short verticals across the reveal — but the tool does not read it, and
  the owner wants it for the 3D.
- **No corner is resolved**, and `check_wall_junctions.py` has not been run.
- **`R3` and `G3` have no recorded length** — an INDETERMINATE SPLIT in
  `wall_blocks.csv`. The vector may now be able to settle it; not attempted.

## What none of this changes

**⚠️ Precision is not accuracy.** These are the developer's **project**
dimensions. The as-built runs **+1.0% to +1.9% SMALLER**, 12 of 12. Size nothing
tight from this.

**Coordinates are sheet-relative**, shared between the two datasets but not a
flat-local datum.

⚠️ **Validate by CHAIN CLOSURE, never against a printed area.**
