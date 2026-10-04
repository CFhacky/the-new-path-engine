#!/usr/bin/env python3
"""corpus-mass-translator pipeline for the Warhammer Dwarf weapon-rune corpus (harvest -> triage -> convert -> register).
State: ./_translation_state.json (skill schema). Idempotent; state written after every entity.
Usage: python wow_pipeline.py all
Rules: ../FUSED_ENGINE_RESOLUTION.md; conventions and rate card: wh_translations.py header (Crusader, Registry section 2).
Tier rule (stated before conversion): bonus-equivalent +1 -> Tier 4 (levels 5-8), +2 -> Tier 3 (levels 9-12), +3 -> Tier 2 (13-16).
Relevance 0-10: +1 loot-economy fit; +2 tier 3-4 (party-relevant now); +3 necromancy/undead-adjacent; +1 NEW (fills an empty slot);
+1 usable by any martial wielder, -1 needs a class, a caster or a resource the party lacks.
"""
import datetime, hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wh_translations import T

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
STATE = os.path.join(HERE, "_translation_state.json")
PACKET = os.path.join(HERE, "sources", "dwarf_weapon_runes.txt")
OUT = os.path.join(ROOT, "entities", "warhammer_runes")
TIER = {2: "Heroic Elite (levels 13-16)", 3: "Heroic (levels 9-12)", 4: "Competent (levels 5-8)"}
CASTER = set()
CLASSLOCK = {"Master Rune of Kragg the Grim"}
NECRO = {"Master Rune of Banishment", "Master Rune of Death"}
slug = lambda n: re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
today = lambda: datetime.date.today().isoformat()


def save(st):
    st["last_updated"] = today(); tmp = STATE + ".tmp"
    json.dump(st, open(tmp, "w", encoding="utf-8"), indent=1, ensure_ascii=False); os.replace(tmp, STATE)


def harvest(st):
    blocks = re.split(r"^=== (.+?) ===\n", open(PACKET, encoding="utf-8").read(), flags=re.M)[1:]
    have = {c["candidate_id"] for c in st["candidates"]}; n = 0
    for name, body in zip(blocks[0::2], blocks[1::2]):
        f = dict(re.findall(r"^(group|quality|url|tooltip|facts|gaps): (.*)$", body, flags=re.M))
        cid = hashlib.sha1(f"wh|{f['url']}|{name}".encode()).hexdigest()[:12]
        if cid in have: continue
        st["candidates"].append(dict(candidate_id=cid, name=name, source_book="Warhammer Armies Dwarfs (PDF Room)", source_page=f["url"], category="weapon_rune",
            scale="wfb_special_rules", verbatim_block=body.strip(), extraction_quality=f["quality"], group=f["group"], status="harvested",
            superseded_by=None, tier=None, relevance=None, rank=None, output_path=None, note=None)); have.add(cid); n += 1
    st["books"]["Warhammer Armies Dwarfs (PDF Room)"] = dict(status="swept", candidates_found=n, swept_on=today())
    st["phase_status"]["harvest"] = dict(status="done", books_swept=1, books_total=1)
    save(st); return n


def triage(st):
    for c in st["candidates"]:
        t = T.get(c["name"])
        if not t: c["status"], c["note"] = "blocked", "no translation entry"; continue
        c["pool_verdict"], c["pool_row"] = t["verdict"], t["base"]
        if t["verdict"] == "COVERED":
            c["status"], c["note"] = "duplicate_of_catalog", f"covered by existing Registry row: {t['base']}"; c["tier"] = None; continue
        c["tier"] = t.get("tier") or {1: 4, 2: 3, 3: 2}[t["bonus"]]; c["price"] = t.get("price") or f"+{t['bonus']} = {t['bonus']**2*2000:,} gp"
        rel = 1 + (2 if c["tier"] >= 3 else 1) + (3 if c["name"] in NECRO else 0) + (1 if t["verdict"] == "NEW" else 0)
        rel += -1 if (c["name"] in CASTER or c["name"] in CLASSLOCK) else 1
        c["relevance"] = max(0, min(10, rel)); c["status"] = "queued"
    q = sorted((c for c in st["candidates"] if c["status"] == "queued"), key=lambda c: (-c["relevance"], c["tier"], c["extraction_quality"] == "degraded", c["name"]))
    for i, c in enumerate(q, 1): c["rank"] = i
    st["phase_status"]["triage"] = dict(status="done", candidates_triaged=sum(1 for c in st["candidates"] if c["status"] != "harvested"))
    st["phase_status"]["convert"]["worklist_total"] = len(q); save(st); return q


def entity(c, t):
    L = [f"# {c['name'].upper()}", f"**Warhammer Dwarf weapon rune — {c['group']} ({c['source_page']})**",
         f"**Tier {c['tier']} — {TIER[c['tier']]}** (rule in `wow_pipeline.py`; price {c['price']})", "",
         "## SOURCE (as fetched; see packet header: extraction, not byte-exact)", "```", c["verbatim_block"], "```", "",
         "## D&D 3.5e", t["three_e"], "", "## GURPS 4e", t["gurps"], "",
         "**Engine crosswalk:** Gadget on the weapon (Breakable DR 6 -25%, Can Be Stolen grab-first -10%); dice read as-is; source seconds kept exact; "
         "riders ignore worn DR; no GURPS point total on affix entries (FUSED_ENGINE_RESOLUTION.md).", "",
         "## PRICE", f"{c['price']} (bonus-equivalent squared x 2,000 gp; Crusader rate card).", "",
         "## POOL COVERAGE / DEDUPE", f"Verdict: {t['verdict']}. Existing row: {t['base']}.", "",
         "## NAME COLLISION", t["collision"], "", "## FORKS NEEDING A RULING", t["forks"], "",
         "## CONVERSION NOTES", f"Anchor: Crusader (ratified, Registry section 2). Conventions: `wh_translations.py` header. Extraction quality: {c['extraction_quality']}.", ""]
    return "\n".join(L)


def convert(st):
    os.makedirs(OUT, exist_ok=True); n = 0
    for c in sorted((c for c in st["candidates"] if c["status"] in ("queued", "in_progress")), key=lambda c: c["rank"]):
        c["status"] = "in_progress"; save(st)
        p = os.path.join(OUT, slug(c["name"]) + ".md"); open(p, "w", encoding="utf-8").write(entity(c, T[c["name"]]))
        c["status"], c["output_path"] = "converted", os.path.relpath(p, ROOT); n += 1; save(st)
    st["phase_status"]["convert"].update(status="done", converted=sum(1 for c in st["candidates"] if c["status"] == "converted")); save(st); return n


def register(st):
    for c in st["candidates"]:
        if c["status"] == "converted" and os.path.exists(os.path.join(ROOT, c["output_path"])): c["status"] = "registered"
    reg = sorted((c for c in st["candidates"] if c["status"] == "registered"), key=lambda c: (c["tier"], c["name"]))
    dup = sorted((c for c in st["candidates"] if c["status"] == "duplicate_of_catalog"), key=lambda c: c["name"])
    rows = ["# MASTER INDEX — WARHAMMER DWARF WEAPON RUNE CORPUS", "## Dwarf runic weapons (WFB): master runes and stacking weapon runes", "",
            "Deliverable: `WARHAMMER_RUNE_COMPENDIUM.md`. Entity files under `entities/warhammer_runes/`. State: `warhammer_runes/_translation_state.json`.", "",
            "| Entity | Source | Category | Tier | 3.5e | GURPS | File |", "|---|---|---|:-:|:-:|:-:|---|"]
    rows += [f"| {c['name']} | {c['group']} | Weapon rune | {c['tier']} | Y | Y | `{c['output_path']}` |" for c in reg]
    rows += ["", f"**Registered: {len(reg)}** · Duplicates of Registry pool rows (no second document): {len(dup)} · Candidates: {len(st['candidates'])} (1/1 sources swept; armour, talismanic, banner and engineering runes not weapon enchants)"]
    open(os.path.join(ROOT, "MASTER_INDEX_WARHAMMER_RUNES.md"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    assert len(reg) == sum(1 for r in rows if "| Y | Y |" in r)
    flags = [f"{c['name']}: degraded source (summary only; no verbatim tooltip or proc rate)" for c in reg if c["extraction_quality"] == "degraded"]
    flags += [f"{c['name']}: forks listed in its entry" for c in reg if T[c["name"]]["forks"].strip() not in ("none.", "none")]
    cnt = {t: sum(1 for c in reg if c["tier"] == t) for t in (2, 3, 4)}
    out = ["# WARHAMMER DWARF WEAPON RUNE COMPENDIUM",
           f"**Corpus Mass Translation — Warhammer Fantasy Dwarf weapon runes (Warhammer Armies: Dwarfs, unofficial 9th-edition compilation, PDF Room scan, pp. 201-203). Built {today()}.**", "",
           "## HOW TO USE / TIER OVERVIEW",
           "Each entry: the source tooltip as fetched, the 3.5e rules, the GURPS crosswalk, price, pool coverage, collisions and forks. Rate card and rules: Crusader (Affix Registry section 2) and `docs/translation/FUSED_ENGINE_RESOLUTION.md`. "
           "Conventions used throughout: 1 / 2 / 3 copies of a rune = the Crusader rungs (Magic +1, Rare +2, Unique +3); +1 WS = +1 attack, +1 S = +2 Strength, armour-save modifiers = ignored DR, Multiple Wounds = extra weapon-damage rolls, Killing Blow = a Lethal-severity crit result on a confirmed natural 20; master runes are single-rung; the Rules of the Runes carry over; price = bonus-equivalent squared x 2,000 gp. "
           "`Registered` means indexed here; a Notion Registry family entry is written when an affix is first rolled or placed. Only the 21 weapon runes are here; armour, talismanic, banner and engineering runes are not weapon enchants, and WFRP runic weapons (Old World Armoury) were not read in this pass. The source is an unofficial compilation, not a Games Workshop product.", "",
           "| Tier | Registered |", "|---|---:|", *[f"| {t} {TIER[t].split(' (')[0]} | {cnt[t]} |" for t in (2, 3, 4)], ""]
    for t in (2, 3, 4):
        if cnt[t]:
            out += [f"## TIER {t} — {TIER[t].upper()}", ""]
            for c in (x for x in reg if x["tier"] == t):
                out += [re.sub(r"^# ", "### ", open(os.path.join(ROOT, c["output_path"]), encoding="utf-8").read(), count=1), "\n---\n"]
    out += ["## COVERED BY AN EXISTING REGISTRY ROW (no second document)", "", "| Enchant | Existing row | Note |", "|---|---|---|",
            *[f"| {c['name']} | {c['pool_row']} | {T[c['name']]['note']} |" for c in dup], "", "## OPEN VERIFICATION ITEMS", "", *[f"- {f}" for f in flags], ""]
    open(os.path.join(ROOT, "WARHAMMER_RUNE_COMPENDIUM.md"), "w", encoding="utf-8").write("\n".join(out))
    st["phase_status"]["register"] = dict(status="done", registered=len(reg)); save(st)
    return len(reg), len(dup), len(flags)


if __name__ == "__main__":
    st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else dict(corpus="warhammer_dwarf_weapon_runes", created=today(), last_updated=today(),
        phase_status=dict(harvest=dict(status="in_progress", books_swept=0, books_total=1), triage=dict(status="pending", candidates_triaged=0),
                          convert=dict(status="pending", converted=0, worklist_total=0), register=dict(status="pending", registered=0)), books={}, candidates=[], gaps=[])
    h = harvest(st); q = triage(st); n = convert(st); r = register(st)
    print(f"harvested +{h}; queued {len(q)}; converted +{n}; registered {r[0]}; duplicates {r[1]}; open items {r[2]}")
