"""Read-only export of design product IDs against the existing SQLite price DB."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--database", type=Path, default=Path("data/scraper.db"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    design = json.loads(args.design.read_text(encoding="utf-8"))
    items = design.get("procurement_items", [])
    ids = [item["product_id"] for item in items if item.get("product_id")]
    result = {"database": str(args.database), "read_only": True, "items": []}
    with sqlite3.connect(args.database) as db:
        db.row_factory = sqlite3.Row
        for item in items:
            product_id = item.get("product_id")
            row = db.execute("SELECT id, brand, model, title, last_updated FROM products WHERE id = ?", (product_id,)).fetchone() if product_id else None
            offers = []
            if row:
                offers = [dict(offer) for offer in db.execute("SELECT source, reseller_name, reseller_url, price, price_unit, availability, last_updated FROM offers WHERE product_id = ? ORDER BY price ASC", (product_id,))]
            result["items"].append({"design_item_id": item.get("item_id"), "product_id": product_id, "quantity": item.get("quantity"), "unit": item.get("unit"), "product": dict(row) if row else None, "offers": offers, "status": "matched" if row else "unmatched"})
    result["summary"] = {"requested": len(ids), "matched": sum(item["status"] == "matched" for item in result["items"]), "unmatched": sum(item["status"] == "unmatched" for item in result["items"])}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote read-only price export: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
