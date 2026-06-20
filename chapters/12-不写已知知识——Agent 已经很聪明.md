
> 学习目标：理解Skill应该补充什么，而不是重复Agent已知的内容

---


## 引言

很多人写 Skill 有个误区：写得越多越好。

结果呢？SKILL.md 动辄几千字，教 Agent 怎么写代码、怎么设计架构、怎么写文档。

问题是：**这些 Agent 本来就会**。

你写的越多，浪费的 context 越多，反而容易干扰 Agent 的判断。

## 核心内容

### Agent 已经知道什么？

Agent 经过大量训练，已经具备：

- **通用编程知识**：语法、设计模式、最佳实践
- **常见框架用法**：React、Vue、Django、Spring 等
- **标准文档规范**：README、API 文档、commit message 格式
- **通用调试技巧**：常见错误、排查思路

### 你应该补充什么？

**只有 Agent 默认不知道的东西**：

| 类型 | 示例 |
|------|------|
| **团队约定** | "我们团队不用 Inter 字体和紫色渐变" |
| **内部规范** | "API 返回格式必须包含 code、data、message 三个字段" |
| **业务上下文** | "用户状态有三种：active、pending、suspended" |
| **踩过的坑** | "这个 API 在 Q4 流量高峰会超时，要加重试逻辑" |

### Anthropic 内部案例

**问题**：Agent 生成的前端界面总是用 Inter 字体和紫色渐变，看起来很"AI味"，客户不喜欢。

**错误做法**：写一大堆教程教 Agent 怎么设计界面。

**正确做法**：只写一件事——"别再用 Inter 和紫色渐变，客户不喜欢"。

**效果**：几句话解决问题，不需要教 Agent 怎么写 React。

### 审视每一条内容

写 Skill 时，对每一条内容问三个问题：

1. **Agent 真的需要这个吗？**
2. **Agent 本来就知道吗？**
3. **这段内容值得它的 token 成本吗？**

如果答案是"Agent 已经知道"，**删掉**。

### 对比示例

**错误写法（约 150 tokens）**：

```markdown
## PDF 处理

PDF（Portable Document Format）是一种常见的文件格式，包含文本、图像等内容。要提取 PDF 中的文本，需要使用专门的库。有很多库可以处理 PDF，推荐使用 pdfplumber，因为它易用且效果好。首先需要安装它...

import pdfplumber
```

**正确写法（约 50 tokens）**：

```markdown
## 提取 PDF 文本

使用 pdfplumber：

import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

简洁版本假设 Agent 已经知道什么是 PDF、库的工作原理。

### 核心原则

**补充未知，不重复已知。**

Skill 的价值在于补充 Agent 默认不知道的：

- 上下文（Context）
- 偏好（Preference）
- 坑点（Gotchas）

而不是重复 Agent 已经掌握的通用知识。

## 总结

今天我们学习了"不写已知知识"：

1. **Agent 已经知道大量通用知识**，不需要重复教
2. **只补充 Agent 默认不知道的东西**：团队约定、内部规范、业务上下文、踩过的坑
3. **审视每一条内容**：Agent 需要吗？知道吗？值得吗？

**核心原则**：补充未知，不重复已知。

## 下节预告

下一节，我们会学习"Gotchas 坑点"：真正有价值的内容，是踩过的坑。

理想情况下，应该随着时间不断更新 Skill，把新踩的坑也加进去。


---

## 🔗 章节导航

← [上一章：11-Pipeline 模式——分步执行流程](./chapters/11-Pipeline 模式——分步执行流程.md) | [下一章：13-Gotchas 坑点——最有价值的内容是踩过的坑](./chapters/13-Gotchas 坑点——最有价值的内容是踩过的坑.md) →
