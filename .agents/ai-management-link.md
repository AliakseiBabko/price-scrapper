# Cross-repo coordination pointers

Not tracked skill content — a short orientation note for a future session in
this repo, on how `price-scrapper` connects to the sibling `ai-*` repos.

## ai-telemetry (already live, verified 2026-08-20)

`scripts/record_telemetry.py` in this repo forwards to
`C:\Users\User\Documents\ai-telemetry`'s `record_*.py` scripts, with
`--project-id price-scrapper` baked in. `price-scrapper` is already a
registered project there (`ai-telemetry/projects.yaml`) with a confirmed
real (non-dry-run) native `sessions` row on record. Common call:

```powershell
python scripts/record_telemetry.py current-session
```

See `ai-telemetry/README.md` ("Recording native telemetry", "Near-automatic
current-session recording") for the full command set.

## ai-skills (shared generic skills, already linked)

The shared skills `.agents/skills/renovation-knowledge-intake/SKILL.md`
delegates to (`youtube-transcript-fetch`, `meeting-transcript-extract`,
`tiered-knowledge-base`, `visual-evidence-organize`) live in
`C:\Users\User\Documents\ai-skills\skills\` and are linked (LINKED/junction
mode) into `~/.claude/skills/` and `~/.codex/skills/` — Skill-tool-invocable
directly by name in either runtime, no project-local adapter needed for
these. `management-plan-dialogue` (below) was linked the same way on
2026-08-20.

This repo's own project-specific skills
(`renovation-knowledge-intake`, `homestyler-cad-to-revit`,
`residential-bim-geometry-rules`) currently live as real, git-tracked copies
under `.agents/skills/` rather than as junction adapters to a separate
`ai-project-contexts/price-scrapper/` store — that migration was not part of
the 2026-08-20 connection work and is a candidate for later, not done here.
`youtube-to-obsidian` is **deprecated as of 2026-08-04** and must not be
followed for a new batch. Use `renovation-knowledge-intake/SKILL.md` instead —
it wraps the shared `youtube-transcript-fetch` and `tiered-knowledge-base`
skills and is the maintained path. The old `scripts/get_youtube_transcript.py`
still runs and is usable as a manual fallback; the skill's *instructions* are
what is out of date. The canonical `processed_sources.csv` schema and status
vocabulary live in `renovation-knowledge-intake/SKILL.md`, not in the
deprecated skill's copy.

Two project-local tools under `tools/youtube/` support this path:
`preflight_playlist.py` (canonical video-ID dedup against
`00_Master/processed_sources.csv` and source-note filenames, plus an
availability/caption probe) and `archive_transcripts.py` (moves fetched
transcripts to `_Archive/processed_sources/` and repoints each note's
`transcript_file:` frontmatter, matching on the `.meta.json` sidecar's
`video_id` rather than by filename glob, which broke once on a leading-
underscore ID).

*Drained from Claude machine-local memory 2026-08-31 (WS-3). The memory copy
said `90_Archive/processed_sources/`, a path that no longer exists — it became
`_Archive/` in the 2026-08-30 restructure. That staleness is the argument for
this file being the record and memory being only an inbox.*

## ai-management (multi-agent plan dialogue, added 2026-08-20)

Cross-agent (Claude + Codex) collaboration on larger implementation plans for
this project happens via the shared, private
`C:\Users\User\Documents\ai-management` repo's `management/` folder and the
`management-plan-dialogue` skill (linked globally into both `~/.claude/skills/`
and `~/.codex/skills/` on 2026-08-20).

**Active dialogue**: `PRICE_SCRAPPER_KNOWLEDGE_INTAKE_OPTIMIZATION` — a plan
to reduce token cost and improve stopping/quality signals in the
renovation-knowledge-intake pipeline (store split, SKILL.md trim, per-round
yield metric, source-note quality fields, flat dedup index, batch-status
file). Canonical plan:
`ai-management/management/PRICE_SCRAPPER_KNOWLEDGE_INTAKE_OPTIMIZATION_IMPLEMENTATION_PLAN.md`.
Dialogue state: `ai-management/management/dialogue/PRICE_SCRAPPER_KNOWLEDGE_INTAKE_OPTIMIZATION_state.json`.
Turn 1 (CLAUDE, plan draft) recorded 2026-08-20; turn 2 (CODEX) prepared at
`ai-management/management/dialogue/PRICE_SCRAPPER_KNOWLEDGE_INTAKE_OPTIMIZATION_NEXT_TURN.md`.

To check status or advance the dialogue from either repo:

```powershell
cd C:\Users\User\Documents\ai-management
python ..\ai-skills\scripts\management_dialogue.py status --topic PRICE_SCRAPPER_KNOWLEDGE_INTAKE_OPTIMIZATION
python ..\ai-skills\scripts\management_dialogue.py next --topic PRICE_SCRAPPER_KNOWLEDGE_INTAKE_OPTIMIZATION
```

Real implementation work for an accepted plan item still happens inside
*this* repo (`price-scrapper`) — `ai-management` only holds the plan/review/
response dialogue artifacts, never this project's own code or knowledge-base
content.
