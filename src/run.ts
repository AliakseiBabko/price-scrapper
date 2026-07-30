import { initDb, db } from './database/db.js';
import { OnlinerScraper } from './scraper/onliner.js';
import { HlzScraper } from './scraper/hlz.js';
import { MlSmartScraper } from './scraper/mlsmart.js';
import { ZukerScraper } from './scraper/zuker.js';
import { CsScraper } from './scraper/cs.js';
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
      
      const firstEqIndex = arg.indexOf('=');
      if (firstEqIndex !== -1) {
        const val = arg.substring(firstEqIndex + 1);
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
  const category = options.category || (site === 'zuker' ? 'quartz_stone' : (site === 'onliner' ? 'oven_cooker' : (site === 'cs' ? 'compact_hpl' : 'ldsp')));
  const limit = options.limit ? parseInt(options.limit, 10) : 1000;
  const filterStr = options.filter || '';

  // 1. Initialize SQLite Database
  console.log("Initializing local SQLite database...");
  initDb();

  // 2. Check freshness in SQLite database
  const forceUpdate = options.force === 'true' || options.force === '1';
  try {
    const row = db.prepare(`
      SELECT last_updated 
      FROM offers 
      WHERE source = ? AND product_id IN (SELECT id FROM products WHERE category_id = ?)
      LIMIT 1
    `).get(site, category) as { last_updated: string } | undefined;

    if (row) {
      const lastUpdated = new Date(row.last_updated.replace(' ', 'T') + 'Z');
      const now = new Date();
      const diffTime = Math.abs(now.getTime() - lastUpdated.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays <= 7 && !forceUpdate) {
        console.log(`\n🎉 Data for site '${site}' and category '${category}' is fresh (last updated ${diffDays} days ago).`);
        console.log(`Skipping network scrape to save traffic and time. Use --force=true to override.`);
        
        const dbProducts = db.prepare(`SELECT * FROM products WHERE category_id = ?`).all(category) as any[];
        const dbOffers = db.prepare(`
          SELECT o.* FROM offers o
          JOIN products p ON o.product_id = p.id
          WHERE o.source = ? AND p.category_id = ?
        `).all(site, category) as any[];

        console.log("\n==================================================");
        console.log("             CRAWL RUN SUMMARY (CACHED)           ");
        console.log("==================================================");
        console.log(`Source marketplace:   ${site}`);
        console.log(`Category:             ${category}`);
        console.log(`Products in DB:       ${dbProducts.length}`);
        console.log(`Offers in DB:         ${dbOffers.length}`);
        console.log("==================================================\n");
        return;
      }
    }
  } catch (e: any) {
    console.warn(`Could not verify data freshness: ${e.message}. Proceeding with crawl.`);
  }

  // 3. Parse filters from query string format (e.g., brand[]=bosch&price[from]=2100)
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

  // 4. Select and execute scraper
  let scraper;
  if (site === 'onliner') {
    scraper = new OnlinerScraper();
  } else if (site === 'hlz') {
    scraper = new HlzScraper();
  } else if (site === 'mlsmart') {
    scraper = new MlSmartScraper();
  } else if (site === 'zuker') {
    scraper = new ZukerScraper();
  } else if (site === 'cs') {
    scraper = new CsScraper();
  } else {
    console.error(`Error: Unsupported site '${site}'. Supported: 'onliner', 'hlz', 'mlsmart', 'zuker', 'cs'.`);
    process.exit(1);
  }

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
}

main().catch(console.error);
