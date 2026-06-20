
> 学习目标：掌握按需 Hooks 的核心概念，学会用临时规则实现灵活控制

---


## 引言

你是不是也遇到过这种情况：想阻止某些危险操作，但又不想全局禁止？

比如阻止 `rm -rf`、`DROP TABLE`、强制推送这些危险命令，你不想让 Agent 一直都不能用，但在操作生产环境时又必须禁止。

**问题**：全局规则太死板，临时约束难以控制。

**解决**：按需 Hooks——临时规则，会话隔离。

---

## 📚 核心问题

**有些规则太严格，不想一直开启，但特定场景下又需要。**

常见场景：

- 生产环境操作：要阻止危险命令，但开发环境可以宽松
- 数据库迁移：要阻止删除操作，但测试环境可以删除
- 安全审计：要记录所有操作，但不希望一直记录

---

## 💡 按需 Hooks 的解决方案

**核心思想**：**技能中可以包含在调用时被激活的钩子。针对高危操作、临时约束场景配置钩子，在调用对应技能时生效。**

**特点**：

1. **按需激活**：只在调用特定 Skill 时生效
2. **会话隔离**：只在当前会话有效，会话结束后自动失效
3. **灵活控制**：不同场景用不同规则，不影响其他用户

---

## ⚠️ 重要说明：Hook 机制的适用范围

**注意**：本节介绍的 Hook 机制目前主要在 **Claude Code** 中得到完整支持和文档化。

**其他 Agent 平台的 Hook 支持情况**：

- **Claude Code**：完整支持 PreToolUse / PostToolUse / SkillTrigger 三类 Hook
- **GitHub Copilot**：尚未确认是否支持同类 Hook 机制
- **Cursor**：尚未确认是否支持同类 Hook 机制
- **Gemini CLI**：尚未确认是否支持同类 Hook 机制
- **Codex**：尚未确认是否支持同类 Hook 机制
- **其他 Agent**：请查阅具体平台的官方文档确认 Hook 支持情况

**建议**：

- 如果你使用的是 Claude Code，可以直接应用本节介绍的 Hook 机制
- 如果你使用其他 Agent 平台，请先查阅官方文档确认是否支持类似功能
- Hook 机制的设计思想（按需激活、会话隔离、灵活控制）具有普适性，即使平台不支持，也可以借鉴其理念设计其他约束机制

---

## 🔧 Hooks 的类型

Claude Code 支持多种 Hooks：

| Hook 类型 | 触发时机 | 用途 |
|----------|---------|------|
| **PreToolUse** | 执行工具前 | 检查、阻止、记录 |
| **PostToolUse** | 执行工具后 | 验证、清理、追加 |
| **SkillTrigger** | Skill 触发时 | 过滤、路由、限制 |

本节重点讲解 **PreToolUse Hook**，因为它是最常用的安全防护机制。

---

## 📌 真实案例 1：careful Skill（阻止危险命令）

来自 Thariq 的文章《Lessons from Building Claude Code》：

**场景**：需要阻止危险的 Bash 命令（`rm -rf`、`DROP TABLE`、force-push、`kubectl delete`），但不想全局禁止。

**解决方案**：创建 `careful` Skill，在调用时激活 PreToolUse hook。

**SKILL.md 配置**：

````markdown
# .claude/skills/careful/SKILL.md
---
name: careful
description: Arms strict guardrails for this session. Invoke when touching
  production systems, running migrations, or operating in restricted
  directories. Blocks rm -rf, DROP TABLE, force-push, and kubectl delete.
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: command
          command: .claude/hooks/block-destructive.sh
---

You are operating in careful mode. Every destructive command will be blocked.
Confirm with the user before proceeding with any irreversible operation.
````

**Hook 脚本（block-destructive.sh）**：

```bash
#!/bin/bash
# ~/.claude/hooks/block-destructive.sh
# 阻止危险的 Bash 命令

# 从 stdin 读取 hook payload
payload=$(cat)

# 提取 Bash 命令
command=$(jq -r '.tool_input.command // ""' <<< "$payload")

# 定义危险命令模式
dangerous_patterns=(
    "rm -rf"
    "rm -r -f"
    "DROP TABLE"
    "DROP DATABASE"
    "git push --force"
    "git push -f"
    "kubectl delete"
    "kubectl delete namespace"
    "truncate table"
)

# 检查命令是否包含危险模式
for pattern in "${dangerous_patterns[@]}"; do
    if  "$command" == *"$pattern"* ; then
        echo "❌ BLOCKED: Dangerous command detected: $pattern"
        echo "Command: $command"
        echo ""
        echo "This operation has been blocked by the 'careful' skill."
        echo "If you need to proceed, please disable careful mode or confirm with the user."
        exit 1  # 非零退出码会阻止命令执行
    fi
done

# 如果不是危险命令，允许执行
exit 0
```

**使用流程**：

1. 用户说："我要在生产环境执行迁移，请小心"
2. Agent 触发 `careful` Skill
3. PreToolUse hook 注册，监控所有 Bash 命令
4. Agent 执行命令前，hook 先检查是否危险
5. 如果危险，阻止执行并提示用户
6. 会话结束，hook 自动失效

**价值**：

- 规则按需开启，不是全局生效
- 灵活控制，不同场景用不同规则
- 会话隔离，不会影响其他用户

---

## 📌 真实案例 2：Skill 使用监控（记录使用情况）

**场景**：需要了解哪些 Skill 受欢迎，哪些触发频率过低。

**解决方案**：使用全局 PreToolUse hook，记录所有 Skill 调用。

**全局配置（settings.json）**：

```json
# ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Skill",
      "hooks": [{ "type": "command", "command": "~/.claude/hooks/log-skill.sh" }]
    }]
  }
}
```

**Hook 脚本（log-skill.sh）**：

```bash
# ~/.claude/hooks/log-skill.sh

#!/bin/bash
# stdin is the hook payload: { tool_name, tool_input: { skill, args }, session_id, ... }
# matcher already filtered to Skill, so no tool_name check needed
payload=$(cat)
skill=$(jq -r '.tool_input.skill' <<< "$payload")
args=$(jq -r '.tool_input.args // ""' <<< "$payload")

echo "$(date -u +%s)  $USER   $skill  $args" >> ~/.claude/skill-usage.tsv
```

**使用场景**：

- 发现哪些 Skill 受欢迎
- 检测触发频率过低的情况
- 优化 Skill 库，淘汰低使用率的 Skill

---

## 🔧 Hooks 的实现方式

**注册 hook 的两种方式**：

| 方式 | 配置位置 | 作用范围 | 适用场景 |
|------|---------|---------|---------|
| **SKILL.md frontmatter** | Skill 文件内 | 仅当前 Skill | 特定 Skill 的防护规则 |
| **settings.json** | 全局配置文件 | 所有 Skill/Tool | 全局监控与日志 |

**区别对比**：

| 特性 | SKILL.md 配置 | settings.json 配置 |
|------|--------------|-------------------|
| 作用范围 | 仅当前 Skill | 所有 Skill/Tool |
| 激活方式 | 调用 Skill 时自动激活 | 会话启动时就激活 |
| 适用场景 | 安全防护、临时约束 | 全局监控、审计日志 |
| 灵活性 | 高（按需激活） | 低（全局生效） |

### Hook 脚本如何编写

写 Hook 脚本时，需要理解两个关键技术细节：**payload 结构**和**返回值机制**。

**1. Payload 结构**

PreToolUse hook 会通过 stdin 发送 JSON payload：

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /data",
    "timeout": 120000
  },
  "session_id": "abc123",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Payload 字段说明**：

- **tool_name**：工具名称（Bash、Skill、Read、Write 等）
- **tool_input**：工具输入参数（具体内容取决于工具类型）
- **session_id**：当前会话ID
- **timestamp**：触发时间戳

脚本中用 `payload=$(cat)` 读取，然后用 `jq` 提取需要的字段。

**2. 返回值机制**

Hook 脚本的退出码决定后续行为：

| 退出码 | 效果 | 适用场景 |
|--------|------|---------|
| **exit 0** | 允许工具执行 | 检查通过，放行 |
| **exit 1（或其他非0值）** | 阻止工具执行 | 检查失败，拦截 |

**示例**：

```bash
# 检查逻辑
if  "$command" == *"dangerous"* ; then
    echo "Dangerous operation blocked"
    exit 1  # 阻止执行
fi

# 如果检查通过
exit 0  # 允许执行
```

---

## ✅ 脚本 vs Hooks 的区别

| 方式 | 用途 | 特点 | 适用场景 |
|------|------|------|---------|
| **脚本** | 封装稳定能力 | 永久可用，随时调用 | PDF提取、数据转换、表单填写 |
| **Hooks** | 临时规则 | 按需注册，会话隔离 | 安全防护、监控日志、临时约束 |

**何时用脚本？何时用 Hooks？**

| 问题 | 解决方案 |
|------|---------|
| "每次都要重新写同样的代码" | 用脚本封装稳定能力 |
| "有些规则不想一直开启，但特定场景需要" | 用 Hooks 按需激活 |

---

## 🎯 本节核心观点

**按需 Hooks 的三个关键**：

1. **按需激活**：只在调用特定 Skill 时生效，不全局禁止
2. **会话隔离**：只在当前会话有效，不影响其他用户
3. **灵活控制**：PreToolUse hook 可以检查、阻止、记录工具执行

**核心原则**：规则按需开启，灵活控制，会话隔离。

---

## 🔗 下节预告

下一节我们学习一个完整的实战案例：**从 0 到 1 写一个 Skill**。

把前面学到的所有实践（description、不写已知知识、Gotchas、文件组织、避免过度约束、设置流程、脚本、Hooks）整合起来，写一个真正能用的 Skill。

---

## 🔗 章节导航

← [上一章：17-脚本——给 Agent 可调用的代码](./chapters/17-脚本——给 Agent 可调用的代码.md) | [下一章：19-实战案例——从 0 到 1 写一个 Skill](./chapters/19-实战案例——从 0 到 1 写一个 Skill.md) →
