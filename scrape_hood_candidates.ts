import { chromium } from 'playwright';
import { initDb } from './src/database/db.js';
import { OnlinerScraper } from './src/scraper/onliner.js';
import fs from 'fs';

interface ProductEntry {
  key: string;
  brand: string;
  brandKey: string;
  name: string;
  priceMin?: number;
}

(async () => {
  initDb();

  const candidates: ProductEntry[] = JSON.parse(fs.readFileSync('./scratch/hood_candidates.json', 'utf-8'));
  console.log(`Loaded ${candidates.length} hood candidates. Starting full detail scrape...`);

  const scraper = new OnlinerScraper();

  for (let i = 0; i < candidates.length; i++) {
    const c = candidates[i];
    console.log(`\n[${i + 1}/${candidates.length}] Scraping: ${c.name} (key: ${c.key}, brand: ${c.brand})`);
    try {
      await scraper.scrapeSingle(c.key, 'hoods', c.brand);
      console.log(`  ✅ Done`);
    } catch (e: any) {
      console.warn(`  ❌ Failed: ${e.message}`);
    }
  }

  console.log('\n✅ All candidates scraped and saved to DB.');
})().catch(console.error);
