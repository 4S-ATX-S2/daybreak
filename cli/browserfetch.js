#!/usr/bin/env node
/*
 * browserfetch.js — the 403 fallback.
 *
 * Some Tier-1 sources (texassports.com row 20, the Hormuz tracker row 9) sit behind
 * bot protection and refuse a plain HTTP client with 403. They serve the same public
 * page to a real browser. Playwright/Chromium is already part of this pipeline
 * (render.js uses it for the PDFs), so no new dependency.
 *
 *   node browserfetch.js '<url>' [outfile]
 *
 * Prints the page's visible text to stdout; writes full HTML to outfile if given.
 * Exit 0 on success, 1 on failure. Never hangs past 45s.
 */
const { chromium } = require('playwright');
const fs = require('fs');

const url = process.argv[2];
const out = process.argv[3];
if (!url) { console.error('usage: browserfetch.js <url> [outfile]'); process.exit(1); }

(async () => {
  let browser;
  const timer = setTimeout(() => { console.error('TIMEOUT'); process.exit(1); }, 45000);
  try {
    // Honour an egress proxy when one is configured (cloud runners often have one;
    // a laptop normally has none, in which case this is a no-op).
    const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
    browser = await chromium.launch({
      args: ['--no-sandbox'],
      ...(proxy ? { proxy: { server: proxy } } : {}),
    });
    const ctx = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
                 '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
      viewport: { width: 1280, height: 1600 },
      locale: 'en-US', timezoneId: 'America/Chicago',
    });
    const page = await ctx.newPage();
    const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 35000 });
    await page.waitForTimeout(2500);               // let client-side calendars render
    const status = resp ? resp.status() : 0;
    const html = await page.content();
    let text = await page.evaluate(() => document.body ? document.body.innerText : '');
    if (/<\/?[a-z][\s\S]*>/i.test(text.slice(0, 400))) {      // page returned markup, not text
      text = text.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, ' ')
                 .replace(/<[^>]+>/g, ' ').replace(/&nbsp;?/g, ' ').replace(/\s+/g, ' ');
    }
    if (out) fs.writeFileSync(out, html);
    clearTimeout(timer);
    await browser.close();
    if (status >= 400) { console.error(`HTTP ${status}`); process.exit(1); }
    process.stdout.write(text.replace(/\n{3,}/g, '\n\n').slice(0, 200000));
    process.exit(0);
  } catch (e) {
    clearTimeout(timer);
    if (browser) await browser.close().catch(() => {});
    console.error(String(e.message || e));
    process.exit(1);
  }
})();
