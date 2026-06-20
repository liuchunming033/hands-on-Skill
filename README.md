# 上手 Skill —— Agent Skill 设计、实战与评估全指南

[English](./README.en.md) | 简体中文

> **教程简介**：从 0 到 1 掌握 Agent Skill 的完整体系——认知、设计、实战、评估、运营安全
> 
> **适合读者**：AI 工程师、产品经理、技术团队负责人
> 
>**阅读时长**：每章约 5 分钟，全书约 2.5 小时
> 
> **核心价值**：学会构建稳定可靠的 Agent 能力，让 AI 真正成为生产力工具

---

## 为什么会有这个教程

这本教程的产生，本身就是一个"Learn by Doing"的副产品。

2025 年，Agent Skill 的格式标准基本统一。但我在大量阅读 Anthropic、Google、OpenAI、社区开源库的 Skill 代码后，发现了一个反复出现的现象：**好的 Skill 不是"写一堆指令塞进去"，而是在用一套隐性的设计语言——什么时候加载知识、什么时候不加载、什么时候问用户、什么时候强制检查。** 

格式文档人人能读，但设计直觉没人教。我遵循的输入原则很简单：**follow builders, not influencers**（From 张咋啦）。这十几套参考代码库的作者——Garry Tan、Addy Osmani、Karpathy、OpenAI Codex 团队、Google Cloud 团队——都是亲手做产品、落地工具的实干者。

读完不是终点。我把这些设计模式逐一拆解、在自己的场景里验证、踩坑、修正，然后**用费曼法写出来**：把所有隐性知识显性化，讲清楚、讲通透。这不是一本官方文档的翻译，这是我"学到的、做到的、踩过坑的"完整记录。

所以有了这本教程。它是一门"做成的东西"，不是搬运的理论。

---

## 教程理念：动手学，公开做，持续迭代

### 底层信念：不被动假学习

单纯刷教程、看文档是"懒惰式学习"——永远停留在输入，永远不会真正掌握。这本教程的设计铁律是：**每一章你都能停下来，动手试一下。** 你不需要读完 27 章才开始写第一个 Skill，读完第 2 章就够。

教程的五篇结构，本质是一个缩小版的个人成长闭环：

```text
精输入（认知篇）→ 学模式（设计篇）→ 动手做（实战篇）→ 验证效果（评估篇）→ 沉淀体系（运营安全篇）
```

这个闭环不是理论推导出来的，它就是我自己摸索 Skill 的过程——先啃原始资料，再拆解模式，再动手写、跑评估、踩坑修正，最后把能复用的沉淀成体系。

### 设计原则

**MVP 驱动，不追求完美。** 每章约 5 分钟，给出 60 分完整可用的认知模块。先上线，根据反馈迭代——这和做产品的逻辑完全一样。持续产出远胜过一次性完美大作。

**把手弄脏，深度体验。** 教程里的每一条结论，都来自对真实 Skill 代码库的完整拆解——不是读别人写的评测，是自己打开 SKILL.md 一行一行看、跑、改、验证。

**内容即实践副产品。** 这本教程不是专门的"写教程项目"，而是我搭建 AI 工作流、研究 Agent 能力边界过程中自然产出的记录。真实踩坑经验比凭空编造的教程更有说服力。

**开放生态优先。** 全部参考案例来自公开开源仓库，不依赖任何闭源付费工具。普通人零成本就能复现全部学习路径。

### 这条路的终点不是"学会 Skill"

Skill 只是载体。你真正在培养的是**一种新的判断力**：能把模糊的工程经验，转化为 Agent 可稳定复用的能力单元。这种判断力不是靠背格式文档获得的，是靠精输入、动手做、费曼输出、持续迭代，一天一天积累出来的。

AI 时代的红利属于"会动手的实践者"。如果你只想知道格式怎么写，看 Anthropic 官方文档就够了。如果你想掌握"写一个好 Skill"的判断力和设计直觉，这本教程是为你准备的。

---

## 💡 教程特色

1. **真实案例驱动**：所有示例和分析来自公开开源 Skill 代码库
2. **渐进式学习**：从认知→设计→实战→评估→运营，循序渐进
3. **问题导向**：每章解决一个实际问题，5 分钟可读完
4. **普适性强**：适用于任何 Agent 平台，不局限于特定产品
5. **结构清晰**：27 章独立完整，可按需跳读

---

## 📚 教程结构（27 章 + 导言 + 附录）

### 导言

- [00-导言——Agent 架构全景：四大组件定位](./chapters/00-导言——Agent架构全景：四大组件定位.md) — Prompt / Skill / Subagent / MCP 的区别与定位

---

### 第一篇：认知篇

**目标**：建立 Skill 的基础认知框架

- [01-为什么要学 Skill？—— 通用智能体的最后一公里](./01-为什么要学%20Skill？——%20通用智能体的最后一公里.md) — Skill 的价值与必要性，从 prompt 到能力的跃迁
- [02-Skill 长什么样？—— 文件结构与核心规范](./02-Skill%20长什么样？——%20文件结构与核心规范.md) — 文件结构、命名规范、目录组织
- [03-YAML Frontmatter 的精髓——写好 description 是成功的一半](./03-YAML%20Frontmatter%20的精髓——写好%20description%20是成功的一半.md) — description 字段的核心作用与写法
- [04-渐进式披露——Skill 碾压传统 Prompt 的核心设计原理](./04-渐进式披露——Skill%20碾压传统%20Prompt%20的核心设计原理.md) — 三级加载机制，突破上下文限制
- [05-三档自由度——如何把控指令的粗细粒度](./chapters/05-三档自由度——如何把控指令的粗细粒度.md) — 高/中/低自由度的控制策略
- [06-心智模型跃迁——从写步骤到写决策框架](./chapters/06-心智模型跃迁——从写步骤到写决策框架.md) — 从"写 prompt"到"构建能力"的思维转变

---

### 第二篇：设计篇（五大设计模式）

**目标**：掌握 Skill 的核心设计模式，解决常见问题

- [07-ToolWrapper 模式——按需注入知识](./07-ToolWrapper%20模式——按需注入知识.md) — 按需加载领域知识，避免 context 过载
- [08-Generator 模式——固定输出结构](./08-Generator%20模式——固定输出结构.md) — 模板化输出，解决格式不稳定问题
- [09-Reviewer 模式——分离审查与检查规则](./09-Reviewer%20模式——分离审查与检查规则.md) — 流程与规则解耦，灵活替换
- [10-Inversion 模式——先问清需求再开工](./10-Inversion%20模式——先问清需求再开工.md) — 主动询问机制，避免盲目猜测
- [11-Pipeline 模式——分步执行流程](./11-Pipeline%20模式——分步执行流程.md) — Gate 机制，防止跳步骤

---

### 第三篇：实战篇

**目标**：学会编写真正有用的 Skill

- [12-不写已知知识——Agent 已经很聪明](./12-不写已知知识——Agent%20已经很聪明.md) — 补充 Agent 不知道的，而不是重复已知的
- [13-Gotchas 坑点——最有价值的内容是踩过的坑](./13-Gotchas%20坑点——最有价值的内容是踩过的坑.md) — 踩坑记录的价值，让 Skill 真正有用
- [14-文件组织与渐进式披露——Skill 是文件夹不是文件](./14-文件组织与渐进式披露——Skill%20是文件夹不是文件.md) — references 组织策略，实现精准加载
- [15-避免过度约束——约束目标，不约束路径](./chapters/15-避免过度约束——约束目标，不约束路径.md) — 给 Agent 足够的自由度，不要过度限制
- [16-设置流程与内存——让 Skill 有记忆](./16-设置流程与内存——让%20Skill%20有记忆.md) — config.json 与日志追加，让 Skill 有记忆
- [17-脚本——给 Agent 可调用的代码](./17-脚本——给%20Agent%20可调用的代码.md) — 封装稳定能力，避免重复造轮子
- [18-按需 Hooks——临时规则，会话隔离](./18-按需%20Hooks——临时规则，会话隔离.md) — PreToolUse hook，安全防护与监控
- [19-实战案例——从 0 到 1 写一个 Skill](./19-实战案例——从%200%20到%201%20写一个%20Skill.md) — 从 0 到 1 完整案例，整合所学

---

### 第四篇：评估篇

**目标**：建立 Skill 的质量保障体系

- [20-为什么需要评估——两个维护面与核心转变](./chapters/20-为什么需要评估——两个维护面与核心转变.md) — 没有评估的 Skill 只是假设
- [21-两类 Skill 分类——补能力还是固化偏好？](./21-两类%20Skill%20分类——补能力还是固化偏好？.md) — Capability Uplift vs Encoded Preference
- [22-七步生命周期——从草稿到迭代闭环](./chapters/22-七步生命周期——从草稿到迭代闭环.md) — 从草稿到迭代闭环的标准流程
- [23-两类评分器——确定性检查与评分细则检查](./chapters/23-两类评分器——确定性检查与评分细则检查.md) — 确定性检查与评分细则检查
- [24-六类评估指标——量化 Skill 表现](./chapters/24-六类评估指标——量化Skill表现.md) — 通过率、Token 消耗、执行时长、命令次数、重试率、错误分布
- [25-A-B 对比测试——持续验证与优化](./chapters/25-A-B对比测试——持续验证与优化.md) — 版本对比、开关对比、模型对比

---

### 第五篇：运营安全篇

**目标**：让 Skill 在团队中长期稳定运行

- [26-Skill 的长期维护与团队管理](./26-Skill%20的长期维护与团队管理.md) — 分发策略、市场机制、度量方法、依赖管理
- [27-Skill 安全三原则——强大能力的风险管理](./27-Skill%20安全三原则——强大能力的风险管理.md) — 权限控制、输入验证、依赖管理

---

### 附录

- [附录1-Anthropic 的 9 大 Skill 分类——团队能力诊断地图](./appendices/附录1-Anthropic%20的%209%20大%20Skill%20分类——团队能力诊断地图.md) — Anthropic 官方 Skill 类型分类体系（认知→生产→验证→交付）
- [附录2-OpenAI 的 Skill 实践案例——代码助手能力构建](./appendices/附录2-OpenAI的Skill实践案例——代码助手能力构建.md) — OpenAI Codex 真实 Skill 库（持续监控 + Subagent 并行审查 + 注意力量化 + 失败路径设计）
- [附录3-Superpowers 开源 Skill 库——社区驱动的能力复用](./appendices/附录3-Superpowers开源Skill库——社区驱动的能力复用.md) — 社区驱动完整工程纪律系统（Red Flags 表 + Iron Law + Hard Gate + 文件传递 + Progress Ledger）
- [附录4-addyosmani-agent-skills——生产级 Skill 工作流设计](./appendices/附录4-addyosmani-agent-skills——生产级Skill工作流设计.md) — Google 工程总监 Addy Osmani 的生产级 Skill 工作流库
- [附录5-garrytan-gstack——创业者导向的完整产品研发流程](./appendices/附录5-garrytan-gstack——创业者导向的完整产品研发流程.md) — YC 总裁 Garry Tan 的单人全栈工程体系（四大基石：Ethos 注入 + preamble-tier 编排 + Preamble Bash + GBrain Schema 跨会话记忆）
- [附录6-google-skills——平台化产品的安全 Agent 入口设计](./appendices/附录6-google-skills——平台化产品的安全Agent入口设计.md) — Google 官方 Skill 库，35 个云端产品 Skill（安全护栏 + 数据缩减 + 强制前置验证 + 渐进式加载）

---

## 🎯 学习路径建议

### 路径一：快速入门（1 小时）

适合：想快速了解 Skill 基本概念的读者

1. 导言 → 第 1 节 → 第 2 节 → 第 3 节
2. 第 7 节 → 第 8 节 → 第 12 节

### 路径二：完整掌握（2.5 小时）

适合：需要系统学习 Skill 构建的读者

1. 按顺序阅读所有节
2. 重点理解设计篇和实战篇
3. 实践：跟随第 19 节完成一个 Skill

### 路径三：特定问题解决（30 分钟）

适合：遇到特定问题需要解决方案的读者

| 问题类型 | 推荐小节 |
|---------|---------|
| Skill 不触发 | 第 3 节 |
| 输出不稳定 | 第 8 节 |
| Context 过载 | 第 7 节、第 14 节 |
| 审查规则混乱 | 第 9 节 |
| Agent 盲目猜测 | 第 10 节 |
| 跳步骤 | 第 11 节 |
| 没有记忆 | 第 16 节 |
| 不知道如何评估 | 第 20-25 章 |

---

## 🔗 外部参考链接

教程中分析引用的全部代码仓库和参考资源：

- [Anthropic Agent Skills 官方文档](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
- [Claude Code Skills 文档](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Google ADK — Skill 设计模式](https://github.com/google/adk-python)
- [Google Skills 代码库](https://github.com/google/skills) — 35 个云端产品 Skill
- [OpenAI Codex Skills 代码库](https://github.com/openai/codex/tree/main/.codex/skills) — Codex 的 Skill 实践
- [Superpowers 开源 Skill 库](https://github.com/obra/superpowers) — 社区驱动的工程纪律系统
- [gstack 代码库](https://github.com/garrytan/gstack) — Garry Tan 的单人全栈工程体系
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — 生产级 Skill 工作流设计
- [Karpathy — LLM Wiki 规范](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [AgentSkills.io](https://agentskills.io) — Skill 格式标准与客户端兼容列表
- [Anthropic — The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)

---

## 📄 License

MIT License — 详见 [LICENSE](./LICENSE) 文件。

