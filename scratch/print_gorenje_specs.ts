import { initDb, db } from '../src/database/db.js';

async function main() {
  initDb();
  const items = db.prepare(`SELECT id, title, specs_json FROM products WHERE brand = 'Gorenje' AND category_id = 'hob_cooker'`).all() as any[];
  for (const item of items) {
    console.log(`\n==================================================`);
    console.log(`Product: ${item.title} (${item.id})`);
    const specs = JSON.parse(item.specs_json);
    for (const [k, v] of Object.entries(specs)) {
      console.log(`  - ${k}: ${v}`);
    }
  }
}

main().catch(console.error);
