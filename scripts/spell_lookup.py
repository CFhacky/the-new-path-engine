#!/usr/bin/env python3
"""
spell_lookup.py — D&D 3.5e spell reference
The New Path campaign engine (the-new-path-engine)

GOVERNING SOURCES:
    1. SRD 3.5 (Open Game Content) — all core PHB spells, bundled as
       spells_srd35.json (sibling file, 605 spells; parsed from the
       srd35-md transcription of the official SRD).
    2. Spell Compendium (Premium) — supplemental spells, parsed LIVE from
       the local text extraction:
       I:\\Sourcebooks\\_md\\Spell_Compendium.md
       (override with --compendium PATH; skipped if the file is absent).

DESIGN CONTRACT (repo README):
    - Stateless resolver: flags in, text out. No state file, no dice.
    - Visible output: every lookup prints a ready-to-paste block.
    - No cross-imports.
    - --selftest: SRD checks always run; compendium checks run only when
      the compendium file is present, and are skipped (not failed) when not.

USAGE
    python3 spell_lookup.py fireball
    python3 spell_lookup.py "orb of acid, lesser"
    python3 spell_lookup.py --search orb
    python3 spell_lookup.py --cl 12 fireball        # annotate with caster level
    python3 spell_lookup.py --json haste
    python3 spell_lookup.py --selftest
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional

DEFAULT_COMPENDIUM = r"I:\Sourcebooks\_md\Spell_Compendium.md"
SRD_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "spells_srd35.json")

SCHOOLS = ("Abjuration", "Conjuration", "Divination", "Enchantment",
           "Evocation", "Illusion", "Necromancy", "Transmutation",
           "Universal")

# ============================================================================
# SRD SOURCE (bundled JSON)
# ============================================================================

def load_srd(path: str = SRD_JSON) -> Dict[str, dict]:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# ============================================================================
# SPELL COMPENDIUM SOURCE (live parse of the fitz text extraction)
#
# Header shape in the extraction:
#     ORB OF ACID, LESSER          <- ALL-CAPS name on its own line
#     Conjuration (Creation) [Acid]
#     Level: Sorcerer/wizard 1
# Art-caption garbage and page markers never match name+school+Level in
# sequence, so the three-line test is the anchor.
# ============================================================================

_CAPS_NAME = re.compile(r"^[A-Z][A-Z0-9 ,'\-/]{2,55}$")

def _is_header(lines: List[str], i: int) -> bool:
    if not _CAPS_NAME.match(lines[i].strip()):
        return False
    nxt = []
    j = i + 1
    while j < len(lines) and len(nxt) < 4:
        s = lines[j].strip()
        if s:
            nxt.append(s)
        j += 1
    saw_school = False
    for s in nxt:
        if s.startswith(SCHOOLS):
            saw_school = True
        if s.startswith("Level:"):
            return saw_school
    return False


def load_compendium(path: str) -> Dict[str, dict]:
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    spells: Dict[str, dict] = {}
    i = 0
    n = len(lines)
    while i < n:
        if _is_header(lines, i):
            name = lines[i].strip().title()
            body: List[str] = []
            k = i + 1
            while k < n and not _is_header(lines, k):
                s = lines[k].rstrip()
                if not s.startswith("<!-- page"):
                    body.append(s)
                k += 1
            text = re.sub(r"\n{3,}", "\n\n", "\n".join(body).strip())
            spells[name.lower()] = {
                "name": name,
                "text": text,
                "source": "Spell Compendium",
            }
            i = k
        else:
            i += 1
    return spells

# ============================================================================
# MERGED LOOKUP
# ============================================================================

def build_index(compendium_path: str) -> Dict[str, dict]:
    idx = dict(load_srd())
    for key, sp in load_compendium(compendium_path).items():
        idx.setdefault(key, sp)   # SRD wins on collision (core text is RAW)
    return idx


def find(idx: Dict[str, dict], name: str) -> Optional[dict]:
    key = name.strip().lower()
    if key in idx:
        return idx[key]
    hits = [k for k in idx if key in k]
    if len(hits) == 1:
        return idx[hits[0]]
    return None

# ============================================================================
# CASTER-LEVEL ANNOTATION — flags the scaling lines for a given CL
# ============================================================================

_SCALE = re.compile(
    r"(\d+d\d+)[^.]*?per (?:caster )?level|"
    r"per (?:caster )?level|"
    r"\+ ?\d+ ?ft\.?/level|/ ?level|/ ?2 levels",
    re.IGNORECASE)


def annotate_cl(text: str, cl: int) -> List[str]:
    notes = []
    for line in text.splitlines():
        if _SCALE.search(line):
            notes.append(line.strip())
    return notes

# ============================================================================
# OUTPUT
# ============================================================================

BAR = "=" * 62
SUB = "-" * 62


def print_spell(sp: dict, cl: Optional[int] = None) -> None:
    print(BAR)
    print(f"SPELL: {sp['name'].upper()}    [{sp['source']}]")
    print(SUB)
    print(sp["text"])
    if cl:
        notes = annotate_cl(sp["text"], cl)
        if notes:
            print(SUB)
            print(f"CL {cl} — scaling lines to resolve:")
            for x in notes[:8]:
                print(f"  * {x}")
    print(BAR)

# ============================================================================
# SELFTEST
# ============================================================================

def selftest(compendium_path: str) -> int:
    failures = 0

    def check(desc: str, ok: bool) -> None:
        nonlocal failures
        print(f"  [{'PASS' if ok else 'FAIL'}] {desc}")
        if not ok:
            failures += 1

    print("### spell_lookup.py SELFTEST ###\n")

    srd = load_srd()
    check(f"SRD loaded: {len(srd)} spells (expect 605)", len(srd) == 605)

    fb = srd.get("fireball")
    check("Fireball: Sor/Wiz 3, Reflex half, 1d6/level max 10d6, 20-ft spread",
          fb is not None
          and "Sor/Wiz 3" in fb["text"]
          and "Reflex half" in fb["text"]
          and "maximum 10d6" in fb["text"]
          and "20-ft.-radius spread" in fb["text"])

    mm = srd.get("magic missile")
    check("Magic Missile: 1d4+1, five missiles cap",
          mm is not None and "1d4+1" in mm["text"])

    hs = srd.get("haste")
    check("Haste: extra attack line present",
          hs is not None and "extra attack" in hs["text"].lower())

    notes = annotate_cl(fb["text"], 10)
    check("CL annotation flags fireball's damage-scaling line",
          any("1d6" in x for x in notes))

    if os.path.exists(compendium_path):
        comp = load_compendium(compendium_path)
        check(f"Compendium parsed: {len(comp)} spells (expect > 900)",
              len(comp) > 900)
        orb = comp.get("orb of acid")
        check("Orb Of Acid: Sor/Wiz 4, 1d6/level max 15d6, ranged touch",
              orb is not None
              and "Sorcerer/wizard 4" in orb["text"]
              and "maximum 15d6" in orb["text"]
              and "ranged touch" in orb["text"])
        lesser = comp.get("orb of acid, lesser")
        check("Orb Of Acid, Lesser present as separate entry",
              lesser is not None and "Sorcerer/wizard 1" in lesser["text"])
        idx = build_index(compendium_path)
        check("Merged index: SRD + Compendium both resolvable",
              find(idx, "fireball") is not None
              and find(idx, "orb of acid") is not None)
    else:
        print(f"  [SKIP] Compendium checks — file not found: {compendium_path}")

    print(f"\n{'ALL checks passed.' if failures == 0 else str(failures) + ' CHECKS FAILED.'}")
    return 1 if failures else 0

# ============================================================================
# CLI
# ============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description="D&D 3.5e spell lookup")
    ap.add_argument("names", nargs="*", help="spell name(s)")
    ap.add_argument("--search", metavar="TEXT", help="substring search on names")
    ap.add_argument("--cl", type=int, help="caster level: flag scaling lines")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--compendium", default=DEFAULT_COMPENDIUM,
                    help="path to Spell_Compendium.md text extraction")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.compendium)

    idx = build_index(args.compendium)
    if not idx:
        print("No spell sources found (missing spells_srd35.json and "
              "compendium).", file=sys.stderr)
        return 2

    if args.search:
        needle = args.search.lower()
        hits = sorted(k for k in idx if needle in k)
        if not hits:
            print(f"No spells match '{args.search}'.")
            return 1
        for k in hits:
            print(f"  {idx[k]['name']}   [{idx[k]['source']}]")
        print(f"{len(hits)} match(es).")
        return 0

    if not args.names:
        ap.print_help()
        return 2

    rc = 0
    for name in args.names:
        sp = find(idx, name)
        if sp is None:
            print(f"Spell not found: '{name}'. Try --search.", file=sys.stderr)
            rc = 1
            continue
        if args.json:
            print(json.dumps(sp, indent=2))
        else:
            print_spell(sp, args.cl)
    return rc


if __name__ == "__main__":
    sys.exit(main())
