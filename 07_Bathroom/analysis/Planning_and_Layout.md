# Bathroom — Planning & Layout

Covers the decisions to settle before drawing a layout: approvals, combined-vs-separate, budgeting for finish-layer thickness, a full sizing formula for a tight "two-fixture" bathroom, two planning techniques, fixture-placement priority, and the toilet-visibility preference question. Part of [[07_Bathroom/Bathroom_Guide|Bathroom Guide]] — see that page for the full section index.

## Approvals and Expansion Direction

- **Order an ЕГРН extract with its graphic (floor-plan) section before starting any layout planning**, per the Russian process described (via Госуслуги/state services) — every organization you'd ask "can this be approved" will require this document first, alongside your own proposed plan (hand-drawn or software-made, either is fine). `single-account`, **Russia-specific process — not confirmed to apply to Belarus**; treat as a prompt to find the equivalent Belarus document/process, not as this project's own procedure. *(This project's stricter-bar regulations store is at `11_Budget_and_Planning/_supporting/knowledge/intermediate/renovation_regulations_belarus_knowledge_store.md` — this source doesn't meet that store's Belarus-location bar and isn't added there.)*
- **If expanding the bathroom's footprint, you can only expand into non-residential space** (typically a hallway/corridor or a storage closet) — expanding into a living room or bedroom is described as essentially never approvable, for any apartment above the ground floor. An apartment on the ground floor above a basement or commercial unit reportedly follows different (looser) rules. `single-account`, same Russia-specific caveat.

## Combined vs. Separate Bathroom/WC

Default to a **separate** bathroom and WC. Build/keep a **combined** layout only when:
- The apartment is small and ≤3 people use the one bathroom.
- The unit has multiple bathrooms, each serving ≤2 people.
- The apartment is intended for rental — a combined layout saves on tiling/waterproofing labor (one fewer wall needing two-sided finishing) and reads as more modern/photogenic in listing photos.

`single-account`, but a clear, actionable default with stated reasoning rather than a bare preference.

## Budget for Finish-Layer Thickness, Not Raw Measurements

**Don't plan a layout against the raw measured room dimensions** — budget for what plaster and tile actually consume off each wall before finalizing clearances:
- **Plaster**: ~1–1.5 cm per side (recommend budgeting the full 1.5 cm).
- **Tile + adhesive**: ~1.5 cm per side (roughly 0.5 cm adhesive + ~0.9–1 cm for the tile itself).

A wall measured at 3.5 m can easily finish out closer to 3.2 m once both layers are accounted for on both sides — plan fixture clearances against the *finished* dimension, not the bare-shell one. `single-account`, but a concrete, checkable number worth applying regardless of source.

- **Sink minimum clear width: 80 cm after finish layers** — a worked example from a critiqued layout: a nominal 81 cm stud-to-stud gap shrank to just 75 cm once plaster and tile were applied, judged too narrow. Directly reinforces the finish-layer-thickness caveat above with a concrete case where skipping it produced an unusable width. `single-account`, `unverified`. [source: `_Archive/processed_sources/20260804_worst_layout_bathroom_kitchen_clearances_7629bd27.txt`]

## Minimum "Two-Fixture" Bathroom Sizing Formula — per Zemskov/Zemstandart

> [!NOTE]
> Everything in this subsection is **one practitioner's (Alexey Zemskov / Zemstandart-Zemsproekt, Moscow-based) own stated design convention**, `single-account` throughout, presented in his video as his company's standard formula — not a building code and not independently verified against another source. Treat it as a self-consistent, arithmetic-checkable starting point to weigh against your own preferences, not a settled rule. [source: `_Archive/processed_sources/20260810_small_two_fixture_bathroom_sizing_aa1b3a59.txt`]

Covers the specific case of a "two-fixture" bathroom (tub + one of: toilet/sink/washing machine) where risers/plumbing stacks sit in an *adjacent* room:
- **Room width** (Zemskov's formula): from the start wall → +100mm wall thickness → +915mm door-and-trim clearance (15mm tile+adhesive + 100mm door-trim standoff + 700mm smallest door + 100mm standoff) → + the bathtub's own width. **Zemskov's rule**: don't add the 15mm tile allowance on the bathtub side — the tub sits flush, tile overhangs the rim instead.
- **Bathtub width, per Zemskov**: 700mm minimum (workable but uncomfortable), 800mm his practical default, 900mm for larger-bodied occupants.
- **Room length, per Zemskov**: = the bathtub's own length, no added tile allowance (tile overhangs the tub on the three exposed sides).
- **Bathtub length matched to occupant height, per Zemskov**: length ≈ occupant height, or up to 10cm less — his worked example: a 178cm-tall person fits a 180cm tub comfortably, but the same person in a 190cm tub could slide under and choke. His defaults: 1700mm typical / 1800mm for taller occupants.
- **Zemskov's resulting standard footprint**: 1715×1700mm or 1815×1800mm, depending on tub choice.
- **Zemskov's mixer-placement rule, flagged as the single most common mistake he sees**: always center the mixer on the tub's true physical center, never on the reduced width left after subtracting the tile overhang — an off-center mixer next to a centered drain/overflow reads as visibly wrong.
- **Zemskov's toilet cistern-box height rule**: build full floor-to-ceiling with a 600×900mm access hatch if a shutoff manifold or chemical cabinet sits above; otherwise 1250mm topped with a decorative countertop.

> [!NOTE]
> **Zemskov's tub-length rule above (170cm typical for a ~178-180cm occupant) contradicts a different practitioner's rule** in [[07_Bathroom/analysis/Bathtub_and_Shower|Bathtub & Shower Selection]] §Length Ergonomics ("170cm even for a ~180cm-tall person, don't default to the longest tub that fits"). The two land on similar numbers but via different reasoning (occupant-height-matched vs. "shorter forces better back-bracing") — see that page's own framing for the full contrast.

## Two Planning Techniques

1. **Write an explicit list of everything the bathroom needs to fit** before laying anything out: every fixture (tub, sink, hygienic shower, toilet type — wall-hung/floor-standing), washer/dryer (separate or combo), storage for cleaning supplies, a laundry hamper, storage systems (open/closed shelving, wall/floor-mounted cabinetry), water heater type, and every planned light source (main, dimmed/decorative, mirror-specific, niche/accent). Handing a complete list to a designer (or using it yourself) catches "this doesn't fit" problems on paper instead of during construction.
2. **Mentally walk through the actual use scenario** once a draft layout exists: leaving the shower, where's the towel — floor, hook, rail? Where do you put worn clothes? Where does the laundry hamper live, and how do you load it? This kind of walkthrough surfaces placement mistakes a static floor plan doesn't.
3. **Verify fixture clearance against the door opening's actual position, not just gross wall dimensions.** A documented developer-layout defect: a toilet with only ~7 cm of passage clearance because the door opening was located without checking it against the space actually needed for toilet + sink + tub placement — a person entering repeatedly hit the fixture with their knee. A narrow wall stub next to a bathroom doorway (360 mm in the same example) was called out as too narrow to place fixtures without one protruding into the opening. `single-account`, `unverified`, but a genuinely checkable planning failure mode. [source: `_Archive/processed_sources/20260804_worst_layout_toilet_clearance_kitchen_sill_91ec632e.txt`]

## Fixture Placement Priority

**Start placing fixtures with the toilet, not last.** It has the widest drain pipe and should have the shortest, straightest run to the stack — everything else is placed around it. **The shower podium/drain is the second priority**, since it's the lowest drainage point in the room (where the trap sits) and also has real routing constraints. Everything else can be placed more flexibly around these two anchors.

## Toilet Visibility From the Entrance

A pure design/personal-preference point, included for completeness: some people strongly dislike seeing the toilet immediately upon entering and design the layout (sink or shower up front, toilet tucked away) around hiding it; others (including the Ontario source, personally) don't consider it worth trading entry convenience for. If this matters to you, it's worth deciding deliberately rather than defaulting — the source notes a real case where a client had the door position shifted specifically to avoid a toilet sightline, accepting a less convenient entry angle in exchange.

## Comfort-Class Labor Cost (restated)

**Comfort-class labor-only cost band, restated by Zemskov**: 25,000-45,000 RUB/m², matching a figure this store already has from a different Zemstandart video — same channel repeating its own convention over time, not independent corroboration.
