"""The built-place path through realm_map.py.

A suffered realm is rolled whole and re-rolled on every entry. A built one is
read from its definition file and only its new work is thrown for. These tests
cover the second case: a grammar the file supplies, areas and adjacencies the
resolver refuses to invent, an anchor that suppresses the psychotecture seeds,
the named faces that break that anchor, and a growth pass that leaves every
existing area, edge and the law roll exactly where they were.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import tempfile
import types
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "realm_map.py"
SPEC = importlib.util.spec_from_file_location("realm_map", SCRIPT)
assert SPEC and SPEC.loader
realm_map = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = realm_map
SPEC.loader.exec_module(realm_map)


def definition(**over):
    """A minimal built place: three fixed areas, two fixed adjacencies."""
    d = {
        "name": "Test built place",
        "archetype": "composite-city",
        "label": "CAMPAIGN-ORIGINAL",
        "facts": ["A fact, quoted from somewhere that is not this engine."],
        "law": {"referent": "an anchor", "citation": "a page", "rule": "The ground does not lie."},
        "anchored": True,
        "grammar": {
            "layout": "lemniscate",
            "law": {str(i): f"law face {i}" for i in range(1, 7)},
            "hazards": {str(i): f"hazard face {i}" for i in range(1, 7)},
        },
        "fixed_areas": [
            {"name": "The waist", "dimensions": "80 acres", "cluster": "waist", "role": "the crossing"},
            {"name": "West thing", "dimensions": "280 acres", "cluster": "west"},
            {"name": "East thing", "dimensions": "280 acres", "cluster": "east", "note": "a canon note"},
        ],
        "fixed_edges": [[1, 2, "intersection"], [1, 3, "conjunction"]],
        "growth": {
            "die": "d6",
            "interval": "one year",
            "frontier": "the circuit",
            "edges": ["intersection", "conjunction", "oblique"],
            "anchored": True,
            "unanchored_faces": [2],
            "attach_to": [2, 3],
            "kinds": {"1": ["Ordinary plot", "5 acres"], "2": ["The anomaly", "5 acres nobody agrees about"]},
        },
        "never_roll": ["the three areas above"],
    }
    d.update(over)
    return d


class Args:
    def __init__(self, **kw):
        self.realm = None
        self.realm_file = None
        self.areas = "d8"
        self.band = 2
        self.entry = ""
        self.force = True
        self.plots = None
        self.label = None
        for k, v in kw.items():
            setattr(self, k, v)


class BuiltPlaceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        self.state = str(self.dir / "t.realm.state.json")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, d):
        p = self.dir / "t.realm.json"
        p.write_text(json.dumps(d), encoding="utf-8")
        return str(p)

    def build(self, d=None):
        path = self.write(d or definition())
        realm_map.cmd_new(self.state, Args(realm_file=path))
        return json.loads(pathlib.Path(self.state).read_text(encoding="utf-8"))

    # ---------------------------------------------------------------- reading
    def test_fixed_areas_and_edges_are_read_not_rolled(self):
        st = self.build()
        self.assertEqual(len(st["areas"]), 3)
        self.assertEqual([a["kind"] for a in st["areas"]], ["The waist", "West thing", "East thing"])
        self.assertTrue(all(a["fixed"] for a in st["areas"]))
        self.assertEqual([list(e) for e in st["edges"]], [[1, 2, "intersection"], [1, 3, "conjunction"]])
        ledger = "\n".join(st["ledger"])
        self.assertIn("area count NOT ROLLED", ledger)
        self.assertIn("edges NOT ROLLED", ledger)
        # the only die thrown for a fully fixed place is the law
        self.assertEqual(sum(1 for line in st["ledger"] if line.lstrip().startswith("d")), 1)

    def test_refusals_reach_the_ledger_and_the_sheet(self):
        st = self.build()
        self.assertIn("REFUSED", "\n".join(st["ledger"]))
        sheet = realm_map.render_sheet(st)
        self.assertIn("What this folio refuses to roll", sheet)
        self.assertIn("the three areas above", sheet)

    def test_file_grammar_overrides_the_archetype_tables(self):
        st = self.build()
        self.assertEqual(realm_map.gram(st)["law"][st["law"]], f"law face {st['law']}")
        self.assertEqual(st["layout"], "lemniscate")
        sheet = realm_map.render_sheet(st)
        self.assertIn("in its own vocabulary", sheet)

    def test_campaign_labels_survive_into_the_drawing(self):
        svg = realm_map.render_svg(self.build())
        self.assertIn("LAW (CAMPAIGN-RULING", svg)
        self.assertIn("facts CAMPAIGN-ORIGINAL", svg)
        self.assertIn("READ from the definition file", svg)

    def test_lemniscate_puts_the_lobes_either_side_of_the_waist(self):
        st = self.build()
        pos = realm_map._positions("lemniscate", 3, 1200, 820,
                                   [a["cluster"] for a in st["areas"]])
        waist_x, west_x, east_x = pos[0][0], pos[1][0], pos[2][0]
        self.assertLess(west_x, waist_x)
        self.assertGreater(east_x, waist_x)

    # ---------------------------------------------------------------- anchor
    def test_anchor_suppresses_the_psychotecture_seeds(self):
        d = definition()
        d["fixed_areas"] = []          # roll the areas so the suppression is visible
        d["fixed_edges"] = []
        st = self.build(d)
        self.assertTrue(all(a["contradiction"] == 1 for a in st["areas"]))
        self.assertIn("contradiction NOT ROLLED", "\n".join(st["ledger"]))
        self.assertTrue(all(realm_map.CONTRADICTION[a["contradiction"]] is None for a in st["areas"]))

    def test_an_unanchored_realm_still_rolls_contradictions(self):
        d = definition()
        d["anchored"] = False
        d["fixed_areas"] = []
        d["fixed_edges"] = []
        st = self.build(d)
        self.assertIn("psychotecture contradiction", "\n".join(st["ledger"]))

    # ---------------------------------------------------------------- growth
    def test_growth_appends_and_disturbs_nothing(self):
        st = self.build()
        before_areas = json.dumps(st["areas"])
        before_edges = json.dumps(st["edges"])
        before_law = st["law"]
        realm_map.cmd_grow(self.state, Args(label="one year"))
        after = json.loads(pathlib.Path(self.state).read_text(encoding="utf-8"))
        self.assertEqual(json.dumps(after["areas"][:3]), before_areas)
        self.assertEqual(json.dumps(after["edges"][:2]), before_edges)
        self.assertEqual(after["law"], before_law)
        self.assertGreater(len(after["areas"]), 3)
        for a in after["areas"][3:]:
            self.assertEqual(a["grown"], "one year")
            self.assertFalse(a["fixed"])
            self.assertIn(a["kind"], ("Ordinary plot", "The anomaly"))
        self.assertEqual(after["growth_log"][0]["interval"], "one year")

    def test_new_work_joins_only_the_declared_frontier_and_takes_its_cluster(self):
        self.build()
        realm_map.cmd_grow(self.state, Args())
        after = json.loads(pathlib.Path(self.state).read_text(encoding="utf-8"))
        hosts = {e[0] for e in after["edges"][2:]}
        self.assertTrue(hosts.issubset({2, 3}), f"new work joined {hosts}, outside attach_to")
        by_n = {a["n"]: a for a in after["areas"]}
        for host, new, kind in after["edges"][2:]:
            self.assertEqual(by_n[new]["cluster"], by_n[host]["cluster"])
            self.assertIn(kind, ("intersection", "conjunction", "oblique"))

    def test_named_growth_faces_break_the_anchor(self):
        d = definition()
        d["growth"]["kinds"] = {"1": ["The anomaly", "5 acres nobody agrees about"]}
        d["growth"]["unanchored_faces"] = [1]
        self.build(d)
        realm_map.cmd_grow(self.state, Args())
        after = json.loads(pathlib.Path(self.state).read_text(encoding="utf-8"))
        grown = after["areas"][3:]
        self.assertTrue(grown)
        self.assertTrue(all(not a["anchored"] for a in grown))
        self.assertIn("the anchor does not cover this plot", "\n".join(after["ledger"]))

    def test_the_cap_stops_building_past_the_ground(self):
        d = definition()
        d["growth"]["max_areas"] = 4
        d["growth"]["die"] = "d12"
        self.build(d)
        realm_map.cmd_grow(self.state, Args())
        after = json.loads(pathlib.Path(self.state).read_text(encoding="utf-8"))
        self.assertLessEqual(len(after["areas"]), 4)
        self.assertIn("CAP:", "\n".join(after["ledger"]))

    def test_a_realm_with_no_growth_block_refuses_to_grow(self):
        d = definition()
        d.pop("growth")
        self.build(d)
        with self.assertRaises(SystemExit):
            realm_map.cmd_grow(self.state, Args())

    # ---------------------------------------------------------------- guards
    def test_bad_definition_files_are_refused(self):
        cases = {
            "gappy grammar": {"grammar": {"law": {"1": "a", "3": "c"}}},
            "fixed area with no dimensions": {"fixed_areas": [{"name": "x"}]},
            "edge type outside the vocabulary": {"fixed_edges": [[1, 2, "bridge"]]},
            "edges with no fixed areas": {"fixed_areas": [], "fixed_edges": [[1, 2, "angle"]]},
            "growth with no kinds": {"growth": {"die": "d6"}},
            "unanchored face outside the kinds table": {
                "growth": {"kinds": {"1": ["a", "b"]}, "unanchored_faces": [9]}},
            "attach_to that is not an area number": {
                "growth": {"kinds": {"1": ["a", "b"]}, "attach_to": ["the docks"]}},
        }
        for why, over in cases.items():
            with self.subTest(why=why):
                path = self.write(definition(**over))
                with self.assertRaises(SystemExit):
                    realm_map.load_realm_file(path)

    def test_fixed_edges_cannot_point_past_the_last_area(self):
        d = definition()
        d["fixed_edges"] = [[1, 9, "intersection"]]
        with self.assertRaises(SystemExit):
            realm_map.cmd_new(self.state, Args(realm_file=self.write(d)))

    def test_the_shipped_selftest_still_passes(self):
        self.assertEqual(realm_map.selftest(), 0)


if __name__ == "__main__":
    unittest.main()
