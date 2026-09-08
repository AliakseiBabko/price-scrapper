# The vector plan, and the test that it is our drawing

`_Inbox/_Visual_Drop/3Б_3+ МН5_287.pdf` is the first geometry source in
this project that is not an image — a true ArchiCAD export. **It was issued
for a different unit**, so whether it describes this flat had to be settled by
test before anything could rest on it. It does.

Split out of `Apartment_Geometry_Sources.md` on 2026-09-08, which was within
seven lines of the 400-line backstop. That page keeps the source table and the
tolerance work; this one keeps the test and what the drawing does and does not
carry.

## ✅⚠️ A VECTOR edition of the base case — tested 2026-09-08, and it is the SAME drawing

`_Inbox/_Visual_Drop/3Б_3+ МН5_287.pdf` is a **true CAD export** (ArchiCAD,
`GSPublisherVersion 0.0.100.44`): 5,561 line segments and 195 placed glyphs, no
raster anywhere in the file. **It is the first geometry source in this project
that is not an image.**

> [!WARNING]
> **It was issued for a DIFFERENT UNIT. Owner, 2026-09-08: `МН5_287` is Минина
> street, building 5, apartment 287, per the general plan. This flat is
> building 3, apartment 190.** So it arrived with the standing mirroring
> caveat attached, and the question of whether it describes this flat at all had
> to be answered before anything could be built on it.

**It was answered by test, not by inspection.** Method, and it is reproducible —
`tools/layout/parse_vector_plan.py`:

1. **Handedness — matches.** Rendered from the parsed vectors and compared with
   `fllor_plan_detailed.jpeg`: wet block top-left, лоджия bottom-left with its
   angled glazing, rooms 9,36 / 16,64 / 19,49 left to right, кухня top-right.
   **Not mirrored. No flip is needed and no position needs re-handing.**
2. **All nine printed areas are identical** to the developer figures already in
   `data/canonical/dimension_tolerance.json` — 9,79 / 1,24 / 3,09 / 9,36 /
   16,64 / 5,24 + 19,49 / 6,05(4,24) / 69,09 / 45,49.
3. **Scale is exactly 1:75**, derived by pairing each dimension label with the
   dimension line it annotates — **not assumed, and not taken from a histogram.**
4. **The geometry reproduces its own printed labels to ±0.1 mm**, on 19 of the 24
   labels that paired cleanly. The other five are pairing failures of the
   heuristic (a short label attaching to a longer neighbouring line), not
   disagreements between drawing and number.
5. **Every developer chain this repo had already verified off the raster is
   reproduced exactly**, at the same scale:

   | chain | vault, read off the raster | this PDF, from the vectors |
   | :--- | :--- | :--- |
   | small room width, top | 1795 + 120 + 910 = 2825 | **2825.0**, exact |
   | small room width, bottom | 1120 + 1380 + 150 + 175 = 2825 | **2825.0**, exact, **same start line** |
   | middle room, bottom width | 600 + 1800 + 600 = 3000 | **3000.0**, exact |
   | middle room, internal length | 1050 + 3250 + 1490 = 5790 | **5789.6** |
   | туалет | 1140 × 1090 | **1140.0 × 1090.0** |

   **The small room's two parallel chains close on each other to 0.0 mm** — which
   is the closure validator this repo mandates in place of an area check, now
   passing on vector geometry rather than on a reading.

→ **Conclusion: this is the developer's type drawing for 3Б/3+, the same drawing
as `fllor_plan_detailed.jpeg`, re-issued per unit. It is a VECTOR EDITION OF THE
BASE CASE — not a fourth comparable, and not a mirrored one.** Nothing in the
comparables table changes; `kv53` and `Минина 6` remain the comparables.

### ⚠️ The trap it set on the way, which is exactly standing rule 9

**Fitting the scale by clustering segment lengths onto multiples of 5 mm returned
1:150, cleanly and confidently — and 1:150 is wrong by a factor of two.** It fits
because every length that is a multiple of 5 mm at the true scale is a multiple
of 10 mm at twice it: the test could not distinguish them. It was caught only by
a sanity check outside the fit — at 1:150 the flat comes out **20.4 m wide**.
**The scale was independent of the thing being measured only after it was
re-derived from the dimension labels.** Recorded because it is the rule's own
failure mode, met in the wild: `00_Master/Evidence_Reading_Discipline.md`.

### What it does NOT change

- **⚠️ It is design intent at higher precision, not better truth.** The drawing
  says so itself, in the developer's own words on the sheet: *«Данный лист
  является проектным решением, все размеры — проектные. Фактические параметры
  квартиры могут отличаться от указанных.»* **That is the developer stating the
  as-built may differ — the citable version of a claim this repo had only
  inferred from three surveyed flats.**
- **The +1.0% to +1.9% developer-larger bias stands**, all 12 comparisons. Size
  for a room-scale run up to **~100 mm SHORTER** than drawn, never longer.
- **Areas remain not-evidence**, including the nine that matched.
- **Nothing is field-verified**, and nothing can be until the building completes.

### What it does change

**The raster registration error term retires for chain reading.** `registration`
in `dimension_tolerance.json` exists only because the geometry was an image —
`mm_per_px: 20.6302`, `aspect_error_pct: 1.66`, and 89.1% of CAD wall pixels
landing on drawn wall. **Reading a chain no longer goes through any of that.**
The tracing surfaces keep their role for anything the PDF does not carry.

### ⚠️ The schedule marks carry nothing we need — corrected 2026-09-08

The sheet also carries `ОК-2360`, `ОК-6`, `ББ-8`, `ДЖ11`, seven marks ending in
`ПР` (`111ПР`, `121ПР`, `122ПР`, `242ПР`, `263ПР` ×2, `321ПР`), and a `ТИП nn`
under each room's area label. **Owner, 2026-09-08: these are ordinary schedule
references — `ОК` = окно, `ПР` = проём, `ББ` = балкон. Nothing here is needed.**

> [!CAUTION]
> **This corrects a claim made earlier the same day, and it was the only genuinely
> new content I had attributed to this drawing.** I read the `ПР` suffix as
> **правая** and reported that the sheet carries **door swing handedness** the
> rasters do not. **It does not. `ПР` is проём — an opening reference, with no
> direction in it.** The reading came from the abbreviation alone, with no
> attempt to confirm it against what the mark points at: **the exact move
> standing rule 9 exists to stop, made in the same session that recorded a
> different instance of the same rule.** Nothing was built on it.

### ✅ `ТИП 22` / `ТИП 27` — heated room vs cold room

**`ТИП nn` is not an opening mark at all.** It sits directly under a **room's**
area label, once per room, and the sheet carries exactly two values:

| mark | rooms carrying it |
| :--- | :--- |
| **`ТИП 22`** | all seven: туалет 1,24 · ванная 3,09 · прихожая 9,79 · кухня 5,24 · 9,36 · 16,64 · 19,49 |
| **`ТИП 27`** | **the лоджия alone**, 6,05(4,24) |

**Owner's reading, 2026-09-08: `ТИП 22` = HEATED room, `ТИП 27` = COLD room.**
Every placement agrees — the split is not wet/dry (туалет and ванная both read
`ТИП 22`), and it is not habitable/service (прихожая and кухня read `ТИП 22`
too). **The only line it separates is the warm perimeter from the outside of
it**, and the лоджия is the only room outside.

> [!IMPORTANT]
> **⚠️➡️✅ This is the DEVELOPER classifying the лоджия as unheated, on his own
> drawing** — and that fact currently rests on the owner's colour markup plus the
> building description, i.e. on reasoning about the M1 wall rather than on a
> statement. **It is now corroborated from a third and independent direction.**
>
> **It matters because of what stands on it.** The лоджия being thermally
> decoupled is the premise of the frost-free-through-a-Belarusian-winter target
> in `Family_Requirements.md` §10: essentially no heat leaks in from the flat, so
> the target rests on **solar gain plus the лоджия's own enclosure**, and the
> glazing upgrade does nearly all the work. **That premise is now firmer.**

⚠️ **The sheet carries no legend, so `22` and `27` are not decoded from the
document itself** — this is the owner reading his own developer's convention,
and the placement evidence is consistent with it rather than proof of it. **It
changes no number.** ✅ **It does not need to: it confirms a premise rather than
supplying a quantity, and the лоджия heat-loss calculation was never going to
take a figure from this drawing.**
