"""
拼接独立 PDF 章节为完整教材，写入书签导航，并添加页码。
用法: python3 merge.py <build_dir> <output.pdf>
"""
import sys, os, io
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

build_dir = sys.argv[1]
output = sys.argv[2]

# 按文件名排序找到所有 PDF
pdf_files = sorted(
    [f for f in os.listdir(build_dir) if f.endswith('.pdf')]
)

writer = PdfWriter()
page_offset = 0
ch01_start_page = None  # 页码从 ch01 第一页开始

for pdf_file in pdf_files:
    path = os.path.join(build_dir, pdf_file)
    reader = PdfReader(path)

    # 提取标题
    meta = reader.metadata
    title = (meta.title or pdf_file).replace('.pdf', '')

    # 书签导航
    writer.add_outline_item(title, page_offset, parent=None)

    # 追加所有页面
    for page in reader.pages:
        writer.add_page(page)

    # 记录 ch01（第3个PDF，002-chapter.pdf）的起始页
    if '002-chapter' in pdf_file:
        ch01_start_page = page_offset

    page_offset += len(reader.pages)
    print(f"  ✓ [{len(reader.pages)}p] {title}")

total_pages = page_offset

# 为页面添加页码（从 ch01 开始，连续编号）
# 用 reportlab 生成极小画布（只含页码文字），merge_transformed_page 贴到页脚
# 小画布的白底仅覆盖页脚区域，不会影响正文
if ch01_start_page is not None:
    for page_num in range(ch01_start_page, total_pages):
        display_num = page_num - ch01_start_page + 1

        # 极小画布：宽 40pt，高 16pt，只够放一个页码数字
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(40, 16))
        can.setFont("Helvetica", 9)
        can.setFillColorRGB(0.55, 0.55, 0.55)
        can.drawCentredString(20, 2, str(display_num))
        can.save()
        packet.seek(0)

        overlay = PdfReader(packet).pages[0]

        # A4 底部居中：x = A4宽/2 - 20, y = 15pt（页脚区）
        transform = Transformation().translate(A4[0] / 2 - 20, 15)
        writer.pages[page_num].merge_transformed_page(overlay, transform, over=True)

        print(f"    p{display_num}  ", end="")
        if display_num % 20 == 0:
            print()

print()

# 写入输出
with open(output, 'wb') as f:
    writer.write(f)

print(f"✅ 共 {len(pdf_files)} 个章节，{total_pages} 页 → {output}")
