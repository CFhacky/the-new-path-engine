#!/usr/bin/env python3
"""epic_feat_harvest.py — the D&D 3.5 epic feats (Epic Level Handbook, Table 1-36).

WHY THIS ONE IS DIFFERENT. Every other harvester PARSES a text extraction. The
Epic Level Handbook's text layer is corrupted OCR (dropped leading characters,
Cyrillic bleed: "Deastaing Critical", "Сай Magic Arms", "реїстай"), so parsing it
yields garbage names — and the `_feats` supplement extractions never included the
ELH-only epic feats. Instead, the ELH PDF's PAGE IMAGES are perfectly legible, so
the master epic-feat summary (Table 1-36, ELH pp.46-49: Feat Name + Prerequisites)
was transcribed BY VISION from those rendered pages. This is still book RAW — read
directly off the page, not invented — and it is cited to the exact pages. The full
benefit text of each feat lives at its description page in the ELH; this index is
the name / type / prerequisites table, which is the qualifying mechanic a
translator needs.

    reference/epic_feat_index.json — every epic feat: name, type (general / wild /
                                     metamagic / item-creation / divine), the
                                     prerequisites, book, table, page span
    reference/epic_feat_index.md   — the same, for human eyes

PROVENANCE
    Epic Level Handbook (WotC, 3.5e), Table 1-36 "Epic Feats", pp.46-49. Rendered
    from Epic Level Handbook.pdf via PyMuPDF and read by vision because the OCR
    text layer is unusable. The `(W)/(M)/(I)/(D)` type markers and the legend are
    from the table itself.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "epic_feat_index.json"
OUT_MD = REPO / "reference" / "epic_feat_index.md"
BOOK = "Epic Level Handbook"
CITATION = "Epic Level Handbook (WotC, 3.5e), Table 1-36 'Epic Feats', pp.46-49 " \
           "(vision-transcribed from the PDF page images; the OCR text layer is corrupt)"
PAGES = "46-49"

# (name, type, prerequisites) — transcribed from ELH Table 1-36, pp.46-49.
# type: "" general | W wild | M metamagic | I item-creation | D divine.
_T = [
    ("Additional Magic Item Space", "", "—"),
    ("Armor Skin", "", "—"),
    ("Augmented Alchemy", "", "Int 21, Alchemy 24 ranks"),
    ("Automatic Quicken Spell", "", "Quicken Spell, Spellcraft 30 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Automatic Silent Spell", "", "Silent Spell, Spellcraft 24 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Automatic Still Spell", "", "Still Spell, Spellcraft 27 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Bane of Enemies", "", "Wilderness Lore 24 ranks, five or more favored enemies (as the ranger class feature)"),
    ("Death of Enemies", "", "Bane of Enemies, Wilderness Lore 30 ranks"),
    ("Beast Companion", "W", "Beast Wild Shape, Master Wild Shape, Knowledge (nature) 24 ranks, wild shape 6/day"),
    ("Beast Wild Shape", "W", "Knowledge (nature) 24 ranks, wild shape 6/day"),
    ("Dragon Wild Shape", "W", "Wis 30, Beast Wild Shape, Knowledge (nature) 30 ranks, wild shape 6/day"),
    ("Magical Beast Wild Shape", "W", "Wis 25, Beast Wild Shape, Knowledge (nature) 27 ranks, wild shape 6/day"),
    ("Plant Wild Shape", "W", "Beast Wild Shape, Knowledge (nature) 24 ranks, wild shape 6/day"),
    ("Vermin Wild Shape", "W", "Beast Wild Shape, Knowledge (nature) 24 ranks, wild shape 6/day"),
    ("Blinding Speed", "", "Dex 25"),
    ("Bonus Domain", "", "Wis 21, ability to cast 9th-level divine spells"),
    ("Bulwark of Defense", "", "Con 25, defensive stance 3/day"),
    ("Chaotic Rage", "", "Rage 5/day, chaotic alignment"),
    ("Combat Archery", "", "Dodge, Mobility, Point Blank Shot"),
    ("Craft Epic Magic Arms and Armor", "I", "Craft Magic Arms and Armor, Knowledge (arcana) 28 ranks, Spellcraft 28 ranks"),
    ("Craft Epic Rod", "I", "Craft Rod, Knowledge (arcana) 32 ranks, Spellcraft 32 ranks"),
    ("Craft Epic Staff", "I", "Craft Staff, Knowledge (arcana) 35 ranks, Spellcraft 35 ranks"),
    ("Craft Epic Wondrous Item", "I", "Craft Wondrous Item, Knowledge (arcana) 26 ranks, Spellcraft 26 ranks"),
    ("Damage Reduction", "", "Con 21"),
    ("Deafening Song", "", "Perform 24 ranks, bardic music class feature"),
    ("Hindering Song", "", "Deafening Song, Perform 21 ranks, bardic music class feature"),
    ("Dexterous Fortitude", "", "Dex 25, slippery mind class feature"),
    ("Dexterous Will", "", "Dex 25, slippery mind class feature"),
    ("Diminutive Wild Shape", "W", "Ability to wild shape into a Huge animal"),
    ("Fine Wild Shape", "W", "Ability to wild shape into a Diminutive creature"),
    ("Distant Shot", "", "Dex 25, Far Shot, Point Blank Shot, Spot 20 ranks"),
    ("Efficient Item Creation", "", "Item creation feat to be selected, Knowledge (arcana) 24 ranks, Spellcraft 24 ranks"),
    ("Energy Resistance", "", "—"),
    ("Enhance Spell", "M", "Maximize Spell"),
    ("Epic Dodge", "", "Dex 25, Dodge, Tumble 30 ranks, improved evasion, defensive roll class feature"),
    ("Epic Endurance", "", "Con 25, Endurance"),
    ("Epic Fortitude", "", "—"),
    ("Epic Inspiration", "", "Cha 25, Perform 30 ranks, bardic music class feature"),
    ("Epic Leadership", "", "Cha 25, Leadership, Leadership score 25"),
    ("Legendary Commander", "", "Cha 25, Epic Leadership, Leadership, Diplomacy 30 ranks, must rule own kingdom and have a stronghold"),
    ("Epic Prowess", "", "—"),
    ("Epic Reflexes", "", "—"),
    ("Epic Reputation", "", "—"),
    ("Epic Skill Focus", "", "20 ranks in the skill selected"),
    ("Epic Speed", "", "Dex 21, Run"),
    ("Epic Spell Focus", "", "Greater Spell Focus and Spell Focus in the school selected, ability to cast at least one 9th-level spell of the school"),
    ("Epic Spell Penetration", "", "Greater Spell Penetration, Spell Penetration"),
    ("Epic Spellcasting", "", "Spellcraft 24 ranks, Knowledge (arcana) 24 ranks and ability to cast 9th-level arcane spells (OR the Knowledge religion/nature divine variants)"),
    ("Epic Toughness", "", "—"),
    ("Epic Weapon Focus", "", "Weapon Focus in the weapon to be chosen"),
    ("Epic Weapon Specialization", "", "Epic Weapon Focus, Weapon Focus, Weapon Specialization (all in the weapon to be chosen)"),
    ("Epic Will", "", "—"),
    ("Exceptional Deflection", "", "Dex 21, Wis 19, Deflect Arrows, Improved Unarmed Strike"),
    ("Extended Life Span", "", "—"),
    ("Familiar Spell", "", "Int 25 (if your spellcasting is controlled by Intelligence) OR Cha 25 (if controlled by Charisma)"),
    ("Fast Healing", "", "Con 25"),
    ("Forge Epic Ring", "I", "Forge Ring, Knowledge (arcana) 35 ranks, Spellcraft 35 ranks"),
    ("Gargantuan Wild Shape", "W", "Ability to wild shape into a Huge animal"),
    ("Colossal Wild Shape", "W", "Ability to wild shape into a Gargantuan creature"),
    ("Great Charisma", "", "—"),
    ("Great Constitution", "", "—"),
    ("Great Dexterity", "", "—"),
    ("Great Intelligence", "", "—"),
    ("Great Smiting", "", "Cha 25, smite ability (from class feature or domain granted power)"),
    ("Great Strength", "", "—"),
    ("Great Wisdom", "", "—"),
    ("Group Inspiration", "", "Perform 30 ranks, bardic music class feature"),
    ("Holy Strike", "", "Smite evil class feature, any good alignment"),
    ("Ignore Material Components", "", "Eschew Materials, Spellcraft 25 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Improved Alignment-Based Casting", "", "Access to domain of Chaos, Evil, Good, or Law, alignment must match domain chosen, ability to cast 9th-level divine spells"),
    ("Improved Arrow of Death", "", "Dex 19, Wis 19, Point Blank Shot, Precise Shot, arrow of death class feature"),
    ("Improved Aura of Courage", "", "Cha 25, aura of courage class feature"),
    ("Improved Aura of Despair", "", "Cha 25, aura of despair class feature"),
    ("Improved Combat Casting", "", "Combat Casting, Concentration 25 ranks"),
    ("Improved Combat Reflexes", "", "Dex 21, Combat Reflexes"),
    ("Improved Darkvision", "", "Darkvision"),
    ("Improved Death Attack", "", "Death attack class feature, sneak attack +5d6"),
    ("Improved Elemental Wild Shape", "W", "Wis 25, ability to wild shape into an elemental"),
    ("Improved Favored Enemy", "", "Five or more favored enemies"),
    ("Improved Heighten Spell", "M", "Heighten Spell, Spellcraft 20 ranks"),
    ("Improved Ki Strike", "", "Wis 21, Ki strike +3"),
    ("Improved Low-Light Vision", "", "Low-light vision"),
    ("Improved Manifestation", "", "Ability to manifest powers of the normal maximum level in at least one psionic class"),
    ("Improved Metamagic", "", "Four metamagic feats, Spellcraft 30 ranks"),
    ("Improved Manyshot", "", "Dex 19, base attack bonus +21, Manyshot, Point Blank Shot, Rapid Shot"),
    ("Improved Sneak Attack", "", "Sneak attack +8d6"),
    ("Improved Spell Capacity", "", "Ability to cast spells of the normal maximum spell level in at least one spellcasting class"),
    ("Improved Spell Resistance", "", "Must have spell resistance from a feat, class feature, or other permanent effect"),
    ("Improved Stunning Fist", "", "Dex 19, Wis 19, Improved Unarmed Strike, Stunning Fist"),
    ("Improved Whirlwind Attack", "", "Int 13, Dex 23, Dodge, Expertise, Mobility, Spring Attack, Whirlwind Attack"),
    ("Incite Rage", "", "Cha 25, greater rage class feature"),
    ("Infinite Deflection", "", "Dex 25, Combat Reflexes, Deflect Arrows, Improved Unarmed Strike"),
    ("Inspire Excellence", "", "Perform 30 ranks, bardic music class feature"),
    ("Instant Reload", "", "Quick Draw, Rapid Reload, Weapon Focus (crossbow type to be selected)"),
    ("Intensify Spell", "M", "Empower Spell, Maximize Spell, Spellcraft 30 ranks, ability to cast 9th-level arcane or divine spells"),
    ("Keen Strike", "", "Str 23, Wis 23, Improved Critical (unarmed strike), ki strike +3"),
    ("Vorpal Strike", "", "Str 25, Wis 25, Improved Critical (unarmed strike), Improved Unarmed Strike, Keen Strike, Stunning Fist, ki strike +5"),
    ("Lasting Inspiration", "", "Perform 25 ranks, bardic music class feature"),
    ("Legendary Climber", "", "Dex 21, Balance 12 ranks, Climb 24 ranks"),
    ("Legendary Leaper", "", "Jump 24 ranks"),
    ("Legendary Rider", "", "Ride 24 ranks"),
    ("Legendary Tracker", "", "Wis 25, Track, Knowledge (nature) 30 ranks, Wilderness Lore 30 ranks"),
    ("Legendary Wrestler", "", "Str 21, Dex 21, Improved Unarmed Strike, Escape Artist 15 ranks"),
    ("Lingering Damage", "", "Sneak attack +8d6, crippling strike class feature"),
    ("Master Staff", "", "Craft Staff, Spellcraft 15 ranks"),
    ("Master Wand", "", "Craft Wand, Spellcraft 15 ranks"),
    ("Mighty Rage", "", "Str 21, Con 21, greater rage class feature"),
    ("Mobile Defense", "", "Dex 15, Dodge, Mobility, Spring Attack, defensive stance 5/day class feature"),
    ("Multispell", "", "Quicken Spell, ability to cast 9th-level arcane or divine spells"),
    ("Multiweapon Rend", "", "Dex 15, base attack bonus +9, three or more hands, Multidexterity, Multiweapon Fighting"),
    ("Music of the Gods", "", "Cha 25, Perform 30 ranks, bardic music class feature"),
    ("Negative Energy Burst", "D", "Cha 25, ability to rebuke or command undead, ability to cast inflict critical wounds, an evil alignment"),
    ("Overwhelming Critical", "", "Str 23, Cleave, Great Cleave, Improved Critical (weapon to be chosen), Power Attack, Weapon Focus (weapon to be chosen)"),
    ("Devastating Critical", "", "Str 25, Cleave, Great Cleave, Improved Critical (weapon to be chosen), Overwhelming Critical (weapon to be chosen), Power Attack, Weapon Focus (weapon to be chosen)"),
    ("Penetrate Damage Reduction", "", "—"),
    ("Perfect Health", "", "Con 25, Great Fortitude"),
    ("Perfect Multiweapon Fighting", "", "Dex 25, three or more hands, Greater Multiweapon Fighting, Multidexterity, Multiweapon Fighting"),
    ("Perfect Two-Weapon Fighting", "", "Dex 25, Ambidexterity, Greater Two-Weapon Fighting, Improved Two-Weapon Fighting, Two-Weapon Fighting"),
    ("Permanent Emanation", "", "Spellcraft 25 ranks, ability to cast the spell to be made permanent"),
    ("Planar Turning", "", "Wis 25, Cha 25, ability to turn or rebuke undead"),
    ("Polyglot", "", "Int 25, Speak Language (five languages)"),
    ("Positive Energy Aura", "", "Cha 25, ability to turn undead, ability to cast dispel evil"),
    ("Ranged Inspiration", "", "Perform 25 ranks, bardic music class feature"),
    ("Rapid Inspiration", "", "Perform 30 ranks, bardic music class feature"),
    ("Reactive Countersong", "", "Combat Reflexes, Perform 30 ranks, bardic music class feature"),
    ("Reflect Arrows", "", "Dex 25, Deflect Arrows, Improved Unarmed Strike"),
    ("Righteous Strike", "", "Wis 19, Improved Unarmed Strike, Stunning Fist, any lawful alignment"),
    ("Ruinous Rage", "", "Str 25, Power Attack, Sunder, rage 5/day"),
    ("Scribe Epic Scroll", "I", "Scribe Scroll, Knowledge (arcana) 24 ranks, Spellcraft 24 ranks"),
    ("Self-Concealment", "", "Dex 30, Hide 30 ranks, Tumble 30 ranks, improved evasion"),
    ("Shattering Strike", "", "Epic Weapon Focus (unarmed strike), Weapon Focus (unarmed strike), Concentration 25 ranks, ki strike +3"),
    ("Sneak Attack of Opportunity", "", "Sneak attack +8d6, opportunist class feature"),
    ("Spectral Strike", "", "Wis 19, ability to turn or rebuke undead"),
    ("Spell Knowledge", "", "Ability to cast the maximum spell level of an arcane spellcasting class"),
    ("Spell Opportunity", "", "Combat Casting, Combat Reflexes, Quicken Spell, Spellcraft 25 ranks"),
    ("Spell Stowaway", "", "Spellcraft 24 ranks, caster level 12th"),
    ("Spellcasting Harrier", "", "Combat Reflexes"),
    ("Spontaneous Domain Access", "", "Wis 25, Spellcraft 30 ranks, ability to cast 9th-level divine spells"),
    ("Spontaneous Spell", "", "Spellcraft 25 ranks, ability to cast the maximum normal spell level of at least one spellcasting class"),
    ("Storm of Throws", "", "Dex 23, Point Blank Shot, Quick Draw, Rapid Shot"),
    ("Superior Initiative", "", "Improved Initiative"),
    ("Swarm of Arrows", "", "Dex 23, Point Blank Shot, Rapid Shot, Weapon Focus (type of bow used)"),
    ("Tenacious Magic", "", "Spellcraft 15 ranks, ability to cast the spell to be made tenacious"),
    ("Terrifying Rage", "", "Intimidate 25 ranks, rage 5/day"),
    ("Thundering Rage", "", "Str 25, rage 5/day"),
    ("Trap Sense", "", "Search 25 ranks, Spot 25 ranks, ability to find traps as a rogue"),
    ("Two-Weapon Rend", "", "Dex 15, base attack bonus +9, Ambidexterity, Improved Two-Weapon Fighting, Two-Weapon Fighting"),
    ("Uncanny Accuracy", "", "Dex 21, Point Blank Shot, Precise Shot, Spot 20 ranks"),
    ("Undead Mastery", "D", "Cha 21, ability to rebuke or command undead"),
    ("Zone of Animation", "D", "Cha 25, Undead Mastery, ability to rebuke or command undead"),
    ("Unholy Strike", "", "Smite good class feature, any evil alignment"),
    ("Widen Aura of Courage", "", "Cha 25, aura of courage class feature"),
    ("Widen Aura of Despair", "", "Cha 25, aura of despair class feature"),
]
TYPE_NAME = {"": "general", "W": "wild", "M": "metamagic", "I": "item-creation", "D": "divine"}


@dataclass
class EpicFeat:
    name: str
    book: str
    type: str
    prerequisites: Optional[str]
    citation: str
    pages: str


def build() -> List[EpicFeat]:
    out: List[EpicFeat] = []
    seen = set()
    for name, ty, prereq in _T:
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(EpicFeat(name=name, book=BOOK, type=TYPE_NAME[ty],
                            prerequisites=(None if prereq in ("—", "") else prereq),
                            citation=CITATION, pages=PAGES))
    return out


def write_index() -> int:
    feats = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    from collections import Counter
    by_type = Counter(f.type for f in feats)
    md: List[str] = [
        "# EPIC FEAT INDEX — The New Path",
        "",
        "**Generated by `scripts/epic_feat_harvest.py`. Do not hand-edit; rerun the",
        "harvest.** D&D 3.5 epic feats from the Epic Level Handbook (Table 1-36).",
        "**Vision-transcribed from the PDF page images** (ELH pp.46-49) because the",
        "book's OCR text layer is corrupt — this is still book RAW, read directly",
        "off the page. `type` is general / wild / metamagic / item-creation /",
        "divine; the full benefit text is at each feat's description page in the",
        "ELH. Prereqs left `—` are feats the table lists with no prerequisite.",
        "",
        f"*{len(feats)} epic feats — " +
        ", ".join(f"{n} {t}" for t, n in sorted(by_type.items())) + ".*",
        "",
        "| Epic Feat | Type | Prerequisites |",
        "|---|---|---|",
    ]
    for f in feats:
        md.append(f"| {f.name} | {f.type} | {f.prerequisites or '—'} |")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/epic_feat_harvest.py",
                    "book": BOOK, "citation": CITATION, "pages": PAGES,
                    "note": ("Vision-transcribed from the ELH PDF page images; the "
                             "OCR text layer is corrupt. Book RAW, read off the page."),
                    "total_epic_feats": len(feats),
                    "by_type": dict(by_type),
                    "epic_feats": [asdict(f) for f in feats]}, indent=1),
        encoding="utf-8")
    return len(feats)


def selftest() -> int:
    failures: List[str] = []
    feats = build()
    names = {f.name for f in feats}
    # the ELH-only epic feats the corrupt OCR could not yield must be present now
    for probe in ("Devastating Critical", "Blinding Speed", "Overwhelming Critical",
                  "Epic Toughness", "Vorpal Strike", "Superior Initiative"):
        if probe not in names:
            failures.append(f"missing epic feat '{probe}'")
    if len(feats) < 150:
        failures.append(f"only {len(feats)} epic feats; the book says 'more than 150'")
    dc = next((f for f in feats if f.name == "Devastating Critical"), None)
    if dc and (not dc.prerequisites or "Overwhelming Critical" not in dc.prerequisites):
        failures.append(f"Devastating Critical prereqs look wrong: {dc.prerequisites!r}")
    if len({f.name.lower() for f in feats}) != len(feats):
        failures.append("duplicate epic-feat names")
    # type markers landed
    if not any(f.type == "wild" for f in feats) or not any(f.type == "divine" for f in feats):
        failures.append("type markers (wild/divine) not captured")
    for f in failures:
        print(f"SELFTEST FAIL: {f}")
    print("selftest: " + ("PASS" if not failures else f"{len(failures)} failure(s)"))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--search", metavar="TEXT")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.search:
        q = args.search.lower()
        hits = [f for f in build() if q in f.name.lower()]
        for f in hits:
            print(f"  {f.name} [{f.type}] — {f.prerequisites or '—'}")
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1

    n = write_index()
    print(f"{n} D&D 3.5 epic feats (Epic Level Handbook, Table 1-36, vision-transcribed).")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
