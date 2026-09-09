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
