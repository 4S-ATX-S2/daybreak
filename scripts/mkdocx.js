const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewportSize:{width:1400,height:900}, deviceScaleFactor:3 });
  await p.goto('file:///home/claude/db/DaybreakBrief_DBS_20260905.html', { waitUntil:'networkidle' });
  await p.waitForTimeout(900);
  const el = await p.$('#arc');
  if (!el) { console.error('NO CHART ELEMENT'); process.exit(1); }
  await el.screenshot({ path:'chart_20260905.png' });
  console.log('chart rasterised');
  await b.close();
})();
