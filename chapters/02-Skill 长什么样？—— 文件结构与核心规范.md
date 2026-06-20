
> 学习目标：掌握 Skill 最基本的文件组织和命名规则

---

## 引言

Skill 不是一个文件，而是一个文件夹。

很多人第一次写 Skill 就栽在命名上——用了大写、用了空格，结果上传失败。

我们先从最基础的文件夹结构说起。

---

## 📁 Skill 的标准文件结构

一套完整的 Skill 包含三类内容：

```
my-skill/
├── SKILL.md          # Required: 核心入口文件（必需）
├── scripts/          # Optional: 可执行脚本（可选）
├── references/       # Optional: 参考文档（可选）
├── assets/           # Optional: 资源文件（可选）
└── ...               # 任何其他文件或目录
```

---

## 🔍 逐个拆解

### 1. SKILL.md —— 核心入口（必需）

**这是每一个 Skill 的唯一核心入口，也是官方强制要求的必备文件。**

分为两大部分：

#### YAML Frontmatter（元数据）

**基本格式**：
```yaml
---
name: skill-name
description: 一句话描述技能功能和触发场景
---
```

**实际案例**：

**案例 1：follow-builders Skill**

```yaml
---
name: follow-builders
description: AI builders digest — monitors top AI builders on X and YouTube podcasts, remixes their content into digestible summaries. Use when the user wants AI industry insights, builder updates, or invokes /ai. No API keys or dependencies required — all content is fetched from a central feed.
---
```

**特点**：
- 描述包含功能（"monitors top AI builders"）
- 描述包含触发条件（"Use when the user wants AI industry insights"）
- 说明依赖情况（"No API keys required"）

**案例 2：飞书 Wiki 导入 Skill**

```yaml
---
name: feishu-wiki-to-obsidian
description: 将飞书知识库（Wiki）中的文档导入到本地 Obsidian Vault 的 raw/ 目录。自动获取文档 Markdown 内容、下载文档中的图片到本地 assets 目录、将图片引用替换为 Obsidian 标准语法 `![[文件名称.png]]`。当用户说"导入飞书文档"、"把飞书 Wiki 文章导入本地"、"拉取飞书文档到 Obsidian"或给出飞书 Wiki URL 并要求导入时触发。
---
```

**特点**：
- 描述详细说明功能（"导入到 raw/ 目录"）
- 描述列出具体触发关键词（"导入飞书文档"、"拉取飞书文档"）
- 描述包含 URL 场景（"给出飞书 Wiki URL 并要求导入"）

**案例 3：PDF 处理 Skill（Anthropic 官方示例）**

```yaml
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

**特点**：
- 第三人称描述（"Extracts"而非"I can"）
- 包含功能 + 触发场景
- 关键术语完整（PDF、forms、document extraction）

作用：
- 智能体启动时，会预加载所有 Skill 的元数据进入系统提示词
- 让 AI 只看一句话简介，就能判断「当前任务要不要用这个技能」
- 极致节省 Token，不需要加载全文就能做路由判断

#### 主体正文内容
完整的任务流程、操作规范、使用说明、注意事项。

作用：
- 当 AI 判断需要使用该技能时，才会加载完整这部分内容
- 指导 AI 完成标准作业

---

### 2. scripts/ —— 可执行脚本（可选）

存放 Python、Shell 等可运行代码。

作用：
- 替代低效的文本推演
- 让任务执行高效、稳定、可复现
- 提供确定性操作能力

典型内容：
- `analyze_form.py` — 分析 PDF 表单字段
- `validate_boxes.py` — 验证字段位置冲突
- `fill_form.py` — 填充 PDF 表单

---

### 3. references/ —— 参考文档（可选）

存放详细的参考文档、API 文档、使用指南等。

作用：
- 补充 SKILL.md 无法覆盖的详细说明
- AI 按需读取，不会默认加载
- 降低 SKILL.md 的 Token 消耗

典型内容：
- `api-reference.md` — API 详细文档
- `examples.md` — 使用示例
- `troubleshooting.md` — 问题排查指南

---

### 4. assets/ —— 资源文件（可选）

存放模板、配置文件、静态资源等。

作用：
- 提供标准化的输出模板
- 固化团队的配置规范
- 减少重复编写

典型内容：
- `report-template.md` — 报告模板
- `config.json` — 配置文件
- `diagrams/` — 流程图等

---

## 🚨 文件命名规范（必看）

### 文件夹命名

**必须使用 kebab-case（小写+连字符）**

```
✅ 正确：weekly-report、code-review、pdf-processing
❌ 错误：WeeklyReport、weekly report、weekly_report
```

**规则：**
- 全部小写字母
- 用连字符（-）分隔单词
- 不能用空格、下划线、大写

---

### SKILL.md 命名

**文件名必须是 `SKILL.md`（大写）**

```
✅ 正确：SKILL.md
❌ 错误：skill.md、Skill.md、README.md
```

---

### YAML Frontmatter 规范

#### name 字段
- 最多 64 个字符
- 只能包含小写字母、数字和连字符
- 不能包含 XML 标签
- 不能包含保留词：`anthropic`、`claude`

#### description 字段
- 必须非空
- 最多 1024 个字符
- 不能包含 XML 标签
- 应描述 Skill 的功能以及何时使用它

---

## 💡 实战示例：PDF 处理 Skill

Anthropic 的官方 PDF Skill 示例：

```
pdf/
├── SKILL.md              # 主文件：PDF 处理流程
├── FORMS.md              # 表单填充专属规则（按需加载）
├── scripts/
│   ├── analyze_form.py   # 分析表单字段
│   ├── fill_form.py      # 填充表单
│   └── validate.py       # 验证输出
└── references/
    └── pdf-spec.md       # PDF 技术规范
```

**关键设计：**
- `FORMS.md` 不会默认加载，只有做表单填充任务时才动态读取
- `scripts/` 提供确定性脚本，避免 AI 自己生成代码
- `references/` 存放详细技术文档，SKILL.md 只写核心流程

---

## 🎯 本节核心观点

**Skill 是文件夹体系，不是单一文件：**
- SKILL.md 是唯一核心入口（必需）
- scripts/、references/、assets/ 是可选扩展
- 命名必须用 kebab-case，不能乱写

**文件结构设计原则：**
- SKILL.md 写核心流程（5000 tokens 以内）
- 详细内容拆分到 references/
- 确定性操作放到 scripts/
- 模板配置放到 assets/

---

## 🔗 下节预告

下一节我们讲：「YAML Frontmatter 的精髓——写好 description 是成功的一半」

带你解决 Skill "该用不触发、不该用乱触发"的 90% 问题。

---

