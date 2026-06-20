#!/bin/bash
set -e

VERSION="${1:-dev}"
OUTPUT="hands-on-skill-${VERSION}.pdf"
BUILD_DIR=".build-pdf"
TODAY=$(date +%Y-%m-%d)

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# 复制静态资源到构建目录
cp style.css "$BUILD_DIR/"
cp -r images "$BUILD_DIR/images"

# pandoc 选项（非 standalone，只生成 HTML 片段）
PANDOC_OPTS="--from=markdown+smart --to=html5 --no-highlight"

echo "📖 构建组合 HTML..."

# Step 1: 生成 README body HTML（去掉前3行，预处理列表空行）
tail -n +4 README.md | python3 normalize-md.py | pandoc $PANDOC_OPTS -o "$BUILD_DIR/README-body.html"

# Step 2: 用 Python 将 README 中的章节链接替换为内部锚点
python3 -c "
import re, sys

with open('$BUILD_DIR/README-body.html', 'r') as f:
    html = f.read()

# 替换章节链接: ./chapters/XX-...md → #chXX
html = re.sub(r'href=\"\./chapters/(\d{2})-[^\"]+\.md\"', r'href=\"#ch\1\"', html)

# 替换附录链接: ./appendices/附录N-...md → #appendixN
html = re.sub(r'href=\"\./appendices/附录(\d+)-[^\"]+\.md\"', r'href=\"#appendix\1\"', html)

with open('$BUILD_DIR/README-body.html', 'w') as f:
    f.write(html)
"

# Step 3: 初始化组合 HTML，写入头部和 README body
cat > "$BUILD_DIR/combined.html" << 'HEADER_EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="style.css">
</head>
<body>
HEADER_EOF

# 追加 README body
cat "$BUILD_DIR/README-body.html" >> "$BUILD_DIR/combined.html"
rm "$BUILD_DIR/README-body.html"

# Step 4: 逐章生成 HTML 片段，包裹在 <section class="chapter" id="chXX"> 中
INDEX=0
for f in \
  "chapters/00-导言——Agent架构全景：四大组件定位" \
  "chapters/01-为什么要学 Skill？—— 通用智能体的最后一公里" \
  "chapters/02-Skill 长什么样？—— 文件结构与核心规范" \
  "chapters/03-YAML Frontmatter 的精髓——写好 description 是成功的一半" \
  "chapters/04-渐进式披露——Skill 碾压传统 Prompt 的核心设计原理" \
  "chapters/05-三档自由度——如何把控指令的粗细粒度" \
  "chapters/06-心智模型跃迁——从写步骤到写决策框架" \
  "chapters/07-ToolWrapper 模式——按需注入知识" \
  "chapters/08-Generator 模式——固定输出结构" \
  "chapters/09-Reviewer 模式——分离审查与检查规则" \
  "chapters/10-Inversion 模式——先问清需求再开工" \
  "chapters/11-Pipeline 模式——分步执行流程" \
  "chapters/12-不写已知知识——Agent 已经很聪明" \
  "chapters/13-Gotchas 坑点——最有价值的内容是踩过的坑" \
  "chapters/14-文件组织与渐进式披露——Skill 是文件夹不是文件" \
  "chapters/15-避免过度约束——约束目标，不约束路径" \
  "chapters/16-设置流程与内存——让 Skill 有记忆" \
  "chapters/17-脚本——给 Agent 可调用的代码" \
  "chapters/18-按需 Hooks——临时规则，会话隔离" \
  "chapters/19-实战案例——从 0 到 1 写一个 Skill" \
  "chapters/20-为什么需要评估——两个维护面与核心转变" \
  "chapters/21-两类 Skill 分类——补能力还是固化偏好？" \
  "chapters/22-七步生命周期——从草稿到迭代闭环" \
  "chapters/23-两类评分器——确定性检查与评分细则检查" \
  "chapters/24-六类评估指标——量化Skill表现" \
  "chapters/25-A-B对比测试——持续验证与优化" \
  "chapters/26-Skill 的长期维护与团队管理" \
  "chapters/27-Skill 安全三原则——强大能力的风险管理" \
  "appendices/附录1-Anthropic 的 9 大 Skill 分类——团队能力诊断地图" \
  "appendices/附录2-OpenAI的Skill实践案例——代码助手能力构建" \
  "appendices/附录3-Superpowers开源Skill库——社区驱动的能力复用" \
  "appendices/附录4-addyosmani-agent-skills——生产级Skill工作流设计" \
  "appendices/附录5-garrytan-gstack——创业者导向的完整产品研发流程" \
  "appendices/附录6-google-skills——平台化产品的安全Agent入口设计" \
; do
  file="${f}.md"
  if [ -f "$file" ]; then
    basename=$(basename "$file" .md)

    # 生成章节 ID
    if [[ "$f" == appendices/* ]]; then
      # 附录: 提取数字 → appendix1, appendix2, ...
      appendix_num=$(echo "$basename" | grep -oE '^附录([0-9]+)' | grep -oE '[0-9]+')
      section_id="appendix${appendix_num}"
      chapter_title="附录${appendix_num}"
    else
      # 章节: 提取数字 → ch00, ch01, ch02, ...
      chapter_num=$(echo "$basename" | grep -oE '^[0-9]+')
      section_id="ch${chapter_num}"
      chapter_title="$basename"
    fi

    echo "  📄 [$section_id] $chapter_title"

    # 调整图片路径 + 预处理列表空行 → pandoc 生成 HTML 片段
    sed 's|(../images/|(images/|g' "$file" | python3 normalize-md.py | pandoc $PANDOC_OPTS -o "$BUILD_DIR/fragment.html"

    # 包裹在 <section class="chapter" id="chXX"> 中，追加到 combined.html
    echo "<section class=\"chapter\" id=\"$section_id\">" >> "$BUILD_DIR/combined.html"
    cat "$BUILD_DIR/fragment.html" >> "$BUILD_DIR/combined.html"
    echo "</section>" >> "$BUILD_DIR/combined.html"
    rm "$BUILD_DIR/fragment.html"
  fi
done

# 关闭 body 和 html 标签
echo "</body>" >> "$BUILD_DIR/combined.html"
echo "</html>" >> "$BUILD_DIR/combined.html"

echo ""
echo "🖨️  生成 PDF..."

# Step 5: 用 Playwright 打印组合 HTML 为 PDF
node print-to-pdf.js "$BUILD_DIR/combined.html" "$OUTPUT"

echo ""
echo "🔖 分析章节页面位置..."

# Step 6: 分析章节页面位置
node analyze-chapters.js "$BUILD_DIR/combined.html" "$BUILD_DIR/pages.json" "$BUILD_DIR/style.css"

echo ""
echo "🔖 添加书签与页码..."

# Step 7: 添加 PDF 书签和页码
python3 add-outline.py "$OUTPUT" "$BUILD_DIR/pages.json"

ls -lh "$OUTPUT"
rm -rf "$BUILD_DIR"
echo "✅ 完成: $OUTPUT"
