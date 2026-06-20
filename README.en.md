# Hands-on Skill — A Complete Guide to Agent Skill Design, Practice &amp; Evaluation

English | [简体中文](./README.md)

> **A complete system for designing, building, evaluating, and operating Agent Skills.**
> **For**: AI engineers, product managers, and technical team leads
> **Reading time**: ~5 minutes per chapter, ~2.5 hours total
> **Language**: Simplified Chinese (this README is the English guide)

---

## Why This Guide Exists

By 2025, the file format for Agent Skills had largely converged — Claude Code, Gemini CLI, and Cursor all use the same folder layout and YAML conventions. Format is no longer the barrier.

But here's the real fork in the road: **two SKILL.md files with identical structure can produce wildly different results.** One person's Skill behaves like a throwaway script; another person's Skill runs reliably in production for months. The gap is not in the format — it's in **content design**.

I read through the raw Skill code from Anthropic, Google, OpenAI, and community open-source repositories, and noticed a recurring pattern: **great Skills aren't "a pile of instructions." They follow an implicit design language — when to load knowledge, when not to, when to ask the user, when to enforce a hard check.** That design language can be described as five universal design patterns.

This guide is the byproduct of a **"Learn by Doing"** process. I dissected each pattern, tested it in real scenarios, made mistakes, corrected them, and then wrote everything down using the Feynman technique — making tacit knowledge explicit, clear, and opinionated. It's not a translation of official docs. It's a record of what I learned, built, and broke along the way.

This is a guide that was **built**, not just compiled.

---

## Guide Philosophy: Build in the Open, Iterate Relentlessly

### Core Belief: Passive Learning Is Fake Learning

Watching tutorials and reading docs without building is "lazy learning" — you stay in input mode forever. The iron rule of this guide: **every chapter gives you something you can stop and try immediately.** You don't need all 27 chapters to write your first Skill. Two chapters are enough.

The five-part structure is a miniature personal growth loop:

```text
Curated Input → Learn Patterns → Build Things → Validate Results → Solidify Systems
```

This loop isn't theoretical. It's exactly how I learned — consume raw source material, extract patterns, write Skills, run evals, fix mistakes, and only then solidify what's reusable.

### Design Principles

**MVP-driven.** Each chapter is ~5 minutes, delivering a 60%-complete but immediately usable mental model. Ship first, iterate on feedback — same logic as building a product. Continuous output beats one perfect masterpiece.

**Get your hands dirty.** Every conclusion in this guide comes from actually opening SKILL.md files, reading them line by line, running them, modifying them, and verifying the results. Not reading someone else's summary — doing the work.

**Content as a byproduct of practice.** This isn't a "guide project." It's the natural output of building AI workflows and exploring the boundaries of Agent capabilities. Real scar tissue is more convincing than fabricated tutorials.

**Open ecosystem first.** Every reference case comes from public open-source repositories (Anthropic, Google, OpenAI Codex, Superpowers, gstack, addyosmani/agent-skills). Zero dependency on proprietary paid tools. Anyone can replicate the full learning path at zero cost.

### The Destination Is Not "Learning Skill"

Skill is just the vehicle. What you're really building is **a new kind of judgment**: the ability to convert fuzzy engineering experience into capability units that an Agent can execute reliably. This judgment doesn't come from memorizing format specs. It comes from curated input, hands-on building, Feynman-style output, and continuous iteration — accumulated day by day.

The AI era rewards **builders who actually build**. If you just want the format spec, read the Anthropic docs. If you want the design intuition to write a *good* Skill, this guide is for you.

---

## 💡 What Makes This Guide Different

1. **Real-code driven.** Every example and analysis comes from actual open-source Skill repositories.
2. **Progressive learning.** Cognition → Design → Practice → Evaluation → Operations, step by step.
3. **Problem-oriented.** Each chapter solves one real problem. 5 minutes each.
4. **Platform-agnostic.** Applies to any Agent platform, not tied to a specific product.
5. **Modular.** 27 standalone chapters. Jump anywhere.

---

## 📚 Guide Structure (27 Chapters + Prologue + Appendices)

### Prologue

- [00 — Agent Architecture Overview](./chapters/00-导言——Agent架构全景：四大组件定位.md) — How Prompt, Skill, Subagent, and MCP fit together

---

### Part 1: Cognition (Ch 01–06)

**Goal**: Build the foundational mental model for Skills

| # | Chapter (Chinese) | What It Covers |
|---|-------------------|----------------|
| 01 | Why Learn Skill? | The leap from prompt engineering to capability building |
| 02 | What Does a Skill Look Like? | File structure, naming conventions, directory layout |
| 03 | YAML Frontmatter | Why `description` is half the battle |
| 04 | Progressive Disclosure | The 3-level loading mechanism that beats traditional prompts |
| 05 | Three Degrees of Freedom | High/medium/low control strategies |
| 06 | Mental Model Shift | From writing steps to writing decision frameworks |

---

### Part 2: Design — The Five Patterns (Ch 07–11)

**Goal**: Master the five universal Skill design patterns

| # | Pattern | Chapter (Chinese) | Problem It Solves |
|---|---------|-------------------|-------------------|
| 07 | **ToolWrapper** | [ToolWrapper Pattern](./chapters/07-ToolWrapper%20模式——按需注入知识.md) | Inject domain knowledge on demand; avoid context overload |
| 08 | **Generator** | [Generator Pattern](./chapters/08-Generator%20模式——固定输出结构.md) | Template-driven output; eliminate format instability |
| 09 | **Reviewer** | [Reviewer Pattern](./chapters/09-Reviewer%20模式——分离审查与检查规则.md) | Decouple review flow from review rules; flexible quality checks |
| 10 | **Inversion** | [Inversion Pattern](./chapters/10-Inversion%20模式——先问清需求再开工.md) | Ask questions first; prevent the Agent from guessing |
| 11 | **Pipeline** | [Pipeline Pattern](./chapters/11-Pipeline%20模式——分步执行流程.md) | Gate mechanism; prevent step-skipping in multi-step workflows |

> **Pattern selection and composition guidance is included in Chapter 11.**

---

### Part 3: Practice (Ch 12–19)

**Goal**: Learn to write Skills that actually work

| # | Chapter (Chinese) | What It Covers |
|---|-------------------|----------------|
| 12 | Don't Write Known Knowledge | Supplement what the Agent *doesn't* know |
| 13 | Gotchas Are Gold | Why war stories are the highest-signal content |
| 14 | Skill Is a Folder, Not a File | References organization for precise loading |
| 15 | Constrain Goals, Not Paths | Give the Agent freedom within boundaries |
| 16 | Setup Flow and Memory | config.json, append-only logs, giving Skills memory |
| 17 | Scripts — Give the Agent Executable Code | Encapsulate stable capabilities |
| 18 | On-Demand Hooks | PreToolUse hooks for safety and monitoring |
| 19 | Full Case Study | Build a Skill from 0 to 1 |

---

### Part 4: Evaluation (Ch 20–25)

**Goal**: Build a quality assurance system for Skills

| # | Chapter (Chinese) | What It Covers |
|---|-------------------|----------------|
| 20 | Why Evaluate? | A Skill without evaluation is just a hypothesis |
| 21 | Two Types of Skills | Capability Uplift vs. Encoded Preference |
| 22 | Seven-Step Lifecycle | From draft to iterative closed loop |
| 23 | Two Types of Scorers | Deterministic checks vs. rubric-based scoring |
| 24 | Six Evaluation Metrics | Pass rate, token cost, duration, command count, retry rate, error distribution |
| 25 | A/B Testing | Version comparison, toggle comparison, model comparison |

---

### Part 5: Operations & Safety (Ch 26–27)

**Goal**: Keep Skills running reliably in teams over the long term

| # | Chapter (Chinese) | What It Covers |
|---|-------------------|----------------|
| 26 | Long-Term Maintenance | Distribution, marketplace mechanisms, metrics, dependency management |
| 27 | Three Security Principles | Permission control, input validation, dependency management |

---

### Appendices

| Appendix | Repository / Source | What You'll Learn |
|----------|-------------------|-------------------|
| 附录1 — Anthropic's 9 Skill Categories | [Anthropic Docs](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) | Team capability diagnosis map (Cognition → Production → Validation → Delivery) |
| 附录2 — OpenAI Codex Skills | [openai/codex](https://github.com/openai/codex/tree/main/.codex/skills) | Continuous PR monitoring, subagent parallel review, attention markers, failure path design |
| 附录3 — Superpowers | [obra/superpowers](https://github.com/obra/superpowers) | Red Flags table, Iron Law, Hard Gates, file handoffs, Progress Ledger |
| 附录4 — addyosmani/agent-skills | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Production-grade Skill workflow design with mandatory check gates |
| 附录5 — garrytan/gstack | [garrytan/gstack](https://github.com/garrytan/gstack) | Solo full-stack engineering system: Ethos injection, preamble-tier, Preamble Bash, GBrain schema |
| 附录6 — google/skills | [google/skills](https://github.com/google/skills) | Platform-side safe Agent entry design (35 cloud product Skills) |

---

## 🎯 Learning Paths

### Path 1: Quick Start (~1 hour)
For those who want the essentials fast.
1. Prologue → Chapter 1 → Chapter 2 → Chapter 3
2. Chapter 7 → Chapter 8 → Chapter 12

### Path 2: Full Mastery (~2.5 hours)
For those who need to systematically learn Skill construction.
1. Read all chapters in order
2. Focus deeply on Part 2 (Design) and Part 3 (Practice)
3. Build along: follow Chapter 19 to complete your own Skill

### Path 3: Problem-Driven (30 min)
Jump directly to the chapter that matches your pain point:

| Problem | Go To |
|---------|-------|
| Skill doesn't trigger | Ch 03 |
| Unstable output | Ch 08 |
| Context overload | Ch 07, Ch 14 |
| Review rules are messy | Ch 09 |
| Agent guesses blindly | Ch 10 |
| Skipped steps | Ch 11 |
| No memory | Ch 16 |
| Don't know how to evaluate | Ch 20–25 |

---

## 🔗 External References

All code repositories and resources analyzed in this guide:

- [Anthropic Agent Skills Docs](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
- [Claude Code Skills Docs](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Google ADK — Skill Design Patterns](https://github.com/google/adk-python)
- [Google Skills Repository](https://github.com/google/skills) — 35 cloud product Skills
- [OpenAI Codex Skills](https://github.com/openai/codex/tree/main/.codex/skills)
- [Superpowers](https://github.com/obra/superpowers) — Community-driven engineering discipline system
- [gstack](https://github.com/garrytan/gstack) — Garry Tan's solo full-stack engineering system
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — Production-grade Skill workflows
- [Karpathy — LLM Wiki Spec](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [AgentSkills.io](https://agentskills.io) — Skill format standards and client compatibility
- [Anthropic — The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)

---

## 📄 License

MIT License — see [LICENSE](./LICENSE).

