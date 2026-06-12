import { initDb, db, getProductFreshness, getProductColor } from './database/db.js';
import { OnlinerScraper } from './scraper/onliner.js';

function parseArgs() {
  const args = process.argv.slice(2);
  const parsed: Record<string, string> = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const parts = arg.split('=');
      const key = parts[0].replace('--', '');
      const val = parts[1] ? parts[1].replace(/^['"]|['"]$/g, '') : 'true';
      parsed[key] = val;
    }
  }
  return parsed;
}

async function main() {
  initDb();
  const options = parseArgs();

  if (options.product) {
    const productId = options.product;
    console.log(`Querying product details for ID: ${productId}...`);

    let freshness = getProductFreshness(productId);

    if (!freshness.exists) {
      console.log(`Product ${productId} does not exist in the database. Checking if we can scrape it...`);
      // Since it doesn't exist, we must know its key, category, and brand to scrape it.
      // E.g., if we query like --product=siemens:ex675lxc1e, we can extract details from the ID.
      const parts = productId.split(':');
      if (parts.length === 2) {
        const brand = parts[0];
        const key = parts[1];
        // Guess category (can pass --category, defaults to hob_cooker)
        const categoryId = options.category || 'hob_cooker';
        
        console.log(`Attempting to scrape single product: brand=${brand}, key=${key}, category=${categoryId}...`);
        const scraper = new OnlinerScraper();
        await scraper.scrapeSingle(key, categoryId, brand);
        freshness = getProductFreshness(productId);
      } else {
        console.error("Error: To scrape a new product, specify ID in format 'brand:key' (e.g. siemens:ex675lxc1e)");
        process.exit(1);
      }
    } else if (!freshness.isFresh) {
      console.log(`Product data is stale (older than 7 days). Refreshing from Onliner...`);
      const scraper = new OnlinerScraper();
      if (freshness.storeKey && freshness.categoryId && freshness.brand) {
        await scraper.scrapeSingle(freshness.storeKey, freshness.categoryId, freshness.brand);
      }
    } else {
      console.log("Product data is fresh (updated within 7 days).");
    }

    // Query product from DB
    const product = db.prepare(`SELECT * FROM products WHERE id = ?`).get(productId) as any;
    if (!product) {
      console.error(`Product ${productId} still not found in database after update attempt.`);
      process.exit(1);
    }

    console.log(`\n==================================================`);
    console.log(`Title:       ${product.title}`);
    console.log(`Brand:       ${product.brand}`);
    console.log(`Model:       ${product.model}`);
    console.log(`Color:       ${getProductColor(product.specs_json)}`);
    console.log(`Rating:      ${product.rating} ★ (${product.reviews_count} reviews)`);
    console.log(`Updated:     ${product.last_updated}`);
    console.log(`==================================================`);

    // Query reseller offers
    const offers = db.prepare(`
      SELECT * FROM offers 
      WHERE product_id = ? 
      ORDER BY price ASC
    `).all(productId) as any[];

    console.log(`\nReseller Offers:`);
    console.log(`----------------------------------------------------------------------------------------------------`);
    console.log(`%-25s | %-8s | %-8s | %-12s | %s`.replace(/%/g, '%-'), 'Reseller', 'Price', 'Rating', 'Reviews', 'URL');
    console.log(`----------------------------------------------------------------------------------------------------`);
    for (const off of offers) {
      const priceStr = off.price ? `${off.price.toFixed(2)} BYN` : 'N/A';
      const ratingStr = off.reseller_rating ? `${off.reseller_rating} ★` : 'N/A';
      console.log(
        `%-25s | %-8s | %-8s | %-12s | %s`,
        off.reseller_name.substring(0, 25),
        priceStr,
        ratingStr,
        off.reseller_reviews_count,
        off.reseller_url
      );
    }

    // Query reliable offers
    const reliable = offers.filter(o => o.reseller_rating >= 4.0 && o.reseller_reviews_count >= 1000);
    console.log(`\nReliability Check:`);
    if (reliable.length > 0) {
      console.log(`Lowest reliable price: ${reliable[0].price.toFixed(2)} BYN from ${reliable[0].reseller_name}`);
    } else {
      console.log(`⚠️ No reliable sellers found (rating >= 4.0 and reviews >= 1000) for this product!`);
    }

  } else if (options['color-match']) {
    const targetColor = options.color ? options.color.toLowerCase() : 'черный';
    console.log(`Searching for products matching color: "${targetColor}"...`);

    const products = db.prepare(`SELECT * FROM products`).all() as any[];
    const matched: Record<string, any[]> = {};

    for (const prod of products) {
      const color = getProductColor(prod.specs_json);
      if (color.includes(targetColor)) {
        if (!matched[prod.category_id]) {
          matched[prod.category_id] = [];
        }
        matched[prod.category_id].push(prod);
      }
    }

    console.log(`\nFound matching products:`);
    for (const [cat, items] of Object.entries(matched)) {
      console.log(`\nCategory: ${cat}`);
      console.log(`--------------------------------------------------`);
      for (const item of items) {
        // Find best price
        const bestOffer = db.prepare(`
          SELECT MIN(price) as min_price FROM offers WHERE product_id = ?
        `).get(item.id) as any;
        const priceStr = bestOffer && bestOffer.min_price ? `${bestOffer.min_price.toFixed(2)} BYN` : 'N/A';
        console.log(`- [${item.brand}] ${item.title} (Price from: ${priceStr}) - ID: ${item.id}`);
      }
    }
  } else {
    console.log("Usage Examples:");
    console.log("  npx tsx src/query.ts --product=siemens:ex675lxc1e");
    console.log("  npx tsx src/query.ts --color-match --color=черный");
  }
}

main().catch(console.error);
