# Sheet production roadmap — from the current model to the album

## Purpose

Answers one question: **what has to change in the model for each sheet of the
target album to come out of it?** Scope decision of 2026-08-26: тёплый пол is
not being installed, so that sheet is dropped — **11 sheets in scope**, tracked
in [`price-scrapper-target-set.json`](../data/deliverable_templates/price-scrapper-target-set.json).

Yes, this needs a plan, for one reason: the sheets are not independent
work items. Five of them wait on the same two model changes, and doing those
two changes first turns most of the remaining work into rendering rather than
modelling.

## Where the model actually stands

More is already built than the first pass credited (corrected 2026-08-26):

- `data/outputs/current_apartment/current_apartment_seed.ifc` — 18 walls,
  8 spaces, 11 openings (7 doors, 4 windows), 13 electrical devices,
  3 plumbing devices, 7 light fixtures.
- **Four A3 sheets already generate** via `tools/drawings/apartment_sheet_from_ifc.py`
  (`--sheet-kind architectural|electrical|plumbing|combined`), with a real SVG→PDF
  pipeline, a manifest per sheet, and placement validation that already checks
  symbols snap to walls, avoid openings, and sit inside rooms.
- Status on every one of them: `planned_from_visual_sources_not_field_verified`,
  classified "coordination-ready; not for construction".

So the gap is **not** "we have no drawing engine". It is: the model carries no
*phase*, no *finishes*, no *real furniture*, and no *circuits* — and the sheets
that exist are drawn from heuristics rather than decisions.

## Ten capabilities, in dependency order

Each is a discrete piece of work. Sheet ids refer to the target set.

### cap0 — Approve the control dimension  *(gate, not a blocker for structure)*

Everything numeric is provisional until a field measurement fixes one control
dimension (`tools/cad/PROVISIONAL_MODEL_POLICY.md`; hall depth still carries
2280/2310/2330 mm scenarios and two area scenarios, 69,09 / 69,44 m²).

Nothing below is blocked by this — but **no sheet may lose its "not for
construction" stamp until it is done.** Treat it as a release gate, and keep
building against the provisional model in the meantime.

### cap1 — Drawing conventions layer  *(do first; every sheet uses it)*

One shared module, not per-sheet code: экспликация block (numbered rooms +
areas + key), scale bar, north/entry arrow, wet-zone fill, dashed original
partitions, red demolition hatch, title block, and the "final variant" flag.
These are the conventions read off Dolgushev's albums
([Planning_Project_Deliverable_Set.md](Planning_Project_Deliverable_Set.md#graphical-conventions-worth-copying)).
Cheap, and it lifts all 11 sheets at once.

*Unlocks: every sheet. Touches: `tools/drawings/apartment_sheet_from_ifc.py`.*

### cap2 — Element phase (existing / demolished / new)  *(highest leverage)*

Give every wall, opening and partition a phase property. This is the single
change that unlocks the two sheets a contractor actually starts from.

It also closes the loop with the layout dataset: the `moves[].op` vocabulary
already **is** a phase assignment — `wall.remove` → demolished, `wall.add`/
`wall.thicken` → new, `opening.create` → new opening, `layer.add` → new finish
layer. A chosen variant's move list should be replayable onto the model to
produce the phased state, rather than the phase being typed in by hand.

*Unlocks: sheets 3 (демонтаж), 4 (перегородки). Touches:
`tools/ifc/current_apartment_layout.py`, the case `moves[]` reader.*

### cap3 — Setting-out dimensions

Dimension chains that tie new partitions to existing structure, and ceiling
fixture coordinates. `add_dimension()` already exists in the sheet renderer;
what is missing is choosing *which* chains to draw, from the phase data.

*Unlocks: sheets 4, 7. Depends on: cap2.*

### cap4 — Furniture and appliances as real objects

Replace the placeholder furniture with actual chosen products and their real
dimensions, each tied to a room. This is also what makes the socket plan a
design rather than a guess — sockets follow furniture and appliances.

Note `15_Appliances/` and `14_Furniture/` already exist as wiki folders; the
selection work partly exists in prose and needs to become model data.

*Unlocks: sheets 2 (мебель), 8 (розетки), 10 (сантехника).*

### cap5 — Room finish and ceiling schedule

Per-space: floor finish type, junction lines between finishes, skirting type,
ceiling level. `tools/ifc/calculate_wall_finishes.py` already does the wall
equivalent — extend the same pattern to floors and ceilings, with areas
computed from the model rather than typed.

*Unlocks: sheets 5 (полы), 7 (потолки). Feeds: budget pages.*

### cap6 — Daily scenarios as data

The lighting and socket sheets are the two where Dolgushev's method needs
something we hold only as prose: who does what, where, when. `00_Master/Family_Requirements.md`
and the case schema's `household.scenarios[]` are the shape it should take —
a scenario names the zones it touches, so a socket or switch can cite it.

*Unlocks: sheets 6, 8. Note: this is a decision-capture task, not a coding task.*

### cap7 — Sheet index generator

Emit sheet 1 from the manifests the renderer already writes. Trivial, but do it
last so the list is final.

### cap8 — Circuits and switch grouping

Model which switch drives which fixture group. The value of the lighting sheet
is entirely in this grouping; the fixture dots are already printable.

*Unlocks: sheet 6. Depends on: cap6.*

### cap9 — Marks and table blocks

Mark generator (D-01, W-01 …) plus a reusable table block on the sheet. Needed
for the opening-marking sheet and reusable by any schedule later.

*Unlocks: sheet 9.*

### cap10 — Massing style and per-room views

Grey monochrome output, no materials, one camera per room. `tools/blender/`
already builds the scene; this is styling and view setup.

*Unlocks: sheets 11–15.*

## Suggested order of work

1. **cap1** (conventions) — improves everything already generated, immediately visible.
2. **cap2 + cap3** (phase, setting-out) — the two contractor-facing sheets, and
   the link from the layout dataset into the model.
3. **cap5** (finishes) — floors sheet, and it feeds the budget pages, not just drawings.
4. **cap4** (furniture) — then the furniture, socket and sanitary sheets stop being heuristic.
5. **cap6 + cap8** (scenarios, circuits) — lighting sheet.
6. **cap9, cap10, cap7** (marks, massing, index) — finish the album.
7. **cap0** whenever the field measurement happens; then re-issue everything and
   drop the "not for construction" classification.

That is roughly four working blocks before the album is complete in draft form,
with a usable contractor-facing subset (demolition + partitions + floors) after
step 3.

## Two things to decide before starting

- **Does the model represent one variant or several?** The layout dataset holds
  variants; the IFC currently holds one state. Replaying a variant's moves onto
  the model (cap2) is what would let you compare options as drawings rather than
  as JSON — worth deciding now, because it changes how phase is stored.
- **Where do finish and furniture selections live?** They exist as prose across
  `13_Surfaces_and_Finishes/`, `14_Furniture/`, `15_Appliances/`. cap4 and cap5
  need them as data with a room binding; that is a small schema of its own.
