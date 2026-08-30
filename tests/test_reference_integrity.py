from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reference_audit.py"
SPEC = importlib.util.spec_from_file_location("reference_audit", SCRIPT)
assert SPEC and SPEC.loader
reference_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reference_audit
SPEC.loader.exec_module(reference_audit)

PRESTIGE_SCRIPT = ROOT / "scripts" / "prestige_class_harvest.py"
PRESTIGE_SPEC = importlib.util.spec_from_file_location(
    "prestige_class_harvest", PRESTIGE_SCRIPT)
assert PRESTIGE_SPEC and PRESTIGE_SPEC.loader
prestige_class_harvest = importlib.util.module_from_spec(PRESTIGE_SPEC)
sys.modules[PRESTIGE_SPEC.name] = prestige_class_harvest
PRESTIGE_SPEC.loader.exec_module(prestige_class_harvest)


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

    def test_prestige_full_text_is_exact_and_complete(self) -> None:
        data = json.loads(
            (ROOT / "reference" / "prestige_class_index.json").read_text(encoding="utf-8")
        )
        rows = data["prestige_classes"]
        self.assertEqual(len(rows), 145)
        self.assertEqual(data["full_text_prestige_classes"], 23)
        recovered = [row for row in rows if "full_description" in row]
        self.assertEqual(len(recovered), 23)
        self.assertEqual(len(rows) - len(recovered), 122)
        for row in rows:
            self.assertGreaterEqual(row["issue"], 274)
            self.assertLessEqual(row["issue"], 353)
            self.assertEqual(
                row["issue_source_key"],
                f'Dragon Magazine/Dragon Magazine #{row["issue"]}.pdf')
        by_name = {row["name"]: row for row in rows}
        self.assertEqual(by_name["Zerth Cenobite"]["issue"], 281)
        self.assertEqual(by_name["Arcanopath Monk"]["issue"], 281)
        self.assertEqual(
            {row["name"] for row in rows if not row["issue_ocr_available"]},
            {"Knight of the Chase", "Master of the Secret Sound"})
        for row in recovered:
            self.assertTrue(row["source_path"].startswith("reference/prestige_fulltext_batch_"))
            source = (ROOT / row["source_path"]).read_text(encoding="utf-8").splitlines()
            exact = "\n".join(source[row["start"]:row["end"]]).strip()
            self.assertEqual(row["full_description"], exact)
            self.assertGreater(len(exact), 0)
            if row["source_path"] != "reference/prestige_fulltext_batch_e.md":
                self.assertGreater(len(exact), 4200)
            self.assertIn(row["name"].casefold(), exact[:200].casefold())

    def test_prestige_source_resolver_uses_manifest_and_peer_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            issue_dir = root / "arbitrary-ocr-output"
            issue_dir.mkdir()
            direct = issue_dir / "Dragon Magazine #274.md"
            fallback = issue_dir / "Dragon Magazine #296.md"
            peer = issue_dir / "Dragon Magazine #295.md"
            for path in (direct, fallback, peer):
                path.write_text("readable issue OCR\n", encoding="utf-8")
            manifest_path = root / "manifest.json"
            manifest = {
                "Dragon Magazine/Dragon Magazine #274.pdf": {
                    "has_text_layer": False, "ocr_status": "done",
                    "ocr_output_md": str(direct)},
                "Dragon Magazine/Dragon Magazine #295.pdf": {
                    "has_text_layer": False, "ocr_status": "done",
                    "ocr_output_md": str(peer)},
                "Dragon Magazine/Dragon Magazine #296.pdf": {
                    "has_text_layer": True, "ocr_status": "skipped_has_text",
                    "ocr_output_md": None},
            }
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            routed = prestige_class_harvest.resolve_issue_source(
                274, manifest_path)
            self.assertEqual(routed.text_source, direct)
            self.assertEqual(routed.route, "manifest_ocr_output")
            routed = prestige_class_harvest.resolve_issue_source(
                296, manifest_path)
            self.assertEqual(routed.text_source, fallback)
            self.assertEqual(routed.route, "peer_output_fallback")

    def test_prestige_source_resolver_rejects_compiled_sparse_export(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            compiled = root / prestige_class_harvest.COMPILED_MARKDOWN_NAME
            compiled.write_text("sparse\n", encoding="utf-8")
            manifest_path = root / "manifest.json"
            manifest_path.write_text(json.dumps({
                "Dragon Magazine/Dragon Magazine #298.pdf": {
                    "has_text_layer": False, "ocr_status": "done",
                    "ocr_output_md": str(compiled)}}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "compiled sparse export"):
                prestige_class_harvest.resolve_issue_source(298, manifest_path)

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
