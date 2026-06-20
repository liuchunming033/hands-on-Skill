> 学习目标：理解 gstack 完整产品研发流程的核心概念和实践方法

---

> 这是本课程的参考资料，用于帮助团队从 gstack 项目中学习创业者导向的完整产品交付流程。
>
> **代码库地址**：https://github.com/garrytan/gstack

## 前言

gstack 是一个完整的产品研发流程 Skill 库，由 Y Combinator（YC）总裁兼 CEO Garry Tan 主导创作。

**核心理念**：gstack 是一个流程（process），不是工具集合。这套 Skill 模拟完整虚拟工程团队，覆盖从需求思考到复盘反思的完整研发闭环。

**核心流程**：

```
Think → Plan → Build → Review → Test → Ship → Reflect
思考 → 规划 → 构建 → 审查 → 测试 → 发布 → 反思
```

**核心价值**：单人兼职开发状态下，仍能持续交付生产级服务与功能。

---

## 作者背景

### 核心作者：Garry Tan（加里·谭）

**官方身份**：
- Y Combinator（YC）总裁兼 CEO
- 深耕创业、软件工程 20 年
- 服务数千初创团队（Coinbase、Instacart、Rippling 等早期孵化）

**过往履历**：
- Palantir 早期工程师 / 产品负责人
- Posterous 联合创始人（后出售给 Twitter）
- YC 内部社交产品 Bookface 搭建者

**项目归属**：
- GitHub 账号 garrytan 为个人账号
- garrytan/gstack 是单人独立开源项目
- MIT 开源协议，无企业官方团队托管
- 是他日常自用的 Claude Code 全套 Skill 工程体系
- 对外完全免费开放

---

## 项目完整来历

### 诞生背景与创作动机

**灵感源头：Andrej Karpathy 播客观点**

2026 年 3 月，Karpathy 在《No Priors》播客提出核心观点：

> "现在开发者几乎不需要手写原生代码，依靠 AI Agent 可以单人完成二十人团队量级的交付效率。"

Garry Tan 听完后产生验证想法：自己身兼 YC CEO，全职运营孵化器之余只能抽碎片时间开发，希望搭建一套标准化 AI 工作流工具，把 AI 从"简单代码补全"升级为完整虚拟工程团队。

---

### 个人痛点：传统 AI 工具效率极低

**Garry Tan 自身真实痛点**：

1. **普通 Prompt 零散无流程约束**：
   - AI 容易产出劣质"AI 垃圾代码（AI slop）"
   - 忽略架构设计
   - 跳过测试验证
   - 上线爆 Bug

2. **市面 Skill 缺少完整研发闭环**：
   - 零散的 Skill 没有从需求→规划→设计→编码→评审→测试→发布→复盘的标准化流水线
   - 无法模拟完整团队协作

3. **单人兼职开发，时间极度碎片化**：
   - 需要一套强约束、自动化的 AI 协作体系
   - 大幅提升交付速度

---

### 效率数据佐证开发初衷

**Garry Tan 给出个人开发数据对比**：

| 年份 | 工作方式 | GitHub 贡献次数 | 效率提升 |
|------|---------|---------------|---------|
| 2013 | 无 AI，手动写 Bookface | 全年 772 次 | 基线 |
| 2026 | 使用自研 gstack | 前 4 个月 1237 次 | **240 倍** |

**关键数据**：
- 同等时间产出是 2013 年的 240 倍
- 单位有效代码产出提升约 **810 倍**
- 代码统计标准：不看 AI 生成的冗余垃圾，只统计逻辑变更
- 这套工具让兼职状态下仍能持续交付生产级服务与功能

---

### 项目定位

**gstack 不是单一工具或零散 Skill，而是完整标准化 Claude Code 技能仓库**：

**核心特点**：

1. **完整研发全流程角色封装**：
   - 把一整套软件研发全流程封装为数十个斜杠命令 Skill
   - 模拟完整虚拟工程团队

2. **23 类专业角色模拟**：
   - CEO、产品经理、架构师、设计师、安全官、QA、发布工程师、运维等
   - 每个角色对应独立的 Skill

3. **配套工具完善**：
   - 浏览器自动化
   - 安全审计
   - 文档生成
   - 跨 AI 对比工具

---

## 真实架构：Skill 工程体系的四大基石

gstack 的真实架构远比"七步流程"精妙。它有四个相互咬合的层次：

```text
ETHOS.md (建造者信念宣言，注入每个 Skill)
  → Skill YAML 层 (preamble-tier + triggers + allowed-tools + gbrain)
    → Preamble Bash (会话状态初始化 + 遥测 + 学习记忆)
      → Skill 正文 (执行逻辑)
```

### 基石一：Ethos 注入 —— 每个 Skill 的灵魂预载

每个 gstack Skill 在 preamble 中都会加载 `ETHOS.md`。这不是"参考资料"，而是每个技能启动时都会读到的信念宣言：

```markdown
## The Golden Age
A single person with AI can now build what used to take a team of twenty.
The engineering barrier is gone. What remains is taste, judgment, and the
willingness to do the complete thing.
```

**关键数据表**（ETHOS.md 核心内容）：

| 任务类型 | 人类团队 | AI 辅助 | 压缩比 |
|---------|---------|--------|--------|
| 样板代码/脚手架 | 2天 | 15分钟 | ~100x |
| 测试编写 | 1天 | 15分钟 | ~50x |
| 功能实现 | 1周 | 30分钟 | ~30x |
| Bug 修复+回归测试 | 4小时 | 15分钟 | ~20x |
| 架构/设计 | 2天 | 4小时 | ~5x |
| 研究/探索 | 1天 | 3小时 | ~3x |

**核心原则**："Boil the Ocean"（煮沸海洋）——旧时代说"不要做全"，因为工程时间是瓶颈。现在 AI 让完整性的边际成本趋近于零，所以永远做完整的事。

**课程连接**：对应第 08 章 Generator 模式的精神内核——不是"生成模板"，而是"永远输出完整产物"。Ehthos 通过 preamble 注入，确保每个 Skill 调用的 Agent 都带着"做全"的心态开工。

---

### 基石二：preamble-tier 编排系统 —— 技能触发顺序控制

gstack 的每个 Skill 都有一个 `preamble-tier` 字段（1-4），这决定技能在会话中的加载优先级：

| tier | 含义 | 代表 Skill |
|------|------|-----------|
| 1 (最高) | 基础设施级，最先加载 | `gstack`（浏览器自动化底座） |
| 2 | 会话/元数据级 | `retro`、`learn`、`gstack-upgrade` |
| 3 | 流程启动级 | `office-hours`、`document-generate`、`spec` |
| 4 (最低) | 执行/工具级 | `review`、`qa`、`ship`、`build`、`guard` |

**设计意图**：tier-1 的 `gstack` Skill 负责初始化整个会话环境（浏览器、遥测、会话计数、learning 加载），tier-3 负责需求澄清和设计，tier-4 负责具体执行。这不是"建议顺序"，而是 preamble 执行顺序。

---

### 基石三：Preamble Bash —— 通用会话初始化层

每个 gstack Skill 的正文前面都有一段 50+ 行的标准化 Bash preamble：

```bash
# 更新检查
_UPD=$(~/.claude/skills/gstack/bin/gstack-update-check 2>/dev/null)
# 会话管理
mkdir -p ~/.gstack/sessions
touch ~/.gstack/sessions/"$PPID"
# 主动性配置
_PROACTIVE=$(~/.claude/skills/gstack/bin/gstack-config get proactive)
# 分支检测
_BRANCH=$(git branch --show-current)
# 仓库模式
source <(~/.claude/skills/gstack/bin/gstack-repo-mode)
# 会话类型 (spawned/headless/interactive)
_SESSION_KIND=$(~/.claude/skills/gstack/bin/gstack-session-kind)
# 学习记忆加载
_LEARN_COUNT=$(wc -l < "$_LEARN_FILE")
# 遥测
~/.claude/skills/gstack/bin/gstack-timeline-log '{"skill":"...","event":"started",...}'
```

**为什么这很重要**：这不是"初始化代码"，而是 gstack 的**工程化核心**。每次 Skill 调用都自动完成：更新检查、分支识别、会话计数、仓库模式检测、学习记忆加载、遥测记录。把"工程基础设施"从 Agent 的记忆负担中剥离。

**课程连接**：对应第 18 章 Hooks 的最大规模实践——不是"拦截工具调用"，而是"每次 Skill 启动时自动运行基础设施代码"。

---

### 基石四：GBrain 上下文查询 —— Schema 驱动的跨会话记忆

gstack 的 `gbrain` 字段是一套**声明式上下文预加载系统**：

```yaml
gbrain:
  schema: 1
  context_queries:
    - id: prior-sessions
      kind: list           # API 查询
      filter:
        type: ceo-plan
        tags_contains: "repo:{repo_slug}"
      render_as: "## Prior office-hours sessions in this repo"
    - id: builder-profile
      kind: filesystem     # 文件系统查询
      glob: "~/.gstack/builder-profile.jsonl"
      tail: 1
      render_as: "## Your builder profile snapshot"
    - id: recent-learnings
      kind: filesystem
      glob: "~/.gstack/projects/{repo_slug}/learnings.jsonl"
      tail: 10
```

**为什么这很重要**：它解决了 Agent Skill 最痛的问题——跨会话记忆。不是"请 Agent 记住上次做了什么"，而是在 Skill 启动时自动从文件系统和 API 中加载上下文，以结构化标题注入。

**课程连接**：对应第 16 章"设置流程与内存——让 Skill 有记忆"的终极实现。不是 config.json，而是 schema 化的上下文预加载。

---

## 真实 Skill 分类：七个核心环节

gstack 的真实 Skill 不是 23 个角色，而是按研发闭环组织的 7 个环节：

| 环节 | 核心 Skill | 特征 |
|------|-----------|------|
| **Think** | `office-hours` | YC 面试模式 + 建造者模式，双模式切换，保存设计文档 |
| **Plan** | `spec` | 技术规格生成，API/数据模型/接口文档 |
| **Build** | `design` 系列、`build` | 设计咨询 + 代码实现 + iOS 专门技能 |
| **Review** | `review`、`design-review`、`devex-review` | Karpathy 四骑士 + 设计/开发体验审查 |
| **Test** | `qa`、`qa-only` | 三层 QA (Quick/Standard/Exhaustive)，自动修复+验证 |
| **Ship** | `ship`、`land-and-deploy` | 自动合并 + 测试 + CHANGELOG + PR 创建 |
| **Reflect** | `retro`、`learn` | 周度回顾 + 学习记忆持久化 |

---

### Think：office-hours 的 YC 面试模式

`office-hours` 不是"头脑风暴"，而是两套完整模式：

**Startup 模式**：六个强迫性问题——
1. 需求真实性：你真的见过用户因为这个痛苦吗？
2. 现状检查：用户现在怎么解决这个问题？
3. 绝望程度：这到底是维生素还是止痛药？
4. 最窄截面：你能切出的最小可用版本是什么？
5. 观察：你看到了什么别人没看到的？
6. 未来适配：为什么现在是对的时机？

**Builder 模式**（副项目/黑客松/开源）：标准设计思维流程。

**自动输出**：保存设计文档到 `~/.gstack/projects/{repo_slug}/*-design-*.md`，并通过 GBrain 加载历史设计文档和 builder profile。

**课程连接**：对应第 10 章 Inversion 模式的极致实践——不是"先问需求"，而是"用 YC 合伙人面试的标准先拷问需求"。

---

### Review：Karpathy 的四骑士

gstack 的 `review` Skill 使用了 Andrej Karpathy 提出的代码审查框架，专门用于在合并前自动审查 PR diff：

```text
Karpathy's Four Horsemen of the AI-pocalypse:
1. 错误假设 — 检查做了什么假设？这些假设是否成立？
2. 过度复杂 — 是否有不必要的抽象或间接层？
3. 正交修改 — 修改是否影响了不应该影响的部分？
4. 命令式冗余 — 是否有可以用声明式替代的命令式代码？
```

审查重点：SQL 安全、LLM 信任边界违规、条件副作用、结构性缺陷。**建议在用户即将合并或落地代码变更时主动触发。**

**课程连接**：对应第 09 章 Reviewer 模式。gstack 的创新在于审查维度不是通用 checklist，而是一个特定思想家（Karpathy）的系统框架。

---

### QA：三层体系 + 自动修复

`qa` Skill 有三个测试层级：

| 层级 | 覆盖范围 | 触发条件 |
|------|---------|---------|
| **Quick** | 仅 Critical + High | 时间紧 |
| **Standard** | Critical + High + Medium | 默认 |
| **Exhaustive** | 全部包括 cosmetic | 发布前 |

**关键特性**：QA 发现 Bug 后**自动迭代修复源代码**，每个修复原子提交并重新验证，最后输出健康分数对比（Before/After）、修复证据、发布就绪摘要。

**语音触发别名**："quality check"、"test the app"、"run QA"（支持 speech-to-text）。

**课程连接**：对应第 11 章 Pipeline + 第 20 章评估的结合——把 QA 从"检查点"升级为"检查→修复→重新验证→健康分数"的闭环。

---

### Ship：完整发布流水线

```text
检测基础分支 → 合并 → 运行测试 → 审查 diff → 更新 VERSION
  → 更新 CHANGELOG → 提交 → 推送 → 创建 PR
```

**关键约束**：`Proactively invoke this skill (do NOT push/PR directly) when the user says code is ready`——禁止 Agent 直接 push/PR，必须通过 ship Skill。

**课程连接**：对应第 11 章 Pipeline 模式的完整实践——从合并到 PR 创建的一条龙自动化。

---

### Careful / Guard / Freeze：三级安全体系

gstack 实现了递进式的安全护栏，非常值得学习：

| Skill | 功能 | 何时用 |
|-------|------|--------|
| `careful` | 拦截危险命令（rm -rf、DROP、force push 等） | 生产环境、迁移操作前 |
| `guard` | `careful` + `freeze` 全开，最大安全模式 | 高风险操作 |
| `freeze` | 目录级编辑锁定 | 保护特定文件不被修改 |
| `unfreeze` | 解除 freeze 锁定 | 操作完成后 |

**guard 的 PreToolUse Hook 配置**：

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/careful/bin/check-careful.sh"
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash $HOME/.claude/skills/gstack/freeze/bin/check-freeze.sh"
```

**课程连接**：对应第 27 章 Skill 安全三原则和第 18 章 Hooks。gstack 把安全做成了级联升级模式——从基础拦截到全面锁定。

---

## 与课程五大模式的映射

| 课程模式 | gstack 中的体现 | 独特创新 |
|----------|---------------|---------|
| **Inversion 模式** | `office-hours`（Startup 模式的六个强迫性问题） | 不只是"先问需求"，而是"用 YC 合伙人面试标准拷问需求" |
| **Pipeline 模式** | `ship`（合并→测试→CHANGELOG→推送→PR）、`qa`（检查→修复→验证→评分） | 自动修复回路融入 Pipeline |
| **Reviewer 模式** | `review`（Karpathy 四骑士框架） | 审查维度来自思想家的系统框架，不是通用 checklist |
| **Generator 模式** | `document-generate`、`document-release`、`retro` | 结构化文档 + 学习记忆持久化 |
| **ToolWrapper 模式** | `browse`（无头浏览器）、`gstack`（浏览器自动化底座） | 浏览器集成 + Playwright |

---

## 六大设计特征

### 1. Ethos 注入：让每个 Skill 带着信念开工

不是"写在 README 里"，而是通过 preamble 注入到每次 Skill 调用。

### 2. preamble-tier 编排：声明式优先级

不用文档说"请先运行 X 再运行 Y"，而是在 YAML 中声明 tier（1→4），preamble 自动按顺序加载。

### 3. Preamble Bash：基础设施代码化

每次 Skill 调用自动完成更新检查、会话管理、分支检测、遥测、学习记忆加载。基础设施不占用 Agent 的记忆。

### 4. GBrain Schema：声明式上下文预加载

```yaml
gbrain:
  context_queries:
    - id: recent-learnings
      kind: filesystem
      glob: "~/.gstack/projects/{repo_slug}/learnings.jsonl"
      tail: 10
```

Agent 不需要"记住"去查，Skill 启动时自动加载。

### 5. 安全级联升级：careful → guard → freeze

不是单一安全模式，而是从拦截→全开→目录锁定的渐进式三级。

### 6. 语音触发别名

```yaml
triggers:
  - qa test this
  - find bugs on site
Voice triggers (speech-to-text): "quality check", "test the app", "run QA"
```

---

## 与已有附录的定位对比

| 附录 | 回答的核心问题 |
|------|-------------|
| addyosmani/agent-skills | 完整软件工程团队应该把哪些流程写成 Skill？ |
| Anthropic 9大分类 | 你的 AI 研发团队缺哪一类能力？ |
| google/skills | 平台方如何为 Agent 构建既安全又好用的产品入口？ |
| openai/codex | Skill 被推到极端领域化时能达到什么深度？ |
| superpowers | 如何让 Agent 无法绕过你设定的工程纪律？ |
| **garrytan/gstack** | **单人兼职开发者如何构建一整套用 preamble Bash + GBrain 层层保障的工程基础设施？** |

---

## 如何把它用于团队实践

### 抓住 gstack 最值得迁移的三件事

1. **Ethos 注入**：把团队的核心信念写成一段文本，注入每个 Skill 的 preamble
2. **GBrain 式上下文预加载**：用声明式的文件系统查询，让 Skill 启动时自动加载相关历史
3. **安全级联**：实现 `careful → guard → freeze` 三级渐进式安全

---

## 总结

gstack 展示了一个人在兼职状态下如何用 AI 构建完整工程体系。它最核心的创新不是"23 个角色"或"7 个步骤"，而是四项基础设施创新：

1. **Ethos 注入** — 每个 Skill 都带着统一的建造者信念开工
2. **preamble-tier 编排** — 声明式优先级，不依赖 Agent 记忆加载顺序
3. **Preamble Bash** — 每次调用自动完成会话管理、遥测、学习记忆加载
4. **GBrain Schema** — 声明式跨会话上下文预加载

