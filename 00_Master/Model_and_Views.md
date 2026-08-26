# One model, many views

## The question

Are the 2D plans and the 3D volume two separate models, or one model shown two
ways?

## The answer: one model

**One model. The 2D drawings are generated *from* the 3D model, not drawn
alongside it.** That is the whole reason for the spec → IFC pipeline, and it is
already how everything currently produced works:

```
data/canonical/current_apartment_base.json      the geometry, once
        + data/variants/<id>.json               a variant as a patch
                    │
                    ▼
      tools/ifc/model_from_spec.py              ONE model per variant
                    │
                    ▼
             model.ifc  ── the single source of truth
                    │
   ┌────────────────┼─────────────────┬──────────────────┐
   ▼                ▼                 ▼                  ▼
A3 sheets        DXF plan         Blender / glb      quantities
(SVG + PDF)      (TrueView)       (3D volume)        (areas, finishes)
2D              2D               3D                 non-graphic
```

Every one of those is a **view**. A floor plan is a horizontal section through
the model at about 1.2 m; an elevation is a vertical one; the 3D scene is the
same solids with no section at all; a schedule of floor areas is a view with no
picture in it. In BIM terms they are all derived representations of one dataset,
and that is the standard practice this repo follows.

## Why it has to be one

If the plan and the 3D were separate models, they would drift the first time
anything changed — and you would not find out which one is wrong until a
contractor did. With one model:

- moving a wall in the spec changes the plan, the DXF, the 3D and the floor
  areas in the same run;
- **if two outputs disagree, that is a bug in a generator, not something to fix
  by editing a drawing.** Never correct a plan by hand — correct the model and
  regenerate;
- quantities are computed from the same solids you are looking at, so a
  take-off cannot quietly describe a different flat.

## What legitimately lives outside the model

Not everything belongs in the model, and forcing it there is the opposite
mistake:

| Belongs in the model | Belongs in the drawing layer |
|---|---|
| Walls, openings, rooms, levels | Dimension chains, which ones to show |
| Element phase (existing/demolished/new) | Red demolition hatch, dashed originals |
| Furniture as placed objects | Whether furniture is shown or greyed on this sheet |
| Finish assigned to each surface | The hatch pattern that represents that finish |
| Areas computed from geometry | The экспликация block layout |

That is the same rule as for layers in
[Finishes_and_Furniture_Data_Model.md](Finishes_and_Furniture_Data_Model.md):
the model holds what a thing *is*; the sheet decides what to *show*.

The one deliberate exception is the **3D массинг**: Dolgushev's album uses a
simplified grey volume rather than a render, because it sells understanding of
space rather than a picture of a finished interior. That is still generated from
the same model — a simplified *representation*, never a second model.

## Where this is not true yet — and it should be

The principle is right; the repo has not finished converging on it. Five
geometry definitions exist today:

| File | What it is | Fate |
|---|---|---|
| `data/canonical/current_apartment_base.json` | the spec the variant pipeline uses | **keep — this is the one** |
| `tools/ifc/current_apartment_layout.py` | the original hardcoded seed | retire once the spec is CAD-based; keep as the provenance record |
| `data/canonical/apartment_provisional.json` | earlier provisional model | legacy |
| `data/canonical/apartment_design.json`, `apartment_poc.json` | proof-of-concept models | legacy, demo only |
| `data/cad/wall_plan.json` | the **real** footprint from the Homestyler DXF | should become the source of `current_apartment_base.json` |

So the honest current state is: *one model per variant, but more than one
definition of the flat.* Converging them is the next piece of work — rebuild
`current_apartment_base.json` from the CAD footprint, then the hardcoded seed
and the provisional models have no reason to exist.

## The viewing setup this project uses

Fixed, so it does not have to be rediscovered:

- **2D → DWG TrueView.** Variants export to millimetre DXF with phase layers;
  TrueView's measure tool reads real dimensions.
- **3D → Blender.** Either the `.blend` produced by the repo's portable
  Blender 5.2 + Bonsai (opens in a plain Blender, no add-on), or Bonsai in your
  own Blender to get the data as well as the geometry.
- Everything else — sheets, renders, comparison — through
  `tools/drawings/build_gallery.py`.

Commands in [How_To_View_Outputs.md](How_To_View_Outputs.md).
