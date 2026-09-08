# Gemini Deep Research report — 2D/3D/budgeting toolchain and the agent thesis

**Fetched 2026-09-08** from Google Docs `1qBwtmhZzQKZuF5J4IdybLWzafpVdQR0eTN3iFGfMuQQ` (title: "Gemini research")
via the qa-management repo's stored OAuth token, read-only. **Raw text as returned, unedited.**

⚠️ **This is a SECONDARY source with identified factual errors.** Read
`deep_research_review_20260908.md` before using anything here — in particular, **none of its legal
content may enter `16_Legal_and_Regulations/` without primary verification** (that folder is level-1 only).

---

Belarusian Legal & Regulatory Framework for Apartment Renovation
Presidential Edict № 200, Administrative Procedures
Under Presidential Edict № 200 (26.04.2010, as amended), residential administrative procedures run through the "Одно окно" (One-Stop Shop) service of the local district administration (администрация района / исполком) in Minsk. The procedures governing an apartment renovation under Council of Ministers Resolution № 164 (03.04.2026) follow specific cost and timeframe requirements:

Subparagraph 1.1.21: Approval (permit) for reorganization and/or redevelopment (переустройство и (или) перепланировка)
Submission requirements: Application; passport or identity document; document confirming property ownership (or right to occupy); technical passport (технический паспорт); simplified layout diagram (план-схема) or full project documentation (if required); written notarized consent of all adult registered co-owners/occupants.
Official fee: Free of charge (бесплатно).
Statutory timeframe: 1 month from submission (reduced to 15 calendar days if the applicant provides all supplementary documents independently).
Validity: Indefinite (бессрочно).
Subparagraph 1.1.21¹: Approval of completed works / Acceptance Act (утверждение акта приемки выполненных работ)
Submission requirements: Application; decision/permit issued under 1.1.21; approved план-схема or project; Certificate of Technical Characteristics (ведомость технических характеристик — where applicable); executed Acts of Concealed Works (акты на скрытые работы).
Official fee: Free of charge.
Statutory timeframe: 1 month.
Subparagraph 1.1.21²: Approval of facade-mounted equipment (air conditioners, satellite dishes)
Submission requirements: Application; passport; document confirming ownership; technical passport; manufacturer datasheet/specifications and photo/diagram showing exact mounting location on the facade.
Governing body: Territorial architecture and urban planning department (территориальное подразделение архитектуры и градостроительства).
Official fee: Free of charge.
Statutory timeframe: 15 calendar days.
Subparagraph 1.15.1: Extract from the Unified State Register of Real Estate (ЕГРНИ)
Submission requirements: Passport, proof of title.
Official fee: 0.1 to 0.2 Base Values (базовая величина, БВ).
Statutory timeframe: 1 to 3 working days.
Subparagraph 1.15.3: State registration of changes to real estate (issuing new Certificate of Title and updated Technical Passport)
Submission requirements: Approved Acceptance Act (акт приемки); Technical Passport or ведомость технических характеристик; application; receipt of payment.
Official fee: 0.5 БВ for standard registration + 0.1 БВ for the physical certificate; an optional acceleration surcharge of 0.3 БВ cuts lead times.
Statutory timeframe: 7 working days (2 working days with the accelerated fee).
СН 3.02.01-2020: The "Wet-Zone" Expansion and Relocation Norm
Relocating or expanding bathrooms, toilets, and kitchens is strictly governed by Building Norms of Belarus СН 3.02.01-2020 "Жилые здания" (Clause 4.11):
«Не допускается размещение санитарных узлов (ванных комнат, душевых, туалетов) непосредственно над жилыми комнатами и кухнями квартир нижерасположенных этажей. Допускается размещение санитарного узла над кухней квартир, расположенных на верхнем этаже, а также в двухуровневых квартирах, если санитарный узел находится в пределах одного жилого помещения конкретного собственника.»
Under this norm:
A bathroom or shower room cannot be enlarged or shifted over an area designated as a living room (жилая комната) or kitchen (кухня) in the apartment below.
Expanding a bathroom or WC is permissible only at the expense of non-living, non-kitchen circulation/storage spaces: corridors (коридоры), entrance halls (прихожие), pantries (кладовые), or vestibules (тамбуры), provided continuous waterproofing (гидроизоляция) with upturns of at least 150 mm on walls is executed and documented.
A kitchen cannot be relocated or extended over the living space of the apartment below, because doing so compromises the living conditions of neighbors and violates fire/sanitary standards.
Technical Passport vs. Certificate of Technical Characteristics (ВТХ)
The boundary between the технический паспорт and the ведомость технических характеристик (ВТХ) is established under the Law of the Republic of Belarus № 133-З "On State Registration of Real Estate" and State Property Committee (Госкомимущество) technical instructions:
1 January 2023 Boundary: Substantive amendments to registration law ended the historic practice where a технический паспорт could be updated with arbitrary layout alterations or stamped with "unauthorized renovation" (самовольная перепланировка) notes. Since 1 January 2023, the технический паспорт reflects only lawfully registered, completed, and accepted property states.
Ведомость технических характеристик (ВТХ): A temporary, strictly technical document issued by the territorial organization for state registration and land cadastre (БТИ / Минское городское агентство по государственной регистрации и земельному кадастру). It documents the actual geometric status of an object undergoing reconstruction or redevelopment prior to formal acceptance.
Cost and Lead Time:
ВТХ: Requires an on-site survey by an engineer. Costs 150 to 350 BYN (dependent on area and partition complexity); lead time is 7 to 15 working days.
Updated Технический паспорт: Issued only after the executive committee accepts the renovation under Subparagraph 1.1.21¹ and the registration changes are logged under 1.15.3. Cost is 50 to 100 BYN; lead time is 5 to 7 working days.
Noise Regime: Permitted Windows and Enforcement Boundaries
Residential quiet hours and permitted construction noise are governed by two distinct frameworks:
General Domestic Noise (Положение об условиях и порядке переустройства и перепланировки, Resolution № 399):
Quiet hours run daily from 23:00 to 07:00. Permitted daily activities (speech, television, normal household operation) are allowed between 07:00 and 23:00, provided they do not exceed legal residential decibel thresholds.
Structural and Redevelopment Noise (КоАП РБ, Article 22.12, Part 3):
Any work creating construction noise or vibration (rotary hammer drilling, structural cutting, screed demolition, channel chasing) is permitted strictly on working weekdays between 09:00 and 19:00.
Such work is expressly prohibited on weekends (Saturday, Sunday) and official state holidays.
Enforcement scope: The 09:00–19:00 restriction applies per task (the acoustic profile of the actual tool/activity), not per overall project timeline. Non-vibrating, quiet finish tasks (brush painting, wallpapering, dry measuring) are legal on weekends and during daytime hours from 07:00 to 23:00. However, in residential practice in Minsk, running noisy mechanical equipment outside the 09:00–19:00 weekday window leads immediately to police (РОВД) or utility management (ЖЭУ) intervention under Article 22.12.
СН 2.02.05-2020: Fire-Resistance Requirements for Internal Partitions
Under Building Norms СН 2.02.05-2020 "Пожарная безопасность зданий и сооружений":

Multi-apartment residential buildings are classified as fire safety class Ф1.3.
While inter-apartment separating walls (межквартирные стены) must maintain a certified fire-resistance rating of at least EI 45 (or REI 45) and inter-apartment walls separating dwelling units from public corridors require certified non-combustibility (fire barrier type 1 or 2), internal non-load-bearing partitions entirely within a single apartment are not assigned a mandated fire resistance rating (no EI threshold).
However, material flammability classes are regulated: internal partitions must be constructed from non-combustible materials (НГ) or materials with low flammability (Г1). Standard autoclaved aerated concrete (AAC / газосиликат), solid or hollow gypsum partition blocks (ПГП), clay bricks, and gypsum plasterboard (ГКЛ/ГКЛВ) on galvanized cold-formed steel framing satisfy these baseline requirements without custom fire barrier testing.
Administrative Penalties (КоАП РБ)
Enforcement actions fall under the Code of the Republic of Belarus on Administrative Offences (КоАП РБ), primarily Article 22.12:

Violation
Legal Basis
Penalty (Natural Person / Owner)
Disturbance of domestic peace (noise, vibration) between 23:00 and 07:00
Art. 22.12, Part 1

Fine from 2 to 10 Base Values (БВ)

Repeated noise violation within 1 year of administrative sanction
Art. 22.12, Part 2

Fine from 10 to 30 Base Values (БВ)

Performance of noisy/vibrating renovation works on weekends/holidays or on weekdays outside 09:00–19:00
Art. 22.12, Part 3

Fine from 4 to 10 Base Values (БВ)

Unauthorized renovation (самовольная перепланировка) without impact on load-bearing capacity
Art. 22.12, Part 4

Fine up to 20 Base Values (БВ)

Unauthorized renovation compromising structural load-bearing capacity, or unauthorized tampering with building ventilation shafts
Art. 22.12, Part 5

Fine from 10 to 30 Base Values (БВ) + mandatory remediation

Note: In Belarus, paying an administrative fine does not regularize an unapproved modification; the owner must subsequently legalize the layout via an executive committee decision or return the premises to its original condition at their own expense.

Statutory Interpretation: Resolution № 164
Resolving the Ambiguity in Paragraphs 18 & 23
The issue is whether paragraphs 18 and 23 of Resolution № 164—when exempting «абзацы второй и третий части первой пункта 3» from the requirement to produce a ведомость технических характеристик—exempt the introductory phrase or the list items.
Under the Law of the Republic of Belarus of 17 July 2018 № 130-З "О нормативных правовых актах" (specifically Article 26, regulating rule-drafting technique and structural units of normative acts):
Definition of Paragraph (абзац): An абзац is defined as a discrete portion of text separated by an indentation (indent line / красная строка) ending with a period, semicolon, or colon.
Introductory Lead-Ins: When a numbered paragraph (пункт) or sub-part (часть) contains an introductory clause that terminates with a colon (e.g., «К работам по переустройству и (или) перепланировке относятся:»), that introductory text constitutes абзац первый (the first paragraph) of that structural part.
Sequential Enumeration:
Абзац первый: The introductory mandate («К работам… относятся:»).
Абзац второй: The first indented item of the closed statutory list (works altering gas, central heating, and ventilation systems).
Абзац третий: The second indented item of the closed statutory list (insulation and thermal envelope works).
Legal Conclusion:
Under Belarusian drafting doctrine, the works exempted from procuring a ведомость технических характеристик are the works specified in the first two bulleted list items (gas/heating adjustments and internal thermal envelope/insulation works).
Internal partition modifications (переустройство перегородок), which alter room boundary geometry and floor surface areas (жилая/общая площадь), fall in the subsequent indentation (fourth paragraph). Therefore, internal partition demolition or erection is NOT exempt from the ведомость технических характеристик. Because partition shifts change legal boundary metrics, the territorial registration body (БТИ) must issue a ВТХ to confirm the newly created geometric state before the acceptance commission can validate the completion under § 21.
Drawing Requirements: The "No-Project" План-схема
Under Resolution № 164, a "no-project" track (без разработки проектной документации) is permitted for non-load-bearing partition modifications and openings. The required submission is a план-схема:
Substance of the План-схема:
Based directly upon an official copy of the apartment's current Technical Passport floor plan (поэтажный план БТИ).
Clearly displays all demolished non-bearing elements (conventionally highlighted in red or hatched dashed lines).
Clearly displays all newly proposed non-bearing partitions (conventionally highlighted in green or solid bold lines).
Annotates clear linear dimensions for new partition placements relative to surviving structural/monolithic building axes.
Provides an explicit Room Legend (экспликация помещений) specifying the intended function and provisional area of each resulting space.
Confirms wet-zone perimeters, verifying that sanitary wet zones remain strictly above designated non-residential spaces of the lower unit.
Who Draws It:
Under § 14 of Resolution № 164, an owner may prepare the план-схема personally.
No designer license or engineering certification (аттестат соответствия Белстройцентра) is required for this track. A CAD/IFC-generated drawing from open-source software (Bonsai / IfcOpenShell / ezdxf) is accepted by the administrative authorities provided it clearly, legibly, and dimensionally depicts the modifications against the baseline BTI layout.
Quantity Take-Off (QTO) & Classification
Measured Off the Model vs. Derived From Datasheets
A professional Quantity Take-Off pipeline differentiates between geometry-derived quantities and chemistry/datasheet-derived consumables:



[IFC Model Geometry: Areas / Volumes / Counts]                     │                     ▼       ┌───────────────────────────┐       │ Deduction Rules (POMI/SMM) │       │ Net vs. Gross Dimensions   │       └─────────────┬─────────────┘                     │                     ▼         [Product Technical Datasheet]         ├── Dry Consumption (kg/m²/mm)         ├── Mixing Water Ratios         ├── Application Tool Profile         └── Substrate Loss Allowance                     │                     ▼       [Final Bill of Materials & Costs]
Extracted from the IFC Model:
Direct Net Areas: Qto_WallBaseQuantities.NetSideArea (plaster, primer, paint, tile surface area).
Direct Net Floor Areas: Qto_SpaceBaseQuantities.NetFloorArea (screed, self-leveling underlayment, waterproofing membrane, floor tile, parquet).
Direct Perimeter Lengths: Qto_SpaceBaseQuantities.Perimeter (baseboards, perimeter acoustic damping strip).
Linear Extents: Ceiling perimeter minus opening widths (cornices, shadow gaps).
Counts: Door openings, MEP junction back-boxes (IfcFlowTerminal / IfcElectricAppliance).
Deductions Rules: Professional estimators use deduction thresholds (e.g., standard SMM or DIN 18299/18350 rules): openings $< 0.5 \text{ m}^2$ are ignored when measuring plaster surfaces to offset labor waste on reveal returns. Openings $\ge 0.5 \text{ m}^2$ deduct gross area, adding the reveals' linear meterage (Length * RevealDepth).
Derived from Manufacturer Datasheets:
Dry Bagged Mixes: Volume derived from nominal thickness $\times$ model floor area. Plaster/screed bags cannot be extracted from pure geometry. Plaster (e.g., Knauf Rotband) requires calculating:$$\text{Weight} = \text{Area} \times \text{Average Thickness (mm)} \times 0.85 \text{ kg/(m}^2 \cdot \text{mm)}$$
Tile Adhesive: Derived from tile format and trowel notch depth ($8 \text{ mm}$ notch $\approx 3.5 \text{ kg/m}^2$; $10\text{--}12 \text{ mm}$ notch $\approx 5.0 \text{ kg/m}^2$).
Paints & Primers: Multiplied by nominal wet film thickness and required application coats (typically 2 coats at $120\text{--}150 \text{ ml/m}^2/\text{coat}$).
Waste Percentages vs. 1D/2D Nested Cutting Plans
Heuristic Waste Percentages:
Tile (Rectangular, regular grid layout): 7% to 10%.
Tile (Diagonal or herringbone layout): 12% to 15%.
Engineered Wood / Laminate: 5% (straight), 10% (diagonal).
Drywall (GKL): 10% to 12% to account for stud spacing off-cuts.
Algorithmic Nesting (When Professionals Use It):
Large-format porcelain stoneware ($1200 \times 600 \text{ mm}$, $2700 \times 1200 \text{ mm}$ slabs costing $> 60 \text{ USD/m}^2$): Professional tilers reject rough waste percentages. Running a 2D guillotine/strip nesting algorithm (using Python libraries such as rectpack) over actual unwrapped wall elevations maps tile seams against shower valves and niche reveals. This avoids the loss of an expensive single slab.
Sheet goods for bespoke cabinetry (EGGER MFC, $2800 \times 2070 \text{ mm}$): Sheet nesting tools (OptiCut, CutList Optimizer, or custom Python 2D bin-packing) are mandatory to factor grain direction, edge-banding offsets, and blade kerf ($3.2\text{--}4.0 \text{ mm}$).
Drywall and standard tiles: Area plus standard percentage remains industry practice; full 2D nesting offers little return on standard $2.5 \text{ m}$ drywall boards mounted on standardized $600 \text{ mm}$ center studs.
Classification: Formal BIM Taxonomies vs. Flat Structured Catalogs
For a single apartment renovation, implementing Uniclass 2015 (e.g., Pr_25_71_14_60) or OmniClass is an over-engineered operational failure mode.
These systems are designed for multidisciplinary enterprise projects, complex BIM asset facilities management (CAFM), and federated sub-contractor coordination.
Applying them to a residential apartment introduces excessive schema maintenance without adding tangible value, as Belarusian suppliers and tradesmen do not recognize or consume Uniclass/OmniClass classification codes.
Recommended Approach: A flat, 2-tier alphanumeric taxonomy keyed to production trades and room identifiers:



[Trade Code]-[Task Index] : [Room ID] : [Resource Type]
Examples:
MAS-01:R02:AAC_Block_100 (Masonry partition, Room 02, 100mm AAC block)
WAT-02:R04:Coating_Elastomeric (Waterproofing, Room 04 Bathroom, liquid membrane)
TIL-01:R04:Paving_600x600 (Tiling, Room 04, porcelain tile installation)
This maps cleanly to a SQLite or CSV price schema, ties directly to IfcPropertySet fields via IfcOpenShell, and allows deterministic SQL aggregations without graph traversal or ontological mapping.
Cost Estimation, Belarusian Norms (НРР) & 5D BIM Deltas
The Private Owner and State Estimating Norms (НРР)
Verdict: As a private owner-manager renovating an apartment, you cannot use the Belarusian НРР (НРР-2022 / НРР-2017) estimating basis.
The National Resource Consumption Norms (Нормативы расхода ресурсов, overseen by РНТЦ — Республиканский научно-технический центр по ценообразованию в строительстве) are statutorily mandatory only for state-budget-funded construction, public infrastructure, and projects utilizing state subsidies or preferential lending.
Using НРР for a private apartment renovation introduces structural discrepancies:
Labor Rate Disconnect: НРР labor valuations enforce state-indexed tariff scales (человеко-часы multiplied by the Ministry of Architecture base labor rates), resulting in base labor prices of 4 to 8 BYN per hour. Real-world qualified private trades in Minsk demand 20 to 50+ BYN equivalent per hour. No reputable private crew will work under an НРР labor contract.
Mechanization Incoherence: НРР unit prices (расценки) assume commercial construction methods (tower cranes, mechanical mortar pumps, industrial hoists). Applying these to an interior renovation yields nonsensical equipment rates.
Documentation Overhead: Managing НРР requires licensed estimating software (e.g., SXW, БелСмета, CIC) and formal forms (КБ-2в, КБ-3, C-29), producing excessive paperwork without commercial utility for private contractors.
Pricing Models: Turnkey vs. Itemized Self-Managed
To estimate accurately, rely on current local market quotes, separating the two primary operational models:
Turnkey Contractor Model (Ремонт под ключ):
Market Cost in Minsk: $180\text{--}320 \text{ USD/m}^2$ of floor area for finishing labor; $350\text{--}650+ \text{ USD/m}^2$ total including rough materials (черновые материалы).
Structure: Single general contractor contract; contractor charges a 20% to 35% margin on labor and materials to cover general management, procurement runs, site protection, and dispute risk.
Itemized Self-Managed Model (По видам работ / Прямой подряд):
Market Cost in Minsk: Direct labor averages $120\text{--}200 \text{ USD/m}^2$ of floor area.
Structure: Owner acts as general contractor, scheduling individual specialist trades (demolition, masonry, electrical, plumbing, plastering, tiling, painting).
Unit Market Rates in Minsk:
Plastering walls on beacons (штукатурка по маякам): 18–25 BYN / $\text{m}^2$.
Drywall partition (single frame, 2-layer GKL both sides): 25–35 BYN / $\text{m}^2$.
Porcelain tile installation ($600 \times 600 \text{ mm}$): 45–65 BYN / $\text{m}^2$; mitered 45° edges (заусовка): 25–40 BYN / linear meter.
Rough electrical point (recessed back-box drilling + chasing + cable pull): 18–25 BYN / point.
Plumbing point (water supply + drain termination): 80–120 BYN / point.
Price Validity, Indexation & Protective Contract Clauses
Because material and labor prices fluctuate over an extended construction cycle, private contracts need concrete financial controls:
Currency and Payment Anchoring:
Under the Civil Code of the Republic of Belarus (Article 298), all contracts and settlements between individuals must be designated and transacted in Belarusian Rubles (BYN).
However, pricing can legally be pegged to foreign currency equivalents (эквивалент в иностранной валюте) at the National Bank of the Republic of Belarus (НБРБ) official exchange rate on the actual settlement date:«Оплата производится в белорусских рублях по официальному курсу Национального банка Республики Беларусь на день фактического платежа.»
Short Validity Windows & Staged Quoting:
Subcontractor quotes should carry a firm pricing guarantee of no more than 30 to 45 calendar days.
Contract stages must be severed into discrete trade modules (Stage 1: Demolition & Partitions; Stage 2: Rough MEP; Stage 3: Screed & Plaster; Stage 4: Tiling; Stage 5: Finish Decor). Do not commit to Stage 4 labor rates during Stage 1.
Explicit Re-quoting Triggers (Триггеры пересмотра цены):
Geometric Drift: Any layout delta resulting in a quantity increase $> 5\%$ triggers a re-measurement addendum based on agreed unit rates.
Substrate Defects: Discovery of latent structural conditions (e.g., hollow underlying screed requiring complete tear-out) requires a joint examination act before supplementary work begins.
Owner Delay: If site access or owner-procured materials are delayed by $> 14$ calendar days, the contractor preserves the right to re-quote unit rates to match prevailing market movements.
Owner-Direct Material Purchasing:
Eliminate subcontractor markups by purchasing all primary materials (rough and finish) directly through local distribution networks (e.g., Материк, Mile, ОМА) or regional distributors with delivery manifests logged against your project's canonical BOM.
5D BIM: Automated Cost Deltas Between Layout Variants
An automated 5D cost delta pipeline calculates the financial variance between two IFC layout states (Variant $A$ and Variant $B$) using canonical data structures:



[Variant A (Baseline IFC)]         [Variant B (Proposed IFC)]             │                                  │             ▼                                  ▼[QTO Extractor: ifcopenshell]      [QTO Extractor: ifcopenshell]             │                                  │             └───────────────┬──────────────────┘                             │                             ▼              [Schema Delta Engine (diff)]                             │                             ▼             [Unit Price Database (SQLite)]             ├── Material Unit Rate (BYN)             ├── Labor Unit Rate (BYN)             └── Associated Secondary Tasks                             │                             ▼              [5D Cost Delta Output: JSON]
Canonical JSON Schema Representation



JSON
{  "$schema": "https://json-schema.org/draft/2020-12/schema",  "title": "CostDeltaReport",  "type": "object",  "properties": {    "variants": {      "type": "object",      "properties": {        "base": { "type": "string" },        "candidate": { "type": "string" }      },      "required": ["base", "candidate"]    },    "currency": { "type": "string", "enum": ["BYN", "USD"] },    "items": {      "type": "array",      "items": {        "type": "object",        "properties": {          "code": { "type": "string" },          "description": { "type": "string" },          "unit": { "type": "string" },          "base_qty": { "type": "number" },          "candidate_qty": { "type": "number" },          "delta_qty": { "type": "number" },          "unit_rate_labor": { "type": "number" },          "unit_rate_material": { "type": "number" },          "delta_total_labor": { "type": "number" },          "delta_total_material": { "type": "number" },          "delta_total_combined": { "type": "number" }        },        "required": [          "code", "delta_qty", "unit_rate_labor",           "unit_rate_material", "delta_total_combined"        ]      }    },    "summary": {      "type": "object",      "properties": {        "net_labor_delta": { "type": "number" },        "net_material_delta": { "type": "number" },        "net_combined_delta": { "type": "number" }      },      "required": ["net_labor_delta", "net_material_delta", "net_combined_delta"]    }  }}
Cost Delta Logic & Cascading Tasks
A wall movement delta is not merely (Length_B - Length_A) * WallRate. A 5D pipeline must resolve cascading tasks tied to the geometry:

$$\Delta C_{\text{wall}} = \sum_{k} \left( Q_{\text{candidate}, k} - Q_{\text{base}, k} \right) \times \left( P_{\text{material}, k} + P_{\text{labor}, k} \right)$$
When a $100 \text{ mm}$ partition wall shifts:
Direct Wall Structure: AAC blocks or studs/GKL ($+\text{m}^2$).
Wall Finishes (Both Sides): Plaster $\to$ Primer $\to$ Putty $\to$ Paint ($+2 \times \text{m}^2$).
Baseboards & Cornices: Perimeter change ($+\text{linear meters}$).
Flooring Infill/Deduction: Flooring edge expansion or reduction ($+\text{m}^2$).
Ceiling Intersection: Suspended drywall or stretch ceiling junction perimeter ($+\text{linear meters}$).
2D Construction-Grade from Code, Revision Drift & Site Realities
Drafting Engine Capabilities & Realistic Limits
Evaluating the programmatic toolchain for generating worker-ready A3 sheets reveals distinct functional thresholds:
IfcOpenShell Drawing Engine (ifcopenshell.draw):
Capability: Generates crisp 2D vector sections and plan slices directly from IFC spatial geometry via Open CASCADE. SVG styling is driven by CSS.
Limit: Automatic placement of complex, collision-free, associative dimension chains according to Russian/Belarusian drafting norms is not fully automated. Dimension chains often collide when features are close together, requiring manual SVG post-processing or coordinate adjustment.
Bonsai (formerly BlenderBIM):
Capability: Provides a complete drafting interface on top of native IFC. Supports automatic generation of drawing sheets, camera cut planes, dynamic schedules, and CSS-driven hatches.
Limit: Fully manual placement of detail callouts; requires Blender's graphical interface for practical sheet assembly unless driving headless Python API scripts with rigid layout rules.
ezdxf:
Capability: The industry standard for deterministic DXF manipulation. Full programmatic control over layers, colors, linetypes (ГОСТ/СТБ styles), block references, and dimension entities (DIMENSION).
Limit: It is an export primitives library, not a parametric CAD layout engine. All geometric intersections, dimension offset calculations, and text positioning must be coded manually in Python.
FreeCAD BIM:
Capability: Complete parametric modeling engine with the TechDraw module for generating standards-compliant sheets.
Limit: Headless batch execution via Python scripts is fragile across releases; generating dimension chains via Python requires navigating a dense topological naming API.
Coordination Drawings vs. "Worker-Ready" Construction Sets
A drawing sufficient for administrative approval (план-схема) or general coordination fails on site because it lacks trades-specific execution information:



Coordination Drawing (Spatial Boundary)  │  ├── ❌ Shows approximate socket clusters without baseline offsets  ├── ❌ Omits reference surface datum (rough brick vs. finished plaster)  ├── ❌ Shows continuous tile fill without cut-tile balance  └── ❌ Lacks floor buildup elevation benchmarks  │  ▼Worker-Ready Execution Drawing (Constructible)  │  ├── ✔ Datum offsets: All MEP dimensions reference bare structural corners  ├── ✔ Level markers: Absolute structural slab vs. Finished Floor Level (±0.000)  ├── ✔ Tile origins: Layout datum line, miter details, grout joint width  └── ✔ Construction junctions: Expansion gaps, ceiling drops, baseboard details
Datum References: Coordination drawings show nominal wall-to-wall dimensions. A worker-ready plan explicitly defines whether dimensions are to the rough structural masonry core or to the finished plaster face. Electricians and plumbers require dimensions referenced from bare structural corners; otherwise, a $15 \text{ mm}$ plaster layer will shift a plumbing rough-in off-center from an intended vanity cabinet.
Vertical Benchmarks: A worker-ready drawing explicitly anchors the Finished Floor Level (FFL / Уровень чистого пола, ±0.000) against the bare structural slab (отметка верха плиты перекрытия, e.g., $-0.080$). This governs the installation heights of electrical back-boxes, door rough openings, and plumbing drain slopes.
Tile Setting Plans: Requires defined layout starting axes (раскладка от центра vs от видимого угла), locations of cut pieces (ensuring no cut strip is $< 1/2$ the tile width), specified grout joint widths ($1.5 \text{ mm}$ vs $2.0 \text{ mm}$), and explicit details on whether corner miters (заусовка 45°) or metal profiles are required.
Assembly Details & Junctions: Missing on coordination drawings: recessed baseboard profiles (скрытый плинтус), ceiling expansion reveals (теневой шов), waterproofing band turn-ups at wall-floor junctions, and acoustic decoupling pads beneath floating screeds.
Drawing Revision Drift and Version Control: Git vs. Speckle
Preventing revision drift between trade-specific drawings and model revisions is a core systems-engineering challenge:
Git + Git LFS (File-Centric Approach):
Canonical JSON/CSV definitions and Python scripts reside in Git.
Binary .ifc files or compiled .dxf/.pdf sheets reside under Git Large File Storage (LFS).
Drift Detection: Text diffs operate on the underlying JSON layouts. Visual revision drift on generated 2D sheets is tracked by converting rendered PDF pages to PNG and executing headless pixel-level/DOM-level image diffing (using tools like ImageMagick or pixelmatch).
Speckle (Object-Centric Approach):
Speckle operates at the discrete BIM object level. An IFC or Blender model committed to a Speckle server decomposes into an object tree.
Drift Detection: Speckle provides native visual 3D diffing in a web viewer. It visually flags additions (green), deletions (red), and property/geometry modifications (yellow).
Verdict for Private Owner: Deploying a local Speckle server instance via Docker provides an intuitive visual interface for 3D changes, but Git + canonical JSON + programmatic SVG diffing is leaner, runs entirely offline, and ties code changes directly to cost-delta reports.
Strategic Scoping under Resolution № 164 (§20) & Concealed Works Acts
Scoping for Late-Stage Flexibility:
Section 20 of Resolution № 164 stipulates that the acceptance commission will refuse sign-off if the executed works deviate from the approved план-схема.
Established Strategy: Intentionally under-specify the submitted diagram. Only draft structural non-load-bearing partition centerlines, door opening positions, and functional room names.
Do not draw precise plumbing fixture placements, floor material finishes, electrical sockets, drop ceilings, or furniture on the permit план-схема. These are legally excluded from the closed definition of redevelopment (перепланировка) under § 3. Keeping them off the official submittal isolates finish changes from the legal acceptance perimeter.
Acts of Concealed Works (Акты на скрытые работы) for Self-Performance:
When the owner performs works personally (хозяйственным способом) under § 14, an official general contractor certificate is not required to draft concealed works acts.
The primary critical concealed operations are:
Waterproofing of wet zones (гидроизоляция пола санузлов): Application of primers, placement of elastic corner-sealing bands, and continuous elastomeric liquid membrane coating.
Acoustic floor insulation (звукоизоляция плавающего пола): Damping material installation under screeds, including perimeter acoustic decoupling turn-ups.
Owner Act Protocol: The owner signs the Act of Concealed Works as the executor. The act must be backed by a photographic log displaying a tape measure confirming overlap depths, material batch/article labels, and continuous application across room thresholds.
Architectural Visualization & Reality Capture Pipelines
From EEVEE Clay Demonstrator to Presentable Interior Renderings
The transition from a headless EEVEE clay render to a client-presentable, photorealistic architectural visualization involves distinct asset and computational requirements:
Asset Overhead:
Clay Render: Procedural single diffuse BSDF, world ambient occlusion, basic sun/area lights. Zero external texture dependencies.
Presentable Photoreal Render: High-resolution PBR material stacks (diffuse, roughness, normal, displacement maps at 2K/4K resolution); realistic fabric falloffs (sheen); high-polygon furniture, light fixture, and sanitary assets with bevels; complex light fixture setup with calibrated IES photometric profiles matching target fixture vendors.
Compute Budget:
EEVEE-Next (Blender 4.2+): Headless execution renders a 4K frame in 1 to 3 seconds on an NVIDIA RTX 40-series GPU. However, it relies on screen-space or ray-traced approximation probes for secondary indirect light bounces, frequently resulting in light leaks at wall-ceiling junctions and inaccurate ambient occlusion in tight corners.
Cycles (Path Tracer): Headless rendering with Cycles using OpenImageDenoise (OIDN) requires 150 to 500 samples per interior frame to resolve complex indirect bounces from narrow windows.
Render Time: 1.5 to 4 minutes per 4K interior frame on an RTX 4080.
The Bridge Approach: For an owner-manager, hyper-polished portfolio renders are counterproductive. A tuned Cycles setup utilizing basic white plaster, wood floor textures, accurate window daylight apertures, and IES lamp profiles provides sufficient spatial and lighting clarity without requiring hours of manual scene propping.
Generative Diffusion Models (ControlNet) Over 3D Clay Geometry
Date-Stamp: Evaluated against mid-2024 to early-2026 generative diffusion architectures (SDXL, SD 3.5, Flux.1 with ControlNet / ControlNet-Union).
Geometric Precision:
Conditioning diffusion models on ControlNet Depth + LineArt / SoftEdge / Canny passes derived from headless clay renders locks global camera perspective, major wall bounding boxes, and large cabinet volumes.
Hallucination Limits:
Generative models fail when resolving small-scale structural and execution details. They regularly hallucinate impossible tile joint alignments, invent decorative molding on flat surfaces, alter the physical geometry of faucets, blur electrical outlets, and generate inaccurate baseboard intersections.
Operational Role:
AI diffusion over clay renders is a design exploration and mood-concept tool only.
It cannot serve as a contract document or trade execution guide. Showing a subcontractor a diffusion-generated interior image leads to installation errors, as the tradesperson cannot reliably differentiate real structural intentions from neural hallucinations.
Reverse Reality Capture: Photogrammetry vs. 3D Gaussian Splatting (3DGS)
Assessing phone camera survey workflows across comparable renovation sites:
Interior Photogrammetry (Meshroom / RealityCapture / COLMAP):
Mechanism: Dense matching of visual feature points (SIFT) to reconstruct a metric triangle mesh.
Failure Mode in Residential Interiors: Standard interior apartments feature large, featureless, monochromatic drywall or plastered walls. Feature-point matching routinely fails across uniform surfaces, resulting in non-convergent camera alignment or severe mesh holes and dimensional tearing.
Scale Drift: Photogrammetry is unscaled by default. Without placing physical scale bars or coded AprilTags throughout the space and referencing them to laser measurements, the output model suffers from metric drift of 20 to 80 mm over a 10-meter span.
3D Gaussian Splatting (3DGS via Nerfstudio, Postshot, gsplat):
Mechanism: Optimizes millions of 3D ellipsoidal Gaussians in space to achieve real-time novel view synthesis.
Appearance vs. Measurement: 3DGS produces exceptional visual walk-throughs of existing states, capturing specular reflections and lighting gradients far better than photogrammetry.
Metric Accuracy: It produces appearance only, not measurable CAD geometry. 3D Gaussians have no native topological connectivity, surface normals, or distinct planar boundaries.
Point Cloud Meshing: Extracting clean, planar CAD geometry from 3DGS point clouds using mesh extractors (e.g., SuGaR, Poisson meshing) results in noisy, irregular boundary surfaces that cannot be reliably snapped to in a BIM environment.
The Practical Alternative: A calibrated laser distance meter (e.g., Leica Disto or Bosch Professional with Bluetooth, $< 1.5 \text{ mm}$ error) mapping an orthogonal bounding baseline provides the only reliable dimensional survey for construction drafting. Photogrammetry and 3DGS serve exclusively as visual site-condition archives to confirm where pipes or junction boxes were routed prior to plastering.
Colour & Finish Scheduling for Trade Execution
Systematisable Parameters vs. The Human Eye



        ┌─────────────────────────────────────────────────────────┐        │            Automated BIM / Code Attributes              │        │  • Color IDs (NCS S 1005-Y20R / RAL 9003)               │        │  • Specular Sheen (Deep Matte 2-3% / Semi-Matte 7-10%)  │        │  • Grout Joints (1.5 mm / Epoxy Resin vs. Cementitious)  │        │  • Tile Formats & Miter Angle (45° Заусовка)            │        └────────────────────────────┬────────────────────────────┘                                     │                                     ▼        ┌─────────────────────────────────────────────────────────┐        │                 Mandatory On-Site Human Eye             │        │  • Color Metamerism under 2700K vs. 4000K Lighting       │        │  • On-Site Trial Swatches (Выкрасы) under Natural Sun   │        │  • Tile Shade/Caliber Variations Between Production Lots │        │  • Visual Texture Alignment of Natural Veneers          │        └─────────────────────────────────────────────────────────┘
Systematisable in IFC and Code:
Standard color codification: Explicit color spaces using NCS (Natural Colour System) or RAL Design notations (e.g., NCS S 1502-Y50R). Commercial names (e.g., "Warm Stone") should be avoided in specifications.
Paint sheen ratings: Measured by gloss units at 60°/85° geometry (e.g., deep matte $2\text{--}3\%$, matte $7\%$, semi-matte $20\%$).
Grout joint parameters: Joint width ($1.5 \text{ mm}$), grout type (epoxy vs. high-performance cementitious), manufacturer color identifier.
Tile surface dimensions, thickness, caliber tolerances, and layout start references.
Requiring On-Site Human Judgment:
Color Metamerism: A paint batch verified under $6500 \text{K}$ laboratory lighting will shift visibly under $3000 \text{K}$ LED architectural fixtures or low-angle winter daylight in Minsk.
Wall Swatches (Выкрасы): Large-format ($1 \times 1 \text{ m}$) paint swatches applied directly to prepared, primed wall substrates are mandatory to confirm tone across morning, midday, and artificial lighting conditions.
Tile Production Caliber and Tone (Разнотон / Калибр): Ceramic tiles from the same manufacturer and catalog reference exhibit lot-to-lot color and dimensional variances. An on-site visual check across unboxed packages is required before mortar is applied.
Trade Specifications: Tiler and Painter Execution Requirements
To avoid contractor error, execution schedules must convey exact trade requirements:
What the Tiler Needs
Substrate Preparation Standard: Maximum permissible deviation under a 2-meter straightedge ($< 2 \text{ mm}$ over 2 meters).
Layout Starting Datum: The reference point from which tiles are gridded (e.g., centered on room axis, or aligned full-tile from the main door reveal).
Perimeter and Corner Treatment: Precise locations where outer corners are to be mitered at 45° (заусовка) leaving a $1 \text{ mm}$ factory edge, versus where trim profiles are permitted.
Joint & Grout Matrix: Specified joint width ($1.5 \text{ mm}$ standard; $2.0 \text{ mm}$ for non-rectified tiles); chemistry specified as 2-component epoxy (эпоксидная затирка) in all wet areas and kitchen splashbacks, including polyurethane perimeter movement joints.
What the Painter Needs
Surface Finish Level: Definition according to standard finishing grades:
Grade K3 / Улучшенная: For textured wallpapers or standard matte finishes.
Grade K4 / Высококачественная под покраску: Fully skim-coated with polymer finishing putty, reinforced with embedded fiberglass fleece (малярный стеклохолст $40\text{--}50 \text{ g/m}^2$), sanded under raking inspection light (боковой свет проявочной лампы типа Лосева / Ergolis).
Primer and System Compatibility: Primer chemistry matching the paint manufacturer (acrylic deep-penetrating vs. quartz adhesion primer); mandatory drying intervals between coats (minimum 4 to 6 hours at 20°C and 60% relative humidity).
Roller Specification: Microfiber or polyamide roller nap length (typically $8\text{--}10 \text{ mm}$ for smooth interior matte walls) to prevent irregular stippling texture.
The 2024–2026 CAD/BIM Agent Layer & Verification
Model Context Protocol (MCP) Servers for CAD/BIM
Date-Stamp: Systems architecture reflecting the 2024–2026 emergence of Anthropic Model Context Protocol (MCP) tool interfaces.
The deployment of LLM agents in BIM workflows requires deterministic interfaces. The direct modification of large .ifc text files by LLMs results in file corruption. Instead, agents interface with CAD engines through targeted MCP servers:
IfcOpenShell MCP Tools: Wraps Python APIs as JSON-RPC endpoints:
query_spatial_hierarchy(guid): Returns contained spaces and elements.
extract_quantities(element_filter): Queries geometrical base quantities.
modify_property(guid, pset_name, property_name, value): Safely writes metadata.
run_validation(ids_path): Executes IDS checking and returns deterministic error arrays.
FreeCAD Headless MCP Server: Exposes parametric feature-tree generation primitives, enabling an agent to model parametric solids using pure geometric logic without touching low-level vertex structures.
Agent-Driven Estimating: Current Feasibility
Agents are suited for parsing unstructured subcontractor proposals (PDFs, Excel workbooks, scanned quote printouts), reconciling them against a canonical price database, and running comparison logic:
Extracting Line Items: Agents reliably extract item descriptions, quantities, unit prices, and sub-totals from diverse contractor proposals with low failure rates.
Semantic Matching: An agent can link natural-language lines (e.g., "шпаклевка стен под обои") to structured database keys (PLAS-02) with higher accuracy than regex or fuzzy keyword scripts.
Limitation: Agents hallucinate when tasked with generating complex geometrical estimates directly from unannotated plans. An agent must never be permitted to "guess" quantities; it must run deterministic Python QTO scripts via its MCP toolchain to query model properties directly.
Raster-Plan to Vector Accuracy
Date-Stamp: Mid-2024 to early-2026 Multimodal Vision LLMs and CV vectorizers.
Current State: Passing an old BTI raster plan through multimodal LLMs or raster-to-vector computer vision algorithms (vectorization, wall-line extraction) yields unreliable results for construction execution.
Systemic Failure Modes:
Scale and Orthogonality Drift: Vision pipelines misinterpret small pixel distortions, introducing $1\text{--}3\%$ scaling errors and generating non-orthogonal wall lines (e.g., walls angled at $89.2^\circ$ instead of $90.0^\circ$).
Annotation Hallucination: Blurred text figures on low-resolution BTI scans are misread (e.g., reading a dimension of $3.120 \text{ m}$ as $3.720 \text{ m}$).
Engineering Rule: Never let an AI agent vectorize raster plans directly for construction documentation. The initial BTI plan must be drafted manually using laser-measured distances across primary structural points, with the raster image referenced purely as an underlay.
Review Practices: Model Integrity Gating
To keep agentic modifications safe and prevent corruption of the underlying BIM source of truth, automated continuous validation pipelines are required:



[Agent Output: IFC Modifications]                │                ▼  [Step 1: buildingSMART IDS Validation]  (Verifies Psets, Data Types, Allowed Values)                │         Pass ──┴── Fail ──► [Log Rejection]         │         ▼  [Step 2: Python Geometry & Topological Gate]  (Validates Corner Ownership, Manifold Meshes)                │         Pass ──┴── Fail ──► [Issue BCF XML Topic]         │         ▼  [Step 3: IfcClash Clash Detection]  (Checks Hard Clashes between Partitions & MEP)                │         Pass ──┴── Fail ──► [Reject Change & Rollback]         │         ▼[Commit to Main Project Branch]
buildingSMART Information Delivery Specification (IDS):
A standardized XML/machine-readable format that defines the required properties, data types, and facets for every element in an IFC model.
Implementation: Execute ifcopenshell.validate against an project-specific .ids ruleset. If an agent adds an IfcWall without the mandatory custom properties (Pset_CostData.TradeCode, Pset_CostData.BaseUnit), the commit is automatically blocked.
BIM Collaboration Format (BCF-XML / BCF-API):
Used to flag geometry and semantic issues without modifying the model. When a geometry validator (e.g., room-rollout closure script) detects an open loop or unowned corner, it generates a standardized BCF issue containing the bounding camera coordinates, error description, and element GUIDs, queuing it for review.
Algorithmic Clash Detection:
Using ifcopenshell.geom or IfcClash, hard clashes (e.g., a proposed partition wall passing through an existing plumbing riser or structural ventilation duct) are caught before committing layout iterations to the estimating pipeline.
Gap Table: DIY Open-Source/Agent Pipeline vs. Proprietary CAD/BIM
Capability Domain
Proprietary Commercial Method (Revit, ArchiCAD)
Open-Source / DIY Agent Path
Primary Failure Mode of the Open-Source Approach
BIM Layout Modeling
Parametric family placement, associative wall-junction cleanups, visual snapping.
Canonical JSON/CSV $\to$ Python script $\to$ IfcOpenShell / Bonsai parametric modeling.
Corner ownership artifacts; non-manifold geometry requiring manual Python node patching.
2D Annotation & Tagging
Dynamic smart tags, associative collision-avoiding dimension chains.
ezdxf + IfcOpenShell SVG slices + Jinja2 dynamic SVG overlays.
Dimension chains collide on dense MEP plans; excessive custom code required to handle text overlaps.
5D Cost Variant Delta
Commercial 5D plugins (iTWO, CostX) or Excel parameter schedules.
Python diff engine reading IFC base quantities $\to$ SQLite price database $\to$ Cost Delta JSON.
Cascading indirect dependencies (e.g., forgotten plaster layers or floor transitions) missed in the delta script.
Sheet Layout & Title Blocks
Built-in graphical sheet manager with automatic sheet numbering and revisions.
Bonsai Drawing Worksheets or programmatic SVG compilation $\to$ WeasyPrint / Cairo $\to$ PDF.
Rigid sheet layouts; text overflow in schedule tables breaking sheet margins.
Version Control & Drift
Proprietary cloud platforms (BIM 360, Graphisoft BIMcloud) with visual rollbacks.
Git + Git LFS for IFC/drawings + Speckle open-source server for 3D visual diffing.
Large binary IFC files inflating repositories without proper LFS pruning; team friction if non-programmers collaborate.
Render Asset Generation
Integrated real-time engines (Enscape, Twinmotion) with curated asset libraries.
Blender headless Cycles path tracing + open CC0 PBR textures.
Significant manual labor required to source, unwrap, and scale architectural materials and lighting assets.
Permit Plan Preparation
Pre-configured local drafting templates (СПДС modules for ArchiCAD/Revit).
SVG plan-sхема generator styling layout directly over referenced BTI vector geometry.
Formatting rejections by administrative reviewers due to subtle non-compliance with local plan conventions.
Capability Verdicts
Evaluated for an apartment owner-manager in Minsk, Belarus.
Replaceable by Agents Now (2026):
QTO Extraction & Cost Mathematics: Parsing validated IFC base quantities and multiplying by unit rate databases to compute 5D cost variant deltas.
Subcontractor Proposal Ingestion: Parsing messy contractor PDFs and Excel sheets into structured JSON catalogs.
Administrative Documentation Auditing: Validating compliance against closed legal lists, verifying missing submittal documents, and formatting textual application forms under Resolution № 164.
BIM Data Validation: Automated execution of buildingSMART IDS audits, syntactic schema checks, and BCF issue generation.
Replaceable with Significant Effort (Pipeline Engineering Required):
Parametric Geometry Generation: Generating valid, watertight IFC partitions from clean canonical JSON/CSV layout matrices via IfcOpenShell.
2D Construction Sheet Generation: Building programmatic SVG/DXF pipelines using ezdxf and Bonsai that produce clean, readable drawings with proper line weights, hatches, and title blocks.
Algorithmic 2D Tile Nesting: Developing custom 2D guillotine/bin-packing Python scripts to optimize expensive large-format tiles against wall unwraps.
Not Yet Replaceable (Commercial Software or Human Execution Wins):
Initial Site As-Built Verification: Physical dimensional survey using precision laser measures to resolve wall out-of-plumb and out-of-square conditions. Neither agents, vision models, nor phone photogrammetry can replace a physical site measure.
Trade-Specific Execution Detailing: Nuanced construction detailing (curated structural profiles, shadow line reveals, specialized MEP offsets) without iterative visual human review.
Material Finish and Color Validation: Evaluating color metamerism, paint swatches (выкрасы), and tile lot caliber variations under physical site illumination.
On-Site Concealed Works Inspection: Physically verifying that waterproofing, acoustic decoupling bands, and screed expansion joints are installed without defects prior to pouring mortar.
Technical Standards Matrix: Drawing & Regulatory Controls

Standard Code
Origin & Authority
Mandatory vs. Customary
Functional Scope for Interior Renovation
Постановление Совмина № 164 (03.04.2026)
Belarus (Council of Ministers)
Mandatory
The primary statute governing the closed list of redevelopment tasks, permit paths, self-performance, and acceptance procedures.
СН 3.02.01-2020
Belarus (Минстройархитектуры)
Mandatory
Residential building standards; enforces the wet-zone rule (Clause 4.11) prohibiting bathroom placement over living areas and kitchens.
СН 2.02.05-2020
Belarus (Минстройархитектуры)
Mandatory
Fire safety in buildings; sets flammability classes (НГ/Г1) for internal partitions in residential unit class Ф1.3.

СТБ 2255-2011
Belarus (Госстандарт)
Mandatory for Project Sets
Belarusian national standard for the execution of design and working documentation (title blocks, sheet structure, revision registers).
ГОСТ 21.501-2018
Interstate (EAC / Belarus Adopted)
Customary for Renovations
Rules for architectural and structural construction drawings (line weights, hatch symbols, opening tags, dimension chain layouts).
ГОСТ 21.101-2020
Interstate (EAC / Belarus Adopted)
Customary for Renovations
General requirements for project and working documentation; standard sheet margins, signature blocks (основные надписи).
ТКП 45-1.03-85-2007
Belarus (Минстройархитектуры)
Mandatory for Acceptance
Rules for internal finishing and flooring works; governs execution tolerances and the formal drafting of Acts of Concealed Works.
СПДС (Russian National Codes)
Russian Federation (СП / ГОСТ Р)
Non-Applicable in Belarus
Russian national construction rules (e.g., Russian СП 54.13330); cannot be cited or submitted to Belarusian administrative authorities.
Established Contents: «Планировочный проект» Album
An established, trade-tested planning project album (планировочный проект) prepared for interior execution comprises a standardized sequence of sheets:



[Sheet 01] Title Sheet & Project Data (Общие данные, ведомость чертежей)     │     ├── [Sheet 02] Baseline Survey Plan (Обмерочный чертеж с привязкой коммуникаций)     ├── [Sheet 03] Demolition Plan (План демонтажа перегородок и конструкций)     ├── [Sheet 04] Erection Plan (План возводимых перегородок с узлами примыкания)     ├── [Sheet 05] Furniture & Equipment Layout (План расстановки мебели и оборудования)     ├── [Sheet 06] Dimensioned Functional Plan (Кладочный план с экспликацией помещений)     ├── [Sheet 07] Floor Finishes & Levels (План полов с указанием отметок, типов и швов)     ├── [Sheet 08] Ceiling Plan & Drops (План потолков, уровней, карнизов и теневых швов)     ├── [Sheet 09] Lighting & Switch Matrix (План освещения с привязкой к выключателям)     ├── [Sheet 10] Power & Low-Voltage Outlets (План силовой электрики и слаботочных сетей)     ├── [Sheet 11] Plumbing Equipment & Rough-Ins (План сантехнического оборудования и трасс)     ├── [Sheet 12] Wall Finishes & Tiling Unwraps (Ведомость отделки стен и развертки санузлов)     └── [Sheet 13] Structural & Finish Details (Монтажные узлы: плинтусы, стыки, перемычки)
Sheet 01: General Data (Общие данные): Drawing sheet index, project explanatory summary, general execution notes, references to applicable norms (СТБ 2255, СН 3.02.01).
Sheet 02: Baseline Survey Plan (Обмерочный чертеж): Raw laser survey of the existing condition; structural wall perimeters, ceiling height benchmarks across different rooms, locations of vertical MEP risers, ventilation ducts, and primary electrical feed panels.
Sheet 03: Demolition Plan (План демонтажа): Specific indication of partitions, door assemblies, and wall sections slated for removal, with clear dimensional references to surviving structural elements.
Sheet 04: Erection Plan (План возводимых перегородок): Construction layout indicating newly erected partitions, block materials (AAC, gypsum, GKL), doorway opening clearances, lintel schedules, and soundproofing insulation details.
Sheet 05: Furniture & Equipment Layout (План расстановки мебели): Conceptual arrangement of furniture, kitchen work surfaces, and major appliances to validate ergonomic clearances.
Sheet 06: Dimensioned Functional Plan (Кладочный план): Clean architectural plan post-redevelopment showing final dimensions, nominal door swings, and the formal Room Legend (экспликация помещений).
Sheet 07: Floor Finishes & Levels (План полов): Flooring materials schedule, floor level benchmarks (Finished Floor Level $\pm 0.000$), directional laying axes, expansion joints in screeds, and waterproofing boundaries with upturn details.
Sheet 08: Ceiling Plan (План потолков): Ceiling structures (drywall, stretch membrane, acoustic panels), finished ceiling heights, access hatch locations, curtain pockets, and shadow gap perimeters.
Sheet 09: Lighting Layout & Switch Grouping (План освещения): Locations of luminaires, LED channels, and emergency fixtures, with explicit visual linkages connecting light fixtures to their designated physical wall switch groups.
Sheet 10: Power & Low-Voltage Outlets (План розеточных сетей): Placed outlets with vertical and horizontal dimensions referenced to finished walls and floor levels; includes kitchen appliance groups, TV zones, Ethernet drops, and heated floor thermostats.
Sheet 11: Plumbing Rough-In & Fixture Plan (План сантехники): Locations and centerlines of plumbing fixtures (toilets, basins, showers, floor gullies), supply line drop points, and drain pipe slope requirements.
Sheet 12: Wall Finishes & Tile Unwraps (Развертки стен и ведомость отделки): Surface finishing schedules; room-by-room elevations displaying tile layouts, joint start lines, internal corners, niche details, and paint transition edges.
Sheet 13: Construction Details (Архитектурные узлы): Detailed sections showing recessed baseboard assemblies, joints between dissimilar flooring materials (parquet to porcelain tile), and door jamb interfaces.
Tool Maturity & Licensing Inventory
Tool / Library
Version Evaluated
License
Production Maturity
Primary Use Case in Your Stack
IfcOpenShell
0.8.x (Py3)
LGPL-3.0-or-later
High (Core BIM Engine)
Programmatic creation, parsing, geometric analysis, and quantity extraction from IFC files.
Bonsai (BlenderBIM)
0.0.24+
GPL-3.0-or-later
Medium-High (GUI BIM)
Authoring native IFC models, inspecting spatial hierarchies, and compiling styled drawing sheets in Blender.
ezdxf
1.3.x
MIT
High (Production Library)
Generating and manipulating structured, standards-compliant 2D DXF files with fine layer and line-type controls.
FreeCAD (BIM)
0.21 / 1.0
LGPL-2.1-or-later
Medium
Parametric solid modeling engine; fallback for complex Boolean solid CAD operations.
Speckle Server / SDK
2.18+
Apache-2.0
High (Data Hub)
Object-level version control, branch management, and visual web-based 3D model diffing.
OpenCASCADE (OCC)
7.7.x / 7.8.x
LGPL-2.1 (with exception)
High (Industrial Kernel)
Underlying boundary representation (B-Rep) geometric modeling engine driving IfcOpenShell.
rectpack / cutting
Latest Stable
MIT
High (Algorithmic)
2D bin-packing and guillotine-cutting optimization in Python for tile and sheet good layouts.
WeasyPrint / Cairo
60.x+
BSD-3-Clause / LGPL
High (Document Engine)
Compiling programmatically generated HTML/SVG sheets into unified, printable A3 PDF drawing albums.
The "Don't Build This — Buy or Outsource" List
Don't build a custom interactive drafting GUI:
Reality: Developing an interactive web-based (Three.js/Canvas) drawing application with visual snapping, wall healing, and dynamic dimensioning takes hundreds of engineering hours to achieve basic reliability.
Solution: Keep your layout logic in structured text (JSON/CSV) and use Bonsai or commercial tools when manual visual drafting is needed.
Don't build a photorealistic rendering asset pipeline:
Reality: Modeling bespoke, production-ready furniture, faucets, appliances, and PBR material shaders from scratch in Blender consumes immense time that adds no technical value to construction management.
Solution: Use existing open CC0 texture platforms (e.g., AmbientCG, Poly Haven) for baseline materials. For high-end marketing images, outsource single-room renders to freelance visualizers on 3D platforms for a one-off cost of 40 to 90 USD per room.
Don't build a custom raster-plan vectorizer:
Reality: Using neural networks or computer vision edge-detectors to convert fuzzy BTI plan scans into clean, orthogonal walls produces scaling errors and rounding drift that will compromise downstream construction tolerances.
Solution: Manually trace the baseline BTI drawing once over an orthogonal coordinate grid in CAD (1.5 to 2 hours of work).
Don't build an internal regulatory compliance database:
Reality: Coding an expert-system rule engine that parses all constraints of СН 3.02.01, СН 2.02.05, and local administrative circulars is inefficient for a single apartment.
Solution: Review your layout constraints manually against the six statutory rules outlined in this report. If load-bearing walls or gas/heating rerouting are involved, hire an accredited local design firm for the project section (typical market cost: 350 to 500 BYN).
Don't build a real-time on-site photogrammetry processing suite:
Reality: Processing hundreds of phone photos through dense reconstruction pipelines (Meshroom, COLMAP) on an interior flat with blank white walls yields noisy, non-planar meshes with scale errors.
Solution: Buy a Bluetooth-enabled laser distance meter (60 to 120 USD) and record point-to-point structural dimensions directly into your canonical JSON data model.
Phased Project Build Order & Execution Schedule
Factoring in statutory constraints (Council of Ministers Resolution № 164, Presidential Edict № 200), local noise laws (КоАП 22.12: weekday noisy work restricted to 09:00–19:00, weekends barred), and the mandatory 30-calendar-day advance notice required prior to convening the official acceptance commission (§ 17), the project's critical path is dictated by calendar lead times, not compute cycles.



[Phase 1: Laser Survey & Baseline Data] (Day 1 - 5)  │  ▼[Phase 2: Administrative Submission — План-схема] (Day 6 - 35)  │  ├── 30-Day Statutory Review Window (Edict № 200, 1.1.21)  │  └── Concurrently: 5D Cost Deltas, Trade Sourcing, BOM Assembly  │  ▼[Phase 3: Noisy Demolition & Core Structural Works] (Day 36 - 55)  │  ├── Strictly Weekdays 09:00–19:00 (КоАП 22.12 Part 3)  │  └── Rubbish Disposal & New Partition Construction  │  ▼[Phase 4: Rough MEP & Hidden Works Documentation] (Day 56 - 80)  │  ├── Waterproofing & Acoustic Insulation  │  └── Execute & Photo-Log Acts of Concealed Works  │  ▼[Phase 5: Submittal for Acceptance Commission & Finishing] (Day 81 - 110)  │  ├── File 30-Day Advance Commission Notice (§ 17)  │  ├── Order BTI Survey for Certificate of Tech Characteristics (ВТХ)  │  └── Concurrently: Tiling, Skim-Coating, Painting, Joinery  │  ▼[Phase 6: Commission Sign-Off & Title Registration] (Day 111 - 125)     ├── Commission Acceptance (§ 20, checked against submitted План-схема)     └── Register Title Changes at BTI (Edict № 200, 1.15.3)
Phase 1: Spatial Ingestion & Canonical Baseline (Calendar Days 1–5)
Compute: Ingest manual laser measurements into canonical JSON/CSV schema. Run Python geometry validator to check wall closures and bounding box ownership.
Output: Validated baseline IFC model generated via IfcOpenShell.
Phase 2: Administrative Permitting & Cost Setup (Calendar Days 6–35)
Permitting Submission: Generate the simplified план-схема and submit the application for redevelopment under Subparagraph 1.1.21 of Edict № 200 at the local administration's "Одно окно". Scope the submittal strictly to non-bearing partition walls, avoiding finish or MEP annotations to protect future layout flexibility.
Statutory Window: 1-month administrative review clock begins.
Compute: Concurrently run the 5D BIM delta engine across candidate internal layouts. Query candidate IFC states, execute bin-packing routines for expensive finishes, ingest contractor quotes, and compile the finalized Bill of Materials.
Phase 3: Noisy Demolition & Partition Erection (Calendar Days 36–55)
Statutory Milestone: Executive committee permit received.
Site Constraints: Construction tasks generating noise (demolition, cutting, channel chasing) are scheduled strictly on weekdays between 09:00 and 19:00 under КоАП Article 22.12 Part 3. No noisy operations on weekends.
Execution: Demolish partitions, bag and haul debris under formal disposal agreements (§ 10), erect new non-load-bearing partitions (AAC/GKL) matching the approved план-схема.
Phase 4: Rough MEP & Concealed Works Documentation (Calendar Days 56–80)
Execution: Route electrical cables, plumbing lines, and underfloor acoustic membranes. Apply wet-zone floor elastomeric waterproofing with 150 mm wall upturns.
Quality Control: Draft Acts of Concealed Works (акты на скрытые работы) for waterproofing and acoustic insulation under self-performance rules (§ 14). Compile high-resolution photo-logs with dimensional scales over open installations.
Phase 5: Commission Application & Surface Finishing (Calendar Days 81–110)
Statutory Milestone: Apply to the executive committee to appoint the Acceptance Commission (§ 17), triggering the mandatory 30-calendar-day advance notice requirement.
Registration Trigger: Order the on-site survey from the territorial registration body (Минское городское агентство по госрегистрации / БТИ) to produce the Certificate of Technical Characteristics (ВТХ).
Site Execution: While the 30-day commission lead time elapses, complete all non-noisy finish installations: self-leveling screed, tiling, wall painting, and cabinetry installation.
Phase 6: Formal Acceptance & Title Updating (Calendar Days 111–125)
Statutory Milestone: Acceptance commission conducts on-site review. The executed layout is cross-checked against the approved план-схема (§ 20).
Sign-Off: Executive committee approves the Acceptance Act under Subparagraph 1.1.21¹ of Edict № 200.
Final Registration: Submit the Acceptance Act and ВТХ to the registration agency under Subparagraph 1.15.3 to update the state real estate register and receive the updated технический паспорт. Project closed.
