# 摄影测量学期末复习 · 课程索引

课程复习包，来自「摄影测量学」课程期末复习，双层资料结构（`detailed/` 详细版 + `simple/` 简版）。学习顺序与资料结构说明见 [README.md](README.md)，本页只做 SCHEMA.md「分层索引」规则下的文件清单，供根 `_index.md` 以一行 bundle 指向。

## 文件清单

### 总纲与考点（md，均已补 frontmatter，`status: active`）

| 文件 | 内容 |
|---|---|
| [00_总复习提纲与自测题.md](00_总复习提纲与自测题.md) | 总纲、公式速查、易混点、自测题 |
| [exam-focus.md](exam-focus.md) | 2024 题型重点与背诵优先级 |
| [README.md](README.md) | 资料结构、推荐学习顺序、详细版讲义进度表 |

### detailed/（Claude 详细版讲义，5 讲）

| 文件 | 内容 |
|---|---|
| [detailed/第一讲_绪论.md](detailed/第一讲_绪论.md) | 定义、三大原理、发展三阶段 |
| [detailed/第二讲_摄影测量基本知识.md](detailed/第二讲_摄影测量基本知识.md) | 航摄基础、中心投影、像点位移 |
| [detailed/第四讲_单像空间后方交会.md](detailed/第四讲_单像空间后方交会.md) | 内定向、后方交会、误差方程、精度 |
| [detailed/第六讲_解析空中三角测量.md](detailed/第六讲_解析空中三角测量.md) | 航带法、独立模型法、光束法、GPS/POS |
| [detailed/第七讲_影像特征提取与匹配_SIFT.md](detailed/第七讲_影像特征提取与匹配_SIFT.md) | SIFT、DoG、128 维描述子、RANSAC |

第三、五、八、九讲暂无详细版，用 `simple/` 对应篇目替代（见 README.md 进度表）。

### simple/（Hermes 早期简版讲义，9 讲全）

| 文件 | 内容 |
|---|---|
| [simple/01-绪论.md](simple/01-绪论.md) | 第一讲简版 |
| [simple/02-摄影测量基本知识.md](simple/02-摄影测量基本知识.md) | 第二讲简版 |
| [simple/03-常用坐标系与共线方程.md](simple/03-常用坐标系与共线方程.md) | 第三讲简版 |
| [simple/04-单像空间后方交会.md](simple/04-单像空间后方交会.md) | 第四讲简版 |
| [simple/05-双像解析摄影测量.md](simple/05-双像解析摄影测量.md) | 第五讲简版 |
| [simple/06-解析空中三角测量.md](simple/06-解析空中三角测量.md) | 第六讲简版 |
| [simple/07-影像特征提取与匹配.md](simple/07-影像特征提取与匹配.md) | 第七讲简版 |
| [simple/08-特征匹配.md](simple/08-特征匹配.md) | 第八讲简版 |
| [simple/09-密集匹配.md](simple/09-密集匹配.md) | 第九讲简版 |

### assets/（图表与生成脚本，未纳入 Markdown lint/索引范围）

`make_photogrammetry_diagram.py`、`make_photogrammetry_rigorous_diagram.py` 及其生成的 `.png` 示意图，供笔记内嵌图引用。

## 关联

- 根索引行：见 `_index.md` 中 `photogrammetry-final-review/` 一行。
