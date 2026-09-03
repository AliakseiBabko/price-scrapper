#!/usr/bin/env python3
"""Guard this vault's wiki pages against growing out of control.

Two jobs, and the difference between them matters:

  1. A HARD CEILING of 300 lines. Introduced 2026-09-02 at the owner's
     instruction, after a vault-wide recalibration took twenty pages down
     under it. A page at or over the ceiling is a BREACH, not a suggestion,
     and this tool exits non-zero on one. The advisory exceptions file
     CANNOT waive it - that is the whole point of a ceiling.

  2. An advisory EARLY WARNING below the ceiling, so a page is caught while
     it is still growing rather than after it has broken the rule. Detail
     pages warn at 260 lines, or 220 with 12+ top-level (##) sections; guide
     pages at 280, or 240 clustered. Warnings are advisory, do not affect
     the exit code, and can be waived in the exceptions file.

  3. FRAGMENTED, the opposite failure: 12+ sections where at least half the
     headings name a processing batch ("added 2026-08-24, Round 3") rather
     than a topic, at under 17 lines each. The fix there is MERGING, not
     splitting - splitting a fragmented page makes it strictly worse.
     Advisory.

"12+ top-level sections" is a proxy for "many independent topic/decision
clusters" - a heuristic, not a claim that heading count equals editorial
judgment. A warned page still needs a human/agent decision on whether and
how to split it. A BREACHED page does not: it has to come down.

Why the old thresholds are gone. Until 2026-09-02 this file carried four
tiers - 400/260 detail, 500/350 guide - recalibrated upward on 2026-08-31
because the values before them flagged correctly-split result pages. Under a
300-line ceiling every one of those numbers is unreachable and therefore
dead code, so they were replaced by the warning band above, which sits
*below* the ceiling and is deliberately reachable. The 2026-08-31 lesson
still holds and is why warnings stay advisory: a warning says "this page is
approaching the ceiling", never "this page is wrong".

Positive page selector (matches Workstream C's definition so the two stay
consistent): only files directly under a numbered folder (NN_Name/) or
directly under NN_Name/analysis/ are considered. Everything else -
_Sources/**, _Knowledge/**, _Archive/**, _Inbox/**, source notes, case
studies, change logs - is out of scope for this checker.

Usage:
    python tools/check_page_sizes.py [--json] [--exceptions PATH] [--no-fail]

Exit codes: 0 = no ceiling breach (warnings may still be printed),
            2 = at least one page at or over the 300-line hard ceiling.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NUMBERED_FOLDER_RE = re.compile(r"^(?!00_)\d{2}_")  # excludes 00_Master (project docs, not wiki pages)

# The hard ceiling. Set 2026-09-02 by the vault owner: "keep them under three
# hundred". It is deliberately a single number for every page kind, because a
# ceiling that needs a lookup table is not a ceiling. The exceptions file does
# not apply to it.
HARD_CEILING_LINES = 300

# The advisory warning band, sitting below the ceiling so growth is caught on
# the way up. A source-attributed prose section in this vault runs 20-60 lines,
# so 260 gives a detail page roughly one more source before it breaches.
DETAIL_WARN_LINES = 260
DETAIL_WARN_LINES_CLUSTERED = 220
GUIDE_WARN_LINES = 280
GUIDE_WARN_LINES_CLUSTERED = 240
CLUSTER_THRESHOLD = 12

# The opposite failure: a page with many headings and very little under each is
# not too long, it is FRAGMENTED, and the fix is merging rather than splitting.
# Splitting it would make things actively worse.
#
# Detector rewritten 2026-09-02, second pass. The previous test - 20+ sections
# averaging under 12 lines - had two faults, both found by running it over the
# whole vault:
#
#   1. It almost never fired. Only two pages in 273 tripped it, and both only
#      after a split had removed the large sections that were masking their
#      average. Fragmentation that had been accumulating for weeks went unseen.
#   2. Average section length is the wrong primary signal, because it also
#      describes the target shape. A compact guide page - Kitchen_Furniture.md,
#      11 thematic sections in 80 lines - looks identical to a fragmented page
#      by that measure, and the old detector would have condemned exactly the
#      structure the convention asks for.
#
# What actually distinguishes them is WHAT THE HEADINGS SAY. A well-formed page
# has thematic headings. A fragmented page has ingestion-log headings: "...
# (Игорь Краснов, added 2026-09-01, Round 4)". The heading records when a fact
# arrived instead of what it is about, which is the defect itself, visible in
# the text rather than inferred from arithmetic.
#
# So the test is the PROPORTION of headings that are dated batch headings, with
# section count and average length as supporting conditions rather than the
# primary signal.
FRAGMENT_MIN_SECTIONS = 12
FRAGMENT_MIN_DATED_RATIO = 0.5
FRAGMENT_MAX_LINES_PER_SECTION = 17

# "added 2026-08-24", "Round 11", "(added ...)" - the fingerprints of a heading
# that names a batch rather than a topic.
DATED_HEADING_RE = re.compile(r"added 20\d\d-\d\d-\d\d|Round \d+|\(added|20\d\d-\d\d-\d\d\)")

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


def top_level_headings(text: str) -> list[str]:
    """Level-2 (##) headings. Level-1 (#) is the page title, not a cluster
    boundary."""
    return re.findall(r"^## .*$", text, flags=re.MULTILINE)


def count_top_level_sections(text: str) -> int:
    return len(top_level_headings(text))


def count_dated_headings(text: str) -> int:
    """Headings that name a processing batch ("added 2026-08-24, Round 3")
    rather than a topic. See the FRAGMENT_* constants for why this is the
    signal that matters."""
    return sum(1 for h in top_level_headings(text) if DATED_HEADING_RE.search(h))


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

    with path.open("r", encoding="utf-8") as f:
        text = f.read()
    line_count = text.count(chr(10)) + (0 if text.endswith(chr(10)) else 1)
    sections = count_top_level_sections(text)
    clustered = sections >= CLUSTER_THRESHOLD

    # The ceiling is checked BEFORE the exceptions file, on purpose. A reviewed
    # exception can say "this page does not need splitting yet"; it cannot say
    # "this page may exceed the ceiling".
    if line_count >= HARD_CEILING_LINES:
        return {
            "path": rel_path,
            "kind": kind,
            "severity": "BREACH",
            "line_count": line_count,
            "top_level_sections": sections,
            "clustered": clustered,
            "fragmented": False,
            "threshold_used": HARD_CEILING_LINES,
            "waivable": False,
            "reason": (
                f"CEILING BREACH: {line_count} lines, at or over the "
                f"{HARD_CEILING_LINES}-line hard ceiling. This is not advisory and "
                f"cannot be waived in the exceptions file. Split it with "
                f"`python tools/split_page.py analyse {rel_path}`, or - if the page "
                f"has many small dated sections - MERGE them first."
            ),
        }

    if rel_path in exceptions:
        return None

    if kind == "detail":
        threshold = DETAIL_WARN_LINES_CLUSTERED if clustered else DETAIL_WARN_LINES
    else:
        threshold = GUIDE_WARN_LINES_CLUSTERED if clustered else GUIDE_WARN_LINES

    per_section = line_count / sections if sections else line_count
    dated = count_dated_headings(text)
    dated_ratio = dated / sections if sections else 0.0
    fragmented = (
        sections >= FRAGMENT_MIN_SECTIONS
        and dated_ratio >= FRAGMENT_MIN_DATED_RATIO
        and per_section < FRAGMENT_MAX_LINES_PER_SECTION
    )

    if line_count < threshold and not fragmented:
        return None

    if fragmented:
        reason = (
            f"{kind} page is FRAGMENTED, not oversized: {dated} of its "
            f"{sections} top-level headings name a processing batch rather than "
            f"a topic ({dated_ratio:.0%}), at {per_section:.1f} lines each. The "
            f"content is organised by when it arrived, not by what it is about. "
            f"The fix is MERGING under thematic parents - "
            f"`python tools/split_page.py merge` demotes the dated headings to "
            f"### rather than deleting them, so attributions survive. Do NOT "
            f"split this page; splitting would make it worse."
        )
    else:
        reason = (
            f"approaching the {HARD_CEILING_LINES}-line ceiling: {kind} page at "
            f"{line_count} lines >= {threshold}-line warning threshold "
            f"({'clustered: ' + str(sections) + ' top-level sections' if clustered else 'base threshold, no cluster signal'}). "
            f"Advisory - plan the split now rather than after it breaches."
        )

    return {
        "path": rel_path,
        "kind": kind,
        "severity": "WARN",
        "line_count": line_count,
        "top_level_sections": sections,
        "clustered": clustered,
        "fragmented": fragmented,
        "dated_headings": dated,
        "dated_ratio": round(dated_ratio, 2),
        "threshold_used": threshold,
        "waivable": True,
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
    parser.add_argument(
        "--no-fail",
        action="store_true",
        help="report ceiling breaches but still exit 0 (for read-only inventory runs)",
    )
    args = parser.parse_args()

    exceptions = load_exceptions(args.exceptions)
    pages = discover_pages()
    flagged = [
        result
        for entry in pages
        if (result := check_page(entry, exceptions)) is not None
    ]

    breaches = [r for r in flagged if r["severity"] == "BREACH"]
    warnings = [r for r in flagged if r["severity"] == "WARN"]

    if args.json:
        print(json.dumps(
            {
                "pages_scanned": len(pages),
                "hard_ceiling_lines": HARD_CEILING_LINES,
                "exceptions_applied": len(exceptions),
                "breach_count": len(breaches),
                "warning_count": len(warnings),
                "flagged_count": len(flagged),
                "flagged": flagged,
            },
            indent=2,
            ensure_ascii=False,
        ))
    else:
        print(f"Scanned {len(pages)} pages against a {HARD_CEILING_LINES}-line hard ceiling "
              f"({len(exceptions)} advisory exceptions on file).")
        if breaches:
            print("")
            print(f"{len(breaches)} CEILING BREACH(ES) - these must be split:")
            print("")
            for r in breaches:
                print(f"  {r['path']}  ({r['line_count']} lines)")
                print(f"    {r['reason']}")
        if warnings:
            print("")
            print(f"{len(warnings)} advisory warning(s):")
            print("")
            for r in warnings:
                print(f"  {r['path']}")
                print(f"    {r['reason']}")
        if not flagged:
            print("No pages flagged.")
        elif not breaches:
            print(chr(10) + "No page is over the ceiling.")

    if breaches and not args.no_fail:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
