#!/usr/bin/env python3
"""build_lexicon.py - collapse the weapon-affix drafts into one lookup table.

Reads docs/translation/affixes/*.md (DMG, one file per ability) and
docs/translation/affixes/mic/mic-*.md (Magic Item Compendium, many per file)
and writes docs/translation/AFFIX_LEXICON.md plus a completeness check.

Not a resolver: it only restates what the drafts already say. Where a draft is
the authority, the draft wins. FUSED_ENGINE_RESOLUTION.md overrides both.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "AFFIX_LEXICON.md")

def clean(s, n):
    s = re.sub(r"\s+", " ", s.replace("|", "/")).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

def price_from_heading(head):
    m = re.search(r"printed \+([\d,]+) gp", head)
    if m:
        return f"{m.group(1)} gp (flat)", int(m.group(1).replace(",", ""))
    m = re.search(r"printed \+(\d)\b", head)
    if m:
        b = int(m.group(1)); g = b * b * 2000
        return f"+{b} = {g:,} gp", g
    return None, None

def price_from_body(body):
    m = re.search(r"(?:Pricing|Price)[^:]*:\s*(?:printed )?\+?(\d)\b[^=\n]*=\s*([\d,]+) gp", body)
    if m:
        return f"+{m.group(1)} = {m.group(2)} gp", int(m.group(2).replace(",", ""))
    m = re.search(r"(?:Pricing|Price)[^:]*:\s*(?:printed )?\+?([\d,]+) gp", body)
    if m:
        return f"{m.group(1)} gp (flat)", int(m.group(1).replace(",", ""))
    return None, None

def flags(text, head=""):
    f = []
    if "OCR-uncertain" in text: f.append("OCR-uncertain")
    if "INACTIVE" in head or "INACTIVE" in text[:400]: f.append("INACTIVE (psionic/incarnum)")
    if "NAME COLLISION" in text: f.append("name collision: names stay, never merge")
    if re.search(r"RULING \(final\)|Rulings \(final\)", text): f.append("ruled")
    return f

def norm_verdict(v):
    return {"COVERED": "COVERED", "PARTIAL": "DELTA", "NEW": "NEW"}[v]

rows = []

# ---- DMG: one file per ability --------------------------------------------
for f in sorted(glob.glob(os.path.join(HERE, "affixes", "*.md"))):
    t = open(f, encoding="utf-8").read()
    m = re.match(r"# (.+?) — (COVERED|PARTIAL|NEW)", t)
    if not m:
        print("SKIP (no header):", f, file=sys.stderr); continue
    name = m.group(1).title()
    body = t
    pm = re.search(r"^Existing pool coverage:\s*(.+)$", body, flags=re.M)
    pool = clean(pm.group(1), 170) if pm else "none"
    em = re.search(r"^Source text \(key facts[^)]*\):\s*(.+)$", body, flags=re.M)
    effect = clean(em.group(1), 260) if em else ""
    pr, g = price_from_body(body)
    if not pr:
        hm = re.search(r"printed(?: bonus-equivalent)?:? Price \+(\d) bonus|printed bonus-equivalent: \+(\d)|printed bonus-equivalent / price: \+(\d) bonus", body)
        if hm:
            b = int(hm.group(1) or hm.group(2) or hm.group(3)); pr, g = f"+{b} = {b*b*2000:,} gp", b*b*2000
    rows.append(dict(name=name, src="DMG 223-227", verdict=norm_verdict(m.group(2)), pool=pool,
                     effect=effect, price=pr, gp=g, flags=flags(body), file=os.path.relpath(f, HERE)))

# ---- MIC: many entries per file --------------------------------------------
wl = json.load(open(os.path.join(HERE, "affix_worklist.json"), encoding="utf-8"))
pages = {r["name"].upper(): r["page"] for r in wl["mic"]}
for f in sorted(glob.glob(os.path.join(HERE, "affixes", "mic", "mic-*.md"))):
    t = open(f, encoding="utf-8").read()
    parts = re.split(r"^## ", t, flags=re.M)[1:]
    for p in parts:
        head, _, body = p.partition("\n")
        m = re.search(r"— (COVERED|PARTIAL|NEW)", head)
        if not m: print("SKIP head:", head[:60], file=sys.stderr); continue
        verdict = norm_verdict(m.group(1))
        names = [re.match(r"(.+?) \(", head).group(1).strip()]
        if " and DISLOCATOR, GREAT" in head:
            names = ["DISLOCATOR", "DISLOCATOR, GREAT"]
        sm = re.search(r"^Source:\s*(.+)$", body, flags=re.M)
        effect = clean(sm.group(1), 260) if sm else clean(body.split("\n")[0], 260)
        pm = re.search(r"^Pool:\s*(.+?)(?:\s3\.5e|\sGURPS:|$)", body, flags=re.M)
        pool = clean(pm.group(1), 170) if pm else "none"
        pr, g = price_from_heading(head)
        for nm in names:
            pg = pages.get(nm.upper())
            rows.append(dict(name=nm.title().replace("'S", "'s"), src=f"MIC p.{pg}" if pg else ("MIC (synergy)" if "SYNERGY" in head else "MIC"),
                             verdict=verdict, pool=pool, effect=effect, price=pr, gp=g,
                             flags=flags(head + "\n" + body, head), file=os.path.relpath(f, HERE)))

BASE = {
 "Auran": "Banefire (Elemental 93-96) via Aquan; same family as Aquan",
 "Ignan": "Banefire (Elemental 93-96) via Aquan; same family as Aquan",
 "Terran": "Banefire (Elemental 93-96) via Aquan; same family as Aquan",
 "Desiccating Burst": "Desiccating (MIC, base) plus the burst template",
 "Psychokinetic Burst": "Psychokinetic (MIC, base) plus the burst template",
 "Sacred Burst": "Sacred (MIC, base) plus the Profane Burst template",
 "Screaming Burst": "Screaming (MIC, base) plus the burst template",
 "Unholy Surge": "Unholy (DMG, base) plus the Holy Surge pattern",
}
for r in rows:
    if r["name"] in BASE: r["pool"] = BASE[r["name"]]

BASE_ROW = {
 "Warning": "Timesense (Utility fragment 97-100)", "Flaming Burst": "Flaming (Elemental 01-08)", "Shocking Burst": "Shocking (Elemental 17-24)",
 "Icy Burst": "Freezing (Elemental 09-16)", "Power Storing": "Spell Storing (DMG) / Reservoir (Resource 49-54)",
 "Spellstrike": "Defending (DMG) / Stalwart (Defensive 13-18)", "Ethereal Reaver": "Ghost Touch (DMG) + Truesight (Utility 31-36)",
 "Aquan": "Banefire (Elemental 93-96)", "Auran": "Banefire (Elemental 93-96)", "Ignan": "Banefire (Elemental 93-96)", "Terran": "Banefire (Elemental 93-96)",
 "Desiccating Burst": "Desiccating (MIC)", "Psychokinetic Burst": "Psychokinetic (MIC)", "Sacred Burst": "Sacred (MIC)", "Screaming Burst": "Screaming (MIC)",
 "Energy Aura": "Flaming / Freezing / Shocking / Corroding (Elemental)", "Energy Surge": "Flaming / Freezing / Shocking / Corroding (Elemental)",
 "Fiercebane": "Bane (DMG)", "Magebane": "Bane (DMG)", "Psibane": "Bane (DMG)",
 "Ghost Strike": "Ghost Touch (DMG)", "Incorporeal Binding": "Ghost Touch (DMG)", "Holy Surge": "Holy (DMG)", "Unholy Surge": "Unholy (DMG)",
 "Mighty Cleaving": "Cleave Through (temper 23A-1)", "Parrying": "Warding (Defensive 01-06) + Stalwart (Defensive 13-18)",
 "Profane": "Shadowtouch (Elemental 39-44)", "Profane Burst": "Profane (MIC)", "Soulbreaker": "Enervating (MIC)", "Souldrinking": "Enervating (MIC)",
 "Venomous": "none (pool 'Venomous' is a different affix; names stay)", "Weakening": "none (pool 'Weakening' is a different affix; names stay)",
}
_POOLROW = re.compile(r"([A-Z][A-Za-z' ]+?) \((?:Elemental|Offensive|Defensive|Resource|Utility|Skill/Class|Condition)(?: pool)? ?\d\d-\d\d\)")
for r in rows:
    if r["name"] in BASE_ROW:
        r["base"] = BASE_ROW[r["name"]]
    else:
        ms = [m.group(0).replace(" pool", "") for m in _POOLROW.finditer(r["pool"])]
        r["base"] = ", ".join(dict.fromkeys(ms))[:90] if ms else "none"
rows.sort(key=lambda r: r["name"].lower())

# ---- completeness check ------------------------------------------------------
problems = []
mic_names = {r["name"].upper() for r in rows if r["src"].startswith("MIC")}
for w in wl["mic"]:
    if w["name"].startswith(("Crystal", "Demolition", "Fiendslayer", "Phoenix", "Revelation", "Truedeath", "Witchlight")):
        continue
    if w["name"].upper() not in mic_names:
        problems.append(f"worklist MIC entry missing: {w['name']}")
dmg_names = {r["name"].upper() for r in rows if r["src"].startswith("DMG")}
for w in wl["dmg"]:
    if w["name"].upper() not in dmg_names:
        problems.append(f"worklist DMG entry missing: {w['name']}")
for r in rows:
    if not r["effect"]: problems.append(f"no effect text: {r['name']}")
    if not r["price"]: problems.append(f"no price: {r['name']}")
    if r["verdict"] in ("COVERED", "DELTA") and r["base"] == "none" and "names stay" not in r["pool"] + r["base"]:
        problems.append(f"{r['verdict']} row names no existing pool row: {r['name']}")

# ---- write ---------------------------------------------------------------------
cnt = {v: sum(1 for r in rows if r["verdict"] == v) for v in ("COVERED", "DELTA", "NEW")}
lines = [
    "# Weapon Affix Lexicon (book weapon properties)",
    "",
    "One row per affix. Generated by `docs/translation/build_lexicon.py` from the drafts in `docs/translation/affixes/`.",
    "**Rules that govern every row:** `docs/translation/FUSED_ENGINE_RESOLUTION.md` (item effects run on the 3.5e chassis; riders ignore worn DR; GURPS dice read as-is; wrong-aligned wielders take Energy Drained; names stay and never merge).",
    "",
    f"**{len(rows)} affixes:** {cnt['COVERED']} COVERED (an existing Registry pool row already does it) · {cnt['DELTA']} DELTA (an existing row plus a missing piece) · {cnt['NEW']} NEW (needs a full family entry the first time it is rolled or placed).",
    "",
    "Price is the printed book price: +N bonus priced bonus-squared x 2,000 gp, or the printed flat gp. Flags: OCR-uncertain (a scanned figure could not be verified), INACTIVE (needs a psionic/incarnum character), ruled (one of the four engine-gap rulings applies).",
    "",
    "| Affix | Source | Verdict | Base row | Existing-row note | Printed effect | Price | Flags |",
    "|---|---|---|---|---|---|---|---|",
]
for r in rows:
    lines.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
        r["name"], r["src"], r["verdict"], r["base"], clean(r["pool"], 120), clean(r["effect"], 200),
        r["price"] or "—", "; ".join(r["flags"]) or ""))
lines += ["", "## The four rulings the engine does not settle", "",
          "1. **Implacable:** capped at 5 stacks, never on a weapon that also carries Fatal Wound, any magical healing ends it.",
          "2. **Vorpal:** a confirmed natural-20 crit forces the Head location at Lethal severity on the fused engine's crit table; no separate save.",
          "3. **Soulbreaker:** NPC wielders as printed; against a PC the negative levels last 24 hours unless purged and never convert to level loss.",
          "4. **Psionic and incarnum entries:** inactive until such a character exists.",
          "", "Crusader (WoW) is not in this table: it is ratified in the Notion Affix Registry, section 2."]
open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"rows={len(rows)}", cnt)
if problems:
    print("PROBLEMS:", len(problems))
    for p in problems: print(" -", p)
    sys.exit(1)
print("completeness check: OK")
