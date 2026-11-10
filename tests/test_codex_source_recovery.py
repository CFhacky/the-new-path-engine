"""Source resolution and recovery gates, without proprietary fixtures."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'scripts'))
from source_paths import resolve_source
import epic_source_check

spec = importlib.util.spec_from_file_location('codex_recovery_builder', REPO / 'codex/build_codex.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class SourceRecoveryTests(unittest.TestCase):
    def test_windows_provenance_remaps_on_any_host(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'NEW_PATH_SOURCEBOOKS': tmp}):
            expected = Path(tmp) / '_text' / 'D&D 3.5e' / 'DM Toolkits' / 'test.md'
            for corpus in (r'I:\Sourcebooks\_text', r'D:\Backup\I-drive\Sourcebooks\_text'):
                row = {'_corpus': corpus, '_source_path': r'D&D 3.5e\DM Toolkits\test.md'}
                self.assertEqual(Path(builder._exact_source_file(row)), expected)
            self.assertEqual(resolve_source(r'I:\Sourcebooks\_text\D&D 3.5e\DM Toolkits\test.md'), expected)
            # Repo-owned sources retain their provenance and location.
            self.assertEqual(builder._exact_source_file({'_source_path': 'corpus/teatd/vol1.md'}),
                             str(REPO / 'corpus/teatd/vol1.md'))
            builder.configure_sources()
            self.assertEqual(builder.SOURCE_ROOTS[-1], str(Path(tmp) / '_text'))

    def test_wrong_hash_is_not_accepted_even_with_valid_headings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index = json.loads((REPO / 'reference/epic_spell_index.json').read_text())
            target = root / '_text' / Path(index['source_path'].replace('\\', '/'))
            target.parent.mkdir(parents=True)
            target.write_text('AFFLICT [EPIC SPELL DESCRIPTION]\nsynthetic fixture only\n')
            result = epic_source_check.check_family('epic_spell', root)
            self.assertEqual(result['verified_entries'], 0)
            self.assertTrue(any('SHA-256 mismatch' in error for error in result['errors']))

    def test_missing_sources_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            for family in epic_source_check.FAMILIES:
                result = epic_source_check.check_family(family, Path(tmp))
                self.assertEqual(result['errors'], ['source missing'])
                self.assertEqual(result['verified_entries'], 0)

    def test_build_rejects_epic_impostor_and_measures_coverage(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'NEW_PATH_SOURCEBOOKS': tmp}):
            root = Path(tmp)
            ref = root / 'reference'
            ref.mkdir()
            source = root / '_text' / 'fixture.md'
            source.parent.mkdir()
            source.write_text('AFFLICT\nsynthetic body\n')
            fixture = {'corpus': r'I:\Sourcebooks\_text', 'source_path': 'fixture.md',
                       'source_sha256': '0' * 64,
                       'entries': [{'name': 'Afflict', 'book': 'Fixture', 'start': 0, 'end': 2}]}
            (ref / 'epic.json').write_text(json.dumps(fixture))
            families = [{'id': 'epic_spell', 'json': 'reference/epic.json',
                         'entry_path': 'entries', 'expected_count': 1}]
            with patch.object(builder, 'REPO', root), patch.object(builder, 'BUILD', root / 'build'), \
                 patch.object(builder, '_family_specs', return_value=families):
                # Satisfy the unrelated magic-item completeness gate with synthetic rows.
                items = [{'name': f'Item {i}', 'book': 'Fixture', 'special_rules': 'synthetic'}
                         for i in range(1454)]
                (ref / 'items.json').write_text(json.dumps({'entries': items}))
                families.append({'id': 'magic_item', 'json': 'reference/items.json',
                                 'entry_path': 'entries', 'expected_count': 1454})
                builder.build()
                data = json.loads((root / 'build/engine_data.json').read_text())
                self.assertFalse(data[0].get('full'))
                fixture['source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
                (ref / 'epic.json').write_text(json.dumps(fixture))
                builder.build()
                data = json.loads((root / 'build/engine_data.json').read_text())
                self.assertEqual(data[0]['full'], 'AFFLICT\nsynthetic body')
                coverage = json.loads((root / 'build/coverage.json').read_text())
                self.assertEqual(coverage['families']['epic_spell'], {'full': 1, 'total': 1})
                source.unlink()
                decoy = root / '_md' / 'Fixture.md'
                decoy.parent.mkdir()
                decoy.write_text('AFFLICT\nwrong extraction\n')
                builder.build()
                data = json.loads((root / 'build/engine_data.json').read_text())
                self.assertFalse(data[0].get('full'))


if __name__ == '__main__':
    unittest.main()
