import { initDb } from './database/db.js';
import { OnlinerScraper } from './scraper/onliner.js';
import { chromium } from 'playwright';

const appliances = [
  // Kitchen Set 1 (Premium)
  { model: "HBG7764B1", brand: "Bosch" },
  { model: "BFL7221B1", brand: "Bosch" },
  { model: "PIF63KHC1E", brand: "Bosch" },
  { model: "SMV8YCX02E", brand: "Bosch" },
  { model: "DHL555BL", brand: "Bosch" },

  // Kitchen Set 2 (Balanced)
  { model: "HBG578EB3", brand: "Bosch" },
  { model: "BFL524MS0", brand: "Bosch" },
  { model: "PIE631HB1E", brand: "Bosch" },
  { model: "SMV6ECX08E", brand: "Bosch" },

  // Kitchen Set 3 (Economy)
  { model: "BPSA6747A08BG", brand: "Gorenje" },
  { model: "BM201AG1BG", brand: "Gorenje" },
  { model: "EIT61443B", brand: "Electrolux" },
  { model: "GV643E90", brand: "Gorenje" },
  { model: "Crosby Singolo 60", brand: "MAUNFELD" },

  // Laundry Set 1 (LG V9)
  { model: "F4V9LA2W", brand: "LG" },
  { model: "DC90V9V9WN", brand: "LG" },

  // Laundry Set 2 (Samsung Bespoke)
  { model: "WW11CB944CGHLP", brand: "Samsung" },
  { model: "DV90BB9445GHLP", brand: "Samsung" },

  // Laundry Set 3 (Bosch ME)
  { model: "WGB244040", brand: "Bosch" },
  { model: "WQB245B0ME", brand: "Bosch" },

  // Laundry Set 4 (Bosch Premium)
  { model: "WGB244A40", brand: "Bosch" },
  { model: "WQB245B40", brand: "Bosch" }
];

async function main() {
  initDb();
  console.log("Starting automated search and ingestion for all appliances...");

  console.log("Launching Chromium for searching...");
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log("Navigating to establish catalog origin context...");
  await page.goto("https://catalog.onliner.by", { waitUntil: 'domcontentloaded' });
  await new Promise(resolve => setTimeout(resolve, 2000));

  const scraper = new OnlinerScraper();

  for (let i = 0; i < appliances.length; i++) {
    const item = appliances[i];
    console.log(`\n[${i + 1}/${appliances.length}] Searching for ${item.brand} ${item.model}...`);

    const searchUrl = `https://catalog.onliner.by/sdapi/catalog.api/search/products?query=${encodeURIComponent(item.model)}`;
    
    try {
      const searchData = await page.evaluate(async (url) => {
        const resp = await fetch(url);
        if (!resp.ok) return { products: [] };
        return await resp.json();
      }, searchUrl);

      if (searchData.products && searchData.products.length > 0) {
        // Find product that best matches our model query in name or key
        const modelQuery = item.model.toLowerCase().replace(/[^a-z0-9]/g, '');
        let product = searchData.products.find((p: any) => {
          const nameClean = p.name.toLowerCase().replace(/[^a-z0-9]/g, '');
          const keyClean = p.key.toLowerCase().replace(/[^a-z0-9]/g, '');
          return nameClean.includes(modelQuery) || keyClean.includes(modelQuery);
        });

        // Fallback to first search result if no strict name match
        if (!product) {
          product = searchData.products[0];
        }

        const categoryId = product.schema.key;
        console.log(`  Found product: "${product.full_name}" with key "${product.key}" under category "${categoryId}"`);
        
        // Scraping the details and saving to DB + downloading image
        await scraper.scrapeSingle(product.key, categoryId, item.brand);
        console.log(`  Successfully ingested ${item.brand} ${item.model}`);
      } else {
        console.warn(`  ⚠️ No product found on Onliner for query "${item.model}"`);
      }
    } catch (err: any) {
      console.error(`  ❌ Failed to search or ingest ${item.brand} ${item.model}: ${err.message}`);
    }

    // Small delay between searches to be polite
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  await browser.close();
  console.log("\nAutomated Ingestion Complete!");
}

main().catch(console.error);
