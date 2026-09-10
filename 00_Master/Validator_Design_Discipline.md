# Validator design discipline — and what "done" means

**Opened 2026-09-10**, from the closed `ai-management` dialogue
`V0_DXF_RASTER_FIDELITY` (six review rounds, `price-scrapper@22aa190`) and the
earlier `VECTOR_PLAN_TO_MODEL_EXTRACTION` (five rounds). Both were adversarial
reviews of *checking code*, and between them they produced the same handful of
failures over and over.

This page exists for the same reason `Evidence_Reading_Discipline.md` does:
**writing a rule does not install it.** One class below appeared **four times in
six rounds**, and twice inside the code written to fix its previous appearance.
Read Part 1 before writing a check, and Part 2 before reporting anything as
finished.

---

## Part 1 — the failure classes, with how often each actually recurred

Ordered by recurrence, not by severity. The count is the point: each of these
was understood, written down, and then committed again.

### ⚠️⚠️ A collection that deduplicates destroys the defect being checked — **4×**

| where | what it hid |
| :--- | :--- |
| `walls_from_dxf` returned a **dict keyed by label** | a duplicate wall overwrote the original; the count never moved |
| the label-parity check called **`set(label_names(...))`** | a duplicate label collapsed 26 entities to 25 names |
| `read_placement()` returned a **dict keyed by `wall_id`** | a duplicate placement silently won, so the absolute anchor compared against the wrong one |
| every canonical table read as **`dict((r['wall_id'], r) …)`** | a byte-identical duplicate row, last-wins |

The fix is always the same shape: **keep the raw sequence, assert the property,
and only then build the index.** If you are checking that something appears
exactly once, you may not use a container whose contract is that things appear
at most once.

**The trap:** the second and third instances were in the checks written to catch
the first. A parity check built on a set cannot see a duplicate.

### ⚠️⚠️ Printing is not checking — **3×**

- `build_wall_corners.py` printed `solid_mm == clear_mm + owned corners` for
  weeks without asserting it. `R8` was wrong by 300 mm the whole time.
- `export_v0_dxf.py` printed *"drawn == solid_mm: 14 of 25 walls within 15 mm"*
  every run, and it was read past and reported as agreement.
- the closure gate printed *"26 named walls"* on the same line as *"25 label
  ENTITIES"* and then declared every wall present exactly once.

**If a number is worth printing, decide whether a wrong value should fail. If it
should, assert it. If it should not, do not print it beside numbers that are
asserted** — putting a row count next to two entity counts is what let 26 sit
next to 25 unchallenged.

### An accidental rejection is not a check — **2×**

A seeded defect that "fails" because the tool **crashed** proves nothing, and it
reads as coverage. One gate rejected a malformed wall with
`NameError: findings referenced before assignment`; a selftest seed shrank the
wrong end of a wall and the gate was right to accept it.

**Every negative case must fail for the reason it names.** Check the message,
not just the exit code.

### A seed that cannot fail is worse than no seed — **2×**

A stale-artefact seed was written as a copy-mutating case, but the staleness
check is deliberately scoped to the *committed* artefact — so the seed mutated a
temporary file nothing looked at, and passed while testing nothing. Earlier, a
"whole-model shift" seed moved only the first six walls, which *breaks*
junctions, so it tested the opposite property and passed for the wrong reason.

**Before adding a seed, break the check on purpose and watch it fail.** A green
suite of seeds that cannot fail is the most expensive kind of false confidence.

### An input a fixture cannot mutate reads as covered and is not — **1×, and it was the anchor**

One reader ignored the injectable canonical-directory argument, so the gate's
**only absolute anchor** against a rigid displacement was the single input no
seeded fixture could reach. A probe against it could never have failed.

**When you add an injection point for testing, assert that every reader honours
it.** This was found by a self-audit, not by a review — nothing would have
surfaced it, because the suite looked complete.

### A checker must not share an editable measurement with the thing it checks — **2×**

- The extent check compared the DXF against `wall_blocks.csv`. Editing both
  together — an ordinary coupled correction — made a wrong extent
  self-consistent, and it even preserved the separate `clear + corners = solid`
  invariant.
- The stale-drawing check authenticated a **sidecar** that asserted, without
  evidence, that it described the delivered image. Replacing only the image
  passed. A digest stored in that same sidecar would not have helped either.

**Derive the expected value from something the artefact's author does not edit,
or recompute it.** Here: hatched solids re-read from the source PDF with its
sha256 asserted, and expected image bytes recomputed by re-running the renderer.
Two things a person edits together agreeing proves only that they agree.

### Anything a reader will trust must be derived, never hand-maintained — **2×**

A review drawing's "Still open" caption was prose in the renderer. It went stale
twice — claiming a wall was absent while the drawing showed it, then claiming the
лоджия was open while it was closed. **The first fix was to edit the words, and
that was the wrong fix**: a caption a person maintains drifts every time the
geometry moves, and the owner reads the caption.

### Fail closed on a contract, rather than cope with arbitrary input — **1×**

A wall polyline was reduced to its bounding box by two readers, so a closed
triangle on three of a rectangle's corners kept the label, layer, bbox and
nominal size, lost half the body, and passed both gates. Nothing downstream
could have caught it, because by then the real polygon was gone.

The exporter draws rectangles, so the reader now **refuses** anything that is not
one. Handling arbitrary polygons would have been a larger change with more
places to be subtly wrong.

### Consistency is not validity, and an area is not evidence

A BOM identifier carrying an invisible character satisfies every join, because
both sides are equally wrong. A shoelace area integrates a self-intersecting
polygon happily, lobes cancelling. `float('nan')` parses and then defeats every
comparison it reaches, so `if abs(got - want) > tol: complain` reports
**agreement** on nan input. Use `tools/lib/tabular.py` — `read_csv()` and
`finite()` — not `csv.DictReader` and `float()`.

---

## Part 2 — indicators that a job is done

Different kinds of work finish differently, and the failure has been to report
one kind as though it were another. **Name which kind you are doing.**

### Deliverable work — the model, the geometry, the drawing, the data

**Done when:** a named gate that is *capable of failing* passes, every generated
artefact has been regenerated, and the change appears in a **declared
deliverable path** (`data/canonical/`, `data/cad/`).

**Indicator:** a file under a deliverable path changed.
**Anti-indicator:** the diff touches only `tools/` and `scripts/`.

### Apparatus work — gates, checkers, selftests, tooling

**Done when:** a seed that **previously passed** is now rejected **by the check
and not by a crash**, the seed is permanent in a suite, the class it belongs to
is named, and the real artefact still passes.

**Indicator:** the suite's seed count went up, and you can say which class each
new seed belongs to.
**Anti-indicator:** "I improved the checker" with no seed, or a seed whose
failure you did not personally watch.

⚠️ **Apparatus work is legitimate and it is not progress on the deliverable.**
Both `ai-management` dialogues reached a state where every round found a real
defect and the thing being built had not moved for rounds — because the defects
were all in the checking code, and half of them in the previous fix. Track the
two separately; the cross-agent side of this is enforced by
`--deliverable-path` / `--apparatus-rounds` in the `management-plan-dialogue`
coordinator, capped at **three** consecutive apparatus-only rounds.

### Planning work

**Done when:** the next action is unambiguous, and every open question is
assigned to whoever can actually answer it.

**Indicator:** two rounds, at most. A third means the disagreement is about
approach and should be settled directly, not iterated.
**Anti-indicator:** new ideas arriving with no owner; an open item that has been
restated in three successive versions.

### Review work

**Done when:** it produces either a finding that **reproduces against the
committed state**, or an explicit record that it found none.

**Indicator:** you re-ran the thing. Every round in these dialogues that was
worth its tokens found something by *executing* the committed state; the one
that reported a passing gate by reading its own intent was wrong on three counts
at once.
**Anti-indicator:** a review that re-reads and comments. That is not a round; a
round with no finding is the signal to stop.

### The universal ones

- **A gate nobody has watched fail is not a gate.**
- **An assertion you cannot make fail on purpose is decoration.**
- **A criterion that no finite evidence can satisfy will never be met** — see
  the withdrawn `C-01`, whose *"adversarially validated rather than
  self-reported"* could be refuted by one failing seed and established by no
  number of passing ones. Enumerate the classes instead of the sentiment.
- **Report the outcome, not the intent.** *"The gate passes"* must mean it was
  run, in the committed tree, since the last change.

---

## What this cost, so the next reader believes the counts

`V0_DXF_RASTER_FIDELITY`: six review rounds, **every one** finding a real
reproduced defect; **24 + 7** permanent adversarial seeds, every one of which
exists because something passed. `VECTOR_PLAN_TO_MODEL_EXTRACTION` before it:
five rounds, four false passes in one slice of unrelated validators, including a
cost roll-up that printed **`nan–nan BYN`** and exited 0.

Ten extent exceptions in `data/canonical/wall_extent_exceptions.csv` remain
**open** — recorded disagreements between the record and the drawing, pinned so
they cannot drift. That is containment, and it is not resolution; the page that
tracks the geometry itself is `V0_Geometry_Status.md`.
