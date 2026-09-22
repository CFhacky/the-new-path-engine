#!/usr/bin/env python3
"""D2-derived equipment/paperdoll substrate for The New Path.

SOURCE-DERIVED:
- Quality enum, core equipped slots, item state, durability, sockets, set-piece
  partial bonuses, set-wide partial/full bonuses, ordered runeword recipes.
- Upstream pin: reference/d2_equipment_upstream_manifest.json.

NEW-PATH EXTENSIONS:
- Arbitrary/multi-slot occupancy beyond D2's core paperdoll.
- Tag-based requirements (lineage, form, attunement, artifact state, etc.).
- Broken-item suppression as a tabletop runtime state.
- System-neutral properties whose terminal arithmetic is translated elsewhere.

This module deliberately does NOT convert D2 Defense directly into 3.5e AC or
GURPS DR. It owns equipment truth; translator layers own system expression.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Iterable, Mapping


class ItemQuality(IntEnum):
    UNKNOWN = 0
    INFERIOR = 0x01
    NORMAL = 0x02
    SUPERIOR = 0x03
    MAGIC = 0x04
    SET = 0x05
    RARE = 0x06
    UNIQUE = 0x07
    CRAFTED = 0x08
    TEMPERED = 0x09


class ItemLocation(IntEnum):
    STORED = 0x00
    EQUIPPED = 0x01
    BELT = 0x02
    BUFFER = 0x04
    SOCKET = 0x06


class CoreEquipSlot(IntEnum):
    NONE = 0
    HEAD = 1
    NECK = 2
    TORSO = 3
    RIGHT_ARM = 4
    LEFT_ARM = 5
    RIGHT_RING = 6
    LEFT_RING = 7
    BELT = 8
    FEET = 9
    GLOVES = 10
    ALT_RIGHT_ARM = 11
    ALT_LEFT_ARM = 12


CORE_SLOT_NAMES = {slot.name for slot in CoreEquipSlot if slot is not CoreEquipSlot.NONE}

# NEW-PATH EXTENSION slots. These do not overwrite D2 ids.
EXTENDED_SLOT_NAMES = {
    "RIGHT_SHOULDER",
    "LEFT_SHOULDER",
    "RIGHT_FOREARM",
    "LEFT_FOREARM",
    "RIGHT_KNEE",
    "LEFT_KNEE",
    "RIGHT_LOWER_LEG",
    "LEFT_LOWER_LEG",
    "CLOAK",
    "ARTIFACT_ANCHOR",
}


@dataclass(frozen=True)
class Property:
    code: str
    value: Any = None
    parameter: Any = None
    provenance: str = "SOURCE-DERIVED"
    notes: str = ""


@dataclass(frozen=True)
class Requirement:
    min_level: int = 0
    min_stats: Mapping[str, int] = field(default_factory=dict)
    required_tags: frozenset[str] = frozenset()
    forbidden_tags: frozenset[str] = frozenset()

    def check(self, *, level: int, stats: Mapping[str, int], tags: Iterable[str]) -> tuple[bool, list[str]]:
        tagset = set(tags)
        failures: list[str] = []
        if level < self.min_level:
            failures.append(f"level {level} < {self.min_level}")
        for key, minimum in self.min_stats.items():
            actual = int(stats.get(key, 0))
            if actual < minimum:
                failures.append(f"{key} {actual} < {minimum}")
        missing = self.required_tags - tagset
        if missing:
            failures.append("missing tags: " + ", ".join(sorted(missing)))
        forbidden = self.forbidden_tags & tagset
        if forbidden:
            failures.append("forbidden tags: " + ", ".join(sorted(forbidden)))
        return (not failures, failures)


@dataclass
class Durability:
    current: int
    maximum: int
    indestructible: bool = False

    def __post_init__(self) -> None:
        if self.maximum < 0:
            raise ValueError("maximum durability cannot be negative")
        if not 0 <= self.current <= self.maximum:
            raise ValueError("current durability must be between 0 and maximum")

    @property
    def broken(self) -> bool:
        return (not self.indestructible) and self.maximum > 0 and self.current <= 0

    def damage(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("damage must be non-negative")
        if self.indestructible or self.maximum == 0:
            return self.current
        self.current = max(0, self.current - amount)
        return self.current

    def repair(self, amount: int | None = None) -> int:
        if self.indestructible or self.maximum == 0:
            return self.current
        if amount is None:
            self.current = self.maximum
        else:
            if amount < 0:
                raise ValueError("repair amount must be non-negative")
            self.current = min(self.maximum, self.current + amount)
        return self.current


@dataclass(frozen=True)
class SocketInsert:
    id: str
    code: str
    properties: tuple[Property, ...] = ()
    tags: frozenset[str] = frozenset()


@dataclass(frozen=True)
class RunewordDefinition:
    id: str
    name: str
    ordered_runes: tuple[str, ...]
    eligible_item_types: frozenset[str]
    properties: tuple[Property, ...] = ()

    def matches(self, item: "EquipmentItem") -> bool:
        if item.item_type not in self.eligible_item_types:
            return False
        return tuple(x.code for x in item.socketed) == self.ordered_runes


@dataclass(frozen=True)
class SetDefinition:
    id: str
    name: str
    piece_ids: frozenset[str]
    # D2 Sets.txt PCode2..PCode5 semantics.
    partial_properties: Mapping[int, tuple[Property, ...]] = field(default_factory=dict)
    # D2 Sets.txt FCode semantics.
    full_properties: tuple[Property, ...] = ()

    @property
    def piece_count(self) -> int:
        return len(self.piece_ids)


@dataclass
class EquipmentItem:
    id: str
    name: str
    item_type: str
    quality: ItemQuality = ItemQuality.NORMAL
    location: ItemLocation = ItemLocation.STORED

    # Slot occupancy is system-neutral. D2 core names are preserved; extensions are additive.
    slots: tuple[str, ...] = ()

    base_code: str | None = None
    level: int = 0
    tier: str | None = None
    ethereal: bool = False
    personalized_name: str | None = None

    # Preserve raw/source values without pretending they are already tabletop values.
    source_defense: int | None = None
    source_min_damage: int | None = None
    source_max_damage: int | None = None

    durability: Durability | None = None
    socket_capacity: int = 0
    socketed: list[SocketInsert] = field(default_factory=list)

    requirements: Requirement = field(default_factory=Requirement)
    properties: tuple[Property, ...] = ()

    set_id: str | None = None
    # D2 SetItems.txt aprop* semantics: bonuses carried by this piece as set count rises.
    item_partial_set_properties: Mapping[int, tuple[Property, ...]] = field(default_factory=dict)

    runeword_id: str | None = None
    tags: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.socket_capacity < 0:
            raise ValueError("socket_capacity cannot be negative")
        if len(self.socketed) > self.socket_capacity:
            raise ValueError("socketed items exceed socket capacity")
        valid = CORE_SLOT_NAMES | EXTENDED_SLOT_NAMES
        bad = [slot for slot in self.slots if slot not in valid]
        if bad:
            raise ValueError(f"unknown equipment slot(s): {bad}")

    @property
    def broken(self) -> bool:
        return bool(self.durability and self.durability.broken)

    def socket(self, insert: SocketInsert) -> None:
        if len(self.socketed) >= self.socket_capacity:
            raise ValueError(f"{self.name} has no empty sockets")
        self.socketed.append(insert)

    def unsocket_all(self) -> list[SocketInsert]:
        removed = list(self.socketed)
        self.socketed.clear()
        self.runeword_id = None
        return removed

    def resolve_runeword(self, definitions: Iterable[RunewordDefinition]) -> RunewordDefinition | None:
        for definition in definitions:
            if definition.matches(self):
                self.runeword_id = definition.id
                return definition
        self.runeword_id = None
        return None


@dataclass
class EquipmentState:
    items: dict[str, EquipmentItem] = field(default_factory=dict)
    occupied_slots: dict[str, str] = field(default_factory=dict)
    sets: dict[str, SetDefinition] = field(default_factory=dict)
    runewords: dict[str, RunewordDefinition] = field(default_factory=dict)

    def register_item(self, item: EquipmentItem) -> None:
        if item.id in self.items:
            raise ValueError(f"duplicate item id: {item.id}")
        self.items[item.id] = item

    def register_set(self, definition: SetDefinition) -> None:
        self.sets[definition.id] = definition

    def register_runeword(self, definition: RunewordDefinition) -> None:
        self.runewords[definition.id] = definition

    def equip(
        self,
        item_id: str,
        *,
        level: int,
        stats: Mapping[str, int],
        tags: Iterable[str] = (),
        replace: bool = False,
    ) -> list[str]:
        item = self.items[item_id]
        ok, failures = item.requirements.check(level=level, stats=stats, tags=tags)
        if not ok:
            raise ValueError(f"cannot equip {item.name}: " + "; ".join(failures))
        if not item.slots:
            raise ValueError(f"{item.name} has no equip slots")

        displaced: list[str] = []
        conflicts = {self.occupied_slots[s] for s in item.slots if s in self.occupied_slots}
        conflicts.discard(item_id)
        if conflicts and not replace:
            raise ValueError(f"slot conflict for {item.name}: {sorted(conflicts)}")
        for conflict_id in sorted(conflicts):
            self.unequip(conflict_id)
            displaced.append(conflict_id)

        # Clear stale occupancy for this item before re-equipping.
        for slot, occupant in list(self.occupied_slots.items()):
            if occupant == item_id:
                del self.occupied_slots[slot]
        for slot in item.slots:
            self.occupied_slots[slot] = item_id
        item.location = ItemLocation.EQUIPPED
        return displaced

    def unequip(self, item_id: str) -> None:
        item = self.items[item_id]
        for slot, occupant in list(self.occupied_slots.items()):
            if occupant == item_id:
                del self.occupied_slots[slot]
        item.location = ItemLocation.STORED

    def equipped_items(self, *, include_broken: bool = True) -> list[EquipmentItem]:
        ids = set(self.occupied_slots.values())
        out = [self.items[x] for x in ids]
        if not include_broken:
            out = [x for x in out if not x.broken]
        return sorted(out, key=lambda x: x.id)

    def set_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.equipped_items(include_broken=False):
            if item.set_id:
                counts[item.set_id] = counts.get(item.set_id, 0) + 1
        return counts

    def active_properties(self) -> list[Property]:
        """Return all active equipment properties with D2-like set layering.

        Broken equipment is physically present but mechanically inactive.
        Base properties + socket properties + recognized runeword properties apply.
        Set-piece partial bonuses and set-wide threshold/full bonuses then apply.
        """
        out: list[Property] = []
        equipped = self.equipped_items(include_broken=False)
        counts = self.set_counts()

        for item in equipped:
            out.extend(item.properties)
            for insert in item.socketed:
                out.extend(insert.properties)
            if item.runeword_id and item.runeword_id in self.runewords:
                out.extend(self.runewords[item.runeword_id].properties)
            if item.set_id:
                count = counts.get(item.set_id, 0)
                for threshold, props in sorted(item.item_partial_set_properties.items()):
                    if count >= threshold:
                        out.extend(props)

        for set_id, count in counts.items():
            definition = self.sets.get(set_id)
            if not definition:
                continue
            for threshold, props in sorted(definition.partial_properties.items()):
                if count >= threshold:
                    out.extend(props)
            if definition.piece_count and count >= definition.piece_count:
                out.extend(definition.full_properties)

        return out

    def damage_item(self, item_id: str, amount: int) -> int | None:
        item = self.items[item_id]
        if item.durability is None:
            return None
        return item.durability.damage(amount)

    def repair_item(self, item_id: str, amount: int | None = None) -> int | None:
        item = self.items[item_id]
        if item.durability is None:
            return None
        return item.durability.repair(amount)

    def paperdoll(self) -> dict[str, str]:
        return dict(sorted(self.occupied_slots.items()))
