"""Deterministic fake-transport integration tests; not live API schema validation."""
from __future__ import annotations
import contextlib
import copy
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from common import LabError, issue_body, load_plan, task_specs
import sync_project


class FakeProject:
    def __init__(self):
        self.plan = load_plan()
        self.issues = [{'number': n, 'node_id': f'ISSUE{n}', 'body': issue_body(t, self.plan),
                        'html_url': f'https://example.invalid/issues/{n}'}
                       for n, t in enumerate(task_specs(self.plan), 1)]
        self.project = None
        self.fields = []
        self.items = []
        self.writes = 0

    def assert_owner(self, owner):
        assert owner == 'isqiwen'

    def all(self, endpoint):
        assert '/issues?' in endpoint
        return copy.deepcopy(self.issues)

    @staticmethod
    def page(rows):
        return {'nodes': copy.deepcopy(rows), 'pageInfo': {'hasNextPage': False, 'endCursor': None}}

    def graphql(self, query, variables=None, *, write=False):
        v = variables or {}
        if write:
            self.writes += 1
        if 'projectsV2(first' in query:
            return {'user': {'id': 'USER', 'projectsV2': self.page([self.project] if self.project else [])}}
        if 'createProjectV2(' in query:
            self.project = {'id': 'PROJECT', 'title': self.plan['project_title'], 'number': 5,
                            'closed': False, 'public': False, 'url': 'https://example.invalid/projects/5'}
            return {'createProjectV2': {'projectV2': copy.deepcopy(self.project)}}
        if 'fields(first' in query:
            return {'node': {'fields': self.page(self.fields)}}
        if 'items(first' in query:
            return {'node': {'items': self.page(self.items)}}
        if 'addProjectV2ItemById' in query:
            item = {'id': f"ITEM{len(self.items)+1}", 'isArchived': False,
                    'content': {'id': v['c']}, 'fieldValues': self.page([])}
            self.items.append(item)
            return {'addProjectV2ItemById': {'item': {'id': item['id']}}}
        if 'updateProjectV2ItemFieldValue' in query:
            item = next(x for x in self.items if x['id'] == v['i'])
            for name, field_id in v.items():
                if not name.startswith('f'):
                    continue
                value = v['v' + name[1:]]
                field = next(x for x in self.fields if x['id'] == field_id)
                if 'text' in value:
                    row = {'text': value['text'], 'field': {'id': field_id, 'name': field['name']}}
                else:
                    option = next(x for x in field['options'] if x['id'] == value['singleSelectOptionId'])
                    row = {'name': option['name'], 'optionId': option['id'], 'field': {'id': field_id, 'name': field['name']}}
                item['fieldValues']['nodes'].append(row)
            return {'m0': {'projectV2Item': {'id': item['id']}}}
        raise AssertionError(query)

    def cli(self, args, *, json_output=True, write=False):
        assert args[:2] == ['project', 'field-create']
        self.writes += 1
        name, kind = args[args.index('--name')+1], args[args.index('--data-type')+1]
        options = args[args.index('--single-select-options')+1].split(',') if '--single-select-options' in args else []
        field = {'id': f'FIELD{len(self.fields)+1}', 'name': name, 'dataType': kind,
                 'options': [{'id': f'{name}{n}', 'name': o} for n, o in enumerate(options)]}
        self.fields.append(field)
        return field


class IntegrationTests(unittest.TestCase):
    def test_full_sync_and_non_destructive_retry(self):
        fake = FakeProject()
        with tempfile.TemporaryDirectory() as directory, patch.object(sync_project, 'ROOT', Path(directory)), contextlib.redirect_stdout(io.StringIO()):
            first = sync_project.sync(load_plan(), fake, create=True)
            self.assertTrue(first['created'])
            self.assertEqual(len(fake.items), 61)
            self.assertEqual(len(fake.fields), 5)
            fake.items[0]['isArchived'] = True
            fake.items[1]['fieldValues']['nodes'].append({'field': {'id': 'STATUS'}, 'name': 'In Progress', 'optionId': 'CURRENT'})
            before = copy.deepcopy(fake.items)
            writes = fake.writes
            second = sync_project.sync(load_plan(), fake, create=True)
            self.assertFalse(second['created'])
            self.assertEqual(fake.items, before)
            self.assertEqual(fake.writes, writes)

    def test_project_not_created_without_explicit_flag(self):
        fake = FakeProject()
        with self.assertRaises(LabError):
            sync_project.sync(load_plan(), fake)
        self.assertEqual(fake.writes, 0)

    def test_wrong_project_number_never_touches_another_board(self):
        fake = FakeProject()
        fake.project = {'id': 'OTHER', 'number': 1, 'title': 'Northstar Quant', 'closed': False, 'public': False, 'url': 'https://example.invalid/1'}
        with self.assertRaises(LabError):
            sync_project.sync(load_plan(), fake, project_number=1)
        self.assertEqual(fake.writes, 0)


if __name__ == '__main__':
    unittest.main()
