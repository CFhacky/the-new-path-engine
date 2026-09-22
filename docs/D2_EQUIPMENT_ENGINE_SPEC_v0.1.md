# D2 Equipment Engine Specification v0.1

**Status:** SOURCE-BOUND IMPLEMENTATION BASELINE  
**Date:** 2026-09-22  
**Runtime:** `scripts/d2_equipment_engine.py`  
**Upstream manifest:** `reference/d2_equipment_upstream_manifest.json`

## 1. Decision

The New Path adopts the Diablo II item/equipment model as the default equipment-state substrate wherever the mechanic is system-agnostic.

This is not a cosmetic "paperdoll inspired by D2." The engine preserves the D2 concepts of:

- discrete equipped locations;
- individual item identity;
- base item record;
- quality;
- requirements;
- durability;
- sockets and inserted items;
- item properties;
- Set membership;
- per-piece partial Set bonuses;
- Set-wide partial and full bonuses;
- ordered runeword recipes;
- alternate weapon slots;
- tier/upgraded base identity;
- ethereal state;
- personalization/naming.

Only terminal combat arithmetic is translated. D2 Defense is not automatically D&D 3.5e AC and is not automatically GURPS DR.

## 2. Source authority

Primary implementation source is WalterCouto/D2CE pinned at:

- commit `c246509f385790462979004aeeaf7a47696ed605`
- tree `f6ae482e04c8d525a8e10c7b4831a59ff86bacd7`
- recursive tree verified complete by GitHub.

The exact source files and blob SHAs live in `reference/d2_equipment_upstream_manifest.json`.

Existing campaign D2 source work under `campaign-development-vault/projects/in-progress/malcador-d2-prison/` remains the authority for source-row/edition adjudication. D2CE supplies the item-state/runtime grammar; the pinned campaign source corpus supplies edition-aware D2 content.

## 3. Classification matrix

| D2 mechanic | New Path disposition | Rule |
|---|---|---|
| Item object identity | **ADOPT DIRECTLY** | One item is a persistent object with its own state. |
| Quality enum | **ADOPT DIRECTLY** | UNKNOWN, INFERIOR, NORMAL, SUPERIOR, MAGIC, SET, RARE, UNIQUE, CRAFTED, TEMPERED. |
| Item location | **ADOPT DIRECTLY** | Stored, equipped, belt, buffer, socket remain distinct states. |
| Core equip slots | **ADOPT DIRECTLY** | HEAD, NECK, TORSO, RIGHT_ARM, LEFT_ARM, RIGHT_RING, LEFT_RING, BELT, FEET, GLOVES, ALT_RIGHT_ARM, ALT_LEFT_ARM. |
| Base armor Defense | **TRANSLATE NUMERICALLY** | Preserve raw value; System Translator produces 3.5e/GURPS/fused expression. |
| Weapon min/max damage | **TRANSLATE NUMERICALLY** | Preserve raw values; translator owns dice/damage expression. |
| Strength/Dex/level requirements | **ADOPT + TRANSLATE** | Preserve source requirement; campaign/native items may add equivalent tabletop requirements. |
| Durability | **ADOPT DIRECTLY** | Current/max state persists. Broken state is runtime-significant. |
| Indestructible | **ADOPT DIRECTLY** | No durability loss where explicitly present. |
| Sockets | **ADOPT DIRECTLY** | Capacity, occupancy and insertion order persist. |
| Socketed-item properties | **ADOPT DIRECTLY** | Inserted object properties aggregate through host. |
| Runewords | **ADOPT DIRECTLY** | Ordered rune sequence + eligible base type + resulting property package. |
| Set pieces | **ADOPT DIRECTLY** | Piece identity and Set membership are explicit. |
| Per-piece partial Set bonuses | **ADOPT DIRECTLY** | D2 SetItems-style bonus thresholds remain. |
| Set-wide partial/full bonuses | **ADOPT DIRECTLY** | D2 Sets-style threshold/full properties remain. |
| Item tier upgrades | **ADOPT DIRECTLY** | Normal/exceptional/elite or analogous campaign tier changes base object, not object identity. |
| Ethereal | **ADOPT DIRECTLY** | Retained as item state; exact tabletop effect translated by source/campaign. |
| Personalization | **ADOPT DIRECTLY** | Naming/ownership metadata persists. |
| Inventory width/height | **DEFER, RETAINABLE** | Useful if grid inventory is later enabled; not required for paperdoll resolution. |
| Stack quantity | **ADOPT WHERE APPLICABLE** | Consumables/ammunition can use it; armor does not need it. |
| Vendor/gambling tables | **NOT PART OF THIS ENGINE** | Economy/loot acquisition concern. |
| Save checksum/bit layout | **NOT PART OF RUNTIME** | Provenance only. |
| UI bitmaps/menu appearance | **NOT PART OF RUNTIME** | Presentation layer only. |

## 4. Core paperdoll

D2 core slots are preserved exactly.

```
HEAD
NECK
TORSO
RIGHT_ARM
LEFT_ARM
RIGHT_RING
LEFT_RING
BELT
FEET
GLOVES
ALT_RIGHT_ARM
ALT_LEFT_ARM
```

The New Path adds slots only when tabletop physicality requires a location D2 does not expose as an independently equipped object.

Current extension registry:

```
RIGHT_SHOULDER
LEFT_SHOULDER
RIGHT_FOREARM
LEFT_FOREARM
RIGHT_KNEE
LEFT_KNEE
RIGHT_LOWER_LEG
LEFT_LOWER_LEG
CLOAK
ARTIFACT_ANCHOR
```

These are additive. They do not renumber or redefine D2's core ids.

D2's `armor.txt` also contains appearance-component columns for right/left shoulder pads (`rSPad`, `lSPad`). That is useful source evidence that shoulder presentation is already represented independently at the art/component layer even though D2 does not expose shoulder guards as player equip slots.

## 5. Item object

Every equipment object may carry:

- stable item id;
- display name;
- base code;
- item type;
- quality;
- item level;
- base/tier identity;
- equipped/stored/socket state;
- one or more occupied slots;
- raw/source Defense;
- raw/source min/max damage;
- requirements;
- current/max durability;
- indestructible flag;
- socket capacity;
- ordered socket contents;
- ordinary properties;
- Set id;
- per-piece Set threshold properties;
- resolved runeword id;
- ethereal state;
- personalized name;
- tags and provenance metadata.

A character sheet should consume this state. It should not duplicate equipment-derived facts as unrelated permanent character numbers.

## 6. Multi-slot equipment

New Path items may occupy multiple slots.

This is an extension required for physical objects such as:

- paired armor assemblies;
- two-handed weapons;
- objects that cover both lower legs;
- harnesses crossing torso and shoulders.

Equipping a multi-slot object checks all slots. A conflict either blocks the equip or explicitly displaces the conflicting item(s).

This lets a physical design remain one object when appropriate without inventing fake duplicate items solely to satisfy the paperdoll.

## 7. Durability and breakage

D2 durability is retained as persistent item state.

New Path adds one tabletop runtime rule:

> At 0 durability, a breakable equipped item remains physically present but contributes no active mechanical properties until repaired.

This is an **EXTEND FOR NEW PATH** rule, not claimed as a verbatim D2 combat implementation.

Damage and repair operate on the item object, not the character sheet.

Indestructible items ignore durability damage.

## 8. Properties

Properties are stored system-neutrally as:

- code;
- parameter;
- value/min/max or translated payload;
- provenance;
- notes.

D2 `properties.txt` is the upstream grammar for source codes such as Defense, enhanced Defense, damage reduction, resistances, attack modifiers, skill grants and triggered effects.

The Equipment Engine aggregates property objects. It does **not** silently reinterpret them into another rules system.

The translator then maps the active property list to:

- D&D 3.5e;
- GURPS 4e;
- fused runtime effects.

## 9. Set mechanics

Both D2 Set layers are retained.

### Piece-local partial bonuses

D2 `setitems.txt` carries ordinary properties plus `aprop*` threshold properties. A piece can therefore gain additional properties as more pieces from its Set are equipped.

The engine models this as:

```
item_partial_set_properties[count] -> properties
```

### Set-wide bonuses

D2 `sets.txt` carries partial bonuses by equipped-piece count plus full-set properties.

The engine models this as:

```
set.partial_properties[count] -> properties
set.full_properties -> properties
```

Broken items do not count as active Set pieces until repaired.

## 10. Sockets and runewords

Socket state is structural, not a tooltip fiction.

Each host item tracks:

- socket capacity;
- ordered inserted objects;
- inserted-object properties.

Runeword recognition requires:

1. eligible base item type;
2. the correct number/order of runes;
3. exact ordered rune codes.

If matched, the host gains the runeword property package while the constituent rune objects remain physically installed.

This permits campaign extensions such as soul fragments, divine remnants, crystals and other socketable objects without changing the underlying socket model.

## 11. Requirements

D2's level/stat/equip-legality logic is retained conceptually.

New Path extends requirements with tags for states D2 does not need:

- lineage;
- body form;
- species;
- attunement;
- artifact bond;
- faction/office;
- metaphysical state.

Requirements answer whether an item can be equipped. They do not themselves grant its effects.

## 12. Alternate weapon configuration

`ALT_RIGHT_ARM` and `ALT_LEFT_ARM` are retained.

This gives the engine a native place for secondary weapon configurations without inventing an unrelated "carried weapon" subsystem.

Switch timing remains an action-economy concern owned by the active rules system.

## 13. Translation boundary

The engine must preserve source facts before translation.

Example:

```
source_defense = 120
property = ac% +50
durability = 36/36
```

is equipment truth.

A translator may then produce something such as:

```
3.5e: armor/guard contribution +N
GURPS: DR N at locations X/Y
Fused: targeted protection / active-defense interaction
```

Those translated numbers are separate fields/rules and must identify their provenance.

No formula may infer that "120 D2 Defense = 12 AC" merely because the numbers look convenient.

## 14. Character-sheet contract

A table-facing sheet should expose both:

1. **intrinsic character defense**, and
2. **derived equipped defense**.

If equipment changes, the sheet's derived totals change.

For example, a character's displayed AC should be explainable as:

```
intrinsic body
+ Dexterity
+ active equipped items
+ active Set properties
+ temporary/situational modifiers
```

The same principle applies to GURPS DR, parry modifiers, resistances, movement modifiers and other equipment-derived effects.

## 15. Gressil integration contract

Gressil is the first campaign consumer, but no Gressil-specific rule belongs in the generic engine.

Her campaign fixture should instantiate, at minimum:

- slim black-runesteel gorget;
- right black-runesteel shoulder guard;
- left black-runesteel shoulder guard;
- right articulated forearm guard;
- left articulated forearm guard;
- right knee/lower-leg protection;
- left knee/lower-leg protection;
- dueling boots;
- cloth/runic doublet and split war-skirt as clothing objects where useful;
- Incarnate Edge;
- physical Root in ARTIFACT_ANCHOR state/slot semantics;
- future jewelry through standard ring/neck slots unless a campaign-specific object says otherwise.

Her paired shoulder guards are two physical armor pieces and can therefore have independent durability while belonging to the same Set.

The video reference does not define this equipment. Her previously locked regalia remains the visual/equipment authority.

## 16. What remains unresolved after v0.1

The engine structure is now defined and implemented. These are deliberately not guessed:

- D2 Defense -> 3.5e AC conversion;
- D2 Defense -> GURPS DR conversion;
- durability scale for campaign-authored items that have no D2 source row;
- Gressil's individual runesteel piece values;
- Gressil's partial/full regalia Set bonuses;
- repair difficulty/cost for black runesteel;
- whether her artifact-born pieces can receive sockets at first Incarnation.

Those belong to the numeric translation / Gressil instantiation pass, not the equipment substrate.

## 17. Governance

When adding an equipment rule, mark it:

- **SOURCE-DERIVED** — present in the pinned D2 implementation/data;
- **UPSTREAM-ADOPTED** — D2 behavior intentionally retained as New Path runtime;
- **TRANSLATED** — source mechanic numerically expressed in 3.5e/GURPS;
- **NEW-PATH EXTENSION** — added because tabletop/campaign physicality needs it;
- **CAMPAIGN-RULED** — setting/character-specific;
- **UNRESOLVED** — no number or behavior has yet been authorized.

Do not silently turn an extension into a claim about D2.
