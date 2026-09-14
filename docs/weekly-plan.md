# 52 周执行基线

计划源：`planning/plan.json`。每个 QF-Wxx 是一个 6–8h 的工作包，含阅读、实践、分析和复盘；时间未获本人确认。W01 从真正开始学习算起，不能由当前日期推导日历截止日。下列产物路径是**待交付目标**，并不意味着这些实验已完成。

## M1 · 市场机制与能力诊断

阶段门槛：独立解释合约、保证金和逐日结算；完成三份带来源的合约卡与人工账本核对。

### QF-W01 · 能力诊断、总时间预算与学习环境

分类：Evaluation；优先级：P0；前置：无；先完成诊断。

选读资源：CME, MIT-PROB（参见 [资源登记](resources.md)）。

产物：`notes/diagnostic.md`、`notes/time-budget.md`。

验收：
- [ ] 独立完成诊断题并区分会解释、会实现、待补课
- [ ] 记录与 llm-learning-lab 共用的每周总预算，不叠加两份全时计划
- [ ] 运行仓库测试，明确这只验证脚手架而非个人能力

独立问答：**为什么软件测试全通过仍不能证明你掌握量化研究？**

### QF-W02 · 读懂三个国内期货合约与规则版本

分类：Learning；优先级：P1；前置：QF-W01。

选读资源：SHFE, DCE, CZCE, CFA（参见 [资源登记](resources.md)）。

产物：`notes/contracts/three-contracts.md`。

验收：
- [ ] 至少跨两个交易所选择三个品种，记录来源、生效日、查询日
- [ ] 解释乘数、tick、到期、交割和自然人持仓约束；未知项标为待核验
- [ ] 区分交易所最低要求与期货公司实际条件，不写死当前费率

独立问答：**为什么主力连续不是一个可以直接下单的合约？**

### QF-W03 · 盈亏、逐日结算、手续费与保证金

分类：Implementation；优先级：P0；前置：QF-W02。

选读资源：CME, SHFE（参见 [资源登记](resources.md)）。

产物：`labs/ledger-audit/`、`reports/ledger-audit.md`。

验收：
- [ ] 人工与代码核对多空、隔夜、平今及平昨的教学案例
- [ ] 资金权益与保证金占用分列；收益分母明确，不用占用保证金冒充总资金收益
- [ ] 扩展示例加入至少一个失败用例；教学规则不可当成真实结算规则

独立问答：**释放保证金为什么不等于赚到了钱？**

### QF-W04 · 交易时段、风险机制与 M1 复盘

分类：Evaluation；优先级：P1；前置：QF-W03。

选读资源：SHFE-EDU, SHFE, CZCE, GFEX, CSRC-EDU（参见 [资源登记](resources.md)）。

产物：`notes/market-mechanics.md`、`reports/M1-review.md`。

验收：
- [ ] 说明夜盘自然日和交易日的区别，并核验选定品种日历
- [ ] 记录涨跌停、限仓、临近交割等需动态复核的项目
- [ ] 不查笔记解释三份合约卡与账本；不通过则延长阶段

独立问答：**止损单为什么不能保证在设定价格离场？**

## M2 · 统计、时间序列与研究方法

阶段门槛：能做时间顺序评价、区间估计与多重尝试记录；不以一次高 Sharpe 判断有效。

### QF-W05 · 概率、尾部与风险的数值直觉

分类：Learning；优先级：P1；前置：QF-W04。

选读资源：MIT-PROB（参见 [资源登记](resources.md)）。

产物：`notes/probability.md`、`labs/tail-risk/`。

验收：
- [ ] 解释条件概率、期望、方差与样本依赖
- [ ] 比较正态假设与合成厚尾序列，不把样本最大亏损当风险上界
- [ ] 推导期望盈亏并写出收益期望不能决定资金生存的反例

独立问答：**高胜率策略为什么仍可能有负期望或破产风险？**

### QF-W06 · 统计推断、相关样本与置信区间

分类：Experiment；优先级：P1；前置：QF-W05。

选读资源：MIT-PROB, FPP3（参见 [资源登记](resources.md)）。

产物：`labs/inference/`、`reports/inference.md`。

验收：
- [ ] 比较独立样本 bootstrap 与分块抽样的适用边界
- [ ] 报告效应大小和区间，而非只给 p 值
- [ ] 给出自相关减少有效样本信息的合成例子

独立问答：**一万根分钟 K 线为什么不等于一万个独立样本？**

### QF-W07 · 回归、协方差与正则化基础

分类：Implementation；优先级：P1；前置：QF-W06。

选读资源：MIT-PROB, ISLP（参见 [资源登记](resources.md)）。

产物：`labs/regression-baseline/`、`notes/regression.md`。

验收：
- [ ] 用小样本手工/库函数核对线性回归或 ridge
- [ ] 解释共线性、估计误差和标准化的作用
- [ ] 所有拟合参数仅来自训练段，构造全样本标准化泄漏反例

独立问答：**模型拟合更好与可交易收益更好差在哪里？**

### QF-W08 · 时间序列、非平稳与结构变化

分类：Learning；优先级：P1；前置：QF-W07。

选读资源：FPP3, FPP-PY（参见 [资源登记](resources.md)）。

产物：`notes/time-series.md`、`labs/time-series-diagnostics/`。

验收：
- [ ] 区分价格、收益、价差与差分序列
- [ ] 检查 ACF、趋势和波动聚集；解释检验的假设与局限
- [ ] 给出制度或合约改变导致结构变化的研究处理原则

独立问答：**两个价格高度相关为何不足以证明价差均值回归？**

### QF-W09 · 滚动预测起点与朴素基线

分类：Experiment；优先级：P1；前置：QF-W08。

选读资源：FPP-CV, FPP-PY（参见 [资源登记](resources.md)）。

产物：`labs/rolling-forecast/`、`reports/rolling-forecast.md`。

验收：
- [ ] 以 expanding 或 rolling 方式重估，训练时刻严格早于预测时刻
- [ ] 对照持平/历史均值等朴素预测，不先扫大量模型
- [ ] 区分预测误差指标与含成本交易收益

独立问答：**为什么随机拆分时间序列可能虚高结果？**

### QF-W10 · 多重尝试、试验登记与 M2 门槛

分类：Evaluation；优先级：P0；前置：QF-W09。

选读资源：PBO, DSR, ISLP（参见 [资源登记](resources.md)）。

产物：`research/trial-register.csv`、`reports/M2-review.md`。

验收：
- [ ] 运行并解释纯噪声搜索示例，再换种子检查差异
- [ ] 登记每个试验家族、参数尝试和被否定结果；不编造有效独立次数
- [ ] 在任何真实收益研究前冻结数据切分及首次评价协议

独立问答：**从一千个参数中选冠军，为什么不只评冠军的 Sharpe？**

## M3 · 期货数据与可信回测

阶段门槛：合约级账本、换月、成本、可成交性和 as-of 时间通过审计；负面对照能抓住未来函数。

### QF-W11 · 数据授权、字段契约与固定快照

分类：Implementation；优先级：P1；前置：QF-W02, QF-W10。

选读资源：TUSHARE, SHFE, NAUTILUS-BT（参见 [资源登记](resources.md)）。

产物：`notes/data-contract.md`、`data/manifests/study-example.json`。

验收：
- [ ] 记录供应商、字段、单位、许可、覆盖、查询版本和哈希
- [ ] 真实行情保存在仓库外，仓库仅有可公开元数据或合成数据
- [ ] 列出缺失、重复、无成交与停止交易的不同语义

独立问答：**原始数据被修订之后，怎样复跑去年做过的实验？**

### QF-W12 · 夜盘、交易日与多周期时间对齐

分类：Implementation；优先级：P1；前置：QF-W11。

选读资源：SHFE, FPP-CV（参见 [资源登记](resources.md)）。

产物：`labs/session-alignment/`、`reports/session-alignment.md`。

验收：
- [ ] 按真实交易时段验证分钟聚合，不跨休市拼接伪连续时段
- [ ] 区分 event_time、available_at、received_at 与 decision_time
- [ ] 测试夜盘、节假日、海外夏令时及迟到记录

独立问答：**日线最终成交量能否用于当天早盘选择主力？**

### QF-W13 · 可投资品种池与主力映射的 as-of 约束

分类：Experiment；优先级：P1；前置：QF-W12。

选读资源：TUSHARE, SHFE, DCE（参见 [资源登记](resources.md)）。

产物：`labs/universe-asof/`、`reports/universe-audit.md`。

验收：
- [ ] 品种与合约在当时已上市且满足事先定义的流动性条件
- [ ] 主力/次主力选择只使用决策时已知的信息
- [ ] 保留退市与失败样本；区分供应商最终主连与历史可交易映射

独立问答：**用今天最活跃的品种回测十年，会漏掉哪些样本？**

### QF-W14 · 换月、连续价格与真实可交易盈亏

分类：Implementation；优先级：P0；前置：QF-W13。

选读资源：CME, NAUTILUS-BT（参见 [资源登记](resources.md)）。

产物：`labs/roll-audit/`、`reports/roll-audit.md`。

验收：
- [ ] 手工构造主连换月跳空，并与两条真实合约腿的盈亏对照
- [ ] 信号序列、执行价格、结算价格分离；记录复权构造时点
- [ ] 计入旧仓平仓和新仓开仓成本，解释价差不自动等于收益

独立问答：**近月100、远月110，换过去是不是立刻赚10？**

### QF-W15 · 最小回测账本与 Northstar 差分核对

分类：Implementation；优先级：P0；前置：QF-W03, QF-W14。

选读资源：CME, NAUTILUS-BT, VNPY（参见 [资源登记](resources.md)）。

产物：`labs/ledger-oracle/`、`reports/northstar-ledger-gap.md`。

验收：
- [ ] 只做小型独立核对器，不再搭建生产回测平台
- [ ] 逐笔记录成交、持仓、现金/权益、费用和结算；可人工复核
- [ ] 与现有 Northstar 导出结果比较，缺接口则提交规范而不伪造已集成

独立问答：**持仓收益、已实现收益和账户权益如何在换月日核对？**

### QF-W16 · 成交约束：成本、涨跌停和不可成交

分类：Experiment；优先级：P0；前置：QF-W15。

选读资源：SHFE, CZCE, NAUTILUS-BT（参见 [资源登记](resources.md)）。

产物：`labs/fill-adversarial/`、`reports/fill-assumptions.md`。

验收：
- [ ] 信号产生后才允许成交，明确下一 bar/报价及滞后
- [ ] 测试涨跌停、无量、部分成交与双腿不同时成交
- [ ] 明确日线/分钟线不能恢复真实排队顺序，结论标注模型假设

独立问答：**看到最高价经过限价单价格，能否断言已经成交？**

### QF-W17 · 训练、验证、测试隔离与标签重叠

分类：Implementation；优先级：P0；前置：QF-W16。

选读资源：FPP-CV, ISLP, PBO（参见 [资源登记](resources.md)）。

产物：`research/evaluation-protocol.md`、`labs/leakage-tests/`。

验收：
- [ ] 训练/验证/最终测试的功能分离；测试集不参与择参
- [ ] 当标签跨区间时按实际信息跨度 purge；embargo 需解释适用方式
- [ ] 未来字段、全样本标准化、调过的测试集等负面对照被识别

独立问答：**purge 和 embargo 为什么不是随意空出固定百分之几？**

### QF-W18 · 端到端回测审计与 M3 冻结基线

分类：Evaluation；优先级：P0；前置：QF-W17。

选读资源：NAUTILUS-BT, PBO（参见 [资源登记](resources.md)）。

产物：`reports/M3-audit.md`、`research/baseline-spec.md`。

验收：
- [ ] 从固定数据到费用后权益曲线均能复跑并对账
- [ ] 至少覆盖换月、时间泄漏、手续费和不可成交的反例
- [ ] 通过正确性门槛后才研究策略表现；修复消耗本周而不硬赶进度

独立问答：**漂亮收益曲线出现时，你先排除哪五类工程假象？**

## M4 · 核心策略家族

阶段门槛：趋势为主，carry/截面/价差选配；至少两类策略在同一协议下比较，保留负结果。

### QF-W19 · 趋势收益来源与 Time Series Momentum 深读

分类：Research；优先级：P1；前置：QF-W18。

选读资源：TSMOM, MIT-FIN（参见 [资源登记](resources.md)）。

产物：`papers/time-series-momentum-review.md`、`research/trend-hypothesis.md`。

验收：
- [ ] 区分时序趋势与截面动量
- [ ] 记录原论文市场、频率、成本及自身迁移差异
- [ ] 写可证伪假设、比较基线、失败条件，不预设国内一定有效

独立问答：**为什么海外月度趋势的证据不能直接证明国内15分钟策略有效？**

### QF-W20 · 趋势基线：动量、均线、突破

分类：Implementation；优先级：P1；前置：QF-W19。

选读资源：TSMOM, VNPY（参见 [资源登记](resources.md)）。

产物：`labs/trend-baselines/`、`reports/trend-baselines.md`。

验收：
- [ ] 选一条主实现，其余只做小规模结构对照
- [ ] 参数在验证方案中约束，记录全部试验而不广搜最优
- [ ] 信号滞后一致、成本一致、资金口径一致

独立问答：**趋势模型是在预测价格，还是在规定持仓响应规则？**

### QF-W21 · 波动率缩放与整数手数

分类：Experiment；优先级：P1；前置：QF-W20。

选读资源：MIT-FIN, TSMOM（参见 [资源登记](resources.md)）。

产物：`labs/volatility-sizing/`、`reports/volatility-sizing.md`。

验收：
- [ ] 用过去信息估计波动，避免全样本波动缩放
- [ ] 测试零/低波动、缺失值和不稳定估计的处理
- [ ] 比较连续权重与整数合约，记录最小交易单位造成的偏差

独立问答：**同样名义权重为什么不代表同样风险？**

### QF-W22 · 趋势策略的 walk-forward 与机制敏感性

分类：Evaluation；优先级：P1；前置：QF-W21。

选读资源：TSMOM, FPP-CV（参见 [资源登记](resources.md)）。

产物：`reports/trend-walk-forward.md`。

验收：
- [ ] 固定方案后分时段和按品种外推，不挑最好时间段
- [ ] 分析费用、换月规则和波动窗口的扰动
- [ ] 明确该周测试数据后续已属于开发证据，不能重复称最终留出

独立问答：**换月规则稍变收益就消失，应该得出什么结论？**

### QF-W23 · 期限结构、基差与 carry 的区别

分类：Learning；优先级：P1；前置：QF-W22。

选读资源：CME, CFA, SHFE（参见 [资源登记](resources.md)）。

产物：`notes/carry-conventions.md`、`labs/curve-features/`。

验收：
- [ ] 显式定义近远月符号、期限、计价单位和年化约定
- [ ] 区分现货基差与纯期货曲线 proxy，不把后者包装为真实现货基差
- [ ] 解释仓储、资金与交割差异；不能由曲线形状断言无风险利润

独立问答：**正向市场、负向市场与下一期实际展期盈亏是什么关系？**

### QF-W24 · 截面动量与 carry 的统一比较

分类：Experiment；优先级：P1；前置：QF-W21, QF-W23。

选读资源：TSMOM, MIT-FIN（参见 [资源登记](resources.md)）。

产物：`labs/cross-sectional-signals/`、`reports/cross-sectional.md`。

验收：
- [ ] 同一 as-of 可交易池中计算排名与分组
- [ ] 明确等权、等风险和缺失样本处理，记录行业暴露
- [ ] 费用后与简单趋势比较，不只报告 IC

独立问答：**IC 较高为什么可能仍无法盈利？**

### QF-W25 · 均值回归与反转：先寻找失败条件

分类：Experiment；优先级：P1；前置：QF-W24。

选读资源：FPP3, ISLP（参见 [资源登记](resources.md)）。

产物：`labs/reversal-baseline/`、`reports/reversal-failure-cases.md`。

验收：
- [ ] 建立简单反转基线及趋势期失效样本
- [ ] 区分超卖叙事与可验证统计条件
- [ ] 报告换手、尾部损失和费用，不按胜率选策略

独立问答：**价格跌得多为什么不是买入的充分条件？**

### QF-W26 · 跨期/跨品种价差与双腿风险

分类：Experiment；优先级：P1；前置：QF-W08, QF-W16, QF-W23。

选读资源：CME, CFA, FPP3（参见 [资源登记](resources.md)）。

产物：`labs/spread-study/`、`reports/spread-study.md`。

验收：
- [ ] 先验证经济关联、单位与两腿交易时段，再考虑统计关系
- [ ] 对冲比率或协整参数只用过去数据估计；高相关不是平稳证据
- [ ] 计入双腿成本、整数配比、交割差异和单腿暴露

独立问答：**统计价差回归为什么不等于无风险套利？**

### QF-W27 · 季节性和库存信号的时点约束

分类：Experiment；优先级：P1；前置：QF-W26。

选读资源：CFA, USDA, SHFE（参见 [资源登记](resources.md)）。

产物：`labs/seasonality/`、`reports/seasonality.md`。

验收：
- [ ] 区分月份规律、样本偶然性与交割季节效应
- [ ] 季节均值仅由过去年份计算；库存按实际发布日期对齐
- [ ] 比较价格独立基线；库存数据不可用则记录失败与替代设计

独立问答：**仓单减少是否一定说明终端需求变好？**

### QF-W28 · 策略家族对照与 M4 门槛

分类：Evaluation；优先级：P0；前置：QF-W27。

选读资源：PBO, DSR, TSMOM（参见 [资源登记](resources.md)）。

产物：`reports/M4-strategy-comparison.md`。

验收：
- [ ] 在同一数据快照和成本假设下比较至少两类策略
- [ ] 保留参数搜索记录、负结果和资金/风险暴露解释
- [ ] 形成保留/淘汰/证据不足三类结论，不以必须赚钱验收

独立问答：**你能否解释收益来自方向、波动缩放还是交易成本假设？**

## M5 · 产业、宏观与事件

阶段门槛：两个产业链知识档案及一个严格按当时可用信息构建的基本面或事件实验。

### QF-W29 · 产业链地图：先精读两条链

分类：Learning；优先级：P1；前置：QF-W28。

选读资源：CFA, SHFE, DCE, CZCE（参见 [资源登记](resources.md)）。

产物：`notes/commodities/two-chains.md`。

验收：
- [ ] 从黑色、有色、能源化工、油脂油料、农产品等选两条主线
- [ ] 整理供需、成本、产能、贸易、库存和可交割品联系
- [ ] 为每个关键变量指定一手来源和可得性，不凭新闻标题归因

独立问答：**库存、产量与产能分别属于什么变量？**

### QF-W30 · 供需平衡表与统计口径

分类：Implementation；优先级：P1；前置：QF-W29。

选读资源：USDA, EIA, NBS, CFA（参见 [资源登记](resources.md)）。

产物：`labs/balance-sheet/`、`notes/balance-sheet-conventions.md`。

验收：
- [ ] 统一单位、统计期间、地域、进口/出口和库存定义
- [ ] 对一条链建立可核对平衡表及误差项
- [ ] 区分估算、初值、修订值，不将修订后平衡表前推使用

独立问答：**为什么同一商品不同来源库存数不能直接相加？**

### QF-W31 · 现货基差、仓单与产业利润

分类：Research；优先级：P1；前置：QF-W30。

选读资源：SHFE, CFA, CZCE（参见 [资源登记](resources.md)）。

产物：`notes/spot-basis-audit.md`、`research/fundamental-feature-spec.md`。

验收：
- [ ] 核查现货品级、地点、税、汇率和交割品可比性
- [ ] 区分社会库存、交易所库存、仓单和可交割库存
- [ ] 估算利润注明加工比率和成本遗漏，未授权现货数据不入仓库

独立问答：**没有真实可比现货价格时，你的基差因子到底测量什么？**

### QF-W32 · 宏观、美元与内外盘传导

分类：Learning；优先级：P1；前置：QF-W31。

选读资源：MIT-FIN, ALFRED, NBS, EIA（参见 [资源登记](resources.md)）。

产物：`notes/macro-transmission.md`、`labs/macro-asof/`。

验收：
- [ ] 画出可检验的传导路径及相反解释
- [ ] 历史宏观变量使用当时版本，处理发布时间与时区
- [ ] 区分相关、条件预测和因果，不把单次事件写成定律

独立问答：**为什么降息既可能伴随商品上涨，也可能伴随下跌？**

### QF-W33 · 事件研究：EIA 或 USDA 的单一案例

分类：Experiment；优先级：P1；前置：QF-W32。

选读资源：EIA, EIA-SCHEDULE, USDA, ALFRED（参见 [资源登记](resources.md)）。

产物：`research/event-study-protocol.md`、`reports/event-study.md`。

验收：
- [ ] 事先定义事件、估计窗、反应窗与异常/对照基线
- [ ] 核验首次公布时间、节假日和夏令时；未获取时点信息则不能声称可交易
- [ ] 公布值、预期差与事后修订分离，缺共识预期时明确研究问题改变

独立问答：**知道某月报告的最终值，是否就知道公告时市场受到的冲击？**

### QF-W34 · 一个基本面增量实验与 M5 复盘

分类：Evaluation；优先级：P1；前置：QF-W33。

选读资源：USDA, EIA, ALFRED, PBO（参见 [资源登记](resources.md)）。

产物：`reports/M5-fundamentals.md`。

验收：
- [ ] 仅选择一个新增变量，对比价格基线和基线+变量
- [ ] 冻结试验预算并说明数据时点与覆盖的限制
- [ ] 资料不足可以产出否定/不可检验报告，不能合成真实结论

独立问答：**基本面解释合理，但没有样本外增量时该怎样处理？**

## M6 · 组合、成本与风险

阶段门槛：整数手数、资金分母、相关性、保证金和不可平仓压力均有证据；不要求盈利。

### QF-W35 · 组合理论与朴素配置基线

分类：Implementation；优先级：P1；前置：QF-W21, QF-W28。

选读资源：MIT-FIN（参见 [资源登记](resources.md)）。

产物：`labs/portfolio-baselines/`、`notes/portfolio-risk.md`。

验收：
- [ ] 对比等权、波动倒数与受约束配置的少量基线
- [ ] 解释协方差估计误差、相关性与杠杆
- [ ] 分别报告单策略和组合的资金收益口径

独立问答：**多个策略都赚钱是否就能保证组合更稳？**

### QF-W36 · 小资金约束、合约粒度与风险预算

分类：Experiment；优先级：P1；前置：QF-W35。

选读资源：CME, MIT-FIN（参见 [资源登记](resources.md)）。

产物：`labs/integer-allocation/`、`reports/small-capital-feasibility.md`。

验收：
- [ ] 只使用明确标为假设的资金情景，不代入用户真实账户
- [ ] 测试最小一手、合约乘数、费用与保证金导致的不可行配置
- [ ] 允许不交易；不可为了凑满品种而强制提高风险

独立问答：**理论上10%权重对应0.2手时，怎样诚实处理？**

### QF-W37 · 行业聚类、相关性变化与分散

分类：Experiment；优先级：P1；前置：QF-W36。

选读资源：MIT-FIN, CFA（参见 [资源登记](resources.md)）。

产物：`labs/correlation-stress/`、`reports/diversification.md`。

验收：
- [ ] 按经济链条及历史相关性识别集中暴露
- [ ] 估计只用训练窗口，不用危机后的协方差回看配置
- [ ] 比较常态与相关性抬升情景，风险预算不等于风险保证

独立问答：**十个品种为什么可能只有两三个风险来源？**

### QF-W38 · 尾部、保证金与无法平仓压力测试

分类：Evaluation；优先级：P0；前置：QF-W37。

选读资源：SHFE, CZCE, GFEX, CME（参见 [资源登记](resources.md)）。

产物：`labs/margin-stress/`、`reports/margin-stress.md`。

验收：
- [ ] 压力场景包括连续涨跌停、跳空、保证金上调与流动性消失
- [ ] 展示权益、占用、可用资金和风险限制，不假设止损必能成交
- [ ] 明示教学场景与真实交易所/期货公司政策的差异

独立问答：**净值仍为正时为什么也可能不能继续持仓？**

### QF-W39 · 交易成本、容量与参与率

分类：Experiment；优先级：P1；前置：QF-W38。

选读资源：NAUTILUS-BT, VNPY（参见 [资源登记](resources.md)）。

产物：`research/cost-model-spec.md`、`reports/cost-sensitivity.md`。

验收：
- [ ] 费用、点差、冲击与延迟分项，场景化而不伪称精确估计
- [ ] 按可观察交易量、时段和合约评估规模约束
- [ ] 没有逐笔或盘口数据时，明确日线研究不能验证排队成交

独立问答：**收益随着规模放大为什么不能线性外推？**

### QF-W40 · 组合外推评价与 M6 门槛

分类：Evaluation；优先级：P0；前置：QF-W39。

选读资源：MIT-FIN, PBO, DSR（参见 [资源登记](resources.md)）。

产物：`reports/M6-portfolio-audit.md`。

验收：
- [ ] 组合、成本和风控规则在评价前冻结
- [ ] 呈现风险调整和未调整表现、回撤路径及不确定性
- [ ] 输出继续研究/暂停/淘汰，不把本关当实盘准入

独立问答：**最坏历史回撤为什么不是未来亏损的上限？**

## M7 · 执行、运维与模拟验证

阶段门槛：订单状态、恢复核对和故障演练可复核；Paper/只读/影子/实盘证据严格分开。

### QF-W41 · 订单生命周期与本地故障注入

分类：Implementation；优先级：P1；前置：QF-W16, QF-W40。

选读资源：VNPY, NAUTILUS（参见 [资源登记](resources.md)）。

产物：`labs/order-state-fixtures/`、`notes/execution-state.md`。

验收：
- [ ] 列出下单、确认、拒绝、部分成交、撤单和撤单失败状态
- [ ] 测试重复、乱序、超时和取消后迟到成交回报
- [ ] 仅合成事件，不连接真实发单通道

独立问答：**撤单请求返回成功与订单已经撤销有何区别？**

### QF-W42 · CTP/SimNow 只读观察与环境边界

分类：Operations；优先级：P1；前置：QF-W41。

选读资源：SIMNOW, VNPY（参见 [资源登记](resources.md)）。

产物：`notes/simnow-observation-plan.md`、`reports/read-only-observation.md`。

验收：
- [ ] 从当前官方及期货公司材料核验 API、接入地址、权限与时段
- [ ] 先做脱敏日志或本地回放；可用时才在本人授权模拟账户只读观察
- [ ] 研究、Paper、SimNow 与真实账户证据分开；未连通如实记录

独立问答：**模拟行情、模拟成交与真实柜台执行分别证明了什么？**

### QF-W43 · 恢复、幂等与账户/委托核对

分类：Experiment；优先级：P0；前置：QF-W42。

选读资源：NAUTILUS, VNPY（参见 [资源登记](resources.md)）。

产物：`labs/reconciliation-fixtures/`、`reports/recovery-drill.md`。

验收：
- [ ] 定义具有业务域边界的订单和成交去重键
- [ ] 重启前后对照持仓、未完委托、成交和本地意图
- [ ] 恢复先核对再人工批准，不自动重发不确定订单

独立问答：**连接断开时不知道订单有没有成交，应不应该直接重发？**

### QF-W44 · 运行监控、风险开关与故障手册

分类：Operations；优先级：P1；前置：QF-W43。

选读资源：NAUTILUS, VNPY, CSRC-EDU（参见 [资源登记](resources.md)）。

产物：`notes/runbook.md`、`reports/failure-drills.md`。

验收：
- [ ] 区分禁止新仓、撤单、主动平仓和断开连接
- [ ] 演练行情过期、时钟偏差、进程重启、磁盘与网络故障
- [ ] 规则、报告、账号适当性等列为需向期货公司核验事项；不写已完成合规

独立问答：**停掉策略进程为什么不一定停止已有订单带来的风险？**

### QF-W45 · 前瞻 Paper/影子观察与偏差归因

分类：Evaluation；优先级：P1；前置：QF-W44。

选读资源：NAUTILUS-BT, VNPY（参见 [资源登记](resources.md)）。

产物：`research/forward-observation-spec.md`、`reports/paper-shadow-gap.md`。

验收：
- [ ] 冻结候选版本和观察窗口，再记录之后产生的信息
- [ ] 累计延迟、漏信号、费用和不可成交差异，不仅看净值
- [ ] 观察窗口未结束或样本不足时标记进行中/证据不足，不强行验收盈利

独立问答：**过去文件回放的 Paper 与前瞻影子观察有什么不同？**

### QF-W46 · 向 Northstar 移交规范与 M7 门槛

分类：Evaluation；优先级：P0；前置：QF-W45。

选读资源：NAUTILUS, VNPY（参见 [资源登记](resources.md)）。

产物：`research/northstar-handoff.md`、`reports/M7-execution-audit.md`。

验收：
- [ ] 形成数据字段、时间语义、信号、仓位、成本、故障用例和回滚条件
- [ ] 链接 Northstar 实际实现 Issue/PR；没有就明确仅提交学习规格
- [ ] 学习仓库没有自动发单、部署生产或账户密钥

独立问答：**一项研究在什么时候才有资格进入独立的工程验收流程？**

## M8 · 复现、机器学习对照与独立研究

阶段门槛：一份完整复现/迁移检验报告和一个可证伪研究循环；说明未解决问题与后续条件。

### QF-W47 · 复现问题、数据差异与预注册

分类：Research；优先级：P1；前置：QF-W28, QF-W34, QF-W40。

选读资源：TSMOM, PBO, DSR（参见 [资源登记](resources.md)）。

产物：`research/replication-plan.md`。

验收：
- [ ] 选择一项先前基线做深入复现/迁移检验，不新增无限策略家族
- [ ] 记录原论文与本实验数据、时期、市场和成本差异
- [ ] 冻结主要结论、试验预算、结果判断与剩余留出信息

独立问答：**你复现的是原论文数字、算法机制，还是在新市场重新检验？**

### QF-W48 · 复现执行与独立核对

分类：Research；优先级：P1；前置：QF-W47。

选读资源：TSMOM, NAUTILUS-BT（参见 [资源登记](resources.md)）。

产物：`reports/replication.md`、`research/replication-artifacts.json`。

验收：
- [ ] 保存数据哈希、代码版本、参数与命令
- [ ] 将关键中间值与独立实现或人工计算核对
- [ ] 负结果、缺数据和运行失败进入报告，不补写未做的测试

独立问答：**别人如何从你的报告复跑同一条权益曲线？**

### QF-W49 · 反证、消融与稳健性边界

分类：Research；优先级：P1；前置：QF-W48。

选读资源：PBO, DSR, ISLP（参见 [资源登记](resources.md)）。

产物：`reports/falsification.md`。

验收：
- [ ] 加入预先约定的时间错位、随机信号或无信息对照
- [ ] 选择少量有机制解释的消融，登记任何新增探索
- [ ] 报告结论成立的范围，不用扰动后最优参数修饰原结果

独立问答：**哪些证据会让你放弃最喜欢的策略解释？**

### QF-W50 · 机器学习只做一次受控增量比较

分类：Experiment；优先级：P1；前置：QF-W07, QF-W17, QF-W47。

选读资源：ISLP, FPP-CV（参见 [资源登记](resources.md)）。

产物：`labs/ml-incremental/`、`reports/ml-vs-baseline.md`。

验收：
- [ ] 在线性/正则化/树模型中选一个，与既有简单基线等预算比较
- [ ] 特征预处理、标签和模型选择严格限制在训练/验证历史
- [ ] 报告费用后与风险约束后的增量；LLM/深度模型仅为后续选修

独立问答：**复杂模型的提升究竟来自新信息、调参预算还是信息泄漏？**

### QF-W51 · 研究报告、反方评审与证据清单

分类：Research；优先级：P1；前置：QF-W50。

选读资源：PBO, DSR（参见 [资源登记](resources.md)）。

产物：`reports/final-research-report.md`、`reports/red-team-review.md`。

验收：
- [ ] 披露所有主要试验、选择过程与未成功结果
- [ ] 把经济解释、统计证据、工程可行性分别评分
- [ ] 反方审查数据泄漏、成本、跨期漂移和风险假设

独立问答：**你的结论能否经受一个专门找漏洞的人复核？**

### QF-W52 · 能力验收与下一轮路线重排

分类：Evaluation；优先级：P0；前置：QF-W51。

选读资源：MIT-FIN, PBO（参见 [资源登记](resources.md)）。

产物：`reports/M8-review.md`、`notes/next-cycle.md`。

验收：
- [ ] 无 AI 代答完成口述、手算与小型独立实现抽测
- [ ] 仅把有证据且本人掌握的项目写入 PROGRESS
- [ ] 基于差距缩减/扩展下轮范围，不自动开启实盘或宣称能靠量化谋生

独立问答：**目前哪些能力已被证明，哪些只是借助工具暂时跑通？**

