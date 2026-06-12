import { initDb } from './database/db.js';
import { OnlinerScraper } from './scraper/onliner.js';
import { chromium } from 'playwright';

const appliances = [
  // Kitchen Set 1 (Premium)
  { model: "HBG7764B1", brand: "Bosch", releaseYear: "2023 - 2026" },
  { model: "BFL7221B1", brand: "Bosch", releaseYear: "2024 - 2026" },
  { model: "PIF63KHC1E", brand: "Bosch", releaseYear: "2023 - 2026" },
  { model: "SMV8YCX02E", brand: "Bosch", releaseYear: "2023 - 2026" },
  { model: "DHL555BL", brand: "Bosch", releaseYear: "2015 - 2026" },

  // Kitchen Set 2 (Balanced)
  { model: "HBG578EB3", brand: "Bosch", releaseYear: "2020 - 2024" },
  { model: "BFL524MB0", brand: "Bosch", releaseYear: "2020 - 2024" },
  { model: "PIE631HB1E", brand: "Bosch", releaseYear: "2023 - 2026" },
  { model: "SMV4EVX00E", brand: "Bosch", releaseYear: "2023 - 2026" },

  // Kitchen Set 3 (Gorenje Manual)
  { model: "BPSA6747A08BG", brand: "Gorenje", releaseYear: "2021 - 2025" },
  { model: "BM251M2BG", brand: "Gorenje", releaseYear: "2021 - 2025" },
  { model: "GI6401BSC", brand: "Gorenje", releaseYear: "2021 - 2025" },
  { model: "GV643D90", brand: "Gorenje", releaseYear: "2022 - 2025" },
  { model: "BHI626E6B", brand: "Gorenje", releaseYear: "2020 - 2025" },

  // Kitchen Set 4 (Electrolux Touch)
  { model: "EOE7P31Z", brand: "Electrolux", releaseYear: "2021 - 2025" },
  { model: "LMS4253TMK", brand: "Electrolux", releaseYear: "2021 - 2025" },
  { model: "EEM48321L", brand: "Electrolux", releaseYear: "2021 - 2025" },
  { model: "LFP326FB", brand: "Electrolux", releaseYear: "2021 - 2025" },

  // Laundry Set 1 (LG V9)
  { model: "F4V9LA2W", brand: "LG", releaseYear: "2019 - 2024" },
  { model: "DC10V9V9E", brand: "LG", releaseYear: "2024 - 2026" },

  // Laundry Set 2 (Samsung Bespoke)
  { model: "WW11CB944CGHLP", brand: "Samsung", releaseYear: "2023 - 2026" },
  { model: "DV90BB9445GHLP", brand: "Samsung", releaseYear: "2023 - 2026" },

  // Laundry Set 3 (Bosch ME)
  { model: "WGB244040", brand: "Bosch", releaseYear: "2023 - 2026" },
  { model: "WQB245B0ME", brand: "Bosch", releaseYear: "2023 - 2026" },

  // Laundry Set 4 (Bosch Premium)
  { model: "WGB244A40", brand: "Bosch", releaseYear: "2023 - 2026" },
  { model: "WQB245B40", brand: "Bosch", releaseYear: "2023 - 2026" }
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
        await scraper.scrapeSingle(product.key, categoryId, item.brand, (item as any).releaseYear);
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
