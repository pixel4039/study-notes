---
title: 摄影测量原始提取文本迁移记录
type: source
created: 2026-07-16
updated: 2026-07-16
tags: [photogrammetry, course-materials, raw-extracted, migration]
sources: [raw-extracted/]
related: [../../../photogrammetry-final-review/_index.md]
confidence: high
status: active
author: codex
---

# 摄影测量原始提取文本迁移记录

> [!ai-note]
> 本页只记录迁移证据；`raw-extracted/` 下 11 份 `.txt` 是不可变课程原文，迁移时未改写内容。

- 原位置：`/home/ubuntu/ops-notes/photogrammetry_review_extracted/`
- 现位置：`/home/ubuntu/study-notes/sources/course-materials/photogrammetry/raw-extracted/`
- 文件数：11
- 路由理由：内容是摄影测量课程讲义/复习提取文本，属于学习资料，不属于运维或通用资源。
- 去重结论：迁移前对 study-notes 全树做 SHA-256 比对，11 份均无同哈希副本；因此作为独有 raw source 保留，不覆盖 legacy bundle。
- 回滚：从当前 Git 提交恢复本目录，或依据 `/home/ubuntu/ops-notes/ops/2026-07-17__ops__home-eg-sr-gemini-migration.md` 的迁移清单恢复原路径。

## SHA-256

```text
b87687d87ffae424b549eeeb76cb41d315ae7b018bd54172d32e65f9ecaedcd2  2024深圳大学摄影测量.txt
b9eddcac46144b65838058c3d543be004cf7ccf542516015cbe20ed67eb2be13  摄影测量学期末复习.txt
cc1b49755985cc8a86905cbfddadd78df4d7bc2048bb008a0388e0f451736291  第一讲 绪论-20250224.txt
3d7fce62bf9cb3b81f129558b2fa68bded17b08ea5b8f42b74298f74dc609598  第七讲 影像特征提取与匹配-20250609-part2.txt
79109f719107c2a750dd146299200b90efba930b114d10ebdf88f34c2a639455  第三讲 常用坐标系与共线方程-20250310.txt
809a870f0a8410cda0f355dc175ae920e361d703fc9508a70be8b14e4b8d957e  第九讲 密集匹配 part 1.txt
0df6f03f61371a0e337ee3370aecffb2fd7231b4017ed740ded3a6559d1c8935  第二讲 摄影测量基本知识-20250303.txt
5ebf2c5978d10471ebe95e1ee4e28b560d31867185050772dffd06ed6e021b05  第五讲 双像解析摄影测量-20250407.txt
06e95946e8f9b9feb971f2b5487eaa9f784a0cd2d166244905cc196b28f0510d  第八讲 特征匹配.txt
13c7dd4d6f61225536623e9587fcf8afb45e45afd18e8e73855cbb40c10edc13  第六讲 解析空中三角测量-20250512.txt
1affd570418d726d93036a98a9c333592587e15cf1866cea02089466e61c54e7  第四讲 单像空间后方交会-20250331.txt
```

## See Also

- [本 bundle 索引](_index.md)
- [摄影测量期末复习 legacy bundle](../../../photogrammetry-final-review/_index.md)
