# Visual plan alignment

Sources inspected from `00_Inbox/_Visual_Drop/`:

| Source | Role | Observations |
|---|---|---|
| `fllor_plan_detailed.jpeg` | Current apartment, dimensioned design | Main geometry source; entrance opening is 1010 mm; current room and wall dimensions are planned, not field-verified. |
| `floor_plan_basic.jpg` | Current apartment, simplified design | Same current layout and room areas; useful as a topology cross-check, not a dimensional source. |
| `floor plan_1.jpg` | Comparable previous building | Entrance/corridor depth approximately 2.33 m; corridor 10.2 m²; room values 25.2, 16.8, and 9.3 m². |
| `floor plan_2.jpg` | Comparable previous building | Entrance/corridor depth approximately 2.28 m; corridor 10.1 m²; room values 25.0, 16.7, and 9.3 m². |
| `floor plan_3.jpg` | Comparable previous building | Entrance/corridor depth approximately 2.31 m; corridor 10.0 m²; room values 25.1, 16.7, and 9.2 m². |
| `building_floor_plan.jpg` | Building-level context | Confirms the current apartment's location and repeated building typology; not suitable for measuring the apartment. |

## Recommended geometry policy

Use the current detailed plan as the primary topology and geometry source. Do
not average room dimensions from the three previous-building plans: they are
similar typologies, not the same apartment, and averaging them would move walls
without evidence.

For the missing entrance-hall depth, use three explicit design scenarios:

| Scenario | Depth |
|---|---:|
| Lower | 2.28 m |
| Nominal median | 2.31 m |
| Upper | 2.33 m |

The arithmetic mean is 2.3067 m, which rounds to 2.31 m. Therefore 2.31 m is a
reasonable nominal placeholder, with a documented uncertainty band of ±0.03 m.
The median is preferable to the mean because the sample is only three values
and the drawings are comparable but not identical.

The 1010 mm entrance opening should remain the current-plan control geometry.
The likely 910 mm door leaf is a separate object dimension and must not replace
the 1010 mm opening unless the frame/reveal convention is explicitly confirmed.

## Area policy

Use the official/current detailed plan for the current apartment's room areas
and wall layout. Use the previous plans only to establish uncertainty ranges or
to test whether a proposed layout is plausible. Do not average declared areas
with prior-building areas for the canonical geometry.

The current basic and detailed images show approximately 69.44 m² and 69.09 m²
respectively, a difference of about 0.35 m² (roughly 0.5%). Treat that as a
documentation/measurement discrepancy until field dimensions are available,
not as evidence that every current wall should be enlarged by a common factor.

## Canonical-model recommendation

Create a nominal model from the current detailed plan with:

- units: millimetres in the CAD source, metres in canonical JSON;
- entrance opening: 1010 mm;
- entrance-hall depth: 2310 mm nominal;
- uncertainty scenarios: 2280 mm and 2330 mm;
- geometry status: `planned_with_comparable-building-calibration`;
- unit status: `header-confirmed_manual-control-dimension-pending`.

Keep all three hall-depth scenarios until one independent site measurement is
available. Quantities and furniture clearances should be reported against the
nominal model and rechecked against the lower/upper scenarios.
