const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewportSize:{width:1500,height:900}, deviceScaleFactor:3 });
  await p.goto('file:///home/claude/db/DaybreakBrief_FULL_20260905.html', { waitUntil:'networkidle' });
  await p.waitForTimeout(600);
  const el = await p.$('.map-wrap svg');
  if(!el){console.error('NO MAP');process.exit(1);}
  await el.screenshot({ path:'map_20260905.png' });
  console.log('map rasterised');
  await b.close();
})();
