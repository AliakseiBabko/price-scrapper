# Transcript fetching: fallback chain and failure classification

## Why two methods (three counting whisper, which is deliberately separate)

`youtube-transcript-api` talks to YouTube's internal timedtext endpoints
directly and is fast, but it can be blocked by IP-based rate limiting, or
fail on videos where only auto-captions exist in an unexpected language
variant. `yt-dlp` is heavier (spawns a subprocess, writes temp files) but
has broader, more actively-maintained handling of YouTube's caption
delivery quirks (age-gating prompts, consent walls, regional variants,
`asr`-only tracks). Trying the API first and falling back to `yt-dlp` gives
speed on the common case and resilience on the edge cases.

A third method, local Whisper transcription (`--mode whisper`, see
`SKILL.md`'s "When captions are genuinely unavailable"), exists for videos
where *neither* method above finds any caption track at all - i.e. the
uploader genuinely disabled captions, not a transient API/rate-limit issue.
It is intentionally excluded from `auto` and must be invoked explicitly,
because unlike the two caption-based methods (which either return real
uploader-provided text or fail cleanly), Whisper always returns *something*
- including, at smaller model sizes, confidently wrong somethings. A silent
fallback to Whisper would make a genuinely-missing-transcript failure look
identical to a successfully-fetched one downstream, which is worse than
just failing loudly.

## What counts as a real attempt

A real attempt means the script actually called the transcript API or
invoked `yt-dlp` and got a response (success, or a real exception/non-zero
exit with a message). It does **not** mean:

- Fetching the YouTube watch page HTML with a generic web-fetch tool and
  scanning for caption-related strings. Caption tracks are not reliably
  present in the raw page HTML - a miss there proves nothing about whether
  captions exist.
- Checking video metadata (title, description) for the word "transcript"
  or "captions".
- Assuming failure because the video is long, non-English, or from a
  channel that "usually doesn't have captions".

If neither `youtube-transcript-api` nor `yt-dlp` was actually invoked, the
correct status is "not yet attempted", not "unavailable".

## Failure classification

When `fetch_youtube_transcript.py` exits non-zero, the `attempts` list (also
echoed to stderr and written into `<video_id>.FAILED.meta.json`) contains
one entry per method with the literal exception text. Common patterns and
what they mean:

| Error pattern | Meaning | Typically NOT a dead end |
|---|---|---|
| `TranscriptsDisabled` | Uploader disabled all captions/transcripts for this video | Confirmed unavailable via API; still worth trying `yt-dlp` in `auto` mode as a second opinion, but usually also fails |
| `NoTranscriptFound` / `could not retrieve a transcript` | No track exists in the requested language list | Retry with a broader `--languages` list (e.g. add the video's likely spoken language) |
| `VideoUnavailable` | Video is private, deleted, or region-blocked for this request context | Confirm the URL/ID is correct; not fixable by retrying |
| `yt-dlp ... exited 1: ERROR: ... Sign in to confirm your age` | Age-gated video without auth | Out of scope for this skill (no login flow); report as a hard failure |
| `yt-dlp found no subtitle tracks for languages [...]` | Track list came back empty for every requested language | Retry with `--languages` widened, or the video genuinely has no captions in any language |
| Import error mentioning `youtube_transcript_api` | Package not installed in the environment running the script | Install with `pip install youtube-transcript-api`; not evidence the video lacks a transcript |
| `yt-dlp` not found / `FileNotFoundError` | `yt-dlp` not installed or not on PATH | Install with `pip install yt-dlp`; not evidence the video lacks captions |
| Import error mentioning `faster_whisper` (mode=whisper only) | Package not installed | Install with `pip install faster-whisper`; not evidence of anything about the video |
| `faster-whisper produced an empty transcript` (mode=whisper only) | Audio downloaded but ASR found no speech (silent/music-only audio, or a genuine transcription failure) | Not fixable by retrying the same model; try a different `--whisper-model`, or the audio may genuinely have no speech |
| `yt-dlp audio download produced no output file` (mode=whisper only) | Audio-only download failed for the same reasons a video download might (region block, private/deleted, `ffmpeg` missing for the postprocessor step) | Check `ffmpeg` is on PATH; otherwise same causes as a `yt-dlp` subtitle failure above |

## Reporting failures to the user

Always quote the exact error text from `attempts`, not a paraphrase. A
missing dependency and a genuinely caption-less video look identical if you
summarize both as "transcript unavailable" - the exact message is what lets
the user (or a follow-up task) tell them apart and decide whether to
install a package, retry with different languages, or give up on this
video.

## Deduplication scope

The script's dedup check only looks inside the `--output-dir` you pass it,
matching on `video_id` + content `sha256` from each file's `.meta.json`
sidecar. It intentionally does not check any project-level CSV, database,
or index - if a calling project already tracks processed sources elsewhere
(e.g. a `processed_sources.csv`), that project's own workflow is
responsible for checking there too before calling this skill, and for
logging the new entry afterward.
