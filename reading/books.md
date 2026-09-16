# 五本核心书：版本、选读与产出

本页将教材用作实验的配套资料，不把通读全书设为前置条件。书目信息与 Hull 第九版目录按以下出版社页面核对于 2026-09-16；选读顺序和练习是本仓库的学习设计，不是作者的学习要求。

| 编号 | 书与版本 | 本仓库用途 | 配套阶段 |
|---|---|---|---|
| B01 | John C. Hull, *Options, Futures, and Other Derivatives*, **9th Global Edition** | 合约、结算、套保与定价；按当前持有的第九版学习，不要求换购 | M1、M3，风险部分 M6 |
| B02 | Hélyette Geman, *Commodities and Commodity Derivatives: Modeling and Pricing for Agriculturals, Metals and Energy*, **Wiley 2005，第一版** | 库存、便利收益、商品期限结构与产业差异 | M1 选读、M4–M5 深入 |
| B03 | Robert Carver, *Systematic Trading*, **Harriman House 2015，第一版** | 信号、风险缩放、仓位、组合与成本 | M4、M6 |
| B04 | Robert Carver, *Advanced Futures Trading Strategies*, **Harriman House 2023** | 趋势、carry、截面及价差策略的实现参考 | M4、M6，进阶选修 |
| B05 | Marcos López de Prado, *Advances in Financial Machine Learning*, **Wiley 2018，第一版** | 标签、依赖样本、验证、过拟合与金融 ML 实验规范 | M2 先读方法；M8 再结合模型 |

B04 是独立的进阶书，不是 B03 的第二版。书籍出版年份、电子版上架年份和重印年份不能混作新版；笔记记录实际版本和 ISBN。正版纸质、电子或图书馆借阅均可，不要求同时购买两种格式。

## B01：Hull 第九版的准确选章

以下编号对应 [Pearson 第九版 Global Edition 目录](https://www.pearson.com/nl/en_NL/higher-education/subject-catalogue/finance/Options-Futures-and-Other-Derivatives-Hull.html)，全书 36 章。不同地区版、译本或重排电子书需按章名交叉核对，不推测页码。

| 轮次 | 章号与主题 | 阅读任务 |
|---|---|---|
| 第一轮 | 1 Introduction；2 Mechanics of Futures Markets | 第 1 章概览，第 2 章精读；完成合约卡、保证金与逐日结算例子 |
| 第一轮 | 3 Hedging Strategies Using Futures | 解释 basis risk、cross hedge 与 hedge ratio，不将套保等同零风险 |
| 第一轮 | 4 Interest Rates；5 Determination of Forward and Futures Prices | 利率只取贴现与复利基础；精读远期/期货定价，明确现金流和符号 |
| 第一轮选读 | 34 Energy and Commodity Derivatives | 联系库存、仓储、便利收益和不同商品的限制条件 |
| 第二轮 | 23 Estimating Volatilities and Correlations；36 Derivatives Mishaps and What We Can Learn from Them | 支持波动率估计、风险讨论和失败案例；不是直接的交易策略规格 |
| 期权扩展 | 10、11、13、15、18、19 | 期权机制与性质、二叉树、BSM、期货期权、Greeks；需要时读 |

建议顺序：`1 概览 → 2 → 3 → 4 基础 → 5 → 34 选读`。先理解随机过程和风险的基本概念，不要求先掌握全部随机微积分、信用衍生品、复杂利率模型和奇异期权定价。第九版本来就有 OIS 相关内容，不把它误说成后续版本才新增。

**本仓库练习：** 一份有有效日期的合约卡；一个逐日结算核对；一个明确 `basis = spot - futures` 或其他约定的定价例子；解释可交易月份合约与主连续序列的区别。当前手续费与交易权限须另查交易所和期货公司，不能照抄旧教材。

## B02：Geman，解释商品的经济结构

[Wiley 出版社页面，纸质 ISBN 9780470012185](https://www.wiley.com/en-us/Commodities%2Band%2BCommodity%2BDerivatives%3A%2BModeling%2Band%2BPricing%2Bfor%2BAgriculturals%2C%2BMetals%2Band%2BEnergy-p-9780470012185)。优先选读现货/远期/期货、库存和便利收益，再选一个农产品与一个能源或金属主题；不要将某个可储存商品模型无条件推广至所有商品。

**本仓库练习：** 为两类商品画出“供需—库存—现货—期限曲线”的假设链，逐个写出可观察变量、数据发布时间与反例。配 Working、Fama–French；R01/R06/R09 中明确哪些是假设、哪些是真实可得数据。

## B03：Systematic Trading，把信号变为组合

[Harriman House 出版社页面，ISBN 9780857194459](https://www.harriman-house.com/authors/robert-carver/systematic-trading/9780857194459)。按 forecast、风险缩放、仓位、分散化和成本主题阅读。

**本仓库练习：** 对同一信号比较未缩放与事前波动率缩放；单独记录整手取整、资金分母和交易成本影响。配 R04/R08，而不是给每个品种搜索一组最优均线参数。

## B04：Advanced Futures Trading Strategies，连接策略与实验

[Harriman House 出版社页面，ISBN 9780857199683](https://www.harriman-house.com/authors/robert-carver/advanced-futures-trading-strategies/9780857199683)。出版社介绍的是由浅入深的 30 种期货策略；包含趋势、breakout、均值回归和 calendar spreads 等。它不是要求全部实现的任务清单。

理解 B03 的基本概念后，先读趋势和 carry，再结合截面与多策略组合；跨期/跨品种价差留到合约级成本和多腿执行假设清楚后。书中海外历史表现不作为国内收益证据。

**本仓库练习：** 选择一个趋势和一个 carry 例子，写出与 R04/R09 原论文的定义差异。做书籍复现时以书中指定版本为规格；做论文复现时以锁定论文为规格，不能混合后仍宣称忠实复现。快策略必须单独评估频率、流动性、滑点与换手。

## B05：AFML，先学怎样避免错误结论

[Wiley 出版社页面，纸质 ISBN 9781119482086](https://www.wiley.com/en-us/Advances%2Bin%2BFinancial%2BMachine%2BLearning-p-9781119482086)。M2 就可选读标签、样本依赖、验证和多重试验；真正的 ML 模型实验放在 M8。无需等传统策略全部完成才认识数据泄漏。

**本仓库练习：** 画出特征可得区间与标签结束区间，演示重叠标签污染；把 purge 与 embargo 的使用条件写入切分规格。以线性/简单树为对照，不把书中每种技术设为必需，也不把 CV 得分视为实盘批准。

## 使用方法

主线可概括为 `Hull 基础 + Carver 实践`，Geman 随商品问题深入，B04 随策略扩展，AFML 方法贯穿统计与模型验证。不是五本串行通读。

用 [书籍笔记模板](../templates/book-note.md) 记录章节、个人推导、反例、可复跑例子与仍不理解的问题。具体配套论文和时间安排见 [阅读路线](reading_roadmap.md)。
