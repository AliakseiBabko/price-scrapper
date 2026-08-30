#!/usr/bin/env python3
"""Verify a batch of changes between two git refs before merging.

Automates the checks this project's review process runs by hand every
round: mojibake/corruption scan, BOM check, retired-pattern scan,
source-citation-ID drift detection (a dropped/retyped character in a
`yt_...`-style marker breaks traceability silently and none of the other
checks catch it), USD-cents detection, a rounding-bucket check on every
'≈$' figure (nearest 10/100/1,000 by magnitude - see
check_rounding_bucket's docstring), and a rate-vs-table plus arithmetic-
plausibility check on newly-added USD-equivalent annotations (the latter
is a heuristic limited to unambiguous single-value lines - see
check_arithmetic_plausibility's docstring for why).

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

# A USD figure with cents, e.g. "$494.6" or "$1,209.30" - per explicit user
# correction (2026-08-21), USD equivalents are a comparability aid for an
# approximate source figure, never a precise transaction record, so cents/
# decimal places should not appear at all.
# Two exclusions, both found by a real false-positive audit on 2026-08-30
# (the `_supporting` dissolution surfaced 58 usd_cents hits, 41 of them noise):
#   - a trailing k/K/m/M is thousands/millions shorthand, not cents. A case
#     study's "$3.5k" means $3,500; matching "$3.5" out of it and demanding it
#     be rounded to "$4" would corrupt the figure.
#   - a figure below $10 is exempt (see SMALL_FIGURE_FLOOR): at that magnitude
#     the decimal carries real information rather than false precision.
USD_CENTS_PATTERN = re.compile(r"\$[\d,]+\.\d+(?![\d]*[kKmM])")

# Below this, the no-cents and rounding-bucket rules stop making sense and
# start destroying data. The 2026-08-21 rounding correction's own rationale is
# that a USD equivalent is "a comparability aid for an approximate figure, not
# a transaction record" - but at single-dollar magnitudes the opposite holds:
# rounding "≈$1 for a 0.5m strip of sandpaper" to the nearest $10 yields $0,
# and "$0.46" per unit rounds to nothing at all. The same correction's explicit
# exception clause already covers these ("a figure that is itself genuinely
# exact ... stays precise"). Confirmed against real flagged lines on 2026-08-30.
SMALL_FIGURE_FLOOR = 10

# Matches this project's "USD equivalent" annotation convention, e.g.:
#   (÷ 83.21 RUB/USD, 2025 annual average, see [[...]])
RATE_ANNOTATION_PATTERN = re.compile(
    r"[÷/]\s*([\d.]+)\s*(RUB|BYN)/USD,?\s*(\d{4})\s*annual average"
)

# For the arithmetic-plausibility check: the last "$N" before a rate
# annotation, and the last "N RUB"/"N BYN" before that dollar figure.
# Captures an optional decimal part too (rather than trying to exclude it
# via lookahead, which can backtrack into a truncated match, e.g. matching
# "$458" out of "$4,589.7") - the decimal case is filtered out in code
# instead, where the full matched text is available to check cleanly.
DOLLAR_FIGURE_PATTERN = re.compile(r"\$([\d,]+(?:\.\d+)?)")
ORIGINAL_AMOUNT_PATTERN = re.compile(r"([\d,]+)\s*(RUB|BYN)\b")

# A converted-figure marker '≈$X' and, optionally, its range partner
# '-$Y' immediately after (e.g. "≈$18,900-$63,000"). Scoped tightly to the
# figure(s) actually attached to the '≈' marker, not just any '$' figure
# elsewhere on the same line - an early version scanned the whole line and
# produced a false positive on "...is ≈$30... below $1/month" (the $1 there
# is a genuinely-unrounded "less than $1" convention, unrelated to the ≈$30
# conversion earlier in the sentence).
APPROX_DOLLAR_PATTERN = re.compile(
    r"≈\$(\d{1,3}(?:,\d{3})*)(?:\.\d+)?"
    r"(?:\s*[-–—]\s*\$(\d{1,3}(?:,\d{3})*)(?:\.\d+)?)?"
)

# The rounding-bucket rule itself (per the 2026-08-21 rounding correction):
# a converted USD figure is a comparability aid, not a precise transaction
# record, so it must land on a "round" value at a precision matching its own
# magnitude - nearest 10 below $1,000, nearest 100 from $1,000-$99,999,
# nearest 1,000 above that.
def _rounding_unit(n: float) -> int:
    if n < 1000:
        return 10
    if n < 100_000:
        return 100
    return 1000

# Files whose dollar figures are arithmetic-exact by construction and are
# therefore exempt from the rounding-bucket and no-cents rules. This is not a
# convenience suppression - the 2026-08-21 rounding correction states the
# exception itself, and names one of these files as the example: "a figure ...
# recovered by an explicit arithmetic cross-check against other stated figures
# in the same source (e.g. the 7komnat.by case's $70,000/52m² totals) - those
# stay precise, since rounding them would discard real information rather than
# avoid manufacturing false precision." A case study's per-m² column is exactly
# that: $2,700 / 52 m² = $51.92/m². Added 2026-08-30 after the checker was
# found flagging 32 such figures.
EXACT_FIGURE_PATH_PREFIXES = (
    "11_Budget_and_Planning/case_studies/",
    "_Knowledge/store/USD_Backfill_Inventory.md",
)


def figures_are_exact_by_construction(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in EXACT_FIGURE_PATH_PREFIXES)


# Frozen content: archived raw evidence and superseded legacy pages. These are
# a historical record and must not be edited to satisfy a present-day style
# rule - rewriting a figure inside archived evidence would falsify the
# evidence. `tools/check_page_sizes.py` already excludes `_Archive/**` on the
# same reasoning. Added 2026-08-30, when 13 of 73 remaining money-check hits
# turned out to be in a superseded pre-reorg legacy guide.
FROZEN_PATH_PREFIXES = ("_Archive/",)


def path_is_frozen(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in FROZEN_PATH_PREFIXES)


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


def _plausibility_tolerance(raw_value: float) -> float:
    """How far a rounded USD figure may legitimately drift from the raw
    division, given this project's 'round to match source precision' policy
    (nearest 10 under $1,000, nearest 100 into the thousands, etc). Wide
    enough to accept correct aggressive rounding, narrow enough to catch a
    value copied from an unrelated line - tuned against every real rounding
    example verified this session (see git history for the worked cases)."""
    return max(3.0, 0.15 * raw_value)


def check_arithmetic_plausibility(path: str, base_text: str, head_text: str) -> list[str]:
    """For each newly-added rate annotation with exactly one whole-dollar
    figure and exactly one 'amount RUB/BYN' figure anywhere in the text
    before it, recompute amount/rate and flag if the stated result is
    implausibly far off - catches a value copy-pasted from a neighboring
    line's different rate (the recurring defect class found in
    PRICE_SCRAPPER_ATTRIBUTION_AND_CURRENCY_NORMALIZATION turns 100/102).

    Deliberately narrow: requires exactly one candidate of each kind, not
    just the closest one. A first version took the *last* candidate before
    the rate annotation regardless of how many others were also present,
    which mispaired ranges/multi-figure lines using this store's common
    "$X for the stated Y RUB range" phrasing (result stated before its RUB
    origin) - producing false positives on real, correct content. Requiring
    exact-one-each instead skips every multi-value line rather than risk
    guessing the wrong pairing; this is a heuristic supplement to, not a
    replacement for, manually re-deriving arithmetic against the actual
    source-of-truth table."""
    problems: list[str] = []
    base_lines = set(base_text.splitlines())
    head_lines = head_text.splitlines()
    added_lines = [line for line in head_lines if line not in base_lines]

    for line in added_lines:
        for match in RATE_ANNOTATION_PATTERN.finditer(line):
            stated_rate = float(match.group(1))
            prefix = line[: match.start()]

            # Only whole-dollar figures are eligible candidates - a decimal
            # one (still legal in pre-2026-08-21 content, or content this
            # tool's own usd_cents check will separately flag) isn't the
            # rounded result this check knows how to validate.
            dollar_matches = [
                m for m in DOLLAR_FIGURE_PATTERN.finditer(prefix) if "." not in m.group(1)
            ]
            if len(dollar_matches) != 1:
                continue
            dollar_match = dollar_matches[0]
            result = float(dollar_match.group(1).replace(",", ""))

            amount_matches = list(ORIGINAL_AMOUNT_PATTERN.finditer(prefix))
            if len(amount_matches) != 1:
                continue
            amount_match = amount_matches[0]
            amount = float(amount_match.group(1).replace(",", ""))

            if stated_rate == 0:
                continue
            raw = amount / stated_rate
            tolerance = _plausibility_tolerance(raw)
            if abs(raw - result) > tolerance:
                snippet = line.strip()[:80]
                problems.append(
                    f"USD figure ${result:,.0f} looks implausible for "
                    f"{amount_match.group(1)} {amount_match.group(2)} at rate {stated_rate} "
                    f"(raw {amount_match.group(1)}/{stated_rate}={raw:,.1f}, expected within "
                    f"~{tolerance:,.0f} of that) - possible copy from a different line/rate "
                    f"(line: {snippet}...)"
                )
    return problems


def check_rounding_bucket(path: str, base_text: str, head_text: str) -> list[str]:
    """For each newly-added '≈$X' (and its optional '-$Y' range partner),
    flag any whole-dollar figure that isn't a multiple of the rounding unit
    for its own magnitude - catches false precision like '≈$63' (should be
    $60) or '≈$53,000' (should be $53,200), the defect class found in
    PRICE_SCRAPPER_USD_BACKFILL_RESIDUAL round 7, which slipped past two
    prior review rounds because nobody hand-checked the rounding bucket on
    every figure, only whether the total looked plausible.

    Scoped tightly to the figure(s) actually attached to the '≈' marker
    this store uses exclusively for converted (not originally-USD)
    figures - see APPROX_DOLLAR_PATTERN's docstring for why a whole-line
    scan was rejected. Any decimal part is dropped before checking (a
    decimal '≈$' figure is separately flagged by check_usd_cents already,
    so this just evaluates the truncated integer)."""
    problems: list[str] = []
    if figures_are_exact_by_construction(path) or path_is_frozen(path):
        return problems
    base_lines = set(base_text.splitlines())
    head_lines = head_text.splitlines()
    added_lines = [line for line in head_lines if line not in base_lines]

    for line in added_lines:
        prose_line = INLINE_CODE_SPAN.sub("", line)
        for match in APPROX_DOLLAR_PATTERN.finditer(prose_line):
            for raw in match.groups():
                if raw is None:
                    continue
                n = float(raw.replace(",", ""))
                if n < SMALL_FIGURE_FLOOR:
                    # Rounding a single-dollar figure to the nearest $10 gives
                    # $0. See SMALL_FIGURE_FLOOR.
                    continue
                unit = _rounding_unit(n)
                if n % unit != 0:
                    snippet = line.strip()[:80]
                    problems.append(
                        f"USD figure ${raw} isn't a multiple of the expected rounding unit "
                        f"(${unit:,}) for its magnitude - false precision (line: {snippet}...)"
                    )
    return problems


def check_usd_cents(path: str, base_text: str, head_text: str) -> list[str]:
    """Find newly-added USD figures with cents/decimal places - per explicit
    user correction (2026-08-21), a USD equivalent is a rounded comparability
    aid, never a precise transaction record; cents should never appear."""
    problems: list[str] = []
    if figures_are_exact_by_construction(path) or path_is_frozen(path):
        return problems
    base_lines = set(base_text.splitlines())
    head_lines = head_text.splitlines()
    added_lines = [line for line in head_lines if line not in base_lines]

    for line in added_lines:
        # Strip inline `code spans` before matching - documentation that
        # quotes a bad-example figure (e.g. "not `$47.2/m2`") isn't a live
        # violation, same reasoning as the retired-pattern check above.
        prose_line = INLINE_CODE_SPAN.sub("", line)
        hits = [
            hit for hit in USD_CENTS_PATTERN.findall(prose_line)
            if float(hit.lstrip("$").replace(",", "")) >= SMALL_FIGURE_FLOOR
        ]
        if hits:
            snippet = line.strip()[:80]
            problems.append(
                f"USD figure(s) with cents/decimals found ({', '.join(sorted(set(hits)))}) - "
                f"round to a whole dollar (and further, to match the source's own precision, "
                f"per the 2026-08-21 rounding correction) (line: {snippet}...)"
            )
    return problems


def repo_wide_id_hits(id_value: str, exclude_path: str, ref: str | None) -> int:
    """Count files (other than exclude_path) containing id_value.

    Searches `ref` when given (a commit/branch the working tree may not
    have checked out - e.g. `--head origin/topic/...` while sitting on
    `main`); falls back to the working tree when `ref` is None (the
    --head-omitted / uncommitted-changes case `git grep` naturally
    handles). Found via a real false positive: running this against
    `origin/topic/...` while `main` was checked out searched the wrong
    tree entirely and flagged 3 genuinely-fine IDs as unverifiable
    (PRICE_SCRAPPER_USD_BACKFILL_RESIDUAL round 8)."""
    # Search the bare core ID, not just the prefixed "yt_<id>" form. The same
    # source is written several ways across the vault - "yt_<id>" in store
    # prose, "YT_<id>_<slug>.md" as the source-note filename, "watch?v=<id>" in
    # processed_sources.csv, and a bare "<id>" line in processed_video_ids.txt.
    # Matching only the prefixed form reported every ID in a batch as
    # unverifiable: 156 of them on 2026-08-30, all of which existed. Falling
    # back to the core ID makes the check answer the question it is actually
    # asking - "does this source exist anywhere else?" - rather than "is it
    # spelled this one way elsewhere?".
    candidates = [id_value]
    core = id_value.split("_", 1)[1] if "_" in id_value else id_value
    if core and core != id_value:
        candidates.append(core)

    hits: set[str] = set()
    for candidate in candidates:
        cmd = ["git", "grep", "-l", "-F", candidate]
        if ref is not None:
            cmd.append(ref)
        result = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode not in (0, 1):
            return -1
        lines = result.stdout.splitlines()
        if ref is not None:
            # "git grep -l <ref> -- ..." prefixes each hit with "<ref>:<path>".
            prefix = f"{ref}:"
            lines = [line[len(prefix):] if line.startswith(prefix) else line for line in lines]
        hits.update(line for line in lines if line.strip() != exclude_path)
    return len(hits)


def main() -> int:
    # Some Windows consoles default stdout to a restricted codepage (cp1252)
    # that can't encode currency/comparison symbols (≈, –, ÷) this tool's own
    # messages may contain - reconfigure to UTF-8 with a safe fallback rather
    # than crash with an unhandled UnicodeEncodeError mid-run.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

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
                hits = repo_wide_id_hits(aid, path, args.head)
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
            for msg in check_arithmetic_plausibility(path, base_text, head_text):
                problems.append({"file": path, "check": "arithmetic_implausible", "message": msg})

        if not is_self_or_excluded:
            for msg in check_usd_cents(path, base_text, head_text):
                problems.append({"file": path, "check": "usd_cents", "message": msg})
            for msg in check_rounding_bucket(path, base_text, head_text):
                problems.append({"file": path, "check": "rounding_bucket", "message": msg})

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
                "Rate-vs-table, cents, and rounding-bucket checks are exact. The arithmetic-"
                "plausibility check is a heuristic that only fires on single-value, unambiguous "
                "lines (skips ranges/multi-figure lines rather than risk a wrong pairing) - it "
                "does not replace manually re-deriving arithmetic against the actual source-of-"
                "truth table, only supplements it. Plus mojibake/BOM/retired-pattern/citation-"
                "ID-drift checks."
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

    print("\nPASS - no mojibake, no BOM, no retired patterns, no ID drift, no wrong-year rate")
    print("annotations, no cents/decimals, and no implausible single-value arithmetic found.")
    print("Note: the arithmetic-plausibility check is a heuristic limited to unambiguous")
    print("single-value lines (it skips ranges/multi-figure lines rather than risk a wrong")
    print("pairing) - re-derive arithmetic by hand for anything it doesn't cover.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
