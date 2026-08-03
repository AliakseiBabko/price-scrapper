# Provisional apartment model policy

The apartment is not built yet, so the current model is a planning baseline,
not an as-built survey.

## Source hierarchy

1. `fllor_plan_detailed.jpeg` is the primary source for the current apartment's
   topology, room adjacency, openings, and planned dimensions.
2. `floor_plan_basic.jpg` is a consistency check for the same current layout.
3. `floor plan_1.jpg`, `floor plan_2.jpg`, and `floor plan_3.jpg` are reference
   apartments used only to establish plausible uncertainty ranges.
4. Future millimetre field measurements supersede all planned values.

## Modeling rules

- Do not average the reference apartments into the current apartment geometry.
- Do not apply one global scale factor to force calculated area to match a
  declared area.
- Store documented area values separately from areas calculated from model
  geometry.
- Use the current detailed plan as the nominal baseline.
- Preserve alternative values as scenarios, not hidden corrections.
- Keep AI/cloud assets, furniture, and quantities marked provisional until the
  relevant dimensions are verified.

## Current provisional values

- entrance opening: 1010 mm;
- probable door leaf: 910 mm, separate from the opening;
- missing entrance-hall depth: 2310 mm nominal;
- entrance-hall scenarios: 2280 mm and 2330 mm;
- area scenarios: 69.09 m² (detailed plan) and 69.44 m² (basic plan);
- geometry status: `planned`, not `measured`.

The model should be regenerated after field measurement rather than manually
scaled to fit the old plan. This keeps IFC geometry, sheets, quantities, and
pricing traceable to the same source revision.
