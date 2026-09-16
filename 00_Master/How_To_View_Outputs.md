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

## ⚠️ Walking the model in a browser (built 2026-09-16)

**The quickest way to answer a SPATIAL question — does the passage past a lowered
wall bed work, is that clearance tolerable — without opening Blender at all.**

```powershell
# 1. build the GLB from a variant's IFC (once per change to the model)
$env:BLENDER_USER_CONFIG     = "$PWD	oolslender\profile3\config"
$env:BLENDER_USER_EXTENSIONS = "$PWD	oolslender\profile3\extensions"
toolslenderinlender-5.2.0-windows-x64lender.exe --background `
  --python toolslender\export_glb.py -- `
  data\outputsariants0-existing\model.ifc `
  data\outputsariants0-existing\model.glb `
  data\outputsariants0-existing\glb_export.json `
  "$PWD	oolslender\profile3\extensions\.local\lib\python3.13\site-packages"

# 2. walk it
.venv\Scripts\python.exe toolslender\serve_walk_viewer.py
```

**W A S D** or the **arrow keys** to move, **Q/E** down/up, **Shift** to creep. The
HUD prints the model's extents and your eye height.

**⚠️ Layer buttons in the HUD switch each IFC class on and off** — Wall, Slab,
Door, Window, FlowTerminal. **Turn DOORS off to read a doorway as an opening**:
the model carries door leaves, which fill their openings and block the view when
what you want is the circulation. The class is carried in the GLB's node
`extras`, written by `export_glb.py`.

**Two ways to look around, and movement never depends on either**: click the
canvas for pointer-lock mouse-look, **or just click and drag**. ⚠️ **WASD works
whenever the page has focus**, locked or not — an earlier build gated movement on
pointer lock, and when the lock did not engage the viewer looked completely dead
while rendering perfectly.

> [!WARNING]
> **⚠️⚠️ JUDGE SPACE HERE, NEVER DIMENSIONS.** Eye height and stride are nominal
> figures chosen to make walking feel right. **Measure in the model**, per
> `00_Master/Evidence_Reading_Discipline.md`. The viewer says so on screen too.

**Why it must be served rather than double-clicked**: a browser refuses to fetch
the `.glb` from a `file://` page, so the viewer would sit on "loading…" with an
error only the console shows. `serve_walk_viewer.py` serves the working tree
read-only on localhost and opens the right URL.

### ⚠️ What the walkable view deliberately is not

- **Untextured, by design.** `tools/blender/glb_material_probe.py` establishes by
  parsing the exported GLB — not by looking at it — that **a flat Principled BSDF
  base colour survives a glTF export exactly** (colour, roughness and metallic all
  arrive) while **a procedural node network is dropped** (its material exports with
  a null `baseColorFactor`). **Textures would mean UV-unwrapping the whole
  apartment and baking per channel, because an IFC model out of Bonsai has no UV
  maps.** For judging clearance, flat colour is not a limitation — it is the point,
  and it keeps the file small enough to open in a browser. See
  [[00_Master/Model_and_Views|One model, many views]].
- **Each IFC class gets one flat colour** (walls neutral, doors orange, windows
  blue, fittings pale) purely for legibility while walking.
- **`IfcSpace` is dropped.** Room volumes are not physical; exported, they fill
  every room with a solid block you cannot see past.
- **⚠️ It is a VIEW, regenerated from `model.ifc`, and is never edited.** Nothing
  is authored here. If the walkthrough and the plan disagree, that is a bug in a
  generator — fix the model and re-export.

**⚠️ Reading the current export (`v0-existing`)**: 47 mesh objects, **65 KB**, 756
triangles, **10.28 × 8.56 × 2.72 m** overall — which is 0.12 floor slab + **2.50
clear height** + 0.10 ceiling slab. Two slabs, 18 walls, 7 doors, 4 windows, 16
flow terminals.

⚠️ **The clear height is the constructor's 2500 mm (screed to ceiling underside),
set 2026-09-16**, replacing an assumed 2.8 m. **So headroom in the walkthrough is
now representative** — earlier builds felt ~300 mm roomier than the flat will.
⚠️ **`v1-homestyler` carries no slabs at all**, floor or ceiling: it derives from a
canonical file that never had one. Pre-existing, and why only `v0-existing` reads
as an enclosed room.

⚠️ **A rebuild on 2026-09-16 also dropped 7 ceiling light fixtures** that the
previous (2026-08-26) build carried. **That is the model catching up, not a
regression**: `model_from_spec.py` now emits lighting only when a spec sets
`lighting.enabled`, on the stated grounds that *"a light in the middle of every
room is a decision nobody made."* **The old artefact predated that rule.**

**⚠️ `tools/blender/glb_inspect.py` reads any `.glb` without Blender** and prints
what is actually inside it — meshes, materials, base colours, texture count. Use it
rather than trusting the exporter's own report; it is the same reason the DXF gates
re-derive geometry from the source PDF.

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

> [!WARNING]
> **⚠️⚠️ Do NOT press `Ctrl+S` in that session. It writes to the `.ifc`.**
>
> Once Bonsai has a `.blend` and an `.ifc` connected, **the save shortcut saves
> both** — an ordinary `Ctrl+S`, or `File → Save`, rewrites the model file you
> opened to look at. Blender users press it by reflex.
>
> **Nothing currently catches this.** `check_dxf_closure.py` and
> `raster_fidelity.py` both assert the **DXF** against `data/canonical/` and the
> source PDF; **a mutated `.ifc` that nothing re-derives from is checked by
> neither.** The model files under `data/outputs/` are build products, so a
> stray save is recoverable by rebuilding — **but only if you notice.**
>
> **Until this is gated, treat viewing as read-only**: rebuild rather than trust
> a file you have had open. Source and the two candidate fixes (read-only
> viewing copy, or hash the IFC in the batch gate):
> [[18_Digital_Toolchain/analysis/Model_To_Drawing_Pipeline|Model to Drawing Pipeline]] §6.

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
