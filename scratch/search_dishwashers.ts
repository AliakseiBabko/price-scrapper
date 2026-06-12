import { chromium } from 'playwright';
import { OnlinerScraper } from '../src/scraper/onliner.js';
import { initDb, db } from '../src/database/db.js';

async function main() {
  initDb();
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://catalog.onliner.by', { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 2000));
  
  const scraper = new OnlinerScraper();
  
  // 1. Scrape Gorenje GV643D90
  console.log("Scraping Gorenje GV643D90...");
  try {
    const result = await scraper.scrapeSingle('gv643d90', 'dishwasher', 'Gorenje', '2022 - 2026');
    const p = db.prepare(`SELECT * FROM products WHERE id = 'gorenje:gv643d90'`).get() as any;
    if (p) {
      const offers = db.prepare(`SELECT MIN(price) as min_price FROM offers WHERE product_id = ?`).get(p.id) as { min_price: number | null };
      console.log(`Successfully scraped GV643D90!`);
      console.log(`Title: ${p.title}`);
      console.log(`Min Price: ${offers.min_price ? offers.min_price + ' BYN' : 'N/A'}`);
      console.log(`Offers: ${db.prepare(`SELECT COUNT(*) as cnt FROM offers WHERE product_id = ?`).get(p.id).cnt}`);
      
      const specs = JSON.parse(p.specs_json);
      console.log(`Specs:`);
      console.log(`  - Индикация на полу: ${specs['Индикация на полу'] || specs['Информационный сигнал'] || 'N/A'}`);
      console.log(`  - Класс сушки: ${specs['Класс сушки'] || 'N/A'}`);
      console.log(`  - Количество программ: ${specs['Количество программ'] || 'N/A'}`);
    }
  } catch (e: any) {
    console.error(`Error scraping GV643D90: ${e.message}`);
  }
  
  console.log('\n==================================================\n');
  
  // 2. Search for Electrolux dishwashers currently in stock (width 60cm, fully integrated)
  console.log("Searching for Electrolux dishwashers on page 1...");
  const searchUrl = `https://catalog.onliner.by/sdapi/catalog.api/search/dishwasher?mfr[0]=electrolux&page=1`;
  try {
    const data = await page.evaluate(async (u) => {
      const r = await fetch(u);
      return r.ok ? await r.json() : null;
    }, searchUrl);
    
    if (data && data.products) {
      console.log(`Found ${data.products.length} Electrolux dishwashers:`);
      for (const p of data.products) {
        console.log(`- Title: "${p.full_name}"`);
        console.log(`  Key:   "${p.key}"`);
        console.log(`  Price: Min=${p.prices?.price_min?.amount || 'N/A'}, Max=${p.prices?.price_max?.amount || 'N/A'}`);
        console.log(`  Offers count: ${p.prices?.offers?.count || 0}`);
        console.log(`  Description: ${p.micro_description || 'N/A'}`);
        console.log('--------------------------------------------------');
      }
    } else {
      console.log("No Electrolux dishwashers found.");
    }
  } catch (e: any) {
    console.error(`Error searching Electrolux dishwashers: ${e.message}`);
  }

  await browser.close();
}

main().catch(console.error);
