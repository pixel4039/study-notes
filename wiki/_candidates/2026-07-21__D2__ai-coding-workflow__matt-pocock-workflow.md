---
title: "AI 辅助编程工作流方法论（Matt Pocock Skills）"
type: candidate
created: 2026-07-21
tags: [wiki, ai-coding, workflow, methodology]
sources:
  - "[[sources/bilibili/19375009/transcripts/2026/2026-07-21__Matt-Pocock-AI辅助编程高效工作流全流程__BV1us5r6MEg6__P01]]"
  - https://github.com/mattpocock/skills
confidence: medium
status: candidate
author: hermes
d_level: D2
original_date: 2026-05-16
---

# 候选：AI 辅助编程工作流方法论（Matt Pocock Skills）

> 原始条目日期：2026-05-16（视频发布日）
> 来源回链：[[sources/bilibili/19375009/transcripts/2026/2026-07-21__Matt-Pocock-AI辅助编程高效工作流全流程__BV1us5r6MEg6__P01]]
> D 级判定：D2（细化）— wiki 目前「计算机/AI」分支为空，此为本分支首个候选；内容不是全新概念（D1），而是对"AI 编程工程化"这个已有方向的系统性方法论细化。

## 候选摘要

Matt Pocock（TypeScript 社区知名教育者，Total TypeScript 作者）将工程师传统纪律编码为 ~50 行可组合 Markdown Skill，形成一套不接管流程但固化工程基本功的 AI 编程工作流。核心主张：

1. **对齐先于实现**：/grill-with-docs 在写代码前让 Agent 拷问你，把模糊需求变成明确规格，副作用是沉淀 CONTEXT.md（领域语言）和 ADR
2. **垂直切片 TDD**：反对水平切片（先写全部测试再全部实现），要求 test1→impl1→test2→impl2 的 tracer bullet 节奏
3. **2 秒反馈环**：diagnose 6 阶段调试法的核心是"先建一个 2 秒内出 pass/fail 的信号"
4. **周期性架构精修**：AI 让代码写得快 5 倍也烂得快 5 倍，/improve-codebase-architecture 每周跑一次
5. **composable 不 lock-in**：纯 Markdown，任何 LLM/编辑器/工程师都能用，21 个文件零运行时

## 拟挂载位置

wiki/index.md → 计算机/AI → AI 编程工程化

## 拟生成页面

- wiki/methods/ai-coding-workflow-matt-pocock.md（方法论页）

## 待审批问题

- [ ] D0：wiki 目前无同名/近似页 → 不重复
- [ ] D1：是否构成新证据？→ 不是新发现，是已有方向的系统方法论
- [ ] D2：细化程度是否足够？→ 有完整 7 阶段流程 + 具体命令 + 框架对比
- [ ] D3：是否有闪光点/用户原创洞察？→ 暂无用户批注，等主人阅读后补充
- [ ] D4：案例/反例？→ 有 5 个框架横向对比
- [ ] D5：与现有知识冲突？→ 无

## 下一步

等主人阅读转录稿后确认/批注，再正式生成 wiki/methods/ 页面并挂载到 index.md。
