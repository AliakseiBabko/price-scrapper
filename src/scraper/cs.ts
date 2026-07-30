import { BaseScraper, ScraperOptions, ScrapeResult } from './base.js';
import { saveScrapedData, normalizeModel, DbCategory, DbProduct, DbOffer } from '../database/db.js';
import { chromium } from 'playwright';

interface RawItem {
  name: string;
  url: string;
  priceText: string;
  skuText: string;
  descText: string;
}

export class CsScraper extends BaseScraper {
  sourceName = 'cs';
  private baseUrl = 'https://c-s.by';

  async scrape(options: ScraperOptions): Promise<ScrapeResult> {
    const categoryId = options.category;
    const limit = options.limit ?? 1000;

    if (categoryId !== 'compact_hpl') {
      throw new Error(`Unsupported category '${categoryId}' for c-s.by. Only 'compact_hpl' is supported.`);
    }

    console.log(`Launching browser for CsScraper: ${categoryId}...`);
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    await page.setExtraHTTPHeaders({
      'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    });

    const dbCategory: DbCategory = {
      id: categoryId,
      name: 'Компакт плиты',
      url: `${this.baseUrl}/katalog/kromka.html`
    };

    const rawItems: RawItem[] = [];
    let currentUrl = dbCategory.url;
    let pageNum = 1;

    while (true) {
      console.log(`Processing page ${pageNum}: ${currentUrl}...`);
      
      try {
        await page.goto(currentUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(2000);
      } catch (err: any) {
        console.error(`Error navigating to ${currentUrl}: ${err.message}`);
        break;
      }

      // Extract products from current page
      const pageItems = await page.evaluate(() => {
        const results: { name: string; url: string; priceText: string; skuText: string; descText: string }[] = [];
        const cards = document.querySelectorAll('div.product.product-item');
        
        cards.forEach(card => {
          const titleEl = card.querySelector('div.vm-product_name a');
          const priceEl = card.querySelector('div.product-price span.PricesalesPrice');
          const skuEl = card.querySelector('div.sku');
          const descEl = card.querySelector('div.product-short-description div.detail_text');
          
          if (titleEl) {
            const name = titleEl.textContent?.trim() || '';
            const url = (titleEl as HTMLAnchorElement).href || '';
            const priceText = priceEl?.textContent?.trim() || '';
            const skuText = skuEl?.textContent?.trim() || '';
            
            // Replace <br> tags with newlines and strip remaining HTML tags
            const descText = descEl ? descEl.innerHTML.replace(/<br\s*\/?>/gi, '\n').replace(/<[^>]+>/g, '').trim() : '';
            
            results.push({ name, url, priceText, skuText, descText });
          }
        });
        return results;
      });

      console.log(`Found ${pageItems.length} items on page ${pageNum}`);
      rawItems.push(...pageItems);

      // Check if we hit the limit or there are no items
      if (pageItems.length === 0 || rawItems.length >= limit) {
        break;
      }

      // Find next page link
      const nextPageUrl = await page.evaluate(() => {
        const links = Array.from(document.querySelectorAll('ul.pagination a, .vm-pagination a, div.pagination a'));
        const nextLink = links.find(a => a.textContent?.trim().toLowerCase() === 'вперёд');
        return nextLink ? (nextLink as HTMLAnchorElement).href : null;
      });

      if (!nextPageUrl || nextPageUrl === currentUrl) {
        console.log('No next page link found.');
        break;
      }

      currentUrl = nextPageUrl;
      pageNum++;
    }

    await browser.close();

    console.log(`Scraping finished. Total items extracted: ${rawItems.length}`);

    const products: DbProduct[] = [];
    const offers: DbOffer[] = [];
    const uniqueProductsMap = new Map<string, DbProduct>();

    // Process all items and map to DB format
    const itemsToProcess = rawItems.slice(0, limit);
    for (const item of itemsToProcess) {
      const priceCleanStr = item.priceText
        .replace(/[^\d,.]/g, '')
        .replace(',', '.');
      
      const priceNum = parseFloat(priceCleanStr);
      if (isNaN(priceNum) || priceNum <= 0) {
        // Skip items without a valid price
        continue;
      }

      // Parse specs from description
      const normalizedDesc = item.descText.replace(/&nbsp;/g, ' ').replace(/\u00a0/g, ' ');
      
      const getSpec = (key: string, text: string): string => {
        const lines = text.split('\n');
        const regex = new RegExp(`^${key}:\\s*(.+)`, 'i');
        for (const line of lines) {
          const m = line.trim().match(regex);
          if (m) return m[1].trim();
        }
        return '';
      };

      let brand = getSpec('Производитель', normalizedDesc);
      let coreColor = getSpec('Сердечник', normalizedDesc);
      let thickness = getSpec('Толщина', normalizedDesc);
      let width = getSpec('Ширина', normalizedDesc);
      let length = getSpec('Длина', normalizedDesc);
      let decor = getSpec('Структура', normalizedDesc);
      let article = getSpec('Артикул', normalizedDesc);

      // Fallback: Try parsing from Title if description specs are empty
      if (!thickness || !width || !length) {
        const sizeMatch = item.name.match(/(\d+)\s*[xх×*]\s*(\d+)\s*[xх×*]\s*(\d+)/i);
        if (sizeMatch) {
          thickness = thickness || `${sizeMatch[1]} мм`;
          width = width || sizeMatch[2];
          length = length || sizeMatch[3];
        }
      }

      // Parse brand from title if missing
      if (!brand) {
        const lowerName = item.name.toLowerCase();
        if (lowerName.includes('egger')) brand = 'Egger';
        else if (lowerName.includes('kronospan') || lowerName.includes('кроношпан')) brand = 'Kronospan';
        else if (lowerName.includes('arcobaleno') || lowerName.includes('аркобалено')) brand = 'Arcobaleno';
        else if (lowerName.includes('smart') || lowerName.includes('sm`art')) brand = 'Smart';
        else if (lowerName.includes('abet')) brand = 'Abet laminati';
        else if (lowerName.includes('arpa')) brand = 'Arpa';
        else if (lowerName.includes('asd')) brand = 'ASD Laminat';
        else if (lowerName.includes('duropal')) brand = 'Duropal';
        else if (lowerName.includes('gentas')) brand = 'Gentas';
        else if (lowerName.includes('sloplast')) brand = 'Sloplast';
        else if (lowerName.includes('slotex')) brand = 'Slotex';
        else brand = 'Unknown';
      }

      // Clean thickness and dimensions
      const cleanThickness = thickness.replace(/\s+/g, '').toLowerCase();
      const dimensions = (width && length) ? `${width.trim()}×${length.trim()}` : '';

      // Construct model code
      const cleanArticle = article ? article.replace(/\s+/g, '_') : item.skuText.replace(/Артикул:\s*/i, '').replace(/\s+/g, '_');
      const modelCode = `${cleanArticle || 'decor'}_${cleanThickness || '12mm'}_${dimensions.replace('×', 'x') || 'unknown'}`.toLowerCase()
        .replace(/[^a-z0-9_]/g, '')
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
            manufacturer: brand,
            coreColor,
            thickness,
            width,
            length,
            decor,
            article,
            dimensions
          })
        });
      }

      // Offer details
      const urlKey = item.url.split('/').pop()?.replace('.html', '') || item.name.toLowerCase().replace(/[^a-z0-9]/g, '');
      offers.push({
        id: `cs:cs:${urlKey}`,
        product_id: canonicalId,
        source: this.sourceName,
        store_key: urlKey,
        reseller_id: 'cs',
        reseller_name: 'Центр Столешниц',
        reseller_url: item.url,
        price: priceNum,
        price_unit: 'BYN/шт',
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
