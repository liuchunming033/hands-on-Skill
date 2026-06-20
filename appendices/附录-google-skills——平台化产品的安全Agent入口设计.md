> 学习目标：从 google/skills 的 35 个云端产品 Skill 中，学习如何为平台化产品构建"安全第一、验证驱动、渐进式加载"的生产级 Skill 体系

---

> 这是本教程的参考资料，用于帮助团队从 Google 官方 Skill 库中学习平台化产品的 Skill 设计方法。
>
> **代码库地址**：https://github.com/google/skills
>
> **阅读对象**：已经学完本教程前 27 章，希望参考 Google 官方实践来为云平台、API 产品和 SaaS 服务构建 Skill 的读者。

## 先给结论

google/skills 最值得学的不是"它有很多 Google Cloud 产品 Skill"，而是它从平台一侧揭示了 **Skill 的三种核心定位**：

- **安全护栏**：Skill 不是让 Agent 更自由，而是让 Agent 在危险操作面前自然停住（denylist、dry-run、no interactivity）
- **按需加载**：Skill 不是把所有文档塞进去，而是把 Agent 需要的字段、命令、流程在正确的时间精准注入（projection、filtering、limit）
- **验证驱动**：不是"建议 Agent 验证"，而是"不验证就不允许执行"（mandatory prerequisites、validation checklist、stop and wait）

这正好对应本教程反复强调的观点：**Skill 不是资料库，而是决策框架和执行边界**。Google 把这个理念写成了对平台级 Agent 的安全操作规范。

---

## 核心价值：为什么这个库值得学

Google Skills 与教程其他附录的定位完全不同：

| 附录 | 视角 | 核心价值 |
|------|------|---------|
| addyosmani/agent-skills | 软件工程全生命周期 | 教你"一个完整软件工程团队会把哪些流程写成 Skill" |
| Anthropic 9大分类 | AI 研发团队内部 | 教你"诊断团队能力缺口，按四个环节建设 Skill" |
| garrytan/gstack | 独立开发者 / 初创团队 | 教你"单人兼职如何用 Skill 模拟虚拟工程团队" |
| **google/skills** | **云平台 / 产品方** | **教你"产品方如何为 Agent 构建既安全又好用的 Skill"** |

**核心问题**：如果你负责 BigQuery、Cloud Run、Firebase 这种复杂云产品的 Agent 入口，你应该怎么设计 Skill？

Google 的回答是三个字：**安全、精准、渐进**。

---

## 这个库的基本结构

当前仓库的 `skills/cloud/` 目录包含 35 个 Skill，按功能可分为 5 大类别：

| 类别              | 数量   | 代表 Skill                                                                                        | 核心设计特点                                |
| --------------- | ---- | ----------------------------------------------------------------------------------------------- | ------------------------------------- |
| **产品服务入门**      | 8 个  | `bigquery-basics`、`cloud-run-basics`、`firebase-basics`、`gke-basics`                             | 强制前置检查 + 结构化工作流 + Gotchas 板块          |
| **Agent 平台操作**  | 11 个 | `agent-platform-deploy`、`agent-platform-skill-registry`、`agent-platform-prompt-management`      | Python 脚本集成 + references 渐进式加载 + 环境验证 |
| **工具与运行时**      | 4 个  | `gcloud`、`gemini-api`、`gemini-interactions-api`                                                 | 安全护栏优先 + 命令验证强制 + 数据缩减策略              |
| **最佳实践指南（WAF）** | 6 个  | `google-cloud-waf-security`、`google-cloud-waf-reliability`、`google-cloud-waf-cost-optimization` | 核心原则 → 评估提问 → 验证清单                    |
| **运维管理**        | 3 个  | `iam-recommendations-fetcher`、`gke-upgrades`、`workload-manager-basics`                          | 运维流程封装 + 权限边界控制                       |

README 中还引用了两个外部 Skill 库：

```text
google/skills (本库)
├── Flutter Skills  → https://github.com/flutter/skills
├── Dart Skills     → https://github.com/dart-lang/skills
└── Advanced GCS    → https://github.com/gemini-cli-extensions/google-cloud-storage
```

有趣的是，Google 并没有把所有产品 Skill 塞进一个仓库，而是让各产品团队维护独立的 Skill 库，本仓库只做「入口和索引」。这本身就是一种**渐进式分发**的思路。

---

## 统一 anatomy：Google Skill 的骨架特征

这个库里的 Skill 有几种典型骨架，但共享共同特征：

### 类型一：产品入门型（"Basics" 模板）

```markdown
---
name: <product>-basics
description: Use this skill whenever you are working on [specific scenario].
---

# <Product> Basics

### CRITICAL Mandatory prerequisites
[不满足前提条件就不能继续，有时要求 Stop and wait]

## Quick start
[最小可行动路径]

## Structured workflows
[按任务类型的结构化流程]
```

**核心特征**：
- description 写成触发场景，不是功能摘要
- 强制前置条件，有时要求"Stop and wait for user confirmation"
- 结构化工作流，按任务类型分表

### 类型二：WAF 指南型（Well-Architected Framework 模板）

```markdown
---
name: google-cloud-waf-<pillar>
description: Generates <pillar>-focused guidance. Use this skill to evaluate
  a workload, identify <pillar> requirements, and provide actionable
  recommendations.
---

## Overview
## Core principles
[每个原则附带 grounding document URL]
## Relevant Google Cloud products
[按子类别分组的产品列表]
## Workload assessment questions
[大量可选择性提问的结构化问题]
## Validation checklist
[可勾选的验证清单]
```

**核心特征**：
- 核心原则附带来源文档 URL（让 Agent 可以查证，而非依赖记忆）
- 评估提问是"选择题库"——选问，不是全问
- 验证清单是最终 Gate：所有检查项都要通过
- 这些 Skill 把"架构审查"从一个主观判断变成了可执行的检查点

### 类型三：安全工具型（gcloud 模板）

```markdown
---
name: gcloud
description: >-
  Interacts with Google Cloud services using the gcloud CLI safely and
  efficiently. You MUST read this skill before invoking any gcloud command.
---

## Core Principles
1. Explicit Command Validation (Mandatory) — "你被禁止执行未经验证的命令"
2. Data Reduction Strategies — --format, --limit, --filter
3. Execution Constraints — 单命令、无管道、无交互
4. Project and Location Scoping — 必须显式指定

## Safety & Guardrails
[Denylist: 明确列出禁止的操作]
```

**核心特征**：
- 安全是第一优先级，不是附件
- 明确禁止操作的 Denylist
- Dry-run 强制规则
- 数据缩减不只是建议，而是防止上下文过载的工程要求

---

## 与教程五大模式的映射

| 教程模式 | Google Skills 中的体现 | 学习重点 |
|----------|----------------------|----------|
| **ToolWrapper 模式** | `gcloud`、`gemini-api`、`bigquery-basics` | 把 CLI 和 API 封装成安全可用的工具，重点是 safety guardrails 和 data reduction |
| **Reviewer 模式** | WAF 系列（security、reliability、cost、ops、perf、sustainability） | 用 assessment questions + validation checklist 构成可执行的审查流程 |
| **Pipeline 模式** | `firebase-basics`（prerequisites → quick start → task）、`agent-platform-deploy` | 用 mandatory prerequisites → workflows → verification 构成 Gate 机制 |
| **Generator 模式** | WAF 系列（输出结构化建议）、`agent-platform-skill-registry`（skill scaffolding） | 固定输出结构：recommendations、reports、skill templates |
| **Inversion 模式** | WAF 系列的 assessment questions | 先问清需求再给建议，问题来源不是随机而是 workload assessment |

Google Skills 最特殊的地方在于：它不光有这些模式，还多了一层 **Safety Layer**。

---

## 五大设计特征逐项解析

### 特征一：安全护栏前置（Safety by Default）

Google Skills 对安全的态度是做在 Skill 结构里，而不是写在旁注里。

**gcloud 的 Denylist 机制**：

```markdown
### Prohibited Operations (Denylist)

You are **strictly prohibited** from executing the following commands
autonomously:

- **Any IAM policy, role, or binding modification**
- **`gcloud * delete`**
- **`gcloud billing *`**
- **`gcloud organizations *`**
- **`gcloud kms *`**
- **`gcloud infra-manager deployments apply`**
```

**Dry-run 强制规则**：

```markdown
### Dry Run (Mandatory)

You MUST invoke a command with `--dry-run` (or equivalent) first if it
exists, before executing the actual command, to preview changes.
```

**为什么这很重要**：Agent 对自己的 CLI 操作是没有风险意识的。一个 `gcloud compute instances delete` 对 Agent 来说和一个 `ls` 没有区别。Skill 必须显式建立"哪些事绝对不允许自动做"的边界。

**教程连接**：对应第 27 章"Skill 安全三原则"。Google 把它写成了可执行的 Denylist + Dry-run + Proactive API Enabling 禁止规则。

---

### 特征二：数据缩减策略（Data Reduction by Design）

这是 Google Skills 最独特的贡献：**它不只看怎么把数据放进去，更看怎么防止数据把 Agent 淹死**。

**gcloud 的三层数据缩减**：

```text
Projection: --format=json(key1, key2, ...)     # 只要需要的字段
Limiting:   --limit=N                           # 限制返回数量
Filtering:  --filter="status:RUNNING"           # 服务端过滤
```

**Schema Discovery（模式发现）**：

```bash
# 先拿一条数据看结构，再决定查什么
gcloud <GROUP> <RESOURCE> list --limit=1 --format=json
```

**为什么这很重要**：Agent 的上下文窗口是有限资源。一个 `gcloud compute instances list` 不加 filter 和 limit，可能返回上千行 JSON，直接把上下文窗口占满。Google 把这些数据缩减策略写成了**技能级的要求**，而不是可选的建议。

**教程连接**：对应第 14 章"文件组织与渐进式披露"和第 07 章 ToolWrapper 模式。它把"精准加载"从文件组织扩展到了运行时数据获取。

---

### 特征三：强制前置验证（Mandatory Prerequisites）

Google Skills 不是"建议你做 A"，而是"没有 A，就不能进入 B"。

**Firebase Basics 的强制前置**：

```markdown
### **CRITICAL** Mandatory prerequisites

Before attempting to fulfill any user request regarding Firebase, you **MUST**
follow these steps in order. Do not proceed to implementation until these are
completed.

1. Ensure NPM is installed.
2. Install agent skills: npx -y skills add firebase/agent-skills -y
3. Log in to Firebase CLI.
4. Set an active project for the CLI.

# Step 2: Stop and wait for user confirmation
```

**Agent Platform 的环境验证**：

```bash
# 在任何操作之前，必须先执行环境验证脚本
python3 scripts/validate_env.py
```

**为什么这很重要**：普通 prompt 写法是"你应该先检查环境"，Agent 可能跳过。Google 的写法是用 `CRITICAL`、`MUST`、`Stop and wait` 建立**不可略过的检查点**。

**教程连接**：对应第 11 章 Pipeline 模式的 Gate 机制。Google 把 Gate 从"建议"升级到了"MUST + Stop and wait"。

---

### 特征四：结构化验证清单（Validation Checklist as Gate）

WAF 系列的每个 Skill 都以 Validation Checklist 收尾，这个 checklist 不只是检查项，而是 Gate。

**Security WAF 的验证清单**：

```markdown
## Validation checklist

- **Security by design**:
  - [ ] Are system components selected based on their security features?
  - [ ] Is defense-in-depth implemented at network, host, and application layers?
  - [ ] Are safe libraries and frameworks used?

- **Zero trust**:
  - [ ] Is access control enforced based on identity and context?
  - [ ] Are VPC Service Controls perimeters established?
  - [ ] Are default networks disabled in all projects?
```

**它与普通 checklist 的区别**：

| 普通 checklist | Google WAF checklist |
|---------------|---------------------|
| "建议检查这些" | "以下所有项必须通过" |
| 列在文档末尾当参考 | 作为流程的最后一道 Gate |
| 检查项模糊 | 每项有明确的通过条件 |
| 无 grounding | 每项对应核心原则和来源文档 |

**教程连接**：对应第 09 章 Reviewer 模式和第 20-24 章评估篇。Google 把"验证不是感觉，是证据"写成了 WAF 六支柱的完整检查清单。

---

### 特征五：渐进式按需加载（Progressive Disclosure by Folder）

Agent Platform 系列 Skill 大规模使用了 `references/` 文件夹结构：

```
agent-platform-skill-registry/
├── SKILL.md                    # 入口：概述 + 快速开始
├── references/
│   ├── query-skills.md         # 按需：技能发现操作
│   ├── manage-skills.md        # 按需：技能生命周期管理
│   ├── monitor-operations.md   # 按需：操作监控
│   └── generate-skill.md       # 按需：Skill 脚手架
└── scripts/
    ├── validate_env.py         # 环境验证脚本
    └── skill_registry_ops.py   # 注册表操作脚本
```

SKILL.md 只写核心指令和快速开始，详细操作说明在 references/ 子文件中，Agent 按任务需求按需读取。

**教程连接**：对应第 14 章"Skill 是文件夹不是文件"。Google Agent Platform 系列是这个原则的完美实践样本。

---

## 最值得拆开的 6 个经典 Skill

如果只选 6 个来学习，建议按这个顺序读。

### 1. gcloud：安全护栏的教科书级设计

**类型**：ToolWrapper + Safety Layer

**为什么值得学**：它把"用命令行工具"这件看似普通的事，写成了有完整安全模型的 Skill。

**可迁移的设计点**：
- Denylist：列出绝对不允许的操作
- Dry-run 强制：变更类命令必须先预览
- 数据缩减：--format、--limit、--filter 不是建议，是要求
- 单命令约束：不允许管道和命令替换，防止注入
- 显式范围：禁止依赖默认配置，--project 和 --region 必须显式

**适用于**：任何涉及 CLI 操作、数据库查询、API 调用的 Skill。

---

### 2. firebase-basics：强制前置检查的最严实现

**类型**：Pipeline + Mandatory Gate

**为什么值得学**：它把"准备工作"写成了不可跳过的必做项。

**可迁移的设计点**：
- CRITICAL 标记：明确区分"建议做"和"必须做"
- Stop and wait：需要用户交互的地方，明确停下来等
- 依赖检查链：npm check → skills install → CLI login → project set

**适用于**：任何有环境依赖的程序框架 Skill。

---

### 3. google-cloud-waf-security：验证不是感觉，是清单

**类型**：Reviewer + Validation Checklist

**为什么值得学**：它把"架构安全审查"从一个经验判断变成了可重复执行的检查清单。

**可迁移的设计点**：
- 核心原则 + grounding document URL
- 评估提问库（选问，不是全问）
- 验证清单（每项可勾选）
- 按维度分组的检查结构

**适用于**：任何需要"审查"和"评估"场景的 Skill。

---

### 4. agent-platform-skill-registry：脚本 + 渐进式加载

**类型**：ToolWrapper + Progressive Disclosure

**为什么值得学**：它展示了"SKILL.md 是入口，references/ 是手册，scripts/ 是引擎"的完整文件夹模式。

**可迁移的设计点**：
- SKILL.md < 100 行，只写概述和快速开始
- references/ 按操作分类（query、manage、monitor、generate）
- scripts/ 封装稳定操作（环境验证、API 调用）
- 内部引用用相对路径 `references/xxx.md`

**适用于**：任何需要复杂 API 操作和脚本配合的 Skill。

---

### 5. google-cloud-recipe-onboarding：把"上手"写成可执行流程

**类型**：Pipeline + Recipe

**为什么值得学**：它把"新用户如何上手"这个模糊需求写成了按步骤执行的工作流。

**可迁移的设计点**：
- 按阶段分步的流程结构
- 每步有明确输出
- 避免技术栈假设，面向多场景

**适用于**：任何"引导类"、"教程类" Skill。

---

### 6. gemini-api：API Skill 的标准写法

**类型**：ToolWrapper + API Reference

**为什么值得学**：它展示了 API 类 Skill 应该怎么写：不是把整个 API 文档复制过来，而是写 Agent 最容易出错的用法。

**可迁移的设计点**：
- 最常用的 API 调用模式
- 常见错误和正确做法对比
- 不重复官方 API 文档

**适用于**：任何面向 API 服务的 Skill。

---

## 10 条启发：Google Skill 对 Skill 写作的补充

### 1. 把安全写进 Skill 结构，而不是附件

不是写一个"安全注意事项"章节，而是让安全在每一个操作点自然出现：

```markdown
# ✅ 好的写法
## Execute a command
1. Validate syntax with `gcloud help <command>` (MANDATORY)
2. Run with `--dry-run` first (MANDATORY)
3. Check denylist (NEVER skip)
4. Execute with explicit --project and --region

# ❌ 弱的写法
## Execute a command
1. Run the command
2. If error, check security notes at bottom
```

---

### 2. 教 Agent 如何少拿数据

不是"你可以用 --format"，而是"你必须用 --format"：

```markdown
✅ 推荐写法：
To save context window, always minimize data returned:
- Projection: --format=json(key1, key2)
- Limiting: --limit=10
- Filtering: --filter="status:RUNNING"

Schema Discovery: Before querying, discover structure with
`gcloud <RESOURCE> list --limit=1 --format=json`
```

---

### 3. Stop and wait 不只是礼貌，是质量控制

```markdown
# 真正有用的 Stop and wait
## Step 2: Install Node.js
Ask the user to download LTS from https://nodejs.org.
**Stop and wait** for user confirmation before proceeding.
```

这不是过度约束，而是在"需要人类参与的步骤"上设置明确的交接点。

---

### 4. 用 Denylist 替代"请注意"

"请注意安全"对 Agent 无效，Denylist 才有效：

```markdown
# ❌ 无效写法
⚠️ 注意：请谨慎使用删除操作

# ✅ 有效写法
## Prohibited (Denylist)
You are STRICTLY PROHIBITED from:
- `gcloud * delete`
- `gcloud billing *`
- `gcloud kms *`
```

---

### 5. WAF 模式：核心原则必须附带来源

```markdown
## Core principles

- **Implement zero trust**: Use a never trust, always verify approach.
  Grounding document:
  https://docs.cloud.google.com/architecture/framework/security/...

- **Implement shift-left security**: ...
  Grounding document:
  https://docs.cloud.google.com/architecture/framework/security/...
```

Agent 不是凭记忆做审查，而是可以验证每一条原则的来源。这对教程第 12 章"不写已知知识"是一个重要补充：你要给的不是教程，而是"如何验证"的入口。

---

### 6. 评估提问是选择题库，不是问卷

WAF 的 assessment questions 是"按需选择"而不是"全问一遍"：

```markdown
Ask appropriate questions to understand the workload. Choose questions
from the following list:
```

然后每个维度下列 10 个问题。这让 Agent 有智能选择的空间——它可以根据对话上下文只挑相关的问。

---

### 7. 用 GitHub 组织产品 Skill 生态

Google 没有把所有 Skill 塞进一个仓库，而是用「入口仓库 + 产品独立仓库」的模式：

```text
google/skills (入口) → flutter/skills (Flutter 产品)
                    → dart-lang/skills (Dart 产品)
                    → gemini-cli-extensions/google-cloud-storage (GCS)
```

这解决了第 26 章"Skill 长期维护"中提到的一个核心矛盾：一个仓库装不下所有产品，多仓库又难发现。入口仓库做索引，产品仓库做实现。

---

### 8. Dry-run 不是可选项

Google 把 dry-run 写成强制要求，这是生产级 Skill 和演示级 Skill 的分界线：

```markdown
You MUST invoke a command with `--dry-run` (or equivalent) first if it
exists, before executing the actual command.
```

对应教程第 27 章"安全三原则"：对变更类操作，永远先预览再执行。

---

### 9. 产品 Skill 不要写教程，要写 Agent 容易错的地方

gemini-api 和 bigquery-basics 都没有重写官方文档。它们写的是：
- 最常见的使用场景和代码片段
- Agent 最容易用错的 API 用法
- 错误处理和边界条件

---

### 10. scripts/ 不是"有就好"，而是"环境验证必须前置"

Agent Platform 系列在每个 Skill 里都有 `python3 scripts/validate_env.py`，执行任务前强制验证环境。这意味着**脚本的第一用途不是工具，而是门禁**。

---

## 对比本教程：它补充了什么

| 本教程关注点 | google/skills 的补充 |
|--------------|---------------------|
| Skill 文件结构 | 三种 Skill 骨架模板（Basics、WAF、Tool） |
| description 写法 | 每个 description 写具体触发场景，部分写 MUST READ |
| 渐进式披露 | references/ 按操作类型分文件，SKILL.md 保持精简 |
| 三档自由度 | gcloud 是低自由度代表（禁止管道/命令替换），WAF 是中自由度（选择题库） |
| 五大模式 | ToolWrapper、Pipeline、Reviewer、Generator 都有成熟案例 |
| Gotchas | 以 Safety & Guardrails 的方式呈现 |
| 安全 | Denylist、Dry-run、No interactivity、Proactive API enabling 禁止 |
| 上下文管理 | 独创 data reduction 策略：projection、limiting、filtering |
| 团队运营 | 入口仓库 + 产品独立仓库的分发模式 |

如果说本教程教你"如何设计 Skill"，addyosmani 教你"团队需要哪些 Skill"，Anthropic 9 分类教你"诊断能力缺口"，Google Skills 教你"为平台化产品构建安全可用的 Agent 入口"**。

---

## 如何把它用于团队实践

### 第一步：识别你团队的产品类型

| 你的产品类型 | 最值得参考的 Google Skill 模板 |
|-------------|------------------------------|
| CLI 工具 / SDK | `gcloud`（安全护栏 + 数据缩减） |
| 云服务 / API | `bigquery-basics`、`cloud-run-basics` |
| 框架 / 平台 | `firebase-basics`（强制前置检查） |
| 需要审查评估 | WAF 系列（评估提问 + 验证清单） |
| 复杂 API 操作 | Agent Platform 系列（脚本 + 渐进加载） |

### 第二步：先写安全边界，再写功能流程

不要一上来就写"怎么用"。先写：
1. Denylist：Agent 绝对不能做什么
2. Dry-run 规则：变更前必须预览
3. 交互边界：哪些操作必须人工确认

### 第三步：用 data reduction 保护上下文窗口

- 查询类操作：写清 `--limit`、`--filter`、`--format` 规则
- 列表类操作：要求 Schema Discovery 先查一条看结构
- API 调用：只返回任务需要的字段

### 第四步：把验证清单做成 Gate

不用 `.github/` 或外部 CI，直接在 Skill 末尾写：

```markdown
## Validation checklist
- [ ] <条件1>
- [ ] <条件2>
- [ ] <条件3>

All items must pass before this task is complete.
```

### 第五步：用入口仓库管理多产品 Skill

如果团队有多个产品线，考虑：
- 一个入口仓库做索引（类似 `google/skills`）
- 每个产品线维护独立仓库
- README 里提供安装命令：`npx skills add your-org/product-skills`

---

## 小结

google/skills 是平台产品方构建 Agent Skill 的优秀参考，尤其值得学习 5 点：

1. **安全不是附件，是结构**：Denylist + Dry-run + No interactivity 嵌入 Skill 骨架
2. **数据缩减是工程要求**：--format、--limit、--filter 不是建议，是防止上下文过载的必需策略
3. **强制前置验证**：CRITICAL prerequisites + Stop and wait + validate_env.py 构成不可跳过的检查点
4. **WAF 验证清单**：把"审查"从主观判断变成可重复执行的 checklist
5. **入口仓库模式**：不把全部 Skill 塞一起，用索引仓库 + 产品独立仓库实现渐进式分发

它给我们的最大启发是：

> **好 Skill 不只是让 Agent 更会做，更是让 Agent 在危险面前自然停住，在过多数据面前主动缩减，在没有验证时不贸然向前。**

