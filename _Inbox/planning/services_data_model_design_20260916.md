# Services data model — identity, concepts and status vocabulary

**2026-09-16. DESIGN. NOT approved for generation.** It moves to `00_Master/` beside `Finishes_and_Furniture_Data_Model.md` once accepted; until then nothing generates from it.

> [!IMPORTANT]
> **Status, 2026-09-16 after review:**
> - ✅ **The GUID rule in §2 is APPROVED** — `identity_uuid` immutable, IFC `GlobalId` derived from it and nothing else.
> - ✅ **The five required amendments are now APPLIED to §§2–3**, which are normative. §7 is kept as the CHANGE RECORD of what was corrected and why, not as an override — there are no contradictory sections left for an implementer to reconcile.
> - ⛔ **Still NOT approved for generation.** §6 lists what remains unsettled, chiefly the host-local locator.
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
| **Assembly** | a NAMED GROUP of occurrences that is itself a thing, with component relations | `SW-K`, the hot **and** cold take-offs; `SW-B`, the risers with their meters and valves |
| **Observation** | what a photo or an owner statement establishes, and its limits | *"three boxes in a row, 915–1105, oblique shot, no scale in the wall plane"* |
| **Connectivity** | circuits, systems, ports, A→B relationships | *"this socket is on circuit C3"* |
| **Route** | a physical or intended path | *"C3 runs in the G3 wall zone at 300 mm"* |

> ⚠️⚠️ **`assembly` is the FIFTH concept, and it was missing.** §1 originally called `SW-K` an assembly while the concept model declared only four — so an implementer had no place to put it and the only available moves were both wrong: **flatten it into one terminal occurrence**, losing the hot/cold pair, or **invent two occurrences** with no record that they are one unit.
>
> **An assembly parent is NOT one of its own component occurrences.** It must never be counted as one when checking how many occurrences a source produced, or the arithmetic double-counts the thing against its own parts.

An occurrence **cites** observations. It does not absorb them: the evidence has to survive the conclusion, because that is what let the window error be caught.

---

## 2. Identity — continuity, not the strings

**Do not promote `S1`, `SW-K` or `E-KL-SOC-K` to permanent identity just because they exist.** They are not stable, not uniform and not all the same kind of thing.

| Field | Rule |
| :--- | :--- |
| `identity_uuid` | **The ONLY immutable field.** Machine-generated, never reused. The IFC `GlobalId` derives from this and from nothing else. |
| `service_id` | Readable and unique. **Renameable, and audited when it changes** — old codes are kept as aliases. |
| `display_mark` | What a drawing prints. **May change freely**; carries no identity. |
| `legacy_alias` | **Namespaced**, list-valued: `legacy_sheet:S1`, `service_outlets:SW-K`, `electrical_existing:E-KL-SOC-K`. |
| `supersedes` / `superseded_by` | **A RELATION, not a single value.** A record may have several successors: `E-KL-SOC-K` is one observation of three outlets, so a split is expected, and merges are equally legitimate. |

> ⚠️⚠️ **SUPERSEDE ONLY WHEN THE REPRESENTED THING CHANGES.** A mistaken `service_id` is a NAMING correction: rename it and record the old code as an alias. Superseding instead would manufacture a physical replacement in the history — the record would claim a socket was replaced when somebody only fixed a typo.

> ⚠️⚠️ **Why the GUID must derive from `identity_uuid` and not from `service_id`:** a regenerated IFC has to re-join to annotations, review decisions and previously issued sheets. Derive the GUID from a readable code and the day someone improves that code, every annotation against it is orphaned — silently, because the model still loads. **This rule is approved.**

---

## 3. Status — independent fields and records, never one column

**One `status` column would force unrelated facts to share a slot**, and the first casualty is always the distinction between *what we know* and *what we have decided*.

| Concern | Where it lives | Values |
| :--- | :--- | :--- |
| `phase` | occurrence | `existing` / `demolished` / `new` |
| **knowledge basis** | **on each VALUE**, not the occurrence | `measured` / `observed` / `derived` / `assumed` |
| **approvals** | **a list of RECORDS** | see below |
| `route_state` | route | `topology_only` / `design_intent` / `construction_approved` / `as_built` |

### 3.0 Parsed multiplicity and REVIEWED multiplicity are different fields

**The parser reports what a row SAYS and never more.** `service_outlets.csv` has no `count` column at all, so every row in it parses as `multiplicity: unstated` — and that stays.

**Classification may resolve it from the row's complete evidence, in its own field, with a note.** `SS-B` is *"sewer connection, MAIN"* and the vault observes one main stack, so one occurrence is the right reading — **but it is a reading, justified by the singular description and the observation, not by the absent column.** Recording it as `reviewed_multiplicity` beside an untouched `multiplicity: unstated` keeps the difference between *what the source said* and *what somebody concluded* — which is the same distinction §3.1 draws for every other value.

### 3.1 Knowledge basis belongs to each value

**One basis per occurrence cannot describe reality, and the existing data already proves it.** A single socket can simultaneously have **observed** existence, **derived** height, **assumed** host and **unknown** horizontal position — which is exactly what `electrical_existing.csv` records today.

So every locator and dimension value carries **its own basis and its own observation references**. An occurrence-level basis, if kept at all, is a derived summary and never the store.

### 3.2 Approvals are records

`owner_approved` then `trade_approved` **must not erase the owner's approval**, and an approval has to say *what* was approved — count, position, voltage, route.

An approval record carries **subject / property, actor, decision, date, evidence**. `decision_status` becomes a **derived summary** of those records.

### 3.3 Uncertain measurements are typed

**The amendment the existing data most needs.** `electrical_existing.csv` records heights as `"ceiling"`, `"low + one mid"`, `"915-1105"`, `"~880"`. None is a `height_mm`, and **`"low + one mid"` is a grouped observation, not one height locator.**

| Field | Values / meaning |
| :--- | :--- |
| `vertical_mode` | `point` / `range` / `band` / `relative` / `full_height` / `unknown` |
| `datum` | `finished_floor` / `slab` / `ceiling` / host-relative |
| `nominal_mm`, `min_mm`, `max_mm`, `uncertainty_mm` | as applicable to the mode |
| observation ref + basis | per §3.1 |

**Keep the raw observation text.** Normalisation sits beside it and never replaces it.

> ⚠️⚠️ **These four are genuinely orthogonal.** An existing socket can be `observed` but not measured, and `proposed` for removal. A new luminaire can be `owner_approved` while its circuit is still `topology_only`.

> ⚠️⚠️ **`as_built` is a LATER ASSERTION than `construction_approved`, not a synonym.** Approved means someone signed off a path; as-built means someone recorded what was installed. **A generator may never promote one to the other, and may never promote `topology_only` into a route at all.**

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

## 7. Change record — the five amendments, and why (APPLIED to §§2–3 above)

From review, 2026-09-16. **All five are now written into §§2–3, which are the normative sections. This section is kept for the reasoning**, because each amendment records a way the first draft would have lost information.

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
