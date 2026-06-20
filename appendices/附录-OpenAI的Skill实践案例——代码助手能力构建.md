> 学习目标：从 openai/codex 的 14 个真实 Skill 中，学习如何为特定代码库构建"极度具体、持续监控、状态驱动"的领域化 Skill 体系

---

> 这是本课程的参考资料，用于帮助团队从 OpenAI Codex 的真实 Skill 实践中学习领域化能力构建方法。
>
> **代码库地址**：https://github.com/openai/codex/tree/main/.codex/skills
>
> **阅读对象**：已经学完本课程前 27 章，希望参考 OpenAI 官方实践来为具体代码库构建深度领域化 Skill 的读者。

## 先给结论

openai/codex 的 `.codex/skills/` 最值得学的不是"它有很多 Skill"，而是它揭示了一个反直觉的事实：

**最好的 Skill 往往极端领域化，无法直接迁移给其他项目。**

Codex 的 14 个 Skill 没有一个是"通用代码审查"或"通用脚手架"。它们精确到 Rust 类型选择（`path-types`）、V8 版本更新流程（`update-v8-version`）、特定 PR 的 CI 康复流程（`babysit-pr`）、特定代码库的 issue 热度判断（`codex-issue-digest` 的 🔥🔥 系统）。

对比其他附录的定位：

| 附录 | Skill 定位 | 通用性 |
|------|-----------|--------|
| addyosmani/agent-skills | 软件工程全生命周期流程 | 高（可迁移给任何工程团队） |
| Anthropic 9大分类 | 通用 AI 研发能力诊断 | 高（适用于任何行业的 AI 团队） |
| garrytan/gstack | 创业者产品研发全流程 | 较高（适用于初创团队） |
| google/skills | 云平台产品 Agent 入口 | 中（适用于有云产品的平台方） |
| **openai/codex** | **特定代码库的深度领域操作** | **低 —— 但这恰恰是它的价值所在** |

**核心价值**：它展示了当 Skill 被推到极端领域化时能达到什么深度。不是"帮你审查代码"，而是"审查 Codex 的 Rust path 类型转换是否违反 URI 迁移契约，同时检查模型上下文是否引入了大于 10K token 的项"。

---

## 仓库基本结构

`.codex/skills/` 目录包含 14 个 Skill，按功能可归纳为 4 类：

| 类别 | 数量 | Skill 列表 | 核心特征 |
|------|------|-----------|---------|
| **PR 生命周期管理** | 3 个 | `babysit-pr`、`codex-pr-body`、`pushing-ci-changes` | 持续监控、自动修复、状态驱动 |
| **代码审查** | 5 个 | `code-review`（编排器）+ `code-review-breaking-changes`、`code-review-change-size`、`code-review-context`、`code-review-testing` | Subagent 并行、极端领域化规则 |
| **Issue 管理** | 2 个 | `codex-bug`、`codex-issue-digest` | 自动诊断分类、注意力标记系统 |
| **代码库特定操作** | 4 个 | `path-types`、`remote-tests`、`test-tui`、`update-v8-version` | 极端领域化、精确到文件和类型 |

---

## 五大设计特征逐项解析

### 特征一：持续监控与自主修复（babysit-pr）

这是整个仓库中最复杂、最值得学的 Skill。它不是"检查一次 PR 的 CI 状态"，而是一个**持续运行的自主监控循环**。

**核心循环**：

```text
Snapshot PR state → Check CI + reviews + mergeability
  → Diagnose failures
  → Auto-fix branch-related issues
  → Retry flaky failures (up to 3×)
  → Process review feedback
  → Push + restart watcher
  → Repeat until merged/closed or human-help-required
```

**严格的 Stop Conditions**：

```markdown
## Stop Conditions (Strict)
Stop only when:
- PR merged or closed
- User intervention is required and Codex cannot safely proceed alone

Keep polling when:
- CI is still running/queued
- Review state is quiet but CI is not terminal
- CI is green and mergeable, but the PR is still open
- CI is green but blocked on review approval
```

**CI 失败分类逻辑**：

```markdown
## CI Failure Classification
- Branch-related → auto-fix and push
- Flaky/unrelated → retry up to 3×, then stop for human help
- Ambiguous → one manual diagnosis attempt before choosing
```

**为什么这很重要**：大部分 Skill 写到最后是"生成一份报告"或"审查一份代码"。babysit-pr 展示了 Skill 的另一种可能：**持续运行、自主决策、直到终点条件满足才停止**。这不是"工具"，而是"进程"。

**课程连接**：对应第 11 章 Pipeline 模式和第 18 章 Hooks。babysit-pr 把 Pipeline 从"一步一 Gate"升级到了"持续监控 + 自动修复 + 条件终止"。

---

### 特征二：Subagent 并行审查（code-review）

Codex 不做单一的代码审查，而是用一个**编排器 Skill** 启动 5 个 Subagent 并行审查：

```text
code-review (orchestrator)
  ├── subagent: code-review-breaking-changes
  ├── subagent: code-review-change-size
  ├── subagent: code-review-context
  ├── subagent: code-review-testing
  └── (others)
```

**编排器核心逻辑**：

```markdown
Use subagents to review code using all code-review-* skills.
One subagent per skill. Pass full skill path to subagents. Use xhigh reasoning.

You must return every single issue from every subagent.
Each finding must include a specific file path and line number.
```

**各审查维度极度领域化**：

| 审查维度 | 规则 | 通用性 |
|---------|------|--------|
| `code-review-change-size` | 非机械变更上限 800 行，复杂逻辑变更上限 500 行 | 较高 |
| `code-review-breaking-changes` | 只检查 app-server APIs、CLI 参数、config loading、session resume | 极低 |
| `code-review-context` | 模型上下文不超 10K token、必须实现 ContextualUserFragment trait | 极低 |
| `code-review-testing` | agent 逻辑变更必须有 `core/suite` 下的集成测试 | 极低 |

**为什么这很重要**：普通审查 Skill 给一堆通用 checklist，Agent 扫一遍交差。Codex 的审查是：**一个编排器分发，5 个 Subagent 以 xhigh reasoning 并行审查，每个只盯一个维度，每个维度都是精确到代码库具体 trait、具体文件路径的领域规则。**

**课程连接**：对应第 09 章 Reviewer 模式。Codex 把它推到了极致：不止流程与规则分离，还要审查维度之间并行独立。

---

### 特征三：注意力标记系统（codex-issue-digest 的 🔥🔥）

这个 Skill 最创新的设计是：**用数据驱动的注意力标记替代人工判断优先级**。

```text
注意力标记算法：
- 基线（24h窗口）：≥5 个独立用户交互 → 🔥，≥10 个 → 🔥🔥
- 时间缩放：1周窗口 → 35 和 70 个交互
- 独立用户去重：同一用户多次操作只计一次
- Bot 排除：看真实用户行为，排除机器人
```

**摘要输出模式**：

```markdown
## Summary
Two issues are being surfaced by users:
🔥🔥 Terminal launch hangs on startup [1](...)
🔥 Resume switches model providers unexpectedly [2](...)
```

**为什么这很重要**：普通"issue 摘要" Skill 让 Agent 自己判断哪个重要，但 Agent 容易被标题党误导。Codex 用**可量化的算法**替代主观判断：不是 Agent 觉得重要，而是"过去 24h 有 12 个独立用户在这个 issue 上留下了交互"。

**课程连接**：对应第 24 章"六类评估指标"。🔥🔥 系统本质上是一套**自动化的"信号 vs 噪声"分离器**，让 Agent 的注意力聚焦在真正需要人工关注的议题上。

---

### 特征四：极度领域化的知识固化（path-types）

这是整个仓库中"最不通用但最体现 Skill 价值"的一个。

```markdown
# Path Types
- 在 app-server 协议类型中，使用 LegacyAppPathString
  在协议边界转换为 PathUri，内部使用 PathUri
- 在 exec-server 协议类型中，使用 PathUri
- 共享依赖中，使用 PathUri 或分离 API
- 模型工具调用参数：反序列化为普通 String，组件特定的路径处理
```

**迁移约束清单**：

```markdown
* 现有 app-server 客户端继续发送原生路径字符串
* app-server 可以保留和操作异构平台的 path URI
* exec-server API 使用 file:// URI
* 本地操作不能改变模型可见文本
* URI 不能显式编码执行器的路径约定或操作系统
* 用户不能配置环境 OS/路径约定
* URI 不应存储在 rollouts、数据库等持久化存储中
```

**为什么这很重要**：这个 Skill 的内容不可能在任何通用 Skill 或教程中找到。它是 Codex 团队在迁移到 URI 路径系统时，把**所有踩过的坑和架构约束**压缩成的领域规则。这正是第 13 章"Gotchas 最有价值"的极致体现——不是"常见错误"，而是"这个代码库在这个时间点上的所有禁区"。

**课程连接**：对应第 13 章"Gotchas 坑点"和第 12 章"不写已知知识"。path-types 是终极补充知识型 Skill：补的不是"Rust 怎么用"，而是"Codex 的路径类型迁移到了哪个阶段、有哪些绝对不能做的边界"。

---

### 特征五：失败路径是流程的第一等公民（update-v8-version）

```markdown
# Update V8 Version

## Core Workflow
1. Read third_party/v8/README.md
2. Update 5 specific files
3. Run 3 specific validation scripts
4. Validate via v8-canary CI

## Failure Path
1. Capture failing target and first actionable error
2. Compare current vs target version deltas
3. Track build-relevant deltas across 6 categories
4. Trace each failing delta into Codex's build graph (4 files)
5. Update only pieces required to restore build
6. Re-run focused validation
```

**为什么这很重要**：大部分 Skill 只写 Happy Path。Codex 的 `update-v8-version` 把 Happy Path 和 Failure Path 写成并列的第一级结构——失败不是一个"怎么办"的附注，而是流程的另一半。

**课程连接**：对应第 11 章 Pipeline 模式。Codex 补了一课：Pipeline 不应该只有一个分支，要写 Failure Path 作为明确的、并列的流程。

---

## 与课程五大模式的映射

| 课程模式 | Codex Skill 中的体现 | 创新与突破 |
|----------|---------------------|-----------|
| **Pipeline 模式** | `babysit-pr`（持续监控循环）、`update-v8-version`（含 Failure Path） | 把 Pipeline 从"一次性的步骤链"升级为"持续循环直到条件满足"，失败路径是第一等公民 |
| **Reviewer 模式** | `code-review`（Subagent 编排器 + 5 个领域审查 Skill） | Subagent 并行审查替代单一审查，每个 Subagent 只盯一个极端领域化的维度 |
| **Generator 模式** | `codex-pr-body`（PR 描述生成）、`codex-issue-digest`（Issue 摘要） | 不是自由生成，而是严格遵循输出结构（net change、attention markers） |
| **ToolWrapper 模式** | `path-types`、`remote-tests`、`test-tui` | 封装的是代码库特定的类型规则和工具约束，不是通用 SDK |
| **Inversion 模式** | `codex-bug`（先确认 issue URL 和 repo 正确性才能继续）、`codex-pr-body`（先检查 existing body 是否有不可恢复的内容） | Inversion 不仅用于需求澄清，还用于防止数据丢失 |

---

## 最值得拆开的 6 个经典 Skill

### 1. babysit-pr：持续自主监控的工业级实现

**类型**：Pipeline + Continuous Monitoring

**为什么值得学**：
- 把 Skill 从"执行一个任务"升级为"持续监控直到条件满足"
- 严格的 Stop Conditions：绿 + review-clean + mergeable 只是进度，不是终点
- CI 失败分类：branch-related vs flaky/unrelated 的明确标准
- 每 push 后不停止，自动重启 watcher

**可迁移的结构**：任何需要"持续等待 + 自动修复 + 按条件终止"的流程都可以用这个模式。

---

### 2. codex-issue-digest：注意力量化系统

**类型**：Generator + Attention Algorithm

**为什么值得学**：
- 用算法而非主观判断决定"什么值得关注"
- 🔥🔥 阈值随窗口大小缩放
- 摘要和详情分两次输出（默认摘要，按需详情）
- 明确提出集群概念：多 issue 共享同一产品问题时自动聚合

**可迁移的结构**：任何需要"从大量信息中筛选信号"的 Skill 都可以借鉴注意力标记系统。

---

### 3. codex-bug：领域 Bug 诊断流程

**类型**：Pipeline + Inversion

**为什么值得学**：
- 输入验证前置（必须是 `github.com/openai/codex/issues/…` URL）
- 先总结再调查（避免猜测式诊断）
- 三条处置路径：Verify with sources / Request more info / Explain not a bug
- 以 Thread ID 为核心的数据查找方式

**可迁移的结构**：任何"诊断 + 分类 + 决定下一步"的 Skill。

---

### 4. path-types：领域知识固化的终极形态

**类型**：Domain Knowledge + Constraints

**为什么值得学**：
- 不是"建议"，是"当前迁移阶段的状态描述"
- 区分了协议层、内部层、共享层的不同规则
- 明确标注"以下是迁移要求，不是永久设计"

**可迁移的结构**：为团队内部"正在进行的架构迁移"创建 Skill，让 Agent 和人在同一个迁移状态上操作。

---

### 5. code-review：Subagent 并行审查编排

**类型**：Reviewer Orchestrator

**为什么值得学**：
- 编排器本身不审查，只分发和聚合
- `Use xhigh reasoning` 明确对推理深度的要求
- `You must return every single issue` 确保不遗漏
- 要求每个 finding 有具体文件路径和行号

**可迁移的结构**：任何需要多维度审查的场景，可以用这个编排器模式替代单一大而全的审查 Skill。

---

### 6. update-v8-version：失败路径是第一等公民

**类型**：Pipeline + Failure Path

**为什么值得学**：
- Happy Path 和 Failure Path 并列
- 失败时精确到 6 类 build-relevant deltas
- 只修需要修的部分："Update only the pieces required to restore the target version's build"
- 每次修复后重新聚焦验证

**可迁移的结构**：任何有高失败率的操作流程，都值得把 Failure Path 写成和 Happy Path 并列的流程。

---

## 与已有附录的定位对比

| 附录 | 回答的核心问题 |
|------|-------------|
| addyosmani/agent-skills | 一个完整的软件工程团队应该把哪些流程写成 Skill？ |
| Anthropic 9大分类 | 你的 AI 研发团队缺哪一类能力？ |
| garrytan/gstack | 单人兼职开发者如何用 Skill 模拟完整虚拟工程团队？ |
| google/skills | 平台方如何为 Agent 构建既安全又好用的产品入口？ |
| **openai/codex** | **当 Skill 被推到极端领域化时能达到什么深度？** |

Codex 的 Skill 不适合全量迁移，但它的 **"极度具体"** 本身就是一种设计哲学：不要写"帮助审查代码"的 Skill，要写"检查本次 PR 是否在核心路径文件中引入了大于 10K token 的模型上下文项，该类必须实现 ContextualUserFragment trait"的 Skill。

---

## 8 条启发：从 Codex Skill 学到的设计哲学

### 1. 最好的 Skill 是领域化的，不是通用的

Codex 的 14 个 Skill 没有一个可以原样迁移给另一个项目。但这恰恰是它们的价值——它们把 Codex 代码库特有的约束变成了 Agent 可执行的规则。

**启发**：不要纠结"这个 Skill 能不能开源给所有人用"。先解决你自己代码库里最痛的 3 个工程问题，把它们写成极度具体的 Skill。

---

### 2. 持续监控比一次性审查更有价值

babysit-pr 的价值不在于"检查一次 PR 状态"，而在于"持续看着它直到合并，中间自动处理 CI 失败、Review 反馈、Retry 重试"。

**启发**：思考哪些流程应该是**持续性进程**（daemon-like Skill），而不是**一次性任务**（one-shot Skill）。

---

### 3. 编排器 + 子 Skill 比大而全的 Skill 更好

Codex 没有做一个 `code-review-all` 的 Skill，而是用一个轻量编排器并行调用多个专注的审查 Skill。

**启发**：拆分为多个小 Skill 并用编排器组合，比一个大而全的 Skill 更灵活、更容易维护。

---

### 4. 用可量化算法替代主观判断

`codex-issue-digest` 不依赖 Agent "觉得"哪个 issue 重要，而是用量化的用户交互计数 + 时间窗口缩放算法。

**启发**：当需要有优先级判断时，尽量给出可量化的标准而非"请根据重要性排序"。

---

### 5. 失败路径要写成第一等流程

大多数 Skill 只写 Happy Path，失败处理放在末尾或省略。Codex 的 `update-v8-version` 把 Failure Path 写成和 Core Workflow 并列的章节。

**启发**：如果某个操作的失败率超过 20%，把 Failure Path 写成平行的、独立的流程块。

---

### 6. "Net Change" 思维方式

`codex-pr-body` 强调"讨论的是净变更，不是开发过程中的探索和回退"。这避免了 Agent 在 PR 描述中写"我先试了 A，发现不行，又试了 B…"

**启发**：当 Skill 要求 Agent 产出面向他人的文档时，明确"你现在应该讲的是什么故事"。

---

### 7. 明确标注代码库所处状态

`path-types` 不假装自己是"永久的 path 规范"，它明确写："这是当前迁移阶段的状态，这些约束可能会变。"

**启发**：为正在演进的架构创建 Skill 时，标注"这是当前状态，不是永久真理"，并给出判断标准。

---

### 8. State Mutation Policy 是生产级 Skill 的必备

babysit-pr 有明确的 **GitHub State Mutation Policy**：

```markdown
You can: push to update code, resolve your own review threads
Do NOT: comment on others' threads, close/reopen PRs,
         make changes that blur the line between human and bot actions
```

**启发**：任何会改变外部系统状态的 Skill，必须有明确的"你能改变什么、不能改变什么"的边界宣言。

---

## 对比本课程：它补充了什么

| 本课程关注点 | openai/codex 的补充 |
|--------------|-------------------|
| 五大模式 | Pipeline → 持续监控循环；Reviewer → Subagent 并行编排；Generator → 注意力量化算法 |
| 三档自由度 | 低自由度：path-types（精确到 trait 和字段）；高自由度：babysit-pr（持续自主决策） |
| Gotchas | 从"常见错误"升级到"代码库当前迁移阶段的全部禁区" |
| 安全三原则 | GitHub State Mutation Policy：明确"能做什么、不能做什么" |
| Pipeline 模式 | Happy Path + Failure Path 并列，失败不是附注 |
| 文件组织 | Subagent 编排器 + 领域审查 Skill 的分层架构 |

如果说本课程教你"Skill 的设计方法论"，其他附录教你"不同场景下的 Skill 分类和实践"，Codex 教你的是：

> **Skill 被推到极端领域化时能达到什么深度——它不是"帮我做代码审查"，而是"在这个代码库的这条规则上，用这个检查维度，以 Subagent 并行方式审查"。**

---

## 如何把它用于团队实践

### 第一步：不做"通用"Skill，做"你的代码库"的 Skill

打开你的代码库，找出：
- 最复杂的 CI 流程
- 最容易被改坏的模块
- 最频繁的 bug 报告类型
- 正在进行中的架构迁移

把这些写成极度领域化的 Skill。

### 第二步：把"等待"变成"持续监控"

如果你的流程有"等 CI 通过""等 Review 反馈""等测试完成"这类环节，参考 babysit-pr 做持续监控循环，而不是期望 Agent 自己记得回来看。

### 第三步：审查用编排器 + 子 Skill 模式

```text
review-orchestrator
  ├── review-module-A（只审 Module A 的特定规则）
  ├── review-module-B（只审 Module B 的特定规则）
  └── review-common（审跨模块通用规则）
```

### 第四步：有外部状态变更就要写 Mutation Policy

```markdown
## Mutation Policy
You can:
- [允许的操作 1]
- [允许的操作 2]

Do NOT (unless explicitly asked):
- [禁止的操作 1]
- [禁止的操作 2]
```

### 第五步：高失败率流程写 Failure Path

如果某个操作的失败率超过 20%，不要只写"如果失败，请联系用户"，而是像 `update-v8-version` 那样写一个完整的 Failure Path 流程。

---

## 小结

openai/codex 的 14 个真实 Skill 展示了领域化 Skill 的最高水准，尤其值得学习 5 点：

1. **极度领域化**：Skill 精确到代码库的具体文件路径、Rust trait、V8 版本号
2. **持续监控优先**：babysit-pr 证明了 Skill 可以是持久运行的自主进程
3. **Subagent 编排**：用编排器 + 并行子 Skill 替代大而全的单体审查
4. **注意力量化**：用可计算算法替代 Agent 主观判断优先级
5. **失败是第一等路径**：Happy Path 和 Failure Path 并列，不是附注

它给我们的最大启发是：

> **最好的 Skill 不适合直接迁移给其他项目。它的价值恰恰在于它的不可迁移性——它把你代码库里最复杂、最独特、最难传递的那部分知识，变成了 Agent 可执行的领域规则。**

