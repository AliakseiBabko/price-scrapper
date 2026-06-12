import { chromium } from 'playwright';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto("https://catalog.onliner.by", { waitUntil: 'domcontentloaded' });
  await new Promise(resolve => setTimeout(resolve, 2000));

  const url = `https://catalog.onliner.by/sdapi/catalog.api/search/products?query=BFL7221B1`;
  
  try {
    const data = await page.evaluate(async (u) => {
      const r = await fetch(u);
      return r.ok ? await r.json() : null;
    }, url);
    
    console.log(JSON.stringify(data, null, 2).substring(0, 1500));
  } catch (e: any) {
    console.log(`Error: ${e.message}`);
  }

  await browser.close();
}

main().catch(console.error);
