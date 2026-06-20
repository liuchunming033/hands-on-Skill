"""
为 PDF 添加书签导航和页码。
用法: python3 add-outline.py <input.pdf> <pages.json>
"""
import sys, io, json
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

pdf_path = sys.argv[1]
pages_json_path = sys.argv[2]

# 读取章节页面映射
with open(pages_json_path) as f:
    chapter_pages = json.load(f)

# 章节标题映射（用于书签显示名称）
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
    "appendix1": "附录1-Anthropic 的 9 大 Skill 分类",
    "appendix2": "附录2-OpenAI 的 Skill 实践案例",
    "appendix3": "附录3-Superpowers 开源 Skill 库",
    "appendix4": "附录4-addyosmani-agent-skills",
    "appendix5": "附录5-garrytan-gstack",
    "appendix6": "附录6-google-skills",
}

# 读取 PDF
reader = PdfReader(pdf_path)
total_pages = len(reader.pages)
writer = PdfWriter()

# 追加所有页面
for page in reader.pages:
    writer.add_page(page)

# 添加书签导航（大纲）
# chapter_pages 中的页码是 1-based
for ch_id, ch_page in sorted(chapter_pages.items(), key=lambda x: x[1]):
    title = CHAPTER_TITLES.get(ch_id, ch_id)
    # page_offset 是 0-based
    page_offset = ch_page - 1
    if page_offset < total_pages:
        writer.add_outline_item(title, page_offset, parent=None)
        print(f"  ✓ 书签: [{ch_page}] {title}")

# 添加页码（从第一章 ch00 首页开始连续编号）
ch00_page = chapter_pages.get("ch00")
if ch00_page is None:
    # fallback: 使用第一个章节
    ch00_page = min(chapter_pages.values()) if chapter_pages else 1

for page_num in range(ch00_page - 1, total_pages):  # ch00_page 是 1-based
    display_num = page_num - (ch00_page - 1) + 1  # ch00 首页为 1

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

    if display_num % 20 == 0:
        print(f"    页码已添加至第 {display_num} 页")

# 写入输出
with open(pdf_path, 'wb') as f:
    writer.write(f)

print(f"✅ 共 {len(chapter_pages)} 个书签，页码从 ch00（第 {ch00_page} 页）开始，总计 {total_pages} 页")
