# Reference sample analysis

## Sources inspected

- `data/samples/AC20-FZK-Haus.ifc` — KIT FZK Haus IFC4 sample, downloaded from
  the STEP Tools public sample listing.
- `data/samples/Sample-Test-Files-main` — official buildingSMART sample/test
  repository archive.
- The attached Gemini report — useful taxonomy, but it does not provide
  stable direct download URLs, file hashes, or licensing evidence for most
  third-party DWG sources.

## What the KIT reference demonstrates

The FZK Haus model contains 26 walls, 17 `IfcOpeningElement` objects, 17
`IfcRelVoidsElement` relationships, 5 doors, 11 windows, and 16
`IfcRelFillsElement` relationships. It also contains 7 spaces, two storeys,
quantity/property data, and space-boundary relationships.

The important implementation pattern is:

1. One `IfcWallStandardCase` represents the host construction wall.
2. An `IfcOpeningElement` represents the geometric void.
3. `IfcRelVoidsElement` connects the opening to the host wall.
4. `IfcDoor` or `IfcWindow` fills the opening through `IfcRelFillsElement`.
5. Wall area and opening quantities are derived from the host/opening model,
   not from four independent visual fragments.

## Changes applied to the demonstrator

`tools/ifc/demo_apartment_layout.py` now creates one host `IfcWall` per wall
plane, seven native openings, and native door/window fill relationships. The
model therefore supports the requested future wall-by-wall rollout better than
the earlier segmented-wall prototype.

## Drawing conventions extracted for the next stage

- Keep model geometry and sheet graphics separate.
- Use one wall identity for paint/plaster area, with opening deductions linked
  to the same wall.
- Generate interior wall elevations/rollouts from wall orientation and opening
  placement.
- Show windows as bounded openings with sill/head heights; do not represent
  them as opaque wall plates.
- Show door heads and wall above them; door leaves and swing arcs belong to the
  drawing layer.
- Mount electrical devices to a host wall with a height and face/orientation,
  not just an XY point.
- Use dedicated sheet layers for walls, openings, doors/windows, furniture,
  electrical, dimensions, annotations, and title-block metadata.

## Limits of the downloaded references

IFC samples validate model semantics and geometry exchange; they do not define
Belarus/Minsk title blocks, approval requirements, lineweights, or contractor
sheet conventions. Third-party DWG libraries remain style references until a
specific file's license, provenance, units, and layer structure are verified.
