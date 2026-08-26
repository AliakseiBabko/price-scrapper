# How to look at what the tooling produces

## The one thing to remember

```powershell
.\.venv\Scripts\python.exe tools\drawings\build_gallery.py
start data\outputs\gallery\index.html
```

That walks `data/outputs/` and `data/cad/`, renders a thumbnail for every PDF,
and writes one page listing all of it — currently 110 files in 26 groups. Every
tile links to the real file on disk, so the page never shows something the
filesystem does not have. Re-run it after generating anything new.

## What each format is, and what opens it

| Format | What it is | How to view |
|---|---|---|
| `.pdf` | The A3 sheets — the deliverable | Double-click. Any PDF reader. |
| `.svg` | The same sheets before PDF conversion | **Open in a browser** — vector, so zoom is lossless and text stays sharp. Best way to inspect a plan closely. |
| `.png` | Blender renders | Double-click. |
| `.ifc` | The BIM model itself — walls, rooms, openings, fixtures | Needs a viewer, see below. |
| `.blend` | Blender scene | Blender. |
| `.dxf` | The Homestyler CAD export | DWG TrueView, LibreCAD, or re-import to Homestyler. |

## The two things worth looking at right now

- **`data/outputs/variants/comparison/variant_comparison_a3.pdf`** — the three
  layout variants side by side, with metrics and rule checks under each. This is
  the "compare options as drawings" output.
- **`data/cad/wall_plan.svg`** — the real wall footprint pulled out of your
  Homestyler DXF (9819 × 9860 mm, true thicknesses down to 70 mm). Open it in a
  browser and zoom; this is the geometry the model should be rebuilt on.

Per-variant A3 sheets live in `data/outputs/variants/<variant-id>/sheets/`.

## With DWG TrueView (installed here)

TrueView opens DWG/DXF and nothing else, so each variant is also exported as a
millimetre DXF:

```powershell
.\.venv-ifc314\Scripts\python.exe tools\drawings\export_variant_dxf.py --all
```

Then open `data\outputs\variants\<variant-id>\<variant-id>_plan.dxf`.

`$INSUNITS` is set to millimetres, so **TrueView's own measure tool reads real
dimensions** — this is the file to use when you want to check a width rather
than just look at the layout. Layers carry the phase distinction, so switching
them tells the story:

| Layer | Shows |
|---|---|
| `A-WALL-EXIST` | walls that stay (hatched) |
| `A-WALL-DEMO` | walls to be removed — red, dashed |
| `A-WALL-NEW` | walls to be built — cyan |
| `A-DOOR` / `A-WINDOW` | openings, each labelled with its width in mm |
| `A-ROOM` / `A-ROOM-TEXT` | room outlines, names and areas |
| `A-FURN` | furniture, once there is any |

Turn `A-WALL-DEMO` on over `A-WALL-EXIST` and you are looking at a demolition
plan.

The original Homestyler export opens there too:
`data\cad\dxf\20260727-ZK Dubravinskiy.dxf` — though it carries all 8 plan
instances plus every elevation, so it is crowded.

## Viewing the 3D model (Blender is installed here)

The IFC is the real model; the renders are just pictures of it.

**1. Open the `.blend` — no add-on needed.** The repo carries its own portable
Blender 5.2 with Bonsai already set up and verified, and uses it to convert a
variant's IFC into a Blender scene:

```powershell
.\.venv-ifc314\Scripts\python.exe tools\blender\verify_environment.py `
  --blender tools\blender\bin\blender-5.2.0-windows-x64\blender.exe `
  --profile tools\blender\profile3 `
  --bonsai-site tools\blender\profile3\extensions\.local\lib\python3.13\site-packages `
  --ifc data\outputs\variants\v1-kitchen-living\model.ifc `
  --blend-output data\outputs\variants\v1-kitchen-living\model.blend `
  --output data\outputs\variants\v1-kitchen-living\blender_env.json
```

The `model.blend` it writes opens in **your own** Blender with nothing
installed. Swap the variant id to build the others. `v1-kitchen-living` is
already built.

**2. Your Blender with Bonsai installed** — then `File → Open IFC Project` on
the `.ifc` directly. This is the only route where the model answers questions:
click a wall and read its phase, click a room and read its area. Worth setting
up once.

**3. Convert to glb** — the repo ships the converter:

   ```powershell
   .\tools\ifc\bin\IfcConvert.exe data\outputs\variants\v1-kitchen-living\model.ifc `
     data\outputs\variants\v1-kitchen-living\model.glb
   ```

   Then double-click the `.glb`. Fastest way to spin the model around, but it
   loses all the data behind the geometry.

## What you are looking at is not final

Every sheet carries "not for construction", and it means it: the model is still
`planned_from_visual_sources_not_field_verified`, and
`tools/ifc/audit_model_quality.py --strict` currently **fails** — two walls are
modelled twice and 10.9% of the wall volume is double-counted at junctions. Look
at the drawings to judge the layout, not to take measurements off.
