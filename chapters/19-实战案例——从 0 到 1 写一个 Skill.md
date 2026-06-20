
> 学习目标：整合所学，从0到1完成一个真实Skill

---


## 引言

前面 8 节，我们学习了 Skill 编写的所有核心实践：

- description 写触发条件
- 不写已知知识
- Gotchas 坑点
- 文件组织与渐进式披露
- 避免过度约束
- 设置流程与内存
- 脚本
- 按需 Hooks

今天，我们用一个完整案例把它们串起来：**从 0 到 1 写一个 commit message Skill**。

## 核心内容

### 第一步：确定需求

**目标**：帮助团队生成符合规范的 commit message。

**痛点**：
- 每次写 commit message 格式不一致
- 有人写得很简单，有人写得很长
- 没有遵循 Conventional Commits 规范

### 第二步：写 description（触发条件）

```yaml
---
name: commit-message
description: "当用户说写 commit message、生成提交信息、或查看 git diff 后需要提交时触发。用于生成符合 Conventional Commits 规范的 commit message。"
---
```

**要点**：
- 写触发条件，不是功能说明
- 包含用户会说的关键词
- 说明适用场景

### 第三步：写 SKILL.md（核心逻辑）

```markdown
# Commit Message 生成器

## 流程

1. 读取 git diff --staged
2. 分析改动类型和范围
3. 生成符合规范的 commit message

## 格式规范

<type>(<scope>): <subject>

<body>

<footer>

## 类型映射

| 改动类型 | commit type |
|---------|-------------|
| 新功能 | feat |
| 修复 bug | fix |
| 文档变更 | docs |
| 代码格式 | style |
| 重构 | refactor |
| 测试 | test |
| 构建/依赖 | chore |

## 注意事项

详见 [gotchas.md](gotchas.md)
```

**要点**：
- 只写核心逻辑，不教 Agent 已知知识
- 定义目标，不写死路径
- 详细内容拆分到附属文件

### 第四步：写 gotchas.md（坑点）

```markdown
# Gotchas

## 坑点 1：多改动混在一起

现象：一个 commit 包含多个不相关的改动
问题：难以追溯和回滚
解决：建议拆分成多个 commit

## 坑点 2：Breaking Change 未标注

现象：改动破坏了向后兼容性
问题：用户不知道需要迁移
解决：在 footer 添加 BREAKING CHANGE 说明

## 坑点 3：scope 过于宽泛

现象：scope 写成 "all" 或 "misc"
问题：无法定位改动范围
解决：scope 应该具体到模块或功能
```

**要点**：
- 写团队踩过的坑
- 包含现象、问题、解决
- 随时间持续扩充

### 第五步：文件组织

```
commit-message/
├── SKILL.md          # 核心逻辑（约 50 行）
├── gotchas.md        # 坑点记录
├── examples.md       # 示例（可选）
└── config.json       # 团队偏好配置
```

**config.json**：

```json
{
  "max_subject_length": 50,
  "require_scope": true,
  "default_scope": "core",
  "language": "zh-CN"
}
```

**examples.md**：

````markdown
# Commit Message 示例

## feat（新功能）

### 简单示例
```
feat(auth): 添加用户登录功能
```

### 完整示例
```
feat(auth): 添加用户登录功能

- 支持邮箱和手机号登录
- 添加登录失败重试机制
- 记录登录日志

Closes #123
```

## fix（修复 bug）

### 简单示例
```
fix(api): 修复用户信息查询返回空值的问题
```

### 完整示例
```
fix(api): 修复用户信息查询返回空值的问题

当用户未设置头像时，API 返回 null 导致前端报错。
现在返回默认头像 URL。

Fixes #456
```

## docs（文档变更）

```
docs(readme): 更新安装说明

补充 Node.js 版本要求和依赖安装步骤。
```

## style（代码格式）

```
style: 统一代码缩进为 2 空格

使用 prettier 格式化全部代码文件。
```

## refactor（重构）

```
refactor(utils): 重构日期格式化函数

将多个散落的日期处理逻辑统一到 formatDate 函数中，
提高代码复用性。
```

## test（测试）

```
test(auth): 添加登录功能的单元测试

覆盖正常登录、密码错误、账号不存在等场景。
测试覆盖率达到 95%。
```

## chore（构建/依赖）

```
chore(deps): 升级依赖包版本

- react: 18.0.0 → 18.2.0
- typescript: 4.8.0 → 4.9.0
- jest: 29.0.0 → 29.3.0
```

## BREAKING CHANGE（破坏性变更）

```
feat(api): 重构用户 API 接口

将 /api/user/* 接口迁移到 /api/v2/user/*，返回格式变更。

BREAKING CHANGE: 所有用户相关 API 路径已变更。
旧接口将在 v3.0.0 版本移除。

迁移指南：
- /api/user/profile → /api/v2/user/profile
- /api/user/settings → /api/v2/user/settings

参考文档：https://docs.example.com/migration/v2
```

## 常见错误示例

### 错误 1：过于简单
```
❌ 修复 bug
✅ fix(api): 修复用户信息查询返回空值的问题
```

### 错误 2：包含多个改动
```
❌ feat: 添加登录功能和修复注册 bug
✅ 建议拆分为两个 commit：
   feat(auth): 添加用户登录功能
   fix(auth): 修复注册时邮箱验证失败的问题
```

### 错误 3：scope 过于宽泛
```
❌ feat(all): 添加新功能
✅ feat(auth): 添加用户登录功能
```
````

**要点**：
- 主文件控制骨架
- 详细内容按需加载
- 配置可持久化
- 示例覆盖常见场景

### 第六步：避免过度约束

**错误写法**：

```markdown
1. 运行 git diff --staged
2. 统计改动行数
3. 判断改动类型
4. 按照模板生成
5. 输出 commit message
```

**正确写法**：

```markdown
分析改动内容，生成符合规范的 commit message。根据改动类型选择合适的 type 和 scope。

关键检查点：
- subject 不超过 50 字符
- 使用团队偏好的语言
- 包含必要的说明
```

**要点**：约束目标，不约束路径。

### 第七步：测试和迭代

**测试用例**：

1. 单个新功能 → feat
2. 多个 bug 修复 → fix（建议拆分）
3. Breaking Change → feat + BREAKING CHANGE
4. 文档更新 → docs

**迭代**：

- 发现遗漏 → 补充 gotchas
- 触发不准 → 调整 description
- 输出不稳 → 完善流程说明

## 最终文件结构

```
commit-message/
├── SKILL.md          # 核心逻辑
├── gotchas.md        # 坑点记录
├── examples.md       # 示例
└── config.json       # 团队偏好
```

**SKILL.md 完整内容**：

```yaml
---
name: commit-message
description: "当用户说写 commit message、生成提交信息、或查看 git diff 后需要提交时触发。用于生成符合 Conventional Commits 规范的 commit message。"
---

# Commit Message 生成器

## 流程

分析改动内容，生成符合规范的 commit message。根据改动类型选择合适的 type 和 scope。

## 格式规范

<type>(<scope>): <subject>

<body>

<footer>

## 关键检查点

- subject 不超过 50 字符
- 使用团队偏好的语言（见 config.json）
- Breaking Change 必须标注

## 详细说明

- 类型映射：见 [examples.md](examples.md)
- 常见坑点：见 [gotchas.md](gotchas.md)
```

## 总结

今天我们用一个完整案例串起了前面学到的所有实践：

- **description 写触发条件**（第12节）：让 Skill 能被正确触发
- **不写已知知识**（第13节）：只补充 Agent 不知道的
- **Gotchas 坑点**（第14节）：最有价值的内容
- **文件组织**（第15节）：主文件控制骨架，详细内容按需加载
- **避免过度约束**（第16节）：约束目标，不约束路径
- **设置流程与内存**（第17节）：config.json 持久化配置
- **脚本**（第18节）：封装稳定能力
- **按需 Hooks**（第19节）：临时规则，会话隔离

**核心思想**：好的 Skill 不是写一次就结束的，而是持续迭代的工作流资产。

## 下节预告

下一节，我们会学习"为什么需要评估"：从"我相信"变成"我可以证明"。

没有 Eval 的 Skill，只是一份还没被检验过的假设。


---

## 🔗 章节导航

← [上一章：18-按需 Hooks——临时规则，会话隔离](./chapters/18-按需 Hooks——临时规则，会话隔离.md) | [下一章：20-为什么需要评估——两个维护面与核心转变](./chapters/20-为什么需要评估——两个维护面与核心转变.md) →
