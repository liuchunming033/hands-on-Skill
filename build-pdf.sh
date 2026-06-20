#!/bin/bash
set -e

VERSION="${1:-dev}"
OUTPUT="hands-on-skill-${VERSION}.pdf"
TMP_MD=".tmp-merged.md"
TODAY=$(date +%Y-%m-%d)

echo "📖 合并章节..."

cat > "$TMP_MD" << TITLEEOF
---
title: "上手 Skill —— Agent Skill 设计、实战与评估全指南"
author: "liuchunming"
date: "$TODAY"
documentclass: ctexart
geometry: "a4paper, margin=2.5cm"
fontsize: 11pt
toc: true
toc-depth: 2
numbersections: true
---

\pagenumbering{Roman}

# 课程介绍

**上手 Skill** 是一门从 0 到 1 掌握 Agent Skill 的完整教程，覆盖认知、设计、实战、评估与运营安全五大环节。

课程核心理念：**不是搬运理论，是真实踩坑的完整记录**。

\newpage

\pagenumbering{arabic}

TITLEEOF

# 按课程顺序合并正文章节
for f in \
  "00-导言——Agent架构全景：四大组件定位" \
  "01-为什么要学 Skill？—— 通用智能体的最后一公里" \
  "02-Skill 长什么样？—— 文件结构与核心规范" \
  "03-YAML Frontmatter 的精髓——写好 description 是成功的一半" \
  "04-渐进式披露——Skill 碾压传统 Prompt 的核心设计原理" \
  "05-三档自由度——如何把控指令的粗细粒度" \
  "06-心智模型跃迁——从写步骤到写决策框架" \
  "07-ToolWrapper 模式——按需注入知识" \
  "08-Generator 模式——固定输出结构" \
  "09-Reviewer 模式——分离审查与检查规则" \
  "10-Inversion 模式——先问清需求再开工" \
  "11-Pipeline 模式——分步执行流程" \
  "12-不写已知知识——Agent 已经很聪明" \
  "13-Gotchas 坑点——最有价值的内容是踩过的坑" \
  "14-文件组织与渐进式披露——Skill 是文件夹不是文件" \
  "15-避免过度约束——约束目标，不约束路径" \
  "16-设置流程与内存——让 Skill 有记忆" \
  "17-脚本——给 Agent 可调用的代码" \
  "18-按需 Hooks——临时规则，会话隔离" \
  "19-实战案例——从 0 到 1 写一个 Skill" \
  "20-为什么需要评估——两个维护面与核心转变" \
  "21-两类 Skill 分类——补能力还是固化偏好？" \
  "22-七步生命周期——从草稿到迭代闭环" \
  "23-两类评分器——确定性检查与评分细则检查" \
  "24-六类评估指标——量化Skill表现" \
  "25-A-B对比测试——持续验证与优化" \
  "26-Skill 的长期维护与团队管理" \
  "27-Skill 安全三原则——强大能力的风险管理" \
  "附录-Anthropic 的 9 大 Skill 分类——团队能力诊断地图" \
  "附录-OpenAI的Skill实践案例——代码助手能力构建" \
  "附录-Superpowers开源Skill库——社区驱动的能力复用" \
  "附录-addyosmani-agent-skills——生产级Skill工作流设计" \
  "附录-garrytan-gstack——创业者导向的完整产品研发流程" \
  "附录-google-skills——平台化产品的安全Agent入口设计" \
; do
  file="${f}.md"
  if [ -f "$file" ]; then
    echo "" >> "$TMP_MD"
    cat "$file" >> "$TMP_MD"
    echo "" >> "$TMP_MD"
    echo "  ✓ ${f}"
  else
    echo "  ✗ 跳过: $file (不存在)"
  fi
done

# 清理 Obsidian 图片语法残留 (转义 [[ 为 ![])
sed -i '' 's/!\[\[\([^]]*\)\]\]/![](\1)/g' "$TMP_MD" 2>/dev/null || sed -i 's/!\[\[\([^]]*\)\]\]/![](\1)/g' "$TMP_MD"

echo ""
echo "📄 生成 PDF: $OUTPUT"

pandoc "$TMP_MD" \
  --pdf-engine=xelatex \
  --from=markdown+smart \
  --toc --toc-depth=2 \
  --number-sections \
  --highlight-style=tango \
  -V colorlinks=true \
  -V linkcolor=blue \
  -o "$OUTPUT"

ls -lh "$OUTPUT"
rm "$TMP_MD"
echo "✅ 完成: $OUTPUT"
