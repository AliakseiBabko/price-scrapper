#!/usr/bin/env python3
"""Verify a batch of changes between two git refs before merging.

Automates the checks this project's review process runs by hand every
round: mojibake/corruption scan, BOM check, retired-pattern scan, and
source-citation-ID drift detection (a dropped/retyped character in a
`yt_...`-style marker breaks traceability silently and none of the other
checks catch it).

Usage:
    python tools/verify_batch.py --base <ref> [--head <ref>]
    python tools/verify_batch.py --base main --head HEAD
    python tools/verify_batch.py --base a8b7b6b

`--head` defaults to the current working tree (uncommitted changes included).
`--base` defaults to `origin/main` if not given.

Exit code is non-zero if any check fails.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Byte-sequence signatures seen in this project's actual UTF-8-as-cp1252
# mojibake incidents. Not exhaustive, but these are the ones that recurred.
MOJIBAKE_SIGNATURES = ["Ð", "Ã°", "ï»¿", "Ã¢"]

DEFAULT_RETIRED_PATTERNS = [
    r"attribution:\s*unconfirmed",
]

DEFAULT_ID_PATTERN = r"yt_[A-Za-z0-9_-]+"

# This tool's own path, relative to repo root - excluded from the mojibake
# and retired-pattern scans below, since it legitimately defines those
# strings as data (signature literals, default regex patterns) rather than
# containing them as violations. Found via real self-scan false positives
# (Codex, PRICE_SCRAPPER_ATTRIBUTION_AND_CURRENCY_NORMALIZATION turn 74).
SELF_PATH = "tools/verify_batch.py"

INLINE_CODE_SPAN = re.compile(r"`[^`\n]*`")

# Matches this project's "USD equivalent" annotation convention, e.g.:
#   (÷ 83.21 RUB/USD, 2025 annual average, see [[...]])
RATE_ANNOTATION_PATTERN = re.compile(
    r"[÷/]\s*([\d.]+)\s*(RUB|BYN)/USD,?\s*(\d{4})\s*annual average"
)

EXCHANGE_RATE_TABLE_PATH = "00_Master/exchange_rates_reference.md"
EXCHANGE_RATE_ROW_PATTERN = re.compile(
    r"\|\s*\*\*(\d{4})\*\*\s*\|\s*USD/(RUB|BYN)\s*\|\s*([\d.]+)\s*\w+ per USD\s*\|"
    r".*?\|\s*(confirmed|unverified[^|]*)\s*\|"
)


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def changed_files(base: str, head: str | None) -> list[str]:
    if head is None:
        out = run_git(["diff", "--name-only", base])
    else:
        out = run_git(["diff", "--name-only", base, head])
    return [line.strip() for line in out.splitlines() if line.strip()]


def file_bytes_at(ref: str | None, path: str) -> bytes | None:
    """None means the file didn't exist at that ref, or ref is None (working tree)."""
    if ref is None:
        full = REPO_ROOT / path
        if not full.exists():
            return None
        return full.read_bytes()
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=REPO_ROOT, capture_output=True
    )
    if result.returncode != 0:
        return None
    return result.stdout


def extract_ids(text: str, id_pattern: str) -> set[str]:
    return set(re.findall(id_pattern, text))


def load_confirmed_rates(ref: str | None) -> dict[tuple[str, int], float]:
    """Parse 00_Master/exchange_rates_reference.md at the given ref (None = working tree)
    and return {(currency, year): confirmed_rate} for rows marked 'confirmed'."""
    content_bytes = file_bytes_at(ref, EXCHANGE_RATE_TABLE_PATH)
    if content_bytes is None:
        return {}
    text = content_bytes.decode("utf-8", errors="replace")
    rates: dict[tuple[str, int], float] = {}
    for line in text.splitlines():
        m = EXCHANGE_RATE_ROW_PATTERN.search(line)
        if not m:
            continue
        year, currency, rate, confidence = m.groups()
        if confidence.strip() != "confirmed":
            continue
        rates[(currency, int(year))] = float(rate)
    return rates


def check_rate_annotations(path: str, base_text: str, head_text: str, confirmed_rates: dict) -> list[str]:
    """Find newly-added 'USD equivalent' annotations and verify the stated rate
    matches the actual confirmed rate for that currency/year in the reference
    table — catches the 'wrong-year rate' defect class (a real rate value that
    is simply attributed to the wrong year)."""
    problems: list[str] = []
    base_lines = set(base_text.splitlines())
    head_lines = head_text.splitlines()
    added_lines = [line for line in head_lines if line not in base_lines]

    for line in added_lines:
        for stated_rate, currency, year in RATE_ANNOTATION_PATTERN.findall(line):
            key = (currency, int(year))
            actual = confirmed_rates.get(key)
            snippet = line.strip()[:80]
            if actual is None:
                problems.append(
                    f"annotation cites {currency}/{year} as '{stated_rate}' but that "
                    f"year/currency is not a 'confirmed' row in {EXCHANGE_RATE_TABLE_PATH} "
                    f"(line: {snippet}...)"
                )
                continue
            if abs(float(stated_rate) - actual) > 0.01:
                problems.append(
                    f"annotation states {stated_rate} {currency}/USD for {year}, but "
                    f"the confirmed table rate for {currency}/{year} is {actual} - wrong-year or "
                    f"mistyped rate (line: {snippet}...)"
                )
    return problems


def repo_wide_id_hits(id_value: str, exclude_path: str) -> int:
    result = subprocess.run(
        ["git", "grep", "-l", "-F", id_value],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode not in (0, 1):
        return -1
    hits = [line for line in result.stdout.splitlines() if line.strip() != exclude_path]
    return len(hits)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", required=True, help="Base git ref (the known-good state)")
    parser.add_argument("--head", default=None, help="Head git ref; omit to use the working tree")
    parser.add_argument(
        "--retired-pattern",
        action="append",
        default=[],
        help="Additional retired-pattern regex to scan for (repeatable). Defaults include 'attribution: unconfirmed'.",
    )
    parser.add_argument(
        "--id-pattern",
        default=DEFAULT_ID_PATTERN,
        help=f"Regex for citation/source IDs to track drift on (default: {DEFAULT_ID_PATTERN!r})",
    )
    parser.add_argument(
        "--skip-repo-wide-id-check",
        action="store_true",
        help="Skip the repo-wide existence check for newly-added IDs (faster, less thorough).",
    )
    parser.add_argument(
        "--exclude-path",
        action="append",
        default=[],
        help=(
            "Repo-relative path to skip for mojibake/retired-pattern checks (repeatable). "
            f"'{SELF_PATH}' is always excluded automatically since it legitimately contains "
            "those signatures/patterns as literal data, not violations."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Emit a single machine-readable JSON object to stdout instead of prose - "
            "for feeding management_dialogue.py's --validation field directly, per the "
            "'automated verification harness output' suggestion from this project's own "
            "multi-agent retrospective."
        ),
    )
    args = parser.parse_args()

    retired_patterns = DEFAULT_RETIRED_PATTERNS + args.retired_pattern
    files = changed_files(args.base, args.head)

    if not files:
        if args.json:
            print(json.dumps({
                "base": args.base, "head": args.head, "files_checked": 0,
                "problems": [], "passed": True,
            }))
        else:
            print("No changed files between the given refs.")
        return 0

    if not args.json:
        print(f"Checking {len(files)} changed file(s): base={args.base} head={args.head or '(working tree)'}\n")

    problems: list[str] = []
    confirmed_rates = load_confirmed_rates(args.head)

    for path in files:
        head_bytes = file_bytes_at(args.head, path)
        if head_bytes is None:
            # Deleted file — nothing to scan for corruption, but still check ID drift below.
            head_text = ""
        else:
            try:
                head_text = head_bytes.decode("utf-8")
            except UnicodeDecodeError:
                problems.append({"file": path, "check": "utf8", "message": "not valid UTF-8 in head state"})
                continue
            if head_bytes[:3] == b"\xef\xbb\xbf":
                problems.append({"file": path, "check": "bom", "message": "has a UTF-8 BOM"})

        is_self_or_excluded = path == SELF_PATH or path in args.exclude_path

        if not is_self_or_excluded:
            for sig in MOJIBAKE_SIGNATURES:
                if sig in head_text:
                    count = head_text.count(sig)
                    problems.append({
                        "file": path, "check": "mojibake",
                        "message": f"possible mojibake: '{sig}' x{count}",
                    })

        # Strip inline `code spans` before the retired-pattern scan - a
        # documentation file legitimately quoting the retired pattern as an
        # example (e.g. "do not write `attribution: unconfirmed`") is not a
        # violation of the policy it's explaining.
        prose_text = INLINE_CODE_SPAN.sub("", head_text)
        if not is_self_or_excluded:
            for pattern in retired_patterns:
                if re.search(pattern, prose_text):
                    problems.append({
                        "file": path, "check": "retired_pattern",
                        "message": f"retired pattern still present outside inline code spans: /{pattern}/",
                    })

        base_bytes = file_bytes_at(args.base, path)
        base_text = base_bytes.decode("utf-8", errors="replace") if base_bytes else ""
        base_ids = extract_ids(base_text, args.id_pattern)
        head_ids = extract_ids(head_text, args.id_pattern)
        removed_ids = base_ids - head_ids
        added_ids = head_ids - base_ids

        for rid in sorted(removed_ids):
            problems.append({
                "file": path, "check": "id_drift", "id": rid,
                "message": (
                    f"ID present before but missing now: '{rid}' "
                    f"(if this file's claim about that source was deleted intentionally, ignore; "
                    f"otherwise this may be a truncated/retyped ID)"
                ),
            })

        if not args.skip_repo_wide_id_check:
            for aid in sorted(added_ids):
                hits = repo_wide_id_hits(aid, path)
                if hits == 0:
                    problems.append({
                        "file": path, "check": "id_unverifiable", "id": aid,
                        "message": (
                            f"newly-added ID '{aid}' does not appear anywhere else in the "
                            f"repository - verify it's a real ID, not a typo"
                        ),
                    })

        if path != EXCHANGE_RATE_TABLE_PATH:
            for msg in check_rate_annotations(path, base_text, head_text, confirmed_rates):
                problems.append({"file": path, "check": "rate_year_mismatch", "message": msg})

    passed = len(problems) == 0

    if args.json:
        print(json.dumps({
            "base": args.base,
            "head": args.head,
            "files_checked": len(files),
            "files": files,
            "problems": problems,
            "passed": passed,
            "note": (
                "Does not verify underlying original-amount arithmetic - only that a cited "
                "rate matches the confirmed table rate for its stated year/currency, plus "
                "mojibake/BOM/retired-pattern/citation-ID-drift checks."
            ),
        }, indent=2))
        return 0 if passed else 1

    print(f"Files checked: {len(files)}")
    print(f"Problems found: {len(problems)}")
    if problems:
        print()
        for p in problems:
            print(f"  - [{p['file']}] {p['message']}")
        print("\nFAIL")
        return 1

    print("\nPASS - no mojibake, no BOM, no retired patterns, no ID drift, no wrong-year")
    print("rate annotations detected.")
    print("Note: this does not verify the underlying original-amount arithmetic (e.g. that")
    print("15000/83.21 was computed correctly) - only that a cited rate matches the actual")
    print("confirmed table rate for its stated year/currency. Re-derive the full arithmetic")
    print("by hand for anything not covered by an automated check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
