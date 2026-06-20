
> 学习目标：掌握如何封装稳定能力为脚本，让Agent直接调用而不重复生成

---


## 引言

你是不是也遇到过这种情况：每次让 Agent 写同样的代码，都要从头开始？

比如提取 PDF 文本、转换数据格式、生成报告，明明是重复的操作，Agent 每次都要重新写一遍脚本。

**问题**：Agent 在重复造轮子，浪费时间和 token。

**解决**：把稳定能力封装成脚本，让 Agent 直接调用。

---

## 📚 核心问题

**Agent 每次都要重新写同样的代码，浪费时间、浪费 token，还容易出错。**

常见表现：

- PDF 提取：每次都要写新的提取脚本
- 数据转换：每次都要写新的转换逻辑
- 表单填写：每次都要写新的填充代码
- 报告生成：每次都要写新的模板

---

## 💡 脚本的解决方案

**核心思想**：**给 Agent 最好的工具不是更多文档，而是可调用的代码。**

Claude Code 核心开发者发现：

| 方式 | Agent 操作 | 效果 |
|------|------------|------|
| **文档** | 读完理解，然后生成代码 | 消耗 token，可能出错 |
| **脚本** | 直接调用执行 | 稳定可靠，结果一致 |

**实用脚本的好处**：

- 比生成的代码更可靠（脚本经过测试）
- 节省 token（不需要在上下文中包含代码）
- 节省时间（不需要生成代码）
- 确保一致性（每次执行结果相同）

---

## 🔧 脚本组织示例

### 示例 1：PDF Skill 目录结构

```
pdf-skill/
├── SKILL.md
└── scripts/
    ├── extract_text.py
    ├── extract_tables.py
    └── fill_form.py
```

SKILL.md 中写：

````markdown
## 提取文本

运行脚本：
```bash
python scripts/extract_text.py input.pdf
```

输出格式：纯文本
````

---

### 示例 2：PDF 表单填写脚本（完整案例）

来自 Anthropic 官方最佳实践：

**目录结构**：

```
pdf/
├── SKILL.md              # 主文件
├── FORMS.md              # 表单填充指南（按需加载）
├── scripts/
│   ├── analyze_form.py   # 分析表单字段
│   ├── validate_fields.py # 验证字段映射
│   ├── fill_form.py      # 填充表单
│   └── verify_output.py  # 验证输出
└── examples/
    └── sample-form.pdf   # 示例表单
```

**SKILL.md 工作流说明**：

````markdown
## PDF form filling workflow

按照这个检查清单执行：

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

提取表单字段和位置，保存到 `fields.json`。

**Step 2: Create field mapping**

编辑 `fields.json`，为每个字段添加值。

**Step 3: Validate mapping**

Run: `python scripts/validate_fields.py fields.json`

验证失败则返回 Step 2。

**Step 4: Fill the form**

Run: `python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output**

Run: `python scripts/verify_output.py output.pdf`
````

**脚本示例（analyze_form.py）**：

```python
"""Extract all form fields from PDF and save to JSON."""

import pdfplumber
import json
import sys

def analyze_form(pdf_path):
    """分析 PDF 表单，提取字段信息"""
    with pdfplumber.open(pdf_path) as pdf:
        fields = []
        for page in pdf.pages:
            # 提取表单字段位置和类型
            for field in page.chars:
                fields.append({
                    "name": field.get("text", ""),
                    "type": "text",
                    "x": field["x0"],
                    "y": field["top"]
                })

        # 保存到 JSON
        output = {"fields": fields}
        json.dump(output, sys.stdout, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_form.py <pdf_path>")
        sys.exit(1)

    analyze_form(sys.argv[1])
```

---

## 📌 脚本编写最佳实践

### 实践 1：解决问题，而不是推卸

脚本要处理错误，而不是让 Agent 自己处理。

**错误写法**：

```python
def process_file(path):
    # 直接失败，让 Agent 自己处理
    return open(path).read()
```

**正确写法**：

```python
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # 创建文件，而不是失败
        print(f"File {path} not found, creating default")
        with open(path, "w") as f:
            f.write("")
        return ""
    except PermissionError:
        # 提供替代方案，而不是失败
        print(f"Cannot access {path}, using default")
        return ""
```

**关键**：脚本要处理常见错误，而不是每次都让 Agent 来解决。

---

### 实践 2：避免魔法数字

配置参数要有注释说明，别让 Agent 瞎猜。

**错误写法**：

```python
TIMEOUT = 47  # 为什么是 47？
RETRIES = 5   # 为什么是 5？
```

**正确写法**：

```python
# HTTP 请求通常在 30 秒内完成
# 较长的超时时间可应对慢速连接
REQUEST_TIMEOUT = 30

# 三次重试在可靠性与速度之间取得平衡
# 大多数间歇性故障在第二次重试时即可解决
MAX_RETRIES = 3
```

**关键**：注释要说明为什么是这个值，让 Agent 理解背后的逻辑。

---

### 实践 3：明确执行方式

在 SKILL.md 中明确告诉 Agent：

- **执行脚本**（最常见）：`run analyze_form.py to extract fields`
- **作为参考阅读**（复杂逻辑）：`see analyze_form.py for field extraction algorithm`

大多数情况用**执行**，因为它更可靠、更高效。

---

## ✅ 适用场景

**应该封装成脚本的情况**：

- 操作逻辑稳定，不会频繁变化
- 执行过程复杂，每次重新写容易出错
- 需要确保结果一致性
- 需要与其他系统集成

**不应该封装成脚本的情况**：

- 操作简单，一行命令就能完成
- 逻辑不清晰，需要根据上下文调整
- 只是偶尔使用，不值得封装

---

## 🎯 本节核心观点

**脚本封装的三个关键**：

1. **解决问题而不是推卸**：脚本要处理错误，不要让 Agent 自己解决
2. **避免魔法数字**：配置参数要有注释说明，别让 Agent 瞎猜
3. **明确执行方式**：告诉 Agent 是执行脚本还是作为参考阅读

**核心原则**：最好的工具不是更多文档，而是可调用的代码。

---

## 🔗 下节预告

下一节我们学习 **按需 Hooks**：临时规则，会话隔离。

有些规则太严格，不想一直开启，但特定场景下又需要。

---

