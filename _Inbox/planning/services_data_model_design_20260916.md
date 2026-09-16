# Services data model — identity, concepts and status vocabulary

**2026-09-16. DESIGN. NOT approved for generation.** It moves to `00_Master/` beside `Finishes_and_Furniture_Data_Model.md` once accepted; until then nothing generates from it.

> [!IMPORTANT]
> **Status, 2026-09-16 after review:**
> - ✅ **The GUID rule in §2 is APPROVED** — `identity_uuid` immutable, IFC `GlobalId` derived from it and nothing else.
> - ⛔ **Five amendments are REQUIRED before any service migration or IFC generation.** They are listed in **§7** and are NOT yet applied to §§2–3 below, which therefore still read as first drafted. **Read §7 before implementing anything here.**
> - ▶️ **The geometry compiler extraction proceeds independently** and is not blocked by these.

**Why it exists now.** Services are currently authored in three places that can disagree — Python literals inside `tools/layout/sheets/make_services_sheets.py`, `electrical_existing.csv`, and `service_outlets.csv` — and the IFC consumes none of them. The generator was frozen on 2026-09-16 and its write-back into `data/canonical/` stopped, but **containment is not a fix**. This is the authored-data design that migration needs, and it is the one part of the work that does **not** depend on extracting the geometry compiler first.

---

## 1. Four concepts, not one table

The single biggest error available here is one flat `services.csv` with a `status` column. **The legacy ids already prove the concepts are different things:**

| Legacy id | What it actually is | Concept |
| :--- | :--- | :--- |
| `E-KL-SOC-K` | *"socket outlets, кухня zone, corridor wall, count 3, height 915-1105"*, from one photo | **observation** |
| `SW-K` | *"hot and cold water take-off, clamped, rising from the floor, valve tops 500-610"* | **assembly** |
| `SS-B` | one sewer connection on P1 | **occurrence** |
| `S1` | one symbol on a drawing | **display of an occurrence** |

**⚠️ A one-to-one migration is therefore impossible and must not be forced.** `E-KL-SOC-K` is three sockets seen once at a height range; it becomes one observation plus up to three occurrences, and the observation keeps its identity as evidence.

| Concept | Holds | Example |
| :--- | :--- | :--- |
| **Occurrence** | a thing that exists or will exist, in one place | a socket, a grille, a riser, a luminaire |
| **Observation** | what a photo or an owner statement establishes, and its limits | *"three boxes in a row, 915–1105, oblique shot, no scale in the wall plane"* |
| **Connectivity** | circuits, systems, ports, A→B relationships | *"this socket is on circuit C3"* |
| **Route** | a physical or intended path | *"C3 runs in the G3 wall zone at 300 mm"* |

An occurrence **cites** observations. It does not absorb them: the evidence has to survive the conclusion, because that is what let the window error be caught.

---

## 2. Identity — continuity, not the strings

**Do not promote `S1`, `SW-K` or `E-KL-SOC-K` to permanent identity just because they exist.** They are not stable, not uniform and not all the same kind of thing.

| Field | Rule |
| :--- | :--- |
| `identity_uuid` | **Immutable, machine-generated, never reused.** The IFC `GlobalId` is derived from this and from nothing else. |
| `service_id` | Readable and unique. **Immutable once issued** — if it turns out wrong, supersede rather than rename. |
| `display_mark` | What a drawing prints. **May change freely**; carries no identity. |
| `legacy_alias` | **Namespaced**, list-valued: `legacy_sheet:S1`, `service_outlets:SW-K`, `electrical_existing:E-KL-SOC-K`. |
| `superseded_by` | For genuine replacement. **Records are superseded, never deleted.** |

> ⚠️⚠️ **Why the GUID must derive from `identity_uuid` and not from `service_id`:** a regenerated IFC has to re-join to annotations, review decisions and previously issued sheets. Derive the GUID from a readable code and the day someone improves that code, every annotation against it is orphaned — silently, because the model still loads.

---

## 3. Status — four independent fields, never one column

**One `status` column would force unrelated facts to share a slot**, and the first casualty is always the distinction between *what we know* and *what we have decided*.

| Field | Values | Answers |
| :--- | :--- | :--- |
| `phase` | `existing` / `demolished` / `new` | Is it there now, going, or coming? |
| `knowledge_basis` | `measured` / `observed` / `derived` / `assumed` | **How do we know?** |
| `decision_status` | `proposed` / `owner_approved` / `trade_approved` / `rejected` / `superseded` | **Who has agreed?** |
| `route_state` | `topology_only` / `design_intent` / `construction_approved` / `as_built` | How real is the path? |

**These are genuinely orthogonal.** An existing socket can be `observed` but not measured, and `proposed` for removal. A new luminaire can be `owner_approved` while its circuit is still `topology_only`.

> ⚠️⚠️ **`as_built` is a LATER ASSERTION than `construction_approved`, not a synonym.** Approved means someone signed off a path; as-built means someone recorded what was actually installed. **A generator may never promote one to the other, and may never promote `topology_only` into a route at all** — if the model can invent a path, the model is asserting something nobody decided.

---

## 4. Who decides what

Recorded because it governs which fields a generator is allowed to write.

| Decision | Authority |
| :--- | :--- |
| Terminal positions, what is served, switching, performance intent | **Owner / designer** |
| Technically constrained routes | Services designer or the relevant trade |
| Concealed cable routing **within agreed zones** | **The electrician keeps this freedom** — so the model should assert a zone, not a cable |
| Drainage runs | Pre-coordinated: diameter, slope and invert elevation matter |
| Ventilation runs | Pre-coordinated: a 150–200 mm duct zone under a **2500 mm** ceiling is consequential |
| `as_built` | Recorded from site. **Never derived.** |

---

## 5. IFC mapping, when generation starts

Concrete leaf types, not the generic ones: **`IfcOutlet`, `IfcLightFixture`, `IfcAirTerminal`, `IfcSanitaryTerminal`, `IfcCableSegment`, `IfcPipeSegment`, `IfcDuctSegment`.** Connectivity via **`IfcDistributionPort`** and system membership, which expresses A→B with **no physical path asserted** — exactly what `topology_only` means.

> ⚠️ **Schema version is a separate decision.** `model_from_dxf.py` writes **IFC4**; the `IfcFlowSegment` deprecation that justifies concrete types is an **IFC 4.3** statement. The concrete types are right either way, but **the schema must not change as a side effect of adding services** — it needs its own step, tested against Bonsai, the glTF export and every existing gate.

---

## 6. What this design does NOT settle

1. **The locator.** Every occurrence needs a host-local position — `on_element`, `along_wall_mm`, `height_mm`, plus which face. **Those cannot be defined here**: they must mean the same thing in the IFC and in every discipline sheet, and today only `export_v0_dxf.py` knows what they mean. **Blocked on the geometry compiler, deliberately.**
2. **Whether CSV remains the carrier.** Workable at this scale, but hosts, ports, systems, phases, variants, evidence and approval states are a relational shape. If it stays CSV it needs strict schemas and a validator, not convention.
3. **Migration of the frozen literals.** Every literal in `make_services_sheets.py` must first be classified as observed existing / owner decision / design assumption / route topology. That is a reading job, and it is where owner decisions recorded only as Russian comments — *«ВЛАДЕЛЕЦ: на G7 две розетки, выключателей нет»* — have to be recovered as data rather than prose.

---

## 7. ⛔ REQUIRED AMENDMENTS — apply before any migration or generation

From review, 2026-09-16. **§§2–3 above still read as first drafted; these supersede them where they conflict.**

### 7.1 Only `identity_uuid` is immutable

§2 said a mistaken `service_id` must be superseded. **That is wrong: it manufactures a physical replacement to record a naming correction**, and then the history claims a socket was replaced when someone only fixed a typo.

- `service_id` is **renameable and audited** — old codes are preserved as aliases.
- **Supersede only when the represented THING changes**, never for a naming fix.

### 7.2 Knowledge basis belongs to each value, not to the occurrence

One `knowledge_basis` per occurrence cannot describe reality. **A single socket can simultaneously have observed existence, derived height, assumed host and unknown horizontal position** — and `electrical_existing.csv` already contains exactly that case.

**Every locator and dimension value carries its own basis and its own observation references.** Occurrence-level basis, if kept at all, is a derived summary.

### 7.3 Approvals are records, not a scalar

`owner_approved` then `trade_approved` **must not erase the owner's approval**, and an approval has to say *what* was approved — count, position, voltage, route.

An approval record carries: **subject / property, actor, decision, date, evidence.** `decision_status` becomes a derived summary of those records, not the store.

### 7.4 Typed uncertain measurements — preserve the raw, normalise without inventing precision

**This is the amendment the existing data most needs.** `electrical_existing.csv` records heights as `"ceiling"`, `"low + one mid"`, `"915-1105"`, `"~880"`. None of those is a `height_mm`, and **`"low + one mid"` is a grouped observation, not one height locator.**

| Field | Values / meaning |
| :--- | :--- |
| `vertical_mode` | `point` / `range` / `band` / `relative` / `full_height` / `unknown` |
| `datum` | `finished_floor` / `slab` / `ceiling` / host-relative |
| `nominal_mm`, `min_mm`, `max_mm`, `uncertainty_mm` | as applicable to the mode |
| observation ref + basis | per 7.2 |

**Keep the raw observation text.** Normalisation sits beside it and never replaces it.

### 7.5 Succession is a relation, not a single field

`superseded_by` as one value cannot express a **split** (one recorded group becomes three sockets) or a **merge**. Both are expected here: `E-KL-SOC-K` is one observation of three outlets. **A record may legitimately have several successors.**

---

## 8. What the compiler owes this schema

Recorded now so the extraction does not have to be revisited. **The resolved model must retain:**

- **pre-reconciliation SOURCE values** — what each input asserted before closure, yielding or snapping touched it;
- **final geometry** — what was resolved;
- a **machine-readable reconciliation report** — which rule moved what, and by how much.

**Without the first and third, an uncertain measurement loses its provenance the moment it passes through the compiler** — which is the same defect as the retired schematic, one layer further in.
