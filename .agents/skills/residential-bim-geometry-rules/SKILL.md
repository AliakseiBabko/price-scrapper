---
name: residential-bim-geometry-rules
description: Enforce validated residential IFC and Blender geometry rules for wall junctions, openings, room reachability, electrical and plumbing placement, and slab alignment. Use when generating, modifying, validating, or visually inspecting this apartment demonstrator.
---

# Residential BIM Geometry Rules

## Overview

Apply the project contract in [RESIDENTIAL_BIM_GEOMETRY_CONTRACT.md](../../../../tools/ifc/RESIDENTIAL_BIM_GEOMETRY_CONTRACT.md) before changing apartment IFC or Blender geometry.

## Required invariants

- Keep exterior perimeter sides continuous where possible; do not split a single finish surface without a semantic reason.
- Use lower-left wall bounding-box coordinates consistently. Do not add corner fillers or double-extend intersecting walls.
- Make external corners flush and gap-free. Interior partitions terminate into their host walls without protruding.
- **A corner is a solid, and exactly ONE wall owns it.** An overlap counts the corner volume twice; a void counts it zero times; both are wrong. **The CONCRETE FRAME owns the corner** — it is cast first and the blocks infill against it — then the thicker wall, then the longer run. A partition of ≤120 mm meeting a frame member is a BUTT, never a corner: it lands on the column’s face and the column does not wrap around it.
- **Every wall carries TWO lengths.** `clear_mm` is what the plan prints and what a tape held inside the room reads. `solid_mm` is `clear_mm` plus the thickness of every corner that wall owns. Never add a neighbour’s thickness to a clear dimension and call the result internal.
- **A FACE is not a WALL, and room rollouts (развёртка) are a second model, not a view.** One wall gives a face to two rooms at two different lengths; a shaft or a plumbing block gives a face and is not a wall; and a STEP has no wall of its own. Conflating the two makes a room-face schedule unusable — it did here.
- **AREAS ARE NOT EVIDENCE.** Never validate a reconstruction against a printed area, not even the developer’s own. Use chain closure instead: do the parts sum to the whole? That is the only check here that is arithmetic rather than judgement.
- **Two different tolerances, and they must not be confused.** The BUILD tolerance is ±50 mm (measured, see `00_Master/Geometry_Variance_Study.md`); the RASTER tolerance for reading an edge off a plan JPEG is 25 mm. They happened to share a number once and no longer do.
- Keep collinear walls that represent one finish/calculation surface as one host wall — **but a THICKNESS CHANGE is a semantic reason to split, and the segments must stay separate.** A 250 mm concrete column continuing as a 75 mm partition on the same line is two elements, and the 175 mm the column projects past the partition is a real finish face. Group them for JUNCTION purposes only, so that a crossing wall meets the line once, at its dominant member (frame first, then thickest) — see `successor_groups()` in `tools/layout/check_wall_junctions.py`.
- Model every door/window as a native `IfcOpeningElement` with valid void/fill relationships.
- Place Blender window panes at the host-wall midplane and hide duplicate imported fill meshes in both render and viewport.
- Keep occupiable rooms enclosed, door-connected, and reachable from the entrance hall. Require windows for living room, bedroom, and kitchen in this demonstrator.
- Snap electrical switches, outlets, and their visible coordination routes to wall faces; avoid doors, door clearances, and windows.
- Keep plumbing connections attached to a wall/service zone; hide concealed routes only in finished renders.
- Align slab footprint with the finished exterior wall envelope, including underside corners.

## Verification workflow

**For the flat’s wall geometry, run these first — they are cheap and they catch what review does not:**

1. `tools/layout/check_wall_junctions.py` — no overlap, no gap, no unowned L-corner void.
2. `tools/layout/build_wall_corners.py` — every L-corner owned exactly once.
3. `tools/layout/check_room_rollout.py` — every room rollout closes on both axes.

**After any change to the v0 DXF export, these four as well:**

4. `tools/layout/check_dxf_closure.py` — THE closure gate. Entity shape, identity (present exactly once, labels and polylines in bijection), canonical table keys unique, faces against the placement, extents against hatched solids re-derived from the source PDF, every ledger corner square solid, no unsanctioned overlap or unexplained near-miss or cavity, and the review drawing byte-identical to a fresh render.
5. `tools/layout/raster_fidelity.py` — the raster half, registered from the **PDF** and not from the DXF under test, against a frozen mask.
6. `scripts/dxf_closure_selftest.py` and `scripts/raster_fidelity_selftest.py` — **run these after changing either gate.** 24 + 7 seeds, each of which exists because something passed.

> [!WARNING]
> **Before writing or changing any of these checks, read `00_Master/Validator_Design_Discipline.md`.** Eleven adversarial review rounds produced a short list of failures that kept recurring — a collection that deduplicates destroys the defect being checked (four times), printing is not checking (three times), an accidental rejection is not a check, a seed that cannot fail is worse than no seed. **A gate nobody has watched fail is not a gate.** That page also states what *done* means per kind of work, which is the distinction that let real findings pile up for rounds while the geometry did not move.

> [!IMPORTANT]
> **Before reading any dimension off a drawing or photo, use the checklist in `00_Master/Evidence_Reading_Discipline.md`.** It exists because the same reading error recurred seven times in one modelling session, and one of those was committed AFTER the rule against it had been written in the same session. Writing a rule does not install it.

**For IFC and Blender:**

1. Run `tools/ifc/verify_qto_gate.py` against the generated IFC.
2. Run `tools/ifc/validate_apartment_layout.py` and require `status: valid`.
3. Rebuild the Blender scene with `tools/blender/build_apartment_demo.py`.
4. Inspect top, interior, exterior, and underside views before reporting completion.
5. Keep QTO status review-only unless geometry and professional review requirements are separately satisfied.
