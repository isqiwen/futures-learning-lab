"""Initialize only the dedicated learning Project. Preserve existing progress."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import sys
from common import ROOT, GitHub, LabError, atomic_json, index_issues, load_plan, task_specs, validate_plan

PAGE = 'pageInfo { hasNextPage endCursor }'
FIELD_SELECTION = '''nodes { __typename ... on ProjectV2FieldCommon { id name dataType }
... on ProjectV2SingleSelectField { options { id name } } }'''
FIELDS = {
    'Phase': ('SINGLE_SELECT', ['Planning', *[f'M{i}' for i in range(1, 9)]]),
    'Kind': ('SINGLE_SELECT', ['Epic', 'Learning', 'Implementation', 'Experiment', 'Evaluation', 'Research', 'Operations']),
    'Priority': ('SINGLE_SELECT', ['P0', 'P1', 'P2', 'P3']),
    'Effort': ('SINGLE_SELECT', ['S', 'M', 'L', 'XL']),
    'Target': ('TEXT', []),
}


def next_cursor(connection: dict, current: str | None) -> str | None:
    page = connection['pageInfo']
    if not page['hasNextPage']:
        return None
    cursor = page.get('endCursor')
    if not cursor or cursor == current:
        raise LabError('分页游标无效；不能把部分结果视为全部。')
    return cursor


def projects(gh: GitHub, owner: str) -> tuple[str, list[dict]]:
    query = '''query($login:String!, $after:String) { user(login:$login) { id
    projectsV2(first:100, after:$after) { nodes { id number title closed public url }
    pageInfo { hasNextPage endCursor } } } }'''
    rows, cursor, user_id = [], None, None
    while True:
        user = gh.graphql(query, {'login': owner, 'after': cursor})['user']
        if not user:
            raise LabError('未找到目标个人用户。')
        user_id = user['id']
        connection = user['projectsV2']
        rows += connection['nodes']
        cursor = next_cursor(connection, cursor)
        if cursor is None:
            return user_id, rows


def project_fields(gh: GitHub, project_id: str) -> list[dict]:
    query = '''query($id:ID!, $after:String) { node(id:$id) { ... on ProjectV2 {
    fields(first:100, after:$after) { ''' + FIELD_SELECTION + PAGE + ''' } } } }'''
    rows, cursor = [], None
    while True:
        connection = gh.graphql(query, {'id': project_id, 'after': cursor})['node']['fields']
        rows += connection['nodes']
        cursor = next_cursor(connection, cursor)
        if cursor is None:
            return rows


def field_index(rows: list[dict], *, require_all: bool = True) -> dict[str, dict]:
    result = {}
    for name, (kind, options) in FIELDS.items():
        matches = [f for f in rows if f.get('name') == name]
        if len(matches) > 1:
            raise LabError(f'Project 字段重名：{name}')
        if not matches:
            if require_all:
                raise LabError(f'缺少 Project 字段：{name}')
            continue
        field = matches[0]
        if field.get('dataType') != kind:
            raise LabError(f'{name} 的已有字段类型不兼容；不会覆盖。')
        existing = [o['name'] for o in field.get('options', [])]
        if len(existing) != len(set(existing)) or not set(options).issubset(existing):
            raise LabError(f'{name} 的已有选项不兼容；请人工补齐，不会重建字段。')
        result[name] = field
    return result


def project_items(gh: GitHub, project_id: str) -> list[dict]:
    query = '''query($id:ID!, $after:String) { node(id:$id) { ... on ProjectV2 {
    items(first:100, after:$after) { nodes { id isArchived content { ... on Issue { id url } }
    fieldValues(first:100) { nodes {
    ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2FieldCommon { id name } } }
    ... on ProjectV2ItemFieldSingleSelectValue { name optionId field { ... on ProjectV2FieldCommon { id name } } }
    } pageInfo { hasNextPage endCursor } } } pageInfo { hasNextPage endCursor } } } } }'''
    rows, cursor = [], None
    while True:
        connection = gh.graphql(query, {'id': project_id, 'after': cursor})['node']['items']
        for item in connection['nodes']:
            if item['fieldValues']['pageInfo']['hasNextPage']:
                raise LabError('单项字段值超过 100；当前脚本拒绝不完整处理。')
        rows += connection['nodes']
        cursor = next_cursor(connection, cursor)
        if cursor is None:
            return rows


def item_index(rows: list[dict]) -> dict[str, dict]:
    result = {}
    for item in rows:
        content_id = (item.get('content') or {}).get('id')
        if content_id:
            if content_id in result:
                raise LabError('同一个 Issue 在 Project 中出现重复条目；停止。')
            result[content_id] = item
    return result


def blank_updates(task: dict, fields: dict, item: dict) -> list[tuple[str, dict]]:
    """Return only missing values. Status and every existing value are untouched."""
    if item.get('isArchived'):
        return []
    present = {}
    for value in item.get('fieldValues', {}).get('nodes', []):
        field = value.get('field') or {}
        if field.get('id'):
            present[field['id']] = value.get('text') or value.get('optionId') or value.get('name')
    updates = []
    for name in FIELDS:
        field = fields[name]
        if present.get(field['id']):
            continue
        text = task[name.lower()]
        if field['dataType'] == 'TEXT':
            value = {'text': text}
        else:
            options = [o for o in field['options'] if o['name'] == text]
            if len(options) != 1:
                raise LabError(f'{name} 找不到唯一选项：{text}')
            value = {'singleSelectOptionId': options[0]['id']}
        updates.append((field['id'], value))
    return updates


def fill_values(gh: GitHub, project_id: str, item_id: str, updates: list[tuple[str, dict]]) -> None:
    if not updates:
        return
    declarations, mutations, variables = ['$p:ID!', '$i:ID!'], [], {'p': project_id, 'i': item_id}
    for n, (field_id, value) in enumerate(updates):
        declarations += [f'$f{n}:ID!', f'$v{n}:ProjectV2FieldValue!']
        variables.update({f'f{n}': field_id, f'v{n}': value})
        mutations.append(f'm{n}: updateProjectV2ItemFieldValue(input:{{projectId:$p,itemId:$i,fieldId:$f{n},value:$v{n}}}) {{ projectV2Item {{ id }} }}')
    gh.graphql('mutation(' + ','.join(declarations) + ') {' + '\n'.join(mutations) + '}', variables, write=True)


def sync(plan: dict, gh: GitHub, *, create: bool = False, project_number: int | None = None) -> dict:
    owner, repo = plan['owner'], f"{plan['owner']}/{plan['repository']}"
    gh.assert_owner(owner)
    known = index_issues(gh.all(f'repos/{repo}/issues?state=all&per_page=100'))
    tasks = task_specs(plan)
    if any(t['id'] not in known for t in tasks):
        raise LabError('先运行 scripts/sync_issues.py --apply，确保所有任务存在。')
    user_id, rows = projects(gh, owner)
    if project_number is not None:
        matches = [p for p in rows if p['number'] == project_number]
        if len(matches) != 1 or matches[0]['title'] != plan['project_title'] or matches[0]['closed']:
            raise LabError('指定 Project 不存在、已关闭或标题不符；不会改动其他 Project。')
    else:
        matches = [p for p in rows if p['title'] == plan['project_title'] and not p['closed']]
    if len(matches) > 1:
        raise LabError('同名 Project 不唯一，请用 --project-number 显式指定。')
    created = False
    if matches:
        project = matches[0]
    else:
        if not create:
            raise LabError('学习 Project 不存在；显式加入 --create 才允许创建。')
        response = gh.graphql('''mutation($owner:ID!, $title:String!) {
          createProjectV2(input:{ownerId:$owner,title:$title}) {
          projectV2 { id number title closed public url } } }''',
          {'owner': user_id, 'title': plan['project_title']}, write=True)
        project = response['createProjectV2']['projectV2']
        created = True
        if project['public']:
            # Only a newly created Project is made private, never an existing one.
            gh.graphql('''mutation($id:ID!) { updateProjectV2(input:{projectId:$id,public:false}) {
              projectV2 { id public } } }''', {'id': project['id']}, write=True)
    existing = field_index(project_fields(gh, project['id']), require_all=False)
    for name, (kind, options) in FIELDS.items():
        if name in existing:
            continue
        args = ['project', 'field-create', str(project['number']), '--owner', owner,
                '--name', name, '--data-type', kind, '--format', 'json']
        if options:
            args += ['--single-select-options', ','.join(options)]
        gh.cli(args, write=True)
    fields = field_index(project_fields(gh, project['id']))
    indexed = item_index(project_items(gh, project['id']))
    for task in tasks:
        issue = known[task['id']]
        item = indexed.get(issue['node_id'])
        if item is None:
            response = gh.graphql('''mutation($p:ID!, $c:ID!) {
            addProjectV2ItemById(input:{projectId:$p,contentId:$c}) { item { id } } }''',
            {'p': project['id'], 'c': issue['node_id']}, write=True)
            item = {'id': response['addProjectV2ItemById']['item']['id'], 'isArchived': False,
                    'fieldValues': {'nodes': []}}
        updates = blank_updates(task, fields, item)
        fill_values(gh, project['id'], item['id'], updates)
        print(f"{task['id']}: 填充 {len(updates)} 个空字段；保留已有字段/Status/归档。")
    verified = item_index(project_items(gh, project['id']))
    missing = [t['id'] for t in tasks if known[t['id']]['node_id'] not in verified]
    if missing:
        raise LabError('Project 核验缺少：' + ', '.join(missing))
    unfilled = [t['id'] for t in tasks if blank_updates(t, fields, verified[known[t['id']]['node_id']])]
    if unfilled:
        raise LabError('Project 字段核验仍有空值：' + ', '.join(unfilled))
    result = {'number': project['number'], 'id': project['id'], 'url': project['url'], 'created': created,
              'verified_items': len(tasks), 'verified_at': datetime.now(timezone.utc).isoformat()}
    atomic_json(ROOT / '.local/project.json', result)
    print(f"已核验独立学习 Project：{project['url']}。Views/工作流/原生关系没有配置。")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--create', action='store_true')
    parser.add_argument('--project-number', type=int)
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args()
    try:
        plan = load_plan()
        errors = validate_plan(plan)
        if errors:
            raise LabError('\n'.join(errors))
        if not args.apply or args.validate_only:
            print(f"离线预览：仅目标独立 Project {plan['project_title']}；61 Issues，补空字段，不改 Status。")
            print('未访问 GitHub。创建需要 --apply --create 和本机 project scope。')
            return 0
        sync(plan, GitHub(), create=args.create, project_number=args.project_number)
        return 0
    except (LabError, KeyError, ValueError) as exc:
        print(f'Project 同步停止：{exc}。可能已部分写入，修正后重跑，不做删除回滚。', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
