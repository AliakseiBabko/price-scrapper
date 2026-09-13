# Quantity Take-Off and the Cost Join

Detail page for [[18_Digital_Toolchain/Digital_Toolchain_Guide|Digital Toolchain]].

**How a quantity gets out of a model, and how it becomes a priced line.** General practice from four practitioners and two commercial tools — **not this project's own cost engine**, whose design lives in [`toolchain_gap_analysis_20260908.md`](../../_Inbox/planning/toolchain_gap_analysis_20260908.md) §B.

> [!IMPORTANT]
> **⚠️⚠️ This page exists because the quantity→price join is the one genuinely absent tool in this project's toolchain.** The 2026-09-08 gap analysis verified by grep that **no quantity-to-price join exists anywhere in this repo**, and the 2026-09-13 AI-toolchain round closed with the gap still open. **These sources do not close it either — every tool here derives quantities automatically and prices nothing automatically.** What they supply is *schema thinking*: where a cost attaches, what a cost line carries, and what breaks.
>
> **⚠️ Every price figure in every source here is discarded under standing rule 2** (US 2020/2025, Omsk 2020 — no comparable market or year). **Only mechanisms transfer.**

## 1. Where a cost attaches — the design question

**Cost is not attached per line. It is attached to an entity class, and the choice decides what a price change re-prices.** Quantifier Pro exposes four: **tags, materials, objects, and models.**

| Method | Behaviour | What it is for |
| :--- | :--- | :--- |
| **Object** | A flat cost on a selected object. **Applied to a component, every copy inherits it** | One-offs and repeated identical items |
| **Tag / layer** | Cost on a tag, calculated on one of **four bases: length, area, volume, or weight** | A whole class of member — all studs by length, all siding by area, concrete by volume |
| **Material** | Cost on a named material, **aggregated wherever that material appears in the model** | Finishes — paint, tile, carpet, wallpaper, flooring |

- **⚠️⚠️ Material-keyed cost is a partial implementation of this project's PRIMARY cost requirement.** The owner's correction to the gap analysis states that the cost engine's first axis is **substitution and re-quoting**, not geometric delta: *"the floor tile in room 04"* must be re-pointable at a different product without touching the model. **Because cost attaches to the named material, changing one unit price re-prices every surface carrying it in a single edit.**
  **Partial, because it keys on the material rather than on a ROLE** — so it cannot express two products serving the same role, nor re-point a role at a new product while keeping history. **That gap is exactly where this project's design has to go further than the commercial tool.**
- **⚠️ A gotcha in the length basis, and it is a familiar class of error: the tag method takes the LONGEST AXIS of the group's bounding box.** A group whose longest bounding-box edge is not the member length is mis-measured. **Same hazard `tools/layout/dxf_wall_entities.py` exists to prevent** — that reader was written because two gates each reduced a polyline to its bounding box and a triangle passed both.

### The cost line's fields

**code · description · calculation basis · factor · unit cost · waste % · tax % · comment**

- **⚠️⚠️ WASTE AND TAX ARE FIRST-CLASS FIELDS ON EVERY LINE — and this project's own cost-engine design does not mention waste anywhere.** That is a real omission, surfaced by an outside tool, and it is flagged in the triage note for the owner.
- **The code field is meant to carry your own cost-coding system**, not the tool's. Compatible with the gap analysis's `[Trade]-[Task]:[Room]:[Resource]` taxonomy.
- **Cost data is entered by hand and the tools say so** — *"because this information can vary, this is something that you have to add manually."* **Quantities are derived; prices are not.** That matches this project's own design, where rates come from market quotes through `data/scraper.db` and the FX converter.

[sources: [[_Sources/YT_MZv33G7UE_A_mindsight_quantifier_pro_material_reports|YT_MZv33G7UE_A]], [[_Sources/YT_sSnjQJX4-iY_mastersketchup_quantifier_three_methods|YT_sSnjQJX4-iY]]]

## 2. ⚠️⚠️ Waste is not one number — the sharpest finding on this page

**A commercial tool treats waste as a percentage per cost line** — *"the waste percentage comes in handy when you're calculating materials like studs where you know you're going to have some cut off."* A worked example prices tile at **7% waste**.

**This vault already holds a much better answer for exactly that case.** [[11_Budget_and_Planning/analysis/Bill_of_Quantities_and_Procurement|Bill of Quantities and Procurement]] §5a-quinquies records Vasily_Sanuzel deriving a **cutting plan** from his model — a spreadsheet takes each required piece's length and count and returns both the stock lengths to order **and how to cut each one**:

| Figure | Value |
| :--- | :--- |
| Stock lengths ordered (3 m) | **38** |
| Total ordered | **114 m** |
| Consumed | **~113 m** |
| **Total offcut waste** | **86 cm — under 1%** |

> **→ The synthesis neither source states: WASTE ALLOWANCE IS A FUNCTION OF WHETHER THE MATERIAL NESTS AND WHETHER YOU CONTROL THE CUTTING.**
>
> - **Linear stock you cut yourself** — profiles, studs, skirting, pipe, cable: **nest it and the percentage collapses toward zero.** A flat 7–10% here is money left on the table.
> - **Tile, sheet goods, anything with breakage, edge cuts or pattern matching**: **a percentage is unavoidable** — you cannot nest ceramic the way you nest 3 m profiles.
>
> **So waste belongs in the schema as a per-resource property with a METHOD attached, not as one global rate.**

## 3. What the take-off actually has to carry — a worked schema

**The best-designed data model in this round is an electrical one, and its central decision is a cardinality split.** A drawn line carries **two orthogonal classifications**:

| | **Кабель — the conductor** | **Оболочка — the containment** |
| :--- | :--- | :--- |
| Examples | `3×2.5`, `3×1.5`, `1×6` | гофра, штроба, лоток, траншея, гильза, труба |
| **Cardinality** | **Exactly ONE per line** | **MANY per line, simultaneously** |
| Rendering | Colour per cable group | **Only one displays at a time**, deliberately, since containments overlap |

**The case that proves the cardinality is necessary: a cable runs in гофра for most of its route and passes through a wall inside a гильза. Both are true of the same line at once.**

- **⚠️⚠️ Why this matters for `ELE-01`, which the gap analysis records as unmeasured: the cable length and the containment length are NOT the same number.** A 12 m circuit might be 12 m of cable, 7 m of гофра, 4 m of штроба and 0.4 m of гильза. **A take-off carrying one quantity per line has already lost the containment quantities — which are separately purchased materials and separately paid labour.**
- **Containment entries carry material and size**: `гофра ПВХ 20`, `штроба кирпич 20×20`, `труба металл 25`.
- **A third independent classification: the circuit** («Розетки зал», «Освещение спальня», «ЗУ»).
- **The output is a complete take-off** — per circuit: total length, cable type, **each laying method and its own length**, plus a consolidated materials list, copyable to a spreadsheet.

**⚠️ And the substrate is a rate driver, not a drawing colour.** Wall material — concrete, brick, ГКЛ — is stated to decide *"where sockets and switches go, how the развёртки are read, how runs are routed, and **what works appear in the project**."* **Chasing brick, chasing concrete and fixing to plasterboard are different operations at different rates**, so `штроба кирпич 20×20` is a priced line whose rate depends on `wall_materials.json`.

[sources: [[_Sources/YT_A1HxpHxrvv4_craftelectric_cable_enclosure_schema|YT_A1HxpHxrvv4]], [[_Sources/YT_9-hQsyWSnm4_craftelectric_mooncad_walls_and_scale|YT_9-hQsyWSnm4]]]

## 4. ⚠️⚠️ What a cost model is actually for — three independent arrivals

**None of these sources says a cost model exists to produce a precise final number. All three say it exists to make a decision cheaply.**

1. **It kills a bad option early.** A modeller costing a tiny office he intended to build hit **$5,300 with no siding, no roofing, no interior surfaces and no roof**, concluded it would land near $10,000, and **abandoned the build**. **The estimate was deliberately incomplete and still decisive — precisely because it was already over budget before the expensive parts were added.** → **An estimate incomplete in a known direction is actionable; it only has to be good enough to cross a threshold.**
2. **It makes changes cheap to re-price.** A finisher states it twice, opening and closing: the model exists so that a mid-renovation question or change is answered from it — *«не надо сидеть с бумажками и на калькуляторе каждый раз»* — rather than re-derived on paper each time.
3. **This project's own gap analysis reached the same place**, after the owner's correction: the model's job *"is not to be dimensionally exact — it is to hold quantities stable enough that a substitution re-prices correctly."*

> **→ Precision is not what makes an estimate useful. Re-derivability is.** Three unrelated arrivals — a US modeller, a Russian finisher, and this project's own design — is as strong as convergence gets in this vault.

### Stratify precision by how variable the category actually is

**A finisher's смета has two parts — materials and works — and the materials half has three, with the third deliberately vague:**

| Part | Treatment |
| :--- | :--- |
| **Черновые** (rough) — plaster, profiles, plasterboard | Priced confidently: *«они более-менее одинаково стоят везде»* |
| **Расходники** (consumables) — bits, discs, gloves | **A named line item in its own right**, which most estimates hide inside labour |
| **Чистовые** (finish) | **Greyed out and deliberately approximate** — *«могут очень сильно отличаться»*, because they are a taste-and-tier choice rather than a commodity |

- **→ Pretending to three significant figures on finish materials is false precision.** The client uses that section to size their own budget and choose cheaper or dearer.
- **⚠️ Converges with the gap analysis's own "staged commitment" requirement** — price by trade stage and **do not commit Stage 4 rates during Stage 1** — reached from the opposite direction, by a practitioner explaining why his finish column is grey.
- **Two more practices worth taking**: the works смета **ends with an explicit list of works NOT included** (*«чтобы для клиента не было сюрпризом»*), and a stated **~20% contingency** for непредвиденные расходы, with the reason — you cannot account for everything, and changes get made mid-job.

[sources: [[_Sources/YT_sSnjQJX4-iY_mastersketchup_quantifier_three_methods|YT_sSnjQJX4-iY]], [[_Sources/YT_s0TrXB2WQ2Q_omsk_sketchup_excel_smeta_method|YT_s0TrXB2WQ2Q]]]

## 5. ⚠️⚠️ Three ways a model silently fails to yield the quantity

**From the 2026-09-13 Bonsai/IFC batch. Each is a case where the model looks complete and the schedule is short.**

### A schedule is a traversal of INDIVIDUATED objects — and that is the cheap half

A capability demo produces *"a PDF breaking down piece count, colours, catalogue entries and the shape of each piece"*, and the presenter names the reason it is derivable: *"the way that we are able to understand how many individual pieces make up this model is **by using Blender**"* — each piece is a separate selectable object, so counting is a traversal.

> **→ A COUNTABLE SCHEDULE NEEDS OBJECTS THAT EXIST SEPARATELY AND CARRY A TYPE, AND NOTHING MORE CLEVER THAN THAT.**
>
> ⚠️ **And the limit is the important half.** A brick count is exact by construction because bricks are discrete and identical. **Nothing in that demonstration addresses the quantities that actually cost money on a renovation** — area, length and volume of continuous materials, where waste, cut loss and coursing decide the number (§2). **Counting is the part that was already easy.** [source: [[_Sources/YT_DgovrfgLxYs_brockmesarich_astra_blender_parts_schedule|YT_DgovrfgLxYs]] — `promotional_ratio: very_high`, extracted at 3 facts]

### ⚠️⚠️ An object is in the model because it carries a CLASS — so a drafted-only element is invisible to take-off

Drawing a floor plan, a practitioner represents the kitchen countertop and the built-in cupboards as **2D drafting lines**, deliberately: *"we're not going to model it per se."* They appear on the sheet and are not objects.

> **→ A LEGITIMATE DOCUMENTATION SHORTCUT THAT SILENTLY REMOVES AN ITEM FROM EVERY SCHEDULE. The drawing and the take-off can disagree, and this is how.**
>
> ⚠️ **Joinery is exactly the class of item this hides, and it is not cheap.** The same mechanism appears as a data-loss trap elsewhere: **saving to IFC discards anything not classified as IFC.** **→ A take-off gate should assert that every priced line has a model element behind it, and flag any drawn element that has none.** [sources: [[_Sources/YT_PNoOyCHa_V0_ifcarchitect_blenderbim_floor_plan|YT_PNoOyCHa_V0]], [[_Sources/YT_tAq0foY2GOY_spbproduction_bonsai_ifc_vs_blend_save|YT_tAq0foY2GOY]]]

### The schedule groups by TYPE — so type granularity is a costing decision

A type edit changes every instance, and divergence is expressed by **duplicating the type**. **→ Every genuinely different door in this flat needs its own type**, or the schedule cannot distinguish them. ⚠️ And a thin type library pushes the other way: a practitioner accepts *"the **200 wall, because that's similar to a masonry brick wall of 220**"* — **a 20 mm error taken on to stay inside the library.** **A type-library workflow trades dimensional fidelity for schedulability; ours currently has the fidelity and not the schedule.** Full treatment: [[18_Digital_Toolchain/analysis/Model_To_Drawing_Pipeline|Model to Drawing Pipeline]] §5, §8.

### ⚠️ Per-room faces are the geometric precondition for per-room quantities

Two practitioners independently separate floor faces per room so each can take its own material — and that is the same structure the screed, waterproofing, skirting and cornice lines need. **Corroborates the gap analysis's note that `Qto_SpaceBaseQuantities.NetFloorArea` and `.Perimeter` are the missing inputs.** ⚠️ **And a product-identity note worth keeping**: published manufacturer IFC assets let the model carry *the product actually being ordered* — the `resource_role` / `product_id` split the BOM already uses — **but they are Revit-first exports and must be treated as untrusted imports.** [source: [[_Sources/YT_4JYFYvNg5Xk_blender3darchitect_external_ifc_libraries_bonsai|YT_4JYFYvNg5Xk]]]

## 6. The prerequisite nobody can skip

**Stated as a precondition before any quantity is trustworthy: the model must be organised.** Geometry separated into groups; tags assigned and used; **materials properly named** — *"this is going to make it easy to recognise the objects and materials in your model."*

> **→ The general form, which transfers to a project using no SketchUp at all: a take-off is only as good as the naming and grouping discipline applied while modelling. The quantity engine does not impose structure — it exposes whether you had any.**
>
> **⚠️ The equivalent discipline here is the element taxonomy and the `structural_element_id` scheme in `data/canonical/`.**

- **A cheap convention worth stealing**: prefix pricing tags with **`PR`** (e.g. `PR 2x6 spruce`) so a costing layer stays legible inside a shared namespace.
- **Native capability is not enough, and it is worth knowing why**: SketchUp Pro has an advanced-attributes **price field** and a report generator, and a practitioner who used it calls it *"really limited… not nearly as flexible."* **A price field that cannot aggregate by tag, material, length, area, volume and weight is a price field, not a cost engine.**
- **Quantities can be pulled with no plugin at all** — the native Entity Info tray gives a face's area, a line's length, and **multi-select gives total wall area net of openings, floor area, or whole-flat perimeter.** That is exactly the aggregation the commercial extensions automate.

## 7. ⚠️⚠️ An end-to-end take-off→price workflow, and the two gates in it

**The only source in this folder that carries the join all the way to a priced bid.** ⚠️ It is a commercial contractor's tender process — this project has no bid, no tender and no client — **so it is read for the DIVISION OF LABOUR and the CONTROL STRUCTURE, not the bid machinery.** [source: [[_Sources/YT_VrSs8mGI8ss_fairley_takeoff_to_priced_bid|YT_VrSs8mGI8ss]]]

### ⚠️ The contrarian claim: the assemblies are the work, the measuring is not

Flagged by him as his own opinion that others would dispute:

> *"The annoying thing about doing a quantity take-off is SETTING UP ALL YOUR ASSEMBLIES… By the time you've customised these with all the correct sub-items, all the correct secondary quantities, that is the time-consuming thing. When you're actually going and measuring stuff from the drawings, it genuinely doesn't take that long."*

**His method follows from it, and it is the transferable part:**

- **Keep a BASE ASSEMBLY LIBRARY** — standard breakdowns for walls, concrete, earthworks — **already carrying the productivity rates.**
- **A skill SPECIALISES the standard assembly to the project**: it reads the material specifications called out on the drawings and turns a generic "blockwork wall" into *"wall type 3 as specified on this project"*, with the right depths, volumes and reinforcement.
- **⚠️⚠️ And the critical framing of what the model actually does: *"Instead of using AI to do the counting, we're using AI to EXTRACT THE MATERIAL SPECIFICATIONS AND TEXT TAGS."*** It reads the **text layer**, not the geometry — consistent with §3's counting-versus-measuring split. His reason: *"wall type three isn't a generic universal term. It is specific to this construction project."*
- **Measuring stays manual.** *"AI isn't reliable at this step, so it's better to just do it manually."*

### ⚠️⚠️ Two gates on the pricing step

1. **⚠️⚠️ IT FLAGS EVERY RATE IT DOES NOT KNOW.** *"Importantly, I get it to flag any rates where it does not know the rate."* The unknown rate is then quoted or recorded as an explicit assumption.
   **→ An explicit "no rate for this" output instead of a silently invented one. This is the silently-supplied-values rule applied to PRICES rather than to geometry**, and it is the single most transferable control in the source. **Cheap to adopt in any costing sheet: a required provenance field that cannot be left blank.**
2. **⚠️⚠️ The delegation is scoped as a principle: *"It's always just moving information around."*** The model transports rows from the take-off CSV into the estimate's direct-cost sheet — *"the task I know it can do reliably and accurately"* — and is **not** relied on for judgement. **Delegate transport, not judgement.**

**⚠️ A practical limitation that generalises: a spreadsheet assistant could not see his `CLAUDE.md`** — it knows spreadsheets and nothing about construction. **His workaround is an "AI instructions tab" inside the workbook** describing its structure and where each kind of information lives. **→ When a tool cannot reach your project context, put the context INSIDE the artefact.**

### ⚠️ Indirect cost is a function of duration

**Direct cost is the physical work; indirect is managing it. The key input to indirect cost is the project's DURATION**, and for a self-performing outfit he says no AI is needed: **total labour hours → assume a crew size → forecast duration → allocate.** **The largest indirect cost is recurring overhead, and it scales with how long those roles run.**

- **⚠️ Relevant here despite the commercial framing: a self-managed renovation's equivalent indirect cost is the owner's own time and the duration of disruption**, driven by the same variable. See [[11_Budget_and_Planning/analysis/Project_Duration_and_Scheduling|Project Duration and Scheduling]].

## Related

- [`toolchain_gap_analysis_20260908.md`](../../_Inbox/planning/toolchain_gap_analysis_20260908.md) §B — **this project's own cost-engine design**, including the substitution-first correction, the cascading-task rule, and the `[Trade]-[Task]:[Room]:[Resource]` taxonomy.
- [[11_Budget_and_Planning/analysis/Bill_of_Quantities_and_Procurement|Bill of Quantities and Procurement]] — the practitioner side: what a смета contains, how estimates are compared, and the cutting-plan take-off.
- [[18_Digital_Toolchain/analysis/AI_Reading_Construction_Drawings|AI Reading Construction Drawings]] §2 — take-off as the third data layer, and the IFC origin of the element schema.
