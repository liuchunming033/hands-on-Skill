
> 学习目标：让Skill记住用户配置，从无状态变成有记忆

---


## 引言

你有没有遇到过这种情况：每次调用 Skill，Agent 都要从头开始？

比如站会报告 Skill，每次都要重新问"发布到哪个频道"。或者故障排查 Skill，每次都要重新问"日志在哪里"。

**问题**：Skill 每次运行都是全新的，不记得上次做了什么。

**解决**：让 Skill 有记忆。

## 核心内容

### 无状态 vs 有记忆

| 类型 | 特点 | 体验 |
|------|------|------|
| 无状态 | 每次都是全新开始 | 每次都要重新配置 |
| 有记忆 | 记住上次的选择 | 只配置一次，后续直接用 |

### 用 config.json 存储配置

**场景**：有些 Skill 需要用户配置（如站会要发布到哪个 Slack 频道）。

**解决方案**：

````markdown
## 配置流程

首次运行时，询问用户：
- 发布到哪个频道？
- 包含哪些项目？
- 报告格式偏好？

将配置保存到 config.json：
```json
{
  "channel": "#daily-standup",
  "projects": ["frontend", "backend"],
  "format": "markdown"
}
```

后续运行时，直接读取 config.json，不再询问。
````

**价值**：让 Skill 从无状态工具变成有记忆的助手。

#### 真实案例：follow-builders Skill 配置

来自知识库中的实际 SKILL.md，完整的配置结构：

**首次运行检测**：

````markdown
## First Run — Onboarding

Check if `~/.follow-builders/config.json` exists and has `onboardingComplete: true`.
If NOT, run the onboarding flow...
````

**config.json 完整结构**：

```json
{
  "platform": "openclaw",
  "language": "zh",
  "timezone": "Asia/Shanghai",
  "frequency": "daily",
  "deliveryTime": "08:00",
  "weeklyDay": "Monday",
  "delivery": {
    "method": "telegram",
    "chatId": "123456789",
    "email": "user@example.com"
  },
  "onboardingComplete": true
}
```

**配置创建脚本**：

```bash
cat > ~/.follow-builders/config.json << 'CFGEOF'
{
  "platform": "<openclaw or other>",
  "language": "<en, zh, or bilingual>",
  "timezone": "<IANA timezone>",
  "frequency": "<daily or weekly>",
  "deliveryTime": "<HH:MM>",
  "weeklyDay": "<day of week, only if weekly>",
  "delivery": {
    "method": "<stdout, telegram, or email>",
    "chatId": "<telegram chat ID, only if telegram>",
    "email": "<email address, only if email>"
  },
  "onboardingComplete": true
}
CFGEOF
```

**运行时读取配置**：

````markdown
## Content Delivery — Digest Run

### Step 1: Load Config

Read `~/.follow-builders/config.json` for user preferences.
````

### 用日志追加记录历史

**场景**：故障排查 Skill，需要知道"上次排查到哪一步"。

**解决方案**：

````markdown
## 日志记录

每次运行后，追加一条记录到 log.json：
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "action": "排查数据库超时",
  "status": "进行中",
  "note": "发现连接池配置问题"
}
```

下次运行时，读取日志，只报告新的变化。
````

**价值**：Skill 不再是无状态的脚本，而是有记忆的助手。

### 设置流程的最佳实践

**首次运行**：

1. 检查是否存在 config.json
2. 如果不存在，询问用户
3. 保存配置到 config.json
4. 继续执行任务

**后续运行**：

1. 读取 config.json
2. 使用已保存的配置
3. 如果用户想修改，提供修改入口

### 日志记录的最佳实践

**追加而非覆盖**：

- 每次运行追加一条新记录
- 保留历史，可以追溯
- 不覆盖之前的记录

**结构化格式**：

```json
[
  {"timestamp": "...", "action": "...", "status": "..."},
  {"timestamp": "...", "action": "...", "status": "..."},
  {"timestamp": "...", "action": "...", "status": "..."}
]
```

### 配置文件的位置

**推荐结构**：

```
my-skill/
├── SKILL.md
├── config.json    # 用户配置
└── log.json       # 运行日志
```

或者放在 Skill 外的固定位置：

```
~/.skill-data/
├── standup-report/
│   ├── config.json
│   └── log.json
└── pr-monitor/
│   ├── config.json
│   └── log.json
```

## 总结

今天我们学习了设置流程与内存：

1. **用 config.json 存储配置**：只配置一次，后续直接使用
2. **用日志追加记录历史**：每次运行追加一条，保留历史追溯
3. **让 Skill 有记忆**：从无状态工具变成有记忆的助手

**核心原则**：用户只配置一次，Skill 自己记住历史。

## 下节预告

下一节，我们会学习"脚本"：给 Agent 可调用的代码。

把稳定能力封成脚本和辅助函数，让 Agent 负责组合，而不是重造轮子。


---

## 🔗 章节导航

← [上一章：15-避免过度约束——约束目标，不约束路径](./15-避免过度约束——约束目标，不约束路径.md) | [下一章：17-脚本——给 Agent 可调用的代码](./17-脚本——给 Agent 可调用的代码.md) →
