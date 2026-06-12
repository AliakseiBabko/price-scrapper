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
  
  const models = ['eeg48300l', 'eem48300l', 'ees848200l', 'eem48320l'];
  for (const m of models) {
    console.log(`Scraping Electrolux ${m}...`);
    try {
      await scraper.scrapeSingle(m, 'dishwasher', 'Electrolux', '2021 - 2026');
      const p = db.prepare(`SELECT * FROM products WHERE id = ?`).get(`electrolux:${m}`) as any;
      if (p) {
        const specs = JSON.parse(p.specs_json);
        console.log(`Product: ${p.title}`);
        console.log(`  - Ширина: ${specs['Ширина'] || 'N/A'}`);
        console.log(`  - Тип установки: ${specs['Тип установки'] || 'N/A'}`);
        console.log(`  - Вместимость: ${specs['Вместимость'] || 'N/A'}`);
        console.log(`  - Третий короб для приборов: ${specs['Третий короб для приборов'] || specs['Третий поддон'] || 'N/A'}`);
        console.log(`  - Индикация на полу: ${specs['Индикация на полу'] || specs['Информационный сигнал'] || 'N/A'}`);
        const offers = db.prepare(`SELECT MIN(price) as min_price FROM offers WHERE product_id = ?`).get(p.id) as { min_price: number | null };
        console.log(`  - Min Price: ${offers.min_price} BYN`);
      }
    } catch (e: any) {
      console.error(`Error scraping ${m}: ${e.message}`);
    }
    console.log('--------------------------------------------------');
  }
  
  await browser.close();
}

main().catch(console.error);
