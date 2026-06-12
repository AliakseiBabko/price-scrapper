import { chromium } from 'playwright';

async function main() {
  console.log("Launching Chromium to intercept search API requests...");
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // Set up request interception
  page.on('request', request => {
    const url = request.url();
    if (url.includes('sdapi') || url.includes('search') || url.includes('suggest')) {
      console.log(`>> Intercepted API Request: ${url}`);
    }
  });

  console.log("Navigating to catalog.onliner.by...");
  await page.goto("https://catalog.onliner.by", { waitUntil: 'networkidle' });

  // Locate search input and type query
  console.log("Locating search input and typing 'BFL7221B1'...");
  const searchInput = page.locator('input.fast-search__input');
  await searchInput.click();
  await searchInput.fill('BFL7221B1');
  
  // Wait a few seconds for suggestions to load
  await new Promise(resolve => setTimeout(resolve, 3000));

  console.log("Typing 'DC90V9V9E'...");
  await searchInput.fill('DC90V9V9E');
  await new Promise(resolve => setTimeout(resolve, 3000));

  await browser.close();
  console.log("Browser closed.");
}

main().catch(console.error);
