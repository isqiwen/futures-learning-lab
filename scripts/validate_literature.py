"""Offline integrity checks for literature identities and replication evidence.

No network requests, PDF checks, learning-state mutations or profit judgments.
"""
from __future__ import annotations

import csv
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

PAPER_FIELDS = (
    'id year authors title track market method priority replicate replication_id '
    'source_url notes verification_status metadata_checked_on metadata_evidence_url '
    'pdf_url pdf_status'
).split()
REPLICATION_FIELDS = (
    'replication_id paper_id phase depends_on title status evidence_path learner_confirmed'
).split()


def read_table(path: Path, fields: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    rows: list[dict[str, str]] = []
    try:
        with path.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream, strict=True)
            header = reader.fieldnames or []
            if len(header) != len(set(header)) or set(header) != set(fields):
                return [], [f'{path.name}: invalid or duplicate CSV columns']
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    errors.append(f'{path.name}:{reader.line_num}: wrong field count')
                else:
                    rows.append({key: value.strip() for key, value in row.items()})
    except (OSError, UnicodeError, csv.Error) as error:
        errors.append(f'{path.name}: cannot read CSV: {error}')
    if not rows and not errors:
        errors.append(f'{path.name}: empty catalog')
    return rows, errors


def is_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return parsed.scheme in {'http', 'https'} and bool(parsed.netloc)
    except ValueError:
        return False


def validate_catalog(root: Path, phases: set[str]) -> list[str]:
    """Validate references, not whether an experiment or paper claim is correct."""
    papers, errors = read_table(root / 'reading/papers_manifest.csv', PAPER_FIELDS)
    runs, run_errors = read_table(root / 'reading/replications.csv', REPLICATION_FIELDS)
    errors += run_errors
    if errors:
        return errors
    paper_index: dict[str, dict[str, str]] = {}
    run_index: dict[str, dict[str, str]] = {}
    for row in papers:
        key = row['id']
        label = f'paper {key}'
        if not re.fullmatch(r'[1-9][0-9]*', key) or key in paper_index:
            errors.append(f'{label}: invalid or duplicate ID')
        paper_index[key] = row
        if not row['title'] or not row['authors'] or not re.fullmatch(r'[12][0-9]{3}', row['year']):
            errors.append(f'{label}: missing title/authors or invalid year')
        if row['priority'] not in {'P0', 'P1', 'P2'}:
            errors.append(f'{label}: invalid priority')
        if row['replicate'] not in {'core', 'optional', 'no'}:
            errors.append(f'{label}: invalid replicate flag')
        if (row['replicate'] == 'core') != bool(row['replication_id']):
            errors.append(f'{label}: core flag and replication ID disagree')
        status = row['verification_status']
        if status not in {'imported_unverified', 'metadata_checked', 'needs_review'}:
            errors.append(f'{label}: invalid verification status')
        if status == 'metadata_checked':
            try:
                date.fromisoformat(row['metadata_checked_on'])
            except ValueError:
                errors.append(f'{label}: checked metadata needs a valid date')
            if not is_url(row['metadata_evidence_url']):
                errors.append(f'{label}: checked metadata needs an evidence URL')
        for field in ('source_url', 'metadata_evidence_url', 'pdf_url'):
            if row[field] and not is_url(row[field]):
                errors.append(f'{label}: invalid {field}')
        if row['pdf_status'] not in {'not_checked', 'candidate'}:
            errors.append(f'{label}: unsupported PDF verification claim')
        if row['pdf_status'] == 'candidate' and not row['pdf_url']:
            errors.append(f'{label}: PDF candidate needs a URL')

    for row in runs:
        key = row['replication_id']
        if not re.fullmatch(r'R[0-9]{2,}', key) or key in run_index:
            errors.append(f'{key}: invalid or duplicate replication ID')
        run_index[key] = row
        if row['phase'] not in phases:
            errors.append(f'{key}: unknown phase')
        if not row['title']:
            errors.append(f'{key}: missing title')
        if row['status'] not in {'not_started', 'in_progress', 'blocked', 'review', 'completed'}:
            errors.append(f'{key}: invalid status')
        if row['learner_confirmed'] not in {'true', 'false'}:
            errors.append(f'{key}: invalid learner confirmation')
        if row['status'] == 'completed' and row['learner_confirmed'] != 'true':
            errors.append(f'{key}: completion requires learner confirmation')
        if row['learner_confirmed'] == 'true' and row['status'] != 'completed':
            errors.append(f'{key}: confirmation is only recorded with completed')
        evidence = row['evidence_path']
        if row['status'] in {'review', 'completed'} and not evidence:
            errors.append(f'{key}: review/completion requires evidence')
        if evidence:
            path = Path(evidence)
            resolved = (root / path).resolve()
            if path.is_absolute() or not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                errors.append(f'{key}: evidence must be an existing file inside the repository')
        paper = paper_index.get(row['paper_id'])
        if not paper or paper['replication_id'] != key or paper['replicate'] != 'core':
            errors.append(f'{key}: paper/replication mapping is not bidirectional')

    for row in papers:
        if row['replication_id']:
            run = run_index.get(row['replication_id'])
            if not run or run['paper_id'] != row['id']:
                errors.append(f"paper {row['id']}: missing or mismatched replication")
    graph: dict[str, list[str]] = {}
    for key, row in run_index.items():
        deps = row['depends_on'].split('|') if row['depends_on'] else []
        graph[key] = deps
        if len(deps) != len(set(deps)) or any(dep not in run_index for dep in deps):
            errors.append(f'{key}: duplicate or unknown dependency')
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(key: str) -> None:
        if key in visiting:
            errors.append(f'{key}: dependency cycle')
            return
        if key in visited:
            return
        visiting.add(key)
        for dep in graph.get(key, []):
            if dep in graph:
                visit(dep)
        visiting.remove(key)
        visited.add(key)

    for key in graph:
        visit(key)
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        plan = json.loads((root / 'planning/plan.json').read_text(encoding='utf-8'))
        phases = {row['id'] for row in plan['phases']}
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'Cannot read phase identities: {error}', file=sys.stderr)
        return 1
    errors = validate_catalog(root, phases)
    if errors:
        print('\n'.join('ERROR: ' + message for message in errors), file=sys.stderr)
        return 1
    print('OK: literature identities, phase/dependency links and evidence fields.')
    print('No remote URLs, PDFs, learning attainment or trading results were verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
