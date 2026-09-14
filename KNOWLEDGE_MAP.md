# 期货量化知识地图

“完整”指覆盖问题空间，不意味着第一年把所有主题学到专家级。下表领域按逻辑组织，八阶段按教学依赖组织，两者不一一对应。

| 领域 | 主阶段 | 第一轮目标 | 可验证交付 |
|---|---|---|---|
| [市场与合约机制](knowledge/market.md) | M1 | L2 | 三份带出处的合约卡 + 人工结算账本 |
| [商品、现货与产业链](knowledge/commodities.md) | M5 | L2 | 两个产业链档案 + 一份变量口径字典 |
| [宏观与跨市场传导](knowledge/macro.md) | M5 | L2 | 一份带发布时间的事件研究 |
| [数学、概率与统计推断](knowledge/statistics.md) | M2 | L2 | 手算/数值核对 + 纯噪声选择实验 |
| [数据工程与时间语义](knowledge/data.md) | M3 | L3 | 固定数据清单 + as-of/换月反例测试 |
| [计量与时间序列](knowledge/time-series.md) | M2 | L2 | 一份滚动预测基线对照 |
| [策略与收益来源](knowledge/strategies.md) | M4 | L3 | 两类策略的同协议费用后比较 |
| [回测、评价与可复现性](knowledge/evaluation.md) | M3 | L3 | M3 审计报告 + 最终可复核研究报告 |
| [组合、资金与风险](knowledge/portfolio.md) | M6 | L3 | 含整数约束与无法平仓情景的风险审计 |
| [执行、核对与运行安全](knowledge/execution.md) | M7 | L3 | 合成故障演练 + Northstar 移交规范 |
| [机器学习与 AI 辅助研究](knowledge/ml.md) | M8 | L2（进阶选修） | 一个等预算 ML 基线比较 |
| [研究方法、治理与复盘](knowledge/research.md) | M8 | L3；选题探索L4 | 复现/迁移检验 + 反方评审 + 能力证据清单 |

## 核心依赖

市场/合约 → 资金账本与风险；统计/时间序列 + 数据时点 → 可信回测；可信回测 + 收益机制 → 策略证据；策略证据 + 产业/宏观 → 增量研究；组合/执行验证 → 工程移交。机器学习是增量工具，不是跳过前面能力的捷径。

金融期货/期权/高频等扩展见 [ELECTIVES.md](ELECTIVES.md)。
