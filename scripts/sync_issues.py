"""Create missing labels, milestones, and planned issues. Never overwrite progress."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import sys
from common import ROOT, GitHub, LabError, atomic_json, index_issues, issue_body, load_plan, task_specs, validate_plan


def labels_for(task: dict) -> list[str]:
    return [f"phase:{task['phase']}", f"kind:{task['kind']}", f"priority:{task['priority']}"]


def sync(plan: dict, gh: GitHub) -> dict:
    owner, name = plan['owner'], plan['repository']
    gh.assert_owner(owner)
    repo = f'{owner}/{name}'
    gh.api(f'repos/{repo}')  # Explicitly verify access; don't infer from cached mappings.
    tasks = task_specs(plan)
    all_issues = gh.all(f'repos/{repo}/issues?state=all&per_page=100')
    known = index_issues(all_issues)
    wanted_titles = {f"[{t['id']}] {t['title']}": t['id'] for t in tasks}
    for issue in all_issues:
        if 'pull_request' not in issue and issue.get('title') in wanted_titles:
            key = wanted_titles[issue['title']]
            if key not in known:
                raise LabError(f'Issue #{issue["number"]} 标题匹配 {key} 但缺身份标记；先人工核验，不能重复创建。')
    label_rows = gh.all(f'repos/{repo}/labels?per_page=100')
    existing_labels = {x['name'] for x in label_rows}
    wanted_labels = sorted({label for t in tasks for label in labels_for(t)})
    for label in wanted_labels:
        if label not in existing_labels:
            color = '1D76DB' if label.startswith('phase:') else '5319E7' if label.startswith('kind:') else 'D93F0B'
            gh.api(f'repos/{repo}/labels', method='POST', payload={'name': label, 'color': color, 'description': 'Learning plan classification; not completion status'})
    milestone_rows = gh.all(f'repos/{repo}/milestones?state=all&per_page=100')
    milestones = {}
    for p in plan['phases']:
        title = f"{p['id']} · {p['name']}"
        matches = [m for m in milestone_rows if m['title'] == title]
        if len(matches) > 1:
            raise LabError(f'重复 Milestone: {title}')
        if matches:
            milestones[p['id']] = matches[0]
        else:
            milestones[p['id']] = gh.api(f'repos/{repo}/milestones', method='POST', payload={
                'title': title, 'description': f"相对 W{p['start']:02d}–W{p['end']:02d}；无日历截止日。{p['gate']}"})
    created = 0
    for task in tasks:
        key = task['id']
        if key in known:
            print(f'保留 {key} -> #{known[key]["number"]}（不覆盖正文/状态）')
            continue
        payload = {'title': f"[{key}] {task['title']}", 'body': issue_body(task, plan, known), 'labels': labels_for(task)}
        if task['phase'] in milestones:
            payload['milestone'] = milestones[task['phase']]['number']
        row = gh.api(f'repos/{repo}/issues', method='POST', payload=payload)
        if not row.get('number') or not row.get('html_url') or not row.get('node_id'):
            raise LabError(f'{key}: 创建响应缺少标识，停止；重跑前会从远端重新查找。')
        known[key] = row
        created += 1
        print(f'已创建 {key} -> {row["html_url"]}')
    # Re-read all pages and verify that every planned identity exists once.
    known = index_issues(gh.all(f'repos/{repo}/issues?state=all&per_page=100'))
    missing = [t['id'] for t in tasks if t['id'] not in known]
    if missing:
        raise LabError('远端核验缺少任务：' + ', '.join(missing))
    result = {'repository': repo, 'verified_at': datetime.now(timezone.utc).isoformat(), 'created_this_run': created,
              'issues': {t['id']: {k: known[t['id']][k] for k in ['number', 'id', 'node_id', 'html_url']} for t in tasks},
              'milestones': {k: {'number': v['number'], 'html_url': v['html_url']} for k, v in milestones.items()}}
    atomic_json(ROOT / '.local/issue-map.json', result)
    print(f'远端核验通过：{len(tasks)} 个计划 Issues，8 个 Milestones。')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Create missing resources using local gh authentication')
    args = parser.parse_args()
    try:
        plan = load_plan()
        errors = validate_plan(plan)
        if errors:
            raise LabError('\n'.join(errors))
        if not args.apply:
            print(f"预览：目标 {plan['owner']}/{plan['repository']}；创建缺少的 labels、8 Milestones、61 Issues。")
            print('不覆盖已有正文/状态，不创建原生子任务或依赖。当前未访问 GitHub。')
            return 0
        sync(plan, GitHub())
        return 0
    except LabError as exc:
        print(str(exc), file=sys.stderr)
        print('可能已有部分资源写入；不回滚或删除，可修正后重跑，身份标记用于防重复。', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
