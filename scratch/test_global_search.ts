import { chromium } from 'playwright';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto("https://catalog.onliner.by", { waitUntil: 'domcontentloaded' });
  await new Promise(resolve => setTimeout(resolve, 2000));

  const testUrls = [
    'https://catalog.onliner.by/sdapi/catalog.api/search/oven?query=bosch',
    'https://catalog.onliner.by/sdapi/catalog.api/search/oven_cooker?query=bosch'
  ];

  for (const url of testUrls) {
    try {
      const res = await page.evaluate(async (u) => {
        try {
          const r = await fetch(u);
          const data = r.ok ? await r.json() : null;
          return { ok: r.ok, status: r.status, count: data?.products?.length || 0, first: data?.products?.[0]?.full_name || 'none' };
        } catch (e: any) {
          return { ok: false, status: 0, error: e.message };
        }
      }, url);
      
      console.log(`URL: ${url}`);
      console.log(`  OK: ${res.ok}, Status: ${res.status}, Count: ${res.count}, First: "${res.first}"`);
    } catch (e: any) {
      console.log(`  Error: ${e.message}`);
    }
  }

  await browser.close();
}

main().catch(console.error);
