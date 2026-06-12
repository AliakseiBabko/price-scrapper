import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';
import https from 'https';
import http from 'http';

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
      image_url TEXT,
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

  // Migrate existing databases to have the image_url column
  try {
    db.exec("ALTER TABLE products ADD COLUMN image_url TEXT;");
  } catch (e) {
    // Column already exists, ignore error
  }
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
  image_url?: string;
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
    INSERT INTO products (id, category_id, brand, model, title, specs_json, image_url, rating, reviews_count, last_updated)
    VALUES ($id, $category_id, $brand, $model, $title, $specs_json, $image_url, COALESCE($rating, 0.0), COALESCE($reviews_count, 0), datetime('now'))
    ON CONFLICT(id) DO UPDATE SET
      category_id = excluded.category_id,
      brand = excluded.brand,
      model = excluded.model,
      title = excluded.title,
      specs_json = excluded.specs_json,
      image_url = CASE WHEN excluded.image_url IS NOT NULL THEN excluded.image_url ELSE products.image_url END,
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
      image_url: prod.image_url ?? null,
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

/**
 * Downloads a binary file (e.g. product image) from a URL to a local destination path.
 */
export async function downloadImage(url: string, destPath: string): Promise<void> {
  const dir = path.dirname(destPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(destPath);
    const client = url.startsWith('https') ? https : http;

    client.get(url, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`Failed to download image: HTTP ${response.statusCode}`));
        return;
      }
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(destPath, () => {}); // delete file if error
      reject(err);
    });
  });
}

/**
 * Checks database freshness of a product's offers.
 * Returns metadata and a boolean indicating if it was updated within the last 7 days.
 */
export function getProductFreshness(productId: string): { exists: boolean, isFresh: boolean, storeKey?: string, categoryId?: string, brand?: string } {
  const row = db.prepare(`
    SELECT p.last_updated, p.category_id, p.brand, o.store_key
    FROM products p
    LEFT JOIN offers o ON p.id = o.product_id
    WHERE p.id = ?
    LIMIT 1
  `).get(productId) as { last_updated: string, category_id: string, brand: string, store_key: string } | undefined;

  if (!row) {
    return { exists: false, isFresh: false };
  }

  // Parse last_updated time (assumes UTC representation from SQLite's datetime('now'))
  const lastUpdated = new Date(row.last_updated.replace(' ', 'T') + 'Z');
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - lastUpdated.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  const isFresh = diffDays <= 7;
  return {
    exists: true,
    isFresh,
    storeKey: row.store_key,
    categoryId: row.category_id,
    brand: row.brand
  };
}

/**
 * Helper to parse color from the product specifications JSON string.
 */
export function getProductColor(specsJson: string): string {
  try {
    const specs = JSON.parse(specsJson);
    const colorKeys = ["Цвет", "Цвет фурнитуры", "Цвет корпуса", "Цвет профиля"];
    for (const key of colorKeys) {
      if (specs[key]) {
        return specs[key].trim().toLowerCase();
      }
    }
  } catch (e) {
    // Ignore
  }
  return "unknown";
}
