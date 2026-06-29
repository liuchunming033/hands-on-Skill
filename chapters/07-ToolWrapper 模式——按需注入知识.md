
> 学习目标：掌握如何让 Skill 在需要时才加载特定领域的知识，避免一次性塞满上下文

---

## 引言

当前 Skill 开发的核心痛点：

1. **格式标准化、无技术壁垒**：主流 AI 工具全部适配统一 Skill 规范，目录、YAML、文件结构不用再反复调试，新手也能快速搭出标准框架；参考https://agentskills.io/clients

2. **内容无规范、全靠经验**：官方只给“打包规则”，不给“内容设计规则”，绝大多数人写的 Skill 只是空有框架，逻辑混乱、执行不稳定、复用性极差；

3. **同质化外壳，差异化内核**：看似标准的 Skill 文件，内部工作流程、逻辑架构、执行精度完全取决于内容设计，这也是导致专业智能体的能力差距巨大的原因。

Google Cloud Tech 团队研究了 Anthropic、Vertex AI、Google 内部的大量 Skill 构建实践，他们发现：**问题不在格式，而在内容设计逻辑**。从海量官方落地案例中，总结的高频通用五种模式，覆盖绝大多数工作场景。

![五大模式概览](five-patterns-overview.png)

- Tool Wrapper：让您的代理瞬间成为任何库的专家。
    
- Generator: 从可重复使用的模板生成结构化文档。
    
- Reviewer: 根据严重程度对照清单对内容进行评分。
    
- Inversion: 代理人先对你进行询问再采取行动。
    
- Pipeline: 实施严格的多步骤工作流程并设置检查点。

今天我们先学习第一种设计模式：**ToolWrapper（按需注入知识）**。

---

## 📚 核心问题

**知识什么时候交给 Agent？**

很多团队的做法是：把所有技术栈规范、团队约定都提前塞进 SKILL.md。结果呢？

- 浪费 context，模型被撑死
- 信息过载，容易被干扰
- 不同领域的知识混在一起，混淆输出

---

## 💡 ToolWrapper 的解决方案
![ToolWrapper 模式](toolwrapper-pattern.png)

**核心思想**：把内容放进 references（参考文档），让 Skill 来判断当前任务是否进入某个领域。只有判断命中，才加载那一套知识。

举个例子：

你有个 Skill 专门处理前端开发。如果你把 React、Vue、Angular 三套规范都塞进 SKILL.md，模型会被撑死。但如果用 ToolWrapper 模式：

- Skill 先判断：当前任务是不是要写 React？
- 如果是，才把 React 规范加载进来
- 如果不是，就不加载

**本质**：Skill 像个总闸门，负责在合适的时候把某个专家手册接进上下文。

---

## 🔧 ToolWrapper SKILL.md 示例

**场景**：BigQuery 数据分析 Skill，按领域组织知识

**文件结构**：

```
bigquery-skill/
├── SKILL.md          # 总览和导航
└── reference/
    ├── finance.md    # 财务数据（revenue、billing metrics）
    ├── sales.md      # 销售数据（opportunities、pipeline）
    ├── product.md    # 产品数据（API usage、features）
    └── marketing.md  # 营销数据（campaigns、attribution）
```

**SKILL.md 内容**：

````markdown
---
name: bigquery-analysis
description: Analyze BigQuery data across finance, sales, product, and marketing domains. Use when querying BigQuery or analyzing business metrics.
---

# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)
**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)
**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)

## Quick search

Find specific metrics using grep:

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

**效果**：当用户问财务数据时，Agent 只加载 `reference/finance.md`，不加载其他文件，保持 context 干净。

---

## 📌 经典案例

### 案例：多语言代码审查助手

**场景**：一个代码审查 Skill，需要支持 Python、JavaScript、Go 三种语言的审查。

**问题**：如果将三种语言的风格指南、常见陷阱、最佳实践都塞进 SKILL.md，会导致：
- Context 占用超过 15000 tokens
- 不同语言的规则相互干扰
- Agent 容易混淆 Python 和 JavaScript 的语法

**ToolWrapper 方案**：

```
code-review/
├── SKILL.md              # 审查流程（通用部分）
└── references/
    ├── python-style.md   # Python 风格指南（PEP 8、类型注解）
    ├── javascript-style.md # JavaScript 风格指南（ES6+、异步模式）
    └── go-style.md       # Go 风格指南（错误处理、并发模式）
```

**SKILL.md 核心内容**：

```markdown
# 多语言代码审查

## 审查流程

1. 检测代码语言（通过文件扩展名或代码特征）
2. 加载对应语言的风格指南
3. 逐项检查并输出报告

## 语言识别与规则加载

- 检测到 `.py` 文件 → 加载 [references/python-style.md](references/python-style.md)
- 检测到 `.js/.ts` 文件 → 加载 [references/javascript-style.md](references/javascript-style.md)
- 检测到 `.go` 文件 → 加载 [references/go-style.md](references/go-style.md)

## 输出格式

统一输出：Errors / Warnings / Info 三级结构
```

**案例解析**：

1. **智能路由**：Agent 先识别语言，再加载对应规范，而不是全部加载
2. **Context 节省**：Python 项目审查只加载 python-style.md（约 3000 tokens），而不是全部三种语言（约 12000 tokens）
3. **避免干扰**：不会把 Python 的缩进规则和 Go 的花括号规则混在一起
4. **易于扩展**：新增 Rust 语言支持，只需添加 `references/rust-style.md`，SKILL.md 无需修改

**实际效果对比**：

| 方案 | Context 占用 | 准确率 | 维护成本 |
|------|-------------|--------|---------|
| 全部塞进 SKILL.md | 12000 tokens | 72%（容易混淆） | 高（牵一发动全身） |
| ToolWrapper 模式 | 3000 tokens | 94%（专注单一语言） | 低（独立更新） |

---

## ✅ 适用场景

- **技术栈规范**：React/Vue/Angular 不同框架规范
- **团队约定**：不同团队有不同编码风格
- **领域知识库**：财务/销售/产品等不同业务领域

---

## 🎯 本节核心观点

**ToolWrapper 模式的三个关键**：

1. **不要提前塞满**：把知识放进 references，而不是塞进 SKILL.md
2. **按需加载**：让 Skill 判断当前任务，动态加载对应领域知识
3. **保持 context 干净**：只加载任务所需的，不加载无关的

---

## 🔗 下节预告

下一节我们学习 **Generator 模式**：如何固定输出结构，解决"输出格式不稳定"的问题。

---

