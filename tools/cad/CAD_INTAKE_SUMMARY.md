# CAD intake summary - 20260727-ZK Dubravinskiy

Source:

- `00_Inbox/cad/20260727-ZK Dubravinskiy.dwg`

Generated evidence artifacts, intentionally ignored under `data/`:

- `data/cad/20260727-ZK-Dubravinskiy.auto.intake.json`
- `data/cad/dxf/20260727-ZK Dubravinskiy.dxf`
- `data/cad/20260727-ZK-Dubravinskiy.dxf.summary.json`
- `data/cad/20260727-ZK-Dubravinskiy.control-candidates.json`

## Intake result

- Source DWG hash: `2e87f2703262be9e3d9062b4c5e986e9823a49ddd59d580bd8a96010e6906892`
- DWG header: `AC1021` / AutoCAD 2007.
- Converted DXF hash: `1e44e42f85889d5ce402263be6572162cb6f42ba4e31628474fb5584699fe602`
- Converted DXF version: `AC1032`.
- DXF `$INSUNITS`: `4` / millimetres.
- Model-space entities: 7,886.
- Dimension entities: 1,703.

## Relevant layer counts

- `E-Wall`: 116 `INSERT`
- `E-Door`: 32 `INSERT`
- `E-Opening`: 8 `INSERT`
- `E-Window`: 10 `INSERT`
- `E-Switch`: 11 `INSERT`
- `E-Cabinet`: 257 `INSERT`, 208 `LINE`
- `E-Movable Furniture`: 41 `INSERT`
- `P-Room`: 80 `INSERT`
- `P-Dimension Mark`: 1,703 `DIMENSION`

## Control-dimension candidates

The candidate extractor was run with ±12 mm tolerance.

- 1010 mm entrance-opening target: 20 candidates; closest measured values are
  approximately 1014.671-1014.672 mm.
- 910 mm probable door-leaf target: 31 exact 910.000 mm candidates.
- 2310 mm entrance-hall-depth target: 4 candidates; closest measured value is
  2308.734 mm, with additional 2300.000 mm candidates.
- 2280 mm and 2330 mm comparable-plan scenario targets: no candidates inside
  ±12 mm in the exported DXF dimensions.
- 3275 mm span target: 27 candidates; closest measured values are
  approximately 3275.156 mm.

## Engineering interpretation

The CAD export is good enough for reference-underlay and candidate dimension
search. It should not yet replace the planned current-apartment seed because:

- Homestyler architectural geometry is represented mainly as block inserts, not
  clean wall polylines.
- Several repeated apartment instances appear in the same model space, so a
  candidate dimension still needs visual confirmation against the intended unit.
- Unit evidence comes from DXF headers and dimension values, not field
  measurement.

The current IFC seed should therefore keep the status
`planned_from_visual_sources_not_field_verified` until field measurements or a
manually confirmed CAD control set is available.
