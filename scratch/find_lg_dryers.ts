import { chromium } from 'playwright';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto("https://catalog.onliner.by", { waitUntil: 'domcontentloaded' });
  await new Promise(resolve => setTimeout(resolve, 2000));

  // Search in washingmachine category with manufacturer LG and query "DC9" or "dryer"
  const url = `https://catalog.onliner.by/sdapi/catalog.api/search/washingmachine?mfr[0]=lg&page=1`;
  
  try {
    const data = await page.evaluate(async (u) => {
      const r = await fetch(u);
      return r.ok ? await r.json() : null;
    }, url);
    
    if (data && data.products) {
      console.log(`Found ${data.products.length} LG washing machines/dryers on page 1:`);
      for (const p of data.products) {
        // filter for dryers (usually model starts with DC or contains "сушильная")
        if (p.full_name.toLowerCase().includes('сушильная') || p.key.toLowerCase().startsWith('dc')) {
          console.log(`- Title: "${p.full_name}"`);
          console.log(`  Key:   "${p.key}"`);
          console.log(`  Price: Min=${p.prices?.price_min?.amount || 'N/A'}, Max=${p.prices?.price_max?.amount || 'N/A'}`);
          console.log(`  Offers count: ${p.prices?.offers?.count || 0}`);
          console.log('--------------------------------------------------');
        }
      }
    } else {
      console.log("No data");
    }
  } catch (e: any) {
    console.log(`Error: ${e.message}`);
  }

  await browser.close();
}

main().catch(console.error);
