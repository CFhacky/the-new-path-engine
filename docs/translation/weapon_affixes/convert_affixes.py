#!/usr/bin/env python3
"""Phase 3 CONVERT for the weapon-affix corpus.

Per queued entity, in rank order: mark in_progress -> build the entity file from (a) the verbatim block in the
state file (the source) and (b) the corrected draft translation under ../affixes/ -> write
../entities/weapon_affixes/<Name>.md -> checkpoint the state entry (per entity, not per batch).
An entity whose draft lacks a 3.5e or a GURPS block stays in_progress, never converted.
Conversion rules: ../FUSED_ENGINE_RESOLUTION.md (binding).
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "_translation_state.json")
DRAFTS = os.path.join(HERE, "..", "affixes")
OUT = os.path.join(HERE, "..", "entities", "weapon_affixes")
TIER = {1: "Legendary (levels 17-20)", 2: "Heroic Elite (levels 13-16)", 3: "Heroic (levels 9-12)", 4: "Competent (levels 5-8)"}
MARK = re.compile(r"(?:(?<=^)|(?<=[\s.]))(Source text \(key facts[^)]*\)|Source|Pool|Existing pool coverage|Verdict|Translation identity|3\.5e/GURPS|3\.5e(?: \([^)]*\))?|GURPS(?: \([^)]*\))?|Pricing|Price|"
                  r"Name collision|Forks needing a ruling|Forks|Rulings?(?: \(final\))?|RULING(?: \(final\))?):")
# Mirror entries: same treatment as a converted base entry, with an explicit keying note (never silently copied).
ALIAS = {
    "AURAN": ("AQUAN", "Keyed to the EARTH subtype instead of fire: read every 'fire subtype' in the Aquan text as 'earth subtype'."),
    "IGNAN": ("AQUAN", "Keyed to the WATER subtype instead of fire: read every 'fire subtype' in the Aquan text as 'water subtype'."),
    "TERRAN": ("AQUAN", "Keyed to the AIR subtype instead of fire: read every 'fire subtype' in the Aquan text as 'air subtype'."),
    "UNHOLY SURGE": ("HOLY SURGE", "Mirror of Holy Surge: read holy as unholy, 'evil target' as 'good-aligned target'; synergy prerequisite is Unholy; same 1 + Cha bonus uses per day, no other change."),
    "DISLOCATOR, GREAT": ("DISLOCATOR", "Great rung only: the target is teleported up to 30 feet (Will DC 20 negates) instead of 10 feet (DC 17); synergy prerequisite Dislocator; +1 bonus on top, as printed."),
}
# Engine-grounded text for drafts that had no GURPS block (FUSED_ENGINE_RESOLUTION.md: crits cannot be defended; riders ignore worn DR;
# burst dice follow the weapon's own multiplier class; conditions resolve as a Quick Contest at the printed DC; no point totals).
SUPP = {
    "ENERVATING": {"GURPS": "Trigger: a confirmed critical hit on a living creature (crits are undefended, so no defender 3d6 roll). Effect: one Energy Drained negative level (-1 attacks/saves/skills/ability checks, -5 HP, -1 effective level); no save printed, none added. Fades after 1 hour; never becomes level loss. Repeated crits add one level each, additive. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted."},
    "STYGIAN": {"GURPS": "Swift (mental) activation, 3/day. The next attack that lands before the end of your turn (it still has to beat the defender's 3d6 Parry/Block/Dodge contest as any attack) bestows one Energy Drained negative level for 10 minutes, on top of normal damage; no save printed, none added; never becomes level loss. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted."},
    "SACRED BURST": {"3.5e": "As printed over Sacred: on a critical hit, extra positive-energy damage by the weapon's own multiplier class (x2 1d10, x3 2d10, x4 3d10; evil outsider 2d10 / 4d10 / 6d10), even against crit-immune targets; only the target is harmed unless you are undead (then 1d4 Cha damage to you); continuous.",
                     "GURPS": "Rider on a confirmed crit (undefended): dice by multiplier class 1d / 2d / 3d, doubled against an evil outsider, ignoring worn DR; works against crit-immune targets; undead wielder takes 1d4 Cha as the burst cost. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted."},
    "SCREAMING BURST": {"3.5e": "As printed over Screaming: on a critical hit, extra sonic damage by the weapon's own multiplier class (x2 1d8, x3 2d8, x4 3d8), even against crit-immune targets; only the target is harmed; continuous.",
                        "GURPS": "Rider on a confirmed crit (undefended): sonic dice by multiplier class 1d / 2d / 3d, ignoring worn DR; works against crit-immune targets. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted."},
    "SLOW BURST": {"3.5e": "As printed: on a critical hit the target is slowed (as the slow spell) for 3 rounds, Will DC 14 negates, even against crit-immune targets. Price printed 5,000 gp flat.",
                   "GURPS": "On a confirmed crit (undefended) the target resists with a Quick Contest of Will against effective skill 14 (the printed DC); on failure Affliction (Reduced Move, the Slowing-row mechanism) for 3 turns. Gadget chassis Breakable -25% / Can Be Stolen -10%; uncosted."},
}

slug = lambda n: re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")


def fields(text):
    parts = MARK.split(text)
    out = {}
    for i in range(1, len(parts) - 1, 2):
        k = parts[i].split(" (")[0].strip() if not parts[i].startswith("Source text") else "Source"
        k = {"Source text": "Source", "Pricing": "Price", "Existing pool coverage": "Pool", "Forks needing a ruling": "Forks",
             "Rulings": "Rulings", "Ruling": "Rulings", "RULING": "Rulings"}.get(k, k)
        for kk in (("3.5e", "GURPS") if k == "3.5e/GURPS" else (k,)):
            out.setdefault(kk, "")
            out[kk] += (" " if out[kk] else "") + parts[i + 1].strip()
    return out


def load_drafts():
    d = {}
    for f in sorted(os.listdir(DRAFTS)):
        p = os.path.join(DRAFTS, f)
        if f.endswith(".md") and os.path.isfile(p):                       # DMG: one ability per file
            body = open(p, encoding="utf-8").read()
            m = re.match(r"# (.+?) — ", body)
            if m:
                d[m.group(1).strip().upper()] = fields(body.split("\n", 2)[2])
    mic = os.path.join(DRAFTS, "mic")
    for f in sorted(os.listdir(mic)):
        for sec in re.split(r"^## ", open(os.path.join(mic, f), encoding="utf-8").read(), flags=re.M)[1:]:
            head, _, body = sec.partition("\n")
            name = re.split(r" \(| — ", head)[0].strip().upper()
            d[name] = fields(body)
            d[name]["_head"] = head
    return d


def header(block):
    h = {}
    for k in ("Price", "Price (Item Level)", "Property", "Caster Level", "Aura", "Activation", "Synergy Prerequisite", "Prerequisites", "Cost to Create"):
        m = re.search(rf"^{re.escape(k)}: (.+)$", block, re.M)
        if m:
            h[k] = m.group(1).strip()
    return h


def build(c, dr):
    h, f = header(c["verbatim_block"]), dr
    opens = [s.strip() for s in re.split(r"(?<=[.;])\s", f.get("GURPS", "")) if "OPEN" in s]
    L = [f"# {c['name'].upper()}",
         f"**Weapon property — {c['source_book'].split('/')[-1].replace('.md','')}, PDF p. {c['source_page']} (3.5e source; printed rules are the 3.5e side)**",
         f"**Tier {c['tier']} — {TIER[c['tier']]}** (tier rule in `triage_affixes.py`; price {c['price']})", "",
         "## SOURCE (verbatim, see packet header for normalization)", "```", c["verbatim_block"], "```", "",
         "## D&D 3.5e", "**Printed header:** " + "; ".join(f"{k}: {v}" for k, v in h.items()), "",
         "**As printed:** the source block above is the rule text.", ""]
    if f.get("3.5e"):
        L += ["**Campaign adaptation (engine-bound):** " + f["3.5e"], ""]
    L += ["## GURPS 4e", f.get("GURPS", "(no GURPS block in the draft)"), "",
          "**Engine crosswalk (FUSED_ENGINE_RESOLUTION.md):** item effects run on the 3.5e chassis; damage dice read as-is; "
          "conditions resolve as a Quick Contest of the target's HT or Will against the printed DC used as effective skill; "
          "extra damage riders ignore worn DR; gadget chassis Breakable -25% / Can Be Stolen -10%; no GURPS point total on affix entries.", ""]
    if f.get("Price"):
        L += ["## PRICE", f["Price"], ""]
    L += ["## POOL COVERAGE / DEDUPE", f"Verdict: {c['pool_verdict']}. Existing row: {c['pool_row']}.", f.get("Pool", ""), ""]
    for k, t in (("Name collision", "NAME COLLISION"), ("Forks", "FORKS"), ("Rulings", "RULINGS")):
        if f.get(k):
            L += [f"## {t}", f[k], ""]
    L += ["## CONVERSION NOTES",
          f"Scale: dnd35_srd_prose (book-native 3.5e). Anchor: Crusader (ratified, Registry section 2) for format and rate card. Extraction quality: {c['extraction_quality']}.",
          "Open items (non-blocking under the engine resolution, GURPS point totals and percentages are uncosted by design):" if opens else "No open items.",
          *[f"- {o}" for o in opens], ""]
    return "\n".join(L), opens


def main():
    st = json.load(open(STATE, encoding="utf-8")); dr = load_drafts()
    os.makedirs(OUT, exist_ok=True)
    work = sorted((c for c in st["candidates"] if c["status"] in ("queued", "in_progress")), key=lambda c: c["rank"] or 9999)
    done = short = 0
    for c in work:
        c["status"] = "in_progress"; save(st)
        name = c["name"].upper(); d = dr.get(name)
        if name in ALIAS:
            base = dr.get(ALIAS[name][0])
            if base:
                d = dict(base); d["3.5e"] = ALIAS[name][1] + " " + base.get("3.5e", "")
        if name in SUPP:
            d = {**(d or {}), **{k: v for k, v in SUPP[name].items() if not (d or {}).get(k)}}
        if not d or not d.get("GURPS") or not (d.get("3.5e") or d.get("Source")):
            c["note"] = "draft lacks a 3.5e or GURPS block" if d else "no draft found"; short += 1; save(st); continue
        txt, opens = build(c, d)
        path = os.path.join(OUT, slug(c["name"]) + ".md")
        open(path, "w", encoding="utf-8").write(txt)
        c["status"], c["output_path"] = "converted", os.path.relpath(path, os.path.join(HERE, ".."))
        c["note"] = f"{len(opens)} non-blocking open GURPS item(s)" if opens else None
        done += 1; save(st)
    ps = st["phase_status"]["convert"]
    ps["converted"] = sum(1 for c in st["candidates"] if c["status"] == "converted")
    ps["status"] = "done" if all(c["status"] != "queued" and c["status"] != "in_progress" for c in st["candidates"]) else "in_progress"
    save(st)
    print(f"converted this run: {done}; stayed in_progress: {short}; total converted: {ps['converted']}/{ps['worklist_total']}")
    for c in st["candidates"]:
        if c["status"] == "in_progress":
            print("  in_progress:", c["name"], "-", c["note"])


def save(st):
    st["last_updated"] = datetime.date.today().isoformat()
    tmp = STATE + ".tmp"
    json.dump(st, open(tmp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    os.replace(tmp, STATE)


if __name__ == "__main__":
    main()
