#!/usr/bin/env python3
"""Embed d2/data/*.json into tracker_template.html -> d2/tracker.html (single offline file)."""
import json, pathlib
here = pathlib.Path(__file__).parent
recs = []
for cat in ["unique", "set", "runeword"]:
    recs += json.loads((here / "data" / f"{cat}.json").read_text())["records"]
slim = [{k: r[k] for k in ("id", "category", "name", "quality", "base", "icon", "stats", "mods")} for r in recs]
blob = json.dumps(slim, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
out = (here / "tracker_template.html").read_text().replace("__DATA__", blob)
(here / "tracker.html").write_text(out)
print(f"tracker.html: {len(slim)} records, {len(out)//1024} KB")
