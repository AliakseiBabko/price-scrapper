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
    args = parser.parse_args()

    retired_patterns = DEFAULT_RETIRED_PATTERNS + args.retired_pattern
    files = changed_files(args.base, args.head)

    if not files:
        print("No changed files between the given refs.")
        return 0

    print(f"Checking {len(files)} changed file(s): base={args.base} head={args.head or '(working tree)'}\n")

    problems: list[str] = []

    for path in files:
        head_bytes = file_bytes_at(args.head, path)
        if head_bytes is None:
            # Deleted file — nothing to scan for corruption, but still check ID drift below.
            head_text = ""
        else:
            try:
                head_text = head_bytes.decode("utf-8")
            except UnicodeDecodeError:
                problems.append(f"[{path}] not valid UTF-8 in head state")
                continue
            if head_bytes[:3] == b"\xef\xbb\xbf":
                problems.append(f"[{path}] has a UTF-8 BOM")

        for sig in MOJIBAKE_SIGNATURES:
            if sig in head_text:
                count = head_text.count(sig)
                problems.append(f"[{path}] possible mojibake: '{sig}' x{count}")

        for pattern in retired_patterns:
            if re.search(pattern, head_text):
                problems.append(f"[{path}] retired pattern still present: /{pattern}/")

        base_bytes = file_bytes_at(args.base, path)
        base_text = base_bytes.decode("utf-8", errors="replace") if base_bytes else ""
        base_ids = extract_ids(base_text, args.id_pattern)
        head_ids = extract_ids(head_text, args.id_pattern)
        removed_ids = base_ids - head_ids
        added_ids = head_ids - base_ids

        for rid in sorted(removed_ids):
            problems.append(
                f"[{path}] ID present before but missing now: '{rid}' "
                f"(if this file's claim about that source was deleted intentionally, ignore; "
                f"otherwise this may be a truncated/retyped ID)"
            )

        if not args.skip_repo_wide_id_check:
            for aid in sorted(added_ids):
                hits = repo_wide_id_hits(aid, path)
                if hits == 0:
                    problems.append(
                        f"[{path}] newly-added ID '{aid}' does not appear anywhere else in the "
                        f"repository - verify it's a real ID, not a typo"
                    )

    print(f"Files checked: {len(files)}")
    print(f"Problems found: {len(problems)}")
    if problems:
        print()
        for p in problems:
            print(f"  - {p}")
        print("\nFAIL")
        return 1

    print("\nPASS - no mojibake, no BOM, no retired patterns, no ID drift detected.")
    print("Note: this does not check arithmetic correctness or content meaning - re-derive")
    print("numeric claims against the actual source-of-truth file separately.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
