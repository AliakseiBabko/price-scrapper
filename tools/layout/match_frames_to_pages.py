#!/usr/bin/env python3
"""Match video frames to the PDF sheets they show on screen.

These architects narrate over their own album: the frame is a 720p/1080p
photograph of a sheet that also exists as vector art in the PDF. Matching the
two lets a case cite the crisp sheet for dimensions while keeping the frame as
proof of what was said about it.

Method: normalised cross-correlation of heavily downsampled grayscale images,
tried against the frame as-is and against a few centre crops (the sheet is
often letterboxed or slightly zoomed inside the frame). Cheap, no OpenCV.

Usage:
  python tools/layout/match_frames_to_pages.py <frames_dir> <pdf_pages_dir>
      [--min-score 0.55] [--out matches.json]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pymupdf

REPO = Path(__file__).resolve().parents[2]
N = 128  # comparison resolution - below ~96 near-identical plan variants stop being separable


def raw_gray(path: Path) -> np.ndarray:
    doc = pymupdf.open(path)
    pix = doc[0].get_pixmap(colorspace=pymupdf.csGRAY)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)


def resize(a: np.ndarray) -> np.ndarray:
    h, w = a.shape
    if h < 2 or w < 2:
        return np.zeros((N, N), dtype=np.float32)
    ys = (np.arange(N) * h // N).clip(0, h - 1)
    xs = (np.arange(N) * w // N).clip(0, w - 1)
    return a[np.ix_(ys, xs)].astype(np.float32)


def crop(a: np.ndarray, box: tuple[float, float, float, float]) -> np.ndarray:
    h, w = a.shape
    x0, y0, x1, y1 = box
    return a[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]


def ink_bbox(a: np.ndarray, left_fraction: float = 0.6) -> np.ndarray:
    """Crop to the drawing itself.

    Video sheets and PDF sheets place the same plan differently on the page,
    so comparing whole pages fails. Both put the plan on the left, though, so
    tightening onto the ink in the left band lines the two up.
    """
    band = crop(a, (0.0, 0.0, left_fraction, 1.0))
    dark = band < 200
    rows, cols = np.where(dark)
    if rows.size < 50:
        return band
    return band[rows.min():rows.max() + 1, cols.min():cols.max() + 1]


def ncc(a: np.ndarray, b: np.ndarray) -> float:
    a = a - a.mean()
    b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d else 0.0


def variants_of(path: Path) -> list[np.ndarray]:
    """Comparison vectors: the whole image, and the plan drawing cropped out."""
    a = raw_gray(path)
    out = []
    for frac in (0.5, 0.55, 0.6, 0.72):
        out.append(resize(ink_bbox(a, frac)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("frames_dir")
    ap.add_argument("pdf_pages_dir")
    ap.add_argument("--min-score", type=float, default=0.35,
                    help="floor below which the frame is assumed to show no sheet at all (talking head, intro)")
    ap.add_argument("--min-margin", type=float, default=0.08,
                    help="relative gap between the best and runner-up page needed to call a match")
    ap.add_argument("--out", default="frame_page_matches.json")
    a = ap.parse_args()

    fdir = Path(a.frames_dir)
    pdir = Path(a.pdf_pages_dir)
    frames = sorted((fdir / "frames").glob("*.jpg"))
    pages = sorted((pdir / "pages").glob("*.png"))
    if not frames or not pages:
        raise SystemExit("need %s/frames/*.jpg and %s/pages/*.png" % (fdir, pdir))

    print("loading %d pages" % len(pages), flush=True)
    page_vecs = {p.stem: variants_of(p) for p in pages}

    results = []
    for f in frames:
        fvars = variants_of(f)
        scores = [(max(ncc(v, pv) for v in fvars for pv in pvars), name)
                  for name, pvars in page_vecs.items()]
        ranked = sorted(scores, reverse=True)[:3]
        top, second = ranked[0][0], (ranked[1][0] if len(ranked) > 1 else 0.0)
        margin = (top - second) / top if top > 0 else 0.0
        rec = {
            "frame": "frames/" + f.name,
            "page": int(ranked[0][1]),
            "score": round(top, 3),
            "margin": round(margin, 3),
            "confident": margin >= a.min_margin and top >= a.min_score,
            "candidates": [{"page": int(k), "score": round(sc, 3)} for sc, k in ranked],
        }
        results.append(rec)
        print("  %s -> page %s (score %.3f, margin %.0f%%)%s" % (
            f.name, rec["page"], top, margin * 100, "" if rec["confident"] else "  [check]"), flush=True)

    out = fdir / a.out
    out.write_text(json.dumps({
        "frames_dir": str(fdir),
        "pdf_pages_dir": str(pdir),
        "min_score": a.min_score,
        "min_margin": a.min_margin,
        "matches": results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    hits = sum(1 for r in results if r["confident"])
    print("%d/%d frames matched with a clear margin -> %s" % (hits, len(results), out))
    print("Scores are relative, not absolute: always eyeball the frame against the page it names.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
