# v0 closure gate — the defect classes it did not catch

Every check in `tools/layout/check_dxf_closure.py` exists because a specific mutation passed the gate without it. This page is the record of which ones, seeded by whom, and what each exposed. It is kept separate from `V0_Export_And_Closure.md` because the useful content is the failure taxonomy, not the export procedure: a gate nobody has watched fail is not a gate, and a gate that passed someone else's seed was not the gate I reported.

## Round 2: five of those claims were not true in the committed tree

CODEX re-ran the round-1 artefact against `price-scrapper@cd4e0c8` rather than
reading it, and **C-01 was still unmet.** Every one of the five findings
reproduced on the first attempt. They are recorded here because the pattern
matters more than the individual bugs: **each was a claim I made about code I
had written, verified by reading my own intent rather than by running it.**

| what round 1 claimed | what the tree did |
| :--- | :--- |
| M6b placed, лоджия closed | `place_named_walls.py` **crashed**, `TypeError: 'NoneType' object is not subscriptable`; the DXF held **24 labels** |
| overlay exits 1 on breach | `return 0` unconditionally, printing five breaches |
| six seeded defects rejected | true — but three CODEX seeds **passed** |
| a near-miss check | documented in the header, **never implemented** |
| the review PNG is current | it still read *"M6b absent … the лоджия does not close"* |

### Why the three CODEX seeds passed, and what each one exposed

Not thresholds needing a nudge — three structural holes:

- **A complete 500 mm shift.** Every assertion in the gate was *relative*:
  corner coverage, overlaps and cavities are internal to the DXF, so translating
  the whole drawing satisfies all of them. **My own shift seed moved only the
  first six walls**, which *breaks* junctions — so it tested the opposite thing
  and passed for the wrong reason. Fixed by anchoring each wall's **cross-axis
  faces** to `v0_named_walls_placed.json`; `close_corners` only ever moves a wall
  along its own axis, so faces are exact. A seed for a slide **along** a wall's
  own axis is now in the selftest too, since faces cannot catch that one.
- **A duplicated wall.** `walls_from_dxf` returned a dict keyed by label, so the
  copy overwrote the original and the count never moved. Fixed by returning a
  **list** and asserting one polyline per label. *Presence was being read off an
  index that could not represent the defect.*
- **A 1000 mm over-extension.** It ran into open room, so it opened no cavity
  and overlapped nothing. **Length was never asserted, only printed.**

### The extent check found nine open disagreements, and they are not fixed

Asserting drawn length against `solid_mm` immediately failed on **11 walls**,
deltas from **−910 to +250 mm**. That is not news the gate discovered: the
exporter has printed *"14 of 25 walls within 15 mm"* every run since it was
written, and **I read past it and reported the export as agreeing.** Printing is
not checking — the identical error `build_wall_corners.py` made with its own
invariant.

They are neither silenced nor edited away. Each is pinned in
`data/canonical/wall_extent_exceptions.csv` with its measured delta and a cause,
and the gate **fails on any deviation from the pinned figure**. So the debt is
countable, a wall not on the list must agree, and CODEX's mutation still fails
because it moves a delta. **Nine remain `open`:**

- **G4d −910 / G4b −120** — G4b's recorded 1915 equals G4d's *drawn* 1915. That
  is what a transposition looks like, and G4b's 120 is also exactly its
  `resolve_overlaps` trim against R1b. **The two hypotheses are not separated.**
- **R8 −300 / R9 −250** — both own corners whose gain the clamp correctly
  declined to add, because the placed run *already* covered the abutting wall's
  band. So `clear_mm` as read off the vector is not a face-to-face inner
  dimension, and `clear + owned corners` over-counts. Same root as the standing
  R6–R9 length question.
- **MA +225, G7 +250, M2 +165, R1b +145, G4C −120** — the drawn extent
  terminates on the faces the ledger prescribes, so the *record* is the suspect
  number. I can state which two faces the vector terminates on; I cannot state
  which figure is right.

### A 10 mm gap nobody had ever seen

The near-miss check, once actually implemented, found **MA × R6 10.3 mm apart** —
a butt joint the owner would read as one of the cavities he has now asked about
three times. At an order of magnitude below the ±50 build tolerance it is
extraction noise, not a design question, so `snap_near_misses()` closes any
sub-25 mm perpendicular gap by extending the **lesser** wall (thinner, then
shorter) and reports it. **A gap above that floor is left alone deliberately:**
the gate fails and the owner decides, which is exactly what happened with
`J_G4a_G4b`.

### And M6b had to yield

Placing M6b from R8's *pre-extension* start, then closing R8's corner onto MB,
drove R8's drawn body **50 mm into M6b**. Reordering does not fix the general
case, because a directive is written against a declared face and corner closure
legitimately moves drawn extents afterwards. The rule is an ordering of
authority: **quarantined geometry never displaces accepted geometry.** M6b is
trimmed back to abut, keeps its face alignment, loses 50 mm, and the loss is
reported — a quarantined wall that has lost length is a fact about the
unresolved thickness, not a detail.

### Still open after this round

**The лоджия is not a closed loop even with M6b present.** The glazing run is
drawn at the vector's true splay angle while M2 and M6b are axis-aligned boxes,
so it floats detached from both. The review PNG now says so instead of claiming
the opposite.

## Round 3: two more false passes, and both were the same shape

CODEX seeded again and two probes went through. Neither was topology, and
neither was a threshold that needed tightening — both were **the gate believing a
table a person maintains.**

### The extent oracle moved with the defect

It extended MC by 1000 mm in an isolated fixture **and** edited MC in the copied
`wall_blocks.csv` from `clear_mm=3315, solid_mm=3565` to `4315/4565`. Exit 0.
Faces did not move, the junction stayed filled, nothing overlapped, and the drawn
length agreed with the altered table — and the coupled edit even preserves
`build_wall_corners.py`'s invariant, because `4315 + 250 = 4565`.

Its statement of the problem is the one worth keeping, and it is careful:

> *This is not a demand that a checker resist malicious rewriting of every input;
> it is a finding that the export and its purported extent oracle share the same
> editable measurement, so an ordinary coupled correction can make a wrong extent
> self-consistent.*

**The answer was to stop treating `wall_blocks.csv` as evidence of extent.**
`tools/layout/vector_extent_oracle.py` re-derives the hatched wall solids from
`3Б_3+ МН5_287.pdf` at check time and asserts no wall is drawn past its own solid
by more than the corner allowance — which is itself taken from the drawing's
thickest solid, not from `wall_corners.csv`. The PDF's sha256 is asserted, so
substituting the drawing is caught too. MC + 1000 mm now fails by name:
*"runs 1000.0 mm past hatched solid S04 (9380.9..12946.0); the corner allowance
is 400 mm."*

⚠️ **The residual coupling, stated rather than discovered later:** the oracle
shares extraction *code* with `place_named_walls.py`. A bug in `build_runs` fools
both. That is a real limit — but shared code is reviewable and versioned, which
a shared editable measurement is not.

### The exception ledger's evidence was decorative

CODEX set G4a's `drawn_mm` to 1 and `solid_mm` to 99999, blanked `cause` and
`notes`, invented a status, left `delta_mm` alone — and the gate exited 0,
because it read only `wall_id`, `delta_mm` and `status`. Its verdict:

> *the claimed measurements and explanation are not checks — they are decorative
> fields beside an allowlisted delta.*

Every field is now checked: strict CSV via `tools/lib/tabular.py` so a stray or
missing cell is visible, a declared status vocabulary, unique and known wall ids,
a non-empty cause **and** note, and the row's arithmetic recomputed against the
actual DXF and `wall_blocks.csv`. **It caught its own stale rows within the hour**
— closing the лоджия loop moved M2 and M6b, and the ledger refused the old
numbers until they were re-measured.

### And a hole I found by seeding against myself

`--canon` was added so a fixture could mutate canonical data, which let me ask
what else that unlocks. Deleting R4's polyline **and** its `wall_blocks.csv` row
passed: every table-based presence check agreed there were 24 walls. But the DXF
still carried 25 `V0-WALL-LABEL` texts, because **the drawing labels what it
claims to draw.** Label↔polyline parity is now asserted, and it is the one
presence test that needs no table at all.

## The permanent suites, after three rounds

| suite | seeds |
| :--- | :--- |
| `scripts/dxf_closure_selftest.py` | **16**, four of which mutate the DXF *and* a canonical table together |
| `scripts/raster_fidelity_selftest.py` | **6** — translation, 3% scale, endpoint drift, sideways displacement, a deleted wall, a tampered mask |

Every single one exists because something passed.

## Round 4: the reader invented the geometry, and the drawing reported last round

Two findings, both reproduced on the first attempt, and neither was a
measurement error or a table edit.

### The gates replaced the polygon with its bounding rectangle

CODEX replaced MC's four-point rectangular `LWPOLYLINE` with a **closed triangle
on three of the same four corners.** Label, layer, bounding box, nominal length
and nominal thickness all unchanged; **half the wall body gone.** Both binding
gates returned exit 0.

The cause was one line, written twice:

```python
x0, x1 = min(q[0] for q in p), max(q[0] for q in p)
y0, y1 = min(q[1] for q in p), max(q[1] for q in p)
```

`check_dxf_closure.walls_from_dxf()` and `raster_fidelity.dxf_walls()` each
reduced the polyline to its bounding box, and every corner square, cavity scan,
body mask and dense edge sample downstream then reasoned about **a rectangle
nobody had drawn**. The closure gate could report a corner square fully covered
by an entity that does not cover it.

Two properties make this a class rather than an incident:

1. **It is invisible to every later check.** No amount of care downstream can
   detect it, because by then the real polygon is gone.
2. **It was duplicated.** Two readers meant two chances to make the same
   substitution, and fixing one would have left the other.

So there is now **one** reader, `tools/layout/dxf_wall_entities.py`, and it
refuses anything that is not the shape `export_v0_dxf.py` promises: closed,
zero-bulge, axis-aligned, four distinct corners, **and polygon area equal to
bounding-box area**. Coping with arbitrary polygons would have been a larger
change with more places to be subtly wrong; refusing is small, total, and fails
closed. Both suites carry the triangle, so if the readers ever diverge again the
suite that lost the check says so.

### The review drawing still reported the previous round — for the second time

`render_dxf.py` hard-coded *"the лоджия is still NOT a closed loop"* and *"9
walls carry an OPEN extent exception"* while the loop was closed and the ledger
held **10**.

⚠️ **This is the same defect as round 2, and I fixed it the wrong way then.** In
round 2 the caption claimed M6b was absent while the DXF drew it, and I edited
the words. A caption a person maintains drifts every time the geometry moves —
and **the owner reads the caption**, so a stale one is precisely the *"come back
showing the same result"* failure this whole topic exists to prevent.

The fix is structural. `tools/layout/v0_state.py` derives the whole "Still open"
block — open exception count, quarantine, лоджия loop status computed against the
drawing's own glazing axis — from the same canonical data and the same DXF the
gates read. `render_dxf.py` writes what it drew to a sidecar, and
**`check_dxf_closure.py` now fails when that sidecar disagrees with the current
state.** A stale review drawing is a gate failure, not a documentation slip.

Seeded with CODEX's exact stale claims, the gate reports:

```
FAIL open_exceptions: the drawing says 9, the current state is 10
FAIL loggia_loop_closed: the drawing says False, the current state is True
```

⚠️ **The first version of that seed tested nothing.** Written as a `@paired`
case it mutated a temporary copy of the sidecar, which the staleness check never
looks at — it is deliberately scoped to the committed drawing. It would have
passed while checking nothing. A seed that cannot fail is worse than no seed,
because it reads as coverage; hence the separate in-place runner, which also
verifies the artefact is restored afterwards.

## The permanent suites, after four rounds

| suite | seeds |
| :--- | :--- |
| `scripts/dxf_closure_selftest.py` | **19** — four mutating the DXF *and* a canonical table, one mutating a committed artefact in place |
| `scripts/raster_fidelity_selftest.py` | **7** — including the tampered frozen mask |

Every single one exists because something passed.

## Round 5: the same class a third time, and both defects were in the round-4 fix

### A collection that deduplicates destroys the defect being checked

This is now **three instances of one class**, and the third was in the code I
wrote to fix the second:

| round | the collapsing collection | what it hid |
| :--- | :--- | :--- |
| 2 | `walls_from_dxf` returned a **dict keyed by label** | a duplicate wall overwrote the original; the count never moved |
| 5 | the label-parity check called **`set(label_names(...))`** | a duplicate label collapsed 26 entities to 25 names; the gate printed *"25 labels"* for a file holding 26 |
| 5 (self-audit) | `read_placement()` returned a **dict keyed by `wall_id`** | a duplicate placement entry silently won, so the absolute anchor compared against the wrong one |

The round-2 fix was to return a list. **I then built the round-4 parity check on
a set** — the check whose whole purpose was to catch a missing wall without
trusting a table. Labels are entities in a **bijection** with polylines, not a
set of names, and the gate now keeps the raw list, rejects repeated text,
compares raw counts, and prints the raw count beside the distinct one.

### A sidecar-currentness test is not a drawing-currentness test

Round 4 replaced the hard-coded caption with a derived one and asserted a
sidecar against the current state. CODEX substituted **only the PNG** — the
tracked pre-fix blob `8865871` in place of `da4b46e` — left the fresh sidecar
alone, and the gate called the image current. It had never read the image.

⚠️ **A digest stored in the sidecar would not have fixed it**, because the
sidecar is as editable as the PNG and a coupled edit updates both. So nothing
stored is trusted: `render_dxf.py` is byte-deterministic here, and the gate
**recomputes** the expected bytes by rendering to a temporary path and comparing.
The sidecar's `what` field had asserted it described the PNG, without evidence —
which is the same shape as the exception ledger's decorative fields in round 3.

The sidecar now follows `--out`, so the probe cannot disturb the committed pair.
The one honest caveat is in the code: determinism holds for a given font set, so
a machine resolving different fonts reports a mismatch — and the remedy is the
same as for a genuinely stale image, regenerate, which then shows in the diff.

### What the turn-10 self-audit found

Sweeping for the collapsing-collection class rather than waiting for it to be
seeded a fourth time turned up **two defects in one line** of `read_placement()`:

1. it read `CANON` directly and **ignored `--canon`**, so the placement — the
   gate's only absolute anchor against a rigid shift — was the one input no
   seeded fixture could mutate. **A probe against it could never have failed**,
   which is worse than an unchecked input because it reads as covered.
2. the dict collapsed duplicates, as above.

The permanent seed for it now fails on *both* counts — `duplicate_placement`
and `face_drift` — and that second failure is the evidence the isolation reaches
the anchor at all.

## The permanent suites, after five rounds

| suite | seeds |
| :--- | :--- |
| `scripts/dxf_closure_selftest.py` | **22** — five mutating the DXF *and* a canonical table, two mutating a committed artefact in place |
| `scripts/raster_fidelity_selftest.py` | **7** |

Three classes were added beyond C-03's enumerated floor — duplicate label
entity, stale delivered PNG, duplicate placement entry — which is what the
class-based criterion was written to allow.
