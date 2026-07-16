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

## [2026-07-16] feat | 留言收割流水线落地(Sonnet 执行 / Claude 合同,Sol 验收)
- 依据合同 `.claude/jobs/fc51b3d3/tmp/CONTRACT-harvest.md` 与已批方案 `.claude/plans/effervescent-wiggling-hopcroft.md`,新增 `scripts/harvest_annotations.py`(纯 stdlib、零依赖):扫描 `sources/bilibili/*/transcripts/**/*连续阅读.md` 里未收割的 `> [!留]` callout,取上方最近段落前 60 字作引文,用段首 ~15 字(标点无关)在同目录 canonical 转写稿里做前缀匹配定位块锚与 mm:ss 时间戳(未命中则降级为仅存引文,不失败);收割进对应 `annotations/bilibili/<MID>/<BVID>.md` 的「留言栏(用户原话)」,追加日期小节 + 引文/回链 + 留言正文 + 递增块锚 `^an-<bvid>-pNN-NNN`(延续既有页面里的最大序号,不冲突);annotation 页缺失时按 `BV1syNg6DEFi.md` 既有结构建页;原位置替换为收录指针 `> [!留] ✓ 已收录 → [[annotation页#^锚]]`。
- 专用标记 `> [!留] 批准蒸馏 备注` 改为路由进 `wiki/_candidates/_distill-queue.md` 排队(不入留言栏),原位置替换为 `✓ 已入蒸馏队列`;队列消费仍走 D0–D5 审批,不因收割自动触发,不消耗 LLM token。
- 幂等设计:已收割/已入队的 callout 会被识别为"已处理"(标题以 ✓ 开头),重跑零变化;除目标 callout 行外,连续阅读稿其余字节零改动(已用切片哈希断言验证)。
- 新增 `scripts/harvest_cron.sh`:flock 防重入 → 无新提交且无待收割留言则退出 → `git pull --ff-only`(失败退出待下轮,不 rebase 不强推)→ 跑收割脚本 → 有变化则单主题提交 `harvest: annotations from reading comments` 并 push(被拒则留待下轮)→ 日志写 `.harvest.log`。**本次只写好脚本,未安装 crontab**,是否/何时接入由主人在 Sol 验收通过后另行决定。
- 新增 `scripts/test_harvest.py`(stdlib unittest,10 个测试类/方法,全部在系统 `/tmp` 临时目录构造沙箱跑,未触碰仓库真文件):空转、canonical 匹配命中/未命中降级、多留言锚号递增不冲突、非目标字节零改动(切片哈希断言)、指针替换正确、幂等重跑、dry-run 不写文件、annotation 缺失建页、蒸馏标记识别路由/重复幂等/队列格式。
- 配套文档:`阅读指南.md` 补「随文留言写法」(callout 语法、收割节奏、批准蒸馏标记)与「边读边问怎么问」(QQ/微信找 Sol,带 BVID + 原文引文,沿用现有 Scope Recall 通道,不新建聊天入口)两节;`SCHEMA.md` annotations 小节补收割约定一句;`.gitignore` 追加 `.harvest.log`、`.harvest.lock`;`_index.md` 登记两个新脚本。
- 本次提交只写 `study-notes/` 与 `/tmp/harvest-build-20260716/`,未 push、未装 crontab,遵守合同硬边界。
- Claude 验收(2026-07-16 晚):首轮取证抓出相邻 `[!留]` 合并且标记泄漏正文的 bug(续行循环未在新 callout 起始停止),修复轮补:相邻留言各自独立成条、`.gitignore` 补 `__pycache__/`、写入改同目录 tempfile+os.replace 原子替换(含故障注入测试);测试 12→15 个全绿,Haiku 独立沙箱复验通过后终审放行。crontab 仍未安装,待主人另批。

## [2026-07-16] governance | 迁移后活跃规则指针修正(Codex)
- 经主人授权，将 `AGENTS.md` 中已退役的 `resources/study/`、旧 `hermes-vps-notes` 与 `resources/decisions/...` 指针更新为只读归档、当前 `/home/ubuntu/ops-notes` 真源和现行远端；同步修正 `SCHEMA.md` 的批准文书与 Scope Recall 合同路径。
- 未改写 legacy 课程正文或历史记录；`python3 scripts/test_harvest.py` 复验 15/15 通过。
