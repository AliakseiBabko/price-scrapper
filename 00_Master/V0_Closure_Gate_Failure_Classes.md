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
