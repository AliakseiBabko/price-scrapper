# Toolchain gap analysis — what we have, what is missing, what to add

**Created 2026-09-08.** Answers the owner's question: given the Gemini research, what does this repo already have, what is genuinely missing, and do we need more tools — or more of Blender/Bonsai, which we already run?

**Inputs**: the [research report](../../_Archive/processed_sources/20260908_gemini_research_3d_budgeting_toolchain.md) and its [review](deep_research_review_20260908.md); plus a direct inspection of `tools/`, `data/canonical/`, `00_Master/Sheet_Production_Roadmap.md` and `00_Master/Planning_Project_Deliverable_Set.md` done today rather than recalled.

---

## The headline

> **⚠️⚠️ Most of what looks missing is not missing software. It is (a) data the model does not carry yet, and (b) capability sitting unused inside Bonsai, which is already installed.**
>
> **Exactly one genuinely absent tool matters: a cost engine joining quantities to prices. Verified today — nothing in `tools/ifc/`, `tools/layout/` or `tools/drawings/` touches a price except a PoC and the gallery builder.**

---

## A. What we have (verified 2026-09-08, not recalled)

| Layer | State |
| :--- | :--- |
| **Canonical data** | Wall runs, faces, openings and spans, corner ownership ledger, room schedules, per-room internal rollouts, plumbing anchors, existing electrics, wall materials, dimensional tolerance |
| **Model** | IFC seed built programmatically with IfcOpenShell — 18 walls, 8 spaces, 11 openings, 13 electrical, 3 plumbing, 7 lights |
| **Variants** | Patch files against a base; `make_variant.py` / `build_variant.py` / `compare_variants.py` — one command to build, and a programmatic diff |
| **Validation that gates** | `check_wall_junctions.py`, `build_wall_corners.py`, `check_room_rollout.py`, `validate_canonical.py`, `audit_model_quality.py`, `verify_qto_gate.py` (wall-face boundary enrichment for the demonstrator conventions) |
| **Quantities — partial** | **`calculate_wall_finishes.py` already computes host-wall finish quantities and emits wall-elevation SVGs**, reads an optional finish schedule, reports the source of every dimension, and leaves room-side finishes unassigned rather than guessing |
| **Drawings** | 4 A3 sheets generate from the IFC (architectural / floor plan / electrical-lighting / plumbing) via SVG→PDF with a per-sheet manifest and **symbol-placement validation**; `export_variant_dxf.py` writes phase layers `A-WALL-EXIST/DEMO/NEW` |
| **3D** | Portable **Blender 5.2** + **Bonsai 0.8.6-alpha260801**; `build_apartment_demo.py` builds a scene from the IFC, sets **per-scenario lighting** and renders PNGs headlessly on **EEVEE** |
| **Prices** | `data/scraper.db` + `currency_converter.py` with daily / trailing-N-month / calendar-year bases, and rate backfill |
| **Agent boundary** | `tools/mcp/renovation_mcp.py` — allowlisted JSON-lines, no arbitrary shell, code, network or writes |
| **Targets** | 16-sheet album (`Planning_Project_Deliverable_Set.md`) and an 11-capability roadmap `cap0`–`cap10` |

**That is a lot, and the report engaged with it rather than proposing it again.** Its gap table's "open-source path" column describes, almost line for line, what is already built.

---

## B. What is missing — three different kinds, and conflating them is the trap

### Kind 1 — DATA the model does not carry. **This is the actual blocker.**

The roadmap already says it: *«the gap is not "we have no drawing engine". It is: the model carries no phase, no finishes, no real furniture, and no circuits — and the sheets that exist are drawn from heuristics rather than decisions.»* **The report independently agrees, and adds nothing that changes it.**

| Missing data | Roadmap cap | Consequence today |
| :--- | :--- | :--- |
| Element **phase** (existing / demolished / new) | **cap2 — highest leverage** | The DXF has the layers; the model has no phase to put in them |
| **Finish schedule** | cap5 | `Finishes_and_Furniture_Data_Model.md` designs it (`products.jsonl` + placements + per-room schedule) — **designed, unpopulated** |
| **Furniture and appliances as objects** | cap4 | Furniture sheet is "producible" but from nothing real |
| **Circuits and switch grouping** | cap8 | Lighting and socket sheets need daily scenarios **as data, not prose** (cap6) |
| **Setting-out dimensions** | cap3 | See §E — the report changes the convention this must use |
| **`v0` geometry** | — | The developer's own layout exists only as a dimensioned image, so there is no like-for-like variant comparison |
| **Approved control dimension** | cap0 | **Blocks 4 of the 16 sheets on its own** (`PROVISIONAL_MODEL_POLICY.md`) |

**Sheet-set arithmetic as it stands: 4 producible-but-gated, 1 needs the schedule layer, 5 not modelled at all, 5 are 3D massing needing only an output style.**

### Kind 2 — the one genuinely absent TOOL: a cost engine

**Verified**: `grep` across `tools/ifc/`, `tools/layout/`, `tools/drawings/` finds price references only in `poc_renovation.py` and `build_gallery.py`. **There is no quantity→price join anywhere.**

**And the report hands us the design, which is the most valuable thing in it:**

- **A `CostDeltaReport` JSON Schema** — per line `base_qty` / `candidate_qty` / `delta_qty`, split into labour and material unit rates and totals, plus a summary triple.
- **⚠️ The cascading-task rule, which is the part that makes it honest.** A wall move is **not** `(L_B − L_A) × wallRate`. Moving a 100 mm partition cascades into: wall structure (+m²); **finishes on BOTH faces** — plaster → primer → putty → paint (+2 × m²); skirting and cornice (+lin m); flooring infill or deduction (+m²); ceiling junction perimeter (+lin m). **Its named failure mode is precisely a delta script that misses these.**
- **A classification verdict**: Uniclass/OmniClass is over-engineering at one-flat scale and **Belarusian suppliers and trades do not consume the codes**. Use a **flat two-tier trade-keyed taxonomy** — `TIL-01:R04:Paving_600x600`, i.e. `[Trade]-[Task]:[Room]:[Resource]` — which maps directly onto SQLite/CSV and onto `IfcPropertySet` without ontology work.
- **A pricing basis**: **НРР is unusable by a private owner.** So the rate source is market quotes — which makes `data/scraper.db` + the FX converter **the primary instrument, not a supplement.**

**What has to be built**: the resource catalogue keyed to that taxonomy, unit rates in BYN normalised through the existing converter, the cascade rules, and the diff. **Nothing about it depends on the drawings.**

> [!IMPORTANT]
> **⚠️⚠️ REQUIREMENT CORRECTION 2026-09-08, from the owner — and it re-orders the whole design.**
>
> The section above was written around **geometric** deltas: a wall moves, quantities change, re-price. **The owner's objection is that in a real renovation the changes that actually happen are not geometric:** a material is discontinued, a contractor drops out, a price moves — **and those dominate a couple of centimetres by a wide margin.** He is right, and the vault's own ±25 mm tolerance plus the −45/+30 mm as-built spread say so.
>
> **→ So the cost engine's primary axis is SUBSTITUTION AND RE-QUOTING. The geometric delta is the secondary axis, not the first.** That changes what has to be built:
>
> | Requirement | Why it follows |
> | :--- | :--- |
> | **Separate a resource's ROLE from its identity** — "the floor tile in room 04" must be re-pointable at a different product without touching the model or the quantities | The commonest real change. A discontinued tile should be a one-line swap that re-prices, not a re-modelling exercise |
> | **Per-quote provenance: source, date, and validity window** | The FX converter already normalises by date; what is missing is *when this rate was quoted and when it expires*. The research gives a **30–45 day** firm-quote norm |
> | **Rate source keyed per TRADE, not per line** | So losing a contractor re-prices that whole trade at once instead of line by line |
> | **Re-quote triggers as data** | The research names three: **quantity drift > 5 %**, latent substrate defects found on opening up, and **owner-caused delay > 14 days** |
> | **Staged commitment** | Price by trade stage (demolition/partitions → rough MEP → screed/plaster → tiling → finishes) and **do not commit Stage 4 rates during Stage 1** |
>
> **⚠️ And this reframes what the model is FOR.** Its job is not to be dimensionally exact — it is to hold **quantities stable enough that a substitution re-prices correctly**. That is a much weaker precision requirement than the earlier framing implied, and it is met by the existing ±25 mm nominal model.

### Kind 3 — capability we already own and do not use: **Bonsai**

**This is the direct answer to "do we need additional parts of Bonsai/Blender?" — no, we need to start using the parts we have.**

Today Blender is used for **viewing** and for one **EEVEE demonstrator render**. Bonsai is installed and essentially idle. What it carries that we are currently hand-rolling or missing:

| Bonsai capability | What we do instead today | Verdict |
| :--- | :--- | :--- |
| **Drawings subsystem** — sheet generation, camera cut planes, annotation, **dimensions**, **dynamic schedules**, CSS-driven hatches, title blocks | Hand-rolled SVG→PDF | **⚠️ Adopt it for the annotated sheets.** The report is explicit that hand-rolling fails exactly here: *«dimension chains collide on dense MEP plans; excessive custom code required to handle text overlaps»* and *«text overflow in schedule tables breaking sheet margins»* |
| **IDS validation** (`ifcopenshell.validate` against a `.ids` ruleset) | Nothing | **Adopt.** The report's gating design makes IDS step 1, ahead of our geometry gate |
| **BCF issue generation** | Validators print to stdout | **Adopt.** Turns a failed rollout-closure check into a reviewable issue with camera coordinates and element GUIDs |
| **Qto / base quantities** | `calculate_wall_finishes.py` (walls only) | **Use for the rest** — `Qto_SpaceBaseQuantities.NetFloorArea` and `.Perimeter` are what the screed, waterproofing, skirting and cornice lines need |
| **Native IFC authoring GUI** | Programmatic only | **Keep programmatic.** Use the GUI only where visual drafting genuinely beats code — the report's own "don't build a drafting GUI" advice cuts both ways |

**⚠️ Its stated limit, and it decides the split**: Bonsai *«requires Blender's graphical interface for practical sheet assembly unless driving headless Python API scripts with rigid layout rules»*. **So: keep our SVG pipeline for the diagrammatic sheets it already produces well, and put Bonsai behind the sheets that need dimension chains, tags and schedules.** Two engines, split by whether the sheet is annotated.

---

## C. Additional tools — a short add / buy / outsource / skip list

### Add (all small, all scoped)

| Add | Why | Cost |
| :--- | :--- | :--- |
| **`rectpack`** (MIT) | 2D nesting **only** for large-format tile (>$60/m²) and sheet goods. The report is clear that percentages remain correct practice for drywall and standard tile | free |
| **A project `.ids` ruleset** | Not a tool — a file. Blocks a commit if an `IfcWall` lacks e.g. `Pset_CostData.TradeCode` | free |
| **CC0 PBR textures** (Poly Haven, AmbientCG) | Only if presentable renders are wanted at all | free |

### ⚠️⚠️ Buy — RETRACTED 2026-09-08, on the owner's challenge

> [!CAUTION]
> **The laser-distance-meter recommendation was wrong, and two of my three stated justifications were false.** Withdrawn.
>
> **The decisive fact, which I had in the repo and did not apply**: `tools/cad/PROVISIONAL_MODEL_POLICY.md` opens with **«The apartment is not built yet, so the current model is a planning baseline, not an as-built survey.»** **There is nothing to measure.** I transferred a recommendation Gemini framed for surveying an *existing* flat onto a building that does not exist yet.
>
> **Checking each claim I made for it:**
>
> | Claim | Verdict |
> | :--- | :--- |
> | «unblocks `cap0`, the control dimension» | ❌ **False.** `cap0` is about whether the **Homestyler DXF's scale** agrees with the **printed dimension strings** — a desk check against the detailed plan. The policy file even orders the sources that way, and puts «future millimetre field measurements» as a **later supersession step, not the gate** |
> | «closes `v0`» | ❌ **False.** `v0` exists only as a **dimensioned image**. The fix is reading its printed dimension strings, or a second Homestyler export. **No field measurement is involved at all** |
> | «produces the обмерочный чертёж sheet» | ✅ **True, but not now.** That sheet genuinely needs measurement — **after handover.** It is a $60 decision deferrable to the day the keys exist |
>
> **And the owner's substantive point is stronger than the recommendation was**: at planning stage, centimetres are dominated by decision churn. **This vault already says so formally** — every model dimension is **nominal ±25 mm** (`project_decisions.md`), and `00_Master/Geometry_Variance_Study.md` measured three as-built comparables of the same layout at **−45 to +30 mm** against the developer plan. **So the building's own variance exceeds what a laser would resolve at this stage.** Precision here buys nothing a tolerance band does not already provide.
>
> **Where centimetres genuinely do bite, every case is a desk check against printed dimensions, not a survey** — the norm's 1.5 m bathroom width «с учётом отделки», an 1800 mm bath fitting a 3.09 m² room, a concealed mixer's 50–70 mm depth *including tile*, and tile module setting-out. **All of that argues the owner's way, not mine.**
>
> **Revised position: buy nothing now. Revisit a laser meter at handover, when it becomes an acceptance-inspection and обмерочный-чертёж tool rather than a planning one.**

### Outsource, one-off, only if wanted

- **A presentable room render — $40–90.** Cheaper than building an asset pipeline, which the report puts on its don't-build list.
- **An accredited design firm section — 350–500 BYN**, *only* if the job ever touches gas, central heating or load-bearing structure. Per № 164 §6 that is also the only track needing a проект at all.

### ⚠️ Skip — and one of these is a change of mind

- **Revit / ArchiCAD / SketchUp seat** — nothing in this scope requires one.
- **⚠️ Speckle.** The report's verdict for a single owner: *«Git + canonical JSON + programmatic SVG diffing is leaner, runs entirely offline, and ties code changes directly to cost-delta reports.»* **We already have that. Do not add a Docker server for visual 3D diffing one person will look at.**
- **A custom drafting GUI, a raster-plan vectoriser, a photogrammetry suite, an internal compliance rule engine** — all four on the report's don't-build list, all four with a cheap manual alternative. **For `v0` the alternative is 1.5–2 h of manual tracing over an orthogonal grid.**

---

## D. What this implies for sequencing

**Two tracks that do not block each other**, which is the useful finding:

1. **The cost track needs no drawings.** Taxonomy → resource catalogue → unit rates through the FX converter → cascade rules → `CostDeltaReport`. It consumes `calculate_wall_finishes.py` output plus Bonsai/IfcOpenShell space quantities. **Start here if a budget number early is the goal** — and the report's calendar-driven build order puts exactly this work inside the one-month permit review window.
2. **The documentation track is blocked on data, then on annotation.** `cap0` (control dimension, needs the laser) → `cap2` (phase, highest leverage) → `cap3`/`cap5`/`cap4` → Bonsai for the annotated sheets.

**⚠️ Corrected**: an earlier version of this section put a laser meter on track 2's critical path. **It is not on any critical path — the flat is not built.** Track 2's real gate is `cap0`, and `cap0` is a **desk check of the DXF's scale against the detailed plan's printed dimension strings.** That costs an afternoon and no money.

**⚠️ And on the owner's reframing, track 1 is the higher priority of the two**, because the changes that actually arrive during a renovation are substitutions and re-quotes rather than geometry — so the engine that absorbs them is worth more than the drawings that describe a layout which is already decided.

---

## E. ⚠️ The one convention change to make now, because retrofitting is expensive

The report's answer to "what does worker-ready require" turns out to be **a datum problem, not a drawing-style problem**:

- **MEP dimensions must reference bare structural corners, not the finished plaster face** — otherwise *«a 15 mm plaster layer will shift a plumbing rough-in off-centre from an intended vanity cabinet»*.
- **FFL ±0.000 must be anchored against the bare slab top** (e.g. −0.080), because back-box heights, door rough openings and drain slopes all derive from it.

**→ That is a change to `.agents/skills/residential-bim-geometry-rules/` and to `12_Engineering_and_Systems/analysis/Fixture_Stubout_Coordinates.md`, and it should be made before `cap3` produces dimensions, not after.** Cheap now; a re-dimensioning exercise later.

## Open items this analysis does not resolve

- **Whether Bonsai 0.8.6-alpha's drawing subsystem is stable enough headless** for our build chain, or whether annotated sheets have to be a GUI step. **Testable in an afternoon and worth testing before committing to it.**
- Whether `verify_qto_gate.py`'s demonstrator conventions generalise to the current model, or whether the Qto path should come from Bonsai instead.
- `validate_layout_data.py` reports **39 pre-existing schema errors** in `data/deliverable_templates/zk-dubravinskiy-full-album.json` (`note` not permitted; `optional` and `full_album` outside their enums). Unrelated to anything above, unchanged on `main`, and worth clearing before that template drives sheet production.

---

## F. The wider question: do we have everything to RUN the project?

**Asked 2026-09-08: a tool for planning, for buying materials, for contacting contractors, for building a budget, and a plan to implement the renovation.**

**Answer: no — we have two of the six, and the four we lack are the execution half.**

| What the owner asked for | State | Verified by |
| :--- | :--- | :--- |
| **Knowledge to decide with** | ✅ **Strong.** ~250 wiki pages from ~830 sources, plus the law as of today | this repo |
| **Planning / layout options** | ✅ **Strong.** IFC model, variant patches, validators, 4 generating sheets | §A above |
| **A budget** | ❌ **Nothing.** No quantity→price join anywhere | grep, §B |
| **Buying materials** | ❌ **Nothing.** `data/catalog/` **does not exist**; the only artefact is `finish_schedule_demo.json`. `Bill_of_Quantities_and_Procurement.md` is knowledge *about* BOQs, not a BOQ | `ls data/` |
| **Contacting / comparing contractors** | ❌ **Knowledge only.** `Contractor_Vetting_and_Selection.md`, `Contract_Practice.md`, `Estimate_and_Contract_Templates.md` exist as reading. **No register, no quote intake, no comparison** | `ls 11_Budget_and_Planning/analysis/` |
| **A plan to implement** | ❌ **Prose only.** `Renovation_Sequence.md` and `Project_Duration_and_Scheduling.md` are text. **No task list, no dependencies, no statutory milestones as data** | those files |

> **⚠️ The shape of the gap: this repo is an excellent knowledge base with a geometry model attached. It is not yet a project-management instrument. And none of what is missing needs new software** — it is CSV/JSON plus Python in exactly the pattern already used for `data/canonical/`.

### ⚠️⚠️ One artefact unblocks all four, and it should be built first

**A bill of materials as data.** It is simultaneously **the shopping list, the budget line list, the quote-comparison key, and the source of each trade's own extract.** Nothing else can be built until it exists, and everything else is a read of it.

**Design, per the research plus the owner's churn requirement:**

```
key            TIL-01:R04:Paving_600x600      # [Trade]-[Task]:[Room]:[Resource]
resource_role  floor_tile_wet_room            # WHAT IT IS FOR - stable
product_id     <catalog ref> | null           # WHAT WAS CHOSEN - swappable
qty, unit      12.4, m2
qty_source     model_measured | datasheet_derived | manual
waste_basis    pct:10 | nested:rectpack | none
rate_material  , rate_labour                  # BYN
rate_source    <contractor|supplier id>       # keyed PER TRADE, so one loss re-prices one trade
quote_date     , quote_valid_until            # the 30-45 day norm
stage          1..5                           # no committing stage 4 rates in stage 1
```

**⚠️ The `resource_role` / `product_id` split is the whole point.** A discontinued tile becomes a one-field change that re-prices automatically — which is the change that actually happens, per the owner's correction in §B.

### Build order

1. ✅ **BOM as data — BUILT 2026-09-08.** `data/procurement/bom.csv` (21 lines: 18 purchasable + 3 trade interfaces, wet rooms only), `quotes.csv`, `README.md` stating the contract, and `tools/procurement/validate_bom.py` as a gate in the repo's existing pattern. **Quantities are deliberately empty with `qty_source: unmeasured`** — rate discovery does not wait for them, and the areas-are-not-evidence rule forbids deriving them from the developer's figures. Failure paths self-tested: bad key reference, bad enum, bad date, and stale-quote detection all fire.
2. **Cost rollup + delta** on top of it: join rates, apply the cascade rules, emit `CostDeltaReport`
3. **Quote intake** — parse contractor PDF/XLSX into lines keyed to the same taxonomy; the research rates agents as reliable at exactly this and unreliable at guessing quantities
4. **Schedule as data** — tasks, dependencies, the statutory milestones (1-month permit review, 30-day commission notice) and the **Mon–Fri 09:00–19:00** noise window, which is a hard calendar constraint
5. **Per-trade packs** — the "explicit details for the workers" requirement: one extract per trade from the BOM plus the relevant sheets

**The documentation track (`cap2` phase → `cap3`/`cap4`/`cap5` → Bonsai annotation) continues in parallel but second**, since the layout is largely decided and the churn is in materials and people.

### Does this need more research?

**Mostly no — what remains is retrieval and building, not research.** Three narrow questions are genuinely external and worth one short ask:

1. **Do private Belarusian contractors expect a смета in a recognised form** (С-29, КБ-2в) even when НРР does not apply? **Decides what the BOM must be able to export**, which is a schema question.
2. **Contract clauses for an owner engaging individual trades directly** in Belarus — BYN settlement with currency pegging (Civil Code art. 298, already cited), staged acceptance per trade, the re-quote triggers.
3. **Material lead times and distributor structure in Minsk** — what must be ordered how far ahead. **This is a schedule input**, and nothing in the vault has it.

**Everything else — the taxonomy, the cascade logic, the delta schema, the QTO split, the nesting thresholds — the report already answered. Those are build tasks now.**

---

## G. The design side — the chain the owner described, mapped (2026-09-08)

**His chain**: capture what exists → show what others did with the same layout → suggest options against requirements → *connect the dots*, deriving the electrics and plumbing each option implies. Plus 2D for printout and 3D for visualisation.

**Verified against the repo, not recalled.** The inputs are in much better shape than the outputs.

### Step 1 — capture what exists ✅ **have the containers; he is filling them now**

`plumbing_anchors.csv` (3 rows) · `service_outlets.csv` (8) · `electrical_existing.csv` (11) · `device_counts_per_wall.csv` (50, with an explicit `i_drew_… / YOUR_…` column pair for owner correction) · `internal_wall_faces.csv` · `room_rollouts.csv` · `wall_openings.csv`.

**No gap. This is the right first step and it is the input everything downstream needs** — including the BOM quantities.

### Step 2 — show what others did with this layout 🟡 **corpus exists, nothing presents it**

- ✅ **`data/layout_cases/*.json` — 5 precedent cases in a genuinely useful schema**: `problems` / `moves` / `tradeoffs` / `outcome` / `rules_derived`. So each case records the problem faced, the move made, and what it cost. One (`zemskov-odintsovo-69m2`) is a 69 m² flat — this flat's own size.
- ✅ **`_Survey/` — three flats of the SAME layout**, 30 photographs, positioning plans, indexed by `photo_positions.csv`, with `Geometry_Variance_Study.md` comparing them dimensionally.
- ❌ **Gap: nothing reads either corpus back as an answer.** There is no "for this layout, here is what three other households did and what it cost them" view.
- ⚠️ **And an honest limit on the ask itself**: the 5 cases are *similar-size* flats, not *identical-layout* ones. Only `_Survey/` has the exact layout — and what it holds is **finished appearance and geometry deltas, not layout reasoning.** So "the exact same layout, what did they do and why" is thin by construction. **The precedent that transfers is the case corpus; the identical-layout evidence is dimensional.** Worth not conflating them.

### Step 3 — suggest options against requirements 🟡 **the checking half is missing, and it is cheap**

- ✅ **`data/layout_rules/rules.jsonl` — 43 machine-readable rules with parameters**, e.g. `corridor.min_clear_width` = 1100 mm `measured_state: before plaster`, each with rationale and `applies_to`.
- ✅ The variant patch mechanism can express an option and diff two.
- ❌ **⚠️ Gap, and it is the cheapest high-value item on the design side: NOTHING CONSUMES `rules.jsonl`.** 43 rules are written as data and no tool checks a variant against them. **A rule checker is a small script over data that already exists**, and it turns 43 pieces of practitioner knowledge into an automatic gate on every option.
- ❌ **Gap: requirements are prose, not data** — `cap6`. So an option cannot be *scored* against the household's actual scenarios, only read against them by eye.
- ❌ **`v0` still has no geometry**, so there is no baseline to compare an option *to*. Per the 2026-09-08 correction this is **manual tracing from the printed dimension strings, roughly 1.5–2 h — not a tool.**

**On machine-GENERATING layouts**: this question was in the research prompt and Gemini's plan dropped it. **I am not going to chase it, and the reason is a judgement rather than an omission**: for one flat with a fixed structural frame, three fixed shafts and a decided thesis, the option space is small enough that generation adds nothing. **The value is in checking and comparing options, which is exactly what `rules.jsonl` + the variant diff already almost do.**

### Step 4 — "connecting the dots" ❌ **the real gap — and it is the SAME gap as the budget**

Deriving, per layout option, the electrical points, circuits, switch groups and plumbing points it implies.

- **`cap6` — daily scenarios as data.** Unbuilt. The roadmap already notes it is *"a decision-capture task, not a coding task"* — the household's routines have to be written down as structured data before a socket can cite one.
- **`cap8` — circuits and switch grouping.** Unbuilt, and **depends on cap6**. The roadmap's own line: *"the value of the lighting sheet is entirely in this grouping; the fixture dots are already printable."*

> **⚠️⚠️ THE INSIGHT WORTH ACTING ON: this derivation is simultaneously a design output and a BOM quantity.** "How many sockets does this layout need" is the same number as `ELE-01`'s quantity, which is priced per point. **So `cap6` + `cap8` pay twice — they unlock the lighting and socket sheets AND they populate the budget lines that are currently `unmeasured`.**
>
> **The design gap and the budget gap are one gap.** That is the strongest argument for doing this next, ahead of anything on the drawing side.

### 2D for printout 🟡 · 3D for visualisation 🟡

Unchanged from §A–§C: 4 sheets generate, DXF carries phase layers, wall elevations come out of `calculate_wall_finishes.py`; **5 of 16 sheets are unmodelled and annotation is where hand-rolled SVG fails, so Bonsai's drawing subsystem is the answer there.** 3D is an EEVEE demonstrator wired to an older provisional model; the step to presentable is materials, lighting and camera work, and **the research's advice stands — outsource a room render at $40–90 rather than building an asset pipeline.**

### So: do we need more tools? **No new software. Three small scripts over data we already hold.**

| # | Tool | Reads | Why this order |
| :-- | :--- | :--- | :--- |
| 1 | **Rule checker** — validate a variant against `rules.jsonl` | data that already exists | **Cheapest, and the rules are already written.** Turns 43 pieces of knowledge into a gate |
| 2 | **Service derivation** (`cap6` → `cap8`) | scenarios (to be captured) + the variant | **Pays twice** — design output *and* BOM quantities |
| 3 | **Precedent view** — render the case corpus and survey against a question | `layout_cases/`, `_Survey/` | Presentation, once there is an option to compare |

**Prerequisite for any meaningful comparison: `v0` geometry.** Manual, ~2 h, no tooling.
