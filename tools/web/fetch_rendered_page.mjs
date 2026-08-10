#!/usr/bin/env node
/**
 * Fetch a webpage's real, rendered text content via a headless/headed
 * Chromium browser (Playwright) - the actual post-JS DOM text, not a
 * summarized/paraphrased pass like the WebFetch tool.
 *
 * Why this exists: WebFetch converts a page to markdown and runs a small
 * fast model's summary of it against your prompt - useful for quick
 * questions, but lossy for a source that needs to be intake-processed as
 * evidence (numbers, exact wording, real project examples can get
 * paraphrased or dropped). This script instead saves the page's actual
 * rendered text verbatim, so it can be used as real source evidence the
 * same way a fetched YouTube transcript is.
 *
 * Usage:
 *   node tools/web/fetch_rendered_page.mjs <url> --output-dir <dir> [--headless] [--wait-ms N]
 *
 * Output: <output-dir>/<timestamp>_<hostname+path-slug>.txt (rendered text)
 *         <output-dir>/<timestamp>_<hostname+path-slug>.meta.json (url, timestamp, method)
 */
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--output-dir") args.outputDir = argv[++i];
    else if (a === "--headless") args.headless = true;
    else if (a === "--wait-ms") args.waitMs = parseInt(argv[++i], 10);
    else args._.push(a);
  }
  return args;
}

function slugForUrl(url) {
  const u = new URL(url);
  const raw = (u.hostname + u.pathname).replace(/[^a-zA-Z0-9]+/g, "_").replace(/^_+|_+$/g, "");
  return raw.slice(0, 80) || "page";
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args._.length !== 1 || !args.outputDir) {
    console.error("Usage: node fetch_rendered_page.mjs <url> --output-dir <dir> [--headless] [--wait-ms N]");
    process.exit(2);
  }
  const url = args._[0];
  const waitMs = args.waitMs || 3000;
  fs.mkdirSync(args.outputDir, { recursive: true });

  const browser = await chromium.launch({ headless: !!args.headless });
  const context = await browser.newContext({ locale: "ru-RU", viewport: { width: 1280, height: 1000 } });
  const page = await context.newPage();

  try {
    console.error(`[fetch-rendered] navigating to ${url} ...`);
    await page.goto(url, { waitUntil: "networkidle", timeout: 30000 }).catch(async () => {
      // networkidle can time out on pages with persistent background requests
      // (analytics, chat widgets) - fall back to domcontentloaded + a wait.
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
    });
    await sleep(waitMs);

    const text = await page.evaluate(() => document.body.innerText);
    const title = await page.title();

    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const base = `${timestamp}_${slugForUrl(url)}`;
    const txtPath = path.join(args.outputDir, `${base}.txt`);
    const metaPath = path.join(args.outputDir, `${base}.meta.json`);

    fs.writeFileSync(txtPath, `URL: ${url}\nTITLE: ${title}\nFETCHED: ${new Date().toISOString()}\n\n${text}`, "utf-8");
    fs.writeFileSync(
      metaPath,
      JSON.stringify({ url, title, timestamp: new Date().toISOString(), method: "playwright-rendered-text" }, null, 2),
      "utf-8"
    );

    console.log(`Saved: ${txtPath}`);
    console.log(`Text length: ${text.length} chars`);
    await browser.close();
    process.exit(0);
  } catch (err) {
    console.error(`[fetch-rendered] Error: ${err.message}`);
    await browser.close().catch(() => {});
    process.exit(1);
  }
}

main();
