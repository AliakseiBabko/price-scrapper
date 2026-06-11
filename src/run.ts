import { initDb } from './database/db.js';
import { OnlinerScraper } from './scraper/onliner.js';
import { ScraperFilters } from './scraper/base.js';

function parseArgs() {
  const args = process.argv.slice(2);
  const parsed: Record<string, string> = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const parts = arg.split('=');
      const key = parts[0].replace('--', '');
      let value = parts[1];
      
      // Handle cases like --filter "a=b&c=d" (where value might not have '=' in arg.split if there's no = in value, but there is)
      // Actually, if we pass --filter="a=b&c=d", split('=') splits on all '=', so parts would be ['--filter', 'a', 'b&c', 'd'].
      // To prevent this, let's join back everything after the first split, or split once.
      const firstEqIndex = arg.indexOf('=');
      if (firstEqIndex !== -1) {
        const val = arg.substring(firstEqIndex + 1);
        // Strip outer quotes if any
        parsed[key] = val.replace(/^['"]|['"]$/g, '');
      } else {
        parsed[key] = 'true';
      }
    }
  }

  return parsed;
}

async function main() {
  const options = parseArgs();

  const site = options.site || 'onliner';
  const category = options.category || 'oven_cooker';
  const limit = options.limit ? parseInt(options.limit, 10) : 10;
  const filterStr = options.filter || '';

  // 1. Initialize SQLite Database
  console.log("Initializing local SQLite database...");
  initDb();

  // 2. Parse filters from query string format (e.g., brand[]=bosch&price[from]=2100)
  const filters: ScraperFilters = {};
  if (filterStr) {
    const searchParams = new URLSearchParams(filterStr);
    for (const [key, val] of searchParams.entries()) {
      if (filters[key]) {
        if (Array.isArray(filters[key])) {
          (filters[key] as string[]).push(val);
        } else {
          filters[key] = [filters[key] as string, val];
        }
      } else {
        filters[key] = val;
      }
    }
  }

  // 3. Select and execute scraper
  if (site === 'onliner') {
    const scraper = new OnlinerScraper();
    try {
      const result = await scraper.scrape({
        category,
        limit,
        filters
      });

      console.log("\n==================================================");
      console.log("             CRAWL RUN SUMMARY                    ");
      console.log("==================================================");
      console.log(`Source marketplace:   ${site}`);
      console.log(`Category:             ${result.category.name} (${result.category.id})`);
      console.log(`Products Ingested:    ${result.products.length}`);
      console.log(`Offers Stored:        ${result.offers.length}`);
      console.log(`Reviews Collected:    ${result.reviews.length}`);
      console.log("==================================================\n");

    } catch (error: any) {
      console.error(`Scraping failed: ${error.message}`);
      process.exit(1);
    }
  } else {
    console.error(`Error: Unsupported site '${site}'. Currently only 'onliner' is supported.`);
    process.exit(1);
  }
}

main().catch(console.error);
