"""Publish this reviewed initial seed through the user's local GitHub CLI."""
from __future__ import annotations
import argparse
import json
import re
import sys
from common import ROOT, CommandError, GitHub, LabError, atomic_json, check_manifest, load_plan, run, validate_plan


def repo_identity(url: str) -> str | None:
    patterns = [r'https://github\.com/([^/]+/[^/]+?)(?:\.git)?/?',
                r'git@github\.com:([^/]+/[^/]+?)(?:\.git)?',
                r'ssh://git@github\.com/([^/]+/[^/]+?)(?:\.git)?']
    for pattern in patterns:
        match = re.fullmatch(pattern, url)
        if match:
            return match.group(1)
    return None


def remote_repo(gh: GitHub, repo: str) -> dict | None:
    try:
        return gh.api(f'repos/{repo}')
    except CommandError as exc:
        # Only a genuine 404 is handled as absent. Authentication/network failures stop.
        if 'HTTP 404' in exc.stderr:
            return None
        raise


def publish(plan: dict, *, visibility: str, with_project: bool) -> dict:
    errors = check_manifest()
    if errors:
        raise LabError('初始包完整性检查失败；此发布脚本仅用于原始初始化包：\n' + '\n'.join(errors))
    run([sys.executable, 'scripts/validate.py'])
    test = run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    print(test.stderr.strip())
    gh = GitHub()
    gh.assert_owner(plan['owner'])
    for setting in ['user.name', 'user.email']:
        result = run(['git', 'config', '--get', setting], check=False)
        if not result.stdout.strip():
            raise LabError(f'请先在本机设置 git {setting}；脚本不会猜测作者身份/邮箱。')
    repo = f"{plan['owner']}/{plan['repository']}"
    url = f'https://github.com/{repo}.git'
    initialized = (ROOT / '.git').exists()
    if initialized:
        actual_root = run(['git', 'rev-parse', '--show-toplevel']).stdout.strip()
        if actual_root != str(ROOT):
            raise LabError('当前 Git 根目录不是初始化包根目录；停止。')
        if run(['git', 'status', '--porcelain']).stdout.strip():
            raise LabError('工作区不干净；请先检查，不自动覆盖或提交学习中的改动。')
        if run(['git', 'branch', '--show-current']).stdout.strip() != 'main':
            raise LabError('当前不在 main；不会自动切换或重写已有分支。')
        origin = run(['git', 'remote', 'get-url', 'origin'], check=False)
        if origin.returncode == 0 and repo_identity(origin.stdout.strip()) != repo:
            raise LabError('origin 不匹配目标仓库；停止，避免误推。')
    else:
        parent_git = run(['git', 'rev-parse', '--show-toplevel'], check=False)
        if parent_git.returncode == 0:
            raise LabError('初始化包位于另一个 Git 工作区内；请移到独立目录再运行。')
    existing = remote_repo(gh, repo)
    if existing:
        if existing.get('archived'):
            raise LabError('同名远端已归档；不修改。')
        # Refuse to take over an unrelated repository. Empty repos are safe to initialize.
        try:
            marker = gh.api(f'repos/{repo}/contents/planning/lab.json')
        except CommandError as exc:
            if 'HTTP 404' not in exc.stderr:
                raise
            branches = gh.all(f'repos/{repo}/branches?per_page=100')
            if branches:
                raise LabError('同名远端非空且缺少 learning-lab 标识；不会接管。')
        else:
            import base64
            identity = json.loads(base64.b64decode(marker['content']))
            if identity.get('kind') != 'futures-learning-lab' or identity.get('owner') != plan['owner']:
                raise LabError('同名远端身份标识不符。')
            if not initialized:
                raise LabError('远端已经初始化；请 clone 远端继续，不能用新 ZIP 覆盖历史。')
        print('使用已有目标仓库；不更改可见性/描述/分支设置。')
    else:
        gh.cli(['repo', 'create', repo, f'--{visibility}', '--description', plan['description']],
               json_output=False, write=True)
        existing = gh.api(f'repos/{repo}')
        if existing.get('full_name', '').lower() != repo.lower():
            raise LabError('新仓库返回身份异常；停止。')
    if not initialized:
        run(['git', 'init', '-b', 'main'])
        manifest = json.loads((ROOT / 'MANIFEST.json').read_text(encoding='utf-8'))
        # Never add arbitrary files or local secrets placed beside the seed.
        run(['git', 'add', '--', *manifest['files'].keys(), 'MANIFEST.json'])
        run(['git', 'commit', '-m', 'Initialize futures learning curriculum and reproducible lab scaffold'])
    origin = run(['git', 'remote', 'get-url', 'origin'], check=False)
    if origin.returncode != 0:
        run(['git', 'remote', 'add', 'origin', url])
    elif repo_identity(origin.stdout.strip()) != repo:
        raise LabError('origin 不匹配目标仓库。')
    # No force push, resets, destructive merges, credential extraction or automatic retries.
    run(['git', 'push', '-u', 'origin', 'main'], timeout=300)
    local_sha = run(['git', 'rev-parse', 'HEAD']).stdout.strip()
    actual = gh.api(f'repos/{repo}/commits/main')
    if actual.get('sha') != local_sha:
        raise LabError('远端 main 与本地提交不一致；停止后续同步。')
    result = {'repository': repo, 'url': f'https://github.com/{repo}', 'commit': local_sha,
              'repository_pushed': True, 'issues_verified': False, 'project_verified': False}
    atomic_json(ROOT / '.local/publish-result.json', result)
    from sync_issues import sync as sync_issues
    issue_result = sync_issues(plan, gh)
    result['issues_verified'] = True
    result['issue_count'] = len(issue_result['issues'])
    atomic_json(ROOT / '.local/publish-result.json', result)
    if with_project:
        from sync_project import sync as sync_project
        result['project'] = sync_project(plan, gh, create=True)
        result['project_verified'] = True
    atomic_json(ROOT / '.local/publish-result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Explicitly allow remote writes')
    parser.add_argument('--visibility', choices=['private', 'public'], default='private')
    parser.add_argument('--with-project', action='store_true')
    args = parser.parse_args()
    try:
        plan = load_plan()
        errors = validate_plan(plan)
        if errors:
            raise LabError('\n'.join(errors))
        print(f"目标：{plan['owner']}/{plan['repository']}；新仓库可见性 {args.visibility}。")
        print('范围：初始文件 + 8 Milestones + 61 Issues；不会操作资金、交易账户或既有其他仓库。')
        print('独立学习 Project：' + ('创建/补齐' if args.with_project else '本次不创建'))
        if not args.apply:
            print('当前是离线预览；未访问 GitHub，尚未创建任何远端资源。')
            return 0
        publish(plan, visibility=args.visibility, with_project=args.with_project)
        return 0
    except (LabError, ValueError, KeyError) as exc:
        print(f'发布停止：{exc}', file=sys.stderr)
        print('远端可能已部分写入；不会删除回滚。参考 INSTALL.md 修复并重跑对应步骤。', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
