import { BaseScraper, ScraperOptions, ScrapeResult, ScrapedProduct, ScrapedOffer } from './base.js';
import { saveScrapedData, normalizeModel, DbCategory, DbProduct, DbOffer } from '../database/db.js';

interface RawItem {
  name: string;
  priceNum: number;
  url: string;
  specs: {
    dimensions: string;
    thickness: string;
    decor: string;
    texture: string;
  };
}

export class MlSmartScraper extends BaseScraper {
  sourceName = 'mlsmart';
  private baseUrl = 'https://ml-smart.by';
  private headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Referer': 'https://ml-smart.by/',
  };

  private async fetchPage(url: string): Promise<string> {
    const res = await fetch(url, { headers: this.headers });
    if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
    return res.text();
  }

  private parseName(name: string) {
    // Extract dimensions: e.g. "2800х2070", "2800x2070"
    const dimMatch = name.match(/(\d{4})\s*[xх×*]\s*(\d{3,4})/i);
    const dimensions = dimMatch ? `${dimMatch[1]}×${dimMatch[2]}` : '2800×2070';

    // Extract thickness: e.g. "18 мм", "10 мм", "16 мм"
    const thickMatch = name.match(/(\d+(?:\.\d+)?)\s*мм/i);
    const thickness = thickMatch ? `${thickMatch[1]} мм` : '18 мм';

    // Extract decor code: e.g. "U961", "H1180", "W1000", "F186"
    const decorMatch = name.match(/\b([A-Z]{1,2}\d{3,4}[A-Z]?)\b/);
    const decor = decorMatch ? decorMatch[1].toUpperCase() : '';

    // Extract texture: e.g. "ST9", "ST37", "SM"
    const textureMatch = name.match(/\b(ST\s*\d+|SM|ST\d+\w*)\b/i);
    const texture = textureMatch ? textureMatch[1].replace(/\s/g, '').toUpperCase() : '';

    return { dimensions, thickness, decor, texture };
  }

  private extractItems(html: string): RawItem[] {
    const items: RawItem[] = [];

    const cards = html.split('class="product-card"');
    
    for (let i = 1; i < cards.length; i++) {
      const card = cards[i];
      
      // Extract URL and Title
      const bodyMatch = card.match(/href="([^"]+)"\s+class="product-card__body"\s+title="([^"]+)"/i);
      if (!bodyMatch) continue;
      
      const url = this.baseUrl + bodyMatch[1];
      const name = bodyMatch[2].trim();
      
      // Extract price
      const priceMatch = card.match(/class="price__current"[^>]*>([\s\S]*?)<\/div>/i);
      let priceNum = 0;
      if (priceMatch) {
        const priceText = priceMatch[1].replace(/<[^>]+>/g, '').trim();
        const cleanPrice = priceText.replace(/[^\d,.]/g, '').replace(',', '.');
        priceNum = parseFloat(cleanPrice);
      }
      
      const specs = this.parseName(name);

      items.push({
        name,
        priceNum,
        url,
        specs
      });
    }

    return items;
  }

  private detectTotalPages(html: string): number {
    const pagerRe = /PAGEN_1=(\d+)/g;
    let max = 1;
    let m: RegExpExecArray | null;
    while ((m = pagerRe.exec(html)) !== null) {
      const n = parseInt(m[1]);
      if (n > max) max = n;
    }
    return max;
  }

  async scrape(options: ScraperOptions): Promise<ScrapeResult> {
    const categoryId = options.category;
    const limit = options.limit ?? 1000;
    
    let pathSlug = '';
    let categoryName = '';
    
    if (categoryId === 'ldsp') {
      pathSlug = '/catalog/ldsp/';
      categoryName = 'ЛДСП';
    } else if (categoryId === 'compact_hpl') {
      pathSlug = '/catalog/kompakt-plita/';
      categoryName = 'Компакт плиты';
    } else if (categoryId === 'laminated_countertop') {
      pathSlug = '/catalog/postforming/';
      categoryName = 'Столешницы HPL';
    } else {
      throw new Error(`Unsupported category '${categoryId}' for ml-smart.by`);
    }

    console.log(`Starting MlSmartScraper scrape for category: ${categoryId}...`);
    
    const rawItems: RawItem[] = [];
    let pageNum = 1;
    let totalPages = 1;

    do {
      const url = pageNum === 1
        ? `${this.baseUrl}${pathSlug}`
        : `${this.baseUrl}${pathSlug}?PAGEN_1=${pageNum}`;

      console.log(`  📄 page ${pageNum}/${totalPages}: ${url}`);
      try {
        const html = await this.fetchPage(url);

        if (pageNum === 1) {
          totalPages = this.detectTotalPages(html);
          console.log(`     Found ${totalPages} pages`);
        }

        const items = this.extractItems(html);
        console.log(`     → Extracted ${items.length} items`);
        rawItems.push(...items);
      } catch (err: any) {
        console.error(`  ❌ Failed page ${pageNum}: ${err.message}`);
      }

      pageNum++;
      if (pageNum <= totalPages) {
        await new Promise(r => setTimeout(r, 800));
      }
    } while (pageNum <= totalPages && pageNum <= 30);

    console.log(`Scraping complete! Total items found: ${rawItems.length}`);

    // Map to Db structure
    const dbCategory: DbCategory = {
      id: categoryId,
      name: categoryName,
      url: `${this.baseUrl}${pathSlug}`
    };

    const products: DbProduct[] = [];
    const offers: DbOffer[] = [];
    const uniqueProductsMap = new Map<string, DbProduct>();

    // Truncate list to limit
    const itemsToProcess = rawItems.slice(0, limit);

    for (const item of itemsToProcess) {
      // Determine Brand
      let brand = 'Egger';
      const nameLower = item.name.toLowerCase();
      if (nameLower.includes('kronospan') || nameLower.includes('кроношпан')) {
        brand = 'Kronospan';
      } else if (nameLower.includes('smart') || nameLower.includes('смарт')) {
        brand = 'Smart';
      }

      // Model code
      const cleanDecor = item.specs.decor;
      const cleanThickness = item.specs.thickness.replace(/\s+/g, '');
      const modelCode = cleanDecor 
        ? `${cleanDecor}_${cleanThickness || '18mm'}`.toLowerCase()
        : item.name.toLowerCase().replace(/[^a-z0-9]/g, '_').substring(0, 100);

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
      // Get URL key
      const urlKeyMatch = item.url.match(/\/([^\/]+)\/$/) || item.url.match(/\/([^\/]+)$/);
      const urlKey = urlKeyMatch ? urlKeyMatch[1] : item.name.toLowerCase().replace(/[^a-z0-9]/g, '');

      offers.push({
        id: `mlsmart:mlsmart:${urlKey}`,
        product_id: canonicalId,
        source: this.sourceName,
        store_key: urlKey,
        reseller_id: 'mlsmart',
        reseller_name: 'Smart Group',
        reseller_url: item.url,
        price: item.priceNum > 0 ? item.priceNum : undefined,
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
