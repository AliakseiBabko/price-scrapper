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

## Viewing the 3D model

The IFC is the real model; the renders are just pictures of it. Three ways in,
cheapest first:

1. **Blender + Bonsai** (the IFC add-on, already used in `tools/blender/`) — open
   Blender, install/enable Bonsai, then `File → Open IFC Project`. Full model
   with properties: click a wall and read its phase, click a room and read its
   area.
2. **A free standalone viewer** — BIM Vision on Windows opens IFC directly, no
   setup, good for a quick walk-through and for checking that openings really
   cut the walls.
3. **Convert and use the Windows 3D Viewer** — the repo ships the converter:

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
