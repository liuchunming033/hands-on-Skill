> 学习目标：从 obra/superpowers 的 14 个 Skill 中，学习如何用"反借口清单 + 铁律 + 硬性门禁"构建一套 Agent 无法绕过的完整软件工程纪律系统

---

> 这是本教程的参考资料，用于帮助团队从 Superpowers 开源项目中学习社区驱动的完整软件工程方法论。
>
> **代码库地址**：https://github.com/obra/superpowers
>
> **阅读对象**：已经学完本教程前 27 章，希望理解社区如何用 Skill 构建一整套 Agent 不可绕过的工程纪律系统的读者。

## 先给结论

superpowers 最值得学的不是它的 14 个 Skill 各有什么功能，而是它揭示了一个极其反直觉的事实：

**Agent 的问题不是能力不够，而是太擅长为自己找借口。**

你告诉 Agent "先写测试"，它会说"这个太简单了不需要测试"。你告诉 Agent "先做设计"，它会说"让我先看看代码再回来讨论设计"。每一次它都有非常合理的理由。

Superpowers 的解决方案不是更详细的指令，而是 **两道防线**：

1. **Red Flags 表**：提前列出 Agent 会为自己找的所有借口，并逐一驳斥
2. **Iron Law**：把关键纪律写成绝对禁令，不留下任何"视情况而定"的余地

```
"Even a 1% chance a skill might apply → You MUST invoke it"
"NO production code without a failing test first"
"NO completion claims without fresh verification evidence"
```

这正好对应本教程反复强调的观点：**Skill 不是资料库，而是决策框架和执行边界**。Superpowers 把"执行边界"推到了极致——它不是"建议 Agent 遵循流程"，而是"预先封堵 Agent 可能走的每一条捷径"。

---

## 核心价值：为什么这个 233K Star 的库值得学

| 附录 | 核心创新 | 解决的问题 |
|------|---------|-----------|
| addyosmani/agent-skills | 强制校验门禁 + 反借口清单 | Agent 跳过质量检查 |
| Anthropic 9大分类 | 四环节能力诊断 | 团队不知道缺什么 Skill |
| garrytan/gstack | 虚拟团队角色扮演 | 单人开发者需要多角色协作 |
| google/skills | Denylist + Data Reduction | Agent 在危险操作面前不自然停住 |
| openai/codex | 极度领域化 + 持续监控 | 通用 Skill 对特定代码库作用有限 |
| **superpowers** | **Red Flags + Iron Law + Hard Gate** | **Agent 总是能找到看似合理的理由绕过流程** |

**核心问题**：你说"先写测试"，Agent 说"这只是个小改动"；你说"先做设计"，Agent 说"我先看看代码"；你说"验证后再报告完成"，Agent 说"测试应该通过了"。**你怎么让 Agent 再也不能绕过去？**

Superpowers 的回答：**把 Agent 的每一句合理化借口都提前写进 Red Flags 表，并在旁边写上正确答案。**

---

## 仓库基本结构

`skills/` 目录包含 14 个 Skill，可分为 4 大环节：

| 环节 | Skill | 核心机制 |
|------|-------|---------|
| **启动与元认知** | `using-superpowers` | 1% 规则 + Red Flags 表 + Skill 优先级 |
| **设计与计划** | `brainstorming`、`writing-plans` | Hard Gate + 逐节审批 + 按步计划 |
| **执行与调试** | `subagent-driven-development`、`executing-plans`、`dispatching-parallel-agents`、`test-driven-development`、`systematic-debugging` | 文件传递 + 新鲜子代理 + Iron Law |
| **审查与交付** | `requesting-code-review`、`receiving-code-review`、`verification-before-completion`、`finishing-a-development-branch`、`using-git-worktrees` | 审前 Gate + 证据优先 + 环境隔离 |

另有 `writing-skills` —— Agent 开发新 Skill 的方法论 Skill。

---

## 六大独特设计特征逐项解析

### 特征一：Red Flags 表 — 提前驳斥 Agent 的每一条借口

这是 Superpowers 最天才的设计。每个 Skill 都有一个 **"Red Flags"** 表，格式统一为：

```markdown
| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
```

**为什么这有效**：这些 "Thought" 不是编的——它们是 Agent 在真实会话中反复产生的合理化想法。当你告诉 Agent "先用 brainstorming"，它说"这次太简单了不需要"——这就是 Red Flag。当你告诉它"先检查有没有 Skill 可用"，它说"让我先探索一下代码库"——这也是 Red Flag。

**Red Flags 的核心设计原理**：不是"提醒 Agent 应该怎么做"，而是 **"当 Agent 脑子出现某个想法时，预先告诉它这个想法是错的"**。这从根本上改变了 Skill 和 Agent 的交互模式——从"建议"变成了"思想预先拦截"。

**教程连接**：对应第 03 章 description 和第 05 章三档自由度。Superpowers 把"低自由度"推到了最底层——不是在流程上低自由度，而是在**思维层面**堵住了每一条合理化借口。

---

### 特征二：Iron Law — 不可商量的绝对禁令

Superpowers 在关键纪律上使用了"铁律"模式，措辞极强：

```markdown
# systematic-debugging
## The Iron Law
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
If you haven't completed Phase 1, you cannot propose fixes.

# test-driven-development
## The Iron Law
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
Write code before the test? Delete it. Start over.

# verification-before-completion
## The Iron Law
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
If you haven't run the verification command in this message,
you cannot claim it passes.
```

每个 Iron Law 都附带一个统一的宣言：

```markdown
Violating the letter of this rule is violating the spirit of this rule.
```

**为什么措辞这么强**：因为措辞弱 Agent 就会找借口。"建议先写测试"→ Agent 会说"这次太简单了"。"NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"→ Agent 没有可绕过的语义空间。

**与 google/skills 的 Denylist 对比**：

| 维度 | google/skills Denylist | superpowers Iron Law |
|------|----------------------|---------------------|
| 防御对象 | 危险操作 | 思维捷径 |
| 形式 | 命令黑名单 | 行为绝对禁令 |
| 违反后果 | 操作被阻断 | "你说谎了"（道德层面） |
| 适用范围 | CLI 操作 | 所有工程行为 |

**教程连接**：对应第 27 章 Skill 安全三原则。Superpowers 的安全边界不是"不要执行危险命令"，而是"不要在思维上走捷径"。

---

### 特征三：Hard Gate — 不可跳过的检查点

`brainstorming` Skill 在开头就设置了一个不可跳过的门：

```markdown
<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project,
or take any implementation action until you have presented a design and the
user has approved it. This applies to EVERY project regardless of perceived
simplicity.
</HARD-GATE>
```

紧接着就是 **"Anti-Pattern: This Is Too Simple To Need A Design"** 段落——又一次提前封堵 Agent 最常见的合理化理由。

**Brainstorming 的 9 步检查清单**（必须按顺序完成）：

```text
1. Explore project context
2. Offer visual companion just-in-time
3. Ask clarifying questions (one at a time)
4. Propose 2-3 approaches
5. Present design (section by section, get approval per section)
6. Write design doc → commit
7. Spec self-review (placeholders, consistency, scope, ambiguity)
8. User reviews written spec
9. Transition to writing-plans
```

**教程连接**：对应第 11 章 Pipeline 模式的 Gate 机制。Superpowers 的 Gate 不是"验证条件"，而是"在思维层面禁止跳过"。

---

### 特征四：文件传递 — Subagent 不给上下文，给文件

这是 Superpowers 的 `subagent-driven-development` 中最工程化的创新。

```markdown
## File Handoffs
Everything you paste into a dispatch prompt stays resident in your context
for the rest of the session. Hand artifacts over as files:

- Task brief: scripts/task-brief PLAN_FILE N (extracts task text to file)
- Report file: implementer writes report to file, returns only status + commits
- Reviewer inputs: brief + report + review-package (never paste diffs)
- Fix subagent: appends fix report to same file
```

**为什么这很重要**：大部分 Skill 让 Agent 把上下文粘贴到 Subagent prompt 里。但这些粘贴的内容会**永久驻留在主会话的上下文窗口**中，导致上下文膨胀和注意力稀释。文件传递让 Subagent 通过路径读文件，主 Agent 的上下文保持干净。

**与教程的关系**：这是第 14 章"渐进式披露"的运行时版本——不仅是 Skill 内容按需加载，连**任务执行中的信息传递**也要按需走文件。

---

### 特征五：进度账本（Progress Ledger）— 跨越上下文压缩的记忆

```markdown
## Durable Progress
Conversation memory does not survive compaction. In real sessions,
controllers that lost their place have re-dispatched entire completed
task sequences — the single most expensive failure observed.

- Check for ledger: .superpowers/sdd/progress.md
- When task review comes back clean: append one line
- After compaction: trust the ledger and git log, not your memory
```

**格式**：
```
Task 1: complete (commits a1b2c3d..e4f5g6h, review clean)
Task 2: complete (commits i7j8k9l..m0n1o2p, review clean)
```

**为什么这很重要**：Agent 会话压缩（compaction）后，Agent 会**忘记已完成哪些任务**。没有 ledger，Agent 会重复派发已完成的任务——这是 Superpowers 团队在实际使用中观察到的最昂贵故障。Ledger 用文件系统（不受压缩影响）做耐久性记忆。

**教程连接**：对应第 16 章"设置流程与内存——让 Skill 有记忆"。Superpowers 把"内存"从 config.json 扩展到了进度账本，解决了会话压缩导致的任务重复派发问题。

---

### 特征六：模型分层选择 — 任务难度驱动的算力分配

```markdown
## Model Selection
Use the least powerful model that can handle each role.

- Mechanical implementation (1-2 files, complete spec) → cheap model
- Integration/judgment (multi-file, pattern matching) → standard model
- Architecture/design → most capable model
- Review → matched to diff size, complexity, and risk

Always specify the model explicitly when dispatching.
An omitted model inherits your session's model — often the most expensive.
```

**为什么这很重要**：大多数 Skill 不关心模型选择。Superpowers 把模型选择写成了流程的一部分——不是"用一个模型跑完所有任务"，而是"机械转录用便宜模型，架构判断用强模型，审查用匹配风险的模型"。

---

## 与教程五大模式的映射

| 教程模式 | Superpowers 体现 | 创新点 |
|----------|-----------------|--------|
| **Pipeline 模式** | `brainstorming` → `writing-plans` → `subagent-driven-development` → `requesting-code-review` → `finishing-a-development-branch` | Iron Law + Hard Gate + Red Flags 三重保障 |
| **Reviewer 模式** | `requesting-code-review`（Subagent 审查）、`subagent-driven-development`（任务审查 + 最终审查） | Subagent 审查 + 文件传递（不给上下文给文件路径） |
| **Inversion 模式** | `brainstorming`（9 步需求澄清流程）、`systematic-debugging`（先找根因再修复） | Red Flags 提前封堵"太简单不需要设计"的借口 |
| **Generator 模式** | `writing-plans`（标准化计划模板 + Global Constraints + 按步任务） | 每个计划有 Global Constraints header + bite-sized 任务格式 |
| **ToolWrapper 模式** | `using-git-worktrees`、`dispatching-parallel-agents` | 把 git worktree 和并行 agents 封装为可组合操作 |

---

## 10 条启发：从 Superpowers 学到什么

### 1. 知道 Agent 会找什么借口，就提前驳斥它

不是"提醒 Agent 注意"，而是写 Red Flags 表：

```markdown
# ❌ 弱写法
注意：请务必先检查是否有 Skill 可用。

# ✅ Superpowers 写法
| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
```

---

### 2. 关键纪律用绝对禁令，不留语义空间

```markdown
# ❌ 弱写法
建议先写测试再写代码。

# ✅ Superpowers 写法
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.
Write code before the test? Delete it. Start over.
```

---

### 3. Hard Gate 要有配套的 Anti-Pattern 段落

光有 Gate 不够，还必须预判 Agent 会怎么绕过它：

```markdown
<HARD-GATE> ... </HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"
Every project goes through this process. A todo list, a single-function
utility, a config change — all of them.
```

---

### 4. Subagent 传递信息用文件，不要粘贴进 prompt

```bash
# ✅ 文件传递
scripts/task-brief PLAN_FILE 3  # 提取 Task 3 到文件
# Subagent prompt: "read path/to/task-3-brief.md — this is your requirements"

# ❌ 粘贴传递
# Subagent prompt: "Here's the plan: [50KB of plan text pasted in-line]"
```

---

### 5. 用 Ledger 解决会话压缩导致的记忆丢失

```bash
cat "$(git rev-parse --show-toplevel)/.superpowers/sdd/progress.md"
# Task 1: complete (commits a1b2c..d4e5f, review clean)
# Task 2: complete (commits g6h7i..j8k9l, review clean)
# → 从 Task 3 继续，不要重新派发 Task 1 和 2
```

---

### 6. 禁止模型降级写入成本

```markdown
Always specify the model explicitly when dispatching a subagent.
An omitted model inherits your session's model — often the most
capable and most expensive — which silently defeats this section.
```

---

### 7. 验证不是"感觉完成"，是"证据在输出里"

```markdown
| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Agent completed | VCS diff shows changes | Agent reports "success" |
```

---

### 8. 把"视情况选择"写成流程图

Superpowers 在 `subagent-driven-development`、`dispatching-parallel-agents`、`using-superpowers` 等多个 Skill 中使用 Graphviz 流程图来描述决策树。

**启发**：当有多个分叉决策点时，流程图比文字更容易避免 Agent "跳过检查"。

---

### 9. CI/CD 不属于核心，让分支完成流程处理

Superpowers 没有 CI/CD Skill。`finishing-a-development-branch` 负责验证 → 呈现选项（合并/PR/保留/丢弃）→ 清理工作树。CI/CD 由外部系统处理。

**启发**：不要试图把所有事都做成 Skill。明确 Skill 的边界在哪里。

---

### 10. writing-skills — 用 Skill 写 Skill

Superpowers 内置了一个 `writing-skills` Skill，专门用来开发新 Skill。它有自己的方法论、测试标准、压力测试要求。

**启发**：Skill 开发本身也是一个可以用 Skill 规范化的流程。

---

## 与已有附录的定位对比

| 附录 | 回答的核心问题 |
|------|-------------|
| addyosmani/agent-skills | 一个完整软件工程团队应该把哪些流程写成 Skill？ |
| Anthropic 9大分类 | 你的 AI 研发团队缺哪一类能力？ |
| garrytan/gstack | 单人兼职开发者如何用 Skill 模拟完整虚拟工程团队？ |
| google/skills | 平台方如何为 Agent 构建既安全又好用的产品入口？ |
| openai/codex | 当 Skill 被推到极端领域化时能达到什么深度？ |
| **superpowers** | **如何让 Agent 无法绕过你设定的工程纪律？** |

Superpowers 的 Skill 不适合单独使用——它是一个**完整的纪律系统**（14 个 Skill 互相引用、流程串联）。但它的 Red Flags 表 + Iron Law + Hard Gate 三重保障设计范式，可以单独迁移到任何 Skill 中。

---

## 对比本教程：它补充了什么

| 本教程关注点 | superpowers 的补充 |
|--------------|-------------------|
| description 写法 | `using-superpowers` 的 description 是触发条件，附带 SUBAGENT-STOP 豁免标记 |
| 三档自由度 | 最低自由度不是"步骤"，而是思想层面的 Red Flags 预拦截 |
| Pipeline 模式 | Iron Law + Hard Gate + Anti-Pattern 段落的三重保障 |
| Reviewer 模式 | Subagent 审查 + 文件传递（不给上下文给文件路径） |
| Gotchas | 升级为 Red Flags 表（Agent 会产生的想法 → 现实是什么） |
| 文件组织 | 跨 Skill 引用（`../requesting-code-review/code-reviewer.md`） |
| 内存 | Progress Ledger：跨越会话压缩的耐久性记忆 |
| 脚本 | `scripts/task-brief`、`scripts/review-package`：信息传递的文件化 |
| 安全 | 不是操作安全，而是**思维纪律安全**：不让你在思维上走捷径 |

---

## 如何把它用于团队实践

### 第一步：给现有 Skill 加 Red Flags 表

拿出你最常用的 3 个 Skill，为每个写 5 条 Red Flags：

```markdown
## Red Flags
| Thought | Reality |
|---------|---------|
| [Agent 会产生的合理化想法 1] | [正确做法] |
| [Agent 会产生的合理化想法 2] | [正确做法] |
```

问自己：Agent 最近一次绕过这个 Skill 时说的理由是什么？把它写进 Left 列。

### 第二步：把最关键的一条纪律升级为 Iron Law

```markdown
## The Iron Law
NO [X] WITHOUT [Y] FIRST
Violating the letter of this rule is violating the spirit of this rule.
```

只升级一条——你团队最痛的那条纪律。

### 第三步：给关键 Gate 加 Anti-Pattern 段落

```markdown
<HARD-GATE>
...
</HARD-GATE>

## Anti-Pattern: "[Agent 最常见的绕过理由]"
...
```

### 第四步：如果团队有长任务，加 Progress Ledger

```bash
LEDGER="$(git rev-parse --show-toplevel)/.my-team/progress.md"
# 每个任务完成后追加一行
echo "Task N: complete (commits ...)" >> "$LEDGER"
```

### 第五步：Subagent 传递信息走文件，不粘贴

参考 `scripts/task-brief` 和 `scripts/review-package` 的模式，把你团队 Subagent 间传递的大段信息写到文件里。

---

## 小结

superpowers 是社区驱动的完整 Agent 工程纪律系统，尤其值得学习 5 点：

1. **Red Flags 表**：提前列出 Agent 会产生的每一条合理化想法并驳斥，从思维层面堵住捷径
2. **Iron Law**：关键纪律写成绝对禁令，"违反字面就是违反精神"
3. **Hard Gate + Anti-Pattern**：不只是"不准跳过"，还预判 Agent 会用"这太简单了"来试图跳过
4. **文件传递**：Subagent 间传递信息走文件路径，不粘贴进 prompt，保护上下文窗口
5. **Progress Ledger**：用文件系统跨越会话压缩，避免 Agent 丢失记忆后重复派发已完成的任务

它给我们的最大启发是：

> **Agent 不是不听话，是大擅长为自己不听话找理由。好 Skill 在 Agent 还没开口之前就已经把它的每一条理由堵死了。**

