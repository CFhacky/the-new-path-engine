#!/usr/bin/env python3
"""Harvest Diablo 2 item records from d2emu.com list pages into d2/data/*.json.

Personal-campaign convenience data. NOT campaign canon, NOT book RAW; see d2/README.md.
Stdlib only. Usage: d2emu_harvest.py [unique set runeword]   (default: all three)
"""
import html, json, re, sys, urllib.request, pathlib, datetime

BASE = "https://d2emu.com"
OUT = pathlib.Path(__file__).parent / "data"
CATS = ["unique", "set", "runeword"]
ART = re.compile(r'<article class="db-card db-card--item-preview[^"]*" data-category="([^"]+)" data-record-url="([^"]+)">(.*?)\n</article>', re.S)

def txt(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def parse(cat, url, body):
    rec = {"id": url.rstrip("/").split("/")[-1], "category": cat, "url": BASE + url}
    m = re.search(r'<h3>(.*?)</h3>', body, re.S)
    rec["name"] = txt(re.sub(r'<span class="db-popular.*?</span>', "", m.group(1), flags=re.S)) if m else rec["id"]
    m = re.search(r'class="db-hover-quality">(.*?)</p>', body, re.S)
    rec["quality"] = txt(m.group(1)) if m else None
    m = re.search(r'class="db-hover-base">(.*?)</p>', body, re.S)
    rec["base"] = txt(m.group(1)) if m else None
    m = re.search(r'<img class="db-hover-icon" src="([^"]+)"', body)
    rec["icon"] = BASE + m.group(1) if m else None
    rec["stats"] = {txt(k): txt(v) for k, v in re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', body, re.S)}
    ul = re.search(r'<ul>(.*?)</ul>', body, re.S)
    rec["mods"] = [txt(li) for li in re.findall(r'<li>(.*?)</li>', ul.group(1), re.S)] if ul else []
    return rec

def main(cats):
    OUT.mkdir(exist_ok=True)
    for cat in cats:
        req = urllib.request.Request(f"{BASE}/db/{cat}", headers={"User-Agent": "personal-campaign-harvester/1.0"})
        page = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        recs = [parse(c, u, b) for c, u, b in ART.findall(page)]
        recs.sort(key=lambda r: r["id"])
        doc = {"source": f"{BASE}/db/{cat}", "harvested": datetime.date.today().isoformat(),
               "note": "Personal campaign convenience data; not canon, not book RAW.",
               "count": len(recs), "records": recs}
        (OUT / f"{cat}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print(f"{cat}: {len(recs)} records")

if __name__ == "__main__":
    main(sys.argv[1:] or CATS)
