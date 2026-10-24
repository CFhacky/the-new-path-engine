"""Regression tests: Pale Name fiends must survive sourcebook harvesting.
Run with: py -3.14 -m unittest tests.test_pale_name_source_recovery -v
"""
import importlib.util
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("creature_harvest", REPO / "scripts" / "creature_harvest.py")
import sys
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)

class PaleNameSourceRecovery(unittest.TestCase):
    def test_shadow_demon_and_vrock_in_real_corpus(self):
        if not mod.DEFAULT_BESTIARY.is_dir() or not mod.EXTRA_BOOKS[0].is_file():
            self.skipTest("Owned sourcebook extraction is not mounted")
        corpus = mod.Corpus(mod.DEFAULT_BESTIARY)
        vrocks = corpus.find("vrock", book="MM1")
        self.assertEqual(len(vrocks), 1)
        vl, vr = vrocks[0]
        self.assertGreater(vr.end - vr.start, 90)
        self.assertIn("Dance of Ruin", "\n".join(vl[vr.start:vr.end]))
        shadows = corpus.find("shadow demon", book="Book of Vile Darkness")
        self.assertEqual(len(shadows), 1)
        sl, sh = shadows[0]
        self.assertEqual((sh.hit_dice, sh.hp, sh.ac, sh.cr),
                         ("10d8", "45", "22", "8"))
        self.assertEqual(len(sh.description_spans), 2)
        first, second = sh.description_spans
        self.assertIn("2 claws +17", "\n".join(sl[first[0]:first[1]]))
        self.assertIn("Darkness Enhancement",
                      "\n".join(sl[second[0]:second[1]]))
        self.assertNotIn("CHASME", "\n".join(sl[second[0]:second[1]]))

if __name__ == "__main__":
    unittest.main()
