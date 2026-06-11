import { chromium } from 'playwright';
import { BaseScraper, ScraperOptions, ScrapeResult, ScrapedProduct, ScrapedOffer, ScrapedReview } from './base.js';
import { saveScrapedData, normalizeModel, DbCategory, DbProduct, DbOffer, DbReview } from '../database/db.js';

export class OnlinerScraper extends BaseScraper {
  sourceName = 'onliner';

  // Helper to introduce randomized delay (politeness)
  private async delay(minMs = 1000, maxMs = 2500) {
    const ms = Math.floor(Math.random() * (maxMs - minMs + 1) + minMs);
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async scrape(options: ScraperOptions): Promise<ScrapeResult> {
    const categoryId = options.category;
    const limit = options.limit ?? 10;
    const filters = options.filters ?? {};

    console.log(`Starting crawl for site: ${this.sourceName}, category: ${categoryId}, limit: ${limit}...`);

    console.log("Launching Chromium browser...");
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
      viewport: { width: 1920, height: 1080 },
      locale: 'ru-RU'
    });
    const page = await context.newPage();

    const result: ScrapeResult = {
      category: {
        id: categoryId,
        name: categoryId === 'oven_cooker' ? 'Духовые шкафы' : (categoryId === 'hob_cooker' ? 'Варочные панели' : categoryId),
        url: `https://catalog.onliner.by/${categoryId}`
      },
      products: [],
      offers: [],
      reviews: []
    };

    try {
      // 1. Establish session by loading the category list page
      console.log(`Navigating to category main page: ${result.category.url}...`);
      const response = await page.goto(result.category.url, { waitUntil: 'domcontentloaded' });
      if (response && response.status() === 404) {
        throw new Error(`Category '${categoryId}' not found on catalog.onliner.by (HTTP 404)`);
      }
      
      // Wait for session initialization
      await this.delay(1500, 2500);

      // 2. Build search query string
      const searchParams = new URLSearchParams();
      // Add custom filters
      for (const [k, v] of Object.entries(filters)) {
        if (Array.isArray(v)) {
          v.forEach((val, idx) => {
            searchParams.append(`${k}[${idx}]`, val);
          });
        } else {
          searchParams.append(k, v);
        }
      }

      let currentPage = 1;
      let scrapedCount = 0;
      let hasMorePages = true;

      while (scrapedCount < limit && hasMorePages) {
        searchParams.set('page', currentPage.toString());
        const searchUrl = `https://catalog.onliner.by/sdapi/catalog.api/search/${categoryId}?${searchParams.toString()}`;
        console.log(`Fetching search results page ${currentPage}: ${searchUrl}...`);

        const searchData = await page.evaluate(async (url) => {
          const resp = await fetch(url);
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
          return await resp.json();
        }, searchUrl);

        if (!searchData.products || searchData.products.length === 0) {
          console.log("No more products found in search response.");
          break;
        }

        const pageProducts = searchData.products;
        console.log(`Found ${pageProducts.length} products on search page ${currentPage}.`);

        // Update pagination status
        const lastPage = searchData.page?.last ?? 1;
        hasMorePages = currentPage < lastPage;
        currentPage++;

        // Process each product
        for (const item of pageProducts) {
          if (scrapedCount >= limit) break;

          const productKey = item.key;
          const brand = item.manufacturer?.name || 'Unknown';
          const modelName = item.name || productKey;
          const canonicalId = normalizeModel(brand, modelName);

          console.log(`[${scrapedCount + 1}/${limit}] Processing product: ${item.full_name} (${productKey}) -> Canonical ID: ${canonicalId}`);

          // Fetch Specs (Navigate to details page to scrape DOM specs)
          const productDetailUrl = `https://catalog.onliner.by/${categoryId}/${item.manufacturer?.key}/${productKey}`;
          console.log(`  Scraping specifications from page: ${productDetailUrl}...`);
          
          let specs: Record<string, any> = {};
          try {
            await page.goto(productDetailUrl, { waitUntil: 'domcontentloaded' });
            await this.delay(800, 1500);

            specs = await page.evaluate(() => {
              const res: Record<string, string> = {};
              const tables = document.querySelectorAll('.product-specs__table');
              tables.forEach(table => {
                table.querySelectorAll('tr').forEach(row => {
                  const keyCell = row.querySelector('td:first-child');
                  const valueCell = row.querySelector('td:last-child');
                  if (keyCell && valueCell) {
                    const key = keyCell.textContent?.trim().replace(/\s+/g, ' ') || '';
                    let value = valueCell.textContent?.trim().replace(/\s+/g, ' ') || '';
                    
                    const hasCheck = valueCell.querySelector('.i-tip, .icon_yes, .check, .yes');
                    const hasCross = valueCell.querySelector('.i-x, .icon_no, .cross, .no');
                    if (hasCheck) {
                      value = 'Да';
                    } else if (hasCross) {
                      value = 'Нет';
                    }

                    if (key && value && !key.includes('?')) {
                      res[key] = value;
                    }
                  }
                });
              });
              return res;
            });
            console.log(`  Successfully extracted ${Object.keys(specs).length} specifications.`);
          } catch (err: any) {
            console.warn(`  Failed to extract specifications: ${err.message}`);
          }

          // Fetch Reseller Offers (Positions)
          const positionsUrl = `https://catalog.onliner.by/sdapi/shop.api/products/${productKey}/positions?town=all&town_id=17030`;
          console.log(`  Fetching reseller offers from: ${positionsUrl}...`);
          const scrapedOffers: ScrapedOffer[] = [];
          try {
            const positionsData = await page.evaluate(async (url) => {
              const resp = await fetch(url);
              if (!resp.ok) return { positions: {} };
              return await resp.json();
            }, positionsUrl);

            if (positionsData && positionsData.positions) {
              const primary = positionsData.positions.primary || [];
              const secondary = positionsData.positions.secondary || [];
              const allPositions = [...primary, ...secondary];
              
              const shopsMap = positionsData.shops || {};
              for (const pos of allPositions) {
                const shopId = pos.shop_id?.toString() || '';
                const shop = shopsMap[shopId] || {};
                
                const price = pos.position_price?.amount ? Number(pos.position_price.amount) : undefined;
                const resellerName = shop.title || `Shop #${shopId}`;
                const resellerUrl = shop.html_url || '';
                const resellerRating = shop.reviews?.rating ? Number(shop.reviews.rating) : undefined;
                const resellerReviewsCount = shop.reviews?.count ? Number(shop.reviews.count) : 0;

                scrapedOffers.push({
                  id: `onliner:${shopId}:${productKey}`,
                  product_id: canonicalId,
                  source: this.sourceName,
                  store_key: productKey,
                  reseller_id: shopId,
                  reseller_name: resellerName,
                  reseller_url: resellerUrl,
                  reseller_rating: resellerRating,
                  reseller_reviews_count: resellerReviewsCount,
                  price: price
                });
              }
            }
            console.log(`  Successfully scraped ${scrapedOffers.length} reseller offers.`);
          } catch (err: any) {
            console.warn(`  Failed to fetch reseller offers: ${err.message}`);
          }

          // Fallback if no individual offers were successfully scraped but search result has prices
          if (scrapedOffers.length === 0 && item.prices) {
            const priceMin = item.prices.price_min?.amount ? Number(item.prices.price_min.amount) : undefined;
            if (priceMin) {
              scrapedOffers.push({
                id: `onliner:unknown:${productKey}`,
                product_id: canonicalId,
                source: this.sourceName,
                store_key: productKey,
                reseller_id: 'unknown',
                reseller_name: 'Unknown Reseller',
                reseller_url: '',
                reseller_rating: undefined,
                reseller_reviews_count: 0,
                price: priceMin
              });
            }
          }

          // Fetch Reviews (using API fetch in page context)
          const reviewsUrl = `https://catalog.onliner.by/sdapi/catalog.api/products/${productKey}/reviews?limit=10`;
          console.log(`  Fetching reviews from API: ${reviewsUrl}...`);
          let reviews: ScrapedReview[] = [];
          try {
            const reviewsData = await page.evaluate(async (url) => {
              const resp = await fetch(url);
              if (!resp.ok) return { reviews: [] };
              return await resp.json();
            }, reviewsUrl);

            if (reviewsData.reviews && Array.isArray(reviewsData.reviews)) {
              reviews = reviewsData.reviews.map((r: any) => ({
                id: `onliner:${r.id}`,
                product_id: canonicalId,
                source: this.sourceName,
                author: r.author?.name || 'Anonymous',
                rating: r.rating ? Number(r.rating) : undefined,
                text: r.text || '',
                pros: r.pros || '',
                cons: r.cons || '',
                date: r.created_at ? r.created_at.split('T')[0] : new Date().toISOString().split('T')[0]
              }));
            }
            console.log(`  Successfully fetched ${reviews.length} reviews.`);
          } catch (err: any) {
            console.warn(`  Failed to fetch reviews: ${err.message}`);
          }

          // Gather pricing and offer details
          const ratingNormalized = item.reviews?.rating ? Number(item.reviews.rating) / 10 : 0.0;
          const reviewsCount = item.reviews?.count ? Number(item.reviews.count) : 0;

          const scrapedProduct: ScrapedProduct = {
            id: canonicalId,
            category_id: categoryId,
            brand: brand,
            model: modelName,
            title: item.full_name,
            specs: specs,
            rating: ratingNormalized,
            reviews_count: reviewsCount
          };

          // Save directly to the DB transactionally
          const dbCategory: DbCategory = {
            id: categoryId,
            name: result.category.name,
            url: result.category.url
          };

          const dbProduct: DbProduct = {
            id: scrapedProduct.id,
            category_id: scrapedProduct.category_id,
            brand: scrapedProduct.brand,
            model: scrapedProduct.model,
            title: scrapedProduct.title,
            specs_json: JSON.stringify(scrapedProduct.specs),
            rating: scrapedProduct.rating,
            reviews_count: scrapedProduct.reviews_count
          };

          const dbOffers: DbOffer[] = scrapedOffers.map(o => ({
            id: o.id,
            product_id: o.product_id,
            source: o.source,
            store_key: o.store_key,
            reseller_id: o.reseller_id,
            reseller_name: o.reseller_name,
            reseller_url: o.reseller_url,
            reseller_rating: o.reseller_rating,
            reseller_reviews_count: o.reseller_reviews_count,
            price: o.price
          }));

          const dbReviews: DbReview[] = reviews.map(r => ({
            id: r.id,
            product_id: r.product_id,
            source: r.source,
            author: r.author,
            rating: r.rating,
            text: r.text,
            pros: r.pros,
            cons: r.cons,
            date: r.date
          }));

          saveScrapedData(dbCategory, [dbProduct], dbOffers, dbReviews);

          // Append to memory results
          result.products.push(scrapedProduct);
          result.offers.push(...scrapedOffers);
          result.reviews.push(...reviews);

          scrapedCount++;
          await this.delay(1000, 2000); // Politeness delay between products
        }
      }
    } finally {
      await browser.close();
      console.log("Browser closed.");
    }

    console.log(`Crawl finished. Scraped: ${result.products.length} products, ${result.offers.length} offers, and ${result.reviews.length} reviews.`);
    return result;
  }
}
