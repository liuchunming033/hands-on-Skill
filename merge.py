"""
拼接独立 PDF 章节为完整教材，并写入书签导航。
用法: python3 merge.py <build_dir> <output.pdf>
"""
import sys, os
from pypdf import PdfReader, PdfWriter

build_dir = sys.argv[1]
output = sys.argv[2]

# 按文件名排序找到所有 PDF
pdf_files = sorted(
    [f for f in os.listdir(build_dir) if f.endswith('.pdf')]
)

writer = PdfWriter()
page_offset = 0  # 累计页码偏移

for pdf_file in pdf_files:
    path = os.path.join(build_dir, pdf_file)
    reader = PdfReader(path)

    # 提取标题
    meta = reader.metadata
    title = (meta.title or pdf_file).replace('.pdf', '')

    # 如果是 README，不编号，标题固定
    if 'README' in pdf_file:
        bookmark = writer.add_outline_item(title, page_offset, parent=None)
    else:
        bookmark = writer.add_outline_item(title, page_offset, parent=None)

    # 追加所有页面
    for page in reader.pages:
        writer.add_page(page)

    page_offset += len(reader.pages)
    print(f"  ✓ [{len(reader.pages)}p] {title}")

# 写入输出
with open(output, 'wb') as f:
    writer.write(f)

print(f"✅ 共 {len(pdf_files)} 个章节，{page_offset} 页 → {output}")
