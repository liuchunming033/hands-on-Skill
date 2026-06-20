"""
从 body.pdf 中搜索章节标题，确定每个章节的实际起始页码。
使用 pdftotext 命令行工具（poppler-utils）提取文本，正确处理中文。
章节列表自动从 chapters/ 和 appendices/ 目录扫描，无需手动维护。

用法: python3 find-chapter-pages.py <body.pdf> <pages.json>
"""
import sys, os, re, json, subprocess

body_pdf_path = sys.argv[1]
output_json_path = sys.argv[2]

# 脚本所在目录 = 项目根（chapters/ 和 appendices/ 的父目录）
script_dir = os.path.dirname(os.path.abspath(__file__))


def build_search_list():
    """从 chapters/ 和 appendices/ 目录自动扫描章节，生成 (ch_id, keyword) 列表。"""
    entries = []

    def add_from_dir(subdir, id_pattern):
        dir_path = os.path.join(script_dir, subdir)
        if not os.path.isdir(dir_path):
            print(f"  ⚠ 目录不存在: {dir_path}")
            return
        for fname in sorted(os.listdir(dir_path)):
            if not fname.endswith('.md'):
                continue
            name = fname[:-3]  # 去 .md
            ch_id = id_pattern(name)
            if not ch_id:
                continue
            # 关键词：文件名在第一个分隔符之前的部分
            # 分隔符: ——(中文破折号), ——, ：, :, ？, ?
            keyword = re.split(r'[——：:？?]', name)[0].strip()
            entries.append((ch_id, keyword))

    add_from_dir('chapters', lambda n: f'ch{n[:2]}' if re.match(r'^\d{2}', n) else None)
    add_from_dir('appendices', lambda n: f'appendix{m.group(1)}' if (m := re.match(r'^附录(\d+)', n)) else None)

    return entries


CHAPTER_SEARCH = build_search_list()
print(f"  ✓ 从目录扫描到 {len(CHAPTER_SEARCH)} 个章节")

# 用 pdftotext 提取所有文本（form feed \f 分隔页面）
try:
    result = subprocess.run(
        ["pdftotext", body_pdf_path, "-"],
        capture_output=True, text=True
    )
except FileNotFoundError:
    print("❌ 未找到 pdftotext。请安装 poppler-utils：")
    print("   macOS:  brew install poppler")
    print("   Ubuntu: sudo apt-get install poppler-utils")
    sys.exit(1)
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
