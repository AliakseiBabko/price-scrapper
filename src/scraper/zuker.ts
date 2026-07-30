import { chromium } from 'playwright';
import { BaseScraper, ScraperOptions, ScrapeResult, ScrapedProduct, ScrapedOffer } from './base.js';
import { saveScrapedData, normalizeModel, DbCategory, DbProduct, DbOffer } from '../database/db.js';

interface RawItem {
  name: string;
  priceNum: number;
  url: string;
  specs: {
    dimensions: string;
    thickness: string;
    area: number;
    pricePerM2: number;
    countertopCost: number;
  };
}

export class ZukerScraper extends BaseScraper {
  sourceName = 'zuker';
  private baseUrl = 'https://zuker.by';

  async scrape(options: ScraperOptions): Promise<ScrapeResult> {
    const categoryId = options.category;
    const limit = options.limit ?? 1000;

    let baseCatalogUrl = '';
    let categoryName = '';

    if (categoryId === 'quartz_stone') {
      baseCatalogUrl = 'https://zuker.by/catalog/materialy-dlya-proizvodstva-mebeli-/kvartsevyy-kamen/';
      categoryName = 'Кварцевый камень';
    } else if (categoryId === 'acrylic_stone') {
      baseCatalogUrl = 'https://zuker.by/catalog/materialy-dlya-proizvodstva-mebeli-/akrilovyy-kamen/';
      categoryName = 'Акриловый камень';
    } else {
      throw new Error(`Unsupported category '${categoryId}' for zuker.by`);
    }

    console.log(`Launching browser for ZukerScraper: ${categoryId}...`);
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    
    await page.setExtraHTTPHeaders({
      'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    });

    console.log(`Navigating to ${baseCatalogUrl}...`);
    await page.goto(baseCatalogUrl, { waitUntil: 'networkidle', timeout: 60000 });

    const rawItems: RawItem[] = [];
    let currentPage = 1;

    while (true) {
      console.log(`Processing page ${currentPage}...`);
      
      await page.waitForSelector('.catalog_item, .item_info', { timeout: 10000 }).catch(() => {
        console.log('No catalog items selector found on this page.');
      });

      const pageItems = await page.evaluate(() => {
        const results: { name: string; priceText: string; url: string }[] = [];
        const cards = document.querySelectorAll('.catalog_item, .item_wrap');
        
        cards.forEach(card => {
          const titleEl = card.querySelector('.item-title a');
          const priceEl = card.querySelector('.price');
          
          if (titleEl && priceEl) {
            const name = (titleEl.querySelector('span') || titleEl).textContent?.trim() || '';
            const url = (titleEl as HTMLAnchorElement).href || '';
            const priceText = priceEl.textContent?.trim() || '';
            
            if (name && priceText) {
              results.push({ name, priceText, url });
            }
          }
        });
        return results;
      });

      console.log(`Found ${pageItems.length} items on page ${currentPage}`);

      for (const rawItem of pageItems) {
        const priceCleanStr = rawItem.priceText
          .replace(/цена:/i, '')
          .replace(/\/лист/i, '')
          .replace(/[^\d,.]/g, '')
          .replace(',', '.');
        
        const priceNum = parseFloat(priceCleanStr);
        if (isNaN(priceNum) || priceNum <= 0) {
          continue;
        }

        const lowerName = rawItem.name.toLowerCase();
        if (categoryId === 'quartz_stone') {
          if (!lowerName.includes('кварцев') && !lowerName.includes('caesarstone') && !lowerName.includes('norda') && !lowerName.includes('technistone') && !lowerName.includes('silestone')) {
            continue;
          }
        } else if (categoryId === 'acrylic_stone') {
          if (!lowerName.includes('акриловый камень') && !lowerName.includes('corian') && !lowerName.includes('montelli')) {
            continue;
          }
        }

        const dimMatch = rawItem.name.match(/(\d{4})\s*[xх×*]\s*(\d{3,4})/i);
        let dimensions = categoryId === 'quartz_stone' ? '3050×1400' : '3658×760';
        let area = categoryId === 'quartz_stone' ? 4.27 : 2.78;
        if (dimMatch) {
          const w = parseInt(dimMatch[1]);
          const h = parseInt(dimMatch[2]);
          dimensions = `${w}×${h}`;
          area = (w * h) / 1000000;
        }

        const thickMatch = rawItem.name.match(/(\d+)\s*мм/i);
        const thickness = thickMatch ? `${thickMatch[1]} мм` : '12 мм';

        const pricePerM2 = priceNum / area;
        const countertopCost = pricePerM2 * 1.62;

        rawItems.push({
          name: rawItem.name,
          priceNum,
          url: rawItem.url,
          specs: {
            dimensions,
            thickness,
            area,
            pricePerM2,
            countertopCost
          }
        });
      }

      // Check next page
      const nextPageUrl = `${baseCatalogUrl}?PAGEN_1=${currentPage + 1}`;
      console.log(`Checking next page via URL: ${nextPageUrl}`);
      
      const response = await page.goto(nextPageUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(2000);
      const hasItems = await page.locator('.catalog_item, .item_info').count();
      if (hasItems > 0 && currentPage < 10) {
        currentPage++;
        continue;
      }

      break;
    }

    await browser.close();
    console.log(`Scraping complete! Total items found: ${rawItems.length}`);

    // Deduplicate by name
    const uniqueItemsMap = new Map<string, RawItem>();
    for (const item of rawItems) {
      uniqueItemsMap.set(item.name, item);
    }
    const uniqueItems = Array.from(uniqueItemsMap.values());

    // Map to Db structure
    const dbCategory: DbCategory = {
      id: categoryId,
      name: categoryName,
      url: baseCatalogUrl
    };

    const products: DbProduct[] = [];
    const offers: DbOffer[] = [];
    const uniqueProductsMap = new Map<string, DbProduct>();

    // Truncate list to limit
    const itemsToProcess = uniqueItems.slice(0, limit);

    for (const item of itemsToProcess) {
      // Determine Brand
      let brand = 'Norda';
      const lowerName = item.name.toLowerCase();
      
      if (categoryId === 'quartz_stone') {
        if (lowerName.includes('caesarstone')) brand = 'Caesarstone';
        else if (lowerName.includes('technistone')) brand = 'Technistone';
        else if (lowerName.includes('silestone')) brand = 'Silestone';
      } else if (categoryId === 'acrylic_stone') {
        brand = 'Montelli';
        if (lowerName.includes('corian')) brand = 'Corian';
      }

      // Model: e.g. "Noble Carrara 30mm" -> "noble_carrara_30mm"
      // Try to extract color/model name
      let modelName = item.name;
      const cleanDecorMatch = item.name.match(/цвет\s+([^,0-9]+)/i) || item.name.match(/цвет\s+([a-zA-Z\s]+)/i);
      if (cleanDecorMatch) {
        modelName = cleanDecorMatch[1].trim();
      } else {
        // Fallback: strip brand and prefix
        modelName = modelName
          .replace(/Искусственный акриловый камень/gi, '')
          .replace(/Кварцевый агломерат/gi, '')
          .replace(/Кварцевый камень/gi, '')
          .replace(new RegExp(brand, 'gi'), '')
          .trim();
      }

      // Append thickness
      const cleanThickness = item.specs.thickness.replace(/\s+/g, '');
      const modelCode = `${modelName}_${cleanThickness}`.toLowerCase()
        .replace(/[^a-z0-9]/g, '_')
        .replace(/_+/g, '_')
        .replace(/^_+|_+$/g, '');

      const canonicalId = normalizeModel(brand, modelCode);

      if (!uniqueProductsMap.has(canonicalId)) {
        uniqueProductsMap.set(canonicalId, {
          id: canonicalId,
          category_id: categoryId,
          brand,
          model: modelCode.toUpperCase(),
          title: item.name,
          specs_json: JSON.stringify({
            ...item.specs,
            availability: 'В наличии'
          })
        });
      }

      // Offer details
      const urlKeyMatch = item.url.match(/\/(\d+)\/$/) || item.url.match(/\/([^\/]+)\/$/);
      const urlKey = urlKeyMatch ? urlKeyMatch[1] : item.name.toLowerCase().replace(/[^a-z0-9]/g, '');

      offers.push({
        id: `zuker:zuker:${urlKey}`,
        product_id: canonicalId,
        source: this.sourceName,
        store_key: urlKey,
        reseller_id: 'zuker',
        reseller_name: 'Zuker',
        reseller_url: item.url,
        price: item.priceNum,
        price_unit: 'BYN/лист',
        availability: 'В наличии'
      });
    }

    const uniqueProducts = Array.from(uniqueProductsMap.values());
    console.log(`Saving ${uniqueProducts.length} products and ${offers.length} offers to the database...`);
    
    saveScrapedData(dbCategory, uniqueProducts, offers, []);

    return {
      category: dbCategory,
      products: uniqueProducts.map(p => ({
        id: p.id,
        category_id: p.category_id,
        brand: p.brand,
        model: p.model,
        title: p.title,
        specs: JSON.parse(p.specs_json)
      })),
      offers: offers.map(o => ({
        id: o.id,
        product_id: o.product_id,
        source: o.source,
        store_key: o.store_key,
        reseller_id: o.reseller_id,
        reseller_name: o.reseller_name,
        reseller_url: o.reseller_url,
        price: o.price,
        price_unit: o.price_unit,
        availability: o.availability
      })),
      reviews: []
    };
  }
}
