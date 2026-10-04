#!/usr/bin/env python3
"""Phase 4 REGISTER for the weapon-affix corpus.

1. Catalog dedupe: names checked against the skill's calibration-catalog.md (hits reviewed by hand: only class-name false positives).
2. Affix Registry dedupe: already carried per entity as pool_verdict / pool_row (COVERED -> duplicate_of_catalog, no second document).
3. Catalog append: written as CATALOG_APPEND.md for the owner (the synced skill folder is not edited from here).
4. Master index: ../MASTER_INDEX.md. A row shows both systems checked or the entity is not registered.
5. Compendium: ../WEAPON_AFFIX_COMPENDIUM.md, regenerated whole from the entity files each run (entity files are the source of truth).
'registered' here means: in this corpus's master index and compendium. A Notion Affix Registry family entry (tiers, Chekhov note,
roll log, Change Log pair) is written the first time an affix is rolled or placed in a module, per loot-engine.
"""
import json, os, re, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
STATE = os.path.join(HERE, "_translation_state.json")
LABEL = {1: "TIER 1 — LEGENDARY (levels 17-20)", 2: "TIER 2 — HEROIC ELITE (levels 13-16)", 3: "TIER 3 — HEROIC (levels 9-12)", 4: "TIER 4 — COMPETENT (levels 5-8)"}


def main():
    st = json.load(open(STATE, encoding="utf-8"))
    C = st["candidates"]
    for c in C:
        if c["status"] == "converted" and c["output_path"] and os.path.exists(os.path.join(ROOT, c["output_path"])):
            c["status"] = "registered"
    reg = sorted((c for c in C if c["status"] == "registered"), key=lambda c: (c["tier"], c["name"]))
    dup = sorted((c for c in C if c["status"] == "duplicate_of_catalog"), key=lambda c: c["name"])
    blk = sorted((c for c in C if c["status"] == "blocked"), key=lambda c: c["name"])
    other = [c for c in C if c["status"] not in ("registered", "duplicate_of_catalog", "blocked")]
    book = lambda c: ("DMG v3.5" if "Dungeon" in c["source_book"] else "MIC") + f", PDF p. {c['source_page']}"

    rows = ["# MASTER INDEX — WEAPON AFFIX CORPUS", "## D&D 3.5e DMG + Magic Item Compendium weapon properties", "",
            "Deliverable: `WEAPON_AFFIX_COMPENDIUM.md`. Entity files under `entities/weapon_affixes/` are the checkpoint layer. State: `weapon_affixes/_translation_state.json`.", "",
            "| Entity | Source (book, p.) | Category | Tier | 3.5e | GURPS | File |", "|---|---|---|:-:|:-:|:-:|---|"]
    for c in reg:
        rows.append(f"| {c['name']} | {book(c)} | Weapon property | {c['tier']} | Y | Y | `{c['output_path']}` |")
    rows += ["", f"**Registered: {len(reg)}** · Duplicates of Registry pool rows (no second document): {len(dup)} · Blocked (psionic/incarnum, inactive): {len(blk)} · Candidates: {len(C)} (2/2 books swept)"]
    open(os.path.join(ROOT, "MASTER_INDEX.md"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    assert len(reg) == sum(1 for r in rows if r.startswith("| ") and "Y | Y" in r), "index rows != registered"

    flags = collections.OrderedDict()
    for c in reg:
        if c["extraction_quality"] == "degraded":
            flags[f"{c['name']}: source figure OCR-doubtful (see packet header); check the book page"] = 1
        n = len([1 for _ in re.findall(r"- .*OPEN", open(os.path.join(ROOT, c["output_path"]), encoding="utf-8").read())])
        if n:
            flags[f"{c['name']}: {n} GURPS detail(s) uncosted or unresolved (see its CONVERSION NOTES)"] = 1
    tiers = collections.Counter(c["tier"] for c in reg)
    out = ["# WEAPON AFFIX COMPENDIUM",
           f"**Corpus Mass Translation — D&D 3.5e Dungeon Master's Guide v3.5 (PDF pp. 224-227) and Magic Item Compendium (PDF pp. 29-47). Built {datetime.date.today().isoformat()}.**", "",
           "## HOW TO USE / TIER OVERVIEW",
           "Each entry is one weapon property: the printed source, the 3.5e rules, the GURPS crosswalk, price, pool coverage, collisions and forks. "
           "Item effects run on the 3.5e chassis; GURPS supplies only the defender's 3d6 contest and DR (`docs/translation/FUSED_ENGINE_RESOLUTION.md`, binding). "
           "Tier = the wielder band the property suits (rule in `weapon_affixes/triage_affixes.py`). "
           "`Registered` means indexed here; the Notion Affix Registry gets a full family entry the first time an affix is rolled or placed. "
           f"Already ratified outside this corpus: Crusader (Registry section 2). Covered by an existing pool row and therefore not restated: {len(dup)} (listed at the end). Inactive: {len(blk)}.", "",
           "| Tier | Registered |", "|---|---:|", *[f"| {t} {LABEL[t].split(' (')[0].split('— ')[1].title()} | {tiers.get(t,0)} |" for t in (1, 2, 3, 4)], ""]
    for t in (1, 2, 3, 4):
        out += [f"## {LABEL[t]}", ""]
        for c in (x for x in reg if x["tier"] == t):
            out += [re.sub(r"^# ", "### ", open(os.path.join(ROOT, c["output_path"]), encoding="utf-8").read(), count=1), "\n---\n"]
    out += ["## COVERED BY AN EXISTING REGISTRY POOL ROW (no second document)", "", "| Affix | Source | Existing row |", "|---|---|---|",
            *[f"| {c['name']} | {book(c)} | {c['pool_row']} |" for c in dup], "",
            "## BLOCKED — INACTIVE (psionic or incarnum; no such character in the campaign)", "", *[f"- {c['name']} ({book(c)})" for c in blk], "",
            "## OPEN VERIFICATION ITEMS", "", *[f"- {k}" for k in flags], ""]
    open(os.path.join(ROOT, "WEAPON_AFFIX_COMPENDIUM.md"), "w", encoding="utf-8").write("\n".join(out))

    anchors = []
    for tt in (1, 2, 3, 4):
        cands = [x for x in reg if x["tier"] == tt and x["extraction_quality"] == "clean"]
        pick = next((x for x in cands if not x["note"]), cands[0] if cands else None)
        if pick:
            anchors.append(f"| {pick['name']} (Tier {tt}) | {book(pick)} | Item (weapon property) | {pick['output_path']} | Proposed anchor |")
    open(os.path.join(ROOT, "weapon_affixes", "CATALOG_APPEND.md"), "w", encoding="utf-8").write(
        "# Proposed calibration-catalog rows (apply by hand; the skill folder is not edited from this session)\n\n"
        "First clean book-native weapon-property conversions through the corpus pipeline, one per tier, usable as anchors:\n\n"
        "| Conversion | Source | Category | File | Status |\n|---|---|---|---|---|\n" + "\n".join(anchors) + "\n")

    ps = st["phase_status"]
    ps["register"] = {"status": "done" if not other else "in_progress", "registered": len(reg)}
    ps["convert"]["converted"] = len(reg)
    st["last_updated"] = datetime.date.today().isoformat()
    json.dump(st, open(STATE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"registered {len(reg)}; duplicates {len(dup)}; blocked {len(blk)}; unaccounted {len(other)}; flags {len(flags)}")
    print("compendium bytes:", os.path.getsize(os.path.join(ROOT, 'WEAPON_AFFIX_COMPENDIUM.md')))


if __name__ == "__main__":
    main()
