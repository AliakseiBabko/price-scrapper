#!/usr/bin/env python3
"""Generate a deterministic manifest of the numbered-folder wiki pages.

The positive page population is deliberately narrow: Markdown files directly
under a numbered folder (Guide/page roots, excluding *_Index.md) and Markdown
files directly under that folder's analysis/ directory. Source notes, change
logs, case studies, and the intermediate store are not wiki pages for this
manifest.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUMBERED = re.compile(r"^(?!00_)\d{2}_.+$")  # excludes 00_Master (project docs, not wiki pages)
TAG_RE = re.compile(r"^tags\s*:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


def pages() -> list[tuple[Path, str]]:
    result: list[tuple[Path, str]] = []
    for folder in sorted(p for p in ROOT.iterdir() if p.is_dir() and NUMBERED.match(p.name)):
        for path in sorted(folder.glob("*.md")):
            if not path.name.endswith("_Index.md"):
                result.append((path, "guide"))
        analysis = folder / "analysis"
        if analysis.is_dir():
            result.extend((path, "detail") for path in sorted(analysis.glob("*.md")))
    return result


def git_timestamp(path: Path) -> tuple[str, str]:
    rel = path.relative_to(ROOT).as_posix()
    proc = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", rel],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode == 0 and proc.stdout.strip():
        return proc.stdout.strip(), "git"
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(), "filesystem_mtime_fallback"


def tags(text: str, folder: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    match = TAG_RE.search(text)
    if match:
        raw = match.group(1).strip().strip("[]")
        for value in re.split(r"[,;]", raw):
            value = value.strip().strip("'\"")
            if value:
                found.append({"tag": value, "provenance": "frontmatter"})
    for heading in re.findall(r"^#{1,3}\s+([^\n]+)", text, re.MULTILINE):
        clean = re.sub(r"[*_`]+", "", heading).strip()
        if clean and not any(item["tag"].casefold() == clean.casefold() for item in found):
            found.append({"tag": clean, "provenance": "explicit_heading"})
    if not found:
        found.append({"tag": folder, "provenance": "folder_derived"})
    return found


def build() -> dict:
    rows = []
    for path, kind in pages():
        text = path.read_text(encoding="utf-8")
        timestamp, provenance = git_timestamp(path)
        rel = path.relative_to(ROOT).as_posix()
        folder = path.parts[0]
        rows.append({
            "path": rel,
            "page_kind": kind,
            "room_domain": folder,
            "taxonomy_tags": tags(text, folder),
            "line_count": len(text.splitlines()),
            "last_modified": timestamp,
            "last_modified_provenance": provenance,
        })
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "selector": "numbered-folder top-level Markdown excluding *_Index.md plus numbered-folder/analysis/*.md",
        "page_count": len(rows),
        "pages": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write JSON to this path instead of stdout")
    args = parser.parse_args()
    payload = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
