# Residential BIM Geometry Contract

This contract applies to the apartment IFC and Blender demonstrator. It is a
project invariant, not a construction-code claim.

## Wall topology and junctions

- Represent the exterior perimeter as four continuous host walls whenever the
  wall has no semantic reason to be segmented.
- Use the generator's lower-left bounding-box convention consistently:
  horizontal walls span `x..x+length`, `y..y+thickness`; vertical walls span
  `x..x+thickness`, `y..y+length`.
- Make exterior corners by matching the continuous wall envelopes. Do not add
  decorative corner filler objects, double-extend both intersecting walls, or
  leave outside gaps.
- Merge collinear interior walls when they represent one finish/calculation
  surface. A shorter perpendicular partition may terminate into the host wall;
  it must not protrude through it.
- Keep the wall junction rule in both IFC geometry and Blender presentation.

## Openings and windows

- Every door/window opening must be an `IfcOpeningElement` hosted by exactly
  the intended wall through `IfcRelVoidsElement`.
- Doors and windows fill openings through `IfcRelFillsElement`.
- Window panes/frames are presentation objects placed at the host-wall opening
  midplane. They must not be opaque source boxes attached to the room side.
- Hide the original imported window-fill mesh in both render and viewport when
  it duplicates the presentation pane.
- Do not repair an incorrect window by placing a second rectangle over the
  wall. Fix the host opening, fill placement, and pane plane.

## Room validity and reachability

- An occupiable room requires at least four boundary walls and a door/doorway.
- Living room, bedroom, and kitchen require an exterior window in this
  demonstrator. Technical shafts may be exempt.
- Every occupiable room must be reachable from the entrance hall through an
  explicit doorway graph. Do not infer connectivity merely because several
  rooms share one wall.
- Validate door-to-room pairs explicitly for the demonstrator before claiming
  reachability.

## Electrical and plumbing placement

- Electrical outlets and switches must be flush-mounted to a wall face and
  must not overlap door swings, door clearances, or window openings.
- Electrical routes should terminate at the same snapped wall point as the
  device. Show them in coordination view, but hide them in finished renders
  when they represent concealed chases or ceiling routes.
- Plumbing fixtures may be floor-mounted when appropriate, but connections,
  risers, and concealed runs must be attached to or enclosed by the relevant
  wall/service zone rather than floating in space.
- Never place a service route as a free-floating vertical line based only on a
  room coordinate; snap it to the host wall/device geometry.

## Slab and envelope alignment

- Align the apartment slab footprint with the finished exterior wall envelope.
- Inspect the model from above, inside, outside, and below. Underside slab
  corners must not stop short of or protrude unpredictably beyond the wall
  envelope.

## Required verification before visual handoff

Run:

```powershell
.\.venv-ifc314\Scripts\python.exe tools\ifc\verify_qto_gate.py `
  --source data\outputs\demo\revised\generic_enclosed_apartment.ifc `
  --output data\outputs\demo\revised\generic_enclosed_apartment_validated.ifc `
  --finish-schedule data\canonical\finish_schedule_demo.json

.\.venv-ifc314\Scripts\python.exe tools\ifc\validate_apartment_layout.py `
  --ifc data\outputs\demo\revised\generic_enclosed_apartment_validated.ifc
```

Then rebuild Blender and inspect the wall junctions, window openings, door
clearances, service mounts, and underside slab before reporting completion.
