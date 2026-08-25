# Where finishes and furniture live

## The question

"Should finishes and furniture be separate layers — or what?" Written down
because it decides the shape of `cap4` and `cap5` in
[Sheet_Production_Roadmap.md](Sheet_Production_Roadmap.md), and because getting
it wrong is expensive to undo later.

## Short answer

**Layers are a drawing concept, not a data concept.** In CAD, a "layer" is a
switch that hides or restyles part of a drawing — furniture on, dimensions off,
demolition in red. That is real and we do need it, but it is decided at drawing
time, generated from the data. If the *data* is organised as layers, every
question that crosses a layer ("what does the furniture in the kitchen cost?")
becomes hard.

So: organise the data by **what kind of thing it is**, and let the sheets switch
layers on and off. Finishes and furniture are two different kinds of thing and
should not be stored the same way:

| | Furniture & appliances | Finishes |
|---|---|---|
| What it is | **Objects** that occupy space | **Properties of a surface** |
| Has geometry? | Yes — width, depth, height, position, rotation | No — a floor finish is an attribute of a room's floor |
| Drawn as | An outline on the plan | A hatch/shade plus an area number |
| Blocks things? | Yes — circulation, door swings, socket positions | No |
| Varies per variant? | Heavily — variants differ mostly in furniture | Rarely — usually chosen once for the whole flat |
| Stored as | placements in the variant | a per-room schedule |

## Three files, not one

### 1. `data/catalog/products.jsonl` — what a thing *is*

One line per real product: an IKEA wardrobe, a specific tile, a specific hob.
Independent of any apartment or variant.

```json
{"product_id":"wardrobe-pax-250","category":"furniture","name":"PAX 250×58×236",
 "width_mm":2500,"depth_mm":580,"height_mm":2360,
 "price":{"amount":1180,"currency":"BYN","date":"2026-08-20","region":"minsk"},
 "source_url":"…","status":"candidate"}
```

This is the natural home for the price-scraping half of the repo: prices,
vendors, dates and regions already have tooling in `tools/pricing/`. Keep the
`price` block dated and regional — the standing rule that a price is meaningless
without location and year applies here too.

`category` covers furniture, appliance, sanitary **and finish** — a tile is a
product with a price per m² rather than a width and depth. Same file, different
required fields per category.

### 2. Placements — *where* a thing goes, inside the variant

Furniture placement belongs to a **variant**, because that is exactly what
differs between options. It is already an operation in the variant format:

```json
{"op":"furniture.place",
 "item":{"name":"Wardrobe","room":"Entrance hall","product_id":"wardrobe-pax-250",
         "x_m":2.1,"y_m":6.4,"width_m":2.5,"depth_m":0.58,"rotation_deg":0}}
```

One product may be placed many times; a placement only references the
`product_id`. That separation is what lets the budget be computed by joining
placements to prices, and lets you swap a product without touching any layout.

### 3. Finish schedule — a property of each room

Also a variant operation, but it writes to a per-room map rather than a list of
objects:

```json
{"op":"finish.set","room":"Kitchen",
 "finish":{"floor":"tile-керамогранит-600","wall":"paint-white-matt",
           "ceiling":"stretch-matt","ceiling_height_m":2.62,
           "skirting":"mdf-80"}}
```

The builder already writes these onto the IFC space as properties
(`Pset_ApartmentSpecEvidence`), so the floors sheet, the ceilings sheet and the
finish quantities all read the same single source. Areas are **computed from the
model**, never typed — that is what makes the floors sheet trustworthy and what
feeds the budget pages.

## How that becomes layers on a sheet

Drawing time, derived — nothing to maintain by hand:

| Sheet | Layers switched on |
|---|---|
| План с расстановкой мебели | walls(existing+new) · furniture · room labels · экспликация |
| Демонтажный план | walls **by phase** · dimensions · demolition hatch |
| План полов | rooms shaded **by floor finish** · junction lines · areas |
| План потолков | ceiling levels · light fixtures · dimensions |
| Розетки | walls · furniture (greyed, for reference) · electrical symbols |

Note the furniture appears greyed on the socket sheet: that is a layer decision,
and it works only because furniture is object data, not a "furniture layer" in
the file.

## What this means for you in practice

You do not need CAD skills for any of it. The workflow is: pick products (which
is shopping, and the repo already scrapes prices), say which room each goes in,
and review the PDF that comes out. The drawing conventions are the machine's
problem.

## Decision status

Proposed 2026-08-26, not yet built. `furniture.place` and `finish.set` already
exist as operations in `tools/layout/build_variant.py` and the builder already
carries both onto the IFC — so the mechanism is in place and what is missing is
the catalogue file and the actual selections. See `cap4` and `cap5` in the
roadmap.
