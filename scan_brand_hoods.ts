import { chromium } from 'playwright';
import { initDb } from './src/database/db.js';
import { OnlinerScraper } from './src/scraper/onliner.js';
import fs from 'fs';

// Scan all Onliner hood pages and collect Bosch, Electrolux, Gorenje entries
const TARGET_BRANDS = ['bosch', 'electrolux', 'gorenje'];
const CATEGORY = 'hoods';
const PAGES_TO_SCAN = 15; // 30 products/page → covers ~450 products

interface ProductEntry {
  key: string;
  brand: string;
  brandKey: string;
  name: string;
  priceMin?: number;
}

(async () => {
  initDb();

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    viewport: { width: 1920, height: 1080 },
    locale: 'ru-RU'
  });
  const page = await context.newPage();

  await page.goto(`https://catalog.onliner.by/${CATEGORY}`, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 2000));

  const found: ProductEntry[] = [];
  console.log(`Scanning pages of hoods to find Bosch, Electrolux, Gorenje models...`);

  for (let p = 1; p <= PAGES_TO_SCAN; p++) {
    const url = `https://catalog.onliner.by/sdapi/catalog.api/search/${CATEGORY}?page=${p}`;
    const data = await page.evaluate(async (u) => {
      const r = await fetch(u, { headers: { Accept: 'application/json' } });
      return await r.json();
    }, url);

    if (!data.products || data.products.length === 0) {
      console.log(`No products on page ${p}, stopping.`);
      break;
    }

    for (const item of data.products) {
      const brandKey = (item.manufacturer?.key || '').toLowerCase();
      const brandName = (item.manufacturer?.name || '').toLowerCase();
      if (TARGET_BRANDS.some(b => brandKey.includes(b) || brandName.includes(b))) {
        const entry: ProductEntry = {
          key: item.key,
          brand: item.manufacturer?.name || brandKey,
          brandKey: brandKey,
          name: item.full_name,
          priceMin: item.prices?.price_min?.amount ? Number(item.prices.price_min.amount) : undefined
        };
        // Skip duplicates
        if (!found.find(f => f.key === entry.key)) {
          found.push(entry);
          console.log(`  [${entry.brand}] ${entry.name} (${entry.key}) @ ${entry.priceMin ?? 'N/A'} BYN`);
        }
      }
    }

    const lastPage = data.page?.last ?? 1;
    if (p >= lastPage) {
      console.log(`Reached last page (${lastPage}).`);
      break;
    }

    await new Promise(r => setTimeout(r, 600));
  }

  await browser.close();

  console.log(`\n=== SUMMARY ===`);
  console.log(`Discovered ${found.length} target brand hoods total.`);
  for (const brand of TARGET_BRANDS) {
    const items = found.filter(f => f.brandKey.includes(brand));
    console.log(`\n${brand.toUpperCase()}: ${items.length} models`);
    for (const item of items) {
      console.log(`  - ${item.name} (${item.key}) @ ${item.priceMin ?? 'N/A'} BYN`);
    }
  }

  fs.writeFileSync('./scratch/hood_candidates.json', JSON.stringify(found, null, 2));
  console.log('\nSaved to scratch/hood_candidates.json');
})().catch(console.error);
