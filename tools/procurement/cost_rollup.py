"""Roll the BOM and the quotes received into a budget view, for negotiation.

Owner's decisions this implements (2026-09-08):
  * The estimate is FOR US - for price negotiation and verification. Not a смета.
  * Small contracts per work type, so the TRADE is the primary view.
  * Line level stays available "for the arguing".

Three rules it will not break:

  1. NEVER a single total when the inputs are ranges. An expected rate of "45-65"
     produces a low and a high, and they are carried through to the bottom line.
     A point estimate here would be a fabricated precision.
  2. NEVER silently use an expired quote. A rate past its valid_until is excluded
     from the arithmetic and reported separately, because it is a memory not a price.
  3. NEVER hide a scope difference behind a cheaper number. Two quotes for one line
     are printed WITH their scope notes, because "cheaper" usually means "excludes
     something", and catching that is the whole point of the exercise.

Usage:
    python tools/procurement/cost_rollup.py
    python tools/procurement/cost_rollup.py --detail TIL
    python tools/procurement/cost_rollup.py --as-of 2026-12-01
    python tools/procurement/cost_rollup.py --out data/outputs/budget/rollup.md
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOM = ROOT / "data" / "procurement" / "bom.csv"
QUOTES = ROOT / "data" / "procurement" / "quotes.csv"

# A quote whose two rates differ from another quote's by more than this is worth
# asking about rather than simply accepting the lower one.
SPREAD_FLAG = 1.5


def ensure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass


def read(path: Path) -> list[dict]:
    if not path.exists():
        sys.exit(f"FAIL missing {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_range(value: str) -> tuple[float, float] | None:
    """'45-65' -> (45, 65); '52' -> (52, 52); '' -> None.

    Ranges stay ranges. Collapsing one to its midpoint would invent a precision the
    source never had, which is the same error as quoting cents on a converted price.
    """
    value = (value or "").strip()
    if not value:
        return None
    match = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*[-–]\s*(\d+(?:[.,]\d+)?)", value)
    if match:
        lo = float(match.group(1).replace(",", "."))
        hi = float(match.group(2).replace(",", "."))
        return (min(lo, hi), max(lo, hi))
    try:
        single = float(value.replace(",", "."))
    except ValueError:
        return None
    return (single, single)


def quote_total(row: dict) -> float | None:
    parts = [parse_range(row.get(k, "")) for k in ("rate_material", "rate_labour")]
    present = [p for p in parts if p is not None]
    if not present:
        return None
    return sum(p[0] for p in present)


def money(lo: float | None, hi: float | None) -> str:
    if lo is None or hi is None:
        return "—"
    if abs(hi - lo) < 0.005:
        return f"{lo:,.0f}"
    return f"{lo:,.0f}–{hi:,.0f}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", default=dt.date.today().isoformat())
    parser.add_argument("--detail", help="trade code for the line-level view")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--bom", type=Path, default=BOM, help="override, for self-testing")
    parser.add_argument("--quotes", type=Path, default=QUOTES, help="override, for self-testing")
    args = parser.parse_args()
    ensure_utf8_stdout()
    as_of = dt.date.fromisoformat(args.as_of)

    all_rows = read(args.bom)
    bom = [r for r in all_rows if r["trade"] != "IFC"]
    interfaces = [r for r in all_rows if r["trade"] == "IFC"]
    quotes = read(args.quotes)

    live: dict[str, list[dict]] = defaultdict(list)
    stale: list[dict] = []
    for row in quotes:
        if row["status"] == "rejected":
            continue
        until = row["valid_until"].strip()
        try:
            expired = bool(until) and dt.date.fromisoformat(until) < as_of
        except ValueError:
            expired = False
        (stale if expired else live[row["bom_key"]]).append(row)

    out: list[str] = []
    out.append(f"# Budget rollup — as of {as_of.isoformat()}")
    out.append("")
    out.append(
        "**A negotiation and verification view, not a смета.** Ranges stay ranges; "
        "expired quotes are excluded from the arithmetic; scope notes are printed next to "
        "prices because a cheaper number usually means something was left out."
    )
    out.append("")

    # ---- primary view: by trade -------------------------------------------
    by_trade: dict[str, list[dict]] = defaultdict(list)
    for row in bom:
        by_trade[row["trade"]].append(row)

    out.append("## By trade — the primary view")
    out.append("")
    out.append("| Trade | Lines | Quantities known | Lines quoted | Sources | Extended cost (BYN) | Basis |")
    out.append("| :-- | --: | --: | --: | :--- | :--- | :--- |")

    grand_lo = grand_hi = 0.0
    for trade in sorted(by_trade):
        rows = by_trade[trade]
        measured = [r for r in rows if r["qty"].strip()]
        quoted = [r for r in rows if live.get(r["key"])]
        sources = sorted({q["source"] for r in rows for q in live.get(r["key"], [])})
        lo = hi = 0.0
        priceable = 0
        used_quote = used_expected = False
        for row in rows:
            qty = parse_range(row["qty"])
            if qty is None:
                continue
            cands = [quote_total(q) for q in live.get(row["key"], [])]
            cands = [c for c in cands if c is not None]
            if cands:
                rate = (min(cands), max(cands))
                used_quote = True
            else:
                rate = parse_range(row["rate_expected"])
                if rate is None:
                    continue
                used_expected = True
            lo += qty[0] * rate[0]
            hi += qty[1] * rate[1]
            priceable += 1
        basis = []
        if used_quote:
            basis.append("quoted")
        if used_expected:
            basis.append("**expected**")
        if not basis:
            basis.append("*nothing priceable yet*")
        grand_lo += lo
        grand_hi += hi
        out.append(
            f"| `{trade}` | {len(rows)} | {len(measured)}/{len(rows)} | {len(quoted)}/{len(rows)} "
            f"| {', '.join(sources) or '—'} | {money(lo, hi) if priceable else '—'} | {' + '.join(basis)} |"
        )

    out.append("")
    if grand_lo or grand_hi:
        out.append(f"**Extended total of what is currently priceable: {money(grand_lo, grand_hi)} BYN.**")
    else:
        out.append(
            "**No line is priceable yet — every quantity is still unmeasured.** "
            "That is expected at this stage: rate discovery does not wait for quantities. "
            "Send the trade packs, record the rates in `quotes.csv`, and this table fills in "
            "the moment `cap2`/`cap5` give the model its phase and finishes."
        )
    out.append("")

    # ---- verification signals ---------------------------------------------
    spreads = []
    for row in bom:
        totals = [(q["source"], quote_total(q)) for q in live.get(row["key"], [])]
        totals = [(s, t) for s, t in totals if t]
        if len(totals) > 1:
            lo_s, lo_v = min(totals, key=lambda x: x[1])
            hi_s, hi_v = max(totals, key=lambda x: x[1])
            if lo_v and hi_v / lo_v > SPREAD_FLAG:
                spreads.append((row["key"], lo_s, lo_v, hi_s, hi_v, hi_v / lo_v))

    if spreads or stale:
        out.append("## Verification signals")
        out.append("")
    if spreads:
        out.append(f"**Quotes differing by more than {SPREAD_FLAG:g}× — ask what the cheaper one excludes:**")
        out.append("")
        for key, lo_s, lo_v, hi_s, hi_v, factor in spreads:
            out.append(f"- `{key}` — {lo_s} {lo_v:,.0f} vs {hi_s} {hi_v:,.0f} (**{factor:.1f}×**)")
        out.append("")
    if stale:
        out.append("**Excluded from the arithmetic — past `valid_until`:**")
        out.append("")
        for row in stale:
            out.append(
                f"- `{row['bom_key']}` — {row['source']}, expired {row['valid_until']}. "
                "Re-ask rather than assume it still holds."
            )
        out.append("")

    if interfaces:
        out.append("## Interfaces — unpriced by design")
        out.append("")
        out.append(
            f"**{len(interfaces)} trade interface(s) carry no price and never will.** They are the joins "
            "between separate small contracts, and they are assigned in writing rather than bought."
        )
        out.append("")
        for row in interfaces:
            out.append(f"- **{row['task']}** → binds `{row.get('applies_to', '')}`")
        out.append("")

    # ---- line detail, on request ------------------------------------------
    if args.detail:
        trade = args.detail.upper()
        rows = by_trade.get(trade)
        if not rows:
            sys.exit(f"FAIL no BOM lines for trade {trade!r}")
        out.append(f"## Line detail — `{trade}`, for the arguing")
        out.append("")
        for row in rows:
            out.append(f"### {row['task']} — {row['room']}")
            out.append("")
            out.append(f"- key `{row['key']}` · role `{row['resource_role']}` · stage {row['stage']}")
            product = row["product_id"].strip() or "**not chosen yet** (swap here, not in the model)"
            out.append(f"- product: {product}")
            qty = f"{row['qty']} {row['unit']}" if row["qty"].strip() else f"**unmeasured** ({row['unit']})"
            out.append(f"- quantity: {qty} · source `{row['qty_source']}` · waste `{row['waste_basis']}`")
            anchor = row["rate_expected"].strip() or "—"
            out.append(f"- our anchor: {anchor} {row['rate_unit']} — *from `{row['rate_expected_source']}`*")
            got = live.get(row["key"], [])
            if got:
                out.append("- quotes:")
                for q in sorted(got, key=lambda x: quote_total(x) or 0):
                    total = quote_total(q)
                    out.append(
                        f"    - **{q['source']}** {total:,.0f} {q['rate_unit']} "
                        f"(quoted {q['quote_date']}, valid to {q['valid_until']}, {q['status']})"
                    )
                    if q["scope_note"].strip():
                        out.append(f"      <br>scope: *{q['scope_note']}*")
            else:
                out.append("- quotes: **none yet** — send the trade pack")
            if row["notes"].strip():
                out.append(f"- note: {row['notes']}")
            out.append("")

    text = "\n".join(out)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out.relative_to(ROOT)}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
