
> 学习目标：掌握如何组织references文件，实现渐进式加载

---


## 引言

很多人写 Skill，习惯把所有内容都塞进一个 SKILL.md 文件里。

结果呢？文件越来越大，几千字甚至上万字。每次调用都要加载全部内容，浪费大量 context。

**正确的做法**：Skill 是文件夹，不是文件。

## 核心内容

### 错误做法：单文件巨无霸

```
my-skill/
└── SKILL.md (5000 行)
```

问题：

- 每次调用都加载全部内容
- 浪费 context 窗口
- 信息杂乱，Agent 难以定位

### 正确做法：渐进式披露

```
my-skill/
├── SKILL.md          # 核心逻辑（约 100 行）
├── references.md     # 详细参考文档
├── templates.md      # 模板文件
└── gotchas.md        # 踩坑记录
```

**核心思想**：主文件只写核心逻辑，详细文档按需加载。

### 渐进式披露的三层

| 层级 | 内容 | 加载时机 |
|------|------|---------|
| 第一层 | description（元数据） | 会话启动时预加载 |
| 第二层 | SKILL.md 正文 | 触发时加载 |
| 第三层 | 附属文件 | 需要时才加载 |

### 如何组织文件？

**按功能拆分**：

```markdown
# SKILL.md

## 快速开始
（核心流程）

## 高级功能
详见 [references.md](references.md)

## 模板
详见 [templates.md](templates.md)

## 常见问题
详见 [gotchas.md](gotchas.md)
```

**按领域拆分**：

```
bigquery-skill/
├── SKILL.md          # 总览和导航
└── references/
    ├── finance.md    # 财务数据
    ├── sales.md      # 销售数据
    └── product.md    # 产品数据
```

当用户问财务数据时，Agent 只加载 finance.md，不加载其他文件。

### 渐进式披露的价值

**节省 context**：

- 不需要的内容不加载
- 每次只加载任务所需的部分
- context 窗口利用率最大化

**提高准确性**：

- 信息结构清晰
- Agent 更容易定位
- 减少干扰和混淆

### 避免深层嵌套

**错误做法**：

```markdown
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**问题**：Agent 可能只预览文件，不读取完整内容。

**正确做法**：所有附属文件都从 SKILL.md 直接引用。

```markdown
# SKILL.md
- 基础用法：[instructions.md](instructions.md)
- 高级功能：[advanced.md](advanced.md)
- API 参考：[reference.md](reference.md)
```

### 文件组织原则

1. **主文件控制骨架**：SKILL.md 写核心流程和导航
2. **附属文件存细节**：详细内容拆分到单独文件
3. **一层深度引用**：所有文件从 SKILL.md 直接引用
4. **按需加载**：只有需要时才读取

## 总结

今天我们学习了文件组织与渐进式披露：

1. **Skill 是文件夹不是文件**，可以放脚本、模板、数据文件
2. **渐进式披露**：主文件只写核心逻辑，详细文档按需加载
3. **一层深度引用**：避免深层嵌套，所有文件从 SKILL.md 直接引用

**核心原则**：按需加载，最大化利用上下文窗口。

## 下节预告

下一节，我们会学习"避免过度约束"：约束目标，而不是约束路径。

给 Agent 它需要的信息，但也要给它适应不同情况的灵活性。


---

## 🔗 章节导航

← [上一章：13-Gotchas 坑点——最有价值的内容是踩过的坑](./13-Gotchas 坑点——最有价值的内容是踩过的坑.md) | [下一章：15-避免过度约束——约束目标，不约束路径](./15-避免过度约束——约束目标，不约束路径.md) →
