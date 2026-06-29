# Hands-on Skill — A Complete Guide to Agent Skill Design, Practice & Evaluation

[English](README.en.md) | [简体中文](output/skill/README.md)

> **Overview**: Master the complete Agent Skill system from 0 to 1 — Cognition, Design, Practice, Evaluation, Operations & Safety
>
> **Audience**: AI engineers, product managers, technical team leads
>
> **Reading time**: ~5 minutes per chapter, ~2.5 hours total
>
> **Core value**: Learn to build stable, reliable Agent capabilities that turn AI into a real productivity tool

---

## Why This Guide Exists

This guide is itself a byproduct of "Learn by Doing."

By 2025, the file format for Agent Skills had largely converged. But after reading through the Skill code from Anthropic, Google, OpenAI, and community open-source repositories, I noticed a recurring phenomenon: **great Skills aren't "a pile of instructions stuffed together." They follow an implicit design language — when to load knowledge, when not to, when to ask the user, when to enforce a hard check.**

Format docs are easy to read, but no one teaches design intuition. My input principle is simple: **follow builders, not influencers** (from 张咋啦). The authors of the dozen-plus reference codebases — Garry Tan, Addy Osmani, Karpathy, the OpenAI Codex team, the Google Cloud team — are all builders who ship products and implement tools hands-on.

Reading is not the end. I dissected each design pattern, tested it in my own scenarios, made mistakes, corrected them, and then **wrote it all down using the Feynman technique**: making all tacit knowledge explicit, clear, and thorough. This is not a translation of official documentation. This is a complete record of "what I learned, what I built, and what I broke along the way."

That's how this guide came to be. It's something **built**, not something compiled.

---

## Guide Philosophy: Build Hands-On, Build in the Open, Iterate Continuously

### Core Belief: Passive Learning Is Fake Learning

Mindlessly watching tutorials and reading docs is "lazy learning" — you stay in input mode forever and never truly master anything. The iron rule of this guide: **every chapter gives you something you can stop and try immediately.** You don't need all 27 chapters to write your first Skill. Two chapters are enough.

The five-part structure is essentially a miniature personal growth loop:

```text
Curated Input (Cognition) → Learn Patterns (Design) → Build Hands-On (Practice) → Validate Results (Evaluation) → Solidify Systems (Operations & Safety)
```

This loop isn't derived from theory. It's exactly how I learned Skill — consume raw source material, extract patterns, build things, run evals, make mistakes and fix them, and only then solidify what's reusable into a system.

### Design Principles

**MVP-driven, don't chase perfection.** Each chapter is ~5 minutes, delivering a 60%-complete but immediately usable mental model. Ship first, iterate on feedback — same logic as building a product. Consistent output beats one perfect masterpiece.

**Get your hands dirty, go deep.** Every conclusion in this guide comes from thoroughly dissecting real Skill codebases — not reading someone else's review, but opening SKILL.md files line by line, reading them, running them, modifying them, and verifying the results myself.

**Content as a byproduct of practice.** This guide isn't a dedicated "write a tutorial" project — it's the natural output of building AI workflows and exploring the boundaries of Agent capabilities. Real scar tissue from real mistakes is far more convincing than fabricated tutorials.

**Open ecosystem first.** All reference cases come from public open-source repositories. No dependency on proprietary paid tools. Anyone can replicate the full learning path at zero cost.

### The Destination Is Not "Learning Skill"

Skill is just the vehicle. What you're really building is **a new kind of judgment**: the ability to convert fuzzy engineering experience into capability units that an Agent can execute reliably. This judgment doesn't come from memorizing format specs. It comes from curated input, hands-on building, Feynman-style output, and continuous iteration — accumulated day by day.

The AI era rewards **builders who actually build**. If you just want to know the format, read the Anthropic docs. If you want the design intuition and judgment to write a *good* Skill, this guide is for you.

---

## 💡 What Makes This Guide Different

1. **Real-case driven**: All examples and analysis come from open-source Skill codebases
2. **Progressive learning**: Cognition → Design → Practice → Evaluation → Operations, step by step
3. **Problem-oriented**: Each chapter solves one real problem, readable in ~5 minutes
4. **Platform-agnostic**: Applies to any Agent platform, not tied to a specific product
5. **Clearly structured**: 27 standalone chapters, jump anywhere

---

## 📚 Guide Structure (27 Chapters + Prologue + Appendices)

### Prologue

- [00 — Agent Architecture Overview](00-导言——Agent架构全景：四大组件定位.md) — How Prompt, Skill, Subagent, and MCP fit together

---

### Part 1: Cognition

**Goal**: Build the foundational mental model for Skills

- [01 — Why Learn Skill?](01-为什么要学%20Skill？——%20通用智能体的最后一公里.md) — The value and necessity of Skills; the leap from prompts to capabilities
- [02 — What Does a Skill Look Like?](02-Skill%20长什么样？——%20文件结构与核心规范.md) — File structure, naming conventions, directory organization
- [03 — The Essence of YAML Frontmatter](03-YAML%20Frontmatter%20的精髓——写好%20description%20是成功的一半.md) — The core role of the `description` field and how to write it well
- [04 — Progressive Disclosure](04-渐进式披露——Skill%20碾压传统%20Prompt%20的核心设计原理.md) — The 3-level loading mechanism that breaks through context limits
- [05 — Three Degrees of Freedom](05-三档自由度——如何把控指令的粗细粒度.md) — High / medium / low control strategies
- [06 — Mental Model Shift](06-心智模型跃迁——从写步骤到写决策框架.md) — From "writing prompts" to "building capabilities"

---

### Part 2: Design — The Five Design Patterns

**Goal**: Master the core Skill design patterns and solve common problems

- [07 — ToolWrapper Pattern](07-ToolWrapper%20模式——按需注入知识.md) — Load domain knowledge on demand; avoid context overload
- [08 — Generator Pattern](08-Generator%20模式——固定输出结构.md) — Template-driven output; solve format instability
- [09 — Reviewer Pattern](09-Reviewer%20模式——分离审查与检查规则.md) — Decouple review flow from review rules; flexible replacement
- [10 — Inversion Pattern](10-Inversion%20模式——先问清需求再开工.md) — Ask questions first; prevent the Agent from guessing blindly
- [11 — Pipeline Pattern](11-Pipeline%20模式——分步执行流程.md) — Gate mechanism; prevent step-skipping

---

### Part 3: Practice

**Goal**: Learn to write Skills that are genuinely useful

- [12 — Don't Write Known Knowledge](12-不写已知知识——Agent%20已经很聪明.md) — Supplement what the Agent doesn't know, not what it already knows
- [13 — Gotchas Are Gold](13-Gotchas%20坑点——最有价值的内容是踩过的坑.md) — The value of war stories; what makes a Skill truly useful
- [14 — File Organization & Progressive Disclosure](14-文件组织与渐进式披露——Skill%20是文件夹不是文件.md) — References organization strategy for precise loading
- [15 — Avoid Over-Constraining](15-避免过度约束——约束目标，不约束路径.md) — Give the Agent enough freedom; constrain goals, not paths
- [16 — Setup Flow & Memory](16-设置流程与内存——让%20Skill%20有记忆.md) — config.json and append-only logs; giving Skills memory
- [17 — Scripts — Give the Agent Executable Code](17-脚本——给%20Agent%20可调用的代码.md) — Encapsulate stable capabilities; avoid reinventing the wheel
- [18 — On-Demand Hooks](18-按需%20Hooks——临时规则，会话隔离.md) — PreToolUse hooks for safety and monitoring
- [19 — Full Case Study](19-实战案例——从%200%20到%201%20写一个%20Skill.md) — Build a Skill from 0 to 1, integrating everything learned

---

### Part 4: Evaluation

**Goal**: Build a quality assurance system for Skills

- [20 — Why Evaluate?](20-为什么需要评估——两个维护面与核心转变.md) — A Skill without evaluation is just a hypothesis
- [21 — Two Types of Skills](21-两类%20Skill%20分类——补能力还是固化偏好？.md) — Capability Uplift vs. Encoded Preference
- [22 — Seven-Step Lifecycle](22-七步生命周期——从草稿到迭代闭环.md) — From draft to iterative closed loop
- [23 — Two Types of Scorers](23-两类评分器——确定性检查与评分细则检查.md) — Deterministic checks vs. rubric-based scoring
- [24 — Six Evaluation Metrics](24-六类评估指标——量化Skill表现.md) — Pass rate, token cost, duration, command count, retry rate, error distribution
- [25 — A/B Testing](25-A-B对比测试——持续验证与优化.md) — Version comparison, toggle comparison, model comparison

---

### Part 5: Operations & Safety

**Goal**: Keep Skills running reliably in teams over the long term

- [26 — Long-Term Maintenance & Team Management](26-Skill%20的长期维护与团队管理.md) — Distribution strategies, marketplace mechanisms, metrics, dependency management
- [27 — Three Security Principles](27-Skill%20安全三原则——强大能力的风险管理.md) — Permission control, input validation, dependency management

---

### Appendices

- [Appendix 1 — Anthropic's 9 Skill Categories](附录1-Anthropic%20的%209%20大%20Skill%20分类——团队能力诊断地图.md) — Anthropic's official Skill type classification system (Cognition → Production → Verification → Delivery)
- [Appendix 2 — OpenAI's Skill Practice Cases](附录2-OpenAI的Skill实践案例——代码助手能力构建.md) — OpenAI Codex's real Skill library (continuous monitoring + Subagent parallel review + attention markers + failure path design)
- [Appendix 3 — Superpowers Open-Source Skill Library](附录3-Superpowers开源Skill库——社区驱动的能力复用.md) — Community-driven engineering discipline system (Red Flags table + Iron Law + Hard Gates + file handoffs + Progress Ledger)
- [Appendix 4 — addyosmani/agent-skills](附录4-addyosmani-agent-skills——生产级Skill工作流设计.md) — Google Engineering Director Addy Osmani's production-grade Skill workflow library
- [Appendix 5 — garrytan/gstack](附录5-garrytan-gstack——创业者导向的完整产品研发流程.md) — YC President Garry Tan's solo full-stack engineering system (four pillars: Ethos injection + preamble-tier orchestration + Preamble Bash + GBrain Schema cross-session memory)
- [Appendix 6 — google/skills](附录6-google-skills——平台化产品的安全Agent入口设计.md) — Google's official Skill library, 35 cloud product Skills (safety guardrails + data minimization + mandatory pre-flight verification + progressive loading)

---

## 🎯 Learning Paths

### Path 1: Quick Start (~1 hour)

For readers who want to quickly grasp the basic concepts.

1. Prologue → Chapter 1 → Chapter 2 → Chapter 3
2. Chapter 7 → Chapter 8 → Chapter 12

### Path 2: Full Mastery (~2.5 hours)

For readers who need to systematically learn Skill construction.

1. Read all chapters in order
2. Focus deeply on Part 2 (Design) and Part 3 (Practice)
3. Practice: follow Chapter 19 to complete a full Skill

### Path 3: Problem-Driven (30 min)

For readers facing specific problems who need targeted solutions.

| Problem | Go To |
|---------|-------|
| Skill doesn't trigger | Chapter 3 |
| Unstable output | Chapter 8 |
| Context overload | Chapter 7, Chapter 14 |
| Messy review rules | Chapter 9 |
| Agent guesses blindly | Chapter 10 |
| Skipped steps | Chapter 11 |
| No memory | Chapter 16 |
| Don't know how to evaluate | Chapter 20–25 |

---

## 🔗 External References

All code repositories and resources analyzed in this guide:

- [Anthropic Agent Skills Docs](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
- [Claude Code Skills Docs](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Google ADK — Skill Design Patterns](https://github.com/google/adk-python)
- [Google Skills Repository](https://github.com/google/skills) — 35 cloud product Skills
- [OpenAI Codex Skills](https://github.com/openai/codex/tree/main/.codex/skills) — Codex Skill practices
- [Superpowers](https://github.com/obra/superpowers) — Community-driven engineering discipline system
- [gstack](https://github.com/garrytan/gstack) — Garry Tan's solo full-stack engineering system
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — Production-grade Skill workflow design
- [Karpathy — LLM Wiki Spec](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [AgentSkills.io](https://agentskills.io) — Skill format standards and client compatibility
- [Anthropic — The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)

---

## 📄 License

MIT License — see [LICENSE](./LICENSE).
