# 获取与管理学习仓库

## 已有仓库：从这里开始

`isqiwen/futures-learning-lab` 已有初始化文件；请 clone 后使用正常 Git 流程，不再用 ZIP 创建新历史。

```bash
git clone https://github.com/isqiwen/futures-learning-lab.git
cd futures-learning-lab
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

任务定义入库不等于远端 Issues/Milestones/Project 已创建。补齐它们时先按下文第 2 节检查本机授权，再执行第 4 节的 `sync_issues.py` / `sync_project.py`。下面第 1、3 节保留为原始种子发布说明，不是这个已初始化仓库的下一步。

## 1. 解压与离线检查

把 ZIP 解压到独立目录，例如 `~/Code/learning/futures-learning-lab`。不要解压到 `northstar-quant` 或另一个 Git 仓库内部。需要 Python 3.10+、Git、GitHub CLI；示例及测试仅用 Python 标准库。

```bash
cd ~/Code/learning/futures-learning-lab
python3 --version
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/publish.py --with-project
```

最后一行只预览，不联网、不创建任何资源。**第一次发布前不要修改初始化包内容**；`MANIFEST.json` 会校验要提交的原始文件。发布完成后可以正常学习、修改、提交；此时使用正常 Git 流程，而不是再次运行初始种子发布脚本。

## 2. 检查本机 GitHub 会话

```bash
# 未安装 gh 时才需要
brew install gh

gh auth status
# 尚未登录或身份错误时，通过浏览器登录/切换到 isqiwen
# gh auth login --hostname github.com --web --git-protocol https
# gh auth switch --hostname github.com --user isqiwen

gh auth setup-git --hostname github.com

# 本包含 GitHub Actions；使用 gh OAuth 时补充 workflow scope
# 同时创建学习 Project 则补充 project scope
gh auth refresh --hostname github.com --scopes workflow,project

git config --get user.name
git config --get user.email
```

Git 提交作者名不必等于 macOS 短用户名；沿用本人正确的 Git 配置。没有配置时请用自己的作者名与 GitHub 已验证邮箱/官方 noreply 邮箱设置，脚本不会猜测邮箱。

`gh auth refresh` 针对 gh 保存的 OAuth 登录。环境变量或其他类型令牌不能依靠这条命令自动增加权限；请在本机选择正确登录方式或调整自己的凭据，不上传凭据。组织策略或新仓库权限不足时先解决权限，不在聊天粘贴令牌。

## 3. 一次发布

```bash
python3 scripts/publish.py --apply --with-project
```

实际会：创建**私有** `isqiwen/futures-learning-lab`、使用本机 Git 身份提交初始文件并推送 main、创建缺失分类标签、8 个原生 Milestones 和 61 个 Issues，最后创建/初始化独立 `Futures Learning & Research` Project。

只需要仓库与 Issues、不需要 Project：

```bash
python3 scripts/publish.py --apply
```

确实要新仓库公开时，首次创建命令显式添加 `--visibility public`；已有仓库不会因此改变可见性。Project 新建默认为私有，与仓库可见性独立。发布可能需要数分钟，按顺序运行，不同时开启第二份。

成功后脚本打印**真实远端 URL、提交 SHA 与核验结果**。`.local/publish-result.json`、`.local/issue-map.json` 和可选 `.local/project.json` 保留本机核验记录，默认不入库。没有成功核验输出就不要认为整次发布已经完成。

## 4. 部分失败的恢复

仓库已推送，只是后续 Issues 或 Project 失败时：

```bash
python3 scripts/sync_issues.py             # 离线预览
python3 scripts/sync_issues.py --apply     # 只补缺失任务，保留已有进度
python3 scripts/sync_project.py --apply --create
```

同名 Project 不止一个时，用 `--project-number N` 选择；脚本仍验证标题，不能指定 Northstar/LLM 的其他 Project。网络/速率限制报错时稍后重跑；不要删除所有已建 Issues。

Git 推送因权限失败，保留本地 `.git`，修复 `gh` 授权后重跑发布；不会 force push。同名远端非空但不是本学习仓库时停止，不覆盖。远端已经初始化而当前 ZIP 没有 Git 历史时，应 clone 远端继续，而不是再次推送一份新历史。

极少数在 `git init` 与首个 commit 之间中断的情况，需要先检查 `git status`、确认暂存区只有计划文件，手动完成首个 commit 后再运行。工作区不干净、分支不是 main、origin 不匹配时，发布器会停止，不替你重置或删除文件。

## 5. 创建后只推进第一周

打开 `START_HERE.md` 和 `[QF-W01]` Issue。确认和 LLM 学习共用的时间预算，完成能力诊断、第一份合约卡与手算账本。Project 的初始配置不是学习成果，三个合成演示也不是已通过的个人验收。

## 验证范围

本交付物已做离线计划、路径、代码和模拟 GitHub 行为测试；当前已提交仓库文件，但批量 Issues/Milestones/Project 写入仍需实际执行与核验。初始化脚本不请求金融账户，不拉取受限市场数据，也不含真实柜台发单功能。
