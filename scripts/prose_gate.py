#!/usr/bin/env python3
"""prose_gate.py — pre-delivery prose validator for The New Path campaign.

Governing sources (Notion is canon; on disagreement the page wins, this file gets patched):
  - Register Directive + CONTENT LAW + AI-Default Sweep Addendum:
      surface-campaign-master-gm mirror, Notion 349e8214-84b0-8126-ac8f-f2de981bb8a9
  - Prose Standards: surface-campaign-master-gm SKILL.md Section 1 (authoritative)
  - Standing corrections ledger: memory edits (verdict sentences, jargon repetition,
    interpretive narrator, negation frames, 5e idiom)

Design contract: stateless; stdlib only; visible stdout; exit 0 = PASS (warnings allowed),
exit 1 = FAIL findings present, exit 2 = usage error.

Usage:
  python3 prose_gate.py FILE [--register fiction|document] [--floor N]
                             [--require-header] [--top N]
  python3 prose_gate.py --selftest
"""
import argparse
import re
import sys
from collections import Counter

# ----------------------------------------------------------------------------
# Rule tables. (pattern, label). All matched case-insensitively unless noted.
# GLOBAL rules run on the full text (dialogue included — bad vocabulary is bad
# in anyone's mouth). NARRATION rules run with quoted dialogue blanked out,
# because characters may say things narrators may not.
# ----------------------------------------------------------------------------

GLOBAL_FAIL = [
    (r"\b(?:nestled|vibrant|thriving|bustling|delves?|delving|delved|myriad|"
     r"tapestr(?:y|ies)|intricate|intricacies)\b",
     "AI-default vocabulary (Sweep Addendum: banned on sight)"),
    (r"\btestament to\b", "AI-default vocabulary (Sweep Addendum)"),
    (r"\b(?:serves|stands|served|stood) as\b",
     "copula inflation (Sweep Addendum: use 'is'/'was')"),
    (r"\bboast(?:s|ed|ing)?\b", "copula inflation (Sweep Addendum)"),
    (r"\befficien(?:t|tly|cy)\b", "banned crutch word (Standing Law)"),
    (r"\boptimi[sz](?:e[sd]?|ing|ation)\b", "banned crutch word (Standing Law)"),
    (r"\bload-bearing\b", "banned metaphor (Standing Law)"),
    (r"\b(?:bonus action|short rest|long rest)\b",
     "5e mechanical language (banned vocabulary)"),
    (r"\b(?:advantage|disadvantage) on\b", "5e mechanical language"),
]

NARRATION_FAIL = [
    (r"\bthe kind (?:of \w+ )?that\b", "verdict-phrase crutch: 'the kind that'"),
    (r"\bthat was the (?:worst|best|first|last|whole|start|end) of\b",
     "verdict-phrase crutch (narrator grading the event)"),
    (r"\bwhich (?:meant|told|explained|said)\b",
     "interpretation rider ('which meant')"),
    (r"\bthe way (?:he|she|it|they|[A-Z][a-z]+) (?:always |never )?\w+",
     "mirror construction: 'the way X [verb]s'"),
    (r"\bthe way an? \w+ \w+s\b",
     "comparison crutch: 'the way a [noun] [verb]s'"),
    (r"(?:^|[.!?]\s+)(Wrong|Late|Simple|Perfect|Better|Worse|Gray|Grey|"
     r"Enough|Good|Bad) —",
     "verdict word opening a dash clause (narrator grading)"),
    (r"\bof a (?:man|woman|person|soldier|killer) who\b",
     "trailing authority-clause"),
    (r"\bin the (?:trained|practiced|old|usual|careful|quiet) way\b",
     "verdict-phrase: 'in the X way'"),
    (r"\b(?:clearly|obviously|evidently)\b", "telling (narrator asserting)"),
    (r"\b(?:architectur\w*|structural\w*|framework|infrastructur\w*|"
     r"mechanism|geometr(?:y|ic\w*))\b",
     "banned metaphor family in narration (Standing Law)"),
    (r"\bpredatory\b", "banned label (show the behavior)"),
    (r"\bdevastat(?:e[sd]?|ing)\b", "banned crutch (describe the damage)"),
]

NARRATION_WARN = [
    (r"\bNot \w+(?: \w+)? —", "negation frame (only lawful if it cashes into "
     "concrete imagery in the same beat)"),
    (r"\bnot \w+ but \w+\b", "negation frame (single-clause form)"),
    (r"\b(?:he|she|they) felt\b", "felt-check: raw physical sensation is lawful "
     "sparingly; emotional/cognitive shortcut is banned"),
    (r"\brepresents?\b", "copula inflation check"),
    (r"\brealm\b", "realm-as-filler check"),
    (r"\b\d*7\b", "number ending in 7 (avoid gravitating; dice headers exempt)"),
]

# One-word narration sentences drawn from the verdict lexicon are hard-banned
# (memory: "Wrong." "Late." "Gray." — the narrator grading instead of showing).
VERDICT_LEXICON = {
    "wrong", "late", "early", "simple", "easy", "hard", "perfect", "better",
    "worse", "close", "almost", "enough", "good", "bad", "gray", "grey",
    "nothing", "everything", "done", "over", "fast", "slow", "clean",
}

STOPWORDS = {
    "that", "with", "this", "from", "were", "have", "been", "into", "their",
    "them", "they", "there", "then", "than", "when", "what", "where", "which",
    "would", "could", "should", "will", "went", "came", "come", "said", "says",
    "over", "under", "back", "down", "onto", "still", "just", "like", "more",
    "most", "some", "only", "very", "each", "every", "again", "against",
    "through", "before", "after", "while", "about", "around", "between",
    "himself", "herself", "itself", "another", "other", "toward", "towards",
    "your", "yours", "hers", "his", "its", "ours", "these", "those", "here",
    "because", "though", "across", "behind", "above", "below", "himself",
}

HEADER_MARKERS = ("PHASE 0", "═══", "RESOLUTION", "raw", "bound")


def blank_dialogue(line: str) -> str:
    """Replace quoted spans with spaces so narration rules skip dialogue,
    preserving column positions and line numbers."""
    out, i, in_q = [], 0, False
    openers = '"\u201c'
    closers = '"\u201d'
    for ch in line:
        if not in_q and ch in openers:
            in_q = True
            out.append(" ")
        elif in_q and ch in closers:
            in_q = False
            out.append(" ")
        else:
            out.append(" " if in_q else ch)
    return "".join(out)


def sentences(text: str):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def scan(lines, rules, findings, severity):
    for n, line in enumerate(lines, 1):
        for pat, label in rules:
            for m in re.finditer(pat, line, flags=re.IGNORECASE):
                findings.append((severity, n, label, m.group(0)))


def run_gate(text: str, register: str, floor: int, require_header: bool,
             top: int, name: str = "<text>") -> int:
    raw_lines = text.splitlines()
    narr_lines = [blank_dialogue(l) for l in raw_lines]
    narr_text = "\n".join(narr_lines)
    findings = []  # (severity, line, label, match)

    scan(raw_lines, GLOBAL_FAIL, findings, "FAIL")
    scan(narr_lines, NARRATION_FAIL, findings, "FAIL")
    scan(narr_lines, NARRATION_WARN, findings, "WARN")

    # One-word verdict sentences in narration.
    for n, line in enumerate(narr_lines, 1):
        for s in sentences(line):
            w = re.fullmatch(r"([A-Za-z]+)[.!]", s)
            if w and w.group(1).lower() in VERDICT_LEXICON:
                findings.append(("FAIL", n, "one-word verdict sentence "
                                 "(narrator grading)", s))

    # Ending on a question (narration).
    narr_sents = sentences(narr_text)
    if narr_sents and narr_sents[-1].endswith("?"):
        findings.append(("FAIL", len(raw_lines), "ends on a question "
                         "(Standing Law: end on action/momentum)",
                         narr_sents[-1][:60]))

    # Em-dash density: documents only.
    words = re.findall(r"[A-Za-z']+", text)
    wc = len(words)
    if register == "document" and wc:
        dashes = text.count("\u2014") + text.count("--")
        per_k = dashes * 1000.0 / wc
        if per_k > 1.0:
            findings.append(("WARN", 0, f"em-dash density {per_k:.1f}/1000 words "
                             "(document register target <=1)", f"{dashes} dashes"))

    # Floor.
    if floor and wc < floor:
        findings.append(("FAIL", 0, f"below word floor: {wc} < {floor}", ""))

    # Header presence.
    if require_header and not any(m in text for m in HEADER_MARKERS):
        findings.append(("FAIL", 0, "no Phase 0 / resolution header found in "
                         "delivered text (rolls without visible headers count "
                         "as invented)", ""))

    # Repetition sweep (report; judgment stays human — plain concrete nouns
    # repeat freely, jargon labels and abstractions may not carry description
    # twice; reconciliation rule, 17 Jul 2026).
    counts = Counter(w.lower() for w in words
                     if len(w) >= 4 and w.lower() not in STOPWORDS)
    repeats = [(w, c) for w, c in counts.most_common() if c >= 4][:top]

    # Rhythm pass.
    all_sents = sentences(text)
    lens = [len(re.findall(r"[A-Za-z']+", s)) for s in all_sents if s]
    uniform = 0.0
    if len(lens) >= 10:
        band = sum(1 for L in lens if 15 <= L <= 25)
        uniform = band / len(lens)
        if uniform >= 0.6:
            findings.append(("WARN", 0, f"uniform meter: {uniform:.0%} of "
                             "sentences are 15-25 words — break the rhythm "
                             "(Sweep Addendum)", ""))

    fails = [f for f in findings if f[0] == "FAIL"]
    warns = [f for f in findings if f[0] == "WARN"]

    print("=" * 64)
    print(f"PROSE GATE — {name} | register={register} | {wc} words | "
          f"{len(all_sents)} sentences")
    print("=" * 64)
    for sev, group in (("FAIL", fails), ("WARN", warns)):
        print(f"{sev} ({len(group)}):")
        for _, ln, label, match in group:
            loc = f"L{ln}" if ln else "--"
            snippet = f' -> "{match}"' if match else ""
            print(f"  [{loc}] {label}{snippet}")
        if not group:
            print("  none")
    print(f"REPETITION (4+ uses — vary or ground; concrete nouns may repeat, "
          f"labels may not):")
    if repeats:
        print("  " + ", ".join(f"{w}:{c}" for w, c in repeats))
    else:
        print("  none at threshold")
    if lens:
        print(f"RHYTHM: mean {sum(lens)/len(lens):.1f} words/sentence; "
              f"{uniform:.0%} in the 15-25 band")
    print("TREADMILL (manual): every paragraph must add one new fact, claim, "
          "or turn — cut restatements, don't reword them.")
    verdict = "FAIL" if fails else "PASS"
    print(f"VERDICT: {verdict} ({len(fails)} fail / {len(warns)} warn)")
    print("=" * 64)
    return 1 if fails else 0


DIRTY_FIXTURE = """Darric rose off his knee. Wrong — flank security held unless called.
The light was the kind that flattened distance. She came out of the trunk the
way a swimmer comes up through a pond, nestled in the bark's intricate channels,
a testament to the forest's architecture. He felt afraid, clearly outmatched,
and the wound was devastating. It served as a warning, which meant the fight
had already turned. He gave ground in the trained way, the caution of a man who
had buried friends. Late. He used his bonus action and gained advantage on the
strike. The anvil held. The anvil bled. The anvil answered the anvil.
Would the anvil hold again?"""

CLEAN_FIXTURE = """The scrape ran six feet long under a dead spruce, dug to the
frozen dirt and floored with cut boughs. Blood came out fast and dark. It ran
down inside his belt, steamed at the lips of the cut, and soaked the wool black.
Ovrik bit down on a sound and staggered two steps sideways. His boots skidded
in the churned snow. He stayed up. Merra's finger took up the slack."""


def selftest() -> int:
    print("SELFTEST 1 — dirty fixture (expects FAIL with core categories):")
    rc1 = run_gate(DIRTY_FIXTURE, "fiction", 0, False, 20, "dirty-fixture")
    print("\nSELFTEST 2 — clean fixture (expects PASS):")
    rc2 = run_gate(CLEAN_FIXTURE, "fiction", 0, False, 20, "clean-fixture")
    ok = (rc1 == 1) and (rc2 == 0)
    print(f"\nSELFTEST VERDICT: {'OK' if ok else 'BROKEN'} "
          f"(dirty rc={rc1}, clean rc={rc2})")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Prose gate validator")
    ap.add_argument("file", nargs="?", help="text file to validate")
    ap.add_argument("--register", choices=("fiction", "document"),
                    default="fiction")
    ap.add_argument("--floor", type=int, default=0,
                    help="minimum word count (e.g. 1600 for scenes)")
    ap.add_argument("--require-header", action="store_true",
                    help="fail if no Phase 0 / resolution header text present")
    ap.add_argument("--top", type=int, default=20,
                    help="repetition report size")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.file:
        ap.print_usage()
        return 2
    try:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as e:
        print(f"cannot read {args.file}: {e}", file=sys.stderr)
        return 2
    return run_gate(text, args.register, args.floor, args.require_header,
                    args.top, args.file)


if __name__ == "__main__":
    sys.exit(main())
