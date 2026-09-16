# 书籍、论文与复现实验

这里是 `futures-learning-lab` 的统一阅读与文献入口。2026-09-16 从 `qlib-futures/docs/research/futures/` 迁入，工程仓库只保留迁移指引。

| 入口 | 用途 |
|---|---|
| [阅读路线](reading_roadmap.md) | 教材、论文、代码如何配合现有 M1–M8 阶段 |
| [五本核心书与选章](books.md) | Hull 第九版准确章号、Geman、Carver 两本书、AFML |
| [50 篇候选论文](papers_manifest.csv) | 保留原编号、优先级、研究市场和核验状态 |
| [18 项复现规格](replication_plan.md) | 研究问题、最小实验、基线和验收边界 |
| [实验登记](replications.csv) | R01–R18 的依赖、阶段、执行状态与证据路径 |
| [迁移与勘误](MIGRATION.md) | 来源提交、原始文件身份、书目修正和未核验范围 |

**不是五本全读、五十篇全读、十八个全做。** 第一轮以一个小实验为中心：先补合约与时间语义，再做 R04（TSMOM）、R02（CSMOM）、R09（Carry）。R01 提供定义和数据前置检查，不要求先完成其全部实证部分。后续按数据、问题和时间预算选择。

## 与现有计划的关系

[planning/plan.json](../planning/plan.json) 继续拥有八阶段、52 个相对周和原有工作包；本目录仅提供这些工作包的阅读材料与实验选项，不再增加另一份排期。每周预算仍待本人确认，不与大模型学习时间机械相加。

`replications.csv` 是文献实验登记，不替代 [PROGRESS.md](../PROGRESS.md) 的本人能力验收。迁移时全部登记为 `not_started`，不是把写好的规格算成完成。原有学习进度、Issue 和 Project 不因迁移改变。

## 读懂、核验和复现是三件事

- `verification_status`：`imported_unverified` 为原清单迁入但本次未复核；`metadata_checked` 仅核对书目元数据；`needs_review` 表示发现疑点。
- `metadata_checked_on` 和 `metadata_evidence_url` 保存核对日期与证据。元数据核对不等于已读全文、复现结果或验证所有研究结论。`notes` 中继承的研究描述也必须回到原文核对。
- `pdf_status=not_checked` 表示本次没有验证 PDF 下载；`candidate` 仅表示候选链接。出版社页面能打开不等于有全文权限，不绕过付费墙。
- `P0/P1/P2` 是原清单的学习优先级，不是质量评分；`core/optional/no` 是复现候选分类，不是个人进度。

书和论文的 PDF、EPUB、MOBI 保留在本人有权使用的本地文献库，不提交到公开 Git。这里保存来源、个人原创笔记、规格和可分享的小型实验；真实数据按 [数据政策](../docs/data-policy.md) 处理。

## 每次学习留下什么

使用 [书籍笔记](../templates/book-note.md)、[论文评审](../templates/paper-review.md)、[实验记录](../templates/experiment.md) 和已有 [周复盘](../templates/weekly-review.md)。完成一轮应能独立解释一个公式、给出一个反例，并留下可核对的结果或具体阻塞原因。

实验代码放入现有 `labs/`，研究规格与试验登记放入 `research/`，结果报告按原计划放入 `reports/`（实际产生时再建文件）。不要预先创建十八套空运行器，更不要在学习仓库另造生产交易引擎。
