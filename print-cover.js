/**
 * 用 Playwright (Chromium) 将 cover.html 打印为封面 PDF（1 页，无边距）。
 * cover.html 设计尺寸 1240x1754px（≈A4 @150dpi），通过 CSS zoom 缩放适配 A4。
 * 用法: node print-cover.js <cover.html> <output.pdf>
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// A4 尺寸：210mm × 297mm，96dpi 下 ≈ 794px × 1123px
// cover.html body：1240px × 1754px，缩放比 ≈ 794/1240 ≈ 0.64
const ZOOM = (210 * 96 / 25.4 / 1240).toFixed(6);  // ~0.640340

(async () => {
  const input = path.resolve(process.argv[2]);
  const output = path.resolve(process.argv[3]);

  if (!fs.existsSync(input)) {
    console.error(`❌ 文件不存在: ${input}`);
    process.exit(1);
  }

  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage();

  // viewport 大到够渲染（zoom 后实际占 794×1123）
  await page.setViewportSize({ width: 1240, height: 1754 });
  await page.goto('file://' + input, { waitUntil: 'networkidle' });

  // CSS zoom 缩放使内容恰好填充 A4
  await page.addStyleTag({ content: `body { zoom: ${ZOOM}; }` });

  await page.pdf({
    path: output,
    preferCSSPageSize: true,
    printBackground: true,
    displayHeaderFooter: false,
  });
  await browser.close();
  console.log(`  ✓ 封面: ${path.basename(output)}`);
})();
