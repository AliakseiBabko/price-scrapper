#!/usr/bin/env python3
"""Workstream D (PRICE_SCRAPPER_KNOWLEDGE_BASE_SCALABILITY): flag wiki pages
that have crossed this vault's layered-page-splitting threshold.

This is an advisory checker, not an automated editor. It approximates the
existing "judge by topic decomposition, not a hard line count" convention
(00_Master/wiki_page_format.md) with a two-tier heuristic:

  - Detail pages (under a numbered folder's analysis/): flag at 400 lines,
    or at 260 lines if the page has 12+ top-level (##) sections.
  - Guide pages (top-level file directly in a numbered folder, excluding
    *_Index.md): flag at 500 lines, or at 350 lines if the page has 12+
    top-level (##) sections.
  - Any page: flag as FRAGMENTED at 20+ sections averaging under 12 lines
    each - the opposite problem, where the fix is merging, not splitting.

"12+ top-level sections" is a proxy for "many independent topic/decision
clusters" - a heuristic, not a claim that heading count equals editorial
judgment. A flagged page still needs a human/agent decision on whether and
how to split it.

Thresholds were recalibrated on 2026-08-31 after three real splits showed the
original values flagged the correctly-split result pages too; see the comment
block above the constants for the evidence.

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

# Recalibrated 2026-08-31, on evidence rather than taste. The previous values
# (300/220 detail, 450/300 guide, cluster at 3 sections) were tested for the
# first time by actually performing three splits - Walls_and_Paint 921 lines
# into four pages, Flooring_Guide 865 into three, Waterproofing_and_Plastering
# 815 into four - and they FAILED the test: the flagged count went UP, from 31
# to 35, because seven correctly-sized, single-topic result pages (234-336
# lines) tripped the threshold that their 900-line parent had tripped.
#
# A rule that punishes a correct split is worse than no rule: it tells an
# author their finished work is still wrong, with no achievable target short of
# atomising every page into stubs.
#
# Two changes, both aimed at making the flag mean "too many independent topics"
# rather than "long":
#   - The cluster signal now needs 12+ sections, not 3+. At 3 the clustered
#     threshold applied to essentially every page, so the tool was really a
#     flat 220-line limit wearing a heuristic's clothes; almost no real detail
#     page has fewer than three headings.
#   - Line thresholds raised to match observed reality. A source-attributed
#     prose section in this vault runs 20-60 lines, so 220 lines capped a
#     detail page at roughly five sources before it was declared too long.
DETAIL_FLAG_LINES = 400
DETAIL_FLAG_LINES_CLUSTERED = 260
GUIDE_FLAG_LINES = 500
GUIDE_FLAG_LINES_CLUSTERED = 350
CLUSTER_THRESHOLD = 12

# The opposite failure, which the size checker was structurally blind to: a
# page with many headings and very little under each is not too long, it is
# FRAGMENTED, and the fix is merging rather than splitting. Splitting it would
# make things actively worse. Found on the same 2026-08-31 pass -
# `Lighting_Design.md` had 26 top-level sections in 242 lines, 9 lines each,
# because every batch appended its own dated heading instead of adding to an
# existing one. It had been flagged for splitting for weeks.
FRAGMENT_MIN_SECTIONS = 20
FRAGMENT_MAX_LINES_PER_SECTION = 12

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

    per_section = line_count / sections if sections else line_count
    fragmented = (
        sections >= FRAGMENT_MIN_SECTIONS
        and per_section < FRAGMENT_MAX_LINES_PER_SECTION
    )

    if line_count < threshold and not fragmented:
        return None

    if fragmented:
        reason = (
            f"{kind} page is FRAGMENTED, not oversized: {sections} top-level "
            f"sections across only {line_count} lines ({per_section:.1f} lines "
            f"each). The fix is MERGING related sections, not splitting - "
            f"splitting this would make it worse. Usually caused by each batch "
            f"appending its own dated heading instead of adding to an existing "
            f"section."
        )
    else:
        reason = (
            f"{kind} page at {line_count} lines >= {threshold}-line threshold "
            f"({'clustered: ' + str(sections) + ' top-level sections' if clustered else 'base threshold, no cluster signal'})"
        )

    return {
        "path": rel_path,
        "kind": kind,
        "line_count": line_count,
        "top_level_sections": sections,
        "clustered": clustered,
        "fragmented": fragmented,
        "threshold_used": threshold,
        "reason": reason,
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
