#!/usr/bin/env python3
"""Lay the CAD wall geometry over the developer's raster plan.

The owner drew the Homestyler layout on top of the developer's detailed plan as
a base image, so the two share a coordinate frame up to a scale and an offset.
Recovering that transform is worth doing twice over:

  * it checks the CAD extraction against the plan it came from - if the vector
    walls land on the drawn walls, the extraction is right;
  * it turns the raster into a tracing surface in millimetres, which is how the
    developer's own partitions can become v0 geometry.

Registration is by the wall ink: the drawn plan's wall region and the CAD wall
region should have the same bounding box, because they are the same building.
Dimension lines and text sit outside that box, so they are trimmed by looking
only at strong ink and taking the largest connected structure.

Usage:
  python tools/cad/overlay_plan.py                       # auto-register and report
  python tools/cad/overlay_plan.py --mm-per-px 6.13 --offset-px 120 95
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pymupdf

REPO = Path(__file__).resolve().parents[2]
RASTER = REPO / "_Inbox" / "_Visual_Drop" / "fllor_plan_detailed.jpeg"
WALL_PLAN = REPO / "data" / "cad" / "wall_plan.json"


def load_gray(path: Path, zoom: float = 1.0) -> np.ndarray:
    doc = pymupdf.open(path)
    pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), colorspace=pymupdf.csGRAY)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)


def largest_structure(dark: np.ndarray) -> tuple[int, int, int, int]:
    """Bounding box of the biggest connected run of ink - the walls, not the text."""
    h, w = dark.shape
    seen = np.zeros_like(dark)
    best = (0, (0, 0, 0, 0))
    for sy in range(0, h, 2):
        for sx in range(0, w, 2):
            if not dark[sy, sx] or seen[sy, sx]:
                continue
            stack = [(sy, sx)]
            seen[sy, sx] = True
            cells = 0
            x0 = x1 = sx
            y0 = y1 = sy
            while stack:
                y, x = stack.pop()
                cells += 1
                x0, x1 = min(x0, x), max(x1, x)
                y0, y1 = min(y0, y), max(y1, y)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and dark[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            if cells > best[0]:
                best = (cells, (x0, y0, x1, y1))
    return best[1]


def cad_mask(plan, mm_per_px, env_h):
    """The CAD wall region rasterised at one cell per image pixel."""
    nx = int(plan["envelope_mm"]["width"] / mm_per_px) + 2
    ny = int(env_h / mm_per_px) + 2
    edges = [(c[i][0], c[i][1], c[i + 1][0], c[i + 1][1])
             for c in plan["outline_mm"] for i in range(len(c) - 1)
             if abs(c[i + 1][1] - c[i][1]) > 1e-9]
    mask = np.zeros((ny, nx), dtype=bool)
    for row in range(ny):
        yc = (row + 0.5) * mm_per_px
        xs = sorted(x0 + (yc - y0) * (x1 - x0) / (y1 - y0)
                    for x0, y0, x1, y1 in edges if (y0 > yc) != (y1 > yc))
        for i in range(0, len(xs) - 1, 2):
            lo = max(0, int(xs[i] / mm_per_px))
            hi = min(nx, int(xs[i + 1] / mm_per_px) + 1)
            if hi > lo:
                mask[row, lo:hi] = True
    return np.flipud(mask)


def write_diff(plan, gray, mm_per_px, ox, oy, env_w, env_h, out_ppm: Path) -> dict:
    """Green where the CAD wall sits on a drawn wall, red where it does not.

    Red is what the redesign added. It also picks up registration jitter along
    hatched edges, so read it as "look here", not as a measurement.
    """
    mask = cad_mask(plan, mm_per_px, env_h)
    ih, iw = gray.shape
    h = min(mask.shape[0], ih - oy)
    w = min(mask.shape[1], iw - ox)
    drawn = gray[oy:oy + h, ox:ox + w] < 140
    thick = drawn.copy()
    for s in (1, 2):  # the hatching is drawn as strokes, so close the gaps
        thick[s:, :] |= drawn[:-s, :]
        thick[:-s, :] |= drawn[s:, :]
        thick[:, s:] |= drawn[:, :-s]
        thick[:, :-s] |= drawn[:, s:]
    cad = mask[:h, :w]
    added = cad & ~thick

    rgb = np.stack([gray] * 3, -1).copy()
    sub = rgb[oy:oy + h, ox:ox + w]
    sub[cad & thick] = [60, 140, 60]
    sub[added] = [220, 60, 60]
    rgb[oy:oy + h, ox:ox + w] = sub
    nl = chr(10)
    header = ("P6" + nl + "%d %d" % (iw, ih) + nl + "255" + nl).encode("ascii")
    out_ppm.write_bytes(header + np.ascontiguousarray(rgb).tobytes())

    return {
        "cad_wall_px": int(cad.sum()),
        "on_drawn_wall_px": int((cad & thick).sum()),
        "added_by_redesign_px": int(added.sum()),
        "added_share_pct": round(100 * added.sum() / max(cad.sum(), 1), 1),
        "image": str(out_ppm.name),
        "reading": "Green = CAD wall on a drawn wall (shared shell and retained partitions). "
                   "Red = CAD wall with nothing drawn under it, i.e. added by the redesign - "
                   "plus some jitter along hatched edges.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raster", type=Path, default=RASTER)
    ap.add_argument("--wall-plan", type=Path, default=WALL_PLAN)
    ap.add_argument("--out", type=Path, default=REPO / "data" / "cad" / "overlay_developer_plan.svg")
    ap.add_argument("--mm-per-px", type=float, help="skip auto-registration")
    ap.add_argument("--offset-px", type=float, nargs=2, help="plan origin in image pixels")
    ap.add_argument("--threshold", type=int, default=110, help="ink darkness cutoff")
    ap.add_argument("--diff", action="store_true",
                    help="also write a PPM comparing CAD walls with the drawn walls")
    a = ap.parse_args()

    a.raster = a.raster.resolve()
    plan = json.loads(a.wall_plan.read_text(encoding="utf-8"))
    env_w = plan["envelope_mm"]["width"]
    env_h = plan["envelope_mm"]["depth"]

    gray = load_gray(a.raster)
    ih, iw = gray.shape
    dark = gray < a.threshold

    if a.mm_per_px and a.offset_px:
        mm_per_px = a.mm_per_px
        ox, oy = a.offset_px
        box = None
    else:
        box = largest_structure(dark)
        bx0, by0, bx1, by1 = box
        sx = env_w / max(bx1 - bx0, 1)
        sy = env_h / max(by1 - by0, 1)
        mm_per_px = (sx + sy) / 2.0
        ox, oy = bx0, by0

    report = {
        "raster": str(a.raster.relative_to(REPO)) if a.raster.is_relative_to(REPO) else str(a.raster),
        "image_px": [iw, ih],
        "cad_envelope_mm": [env_w, env_h],
        "registration": {
            "mm_per_px": round(mm_per_px, 4),
            "origin_px": [round(ox, 1), round(oy, 1)],
            "ink_bbox_px": list(box) if box else None,
            "aspect_check": {
                "cad": round(env_w / env_h, 4),
                "ink": round((box[2] - box[0]) / max(box[3] - box[1], 1), 4) if box else None,
            },
        },
    }
    if box:
        cad_aspect = env_w / env_h
        ink_aspect = (box[2] - box[0]) / max(box[3] - box[1], 1)
        report["registration"]["aspect_error_pct"] = round(
            abs(cad_aspect - ink_aspect) / cad_aspect * 100, 2)

    # SVG in image pixel space: raster underneath, CAD walls over it.
    parts = ['<?xml version="1.0" encoding="utf-8"?>',
             '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             'viewBox="0 0 %d %d" width="%d">' % (iw, ih, min(iw, 1400)),
             '<image xlink:href="%s" x="0" y="0" width="%d" height="%d"/>'
             % (a.raster.as_uri(), iw, ih)]
    parts.append('<g fill="#1c6ea4" fill-opacity="0.30" stroke="#1c6ea4" stroke-width="1">')
    for cycle in plan["outline_mm"]:
        pts = " ".join("%.1f,%.1f" % (ox + px / mm_per_px, oy + (env_h - py) / mm_per_px)
                       for px, py in cycle)
        parts.append('<polygon points="%s"/>' % pts)
    parts.append("</g>")
    parts.append('<g fill="#c23b3b" fill-opacity="0.55">')
    for o in plan["openings"]:
        ow = o["width_mm"] if o["horizontal"] else o["depth_mm"]
        oh = o["depth_mm"] if o["horizontal"] else o["width_mm"]
        parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
                     % (ox + o["x_mm"] / mm_per_px,
                        oy + (env_h - o["y_mm"] - oh) / mm_per_px,
                        max(ow / mm_per_px, 2), max(oh / mm_per_px, 2)))
    parts.append("</g>")
    if box:
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#2c7a3f" '
                     'stroke-width="2" stroke-dasharray="6 4"/>'
                     % (box[0], box[1], box[2] - box[0], box[3] - box[1]))
    parts.append("</svg>")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(parts), encoding="utf-8")

    if a.diff:
        report["diff"] = write_diff(plan, gray, mm_per_px, int(ox), int(oy),
                                    env_w, env_h,
                                    a.out.with_name(a.out.stem + "_diff.ppm"))

    (a.out.with_suffix(".json")).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                            encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("overlay -> %s" % a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
