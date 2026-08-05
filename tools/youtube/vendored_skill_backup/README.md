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

## Second patch (2026-08-05, same day): `--cookies-from-browser` opt-in escalation

Trigger: after the circuit-breaker fix above, a same-day retry (with a
VPN) succeeded for 2-3 fetches, then hit a fresh `429`/bot-check again on
the same playlist, and a later yt-dlp metadata check hit `Sign in to
confirm you're not a bot` even for a single call - established this isn't
"one bad IP" but YouTube's automated-traffic defenses reacting to request
*pattern*, since `youtube-transcript-api`/`yt-dlp` are both unofficial
access paths, not a stable sanctioned API.

`scripts/fetch_youtube_transcript.py` changes:
- Added `--cookies-from-browser BROWSER[:PROFILE]` (e.g. `chrome`,
  `firefox:Default`) - opt-in, off by default. Passed through to yt-dlp's
  own `--cookies-from-browser` CLI flag (subtitle-fetch path) and to its
  Python API's `cookiesfrombrowser` ydl_opt (whisper's audio-download
  path) via a small local spec parser (`_parse_cookies_from_browser_spec`).
  Does **not** affect `youtube-transcript-api`'s own request - that path
  is unauthenticated regardless of this flag.
- Never reads, copies, logs, or writes cookie contents or the cookie
  database path - yt-dlp reads the named browser's own cookie store
  directly, in-process. Only the browser/profile name the caller typed is
  ever recorded, in the metadata sidecar (`authenticated_fetch: true`,
  `cookies_from_browser: "<spec>"`) on success, or in
  `<video_id>.FAILED.meta.json` on failure.
- Still stops with exit code 2 on a detected rate-limit/bot-check even
  when authenticated - this is a per-run escalation, not a guarantee.

`SKILL.md` changes:
- New "Root cause of 429/bot-check failures, and the recommended fetch
  cadence" section: default fetching is anonymous/slow/cached (light
  preflight, one fetch at a time, real spacing between fetches, stop on
  exit code 2, rely on the script's own dedup as permanent caching);
  `--cookies-from-browser` is documented as the escalation path for a
  small batch when that default keeps failing, not a new default -
  including the credential-safety rules (no exporting/committing/logging
  cookies, prefer this flag over a manual `cookies.txt`, consider a
  secondary account for a regular workflow given some account-level risk).

`tools/youtube/preflight_playlist.py` (this repo, versioned normally, same
commit) got the matching `--cookies-from-browser` opt-in for its own
`--probe` path.

## Third patch (2026-08-05, same day): local vs. YouTube-side failure classification

Trigger: the first `--cookies-from-browser "chrome:Profile 3"` test run
failed with yt-dlp reporting `Could not copy Chrome cookie database`
(most likely Chrome still running and holding a lock on it) - but the
script's existing single-verdict classifier folded this into
`reason_class: "rate_limited_or_ip_blocked"` / exit code 2, because the
*other* attempt (`youtube-transcript-api`) independently hit a real
IP-block message. That misreported a purely local setup failure as a
YouTube-side signal, which would have wrongly triggered the
stop-and-cooldown circuit breaker even though authenticated fetch was
never actually tested.

`scripts/fetch_youtube_transcript.py` changes:
- Added `_LOCAL_COOKIE_ACCESS_MARKERS` and `_classify_attempt()` - per-
  attempt classification, not just an overall verdict. Detects local
  cookie/credential-access failures (`could not copy`, `could not find`,
  `cookie database`, `cookies database`, `failed to decrypt`, `permission
  denied`) separately from YouTube-side rate-limit/block markers.
- `_classify_failure()` now tags every attempt dict in place with its own
  `"reason_class"`, then derives an overall verdict where a
  `local_setup_failure` on *any* attempt takes priority over a
  `rate_limited_or_ip_blocked` on another - a caller needs to know the
  escalation path wasn't actually exercised, not just that "something
  rate-limit-shaped happened."
- New **exit code 3** for `reason_class: "local_setup_failure"` - distinct
  from exit code 2 (confirmed YouTube-side block) and exit code 1
  (per-video failure). Explicitly NOT a cooldown/circuit-breaker signal -
  guidance is "fix the local problem and retry immediately," including a
  reminder to check for a lingering background browser process (e.g.
  Chrome's "continue running in background" setting) beyond just closed
  windows.
- `.FAILED.meta.json` now has both a per-attempt `"reason_class"` on each
  entry in `"attempts"` and the overall top-level `"reason_class"` - so a
  genuine rate-limit signal from one method isn't lost even when a
  different method's local failure decides the overall exit code.

`SKILL.md` changes: documents all three exit codes and the local-vs-
YouTube-side distinction explicitly.

## Fourth patch (2026-08-05, same day): `--cookies PATH` fallback for a manually-exported cookies file

Trigger: `--cookies-from-browser "chrome:Profile 3"` failed twice for two
different local reasons on the same machine - first a locked cookie
database (`Could not copy Chrome cookie database`), then, after fully
closing Chrome, a Windows DPAPI decryption failure
(`Failed to decrypt with DPAPI`, see yt-dlp#10927) - neither ever reached
YouTube. Rather than keep debugging the live-browser-cookie-store path,
added a fallback that reads a pre-exported cookies file instead.

`scripts/fetch_youtube_transcript.py` changes:
- Added `_check_cookie_file_accessible(path)` - validates the file exists
  and is readable using only filesystem metadata (`os.path.isfile`,
  `os.access`) before any yt-dlp invocation; **never opens, reads, or
  copies the file's contents**. Raises a `RuntimeError` with a message
  that never echoes the path itself.
- New `--cookies PATH` CLI flag, passed straight through to yt-dlp's own
  `--cookies` (subtitle-fetch path) and the Python API's `cookiefile`
  ydl_opt (whisper's audio-download path) - both call
  `_check_cookie_file_accessible` first, so a missing/unreadable file is
  caught immediately, offline, and classified as `local_setup_failure`
  (exit code 3) rather than yt-dlp silently proceeding without cookies or
  producing a confusing downstream error.
- Success and failure metadata sidecars now record `"cookie_source":
  "cookies_file"` when `--cookies` was used - **never the file's own
  path**, distinct from the `--cookies-from-browser` case (which does
  record the browser/profile name, since that isn't sensitive the way a
  local file path can be).
- `SKILL.md` documents `--cookies` as the fallback specifically for when
  `--cookies-from-browser` fails locally, with the same credential-safety
  rules plus: store the exported file outside any repo, never commit it,
  delete it once no longer needed.

Verified entirely offline before any real test: constructing a call with
a nonexistent `--cookies` path raised the expected `RuntimeError`
immediately (no network attempted), and feeding that error text through
`_classify_failure` correctly produced `local_setup_failure` / exit code
3.

## Companion operating policy

See this project's own memory note
`feedback_serialize_youtube_fetches_ratelimit_policy` (Claude Code
project memory, not part of this repo): fetches must be serialized (one
video at a time, no parallel agents fetching), with bounded backoff (at
most one retry after a real cooldown) on a rate-limit/IP-block, and such
a failure must never be logged as `skipped`/`duplicate_skipped` in
`00_Master/processed_sources.csv`.
