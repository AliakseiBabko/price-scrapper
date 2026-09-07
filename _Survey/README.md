# `_Survey/` — the photo survey of three comparable flats

**Moved out of `_Inbox/_Visual_Drop/` on 2026-09-07 at the owner's request**, because this stopped being
inbox material some time ago. It is now a **source in its own right**, and his stated future use is the
one that matters: *"probably the photos with position will help us to digitize the environment — the
apartment in its initial state."*

---

## What is here

| folder | flat | handedness | contents |
| :--- | :--- | :--- | :--- |
| `apartment_109_mirrored/` | unit 109 | **mirrored** vs ours | positioning plan + 13 photos |
| `apartment_2_same_handedness_as_ours/` | unit 2 | **same as ours** | positioning plan + 6 photos |
| `apartment_53_mirrored/` | unit 53 | **mirrored** vs ours | positioning plan + 8 photos |
| ~~`flat_unknown/`~~ | **resolved** | — | the 3 window close-ups turned out to be apartment 53’s `b6f0`, `bdc7` and `9db4` — byte-identical. Folder removed |

Each `positioning_plan.png` is the owner's own annotated survey plan: a **red dot** per camera position,
an **arrow** for the view direction, and a **4-hex id** matching the `.jpg` beside it.

**The index is `data/canonical/photo_positions.csv`** — one row per dot, with the room it sits in, our
equivalent room, the view direction, and what each photo settled.

---

## ⚠️ Why the images are gitignored, and what is in git instead

These are **Realt.by** and **Квадратный метр** listing photos — third-party watermarked material. The
repo already has a precedent for exactly this, in `AGENTS.md`: the three album PDFs in `00_Master/` are
*"gitignored — third-party watermarked client documents; identity is kept via sha256 in the case files."*

So the same treatment applies here:

- the **bytes** stay out of git — `.gitignore` excludes `_Survey/**/*.jpg|jpeg|png`
- the **identity** goes into git — `_Survey/manifest.csv` carries path, flat, description, byte size and
  **sha256** for all 30 files

That means the collection is documented, verifiable and referenceable from the model, without committing
6.7 MB of someone else's watermarked photographs to a remote.

> [!IMPORTANT]
> **This does not make them backed up.** Gitignored means *this machine only*. If the collection matters
> — and it does, since much of the geometry and every services position now rests on it — it needs a
> backup that is not this repository. **Say the word and the bytes go into git instead**; it is one line
> in `.gitignore`, and the precedent above is the only argument against it.

---

## What is deliberately *not* here

The **drawings** stay in `_Inbox/_Visual_Drop/`:

- `floor_plan_basic.jpg` — **our floor**, and the underlay every model drawing is built on
- `fllor_plan_detailed.jpeg` — the only *dimensioned* drawing, and the source of every printed figure
- `building_floor_plan*.jpg` — the block plan and the flat's position in it
- `floor plan_1/2/3.jpg` — the measured surveys behind `00_Master/Geometry_Variance_Study.md`
- `floor_plan_basic_all_walls.jpg`, `..._concrete_walls.jpg` — the owner's own wall markings

Two reasons. They are **drawings, not photographs** — a different class of evidence, and the one the
model is *built from* rather than *checked against*. And the drawing scripts reference
`_Inbox/_Visual_Drop/floor_plan_basic.jpg` by path, so moving it would break every model render for no
gain.

---

## What this collection has already settled

Worth recording, because it is the argument for keeping it:

- **the кухня is a zone, not a room** — confirmed three times over, by two surveyors' own
  «жилая с кухонным оборудованием» labels and by the developer wiring that space with **two** ceiling
  points
- **the лоджия glazing** — glazed at handover, single cold glazing, four bays and one transom, no
  parapet, and a width confirmed to **9 mm** against our derived figure
- **every window's sill and head**, and the internal door head
- **every services position** the model has: the P1 riser zone with its meters, the kitchen sewer and
  water take-offs, the extract grilles
- **sanitaryware is part of the handover** — a WC pan is fitted
- and **~2540 rather than 2500** for the ceiling, by two routes that use nothing but a door standard and
  the owner's tape

> [!NOTE]
> **The manifest earned its keep immediately.** Hashing the 33 files gave only 30 unique digests: the three window close-ups supplied first, and treated as flat-unknown ever since, are byte-identical to apartment 53’s `b6f0`, `bdc7` and `9db4`. So those earliest window measurements came from a **mirrored** flat. That does not touch the sills and heads — mirroring does not change a height — but it does mean the O4 window and door leaves sit on the **opposite sides** in ours, which matters for the inward door swing recorded as a planning constraint.
