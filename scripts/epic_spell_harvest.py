#!/usr/bin/env python3
"""epic_spell_harvest.py — the D&D 3.5 epic spells (Epic Level Handbook, Chapter 2).

WHY THIS ONE IS DIFFERENT (same reason as epic_feat_harvest.py). The Epic Level
Handbook's text layer is corrupted OCR (dropped leading characters, Cyrillic
bleed: "Spelleraft", "Momento Mori" garbles), so parsing it yields garbage
numbers and names. Instead, the ELH PDF's PAGE IMAGES are perfectly legible, so
the epic-spell chapter (Chapter 2, "Epic Spells") was transcribed BY VISION from
those rendered pages. This is still book RAW — read directly off the page, never
invented — and every entry is cited to the exact page.

Two bodies of mechanics are captured, exactly as printed:

  * the epic spell SEEDS (Table 2-1 "Epic Seeds", ELH p.88) — the base building
    blocks, each with its base Spellcraft DC. Every seed's base DC was
    cross-checked against the "To Develop / Seeds:" lines of the sample spells
    (e.g. destroy DC 29, conjure DC 21, summon DC 14, ward DC 14, animate dead
    DC 23) and all agree.

  * the ~46 SAMPLE EPIC SPELLS — each a full description (school + Spellcraft DC
    read off the entry header, ELH pp.74-88) paired with its one-line effect as
    printed in the "Epic Spells by Spellcraft DC" summary list (pp.73-74).

    reference/epic_spell_index.json — every seed + sample spell: name, kind,
                                      spellcraft_dc, school, effect, book, page
    reference/epic_spell_index.md   — the same, for human eyes

FOUR BOOK-INTERNAL DC DISCREPANCIES. The quick "Epic Spells by Spellcraft DC"
list on pp.73-74 disagrees with four full-entry headers by 2. Each such entry
carries the full-entry DC (the actual spell description's stated value) as
spellcraft_dc and records the summary's differing number in `note`:
Origin of Species: Achaierai (entry 38 / list 40), Raise Island (entry 48 /
list 50), Epic Spell Reflection (entry 68 / list 70), Pestilence (entry 104 /
list 102).

PROVENANCE
    Epic Level Handbook (WotC, 3.5e), Chapter 2 "Epic Spells". Rendered from
    Epic Level Handbook.pdf via PyMuPDF at ~2.8x and read by vision because the
    OCR text layer is unusable. Seed base DCs from Table 2-1 (p.88); sample-spell
    schools + Spellcraft DCs from the full descriptions (pp.74-88); one-line
    effects from the "Epic Spells by Spellcraft DC" summary (pp.73-74).
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
OUT_JSON = REPO / "reference" / "epic_spell_index.json"
OUT_MD = REPO / "reference" / "epic_spell_index.md"
BOOK = "Epic Level Handbook"
CITATION = (
    "Epic Level Handbook (WotC, 3.5e), Chapter 2 'Epic Spells' — Table 2-1 "
    "'Epic Seeds' (base Spellcraft DCs, p.88) and the sample epic spells (full "
    "descriptions with school + Spellcraft DC, pp.74-88; 'Epic Spells by "
    "Spellcraft DC' summary + one-line effects, pp.73-74). Vision-transcribed "
    "from the PDF page images because the OCR text layer is corrupt."
)
PAGES = "73-88"
SEED_PAGE = 88  # Table 2-1 "Epic Seeds"
SEED_NOTE = ("Spellcasters without at least 24 ranks in Knowledge (religion) "
             "may not use the heal or life spell seeds (Table 2-1 footnote).")

# ---------------------------------------------------------------------------
# SEEDS — ELH Table 2-1 "Epic Seeds" (p.88). (name, base Spellcraft DC).
# 24 seeds, transcribed exactly off the rendered table image. Cross-checked
# against the sample spells' "Seed(s):" development lines (all agree).
# ---------------------------------------------------------------------------
_SEEDS = [
    ("Afflict", 14),
    ("Animate", 25),
    ("Animate Dead", 23),
    ("Armor", 14),
    ("Banish", 27),
    ("Compel", 19),
    ("Conceal", 17),
    ("Conjure", 21),
    ("Contact", 23),
    ("Delude", 14),
    ("Destroy", 29),
    ("Dispel", 19),
    ("Energy", 19),
    ("Foresee", 17),
    ("Fortify", 17),
    ("Heal", 25),
    ("Life", 27),
    ("Reflect", 27),
    ("Reveal", 19),
    ("Slay", 25),
    ("Summon", 14),
    ("Transform", 21),
    ("Transport", 27),
    ("Ward", 14),
]

# ---------------------------------------------------------------------------
# SAMPLE EPIC SPELLS — ELH pp.74-88.
# (name, spellcraft_dc, school, effect, page, note)
#   spellcraft_dc / school : off the full-entry header (the authoritative value).
#   effect                 : the one-line summary as printed in the "Epic Spells
#                            by Spellcraft DC" list (pp.73-74).
#   page                   : PDF/print page of the full-entry header.
#   note                   : records a summary-vs-entry DC discrepancy, else None.
# ---------------------------------------------------------------------------
_D = None  # readability alias for "no note"
_SPELLS = [
    ("Peripety", 27, "Abjuration",
     "Ranged attacks against you are reflected back on your attacker", 84, _D),
    ("Ruin", 27, "Transmutation",
     "Object or target takes 20d6 damage", 85, _D),
    ("Dreamscape", 29, "Transmutation [Teleportation]",
     "You physically travel the region of dreams", 77, _D),
    ("Mummy Dust", 35, "Necromancy [Evil]",
     "Create two Large 18 HD mummies", 83, _D),
    ("Dragon Knight", 38, "Conjuration (Summoning) [Fire]",
     "An adult red dragon appears and attacks your enemies", 77, _D),
    ("Origin of Species: Achaierai", 38, "Conjuration (Creation, Healing)",
     "Create a true-breeding creature", 84,
     "The 'Epic Spells by Spellcraft DC' summary list (p.73) prints DC 40; the "
     "full entry (p.84) prints DC 38 (used here)."),
    ("Eclipse", 42, "Conjuration (Creation)",
     "A solar eclipse follows you", 78, _D),
    ("Let Go of Me", 43, "Transmutation",
     "Grappler takes 20d6 damage, you take 10d6", 81, _D),
    ("Greater Spell Resistance", 45, "Transmutation",
     "Subject gains SR 35 for 20 hours", 80, _D),
    ("Spell Worm", 45, "Enchantment (Compulsion) [Mind-Affecting]",
     "Subject abandons all her spells", 86, _D),
    ("Epic Mage Armor", 46, "Conjuration (Creation) [Force]",
     "Subject gains +20 AC bonus", 79, _D),
    ("Raise Island", 48, "Conjuration (Creation)",
     "You create a small island in the sea", 85,
     "The summary list (p.73) prints DC 50; the full-entry (p.85) header (faded) "
     "reads DC 48 (used here)."),
    ("Animus Blast", 50, "Evocation [Cold]",
     "Victims of your 10d6 coldball animate as skeletons and serve you", 74, _D),
    ("Dragon Strike", 50, "Conjuration (Summoning) [Fire]",
     "Ten adult red dragons appear and attack your enemies", 77, _D),
    ("Lord of Nightmares", 50, "Conjuration (Summoning)",
     "You are possessed by a dream larva for 20 rounds and take 12d6 damage", 82, _D),
    ("Rain of Fire", 50, "Evocation [Fire]",
     "You create a 2-mile-radius fire storm dealing 1 point of fire damage per round", 85, _D),
    ("Contingent Resurrection", 52, "Conjuration (Healing)",
     "Subject automatically resurrected if slain", 74, _D),
    ("Epic Repulsion", 52, "Abjuration",
     "One creature or object is warded against one type of creature", 79, _D),
    ("Mass Frog", 55, "Transmutation",
     "All in 40-ft.-radius are transformed into frogs", 82, _D),
    ("Soul Scry", 55, "Divination",
     "You experience everything the target experiences", 86, _D),
    ("Crown of Vermin", 56, "Conjuration (Summoning)",
     "You have an aura of one thousand venomous vermin", 75, _D),
    ("Verdigris", 58, "Transmutation",
     "100-ft-area overrun by tsunami of plant growth dealing 10d6 damage", 88, _D),
    ("Greater Ruin", 59, "Transmutation",
     "Object or target takes 35d6 damage", 80, _D),
    ("Superb Dispelling", 59, "Abjuration",
     "As greater dispelling, but +40 on check", 87, _D),
    ("Create Living Vault", 60, "Conjuration (Creation)",
     "You fashion a living vault attuned to you", 75, _D),
    ("Nailed to the Sky", 62, "Transmutation [Teleportation]",
     "Affix foe to the heavens", 83, _D),
    ("Safe Time", 64, "Transmutation [Teleportation]",
     "You contingently duck damage in a static time stream for 1 round", 85, _D),
    ("Epic Spell Reflection", 68, "Abjuration",
     "Creature or object permanently warded against spells", 80,
     "The summary list (p.73) prints DC 70; the full entry (p.80) prints DC 68 "
     "(used here)."),
    ("Epic Counterspell", 69, "Abjuration",
     "Cancel another's epic spell", 79, _D),
    ("Time Duplicate", 71, "Transmutation [Teleportation]",
     "You and your future self exist together for 1 round", 87, _D),
    ("Soul Dominion", 72, "Divination, Enchantment (Compulsion) [Mind-Affecting]",
     "You achieve remote control of the target", 86, _D),
    ("Summon Behemoth", 72, "Conjuration (Summoning)",
     "A behemoth appears and attacks your enemies", 86, _D),
    ("Animus Blizzard", 78, "Evocation [Cold]",
     "Victims of your 20d6 coldball animate as wights and serve you", 74, _D),
    ("Eidolon", 79, "Conjuration (Creation)",
     "Creates duplicate that shares your soul", 78, _D),
    ("Enslave", 80, "Enchantment (Compulsion) [Mind-Affecting]",
     "Subject is a permanent thrall", 79, _D),
    ("Demise Unseen", 82, "Necromancy [Death, Evil], Illusion [Figment]",
     "Animated ghoul of slain victim fools its companions that all is well", 76, _D),
    ("Momento Mori", 86, "Necromancy [Death]",
     "A thought that kills", 83, _D),
    ("Hellball", 90, "Evocation [Acid, Fire, Electricity, Sonic]",
     "You deal 10d6 each of acid, fire, electricity, and sonic damage, you take 10d6", 80, _D),
    ("Damnation", 97, "Enchantment (Compulsion) [Teleportation, Mind-Affecting]",
     "Send your foe to hell", 76, _D),
    ("Kinetic Control", 103, "Abjuration",
     "You store and redirect damage", 81, _D),
    ("Pestilence", 104, "Conjuration, Necromancy",
     "Inflict slimy doom on all creatures and plants in a half-mile-diameter area", 84,
     "The summary list (p.74) prints DC 102; the full entry (p.84) prints DC 104 "
     "(used here)."),
    ("Living Lightning", 140, "Evocation [Electricity]",
     "Spell can cast itself, dealing 10d6 electricity damage to foe", 82, _D),
    ("Eternal Freedom", 150, "Abjuration",
     "Permanent immunity to many hold, stun, stasis and other spells and effects", 80, _D),
    ("Verdigris Tsunami", 170, "Transmutation",
     "1,000-ft.-radius area overrun by permanent tsunami of plant growth dealing 40d6 damage", 88, _D),
    ("Dire Winter", 319, "Evocation [Cold]",
     "1,000-ft. radius emanation deals 2d6 cold damage for 20 hours", 76, _D),
    ("Vengeful Gaze of God", 419, "Transmutation",
     "Target takes 305d6 damage; you take 200d6", 87, _D),
]


@dataclass
class EpicSpellEntry:
    name: str
    kind: str  # "seed" | "spell"
    book: str
    spellcraft_dc: int
    school: Optional[str]
    effect: Optional[str]
    citation: str
    page: int
    note: Optional[str] = None


def build() -> List[EpicSpellEntry]:
    out: List[EpicSpellEntry] = []
    seen = set()
    for name, dc in _SEEDS:
        key = ("seed", name.lower())
        if key in seen:
            continue
        seen.add(key)
        note = SEED_NOTE if name in ("Heal", "Life") else None
        out.append(EpicSpellEntry(name=name, kind="seed", book=BOOK,
                                  spellcraft_dc=dc, school=None, effect=None,
                                  citation=CITATION, page=SEED_PAGE, note=note))
    for name, dc, school, effect, page, note in _SPELLS:
        key = ("spell", name.lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(EpicSpellEntry(name=name, kind="spell", book=BOOK,
                                  spellcraft_dc=dc, school=school, effect=effect,
                                  citation=CITATION, page=page, note=note))
    return out


def write_index() -> int:
    entries = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    from collections import Counter
    by_kind = Counter(e.kind for e in entries)
    seeds = [e for e in entries if e.kind == "seed"]
    spells = sorted((e for e in entries if e.kind == "spell"),
                    key=lambda e: (e.spellcraft_dc, e.name))

    md: List[str] = [
        "# EPIC SPELL INDEX — The New Path",
        "",
        "**Generated by `scripts/epic_spell_harvest.py`. Do not hand-edit; rerun",
        "the harvest.** D&D 3.5 epic spells from the Epic Level Handbook (Chapter",
        "2, 'Epic Spells'). **Vision-transcribed from the PDF page images** because",
        "the book's OCR text layer is corrupt — this is still book RAW, read",
        "directly off the page. Two kinds of entry: **seeds** (the base building",
        "blocks, Table 2-1, with a base Spellcraft DC) and **sample spells** (each",
        "with school, the development Spellcraft DC, and the one-line effect as",
        "printed in the 'Epic Spells by Spellcraft DC' summary). Where the summary",
        "list's DC disagrees with a full-entry header, the full-entry value is used",
        "and the summary's number is noted.",
        "",
        f"*{len(entries)} entries — {by_kind.get('seed', 0)} seeds, "
        f"{by_kind.get('spell', 0)} sample spells.*",
        "",
        "## Epic seeds (Table 2-1, ELH p.88)",
        "",
        "| Seed | Base Spellcraft DC | Note |",
        "|---|---|---|",
    ]
    for e in sorted(seeds, key=lambda e: e.name):
        md.append(f"| {e.name} | {e.spellcraft_dc} | {'heal/life: 24+ ranks Know(religion)' if e.note else ''} |")
    md += [
        "",
        "## Sample epic spells (ELH pp.73-88)",
        "",
        "| Epic Spell | Spellcraft DC | School | Effect | Page |",
        "|---|---|---|---|---|",
    ]
    for e in spells:
        eff = e.effect or ""
        if e.note:
            eff = eff + " *(see note)*"
        md.append(f"| {e.name} | {e.spellcraft_dc} | {e.school or '—'} | {eff} | {e.page} |")
    md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    OUT_JSON.write_text(
        json.dumps({"generated_by": "scripts/epic_spell_harvest.py",
                    "book": BOOK, "citation": CITATION, "pages": PAGES,
                    "note": ("Vision-transcribed from the ELH PDF page images; the "
                             "OCR text layer is corrupt. Book RAW, read off the "
                             "page. Seed base DCs from Table 2-1 (p.88); sample "
                             "spells' school + Spellcraft DC from the full "
                             "descriptions (pp.74-88); one-line effects from the "
                             "'Epic Spells by Spellcraft DC' summary (pp.73-74)."),
                    "total_entries": len(entries),
                    "by_kind": dict(by_kind),
                    "entries": [asdict(e) for e in entries]}, indent=1),
        encoding="utf-8")
    return len(entries)


def selftest() -> int:
    failures: List[str] = []
    entries = build()
    seeds = {e.name: e for e in entries if e.kind == "seed"}
    spells = {e.name: e for e in entries if e.kind == "spell"}

    # both kinds present, in force
    if len(seeds) < 20:
        failures.append(f"only {len(seeds)} seeds; Table 2-1 lists 24")
    if len(spells) < 40:
        failures.append(f"only {len(spells)} sample spells; the book gives ~46")
    if len(entries) < 60:
        failures.append(f"only {len(entries)} total entries; expected ~70")

    # known seeds with exact base DCs (cross-checked against To Develop lines)
    for name, dc in (("Energy", 19), ("Destroy", 29), ("Summon", 14),
                     ("Ward", 14), ("Conjure", 21), ("Animate Dead", 23),
                     ("Life", 27)):
        s = seeds.get(name)
        if not s:
            failures.append(f"missing seed '{name}'")
        elif s.spellcraft_dc != dc:
            failures.append(f"seed '{name}' base DC {s.spellcraft_dc}, expected {dc}")

    # known sample spells with exact DCs
    for name, dc in (("Hellball", 90), ("Vengeful Gaze of God", 419),
                     ("Dire Winter", 319), ("Momento Mori", 86),
                     ("Epic Mage Armor", 46), ("Ruin", 27)):
        sp = spells.get(name)
        if not sp:
            failures.append(f"missing sample spell '{name}'")
        elif sp.spellcraft_dc != dc:
            failures.append(f"spell '{name}' DC {sp.spellcraft_dc}, expected {dc}")

    # the heal/life footnote landed
    if seeds.get("Heal") and not seeds["Heal"].note:
        failures.append("heal seed missing the Knowledge (religion) footnote")

    # discrepancy notes recorded on the four known mismatches
    for name in ("Origin of Species: Achaierai", "Raise Island",
                 "Epic Spell Reflection", "Pestilence"):
        if spells.get(name) and not spells[name].note:
            failures.append(f"'{name}' should carry a summary-vs-entry DC note")

    # every sample spell has a school + effect; every entry a positive DC
    for e in entries:
        if e.spellcraft_dc <= 0:
            failures.append(f"'{e.name}' has non-positive Spellcraft DC")
        if e.kind == "spell" and not e.school:
            failures.append(f"sample spell '{e.name}' missing school")
        if e.kind == "spell" and not e.effect:
            failures.append(f"sample spell '{e.name}' missing effect")

    # no duplicate (kind, name)
    keys = [(e.kind, e.name.lower()) for e in entries]
    if len(set(keys)) != len(keys):
        failures.append("duplicate (kind, name) entries")

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
        hits = [e for e in build()
                if q in e.name.lower()
                or (e.school and q in e.school.lower())
                or (e.effect and q in e.effect.lower())]
        for e in sorted(hits, key=lambda e: (e.kind, e.spellcraft_dc, e.name)):
            if e.kind == "seed":
                print(f"  [seed]  {e.name} — base Spellcraft DC {e.spellcraft_dc} (p.{e.page})")
            else:
                print(f"  [spell] {e.name} — DC {e.spellcraft_dc}, {e.school} "
                      f"— {e.effect} (p.{e.page})")
        print(f"{len(hits)} match(es).")
        return 0 if hits else 1

    n = write_index()
    print(f"{n} D&D 3.5 epic spell entries (Epic Level Handbook, Chapter 2, "
          f"vision-transcribed): 24 seeds + 46 sample spells.")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
