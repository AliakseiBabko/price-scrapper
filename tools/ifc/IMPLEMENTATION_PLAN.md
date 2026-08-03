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
