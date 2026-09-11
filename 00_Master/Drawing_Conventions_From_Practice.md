# Drawing conventions from practice

**Created 2026-09-08.** What practitioners' own documentation does, and why — collected to settle conventions this project has open rather than to admire other people's software.

This page exists because the vault's taxonomy is a taxonomy **of the renovation**, not of the project's paperwork. Socket heights have a home in `12_Engineering_and_Systems/`; *how a socket is dimensioned* has none, and burying a drawing convention inside a page about wiring loses it. Routing decision and its reasoning: [`_Inbox/planning/design_toolchain_sources_triage_20260908.md`](../_Inbox/planning/design_toolchain_sources_triage_20260908.md) §5.

> [!IMPORTANT]
> **⚠️ Everything here is a named practitioner's practice or a named tool's design decision, never a norm.** Nothing on this page is a Belarusian requirement, nothing here has been checked against one, and no figure here has been verified. **Sources are Russian (Moscow) and one Russian software vendor.** Standing rule 4: nothing from these sources goes to `16_Legal_and_Regulations/`.

## Why this page exists now, and what it is for

Three of this project's open capability items are blocked on **conventions we have not chosen** rather than on code:

| Blocked on | Item |
| :--- | :--- |
| What a dimension is measured **to** | `cap3` setting-out dimensions, plus the datum change in [`toolchain_gap_analysis_20260908.md`](../_Inbox/planning/toolchain_gap_analysis_20260908.md) §E |
| Whether a cable stub-out is **the same element** as a socket | The model's electrical taxonomy, and `ELE-01`'s BOM line |
| What a derived services plan actually **contains** | `cap6` → `cap8` |

**§E's warning is the reason for the hurry: these are cheap to choose now and expensive to retrofit once `cap3` starts emitting dimensions.**

---

## 1. Dimensioning

### To the centre, never the edge

**RemPlanner's rule, stated with the builder's reason** (`YT_OTBw7bCrv-o`): dimensions run to the **centre** of a socket, switch or luminaire, not to its edge — *«размеры всех светильников показывают расстояние до их центра, а не до края предмета, что позволяет строителям правильно рассчитать выводы проводов»*.

**The reason is the whole argument: the builder is setting out a cable stub-out, and the stub-out is at the centre.** An edge dimension makes the installer derive the centre from a device width they may not have yet.

- **A point not on a wall — a floor or ceiling socket — carries TWO dimensions, to the nearest walls, still to its centre.**
- **Height tags may be moved independently of the element they annotate**, to stop them colliding with other dimensions. Annotation placement is a separate concern from element position — which is exactly the failure mode the research report named for hand-rolled sheet generation (*«dimension chains collide on dense MEP plans»*).

### ⚠️⚠️ A centred fixture is dimensioned `1/2`, not in millimetres

**The single most useful convention found in this material.** Where a fitting is to sit at a room's exact centre, RemPlanner prints the value **`1/2`** instead of numeric dimensions, *«указывая строителям на то, что светильник должен быть смонтирован ровно по центру комнаты, независимо от любого расхождения в размерах»*. **Rectangular rooms only** — the mechanic is stated not to work otherwise.

**Why this matters to this project specifically, and it is not a stylistic preference:**

- `00_Master/Geometry_Variance_Study.md` measured **−45 to +30 mm** deltas across three surveyed flats of *this very layout* against the developer's plan.
- Every model dimension here is **nominal ±50 mm** (`project_decisions.md`).
- **→ An absolute millimetre dimension to a centred fixture is therefore wrong on site by construction.** A proportional one cannot be. **The notation converts a guaranteed site argument into a non-issue.**

**A relative dimension is a general instrument, not a one-off trick**: anywhere the *intent* is "centred", "equally spaced" or "symmetrical", the intent survives as-built variance and a number does not.

> [!WARNING]
> **⚠️ Two things are unresolved and both should be settled before adopting it.**
> 1. **Whether `1/2` is an established Russian drafting convention or a RemPlanner invention.** Not stated in the source. **It decides whether a Belarusian installer will read it** — if conventional, they will; if a vendor's own, they may not, and an unread convention is worse than a wrong number.
> 2. **Whether our own DXF/SVG pipeline can express a proportional dimension at all**, or whether it needs Bonsai's annotation subsystem. Untested, and it interacts with the open Bonsai-headless question.

### The datum, which is still ours to decide

**Not from these sources — carried here so the decision lives in one place.** Per the research and §E of the gap analysis: **MEP dimensions must reference bare structural corners, not the finished plaster face** (otherwise a 15 mm plaster layer shifts a plumbing rough-in off-centre from the vanity it was set out to), and **FFL ±0.000 must be anchored to the bare slab top**, because back-box heights, door rough openings and drain slopes all derive from it.

**→ This belongs in `.agents/skills/residential-bim-geometry-rules/` and in `12_Engineering_and_Systems/analysis/Fixture_Stubout_Coordinates.md`, and it should be written before `cap3` produces dimensions.** Still open.

### A third-party tolerance figure, for comparison only

Дизайнер Дмитрий К states his working tolerance as **±1–2 cm** against his own site measurements (`YT_TJVXUCKQ1UU`).

⚠️ **Do not adopt it.** It is *tighter* than our ±50 mm for a reason that does not transfer: **he is modelling a flat that exists and that he has measured; this flat is not built yet** (`tools/cad/PROVISIONAL_MODEL_POLICY.md`: *"the current model is a planning baseline, not an as-built survey"*). Different datum, different meaning.

---

## 2. Element taxonomy

### ⚠️ «Вывод провода» is not a socket

**A distinct element type** (`YT_OTBw7bCrv-o`): a cable brought out of the wall where a load connects directly, with no socket. **Named cases: all kinds of подсветка, wall luminaires, and appliances with no plug — air conditioners, ovens.**

**Corroborated by practice, not only by the tool** — Дизайнер Дмитрий К uses выводы for exactly these on both his flats (`YT_DI5GAV64mnU`, `YT_F0rXrbPDPf4`): towel rails, mirror lighting, concealed lighting, air conditioners, and lighting inside a wardrobe.

**→ Consequences for us.** A вывод is installed differently, priced differently, and **cannot be counted in the same BOM line as a socket.** Our model's electrical elements do not distinguish it. It needs its own `resource_role`.

### An element property can render differently per sheet

A socket group can carry a **`vertical` status that changes how it is drawn on the развёртки and in 3D while leaving the plan unchanged** — *«на чертежах при этом ничего не изменится»* (`YT_OTBw7bCrv-o`).

**→ Representation is a function of (element, sheet type), not of element alone.** A data-model insight for our own sheet pipeline, and it generalises well beyond this one property.

### Grouping is a stored relation, not proximity

In RemPlanner, two already-placed single sockets **will not merge** when moved together; one must be deleted and re-placed. The mechanic itself is irrelevant to us — **what it shows is that grouping is a modelled relation between elements rather than a consequence of their positions.** If our model ever needs socket groups (it will, for the common frames on a sheet), **the relation has to be stored, not computed from distance.**

### Per-element annotation is a required field, not a nicety

**Three independent statements in one round.** RemPlanner allows a free-text comment on an individual fitting; Дизайнер Дмитрий К annotates every socket with what it serves (*«я указал, к чему относится соответствующие розетки»*); and he attaches comments to plumbing elements too. **→ A services element needs a `purpose` field.**

---

## 3. Sheet-level conventions

### A services sheet has two audiences and therefore two configurations

**The reviewer needs the furniture; the installer does not.** Stated three times, in three ways:

- RemPlanner gives each services sheet its own visibility settings — furniture can be shown on the socket plan, height tags can be hidden.
- Дизайнер Дмитрий К reads the socket plan **with the furniture layer overlaid**, because *«розетка… в привязке к расположению мебели… чтобы нам было проще ориентироваться»* — a socket position is only meaningful against the object it serves.
- And he **switches the furniture layer off for the issued version**: *«при создании заключительной версии этих чертежей, для того чтобы мебель не мешала, её можно будет отключить»*.

**→ Working view ≠ issued sheet. The same geometry, two layer states.** Our pipeline currently has one.

### A sheet may legitimately be blank, and the album should say so

Both of Дмитрий's walkthroughs carry a **near-empty демонтажный план** — there is no перепланировка, so nothing is notated beyond old radiators — and in both he **explains why rather than dropping the sheet.** Deliverable-set discipline: an absent sheet is ambiguous, a blank sheet with a reason is not.

### The documentation is designed to be taught, not merely handed over

*«Я специально это подробно прокомментировал, чтобы научить своего заказчика разбираться в предложенной мной документации»* (`YT_F0rXrbPDPf4`). **Review happens on a live model link that he narrates, not on the PDF** — because narrating is faster than annotating (*«это быстрее, чем комментировать в печатном виде»*) — and the printable album is generated separately. The model is corrected live and the link reissued.

**Compare our own `_Drawings/review/` convention** (a single overwritten drawing, git holding the previous state). Same underlying assumption — the artefact is expected to change — reached independently.

### Review affordances worth reproducing

His 3D review view can **toggle ceiling lighting, toggle the display of sockets, and hide all furniture to see socket positions alone**, and switch развёртки between 2D and 3D. **Of these, "hide furniture and show only the services" is the one worth having**, because it is the installer's view and it is the one that exposes an orphaned point.

### ⚠️ A scope boundary, stated plainly

*«Эти строительные планы меня не интересуют, дизайнер их не отрабатывают»* — **the construction/строительные plans are not the designer's deliverable.** Useful when arguing about which of our 16 sheets are genuinely in scope for a self-managed project with no designer engaged.

---

## 4. Two tools, split by what each is good at

**The clearest mechanism in this material** (`YT_TJVXUCKQ1UU`), and it is a *pattern*, not a product recommendation:

1. **The accurate tool builds the model from survey dimensions.**
2. **Its plan is exported as a raster and used as an underlay (подложка) in the fast tool.**
3. **The fast tool's only claimed value is its catalogue** — furniture, textures, materials all to hand — so concept variants come out fast and *«быстрее принять принципиальное решение по дизайну»*.
4. **Precise rework goes back to the accurate tool.**

**The load-bearing rationale**: *«с нуля начертить точную модель в планоплане… почти нереально. А вот по хорошей качественной подложке в размерах можно сделать хорошую, точную модель»* — **accuracy is imported via the underlay rather than authored where the content lives.** He rebuilds the same model twice on purpose and says the time is worth it.

⚠️ **Open, and it matters to us**: he does not say whether the exported plan raster carries a scale reference. **Standing rule 9 requires a scale independent of the thing being measured**, so an underlay exported without one would fail our own discipline.

### ⚠️⚠️ What a planning model must be accurate *about*

**Dimensional accuracy is required. Visual identity is not.**

- **Hand-model anything absent from the catalogue AND size-critical.** His three examples are all objects **already owned rather than chosen**: the client's rowing machine, an existing dishwasher migrating from the old flat, an existing door that stays.
- **The rule with its reason**: *«только каталожных моделей или какого-нибудь кубика вместо тренажёра — это будет некрасиво, ненаглядно»* — **a placeholder box defeats the model's purpose, because the purpose is legibility.** And the tolerance he accepts: *«пускай он чуть-чуть отличается… но по размерам, по габаритам он практически идеально точный»*.

> **This converges with the gap analysis from the opposite direction.** That document concluded, from cost, that *"the model's job is not to be dimensionally exact; it is to hold quantities stable enough that a substitution re-prices correctly."* This source concludes, from legibility, **get the size right and leave the identity swappable.** Two independent arguments landing on the same split — and it is the same `resource_role` / `product_id` split the BOM already uses.

---

## 5. Colour at concept stage

**Stated twice, addressed to the clients** (`YT_YEpfNcwwGoU`): *«сейчас мы не разрабатываем цветовое решение интерьера. Все цвета, все контрасты сделаны только для того, чтобы облегчить восприятие планировочной концепции»* — and again of the sketch renders, *«условные цвета… сделаны просто для улучшения восприятия»*. The underlying claim: **legibility is achieved through detail and contrast**, and 3D is what makes a layout comprehensible at all.

> [!IMPORTANT]
> **⚠️ This argues against our current convention.** `Planning_Project_Deliverable_Set.md` records our 3D as *"3D массинг в том же сером стиле"* — we resolved the tension between honest massing and photoreal renders by going grey. **His answer is a third option: use colour and contrast deliberately at concept stage BECAUSE they aid comprehension, and neutralise the misreading risk with an explicit disclaimer.**
>
> **Grey massing avoids the misreading by discarding the legibility that colour buys.** Worth a deliberate decision rather than an inherited default — and cheap to test, since it is a render style rather than a model change.

---

## 6. Getting a dimensioned raster into geometry

**From an English-language batch on AI-agent modelling — triage in [`_Inbox/planning/ai_agent_modelling_sources_triage_20260911.md`](../_Inbox/planning/ai_agent_modelling_sources_triage_20260911.md).** These bear on the open `v0` task: `project_decisions.md` records that **`v0` has no geometry and it blocks layout selection**, with the route being reconstruction from the printed dimension strings over the registered raster.

### ⚠️⚠️ A scaled raster is for orientation, not measurement — type the dimensions, don't click the pixels

Justin Geis (TheSketchUpEssentials), stated plainly: *"If you're trying to model this building exactly, you shouldn't be coming in here and using visuals in order to figure out where this is going to go… you actually need to model using the dimensions if you want this to be exact. If you're just trying to get it close enough, it doesn't really matter."*

**→ Independent corroboration of the route this project already chose for `v0`.** Aaron Dietzen (Trimble SketchUp) gives the mechanical reason: a raster *"is literally a bunch of dots… that could be scaled to any size"* and **nothing in it can be snapped to** — *"it doesn't know that this is an end point."*

### ⚠️⚠️ Two-point scale verification — register on one printed dimension, verify on a second

**A check we do not currently have, and it is cheap.** Scale off one known printed dimension, preferably a long one; **then measure a different feature elsewhere in the drawing and compare it against its own printed value.** Geis: *"And I always want to check… I like to draw a line somewhere else."* His honest verdict on the residual: *"that's about as close as you're going to get by scaling a document like this."*

**This is not chain closure.** Chain closure asserts that a run of dimensions sums to a known whole. This asserts the **registration itself** against a printed figure that played no part in establishing it — the same independence principle as `tools/layout/vector_extent_oracle.py`. **Add it to the `v0` reconstruction procedure before the hand work starts.**

### ⚠️ The ink has width, and the width is an error term

Dietzen, tracing a wall off a raster: *"I could draw an edge from about the middle of this black line to about the middle of this black line… that's probably around 5½ inches. The line itself is maybe an eighth or a quarter inch thick. So you need to take all this with a grain of salt."*

**→ Before reading a thickness off a raster, decide which part of the drawn line you are measuring to — centre, inner face or outer face — and carry the line's own thickness as an error bar.** `Evidence_Reading_Discipline.md` requires identifying the two elements a dimension's extension lines terminate on; **this adds that the terminating element itself has thickness.**

### The oracle principle, stated from the GUI side

Dietzen: *"It doesn't matter how good the information you get, there's always a possibility that there's a difference between what's in the model and the actual dimension it's supposed to represent. So I always recommend double-checking against printed dimensions of some sort."*

**That is exactly why `vector_extent_oracle.py` exists** — the repo learned that asserting the DXF against `wall_blocks.csv` only proves two hand-edited files agree. **Corroboration of the hardest-won lesson in the geometry work, from someone who reached it by hand.**

**And a weaker note worth keeping**: a *vector* CAD import normally leaves non-intersecting near-misses — *"a couple spots where for whatever reason it didn't intersect correctly… a little bit of cleanup"* — which in a GUI are found by eye. Our 400 mm near-miss band finds them automatically.

## 7. Agents that generate building geometry

> [!WARNING]
> **⚠️⚠️ AN AGENT GENERATING BUILDING GEOMETRY SILENTLY INVENTS THE VALUES YOU DID NOT SPECIFY.**
>
> Trimble's own channel, testing the Claude↔SketchUp adapter with a deliberately vague prompt, got **5-inch wall thickness, a 9-ft ceiling and a "standard" 36×80-in door** — none of it asked for — *"based on its knowledge of construction"*, plus **placeholder furniture** as extruded rectangles unless told not to.
>
> **This is the failure class this project already built apparatus to refuse.** Our walls are 200/250 mm masonry with a **70 mm insulation layer taken from the drawing, not from a heuristic** — `tools/layout/place_insulation.py` exists because *"a flat-centroid rule gets M6b wrong"*, and **M6b is deliberately left unsettled rather than guessed.**
>
> **→ The rule: require an agent to enumerate every value it supplied that the prompt did not, and treat each as a defect to be resolved from evidence rather than a default to be accepted.** The adapter's mitigating behaviour is that it does report its assumptions — so the requirement is satisfiable, not merely aspirational.

**On the architecture, honestly assessed**: the adapter is a **file generator, not a live modeller** — *"there's not a direct live connection… It won't go in and edit it"* — each change emitting a new file. **That is what this project's pipeline already does (spec → generated model), except ours is deterministic, patch-based, version-controlled and gated.** On reproducibility, diffability and gating the adapter is behind; on convenience for one-off geometry it is ahead. Its output is at least structured — named components, triangulated but quad-ready, not the *"212 different diagonal angle cuts"* other AI modellers are said to produce.

### Context management for a large drawing set

Tim Fairley demonstrates the naive paths failing on camera — a ~10 MB drawing set that will not upload to chat, the same failure through a project/RAG upload, and a folder-based agent using *"around 30 times the number of tokens"* and answering less accurately. His name for the cause is **context rot**: *"the more information we give AI, the less likely it is to answer accurately."*

His fix is to **summarise each drawing into a row of a structured store and query that instead of the drawings**, with the clearest analogy in either batch: *"it's like giving someone a set of 30 or 100 drawings and saying 'what is the height of the retaining wall?' versus giving someone the retaining wall drawing and telling them this is the height."*

**⚠️ This project already does this and more strictly — `data/canonical/*.csv` IS the condensed queryable store, and the drawings are generated from it rather than queried.** Recorded as validation of the architecture rather than as instruction. The incidental practical notes do transfer: **a spreadsheet is a poor store because the whole sheet lands in context**, where a queried database does not.

⚠️ **Every model-capability verdict in that batch was deliberately discarded** — dated, vendor-adjacent, and stale within months. The evaluation methods and the cautionary rule transfer; the scores do not.

## Sources

All Russian, all Moscow or a Russian vendor. **Round 1 of the design-toolchain group, 2026-09-08.**

| Source note | Practitioner | What it carries here |
| :--- | :--- | :--- |
| [`YT_OTBw7bCrv-o`](../_Sources/YT_OTBw7bCrv-o_remplanner_lesson4_electrics_lighting.md) | RemPlanner (vendor; narrator unnamed) | Dimensioning to centre, the `1/2` notation, вывод as an element type, per-sheet representation |
| [`YT_DI5GAV64mnU`](../_Sources/YT_DI5GAV64mnU_kdmitry_technical_project_remplanner_festivalnaya.md) | Дизайнер Дмитрий К | Staged workflow, socket derivation, furniture-overlay reading, blank-sheet discipline |
| [`YT_F0rXrbPDPf4`](../_Sources/YT_F0rXrbPDPf4_kdmitry_technical_project_remplanner_review.md) | Дизайнер Дмитрий К | The 18-tab sheet set, switch grouping, the finish-scheme-as-costing-input link, scope boundary |
| [`YT_TJVXUCKQ1UU`](../_Sources/YT_TJVXUCKQ1UU_kdmitry_planoplan_sketchup_together.md) | Дизайнер Дмитрий К | The two-tool split, the underlay, what a planning model must be accurate about |
| [`YT_YEpfNcwwGoU`](../_Sources/YT_YEpfNcwwGoU_kdmitry_concept_2room_planoplan_rationale.md) | Дизайнер Дмитрий К | Conventional colour at concept stage; sketch renders as a stage-1 output |
| [`YT_FRKr9X3AFfY`](../_Sources/YT_FRKr9X3AFfY_kdmitry_doors_partitions_planning.md) | Дизайнер Дмитрий К | Door casings constraining partition position; doors modelled open and closed, trim as a later layer |

| [`YT_f0EU_xbavEA`](../_Sources/YT_f0EU_xbavEA_sketchupessentials_import_scale_reference_images.md) | Justin Geis, TheSketchUpEssentials | **Two-point scale verification**; a scaled raster is orientation, not measurement |
| [`YT_9tfvs3XW5qQ`](../_Sources/YT_9tfvs3XW5qQ_trimble_2d_floorplans_to_3d_walls.md) | Aaron Dietzen, Trimble SketchUp | The ink's width as an error term; the oracle principle from the GUI side |
| [`YT_HOjQiiHJ714`](../_Sources/YT_HOjQiiHJ714_trimble_how_good_is_claude_at_modeling.md) | Aaron Dietzen, Trimble SketchUp | An agent silently invents unspecified construction values; file-generator architecture |
| [`YT_3tAYEJTyUFY`](../_Sources/YT_3tAYEJTyUFY_fairley_ai_read_construction_drawings.md) | Tim Fairley | Context rot, and condensing drawings into a queryable store |

**§6–§7 come from a second batch, English-language and US/UK-market, triaged 2026-09-11.** No regulatory claim is made by any of them.

⚠️ **All six transcripts are auto-generated captions on software subject matter, and the ASR is measurably worse than this vault's usual sources** («Rimliner», «канузла», «отвёртки стен» for развёртки, and one video with no punctuation at all). **Every figure quoted on this page was heard once and is a candidate, not a confirmed number.** Full per-source caveats are in the notes.

## Open items

1. **Is `1/2` an established convention or a vendor's own?** Decides whether it can be issued to an installer. **Highest-value question from Round 1.**
2. ✅ **CLOSED 2026-09-11 — "can our DXF/SVG pipeline express a proportional dimension?" No, and neither can anyone else's.** Gemini's geometry report ([review](../_Inbox/planning/deep_research_review_geometry_20260911.md)) establishes that **in DXF a dimension is a static entity with definition points fixed in group codes 10/11/13/14, and a `1/2` or `EQ` string is an arbitrary text override in group code 1 that nothing computes from** — change the geometry and the override goes stale. Autodesk's parametric constraint networks (`AcDbAssocNetwork`) are proprietary and unsupported by `ezdxf`. **In IFC, dimensions are `IfcAnnotation`/`IfcTextLiteral` presentation, and the schema has no constraint solver.** → **The `1/2` notation is a presentation convention, full stop** — still worth adopting for the reason recorded in §1 (it survives as-built variance where an absolute figure cannot), but it is **a string we draw, not a relation anything solves.** Bonsai's annotation subsystem is not needed for this.
3. **The datum decision (§1) is still unmade**, and §E says it must precede `cap3`.
4. ✅ **CLOSED 2026-09-11 — "does the exported-underlay method preserve a scale reference?" It does not, and that turns out not to matter.** §6 answers it: a raster carries no geometry and nothing to snap to, so practitioners register it against one known printed dimension, **verify on a second independent one**, and then model from the printed dimension strings rather than from the pixels. **The underlay is orientation; the dimensions are the measurement.** Standing rule 9 is satisfied by the printed strings, not by the raster.
5. **Grey massing versus disclaimed conventional colour** — an owner decision.
6. ⚠️ **Add two-point scale verification (§6) to the `v0` reconstruction procedure BEFORE the hand work starts.** The only registration check in either batch that this project does not already have.
7. ✅ **CLOSED 2026-09-11 — NO. Do not adopt `IfcRelConnectsPathElements`.** The relationship is **semantically passive**: downstream tools (Solibri, BIMcollab, Navisworks, **Blender/Bonsai**) do not trim geometry from relationship entities on import — they expect explicit `IfcExtrudedAreaSolid`/`IfcFacetedBrep`, so a file annotating a junction while shipping overlapping volumes simply displays a clash. **Retain the corner ledger.** ⚠️ Its real limits, worth knowing: the `solid = clear + owned corners` formula presumes rectangular prisms and breaks at oblique angles; *thicker-then-longer* is indeterminate on ties at T/X junctions; and it cannot arbitrate multi-layer assemblies. **If non-orthogonal partitions ever appear, the fix is 2D planar clipping in Shapely/GEOS — buffer centrelines, partition along angular bisectors, allocate cells, extrude — not the IFC relationship.** See the [review](../_Inbox/planning/deep_research_review_geometry_20260911.md). *(Original question:* should `wall_corners.csv` become `IfcRelConnectsPathElements`?*)*
8. **Should our deliverable set gain an A/C sheet?** Both of Дмитрий's projects ship a план кондиционеров; `grep "кондиционер"` returns 0 across our own sheet set and roadmap. See [`Planning_Project_Deliverable_Set.md`](Planning_Project_Deliverable_Set.md).
