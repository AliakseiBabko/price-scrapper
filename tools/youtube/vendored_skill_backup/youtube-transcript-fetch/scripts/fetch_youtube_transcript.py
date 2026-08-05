#!/usr/bin/env python3
"""Fetch a YouTube transcript into a plain-text file plus a metadata sidecar.

Generic, project-agnostic. Callers pass an explicit output directory; this
script never assumes an Obsidian vault, an archive folder, or a CSV log.

Methods attempted, in order (mode=auto):
  1. youtube-transcript-api (transcript API) - manually-created track first,
     then auto-generated, for the requested languages.
  2. yt-dlp subtitle extraction (manual subs, then auto-generated captions),
     converted from VTT/SRT to plain text.

mode=transcript forces method 1 only. mode=subtitles forces method 2 only.
mode=whisper forces local Whisper (faster-whisper) transcription only - see
below; NOT part of auto, by design (see "Why whisper isn't in auto mode").
Every attempted method and its exact failure message is recorded and, on
total failure, printed to stderr and included in the metadata sidecar
(method="failed") - never silently reported as "unavailable".

## Why whisper isn't in auto mode

A real accuracy comparison (2026-07-31, against a paid reference transcript)
found faster-whisper's "small" and "medium" models both drop or fabricate
whole clauses on a clean, single-speaker recording - not safe to feed into
a knowledge base unreviewed. "large-v3" was the first tier that matched the
reference closely (no dropped/invented content, only minor word-level
noise), but took ~13x longer than "small" on the same short clip - multiple
hours is plausible on a long video. Given that cost/accuracy shape, this
script treats local Whisper as an explicit, opt-in last resort (mode=whisper,
model defaults to large-v3) rather than a silent fallback when captions are
missing - auto mode still only tries the two caption-based methods and
fails/reports if both come up empty, so a caller always makes the
whisper-vs-manual-transcription-service decision deliberately, not by
accident.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


def extract_video_id(url_or_id: str) -> str:
    s = url_or_id.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    if "v=" in s:
        return s.split("v=")[1].split("&")[0]
    if "youtu.be/" in s:
        return s.split("youtu.be/")[1].split("?")[0].split("&")[0]
    if "/shorts/" in s:
        return s.split("/shorts/")[1].split("?")[0].split("&")[0]
    if "/embed/" in s:
        return s.split("/embed/")[1].split("?")[0].split("&")[0]
    raise ValueError(f"Could not extract a YouTube video ID from: {url_or_id!r}")


def sanitize_slug(slug: str) -> str:
    slug = re.sub(r'[\\/*?:"<>|]', "", slug)
    return slug.strip().replace(" ", "_")[:50]


def _parse_cookies_from_browser_spec(spec: str) -> tuple:
    """Parse a "--cookies-from-browser" value into the (browser, profile,
    keyring, container) tuple yt-dlp's Python API expects for the
    `cookiesfrombrowser` ydl_opt. Only supports the common "browser" or
    "browser:profile" forms (not keyring/container) - sufficient for the
    escape-hatch use case this flag exists for. Never logs or returns
    anything beyond what the caller already typed on the command line -
    this function doesn't touch the actual cookie store, just the spec
    string naming which browser to read it from."""
    if ":" in spec:
        browser, profile = spec.split(":", 1)
        return (browser, profile or None, None, None)
    return (spec, None, None, None)


def try_transcript_api(video_id: str, languages: list[str]):
    """Attempt method 1. Returns (text, lang_used, is_generated) or raises."""
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    try:
        transcript = transcript_list.find_manually_created_transcript(languages)
        is_generated = False
    except Exception:
        transcript = transcript_list.find_generated_transcript(languages)
        is_generated = True

    fetched = transcript.fetch()
    text = " ".join(entry.text for entry in fetched if entry.text.strip())
    if not text.strip():
        raise RuntimeError("youtube-transcript-api returned an empty transcript")
    return text, transcript.language_code, is_generated


def _parse_vtt_or_srt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.upper().startswith("WEBVTT"):
            continue
        if line.isdigit():
            continue
        if "-->" in line:
            continue
        if line.startswith(("Kind:", "Language:", "NOTE")):
            continue
        # strip inline VTT tags like <00:00:01.000><c> word</c>
        line = re.sub(r"<[^>]+>", "", line)
        lines.append(line)

    # collapse consecutive duplicate lines (common in auto-captions with
    # rolling/overlapping cue windows)
    deduped = []
    for line in lines:
        if not deduped or deduped[-1] != line:
            deduped.append(line)
    return " ".join(deduped).strip()


def try_ytdlp_subtitles(video_id: str, languages: list[str], cookies_from_browser: str | None = None):
    """Attempt method 2 via yt-dlp CLI. Returns (text, lang_used, is_generated) or raises.

    cookies_from_browser, if given, is passed straight through as yt-dlp's own
    `--cookies-from-browser` CLI value (e.g. "chrome" or "firefox:Default") -
    this makes yt-dlp read the named browser's existing YouTube session
    cookies itself; this script never reads, copies, or logs cookie contents
    or the cookie database path itself."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    lang_arg = ",".join(languages)

    with tempfile.TemporaryDirectory() as tmpdir:
        out_template = os.path.join(tmpdir, "%(id)s.%(ext)s")

        def sanitize(msg: str) -> str:
            # yt-dlp errors can echo the local temp working directory (an
            # environment-specific, user-account-bearing path) - strip it so
            # failure records never carry machine-local path evidence.
            return msg.replace(tmpdir, "<tmp>")

        for sub_flag, is_generated in (("--write-subs", False), ("--write-auto-subs", True)):
            # Invoke yt-dlp as `python -m yt_dlp` on this same interpreter rather than
            # shelling out to a bare "yt-dlp" command. A bare command depends on yt-dlp's
            # console-script entry point being on PATH, which is not guaranteed even when
            # the yt_dlp package is installed and importable (e.g. a venv's Scripts/bin dir
            # not being on PATH) - that gap previously surfaced as a generic WinError 2 /
            # "command not found" failure indistinguishable from "no subtitle tracks exist",
            # so real caption-availability failures and environment-setup failures were
            # being reported identically. Running as a module uses the exact same
            # interpreter/environment already confirmed to have yt_dlp importable (see
            # try_whisper_local below), eliminating the PATH dependency entirely.
            cmd = [
                sys.executable, "-m", "yt_dlp",
                sub_flag,
                "--skip-download",
                "--sub-langs", lang_arg,
                "--sub-format", "vtt",
                "-o", out_template,
            ]
            if cookies_from_browser:
                cmd += ["--cookies-from-browser", cookies_from_browser]
            cmd.append(url)
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if proc.returncode != 0:
                detail = sanitize(proc.stderr.strip()[-800:] or proc.stdout.strip()[-800:])
                raise RuntimeError(f"yt-dlp {sub_flag} exited {proc.returncode}: {detail}")

            vtt_files = [f for f in os.listdir(tmpdir) if f.endswith(".vtt")]
            if not vtt_files:
                continue

            # prefer the first requested language that yt-dlp actually produced
            chosen = None
            for lang in languages:
                for f in vtt_files:
                    if f"." + lang in f or f".{lang}." in f:
                        chosen = f
                        break
                if chosen:
                    break
            if not chosen:
                chosen = vtt_files[0]

            lang_match = re.search(r"\.([a-zA-Z-]+)\.vtt$", chosen)
            lang_used = lang_match.group(1) if lang_match else (languages[0] if languages else "unknown")

            text = _parse_vtt_or_srt(os.path.join(tmpdir, chosen))
            if not text.strip():
                raise RuntimeError(f"yt-dlp produced an empty subtitle file: {chosen}")
            return text, lang_used, is_generated

        raise RuntimeError(
            f"yt-dlp found no subtitle tracks for languages {languages} "
            f"(tried --write-subs and --write-auto-subs)"
        )


def try_whisper_local(video_id: str, model_size: str, whisper_language: str | None, cookies_from_browser: str | None = None):
    """Attempt local Whisper transcription. Returns (text, lang_used, is_generated) or raises.

    Downloads audio via yt-dlp into a temp dir (auto-cleaned), then transcribes
    with faster-whisper. `is_generated` is always True - there is no manual/
    auto-generated distinction for an ASR transcript the way there is for
    YouTube's own captions.
    """
    import yt_dlp as _yt_dlp
    from faster_whisper import WhisperModel

    url = f"https://www.youtube.com/watch?v={video_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_template = os.path.join(tmpdir, f"{video_id}.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_template,
            # Unlike the yt-dlp subtitle path above, this genuinely needs an `ffmpeg`
            # binary on PATH - yt_dlp's FFmpegExtractAudio postprocessor shells out to
            # it directly, and there's no equivalent "run as a Python module" escape
            # hatch the way there is for yt-dlp itself. If this step fails with a
            # generic "ffmpeg not found" error, that's the cause - install ffmpeg and
            # ensure it's on PATH, don't assume the video/environment is otherwise broken.
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }],
            "quiet": True,
            "no_warnings": True,
        }
        if cookies_from_browser:
            ydl_opts["cookiesfrombrowser"] = _parse_cookies_from_browser_spec(cookies_from_browser)
        print(f"[whisper] downloading audio (model={model_size}, this can take a while)...", file=sys.stderr)
        with _yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio_files = [f for f in os.listdir(tmpdir) if f.startswith(video_id)]
        if not audio_files:
            raise RuntimeError("yt-dlp audio download produced no output file")
        audio_path = os.path.join(tmpdir, audio_files[0])

        print(f"[whisper] transcribing locally (model={model_size}; first run for this model downloads it, ~150MB-3GB)...", file=sys.stderr)
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path, language=whisper_language, vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments)
        if not text.strip():
            raise RuntimeError("faster-whisper produced an empty transcript")
        print(f"[whisper] detected language: {info.language} (confidence {info.language_probability:.2f})", file=sys.stderr)
        return text, info.language, True


def find_existing_output(output_dir: str, video_id: str, text_hash: str):
    """Return path of an existing transcript for this video/hash, if any."""
    if not os.path.isdir(output_dir):
        return None
    for fname in os.listdir(output_dir):
        if not (fname.endswith(".txt") or fname.endswith(".md")):
            continue
        if video_id in fname:
            meta_path = os.path.join(output_dir, os.path.splitext(fname)[0] + ".meta.json")
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    if meta.get("video_id") == video_id and meta.get("sha256") == text_hash:
                        return os.path.join(output_dir, fname)
                except Exception:
                    pass
            elif os.path.splitext(fname)[0].endswith(video_id):
                return os.path.join(output_dir, fname)
    return None


EXIT_CODES = """
Exit codes:
  0  Success - transcript written, OR a transcript for this video ID + content
     hash already existed in --output-dir (deduplicated, nothing new written).
  1  Failure, per-video - either url_or_id could not be parsed into a video ID,
     or every attempted retrieval method failed for a reason specific to this
     video (private, unavailable, no captions). The exact error from each
     attempted method is printed to stderr and also written to
     <output-dir>/<video_id>.FAILED.meta.json.
  2  Failure, environment-level rate-limit/IP-block - every attempted method
     failed and at least one failure looks like YouTube throttling/blocking
     this machine (HTTP 429, "Too Many Requests", or an IP-block message from
     youtube-transcript-api), not a per-video captions problem. Same
     FAILED.meta.json is written, with "reason_class": "rate_limited_or_ip_blocked"
     and a "next_retry_guidance" note. A caller processing multiple videos in
     one run should treat exit code 2 as a circuit breaker: stop attempting
     further videos in this run rather than moving on to the next one, since
     the block is almost certainly environment-wide, not video-specific.
"""

_RATE_LIMIT_MARKERS = (
    "429",
    "too many requests",
    "blocking requests from your ip",
    "ip has been blocked",
    "requestblocked",
    "ipblocked",
)


def _classify_failure(attempts: list[dict]) -> str | None:
    """Return "rate_limited_or_ip_blocked" if any attempt's error text looks
    like YouTube throttling/blocking this machine, else None. Deliberately
    string-matches on known error phrasing from both youtube-transcript-api
    and yt-dlp rather than parsing HTTP status objects - both libraries only
    surface these as embedded text in the exception message."""
    for a in attempts:
        err = (a.get("error") or "").lower()
        if any(marker in err for marker in _RATE_LIMIT_MARKERS):
            return "rate_limited_or_ip_blocked"
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube transcript to a text file with metadata.",
        epilog=EXIT_CODES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url_or_id", help="YouTube URL (watch?v=, youtu.be/, /shorts/, /embed/) or a bare 11-character video ID")
    parser.add_argument("--output-dir", required=True,
                         help="Directory to write the transcript + metadata into (created if missing; "
                              "quote it if the path contains spaces). No files are ever written outside this directory.")
    parser.add_argument("--slug", default=None, help="Optional short slug folded into the output filename")
    parser.add_argument("--languages", default="ru,en",
                         help="Comma-separated language preference order, tried in this order by both fetch methods (default: ru,en)")
    parser.add_argument("--mode", choices=["transcript", "subtitles", "auto", "whisper"], default="auto",
                         help="transcript=youtube-transcript-api only, subtitles=yt-dlp only, "
                              "auto=try transcript API then fall back to yt-dlp (default: auto), "
                              "whisper=local faster-whisper transcription only (explicit opt-in - "
                              "NOT tried by auto; see module docstring for why)")
    parser.add_argument("--whisper-model", default="large-v3",
                         help="faster-whisper model size when --mode whisper (tiny/base/small/medium/large-v3). "
                              "Default: large-v3 - the only tier found to match a paid reference transcript "
                              "closely in testing; small/medium both dropped or fabricated content.")
    parser.add_argument("--whisper-language", default=None,
                         help="Force a language code (e.g. 'ru') for Whisper instead of auto-detecting. "
                              "Leave unset unless auto-detection is misfiring on a specific video.")
    parser.add_argument("--extension", choices=["txt", "md"], default="txt", help="Output transcript file extension (default: txt)")
    parser.add_argument(
        "--cookies-from-browser", default=None, metavar="BROWSER[:PROFILE]",
        help="Opt-in escalation path, off by default: authenticate yt-dlp's requests "
             "using an existing logged-in browser session's cookies (e.g. 'chrome', "
             "'firefox:Default') instead of anonymous requests. Use this when anonymous/"
             "VPN fetching keeps hitting a 429 or a 'Sign in to confirm you're not a "
             "bot' wall (exit code 2) - an authenticated session is far less likely to "
             "trigger either. Only affects the yt-dlp-based methods (subtitles, "
             "whisper's audio download) - youtube-transcript-api's own request is not "
             "authenticated by this flag. This script never reads, copies, logs, or "
             "writes cookie contents or the cookie database path itself - yt-dlp reads "
             "the named browser's own cookie store directly and only inside this "
             "process. Still stops (exit code 2) on a 429/bot-check even when "
             "authenticated - this is an escalation path for a small batch, not a "
             "guarantee, and not a reason to loop retries.",
    )
    args = parser.parse_args()

    languages = [lang.strip() for lang in args.languages.split(",") if lang.strip()]

    try:
        video_id = extract_video_id(args.url_or_id)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    slug = sanitize_slug(args.slug) if args.slug else ""

    attempts = []
    text = None
    lang_used = None
    is_generated = None
    method = None

    methods_to_try = []
    if args.mode in ("transcript", "auto"):
        methods_to_try.append("youtube-transcript-api")
    if args.mode in ("subtitles", "auto"):
        methods_to_try.append("yt-dlp")
    if args.mode == "whisper":
        methods_to_try.append(f"faster-whisper:{args.whisper_model}")

    for m in methods_to_try:
        try:
            if m == "youtube-transcript-api":
                text, lang_used, is_generated = try_transcript_api(video_id, languages)
            elif m == "yt-dlp":
                text, lang_used, is_generated = try_ytdlp_subtitles(video_id, languages, args.cookies_from_browser)
            else:
                text, lang_used, is_generated = try_whisper_local(video_id, args.whisper_model, args.whisper_language, args.cookies_from_browser)
            method = m
            break
        except Exception as e:
            attempts.append({"method": m, "error": str(e)})

    if text is None:
        print("Transcript retrieval failed. Attempted methods:", file=sys.stderr)
        for a in attempts:
            print(f"  - {a['method']}: {a['error']}", file=sys.stderr)
        reason_class = _classify_failure(attempts)
        fail_record = {
            "video_id": video_id,
            "url": args.url_or_id,
            "status": "failed",
            "attempts": attempts,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if args.cookies_from_browser:
            fail_record["cookies_from_browser"] = args.cookies_from_browser
        if reason_class == "rate_limited_or_ip_blocked":
            fail_record["reason_class"] = reason_class
            fail_record["next_retry_guidance"] = (
                "This looks like an environment-level YouTube rate-limit/IP-block, "
                "not a per-video captions problem. Do not immediately retry this or "
                "any other video in the same run/session - treat it as a circuit "
                "breaker and stop the whole fetch phase. Retry later (a real cooldown "
                "- tens of minutes to hours - not another immediate attempt), with at "
                "most one bounded retry rather than a retry loop."
            )
            print(
                "This looks like an environment-level rate-limit/IP-block "
                "(exit code 2) - stop fetching further videos this run.",
                file=sys.stderr,
            )
        # write a failure metadata record so the caller has evidence of what was tried
        os.makedirs(args.output_dir, exist_ok=True)
        fail_meta_path = os.path.join(
            args.output_dir,
            f"{video_id}.FAILED.meta.json",
        )
        with open(fail_meta_path, "w", encoding="utf-8") as f:
            json.dump(fail_record, f, indent=2, ensure_ascii=False)
        print(f"Failure details written to: {fail_meta_path}", file=sys.stderr)
        sys.exit(2 if reason_class == "rate_limited_or_ip_blocked" else 1)

    sha256_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    existing = find_existing_output(args.output_dir, video_id, sha256_hash)
    if existing:
        print(f"Transcript already exists (same video ID + content hash): {existing}")
        print(f"SHA-256 Hash: {sha256_hash}")
        sys.exit(0)

    os.makedirs(args.output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    hash8 = sha256_hash[:8]
    name_parts = [date_str]
    if slug:
        name_parts.append(slug)
    name_parts.append(video_id)
    name_parts.append(hash8)
    base_name = "_".join(name_parts)

    transcript_path = os.path.join(args.output_dir, f"{base_name}.{args.extension}")
    meta_path = os.path.join(args.output_dir, f"{base_name}.meta.json")

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(text)

    if method == "youtube-transcript-api":
        source_tool = "youtube-transcript-api"
    elif method == "yt-dlp":
        source_tool = "yt-dlp"
    else:
        source_tool = "faster-whisper"

    meta_record = {
        "url": args.url_or_id,
        "video_id": video_id,
        "language": lang_used,
        "is_generated_captions": is_generated,
        "method": method,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_tool": source_tool,
        "sha256": sha256_hash,
        "attempts_before_success": attempts,
    }
    if source_tool == "faster-whisper":
        # Flag this clearly for any downstream consumer: an ASR-on-audio transcript
        # is lower-fidelity than real captions even at the large-v3 tier (see the
        # module docstring) - extraction/summarization steps should treat facts
        # pulled from it with more skepticism than a real-captions transcript.
        meta_record["asr_fallback"] = True
        meta_record["whisper_model"] = args.whisper_model
    if args.cookies_from_browser and method in ("yt-dlp", f"faster-whisper:{args.whisper_model}"):
        # Record only that authenticated fetching was used, and which browser
        # name the caller supplied on the command line - never cookie contents
        # or the cookie database path itself.
        meta_record["authenticated_fetch"] = True
        meta_record["cookies_from_browser"] = args.cookies_from_browser

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_record, f, indent=2, ensure_ascii=False)

    print(f"Transcript saved to: {transcript_path}")
    print(f"Metadata saved to: {meta_path}")
    print(f"Method used: {method} (language={lang_used}, generated={is_generated})")
    print(f"SHA-256 Hash: {sha256_hash}")


if __name__ == "__main__":
    main()
