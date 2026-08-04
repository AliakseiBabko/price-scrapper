# OpenBIM implementation plan

> Mandatory geometry reference: [`RESIDENTIAL_BIM_GEOMETRY_CONTRACT.md`](RESIDENTIAL_BIM_GEOMETRY_CONTRACT.md). Future apartment IFC/Blender changes must follow its wall-junction, opening, reachability, MEP-placement, and slab-envelope rules.

## Completed

### Milestone 0 — canonical contract and geometry QTO

- Added `schemas/renovation-model.schema.json`.
- Added `tools/ifc/validate_canonical.py`.
- IFC generation now rejects input that fails the schema.
- Added tessellated geometry volume calculations through IfcOpenShell.
- Compared geometry-derived net wall volume with the expected opening
  intersection volume.
- Current fixture QTO consistency deltas are below `0.001 m3`.

### Milestone 1 — deterministic IFC fixture

Input:

```text
data/canonical/apartment_poc.json
```

Outputs:

- real IFC4 wall and slab geometry;
- one opening and one door;
- `IfcRelVoidsElement` and `IfcRelFillsElement` relationships;
- reopened-model relationship checks;
- QTO sanity report;
- IfcOpenShell EXPRESS-rule validation with no issues.

Tested runtime:

- Windows 11;
- Python 3.14 isolated environment;
- IfcOpenShell 0.8.5;
- pytest 8.4.1.

### Milestone 2 — canonical vector sheet prototype

`tools/drawings/floor_plan_svg.py` generates a deterministic SVG from the same
canonical JSON. It proves page geometry, wall cuts, door symbol, dimensions,
and status labeling. It is not yet an IFC HLR renderer and is not contractor
ready.

### Milestone 3 — IFC-derived section SVG

- Installed the official IfcOpenShell 0.8.5 Windows `IfcConvert` binary in an
  ignored local tools directory.
- Added an `IfcSpace` room proxy because the exporter defaults to spaces for
  SVG inclusion; the IFC remains EXPRESS-rule valid.
- Added `tools/drawings/ifcconvert_floor_plan.py` and its filter file.
- Verified a 1:100 section export at 1.2 m containing four IFC walls and one
  IFC door, preserving element names and GlobalIds.
- Classification remains coordination-ready only; title block, revision data,
  line-weight conventions, and professional review are still required before
  contractor use.

### Milestone 4 — print sheet packaging

- Added A3 landscape SVG packaging with title block, scale, sheet number,
  revision, date, and explicit `NOT FOR CONSTRUCTION` status.
- Added a JSON manifest recording source, revision, scale, classification, and
  generation date.
- PDF output is supported through CairoSVG or the Windows-friendly
  ReportLab/SVG fallback; the produced PDF was verified as a PDF artifact.

### Milestone 5 — evidence-calibrated provisional apartment model

- Added `tools/cad/extract_dxf_plan.py` to inspect the converted DXF without
  flattening block inserts or modifying the source.
- Recorded the 1010 mm entrance opening as a user control and retained 2.28 m,
  2.31 m, and 2.33 m hall-depth scenarios from comparable reference plans.
- Added `tools/ifc/provisional_ifc.py`, generating three adjustable IFC4
  coordination variants from labelled areas and explicit aspect-ratio proxies.
- All three IFC variants pass IfcOpenShell validation. The nominal 2.31 m
  variant loads into Bonsai and saves as a Blender 5.2 `.blend` successfully.
- The model remains `planned_not_as_built` and `provisional_not_for_procurement`.

### Milestone 6 — Blender/Bonsai visual technology demonstrator

- Added `tools/blender/build_demo_scene.py`.
- Verified Bonsai IFC import into Blender 5.2, camera creation, measurement
  annotations, artificial-light scenario setup, `.blend` save, and PNG render.
- Produced daylight, mixed, and evening scene variants. This demonstrates the
  software loop; the current proxy layout is intentionally not a project claim.

### Milestone 7 — room-by-room design interaction demonstrator

- Added `tools/blender/build_apartment_demo.py`.
- Added furniture, built-in wardrobe, kitchen cabinetry, bathroom fixtures,
  conceptual electrical symbols, named ceiling fixtures, and room labels.
- Generated separate daylight, mixed, and evening renders from the same scene.
- Saved all design objects in dedicated Blender collections so future UI or
  agent controls can toggle furniture, electrical, and lighting independently.

### Milestone 8 — corrected enclosed apartment demonstrator

- The earlier strip-based proxy was intentionally treated as a failed visual
  architecture test: it proved import/render integration but did not represent
  rooms.
- Added `tools/ifc/demo_apartment_layout.py` with six enclosed spaces, a floor
  slab, continuous perimeter/partition wall layout, four door objects, and
  three window objects.
- Rebuilt the Blender demonstration from this layout. The resulting IFC passes
  validation and the rendered plan visibly contains enclosed rooms.
- Electrical symbols remain conceptual, but are now placed inside rooms rather
  than scattered as unexplained floor objects; the next refinement will mount
  them to walls and add door/window swing symbols for plan output.

### Milestone 9 — IFC placement correction

- Corrected the profile-origin convention in the generic layout generator.
- Wall, slab, space, door, and window bounding boxes are now centered and
  aligned consistently; the previous scattered geometry was caused by mixing
  lower-left coordinates with centered IFC profiles.
- Electrical demonstrator objects now use wall-bound XY coordinates and
  wall-mounted height metadata.

### Milestone 10 — bounded door and window openings

- Replaced floor-to-ceiling wall gaps with bounded opening geometry.
- Windows now have wall piers, a sill below, and a header above; doors have
  wall piers and a continuous header above the door head.
- Bathroom and WC boundaries remain fully enclosed while their door openings
  are explicitly placed in the hall-side partition.
- Window and door inserts are styled as thin design elements inside the wall
  openings. A later IFC-semantic pass can add native void/fill relationships
  without changing the verified geometric arrangement.

## Next milestones

1. Add a JSON Schema validator and provenance/source fields.
2. Add geometry-derived QTO using IfcOpenShell shape utilities and compare it
   with the fixture sanity calculations.
3. ~~Install and test a verified `IfcConvert` binary for IFC-to-SVG projection.~~
4. Compare `IfcConvert` SVG output with the canonical SVG prototype.
5. Add PDF packaging, title block, revision, sheet scale, and print checks.
6. Build a DWG-to-DXF intake tool only after a converter is available; preserve
   the original DWG and require unit/control-dimension approval.
7. Add product IDs and a read-only export into the existing price database.
8. Replace the provisional area/aspect-ratio proxies with one field-measured
   apartment room before adding all rooms.
9. Add parametric cabinetry and verified furniture proxies.
10. Add conceptual MEP routing and clash checks.
11. Add visual lighting scenarios; integrate a specialist lux tool separately.
12. Test Blender/Bonsai in a separate pinned environment.
13. Add cloud asset ingestion with provenance, scale, license, and confidence.
14. Add MCP only as a safe wrapper around validated domain operations.

## Current execution status

- CAD intake and ODA DWG-to-DXF conversion are implemented. The current DXF
  reports millimetre units and 1,703 dimensions, but a known control dimension
  still requires manual approval before canonical geometry is scaled.
- Pricing linkage is implemented as a read-only SQLite export; the current
  design has no product IDs, so its export is intentionally empty.
- The two-room design IFC, built-in wardrobe proxy, conceptual electrical
  terminal, and lighting fixtures are generated and EXPRESS-validated.
- Lighting calculations are approximate lumen/area estimates only; no lux
  compliance or engineering result is claimed.
- Blender 5.2.0 LTS and Bonsai 0.8.6-alpha260801 are installed in an ignored
  portable profile. Headless enable, IFC load, and `.blend` save/reopen smoke
  tests pass.
- External/AI asset registration is implemented, with license/hash/declared
  dimensions and QTO exclusion until manual scale verification.
- The local agent adapter is implemented as an allowlisted JSON-lines boundary;
  arbitrary shell/Python/network operations are rejected.
- A structured DXF plan extraction report is now generated from the converted
  source. It preserves layer/block evidence and records the 1010 mm entrance
  opening plus hall-depth sensitivity scenarios without treating comparable
  reference plans as the current apartment geometry.

## Gates

- No drawing is called contractor-ready without professional review.
- No visual or AI-generated asset participates in QTO until dimension-verified.
- No regulatory rule is enforced without an authoritative source record.
- No Blender/Bonsai version becomes production-pinned without a compatibility
  test and IFC save/reopen test.
- No provisional apartment geometry becomes procurement or construction input
  until the 1010 mm opening, hall depth, and room dimensions are field-verified.

### Milestone 13 — tested wall-finish QTO and wall elevations

- Added `tools/ifc/calculate_wall_finishes.py`.
- Uses host-wall local profile dimensions, linked opening dimensions and
  positions, deduplicated voids, native space boundaries when available, and a
  clearly labelled rectangular-space fallback for the demonstrator.
- Generates per-wall JSON QTO plus SVG wall elevations using actual opening
  stations, sill heights, and door-head heights.
- Regression execution succeeds on the generic demonstrator (12 walls), BOT
  Duplex (57 represented walls), and KIT FZK Haus (13 represented walls).
- Results remain quantity estimates requiring review; no finish is silently
  assigned when room-side evidence is unavailable.

### Milestone 14 — first-level space-boundary mapping

- Verified Gemini's `root.create_entity` plus `boundary.edit_attributes`
  pattern on IfcOpenShell 0.8.5.
- Added explicit first-level `IfcRelSpaceBoundary` relationships to the
  demonstrator: 24 boundaries survive IFC reopen and are visible through
  `wall.ProvidesBoundaries`.
- Added `data/canonical/finish_schedule_demo.json` and verified scheduled
  finish metadata flows into wall QTO output.
- Bonsai/Blender 5.2 import and save still pass.
- `ConnectionGeometry` is intentionally not authored yet, so this upgrades
  semantic adjacency but not exact face-side geometry; QTO remains review-only.

### Milestone 12 — Gemini sample URL audit

- Verified and downloaded the BOT Duplex IFC2X3 model and the minimal
  buildingSMART slab fixture from Gemini's direct URLs.
- Confirmed BOT Duplex import/save through Bonsai and Blender 5.2.
- Recorded three stale/404 URLs instead of silently accepting them as samples.
- Added `tools/ifc/GEMINI_SAMPLE_URL_AUDIT.md` with the results and benchmark
  use of each surviving sample.

### Milestone 11 — reference sample benchmark and native wall semantics

- Downloaded and inspected the KIT FZK Haus IFC4 reference and the official
  buildingSMART sample/test archive.
- Added `tools/ifc/analyze_reference_ifc.py` and
  `tools/ifc/REFERENCE_SAMPLE_ANALYSIS.md`.
- Upgraded the generic demonstrator to one host wall per construction wall,
  native `IfcOpeningElement` voids, and native door/window fill relationships.
- Verified the resulting model contains 12 walls, 7 openings, 7 void
  relationships, 4 doors, 3 windows, and 7 fill relationships.
> Geometry contract: [`RESIDENTIAL_BIM_GEOMETRY_CONTRACT.md`](RESIDENTIAL_BIM_GEOMETRY_CONTRACT.md) is mandatory for future apartment IFC/Blender changes. It records the validated wall-junction, opening, reachability, MEP-placement, and slab-envelope rules.

### Milestone 15 - IFC-driven A3 floor-plan sheet

- Added `tools/drawings/apartment_sheet_from_ifc.py`.
- Generates an A3 landscape SVG/PDF sheet directly from the validated apartment
  IFC, not from hand-drawn room JSON.
- Draws wall cuts, native door/window opening cuts, door swing arcs, window
  lines, room names, room span labels, overall envelope dimensions,
  wall-snapped electrical coordination symbols, legend, and title block.
- Writes `data/outputs/demo/revised/sheets/apartment_floor_plan_a3.svg`,
  `apartment_floor_plan_a3.pdf`, and `apartment_floor_plan_a3_manifest.json`.
- Validates that electrical symbols snap to host walls and avoid
  door/window openings.
- Classification remains `coordination-ready; professional review required;
  not for construction`.

### Milestone 16 - native IFC electrical coordination terminals

- Added 12 conceptual `IfcFlowTerminal` outlet/switch placeholders to
  `tools/ifc/demo_apartment_layout.py`.
- Each terminal is wall-snapped, checked against door/window openings, assigned
  to the storey, and tagged with `Pset_DemoElectricalCoordination` metadata for
  room, host wall, mounting type, device type, and engineering status.
- Updated `tools/drawings/apartment_sheet_from_ifc.py` to render the electrical
  layer from native IFC flow terminals when present, with generated sheet
  symbols retained only as a fallback for older IFC files.
- Updated `tools/blender/build_apartment_demo.py` so imported IFC flow
  terminals receive the electrical material and procedural Blender-only
  electrical symbols are skipped when native IFC terminals exist.
- Regenerated the demonstrator IFC, validated IFC, A3 SVG, A3 PDF, and sheet
  manifest; the manifest now reports `electrical_symbol_source:
  native_ifc_flow_terminals`.

### Milestone 17 - native IFC plumbing coordination terminals

- Added 3 conceptual plumbing `IfcFlowTerminal` placeholders to
  `tools/ifc/demo_apartment_layout.py`: kitchen sink, bathroom vanity, and WC
  cistern/service connection.
- Each plumbing terminal is wall-snapped, checked against door/window openings,
  assigned to the storey, and tagged with `Pset_DemoPlumbingCoordination`
  metadata for room, host wall, device type, system, mounting type, and
  engineering status.
- Updated `tools/drawings/apartment_sheet_from_ifc.py` to render plumbing
  terminals as a separate blue service-symbol layer alongside electrical
  terminals.
- Updated `tools/blender/build_apartment_demo.py` so imported plumbing flow
  terminals receive the plumbing material and procedural Blender-only plumbing
  placeholders are skipped when native IFC plumbing terminals exist.
- Regenerated the demonstrator IFC, validated IFC, A3 SVG, A3 PDF, and sheet
  manifest; the manifest now reports 12 electrical symbols, 3 plumbing symbols,
  and 15 native IFC flow terminals.

### Milestone 18 - native IFC lighting coordination fixtures

- Added 6 conceptual `IfcLightFixture` ceiling-light placeholders to
  `tools/ifc/demo_apartment_layout.py`, one per room.
- Each fixture is centered in its room footprint, assigned to the storey, and
  tagged with `Pset_DemoLightingCoordination` metadata for room, mounting type,
  device type, temperature, approximate lumens, and validation boundary.
- Updated `tools/drawings/apartment_sheet_from_ifc.py` to render native IFC
  light fixtures as a separate lighting symbol layer and validate that they sit
  inside room footprints.
- Updated `tools/blender/build_apartment_demo.py` so imported IFC light-fixture
  geometry receives a dedicated fixture material while Blender area lights
  continue to provide the daylight/mixed/evening render scenarios.
- Regenerated the demonstrator IFC, validated IFC, A3 SVG, A3 PDF, and sheet
  manifest; the manifest now reports 6 native lighting symbols. These are
  visual coordination fixtures only, not lux simulation or electrical design.

### Milestone 19 - discipline-specific A3 sheet set

- Extended `tools/drawings/apartment_sheet_from_ifc.py` with `--sheet-kind`
  and `--sheet-set`.
- The generator can now emit separate A3 SVG/PDF sheets for:
  - `A-101` architectural floor plan;
  - `E-101` electrical and lighting coordination plan;
  - `P-101` plumbing coordination plan;
  - combined coordination plan.
- Each discipline sheet is generated from the same validated IFC and filters
  the native service layers according to the sheet type.
- Generated sheet manifests preserve model-wide symbol counts while also
  reporting the symbols visible on each sheet.
- Classification remains coordination-only and not for construction.

### Milestone 20 - current-apartment planned seed from Visual Drop evidence

- Added `tools/ifc/current_apartment_layout.py` to generate the first
  current-apartment IFC seed from the Visual Drop floor-plan evidence:
  `fllor_plan_detailed.jpeg`, `floor_plan_basic.jpg`, and the comparable
  measured reference plans `floor plan_1.jpg`, `floor plan_2.jpg`, and
  `floor plan_3.jpg`.
- The seed records the current evidence status as
  `planned_from_visual_sources_not_field_verified`; final millimetre dimensions
  still require site measurement.
- The generator now emits 8 spaces, 18 walls, 7 native door/doorway fills,
  4 native window fills, 13 electrical terminals, 3 plumbing terminals, and
  7 ceiling light fixtures.
- Added `tools/ifc/validate_current_apartment_seed.py` as a dedicated rule gate
  for this seed. It checks expected rooms, door-connected reachability from the
  entrance hall, required windows for living rooms/bedrooms/kitchen, native
  opening/fill relationships, wall-mounted services, service/opening clearance,
  lighting placement sanity, and the planned-not-field-verified manifest status.
- Regenerated the current-apartment IFC, validation JSON, discipline A3 sheet
  set, Blender scene, and daylight/mixed/evening renders from the same IFC
  source.

### Milestone 21 - CAD/DWG evidence intake and control candidates

- Processed `00_Inbox/cad/20260727-ZK Dubravinskiy.dwg` non-destructively with
  `tools/cad/intake_cad.py`; the original DWG remains in the inbox.
- Converted the DWG to DXF with ODA File Converter for analysis only and
  confirmed the converted DXF reports millimetre `$INSUNITS`.
- Generated a DXF evidence summary showing 7,886 model-space entities,
  1,703 dimension entities, 116 wall inserts, 32 door inserts, 10 window
  inserts, and 11 switch inserts.
- Added `tools/cad/dxf_control_candidates.py` to locate candidate dimension
  entities near known controls such as the 1010 mm entrance opening, 910 mm
  probable door leaf, and 2.31 m entrance-hall depth.
- Recorded results in `tools/cad/CAD_INTAKE_SUMMARY.md`.
- The CAD export remains a reference underlay and candidate-dimension source,
  not an authoritative BIM geometry source, because Homestyler geometry is
  block-insert heavy and repeated apartment instances require manual visual
  confirmation.

### Milestone 22 - current-apartment reproducible build command

- Added `tools/ifc/build_current_apartment_outputs.py`.
- The wrapper regenerates, in order:
  - current-apartment IFC seed;
  - current-apartment manifest;
  - current-apartment validation JSON;
  - architectural, electrical/lighting, plumbing, and combined A3 sheet set;
  - optionally, the Blender `.blend` and daylight/mixed/evening renders.
- Verified both the fast path with `--skip-blender` and the full path including
  Blender scene generation and daylight/mixed/evening renders.

### Milestone 23 - non-destructive Homestyler noise cleanup

- Added `tools/cad/clean_homestyler_apartment.py` to derive a cropped DXF from
  the noisy Homestyler export without modifying the original DWG or source DXF.
- The selector chose the repeated plan instance anchored near
  `[52274.836, 31819.746]` mm because it combines the 1014.672 mm entrance
  dimension, 910 mm door leaf, 2308.734 mm hall-depth observation, and
  3275.160 mm span.
- Generated `data/cad/20260727-ZK-Dubravinskiy.current-apartment.cleaned.dxf`
  and its JSON report. The first rectangular-crop attempt was rejected after
  visual comparison because it removed too much context. The active version
  uses the actual `P-Wall-Section` footprint, retains 1,098 model-space
  entities, removes 6,788 outside-footprint entities, and reopens successfully
  in ezdxf with millimetre units.
- DWG TrueView 2027 is installed and is the designated visual-review tool for
  the derived DXF. The result remains a reference underlay and requires visual
  review before BIM promotion.
