from __future__ import annotations
import contextlib
import copy
from datetime import datetime
from decimal import Decimal as D
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'examples')]
import common
import publish
import sync_issues
import sync_project
from common import LabError, index_issues, issue_body, load_plan, task_specs, validate_plan
from validate import local_link_errors
from ledger_demo import Contract, pnl, illustrative_margin, roll_example
from asof_demo import Observation, select_asof, demo_rows
from selection_bias_demo import run_experiment


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = load_plan()

    def test_plan_valid(self):
        self.assertEqual(validate_plan(self.plan), [])

    def test_count(self):
        self.assertEqual(len(task_specs(self.plan)), 61)
        self.assertEqual(len(self.plan['phases']), 8)
        self.assertEqual(len(self.plan['sources']), 32)

    def test_relative_dates(self):
        self.assertIsNone(self.plan['budget']['start_date'])
        self.assertFalse(self.plan['budget']['confirmed'])

    def test_forward_dependency_rejected(self):
        self.plan['weeks'][0]['depends_on'] = ['QF-W52']
        self.assertTrue(validate_plan(self.plan))

    def test_unknown_source_rejected(self):
        self.plan['weeks'][0]['resources'] = ['nonexistent']
        self.assertTrue(validate_plan(self.plan))

    def test_duplicate_source_rejected(self):
        self.plan['sources'].append(self.plan['sources'][0])
        self.assertTrue(validate_plan(self.plan))

    def test_missing_week_rejected(self):
        self.plan['weeks'].pop()
        self.assertTrue(validate_plan(self.plan))

    def test_wrong_phase_rejected(self):
        self.plan['weeks'][0]['phase'] = 'M8'
        self.assertTrue(validate_plan(self.plan))

    def test_calendar_date_rejected(self):
        self.plan['budget']['start_date'] = '2026-09-14'
        self.assertTrue(validate_plan(self.plan))

    def test_links(self):
        self.assertEqual(local_link_errors(ROOT), [])

    def test_broken_link_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'a.md').write_text('[x](missing.md)')
            self.assertEqual(len(local_link_errors(root)), 1)

    def test_all_issue_bodies_have_identity_and_gate(self):
        for task in task_specs(self.plan):
            body = issue_body(task, self.plan)
            self.assertIn(f'<!-- futures-learning-lab:{task["id"]} -->', body)
            self.assertIn('## 验收标准', body)
            self.assertIn('本人', body)

    def test_identity_skip_pr(self):
        row = {'pull_request': {}, 'number': 1, 'body': '<!-- futures-learning-lab:QF-W01 -->'}
        self.assertEqual(index_issues([row]), {})

    def test_duplicate_identity_stops(self):
        row = {'number': 1, 'body': '<!-- futures-learning-lab:QF-W01 -->'}
        with self.assertRaises(LabError):
            index_issues([row, row])

    def test_multiple_markers_stop(self):
        with self.assertRaises(LabError):
            index_issues([{'body': '<!-- futures-learning-lab:QF-W01 -->\n<!-- futures-learning-lab:QF-W02 -->'}])


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.contract = Contract('DEMO', D('10'), D('0.5'))

    def test_tick_value(self):
        self.assertEqual(self.contract.tick_value, D('5'))

    def test_long(self):
        self.assertEqual(pnl(self.contract, D('100'), D('103'), 2), D('60'))

    def test_short(self):
        self.assertEqual(pnl(self.contract, D('100'), D('97'), -2), D('60'))

    def test_fees_once(self):
        self.assertEqual(pnl(self.contract, D('100'), D('103'), 2, D('6')), D('54'))

    def test_roll_no_phantom_pnl(self):
        data = roll_example()
        self.assertEqual(data['contract_level_gross_pnl'], D('20'))
        self.assertEqual(data['incorrect_spliced_pnl'], D('120'))

    def test_negative_price_supported_for_pnl(self):
        self.assertEqual(pnl(self.contract, D('-2'), D('1'), 1), D('30'))

    def test_quantity_integral(self):
        with self.assertRaises(ValueError):
            pnl(self.contract, D('1'), D('2'), 0.5)

    def test_finite_required(self):
        with self.assertRaises(ValueError):
            pnl(self.contract, D('NaN'), D('2'), 1)

    def test_margin_example(self):
        self.assertEqual(illustrative_margin(D('100'), -2, self.contract, D('0.1')), D('200'))

    def test_invalid_margin(self):
        with self.assertRaises(ValueError):
            illustrative_margin(D('-1'), 2, self.contract, D('0.1'))


class AsOfTests(unittest.TestCase):
    def setUp(self):
        self.rows = demo_rows()
        self.dt = datetime.fromisoformat

    def test_future_revision_excluded(self):
        found = select_asof(self.rows, self.dt('2026-09-02T10:00:00+08:00'))
        self.assertEqual(next(iter(found.values())).value, 100.0)

    def test_latest_available_revision(self):
        found = select_asof(self.rows, self.dt('2026-09-09T10:00:00+08:00'))
        self.assertEqual(next(iter(found.values())).value, 110.0)

    def test_published_not_yet_received_excluded(self):
        self.assertEqual(select_asof(self.rows, self.dt('2026-09-01T09:00:02+08:00')), {})

    def test_equal_availability_included(self):
        self.assertEqual(len(select_asof(self.rows, self.rows[0].received_at)), 1)

    def test_naive_decision_rejected(self):
        with self.assertRaises(ValueError):
            select_asof(self.rows, self.dt('2026-09-09T10:00:00'))

    def test_bad_receipt_rejected(self):
        with self.assertRaises(ValueError):
            Observation('s', 'p', 1.0, self.rows[1].published_at, self.rows[0].received_at, 0)

    def test_conflicting_revision_rejected(self):
        old = self.rows[0]
        conflicting = Observation(old.series, old.period, 7.0, old.published_at, old.received_at, old.revision)
        with self.assertRaises(ValueError):
            select_asof([old, conflicting], self.rows[1].received_at)

    def test_input_order_independent(self):
        time = self.rows[1].received_at
        self.assertEqual(select_asof(self.rows, time), select_asof(self.rows[::-1], time))


class SelectionTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(run_experiment(4, repetitions=3), run_experiment(4, repetitions=3))

    def test_invalid_inputs(self):
        for args in [{'trials': 0}, {'trials': 2, 'samples': 1}, {'trials': 2, 'repetitions': 0}]:
            with self.assertRaises(ValueError):
                run_experiment(**args)

    def test_reports_both_splits(self):
        result = run_experiment(4, repetitions=3)
        self.assertIn('mean_selected_in_sample_score', result)
        self.assertIn('mean_selected_out_of_sample_score', result)


class FakeIssues:
    def __init__(self):
        self.issues, self.labels, self.milestones, self.writes = [], [], [], []

    def assert_owner(self, owner):
        assert owner == 'isqiwen'
        return {'id': 1, 'login': owner}

    def all(self, endpoint):
        source = self.issues if '/issues?' in endpoint else self.labels if '/labels?' in endpoint else self.milestones
        return copy.deepcopy(source)

    def api(self, endpoint, *, method='GET', payload=None):
        if method == 'GET':
            return {'full_name': 'isqiwen/futures-learning-lab'}
        assert method == 'POST', 'updating existing progress is forbidden'
        self.writes.append((endpoint, copy.deepcopy(payload)))
        if endpoint.endswith('/labels'):
            self.labels.append(copy.deepcopy(payload)); return payload
        target = self.issues if endpoint.endswith('/issues') else self.milestones
        number = len(target) + 1
        row = {**copy.deepcopy(payload), 'number': number, 'id': number, 'node_id': f'I{number}',
               'html_url': f'https://example.invalid/{number}', 'state': 'open'}
        target.append(row)
        return copy.deepcopy(row)


class IssueSyncTests(unittest.TestCase):
    def test_first_run_and_idempotent_retry(self):
        fake = FakeIssues()
        with tempfile.TemporaryDirectory() as directory, patch.object(sync_issues, 'ROOT', Path(directory)), contextlib.redirect_stdout(io.StringIO()):
            result = sync_issues.sync(load_plan(), fake)
            self.assertEqual(result['created_this_run'], 61)
            self.assertEqual(len(fake.milestones), 8)
            fake.issues[0]['state'] = 'closed'
            fake.issues[0]['body'] += '\nPersonal notes must survive.'
            before = copy.deepcopy(fake.issues)
            writes = len(fake.writes)
            retry = sync_issues.sync(load_plan(), fake)
            self.assertEqual(retry['created_this_run'], 0)
            self.assertEqual(fake.issues, before)
            self.assertEqual(len(fake.writes), writes)

    def test_title_without_marker_stops(self):
        fake = FakeIssues()
        task = task_specs(load_plan())[0]
        fake.issues = [{'title': f"[{task['id']}] {task['title']}", 'number': 1, 'body': ''}]
        with self.assertRaises(LabError):
            sync_issues.sync(load_plan(), fake)
        self.assertEqual(fake.writes, [])

    def test_pagination_flattens_all_pages(self):
        gh = common.GitHub.__new__(common.GitHub)
        with patch.object(gh, 'api', return_value=[[{'n': 1}], [{'n': 2}]]):
            self.assertEqual(gh.all('endpoint'), [{'n': 1}, {'n': 2}])

    def test_malformed_pagination_stops(self):
        gh = common.GitHub.__new__(common.GitHub)
        with patch.object(gh, 'api', return_value=[{'n': 1}]):
            with self.assertRaises(LabError):
                gh.all('endpoint')


def field_rows():
    rows = []
    for n, (name, (kind, options)) in enumerate(sync_project.FIELDS.items()):
        rows.append({'id': f'F{n}', 'name': name, 'dataType': kind,
                     'options': [{'id': f'O{n}-{i}', 'name': text} for i, text in enumerate(options)]})
    return rows


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.rows = field_rows()
        self.fields = sync_project.field_index(self.rows)
        self.task = task_specs(load_plan())[0]

    def test_only_five_custom_fields(self):
        updates = sync_project.blank_updates(self.task, self.fields, {'fieldValues': {'nodes': []}})
        self.assertEqual(len(updates), 5)
        self.assertNotIn('Status', sync_project.FIELDS)

    def test_keep_existing_nonempty_field(self):
        field = self.fields['Target']
        item = {'fieldValues': {'nodes': [{'field': {'id': field['id']}, 'text': 'Learner changed target'}]}}
        updates = sync_project.blank_updates(self.task, self.fields, item)
        self.assertNotIn(field['id'], [i for i, _ in updates])

    def test_archived_untouched(self):
        self.assertEqual(sync_project.blank_updates(self.task, self.fields, {'isArchived': True}), [])

    def test_incompatible_field_stops(self):
        self.rows[0]['dataType'] = 'TEXT'
        with self.assertRaises(LabError):
            sync_project.field_index(self.rows)

    def test_missing_option_stops(self):
        self.rows[0]['options'] = []
        with self.assertRaises(LabError):
            sync_project.field_index(self.rows)

    def test_duplicate_item_stops(self):
        item = {'id': '1', 'content': {'id': 'Issue1'}}
        with self.assertRaises(LabError):
            sync_project.item_index([item, item])

    def test_invalid_pagination_stops(self):
        with self.assertRaises(LabError):
            sync_project.next_cursor({'pageInfo': {'hasNextPage': True, 'endCursor': None}}, None)

    def test_existing_falsey_field_gets_value(self):
        field = self.fields['Target']
        item = {'fieldValues': {'nodes': [{'field': {'id': field['id']}, 'text': ''}]}}
        self.assertEqual(len(sync_project.blank_updates(self.task, self.fields, item)), 5)


class PublishSafetyTests(unittest.TestCase):
    def test_expected_git_urls(self):
        for url in ['https://github.com/isqiwen/futures-learning-lab.git',
                    'git@github.com:isqiwen/futures-learning-lab.git',
                    'ssh://git@github.com/isqiwen/futures-learning-lab.git']:
            self.assertEqual(publish.repo_identity(url), 'isqiwen/futures-learning-lab')

    def test_untrusted_git_host(self):
        self.assertIsNone(publish.repo_identity('https://github.com.evil.invalid/isqiwen/repo.git'))

    def test_token_redaction(self):
        exc = common.CommandError(['gh', 'api', 'x'], 1, 'oops ghp_SecretStringHere')
        self.assertNotIn('SecretStringHere', str(exc))

    def test_manifest_tamper_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'a.txt').write_text('original')
            manifest = {'files': {'a.txt': hashlib.sha256(b'original').hexdigest()}}
            (root/'MANIFEST.json').write_text(json.dumps(manifest))
            self.assertEqual(common.check_manifest(root), [])
            (root/'a.txt').write_text('modified')
            self.assertTrue(common.check_manifest(root))

    def test_manifest_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'MANIFEST.json').write_text(json.dumps({'files': {'../escape': 'x'}}))
            self.assertTrue(common.check_manifest(root))

    def test_offline_preview_no_gh_required(self):
        for script in ['publish.py', 'sync_issues.py', 'sync_project.py']:
            result = subprocess.run([sys.executable, str(ROOT/'scripts'/script)], capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('未访问 GitHub', result.stdout)


if __name__ == '__main__':
    unittest.main()
