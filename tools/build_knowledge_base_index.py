#!/usr/bin/env python3
"""Build the generated numeric-claim projection for the renovation vault.

Markdown remains authoritative. This tool extracts atomic numeric mentions
from source notes plus the maintained Numeric_Data and comparison-table store,
then replaces a dedicated SQLite projection atomically. It is intentionally a
conservative projection: ambiguous values remain rows with a skip/status
reason instead of being silently converted or discarded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "11_Budget_and_Planning" / "_supporting" / "knowledge" / "sources"
STORE_DIR = ROOT / "11_Budget_and_Planning" / "_supporting" / "knowledge" / "intermediate" / "store"
DEFAULT_DB = ROOT / "data" / "knowledge_base.db"
SOURCE_ID = re.compile(r"(?:yt|web)_[A-Za-z0-9_-]+", re.IGNORECASE)
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
YEAR = re.compile(r"\b(20\d{2})\b")

# Currency/measurement mentions. A line can yield several atomic rows.
NUMBER = r"\d[\d,]*(?:\.\d+)?"
RANGE = rf"{NUMBER}(?:\s*[–—-]\s*{NUMBER})?"
NUMERIC = re.compile(
    rf"(?P<value>{RANGE})\s*(?P<unit>USD/(?:m²|m2)|RUB/(?:m²|m2)|BYN/(?:m²|m2)|EUR/(?:m²|m2)|USD|RUB|BYN|EUR|\$/(?:m²|m2)|\$|€|%|m²|m2|мм|mm|см|cm|м\b|m\b|кг|kg|дБ|dB|кВт|kW|°C|C\b|дн(?:ей|я)?|days?|час(?:а|ов)?|hours?|лет|years?|тонн(?:ы|а)?|tonnes?)",
    re.IGNORECASE,
)
BARE_CURRENCY = re.compile(rf"(?P<unit>\$|€)\s*(?P<value>{RANGE})")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("'\"")
    return result


def source_files() -> list[Path]:
    files = sorted(SOURCE_DIR.glob("*.md"))
    for name in ("Numeric_Data.md", "Cross_Source_Comparison_Tables.md"):
        path = STORE_DIR / name
        if path.exists() and path not in files:
            files.append(path)
    for folder in sorted(p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^(?!00_)\d{2}_", p.name)):
        files.extend(path for path in sorted(folder.glob("*.md")) if not path.name.endswith("_Index.md"))
        analysis = folder / "analysis"
        if analysis.is_dir():
            files.extend(sorted(analysis.glob("*.md")))
    return files


def context_value(front: dict[str, str], line: str, key: str) -> str | None:
    if key in front:
        return front[key]
    if key == "year":
        match = YEAR.search(line)
        return match.group(1) if match else None
    return None


def region(front: dict[str, str], line: str) -> str | None:
    return front.get("regional_applicability") or front.get("region") or front.get("spoken_project_location")


def region_confidence(value: str | None) -> str:
    if not value or any(marker in value.lower() for marker in ("unresolved", "not stated", "unknown")):
        return "missing"
    if "level 1" in value.lower() or "confirmed" in value.lower():
        return "exact"
    return "inferred"


def source_id(front: dict[str, str], line: str, path: Path) -> str | None:
    for key in ("video_id", "source_id", "web_id"):
        if front.get(key):
            value = front[key]
            if value.lower().startswith(("yt_", "web_")):
                return value
            if key == "video_id":
                return f"yt_{value}"
            if key == "web_id":
                return f"web_{value}"
    match = SOURCE_ID.search(line)
    if match:
        return match.group(0)
    match = SOURCE_ID.search(path.name)
    return match.group(0) if match else None


def currency_for(unit: str, front: dict[str, str]) -> str | None:
    unit = unit.lower()
    unit = unit.split("/", 1)[0]
    if unit in {"$", "usd"}:
        return "USD"
    if unit == "€" or unit == "eur":
        return "EUR"
    if unit in {"rub", "byn"}:
        return unit.upper()
    if unit not in {"rub", "byn", "usd", "$", "eur", "€"}:
        return None
    match = re.search(r"\b(USD|RUB|BYN|EUR)\b", front.get("currency", ""), re.IGNORECASE)
    return match.group(1).upper() if match else None


def normalized(value: str) -> float | None:
    try:
        if "-" in value or "–" in value or "—" in value:
            return None
        return float(value.replace(",", ""))
    except ValueError:
        return None


def confidence(line: str, front: dict[str, str]) -> str:
    for value in ("uncertain", "unverified", "inferred", "single-account", "confirmed"):
        if value in line.lower():
            return value
    return front.get("confidence", "unclassified")


def extract() -> tuple[list[dict], dict]:
    rows: list[dict] = []
    warnings: list[str] = []
    files = source_files()
    for path in files:
        text = path.read_text(encoding="utf-8")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        front = parse_frontmatter(text)
        sid = source_id(front, "", path)
        for line_no, line in enumerate(text.splitlines(), 1):
            matches = list(NUMERIC.finditer(line)) + list(BARE_CURRENCY.finditer(line))
            for match in matches:
                value = match.group("value")
                unit = match.group("unit")
                token = match.group(0)
                anchor_match = re.search(r"^(#{1,6})\s+(.+)$", line)
                anchor = anchor_match.group(2).strip() if anchor_match else None
                source_span = f"{path.relative_to(ROOT).as_posix()}:{line_no}:{match.start()+1}-{match.end()}"
                source_key = sid or path.relative_to(ROOT).as_posix()
                claim_text = line.strip()
                claim_id = hashlib.sha256(
                    "|".join((source_key, source_span, claim_text)).encode("utf-8")
                ).hexdigest()
                year = context_value(front, line, "year") or front.get("upload_date", "")[:4] or None
                reg = region(front, line)
                cur = currency_for(unit, front)
                conversion_status = "not_applicable" if cur == "USD" else ("needs_region_or_year" if not reg or not year else "source_currency_only")
                rows.append({
                    "claim_id": claim_id,
                    "claim_group_id": hashlib.sha256((source_key + "|" + str(line_no)).encode()).hexdigest(),
                "source_id": sid or source_id(front, line, path),
                    "source_path": path.relative_to(ROOT).as_posix(),
                    "source_sha256": digest,
                    "wiki_page": path.relative_to(ROOT).as_posix() if re.match(r"^(?!00_)\d{2}_", path.parts[0]) else None,
                    "section_anchor": anchor,
                    "source_span": source_span,
                    "claim_text": claim_text,
                    "raw_value": value,
                    "normalized_value": normalized(value),
                    "unit": unit,
                    "currency": cur,
                    "region": reg,
                    "region_confidence": region_confidence(reg),
                    "year": int(year) if year and year.isdigit() else None,
                    "delivery_model": front.get("delivery_model") or front.get("delivery_model_class"),
                    "usd_equivalent": None,
                    "conversion_basis": None,
                    "conversion_status": conversion_status,
                    "confidence_tag": confidence(line, front),
                    "citation_token": sid,
                    "extractor_version": "numeric-claims-v1",
                    "extracted_at": datetime.now(timezone.utc).isoformat(),
                })
    metadata = {
        "input_file_count": len(files),
        "claim_count": len(rows),
        "warning_count": len(warnings),
        "warnings": warnings,
        "extractor_version": "numeric-claims-v1",
    }
    return rows, metadata


def create_db(path: Path, rows: list[dict], metadata: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix="knowledge_base.", suffix=".db", dir=path.parent)
    os.close(fd)
    temp = Path(temp_name)
    try:
        conn = sqlite3.connect(temp)
        try:
            conn.executescript("""
                CREATE TABLE numeric_claims (
                    claim_id TEXT NOT NULL,
                    claim_group_id TEXT NOT NULL,
                    source_id TEXT,
                    source_path TEXT NOT NULL,
                    source_sha256 TEXT NOT NULL,
                    wiki_page TEXT,
                    section_anchor TEXT,
                    source_span TEXT NOT NULL,
                    claim_text TEXT NOT NULL,
                    raw_value TEXT NOT NULL,
                    normalized_value REAL,
                    unit TEXT NOT NULL,
                    currency TEXT,
                    region TEXT,
                    region_confidence TEXT NOT NULL,
                    year INTEGER,
                    delivery_model TEXT,
                    usd_equivalent REAL,
                    conversion_basis TEXT,
                    conversion_status TEXT NOT NULL,
                    confidence_tag TEXT NOT NULL,
                    citation_token TEXT,
                    extractor_version TEXT NOT NULL,
                    extracted_at TEXT NOT NULL,
                    PRIMARY KEY (claim_id, extractor_version)
                );
                CREATE INDEX numeric_claims_region_year ON numeric_claims(region, year);
                CREATE INDEX numeric_claims_source ON numeric_claims(source_id);
                CREATE TABLE projection_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            """)
            columns = list(rows[0].keys()) if rows else []
            if columns:
                placeholders = ",".join("?" for _ in columns)
                conn.executemany(
                    f"INSERT INTO numeric_claims ({','.join(columns)}) VALUES ({placeholders})",
                    [[row[column] for column in columns] for row in rows],
                )
            for key, value in metadata.items():
                conn.execute("INSERT INTO projection_metadata VALUES (?, ?)", (key, json.dumps(value, ensure_ascii=False)))
            conn.commit()
        finally:
            conn.close()
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Example: python tools/build_knowledge_base_index.py --json --region Belarus --from-year 2020 --to-year 2020 --unit '$' --text m --priced-only",
    )
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--region", help="case-insensitive substring filter")
    parser.add_argument("--from-year", type=int)
    parser.add_argument("--to-year", type=int)
    parser.add_argument("--unit", help="case-insensitive substring filter, e.g. m²")
    parser.add_argument("--text", help="case-insensitive substring filter over the claim text")
    parser.add_argument("--priced-only", action="store_true", help="exclude measurements without a currency")
    parser.add_argument("--region-confidence", choices=("exact", "inferred", "missing", "any"), default="exact", help="default exact; use inferred/any explicitly")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    rows, metadata = extract()
    create_db(args.database, rows, metadata)
    with sqlite3.connect(args.database) as conn:
        conn.row_factory = sqlite3.Row
        query = "SELECT source_id, source_path, raw_value, unit, currency, region, region_confidence, year, claim_id FROM numeric_claims WHERE 1=1"
        params: list[object] = []
        if args.region:
            query += " AND lower(region) LIKE lower(?)"
            params.append(f"%{args.region}%")
        if args.from_year is not None:
            query += " AND year >= ?"
            params.append(args.from_year)
        if args.to_year is not None:
            query += " AND year <= ?"
            params.append(args.to_year)
        if args.unit:
            query += " AND lower(unit) LIKE lower(?)"
            params.append(f"%{args.unit}%")
        if args.text:
            query += " AND lower(claim_text) LIKE lower(?)"
            params.append(f"%{args.text}%")
        if args.priced_only:
            query += " AND currency IS NOT NULL"
        if args.region_confidence != "any":
            query += " AND region_confidence = ?"
            params.append(args.region_confidence)
        query += " ORDER BY year, source_path, source_span"
        result = [dict(row) for row in conn.execute(query, params).fetchall()]
    output = {"database": args.database.relative_to(ROOT).as_posix() if args.database.is_relative_to(ROOT) else str(args.database), "metadata": metadata, "query_result_count": len(result), "query_results": result}
    print(json.dumps(output, ensure_ascii=False, indent=2) if args.json else f"Built {metadata['claim_count']} numeric claims from {metadata['input_file_count']} files; query matched {len(result)} rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
