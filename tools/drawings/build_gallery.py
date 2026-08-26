#!/usr/bin/env python3
"""Build one HTML page that shows every drawing and render the repo has produced.

The tooling scatters PDFs, SVGs, renders and IFC files across data/outputs and
data/cad, which makes "what does the project look like right now" an
archaeology exercise. This walks those directories, thumbnails what can be
thumbnailed, and writes a single page to open in a browser.

Nothing is copied: the page links to the real files in place, so it always
shows the current state and never goes stale in a way you cannot see.

Usage:
  python tools/drawings/build_gallery.py
  start data/outputs/gallery/index.html
"""
from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCAN = [REPO / "data" / "outputs", REPO / "data" / "cad"]
DRAWABLE = {".pdf", ".svg", ".png", ".jpg", ".jpeg"}
MODELS = {".ifc", ".blend", ".dxf", ".glb", ".obj"}

VIEWER_HINT = {
    ".ifc": "IFC model - open in Blender with the Bonsai add-on, in a free viewer such as "
            "BIM Vision, or convert with tools/ifc/bin/IfcConvert.exe",
    ".blend": "Blender scene - open in Blender",
    ".dxf": "CAD drawing - open in DWG TrueView, LibreCAD or Homestyler",
    ".glb": "3D model - opens in the Windows 3D Viewer or any glTF viewer",
    ".obj": "3D mesh - opens in the Windows 3D Viewer or Blender",
}


def thumb_for(path: Path, thumbs: Path, dpi: int) -> Path | None:
    """PDFs get a rendered first page; raster and SVG are shown as they are."""
    if path.suffix.lower() != ".pdf":
        return None
    try:
        import pymupdf
    except ImportError:
        return None
    out = thumbs / (path.stem + "_" + str(abs(hash(str(path))) % 100000) + ".png")
    if out.exists() and out.stat().st_mtime >= path.stat().st_mtime:
        return out
    try:
        doc = pymupdf.open(path)
        doc[0].get_pixmap(dpi=dpi).save(out)
        return out
    except Exception:
        return None


def rel(target: Path, start: Path) -> str:
    import os
    return os.path.relpath(target, start).replace("\\", "/")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=REPO / "data" / "outputs" / "gallery" / "index.html")
    ap.add_argument("--dpi", type=int, default=70, help="thumbnail resolution for PDF pages")
    a = ap.parse_args()

    out_dir = a.out.parent
    thumbs = out_dir / "thumbs"
    thumbs.mkdir(parents=True, exist_ok=True)

    groups: dict[str, list[dict]] = {}
    for root in SCAN:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or thumbs in path.parents:
                continue
            ext = path.suffix.lower()
            if ext not in DRAWABLE and ext not in MODELS:
                continue
            group = str(path.parent.relative_to(REPO)).replace("\\", "/")
            groups.setdefault(group, []).append({
                "path": path,
                "ext": ext,
                "size_kb": round(path.stat().st_size / 1024),
                "mtime": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                "thumb": thumb_for(path, thumbs, a.dpi),
            })

    order = sorted(groups, key=lambda g: (0 if "variants" in g else 1 if "current_apartment" in g
                                          else 2 if g.endswith("cad") else 3, g))

    parts = ["""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Drawings and models — price-scrapper</title>
<style>
 :root { color-scheme: light dark; --bg:#fbfbf9; --fg:#1c1c1a; --mut:#6d6d66; --card:#fff; --line:#e2e2dc; }
 @media (prefers-color-scheme: dark){ :root{ --bg:#16171a; --fg:#e9e9e4; --mut:#9a9a92; --card:#1e2024; --line:#2f3238; } }
 body { margin:0; padding:32px; background:var(--bg); color:var(--fg);
        font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif; }
 h1 { font-size:22px; margin:0 0 4px; } h2 { font-size:15px; margin:34px 0 10px; color:var(--mut);
      font-weight:600; letter-spacing:.02em; }
 .sub { color:var(--mut); margin-bottom:8px; }
 .grid { display:grid; gap:14px; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); }
 .card { background:var(--card); border:1px solid var(--line); border-radius:10px; overflow:hidden;
         display:flex; flex-direction:column; }
 .card a.view { display:block; background:#fff; }
 .card img, .card object { width:100%; height:190px; object-fit:contain; display:block; }
 .meta { padding:9px 11px; font-size:12.5px; }
 .name { font-weight:600; word-break:break-all; }
 .dim { color:var(--mut); font-size:11.5px; margin-top:3px; }
 .hint { padding:26px 12px; text-align:center; color:var(--mut); font-size:12.5px;
         background:repeating-linear-gradient(45deg,transparent,transparent 8px,rgba(125,125,125,.06) 8px,rgba(125,125,125,.06) 16px); }
 code { font-size:12px; }
</style></head><body>"""]
    parts.append("<h1>Drawings and models</h1>")
    parts.append('<div class="sub">Generated %s · every tile links to the real file on disk · '
                 'nothing here is for construction</div>' % datetime.now().strftime("%Y-%m-%d %H:%M"))

    total = 0
    for group in order:
        items = groups[group]
        total += len(items)
        parts.append("<h2>%s</h2><div class='grid'>" % html.escape(group))
        for it in items:
            href = rel(it["path"], out_dir)
            if it["thumb"]:
                media = '<img src="%s" alt="">' % rel(it["thumb"], out_dir)
            elif it["ext"] in {".png", ".jpg", ".jpeg"}:
                media = '<img src="%s" alt="">' % href
            elif it["ext"] == ".svg":
                media = '<img src="%s" alt="">' % href
            else:
                media = '<div class="hint">%s</div>' % html.escape(
                    VIEWER_HINT.get(it["ext"], "open with an external application"))
            parts.append(
                '<div class="card"><a class="view" href="%s" target="_blank">%s</a>'
                '<div class="meta"><div class="name">%s</div>'
                '<div class="dim">%s · %d KB · %s</div></div></div>'
                % (href, media, html.escape(it["path"].name),
                   it["ext"].lstrip("."), it["size_kb"], it["mtime"]))
        parts.append("</div>")

    parts.append("</body></html>")
    a.out.write_text("\n".join(parts), encoding="utf-8")
    print(json.dumps({"page": str(a.out.relative_to(REPO)), "groups": len(groups),
                      "files": total}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
