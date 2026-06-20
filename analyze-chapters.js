/**
 * 分析组合 HTML 中各章节的页面位置，并捕获目录链接坐标。
 * 用法: node analyze-chapters.js <combined.html> <pages.json> <links.json>
 *
 * 输出 pages.json: { "ch00": 5, "ch01": 8, ... }
 * 输出 links.json: [ { targetId, targetPage, sourcePage, x, y, w, h }, ... ]
 *   - x, y, w, h 是 CSS 像素坐标，相对于 body 左上角
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
  const outputPages = path.resolve(process.argv[3]);
  const outputLinks = process.argv[4] ? path.resolve(process.argv[4]) : null;

  if (!fs.existsSync(input)) {
    console.error(`❌ 文件不存在: ${input}`);
    process.exit(1);
  }

  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage();

  // 设置 viewport 宽度匹配 PDF A4 内容区域宽度
  await page.setViewportSize({ width: CONTENT_WIDTH, height: 900 });
  await page.goto('file://' + input, { waitUntil: 'networkidle' });

  // 获取所有章节 section 的位置、封面高度、以及链接坐标
  const allData = await page.evaluate((pageContentHeight) => {
    const sections = document.querySelectorAll('section.chapter');
    const bodyRect = document.body.getBoundingClientRect();

    // ---- 章节数据 ----
    const chapterResult = [];
    for (const section of sections) {
      const rect = section.getBoundingClientRect();
      const docTop = rect.top - bodyRect.top;
      chapterResult.push({
        id: section.id,
        docTop: docTop,
        height: rect.height,
      });
    }

    // ---- 封面数据 ----
    let coverHeight = 0;
    let coverPages = 0;
    const coverDiv = document.querySelector('.cover-page');
    if (coverDiv) {
      coverHeight = coverDiv.getBoundingClientRect().height;
      coverPages = Math.max(1, Math.ceil(coverHeight / pageContentHeight));
    }

    // ---- 章节页码计算 ----
    let currentPage = 1;
    const pages = {};
    if (chapterResult.length > 0) {
      const readmeHeight = chapterResult[0].docTop - coverHeight;
      const readmePages = Math.ceil(readmeHeight / pageContentHeight);
      currentPage = coverPages + readmePages + 1;
    }
    for (const ch of chapterResult) {
      pages[ch.id] = currentPage;
      const sectionPages = Math.ceil(ch.height / pageContentHeight);
      currentPage += sectionPages;
    }

    // ---- 捕获链接坐标 ----
    const links = [];
    const linkElements = document.querySelectorAll('a[href^="#ch"], a[href^="#appendix"]');
    for (const el of linkElements) {
      const href = el.getAttribute('href'); // e.g. "#ch00"
      if (!href || href === '#') continue;
      const targetId = href.substring(1); // e.g. "ch00"
      const targetPage = pages[targetId];
      if (!targetPage) continue;

      const rect = el.getBoundingClientRect();
      const absY = rect.top - bodyRect.top;

      // 判断链接所在 PDF 页码
      let linkPage;
      if (absY < coverHeight) {
        // 链接在封面区域（基本不会发生）
        linkPage = Math.ceil(absY / pageContentHeight) || 1;
      } else {
        // 链接在 README 区域
        const readmeOffset = absY - coverHeight;
        linkPage = coverPages + 1 + Math.floor(readmeOffset / pageContentHeight);
      }

      links.push({
        targetId: targetId,
        targetPage: targetPage,
        sourcePage: linkPage,
        x: rect.left - bodyRect.left,
        y: absY,
        w: rect.width,
        h: rect.height,
      });
    }

    return {
      pages: pages,
      coverHeight: coverHeight,
      coverPages: coverPages,
      pageContentHeight: pageContentHeight,
      links: links,
    };
  }, CONTENT_HEIGHT);

  await browser.close();

  // 写入章节页面映射
  fs.writeFileSync(outputPages, JSON.stringify(allData.pages, null, 2));
  console.log(`  ✓ 章节页面映射已保存到 ${path.basename(outputPages)}`);
  for (const [id, pg] of Object.entries(allData.pages)) {
    console.log(`    ${id}: 第 ${pg} 页`);
  }

  // 写入链接数据
  if (outputLinks) {
    // 附加上下文数据用于坐标转换
    const linksData = {
      coverHeight: allData.coverHeight,
      coverPages: allData.coverPages,
      pageContentHeight: allData.pageContentHeight,
      links: allData.links,
    };
    fs.writeFileSync(outputLinks, JSON.stringify(linksData, null, 2));
    console.log(`  ✓ 链接坐标已保存到 ${path.basename(outputLinks)}`);
    console.log(`    共 ${allData.links.length} 个可点击链接`);
  }
})();
