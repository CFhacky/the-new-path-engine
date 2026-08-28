#!/usr/bin/env python3
"""ad2e_monster_harvest.py — AD&D 2e monsters, vision-transcribed (labelled).

WHY THIS ONE IS DIFFERENT (same story as epic_feat_harvest). The AD&D 2e
Monstrous Compendium stat blocks were OCR'd as a two-column dump whose VALUE
cells do not line up with their labels (the value order is scrambled), so parsing
the text extraction is hopeless. But the source PDF's page IMAGES are perfectly
legible, so each monster's stat block was transcribed BY VISION from the rendered
pages (PyMuPDF render → read the PNG). This is still book RAW — read directly off
the page, not invented — and cited to the exact pages. Labelled `system: AD&D 2e`
per the other-editions policy (the translator tools convert it); it is a DIFFERENT
edition from the 3.5e `creature_index` and the 5e `dnd5e_creature_index`.

    reference/ad2e_monster_index.json — every monster: the full AD&D 2e stat
                                        block (AC descending, THAC0, HD, No.
                                        Appearing, alignment, size, XP, ...)
    reference/ad2e_monster_index.md   — the same, for human eyes

PROVENANCE
    Planescape Monstrous Compendium Appendix II (TSR, AD&D 2e). Rendered from the
    PDF and read by vision because the OCR text layer scrambles the stat columns.
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
OUT_JSON = REPO / "reference" / "ad2e_monster_index.json"
OUT_MD = REPO / "reference" / "ad2e_monster_index.md"
SYSTEM = "AD&D 2e"
BOOK = "Planescape Monstrous Compendium Appendix II"
CITATION = ("Planescape Monstrous Compendium Appendix II (TSR, AD&D 2e); "
            "vision-transcribed from the PDF page images (the OCR text layer "
            "scrambles the stat columns)")

# Field order matches the AD&D 2e stat block. Transcribed from the MC App II pages.
COLS = ["name", "page", "climate_terrain", "frequency", "organization",
        "activity_cycle", "diet", "intelligence", "treasure", "alignment",
        "no_appearing", "armor_class", "movement", "hit_dice", "thac0",
        "no_of_attacks", "damage_attack", "special_attacks", "special_defenses",
        "magic_resistance", "size", "morale", "xp_value"]

_ROWS = [
    ("Aasimar", 7, "Any", "Rare", "Solitary", "Any", "Omnivore", "Very (11-12)", "R, U", "Any nonevil",
     "1 (1-2)", "3 (10)", "12", "3+3", "17", "1 or by weapon", "1d3 or by weapon", "Spell use",
     "1/2 damage from fire and cold; +2 to saves vs. charm, emotion, fear, or domination", "10%", "M (5.5-6.5' tall)", "Elite (13-14)", "420"),
    ("Abrian", 9, "Outlands, Lower Planes", "Common", "Flock", "Day", "Carnivore", "Low (5-7)", "B (nest); individual J,K,M", "Chaotic evil",
     "4-40", "6", "18", "2+3", "17", "1 beak and 1 kick", "1d3/1d8", "Shriek", "None", "None", "M (7' tall)", "Unsteady (5-7)", "175"),
    ("Eladrin, Bralani (Lesser)", 31, "Arborea (Pelion)", "Uncommon (Common)", "Band", "Any", "Omnivore", "Very (13-14)", "Incidental", "Chaotic good",
     "1-3 (3-24)", "2 (-2)", "15, Fl 30 (A)", "6+9", "15", "1 or 2", "By weapon +4 or 1d10/1d10", "Whirlwind", "See below", "35%", "M (5' tall)", "Elite (13-14)", "9,000"),
    ("Eladrin, Firre (Greater)", 33, "Arborea", "Rare", "Solitary", "Any", "Omnivore", "Genius (17-18)", "Incidental", "Chaotic good",
     "1-4", "-3", "15, Fl 36 (A)", "7+10", "13", "1 or 2", "By weapon +6 or 3d6/3d6", "Spellsong", "Magic use, shapechange; struck only by cold iron or weapon of +2 or better", "40%", "M (6' tall)", "Champion (15-16)", "14,000"),
    ("Eladrin, Ghaele (Greater)", 34, "Arborea", "Rare", "Solitary", "Any", "Omnivore", "Exceptional-Genius (15-18)", "Incidental", "Chaotic good",
     "1 (1-3)", "-5", "18, Fl 60 (A)", "10+15", "11", "1 or 2", "By weapon +7 or 2d12/2d12", "Positive energy, gaze", "Struck only by cold iron or weapon of +3 or better", "40%", "M (6' tall) or L (20' wingspan)", "Fearless (19-20)", "19,000"),
    ("Eladrin, Noviere (Lesser)", 35, "Arborea", "Uncommon", "Clan", "Any", "Omnivore", "High (13-14)", "Incidental", "Chaotic good",
     "2-16", "3 (-3)", "15, Sw 24", "5+7", "15", "1 weapon or 1 ram", "By weapon +3 or 2d8", "Drowning", "Dolphin form", "20%", "M (5' tall or 7' long)", "Fanatic (17-18)", "5,000"),
    ("Eladrin, Shiere (Lesser)", 36, "Arborea", "Common", "Company", "Night", "Omnivore", "Very-Exceptional (11-16)", "Incidental", "Chaotic good",
     "3-24", "4 (-4)", "15, Fl 24 (A)", "8+12", "13", "2", "By weapon +6", "Glance", "Magic use", "25%", "M (7' tall)", "Fearless (19-20)", "11,000"),
    ("Fhorge", 39, "Outlands, Acheron, Baator", "Uncommon", "Pack", "Any", "Omnivore", "Semi- (2-4)", "None", "Neutral",
     "1 (2-8)", "6, head 3", "15", "5+5", "15", "1 and 1", "3d6 and 1d3", "Charge", "+2 on saves vs. mind-affecting or emotion-based spells; continue fighting until reduced to -10 hp", "None", "L (5' high at shoulder)", "Elite (13-14)", "1,400"),
    ("Guardinal, Cervidal", 46, "Elysium", "Common", "Family", "Day", "Herbivore", "High (11-12)", "Incidental", "Neutral good",
     "1 (2-5)", "2", "18, Ju 3", "4+2", "17", "2 hooves and 1 butt", "1d6+2/1d6+2/1d12+3", "Charge", "Negate poison or illusion", "20%", "M (5.5' tall)", "Elite (13-14)", "3,000"),
    ("Guardinal, Lupinal", 49, "Elysium", "Rare", "Pack", "Any", "Omnivore", "Exceptional (15-16)", "Incidental", "Neutral good",
     "1-8", "-2", "18", "8+4", "13", "3", "1d4+4/1d4+4/2d6", "Howl, pull-down", "Struck only by silver or +2 or better weapons", "35%", "M (6' tall)", "Fanatic (17-18)", "9,000"),
    ("Guardinal, Ursinal", 50, "Elysium", "Rare", "Solitary", "Any", "Omnivore", "Genius (17-18)", "Incidental", "Neutral good",
     "1 (1-2)", "-4", "12", "10+5", "11", "3", "2d6+7/2d6+7/1d10", "Spell-like powers", "Struck only by silver weapons or those of +3 or better enchantment", "45%", "L (8' tall)", "Fanatic (17-18)", "14,000"),
    ("Incantifer", 53, "Any", "Very Rare", "Solitary", "Any", "Special", "Supra-genius (19-20)", "R x3 and incidental", "Neutral (evil)",
     "1", "0 or better", "12", "9d4+18 to 9d4+26", "13", "1", "By weapon", "Spells", "Absorption", "20% + 5% per level over 9th", "M (5-6' tall)", "Average (8-10)", "13,000+"),
    ("Leomarh", 61, "Outlands (any plains)", "Uncommon", "Pride", "Day", "Carnivore", "Low (5-7)", "None", "Neutral",
     "2-12", "4", "15", "6+2", "15", "3", "1d6+1/1d6+1/1d10", "Rear claws, knock-down", "Camouflage, immune to magic missiles", "None", "L (6'-7' long)", "Average (8-10)", "1,400"),
    ("Monster of Legend", 65, "Any", "Very rare", "Solitary", "Any", "Carnivore", "Per prime-material monster", "G, Z x2", "Per prime-material monster",
     "1", "0 or better (-6)", "Per prime-material monster (18, Fl 30 D)", "75-150 hit points (120 hp)", "5", "Per prime-material monster (3)", "Varies (4d6/4d6/2d10)", "Varies (roar)", "Varies", "Special (80%)", "Varies (H, 12' tall)", "Fearless (19-20)", "Special (35,000)"),
    ("Noctral", 69, "Mount Celestia", "Rare", "Solitary", "Dusk, night", "Carnivore", "Supra-genius (19-20)", "G", "Lawful good",
     "1", "1", "1, Fl 36 (C)", "5", "15", "3", "2d4/2d4/1d4+1", "Swoop, surprise", "Invisibility", "30%", "M (20' wingspan)", "Champion (15-16)", "3,000"),
    ("Rager", 77, "Any", "Rare", "Band", "Any", "Carnivore", "Low-Very (5-14)", "P, L, Q", "Any chaotic",
     "1-8", "Varies", "12", "3d10 to 8d10", "Varies", "Varies", "By weapon", "Berserk", "None", "None", "M (5'-7' tall)", "Champion (15-16)", "270-2,000 (by HD)"),
    ("Razorvine", 79, "Any", "Common", "Patch", "None", "Sun, soil", "Non- (0)", "None", "Neutral",
     "2-20 vines", "5", "0", "5 hp per vine", "20", "Special", "1d3, 1d4, or 1d6 + special", "None", "None", "None", "M (12'-20' long)", "None", "35 per vine"),
    ("Rilmani, Argenach", 88, "The Spire, any prime world", "Very rare", "Solitary", "Any", "Omnivore", "Genius (17-18)", "R, Z, U", "Neutral",
     "1 (1-4 at the Spire)", "-1", "15", "9", "11", "2 or 1", "1d20/1d20 (rays) or 1d8+10 (weapon +3, +7 damage) or 1d10 (bare fists)", "Beams, spells", "+3 weapon to hit", "55%", "M (7' tall)", "Champion (15-16)", "16,000"),
    ("Rilmani, Aurumach", 89, "The Spire", "Very rare", "Solitary", "Any", "Omnivore", "Godlike (21+)", "R, U, V x2", "Neutral",
     "1 (1-3 on the Spire)", "-3 (-7 in armor)", "15", "12", "9", "3", "1d10+11 (weapon +3, Strength bonus) or 2d8 (bare fists)", "Aura, spells", "Aura, struck only by +4 or better weapons", "65%", "L (10' tall)", "Fanatic (17-18)", "27,000"),
    ("Simpathetic", 95, "Plains, desert, the Abyss", "Very rare", "Family or flock", "Day", "Carnivore/scavenger", "High (13-14)", "None", "Chaotic evil",
     "1-6 (family) or 4-400 (flock)", "7", "3, Fl 18 (B)", "1-4 hp", "20", "1", "1d2", "Alignment drain, spit blood", "Immune to fire-based attacks", "20%", "T (2' wingspan)", "Champion (15-16)", "175"),
    ("Tanar'ri, Alkilith (True)", 107, "The Abyss", "Rare", "Solitary", "Any", "Carnivore", "High (13-14)", "F", "Chaotic evil",
     "1-3", "3", "6", "11", "9", "4", "2d4/2d4/2d4/2d4", "Acid, poison", "1/2 damage from Type S or B weapons; struck only by +2 or better weapons", "40%", "L (6' diameter)", "Champion (15-16)", "17,000"),
    ("Terlen", 115, "Carceri, Gehenna, Gray Waste", "Uncommon", "School", "Day", "Carnivore", "Animal (1)", "None", "Neutral (evil)",
     "1-8", "5", "3, Sw 15, Fl 15 (C)", "4+3", "17", "1", "2d8", "None", "Camouflage", "10%", "M (7' long)", "Elite (13-14)", "975"),
    ("Tso", 117, "Outlands, any lawful plane", "Rare", "Brood", "Any", "Omnivore", "High (13-14)", "E (individuals J,K,M,Q)", "Lawful evil",
     "3-18", "1 (0)", "9, Cl 3", "7", "13", "3 and 1", "1d4/1d4/1d8 and by weapon", "Poison, magic use", "None", "None", "M (5.5' tall)", "Unsteady (5-7)", "3,000"),
    ("Wastrel", 123, "Any forest, marsh, or swamp", "Common", "Flock", "Day", "Scavenger", "Semi- (2-4)", "None", "Neutral evil",
     "10-100", "6", "3, Fl 15 (C)", "1+1", "19", "1", "1d3", "Ability drain", "None", "50%", "S (3' wingspan)", "Unreliable (2-4)", "270"),
    ("Wraithworm", 125, "Any desert or wasteland", "Uncommon", "Solitary", "Day", "Carnivore", "Animal (1)", "None", "Neutral",
     "1", "5", "9", "5+3", "15", "1", "1d8", "Level drain, poison", "Wraithform", "30%", "M (10' long)", "Average (8-10)", "3,000"),
]


@dataclass
class Ad2eMonster:
    name: str
    book: str
    system: str
    page: Optional[int]
    climate_terrain: Optional[str] = None
    frequency: Optional[str] = None
    organization: Optional[str] = None
    activity_cycle: Optional[str] = None
    diet: Optional[str] = None
    intelligence: Optional[str] = None
    treasure: Optional[str] = None
    alignment: Optional[str] = None
    no_appearing: Optional[str] = None
    armor_class: Optional[str] = None
    movement: Optional[str] = None
    hit_dice: Optional[str] = None
    thac0: Optional[str] = None
    no_of_attacks: Optional[str] = None
    damage_attack: Optional[str] = None
    special_attacks: Optional[str] = None
    special_defenses: Optional[str] = None
    magic_resistance: Optional[str] = None
    size: Optional[str] = None
    morale: Optional[str] = None
    xp_value: Optional[str] = None
    citation: str = CITATION


def build() -> List[Ad2eMonster]:
    out: List[Ad2eMonster] = []
    for row in _ROWS:
        d = dict(zip(COLS, row))
        d["book"] = BOOK
        d["system"] = SYSTEM
        out.append(Ad2eMonster(**d))
    return out


def write_index() -> int:
    monsters = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    md: List[str] = [
        "# AD&D 2e MONSTER INDEX — The New Path",
        "",
        "**Generated by `scripts/ad2e_monster_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** **AD&D 2nd Edition** monsters — a DIFFERENT edition from the",
        "3.5e `creature_index` and the 5e `dnd5e_creature_index`. Every row is",
        "stamped `system: AD&D 2e` and is SOURCE MATERIAL for the system-translator",
        "skill. **Vision-transcribed from the Planescape MC Appendix II PDF page",
        "images** (the OCR text layer scrambles the stat columns) — still book RAW,",
        "read off the page. AD&D 2e uses DESCENDING Armor Class and THAC0.",
        "",
        f"*{len(monsters)} monsters, Planescape MC Appendix II.*",
        "",
        "| Monster | AC | HD | THAC0 | No. App. | Move | Alignment | Size | XP | Page |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for m in monsters:
        md.append(f"| {m.name} | {m.armor_class} | {m.hit_dice} | {m.thac0} | "
                  f"{m.no_appearing} | {m.movement} | {m.alignment} | {m.size} | "
                  f"{m.xp_value} | {m.page} |")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/ad2e_monster_harvest.py",
                    "system": SYSTEM, "book": BOOK, "citation": CITATION,
                    "note": ("Vision-transcribed from the PDF page images; the OCR "
                             "text layer scrambles the stat columns. Book RAW."),
                    "total_monsters": len(monsters),
                    "monsters": [asdict(m) for m in monsters]}, indent=1),
        encoding="utf-8")
    return len(monsters)


def selftest() -> int:
    failures: List[str] = []
    monsters = build()
    if len(monsters) != 25:
        failures.append(f"expected 25 MC App II monsters, got {len(monsters)}")
    names = {m.name for m in monsters}
    for probe in ("Aasimar", "Guardinal, Ursinal", "Rilmani, Aurumach",
                  "Tanar'ri, Alkilith (True)", "Wraithworm"):
        if probe not in names:
            failures.append(f"missing monster '{probe}'")
    if len({m.name.lower() for m in monsters}) != len(monsters):
        failures.append("duplicate monster names")
    # every monster must carry the core AD&D 2e stat fields
    for m in monsters:
        for fld in ("armor_class", "hit_dice", "thac0", "alignment", "xp_value"):
            if not getattr(m, fld):
                failures.append(f"{m.name}: missing {fld}")
                break
        if m.system != "AD&D 2e":
            failures.append(f"{m.name}: system not 'AD&D 2e'")
    aas = next((m for m in monsters if m.name == "Aasimar"), None)
    if aas and (aas.armor_class, aas.hit_dice, aas.thac0, aas.xp_value) != ("3 (10)", "3+3", "17", "420"):
        failures.append(f"Aasimar stats wrong: {(aas.armor_class, aas.hit_dice, aas.thac0, aas.xp_value)}")
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
        hits = [m for m in build() if q in m.name.lower()]
        for m in hits:
            print(f"  {m.name} — AC {m.armor_class}, HD {m.hit_dice}, THAC0 {m.thac0}, "
                  f"{m.alignment}, XP {m.xp_value} [p.{m.page}]")
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1

    n = write_index()
    print(f"{n} AD&D 2e monsters (Planescape MC Appendix II, vision-transcribed). "
          f"(system: {SYSTEM})")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
