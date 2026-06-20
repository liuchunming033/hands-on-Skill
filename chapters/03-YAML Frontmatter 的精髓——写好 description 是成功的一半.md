
> 学习目标：解决 Skill "该用不触发、不该用乱触发"的 90% 问题

---

## 引言

如果说 Skill 是一个开关，那 description 就是开关的感应器。

写得好，AI 自动识别场景；写得差，要么不触发，要么乱触发。

这一节教你写出高精度的触发描述。

---

## 📊 description 的核心作用

### 触发路由机制

智能体启动时，会预加载所有 Skill 的元数据（name + description）进入系统提示词。

AI 需要在上百个 Skill 中，只看一句话简介，就能判断：
- **当前任务要不要用这个技能**
- **什么时候该触发这个技能**

这就是 description 的核心作用：**路由触发规则**。

---

## ❌ 90% 的人写错了

### 错误写法 1：太被动

```yaml
description: "Generate weekly reports when asked."
```

**问题**：
- "when asked" 暗示需要用户明确点名才触发
- AI 不敢主动识别场景
- 导致大量漏触发

### 错误写法 2：太模糊

```yaml
description: "Helps with documents"
```

**问题**：
- "documents" 太泛，无法精准匹配场景
- AI 不知道什么时候该用
- 导致大量误触发和漏触发

### 错误写法 3：第一人称视角

```yaml
description: "I can help you process Excel files"
```

**问题**：
- description 会注入到系统提示词中
- 第一人称视角会导致发现问题
- Anthropic 强制要求第三人称编写

---

## ✅ 正确写法公式

### 核心公式

**好描述 = 做什么 + 何时用 + 触发关键词**

### 三个要素

#### 1. 做什么（功能）
清晰描述 Skill 的核心功能。

#### 2. 何时用（触发场景）
明确列出触发场景，帮助 AI 识别。

#### 3. 触发关键词（关键词匹配）
列出用户可能提到的关键词。

---

## 📝 实战示例

### 示例 1：周报生成 Skill

```yaml
✅ 正确：
description: "Generate professional weekly reports for individuals and teams.
Use when the user mentions '周报', 'weekly report', '本周总结', '工作汇报',
'团队周报', or wants to summarize work progress, even if they don't explicitly
ask for a 'report'."
```

**解析**：
- 做什么：Generate professional weekly reports
- 何时用：when user mentions "周报" / "weekly report" / "本周总结"...
- 触发关键词：完整列出所有可能的关键词
- 额外说明：even if they don't explicitly ask（主动识别）

---

### 示例 2：PDF 处理 Skill

```yaml
✅ 正确：
description: "Extract text and tables from PDF files, fill forms, merge documents.
Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
```

**解析**：
- 做什么：Extract text and tables、fill forms、merge documents
- 何时用：working with PDF files
- 触发关键词：PDFs、forms、document extraction

---

### 示例 3：Excel 分析 Skill

```yaml
✅ 正确：
description: "Analyze Excel spreadsheets, create pivot tables, generate charts.
Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files."
```

**解析**：
- 做什么：Analyze Excel、create pivot tables、generate charts
- 何时用：analyzing Excel files
- 触发关键词：Excel、spreadsheets、tabular data、.xlsx

---

## 💡 Perplexity 的最佳实践

Perplexity 建议以 **"Load when"** 开头：

```yaml
description: "Load when the user wants to generate commit messages by analyzing
git diffs, or when reviewing staged changes."
```

**优点**：
- "Load when" 更明确表达触发逻辑
- AI 能快速判断是否需要加载这个 Skill
- 风格统一，易于维护

---

## 🚨 强制规则（Anthropic 官方）

### 1. 必须第三人称编写

```yaml
✅ 正确："Processes Excel files and generates reports"
❌ 错误："I can help you process Excel files"
❌ 错误："You can use this to process Excel files"
```

原因：description 会注入到系统提示词中，第一人称视角会导致发现问题。

---

### 2. 不能包含 XML 标签

```yaml
✅ 正确："Generate weekly reports"
❌ 错误："Generate <weekly> reports"
```

---

### 3. 不能超过 1024 个字符

虽然限制是 1024，但建议控制在 200-300 字符以内，确保简洁高效。

---

## 🎯 description 写作 Checklist

在提交 Skill 前，检查你的 description：

□ 是否清晰描述功能（做什么）
□ 是否明确触发场景（何时用）
□ 是否列出触发关键词
□ 是否使用第三人称
□ 是否避免被动表述（"when asked"）
□ 是否避免第一人称（"I can"）
□ 是否避免模糊词汇（"helps with"）
□ 是否不超过 1024 字符
□ 是否不包含 XML 标签
□ 是否不包含保留词（"anthropic"、"claude")

---

## 📊 反面案例对比表

| 错误类型      | 错误示例                          | 正确示例                                                               |
| --------- | ----------------------------- | ------------------------------------------------------------------ |
| **太被动**   | "Generate reports when asked" | "Generate reports when user mentions 'report' or '汇报'"             |
| **太模糊**   | "Helps with documents"        | "Process PDF files, extract text, fill forms"                      |
| **第一人称**  | "I can help you..."           | "Processes Excel files..."                                         |
| **缺少关键词** | "Generate weekly reports"     | "Generate weekly reports when user mentions '周报', 'weekly report'" |

---

## 🎯 本节核心观点

**description 决定了 Skill 的触发精度：**
- 写得差 = 90% 的触发问题（漏触发、误触发）
- 写得好 = AI 自动识别场景，精准触发

**正确写法公式：做什么 + 何时用 + 触发关键词**

---

## 🔗 下节预告

下一节我们讲：「渐进式披露——Skill 碾压传统 Prompt 的核心设计原理」

带你理解 Skill 为什么能突破上下文窗口限制，比长 Prompt 更高效。

---

