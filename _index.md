# study-notes 根索引

| 日期 | 条目 | 类型 | 摘要 | 本地路径 | 同步状态 |
|---|---|---|---|---|---|
| 2026-07-16 | [SCHEMA.md](SCHEMA.md) | index | 仓库 Schema(已批总装文书落地):三层结构、episode 状态机、D0–D5、legacy 兼容；批准文书与 Scope Recall 合同指向当前 ops-notes 真源 | SCHEMA.md | 已同步 |
| 2026-07-16 | [AGENTS.md](AGENTS.md) | index | 仓库规则入口:三层铁律、legacy bundle 边界、退役归档与当前 ops-notes 边界 | AGENTS.md | 已同步 |
| 2026-07-16 | [wiki/index.md](wiki/index.md) | index | 学科分支导航图入口(骨架) | wiki/index.md | 未同步 |
| 2026-07-16 | [P01 留言与思考](annotations/bilibili/395922059/BV1syNg6DEFi.md) | annotation | 主人已阅读并确认原话；D0 判为来源已有，D2 细化候选留待与 Claude 讨论，token 节省仍是待实测假设 | annotations/bilibili/395922059/BV1syNg6DEFi.md | 本地待验收 |
| 2026-07-16 | [B站：AI林湛星](sources/bilibili/395922059/视频索引.md) | source | 首条视频入库：平台 AI 字幕 192 条，未纠错、未总结；P01 已阅读并建立留言栏 | sources/bilibili/395922059/ | 本地待验收 |
| 2026-07-16 | [阅读指南](阅读指南.md) | index | Obsidian 阅读通道 A 说明：vault 配置、reading CSS、PC/移动端安装步骤、留言写法（含随文留言与边读边问） | 阅读指南.md | 本地待验收 |
| 2026-07-16 | [留言收割脚本](scripts/harvest_annotations.py) | script | 把连续阅读稿里的 `> [!留]` 随文留言确定性收割进 annotation 页（带原文引文/canonical 回链/递增块锚）；`批准蒸馏` 标记单独入 `wiki/_candidates/_distill-queue.md` 排队；纯 stdlib，测试见 `scripts/test_harvest.py` | scripts/harvest_annotations.py | 本地待验收（未装 cron） |
| 2026-07-16 | [收割 cron 包装](scripts/harvest_cron.sh) | script | flock 防重入 + fetch/pull --ff-only + 跑收割脚本 + 单主题提交推回；本次只写好脚本，未安装 crontab | scripts/harvest_cron.sh | 本地待验收（未装 cron） |
| (legacy) | photogrammetry-final-review/ | study | 摄影测量期末复习包(legacy bundle,待迁移合并) | photogrammetry-final-review/ | 落后于 resources/study 07-14 版 |
| (legacy) | spatial_database/ | study | 空间数据库课程包含 15 讲 PDF+复习笔记(legacy bundle;PDF 以本仓库为保管方) | spatial_database/ | 笔记落后于 resources/study 07-14 版 |
| (legacy) | spatial_statics/ | study | 空间统计课程包(legacy bundle,待迁移合并) | spatial_statics/ | 待对账 |
