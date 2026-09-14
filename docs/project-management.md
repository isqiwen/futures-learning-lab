# 学习项目管理与安全发布

## 事实与边界

这份 ZIP 已生成本地文件和计划，**不代表远端仓库、Issues、Milestones 或 Project 已创建**。只有本机发布脚本成功返回远端核验结果，才能宣布对应资源存在。GitHub 账户授权、当前工具动作、远端资源状态是三个不同问题。

目标仓库 `isqiwen/futures-learning-lab`；默认新建为私有。独立 Project 名称 `Futures Learning & Research`，不使用 Northstar 量化工程 Project #1，不修改 `LLM Learning & Research`。脚本先分页精确查找同名 Project；重名需要指定编号，标题不一致就停止。已有资源不改变可见性。

## 任务拆分与事实来源

初始化计划共 **61 个 Issues**：1 个管理任务 `QF-GOV`、8 个阶段 Epic `QF-M1`–`QF-M8`、52 个周工作包 `QF-W01`–`QF-W52`。另建 **8 个 GitHub 原生 Milestones**，按阶段归档任务，不设置日历到期日。实际 Issue 编号由 GitHub 分配，不能假定是 #1–#61。

`planning/plan.json` 是可审核的初始化计划与依赖来源；Issue 保存验收、执行讨论和证据；Project 保存实时执行状态；`PROGRESS.md` 只记录本人已经通过的能力验收。不要维护相互冲突的多份完成率。

Issues 正文包含稳定身份标记，用于防重复。重跑只新建缺失条目，不覆盖已有正文、标签、状态或进度，也不重新打开已关闭任务。Milestone/Issue 可能已有人调整，脚本尊重现有安排。Epic 子任务列表和 Depends on 目前是**文本关系**，不是 GitHub 原生 Sub-issues/Dependencies。

周工作包按相对时间组织，不要求所有任务都一周完成。开始实施时，可以把过大的工作包人工拆为更细子任务；不要自动把远期计划都标成 In Progress。

## 字段与看板

| 字段 | 方案 |
|---|---|
| Status | 使用 Project 内置字段；脚本不修改任何 Status |
| Phase | Planning、M1–M8 |
| Kind | Epic / Learning / Implementation / Experiment / Evaluation / Research / Operations |
| Priority | P0 阶段关键；P1 配套；P2 选修；P3 候选；优先级不是就绪状态 |
| Effort | S ≤4h；M 约4–8h；L 约8–16h；XL 应拆分或作为阶段跟踪，不重复计工时 |
| Target | 相对周次/阶段窗口，文本；不是日历截止日期 |

Project 脚本创建缺少字段，将计划 Issues 加入，并且**只填空字段**。已归档条目保持归档；已有字段类型/选项不兼容则停止，不删除重建；不覆盖已有非空值。单条目字段值超过 100 时脚本明确停止，避免静默漏读。

Views、Status 选项、工作流需要在网页手动设置，脚本未配置。建议三个 View 即可：Roadmap（按 Phase 分组的 Table）、Execution（按 Status 分列，排除 Epic）、Research（Experiment/Evaluation/Research）。需要时将 Status 设为 Backlog / Ready / In Progress / Review / Done；默认 Todo / In Progress / Done 也可先使用。

Done 必须有本人解释与证据；CI 通过不自动代表学习任务完成。Epic 不与子任务重复计完成率。每次只推进一个核心实践任务和一个配套阅读/核验任务。

## 授权、执行与故障恢复

详见 [INSTALL.md](../INSTALL.md)。仓库与 Issue 操作使用本机已登录 `gh`；个人 Projects 另需 `project` scope，推送 Actions 工作流通常需相应 workflow 权限。不要把 PAT、Cookie、私钥、`gh auth token` 输出或账户凭据发到聊天或仓库。

离线预览不访问 GitHub。`--apply` 才写入；需要创建 Project 时另显式 `--create`，或者发布使用 `--with-project`。所有分页读取完整后再判断缺失；身份冲突、网络错误、权限不足都停止。写入间有节流；受到速率限制时等待后重跑，不并行启动多份同步脚本。

发布不是跨资源事务。部分失败不会删除成功的资源；`.local/` 记录已核验远端 ID，且不入 Git。仓库推送成功而 Issue 或 Project 失败时，单独重跑相应同步脚本。已有 Issue 的关闭状态不会被重置。

本包执行了本地测试和模拟 API 测试，**未在真实 GitHub 账户上端到端执行写入**。实际 API、账户策略和权限仍需在本机验证。首轮用默认私有仓库，并检查预览内容后再应用。

官方说明：[gh repo create](https://cli.github.com/manual/gh_repo_create)、[gh api](https://cli.github.com/manual/gh_api)、[Projects API](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)。
