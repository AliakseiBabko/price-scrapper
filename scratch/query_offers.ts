import { initDb, db } from '../src/database/db.js';

async function main() {
  initDb();
  const hobs = ['gorenje:goregi6401bsc', 'gorenje:goreisc645bsc', 'gorenje:gi6401bce'];
  for (const id of hobs) {
    const offers = db.prepare('SELECT reseller_name, price FROM offers WHERE product_id = ? ORDER BY price ASC LIMIT 3').all(id) as any[];
    console.log(`\nOffers for ${id}:`);
    for (const o of offers) {
      console.log(`  - ${o.reseller_name}: ${o.price} BYN`);
    }
  }
}

main().catch(console.error);
