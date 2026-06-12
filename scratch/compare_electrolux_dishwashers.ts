import { initDb, db } from '../src/database/db.js';

async function main() {
  initDb();
  
  // We need to make sure EEM48321L and EEM48221L are scraped so they are in the DB.
  // We will run a scrape for EEM48321L and EEM48221L if they aren't already.
  // Wait, let's just query if they are there, and if not, we will log what is in DB.
  
  const models = ['ees848200l', 'eem48321l', 'eem48221l'];
  for (const m of models) {
    const p = db.prepare(`SELECT * FROM products WHERE id = ?`).get(`electrolux:${m}`) as any;
    if (p) {
      console.log(`\n==================================================`);
      console.log(`Product: ${p.title} (${p.id})`);
      const specs = JSON.parse(p.specs_json);
      for (const [k, v] of Object.entries(specs)) {
        if (k.includes('сушки') || k.includes('Индикация') || k.includes('посуды') || k.includes('программ') || k.includes('короб') || k.includes('Сушка') || k.includes('Дополнительн') || k.includes('Особенности')) {
          console.log(`  - ${k}: ${v}`);
        }
      }
      const offers = db.prepare(`SELECT MIN(price) as min_price FROM offers WHERE product_id = ?`).get(p.id) as { min_price: number | null };
      console.log(`  - Min Price: ${offers.min_price} BYN`);
    } else {
      console.log(`Product electrolux:${m} not found in DB.`);
    }
  }
}

main().catch(console.error);
