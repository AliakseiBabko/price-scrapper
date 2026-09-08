# `_Precedents/` — other people's designs for this apartment

**What somebody else proposed for this flat, or for a flat like it.** Set up on 2026-09-08 at the
owner's request: *"I have another set of at least two or three design projects with renderings… organize
them per project and per author… the same apartment by different author… keep them at hand and reference,
analyze it and reference in our solutions if needed."*

So this folder has one job: **make it cheap to ask "what did other people do with this flat, and what did
it cost them" — and cheap to cite the answer.**

---

## The roster is the index — `roster.csv`

**Start there, not with the folders.** One row per precedent, machine-readable so a future precedent-view
tool can enumerate it:

| column | what it holds |
| :--- | :--- |
| `precedent_id` | the folder name. For a design project: **`<author>__<project>`** |
| `class` | `design_project` · `market_listing` |
| `author` / `project` | human-readable |
| `same_type_as_ours` | `yes` · `no` · `unknown` — **the single most important column**, see below |
| `files` / `examined` | counts, checked against the manifest by the validator |
| `case_file` | the `data/layout_cases/*.json` holding the analysis, if any |
| `status` | `analysed` · `partly_analysed` · `ingested_only` · `rejected` |
| `what_it_settles` | one sentence. If it settles nothing, say so |

---

## Layout

```
_Precedents/
├── README.md            ← you are here: the convention
├── roster.csv           ← the index
├── design_projects/
│   └── <author>__<project>/
│       ├── README.md    ← what it is, what it settles, what may NOT be read off it
│       ├── manifest.csv ← path, role, examined, what, bytes, sha256
│       ├── plans/
│       ├── renderings/
│       └── documents/
└── market_listings/
    └── <slug>/
        ├── README.md
        ├── manifest.csv
        └── images/
```

**Why author-first naming.** The comparison the owner wants is *the same apartment by different authors*,
so the author is the discriminating axis and belongs at the front of the name. `zemskov__euro3-2026` and
`zemskov__three-room-2025` then sort next to each other, and every author's take on this flat sits in one
alphabetical block. **One folder per author-project pair, flat — not nested** — because most authors will
have exactly one project here and a folder containing a single folder helps nobody.

### The two classes are not the same kind of evidence

| | `design_projects/` | `market_listings/` |
| :--- | :--- | :--- |
| what it is | a **named author's proposal** for this apartment type | listing photos or renderings of **some flat** in the development |
| what it is good for | **layout reasoning** — the move, the tradeoff, the option set | **finish level and fittings actually sold here** |
| gets a `layout_cases/*.json`? | **yes**, that is where the analysis goes | normally no |
| layout match | usually verifiable from the plan | **usually unverifiable — assume `unknown`** |

Filing a listing as a design project would let marketing images masquerade as design intent. That is why
`class` exists.

---

## Adding the next one — one command

```bash
python tools/precedents/ingest_precedent.py --author nsdsgn --project euro3-2026 --src "C:/Users/User/Downloads/whatever"
python tools/precedents/ingest_precedent.py --listing some-listing --src "..."          # a listing instead
python tools/precedents/ingest_precedent.py ... --dry-run                              # look first
```

It copies the bytes in, hashes everything, skips byte-identical duplicates, and writes `manifest.csv`
with **every file marked `examined: no`**. Then, and none of it is optional:

1. **Look at every file** and set `role`, `examined` and `what` in `manifest.csv`.
2. **Write the folder's `README.md`** — what it is, who made it, and **what may not be read off it**.
3. **Add a row to `roster.csv`.**
4. If it is worth analysing, create `data/layout_cases/<case_id>.json` and name it in the roster.
5. **Run the gate**: `python tools/precedents/validate_precedents.py`

---

## ⚠️ The rules that exist because something already went wrong

**1. A `role` is a claim, so it requires that someone has looked.** Files land as `examined: no` /
`role: unexamined`, and the validator rejects a role set on an unexamined file. This exists because an
unfurnished plan in the first set was filed as *the developer handover state* when it is actually the
**after** state of a demolition — it shows no кухня partition, while our own schedule lists кухня as a
separate 5.24 m² room. A confident label on an unlooked-at file is worse than no label.

**2. A layout case may not cite an unexamined file.** The validator cross-checks every
`companion_documents[].source_sha256` in `data/layout_cases/*.json` against these manifests and fails if
the cited file is `examined: no`, or if no manifest lists that hash at all.

**3. Identity is the only thing git holds.** The image bytes are **gitignored** — third-party watermarked
material, same treatment as `_Survey/` and the album PDFs. So `sha256` in a manifest is the whole record
of a file's identity, and the validator rehashes every file on disk to confirm the manifest still tells
the truth. **A file on disk that no manifest row mentions is a validator failure**, because it exists
nowhere else.

**4. Undimensioned means undimensioned.** Presentation plans and renderings mostly carry **no dimension
strings**. Set `dimension_policy: undimensioned` on the case and take **every** figure from our own
developer schedule instead. See `00_Master/Evidence_Reading_Discipline.md` — a furnished plan *looks* like
a drawing you can scale, and it is not.

> [!IMPORTANT]
> **Gitignored means this machine only — it is not a backup.** Unlike `_Survey/`, losing these costs
> analysis rather than geometry, because the conclusions already live in the layout cases, which *are* in
> git. That is the argument for leaving it as it stands.

---

## How this differs from the neighbours

| folder | holds | the model is built from it? |
| :--- | :--- | :--- |
| **`_Precedents/`** | **design precedent** — what others *proposed* | **never** |
| `_Survey/` | **measurement evidence** — 30 positioned photos of three built flats of this layout | **yes** — sills, heads, riser zones, the 2540 ceiling |
| `_Inbox/_Visual_Drop/` | **our own drawings** — the dimensioned developer plan, the owner's markings | **yes**, it is the underlay |
| `data/layout_cases/` | **the analysis layer** — problems, moves, tradeoffs, outcomes | it is the reasoning, not the geometry |

`_Survey/` and `_Precedents/` look alike — both third-party, both gitignored, both manifest-indexed. The
difference is that one is evidence of **what is**, and the other of **what somebody wanted**. Mixing them
is the failure `Evidence_Reading_Discipline.md` exists to prevent.
