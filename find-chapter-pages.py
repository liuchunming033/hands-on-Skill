"""
从 body.pdf 中搜索章节标题，确定每个章节的实际起始页码。
使用 pdftotext 命令行工具（poppler-utils）提取文本，正确处理中文。
用法: python3 find-chapter-pages.py <body.pdf> <pages.json>
"""
import sys, json, subprocess

body_pdf_path = sys.argv[1]
output_json_path = sys.argv[2]

# 章节搜索关键词 — 使用 "数字-标题" 格式确保唯一性
# （README 目录中用 "数字 标题" 空格格式，不会误匹配）
CHAPTER_SEARCH = [
    ("ch00", "00-导言"),
    ("ch01", "01-为什么要学 Skill"),
    ("ch02", "02-Skill 长什么样"),
    ("ch03", "03-YAML Frontmatter 的精髓"),
    ("ch04", "04-渐进式披露"),
    ("ch05", "05-三档自由度"),
    ("ch06", "06-心智模型跃迁"),
    ("ch07", "07-ToolWrapper 模式"),
    ("ch08", "08-Generator 模式"),
    ("ch09", "09-Reviewer 模式"),
    ("ch10", "10-Inversion 模式"),
    ("ch11", "11-Pipeline 模式"),
    ("ch12", "12-不写已知知识"),
    ("ch13", "13-Gotchas 坑点"),
    ("ch14", "14-文件组织与渐进式披露"),
    ("ch15", "15-避免过度约束"),
    ("ch16", "16-设置流程与内存"),
    ("ch17", "17-脚本"),
    ("ch18", "18-按需 Hooks"),
    ("ch19", "19-实战案例"),
    ("ch20", "20-为什么需要评估"),
    ("ch21", "21-两类 Skill 分类"),
    ("ch22", "22-七步生命周期"),
    ("ch23", "23-两类评分器"),
    ("ch24", "24-六类评估指标"),
    ("ch25", "25-A-B对比测试"),
    ("ch26", "26-Skill 的长期维护与团队管理"),
    ("ch27", "27-Skill 安全三原则"),
    ("appendix1", "附录1-Anthropic"),
    ("appendix2", "附录2-OpenAI"),
    ("appendix3", "附录3-Superpowers"),
    ("appendix4", "附录4-addyosmani"),
    ("appendix5", "附录5-garrytan"),
    ("appendix6", "附录6-google-skills"),
]

# 用 pdftotext 提取所有文本（form feed \f 分隔页面）
result = subprocess.run(
    ["pdftotext", body_pdf_path, "-"],
    capture_output=True, text=True
)
if result.returncode != 0:
    print(f"❌ pdftotext 失败: {result.stderr}")
    sys.exit(1)

pages = result.stdout.split("\f")
total_pages = len(pages)
print(f"  ✓ 正文 PDF 共 {total_pages} 页")

chapter_pages = {}

for ch_id, keyword in CHAPTER_SEARCH:
    found = False
    # 倒序搜索：最后一次出现 = 实际章节标题（README 目录在前面）
    for page_num in range(total_pages - 1, -1, -1):
        if keyword in pages[page_num]:
            chapter_pages[ch_id] = page_num + 1  # 1-based
            found = True
            print(f"  ✓ {ch_id} → 第 {page_num + 1} 页")
            break
    if not found:
        print(f"  ⚠ {ch_id} 未找到（搜索: {keyword}）")

with open(output_json_path, 'w') as f:
    json.dump(chapter_pages, f, ensure_ascii=False, indent=2)

print(f"✅ 找到 {len(chapter_pages)}/{len(CHAPTER_SEARCH)} 个章节")
