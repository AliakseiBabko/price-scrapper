"""
Generate 00_Master/exchange_rates_reference.md from database.

Backfills unverified rows (BYN 2017-2021) from data/scraper.db while preserving
all previously-confirmed benchmark rates (RUB 2017-2025, BYN 2022-2025) per project policy.
"""

import datetime
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "scraper.db"
DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parents[2] / "00_Master" / "exchange_rates_reference.md"

PRESERVED_CONFIRMED_RUB = {
    "2017": ("58.3 RUB per USD", "2026-08-20", "https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf", "confirmed", "Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average"),
    "2018": ("62.5 RUB per USD", "2026-08-20", "https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf", "confirmed", "Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average"),
    "2019": ("64.7 RUB per USD", "2026-08-20", "https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf", "confirmed", "Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average"),
    "2020": ("71.9 RUB per USD", "2026-08-20", "https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf", "confirmed", "Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average"),
    "2021": ("73.6 RUB per USD", "2026-08-20", "https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf", "confirmed", "Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average"),
    "2022": ("67.5 RUB per USD", "2026-08-20", "https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf", "confirmed", "Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average"),
    "2023": ("84.7 RUB per USD", "2026-08-20", "https://www.cbr.ru/content/document/file/165597/on_eng_2025%282026-2027%29.pdf", "confirmed", "Bank of Russia, Table 3, nominal exchange rate RUB/USD, yearly average"),
    "2024": ("92.66 RUB per USD", "2026-08-21", "https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/01/2024&date_req2=31/12/2024&VAL_NM_RQ=R01235", "confirmed", "Bank of Russia official daily-rate archive, full calendar year, mean of 248 published daily rates (business days only, as CBR publishes)"),
    "2025": ("83.21 RUB per USD", "2026-08-21", "https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/01/2025&date_req2=31/12/2025&VAL_NM_RQ=R01235", "confirmed", "Bank of Russia official daily-rate archive, full calendar year, mean of 247 published daily rates"),
}

PRESERVED_CONFIRMED_BYN = {
    "2022": ("2.6290 BYN per USD", "2026-08-21", "https://www.nbrb.by/api/exrates/rates/dynamics/431?startDate=2022-01-01&endDate=2022-12-31", "confirmed", "National Bank of the Republic of Belarus official daily-rate archive, full calendar year, mean of 365 published daily rates"),
    "2023": ("3.0091 BYN per USD", "2026-08-21", "https://www.nbrb.by/api/exrates/rates/dynamics/431?startDate=2023-01-01&endDate=2023-12-31", "confirmed", "National Bank of the Republic of Belarus official daily-rate archive, full calendar year, mean of 365 published daily rates"),
    "2024": ("3.2458 BYN per USD", "2026-08-21", "https://www.nbrb.by/api/exrates/rates/dynamics/431?startDate=2024-01-01&endDate=2024-12-31", "confirmed", "National Bank of the Republic of Belarus official daily-rate archive, full calendar year, mean of 365 published daily rates"),
    "2025": ("3.0694 BYN per USD", "2026-08-21", "https://www.nbrb.by/api/exrates/rates/dynamics/431?startDate=2025-01-01&endDate=2025-12-31", "confirmed", "National Bank of the Republic of Belarus official daily-rate archive, full calendar year, mean of 365 published daily rates"),
}

def generate_reference_table(db_path: Path) -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Calculate BYN annual averages from DB for 2017-2021
    byn_db_averages = {}
    for year in range(2017, 2022):
        y_str = str(year)
        rows = cursor.execute("""
            SELECT rate FROM exchange_rates
            WHERE currency_pair = 'USD/BYN' AND rate_date >= ? AND rate_date <= ?
        """, (f"{y_str}-01-01", f"{y_str}-12-31")).fetchall()
        if rows:
            rates = [r[0] for r in rows]
            avg = sum(rates) / len(rates)
            byn_db_averages[y_str] = (avg, len(rates))

    conn.close()

    lines = []
    lines.append("# Annual Average Exchange Rates Reference\n")
    lines.append("This reference records annual average exchange rate benchmarks used across the renovation vault to normalize historical or secondary reference price estimates.\n")
    lines.append("> [!IMPORTANT]")
    lines.append("> **Source-Year Conversion Policy**")
    lines.append("> Historical prices from video sources are converted using the average exchange rate of the **source year** (or explicitly stated video year), never the current spot rate. Unverified rates are marked `TODO / needs source`. Projections (e.g. 2026) must not be used for historical price normalization.\n")
    lines.append("## Annual Average Benchmark Table\n")
    lines.append("| year | currency_pair | average_rate | retrieval_date | source_url | confidence | notes |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    # 1. USD/RUB rows (2017 - 2025)
    for year in range(2017, 2026):
        y_str = str(year)
        rate_str, ret_date, src_url, conf, notes = PRESERVED_CONFIRMED_RUB[y_str]
        lines.append(f"| **{y_str}** | USD/RUB | {rate_str} | {ret_date} | {src_url} | {conf} | {notes} |")

    # 2. USD/BYN rows (2017 - 2025)
    for year in range(2017, 2026):
        y_str = str(year)
        if y_str in PRESERVED_CONFIRMED_BYN:
            rate_str, ret_date, src_url, conf, notes = PRESERVED_CONFIRMED_BYN[y_str]
        else:
            avg_rate, count = byn_db_averages[y_str]
            rate_str = f"{avg_rate:.4f} BYN per USD"
            ret_date = "2026-08-21"
            if y_str == "2021":
                src_url = "https://www.nbrb.by/api/exrates/rates/dynamics/145 + /431"
                notes = f"National Bank of the Republic of Belarus official daily-rate archive (transition Cur_ID=145 up to 2021-07-08, Cur_ID=431 from 2021-07-09), full calendar year, mean of {count} published daily rates"
            else:
                src_url = f"https://www.nbrb.by/api/exrates/rates/dynamics/145?startDate={y_str}-01-01&endDate={y_str}-12-31"
                notes = f"National Bank of the Republic of Belarus official daily-rate archive (Cur_ID=145), full calendar year, mean of {count} published daily rates"
            conf = "confirmed"
        lines.append(f"| **{y_str}** | USD/BYN | {rate_str} | {ret_date} | {src_url} | {conf} | {notes} |")

    # 3. 2026 projections
    lines.append("| **2026** | USD/BYN | unverified / partial-year; do not use for historical normalization | 2026-08-20 | https://www.nb-rb.by/engl/statistics/rates/avgrate.htm | projection (do not use for historical normalization) | No complete annual average exists yet |")
    lines.append("| **2026** | USD/RUB | unverified / partial-year; do not use for historical normalization | 2026-08-20 | https://www.cbr.ru/eng/currency_base/dynamics/ | projection (do not use for historical normalization) | No complete annual average exists yet |")

    # 4. unknown rows
    lines.append("| **unknown** | USD/BYN | unverified / needs source | 2026-08-20 | https://www.nb-rb.by/engl/statistics/rates/avgrate.htm | unaligned | Mark source_year as unknown; do not present converted values as directly comparable |")
    lines.append("| **unknown** | USD/RUB | unverified / needs source | 2026-08-20 | https://www.cbr.ru/eng/currency_base/dynamics/ | unaligned | Mark source_year as unknown; do not present converted values as directly comparable |")

    lines.append("\n## Notes on Derivation Methodology & Granularity\n")
    lines.append("- **Annual Benchmarks**: Recorded above for standard yearly normalization across the vault. For USD/RUB (2017–2023), figures reflect nominal yearly averages from the Bank of Russia monetary policy report (Table 3) to preserve consistency with existing vault content. USD/RUB 2024–2025 and USD/BYN 2017–2025 reflect full-calendar-year arithmetic means from official central-bank daily rate series.")
    lines.append("- **Date- and Range-Aware Lookups**: For sources mentioning specific months, quarters, or exact dates, use the `tools/pricing/currency_converter.py` tool, which queries the daily series stored in `data/scraper.db` (CBR and NBRB official publications).")

    return "\n".join(lines) + "\n"

def main() -> int:
    db_path = DEFAULT_DB_PATH
    output_path = DEFAULT_OUTPUT_PATH

    print(f"Reading rates from {db_path}...")
    content = generate_reference_table(db_path)

    print(f"Writing updated reference table to {output_path}...")
    output_path.write_text(content, encoding="utf-8")
    print("Regeneration complete.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
