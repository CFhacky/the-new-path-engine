from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reference_audit.py"
SPEC = importlib.util.spec_from_file_location("reference_audit", SCRIPT)
assert SPEC and SPEC.loader
reference_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reference_audit
SPEC.loader.exec_module(reference_audit)


class ReferenceIntegrityTests(unittest.TestCase):
    def test_family_registry_is_complete(self) -> None:
        families = reference_audit.load_manifest()
        self.assertEqual(len(families), 43)
        self.assertEqual(sum(row["expected_count"] for row in families), 18_296)
        self.assertEqual(len({row["id"] for row in families}), 43)
        self.assertEqual(len({row["json"] for row in families}), 43)

    def test_structural_audit_passes(self) -> None:
        errors, summary = reference_audit.structural_audit()
        self.assertEqual(errors, [])
        self.assertEqual(summary["families"], 43)
        self.assertEqual(summary["rows"], 18_296)

    def test_utterance_family_is_explicit(self) -> None:
        families = reference_audit.load_manifest()
        utterance = next(row for row in families if row["id"] == "utterance")
        self.assertEqual(utterance["entry_path"], "sources[].utterances")
        self.assertEqual(utterance["expected_count"], 65)
        self.assertEqual(utterance["scope"], "native")

    def test_prestige_full_text_is_exact_and_bounded(self) -> None:
        data = json.loads(
            (ROOT / "reference" / "prestige_class_index.json").read_text(encoding="utf-8")
        )
        rows = data["prestige_classes"]
        self.assertEqual(len(rows), 145)
        self.assertEqual(data["full_text_prestige_classes"], 16)
        recovered = [row for row in rows if "full_description" in row]
        self.assertEqual(len(recovered), 16)
        self.assertEqual(len(rows) - len(recovered), 129)
        for row in recovered:
            self.assertTrue(row["source_path"].startswith("reference/prestige_fulltext_batch_"))
            source = (ROOT / row["source_path"]).read_text(encoding="utf-8").splitlines()
            exact = "\n".join(source[row["start"]:row["end"]]).strip()
            self.assertEqual(row["full_description"], exact)
            self.assertGreater(len(exact), 4200)
            self.assertIn(row["name"].casefold(), exact[:200].casefold())

    def test_terms_family_uses_normalized_name(self) -> None:
        families = reference_audit.load_manifest()
        terms = next(row for row in families if row["id"] == "terms_and_affixes")
        self.assertEqual(
            terms["json"], "reference/terms_and_affixes_index.json"
        )
        self.assertTrue((ROOT / terms["json"]).is_file())
        self.assertFalse((ROOT / "reference/terms_and_affixes.json").exists())


if __name__ == "__main__":
    unittest.main()
