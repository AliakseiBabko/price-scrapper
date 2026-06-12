import { initDb, db } from '../src/database/db.js';

async function main() {
  initDb();
  const product = db.prepare(`SELECT * FROM products WHERE id = ?`).get('electrolux:lfp326fb') as any;
  if (product) {
    console.log(`Title: ${product.title}`);
    console.log(`Specs:`);
    const specs = JSON.parse(product.specs_json);
    for (const [k, v] of Object.entries(specs)) {
      console.log(`  - ${k}: ${v}`);
    }
    
    const offers = db.prepare(`SELECT reseller_name, price FROM offers WHERE product_id = ? ORDER BY price ASC LIMIT 5`).all('electrolux:lfp326fb') as any[];
    console.log(`\nOffers:`);
    for (const o of offers) {
      console.log(`  - ${o.reseller_name}: ${o.price} BYN`);
    }
  } else {
    console.log("Product not found in DB.");
  }
}

main().catch(console.error);
