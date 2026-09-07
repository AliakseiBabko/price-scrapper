# `_Drawings/` — where drawings live

**Created 2026-09-07** because `_assets/` had become unnavigable: 122 genuine appliance and fixture
images sat alongside **43 drawings of mine, of which 38 were superseded iterations of the same plan** —
`wall_model_v3` through `v24`, `wall_segments_v8`, `v9`, and so on.

**The rule now: `_assets/` is for referenced assets. `_Drawings/` is for anything I draw.**

---

## The three folders, and what belongs in each

| folder | what it holds | lifetime |
| :--- | :--- | :--- |
| **`sheets/`** | **album sheets — the deliverable.** Named by their sheet number in `data/deliverable_templates/zk-dubravinskiy-full-album.json`, e.g. `sheet_01_sockets.png` | permanent; regenerated in place, never versioned by filename |
| **`review/`** | **the current working drawing, for the owner to check.** One file per subject, no version suffix — `wall_model.png`, not `wall_model_v25.png` | overwritten each time; the *previous* state lives in git |
| **`evidence/`** | **crops and enlargements** taken from a source drawing or photo to settle a specific question, e.g. `west_block_crop.png` | permanent, because the finding cites them |

---

## ⚠️ Why no version suffixes any more

The 22 `wall_model_vNN.png` files existed because each round of the owner's corrections produced a new
drawing, and I kept them all. That was wrong twice over:

- **git already versions them.** Every one was committed; `git log -- _Drawings/review/wall_model.png`
  and `git show <rev>:<path>` recover any past state.
- **and it inverted the point.** A file called `wall_model_v17.png` invites the question *"which one is
  current?"* — the answer should be structural, not a matter of reading numbers.

**So: overwrite `review/wall_model.png`.** If a specific past version genuinely needs to be cited, cite
the **commit**, not a filename.

> [!NOTE]
> The 38 superseded files were removed from the working tree, not from history. Canonical entries that
> pointed at a specific iteration now point here and say which one they were written against.

---

## How drawings get made

Not by hand. `tools/layout/sheets/make_services_sheets.py` renders the album sheets from
`data/canonical/wall_runs.csv`, so a change to the model shows up in the drawing rather than needing to
be re-drawn — and a symbol on the wrong wall face becomes visible immediately, which is how five of them
were caught.

The underlay is `_Inbox/_Visual_Drop/floor_plan_basic.jpg` — **our** floor, 3Б/2+. The dimensioned
detailed plan is the source of printed figures; the basic plan is the source of what exists. See
`data/canonical/wall_materials.json` → `underlay_switched_to_the_basic_plan_2026_09_04`.
