#!/bin/bash
set -e

VERSION="${1:-dev}"
OUTPUT="hands-on-skill-${VERSION}.pdf"
TMP_MD=".tmp-merged.md"
TODAY=$(date +%Y-%m-%d)

echo "📖 合并章节..."

# 生成合并文件头部
cat > "$TMP_MD" << TITLEEOF
---
title: "上手 Skill —— Agent Skill 设计、实战与评估全指南"
author: "liuchunming"
date: "$TODAY"
documentclass: ctexart
geometry: "a4paper, margin=2.5cm"
fontsize: 11pt
toc: true
toc-depth: 1
numbersections: true
---

\newpage

# 课程介绍 {.unnumbered}

TITLEEOF

# 引入 README.md 作为课程介绍（跳过标题和语言切换行）
tail -n +4 README.md >> "$TMP_MD"

cat >> "$TMP_MD" << PAGEEOF

\newpage

\pagenumbering{arabic}

PAGEEOF

# 按课程顺序合并正文章节
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
  "appendices/附录-Anthropic 的 9 大 Skill 分类——团队能力诊断地图" \
  "appendices/附录-OpenAI的Skill实践案例——代码助手能力构建" \
  "appendices/附录-Superpowers开源Skill库——社区驱动的能力复用" \
  "appendices/附录-addyosmani-agent-skills——生产级Skill工作流设计" \
  "appendices/附录-garrytan-gstack——创业者导向的完整产品研发流程" \
  "appendices/附录-google-skills——平台化产品的安全Agent入口设计" \
; do
  file="${f}.md"
  if [ -f "$file" ]; then
    # 提取文件名并去掉数字前缀作为章节标题
    basename="${f##*/}"
    # 去掉 "00-"-"27-" 数字前缀，附录前缀保留
    title=$(echo "$basename" | sed 's/^[0-9]\{2\}-//')
    echo "" >> "$TMP_MD"
    echo "\\newpage" >> "$TMP_MD"
    echo "" >> "$TMP_MD"
    echo "# $title" >> "$TMP_MD"
    echo "" >> "$TMP_MD"
    cat "$file" >> "$TMP_MD"
    echo "" >> "$TMP_MD"
    echo "  ✓ ${f}"
  else
    echo "  ✗ 跳过: $file (不存在)"
  fi
done

# 修复图片路径: ../images/ → images/ (合并后从根目录引用)
sed -i '' 's|](../images/|](images/|g' "$TMP_MD" 2>/dev/null || sed -i 's|](../images/|](images/|g' "$TMP_MD"

echo ""
echo "📄 生成 PDF: $OUTPUT"

pandoc "$TMP_MD" \
  --pdf-engine=xelatex \
  --from=markdown+smart \
  --toc --toc-depth=1 \
  --number-sections \
  --highlight-style=tango \
  -V colorlinks=true \
  -V linkcolor=blue \
  -o "$OUTPUT"

ls -lh "$OUTPUT"
rm "$TMP_MD"
echo "✅ 完成: $OUTPUT"
