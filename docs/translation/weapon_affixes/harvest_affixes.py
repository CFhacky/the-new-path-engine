#!/usr/bin/env python3
"""Phase 1 HARVEST for the weapon-affix corpus (separate from the Warhammer corpus state).

Reads source packets under ./sources/, cuts one candidate per named ability, and
appends to ./_translation_state.json. Idempotent by candidate_id (sha1-12 of
book|page|name); state is written after every book; re-running never duplicates.
Same schema as corpus-mass-translator references/pipeline-phases.md.

  python harvest_affixes.py --book dmg_v35
"""
import argparse, hashlib, json, os, re, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "_translation_state.json")
WORKLIST = os.path.join(HERE, "..", "affix_worklist.json")
BOOKS = {
    "dmg_v35": {
        "packet": os.path.join(HERE, "sources", "dmg_v35_pdf224-227.txt"),
        "source_book": "D&D 3.5e/Core/Dungeon Masters Guide v3.5.md",
        "names_from": "dmg",
        "degraded": {"Frost", "Ki Focus", "Dancing"},  # OCR figure still doubtful in the packet
    },
}
PAGE = re.compile(r"^## \[PDF page (\d+)\]\s*$")


def today():
    return datetime.date.today().isoformat()


def fresh():
    return {
        "corpus": "weapon_affixes_dmg_mic_3.5e",
        "created": today(), "last_updated": today(),
        "phase_status": {
            "harvest": {"status": "in_progress", "books_swept": 0, "books_total": 2},
            "triage": {"status": "pending", "candidates_triaged": 0},
            "convert": {"status": "pending", "converted": 0, "worklist_total": 0},
            "register": {"status": "pending", "registered": 0},
        },
        "books": {}, "candidates": [], "gaps": [],
    }


def save(state):
    state["last_updated"] = today()
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=1, ensure_ascii=False)
    os.replace(tmp, STATE)


def cid(book, page, name):
    return hashlib.sha1(f"{book}|{page}|{name}".encode("utf-8")).hexdigest()[:12]


def harvest(key, spec, state):
    names = [e["name"] for e in json.load(open(WORKLIST, encoding="utf-8"))[spec["names_from"]]]
    lines = open(spec["packet"], encoding="utf-8").read().splitlines()
    heads, page = {}, None  # name -> (line index, pdf page)
    for i, ln in enumerate(lines):
        m = PAGE.match(ln)
        if m:
            page = int(m.group(1)); continue
        for n in names:
            if ln.startswith(n + ":") and n not in heads:
                heads[n] = (i, page)
    missing = [n for n in names if n not in heads]
    order = sorted(heads.items(), key=lambda kv: kv[1][0])
    existing = {c["candidate_id"] for c in state["candidates"]}
    found = 0
    for idx, (n, (start, pg)) in enumerate(order):
        end = order[idx + 1][1][0] if idx + 1 < len(order) else len(lines)
        block = "\n".join(l for l in lines[start:end] if not PAGE.match(l)).strip()
        c = cid(key, pg, n)
        if c in existing:
            continue
        state["candidates"].append({
            "candidate_id": c, "name": n, "source_book": spec["source_book"], "source_page": pg,
            "category": "weapon_property", "scale": "dnd35_srd_prose",
            "verbatim_block": block,
            "extraction_quality": "degraded" if n in spec["degraded"] else "clean",
            "status": "harvested", "superseded_by": None, "tier": None, "relevance": None,
            "rank": None, "output_path": None,
            "note": "packet is a normalized transcription, see sources header; PDF page numbers",
        })
        existing.add(c); found += 1
    return found, missing


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--book", required=True)
    a = ap.parse_args()
    state = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else fresh()
    n, missing = harvest(a.book, BOOKS[a.book], state)
    state["books"][a.book] = {"status": "swept" if not missing else "error", "candidates_found": n,
                              "swept_on": today(), "missing_names": missing}
    state["phase_status"]["harvest"]["books_swept"] = sum(1 for b in state["books"].values() if b["status"] == "swept")
    save(state)
    print(f"{a.book}: +{n} candidates, missing={missing}; total candidates {len(state['candidates'])}")


if __name__ == "__main__":
    main()
