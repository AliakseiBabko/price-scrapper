import { chromium } from 'playwright';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto("https://catalog.onliner.by", { waitUntil: 'domcontentloaded' });
  await new Promise(resolve => setTimeout(resolve, 2000));

  const testCategories = ['oven', 'oven_cooker', 'microwave', 'microwaveoven'];
  const query = 'HBG7764B1';

  for (const cat of testCategories) {
    const url = `https://catalog.onliner.by/sdapi/catalog.api/search/${cat}?query=${query}`;
    try {
      const data = await page.evaluate(async (u) => {
        const r = await fetch(u);
        return r.ok ? await r.json() : null;
      }, url);
      
      if (data && data.products && data.products.length > 0) {
        console.log(`Category: "${cat}" returned ${data.products.length} products. First product: "${data.products[0].full_name}" (key: ${data.products[0].key})`);
      } else {
        console.log(`Category: "${cat}" returned 0 products.`);
      }
    } catch (e: any) {
      console.log(`Category: "${cat}" error: ${e.message}`);
    }
  }

  await browser.close();
}

main().catch(console.error);
