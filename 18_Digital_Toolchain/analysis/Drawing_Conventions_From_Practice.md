# Drawing conventions from practice

**Created 2026-09-08.** What practitioners' own documentation does, and why — collected to settle conventions this project has open rather than to admire other people's software.

This page exists because the vault's room-and-trade taxonomy is a taxonomy **of the renovation**, not of the project's paperwork. Socket heights have a home in `12_Engineering_and_Systems/`; *how a socket is dimensioned* has none, and burying a drawing convention inside a page about wiring loses it. Original routing decision and its reasoning: [`_Inbox/planning/design_toolchain_sources_triage_20260908.md`](../../_Inbox/planning/design_toolchain_sources_triage_20260908.md) §5.

> [!NOTE]
> **Moved 2026-09-13, from `00_Master/` to this folder.** The 2026-09-08 decision put this page in `00_Master/` because that was where the project's own method already lived and the class had no processed sources yet. It now has eleven, with a second batch arriving, and two things settled the move: **`00_Master/` had accumulated four different kinds of document** — the project's own decisions, model status, working discipline, and this general practitioner knowledge — with nothing distinguishing them; and **`00_Master/` is explicitly excluded from `tools/check_page_sizes.py`** (`NUMBERED_FOLDER_RE` skips `00_`), so this page had been growing **ungated** past the 300-line soft target with no fragmentation check. It is now inside the gate.
>
> **The split this folder rests on:** [[18_Digital_Toolchain/Digital_Toolchain_Guide|18_Digital_Toolchain]] holds **general, source-derived** toolchain knowledge; **`00_Master/` keeps this project's own toolchain decisions and status** — `Model_and_Views.md`, `Planning_Project_Deliverable_Set.md`, `Sheet_Production_Roadmap.md`, `Revit_AutoCAD_Integration_Strategy.md`, the `V0_*` pages. **Same relationship `17_Design_and_Ergonomics/` has to `00_Master/Design_Concept.md`** — general practice in the numbered folder, this apartment's own choices in `00_Master/`. **A convention recorded here is a practitioner's; a convention we have *adopted* belongs in `00_Master/project_decisions.md` and in `.agents/skills/residential-bim-geometry-rules/`.**

> [!IMPORTANT]
> **⚠️ Everything here is a named practitioner's practice or a named tool's design decision, never a norm.** Nothing on this page is a Belarusian requirement, nothing here has been checked against one, and no figure here has been verified. **Sources are Russian (Moscow) and one Russian software vendor.** Standing rule 4: nothing from these sources goes to `16_Legal_and_Regulations/`.

## Why this page exists now, and what it is for

Three of this project's open capability items are blocked on **conventions we have not chosen** rather than on code:

| Blocked on | Item |
| :--- | :--- |
| What a dimension is measured **to** | `cap3` setting-out dimensions, plus the datum change in [`toolchain_gap_analysis_20260908.md`](../../_Inbox/planning/toolchain_gap_analysis_20260908.md) §E |
| Whether a cable stub-out is **the same element** as a socket | The model's electrical taxonomy, and `ELE-01`'s BOM line |
| What a derived services plan actually **contains** | `cap6` → `cap8` |

**§E's warning is the reason for the hurry: these are cheap to choose now and expensive to retrofit once `cap3` starts emitting dimensions.**

---

## 1. Dimensioning

### ⚠️⚠️ Three parallel chains, working outward: OPENINGS → ROOMS → OVERALLS, at 400 mm spacing

**The most directly implementable convention found in this material.** Composing a plan's dimensions, the presenter states the order before he starts — *"we're going to do **openings, then rooms, and then we're going to do overalls**"* — and builds three parallel tiers:

| Tier | Contents |
| :--- | :--- |
| **Innermost** | **Openings** — each window and door width, and the wall segments between them |
| **Middle** | **Rooms / spaces** — internal clear dimensions |
| **Outermost** | **Overalls** — the full extent; here one for the outside area and one for the building |

**Row spacing is `400` mm**, typed and repeated for each new tier. Grid lines are then offset a further *"400 or perhaps 500"* to clear the dimension block.

> **→ This is the standard architectural convention, stated with a number, by someone composing it by hand.** ⚠️⚠️ **And it is directly implementable in our own generator**, because `data/canonical/` already holds every wall length, thickness and opening position. **Three chains and a loop.**
>
> ⚠️ **The STRUCTURE transfers; the NUMBERS do not.** 400 mm is one practitioner's working figure **on a 1:50 sheet**, and the same presenter uses 500, 750 and 1000 for annotation lead-outs elsewhere, chosen by eye per drawing. **Treat the offset as a scale-dependent parameter, not a constant** — a dimension block that reads correctly at 1:50 does not at 1:100.
>
> ⚠️ **And note what makes it worth having**: he places every one of these by snapping polyline vertices by hand. **There is no auto-dimension in the tool.** See [[18_Digital_Toolchain/analysis/Model_To_Drawing_Pipeline|Model to Drawing Pipeline]] §4. [source: [[_Sources/YT_VgvPk78IU0U_ifcarchitect_bonsai_2d_drafting|YT_VgvPk78IU0U]]]

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
> 2. ~~**Whether our own DXF/SVG pipeline can express a proportional dimension at all**, or whether it needs Bonsai's annotation subsystem.~~ **⚠️⚠️ ANSWERED 2026-09-13, and the answer is that it needs nothing from Bonsai.** Annotation text in that system is an **SVG document with `{{ }}` placeholders resolved against model data** — the same mechanism drives tags, leaders and title blocks. **A template that can render `{{name}}` can render a literal `1/2`**, and the general principle is the valuable half: **the annotation is DERIVED from the model rather than transcribed beside it.** Template substitution over an SVG is a string operation, and our generator already produces the SVG and already holds the data. See [[18_Digital_Toolchain/analysis/Model_To_Drawing_Pipeline|Model to Drawing Pipeline]] §4b. **⚠️ Point 1 — whether a Belarusian installer will READ `1/2` — remains open and is the one that decides adoption.**

### The datum, which is still ours to decide

**Not from these sources — carried here so the decision lives in one place.** Per the research and §E of the gap analysis: **MEP dimensions must reference bare structural corners, not the finished plaster face** (otherwise a 15 mm plaster layer shifts a plumbing rough-in off-centre from the vanity it was set out to), and **FFL ±0.000 must be anchored to the bare slab top**, because back-box heights, door rough openings and drain slopes all derive from it.

**→ This belongs in `.agents/skills/residential-bim-geometry-rules/` and in `12_Engineering_and_Systems/analysis/Fixture_Stubout_Coordinates.md`, and it should be written before `cap3` produces dimensions.** Still open.

### ⚠️⚠️ …and an agent will silently choose one for you: bottom-left of the wall (Grasshopper Plus Plus, 2026-09-12)

**Testing an agent drawing a plan in AutoCAD from a PDF, a Korean practitioner notices the coordinate origin and calls it out:**

> *«여기 재밌는 게 원점을 여기다 그리더라고요… **이거는 꽤 공통적으로 나옵니다. 벽의 왼쪽 아래를 원점의 중심으로 삼는다.** 이거 굉장히 특이한 발견인 것 같아요.»*
> — **"It puts the origin here. This comes up QUITE COMMONLY. It takes the BOTTOM-LEFT OF THE WALL as the origin."** He then **observes the same placement from a second, different model.**

- **⚠️⚠️ This is the silently-supplied-values rule (§7) applied to THE DATUM — and the datum is the worst thing to have chosen for you, because every other coordinate is measured from it.**
- **→ It does not tell us what OUR datum should be**, which the block above leaves deliberately open and answers on structural grounds (bare structural corners, FFL anchored to the bare slab top). **What it tells us is which convention we will be silently fighting if we choose differently** — and that the fight will be with every generated artefact, not just one.
- **⚠️ Worth stating in `.agents/skills/residential-bim-geometry-rules/` alongside the datum decision itself**: *state the origin explicitly in any generation prompt*, because the alternative is not "no origin" but "an unstated one that two unrelated models both default to." [source: [[_Sources/YT_-FsHQEYldnQ_grasshopperpp_computer_use_autocad|-FsHQEYldnQ]]]

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

### ⚠️⚠️ The plan cut plane sits ~1 m above storey level, and the reason is functional

**Two independent Bonsai practitioners, three years apart, on where a floor plan is cut:**

> *"We're going to create a plan — **not at zero, which is our engine, but at my story, which is that ONE METRE STANDARD HIGH CUT, so it CUTS THE WINDOWS AND THE DOORS**."* — Ifc Architect, who later gives it as *"1 to 1.2 metres high roughly"*
> *"Use as a reference point my story. So it's going to do a cut **I GUESS at 1 m from the floor**."* — Prof Rino

**→ A cut at zero shows a slab; too high misses window sills; too low misses window heads. The plane must pass through both window and door openings, and that is what fixes it.**

- **⚠️ Note the second presenter's hedge — "I guess".** A BIM teacher of ten years does not know the exact height the tool is about to use, **because the UI does not state it.** **A drawing convention with real consequences, applied by a default nobody reads.**
- **→ When this project generates plans, the cut height must be an explicit committed parameter, not a default.** ⚠️ **Contrast the mesh route**, where the cut plane is a box handle dragged by eye and **no height is stated anywhere in the video** — an unstated cut height is an unstated drawing convention. [sources: [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|YT_PNoOyCHa_V0]], [[_Sources/YT_fxpIg-su-00_profrino_first_bim_drawing_bonsai|YT_fxpIg-su-00]], [[_Sources/YT_YYmFMxMV6io_messerschmidt_blender_dimensioned_floor_plan_export|YT_YYmFMxMV6io]]]

### ⚠️ Phase representation, and a reminder that line weights are NATIONAL

**One practitioner's phase convention, stated as personal practice**: **existing = grey**, **demolish = blue or light grey**, **new = red or pink** — *"just to distinguish these elements."* He offers it *"completely metaphorically"*, as a demonstration.

> ⚠️ **Recorded as his, not adopted.** It differs from common European practice, where demolished is often dashed and new solid. **This project carries the same three phases as DXF layers**; the mechanism for generating a phase sheet from one model is in [[18_Digital_Toolchain/analysis/Model_To_Drawing_Pipeline|Model to Drawing Pipeline]] §11.

> [!WARNING]
> **⚠️⚠️ LINE WEIGHT AND SYMBOL CONVENTIONS ARE NATIONAL, and the source of all eight 2026-09-13 additions is a SOUTH AFRICAN architect.** He says so twice — his own line-weight set is *"very South African standardy"*, and he saves a *"South African standard 220 masonry wall."* He also **overrides a convention he knows to be widespread** on personal taste: of the default section arrowheads, *"I know this is standard in a lot of countries, but I just prefer a normal arrow."*
>
> **→ A shipped default is somebody's national convention, and every convention taken from this channel carries an unstated one.** **Standing rule 4 applies: nothing from this source is a Belarusian requirement and none of it routes to `16_Legal_and_Regulations/`.**

### ⚠️⚠️ A fixture's plan symbol is AUTHORED, not derived by cutting it

> *"If I want to see **how the shower actually looks when it's cut**, I can turn on the **plan representation**, so we can see **where the drain is**."*

**A drain does not appear in a section through a shower tray. It appears because the symbol has one.** Each object carries a 2D plan representation distinct from its 3D geometry, rotated into place per instance.

> **→ Our hand-rolled SVG pipeline cannot do this — it can only draw what it can compute from geometry.** Full treatment, with the rest of the model-to-sheet mechanics: [[18_Digital_Toolchain/analysis/Model_To_Drawing_Pipeline|Model to Drawing Pipeline]] §5.

### A services sheet has two audiences and therefore two configurations

**The reviewer needs the furniture; the installer does not.** Stated three times, in three ways:

- RemPlanner gives each services sheet its own visibility settings — furniture can be shown on the socket plan, height tags can be hidden.
- Дизайнер Дмитрий К reads the socket plan **with the furniture layer overlaid**, because *«розетка… в привязке к расположению мебели… чтобы нам было проще ориентироваться»* — a socket position is only meaningful against the object it serves.
- And he **switches the furniture layer off for the issued version**: *«при создании заключительной версии этих чертежей, для того чтобы мебель не мешала, её можно будет отключить»*.

**→ Working view ≠ issued sheet. The same geometry, two layer states.** Our pipeline currently has one.

### ⚠️⚠️ Layer along the seam where responsibility changes hands (Стройплощадка, 2025-03-27)

**A second, independent instance of the rule above — and it generalises it.** An electrical design-and-assembly shop separates **обвязка щита (workshop wiring)** from **подключение (on-site connection)** into distinct layers, for an organisational reason rather than a graphical one: **panels are built in their workshop and connected on site, often by electricians in other cities who ordered the panel remotely.** Toggling shows either what the shop must wire, or what happens on the object. Line-type layers also separate L2, L3 and low-voltage 24 V runs.

> **→ Layer a drawing along the seam where responsibility changes hands. The seam is where errors happen, and a layer toggle makes each party's scope explicit without producing two drawings that can drift apart.**

**⚠️ And the same source shows the mechanism that keeps a schedule honest: the label carries the data.** Terminals carry stickers assigning a number and a group, and the terminal then remembers its marking, article number and function. A purpose-built cable-log sticker is attached to a terminal; **you choose only the conductor, and it inherits everything else from the terminal it is stuck to** — including the connection point. Copying it across terminals **assembles the cable log, which is then generated as a document.**

- **The principle: the annotation object carries the data, and the schedule is GENERATED from the drawing rather than maintained beside it** — which removes the commonest failure in services documentation, a cable log and a panel drawing that disagree because someone updated one.
- **⚠️ This project's direction is the stronger one and it is worth being precise about why.** They attach data to drawing objects and harvest a schedule; **this project generates the drawings FROM `data/canonical/`.** Both eliminate the two-copies problem — **but with the drawing as master there is nothing to check the drawing against, so there can be no equivalent of `check_dxf_closure.py`.** [source: [[_Sources/YT_PVXE79HM0-c_stroyploshchadka_panel_design_toolchain|YT_PVXE79HM0-c]]]

### ⚠️ Three rules for a presentation pass that does not corrupt the drawing (Upstairs, 2026)

**From an architectural-presentation tutorial whose styling recipe is deliberately not routed** — this project's sheets are a working deliverable, not a portfolio piece. **Three workflow rules do transfer, and all three are about keeping a rendered view honest:**

1. **Export the CUT ELEMENTS as their own file.** The walls — everything the section plane cuts — must come out separately from the complete plan, because the cut layer is what carries depth. **A requirement on the EXPORT step, upstream of any styling.**
2. **Preserve scale across the vector-to-raster boundary** — make the raster document the same dimensions and resolution as the source sheet, *"so that you don't change the scale… we want this to be up to scale at the end of the day."* **A presentation pass must not silently destroy the drawing's scale** — the same hazard §6 records from the other direction.
3. **Place LINKED, never embedded** — edit the source, save, and the presentation updates. **A presentation is a VIEW of the drawing, not a copy of it**, which is the single-source principle at the one layer where a copy is most tempting. [source: [[_Sources/YT_YkHGQPfZEgM_upstairs_plan_presentation_technique|YT_YkHGQPfZEgM]]]

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
| [`YT_OTBw7bCrv-o`](../../_Sources/YT_OTBw7bCrv-o_remplanner_lesson4_electrics_lighting.md) | RemPlanner (vendor; narrator unnamed) | Dimensioning to centre, the `1/2` notation, вывод as an element type, per-sheet representation |
| [`YT_DI5GAV64mnU`](../../_Sources/YT_DI5GAV64mnU_kdmitry_technical_project_remplanner_festivalnaya.md) | Дизайнер Дмитрий К | Staged workflow, socket derivation, furniture-overlay reading, blank-sheet discipline |
| [`YT_F0rXrbPDPf4`](../../_Sources/YT_F0rXrbPDPf4_kdmitry_technical_project_remplanner_review.md) | Дизайнер Дмитрий К | The 18-tab sheet set, switch grouping, the finish-scheme-as-costing-input link, scope boundary |
| [`YT_TJVXUCKQ1UU`](../../_Sources/YT_TJVXUCKQ1UU_kdmitry_planoplan_sketchup_together.md) | Дизайнер Дмитрий К | The two-tool split, the underlay, what a planning model must be accurate about |
| [`YT_YEpfNcwwGoU`](../../_Sources/YT_YEpfNcwwGoU_kdmitry_concept_2room_planoplan_rationale.md) | Дизайнер Дмитрий К | Conventional colour at concept stage; sketch renders as a stage-1 output |
| [`YT_FRKr9X3AFfY`](../../_Sources/YT_FRKr9X3AFfY_kdmitry_doors_partitions_planning.md) | Дизайнер Дмитрий К | Door casings constraining partition position; doors modelled open and closed, trim as a later layer |

| [`YT_f0EU_xbavEA`](../../_Sources/YT_f0EU_xbavEA_sketchupessentials_import_scale_reference_images.md) | Justin Geis, TheSketchUpEssentials | **Two-point scale verification**; a scaled raster is orientation, not measurement |
| [`YT_9tfvs3XW5qQ`](../../_Sources/YT_9tfvs3XW5qQ_trimble_2d_floorplans_to_3d_walls.md) | Aaron Dietzen, Trimble SketchUp | The ink's width as an error term; the oracle principle from the GUI side |
| [`YT_HOjQiiHJ714`](../../_Sources/YT_HOjQiiHJ714_trimble_how_good_is_claude_at_modeling.md) | Aaron Dietzen, Trimble SketchUp | An agent silently invents unspecified construction values; file-generator architecture |
| [`YT_3tAYEJTyUFY`](../../_Sources/YT_3tAYEJTyUFY_fairley_ai_read_construction_drawings.md) | Tim Fairley | Context rot, and condensing drawings into a queryable store |

**§6–§7 come from a second batch, English-language and US/UK-market, triaged 2026-09-11.** No regulatory claim is made by any of them.

⚠️ **All six transcripts are auto-generated captions on software subject matter, and the ASR is measurably worse than this vault's usual sources** («Rimliner», «канузла», «отвёртки стен» for развёртки, and one video with no punctuation at all). **Every figure quoted on this page was heard once and is a candidate, not a confirmed number.** Full per-source caveats are in the notes.

## Open items

1. **Is `1/2` an established convention or a vendor's own?** Decides whether it can be issued to an installer. **Highest-value question from Round 1.**
2. ✅ **CLOSED 2026-09-11 — "can our DXF/SVG pipeline express a proportional dimension?" No, and neither can anyone else's.** Gemini's geometry report ([review](../../_Inbox/planning/deep_research_review_geometry_20260911.md)) establishes that **in DXF a dimension is a static entity with definition points fixed in group codes 10/11/13/14, and a `1/2` or `EQ` string is an arbitrary text override in group code 1 that nothing computes from** — change the geometry and the override goes stale. Autodesk's parametric constraint networks (`AcDbAssocNetwork`) are proprietary and unsupported by `ezdxf`. **In IFC, dimensions are `IfcAnnotation`/`IfcTextLiteral` presentation, and the schema has no constraint solver.** → **The `1/2` notation is a presentation convention, full stop** — still worth adopting for the reason recorded in §1 (it survives as-built variance where an absolute figure cannot), but it is **a string we draw, not a relation anything solves.** Bonsai's annotation subsystem is not needed for this.
3. **The datum decision (§1) is still unmade**, and §E says it must precede `cap3`.
4. ✅ **CLOSED 2026-09-11 — "does the exported-underlay method preserve a scale reference?" It does not, and that turns out not to matter.** §6 answers it: a raster carries no geometry and nothing to snap to, so practitioners register it against one known printed dimension, **verify on a second independent one**, and then model from the printed dimension strings rather than from the pixels. **The underlay is orientation; the dimensions are the measurement.** Standing rule 9 is satisfied by the printed strings, not by the raster.
5. **Grey massing versus disclaimed conventional colour** — an owner decision.
6. ⚠️ **Add two-point scale verification (§6) to the `v0` reconstruction procedure BEFORE the hand work starts.** The only registration check in either batch that this project does not already have.
7. ✅ **CLOSED 2026-09-11 — NO. Do not adopt `IfcRelConnectsPathElements`.** The relationship is **semantically passive**: downstream tools (Solibri, BIMcollab, Navisworks, **Blender/Bonsai**) do not trim geometry from relationship entities on import — they expect explicit `IfcExtrudedAreaSolid`/`IfcFacetedBrep`, so a file annotating a junction while shipping overlapping volumes simply displays a clash. **Retain the corner ledger.** ⚠️ Its real limits, worth knowing: the `solid = clear + owned corners` formula presumes rectangular prisms and breaks at oblique angles; *thicker-then-longer* is indeterminate on ties at T/X junctions; and it cannot arbitrate multi-layer assemblies. **If non-orthogonal partitions ever appear, the fix is 2D planar clipping in Shapely/GEOS — buffer centrelines, partition along angular bisectors, allocate cells, extrude — not the IFC relationship.** See the [review](../../_Inbox/planning/deep_research_review_geometry_20260911.md). *(Original question:* should `wall_corners.csv` become `IfcRelConnectsPathElements`?*)*
8. **Should our deliverable set gain an A/C sheet?** Both of Дмитрий's projects ship a план кондиционеров; `grep "кондиционер"` returns 0 across our own sheet set and roadmap. See [`Planning_Project_Deliverable_Set.md`](../../00_Master/Planning_Project_Deliverable_Set.md).

---

**Getting a dimensioned raster into geometry** — scale registration, verification, raster distortion and the ink-width error terms — moved to its own page on 2026-09-13 when this one reached the backstop: [[18_Digital_Toolchain/analysis/Raster_To_Geometry|Raster to Geometry]].
