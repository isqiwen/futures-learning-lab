# 与 Northstar 的职责边界

2026-09-14 查看 `isqiwen/northstar-quant` README 时，该项目的定位是**一个仓库、一个 Python 包，三个应用：Data Hub、Research、Live**。README 区分研究/Paper/模拟/实盘，并明确完整柜台发单与撤单尚未实现。此处是当日读取快照，后续以实际主分支为准。

来源：[Northstar README](https://github.com/isqiwen/northstar-quant/blob/main/README.md)。学习组织参考：[LLM Learning Lab README](https://github.com/isqiwen/llm-learning-lab/blob/main/README.md) 与其 ROADMAP、Project 管理文档。

| 仓库 | 管什么 | 不管什么 |
|---|---|---|
| llm-learning-lab | 大模型原理、实现、系统实验和研究能力 | 期货生产交易 |
| futures-learning-lab | 市场、统计、产业、策略和风险知识；小型核对器与研究报告 | 生产采集服务、完整交易引擎、真实发单 |
| northstar-quant / Data Hub | 正式采集、质量、元数据、不可变数据发布 | 个人课程安排 |
| northstar-quant / Research | 正式因子、策略、回测、版本与研究任务 | 代替学习者能力验收 |
| northstar-quant / Live | 执行与运行边界、观察核对和后续受控柜台实现 | 把研究报告直接当交易授权 |

## 双向流动

学习实验 → 研究规范与失败案例 → Northstar 工程 Issue/PR → 独立工程验收。Northstar 导出的固定结果 → 学习仓库的小型独立核对器 → 差异报告。只链接已经存在的 Issue/PR，不编造编号。

知识仓库可有几百行教学参考实现，用于验证账本、as-of、换月与统计偏差；不为了“完整”重新造 PostgreSQL 服务、下载中心、回测平台、Web UI 或 CTP gateway。

## 移交内容

使用 [移交模板](../templates/handoff.md)：问题、证据、数据版本/授权、时间语义、信号/仓位/成本定义、错误用例、验收边界、未支持功能及回滚条件。学习验证与工程验证需要各自记录，不能互相冒充。

## 项目管理

学习使用独立 `Futures Learning & Research`。不把 52 个学习周任务塞入量化工程 Project #1，也不修改 `LLM Learning & Research`。涉及真实功能实现时才到 Northstar 开独立工程任务并双向链接。
