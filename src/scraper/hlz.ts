import { BaseScraper, ScraperOptions, ScrapeResult, ScrapedProduct, ScrapedOffer } from './base.js';
import { saveScrapedData, normalizeModel, DbCategory, DbProduct, DbOffer } from '../database/db.js';

interface RawItem {
  name: string;
  priceNum: number;
  url: string;
  availability: string;
  specs: {
    dimensions: string;
    thickness: string;
    decor: string;
    texture: string;
  };
}

export class HlzScraper extends BaseScraper {
  sourceName = 'hlz';
  private baseUrl = 'https://hlz.by';
  private headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Referer': 'https://hlz.by/',
  };

  private async fetchPage(url: string): Promise<string> {
    const res = await fetch(url, { headers: this.headers });
    if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
    return res.text();
  }

  private parseName(name: string) {
    // Extract dimensions: e.g. "2800х2070", "3050 х 1320", "2800 * 2070"
    const dimMatch = name.match(/(\d{4})\s*[xх×*]\s*(\d{3,4})/i);
    const dimensions = dimMatch ? `${dimMatch[1]}×${dimMatch[2]}` : '';

    // Extract thickness: e.g. "18 мм", "10 мм", "1 мм"
    const thickMatch = name.match(/(\d+(?:\.\d+)?)\s*мм/i);
    const thickness = thickMatch ? `${thickMatch[1]} мм` : '';

    // Extract decor code: e.g. "U961", "H1180", "W1000", "F186", "R005"
    const decorMatch = name.match(/\b([A-Z]\d{3,4}[A-Z]?)\b/i) || name.match(/\b(R\d{3})\b/i);
    const decor = decorMatch ? decorMatch[1].toUpperCase() : '';

    // Extract texture: e.g. "ST9", "ST38", "SM", "ED", "TM9", "GS/ST7"
    const textureMatch = name.match(/\b(ST\s*\d+|SM|GS|ED|TM\s*\d+)\b/i);
    const texture = textureMatch ? textureMatch[1].replace(/\s/g, '').toUpperCase() : '';

    return { dimensions, thickness, decor, texture };
  }

  private extractItems(html: string): RawItem[] {
    const items: RawItem[] = [];

    // Patterns
    const nameRe = /<div class="item-title">\s*<a href="([^"]+)" class="dark_link">\s*<span>([^<]+)<\/span>/g;
    const priceRe = /data-currency="BYN" data-value="([\d.]+)"/g;
    const stockRe = /<div class="item-stock[^"]*"[^>]*>\s*<span class="value">([^<]+)<\/span>/g;

    const names: Array<{ url: string; name: string }> = [];
    const prices: number[] = [];
    const stocks: string[] = [];

    let m: RegExpExecArray | null;

    while ((m = nameRe.exec(html)) !== null) {
      names.push({ url: this.baseUrl + m[1], name: m[2].trim() });
    }

    while ((m = priceRe.exec(html)) !== null) {
      prices.push(parseFloat(m[1]));
    }

    while ((m = stockRe.exec(html)) !== null) {
      stocks.push(m[1].trim());
    }

    for (let i = 0; i < names.length; i++) {
      const { name, url } = names[i];
      const priceNum = prices[i] ?? 0;
      const availability = stocks[i] ?? '';
      const specs = this.parseName(name);

      items.push({
        name,
        priceNum,
        availability,
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

  private async scrapeSubcategory(pathSlug: string, label: string): Promise<RawItem[]> {
    const allItems: RawItem[] = [];
    let pageNum = 1;
    let totalPages = 1;

    do {
      const url = pageNum === 1
        ? `${this.baseUrl}${pathSlug}`
        : `${this.baseUrl}${pathSlug}?PAGEN_1=${pageNum}`;

      console.log(`  📄 [${label}] page ${pageNum}/${totalPages}: ${url}`);

      const html = await this.fetchPage(url);

      if (pageNum === 1) {
        totalPages = this.detectTotalPages(html);
        console.log(`     Found ${totalPages} pages for ${label}`);
      }

      const items = this.extractItems(html);
      console.log(`     → ${items.length} items extracted`);
      allItems.push(...items);

      pageNum++;
      if (pageNum <= totalPages) {
        await new Promise(r => setTimeout(r, 800));
      }
    } while (pageNum <= totalPages && pageNum <= 15);

    return allItems;
  }

  async scrape(options: ScraperOptions): Promise<ScrapeResult> {
    const categoryId = options.category;
    const limit = options.limit ?? 1000;
    console.log(`Starting HlzScraper scrape for category: ${categoryId}...`);

    let subcategories: { slug: string; label: string }[] = [];
    let categoryName = 'Материалы';

    if (categoryId === 'ldsp') {
      categoryName = 'ЛДСП';
      subcategories = [
        { slug: '/catalog/ldsp/drevesnye/',   label: 'Древесные' },
        { slug: '/catalog/ldsp/odnotonnye/',  label: 'Однотонные' },
        { slug: '/catalog/ldsp/fantaziynye/', label: 'Фантазийные' },
        { slug: '/catalog/ldsp/filvud_mdf/',  label: 'Филвуд MDF' },
      ];
    } else if (categoryId === 'hpl') {
      categoryName = 'HPL Пластик';
      subcategories = [{ slug: '/catalog/bumazhno_sloistye_plastiki/', label: 'HPL Пластик' }];
    } else if (categoryId === 'perfectsense') {
      categoryName = 'PerfectSense';
      subcategories = [{ slug: '/catalog/egger_perfektsens/', label: 'PerfectSense' }];
    } else if (categoryId === 'mdf') {
      categoryName = 'МДФ плиты';
      subcategories = [{ slug: '/catalog/mdf/', label: 'МДФ плиты' }];
    } else if (categoryId === 'compact_hpl') {
      categoryName = 'Компакт плиты';
      subcategories = [{ slug: '/catalog/kompakt_plita/', label: 'Компакт плита' }];
    } else if (categoryId === 'laminated_countertop') {
      categoryName = 'Столешницы HPL';
      subcategories = [{ slug: '/catalog/stoleshnitsy/', label: 'Столешницы' }];
    } else {
      throw new Error(`Unsupported category '${categoryId}' for hlz.by`);
    }

    const rawItems: RawItem[] = [];
    for (const sub of subcategories) {
      try {
        const items = await this.scrapeSubcategory(sub.slug, sub.label);
        rawItems.push(...items);
      } catch (err: any) {
        console.error(`Failed to scrape subcategory ${sub.label}: ${err.message}`);
      }
      await new Promise(r => setTimeout(r, 1000));
    }

    console.log(`Scraping complete! Total items found: ${rawItems.length}`);

    // Map to Db structure
    const dbCategory: DbCategory = {
      id: categoryId,
      name: categoryName,
      url: `${this.baseUrl}/catalog/`
    };

    const products: DbProduct[] = [];
    const offers: DbOffer[] = [];

    const uniqueProductsMap = new Map<string, DbProduct>();

    // Truncate list to limit
    const itemsToProcess = rawItems.slice(0, limit);

    for (const item of itemsToProcess) {
      // Determine Brand
      let brand = 'Egger';
      if (item.name.toLowerCase().includes('kronospan') || item.name.toLowerCase().includes('кроношпан')) {
        brand = 'Kronospan';
      } else if (item.name.toLowerCase().includes('arcobalen') || item.name.toLowerCase().includes('аркобален')) {
        brand = 'Arcobalen';
      } else if (item.name.toLowerCase().includes('sm`art') || item.name.toLowerCase().includes('smart')) {
        brand = 'Smart';
      }

      // Model: decor + thickness if possible, or just the short name
      const cleanDecor = item.specs.decor;
      const cleanThickness = item.specs.thickness.replace(/\s+/g, '');
      const modelCode = cleanDecor 
        ? `${cleanDecor}_${cleanThickness || '18mm'}`.toLowerCase()
        : item.name.toLowerCase().replace(/[^a-z0-9]/g, '_').substring(0, 100);

      const canonicalId = normalizeModel(brand, modelCode);

      // Create product record if not exists
      if (!uniqueProductsMap.has(canonicalId)) {
        uniqueProductsMap.set(canonicalId, {
          id: canonicalId,
          category_id: categoryId,
          brand,
          model: modelCode.toUpperCase(),
          title: item.name,
          specs_json: JSON.stringify({
            ...item.specs,
            availability: item.availability
          })
        });
      }

      // Offer details
      // Get URL key
      const urlKeyMatch = item.url.match(/\/(\d+)\/$/);
      const urlKey = urlKeyMatch ? urlKeyMatch[1] : item.name.toLowerCase().replace(/[^a-z0-9]/g, '');

      offers.push({
        id: `hlz:hlz:${urlKey}`,
        product_id: canonicalId,
        source: this.sourceName,
        store_key: urlKey,
        reseller_id: 'hlz',
        reseller_name: 'Holtz Group',
        reseller_url: item.url,
        price: item.priceNum > 0 ? item.priceNum : undefined,
        price_unit: 'BYN/шт',
        availability: item.availability || 'В наличии'
      });
    }

    const uniqueProducts = Array.from(uniqueProductsMap.values());
    console.log(`Saving ${uniqueProducts.length} products and ${offers.length} offers to the database...`);
    
    saveScrapedData(dbCategory, uniqueProducts, offers, []);

    // Return format
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
