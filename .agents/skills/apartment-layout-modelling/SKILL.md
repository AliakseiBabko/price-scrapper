---
name: apartment-layout-modelling
description: "Turn a described layout change into a built model and every drawing of it, for ZK Dubravinskiy. Holds this flat's non-negotiable facts (which plan is authoritative, clear-vs-gross areas, the ±25 mm tolerance, the services that may never move), the variant patch format and its operation vocabulary, the one-command build chain, and the viewing toolchain. Use whenever a layout option is proposed, compared, modelled, drawn, or rendered - and before quoting any dimension or area of this apartment."
---

# Apartment layout modelling — ZK Dubravinskiy

**Read this before quoting a dimension, proposing a layout, or building a model
of this flat.** The facts below were established from the plans and from the
owner; re-deriving them costs hours and has already produced two wrong answers.

## The flat in one paragraph

Type 3Б/3+, **69.09 m²** total, **4th floor**, building not finished, nothing
field-verified. Rooms as sold: жилая 19.49 / 16.64 / 9.36, прихожая 9.79,
кухня 5.24, ванная 3.09, туалет 1.24, лоджия 6.05 (counted 4.24). Partitions
are drawn **75 mm**. The owner has redesigned it in Homestyler; that redesign is
a *variant*, not the existing state.

## Sources of truth — what each one may be used for

| Source | Authoritative for |
|---|---|
| `_Inbox/_Visual_Drop/fllor_plan_detailed.jpeg` | **The base case (v0).** Room areas, dimension strings, opening widths |
| `_assets/floor_plan_initial.jpg`, `_Inbox/_Visual_Drop/floor_plan_basic.jpg` | Cross-check of the same layout |
| `_assets/floor_plan_modified.png` | **Room names and areas of the owner's redesign** |
| `data/cad/dxf/20260727-ZK Dubravinskiy.dxf` | **Wall geometry of the redesign**, millimetre precision |
| `_Inbox/_Visual_Drop/floor plan_1..3.jpg` | **How much the built flat will differ** |

Extracted, so nobody re-reads the images:
`data/canonical/room_schedules.json`, `data/canonical/dimension_tolerance.json`,
`data/cad/wall_plan.json`. Narrative: `00_Master/Apartment_Geometry_Sources.md`.

## Four facts that change answers

1. **Clear vs gross areas — never compare across them.** The developer publishes
   *clear* floor with service blocks deducted; the БТИ-style measured plans
   publish *gross* to the wall faces. Worked example: туалет 1140 × 1090 =
   1.24 m² clear, plus the 1140 × 490 вентблок = 1.80 m² gross, which is what
   two of the three measured flats print. Where a developer area and a measured
   area differ by about a service block, that is the explanation *before* any
   construction difference is.

2. **Usable floor in the туалет is ~1.24 m², not 1.8.** Anything sized against
   the bigger number will not fit.

3. **±25 mm.** Wall-to-wall dimensions of the same nominal wall differ by
   0–50 mm (median 20) across three as-built comparables. Treat every dimension
   as nominal ±25 mm and **never design a fit needing less than ~30 mm of
   slack** — no full-wall built-in without a scribe.

4. **Ventilation depends on the floor; plumbing does not.** Above the 10th floor
   a flat carries two ventilation sections instead of one, taking extra area.
   This flat is on the 4th — single section, larger areas. So `kv109`
   (туалет 1.6, total 68.3) is a **higher-floor sub-type: do not average it in.**
   Use `kv53` and `Минина 6` as the comparables.

## Services that may never move

Common property. A variant that assumes otherwise produces a drawing nobody can
build, so `make_variant.py` refuses it.

- **Вентблок in the туалет**, 1140 × 490, three channels — verified on the plan.
- **Second вентблок** between the kitchen zone and the laundry/hallway zone —
  owner's account, not yet measured.
- **Стояки** водоснабжения и канализации in the wet zone — identical on every
  floor.

Recorded as `constraints` in `data/canonical/room_schedules.json`.

## One model, many views

2D is **generated from** the model, never drawn beside it. Spec + variant patch →
one IFC → A3 sheets, DXF, Blender/glb, quantities. **If two outputs disagree
that is a generator bug — fix the model and regenerate, never edit a drawing.**
Annotation (dimension chains, hatches, экспликация) belongs to the drawing layer,
not the model. See `00_Master/Model_and_Views.md`.

## Describing a change → a built model

A variant is a **patch** on the base spec, not a copy. Write
`data/variants/<id>.json`:

```json
{
  "schema_version": "0.1.0",
  "variant_id": "v3-example",
  "name": "Вариант 3 — ...",
  "base_spec": "data/canonical/current_apartment_base.json",
  "status": "draft",
  "concept": "one sentence saying what idea this option is testing",
  "cites_rules": ["kitchen.open_to_living_for_flow"],
  "operations": [
    {"op": "wall.remove", "walls": ["Kitchen-living top partition"]},
    {"op": "zone.merge", "rooms": ["Kitchen", "Living room"], "into": "Kitchen-living", "role": "living"}
  ]
}
```

Operation vocabulary — the same verbs the layout-case dataset uses for what
architects do to a plan:

| op | fields |
|---|---|
| `wall.remove` | `walls[]` — flagged demolished, not deleted, so the demolition sheet can draw them |
| `wall.add` | `wall{name,x_m,y_m,length_m,horizontal,thickness_m}` |
| `wall.thicken` | `wall`, `to_m` |
| `opening.create` / `opening.remove` | `opening{...}` / `openings[]`, `fills[]` |
| `zone.merge` / `room.resize` | `rooms[]`,`into`,`role` / `room` + fields |
| `furniture.place` | `item{name,room,product_id,x_m,y_m,width_m,depth_m,rotation_deg}` |
| `finish.set` | `room`, `finish{floor,wall,ceiling,ceiling_height_m,skirting}` |
| `circuit.assign` | `circuits{room: circuit}` |

Then one command builds everything:

```powershell
.\.venv\Scripts\python.exe tools\layout\make_variant.py v3-example
```

It checks the immovable services, builds the model, audits the geometry, and
writes the A3 sheets, the TrueView DXF, the Blender scene, the comparison sheet
and the gallery. `--no-blend` while iterating; `--force` only after confirming a
flagged service is genuinely untouched.

## Viewing

- **2D → DWG TrueView**: `data/outputs/variants/<id>/<id>_plan.dxf`, millimetres,
  phase layers (`A-WALL-EXIST` / `A-WALL-DEMO` / `A-WALL-NEW`). TrueView's
  measure tool reads real dimensions.
- **3D → Blender**: open `model.blend` (no add-on needed), or the `.ifc` with
  Bonsai to get the data as well as the geometry.
- **Everything** → `tools/drawings/build_gallery.py`, then open
  `data/outputs/gallery/index.html`.

Full detail: `00_Master/How_To_View_Outputs.md`.

## Environments and gotchas

- `.venv-ifc314` — ifcopenshell, ezdxf, numpy, Blender tooling.
  `.venv` — pymupdf, cairosvg, scraping. Neither has everything; `make_variant.py`
  calls each tool with the right one.
- Set `PYTHONIOENCODING=utf-8` for anything printing Russian on this console.
- Portable Blender 5.2 + Bonsai live in `tools/blender/`; no install needed.

## Known-open items

- **Room polygons for the redesign** are not extracted — the CAD has empty
  `P-Room` blocks, a gap at every opening, and 3 m openings no narrowness test
  can split. The room *schedule* is known; the polygons are not.
- `current_apartment_base.json` is still the photo-derived geometry and **fails**
  `audit_model_quality.py --strict` (2 duplicate walls, 10.9% double-counted).
  `current_apartment_cad.json` passes and should replace it.
- v0 should become the developer plan; the Homestyler design should become v1.
- The ±25 mm band is documented but not yet applied inside the rule checks.
