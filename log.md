# study-notes 日志

## [2026-07-16] scaffold | 仓库骨架落地(Claude)
- 按已批 schema 总装(resources/decisions/2026-07-15__proposal__study-notes-schema-assembly.md)建立 sources/annotations/wiki/legacy 目录树与 SCHEMA/AGENTS/_index/log;既有三个课程目录标记为 legacy bundle 原样保留。
- 对账结论:本仓库为 PDF 保管方;35 个笔记文件落后于 resources/study 的 2026-07-14 版;内容合并与 resources/study 退役属后续单独批准的迁移计划。

## [2026-07-16] ingest | B站 BV1syNg6DEFi P01 入库(Codex)
- 本地待验收、未提交；平台 AI 字幕 192 条按时间线确定性排版，未纠错、未总结。
- 原始字幕 `P01.json` SHA256：`955820a57b9b0da6a16ac0c872259cbfad902467ac8e34b1f36f0d5e41299330`。
- 原始视频 metadata `BV1syNg6DEFi.json` SHA256：`b545bf23863602ab21425ff7e8d74ee7d9a323731f39f265def0f72651fb5c2a`。

## [2026-07-16] derived-readable | B站 BV1syNg6DEFi P01 连续阅读版(Codex)
- 从平台 AI 字幕派生连续阅读视图：保留 192 条字幕全部原词及顺序，仅移除逐句时间戳/block ID，并添加标点与自然分段；阅读状态仍以带时间戳的 canonical P01 为唯一真源。

## [2026-07-16] capture | P01 阅读完成与首条留言(Codex)
- 主人明确表示已读完 P01；canonical 与视频索引的 `started`/`finished` 更新为 `true`。
- 新建 `annotations/bilibili/395922059/BV1syNg6DEFi.md`，将对话中重复两次的同一段留言按一次逐字保存，暂标 `tentative: true` 待主人核对；Codex 补充使用独立 `[!ai-note]`，未混入用户原话。
- 连续阅读稿末尾与视频索引新增“留言栏”入口。完成状态已触发 D0–D5 重判，但在用户核对转写前不生成或晋升 Wiki candidate。

## [2026-07-16] confirm/review | P01 留言确认与 D0–D5 重判(Codex)
- 主人明确回复“确认这条留言”；annotation 条目转为 `tentative: false`，记录确认者和日期。
- 重判结果：文件入口减少搜索时间属 D0 来源已有；“任务上下文四要素 + Skill 外置流程”可作为单个 D2 细化候选；token 节省因视频未测 token，保持为用户判断/待验证假设。当前不创建 candidate，留待主人和 Claude 讨论，避免新 Wiki 过早碎片化。

## [2026-07-16] feat | Obsidian 阅读通道 A 落地(Sonnet 代笔 / Claude 合同)
- 按 Claude 拟定的阅读通道 A 合同,建立 `.obsidian/`(app.json、appearance.json、snippets/reading.css)最小 vault 配置、`.gitignore` 追加 Obsidian 本地易变项、根目录 `阅读指南.md`。
- reading.css 约 70 行:行距/段距/标题留白/引用块/表格样式全部使用 Obsidian 主题变量,不硬编码颜色,亮暗两态均适配;未安装或配置任何社区插件。
- 本次提交未 push;工作树中 P01 摄入相关的既有未提交改动(`sources/bilibili/**`、`annotations/**`、`_index.md`、`log.md` 的既有修改)使用隔离提交手法保持原样,未被本次提交吸收。
