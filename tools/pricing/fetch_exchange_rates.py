import argparse
import datetime
import json
import os
import sqlite3
import ssl
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "scraper.db"
TODAY = datetime.date.today().isoformat()
SSL_CONTEXT = ssl.create_default_context()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

def init_db(conn: sqlite3.Connection) -> None:
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_pair TEXT NOT NULL,
                rate_date TEXT NOT NULL,
                rate REAL NOT NULL,
                source_url TEXT NOT NULL,
                retrieval_date TEXT NOT NULL,
                UNIQUE(currency_pair, rate_date)
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_exchange_rates_lookup 
            ON exchange_rates(currency_pair, rate_date)
        """)

def fetch_cbr_rub(start_date: datetime.date, end_date: datetime.date) -> list[dict]:
    """
    Fetch USD/RUB daily rates from Central Bank of Russia (CBR) XML dynamic endpoint.
    VAL_NM_RQ=R01235 is the official USD code.
    Dates in query string are DD/MM/YYYY.
    """
    d1 = start_date.strftime("%d/%m/%Y")
    d2 = end_date.strftime("%d/%m/%Y")
    url = f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={d1}&date_req2={d2}&VAL_NM_RQ=R01235"
    
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=30) as resp:
        xml_data = resp.read()
    
    root = ET.fromstring(xml_data)
    results = []
    for record in root.findall("Record"):
        raw_date = record.attrib.get("Date") # DD.MM.YYYY
        dt = datetime.datetime.strptime(raw_date, "%d.%m.%Y").date()
        val_text = record.find("Value").text.replace(",", ".")
        nominal_node = record.find("Nominal")
        nominal = float(nominal_node.text) if nominal_node is not None else 1.0
        rate = float(val_text) / nominal
        
        results.append({
            "currency_pair": "USD/RUB",
            "rate_date": dt.isoformat(),
            "rate": rate,
            "source_url": url,
            "retrieval_date": TODAY
        })
    return results

def fetch_nbrb_byn(start_date: datetime.date, end_date: datetime.date) -> list[dict]:
    """
    Fetch USD/BYN daily rates from National Bank of the Republic of Belarus (NBRB) API.
    Transitions between Cur_ID 145 (up to 2021-07-08) and Cur_ID 431 (from 2021-07-09).
    """
    results = []
    transition_date = datetime.date(2021, 7, 8)
    
    ranges_to_fetch = []
    if start_date <= transition_date:
        r1_end = min(end_date, transition_date)
        ranges_to_fetch.append((145, start_date, r1_end))
    if end_date > transition_date:
        r2_start = max(start_date, datetime.date(2021, 7, 9))
        ranges_to_fetch.append((431, r2_start, end_date))
        
    for cur_id, r_start, r_end in ranges_to_fetch:
        # Fetch year by year to avoid API payload limits
        curr = r_start
        while curr <= r_end:
            year_end = datetime.date(curr.year, 12, 31)
            chunk_end = min(r_end, year_end)
            url = f"https://www.nbrb.by/api/exrates/rates/dynamics/{cur_id}?startDate={curr.isoformat()}&endDate={chunk_end.isoformat()}"
            
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            
            for item in data:
                d_str = item["Date"][:10]
                rate = float(item["Cur_OfficialRate"])
                results.append({
                    "currency_pair": "USD/BYN",
                    "rate_date": d_str,
                    "rate": rate,
                    "source_url": url,
                    "retrieval_date": TODAY
                })
            curr = chunk_end + datetime.timedelta(days=1)
            
    return results

def get_table_counts(conn: sqlite3.Connection) -> dict[str, int]:
    cursor = conn.cursor()
    tables = [r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    counts = {}
    for t in sorted(tables):
        counts[t] = cursor.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
    return counts

def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch and store historical exchange rates for USD/RUB and USD/BYN.")
    parser.add_argument("--db-path", type=Path, default=DEFAULT_DB_PATH, help="Path to sqlite scraper.db")
    parser.add_argument("--start-year", type=int, default=2017, help="Starting year for backfill (default: 2017)")
    parser.add_argument("--end-year", type=int, default=datetime.date.today().year, help="Ending year for backfill")
    parser.add_argument("--backfill", action="store_true", help="Perform full backfill from start-year to today")
    parser.add_argument("--dry-run", action="store_true", help="Fetch rates but do not write to database")
    args = parser.parse_args()

    db_path = args.db_path
    if not db_path.exists() and not args.dry_run:
        print(f"Error: Database not found at {db_path}", file=sys.stderr)
        return 1

    start_date = datetime.date(args.start_year, 1, 1)
    end_date = datetime.date.today()

    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    
    counts_before = get_table_counts(conn)
    print("Database table row counts BEFORE operation:")
    for tbl, cnt in counts_before.items():
        print(f"  - {tbl}: {cnt}")

    if not args.dry_run:
        init_db(conn)

    print(f"\nFetching USD/RUB daily rates from CBR ({start_date} to {end_date})...")
    rub_records = fetch_cbr_rub(start_date, end_date)
    print(f"  Fetched {len(rub_records)} USD/RUB records.")

    print(f"\nFetching USD/BYN daily rates from NBRB ({start_date} to {end_date})...")
    byn_records = fetch_nbrb_byn(start_date, end_date)
    print(f"  Fetched {len(byn_records)} USD/BYN records.")

    all_records = rub_records + byn_records

    if args.dry_run:
        print("\n[DRY RUN] Skipping database write.")
    else:
        print(f"\nWriting {len(all_records)} total records to 'exchange_rates' table...")
        with conn:
            conn.executemany("""
                INSERT OR REPLACE INTO exchange_rates 
                (currency_pair, rate_date, rate, source_url, retrieval_date)
                VALUES (:currency_pair, :rate_date, :rate, :source_url, :retrieval_date)
            """, all_records)
        print("Database commit successful.")

    counts_after = get_table_counts(conn)
    print("\nDatabase table row counts AFTER operation:")
    for tbl, cnt in counts_after.items():
        diff = cnt - counts_before.get(tbl, 0)
        diff_str = f" (+{diff})" if diff > 0 else (" (0)" if diff == 0 else f" ({diff})")
        print(f"  - {tbl}: {cnt}{diff_str}")

    # Report coverage summary
    print("\nCoverage Summary by Year and Currency Pair:")
    for pair in ["USD/RUB", "USD/BYN"]:
        print(f"\n--- {pair} ---")
        rows = [r for r in all_records if r["currency_pair"] == pair]
        years = sorted(list(set(r["rate_date"][:4] for r in rows)))
        for y in years:
            y_rows = [r for r in rows if r["rate_date"].startswith(y)]
            dates = [r["rate_date"] for r in y_rows]
            avg = sum(r["rate"] for r in y_rows) / len(y_rows)
            print(f"  {y}: {len(y_rows):3d} rows | span: {min(dates)} .. {max(dates)} | daily arithmetic mean: {avg:.4f}")

    conn.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
