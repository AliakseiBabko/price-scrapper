#!/usr/bin/env node
/**
 * Experimental fallback: fetch a YouTube transcript by driving a real
 * browser UI (Playwright/Chromium) instead of youtube-transcript-api or
 * yt-dlp. Rationale: both of those talk to unofficial/internal YouTube
 * endpoints and are what triggered this project's 429/bot-check incidents
 * (2026-08-05) - a real rendered page with normal JS execution and browser
 * fingerprint is the same access pattern a human doing this manually would
 * use, so it may succeed where the script-only paths get blocked.
 *
 * Deliberately NOT using any exported cookies or a logged-in session for
 * this test - this launches a fresh, anonymous browser context. If this
 * works anonymously, that's the more valuable result (no credential
 * handling at all); cookies stay a separate, later escalation tier if
 * needed.
 *
 * ## Finding (2026-08-05, ZqfaeREBEYQ, anonymous, headed Chromium)
 *
 * This does NOT bypass the block seen from youtube-transcript-api/yt-dlp -
 * an anonymous rendered YouTube watch page from this environment/IP showed
 * "Sign in to confirm you're not a bot" directly over the video player on
 * first load, confirmed via screenshot. It's the same underlying defense,
 * just rendered as a visible page element instead of an HTTP
 * error/exception. A real logged-in session (e.g. via --cookies once that
 * path works) or a genuinely different IP/cooldown state would need to be
 * tested before concluding whether the browser-UI route offers any real
 * advantage over the script-based methods for this environment. The
 * script's own bot-check detection had a real bug on this first run
 * (page.textContent("body") doesn't pierce shadow DOM, and this exact
 * overlay renders inside a shadow-DOM element - fixed below to use
 * page.getByText(), which does pierce shadow DOM; the fix was verified
 * offline against a synthetic shadow-DOM page, not a live YouTube retry).
 *
 * One video per invocation, one navigation only. No parallelism.
 * Human-paced waits between UI actions (this is deliberate, not a
 * performance bug) - this fallback exists specifically to look like manual
 * browsing, not scripted access.
 *
 * --debug mode captures a screenshot after each stage (load, consent
 * dismissal, description-expand attempt, menu-open attempt, transcript-open
 * attempt) plus a JSON dump of every button's accessible name/aria-label
 * found at each stage, into --output-dir/debug_<video_id>/ - so selector
 * logic can be corrected from real evidence instead of guessed a second
 * time, without a second navigation to the same video.
 *
 * Output matches this project's existing transcript convention: a .txt
 * transcript file and a .meta.json sidecar with method="browser-ui-transcript",
 * written to --output-dir, so the existing archive_transcripts.py tool can
 * pick it up the same way as youtube-transcript-fetch's own output.
 *
 * Usage:
 *   node tools/youtube/browser_ui_transcript_fetch.mjs <video_id_or_url> --output-dir <dir> [--headless] [--debug]
 *
 * Exit codes:
 *   0  Success - transcript written.
 *   1  browser_ui_blocked - a sign-in/bot-check/captcha wall was detected.
 *   2  no_captions_or_ui_transcript_unavailable - page loaded fine, but no
 *      "Show transcript" UI was found (or it produced no segments) within
 *      the timeout budget.
 */
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--output-dir") args.outputDir = argv[++i];
    else if (a === "--headless") args.headless = true;
    else if (a === "--debug") args.debug = true;
    else if (a === "--timeout-ms") args.timeoutMs = parseInt(argv[++i], 10);
    else args._.push(a);
  }
  return args;
}

function extractVideoId(urlOrId) {
  const s = urlOrId.trim();
  if (/^[A-Za-z0-9_-]{11}$/.test(s)) return s;
  const m =
    s.match(/[?&]v=([A-Za-z0-9_-]{11})/) ||
    s.match(/youtu\.be\/([A-Za-z0-9_-]{11})/) ||
    s.match(/\/shorts\/([A-Za-z0-9_-]{11})/) ||
    s.match(/\/embed\/([A-Za-z0-9_-]{11})/);
  if (!m) throw new Error(`Could not extract a YouTube video ID from: ${s}`);
  return m[1];
}

const BOT_CHECK_MARKERS = [
  "sign in to confirm you're not a bot",
  "confirm you're not a robot",
  "unusual traffic",
  "our systems have detected unusual traffic",
];

// Enumerate every visible, enabled button-like element's accessible name -
// used both to find the right selector live and to write a debug dump.
async function enumerateButtons(page) {
  return page.evaluate(() => {
    const nodes = Array.from(
      document.querySelectorAll('button, [role="button"], [role="menuitem"], tp-yt-paper-item')
    );
    return nodes
      .filter((el) => {
        const rect = el.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0;
      })
      .map((el) => ({
        tag: el.tagName.toLowerCase(),
        ariaLabel: el.getAttribute("aria-label") || null,
        text: (el.textContent || "").trim().slice(0, 80),
      }))
      .filter((b) => b.ariaLabel || b.text);
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args._.length !== 1 || !args.outputDir) {
    console.error(
      "Usage: node browser_ui_transcript_fetch.mjs <video_id_or_url> --output-dir <dir> [--headless] [--debug] [--timeout-ms N]"
    );
    process.exit(2);
  }
  const videoId = extractVideoId(args._[0]);
  const url = `https://www.youtube.com/watch?v=${videoId}`;
  const timeoutMs = args.timeoutMs || 45000;
  const outputDir = args.outputDir;
  fs.mkdirSync(outputDir, { recursive: true });

  let debugDir = null;
  const debugLog = [];
  if (args.debug) {
    debugDir = path.join(outputDir, `debug_${videoId}`);
    fs.mkdirSync(debugDir, { recursive: true });
  }

  const shot = async (page, name) => {
    if (!debugDir) return;
    await page.screenshot({ path: path.join(debugDir, `${name}.png`), fullPage: false }).catch(() => {});
  };
  const dumpButtons = async (page, stage) => {
    if (!debugDir) return;
    const buttons = await enumerateButtons(page).catch(() => []);
    debugLog.push({ stage, buttons });
  };

  console.error(`[browser-ui] launching ${args.headless ? "headless" : "headed"} Chromium (anonymous context, no cookies loaded)...`);
  const browser = await chromium.launch({ headless: !!args.headless });
  const context = await browser.newContext({ locale: "en-US", viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();

  const writeFailure = (reasonClass, detail) => {
    const failPath = path.join(outputDir, `${videoId}.FAILED.meta.json`);
    fs.writeFileSync(
      failPath,
      JSON.stringify(
        { video_id: videoId, url, status: "failed", method: "browser-ui-transcript", reason_class: reasonClass, detail, timestamp: new Date().toISOString() },
        null, 2
      ),
      "utf-8"
    );
    console.error(`Failure details written to: ${failPath}`);
  };
  const flushDebugLog = () => {
    if (!debugDir) return;
    fs.writeFileSync(path.join(debugDir, "buttons_by_stage.json"), JSON.stringify(debugLog, null, 2), "utf-8");
    console.error(`[browser-ui] debug artifacts written to: ${debugDir}`);
  };

  try {
    console.error(`[browser-ui] navigating to ${url} (single navigation for this run) ...`);
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: timeoutMs });
    await sleep(3000);
    await shot(page, "01_after_load");

    // Bug fixed 2026-08-05: page.textContent("body") uses the raw DOM API,
    // which does NOT pierce shadow DOM - and this exact bot-check overlay
    // ("Sign in to confirm you're not a bot") renders inside a shadow-DOM
    // custom element (the video player area), so that check silently missed
    // text that was plainly visible on screen (confirmed via screenshot on
    // a real run). page.getByText() uses Playwright's own selector engine,
    // which does pierce shadow DOM, and is used here instead.
    let botCheckDetected = false;
    for (const marker of BOT_CHECK_MARKERS) {
      const loc = page.getByText(new RegExp(marker.replace(/'/g, "['’]"), "i"));
      if (await loc.count().catch(() => 0)) {
        botCheckDetected = true;
        break;
      }
    }
    if (botCheckDetected || /accounts\.google\.com/.test(page.url())) {
      console.error("[browser-ui] BLOCKED: bot-check/sign-in wall detected.");
      writeFailure("browser_ui_blocked", "Bot-check/sign-in wall text (found via shadow-DOM-piercing locator) or accounts.google.com redirect detected.");
      flushDebugLog();
      await browser.close();
      process.exit(1);
    }

    await dumpButtons(page, "after_load");

    // Best-effort cookie-consent dismissal.
    for (const label of ["Accept all", "I agree", "Принять все"]) {
      const btn = page.getByRole("button", { name: label, exact: false });
      if (await btn.count().catch(() => 0)) {
        try {
          await btn.first().click({ timeout: 3000 });
          console.error(`[browser-ui] dismissed a consent dialog ("${label}")`);
          await sleep(1500);
          break;
        } catch {}
      }
    }
    await shot(page, "02_after_consent");
    await dumpButtons(page, "after_consent");

    await sleep(1500);

    // Stage A: direct "Show transcript" button already visible (no expand needed).
    let opened = false;
    const directBtn = page.getByRole("button", { name: /transcript/i });
    if (await directBtn.count().catch(() => 0)) {
      await directBtn.first().click({ timeout: 5000 }).catch(() => {});
      opened = true;
      console.error('[browser-ui] clicked a direct "transcript" button.');
    }

    // Stage B: expand the description, then look again.
    if (!opened) {
      const expandCandidates = [
        page.getByRole("button", { name: /more|show more/i }).first(),
        page.locator("#description-inline-expander tp-yt-paper-button#expand"),
        page.locator("ytd-text-inline-expander #expand"),
      ];
      for (const cand of expandCandidates) {
        if (await cand.count().catch(() => 0)) {
          await cand.click({ timeout: 3000 }).catch(() => {});
          await sleep(1500);
          break;
        }
      }
      await shot(page, "03_after_description_expand");
      await dumpButtons(page, "after_description_expand");

      const transcriptAfterExpand = page.getByRole("button", { name: /transcript/i });
      if (await transcriptAfterExpand.count().catch(() => 0)) {
        await transcriptAfterExpand.first().click({ timeout: 5000 }).catch(() => {});
        opened = true;
        console.error('[browser-ui] clicked "transcript" button found after expanding description.');
      }
    }

    // Stage C: "..." more-actions menu near Like/Share/Save.
    if (!opened) {
      const moreActionsCandidates = [
        page.getByRole("button", { name: /more actions/i }).first(),
        page.locator('button[aria-label="More actions"]').first(),
        page.locator("#actions ytd-menu-renderer #button").first(),
      ];
      let menuOpened = false;
      for (const cand of moreActionsCandidates) {
        if (await cand.count().catch(() => 0)) {
          await cand.click({ timeout: 3000 }).catch(() => {});
          menuOpened = true;
          await sleep(1200);
          break;
        }
      }
      await shot(page, "04_after_more_actions_menu");
      await dumpButtons(page, "after_more_actions_menu");

      if (menuOpened) {
        const menuItem = page.getByRole("menuitem", { name: /transcript/i }).first();
        if (await menuItem.count().catch(() => 0)) {
          await menuItem.click({ timeout: 5000 }).catch(() => {});
          opened = true;
          console.error('[browser-ui] clicked a "transcript" menu item from the more-actions menu.');
        } else {
          // Broaden: any tp-yt-paper-item / ytd-menu-service-item-renderer whose text matches.
          const broadItem = page.locator("tp-yt-paper-item, ytd-menu-service-item-renderer").filter({ hasText: /transcript/i }).first();
          if (await broadItem.count().catch(() => 0)) {
            await broadItem.click({ timeout: 5000 }).catch(() => {});
            opened = true;
            console.error('[browser-ui] clicked a broader transcript-matching menu item.');
          }
        }
      }
    }

    if (!opened) {
      console.error('[browser-ui] No "Show transcript" control found via any stage.');
      writeFailure(
        "no_captions_or_ui_transcript_unavailable",
        "No transcript control found via direct button, post-expand button, or more-actions menu."
      );
      flushDebugLog();
      await browser.close();
      process.exit(2);
    }

    await sleep(2500);
    await shot(page, "05_after_transcript_open_attempt");
    await dumpButtons(page, "after_transcript_open_attempt");

    const segments = await page.locator("ytd-transcript-segment-renderer").allTextContents().catch(() => []);
    const text = segments.map((s) => s.trim()).filter(Boolean).join(" ");

    if (!text) {
      console.error("[browser-ui] Transcript control was clicked but no segment text rendered.");
      writeFailure(
        "no_captions_or_ui_transcript_unavailable",
        "Transcript control clicked successfully but ytd-transcript-segment-renderer yielded no text."
      );
      flushDebugLog();
      await browser.close();
      process.exit(2);
    }

    const sha256 = crypto.createHash("sha256").update(text, "utf-8").digest("hex");
    const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, "");
    const hash8 = sha256.slice(0, 8);
    const baseName = `${dateStr}_${videoId}_${hash8}`;
    const txtPath = path.join(outputDir, `${baseName}.txt`);
    const metaPath = path.join(outputDir, `${baseName}.meta.json`);

    fs.writeFileSync(txtPath, text, "utf-8");
    fs.writeFileSync(
      metaPath,
      JSON.stringify(
        {
          url, video_id: videoId, language: null, is_generated_captions: null,
          method: "browser-ui-transcript", timestamp: new Date().toISOString(),
          source_tool: "playwright-browser-ui", sha256, segment_count: segments.length,
        },
        null, 2
      ),
      "utf-8"
    );

    console.error(`[browser-ui] SUCCESS - ${segments.length} segments, transcript saved.`);
    console.log(`Transcript saved to: ${txtPath}`);
    console.log(`Metadata saved to: ${metaPath}`);
    console.log(`SHA-256 Hash: ${sha256}`);
    flushDebugLog();
    await browser.close();
    process.exit(0);
  } catch (err) {
    console.error(`[browser-ui] Unexpected error: ${err.message}`);
    writeFailure("unexpected_error", String(err.message || err));
    flushDebugLog();
    await browser.close().catch(() => {});
    process.exit(2);
  }
}

main();
