import { chromium } from 'playwright';
import { OnlinerScraper } from './src/scraper/onliner.js';
import { initDb } from './src/database/db.js';

(async () => {
  initDb();
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://catalog.onliner.by', { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 2000));
  const scraper = new OnlinerScraper();
  await scraper.scrapeSingle('bhi626e6b', 'hood', 'Gorenje', '2020 - 2025');
  await browser.close();
  console.log('Done');
})().catch(console.error);
