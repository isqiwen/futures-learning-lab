# Futures Learning Lab

**面向中国期货的量化学习与研究实验室。** 从市场机制、产业与统计基础，到可复核的策略研究、组合风控与执行验证。

主线：**国内商品期货 · 中低频（15 分钟至日线）· 小规模个人研究 · 趋势优先，期限结构/基差/产业与事件按证据扩展。**
金融期货与期权纳入知识地图；高频、做市、深度学习/RL 不是第一轮前提。

> 当前是规划与脚手架阶段，尚无本人学习验收成果；下一步仍是 **QF-W01：能力诊断与总时间预算**。
> 这是学习仓库，不是自动交易系统。生成计划、通过 CI、AI 写好代码都不等于掌握，更不等于证明能盈利。

## 从这里开始

| 文档 | 用途 |
|---|---|
| [START_HERE.md](START_HERE.md) | 第一周怎么开始、诊断与第一份交付物 |
| [书籍、论文与复现总入口](reading/README.md) | 五本书、50 篇候选论文、18 项实验规格 |
| [阅读路线](reading/reading_roadmap.md) | 教材、论文、代码配合现有 M1–M8；不是另一套排期 |
| [书籍与选章](reading/books.md) | Hull 第九版选章、Geman、Carver 两本书与 AFML |
| [KNOWLEDGE_MAP.md](KNOWLEDGE_MAP.md) | 12 个知识领域、优先级和目标能力 |
| [ROADMAP.md](ROADMAP.md) | 八阶段、能力门槛与范围 |
| [CURRICULUM.md](CURRICULUM.md) | 主课程、选读主题和一手资源 |
| [52 周执行基线](docs/weekly-plan.md) | 每周任务、产出、验收与依赖 |
| [研究协议](docs/research-protocol.md) | 数据、时间切分、成本、多重试验、负结果 |
| [产业研究](docs/commodity-research.md) | 产业链、宏观与事件的研究方式 |
| [工程移交边界](docs/northstar-integration.md) | 学习成果如何进入 qlib-futures 与 Northstar |
| [管理与发布](docs/project-management.md) | Issues、Milestones、独立 Project 与本机授权 |
| [PROGRESS.md](PROGRESS.md) | 只记录本人通过验收的成果 |
| [AGENTS.md](AGENTS.md) | AI 助教及编码助手的边界 |

## 阅读与实验如何推进

2026-09-16 将 `qlib-futures/docs/research/futures/` 的学习内容迁入 [reading/](reading/README.md)。这里成为唯一维护入口，工程仓库不再保存第二份书目。迁移来源与书目勘误见 [MIGRATION.md](reading/MIGRATION.md)。

先做合约/时间/资金核对，再做 **R04 TSMOM → R02 CSMOM → R09 Carry**；按需要扩展，不要求先读完五本书、五十篇论文或做完十八项实验。阅读可从 Hull 基础与 Carver 实践并行开始。

[论文清单](reading/papers_manifest.csv) 分开标记元数据核验与 PDF 状态；[实验登记](reading/replications.csv) 保存阶段、依赖和证据路径。迁移时实验全部 `not_started`，现有学习进度没有自动改变。使用 [书籍笔记](templates/book-note.md)、[论文评审](templates/paper-review.md) 和 [实验记录](templates/experiment.md)，不以空模板充当成果。

## 验证本地脚手架

Python 3.10+，仅标准库；不下载真实行情、不请求任何账户、不发单。

```bash
python3 scripts/validate.py
python3 scripts/validate_literature.py
python3 -m unittest discover -s tests -v
python3 examples/ledger_demo.py
python3 examples/asof_demo.py
python3 examples/selection_bias_demo.py
```

初始化时的 57 项测试记录见 [VALIDATION.md](VALIDATION.md)；后续变更以对应提交的 CI 和实际运行结果为准。文献校验新增 CSV 身份、阶段、依赖、证据状态检查，但不证明引用真实、全文可下载或本人已掌握。

三个演示使用明确标为合成的教学数据，帮助理解账本、信息可得时点和多重搜索。它们不是策略收益证据，也不自动完成对应学习任务。仓库含任务定义，不据此宣称 8 个 Milestones、61 个 Issues 或独立 Project 已创建。

## 获取仓库与初始化任务

```bash
git clone https://github.com/isqiwen/futures-learning-lab.git
cd futures-learning-lab
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

仓库已初始化，日常使用正常 Git 流程。`MANIFEST.json` 与 `publish.py` 属于原始种子发布机制，不用它们重新发布当前仓库。

需要初始化远端学习任务时，在本机完成 GitHub CLI 授权后先预览，再显式写入：

```bash
python3 scripts/sync_issues.py                  # 离线预览
python3 scripts/sync_issues.py --apply          # 补齐 8 Milestones + 61 Issues
python3 scripts/sync_project.py --apply --create # 可选：独立学习 Project
```

权限和恢复步骤见 [INSTALL.md](INSTALL.md)。脚本只使用本机已授权 `gh`，不会索要或打印令牌；不会覆盖已有任务正文或学习状态。没有自动配置 Project Views/工作流、原生 Sub-issues/Dependencies，也没有设置日历截止日。

## 仓库分工

`futures-learning-lab` 维护期货学习路线、书目、个人推导与小型可复核实验；`qlib-futures` 维护对应的 Qlib 扩展工程；`northstar-quant` 维护正式研究运行与交易系统；`llm-learning-lab` 维护大模型知识与实验。各自的工程验收与个人学习验收分开，不能互相代替。

学习 Project 不使用量化工程 Project #1，也不改 LLM Project。不提交书籍/论文全文、受限行情、凭据与账户资料。

## 执行原则

一个核心实践任务 + 一个配套阅读/核对任务；每周 6–8 小时和 52 周只是待确认的规划基线，不与 LLM 计划工时机械叠加。先正确、再有效、再讨论成本与可实施性。负结果是合法成果；任何课程或回测均不承诺未来收益。
