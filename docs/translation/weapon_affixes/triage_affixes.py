#!/usr/bin/env python3
"""Phase 2 TRIAGE for the weapon-affix corpus. Reads _translation_state.json + ../AFFIX_LEXICON.md,
writes tier / relevance / rank / status back into the state file. Idempotent; prints the worklist.

Tier rule (stated before conversion; system-translator six-tier scale, item power -> wielder band):
  +1 bonus-equivalent or <= 8,000 gp flat -> Tier 4 (levels 5-8)
  +2 or <= 20,000 gp flat                 -> Tier 3 (levels 9-12)
  +3                                      -> Tier 2 (levels 13-16)
  +4, +5 or > 20,000 gp flat              -> Tier 1 (levels 17-20)
Relevance 0-10 (pipeline-phases rubric adapted to items):
  +1 loot-economy fit (every affix) | +2 tier 3-5 (usable at party level now) or +1 tier 1-2 (later)
  +3 necromancy / undead-adjacent (campaign spine) | +1 fills an empty Registry slot (verdict NEW)
  +1 usable by any martial wielder without a class feature | -2 INACTIVE (psionic/incarnum, no such PC)
  -1 needs a class feature or resource the party lacks | cap 10
Status: INACTIVE -> blocked; COVERED -> duplicate_of_catalog (named row); everything else queued.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "_translation_state.json")
LEX = os.path.join(HERE, "..", "AFFIX_LEXICON.md")
NECRO = {"Consumptive", "Enervating", "Souldrinking", "Soulbreaker", "Stygian", "Vampiric", "Bloodfeeding", "Bloodstone",
         "Body Feeder", "Cursespewing", "Disruption", "Domineering", "Doom Burst", "Weakening", "Profane", "Profane Burst",
         "Vicious", "Vorpal", "Wounding", "Implacable", "Necrotic Focus", "Unholy", "Unholy Surge", "Sacred", "Sacred Burst",
         "Heavenly Burst", "Divine Wrath", "Ghost Touch", "Ghost Strike", "Ethereal Reaver", "Incorporeal Binding"}
NEEDS_CLASS = {"Berserker", "Brash", "Deadly Precision", "Divine Wrath", "Dragondoom", "Harmonizing", "Hunting",
               "Ki Focus", "Mighty Cleaving", "Mighty Smiting", "Arcane Might", "Spell Storing", "Spellstrike"}


def lexicon():
    rows = {}
    for ln in open(LEX, encoding="utf-8"):
        if not ln.startswith("| ") or ln.startswith("| Affix") or ln.startswith("|---"):
            continue
        c = [x.strip() for x in ln.strip().strip("|").split(" | ")]
        if len(c) >= 8:
            rows[c[0]] = {"source": c[1], "verdict": c[2], "base": c[3], "note": c[4], "price": c[6], "flags": c[7]}
    return rows


def tier(price):
    m = re.search(r"\+(\d+)\s*=", price)
    if m:
        b = int(m.group(1)); return 4 if b <= 1 else 3 if b == 2 else 2 if b == 3 else 1
    m = re.search(r"([\d,]+)\s*gp", price)
    g = int(m.group(1).replace(",", "")) if m else 8000
    return 4 if g <= 8000 else 3 if g <= 20000 else 1


def main():
    st = json.load(open(STATE, encoding="utf-8")); lex = lexicon()
    names = {c["name"] for c in st["candidates"]}
    print("in state, not in lexicon:", sorted(names - set(lex)))
    print("in lexicon, not in state:", sorted(set(lex) - names))
    for c in st["candidates"]:
        r = lex.get(c["name"])
        if not r:
            c["status"], c["note"] = "blocked", "no lexicon row; reconcile name"; continue
        t = tier(r["price"]); inactive = "INACTIVE" in r["flags"]
        rel = 1 + (2 if t >= 3 else 1) + (3 if c["name"] in NECRO else 0) + (1 if r["verdict"] == "NEW" else 0)
        rel += (1 if c["name"] not in NEEDS_CLASS else -1) - (2 if inactive else 0)
        c["tier"], c["relevance"] = t, max(0, min(10, rel))
        c["pool_verdict"], c["pool_row"], c["price"] = r["verdict"], r["base"], r["price"]
        if inactive:
            c["status"], c["note"] = "blocked", "psionic/incarnum; inactive until such a character exists"
        elif r["verdict"] == "COVERED":
            c["status"], c["note"] = "duplicate_of_catalog", f"covered by existing Registry pool row: {r['base']}"
        else:
            c["status"] = "queued"
    q = sorted((c for c in st["candidates"] if c["status"] == "queued"),
               key=lambda c: (-c["relevance"], c["tier"], c["extraction_quality"] == "degraded", c["name"]))
    for i, c in enumerate(q, 1):
        c["rank"] = i
    ps = st["phase_status"]
    ps["harvest"]["status"] = "done" if ps["harvest"]["books_swept"] == ps["harvest"]["books_total"] else "in_progress"
    ps["triage"] = {"status": "done", "candidates_triaged": sum(1 for c in st["candidates"] if c["tier"] is not None)}
    ps["convert"]["worklist_total"] = len(q)
    st["last_updated"] = __import__("datetime").date.today().isoformat()
    json.dump(st, open(STATE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    import collections
    print(collections.Counter(c["status"] for c in st["candidates"]))
    print("tiers (queued):", sorted(collections.Counter(c["tier"] for c in q).items()))
    print("relevance (queued):", sorted(collections.Counter(c["relevance"] for c in q).items()))
    for c in q[:12]:
        print(f"  #{c['rank']:<3} T{c['tier']} rel{c['relevance']} {c['name']}")


if __name__ == "__main__":
    main()
