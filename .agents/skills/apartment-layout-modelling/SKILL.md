---
name: apartment-layout-modelling
description: "Turn a described layout change into a built model and every drawing of it, for ZK Dubravinskiy. Holds this flat's non-negotiable facts (which plan is authoritative, clear-vs-gross areas, the ±25 mm tolerance, the services that may never move), the variant patch format and its operation vocabulary, the one-command build chain, and the viewing toolchain. Use whenever a layout option is proposed, compared, modelled, drawn, or rendered - and before quoting any dimension or area of this apartment."
---

# Apartment layout modelling — ZK Dubravinskiy

**Read this before quoting a dimension, proposing a layout, or building a model
of this flat.** The facts below were established from the plans and from the
owner; re-deriving them costs hours and has already produced two wrong answers.

## The flat in one paragraph

**69.1–69.4 m²** total, **4th floor**, building not finished, nothing
field-verified. Rooms as sold: жилая 19.49 / 16.6 / 9.36, прихожая 9.8–10.0,
кухня 5.24, ванная 3.09, туалет 1.2–1.4, лоджия 6.05 (counted 4.24). Partitions
are drawn **75 mm**. The owner has redesigned it in Homestyler; that redesign is
a *variant*, not the existing state.

**The developer issued two drawings and they disagree**, each internally
consistent:

| | designation | total | туалет | прихожая | dimensions? |
|---|---|---|---|---|---|
| `fllor_plan_detailed.jpeg` | 3Б/3+ | 69.09 | 1.24 | 9.79 | **yes — the only dimensioned source** |
| `floor_plan_basic.jpg` | 3Б/2+ | 69.44 | 1.42 | 9.97 | no — **this is the image traced in Homestyler** |

The 0.35 m² spread sits inside the ±25 mm band, so it changes no layout
decision — but **no single area figure here is exact**, and any quoted area
should say which drawing it came from.

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
   construction difference is. (Using the basic plan's 1.42 the sum is 1.98, so
   the match is suggestive, not exact — the mechanism holds, the precision does
   not.)

2. **Usable floor in the туалет is ~1.2–1.4 m², not 1.8.** Anything sized against
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

## Shell and options

Every layout option shares one **structural shell** and differs only in
partitions:

- `data/canonical/current_apartment_shell.json` — 14 walls, 250–484 mm, the
  façade openings, and the immovable services as `constraints`. Never edited by
  a layout option.
- `data/variants/v1-homestyler.json` — the owner's design: 36 partitions added
  to the shell, with its room schedule attached. **The owner's first
  approximation of the wanted layout — layout only, no finishes.**

That split is why an option is a short list of walls rather than a whole
building, and why the invariants cannot be edited by accident. The 200 mm
thickness threshold that separates shell from partition is a heuristic, **not a
structural survey — no wall may be called non-load-bearing on its strength.**

## The raster plan is registered — it is a tracing surface in millimetres

The owner drew the Homestyler layout on the developer's detailed plan as a base
image, so the two share a frame. `tools/cad/overlay_plan.py` recovers it:

- **20.63 mm per pixel, origin at (26, 22)** in `fllor_plan_detailed.jpeg`,
  aspect agreeing with the CAD to 1.7%. Register against the **detailed** plan
  even though the **basic** plan was the tracing base in Homestyler: it is the
  more accurate target. On the basic plan the residual is a thin fringe along
  every wall — a scale/offset error, not a geometric difference.
- `--diff` colours the result: **green where a CAD wall sits on a drawn wall,
  red where it does not**. Output: `data/cad/overlay_developer_plan_diff.png`.

Two things that buys:

1. **The CAD extraction is validated.** 27177 of 30511 wall pixels — **89.1%** —
   land on walls the developer drew. The extraction is faithful to the plan it
   came from, which nothing else had confirmed.
2. **The redesign's additions are visible and measurable**: the remaining 10.9%
   is where the owner added partitions — the laundry/entrance split and the wall
   forming the Kids Room. Read red as "look here", not as a measurement; it also
   picks up jitter along hatched edges.

That registration is also how **v0 gets geometry**: the developer's own
partitions can be traced off the raster in millimetres rather than guessed.

## Describing a change → a built model

A variant is a **patch** on the shell, not a copy. Write
`data/variants/<id>.json`:

```json
{
  "schema_version": "0.1.0",
  "variant_id": "v3-example",
  "name": "Вариант 3 — ...",
  "base_spec": "data/canonical/current_apartment_shell.json",
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

- **v0, the developer's own layout, has no geometry yet.** Its room schedule and
  dimensions are known, but its partition positions are not — they exist only on
  the plan image. Cheapest fix by far: export the *original* layout from
  Homestyler as a second DXF, the way the redesign was exported. Failing that,
  reconstruct the partitions from the dimension strings by hand.
- **Room areas and perimeters are solved.** Homestyler writes them into the DWG
  on layer `P-Comment Text` as `Kids Room S:15.28m² C:18.43m`. Extract with
  `tools/cad/extract_room_labels.py` — 10 rooms, 69.48 m². Those numbers are
  authoritative; use them for quantities.
  **Room outlines are still approximate.** `tools/cad/build_rooms_from_seeds.py`
  grows each room from its label's seed and checks the result against the room's
  own area: 3 of 10 land within 8%, the rest carry `extent_delta_pct` and an
  `extent_confidence` of `approximate`. Use the boxes to place things, never to
  measure them.
- **4 of 13 openings** have no host wall (their gaps are wider than the host
  search reaches); they are carried in `unresolved_openings` and produce no void.
- `current_apartment_base.json` is the old photo-derived geometry and still
  **fails** `--strict` (2 duplicate walls, 10.9% double-counted). Nothing should
  build on it; it stays only as provenance.
- The ±25 mm band is documented but not yet applied inside the rule checks.
- **The sheet renderer still carries demo text** ("Generic enclosed apartment
  demonstrator", "Residential renovation demo") and does not label rooms or draw
  door swings. That is the `cap1` conventions work, not a model problem.
- **The DWG holds every export sheet**, not just the floor plan: the eight
  `P-Wall-Section` instances are the sheet set (A-01…A-13 — Layout Plan,
  Furniture Size Plan, Ceiling, Light Control, Voltage, Water Supply, Material
  Tables). Re-exporting with everything ticked produces the same file we already
  have, so the remaining sheet data is a matter of reading the file, not of
  exporting again.
