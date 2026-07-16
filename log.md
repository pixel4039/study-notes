# study-notes 日志

## [2026-07-16] scaffold | 仓库骨架落地(Claude)
- 按已批 schema 总装(resources/decisions/2026-07-15__proposal__study-notes-schema-assembly.md)建立 sources/annotations/wiki/legacy 目录树与 SCHEMA/AGENTS/_index/log;既有三个课程目录标记为 legacy bundle 原样保留。
- 对账结论:本仓库为 PDF 保管方;35 个笔记文件落后于 resources/study 的 2026-07-14 版;内容合并与 resources/study 退役属后续单独批准的迁移计划。

## [2026-07-16] feat | Obsidian 阅读通道 A 落地(Sonnet 代笔 / Claude 合同)
- 按 Claude 拟定的阅读通道 A 合同,建立 `.obsidian/`(app.json、appearance.json、snippets/reading.css)最小 vault 配置、`.gitignore` 追加 Obsidian 本地易变项、根目录 `阅读指南.md`。
- reading.css 约 70 行:行距/段距/标题留白/引用块/表格样式全部使用 Obsidian 主题变量,不硬编码颜色,亮暗两态均适配;未安装或配置任何社区插件。
- 本次提交未 push;工作树中 P01 摄入相关的既有未提交改动(`sources/bilibili/**`、`annotations/**`、`_index.md`、`log.md` 的既有修改)使用隔离提交手法保持原样,未被本次提交吸收。
