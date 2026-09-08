"""Validate the bill of materials and the quotes recorded against it.

Deliberately in the same shape as this repo's other gates (`validate_canonical.py`,
`check_room_rollout.py`): it refuses to guess, reports the source of every
judgement, and exits non-zero on a real defect rather than warning into a log.

What it does NOT do: invent quantities. A BOM line whose `qty` is empty and whose
`qty_source` is `unmeasured` is CORRECT at this stage of the project - rate discovery
does not wait for quantities, and the standing rule that areas are not evidence
forbids deriving them from the developer's area figures. Those lines are reported as
a working view, not as errors.

Usage:
    python tools/procurement/validate_bom.py
    python tools/procurement/validate_bom.py --as-of 2026-10-01   # test quote expiry
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOM = ROOT / "data" / "procurement" / "bom.csv"
QUOTES = ROOT / "data" / "procurement" / "quotes.csv"

TRADES = {
    "DEM": "demolition",
    "MAS": "masonry",
    "PLA": "plastering",
    "SCR": "screed and levelling",
    "WAT": "waterproofing",
    "TIL": "tiling",
    "PLU": "plumbing",
    "ELE": "electrical",
    "VEN": "ventilation",
    "PNT": "painting and decorating",
    "DOR": "doors and trim",
    "FUR": "furniture and fit-out",
    "IFC": "trade interface - NOT a purchase",
}
QTY_SOURCES = {"model_measured", "datasheet_derived", "manual", "unmeasured"}
STAGES = {"1", "2", "3", "4", "5"}
QUOTE_STATUS = {"received", "shortlisted", "rejected", "accepted", "expired"}
KEY_RE = re.compile(r"^[A-Z]{3}-\d{2}:[A-Za-z0-9_]+:[a-z0-9_]+$")
# `nested` waste is only justified where the research supports it: large-format
# tile and sheet goods. Anywhere else it is over-engineering.
NESTED_OK_TRADES = {"TIL", "FUR"}


def ensure_utf8_stdout() -> None:
    """Windows consoles default to cp1252; a gate must not die on its own output."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover - older interpreters or odd streams
        pass


def load(path: Path) -> list[dict]:
    if not path.exists():
        sys.exit(f"FAIL missing file: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_date(value: str, where: str, problems: list[str]) -> dt.date | None:
    if not value:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        problems.append(f"{where}: date is not ISO yyyy-mm-dd: {value!r}")
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=dt.date.today().isoformat())
    parser.add_argument("--bom", type=Path, default=BOM, help="override, for self-testing")
    parser.add_argument("--quotes", type=Path, default=QUOTES, help="override, for self-testing")
    args = parser.parse_args()
    ensure_utf8_stdout()
    as_of = dt.date.fromisoformat(args.as_of)

    bom = load(args.bom)
    quotes = load(args.quotes)
    problems: list[str] = []

    seen: set[str] = set()
    for row in bom:
        key = row["key"]
        where = f"bom[{key}]"
        if not KEY_RE.match(key):
            problems.append(f"{where}: key must be TRADE-NN:ROOM:resource")
        if key in seen:
            problems.append(f"{where}: duplicate key")
        seen.add(key)
        if row["trade"] not in TRADES:
            problems.append(f"{where}: unknown trade {row['trade']!r}")
        elif not key.startswith(row["trade"] + "-"):
            problems.append(f"{where}: key prefix disagrees with trade {row['trade']!r}")
        if row["qty_source"] not in QTY_SOURCES:
            problems.append(f"{where}: qty_source {row['qty_source']!r} not in {sorted(QTY_SOURCES)}")
        # A populated quantity must say where it came from.
        if row["qty"].strip() and row["qty_source"] == "unmeasured":
            problems.append(f"{where}: qty is populated but qty_source is 'unmeasured' - state the source")
        if row["qty"].strip():
            try:
                float(row["qty"])
            except ValueError:
                problems.append(f"{where}: qty {row['qty']!r} is not a number")
        if row["stage"] not in STAGES:
            problems.append(f"{where}: stage {row['stage']!r} not in 1..5")
        waste = row["waste_basis"]
        if waste and waste != "none" and not (waste.startswith("pct:") or waste == "nested"):
            problems.append(f"{where}: waste_basis {waste!r} must be 'pct:N', 'nested' or 'none'")
        if waste == "nested" and row["trade"] not in NESTED_OK_TRADES:
            problems.append(
                f"{where}: 'nested' waste is only justified for {sorted(NESTED_OK_TRADES)} "
                "(large-format tile, sheet goods) - use pct:N"
            )
        # An expected rate without a stated source is an unattributed number.
        if row["rate_expected"].strip() and not row["rate_expected_source"].strip():
            problems.append(f"{where}: rate_expected is set but rate_expected_source is empty")
        # Interfaces are arguments, not purchases.
        if row["trade"] == "IFC" and (row["rate_expected"].strip() or row["product_id"].strip()):
            problems.append(f"{where}: IFC rows are trade interfaces, not purchases - no rate or product")

    keys = {row["key"] for row in bom}
    for i, row in enumerate(quotes, start=2):
        where = f"quotes[line {i}]"
        if row["bom_key"] not in keys:
            problems.append(f"{where}: bom_key {row['bom_key']!r} does not resolve to a BOM line")
        if row["status"] not in QUOTE_STATUS:
            problems.append(f"{where}: status {row['status']!r} not in {sorted(QUOTE_STATUS)}")
        parse_date(row["quote_date"], where, problems)
        parse_date(row["valid_until"], where, problems)

    # ---- the working view, not defects -------------------------------------
    quotes_by_key: dict[str, list[dict]] = defaultdict(list)
    for row in quotes:
        quotes_by_key[row["bom_key"]].append(row)

    purchasable = [r for r in bom if r["trade"] != "IFC"]
    unmeasured = [r for r in purchasable if not r["qty"].strip()]
    no_quote = [r for r in purchasable if not quotes_by_key.get(r["key"])]
    expired = [
        (r["bom_key"], r["source"], r["valid_until"])
        for r in quotes
        if (d := parse_date(r["valid_until"], "", [])) and d < as_of and r["status"] != "expired"
    ]
    no_rate = [r["key"] for r in purchasable if not r["rate_expected"].strip()]
    unverified_rate = [
        r["key"]
        for r in purchasable
        if r["rate_expected"].strip() and "UNVERIFIED" in r["rate_expected_source"]
    ]

    print(f"BOM lines: {len(bom)}  ({len(purchasable)} purchasable, {len(bom) - len(purchasable)} interfaces)")
    print("By trade: " + ", ".join(f"{t}={n}" for t, n in sorted(Counter(r['trade'] for r in bom).items())))
    print("By stage: " + ", ".join(f"{s}={n}" for s, n in sorted(Counter(r['stage'] for r in bom).items())))
    print(f"Quotes recorded: {len(quotes)}")
    print()
    print(f"  quantities not yet measurable : {len(unmeasured)}/{len(purchasable)}  (expected at this stage)")
    print(f"  lines with no quote at all    : {len(no_quote)}/{len(purchasable)}")
    print(f"  lines with no expected rate   : {len(no_rate)}/{len(purchasable)}")
    if unverified_rate:
        print(
            f"  !! expected rates from an UNVERIFIED, UNDATED source: {len(unverified_rate)}"
            " - anchors for negotiation only, not benchmarks"
        )
    if expired:
        print(f"  !! quotes past valid_until as of {as_of}: {len(expired)}")
        for key, source, until in expired:
            print(f"      {key} <- {source} expired {until}")

    if problems:
        print()
        print(f"FAIL {len(problems)} problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print()
    print("PASS - schema, enums, key format and quote references are consistent.")
    print("Note: empty quantities are correct until the model carries phase and finishes;")
    print("      rate discovery does not wait for them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
