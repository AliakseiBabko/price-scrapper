# Draft target records

**Pass 2 of the services migration.** The ledger beside this folder adjudicates
SOURCES; these tables hold what the migration PRODUCES. The two are separate on
purpose — *"is this a fact at all, and whose?"* is a different question from
*"what exactly does it claim, and how well?"*, and answering both at once is how
a reviewer does both badly.

> [!IMPORTANT]
> ⚠️ **THE SCHEMA IS DECIDED HERE, NOT INSIDE A VALIDATOR.** This file previously
> defined only the common provenance fields, so the typed columns for
> occurrences, assertions, values and locators did not exist anywhere. Writing
> the validator first would have made every one of those decisions silently, in
> validator code, where nobody reviews a schema.
> `tools/services/check_target_schema.py` **enforces** what this file declares;
> it does not get to invent it.

## Keys

Every record carries a **provisional `migration_key`** and its `source_locators`
(semicolon-separated), plus a `target_concept` from: `occurrence`, `assembly`,
`observation`, `assertion`, `value`, `approval`, `connectivity`, `route`,
`relation`.

> ⚠️⚠️ **NO `identity_uuid` IS MINTED HERE.** A UUID is forever by construction —
> the IFC `GlobalId` derives from it — so minting one for a record that may still
> be split, merged or withdrawn would give permanent identity to a provisional
> judgement. UUIDs come after these records are reviewed.

`migration_key` is **unique across every table** and is a stable handle other
records point at. Prefixes are conventional, not semantic: `OCC-`, `ASM-`,
`OBS-`, `ASR-`, `REL-`.

## One file per concept

The gate unions every `*.csv` in this folder, so each concept gets its own file
and its own typed columns. A column that means nothing for a concept is **absent
from that table**, not blank in a shared one.

| File | Concept | Holds |
| :--- | :--- | :--- |
| `occurrences.csv` | `occurrence` | a physical thing, at most one per real object |
| `assemblies.csv` | `assembly` | a named group that is itself a thing |
| `observations.csv` | `observation` | what was seen, **scoped to the flat it was seen in** |
| `assertions.csv` | `assertion` | every typed claim about a subject |
| `relations.csv` | `relation` | aliases and links between records |

## The locator union, as columns

`locator_kind` is required on every occurrence and is one of:

| `locator_kind` | Required | Must be empty |
| :--- | :--- | :--- |
| `wall_face` | `host_ref`, `face_ref` | the `surface_local` columns |
| `surface_local` | `support_ref`, `surface_role` | the `wall_face` columns |
| `unlocated` | — | **both** sets |

⚠️ **`unlocated` is a real, honest value.** `SV-T` exists and its position is
unknown; recording it as a `wall_face` with blank fields would make "unknown"
indistinguishable from "not filled in yet".

⚠️ **`anchor_ref` is how a PARTIAL placement is recorded.** `W6` is anchored to
opening `O10` because that is what the owner said; the wall, the along-face
fraction and the height are not his. An anchor is not a position — it is the
named thing a position will later be measured from.

⚠️ **`surface_local` is recognised but NOT resolvable.** The compiler publishes
no support-surface registry, so nothing can check a `u_mm`/`v_mm` against real
geometry. The schema validator accepts the shape; the geometry validator must
report **"support geometry unavailable"**, never a pass.

## Assertions carry the uncertainty

The assertion table is where `knowledge_basis` and `value_state` live, **per
claim**, because one occurrence can have observed existence, derived height and
assumed host simultaneously (§7.2).

| Column | Values |
| :--- | :--- |
| `property` | `existence`, `count`, `position_along`, `vertical`, `function`, `voltage`, `route_state`, `gang`, `arrangement`, plus the envelope: `extent_along_mm`, `extent_vertical_mm`, `anchor_mode`, `host_interaction` |
| `polarity` | `affirm`, `negate` — **negation is polarity, not a kind of fact** (§3.0e) |
| `knowledge_basis` | `observed`, `derived`, `assumed`, `stated`, `unknown` |
| `value_state` | `asserted`, `candidate`, `disputed`, `unknown`, `retracted` |
| `scope_kind` | **required.** `apartment`, `unit_type`, `building` |
| `scope_ref` | **required.** The identifier for that kind — `ours` or a surveyed comparable (`53`, `109`, `2`) for an apartment; the type designation for `unit_type` |
| `scope_phase` | `existing`, `proposed` |
| `disputed_with` | the `migration_key` this one contradicts |

⚠️ **Scope is TYPED, and that is deliberate.** An apartment enumeration could not
express the thing §3.0f explicitly allows as a route to established existence —
**a developer document governing this unit type**, which is not an apartment.

⚠️ **This is what makes §3.0f enforceable.** An observation in flat 53 and a
candidate projection onto ours are two rows with different scopes — never one
row with a hedge in a note. The validator additionally refuses an assertion
scoped `apartment`/`ours` with `knowledge_basis=observed` unless an observation
**also scoped to ours** backs it, because that is how a projection launders
itself into a field-verified fact.

## The terminal envelope

⚠️ **An occurrence has an anchor POINT, and a point cannot collide with
anything.** Extent lives in the assertion table so each part carries its own
basis and state, and so the validator never has to **invent default device
dimensions internally** — an assumption made inside a validator is invisible.

| Property | Meaning |
| :--- | :--- |
| `anchor_mode` | what the occurrence's point marks: `centre`, `lower_centre`, `upper_centre`, `start`, `end` |
| `extent_along_mm` / `extent_vertical_mm` | the device envelope. **`value_state=unknown` with an empty value is the honest record** when nothing states a size |
| `host_interaction` | `avoid_void`, `creates_penetration`, `fills_opening` |

**The three-state verdict follows from this, and unknown dimensions are not an
excuse to pass:**

| | Verdict |
| :--- | :--- |
| centre inside a void | **invalid** |
| centre clear, extent unknown | **incomplete** — *not* proven valid |
| full asserted envelope clear | **valid** |

⚠️ **`host_interaction` is why a blanket "a service may not overlap a void" rule
is wrong.** `SV-VT` **is** a hole through G4b — the owner's transfer opening
between the ванная and the туалет. Such a rule would eventually reject the one
element whose entire purpose is to be a penetration. The validator dispatches on
this property and **must not treat its absence as `avoid_void`**.

## What the coverage gate requires

`tools/services/check_migration_coverage.py --require-complete` checks **both
directions**: every target cites a real locator, and **every in-scope locator is
cited by at least one target**. Adjudicating a source is not carrying it forward.

**`contradicted` and `retracted` sources still need targets** — they survive as
history. `out_of_scope` is the only ordinary case needing none.

## Status

**This is a deliberate VERTICAL SLICE, not the full migration.** It exists so the
validators are built against real records instead of against an empty folder.
102 in-scope locators need targets; this slice covers a representative handful,
chosen to include every shape that behaves differently.
