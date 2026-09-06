# Soundproofing — which walls in *this* flat, and which are already fine

**Written 2026-09-07**, answering the owner directly: *"probably the only room which really needs
soundproofing is the smaller bedroom — but to make sure, we can analyse this one more time."*

**Short answer: his instinct is half right, and the half that is wrong matters more.** The small bedroom
does carry the flat's one bad *neighbour* adjacency. But the wall involved is the **best** kind this flat
has, and the genuinely weak walls are **internal 75 mm partitions** that no norm forces up and that
separate our own bedrooms from each other.

---

## 1. Every boundary in the flat, ranked

Built from `building_spec.json → neighbours_and_adjacency` and the wall model.

| face | build | on the other side | verdict |
| :--- | :--- | :--- | :--- |
| **R2 · G5 · R7** east | 250 concrete + the neighbouring block's 200, **~400 with a seam** | mirrored flat: **living room faces living room**, no wet rooms | ✅ **Best possible. Needs nothing** |
| **R1a · G2 · R3 · G3** north | 250 | common corridor, then the flat above | ✅ Fine. The weak point is the **entrance door**, not the wall |
| **R1b + upper G4a** west | 250 | neighbour's bathroom — **wet-to-wet** | ✅ Correct pairing. Riser noise is the risk, not speech |
| **lower G4a · R6** west | 250 concrete | ⚠️ neighbour's **habitable room 14.64**, against our **9.36 bedroom** | ⚠️ **The one bad adjacency — but 250 concrete is a good wall** |
| **G8** | **75** aerated block | ⚠️⚠️ our **middle room** — the children — against our **9.36 bedroom** — the adults | ⚠️⚠️ **The worst wall in the flat** |
| **G7** | **75** | ⚠️ our **living room** against the **middle room** | ⚠️ Evening noise against a sleeping child |
| **G6** | **75** | прихожая against the middle room | ⚠️ Circulation noise at a bedroom |
| **G4d** | 120 | прихожая against the 9.36 bedroom | Moderate |
| **MA · MB · MC** | 300 + 70 | outside | Not an issue; the glazing is the path |

---

## 2. ⚠️⚠️ The ranking is not the one the question assumes

**The party wall he is worried about is 250 mm of reinforced concrete.** The walls between our own
bedrooms are **75 mm of aerated block** — a third of the thickness and a fraction of the mass. Mass is
what stops airborne sound.

→ So **G8, between the adults' bedroom and the children's room, is acoustically the worst wall in the
flat**, and it is a wall we own entirely. It is also the only one where the noise is **nightly and
bidirectional** — a child waking the adults and adults waking a child are the same wall.

→ And in **Phase 2**, when the boy moves into the 9.36 room and the adults move to the separated part of
the кухня/living zone, **G7** takes over that role. Both 75 mm walls end up on a bedroom boundary at some
point in the plan.

> [!IMPORTANT]
> **This does not mean the party wall is silent.** It means that of the money available, the internal
> partitions buy more quiet per rouble — and unlike the party wall, we can alter them during the works
> without touching anything shared.

---

## 3. ⚠️ What the vault's own sources say about treating one wall

This is the part that most changes the answer, and it comes from the repo's existing
[Soundproofing](../12_Engineering_and_Systems/analysis/Soundproofing.md) page rather than from this
analysis:

- **The single-wall request is the one practitioners say fails.** «шум не проникает только со стороны
  стены… **в основном всё это идёт через ПЕРЕКРЫТИЕ**… Мы не можем локально избавиться от всех шумов,
  заизолировав одну стенку» — hence «грамотная шумоизоляция — это **ПОМЕЩЕНИЕ В ПОМЕЩЕНИИ**».
- **And the ceiling of what money buys is bounded**: «если вы хотите прямо НАСТОЯЩУЮ шумоизоляцию…
  вы получите **процентов на 20** более тихую атмосферу, и при этом **заплатите раз в 10 больше**».
- **The floor is the cheap side of the problem**: «гораздо лучше делать шумоизоляцию **НА ПЕРЕКРЫТИЕ**
  [сверху] — укладывать на пол гораздо проще, чем крепить к потолку», and it addresses «по крайней мере
  **ТОПОТ**, удар [по] полу».

**How that applies here, and it cuts both ways:**

| | |
| :--- | :--- |
| **against the neighbour** | their noise arrives **structurally, through the slab**, so treating `G4a`/`R6` alone is exactly the intervention the source says under-delivers. ⚠️ **Do not spend here first** |
| **between our own rooms** | both rooms sit on **the same slab**, and the dominant path through a 75 mm partition is **direct airborne**. So treating `G8` is the case where a single-wall treatment actually does most of the work |

→ **That is the whole argument in one line: treat the walls whose noise is airborne and ours; do not
treat the wall whose noise is structural and someone else's.**

---

## 4. What this suggests doing

1. **Nothing on the east side.** ~400 mm with a seam, habitable-to-habitable, no risers. Already the best
   wall in the flat.
2. **`G8` first**, as part of the partition works rather than as a retrofit — it is being touched anyway
   if the layout changes.
3. **`G7` next**, on the same reasoning, and it becomes the bedroom wall in Phase 2.
4. **Floor treatment** where the layout is settled — cheapest per decibel, and the only thing that
   addresses impact noise from above, which nothing in the walls will.
5. **The entrance door**, as a cheap discrete item: it is the acoustic hole in an otherwise sound 250 mm
   north wall.
6. **The party wall last, if at all** — and only with the expectation set by the source above.

> [!WARNING]
> **Not costed, and no Rw figures are asserted here.** The ordering follows from mass, thickness and
> transmission path, which are robust. Actual dB numbers would need sourcing into the vault before any of
> this becomes a specification. The one thing that would change the ranking is if the neighbour's 14.64
> turns out to be a **living room with a television against that wall** — that is recorded as unknown in
> `building_spec.json` and is worth finding out.
