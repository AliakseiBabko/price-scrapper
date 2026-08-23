"""
Exchange Rate Lookup and Currency Normalization Module.

Provides date- and range-aware conversion between USD, RUB, and BYN backed by
daily central-bank rates stored in data/scraper.db.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sqlite3
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "scraper.db"

PAIR_ALIASES = {
    "USD/RUB": "USD/RUB",
    "RUB/USD": "USD/RUB",
    "USDRUB": "USD/RUB",
    "RUB": "USD/RUB",
    "USD/BYN": "USD/BYN",
    "BYN/USD": "USD/BYN",
    "USDBYN": "USD/BYN",
    "BYN": "USD/BYN",
}

def subtract_months(d: datetime.date, months: int) -> datetime.date:
    """Calendar-correct month subtraction (stdlib only, no dateutil dependency) -
    clamps the day-of-month if the target month is shorter (e.g. Mar 31 minus
    1 month -> Feb 28/29, not an invalid Feb 31)."""
    total = d.year * 12 + (d.month - 1) - months
    year, month = divmod(total, 12)
    month += 1
    last_day = (datetime.date(year + (month // 12), month % 12 + 1, 1) - datetime.timedelta(days=1)).day
    return datetime.date(year, month, min(d.day, last_day))


@dataclass
class RateLookupResult:
    currency_pair: str
    requested_period: str
    resolved_start_date: str
    resolved_end_date: str
    sample_count: int
    rate: float
    resolution_method: str
    effective_date: Optional[str] = None
    input_amount: Optional[float] = None
    converted_usd: Optional[float] = None

class CurrencyConverter:
    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Exchange rate database not found: {self.db_path}")

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def normalize_pair(self, pair: str) -> str:
        clean = pair.strip().upper()
        if clean in PAIR_ALIASES:
            return PAIR_ALIASES[clean]
        raise ValueError(f"Unsupported currency pair '{pair}'. Supported: USD/RUB, USD/BYN")

    def lookup_rate(
        self,
        pair: str,
        period: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        amount: Optional[float] = None,
    ) -> RateLookupResult:
        """
        Lookup exchange rate for a given currency pair and period or date range.
        
        Supported period formats:
          - 'YYYY-MM-DD': Exact date lookup (with fallback to nearest prior trading day)
          - 'YYYY-MM': Calendar month arithmetic mean
          - 'YYYY': Calendar year arithmetic mean
          - 'YYYY-MM-DD..YYYY-MM-DD': Custom date range arithmetic mean
        """
        canonical_pair = self.normalize_pair(pair)
        
        # Resolve dates from period or explicit range
        if period:
            period_str = period.strip()
            if ".." in period_str:
                parts = period_str.split("..")
                start_date, end_date = parts[0].strip(), parts[1].strip()
                method_label = "range_arithmetic_mean"
            elif re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", period_str):
                return self._lookup_exact_date(canonical_pair, period_str, amount)
            elif re.fullmatch(r"^\d{4}-\d{2}$", period_str):
                y, m = map(int, period_str.split("-"))
                start_date = f"{y:04d}-{m:02d}-01"
                # Determine last day of month
                if m == 12:
                    end_date = f"{y:04d}-12-31"
                else:
                    next_month = datetime.date(y, m + 1, 1) - datetime.timedelta(days=1)
                    end_date = next_month.isoformat()
                method_label = "month_arithmetic_mean"
            elif re.fullmatch(r"^\d{4}$", period_str):
                y = int(period_str)
                start_date = f"{y:04d}-01-01"
                end_date = f"{y:04d}-12-31"
                method_label = "year_arithmetic_mean"
            else:
                raise ValueError(
                    f"Unrecognized period format '{period}'. Use 'YYYY-MM-DD', 'YYYY-MM', 'YYYY', or 'YYYY-MM-DD..YYYY-MM-DD'."
                )
        elif start_date and end_date:
            period_str = f"{start_date}..{end_date}"
            method_label = "range_arithmetic_mean"
        else:
            raise ValueError("Either 'period' or both 'start_date' and 'end_date' must be provided.")

        # Range query
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            rows = cursor.execute("""
                SELECT rate_date, rate FROM exchange_rates
                WHERE currency_pair = ? AND rate_date >= ? AND rate_date <= ?
                ORDER BY rate_date ASC
            """, (canonical_pair, start_date, end_date)).fetchall()
            
            if not rows:
                raise ValueError(
                    f"No exchange rates found for {canonical_pair} between {start_date} and {end_date}."
                )

            rates = [r[1] for r in rows]
            avg_rate = sum(rates) / len(rates)
            resolved_start = rows[0][0]
            resolved_end = rows[-1][0]
            sample_count = len(rows)

            converted_usd = round(amount / avg_rate, 2) if amount is not None else None

            return RateLookupResult(
                currency_pair=canonical_pair,
                requested_period=period_str,
                resolved_start_date=resolved_start,
                resolved_end_date=resolved_end,
                sample_count=sample_count,
                rate=avg_rate,
                resolution_method=method_label,
                input_amount=amount,
                converted_usd=converted_usd
            )
        finally:
            conn.close()

    def _lookup_exact_date(self, pair: str, date_str: str, amount: Optional[float] = None) -> RateLookupResult:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # Try exact date
            row = cursor.execute("""
                SELECT rate_date, rate FROM exchange_rates
                WHERE currency_pair = ? AND rate_date = ?
            """, (pair, date_str)).fetchone()

            if row:
                rate = row[1]
                converted_usd = round(amount / rate, 2) if amount is not None else None
                return RateLookupResult(
                    currency_pair=pair,
                    requested_period=date_str,
                    resolved_start_date=date_str,
                    resolved_end_date=date_str,
                    sample_count=1,
                    rate=rate,
                    resolution_method="exact_date",
                    effective_date=date_str,
                    input_amount=amount,
                    converted_usd=converted_usd
                )

            # Fallback to nearest prior trading day within 7 days
            target_dt = datetime.date.fromisoformat(date_str)
            min_dt = target_dt - datetime.timedelta(days=7)
            row = cursor.execute("""
                SELECT rate_date, rate FROM exchange_rates
                WHERE currency_pair = ? AND rate_date < ? AND rate_date >= ?
                ORDER BY rate_date DESC LIMIT 1
            """, (pair, date_str, min_dt.isoformat())).fetchone()

            if row:
                effective_date, rate = row[0], row[1]
                converted_usd = round(amount / rate, 2) if amount is not None else None
                return RateLookupResult(
                    currency_pair=pair,
                    requested_period=date_str,
                    resolved_start_date=effective_date,
                    resolved_end_date=effective_date,
                    sample_count=1,
                    rate=rate,
                    resolution_method="nearest_prior_trading_day",
                    effective_date=effective_date,
                    input_amount=amount,
                    converted_usd=converted_usd
                )

            raise ValueError(
                f"No rate found for {pair} on or within 7 days prior to {date_str}."
            )
        finally:
            conn.close()

    def convert(self, amount: float, pair: str, period: str) -> RateLookupResult:
        return self.lookup_rate(pair=pair, period=period, amount=amount)

    def lookup_trailing(
        self,
        pair: str,
        months: int,
        before_date: str,
        amount: Optional[float] = None,
    ) -> RateLookupResult:
        """Trailing N-calendar-month average ending on (and including) before_date -
        the project's default precision for general renovation materials/services
        pricing (per explicit user instruction, 2026-08-21): a video published on
        date X normalizes against the average rate over the N months leading up to
        X, not a calendar-year average, since the two rarely line up with when the
        price was actually current. Use months=6 or 12 per that policy; for
        individually volatile categories (e.g. appliances) use the exact-date
        lookup instead, not this trailing average."""
        end = datetime.date.fromisoformat(before_date)
        start = subtract_months(end, months)
        result = self.lookup_rate(
            pair=pair, start_date=start.isoformat(), end_date=end.isoformat(), amount=amount
        )
        result.resolution_method = f"trailing_{months}_month_arithmetic_mean"
        return result

def convert_amount(amount: float, pair: str, period: str, db_path: Path | str = DEFAULT_DB_PATH) -> RateLookupResult:
    converter = CurrencyConverter(db_path=db_path)
    return converter.convert(amount, pair, period)

def get_rate(pair: str, period: str, db_path: Path | str = DEFAULT_DB_PATH) -> RateLookupResult:
    converter = CurrencyConverter(db_path=db_path)
    return converter.lookup_rate(pair, period=period)

def convert_trailing(
    amount: float, pair: str, months: int, before_date: str, db_path: Path | str = DEFAULT_DB_PATH
) -> RateLookupResult:
    """Convenience wrapper for the trailing-N-month-average convention (see
    CurrencyConverter.lookup_trailing's docstring for the policy this backs)."""
    converter = CurrencyConverter(db_path=db_path)
    return converter.lookup_trailing(pair=pair, months=months, before_date=before_date, amount=amount)

def main() -> int:
    parser = argparse.ArgumentParser(description="Query exchange rates and convert historical amounts.")
    parser.add_argument("--pair", required=True, help="Currency pair (USD/RUB, USD/BYN)")
    parser.add_argument("--period", help="Date or interval: 'YYYY-MM-DD', 'YYYY-MM', 'YYYY', or 'YYYY-MM-DD..YYYY-MM-DD'")
    parser.add_argument("--date", help="Exact date alias (YYYY-MM-DD)")
    parser.add_argument("--from", dest="from_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--amount", type=float, help="Amount in local currency to convert to USD")
    parser.add_argument("--db-path", type=Path, default=DEFAULT_DB_PATH, help="Path to scraper.db")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    parser.add_argument(
        "--trailing-months", type=int,
        help="Trailing N-calendar-month average ending on --before (project default "
             "precision for general renovation materials/services pricing, per "
             "2026-08-21 policy - use 6 or 12; use exact-date lookup instead for "
             "individually volatile categories like appliances)",
    )
    parser.add_argument("--before", help="End date for --trailing-months (YYYY-MM-DD, usually the source's publish date)")
    args = parser.parse_args()

    period = args.period
    if args.date:
        period = args.date

    converter = CurrencyConverter(db_path=args.db_path)
    try:
        if args.trailing_months:
            if not args.before:
                raise ValueError("--trailing-months requires --before <YYYY-MM-DD>")
            res = converter.lookup_trailing(
                pair=args.pair, months=args.trailing_months, before_date=args.before, amount=args.amount
            )
        else:
            res = converter.lookup_rate(
                pair=args.pair,
                period=period,
                start_date=args.from_date,
                end_date=args.to_date,
                amount=args.amount
            )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        data = asdict(res)
        print(json.dumps(data, indent=2))
    else:
        print("=== Exchange Rate Lookup Result ===")
        print(f"Currency Pair:     {res.currency_pair}")
        print(f"Requested Period:  {res.requested_period}")
        print(f"Resolution Method: {res.resolution_method}")
        if res.effective_date:
            print(f"Effective Date:    {res.effective_date}")
        print(f"Resolved Span:     {res.resolved_start_date} .. {res.resolved_end_date} ({res.sample_count} samples)")
        print(f"Exchange Rate:     {res.rate:.4f} {res.currency_pair.split('/')[1]} per USD")
        if res.input_amount is not None:
            print(f"Input Amount:      {res.input_amount:,.2f} {res.currency_pair.split('/')[1]}")
            print(f"USD Equivalent:    ${res.converted_usd:,.2f}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
