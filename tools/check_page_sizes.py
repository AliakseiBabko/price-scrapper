#!/usr/bin/env python3
"""Guard this vault's wiki pages against growing out of control.

The rule this enforces is **approximate size plus structural integrity**, not a
line count. A page of 310 lines whose structure is logical and whose sections
belong together is fine. A page of 260 lines that is really twenty dated
fragments is not. The checker is built around that ordering.

Three signals, in descending order of how much they should worry you:

  1. FRAGMENTED - the integrity failure, and the one that actually matters.
     12+ sections where at least half the headings name a processing batch
     ("added 2026-08-24, Round 3") rather than a topic, at under 17 lines
     each. The page is organised by when facts arrived, not by what they are
     about. The fix is MERGING, never splitting. Advisory, because the fix
     needs judgment about which sections belong together.

  2. OVER BACKSTOP - 400+ lines. Not a style opinion: at this length a page
     has almost certainly stopped being one topic, and every page this vault
     has ever found at this size was in fact several. This is the only
     condition that exits non-zero, and a reviewed exception CAN waive it if
     the structure genuinely justifies the length.

  3. OVER SOFT TARGET - past ~300 lines. Purely informational. **Being over
     the soft target is not a defect.** It is a prompt to look at the page and
     ask whether it still holds one coherent subject. If it does, leave it.

Why it is shaped this way. The 300 figure was briefly a hard gate (2026-09-02,
first pass) and that was wrong: it made "310 lines and perfectly coherent" fail
in the same way "878 lines of twenty batches" failed, which tells an author
nothing useful and pushes toward splitting pages that should not be split. The
owner corrected it the same day. The number was never the point; the point is
that nobody notices a page growing until someone looks.

So: the soft target makes you look, the integrity test says whether anything is
actually wrong, and the backstop catches the runaway case that motivated all of
this - pages found at 878, 740 and 696 lines, none of which got there by a
decision.

Positive page selector (matches Workstream C's definition so the two stay
consistent): only files directly under a numbered folder (NN_Name/) or
directly under NN_Name/analysis/ are considered. Everything else -
_Sources/**, _Knowledge/**, _Archive/**, _Inbox/**, source notes, case
studies, change logs - is out of scope for this checker.

Usage:
    python tools/check_page_sizes.py [--json] [--exceptions PATH] [--no-fail]

Exit codes: 0 = nothing over the backstop (notes and warnings may still print),
            2 = at least one page at or over the 400-line backstop.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NUMBERED_FOLDER_RE = re.compile(r"^(?!00_)\d{2}_")  # excludes 00_Master (project docs, not wiki pages)

# The soft target. Crossing it is INFORMATIONAL - it means "go and look at this
# page", not "this page is wrong". Set by the vault owner 2026-09-02: pages
# should be roughly this size, and "if its structure is logical and requires,
# for example, 310 lines, that's okay - not a problem."
SOFT_TARGET_LINES = 300

# The backstop. This one fails the build. It is set far enough above the soft
# target that reaching it is evidence of a real problem rather than of a page
# being slightly long: every page this vault has found at 400+ lines turned out
# to be several topics sharing a file. Unlike the short-lived hard ceiling it
# replaces, a reviewed exception CAN waive it - see page_size_exceptions.json.
BACKSTOP_LINES = 400

# Advisory band for pages growing toward the soft target, so growth is visible
# early. A source-attributed prose section in this vault runs 20-60 lines.
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

    # The backstop is checked first, but unlike the hard ceiling it replaces it
    # is waivable: the exceptions-file lookup below still applies to it.
    if line_count >= BACKSTOP_LINES and rel_path not in exceptions:
        return {
            "path": rel_path,
            "kind": kind,
            "severity": "BACKSTOP",
            "line_count": line_count,
            "top_level_sections": sections,
            "clustered": clustered,
            "fragmented": False,
            "threshold_used": BACKSTOP_LINES,
            "waivable": True,
            "reason": (
                f"OVER BACKSTOP: {line_count} lines, at or over {BACKSTOP_LINES}. "
                f"At this length a page has almost certainly stopped being one "
                f"topic. Run `python tools/split_page.py analyse {rel_path}` - if "
                f"it reports FRAGMENTED, MERGE first, then extract. If the "
                f"structure genuinely justifies the length, add a reviewed entry "
                f"to tools/page_size_exceptions.json saying why."
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
        if line_count >= SOFT_TARGET_LINES:
            return {
                "path": rel_path,
                "kind": kind,
                "severity": "NOTE",
                "line_count": line_count,
                "top_level_sections": sections,
                "clustered": clustered,
                "fragmented": False,
                "dated_headings": count_dated_headings(text),
                "threshold_used": SOFT_TARGET_LINES,
                "waivable": True,
                "reason": (
                    f"over the ~{SOFT_TARGET_LINES}-line soft target at {line_count} "
                    f"lines, across {sections} topic-shaped sections. **This is not a "
                    f"defect.** Worth a look to confirm the page still holds one "
                    f"coherent subject; if it does, leave it alone."
                ),
            }
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
            f"approaching the ~{SOFT_TARGET_LINES}-line soft target: {kind} page at "
            f"{line_count} lines >= {threshold}-line warning threshold "
            f"({'clustered: ' + str(sections) + ' top-level sections' if clustered else 'base threshold, no cluster signal'}). "
            f"Advisory - a good moment to check the page still holds one subject."
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
        help="report backstop hits but still exit 0 (for read-only inventory runs)",
    )
    args = parser.parse_args()

    exceptions = load_exceptions(args.exceptions)
    pages = discover_pages()
    flagged = [
        result
        for entry in pages
        if (result := check_page(entry, exceptions)) is not None
    ]

    over = [r for r in flagged if r["severity"] == "BACKSTOP"]
    warnings = [r for r in flagged if r["severity"] == "WARN"]
    notes = [r for r in flagged if r["severity"] == "NOTE"]
    fragmented = [r for r in warnings if r.get("fragmented")]

    if args.json:
        print(json.dumps(
            {
                "pages_scanned": len(pages),
                "soft_target_lines": SOFT_TARGET_LINES,
                "backstop_lines": BACKSTOP_LINES,
                "exceptions_applied": len(exceptions),
                "over_backstop_count": len(over),
                "fragmented_count": len(fragmented),
                "warning_count": len(warnings),
                "note_count": len(notes),
                "flagged": flagged,
            },
            indent=2,
            ensure_ascii=False,
        ))
    else:
        print(f"Scanned {len(pages)} pages: soft target ~{SOFT_TARGET_LINES} lines, "
              f"backstop {BACKSTOP_LINES} ({len(exceptions)} reviewed exceptions).")
        if over:
            print("")
            print(f"{len(over)} page(s) OVER THE BACKSTOP:")
            print("")
            for r in over:
                print(f"  {r['path']}  ({r['line_count']} lines)")
                print(f"    {r['reason']}")
        if fragmented:
            print("")
            print(f"{len(fragmented)} FRAGMENTED page(s) - merge, do not split:")
            print("")
            for r in fragmented:
                print(f"  {r['path']}")
                print(f"    {r['reason']}")
        other = [r for r in warnings if not r.get("fragmented")]
        if other:
            print("")
            print(f"{len(other)} page(s) growing toward the soft target:")
            print("")
            for r in other:
                print(f"  {r['path']}  ({r['line_count']} lines)")
        if notes:
            print("")
            print(f"{len(notes)} page(s) over the ~{SOFT_TARGET_LINES}-line soft target "
                  f"- informational, not defects:")
            print("")
            for r in notes:
                print(f"  {r['path']}  ({r['line_count']} lines, "
                      f"{r['top_level_sections']} sections)")
        if not flagged:
            print("Nothing flagged.")
        elif not over:
            print("")
            print("Nothing over the backstop.")

    if over and not args.no_fail:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
