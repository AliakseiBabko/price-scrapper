---
name: youtube-transcript-fetch
description: "Fetch a YouTube video's transcript or captions into a plain-text file with a metadata sidecar (URL, video ID, language, method, timestamp). Generic and project-agnostic - the caller decides the output directory and what to do with the transcript afterward (archiving, indexing, summarizing). Use whenever the user asks to fetch, get, check, extract, download, pull, or verify a YouTube transcript, captions, or subtitles, or asks 'what does this YouTube video say' / 'summarize this YouTube video' and no transcript exists yet."
---

# YouTube Transcript Fetch

## Overview

Fetches the transcript/captions for a YouTube video and writes them to a
plain-text (or Markdown) file plus a small JSON metadata sidecar, so the
evidence (source URL, video ID, language, method used, timestamp) travels
with the text. This skill only fetches and preserves the transcript - it
never decides where the file should be archived, whether an index or
Obsidian note should be updated, or whether a processed-sources CSV should
get a new row. Those decisions belong to the calling project/skill.

## When to use this skill

Trigger on any request to fetch, check, extract, download, pull, or verify
a YouTube video's transcript, captions, or subtitles - including indirect
requests like "what does this video say" or "summarize this YouTube video"
when no transcript file exists yet for that video.

**Never claim a transcript is "unavailable" based only on fetching the
YouTube watch-page HTML** (e.g. via a generic web fetch tool). Page HTML
does not reliably expose caption tracks. Only report unavailability after
actually running this skill's script (or an equivalent transcript-API /
yt-dlp attempt) and getting a real failure from both methods.

## Root cause of 429/bot-check failures, and the recommended fetch cadence

Neither `youtube-transcript-api` nor `yt-dlp` is a stable, sanctioned
YouTube API - both are unofficial access paths (transcript-endpoint
scraping and Innertube-internal calls, respectively) sensitive to request
pattern, IP reputation, VPN/datacenter IPs, and repeated retries. A `429`
and a `Sign in to confirm you're not a bot` failure are two different
defenses YouTube can trigger from the same underlying cause: this
process's traffic looking automated. Treat "this specific video/channel is
blocked" as the wrong mental model - it's usually the access pattern, not
the content.

Default fetching should therefore be **anonymous, slow, and cached**, not
"as fast as the network allows":

- Light preflight only (the default as of 2026-08-05 - see the calling
  project's own preflight tool docs); skip metadata/caption probing unless
  actually needed.
- One transcript fetch at a time - never parallel across videos or agents.
- Real spacing between fetches in a multi-video run (order of minutes, not
  back-to-back) - a rate-limit/bot-check can trigger even across
  *sequential* single fetches if they're close together in time, not just
  from literal concurrency.
- Stop immediately on exit code 2 (see below) - don't attempt the next
  video in the same run.
- Every successful fetch is already cached permanently by this script's
  own dedup behavior (see "Deduplication" below) - never re-fetch a video
  ID + content hash already on disk in `--output-dir`.

`--cookies-from-browser` (below) is the escalation path for when that
default keeps failing on a small batch - not a replacement default. See
its own flag documentation for the tradeoffs before reaching for it.

## Quick start

```bash
python scripts/fetch_youtube_transcript.py "<youtube_url_or_video_id>" --output-dir "<caller-chosen-dir>"
```

Useful optional flags:

```bash
python scripts/fetch_youtube_transcript.py "<url>" \
  --output-dir "<dir>" \
  --slug "short_title_slug" \
  --languages "ru,en" \
  --mode auto \
  --extension txt
```

- `url_or_id` (positional, required): full YouTube URL (`watch?v=`, `youtu.be/`,
  `/shorts/`, `/embed/`) or a bare 11-character video ID.
- `--output-dir` (required): where the transcript + metadata files are
  written. This skill never assumes or hardcodes a project's archive,
  Obsidian, or inbox folder - the caller must pass this explicitly.
- `--slug` (optional): short human-readable label folded into the filename.
- `--languages` (optional, default `ru,en`): comma-separated language
  preference order, tried in this order by the two caption-based methods.
- `--mode` (optional, default `auto`):
  - `transcript` - only try the `youtube-transcript-api` transcript API.
  - `subtitles` - only try `yt-dlp` subtitle extraction.
  - `auto` - try the transcript API first, then fall back to `yt-dlp` if it
    fails. Preferred default: the transcript API is faster and doesn't
    require a full `yt-dlp` invocation, but `yt-dlp` also picks up
    auto-generated captions in more edge cases (e.g. age-gated or
    region-quirky metadata).
  - `whisper` - local ASR transcription via `faster-whisper`, for a video
    with no captions available through either method above. **Not** part of
    `auto` - always an explicit, separate invocation. See "When captions are
    genuinely unavailable" below before reaching for this.
- `--whisper-model` (optional, default `large-v3`, only used with `--mode
  whisper`): `tiny`/`base`/`small`/`medium`/`large-v3`. Default is `large-v3`
  deliberately - see below.
- `--whisper-language` (optional, only used with `--mode whisper`): force a
  language code instead of letting Whisper auto-detect. Auto-detect was
  reliable (99-100% confidence) in testing; only set this if a specific
  video is misdetected.
- `--extension` (optional, default `txt`): `txt` or `md` for the transcript
  file.
- `--cookies-from-browser BROWSER[:PROFILE]` (optional, e.g. `chrome` or
  `firefox:Default`) - **opt-in escalation path, off by default.** Default
  anonymous fetching is the normal mode: light preflight, one fetch at a
  time, real spacing between videos (see "Rate-limit/IP-block circuit
  breaker" below) - reach for this flag only when that default keeps
  hitting a 429 or a "Sign in to confirm you're not a bot" wall (exit code
  2) and the batch is small enough that authenticating is worth the
  tradeoff. Makes yt-dlp read the named browser's existing logged-in
  YouTube session cookies instead of requesting anonymously - substantially
  less likely to trigger either defense, since it looks like a real user
  session rather than automated traffic. Only affects the yt-dlp-based
  methods (`subtitles` mode, and whisper's own audio download) -
  `youtube-transcript-api`'s request is not authenticated by this flag.
  **This script never reads, copies, logs, or writes cookie contents or the
  cookie database path** - yt-dlp reads the named browser's own cookie
  store directly, in-process; only the browser name/profile the caller
  typed is ever recorded (in the metadata sidecar, as
  `cookies_from_browser`). Still stops on a 429/bot-check (exit code 2)
  even when authenticated - this is a per-run escalation, not a guarantee,
  and not a reason to loop retries. In practice this flag can itself fail
  locally before ever reaching YouTube (a locked cookie database, or on
  Windows a DPAPI decryption failure) - see `--cookies` below as the
  fallback for exactly that case, and exit code 3 in "Behavior and
  guarantees" for how such a failure is classified. **Credential-safety
  rules for the caller**: don't export cookies into a repo, don't commit a
  cookies file, don't print cookie contents/paths; using a personal
  account's session for repeated/automated fetching carries some
  account-level risk (distinct from IP-level rate-limiting) - consider a
  secondary account for a regular workflow.
- `--cookies PATH` (optional) - **opt-in escalation path, off by default,
  and a fallback for `--cookies-from-browser` specifically.** Points to a
  manually-exported Netscape-format cookies file instead of having yt-dlp
  read a live browser's cookie store directly - use this when
  `--cookies-from-browser` fails locally (locked database, DPAPI
  decryption failure) rather than genuinely reaching YouTube. Same
  tradeoffs and credential-safety rules as `--cookies-from-browser` apply,
  plus: **store the exported file outside any repo, never commit it, and
  delete it once you're done testing if it's not needed long-term.** This
  script never reads, opens, prints, or copies the file's contents, and
  never records its path in any metadata sidecar - only that authenticated
  fetching was attempted (`"cookie_source": "cookies_file"`). Checked for
  existence/readability before use (filesystem metadata only, never
  content) - a missing or unreadable file is reported as exit code 3
  (local setup failure), not a YouTube-side signal, so it's never
  mistaken for a rate-limit/IP-block that needs a cooldown. Can be
  combined with `--cookies-from-browser`, though typically only one is
  needed.

## When captions are genuinely unavailable

If both `youtube-transcript-api` and `yt-dlp` fail (`auto` mode exhausted,
`TranscriptsDisabled` or equivalent for both), you have two real options -
**neither should be silently substituted for the other**:

1. **Manual transcription via a paid service** (e.g. Turboscribe or similar) -
   higher fidelity, requires a human step (no API for most such services),
   worth it for a video you actually want to trust as a knowledge-base
   source.
2. **`--mode whisper` (local, free, offline)** - convenient, but **do not
   default to this without understanding the accuracy/time tradeoff**: a
   real comparison (2026-07-31) against a paid reference transcript on a
   short, clean, single-speaker video found:
   - `small` and `medium` models both **dropped or fabricated entire
     clauses** - not paraphrasing errors, actual missing/invented content
     (e.g. medium replaced a full sentence explaining *why* the video's
     topic mattered with unrelated fabricated names). Roughly 55-65% content
     fidelity against the reference.
   - `large-v3` was the first tier that matched the reference closely - no
     dropped or fabricated content, only minor word-level noise (a wrong
     word here and there) and loss of punctuation/sentence breaks partway
     through. This is why it's the default for `--mode whisper`.
   - The cost: `large-v3` took **~13x longer** than `small` on the same
     short clip (about 13.5 minutes vs. about 1 minute for a ~1-2 minute
     video). A long video could mean hours of local compute.
   - **Treat any `--mode whisper` output as needing a skeptical read before
     trusting specific facts/numbers from it**, even at `large-v3` - the
     metadata sidecar sets `"asr_fallback": true` specifically so a
     downstream extraction step can apply that skepticism automatically
     instead of relying on someone remembering to.

## Behavior and guarantees

1. **Method order (auto mode)**: `youtube-transcript-api` (manually-created
   track first, then auto-generated) → `yt-dlp` subtitle extraction (manual
   subs first, then auto-subs, converted from VTT to plain text).
2. **On success**: writes `<date>_<slug>_<video_id>_<hash8>.<ext>` (transcript
   text) and a matching `.meta.json` sidecar containing `url`, `video_id`,
   `language`, `is_generated_captions`, `method`, `timestamp` (UTC ISO 8601),
   `source_tool`, and `sha256` of the transcript text.
3. **Deduplication**: before writing, the script scans `--output-dir` for an
   existing file whose metadata sidecar has the same `video_id` and
   `sha256` hash, and skips writing a duplicate if found (prints the
   existing path instead). It does not touch any external CSV/index -
   dedup is purely within the given output directory.
4. **On failure**: exits non-zero, prints every attempted method with its
   exact exception/error message to stderr, and still writes a
   `<video_id>.FAILED.meta.json` record of the attempts to `--output-dir` so
   the failure is evidenced, not just asserted. Report these exact messages
   back to the user - do not paraphrase them into a generic "unavailable".
   Three distinct non-zero exit codes:
   - **1 - per-video failure**: private, unavailable, or genuinely no
     captions for this specific video. Safe to move on to the next video in
     a batch.
   - **2 - environment-level rate-limit/IP-block circuit breaker, confirmed
     reached YouTube**: at least one attempt's error text matched a known
     throttling/block signature (HTTP 429, "Too Many Requests", or a
     youtube-transcript-api IP-block message), **and no attempt was a local
     setup failure** (see exit code 3 - a local failure always takes
     priority in the overall classification, since it means an escalation
     path was never actually tested). The `.FAILED.meta.json` gets
     `"reason_class": "rate_limited_or_ip_blocked"`, a `next_retry_guidance`
     field, and each individual attempt is tagged with its own
     `"reason_class"` too. **Treat exit code 2 as a stop signal for the
     whole fetch phase** - do not attempt the next video in the same run,
     and do not immediately retry; wait for a real cooldown (tens of minutes
     to hours) and use at most one bounded retry, not a retry loop.
   - **3 - local setup failure, never reached YouTube**: at least one
     attempt failed before the request left this machine - most commonly
     `--cookies-from-browser` couldn't read the named browser's cookie
     database (the browser, including a background/tray instance, was still
     running and holding it locked). **This is not a YouTube-side signal and
     must not be treated as a rate-limit/IP-block cooldown trigger** - it
     means the escalation path (e.g. authenticated fetch) was never actually
     exercised. Even if a *different* attempt in the same run independently
     hit a real rate-limit/block, the overall exit code is still 3 (local
     setup dominates the overall classification) - but that other attempt's
     own `"reason_class": "rate_limited_or_ip_blocked"` is still present
     per-attempt in `.FAILED.meta.json`, so that signal isn't lost, just not
     what decides the overall result. Fix the local problem (fully close the
     named browser - check Task Manager/Activity Monitor for a lingering
     background process, not just closed windows; on Chrome specifically,
     "Continue running background apps when Google Chrome is closed" under
     Settings → System can keep it alive after every window is closed) and
     retry immediately - no cooldown needed.
5. **Filesystem scope**: `--output-dir` is created if it doesn't exist. The
   script never writes a persistent file outside that directory. `yt-dlp`
   subtitle downloads land in an OS temp directory that's deleted
   automatically once that attempt finishes; any local temp-directory path
   that would otherwise leak into a yt-dlp error message is stripped before
   it's logged or written to `.FAILED.meta.json`.

### Example invocation

```bash
python scripts/fetch_youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --output-dir "C:\Path\To\Your Project\transcripts" \
  --slug "example_video_title" \
  --languages "ru,en"
```

Quote `--output-dir` (and any other path argument) whenever it may contain
spaces - the script itself handles spaced paths fine either way, but shell
quoting is still needed so the shell doesn't split the path into multiple
arguments. Replace the URL, path, and slug above with real values; nothing
in this skill assumes a specific repository or folder layout.

See `references/transcript-fetching.md` for why the fallback chain is
ordered this way, how to classify specific error messages (missing
dependency vs. genuinely caption-less video), and the exact scope of the
deduplication check.

## Dependencies

- `youtube-transcript-api` (Python package) - required for `--mode transcript`
  and used first in `--mode auto`.
- `yt-dlp` (CLI *and* importable Python package - both are used: the CLI for
  `--mode subtitles`/`auto`, the Python package for downloading audio in
  `--mode whisper`) - required for `--mode subtitles`, used as the fallback
  in `--mode auto`, and required (alongside `faster-whisper`) for `--mode
  whisper`.
- `faster-whisper` (Python package) - only required for `--mode whisper`.
  Downloads its model weights from Hugging Face on first use of a given
  model size (`tiny`≈75MB up to `large-v3`≈3GB), cached afterward under
  `~/.cache/huggingface/hub/`. CPU-only inference (`device="cpu",
  compute_type="int8"`) - no GPU required, but this is also why `large-v3`
  is slow (see "When captions are genuinely unavailable" above).

If a dependency is missing, the corresponding method's attempt will record
an import/exec error in the failure report rather than crashing the whole
script (unless *every* requested method is unavailable, in which case the
script exits non-zero with both errors listed).

**Do not install any dependency unilaterally.** Check first (e.g.
`pip show youtube-transcript-api`, `pip show faster-whisper`, `where yt-dlp`
/ `which yt-dlp`, or just run the script and read the failure report), then
tell the user which package is missing and ask before running an install
command (`pip install youtube-transcript-api` / `pip install yt-dlp` /
`pip install faster-whisper`) - installing into someone else's environment
is exactly the kind of action that needs a confirmation, not an assumption.
This applies doubly to `--mode whisper`: a first-time model download is a
real, sometimes-multi-GB network fetch, not just a small package install.

## After fetching

Once the transcript file and metadata sidecar exist, hand off to whatever
the calling project/task actually needs: summarizing the content, updating
project-specific notes or knowledge bases, logging the source in a
project's own tracking file, or archiving the raw transcript. This skill's
job ends at "transcript safely on disk with evidence of how it got there."

This skill only fetches and preserves transcript evidence - it does not
summarize, synthesize, or fold the transcript into any wiki/knowledge
base. For turning a fetched transcript (plus other sources) into a
structured knowledge store or a readable master wiki page over time, use
the shared `tiered-knowledge-base` skill (if available).
