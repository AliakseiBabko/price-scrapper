# Wet-Zone Placement & Minimum Room Dimensions — Belarus

**Level 1 only.** Created 2026-09-08 from the primary norm: **[СН 3.02.01-2019 «Жилые здания», clause 4.9](../../_Sources/DOC_SN_3_02_01_2019_zhilye_zdaniya.md)** — read from the document itself, not from a summary.

> [!IMPORTANT]
> **⚠️ Two provenance caveats before anything on this page is used for a submission.**
> **The copy read is a preview watermarked «Для ознакомления» and does NOT include Изменения №1 и №2**, which the norm is advertised as having. **Re-check every figure against the consolidated current text.**
> **And the norm is a DESIGN norm (§4.1).** It binds a renovation indirectly, through **№ 164 §4**'s prohibition on переустройство «с нарушением строительных… требований» — see [[16_Legal_and_Regulations/analysis/Renovation_Permits_and_Approvals|Permits & Approvals]]. **That route should be confirmed with the исполком.**

## ⚠️⚠️ Clause 4.9 — the rule, verbatim

> **«Не допускается размещать санитарные узлы непосредственно над жилыми комнатами и кухнями. Размещение санитарного узла над кухней допускается в многоуровневых квартирах в случае, когда санитарный узел и кухня входят в состав одной квартиры.**
>
> **Частичное размещение одного из помещений санитарного узла (не более 25 % его площади) над жилой комнатой разрешается, если выполнены мероприятия по повышению гидро- и звукоизоляции конструкции пола этого санитарного узла.**
>
> **Размеры в плане ванной комнаты (с учетом отделки) должны быть не менее 1,5×1,7 м, совмещенного санитарного узла — 1,5×2,5 м и должны обеспечивать размещение в них ванны длиной не менее 1,7 м. Размеры в плане туалета без умывальника должны быть не менее 0,8×1,5 м, с умывальником — 1,4×1,5 м»**

| | |
| :--- | :--- |
| **Prohibition** | A санитарный узел may **not** sit **directly over living rooms or kitchens** |
| **Sole exception** | **Multi-level flats**, over a **kitchen**, **and only where the sanitary unit and that kitchen are in the same flat** |
| **⚠️ The 25 % allowance** | **Partial placement of ONE of the sanitary unit's rooms, up to 25 % of its area, over a living room IS permitted — conditional on enhanced waterproofing AND sound insulation of that unit's floor construction** |

**⚠️ The 25 % allowance is the part everyone omits, and it is the only real planning lever here.** But note its cost: enhanced гидро- and звукоизоляция are themselves «устройство гидро-, паро-, звукоизоляции», which **№ 164 §3 makes works requiring согласование in their own right.** So invoking the allowance adds a permitted work, not just a detail.

**⚠️ And note what the definition of a санитарный узел includes**: clause 3.33 defines it as the sanitary-hygienic room(s) in a flat holding bath or shower, washbasin, WC (possibly bidet) **and the washing machine.** So a laundry position inside the wet room is part of the regulated unit — relevant to [[09_Laundry_Room/Laundry_Guide|Laundry]].

## ⚠️⚠️ Minimum plan dimensions, «с учётом отделки»

| Room | Minimum in plan | Area implied |
| :--- | :--- | :--- |
| **ванная комната** | **1.5 × 1.7 m** | 2.55 m² |
| **совмещённый санузел** | **1.5 × 2.5 m** | 3.75 m² |
| both of the above | must accommodate **a bath ≥ 1.7 m long** | |
| **туалет without washbasin** | **0.8 × 1.5 m** | 1.20 m² |
| **туалет with washbasin** | **1.4 × 1.5 m** | 2.10 m² |

**⚠️ «С учётом отделки» — after finishes.** So tile build-up is inside the figure, not outside it. **Which means these are clear finished dimensions and the tiling decision eats into compliance**, not just into comfort. See [[07_Bathroom/analysis/Tile_Installation_Sequencing_and_Acceptance|Tile Installation]].

**⚠️ And these are DIMENSIONS, not areas** — consistent with this project's own standing rule that **areas are not evidence and linear dimensions are** ([[00_Master/Geometry_Variance_Study|Geometry Variance Study]]). A room can pass on area and fail on width.

## ⚠️⚠️ Applied to this flat

**ванная 3.09 m², туалет 1.24 m², floor 4 of 21** — so **no multi-level and no top-floor exception is available.**

- **ванная**: 3.09 m² clears the 2.55 m² implied by the minimum — **but the binding test is the 1.5 m minimum width after finishes, which has to be checked against the model rather than inferred from the area.** Flagged for `data/canonical/` verification.
- **⚠️ туалет: the WC clears 0.8 × 1.5 m = 1.20 m² only just, at 1.24 m², and only if both dimensions actually hold.**
  > **⚠️⚠️ And with a washbasin the minimum becomes 1.4 × 1.5 m = 2.10 m², which a 1.24 m² room cannot reach on any dimension arrangement. → A washbasin in the separate туалет is not compliant at this room's size.**
  >
  > **That settles a design question rather than raising one**, and it does so against a norm rather than a preference. See [[08_WC/WC_Guide|WC]] and [[00_Master/project_decisions|Project Decisions]].
- **The developer's layout keeps the wet rooms where they are**, so the over-living-room prohibition is not currently engaged — it becomes live only if a wet room is enlarged or moved, which is exactly what the 25 % allowance and its insulation conditions would then govern.

### ⚠️⚠️ And the туалет's own dimensions do not appear to reach the norm's minimum

**The one туалет dimension this vault actually holds is the ventilation block**: `data/canonical/room_schedules.json` records **«Вентблок в туалете у стены, противоположной входу: 1140 × 490 мм… не переносится — общедомовая шахта»**.

**So one wall of the туалет is at least ~1140 mm.** With the room at **1.24 m²**, the other dimension works out at roughly **1.09 m** — and **on those figures no dimension of the room reaches the norm's 1.5 m minimum.**

> **⚠️ Recorded as a discrepancy to resolve, NOT as a finding of non-compliance.** Three explanations are available and I cannot choose between them from what has been read:
> 1. **Изменения №1 и №2 changed these figures** — the most likely, and the reason the amendments are the top follow-up on this page.
> 2. **The minimums bind the DESIGN of a new building under the norm in force at the time it was designed**, not this flat as built.
> 3. The area figure is a CAD recalculation and the room's true shape differs — though the ventblock's 1140 mm makes a 1.5 m dimension hard to reconstruct in 1.24 m² either way. **This project's own rule that areas are not evidence cuts both ways here.**
>
> **What does NOT depend on resolving it**: the **washbasin** minimum of **1.4 × 1.5 m = 2.10 m²** is unreachable in a 1.24 m² room under any arrangement. **That conclusion holds on all three explanations** unless the amendments changed the figure itself.

### ⚠️ How this interacts with the practitioner method already in the vault

[[08_WC/WC_Guide|The WC guide]] carries a worked dimensional method from Zemskov: **absolute minimum length 1.0 m** from the installation's front face, comfortable 1.10 m; **minimum finished width 87 cm** (door-casing-driven), 90 cm before tiling; and **1.0 m width once a basin is added.**

**Put the two side by side and neither source alone gives the governing pair:**

| | Practitioner method | СН 3.02.01-2019 §4.9 | **Governing** |
| :--- | :--- | :--- | :--- |
| **Length, no basin** | ≥ 1.0 m | **≥ 1.5 m** | **the norm** |
| **Width, no basin** | **≥ 0.87 m finished** | ≥ 0.8 m | **the practitioner** |
| **Width, with basin** | ≥ 1.0 m | **≥ 1.4 m** | **the norm, by a wide margin** |

> **→ The practitioner's ergonomic minimum is more demanding on width, the norm is more demanding on length, and the norm's with-basin width is 40 cm beyond what the ergonomic method calls sufficient. A design satisfying only the practitioner method could be ergonomically fine and still non-compliant.**

## Other clauses worth carrying

- **⚠️ 4.7 — door ventilation is mandatory**: kitchen, combined sanitary unit, WC and bathroom doors must have **grilles or equivalent of at least 0.02 m²**, positioned so their **bottom edge is no more than 0.03 m above the floor.** A specification requirement on door selection, not an optional extra — see [[07_Bathroom/analysis/Doors|Bathroom Doors]] and [[12_Engineering_and_Systems/analysis/Fresh_Air_Ventilation_and_Ducting|Ventilation & Ducting]].
- **4.8 — a living room over or under a GAS-STOVE kitchen** is permitted only in single-family and blocked houses, or on the **top floor / mansard of multi-apartment buildings with multi-level flats**, kitchen and room in the same flat. ⚠️ **This is the clause whose top-floor allowance is commonly misattributed to the sanitary-unit rule** — it is a different rule about a different pairing.

## Open Questions

- **⚠️ What Изменения №1 и №2 change.** The dimensions and the 25 % allowance are exactly the kind of provision that gets amended. **Highest-priority follow-up on this page.**
- **Whether clause 4.9's dimensions bind an existing flat's перепланировка** or only the design of a new building — the indirect route via № 164 §4 is an inference, not a stated rule.
- **How «размеры в плане» is measured** — the norm says «с учётом отделки» but does not define the convention (clear internal? to finish face? at what height?).
- **Whether a shower instead of a bath changes the ванная minimum**, given the clause ties the dimension to accommodating a bath ≥ 1.7 m.
- **Whether the 25 % is measured on the sanitary unit's own area or on the room below.** Text says «не более 25 % его площади» — «его» reads as the sanitary room's, but this is worth confirming before relying on it.
