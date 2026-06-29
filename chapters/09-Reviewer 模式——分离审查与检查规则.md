
> 学习目标：掌握如何让审查型 Skill 的流程和规则解耦，实现"流程不动、规则可换"

---

## 引言

审查任务经常推倒重来——为什么？

因为"检查什么"和"怎么检查"写混了。

比如你写了个代码审查的 Skill：

```
请审查这段代码：
1. 检查是否有安全漏洞
2. 检查是否遵循 Python 风格
3. 检查是否有性能问题
...
```

如果明天要改成 OWASP 安全检查，或者要改成 JavaScript 风格，整个 Skill 都要改。

**Reviewer 模式**解决的就是这个问题。

---

## 📚 核心问题

**审查规则和审查流程耦合在一起。**

常见表现：

- 换一种检查规则就要重写整个 Skill
- 不同团队有不同审查标准，无法复用
- 规则更新后，流程也要跟着改

---

## 💡 Reviewer 的解决方案

**核心思想**：分离规则。

- **检查什么** → 放进 checklist（可替换）
- **怎么检查** → 留在 SKILL.md（流程不动）
![Reviewer 模式](reviewer-pattern.png)

**流程**：

1. 读取 checklist
2. 逐项检查
3. 输出结构化结果（error/warning/info）

**价值**：流程不动、规则可换。今天 Python 风格审查，明天 OWASP 安全检查，后天合规规则，只需要替换 checklist。

---

## 🔧 Reviewer SKILL.md 示例

**文件结构**：

```
code-review/
├── SKILL.md           # 审查流程
├── checklists/
│   ├── python.md      # Python 风格检查
│   ├── security.md    # OWASP 安全检查
│   ├── javascript.md  # JavaScript 风格检查
│   └── performance.md # 性能检查
└── templates/
    └── review-output.md
```

**SKILL.md 内容**：

````markdown
---
name: code-review
description: Review code against customizable checklists. Use when reviewing PRs, auditing code, or checking code quality.
---

# Code Review

## 审查流程

1. 读取本次使用的 checklist（根据用户指定或自动判断）
2. 逐项检查代码
3. 输出结构化审查报告

## 可用 Checklist

| 类型 | 文件 | 适用场景 |
|------|------|---------|
| Python 风格 | [checklists/python.md](checklists/python.md) | Python 代码审查 |
| 安全检查 | [checklists/security.md](checklists/security.md) | 安全漏洞扫描 |
| JavaScript 风格 | [checklists/javascript.md](checklists/javascript.md) | JS/TS 代码审查 |
| 性能检查 | [checklists/performance.md](checklists/performance.md) | 性能问题排查 |

## 输出格式

```markdown
## 审查结果

### 🔴 Errors (必须修复)
- [文件:行号] 具体问题描述

### 🟡 Warnings (建议修复)
- [文件:行号] 具体问题描述

### 🔵 Info (可选改进)
- [文件:行号] 具体问题描述

## 总结
- 发现 X 个问题，其中 Y 个必须修复
```

## 使用方式

用户可以说：
- "用安全检查审一下这段代码" → 加载 checklists/security.md
- "审查这个 PR 的 Python 风格" → 加载 checklists/python.md
- "帮我看看性能问题" → 加载 checklists/performance.md
````

**checklists/security.md 示例**：

```markdown
# OWASP 安全检查清单

## 注入漏洞
- [ ] 是否存在 SQL 注入风险？（未参数化的查询）
- [ ] 是否存在命令注入风险？（用户输入直接执行）
- [ ] 是否存在 XSS 风险？（未转义的用户输入）

## 认证与授权
- [ ] 敏感操作是否有权限检查？
- [ ] 密码是否明文存储？
- [ ] Session 管理是否安全？

## 敏感数据
- [ ] 是否有敏感信息硬编码？（API key、密码）
- [ ] 日志是否记录了敏感信息？
- [ ] 数据传输是否加密？
```

---

## 📌 经典案例

### 案例：安全漏洞审查助手

**场景**：安全团队需要对代码进行不同标准的安全审查。

**问题**：不同项目有不同的安全要求：
- 面向公众的 Web 应用 → 需要 OWASP Top 10 检查
- 内部工具 → 需要企业安全规范检查
- 金融产品 → 需要合规审查（PCI DSS、SOC 2）

如果写成一个固定的审查清单，无法适应不同场景。

**Reviewer 方案**：

```
security-review/
├── SKILL.md                    # 审查流程（通用）
├── checklists/
│   ├── owasp-top10.md          # OWASP Top 10 检查清单
│   ├── enterprise-security.md  # 企业安全规范
│   ├── pci-dss.md              # PCI DSS 合规检查
│   └── soc2.md                 # SOC 2 合规检查
└── templates/
    └── report.md               # 审查报告模板
```

**SKILL.md 核心内容**：

```markdown
# 安全漏洞审查

## 审查流程

1. 确认审查标准（根据项目类型）
2. 加载对应的检查清单
3. 逐项扫描代码
4. 输出结构化报告

## 检查清单选择

- **Web 应用（面向公众）** → 加载 [checklists/owasp-top10.md](checklists/owasp-top10.md)
- **内部工具** → 加载 [checklists/enterprise-security.md](checklists/enterprise-security.md)
- **金融产品** → 加载 [checklists/pci-dss.md](checklists/pci-dss.md) 或 [checklists/soc2.md](checklists/soc2.md)

## 输出格式

统一输出 Critical / High / Medium / Low 四级漏洞列表
```

**checklists/owasp-top10.md 示例**：

```markdown
# OWASP Top 10 安全检查清单

## A01: Broken Access Control
- [ ] 是否存在未授权的 API 访问？
- [ ] 用户权限检查是否完整？
- [ ] 路径遍历漏洞是否存在？

## A02: Cryptographic Failures
- [ ] 敏感数据是否加密存储？
- [ ] 传输是否使用 HTTPS？
- [ ] 加密算法是否足够强？

## A03: Injection
- [ ] SQL 查询是否使用参数化？
- [ ] 用户输入是否经过验证和转义？
- [ ] 命令注入风险是否存在？

...（共 10 大类）
```

**案例解析**：

1. **流程与规则分离**：审查流程不变，检查清单可替换
2. **灵活适配**：根据项目类型选择不同的审查标准
3. **易于维护**：新增安全标准只需添加新的 checklist 文件
4. **专业精准**：每种审查标准都由安全专家编写，不会混淆

**实际效果对比**：

| 方案 | 灵活性 | 维护成本 | 审查准确性 |
|------|--------|---------|-----------|
| 固定清单 | 低（一种标准） | 高（修改影响全局） | 中（不精准） |
| Reviewer 模式 | 高（多种标准） | 低（独立更新） | 高（专业精准） |

**团队反馈**：
"以前一套审查标准用到底，现在可以根据项目选择 OWASP 或 PCI DSS，审查报告更专业了。"  Reviewer 模式的经典 Skill 案例

---

## ✅ 适用场景

- **代码审查**：不同语言/框架的审查规则
- **安全检查**：OWASP、CWE 等不同安全标准
- **合规审查**：不同行业的合规要求
- **任何规则经常变化的审查任务**

---

## 🎯 本节核心观点

**Reviewer 模式的三个关键**：

1. **流程和规则分离**：检查流程不变，检查规则可替换
2. **结构化输出**：统一成 error/warning/info 层级
3. **可扩展**：新增检查维度只需添加新的 checklist 文件

---

## 🔗 下节预告

下一节我们学习 **Inversion 模式**：如何让 Agent 先问清需求再开工，避免"信息不够就自己猜"。

---

