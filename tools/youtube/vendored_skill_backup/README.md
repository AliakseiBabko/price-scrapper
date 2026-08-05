# Vendored backup: `youtube-transcript-fetch` shared skill

This directory is a **point-in-time, read-only backup** of the global,
machine-local `youtube-transcript-fetch` skill that lives outside this
repo at `~/.claude/skills/youtube-transcript-fetch/` (on this machine:
`C:\Users\User\.claude\skills\youtube-transcript-fetch\`). It exists so
the 2026-08-05 rate-limit/IP-block hardening fix to that skill (see
below) doesn't silently disappear if a different machine/session/profile
has an older, unpatched copy of the global skill and nothing in this repo
records what the fix was supposed to look like.

**This copy is not live and is not imported by anything in this repo.**
`.agents/skills/renovation-knowledge-intake/SKILL.md` and the intake
pipeline still call the real global skill at `~/.claude/skills/...`, not
these files. If you need to re-apply or re-verify the fix on a machine
where the global skill is out of date, diff that machine's live copy
against this backup and reconcile by hand - don't just copy this
directory over the global skill location without checking for other
changes made there since 2026-08-05.

## What was patched here (2026-08-05)

Trigger: two sequential `youtube-transcript-fetch` runs against a
3-video playlist both hit an identical YouTube `429 Too Many Requests` /
IP-block response (see [[project_price_scrapper_youtube_ingestion_tooling]]-
adjacent session history; also documented in this repo's own
`.agents/skills/renovation-knowledge-intake/SKILL.md`).

`scripts/fetch_youtube_transcript.py` changes:
- Added `_RATE_LIMIT_MARKERS` / `_classify_failure()` - detects when a
  failed attempt's error text looks like a YouTube rate-limit/IP-block
  (`429`, `too many requests`, `blocking requests from your ip`, `ip has
  been blocked`, `requestblocked`, `ipblocked`).
- On such a failure, `<video_id>.FAILED.meta.json` now additionally gets
  `"reason_class": "rate_limited_or_ip_blocked"` and a
  `"next_retry_guidance"` field.
- Exit code is now **2** (not the generic 1) specifically for this
  reason class - a caller should treat exit code 2 as a circuit breaker
  for the whole fetch phase (stop attempting further videos in the same
  run), not just a per-video failure to skip past.
- `EXIT_CODES` docstring updated to describe both exit codes.

`SKILL.md` changes:
- Documents the two distinct non-zero exit codes and the "stop the whole
  fetch phase on exit code 2" guidance.

This repo's own companion fix (versioned normally, in this same commit):
`tools/youtube/preflight_playlist.py` now defaults to light mode
(duplicate check only, no network probing) instead of probing every
fresh video by default, and its own optional `--probe` path has a
matching circuit breaker on a detected rate-limit response.

## Companion operating policy

See this project's own memory note
`feedback_serialize_youtube_fetches_ratelimit_policy` (Claude Code
project memory, not part of this repo): fetches must be serialized (one
video at a time, no parallel agents fetching), with bounded backoff (at
most one retry after a real cooldown) on a rate-limit/IP-block, and such
a failure must never be logged as `skipped`/`duplicate_skipped` in
`00_Master/processed_sources.csv`.
