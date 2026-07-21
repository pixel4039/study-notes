---
title: Matt Pocock 演示：AI 辅助编程的高效工作流全流程
type: transcript
created: 2026-07-21
updated: 2026-07-21
tags: [bilibili, ai-coding, workflow, claude-code, skills]
sources:
  - https://www.bilibili.com/video/BV1us5r6MEg6
  - https://www.youtube.com/watch?v=-QFHIoCo-Ko
related:
  - "[[wiki/_candidates/2026-07-21__D2__ai-coding-workflow__matt-pocock-workflow]]"
confidence: high
status: active
author: hermes
---

# BV1us5r6MEg6 — Matt Pocock 演示：AI 辅助编程的高效工作流全流程

> UP主：Gelai_AI (MID: 19375009)
> 合集：AI 工具实战 (4/40)
> 发布：2026-05-16 | 播放：1.8万 | 时长：01:36:30
> 原始演讲：Matt Pocock 在 AI Engineer 大会 Full Walkthrough（YouTube 113万+播放）
> Skills 仓库：github.com/mattpocock/skills（49.8K Star）

> [!ai-note]
> 本转录稿由 Hermes 基于视频页面信息、掘金深度拆解文章、YouTube 原始演讲时间线和 Skills v1.1 更新视频综合整理。非逐字字幕转录，而是结构化内容还原。原始 B站字幕未获取（API 被拒）。

## 一、核心论点

AI 编程的失败不是因为模型不够强，而是**工程反馈链失效**。Matt Pocock 的解法不是做一个更大的框架，而是把工程师几十年来踩过坑的小动作，每个做成 ~50 行可组合的 Skill（Markdown 提示词）。

> "Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the process hard to resolve."

设计哲学：不接管流程，给你工程基本功。

## 二、完整工作流 7 个阶段

（来源：AI Engineer 大会演讲时间线）

### Phase 1: Research & Prototyping（研究与原型）[00:04:20]
- 用 /research 和 /prototype 探索技术方案
- 先搞清楚"能不能做、怎么做"，再进入正式开发

### Phase 2: Grill Session（需求拷问）[00:12:45]
- 用 /grill-me 或 /grill-with-docs 让 Agent 反过来"拷问"你
- 目的：在写代码前对齐需求，把模糊想法变成明确规格
- /grill-with-docs 会顺手更新 CONTEXT.md（领域语言文档）和 ADR（架构决策记录）
- **每次开始新需求前都先跑一遍**

### Phase 3: Writing the PRD（写产品需求文档）[00:22:10]
- 用 /to-prd（v1.1 中更名为 /to-spec）把对话凝练成结构化 PRD
- 在生成 PRD 前先盘问影响哪些模块
- PRD 提交为 issue

### Phase 4: Slicing Work into Issues（切分工作）[00:35:50]
- 用 /to-issues（v1.1 中更名为 /to-tickets）把 PRD 拆成"垂直切片"GitHub Issue
- 垂直切片原则：每个 issue 是**端到端可独立验收**的最小用户可感知改动
  - ✅ "在登录页加 Github OAuth 按钮"
  - ❌ "加一个 OAuth utils 文件"
- 切片之间可以并行执行

### Phase 5: Implementation with AI Agents（AI 实现）[00:48:15]
- 用 /tdd 执行 red-green-refactor 循环
- 用 /diagnose 处理难 bug（6 阶段调试法）
- 用 /zoom-out 进入陌生模块时让 Agent 站在全局视角
- 从 human-in-the-loop 逐步过渡到全自主（AFK）运行

### Phase 6: Human-in-the-Loop Review（人工审查）[01:05:30]
- Agent 完成实现后，人工 review
- 根据 Agent 表现调整 prompt
- 逐步提升信任度

### Phase 7: Deployment & Monitoring（部署与监控）[01:18:45]
- 生产部署 + 监控反馈
- 周期性用 /improve-codebase-architecture 精修架构

## 三、Skills v1.1 更新要点（2026-07-08）

来源：Matt Pocock YouTube "New Skills! v1.1 brings /wayfinder, /research, /implement, /to-spec, /to-tickets"

| 变更 | 说明 |
|---|---|
| /to-prd → /to-spec | 更名，从 PRD 泛化为 spec |
| /to-issues → /to-tickets | 更名，更通用 |
| /grill 改进 | 拷问技能优化 |
| 完整开发生命周期流 | spec → tickets → implement 串联 |
| /wayfinder（新） | 大型项目规划，比单 issue 更宏观的路线图 |
| /research（新） | 支撑技能，实现前先研究 |
| /implement（新） | 实现阶段专用 skill |
| /code-review 改进 | 新增 refactoring smells 检测 |
| TDD 更新 | 配合新流程调整 |

更新命令：`npx skills add mattpocock/skills`

## 四、核心 Skill 速查

### Engineering（日常开发主力）

| Skill | 定位 | 何时用 |
|---|---|---|
| grill-with-docs | 拷问需求 + 更新 CONTEXT.md/ADR | 每次新需求前 |
| tdd | 强制 red-green-refactor，垂直切片 | 写新功能/修 bug |
| diagnose | 6 阶段调试（reproduce→minimise→hypothesise→instrument→fix→regression-test） | 难复现 bug |
| to-spec | 对话 → 结构化 spec | 拷问完成后 |
| to-tickets | spec → 垂直切片 issue | 准备并行执行 |
| triage | Issue 状态机分类 | 接手新 backlog |
| improve-codebase-architecture | 架构精修，找"加深模块"机会 | 每周/每隔几天 |
| zoom-out | 站在系统层面解释代码 | 进入陌生模块 |
| wayfinder | 大型项目规划 | 新项目/大重构 |
| research | 实现前技术调研 | 不确定方案时 |
| implement | 实现阶段 | 有明确 ticket 时 |
| setup-matt-pocock-skills | 一次性初始化配置 | 装完第一次跑 |

### Productivity（通用工具）

| Skill | 定位 |
|---|---|
| caveman | 极简通信，token 省 ~75% |
| grill-me | 非代码场景的需求拷问 |
| write-a-skill | 按规范写新 skill |

### Misc（偶尔用）

| Skill | 定位 |
|---|---|
| git-guardrails-claude-code | 拦截 force push / reset --hard / clean -fd |
| setup-pre-commit | Husky + lint-staged + Prettier + tsc + test |

## 五、四个核心痛点与解法

| 痛点 | 解法 | 对应 Skill |
|---|---|---|
| Agent 没听懂（Misalignment） | 写代码前先让 Agent 拷问你 | grill-me / grill-with-docs |
| Agent 太啰嗦（Verbosity） | 建立共享领域语言 CONTEXT.md | grill-with-docs（副作用：自动沉淀术语） |
| 代码不 work（Quality） | 建立反馈环：TDD + 诊断 | tdd / diagnose |
| 项目变大泥球（Architecture Decay） | 周期性架构精修 | improve-codebase-architecture / zoom-out |

## 六、TDD 的关键区别

Matt 强调**垂直切片 TDD**，反对水平切片：

```
❌ 水平切片（Anti-pattern）:
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

✅ 垂直切片（Tracer Bullet）:
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

原因：水平切片让你对着想象中的行为写测试，测试只测"形状"，真正行为变了不报警。

规则：只测公共接口的行为，不要 mock 内部协作者。如果重命名一个内部函数测试就挂，那测试本身就是错的。

## 七、Diagnose 6 阶段调试法

1. **Build Feedback Loop**（最重要！）—— 先有一个 2 秒内能跑完的确定性 pass/fail 信号
2. Reproduce —— 稳定复现（复现率低于 50% 先提复现率）
3. Minimise —— 最小化复现条件
4. Hypothesise —— 提出假设
5. Instrument —— 插桩验证
6. Fix + Regression Test —— 修复并加回归测试

> "If you have a feedback loop, you will find the cause — bisection, hypothesis-testing, and instrumentation all just consume that signal."

## 八、安装与标准打法

### 安装

```bash
npx skills@latest add mattpocock/skills
```

推荐至少勾选：setup-matt-pocock-skills、grill-with-docs、tdd、diagnose、to-spec、to-tickets、improve-codebase-architecture

### 初始化

```
/setup-matt-pocock-skills
```

会问三件事：Issue tracker 用什么 / triage 标签 / 领域文档路径

### 标准工作流

```
1. /grill-with-docs   ← 拷问需求，沉淀领域语言到 CONTEXT.md
2. /to-spec           ← 对话凝结成 spec
3. /to-tickets        ← 拆成垂直切片 issue
4. 选一个 ticket：
   /tdd              ← red-green-refactor 实现
   /diagnose         ← 遇到难 bug 切到这个
   /zoom-out         ← 走进陌生模块时
5. 每周跑一次：
   /improve-codebase-architecture  ← 架构精修
```

## 九、框架横向对比

| 维度 | mattpocock/skills | GSD | BMAD | Superpowers | Spec-Kit |
|---|---|---|---|---|---|
| 核心理念 | 不接管流程，给工程基本功 | 接管 context window | 接管 SDLC，模拟敏捷团队 | 接管 TDD 纪律 | 接管 spec→impl 转换 |
| 抽象单位 | Skill（.md 提示词） | Phase + Slash command | Agent 角色 | 单 orchestrator + 子 agent | Spec 文档 |
| 可定制度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 学习成本 | 低 | 中 | 高 | 中 | 中 |
| 适用场景 | 日常工程，保留控制权 | 跨天多文件长任务 | 敏捷流程产品/团队 | 强 TDD 信仰 | 需求驱动型企业 |

一句话总结：
- **mattpocock/skills** = 瑞士军刀，每把刀都锋利，你自己选
- **GSD** = 全自动流水线，长任务零 context rot，杀小项目
- **BMAD** = 虚拟敏捷团队，流程重，新手被淹没
- **Superpowers** = TDD 警长，纪律最强，超长 session context 会爆
- **Spec-Kit** = 规格驱动，适合强需求评审文化

## 十、实用套路

1. **grill-with-docs 是省钱第一神器**：坚持几周，CONTEXT.md 成为行话词典，所有 session 启动 token 省 30%-50%
2. **to-tickets 学会垂直切片**：每个 issue 端到端可独立验收，按行为拆不按文件拆
3. **调试先建 2 秒反馈环**：没有就先建，再查 bug
4. **每周修剪一次**：improve-codebase-architecture 周期性使用，坚持一个季度项目不变泥球
5. **caveman + git-guardrails 长期开着**：省 token + 防删库，装上忘掉

## 十一、设计决策解读

1. **为什么用 Markdown 不用 DSL？** 任何 LLM 都能读，任何编辑器都能改，任何工程师都能贡献。零 lock-in。
2. **为什么强调 composable？** 每个 skill ~50 行，假设其他 skill 存在。不强迫跑全套，配合起来就是完整工作流。
3. **为什么 ADR 在第一线？** 只在决策"难以反转、缺少上下文会让人困惑、有真实 trade-off"时才写。
4. **caveman 的存在**：说明 Matt 真的在乎 token 成本，工程实用主义写在 DNA 里。

## 十二、金句

- "AI 不是来替你做工程师的，是来放大你工程能力的。但前提是——你得真的有工程能力。"
- "先别急着 vibe coding，把工程基本功捡回来。"
- "No-one knows exactly what they want." — The Pragmatic Programmer
- "Always take small, deliberate steps. The rate of feedback is your speed limit." — The Pragmatic Programmer
- "Invest in the design of the system every day." — Extreme Programming Explained

## 参考链接

- B站视频：https://www.bilibili.com/video/BV1us5r6MEg6
- 原始演讲（AI Engineer）：https://www.youtube.com/watch?v=-QFHIoCo-Ko
- Skills v1.1 更新视频：https://www.youtube.com/watch?v=A8mokin_YOs
- Skills 仓库：https://github.com/mattpocock/skills
- Matt Pocock Newsletter：https://aihero.dev/skills/subscribe
- Matt Twitter：https://twitter.com/mattpocockuk
- 掘金深度拆解：https://juejin.cn/post/7634508738561409059
