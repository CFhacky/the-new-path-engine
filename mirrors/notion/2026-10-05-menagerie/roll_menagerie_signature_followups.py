"""Menagerie signature items — follow-up rolls (6 Oct 2026). loot_roll.py die() and tables (Python secrets, binding).
Masterwork property lists (stated before rolling):
  minor (21A 9-12, the table's own examples): d3 1 keen · 2 defending · 3 ghost touch
  mid (21A 13-16, SRD +1 melee non-alignment): d12 1 bane · 2 defending · 3 flaming · 4 frost · 5 shock · 6 ghost touch ·
      7 keen · 8 ki focus · 9 mighty cleaving · 10 spell storing · 11 thundering · 12 vicious
  major (21A 17-20, Hand precedent): d4 1 flaming burst · 2 icy burst · 3 shocking burst · 4 wounding
  shield mid (21B 13-16, SRD +1 shield): d4 1 arrow catching · 2 bashing · 3 blinding · 4 light fortification
  Keen on a bludgeoning head is a true rules impossibility: reroll within the list, logged.
Add-ons (Hand precedent): temper 1d4+1 · aspect 3d3+3 · strange socket 1d6+2.
Socket fills (PROPOSED readings, flagged for Chad; the rolls stand only if he confirms):
  Seal = a ward or binding: d2 1 Defensive pool · 2 Condition/Control pool, d100 row at the item's tier.
  Charm = a small passive: d2 1 Utility · 2 Skill/Class, d100 row one tier lower, never Greater.
  Shard = the Summoning pool's Elemental Shard row at the item's tier (no roll; element authored).
  Strange = DM-authored geometry seeded by one aspect-table draw (d10 table, d8 entry; 24J allowed at T1)."""
import sys
sys.path.insert(0, "/root/.claude/skills/synced/07327e22-ff68-47f1-ad4a-8176d4a886f0_c7d5c9b9-16d6-4e70-9b16-504f3872f1f8/loot-engine/scripts")
from loot_roll import die, out, load_tables, band_lookup, tier_value, ASPECT_TABLES

MINOR = ["keen", "defending", "ghost touch"]
MID = ["bane", "defending", "flaming", "frost", "shock", "ghost touch", "keen", "ki focus",
       "mighty cleaving", "spell storing", "thundering", "vicious"]
MAJOR = ["flaming burst", "icy burst", "shocking burst", "wounding"]
SHIELD_MID = ["arrow catching", "bashing", "blinding", "light fortification"]

def pick(label, lst, blunt=False):
    while True:
        r = die(len(lst)); p = lst[r-1]
        if blunt and p == "keen":
            out(f"{label}: d{len(lst)}={r} → keen — bludgeoning head, rules impossibility → reroll within list"); continue
        out(f"{label}: d{len(lst)}={r} → {p}"); return p

def roll(label, n, s, k=0):
    raws = [die(s) for _ in range(n)]
    out(f"{label}: {n}d{s}{'+'+str(k) if k else ''} → raw {raws} → {sum(raws)+k}")

def pool_row(tables, label, pool, tier, lower=False):
    t = min(5, tier + 1) if lower else tier
    while True:
        r = die(100); row = band_lookup(tables[pool], r)
        if row is None:
            out(f"  {label}: d100={r} → no row → reroll"); continue
        tv = tier_value(" ".join(row["cells"]), t) if row["cells"] else None
        out(f"  {label}: {pool} d100={r} → {row['name']}" + (f" | T{t} value: {tv}" if tv else "")); return

def main():
    T = load_tables()
    out("=" * 62); out("MENAGERIE SIGNATURE ITEMS — FOLLOW-UP ROLLS — BINDING"); out("=" * 62)
    out("-- masterwork properties")
    pick("Quavein beak-mace MW14 mid property", MID, blunt=True)
    pick("Hadda punch-dagger MW17 major property", MAJOR)
    pick("Kesh mantis-sickles MW17 major property", MAJOR)
    pick("Brunna tucks MW20 major property", MAJOR)
    pick("Osmund censer MW9 minor property", MINOR, blunt=True)
    pick("Faelith tower shield MW13 shield mid property", SHIELD_MID)
    pick("Edwyn mail mitten MW12 minor property", MINOR)
    out("-- capstones (one non-Greater affix becomes Greater)")
    pick("Brunna capstone", ["Aegis", "Chameleon", "Souldrinker", "Featherfall"])
    pick("Zaheda capstone", ["Riposte", "Swiftfoot", "Chaos Element"])
    out("-- temper add-ons 1d4+1")
    for b in ["Quavein", "Hadda", "Tarvash", "Aerendyl", "Kesh", "Marit", "Brunna", "Zaheda", "Dace",
              "Osmund", "Faelith", "Patience", "Rhun", "Edwyn", "Ashavel"]:
        roll(f"{b} temper add-on", 1, 4, 1)
    out("-- aspect add-ons 3d3+3")
    for b in ["Quavein", "Hadda", "Kesh", "Marit", "Brunna", "Zaheda", "Osmund", "Faelith", "Rhun", "Edwyn"]:
        roll(f"{b} aspect add-on", 3, 3, 3)
    out("-- socket fills (proposed readings)")
    for b, tier in [("Quavein seal", 1), ("Naevys seal", 1)]:
        r = die(2); pool = "Defensive" if r == 1 else "Condition/Control"
        out(f"{b}: d2={r} → {pool}"); pool_row(T, b, pool, tier)
    r = die(2); pool = "Utility" if r == 1 else "Skill/Class"
    out(f"Aerendyl charm: d2={r} → {pool}"); pool_row(T, "Aerendyl charm", pool, 1, lower=True)
    for b in ["Aerendyl strange", "Dace strange", "Rhun strange"]:
        t = die(10); tab = ASPECT_TABLES[t-1]
        e = die(6 if tab.startswith("J") else 8)
        out(f"{b}: seed d10={t} → table {tab}; entry d{'6' if tab.startswith('J') else '8'}={e}")
        roll(f"{b} UDRP add-on", 1, 6, 2)
    out("Marit shard, Ashavel shard: Elemental Shard T1 (Huge elemental 1/day), no roll; element authored")

if __name__ == "__main__":
    main()
