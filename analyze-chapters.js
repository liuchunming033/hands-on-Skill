/**
 * 分析组合 HTML 中各章节的页面位置。
 * 用法: node analyze-chapters.js <combined.html> <pages.json> [style.css]
 *
 * 输出 JSON: { "ch00": 5, "ch01": 8, ... }
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// A4 尺寸常量（CSS 像素，96dpi）
// A4: 210mm x 297mm，margin: top 1.5cm, bottom 2.5cm, left 2.5cm, right 2.5cm
// 内容区域: 160mm x 257mm
const CONTENT_WIDTH = Math.round(160 * 96 / 25.4);   // ~605px
const CONTENT_HEIGHT = Math.round(257 * 96 / 25.4);  // ~971px

(async () => {
  const input = path.resolve(process.argv[2]);
  const output = path.resolve(process.argv[3]);

  if (!fs.existsSync(input)) {
    console.error(`❌ 文件不存在: ${input}`);
    process.exit(1);
  }

  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage();

  // 设置 viewport 宽度匹配 PDF A4 内容区域宽度
  await page.setViewportSize({ width: CONTENT_WIDTH, height: 900 });
  await page.goto('file://' + input, { waitUntil: 'networkidle' });

  // 获取所有章节 section 的位置和高度
  const chapterData = await page.evaluate((pageContentHeight) => {
    const sections = document.querySelectorAll('section.chapter');
    const bodyRect = document.body.getBoundingClientRect();

    const result = [];
    let lastBottom = bodyRect.top; // 文档顶部

    for (const section of sections) {
      const rect = section.getBoundingClientRect();
      // 相对于文档顶部的 Y 位置
      const docTop = rect.top - bodyRect.top;
      result.push({
        id: section.id,
        docTop: docTop,
        height: rect.height,
      });
    }

    // 模拟 PDF 分页（page-break-before: always 强制每个 section 另起一页）
    let currentPage = 1;
    const pages = {};

    // 第一个 section 之前的内容（README）所占页数
    if (result.length > 0) {
      const readmeHeight = result[0].docTop;
      const readmePages = Math.ceil(readmeHeight / pageContentHeight);
      // 由于 section.chapter 有 page-break-before: always，第一个 section 另起一页
      currentPage = readmePages + 1;
    }

    for (const ch of result) {
      pages[ch.id] = currentPage;
      const sectionPages = Math.ceil(ch.height / pageContentHeight);
      currentPage += sectionPages;
    }

    return pages;
  }, CONTENT_HEIGHT);

  await browser.close();

  fs.writeFileSync(output, JSON.stringify(chapterData, null, 2));
  console.log(`  ✓ 章节页面映射已保存到 ${path.basename(output)}`);
  for (const [id, page] of Object.entries(chapterData)) {
    console.log(`    ${id}: 第 ${page} 页`);
  }
})();
