import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';

// Ensure the data directory exists
const DB_DIR = path.resolve('data');
if (!fs.existsSync(DB_DIR)) {
  fs.mkdirSync(DB_DIR, { recursive: true });
}

const dbPath = path.join(DB_DIR, 'scraper.db');
export const db = new Database(dbPath);

// Enable foreign keys
db.pragma('foreign_keys = ON');

// Initialize the database tables
export function initDb() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS categories (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      url TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS products (
      id TEXT PRIMARY KEY,
      category_id TEXT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
      brand TEXT NOT NULL,
      model TEXT NOT NULL,
      title TEXT NOT NULL,
      specs_json TEXT NOT NULL,
      rating REAL DEFAULT 0.0,
      reviews_count INTEGER DEFAULT 0,
      last_updated TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS offers (
      id TEXT PRIMARY KEY, -- source:reseller_id:store_key
      product_id TEXT REFERENCES products(id) ON DELETE CASCADE,
      source TEXT NOT NULL,
      store_key TEXT NOT NULL,
      reseller_id TEXT NOT NULL,
      reseller_name TEXT NOT NULL,
      reseller_url TEXT NOT NULL,
      reseller_rating REAL,
      reseller_reviews_count INTEGER,
      price REAL,
      last_updated TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS price_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      offer_id TEXT NOT NULL REFERENCES offers(id) ON DELETE CASCADE,
      price REAL,
      timestamp TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS reviews (
      id TEXT PRIMARY KEY,
      product_id TEXT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
      source TEXT NOT NULL,
      author TEXT,
      rating REAL,
      text TEXT,
      pros TEXT,
      cons TEXT,
      date TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
    CREATE INDEX IF NOT EXISTS idx_products_model ON products(model);
    CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
    CREATE INDEX IF NOT EXISTS idx_offers_product ON offers(product_id);
    CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);
    CREATE INDEX IF NOT EXISTS idx_price_history_offer ON price_history(offer_id);
  `);
}

/**
 * Normalizes model names to match products across different websites.
 * Removes batch/reseller suffixes like "/01" but preserves core code characteristics.
 * E.g., "HBG7764B1/01" -> "hbg7764b1"
 * E.g., "KGN-49X03" -> "kgn49x03"
 */
export function normalizeModel(brand: string, model: string): string {
  const cleanBrand = brand.trim().toLowerCase().replace(/[^a-z0-9]/g, '');
  
  // Split at forward slash to discard manufacturing batch/variant suffixes (e.g. /01)
  let cleanModel = model.trim().split('/')[0].toLowerCase();
  
  // Remove non-alphanumeric chars (like spaces, dashes, etc.) to get core model index
  cleanModel = cleanModel.replace(/[^a-z0-9]/g, '');
  
  return `${cleanBrand}:${cleanModel}`;
}

// Interfaces for inserting data
export interface DbCategory {
  id: string;
  name: string;
  url: string;
}

export interface DbProduct {
  id: string;
  category_id: string;
  brand: string;
  model: string;
  title: string;
  specs_json: string;
  rating?: number;
  reviews_count?: number;
}

export interface DbOffer {
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
}

export interface DbReview {
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

/**
 * Transactionally saves a list of products, their offers, and reviews.
 */
export const saveScrapedData = db.transaction((
  category: DbCategory,
  products: DbProduct[],
  offers: DbOffer[],
  reviews: DbReview[]
) => {
  // 1. Upsert Category
  const insertCategory = db.prepare(`
    INSERT INTO categories (id, name, url)
    VALUES (?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
      name = excluded.name,
      url = excluded.url
  `);
  insertCategory.run(category.id, category.name, category.url);

  // 2. Upsert Products
  const insertProduct = db.prepare(`
    INSERT INTO products (id, category_id, brand, model, title, specs_json, rating, reviews_count, last_updated)
    VALUES ($id, $category_id, $brand, $model, $title, $specs_json, COALESCE($rating, 0.0), COALESCE($reviews_count, 0), datetime('now'))
    ON CONFLICT(id) DO UPDATE SET
      category_id = excluded.category_id,
      brand = excluded.brand,
      model = excluded.model,
      title = excluded.title,
      specs_json = excluded.specs_json,
      rating = CASE WHEN excluded.rating > 0 THEN excluded.rating ELSE products.rating END,
      reviews_count = CASE WHEN excluded.reviews_count > 0 THEN excluded.reviews_count ELSE products.reviews_count END,
      last_updated = datetime('now')
  `);

  for (const prod of products) {
    insertProduct.run({
      id: prod.id,
      category_id: prod.category_id,
      brand: prod.brand,
      model: prod.model,
      title: prod.title,
      specs_json: prod.specs_json,
      rating: prod.rating ?? 0,
      reviews_count: prod.reviews_count ?? 0
    });
  }

  // 3. Upsert Offers and Track Prices (reseller specific)
  const insertOffer = db.prepare(`
    INSERT INTO offers (id, product_id, source, store_key, reseller_id, reseller_name, reseller_url, reseller_rating, reseller_reviews_count, price, last_updated)
    VALUES ($id, $product_id, $source, $store_key, $reseller_id, $reseller_name, $reseller_url, $reseller_rating, $reseller_reviews_count, $price, datetime('now'))
    ON CONFLICT(id) DO UPDATE SET
      product_id = excluded.product_id,
      reseller_name = excluded.reseller_name,
      reseller_url = excluded.reseller_url,
      reseller_rating = excluded.reseller_rating,
      reseller_reviews_count = excluded.reseller_reviews_count,
      price = excluded.price,
      last_updated = datetime('now')
  `);

  const insertPriceHistory = db.prepare(`
    INSERT INTO price_history (offer_id, price, timestamp)
    VALUES (?, ?, datetime('now'))
  `);

  // We want to check if the latest price history record is different before inserting, or if it's a new day
  const getLatestPriceHistory = db.prepare(`
    SELECT price, timestamp
    FROM price_history
    WHERE offer_id = ?
    ORDER BY timestamp DESC
    LIMIT 1
  `);

  for (const offer of offers) {
    insertOffer.run({
      id: offer.id,
      product_id: offer.product_id,
      source: offer.source,
      store_key: offer.store_key,
      reseller_id: offer.reseller_id,
      reseller_name: offer.reseller_name,
      reseller_url: offer.reseller_url,
      reseller_rating: offer.reseller_rating ?? null,
      reseller_reviews_count: offer.reseller_reviews_count ?? 0,
      price: offer.price ?? null
    });

    // Price History Ingestion
    const latest = getLatestPriceHistory.get(offer.id) as { price: number | null, timestamp: string } | undefined;
    
    const today = new Date().toISOString().split('T')[0];
    const isDifferent = !latest || latest.price !== offer.price;
    const isNewDay = latest && latest.timestamp.split(' ')[0] !== today;

    if (isDifferent || isNewDay) {
      insertPriceHistory.run(offer.id, offer.price ?? null);
    }
  }

  // 4. Upsert Reviews
  const insertReview = db.prepare(`
    INSERT INTO reviews (id, product_id, source, author, rating, text, pros, cons, date)
    VALUES ($id, $product_id, $source, $author, $rating, $text, $pros, $cons, $date)
    ON CONFLICT(id) DO UPDATE SET
      rating = excluded.rating,
      text = excluded.text,
      pros = excluded.pros,
      cons = excluded.cons,
      date = excluded.date
  `);

  for (const rev of reviews) {
    insertReview.run({
      id: rev.id,
      product_id: rev.product_id,
      source: rev.source,
      author: rev.author || 'Anonymous',
      rating: rev.rating ?? null,
      text: rev.text,
      pros: rev.pros || '',
      cons: rev.cons || '',
      date: rev.date
    });
  }
});
