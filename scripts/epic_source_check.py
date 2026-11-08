#!/usr/bin/env python3
"""Read-only ELH recovery gate: committed hashes, spans and optional Codex text.

Never writes indices or source text. A regenerated candidate with a different
hash is NOT an exact recovery, even when its headings and counts match.
"""
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import importlib
import json
from pathlib import Path
import re

from source_paths import local_path, resolve_source, sourcebooks_root

REPO = Path(__file__).resolve().parents[1]
FAMILIES = {'epic_spell': ('entries', 70, 70),
            'epic_monster': ('monsters', 64, 50)}


def check_family(family, root=None, codex=None):
    key, count, blocks = FAMILIES[family]
    index = json.loads((REPO / 'reference' / f'{family}_index.json').read_text(encoding='utf-8'))
    path = resolve_source(index['corpus'], root) / local_path(index['source_path'])
    result = {'family': family, 'path': str(path), 'expected_entries': count,
              'expected_blocks': blocks, 'expected_sha256': index['source_sha256'],
              'verified_entries': 0, 'errors': []}
    errors = result['errors']
    if not path.is_file():
        errors.append('source missing')
        return result
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result['actual_sha256'] = digest
    if digest != index['source_sha256']:
        errors.append('SHA-256 mismatch: candidate requires separate source review; keep original indices')
    lines = path.read_text(encoding='utf-8').splitlines()
    mod = importlib.import_module(f'{family}_harvest')
    try:
        live = {row.name: asdict(row) for row in mod.build(lines)}
    except (ValueError, KeyError) as exc:
        errors.append(f'malformed description source: {exc}')
        return result
    rows = index[key]
    if len(rows) != count or set(live) != {row['name'] for row in rows}:
        errors.append('roster mismatch')
    spans = {(row['start'], row['end']) for row in rows}
    if len(spans) != blocks:
        errors.append('shared-block count mismatch')
    expected_full = {}
    for row in rows:
        start, end = row['start'], row['end']
        current = live.get(row['name'], {})
        if any(current.get(field) != row.get(field) for field in
               ('start', 'end', 'description_pages', 'soft')):
            errors.append(f"span/provenance mismatch: {row['name']}")
            continue
        if not 0 <= start < end <= len(lines) or row.get('soft'):
            errors.append(f"invalid span: {row['name']}")
            continue
        name = row.get('description_key') or row['name']
        if mod._name_key(name) not in mod._name_key(lines[start]):
            errors.append(f"heading mismatch: {row['name']}")
            continue
        expected_full[row['name']] = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines[start:end]).strip())
    result['valid_spans'] = len(expected_full)
    if codex is not None:
        attached = [row for row in codex if row.get('fam') == family]
        result['codex_entries'] = len(attached)
        result['codex_with_full_text'] = sum(bool(row.get('full')) for row in attached)
        if Counter(row['name'] for row in attached) != Counter(row['name'] for row in rows):
            errors.append('Codex roster mismatch')
        for row in attached:
            if not row.get('full') or row['full'] != expected_full.get(row['name']):
                errors.append(f"Codex source-slice mismatch: {row['name']}")
    if not errors:
        result['verified_entries'] = len(expected_full)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sourcebooks', type=Path)
    parser.add_argument('--codex-data', type=Path, help='also verify rebuilt epic blocks exactly')
    args = parser.parse_args()
    codex = json.loads(args.codex_data.read_text(encoding='utf-8')) if args.codex_data else None
    results = [check_family(family, sourcebooks_root(args.sourcebooks), codex) for family in FAMILIES]
    print(json.dumps(results, indent=2))
    return 1 if any(row['errors'] for row in results) else 0


if __name__ == '__main__':
    raise SystemExit(main())
