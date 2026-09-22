import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from d2_equipment_engine import (  # noqa: E402
    CoreEquipSlot,
    Durability,
    EquipmentItem,
    EquipmentState,
    ItemQuality,
    Property,
    Requirement,
    RunewordDefinition,
    SetDefinition,
    SocketInsert,
)


class D2EquipmentEngineTests(unittest.TestCase):
    def test_source_enum_values_are_preserved(self):
        self.assertEqual(ItemQuality.INFERIOR.value, 0x01)
        self.assertEqual(ItemQuality.TEMPERED.value, 0x09)
        self.assertEqual(CoreEquipSlot.HEAD.value, 1)
        self.assertEqual(CoreEquipSlot.GLOVES.value, 10)
        self.assertEqual(CoreEquipSlot.ALT_LEFT_ARM.value, 12)

    def test_multislot_extension_and_replace(self):
        state = EquipmentState()
        shoulders = EquipmentItem(
            id="paired",
            name="Paired Spaulders",
            item_type="armor",
            slots=("RIGHT_SHOULDER", "LEFT_SHOULDER"),
        )
        right = EquipmentItem(
            id="right",
            name="Right Guard",
            item_type="armor",
            slots=("RIGHT_SHOULDER",),
        )
        state.register_item(shoulders)
        state.register_item(right)
        state.equip("paired", level=1, stats={})
        with self.assertRaises(ValueError):
            state.equip("right", level=1, stats={})
        displaced = state.equip("right", level=1, stats={}, replace=True)
        self.assertEqual(displaced, ["paired"])
        self.assertEqual(state.paperdoll(), {"RIGHT_SHOULDER": "right"})

    def test_requirements_include_new_path_tags(self):
        item = EquipmentItem(
            id="bonded",
            name="Bonded Guard",
            item_type="armor",
            slots=("NECK",),
            requirements=Requirement(
                min_level=10,
                min_stats={"STR": 15},
                required_tags=frozenset({"artifact-bond"}),
            ),
        )
        state = EquipmentState()
        state.register_item(item)
        with self.assertRaises(ValueError):
            state.equip("bonded", level=9, stats={"STR": 20}, tags={"artifact-bond"})
        state.equip("bonded", level=10, stats={"STR": 15}, tags={"artifact-bond"})
        self.assertEqual(state.paperdoll()["NECK"], "bonded")

    def test_broken_item_suppresses_properties_and_set_count(self):
        state = EquipmentState()
        p = Property("guard", 1)
        item = EquipmentItem(
            id="a",
            name="Guard",
            item_type="armor",
            quality=ItemQuality.SET,
            slots=("RIGHT_SHOULDER",),
            durability=Durability(2, 2),
            properties=(p,),
            set_id="set-a",
        )
        state.register_set(SetDefinition("set-a", "Set A", frozenset({"a"})))
        state.register_item(item)
        state.equip("a", level=1, stats={})
        self.assertEqual(state.set_counts(), {"set-a": 1})
        self.assertEqual([x.code for x in state.active_properties()], ["guard"])
        state.damage_item("a", 2)
        self.assertTrue(item.broken)
        self.assertEqual(state.set_counts(), {})
        self.assertEqual(state.active_properties(), [])
        state.repair_item("a")
        self.assertFalse(item.broken)
        self.assertEqual(state.set_counts(), {"set-a": 1})

    def test_piece_partial_and_set_wide_bonuses_layer(self):
        state = EquipmentState()
        p1 = Property("piece-base", 1)
        p2 = Property("piece-at-2", 1)
        s2 = Property("set-at-2", 1)
        sf = Property("set-full", 1)
        definition = SetDefinition(
            "regalia",
            "Regalia",
            frozenset({"left", "right"}),
            partial_properties={2: (s2,)},
            full_properties=(sf,),
        )
        left = EquipmentItem(
            id="left",
            name="Left",
            item_type="armor",
            quality=ItemQuality.SET,
            slots=("LEFT_SHOULDER",),
            properties=(p1,),
            set_id="regalia",
            item_partial_set_properties={2: (p2,)},
        )
        right = EquipmentItem(
            id="right",
            name="Right",
            item_type="armor",
            quality=ItemQuality.SET,
            slots=("RIGHT_SHOULDER",),
            set_id="regalia",
        )
        state.register_set(definition)
        state.register_item(left)
        state.register_item(right)
        state.equip("left", level=1, stats={})
        self.assertEqual([x.code for x in state.active_properties()], ["piece-base"])
        state.equip("right", level=1, stats={})
        codes = [x.code for x in state.active_properties()]
        self.assertEqual(codes, ["piece-base", "piece-at-2", "set-at-2", "set-full"])

    def test_socket_order_controls_runeword(self):
        state = EquipmentState()
        rw = RunewordDefinition(
            id="ral-ort-tal",
            name="Test Word",
            ordered_runes=("r08", "r09", "r07"),
            eligible_item_types=frozenset({"shield"}),
            properties=(Property("res-all", 13),),
        )
        state.register_runeword(rw)
        host = EquipmentItem(
            id="host",
            name="Host Shield",
            item_type="shield",
            slots=("LEFT_ARM",),
            socket_capacity=3,
        )
        state.register_item(host)
        for rune in ("r08", "r09", "r07"):
            host.socket(SocketInsert(id=rune, code=rune))
        resolved = host.resolve_runeword(state.runewords.values())
        self.assertIsNotNone(resolved)
        self.assertEqual(host.runeword_id, "ral-ort-tal")
        state.equip("host", level=1, stats={})
        self.assertEqual([x.code for x in state.active_properties()], ["res-all"])


if __name__ == "__main__":
    unittest.main()
