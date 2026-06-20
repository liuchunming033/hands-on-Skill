"""
合并封面与正文 PDF，添加书签导航、页码和内链跳转。
用法: python3 add-outline.py <body.pdf> <pages.json> <links.json> <cover.pdf> <output.pdf>
"""
import sys, io, json
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

body_pdf_path = sys.argv[1]
pages_json_path = sys.argv[2]
cover_pdf_path = sys.argv[3] if len(sys.argv) > 3 else None
output_pdf_path = sys.argv[4] if len(sys.argv) > 4 else body_pdf_path

# ---- PDF 坐标常量 ----
PAGE_W = 595.28
PAGE_H = 841.89

# ---- 章节标题映射 ----
CHAPTER_TITLES = {
    "ch00": "导言——Agent架构全景：四大组件定位",
    "ch01": "为什么要学 Skill？——通用智能体的最后一公里",
    "ch02": "Skill 长什么样？——文件结构与核心规范",
    "ch03": "YAML Frontmatter 的精髓——写好 description 是成功的一半",
    "ch04": "渐进式披露——Skill 碾压传统 Prompt 的核心设计原理",
    "ch05": "三档自由度——如何把控指令的粗细粒度",
    "ch06": "心智模型跃迁——从写步骤到写决策框架",
    "ch07": "ToolWrapper 模式——按需注入知识",
    "ch08": "Generator 模式——固定输出结构",
    "ch09": "Reviewer 模式——分离审查与检查规则",
    "ch10": "Inversion 模式——先问清需求再开工",
    "ch11": "Pipeline 模式——分步执行流程",
    "ch12": "不写已知知识——Agent 已经很聪明",
    "ch13": "Gotchas 坑点——最有价值的内容是踩过的坑",
    "ch14": "文件组织与渐进式披露——Skill 是文件夹不是文件",
    "ch15": "避免过度约束——约束目标，不约束路径",
    "ch16": "设置流程与内存——让 Skill 有记忆",
    "ch17": "脚本——给 Agent 可调用的代码",
    "ch18": "按需 Hooks——临时规则，会话隔离",
    "ch19": "实战案例——从 0 到 1 写一个 Skill",
    "ch20": "为什么需要评估——两个维护面与核心转变",
    "ch21": "两类 Skill 分类——补能力还是固化偏好？",
    "ch22": "七步生命周期——从草稿到迭代闭环",
    "ch23": "两类评分器——确定性检查与评分细则检查",
    "ch24": "六类评估指标——量化Skill表现",
    "ch25": "A-B对比测试——持续验证与优化",
    "ch26": "Skill 的长期维护与团队管理",
    "ch27": "Skill 安全三原则——强大能力的风险管理",
    "appendix1": "Anthropic 的 9 大 Skill 分类——团队能力诊断地图",
    "appendix2": "OpenAI 的 Skill 实践案例——代码助手能力构建",
    "appendix3": "Superpowers 开源 Skill 库——社区驱动的能力复用",
    "appendix4": "addyosmani-agent-skills——生产级Skill工作流设计",
    "appendix5": "garrytan-gstack——创业者导向的完整产品研发流程",
    "appendix6": "google-skills——平台化产品的安全Agent入口设计",
}

# ---- 读取数据 ----
with open(pages_json_path) as f:
    chapter_pages = json.load(f)  # 1-based, 正文内部页码

# ---- 合并 PDF ----
writer = PdfWriter()
cover_page_count = 0

if cover_pdf_path:
    cover_reader = PdfReader(cover_pdf_path)
    for page in cover_reader.pages:
        writer.add_page(page)
    cover_page_count = len(cover_reader.pages)
    print(f"  ✓ 合并封面: {cover_page_count} 页")

body_reader = PdfReader(body_pdf_path)
body_page_count = len(body_reader.pages)
for page in body_reader.pages:
    writer.add_page(page)
print(f"  ✓ 合并正文: {body_page_count} 页")

total_pages = cover_page_count + body_page_count

# 封面偏移量：正文页码 → 合并后页码的偏移
PAGE_OFFSET = cover_page_count  # 1（封面占 1 页）

# ---- 添加书签导航 ----
outline_items = []
for ch_id, ch_page in sorted(chapter_pages.items(), key=lambda x: x[1]):
    title = CHAPTER_TITLES.get(ch_id, ch_id)
    if ch_id.startswith("appendix"):
        num = ch_id.replace("appendix", "")
        numbered_title = f"附录{num} {title}"
    elif ch_id.startswith("ch"):
        num = ch_id[2:]
        numbered_title = f"{num} {title}"
    else:
        numbered_title = title
    # 正文页码 + 封面偏移 = 合并后页码
    outline_items.append((ch_page + PAGE_OFFSET, numbered_title))

for ch_page, title in outline_items:
    page_offset = ch_page - 1  # 0-based
    if page_offset < total_pages:
        writer.add_outline_item(title, page_offset, parent=None)
        print(f"  ✓ 书签: [{ch_page}] {title}")

# ---- 注册命名目标 ----
# Chromium 已将 HTML <a href="#chXX"> 转为 PDF 命名目标链接，
# 注册命名目标使这些链接在合并后的 PDF 中正确跳转。
print("  ✓ 注册命名目标...")
for ch_id, ch_page in chapter_pages.items():
    writer.add_named_destination(ch_id, ch_page - 1 + PAGE_OFFSET)
    print(f"    {ch_id} → 第 {ch_page + PAGE_OFFSET} 页")

# ---- 添加页码 ----
ch00_body_page = chapter_pages.get("ch00")
if ch00_body_page is None:
    ch00_body_page = min(chapter_pages.values()) if chapter_pages else 1

# ch00 在合并后 PDF 中的页码（1-based）
ch00_merged_page = ch00_body_page + PAGE_OFFSET

for page_num in range(ch00_merged_page - 1, total_pages):
    display_num = page_num - (ch00_merged_page - 1) + 1

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(40, 16))
    can.setFont("Helvetica", 9)
    can.setFillColorRGB(0.55, 0.55, 0.55)
    can.drawCentredString(20, 2, str(display_num))
    can.save()
    packet.seek(0)

    overlay = PdfReader(packet).pages[0]
    transform = Transformation().translate(PAGE_W / 2 - 20, 15)
    writer.pages[page_num].merge_transformed_page(overlay, transform, over=True)

    if display_num % 20 == 0:
        print(f"    页码已添加至第 {display_num} 页")

# ---- 写入输出 ----
with open(output_pdf_path, 'wb') as f:
    writer.write(f)

print(f"✅ 共 {len(chapter_pages)} 个书签，页码从 ch00（第 {ch00_merged_page} 页）开始，总计 {total_pages} 页")
