"""Generate the per-trade scope document sent to a contractor to solicit a quote.

Why this exists, and why it comes BEFORE quote intake: you cannot receive a quote
without first sending a scope. The owner's decision of 2026-09-08 - "no one contract,
small contracts per each type of work" - makes the trade the unit of engagement, so
the per-trade pack is a first-class output rather than a reporting convenience.

Each pack joins three things:
  * the BOM lines for that trade                     (data/procurement/bom.csv)
  * the requirements, questions and acceptance basis (data/procurement/trade_requirements.json)
  * the interfaces that touch that trade             (BOM rows with trade = IFC)

Every requirement prints with the vault page it came from, so a contractor's question
about "why" has an answer, and so a claim can be checked rather than taken on trust.

Usage:
    python tools/procurement/trade_pack.py --trade TIL
    python tools/procurement/trade_pack.py --all
    python tools/procurement/trade_pack.py --all --out-dir data/outputs/trade_packs
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOM = ROOT / "data" / "procurement" / "bom.csv"
REQS = ROOT / "data" / "procurement" / "trade_requirements.json"
DEFAULT_OUT = ROOT / "data" / "outputs" / "trade_packs"


def ensure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # pragma: no cover
        pass


def load_bom() -> list[dict]:
    with BOM.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def fmt_qty(row: dict) -> str:
    """A quantity we do not have is stated as such, never guessed or blanked."""
    if row["qty"].strip():
        return f"{row['qty']} {row['unit']}"
    if row["unit"].strip():
        return f"**to be confirmed** ({row['unit']})"
    return "**n/a**"


def fmt_rate(row: dict) -> str:
    if not row["rate_expected"].strip():
        return "—"
    caveat = ""
    if "UNVERIFIED" in row["rate_expected_source"]:
        caveat = " ⚠️ *unverified, undated — an anchor, not a benchmark*"
    return f"{row['rate_expected']} {row['rate_unit']}{caveat}"


def render(trade: str, reqs: dict, bom: list[dict]) -> str:
    spec = reqs.get(trade)
    if spec is None:
        sys.exit(f"FAIL no requirements defined for trade {trade!r} in {REQS.name}")
    universal = reqs["_universal"]

    lines = [r for r in bom if r["trade"] == trade]
    # An interface names the trades it binds, explicitly. An earlier version matched
    # the trade's name against the interface text and silently missed "tiler" when
    # looking for "tiling" - which is exactly the kind of quiet omission that would
    # leave a join unassigned on site.
    interfaces = [
        r
        for r in bom
        if r["trade"] == "IFC"
        and trade in [t.strip() for t in r.get("applies_to", "").split(";") if t.strip()]
    ]

    out: list[str] = []
    out.append(f"# Scope for quotation — {spec['title']}")
    out.append("")
    out.append(
        f"**ЖК Дубравинский, Minsk · generated {dt.date.today().isoformat()} · "
        f"trade code `{trade}` · {len(lines)} scope line(s)**"
    )
    out.append("")
    out.append(
        "This is a request for a **rate**, not a request for a lump sum. "
        "**Quantities marked *to be confirmed* are being measured and do not block quoting** — "
        "we would like your unit rate now and will apply it to the measured quantity."
    )
    out.append("")
    out.append("---")
    out.append("")

    out.append("## 1. What we are asking you to price")
    out.append("")
    if lines:
        out.append("| # | Work | Room | Quantity | Our expected rate | Stage |")
        out.append("| :-- | :--- | :--- | :--- | :--- | :-- |")
        for i, row in enumerate(lines, 1):
            out.append(
                f"| {i} | {row['task']} | {row['room']} | {fmt_qty(row)} "
                f"| {fmt_rate(row)} | {row['stage']} |"
            )
        out.append("")
        out.append(
            "**The expected rate is our own working anchor, openly stated so the "
            "conversation starts from a number rather than from nothing. "
            "Where it is marked unverified, treat it as exactly that.**"
        )
    else:
        out.append("*No scope lines are recorded for this trade yet.*")
    out.append("")

    for row in lines:
        if row["notes"].strip():
            out.append(f"- **{row['task']} ({row['room']})** — {row['notes']}")
    out.append("")

    out.append("## 2. Requirements")
    out.append("")
    out.append(f"### {spec['title']}")
    out.append("")
    for req in spec["requirements"]:
        out.append(f"- {req['text']}")
        out.append(f"  <br>↳ *basis: `{req['source']}`*")
    out.append("")
    out.append(f"### {universal['title']}")
    out.append("")
    for req in universal["requirements"]:
        out.append(f"- {req['text']}")
        out.append(f"  <br>↳ *basis: `{req['source']}`*")
    out.append("")

    if interfaces:
        out.append("## 3. Interfaces with other trades — to be agreed before you start")
        out.append("")
        out.append(
            "**These are not items to price.** They are the joins between contracts, "
            "which belong to nobody by default and are the main risk of letting the work "
            "as several small contracts."
        )
        out.append("")
        for row in interfaces:
            out.append(f"- **{row['task']}**")
            if row["notes"].strip():
                out.append(f"  <br>{row['notes']}")
        out.append("")
        for req in reqs["IFC"]["requirements"]:
            out.append(f"> {req['text']}")
            out.append(f"> <br>↳ *basis: `{req['source']}`*")
        out.append("")

    section = 4 if interfaces else 3
    out.append(f"## {section}. What we need you to tell us")
    out.append("")
    for question in spec.get("questions", []):
        out.append(f"- {question}")
    for question in universal["questions"]:
        out.append(f"- {question}")
    out.append("")

    out.append(f"## {section + 1}. Acceptance basis")
    out.append("")
    out.append("**Work is accepted against this, and it is stated up front rather than raised at the end.**")
    out.append("")
    for item in spec.get("acceptance", []):
        out.append(f"- {item}")
    for item in universal["acceptance"]:
        out.append(f"- {item}")
    out.append("")
    out.append("---")
    out.append("")
    out.append(
        "*Every requirement above cites the page it came from. Those pages are a private "
        "knowledge base built from practitioner sources and from the governing Belarusian "
        "legislation — so if you disagree with one, we would genuinely like to know, because "
        "it means either we have it wrong or the source does.*"
    )
    out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trade", help="trade code, e.g. TIL")
    parser.add_argument("--all", action="store_true", help="every trade present in the BOM")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    ensure_utf8_stdout()

    if not args.trade and not args.all:
        parser.error("give --trade CODE or --all")

    reqs = json.loads(REQS.read_text(encoding="utf-8"))
    bom = load_bom()

    if args.all:
        present = sorted({r["trade"] for r in bom if r["trade"] != "IFC"})
    else:
        present = [args.trade]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    skipped = []
    for trade in present:
        if trade not in reqs:
            skipped.append(trade)
            continue
        slug = reqs[trade]["title"].lower().replace(" ", "_").replace("-", "")
        path = args.out_dir / f"{trade}_{slug}.md"
        path.write_text(render(trade, reqs, bom), encoding="utf-8")
        written.append(path)

    for path in written:
        print(f"wrote {path.relative_to(ROOT)}")
    if skipped:
        print()
        print(f"!! {len(skipped)} trade(s) in the BOM have no requirements defined yet: {', '.join(skipped)}")
        print("   A pack without requirements would be a bare quantity list, so none was written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
