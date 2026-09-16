# Draft target records

**Pass 2 of the services migration.** The ledger beside this folder adjudicates
SOURCES; these tables hold what the migration PRODUCES. The two are separate on
purpose — *"is this a fact at all, and whose?"* is a different question from
*"what exactly does it claim, and how well?"*, and answering both at once is how
a reviewer does both badly.

## Keys

Every record carries a **provisional `migration_key`** and its `source_locators`
(semicolon-separated), plus a `target_concept` from: `occurrence`, `assembly`,
`observation`, `assertion`, `value`, `approval`, `connectivity`, `route`,
`relation`.

> ⚠️⚠️ **NO `identity_uuid` IS MINTED HERE.** A UUID is forever by construction —
> the IFC `GlobalId` derives from it — so minting one for a record that may still
> be split, merged or withdrawn would give permanent identity to a provisional
> judgement. UUIDs come after these records are reviewed.

## What the gate requires

`tools/services/check_migration_coverage.py --require-complete` checks **both
directions**: every target cites a real locator, and **every in-scope locator is
cited by at least one target**. Adjudicating a source is not carrying it forward.

**`contradicted` and `retracted` sources still need targets** — they survive as
history. `out_of_scope` is the only ordinary case needing none.
