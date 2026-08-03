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
- Keep collinear walls that represent one finish/calculation surface as one host wall.
- Model every door/window as a native `IfcOpeningElement` with valid void/fill relationships.
- Place Blender window panes at the host-wall midplane and hide duplicate imported fill meshes in both render and viewport.
- Keep occupiable rooms enclosed, door-connected, and reachable from the entrance hall. Require windows for living room, bedroom, and kitchen in this demonstrator.
- Snap electrical switches, outlets, and their visible coordination routes to wall faces; avoid doors, door clearances, and windows.
- Keep plumbing connections attached to a wall/service zone; hide concealed routes only in finished renders.
- Align slab footprint with the finished exterior wall envelope, including underside corners.

## Verification workflow

1. Run `tools/ifc/verify_qto_gate.py` against the generated IFC.
2. Run `tools/ifc/validate_apartment_layout.py` and require `status: valid`.
3. Rebuild the Blender scene with `tools/blender/build_apartment_demo.py`.
4. Inspect top, interior, exterior, and underside views before reporting completion.
5. Keep QTO status review-only unless geometry and professional review requirements are separately satisfied.
