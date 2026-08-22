from __future__ import annotations

import importlib.util
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "resume_card.py"
SPEC = importlib.util.spec_from_file_location("resume_card", SCRIPT)
assert SPEC and SPEC.loader
resume_card = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = resume_card
SPEC.loader.exec_module(resume_card)


class ResumeCardTests(unittest.TestCase):
    def test_generated_template_is_valid(self) -> None:
        result = resume_card.validate_snapshot(resume_card.render_template("ARIK"))
        self.assertTrue(result.ok, result.errors)

    def test_missing_required_lane_label_fails(self) -> None:
        text = resume_card.render_template("ARIK").replace(
            "**Hard prohibitions.**", "**Warnings.**", 1
        )
        result = resume_card.validate_snapshot(text)
        self.assertFalse(result.ok)
        self.assertTrue(any("Hard prohibitions" in error for error in result.errors))

    def test_authoritative_github_snapshot_fails(self) -> None:
        text = resume_card.render_template("ARIK").replace(
            "authority: NON-AUTHORITATIVE MIRROR", "authority: CURRENT AUTHORITY", 1
        )
        result = resume_card.validate_snapshot(text)
        self.assertFalse(result.ok)

    def test_invalid_date_fails(self) -> None:
        original = resume_card.render_template("ARIK")
        text = re.sub(
            r"snapshot_date: \d{4}-\d{2}-\d{2}",
            "snapshot_date: 2026-13-40",
            original,
            count=1,
        )
        result = resume_card.validate_snapshot(text)
        self.assertFalse(result.ok)


if __name__ == "__main__":
    unittest.main()
