# Geometry variance — the developer's drawing against three measured flats

**Written 2026-09-04 from the owner's readings.** He compared the developer's plan against
`floor plan_1.jpg`, `floor plan_2.jpg` and `floor plan_3.jpg` — measured surveys of **real, completed
apartments of the same layout**, which may be mirrored horizontally.

This is the first time the model has been tested against anything built.

---

## 1. The four comparisons

| dimension | developer | measured | measured | delta |
| :--- | ---: | ---: | ---: | ---: |
| divider run, R3 → R5 *(= G2 → R4)* | **2310** | 2330 *(plan 1)* | 2340 *(other)* | **+20, +30** |
| big room, long axis | **7460** | 7460 *(plan 1)* | 7450 *(plan 3)* | **0, −10** |
| big room width, at the кухня | **3315** | 3300 *(plan 1)* | 3270 *(plan 3)* | **−15, −45** |
| middle room width | **3000** | 2970 *(plan 1)* | 2970 *(plan 3)* | **−30, −30** |

**Spread of deltas: −45 to +30 mm.**

---

## 2. ✅ The 7460 closes the big room completely

```
R2 1675  +  G5 4035  +  R7 1750  =  7460
```

— and `floor plan_1` measures **7460 exactly**, `floor plan_3` measures 7450.

**Three independent routes to one number**: the developer's printed chain, a real flat's survey, and a
second real flat's survey. The big room's east side is settled as firmly as anything in this model.

---

## 3. ⚠️ The sign is not systematic, and that retires an earlier assumption

| | |
| :--- | :--- |
| the divider | comes out **bigger** in reality — +20, +30 |
| both room widths | come out **smaller** — −15 to −45 |
| the long axis | dead on — 0, −10 |

→ **So "the real dimension is usually a little bit bigger" does not hold.** The owner said that when he
first handed over the sources, and it was carried in the repo as a working assumption. **This data does
not support it.** Deviation is roughly symmetric and depends on which dimension, not on a direction of
bias.

→ Practical consequence: **you cannot pre-compensate.** There is no safe direction to round in when
ordering. Anything cut to a dimension has to be measured on site.

---

## 4. ⚠️⚠️ The middle room is the one that matters commercially

```
developer   1800 + 600 + 600  =  3000     ← every term is round
floor plan_1                     2970
floor plan_3                     2970     ← both real flats AGREE
```

**Two independent surveys landing on the same 30 mm shortfall is not noise.** The 3000 reads as a
*nominal* chain — round numbers summed — and the 2970 as the *built* result.

→ **This is the middle room's window wall (MB, carrying O2).** A window ordered to a 1800 nominal
opening in a wall that is 30 mm shorter than drawn is exactly the kind of error that gets discovered on
delivery day. **Measure MB before ordering anything for O2.**

→ It also mildly weakens the divider figure by contrast: the divider deltas (+20, +30) disagree with each
other, while these two agree exactly. Agreement between independent surveys is the strong signal.

---

## 5. The tolerance this repo carries was too tight

`AGENTS.md` said **dimensions nominal ±25 mm**. The observed spread here reaches **45 mm**.

→ Updated to **±50 mm**, and it is now **measured rather than assumed** — which is the more important
change. The old figure had no evidence behind it.

> [!NOTE]
> This is the **build** tolerance — how far a completed flat departs from the drawing. It is not the same
> as the **raster** tolerance used inside `tools/layout/check_wall_junctions.py`, which is about reading a
> JPEG and stays at 25 mm. Two different quantities that happened to share a number.

---

## 6. What this does and does not license

- ✅ **Use the developer's printed dimensions as the model's basis.** They are internally consistent and
  they close, repeatedly — the west edge to 36 mm, G4C to 34 mm, the big room exactly.
- ✅ **Treat any single figure as ±50 mm** when it drives a purchase or a cut.
- ⚠️ **Do not average the developer's figure with a measured one.** The measured flats are *different
  flats*, possibly mirrored; they bound the error, they do not refine the number.
- ⚠️ **Do not use them to settle a dimension the developer's plan leaves open** — R1a, the R3|G3 split.
  A survey of another flat cannot resolve what this one's drawing never stated.
