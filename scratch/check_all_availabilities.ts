import { initDb, db } from '../src/database/db.js';

async function main() {
  initDb();
  
  const products = db.prepare(`SELECT id, brand, model, title FROM products`).all() as any[];
  
  console.log("Checking availability (offers count) for all products in database:");
  console.log("----------------------------------------------------------------------");
  for (const p of products) {
    const offers = db.prepare(`SELECT COUNT(*) as cnt FROM offers WHERE product_id = ?`).get(p.id) as { cnt: number };
    const bestPrice = db.prepare(`SELECT MIN(price) as min_price FROM offers WHERE product_id = ?`).get(p.id) as { min_price: number | null };
    
    console.log(`- Product: [${p.brand}] ${p.model} (${p.title})`);
    console.log(`  ID:      ${p.id}`);
    console.log(`  Offers:  ${offers.cnt}`);
    console.log(`  Min Price: ${bestPrice.min_price ? bestPrice.min_price + ' BYN' : 'N/A'}`);
    console.log("----------------------------------------------------------------------");
  }
}

main().catch(console.error);
