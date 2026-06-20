/**
 * 用 Playwright (Chromium) 将 HTML 打印为 PDF。
 * 用法: node print-to-pdf.js <input.html> <output.pdf>
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const input = path.resolve(process.argv[2]);
  const output = path.resolve(process.argv[3]);

  if (!fs.existsSync(input)) {
    console.error(`❌ 文件不存在: ${input}`);
    process.exit(1);
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + input, { waitUntil: 'networkidle' });
  await page.pdf({
    path: output,
    format: 'A4',
    margin: { top: '2.5cm', right: '2.5cm', bottom: '2.5cm', left: '2.5cm' },
    printBackground: true
  });
  await browser.close();
  console.log(`  ✓ ${path.basename(output)}`);
})();
