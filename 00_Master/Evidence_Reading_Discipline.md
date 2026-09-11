# Reading evidence — seven failures and the checks that caught them

**Written 2026-09-07**, from four days of building the flat's geometry model with the owner correcting it
in real time. Every item below is a real error I made and he found, or a check that worked.

**The point of the page is not the list. It is that all seven failures are the same failure**, and one
short check in front of each would have prevented six of them.

---

## 1. The one error family

| # | what I claimed | what it was |
| :--- | :--- | :--- |
| 1 | `G3 = 3315` | the 3315 runs from the shaft to R2, not from the R3\|G3 split |
| 2 | `G4b = 1140` | the 1140 is the туалет's width, not the wall's length |
| 3 | retracting `R1a` because 1795 "is the 9.36 room's" | it is **both** rooms' — same two bounding verticals |
| 4 | `V1 = 1140 × 490` | the 490 is the wall segment beside the O7 door |
| 5 | O3 sill `538` | I read the sill board, not the frame base — the tape says 266 |
| 6 | a `110` sewer socket | it is DN50; I measured the plastered blob around it |
| 7 | the floor stencil reads `ОТОПЛЕНИЕ` | it reads `ВОДОСНАБЖЕНИЕ` |

**⚠️⚠️ The diagnosis, and it is the same every time: I had a hypothesis before I had the evidence, and
the evidence got read to fit it.** The building spec mentions heating, so a blurred stencil said heating.
A shaft needs a footprint, so the nearest two numbers became its footprint. A kitchen needs a sewer, so
the nearest pipe became a 110 socket.

> [!WARNING]
> **Number 4 is the one that should worry a future reader.** I committed it *after* writing the check
> against it — "identify both elements a dimension's extension lines terminate on" — in the same
> session. Writing a rule does not install it. **The rule has to be a step you take, not a paragraph you
> have read.**

---

## 2. Two failure modes that are not the same as the above

**Over-correction.** After being wrong three times about mis-assigned dimensions, I retracted a *good*
figure on a pattern match (#3). **Having a known weakness makes you wrong in the other direction too.**

**Circular validation, which is worse than a wrong number** (#6). I measured an object, got 113 mm, and
wrote *"113 reads as a standard 110 socket, which is the check that the scale is right."* That used the
object being measured to validate the scale that produced the measurement — and dressed the coincidence
as verification. **A wrong number that is flagged is safe. A wrong number wearing a cross-check is not.**

---

## 3. The checks that actually caught things

| check | what it caught |
| :--- | :--- |
| **Chain closure** — do the parts sum to the whole? | the west edge to **36 mm**, G4C to **34**, the room rollout's north–south axis **exactly**, the divider's 2340 |
| **Shoot square-on** | 9902 falsified an oblique sill reading it could not itself replace; the tape later confirmed which was wrong |
| **A manufactured standard as the scale** — a door block, a socket plate, a WC rim | the ceiling height, by two routes using no ceiling assumption |
| **Functional plausibility** | DN110 is for a WC; there is no WC in a kitchen. The owner saw it in one line, before any pixel |
| **A re-runnable script, not a habit** | the crossing sweep found `G2 × G4C`, which nobody was looking for |
| **sha256 on a file collection** | three photos were duplicates, and the earliest window measurements came from a **mirrored** flat |
| **Confidence drawn, not written** | the services plan: solid = located here, dashed = pattern only, ✕ = unknown |

---

## 4. The checklist

Before using any dimension read off a drawing or a photo:

1. **What two things does it terminate on?** Not "what is it near". Six of the seven failures die here.
2. **What could this plausibly be?** A dimension that contradicts function is wrong even when the pixels
   agree.
3. **What is my scale, and is it independent of the thing I am measuring?** If the answer is "the object
   tells me", stop.
4. **Does it close?** Sum the parts against a known whole. This is the only check that is arithmetic
   rather than judgement, so prefer it over everything above where it is available.
5. **If it disagrees with the drawing by roughly a wall thickness, suspect the convention**, not the
   drawing. Twice I invented a junction defect that was my own arithmetic.
6. **Is the photo square-on?** If not, verticals are still usable and horizontals are not — a horizontal
   rotation does not foreshorten a vertical.
7. **Which flat is this?** Mirrored is the default failure. Heights survive mirroring; left and right do
   not.
8. **If I registered a raster, did I verify on a SECOND printed dimension?** Register the scale on one
   printed figure — preferably a long one — then measure a *different* feature elsewhere on the sheet and
   check it against its own printed value. ⚠️ **This is not item 4.** Chain closure asks whether a run of
   dimensions sums to a known whole; this asks whether the **registration itself** is right, against a
   figure that played no part in establishing it. Both can be needed, and passing one says nothing about
   the other.
9. **How thick is the line I measured to?** A drawn wall face is ink with width, so decide before you
   start whether you are reading to its centre, its inner face or its outer face — an unstated choice is
   an unstated error, and at plan scale the stroke can be the same order as the tolerance being claimed.

> [!NOTE]
> **Items 8 and 9 were added 2026-09-11 from two practitioners**, not from a failure here — Justin Geis
> (TheSketchUpEssentials) and Aaron Dietzen (Trimble SketchUp), via
> [`Drawing_Conventions_From_Practice.md`](Drawing_Conventions_From_Practice.md) §6. **Item 8 is the only
> check in either research batch this project did not already have.** Dietzen also states item 3's rule
> from the other side and more strongly than it is written above: *"it doesn't matter how good the
> information you get… always double-check against printed dimensions of some sort."*

---

## 5. What to write down, and how

- **An item can be CLOSED without being ANSWERED.** The R3\|G3 split is unknowable — it is under
  finishes. Leaving it "open" implies someone should keep looking when looking will not help.
- **An unexplained residual is a QUESTION, never a new element.** I gave two residuals ids (`Z1`, `Z2`),
  drew them, and wrote them into a canonical file. Naming a residual is how it stops being questioned.
- **Record the retraction, not just the correction.** Every entry above survives in
  `data/canonical/wall_materials.json` with what was claimed, who found it and why it was wrong. That is
  what makes the *pattern* visible; individually they look like bad luck.
- **State the error bar and its cause.** "±50, because the raster is good to 5 px" is usable. A bare
  figure is not, and a false-precision figure is worse than a range.

---

## 6. Two things the owner did that are worth imitating

**He measured rather than argued.** Given a disputed figure he produced a tape reading, a product photo,
or a second flat. Every one of the seven was settled by evidence, not by discussion.

**⚠️ And he tested my *reasoning*, not just my numbers** — "compare R1a|R1b with R7|MC" found a
convention error, not an arithmetic one. **That is the class of mistake a model cannot self-check**, and
it is the reason the corner ledger, the successor grouping and the two-length scheme exist at all.
