const { chromium } = require('playwright-core');
const DATE = '20260905';
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  for (const kind of process.argv.slice(2)) {
    const f = `DaybreakBrief_${kind}_${DATE}.html`;
    await p.goto('file:///home/claude/db/' + f, { waitUntil: 'networkidle' });
    await p.emulateMedia({ media: 'print' });
    await p.waitForTimeout(900);
    await p.pdf({ path: `DaybreakBrief_${kind}_${DATE}.pdf`, format: 'Letter', printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' } });
    console.log('rendered', kind);
  }
  await b.close();
})();
