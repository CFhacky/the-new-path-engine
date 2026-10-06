"""Menagerie signature-item pass (6 Oct 2026). Drives loot-engine's loot_roll.py functions directly
(Python secrets, binding, raw stdout saved to menagerie_signature_rolls.txt).
Skipped by rule: base_item (bases are authored looks) and sockets (rolled 5 Oct, menagerie_socket_rolls.txt).
Archetype by class: cleric/druid -> divine; wizard/sorcerer -> arcane; fighter/barbarian/ranger/monk/warblade -> martial;
rogue-assassin/swordsage -> shadow; duskblade/psychic warrior -> hybrid. Magnitude: named (all bearers).
Extras per the Hand precedent (05b_THE_HAND_SIGNATURE_ITEMS.md): UDRP base roll by rarity, item CL 1d4+12."""
import sys
sys.path.insert(0, "/root/.claude/skills/synced/07327e22-ff68-47f1-ad4a-8176d4a886f0_c7d5c9b9-16d6-4e70-9b16-504f3872f1f8/loot-engine/scripts")
from loot_roll import (load_tables, set_tier, roll_rarity, affix_count, draw_affixes,
                       greater_affixes, temper, aspect, masterwork, die, out)

PIECES = [  # (bearer, CR, archetype, piece)
    ("Quavein Orlzynn", 17, "divine", "the beak-mace (heavy mace)"),
    ("Hadda", 16, "arcane", "the punch-dagger"),
    ("Tarvash", 17, "martial", "the paired scimitars (one roll, both blades)"),
    ("Aerendyl", 16, "martial", "the prayer-cord (garrotte)"),
    ("Kesh", 16, "martial", "the mantis-sickles (one roll, both blades)"),
    ("Marit", 17, "shadow", "the boning knife (dagger)"),
    ("Naevys", 16, "arcane", "the boar-spear (shortspear)"),
    ("Brunna", 16, "shadow", "the tucks (one roll, both estocs)"),
    ("Mercy", 16, "martial", "the gaff (light pick)"),
    ("Zaheda", 16, "divine", "the notebook and reed pen (wondrous)"),
    ("Ysmay", 16, "martial", "the old sword (bastard sword)"),
    ("Ilvaera", 17, "hybrid", "the manticore darts (one roll, the quiver of twenty)"),
    ("Dace", 16, "hybrid", "the short spear (shortspear)"),
    ("Osmund Tarrow", 12, "divine", "the brass censer (light flail)"),
    ("Kerra Lisle", 14, "arcane", "the duelling rapier"),
    ("Wenna Sorrel", 14, "arcane", "the short hatchet (handaxe)"),
    ("Faelith Ammarin", 14, "martial", "the darkwood tower shield (armor; bashed)"),
    ("Patience Haskett", 13, "martial", "the two-headed flail (dire flail)"),
    ("Rhun Talbridge", 13, "martial", "the pollaxe (halberd)"),
    ("Edwyn Coldry", 13, "arcane", "the mail mitten (spiked gauntlet)"),
    ("Ashavel Oriym", 14, "shadow", "the iron war-fans (one roll, the pair)"),
]
UDRP_BASE = {"Rare": ("1d4+2", 4, 2), "Legendary": ("2d4+4", 4, 4), "Ancestral Legendary": ("2d5+8", 5, 8)}

def udrp_base(rarity):
    expr, sides, k = UDRP_BASE[rarity]
    n = 2 if expr.startswith("2") else 1
    raws = [die(sides) for _ in range(n)]
    out(f"UDRP BASE: {rarity} {expr} → raw {raws} +{k} → {sum(raws)+k}")

def main():
    tables = load_tables()
    out("=" * 62)
    out("MENAGERIE SIGNATURE ITEMS — loot_roll.py functions, Python secrets, BINDING")
    out("=" * 62)
    for bearer, cr, arch, piece in PIECES:
        out()
        out(f"### {bearer} — {piece} · CR {cr} · named · archetype {arch}")
        tier_num, _ = set_tier(cr, "named")
        rarity, _ = roll_rarity("named")
        if rarity in ("Unique", "Mythic / Artifact"):
            out(f"→ {rarity}: EXIT the dice pipeline; author per unique-design.md.")
            if rarity == "Unique":
                r = die(16); out(f"UDRP BASE: Unique 1d16+14 → raw {r} +14 → {r+14}")
            c = die(4); out(f"ITEM CL: 1d4+12 → raw {c} → {c+12}")
            continue
        n = affix_count(rarity)
        out("AFFIX DRAWS:")
        drawn = draw_affixes(tables, n, tier_num, arch, pool_limit=2)
        greater_affixes(rarity, drawn, tier_num)
        temper(rarity)
        aspect(rarity, tier_num)
        out("SOCKETS: skipped by rule (rolled 5 Oct 2026, menagerie_socket_rolls.txt)")
        masterwork(rarity)
        udrp_base(rarity)
        c = die(4); out(f"ITEM CL: 1d4+12 → raw {c} → {c+12}")

if __name__ == "__main__":
    main()
