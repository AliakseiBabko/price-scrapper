export interface ScrapedProduct {
  id: string; // brand:model normalized
  category_id: string;
  brand: string;
  model: string;
  title: string;
  specs: Record<string, any>;
  rating?: number;
  reviews_count?: number;
}

export interface ScrapedOffer {
  id: string; // source:reseller_id:store_key
  product_id: string;
  source: string;
  store_key: string;
  reseller_id: string;
  reseller_name: string;
  reseller_url: string;
  reseller_rating?: number;
  reseller_reviews_count?: number;
  price?: number;
  price_unit?: string;
  availability?: string;
}

export interface ScrapedReview {
  id: string; // source:review_id
  product_id: string;
  source: string;
  author: string;
  rating?: number;
  text: string;
  pros: string;
  cons: string;
  date: string;
}

export interface ScrapeResult {
  category: {
    id: string;
    name: string;
    url: string;
  };
  products: ScrapedProduct[];
  offers: ScrapedOffer[];
  reviews: ScrapedReview[];
}

export type ScraperFilters = Record<string, string | string[]>;

export interface ScraperOptions {
  category: string;
  limit?: number;
  filters?: ScraperFilters;
}

export abstract class BaseScraper {
  abstract sourceName: string;
  abstract scrape(options: ScraperOptions): Promise<ScrapeResult>;
}
