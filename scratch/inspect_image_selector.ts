import { chromium } from 'playwright';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  const url = 'https://catalog.onliner.by/oven_cooker/bosch/hbg7764b1';
  console.log(`Navigating to: ${url}...`);
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await new Promise(resolve => setTimeout(resolve, 3000));

  const images = await page.evaluate(() => {
    const imgs = Array.from(document.querySelectorAll('img'));
    return imgs.map(img => ({
      src: img.src,
      className: img.className,
      id: img.id,
      alt: img.alt
    }));
  });

  console.log(`Found ${images.length} images on the page. Printing indexes 30 to 52:`);
  images.slice(30).forEach((img, idx) => {
    console.log(`[${idx + 31}] Src: "${img.src.substring(0, 120)}" | Class: "${img.className}" | Alt: "${img.alt}"`);
  });

  await browser.close();
}

main().catch(console.error);
