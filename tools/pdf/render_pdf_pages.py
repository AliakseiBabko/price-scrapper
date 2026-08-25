#!/usr/bin/env python3
"""Render a PDF's pages to images and pull each page's text layer.

Built for architect album/plan PDFs: the drawings are the evidence, and the
vector text layer carries the room names, dimensions and sheet titles that a
video frame of the same sheet cannot resolve.

Writes <outdir>/pages/NNN.png plus index.json holding, per page, its size,
text layer, and any drawing-like image blocks.

Usage:
  python tools/pdf/render_pdf_pages.py <file.pdf> [--outdir DIR] [--dpi 150]
      [--pages 1-10] [--no-text]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pymupdf

REPO = Path(__file__).resolve().parents[2]


def parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(total))
    out: list[int] = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a) - 1, int(b)))
        else:
            out.append(int(part) - 1)
    return [p for p in out if 0 <= p < total]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--outdir")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--pages", help="1-based, e.g. 1-10,14")
    ap.add_argument("--no-text", action="store_true")
    a = ap.parse_args()

    src = Path(a.pdf).resolve()
    doc = pymupdf.open(src)
    sha = hashlib.sha256(src.read_bytes()).hexdigest()
    # Cyrillic filenames collapse to the same ASCII slug - disambiguate by hash.
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", src.stem).strip("_")[:50] + "_" + sha[:8]
    out = Path(a.outdir) if a.outdir else REPO / "_Inbox" / "pdf_pages" / slug
    (out / "pages").mkdir(parents=True, exist_ok=True)
    wanted = parse_pages(a.pages, doc.page_count)
    pages = []
    for i in wanted:
        page = doc[i]
        pix = page.get_pixmap(dpi=a.dpi)
        name = "%03d.png" % (i + 1)
        pix.save(out / "pages" / name)
        rec = {
            "page": i + 1,
            "file": "pages/" + name,
            "width_pt": round(page.rect.width, 1),
            "height_pt": round(page.rect.height, 1),
            "orientation": "landscape" if page.rect.width >= page.rect.height else "portrait",
        }
        if not a.no_text:
            text = page.get_text().strip()
            rec["text"] = text
            rec["has_text_layer"] = bool(text)
        pages.append(rec)
        print("  page %d/%d" % (i + 1, doc.page_count), flush=True)

    meta = {
        "source_file": str(src.relative_to(REPO)) if src.is_relative_to(REPO) else str(src),
        "source_sha256": sha,
        "page_count": doc.page_count,
        "rendered_pages": len(pages),
        "dpi": a.dpi,
        "pdf_metadata": {k: v for k, v in (doc.metadata or {}).items() if v},
        "generated": datetime.now(timezone.utc).isoformat(),
        "pages": pages,
    }
    (out / "index.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print("done -> " + str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
