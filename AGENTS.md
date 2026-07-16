# study-notes 仓库级 AGENTS.md

> 上位总则:`/home/ubuntu/AGENTS.md`(Home 治理总则)。在本仓库创建、移动、归档或重组文件前必须先读该总则;冲突时以上位总则为准。
> 本仓库 ↔ 远端 `pixel4039/study-notes`(默认分支 **master**,不是 main)。这是学习资料的唯一可编辑真源仓库;迁移前旧副本已于 2026-07-16 退役到只读归档 `/home/ubuntu/.archive/resources-study-retired-20260716/`,不再是活跃副本。

## 开工规则(所有 Agent)

1. 先读 `SCHEMA.md`,再查 `_index.md`,不重复建档、不放错层。
2. **三层铁律**:`sources/` 原话不可变(AI 注记只能进 `[!ai-note]` callout);`annotations/` 是用户声音,AI 只能转写与追加,转写未确认前标 `tentative: true`;`wiki/` 只有经 D0–D5 审批的内容才能写入,候选一律先进 `wiki/_candidates/`。
3. tentative 永不静默使用;误召(存伪)不可接受、精确率优先——引用任何本仓库内容时按此准则。
4. `created >= 2026-07-15` 的新页 frontmatter 必写 `author: hermes | claude | codex | user`。
5. 新重要页面登记 `_index.md`、记 `log.md`;新页与至少一个相关页双向链接(See Also),不造孤页。
6. 根目录现存课程目录(`photogrammetry-final-review/`、`spatial_database/`、`spatial_statics/`)是 **legacy bundle**:原样保留,lint 豁免,不得擅自改造、重命名或与已退役归档互相覆盖。
7. 每个提交单一主题;推送前确认分支为 master;不夹带无关文件。
8. 密钥、令牌、可恢复备份不进本仓库。

## 与其他系统的边界

- Scope Recall 只保存指向本仓库的检索锚点(路径+block ID+origin_date+状态),不存第二份可编辑正文——合同见 `/home/ubuntu/ops-notes/decisions/2026-07-15__proposal__scope-recall-anchor-bridge-contract.md`。
- 运维记录归 `/home/ubuntu/ops-notes`（远端 `pixel4039/ops-notes`），不进本仓库；通用资源归 `/home/ubuntu/resources`（2026-07-16 已落地为本地 Git 仓库，当前无远端）。

## 规则入口

`.hermes.md`、`CLAUDE.md` 为指向本文件的指针 stub,不重复维护正文。
