# Futures Learning Lab

**面向中国期货的量化学习与研究实验室。** 从市场机制、产业与统计基础，到可复核的策略研究、组合风控与执行验证。

主线：**国内商品期货 · 中低频（15 分钟至日线）· 小规模个人研究 · 趋势优先，期限结构/基差/产业与事件按证据扩展。**
金融期货与期权纳入知识地图；高频、做市、深度学习/RL 不是第一轮前提。

> 当前是规划与脚手架初始化，尚无本人学习验收成果；下一步是 **QF-W01：能力诊断与总时间预算**。
> 这是学习仓库，不是自动交易系统。生成计划、通过 CI、AI 写好代码都不等于掌握，更不等于证明能盈利。

## 从这里开始

| 文档 | 用途 |
|---|---|
| [START_HERE.md](START_HERE.md) | 第一周怎么开始、诊断与第一份交付物 |
| [KNOWLEDGE_MAP.md](KNOWLEDGE_MAP.md) | 12 个知识领域、优先级和目标能力 |
| [ROADMAP.md](ROADMAP.md) | 八阶段、能力门槛与范围 |
| [CURRICULUM.md](CURRICULUM.md) | 主课程、选读主题和一手资源 |
| [52 周执行基线](docs/weekly-plan.md) | 每周任务、具体产出、验收与依赖 |
| [研究协议](docs/research-protocol.md) | 数据、时间切分、成本、多重试验、负结果 |
| [产业研究](docs/commodity-research.md) | 产业链、宏观与事件的研究方式 |
| [Northstar 边界](docs/northstar-integration.md) | 学习成果如何进入现有工程项目 |
| [管理与发布](docs/project-management.md) | Issues、Milestones、独立 Project 与本机授权 |
| [PROGRESS.md](PROGRESS.md) | 只记录通过验收的成果 |
| [AGENTS.md](AGENTS.md) | AI 助教及编码助手的边界 |

## 验证本地脚手架

Python 3.10+，仅标准库；不下载真实行情、不请求任何账户、不发单。

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 examples/ledger_demo.py
python3 examples/asof_demo.py
python3 examples/selection_bias_demo.py
```

本地已通过 57 项测试，检查记录见 [VALIDATION.md](VALIDATION.md)。仓库文件与学习任务的远端创建是两件事：本仓库已包含任务定义，但未据此宣称 8 个 Milestones、61 个 Issues 或独立 Project 已创建。

三个演示使用明确标为合成的教学数据，帮助理解账本、信息可得时点和多重搜索。它们不是策略收益证据，也不自动完成对应学习任务。

## 获取仓库与初始化任务

```bash
git clone https://github.com/isqiwen/futures-learning-lab.git
cd futures-learning-lab
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

文件已经入库，不需要再次运行 `publish.py` 创建仓库。日常使用正常 Git 流程。
需要初始化远端学习任务时，在本机完成 GitHub CLI 授权后先预览，再显式写入：

```bash
python3 scripts/sync_issues.py                  # 离线预览
python3 scripts/sync_issues.py --apply          # 补齐 8 Milestones + 61 Issues
python3 scripts/sync_project.py --apply --create # 可选：独立学习 Project
```

权限和恢复步骤见 [INSTALL.md](INSTALL.md)。脚本只使用本机已授权 `gh`，不会索要或打印令牌；不会覆盖已有任务正文或学习状态。`publish.py` 保留用于向新的空仓库发布完整种子，不作为日常同步入口。没有自动配置 Project Views/工作流、原生 Sub-issues/Dependencies，也没有设置日历截止日。

## 三个仓库各管什么

`llm-learning-lab` 管大模型学习与实验；本仓库管期货量化知识与研究训练；`northstar-quant` 管 Data Hub / Research / Live 的工程实现。新建学习 Project **不使用量化工程 Project #1，也不改 LLM Project**。

## 执行原则

一个核心实践任务 + 一个配套阅读/核对任务；每周 6–8 小时和 52 周只是待确认的规划基线，不与 LLM 计划工时机械叠加。先正确、再有效、再讨论成本与可实施性。负结果是合法成果；任何课程或回测均不承诺未来收益。
