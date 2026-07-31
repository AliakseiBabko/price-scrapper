import sys
import json
import os
import hashlib
import csv
import re
import tempfile
import shutil
from datetime import datetime, timezone
from youtube_transcript_api import YouTubeTranscriptApi

# Whisper model size for the local-transcription fallback. "small" is a reasonable
# accuracy/speed tradeoff for renovation-video Russian/English speech on a laptop CPU;
# bump to "medium" if accuracy on a specific video is poor, or down to "base" if speed
# matters more than accuracy for a large batch.
WHISPER_MODEL_SIZE = "small"


def get_transcript_from_captions(video_id):
    """Primary path: pull existing YouTube captions (manual, then auto-generated)."""
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    try:
        transcript = transcript_list.find_transcript(['en', 'ru'])
    except Exception:
        # Fallback to generated if manually created doesn't exist
        transcript = transcript_list.find_generated_transcript(['ru', 'en'])
    text = " ".join([entry.text for entry in transcript.fetch()])
    return text


def get_transcript_from_whisper(url, video_id, model_size=WHISPER_MODEL_SIZE):
    """
    Fallback path for videos with captions/subtitles disabled: download audio with
    yt-dlp and transcribe locally with faster-whisper. Slower (minutes, not seconds)
    and lower-fidelity than real captions (no speaker labels, ASR errors of its own),
    but the only way to get anything at all from a captions-disabled video.
    """
    import yt_dlp
    from faster_whisper import WhisperModel

    tmp_dir = tempfile.mkdtemp(prefix="yt_audio_")
    try:
        audio_path_template = os.path.join(tmp_dir, f"{video_id}.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_path_template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }],
            "quiet": True,
            "no_warnings": True,
        }
        print(f"No captions available - downloading audio for local transcription (this takes a few minutes)...", file=sys.stderr)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio_files = [f for f in os.listdir(tmp_dir) if f.startswith(video_id)]
        if not audio_files:
            raise RuntimeError("Audio download produced no output file")
        audio_path = os.path.join(tmp_dir, audio_files[0])

        print(f"Transcribing locally with faster-whisper ({model_size} model, first run downloads the model)...", file=sys.stderr)
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        # language=None lets Whisper auto-detect (this project's sources are a mix of
        # Russian and English) rather than assuming one language up front.
        segments, info = model.transcribe(audio_path, language=None, vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments)
        print(f"Whisper detected language: {info.language} (confidence {info.language_probability:.2f})", file=sys.stderr)
        return text
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def sanitize_slug(slug):
    # Remove invalid Windows filename characters and limit length
    slug = re.sub(r'[\\/*?:"<>|]', "", slug)
    return slug.strip().replace(" ", "_")[:50]

def is_duplicate(file_hash):
    csv_file = os.path.join("00_Master", "processed_sources.csv")
    if not os.path.exists(csv_file):
        return False
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("source_hash") == file_hash:
                    return True
    except Exception as e:
        print(f"Error: Could not check duplicates in CSV: {e}", file=sys.stderr)
        sys.exit(1)
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_youtube_transcript.py <youtube_url> [slug_name] [--whisper] [--model=SIZE]")
        print("  --whisper      Force local Whisper transcription for this run (manual opt-in only - see below).")
        print("  --model=SIZE   Whisper model size (tiny/base/small/medium/large-v3). Default: " + WHISPER_MODEL_SIZE)
        print()
        print("Note: if captions are unavailable, this script now fails/skips by default rather than")
        print("silently falling back to Whisper. Decision made 2026-07-31 after comparing small/medium")
        print("Whisper output against a reference transcript (Turboscribe) on a real video: both tiers")
        print("dropped or fabricated whole clauses (~55-65% faithful content recovery), which is not safe")
        print("to feed into the knowledge base unreviewed. Pass --whisper explicitly to opt in for a")
        print("specific video you're willing to manually review, or use Turboscribe (no API - manual only)")
        print("for anything you actually want trusted.")
        sys.exit(1)

    url = sys.argv[1]
    rest_args = sys.argv[2:]
    force_whisper = "--whisper" in rest_args
    model_size = WHISPER_MODEL_SIZE
    for a in rest_args:
        if a.startswith("--model="):
            model_size = a.split("=", 1)[1]
    positional_args = [a for a in rest_args if a != "--whisper" and not a.startswith("--model=")]
    raw_slug = positional_args[0] if positional_args else "youtube_video"
    slug = sanitize_slug(raw_slug)
    if not slug:
        slug = "youtube_video"

    video_id = None
    if "v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]

    if not video_id:
        print("Could not extract video ID from URL", file=sys.stderr)
        sys.exit(1)

    method = "youtube-transcript-api"
    text = None

    if not force_whisper:
        try:
            text = get_transcript_from_captions(video_id)
        except Exception as e:
            # Deliberately does NOT auto-fall-back to Whisper here (see the usage note
            # above) - local Whisper (small or medium) was found to drop or fabricate
            # whole clauses on a real test video, unsafe to feed into the knowledge base
            # without review. Skip by default; re-run with --whisper to opt in manually.
            print(f"Error fetching transcript: {e}", file=sys.stderr)
            print("Skipping (captions unavailable). Re-run with --whisper to opt into local", file=sys.stderr)
            print("transcription for this video, or transcribe manually (e.g. Turboscribe) instead.", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            text = get_transcript_from_whisper(url, video_id, model_size=model_size)
            method = f"whisper-local-{model_size}"
        except Exception as e:
            print(f"Error: Whisper transcription failed: {e}", file=sys.stderr)
            sys.exit(1)

    if text:
        # Hash the text
        sha256_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

        if is_duplicate(sha256_hash):
            print(f"Error: Transcript already processed! (Duplicate hash: {sha256_hash})", file=sys.stderr)
            sys.exit(1)

        hash8 = sha256_hash[:8]

        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{date_str}_{slug}_{hash8}.txt"
        out_dir = os.path.join("00_Inbox", "transcripts")
        os.makedirs(out_dir, exist_ok=True)

        file_path = os.path.join(out_dir, filename)

        # newline='' prevents Python's universal-newline translation (\n -> \r\n on
        # Windows) so the bytes written to disk exactly match what was hashed above.
        with open(file_path, "w", encoding="utf-8", newline='') as f:
            f.write(text)

        # Sidecar metadata so downstream processing/logging knows this transcript came
        # from ASR-on-audio rather than YouTube's own captions - lower fidelity, no
        # existing speaker/caption-quality signal, worth flagging in any extraction note.
        meta_path = file_path.rsplit(".", 1)[0] + ".meta.json"
        with open(meta_path, "w", encoding="utf-8", newline='') as f:
            json.dump({
                "url": url,
                "video_id": video_id,
                "method": method,
                "sha256": sha256_hash,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            }, f, ensure_ascii=False, indent=2)

        print(f"Transcript saved to: {file_path}")
        print(f"Method: {method}")
        print(f"SHA-256 Hash: {sha256_hash}")
    else:
        print("Transcript was empty.", file=sys.stderr)
        sys.exit(1)
