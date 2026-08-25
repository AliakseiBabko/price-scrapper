# Layout analysis dataset

How re-planning knowledge extracted from architect/contractor videos is stored so
that CAD, IFC and visualisation tooling can consume it.

## Four layers, one direction of flow

```
_Inbox/frames/<date>_<video_id>/     raw evidence   (gitignored, reproducible)
  index.json, frames/*.jpg           transcript segments + the frame on screen

data/layout_cases/<case_id>.json     one case       (schemas/layout-case.schema.json)
  problems -> moves -> tradeoffs, every item anchored to a timestamp + frame

data/layout_rules/rules.jsonl        reusable rules (schemas/layout-rule.schema.json)
  one line per rule, numeric params, attributed to a named practitioner

17_*/analysis/*.md                   prose          (the vault's existing convention)
  the reasoning, disagreements between sources, and your own judgement
```

Each layer is derived from the one above it and can be rebuilt from it. Nothing
flows upward: the wiki never becomes the system of record for a number.

## Why the dataset is the load-bearing layer

`tools/ifc/current_apartment_layout.py` and friends build geometry from numeric
parameters. They cannot read prose. A rule such as

```json
{"rule_id":"corridor.min_clear_width","params":{"min_clear_width_mm":1100}}
```

can be evaluated directly against a candidate layout; the same knowledge as a
paragraph in a guide cannot. So the numbers live in JSON with units in the key
name, and the prose keeps what JSON is bad at - the reasoning and the
disagreements.

## Cases and rules are separate on purpose

One case yields many rules; one rule is supported by many cases. Keeping them in
one file would force a choice between duplicating rules per case and losing the
per-case evidence. They are linked many-to-many:
`rule.supported_by[] <-> case.rules_derived[]`, checked in both directions by the
validator. This mirrors `00_Master/source_relationships.csv`.

## Nothing is a flat fact

Every rule carries `attribution` (who said it, their role, their region) and an
`epistemic_status` that defaults to `practitioner_opinion`. Where two
practitioners disagree, both rules stay, marked `confidence: contested` and
linked through `conflicts_with` - the disagreement is data, not a defect to
resolve. Regional and date context is mandatory for the same reason it is for
prices: a Moscow contractor's 1100 mm corridor is a Moscow opinion from a
particular year.

## Validate

```powershell
.\.venv\Scripts\python.exe tools\layout\validate_layout_data.py --strict-frames
```

Beyond JSON Schema it checks what a schema cannot: that every `solves`,
`sequence_after` and `zone_ids` id resolves, that every cited frame exists, that
no stated problem is silently left unaddressed, and that case/rule links agree
both ways. Drop `--strict-frames` when the frame directories have been cleaned
up (they are gitignored and re-derivable with
`tools/youtube/extract_layout_frames.py`).

## Move vocabulary

`moves[].op` is a closed vocabulary (`wall.thicken`, `opening.shift`,
`niche.create`, `duct.reduce`, `layer.add`, …) rather than free text, so a future
tool can replay a case's moves against your own plan and report which ones are
even applicable. Parameters use unit-suffixed keys (`depth_mm`, `sill_above_screed_mm`)
so no prose parsing is ever needed to get a number out.
