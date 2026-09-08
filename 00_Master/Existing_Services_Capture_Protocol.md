# Capturing existing services from photos — who does what, and why photo-only failed

**Written 2026-09-08**, answering the owner's question: *"to put existing electric outlets and switches
to the walls, what do I need to do? … I tried to show the photos, the real photos to the model, and it
wasn't able to find right positioning on the 2D plan. The positioning was wrong. … will photo plus my
description be enough to get something reproducible for future photos?"*

**Short answer: yes, and the division of labour is the whole trick. You assign the wall; the model reads
the wall.** You do not need to analyse every photo yourself. You need to supply the one thing a photograph
physically cannot contain.

---

## 1. ⚠️ Why the model got the positioning wrong — and why "more guidance" will not fix it

It was not a capability failure. **The information is not in the image.**

| what you asked the photo to establish | can a photo establish it? |
| :--- | :--- |
| **which wall this is** | ❌ **No.** Never. See below |
| how many sockets, and their grouping (single / double / triple) | ✅ Yes, reliably |
| what kind of device it is | ✅ Yes |
| the order of devices along the wall | ✅ Yes |
| a device's **height in mm** | ⚠️ Only if something of known length is in the same plane |
| this flat's dimensions | ❌ No — these are photos of *other* flats. See §5 |

**Wall identity is unrecoverable from a photo of this apartment type, for three compounding reasons:**

1. **The flat repeats.** Three habitable rooms, several plain plastered walls, no finishes yet, no
   furniture. A blank wall with two low sockets is visually consistent with a dozen wall faces.
2. **⚠️⚠️ THE BUILDING CONTAINS BOTH HANDEDNESSES.** It is two mirrored blocks, and **three of the four
   surveyed flats are mirrored relative to ours** (109, 53 mirrored; 2 same). A mirrored photo read as
   this layout puts every device on the opposite wall — and `Photo_Evidence_Request.md` records that
   **mis-assignment is the dominant error in this model**: four figures retracted in two days, each *"a
   real number attached to the wrong element."*
3. **Nothing in frame is unique.** Sockets, switches and plaster look the same everywhere.

> **→ So no amount of prompting, examples or fine-tuning makes a photo self-locating. The fix is not a
> better reader; it is an index that says which wall each photo shows.** That index is
> `data/canonical/photo_positions.csv`, it already covers **27 photos**, and it is the reason the survey
> photos *did* produce usable findings while loose photos did not.

---

## 2. What you actually need to say — the dictation template

**Per wall, one line. This is the whole protocol.**

```
<room>, <wall code>: <count> <device>, <height band>[, <where along the wall>]
```

Real examples in exactly the form that works:

```
кухня-гостиная 24.73, G3: 2 sockets, low, near the window end
кухня-гостиная 24.73, G3: 1 switch, switch height, right of the door
кухня-гостиная 24.73, ПОТОЛОК: 2 ceiling light points
прихожая 9.79, R2: 1 smoke detector, ceiling
туалет 1.24, G4b: 1 sewer stub + hot and cold capped, low
```

**That is enough.** You do not need millimetres, and you should not guess them — see §3.

### The three things that make a line usable

1. **The room string, copied exactly** from `device_counts_per_wall.csv` (e.g. `кухня-гостиная 24.73`).
   The validator rejects anything else, and prints the valid wall codes for that room when you get one
   wrong — so a mistake is self-correcting rather than silent.
2. **The wall code** — `G3`, `R2`, `M6b`, or `ПОТОЛОК` for ceiling and `ПОЛ` for floor. These are your
   own colour-marking codes, already the key in `device_counts_per_wall.csv`.
3. **Which photo you are looking at**, if any — its `photo_id` from `photo_positions.csv` (`add8`, `930d`,
   …). If you are stating it from memory or from the developer's spec rather than a photo, say so and it
   is recorded as `owner_statement`. **Both are legitimate; conflating them is not.**

### Height bands — say the band, not a number

`floor` · `low` (~300, socket at skirting level) · `mid` · `worktop` (above a kitchen worktop) ·
`switch` (~900–1100) · `high` · `ceiling` · `unknown`

**`unknown` is a perfectly good answer** and far better than a guess.

---

## 3. When a millimetre figure is allowed

Only when **something of known length is in the same plane as the device.** Then everything in that plane
is measurable by ratio, and the validator requires you to *name* the reference.

The model already knows these lengths — from `Photo_Evidence_Request.md` §2:

| room | known length in frame |
| :--- | :--- |
| middle room / living room, window wall | **O2 / O3 opening = 1800 wide** |
| туалет | wall width **1140**; V1 shaft **700 × 400** |
| ванная | depth **1800** |
| the 9.36 room | width **1795** |
| anywhere with a column | concrete **250**, partition **75**, the step **175** |

**No reference in the plane → no number.** `data/canonical/electrical_existing.csv` already carries rows
that say exactly this: *"Heights not measured — the shot is oblique with no independent scale in the wall
plane."* That is the honest outcome, and the gate enforces it rather than letting a plausible-looking
number through.

---

## 4. Where it goes, and the gate

**`data/canonical/services_observed.csv`** — one row per device group, covering electrical, plumbing,
heating and ventilation, so the same protocol serves the work you are doing now on heating and next on
electrics.

```bash
python tools/canonical/validate_services_observed.py
```

**Five rules, each blocking a failure that has already happened here:**

| rule | what it stops |
| :--- | :--- |
| room + wall code must already exist in `device_counts_per_wall.csv` | inventing a wall by typing it |
| `height_mm` or `along_wall_mm` requires a named `scale_ref` | a number with no scale behind it |
| `along_wall_mm` requires `along_wall_ref` | "600 along the wall" — from which end? |
| `handedness: mirrored` requires `mirror_applied: yes` | the dominant documented error |
| a dimension from another flat may not be `confidence: high` | treating a bound as a refinement |

---

## 5. ⚠️ The limit that does not go away: this flat is not built

**Every photo available is of another flat.** So per `Photo_Evidence_Request.md` §1 and
`Geometry_Variance_Study.md` (measured deltas **−45 to +30 mm**):

- **Strong** — *what exists at all*, and *building-wide standards*: how many sockets the developer fits on
  a wall, at what band, whether stubs are capped, what the extract outlet is. **These do not vary flat to
  flat; they are how the developer builds.** This is exactly what you are capturing, and it is the
  strongest thing a photo of another flat can give.
- **Weak** — *this flat's* exact positions. Another flat bounds them; it never refines them.

> **→ So the goal of this exercise is a correct INVENTORY and correct WALL ASSIGNMENT, at band-level
> heights. That is genuinely achievable from other flats' photos and it is what the drawings need.
> Millimetre positions for our own flat wait for access, and nothing downstream is blocked on them.**

---

## 6. The faster path you already have, for verification alone

If the goal is just to **check what I derived** rather than to place devices:
`data/canonical/device_counts_per_wall.csv` has **50 rows** already, with paired columns —
`i_drew_sockets_220` / `YOUR_sockets_220`, and the same for `power_380` and `switches`.

**Every `YOUR_*` column is currently empty.** Filling them, wall by wall, corrects my derivation with no
new tooling and no protocol at all. **That is the cheapest possible verification pass** — and it is
independent of the placement work above.

---

## 7. So: what do you need to do?

1. **Nothing new for heating** — carry on as you are.
2. For electrics, per wall, dictate the one-line form in §2. **Give me the wall code and the photo id; I
   will read the devices off the photo.** You are not signing up to analyse every photo.
3. If a photo shows a known length in the wall plane, mention it and heights become real numbers.
4. **For any photo not yet in `photo_positions.csv`, it needs a row first** — which flat, which room,
   view direction. Without that the photo cannot be cited, by anyone, ever.
5. Run the gate. It tells you what is wrong and prints the valid wall codes when you miss one.

**Reproducible for future photos: yes — but the reproducible part is the index and the template, not the
image reading.** The template makes your description machine-checkable; the index makes the photo
locatable. The model's contribution is counting and identifying, which it does well. Locating is yours,
because only you know where you were standing.
