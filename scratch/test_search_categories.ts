import { chromium } from 'playwright';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto("https://catalog.onliner.by", { waitUntil: 'domcontentloaded' });
  await new Promise(resolve => setTimeout(resolve, 2000));

  const testCats = [
    'microwave',
    'microwaveoven',
    'dishwasher',
    'dishwashingmachine',
    'washingmachine',
    'washing_machine',
    'dryer',
    'rangehood',
    'range_hood'
  ];

  for (const cat of testCats) {
    const url = `https://catalog.onliner.by/sdapi/catalog.api/search/${cat}?query=bosch`;
    try {
      const res = await page.evaluate(async (u) => {
        try {
          const r = await fetch(u);
          return { ok: r.ok, status: r.status };
        } catch (e: any) {
          return { ok: false, status: 0, error: e.message };
        }
      }, url);
      console.log(`Category: "${cat}" -> OK: ${res.ok}, Status: ${res.status}`);
    } catch (e: any) {
      console.log(`Category: "${cat}" error: ${e.message}`);
    }
  }

  await browser.close();
}

main().catch(console.error);
