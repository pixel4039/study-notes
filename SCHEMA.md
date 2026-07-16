# study-notes Schema

来源:`resources/decisions/2026-07-15__proposal__study-notes-schema-assembly.md`(2026-07-15 用户批准,7 个待批点按默认值生效)。本文件是该总装文书在仓库内的落地正文;冲突时以批准文书为准。

## 目录布局

```text
study-notes/
├── SCHEMA.md                 本文件
├── AGENTS.md                 仓库规则入口(.hermes.md/CLAUDE.md 指向它)
├── _index.md                 根索引(表格式,课程目录用 bundle 行)
├── log.md                    重要 ingest/update/审批日志
├── sources/                  来源原话,不可变层
│   ├── bilibili/<MID>/
│   │   ├── raw/<year>/<BVID>/P01.json          平台字幕/ASR 原始 JSON,不可变
│   │   ├── transcripts/<year>/<date>__<title-at-ingest>__<BVID>__P01.md
│   │   ├── metadata/
│   │   └── 视频索引.md
│   └── interactions/<year>/YYYY-MM-DD__<topic-slug>__NN.md   episode
├── annotations/              用户声音层,AI 不得覆盖
│   ├── bilibili/<MID>/<BVID>.md                视频摘录配套页
│   └── thinking/<topic-slug>.md                主题思考页
├── wiki/                     经 D0–D5 审批的蒸馏稿本体
│   ├── concepts/  methods/  cases/  glossary/
│   ├── _candidates/YYYY-MM-DD__<D级>__<concept>__<slug>.md
│   ├── index.md              学科分支导航图入口
│   └── log.md
└── legacy/<course>/          旧课程 legacy bundle(lint 全豁免)
```

> 过渡说明:根目录现存的 `photogrammetry-final-review/`、`spatial_database/`、`spatial_statics/` 是迁移前的 legacy bundle,原样保留、原地视同 `legacy/` 成员;正式并入 `legacy/` 或按新 schema 改造需单独迁移计划与用户批准。

## frontmatter

沿用 resources 字段集(title/type/created/updated/tags/sources/related/confidence/author),`type` 扩展:

```yaml
type: transcript | episode | annotation | thinking | concept | method | case | glossary | candidate | index
author: hermes | claude | codex | user        # created >= 2026-07-15 必填
```

## episode(sources/interactions/)

- Sol 在检查点自动转写完整保序对话段;AI 不改写;AI 注记只能放 `> [!ai-note]` callout。
- 回合 block ID:`^ep-YYYYMMDD-NN-q01` 递增。
- 专有字段:`status: active|consolidated|archived`、`last_activated`、`consolidated_by`(复述页或获批 wiki 页链接)、`source_session`。
- 生命周期:复述确认或对应蒸馏稿获批 → consolidated;**180 天**未激活 → archived(不删除,退出默认召回面)。「激活」= 被召回引用/重放/回链,由执行方更新 `last_activated`。

## annotations/

- thinking 页:一主题一页,条目带日期、状态 `current|revised|superseded|retracted`、block ID `^tk-<slug>-NNN`、来源回链;旧观点改状态不删正文。
- 转写条目用户确认前标 `tentative: true`,tentative 永不静默使用。
- 本层是用户声音:AI 只能转写与追加。
- 收割约定:主人可在连续阅读稿(`*连续阅读.md`)对应段落下方直接写 `> [!留] 想法` 随文留言;确定性脚本 `scripts/harvest_annotations.py`(纯 stdlib、零 LLM token)把它收割进对应 `annotations/bilibili/<MID>/<BVID>.md` 的「留言栏(用户原话)」,带日期小节、原文引文与 canonical 锚点回链 `[[...#^锚|mm:ss]]`、递增块锚 `^an-<bvid>-pNN-NNN`;原位置替换为收录指针 `> [!留] ✓ 已收录 → [[annotation页#^锚]]`。留言里写 `> [!留] 批准蒸馏 备注` 则改为进入 `wiki/_candidates/_distill-queue.md` 排队,原位置变 `✓ 已入蒸馏队列`;队列消费(生成正式 candidate)仍走 D0–D5 审批,不因收割自动触发。详见 `阅读指南.md`「随文留言写法」。

## wiki 与 D0–D5

- 概念页全局唯一真源;新来源增量走 `_candidates/`,按 D0(重复)/D1(新证据)/D2(细化)/D3(闪光点)/D4(案例反例)/D5(冲突,逐条确认)审批;候选必带**原始条目日期**与来源回链。
- 获批合并用 `[!insight]` 高亮;概念页回链原话块;页拆分/合并/重命名一律明确确认。
- `wiki/index.md` 是学科分支导航图入口(需求2的落点)。

## 阅读状态

分P级 `started`/`finished` 复选框;`finished: true` 触发全篇收口与 D0–D5 重判;不跟踪观看进度。

## 索引与日志义务

新重要页面登记 `_index.md`(课程/来源目录用 bundle 行,路径尾 `/`);重要动作在 `log.md` 追加一行。Scope Recall 只存指向本仓库的检索锚点(见 resources 锚点桥接合同),不存正文副本。
