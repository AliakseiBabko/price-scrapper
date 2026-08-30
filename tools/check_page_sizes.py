#!/usr/bin/env python3
"""Workstream D (PRICE_SCRAPPER_KNOWLEDGE_BASE_SCALABILITY): flag wiki pages
that have crossed this vault's layered-page-splitting threshold.

This is an advisory checker, not an automated editor. It approximates the
existing "judge by topic decomposition, not a hard line count" convention
(00_Master/wiki_page_format.md) with a two-tier heuristic:

  - Detail pages (under a numbered folder's analysis/): flag at 300 lines,
    or at 220 lines if the page has 3+ top-level (##) sections.
  - Guide pages (top-level file directly in a numbered folder, excluding
    *_Index.md): flag at 450 lines, or at 300 lines if the page has 3+
    top-level (##) sections.

"3+ top-level sections" is a proxy for "3+ independent topic/decision
clusters" - a heuristic, not a claim that heading count equals editorial
judgment. A flagged page still needs a human/agent decision on whether and
how to split it.

Positive page selector (matches Workstream C's definition so the two stay
consistent): only files directly under a numbered folder (NN_Name/) or
directly under NN_Name/analysis/ are considered. Everything else -
_Sources/**, _Knowledge/**, _Archive/**, _Inbox/**, source notes, case
studies, change logs - is out of scope for this checker.

Usage:
    python tools/check_page_sizes.py [--json] [--exceptions PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NUMBERED_FOLDER_RE = re.compile(r"^(?!00_)\d{2}_")  # excludes 00_Master (project docs, not wiki pages)

DETAIL_FLAG_LINES = 300
DETAIL_FLAG_LINES_CLUSTERED = 220
GUIDE_FLAG_LINES = 450
GUIDE_FLAG_LINES_CLUSTERED = 300
CLUSTER_THRESHOLD = 3

DEFAULT_EXCEPTIONS_PATH = REPO_ROOT / "tools" / "page_size_exceptions.json"


def discover_numbered_folders() -> list[Path]:
    return sorted(
        p for p in REPO_ROOT.iterdir()
        if p.is_dir() and NUMBERED_FOLDER_RE.match(p.name)
    )


def discover_pages() -> list[dict]:
    """Positive selector: Guide pages (top-level, not *_Index.md) and
    detail pages (directly under analysis/) in every numbered folder."""
    pages = []
    for folder in discover_numbered_folders():
        for f in sorted(folder.glob("*.md")):
            if f.name.endswith("_Index.md"):
                continue
            pages.append({"path": f, "kind": "guide"})
        analysis_dir = folder / "analysis"
        if analysis_dir.is_dir():
            for f in sorted(analysis_dir.glob("*.md")):
                pages.append({"path": f, "kind": "detail"})
    return pages


def count_top_level_sections(text: str) -> int:
    """Count level-2 (##) headings as a proxy for independent topic/decision
    clusters. Level-1 (#) is the page title, not a cluster boundary."""
    return len(re.findall(r"^## ", text, flags=re.MULTILINE))


def load_exceptions(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def check_page(entry: dict, exceptions: dict) -> dict | None:
    path = entry["path"]
    kind = entry["kind"]
    rel_path = path.relative_to(REPO_ROOT).as_posix()

    if rel_path in exceptions:
        return None

    with path.open("r", encoding="utf-8") as f:
        text = f.read()
    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    sections = count_top_level_sections(text)
    clustered = sections >= CLUSTER_THRESHOLD

    if kind == "detail":
        threshold = DETAIL_FLAG_LINES_CLUSTERED if clustered else DETAIL_FLAG_LINES
    else:
        threshold = GUIDE_FLAG_LINES_CLUSTERED if clustered else GUIDE_FLAG_LINES

    if line_count < threshold:
        return None

    return {
        "path": rel_path,
        "kind": kind,
        "line_count": line_count,
        "top_level_sections": sections,
        "clustered": clustered,
        "threshold_used": threshold,
        "reason": (
            f"{kind} page at {line_count} lines >= {threshold}-line threshold "
            f"({'clustered: ' + str(sections) + ' top-level sections' if clustered else 'base threshold, no cluster signal'})"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument(
        "--exceptions",
        type=Path,
        default=DEFAULT_EXCEPTIONS_PATH,
        help="path to a reviewed exceptions JSON file (path -> reason)",
    )
    args = parser.parse_args()

    exceptions = load_exceptions(args.exceptions)
    pages = discover_pages()
    flagged = [
        result
        for entry in pages
        if (result := check_page(entry, exceptions)) is not None
    ]

    if args.json:
        print(json.dumps(
            {
                "pages_scanned": len(pages),
                "exceptions_applied": len(exceptions),
                "flagged_count": len(flagged),
                "flagged": flagged,
            },
            indent=2,
            ensure_ascii=False,
        ))
    else:
        print(f"Scanned {len(pages)} pages ({len(exceptions)} exceptions on file).")
        if not flagged:
            print("No pages flagged.")
        else:
            print(f"{len(flagged)} page(s) flagged for possible layered-page splitting:\n")
            for r in flagged:
                print(f"  {r['path']}")
                print(f"    {r['reason']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
