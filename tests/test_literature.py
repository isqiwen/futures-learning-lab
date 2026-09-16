"""Malformed catalogs must not silently relabel evidence or lose references."""
from __future__ import annotations
import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_literature import PAPER_FIELDS, REPLICATION_FIELDS, validate_catalog


class LiteratureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'reading').mkdir()
        self.paper = {field: '' for field in PAPER_FIELDS}
        self.paper.update(id='1', year='2012', authors='Demo Author', title='Synthetic fixture',
                          priority='P0', replicate='core', replication_id='R01',
                          verification_status='imported_unverified', pdf_status='not_checked')
        self.run = dict(replication_id='R01', paper_id='1', phase='M4', depends_on='',
                        title='Synthetic fixture', status='not_started', evidence_path='',
                        learner_confirmed='false')
        self.papers, self.runs = [self.paper], [self.run]

    def write(self):
        for name, fields, rows in [('papers_manifest.csv', PAPER_FIELDS, self.papers),
                                   ('replications.csv', REPLICATION_FIELDS, self.runs)]:
            with (self.root / 'reading' / name).open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)

    def errors(self):
        self.write()
        return validate_catalog(self.root, {'M4', 'M8'})

    def test_valid_unstarted_catalog(self):
        self.assertEqual(self.errors(), [])

    def test_duplicate_paper_rejected(self):
        self.papers.append(dict(self.paper))
        self.assertTrue(self.errors())

    def test_duplicate_replication_rejected(self):
        self.runs.append(dict(self.run))
        self.assertTrue(self.errors())

    def test_wrong_paper_mapping_rejected(self):
        self.run['paper_id'] = '999'
        self.assertTrue(self.errors())

    def test_orphan_core_paper_rejected(self):
        self.paper['replication_id'] = 'R99'
        self.assertTrue(self.errors())

    def test_unknown_phase_rejected(self):
        self.run['phase'] = 'M99'
        self.assertTrue(self.errors())

    def test_unknown_dependency_rejected(self):
        self.run['depends_on'] = 'R99'
        self.assertTrue(self.errors())

    def test_indirect_cycle_rejected(self):
        self.papers.append({**self.paper, 'id': '2', 'replication_id': 'R02'})
        self.runs.append({**self.run, 'replication_id': 'R02', 'paper_id': '2', 'depends_on': 'R01'})
        self.run['depends_on'] = 'R02'
        self.assertTrue(any('cycle' in e for e in self.errors()))

    def test_metadata_claim_needs_date_and_source(self):
        self.paper['verification_status'] = 'metadata_checked'
        self.assertTrue(self.errors())
        self.paper.update(metadata_checked_on='2026-09-16',
                          metadata_evidence_url='https://example.org/publication')
        self.assertEqual(self.errors(), [])

    def test_fake_pdf_verification_rejected(self):
        self.paper['pdf_status'] = 'downloaded'
        self.assertTrue(self.errors())

    def test_completion_needs_confirmation_and_evidence(self):
        self.run['status'] = 'completed'
        self.assertTrue(self.errors())
        self.run['learner_confirmed'] = 'true'
        self.assertTrue(self.errors())
        (self.root / 'report.md').write_text('Synthetic test evidence', encoding='utf-8')
        self.run['evidence_path'] = 'report.md'
        self.assertEqual(self.errors(), [])

    def test_evidence_cannot_escape_repository(self):
        self.run['evidence_path'] = '../outside.md'
        self.assertTrue(self.errors())

    def test_short_or_extra_row_rejected(self):
        self.write()
        path = self.root / 'reading/papers_manifest.csv'
        with path.open('a', encoding='utf-8') as stream:
            stream.write('2,2013,too few fields\n')
        self.assertTrue(validate_catalog(self.root, {'M4'}))

    def test_duplicate_header_rejected(self):
        self.write()
        path = self.root / 'reading/replications.csv'
        path.write_text('replication_id,replication_id\nR01,R01\n', encoding='utf-8')
        self.assertTrue(validate_catalog(self.root, {'M4'}))

    def test_csv_with_quoted_comma_and_newline(self):
        self.paper['title'] = 'A title, with a comma\nand newline'
        self.assertEqual(self.errors(), [])


if __name__ == '__main__':
    unittest.main()
