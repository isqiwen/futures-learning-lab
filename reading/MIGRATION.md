# 2026-09-16 文献迁移与勘误

## 来源与归属

来源固定为 [qlib-futures 提交 c0161c1](https://github.com/isqiwen/qlib-futures/tree/c0161c1130ceeb98aca9bc4f1af654f86d3555c3/docs/research/futures)，迁移前目标仓库主分支为 `c5517da585f590323ef007ef21045633765e39f3`。

| 原路径（docs/research/futures/ 下） | 原 Git blob SHA | 本仓库归属 |
|---|---|---|
| README.md | 71d4a080e27ddfa407a1df9c7c28ad7a8b4051f5 | reading/README.md：重组为学习入口 |
| papers_manifest.csv | 430cad1e67fa59eab68cd0b0305e399e13c78321 | reading/papers_manifest.csv：保留 1–50 ID 并加核验字段 |
| reading_roadmap.md | b415606f0ad04aef43093c781ade538eb58ce459 | reading/reading_roadmap.md + books.md：对齐 M1–M8 |
| replication_plan.md | 4885594ef187ba287b75fa05979ccfaed9ecf3ac | reading/replication_plan.md + replications.csv：保留 R01–R18 |

原英文内容可从固定提交恢复；不是整段逐字复制，而是保留研究主题并纠正作用域、时序和核验问题。目标仓库不改变现有 `planning/plan.json`、52 周定义、本人学习进度、账户/生产代码，也不批量创建新的学习任务。

后续只在本仓库维护课程、书目和复现规格；`qlib-futures` 的旧 Markdown 入口改为迁移指引，旧 CSV 在目标文件确认后删除。Git 历史保留，不重写历史。

## 已修正的书目问题

| 论文 ID | 修正 | 一手核对入口 |
|---|---|---|
| 14 | Fuertes 等（2010）的 DOI 改为 `10.1016/j.jbankfin.2010.04.009`，不是原 `.09.009` | [City 仓库](https://openaccess.city.ac.uk/id/eprint/6416/) |
| 23 | Kim、Tse、Wald（2016）是 *Journal of Financial Markets* 论文；DOI `10.1016/j.finmar.2016.05.003`，不是原 jempfin DOI | [出版商条目](https://www.sciencedirect.com/science/article/abs/pii/S1386418116301379) |
| 29 | *Basis-Momentum* 的共同作者为 **Melissa Porras Prado**，不是原清单的 Francisco | [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12738) |
| 24、31、32 | 补全作者姓名和元数据证据入口 | 各行 `metadata_evidence_url` |
| 25 | 原 DOI 匹配未可靠确认，清空 `source_url` 并标为 `needs_review`，不猜测替代链接 | 待核验 |

本次抽核 13 条书目元数据，36 条保留 `imported_unverified`，1 条 `needs_review`。核验范围不是 50 篇全文，不能把迁移等同全部书目与论文结论已审查。后续修订会改变这些计数；当前状态以 CSV 为准。

`metadata_checked` 只代表对照了标题、作者、年份/版本等元数据，不等于已读全文、下载成功、证明模型效果或可实施交易。原 `notes` 的研究描述保留为线索，使用时仍需核对正文。

## 已调整的学习语义

原 Stage 0–6 主题并入现有 M1–M8，保留教材、经典因子、中国迁移、ML、文本、深度模型、RL 各线；不增加另一套时间承诺。五本书包括 *Advanced Futures Trading Strategies*，Hull 选章按用户当前第九版。

不要求先完成全部国外实证再研究中国；原论文样本与国内迁移分开报告。没有超过基准也是有效结果；十八项规格不是已实现代码，也不是个人掌握证据。原计划中的生产导向措辞改成学习报告与工程移交。

## 全文与权限

本次未下载或验证任何书/论文 PDF，所有 `pdf_status` 初始化为 `not_checked`。原对话中的下载包不作为本次可用性证据。书籍只登记出版社入口和版本；原文、付费数据和个人学习记录的公开范围须逐项确认。

## 校验边界

离线校验检查 CSV 结构、唯一身份、论文与 R 编号双向关系、阶段、依赖无环及完成状态所需证据。它不核验远端网址可达性、PDF 权限、金融结论或本人能力。

保留根目录 `MANIFEST.json` 作为 2026-09-14 初始化包身份；它不是滚动文件清单。迁移后日常使用 Git 和 CI，不重新运行初始化 `publish.py --apply`。
