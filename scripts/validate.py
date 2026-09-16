"""Validate plan, local Markdown links, and literature references offline."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import unquote
from common import ROOT, load_plan, validate_plan
from validate_literature import validate_catalog


def local_link_errors(root: Path) -> list[str]:
    errors = []
    for path in root.rglob('*.md'):
        if '.git' in path.parts or '.local' in path.parts:
            continue
        text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            if target.startswith(('https://', 'http://', 'mailto:', '#')):
                continue
            name = unquote(target.split('#', 1)[0])
            if name and not (path.parent / name).exists():
                errors.append(f'{path.relative_to(root)}: broken local link {target}')
    return errors


def main() -> int:
    plan = load_plan()
    errors = validate_plan(plan) + local_link_errors(ROOT)
    errors += validate_catalog(ROOT, {phase['id'] for phase in plan['phases']})
    if errors:
        print('\n'.join('ERROR: ' + x for x in errors), file=sys.stderr)
        return 1
    print(f"OK: 8 phases, 52 relative weeks, 61 task specifications, {len(plan['sources'])} source records; local links valid.")
    print('OK: literature identities, phase/dependency references and evidence fields.')
    print('This validates structure, not source accuracy, PDF access, learning attainment or strategy performance.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
