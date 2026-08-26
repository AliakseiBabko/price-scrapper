# Carrying two or three options to the end

## The question

Do we keep one model, or a separate model per option? And how do we carry two or
three options — layout, furniture, finishes — all the way to a full document set
each, and only choose at the end?

## The answer: one shell, many patches, a model per option **on build**

There is no choice to make between "one model" and "several models", because
they are different things:

- **Stored**: one shell plus a small patch file per option. Nothing is copied.
- **Built**: each option produces its *own* complete model — its own IFC, sheets,
  DXF, Blender scene, quantities. Those are outputs, regenerated on demand and
  never hand-maintained.

So you get exactly what you asked for — a full document set per option — without
ever maintaining three models. The models are generated; the *decisions* are what
is stored.

**Why not copies.** If option B were a copy of option A's model, every fix to the
shared shell would have to be made three times, and the day one copy was missed
the three options would quietly stop describing the same apartment. As patches,
the shell is fixed once and all options are rebuilt from it.

## Layout, furniture and finishes are separate layers

They are separate decisions and should not be entangled. A variant may `extend`
another variant instead of the shell, so choices compose:

```
current_apartment_shell.json          the flat, unchangeable
   ├── v1-homestyler                  layout option A  (your Homestyler design)
   │      ├── v1-furniture-family     furniture scheme 1 on layout A
   │      └── v1-furniture-open       furniture scheme 2 on layout A
   └── v2-something                   layout option B
          └── v2-furniture-family     the same furniture thinking on layout B
```

A finishes patch is the same shape. That is what lets you test "does the family
furniture scheme work in both layouts" without a second copy of either layout.

Build any node and you get the whole chain applied in order:

```powershell
.\.venv\Scripts\python.exe tools\layout\make_variant.py v1-furniture-family
```

The applied chain is recorded in the built spec as `variant_chain`, so any
drawing can say exactly which decisions produced it.

## How an option progresses

Each variant carries a `status`:

| status | meaning |
|---|---|
| `draft` | being explored; may be broken or half-formed |
| `candidate` | complete enough to compare — gets a full document set |
| `selected` | the one to build. **At most one.** |
| `rejected` | considered and dropped — kept, with the reason in `decision` |
| `superseded` | replaced by a later variant, named in `decision` |

Rejected options are **kept, not deleted**. Dolgushev's album ships variants 1–4
alongside the final one for the same reason: six months from now the useful
question is not only what was chosen but what was ruled out and why.

## What "choose at the end" looks like

1. Carry two or three `candidate` variants. Each builds its own document set.
2. Compare them as drawings — `compare_variants.py` puts them side by side with
   metrics and the rule checks from `data/layout_rules/`.
3. Flip one to `selected` and write the `decision`; flip the others to
   `rejected`, each with its reason.
4. Rebuild. The selected option's document set is the one you hand a contractor;
   the rest stay in the repo as the record of the choice.

Nothing is thrown away, nothing is duplicated, and the decision is a one-line
edit rather than a migration.

## Versions

Git already versions the patches, so "version 3 of the kitchen idea" is a commit,
not a filename. Do not create `v1-homestyler-v2.json`; edit the variant and let
the history hold the versions. Reach for a new variant id only when you want to
*compare* the two side by side rather than replace one with the other.
