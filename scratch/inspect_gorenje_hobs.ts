import { chromium } from 'playwright';
import { OnlinerScraper } from '../src/scraper/onliner.js';
import { initDb, db, getProductColor } from '../src/database/db.js';

async function main() {
  initDb();
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://catalog.onliner.by', { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 2000));
  
  const scraper = new OnlinerScraper();
  
  const hobsToScrape = [
    { key: 'goregi6401bsc', brand: 'Gorenje' },
    { key: 'goreisc645bsc', brand: 'Gorenje' },
    { key: 'gi6401bce', brand: 'Gorenje' }
  ];

  for (const hob of hobsToScrape) {
    console.log(`Scraping ${hob.brand} ${hob.key}...`);
    try {
      await scraper.scrapeSingle(hob.key, 'hob_cooker', hob.brand, '2021 - 2025');
      const product = db.prepare(`SELECT * FROM products WHERE id = ?`).get(`${hob.brand.toLowerCase()}:${hob.key}`) as any;
      if (product) {
        console.log(`Product: ${product.title}`);
        console.log(`Specs parsed color: ${getProductColor(product.specs_json)}`);
        const specs = JSON.parse(product.specs_json);
        console.log(`Specs detail:`);
        console.log(`  - Тип варочной панели: ${specs['Тип варочной панели']}`);
        console.log(`  - Материал панели: ${specs['Материал панели']}`);
        console.log(`  - Управление: ${specs['Управление']}`);
        console.log(`  - Рамка панели: ${specs['Рамка панели'] || specs['Тип краев панели'] || 'N/A'}`);
        console.log(`  - Цвет: ${specs['Цвет'] || 'N/A'}`);
      }
    } catch (e: any) {
      console.error(`Error scraping ${hob.key}: ${e.message}`);
    }
    console.log('--------------------------------------------------');
  }
  
  await browser.close();
}

main().catch(console.error);
