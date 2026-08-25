#!/usr/bin/env python3
"""Pair a YouTube video's timestamped transcript with video frames.

Built for apartment-layout-analysis videos: the author talks over a floor
plan, and the useful evidence is the *plan on screen at that moment*, not
the words alone.

Pipeline:
  1. fetch the timestamped transcript (original language, never translated)
  2. cut it into logical segments on discourse cues + pause/length limits
  3. download a video-only stream with yt-dlp
  4. run ffmpeg scene detection to find where the picture actually changes
  5. for each segment, grab the frame from the scene that covers it
  6. write frames/ + index.json + index.md pairing segment text to frame

Usage:
  python tools/youtube/extract_layout_frames.py <url-or-id> [--outdir DIR]
      [--format 136] [--lang ru] [--scene 0.25] [--min-seg 25] [--max-seg 120]
      [--times 90,215,430]   # explicit timestamps instead of auto-segmenting
      [--keep-video]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# Discourse markers that, in these layout videos, start a new logical unit:
# a numbered problem, a proposed change, a pro/con, a new zone.
CUE_PATTERNS = [
    r"\bво-первых\b", r"\bво-вторых\b", r"\bв-третьих\b", r"\bв-четвёртых\b", r"\bв-пятых\b",
    r"\b(перв|втор|трет|четвёрт|четверт|пят|шест|седьм|восьм)\w*\s+(проблема|минус|плюс|вариант|нюанс|момент)\b",
    r"\bпроблема\s+(заключается|состоит|номер)\b",
    r"\b(следующ\w+|ещё одна|вторая|третья)\s+(проблема|сложность)\b",
    r"\bтеперь\s+(расскажу|давайте|перейдём|перейдем|посмотрим|разберём|разберем)\b",
    r"\b(перейдём|перейдем|переходим)\s+к\b",
    r"\bчто\s+(я\s+)?(предлагаю|сделал|сделаем)\b",
    r"\b(предлагаю|предлагается)\b",
    r"\bвариант\s+(номер\s+)?\w+\b",
    r"\bпервое решение\b", r"\bвторое решение\b",
    r"\b(итоговая|получившаяся|новая|итоговый)\s+(планировк|вариант|план)\w*\b",
    r"\b(плюс|минус)ы?\s+(этого|такого|данного)\b",
    r"\b(достоинств|преимуществ|недостатк)\w+\b",
    r"\b(кухн|прихож|коридор|санузел|ванн|спальн|гостин|детск|балкон|лоджи|гардероб)\w*\s+(при\s+)?(взгляд|выглядел|получ)\w*",
    r"\bдавайте\s+(посмотрим|разберём|разберем)\b",
]
CUE_RE = re.compile("|".join(CUE_PATTERNS), re.IGNORECASE)


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", **kw)


def video_id(s: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[\w-]{11}", s):
        return s
    raise SystemExit("cannot parse a video id out of " + repr(s))


def fetch_cues(vid: str, lang: str) -> tuple[list[dict], str]:
    """Return [{start, duration, text}, ...] in the ORIGINAL language."""
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    listing = api.list(vid)
    try:
        tr = listing.find_manually_created_transcript([lang])
    except Exception:
        tr = listing.find_transcript([lang])
    if getattr(tr, "is_translated", False) or tr.language_code != lang:
        raise SystemExit("refusing a translated/mismatched transcript - original language only")
    cues = [{"start": c.start, "duration": c.duration, "text": c.text.replace("\n", " ").strip()}
            for c in tr.fetch()]
    return cues, tr.language_code


def segment(cues: list[dict], min_len: float, max_len: float) -> list[dict]:
    """Group cues into logical segments on discourse cues, bounded by length."""
    segs: list[dict] = []
    cur: list[dict] = []

    def flush():
        if not cur:
            return
        start = cur[0]["start"]
        end = cur[-1]["start"] + cur[-1]["duration"]
        segs.append({"start": start, "end": end,
                     "text": " ".join(c["text"] for c in cur).strip()})

    for c in cues:
        if cur:
            span = (c["start"] + c["duration"]) - cur[0]["start"]
            starts_unit = bool(CUE_RE.search(c["text"]))
            if (starts_unit and span >= min_len) or span >= max_len:
                flush()
                cur = []
        cur.append(c)
    flush()
    for i, s in enumerate(segs, 1):
        s["index"] = i
    return segs


def download_video(vid: str, fmt: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "yt_dlp", "-f", fmt, "--no-playlist",
           "--js-runtimes", "node,deno",
           "-o", str(dest), "https://www.youtube.com/watch?v=" + vid]
    p = run(cmd)
    if not dest.exists():
        cands = sorted(dest.parent.glob(dest.stem + ".*"))
        if cands:
            return cands[0]
        raise SystemExit("yt-dlp failed:\n" + p.stdout[-2000:] + "\n" + p.stderr[-2000:])
    return dest


def scene_times(video: Path, threshold: float) -> list[float]:
    """Timestamps (s) where the picture changes - i.e. a new plan/slide."""
    p = run(["ffmpeg", "-i", str(video), "-vf",
             "select='gt(scene," + str(threshold) + ")',metadata=print",
             "-an", "-f", "null", "-"])
    times = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", p.stderr)]
    return sorted(set([0.0] + times))


def still_windows(seg: dict, scenes: list[float]) -> list[tuple[float, float]]:
    """Windows inside the segment during which the picture does not change.

    A long window means a plan is sitting still on screen; a short one is
    usually a pan/zoom/animation frame and makes a poor screenshot.
    """
    s, e = seg["start"], seg["end"]
    inside = [t for t in scenes if s <= t < e]
    covering = [t for t in scenes if t <= s]
    starts = ([covering[-1]] if covering else [s]) + inside
    wins = []
    for i, st in enumerate(starts):
        nxt = starts[i + 1] if i + 1 < len(starts) else e
        wins.append((max(st, s), min(nxt, e)))
    return sorted(wins, key=lambda w: w[1] - w[0], reverse=True)


def pick_frame_times(seg: dict, scenes: list[float], count: int) -> list[tuple[float, float]]:
    """(timestamp, stillness_seconds) for the `count` steadiest shots."""
    picks = []
    for win_s, win_e in still_windows(seg, scenes)[:count]:
        span = win_e - win_s
        # sample late in the still window: on-screen arrows/labels get drawn
        # after the shot settles.
        t = win_s + (span * 0.75 if span < 4 else span - 1.0)
        picks.append((round(max(t, 0.0), 2), round(span, 2)))
    return picks or [(round(seg["start"], 2), 0.0)]


def grab(video: Path, t: float, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-ss", str(t), "-i", str(video), "-frames:v", "1",
         "-q:v", "2", str(out)])


def hhmmss(t: float) -> str:
    t = int(t)
    return "%02d:%02d:%02d" % (t // 3600, (t % 3600) // 60, t % 60)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--outdir")
    ap.add_argument("--format", default="136", help="yt-dlp format id (136=720p, 137=1080p)")
    ap.add_argument("--lang", default="ru")
    ap.add_argument("--scene", type=float, default=0.25)
    ap.add_argument("--min-seg", type=float, default=25.0)
    ap.add_argument("--max-seg", type=float, default=120.0)
    ap.add_argument("--times", help="comma-separated seconds; skip auto-segmenting")
    ap.add_argument("--per-seg", type=int, default=1,
                    help="frames per segment, taken from the steadiest shots")
    ap.add_argument("--keep-video", action="store_true")
    a = ap.parse_args()

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg not on PATH")

    vid = video_id(a.video)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out = Path(a.outdir) if a.outdir else REPO / "_Inbox" / "frames" / (stamp + "_" + vid)
    out.mkdir(parents=True, exist_ok=True)

    print("[1/5] transcript " + vid + " (" + a.lang + ")", flush=True)
    cues, lang = fetch_cues(vid, a.lang)

    if a.times:
        marks = [float(x) for x in a.times.split(",")]
        segs = []
        for i, t in enumerate(marks, 1):
            end = marks[i] if i < len(marks) else cues[-1]["start"] + cues[-1]["duration"]
            txt = " ".join(c["text"] for c in cues if t <= c["start"] < end)
            segs.append({"index": i, "start": t, "end": end, "text": txt.strip()})
    else:
        segs = segment(cues, a.min_seg, a.max_seg)
    print("      %d cues -> %d segments" % (len(cues), len(segs)), flush=True)

    print("[2/5] download stream fmt=" + a.format, flush=True)
    video = download_video(vid, a.format, out / (vid + ".mp4"))

    print("[3/5] scene detection", flush=True)
    scenes = scene_times(video, a.scene)
    print("      %d scene changes" % len(scenes), flush=True)

    print("[4/5] frame extraction", flush=True)
    frames_dir = out / "frames"
    if frames_dir.exists():
        shutil.rmtree(frames_dir)  # stale frames from an earlier run would mislead
    for s_ in segs:
        s_["frames"] = []
        for k, (t, still) in enumerate(pick_frame_times(s_, scenes, a.per_seg), 1):
            name = "%02d%s_%s.jpg" % (s_["index"], "" if a.per_seg == 1 else chr(96 + k),
                                      hhmmss(t).replace(":", ""))
            grab(video, t, frames_dir / name)
            s_["frames"].append({"file": "frames/" + name, "time": t, "still_seconds": still})

    print("[5/5] index", flush=True)
    meta = {"video_id": vid, "url": "https://www.youtube.com/watch?v=" + vid,
            "language": lang, "format": a.format, "scene_threshold": a.scene,
            "generated": datetime.now(timezone.utc).isoformat(),
            "segments": segs}
    (out / "index.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Frame/transcript pairs - " + vid, "",
             "Source: https://www.youtube.com/watch?v=" + vid + " (language: " + lang + ")", ""]
    for s in segs:
        lines += ["## %02d. %s-%s" % (s["index"], hhmmss(s["start"]), hhmmss(s["end"])), ""]
        for f in s["frames"]:
            lines += ["![%s](%s) <!-- @%s, still %.1fs -->" % (
                s["index"], f["file"], hhmmss(f["time"]), f["still_seconds"]), ""]
        lines += [s["text"], ""]
    (out / "index.md").write_text("\n".join(lines), encoding="utf-8")

    if not a.keep_video:
        video.unlink(missing_ok=True)
    print("done -> " + str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
