# IFC geometry PoC

This PoC is independent of Blender, Bonsai, MCP, DWG conversion, and cloud
assets. It creates a small IFC4 model from canonical JSON, reopens it, checks
the basic geometry/entity relationships, and writes a transparent QTO JSON
summary.

The canonical input is validated against
`schemas/renovation-model.schema.json` before model generation.

## Environment

The IFC core was tested in an isolated Python 3.14 environment with
IfcOpenShell 0.8.5. Blender/Bonsai will use its own separately verified Python
runtime; this environment is not a Bonsai environment. The repository's main
`.venv` remains unchanged.

```powershell
.\.venv-ifc314\Scripts\python.exe -m pip install -r tools\ifc\requirements.txt

.\.venv-ifc314\Scripts\python.exe tools\ifc\validate_canonical.py `
  --schema schemas\renovation-model.schema.json `
  --input data\canonical\apartment_poc.json
```

## Run

```powershell
.\.venv-ifc314\Scripts\python.exe tools\ifc\poc_renovation.py `
  --input data\canonical\apartment_poc.json `
  --output-dir data\outputs\ifc-poc
```

Expected outputs:

- `renovation_poc.ifc`
- `renovation_poc.qto.json`
- `renovation_poc.validation.json`

This is not yet a drawing exporter. SVG/PDF generation is a separate milestone
after the IFC fixture passes external validation. A separate deterministic SVG
floor-plan prototype is available at `tools/drawings/floor_plan_svg.py`; it is
canonical-JSON driven and is not yet an IFC HLR/Bonsai drawing exporter.

```powershell
\.venv-ifc314\Scripts\python.exe tools\drawings\floor_plan_svg.py `
  --input data\canonical\apartment_poc.json `
  --output data\outputs\ifc-poc\floor_plan.svg
```

## IFC-derived floor-plan export

The local PoC also uses the official IfcOpenShell 0.8.5 `IfcConvert` Windows
package. The binary is intentionally not committed; download it from the
[IfcOpenShell 0.8.5 release](https://github.com/IfcOpenShell/IfcOpenShell/releases/download/ifcconvert-0.8.5/ifcconvert-0.8.5-win64.zip)
and place `IfcConvert.exe` under `tools/ifc/bin/`.

```powershell
.\.venv-ifc314\Scripts\python.exe tools\drawings\ifcconvert_floor_plan.py `
  --ifc data\outputs\ifc-poc\renovation_poc.ifc `
  --output data\outputs\ifc-poc\ifcconvert_section.svg
```

The wrapper performs a 1.2 m section cut at 1:100 and checks that the output
is non-empty, valid XML with IFC-named elements. It is a coordination export,
not a contractor-ready sheet.

Package the export as an A3 landscape sheet with title block and manifest:

```powershell
.\.venv-ifc314\Scripts\python.exe tools\drawings\package_sheet.py `
  --input data\outputs\ifc-poc\ifcconvert_section.svg `
  --output-svg data\outputs\ifc-poc\A-101_floor_plan.svg `
  --output-pdf data\outputs\ifc-poc\A-101_floor_plan.pdf
```

PDF creation uses CairoSVG when native Cairo is available, otherwise the
Windows-friendly ReportLab/SVG fallback. The SVG and manifest are still
produced even if neither renderer is available.
