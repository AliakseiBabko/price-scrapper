# Backlog — audit the whole class of check, not just the assembly layer

**Opened 2026-09-09**, as the closing follow-up of the `ai-management` dialogue
`VECTOR_PLAN_TO_MODEL_EXTRACTION` (closed, C-01 and C-02 met, verification
`pass`). The dialogue's own plan §4.10 records it as **non-blocking**.

> **Codex's closing position, and it is the right scope call:** C-02 covered the
> assembly/corner model, coordinate provenance and the two gates. Widening it to
> unrelated validators would have retroactively changed the criterion's scope.
> So this is a new piece of work, not an unfinished one.

## ✅ Slice 1 done — 2026-09-09

**Seeded `cost_rollup.py` and `check_room_rollout.py`. Four real false passes
found, all fixed, 13 regression cases added** in
`scripts/tabular_gate_selftest.py`.

| seed | before |
| :--- | :--- |
| `qty = nan` in `bom.csv` | **exit 0**, and the bottom line printed **`nan–nan BYN`** |
| an extra CSV cell in `bom.csv` | exit 0 |
| `kind` misspelled `openning` | **exit 0**, and the opening became finishable wall area |
| a duplicate `seq` / an extra cell in `room_rollouts.csv` | exit 0 |

⚠️ **The money one is the finding.** `parse_range()` wrapped `float()` in
`try/except ValueError`, and `float("nan")` does not raise — so a single bad cell
propagated to a total that was not a number, silently, exit 0. That breaks the
tool's own first rule (*never a fabricated precision*) in the worst way
available. It now fails closed and names the row.

**And one prediction of mine was WRONG, which is the most useful thing here.** I
expected `check_room_rollout.py` to swallow a nan length. It rejected it — because
its test is `ok = abs(d) <= tol`, and nan makes that False. The assembly
validator's area test was `if abs(got − want) > tol: complain`, and nan made
*that* False too, which **passed**. → **Whether a nan is caught or swallowed
depends on which way the comparison is written.** That is far too subtle to leave
at each call site, which is why `tools/lib/tabular.py` now exists and why
`finite()` belongs there rather than in each tool.

**Remaining:** `dimension_tolerance.json` (untested), plus the ~19 other
`csv.DictReader` call sites that still drop stray cells. `tools/lib/tabular.py`
is wired into two tools so far.

---

## Why this exists

Five adversarial rounds against **one** validator found **5 → 3 → 3** real
defects. The rate did not fall as fast as the fixes accumulated, and the defects
were not one-off bugs — they were **two repeatable failure families**:

1. **A recomputed value can agree with an invalid value.** `float('nan')` parses,
   and every comparison against nan is False — so `abs(nan − recorded) > tol`
   *reports agreement*. And the shoelace formula integrates a self-intersecting
   polygon happily, the crossed lobes cancelling to a plausible total. **A
   recomputation only vouches for input the code has already proved usable.**
2. **Mutually consistent cross-references can still be invalid.** A BOM inside an
   identifier, used consistently in all three files, satisfied every referential
   check because both sides of every join were equally wrong. **Consistency is
   not validity**; a validator built only from cross-references cannot see a
   uniform corruption.

⚠️ **And `tools/verify_batch.py` did not catch the BOM**, despite having a BOM
check — it scans only files *changed between two refs*, so it is not the gate for
data already committed or sitting in a working tree.

## The three untested surfaces

Named in plan §4.10. **No claim is made that they are clean; they were not
tested.**

| surface | why it has the same shape |
| :--- | :--- |
| `data/canonical/dimension_tolerance.json` | holds recomputed-vs-recorded comparisons throughout (area closures, developer-vs-measured deltas) |
| `data/canonical/wall_opening_spans.csv` | cross-references `wall_id` and `opening_id` against two other files, with no value validation |
| `tools/layout/check_room_rollout.py` | its whole result is a closure comparison — "the loop must close on both axes" |

## What to do, per surface

Seed each of the families that actually found something:

- non-finite and malformed numerics (`nan`, `inf`, empty, text)
- exact row shape — extra cells (`csv.DictReader` drops them without `restkey`)
  and missing cells (they become `None`)
- an invalid identifier used **consistently on both sides** of a join
- degenerate data that still satisfies the final comparison — a zero area, a
  self-touching loop, two matching zeroes

**Record every demonstrated false pass, then add a regression case with its
repair** — the pattern `scripts/structural_assembly_selftest.py` already
establishes, and `scripts/verify_batch_selftest.py` before it.

## The standard this leaves behind

Worth keeping whether or not this backlog is picked up:

- **A validator nobody has watched fail is not yet a validator.**
- **A validator that has only been watched to PASS is not one either** — and the
  way to find out is to have someone else write the seeds. I wrote 14 and
  believed them; the six that mattered came from outside.
- **An accidental rejection is not a check.** A duplicate id was being caught by
  an unrelated rule about walls; with slightly different data it would have
  passed.

## Reference

- Plan: `ai-management/management/VECTOR_PLAN_TO_MODEL_EXTRACTION_IMPLEMENTATION_PLAN.md`
  §4.10 (and §4 for the accepted design this came out of).
- Closing review: `.../reviews/VECTOR_PLAN_TO_MODEL_EXTRACTION_CODEX_ROUND-05_2026-09-09.md`.
- The 26-case suite that came out of it: `scripts/structural_assembly_selftest.py`.
