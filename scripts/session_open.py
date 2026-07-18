#!/usr/bin/env python3
"""
session_open.py -- Session Start Protocol dice layer (Arik surface campaign)
The New Path campaign engine (the-new-path-engine)

Rolls the ENTIRE dice side of the Arik session-open protocol in protocol
order, one run per session open, printing a complete roll log that the
session instance interprets against Notion. This script does NOT read
Notion -- it prints the Step 0/0.5 read checklist as text and then rolls.

GOVERNING SOURCES (read 2026-07-17, cited per table below):
    Notion "Session Start Protocol -- Arik Surface Campaign"
        page 364e8214-84b0-8144-bfc4-cd1f25ae3c3a  (self-contained,
        Amendments 1-5 integrated; Steps 0-8, 4.5A-E added 2026-07-10)
    Notion "SESSION STATE -- ARIK ARC (Boot Page)" -- THE WORLD-MOVE LAW
        page 390e8214-84b0-819c-9577-d8103a27467e
    Notion "Inevitable City -- District Gazetteer & Hell-Quarter Ledger"
        page 399e8214-84b0-81e8-a738-f93f1e833aeb  (Step 4.5E dice)
    Standing Law G2 (boot custom instructions): python secrets, raw
        stdout BEFORE outcomes, four throws per roll bound mode-else-median.

DESIGN CONTRACT (repo README / AUTHORITY.md):
    - Stateless resolver: flags in, text out. The only state file is the
      session-local threads.json the USER maintains (thread list and NPC
      principals change over time and must not fossilize in code).
      Ship it with --write-threads-template.
    - No campaign FACTS in code: no clock values, no dates, no NPC stats.
      The Lolth accumulator is a FLAG INPUT echoed against its thresholds,
      never stored.
    - Real dice: python secrets. Raw values print before interpretation.
    - Every threshold result the protocol marks as a World-Move Law
      trigger state is collected into the THRESHOLD SUMMARY for cash-in.

THROW MODE (Chad ruling, 17 Jul 2026 — "it depends"):
    DEFAULT IS SINGLE RAW DICE: session-open rolls are PLAY, and outliers
    (door-knock 19s, nat-20 windfalls, 1-band crises) are content, not
    noise — matching the S074 roll log on the protocol page.
    Pass --four-throw when a roll is a RULING wanting stability: four
    throws, unique modal value binds; otherwise median of the four =
    mean of the middle two, fractional rounds DOWN (conservative).
    Choose per the roll's nature, not per habit.

USAGE
    python session_open.py --write-threads-template
    python session_open.py --months-elapsed 1 --quarter-elapsed --hell-side \
        --quenthel-due --gromph-case-due --city-years 2 --lolth-accumulator 0 \
        --log rolls.log
"""

import argparse
import datetime
import io
import json
import os
import secrets
import statistics
import sys
from typing import Dict, List, Optional, Tuple

if sys.platform == "win32":          # cp1252 consoles choke on box glyphs
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ============================================================================
# DICE ENGINE -- secrets only; raw values always printed before outcomes.
# Four-throw discipline per Standing Law G2 (see docstring for the tie rule).
# ============================================================================

SINGLE_THROW = False      # set by --single-throw


def _throw(sides: int) -> int:
    return secrets.randbelow(sides) + 1


def bind_four(values: List[int]) -> Tuple[int, str]:
    """Mode-else-median binding over four throws (Standing Law G2)."""
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    best = max(counts.values())
    modes = sorted(v for v, c in counts.items() if c == best)
    if best >= 2 and len(modes) == 1:
        return modes[0], "mode"
    s = sorted(values)
    med = (s[1] + s[2]) / 2
    return int(med), "median"        # fractional median rounds down


def roll(sides: int, label: str, mod: int = 0,
         mod_note: str = "") -> Tuple[int, str]:
    """One protocol roll: four throws (or one), bound, modifier applied.
    Returns (total, printed line). Raw throws appear in the line FIRST."""
    if SINGLE_THROW:
        raw = _throw(sides)
        bound, how = raw, "single"
        raws = [raw]
    else:
        raws = [_throw(sides) for _ in range(4)]
        bound, how = bind_four(raws)
    total = bound + mod
    mtxt = f" {mod:+d}" if mod else ""
    line = (f"  d{sides} throws {raws} -> bind {bound} ({how}){mtxt}"
            f" = {total}  [{label}{('; ' + mod_note) if mod_note else ''}]")
    return total, line


def roll_expr_2d6x10() -> Tuple[int, str]:
    """4.5B muster size: 2d6 x 10. Four throws of the full 2d6 expression,
    bound on the 2d6 total, then x10 (Standing Law G2 applied to the
    expression as a unit)."""
    if SINGLE_THROW:
        pair = [_throw(6), _throw(6)]
        bound, how, raws = sum(pair), "single", [pair]
    else:
        raws = [[_throw(6), _throw(6)] for _ in range(4)]
        totals = [sum(p) for p in raws]
        bound, how = bind_four(totals)
    return bound * 10, (f"  2d6 throws {raws} -> bind {bound} ({how})"
                        f" x10 = {bound * 10}  [muster size]")

# ============================================================================
# BAND TABLES -- every table cites its source line on the protocol page.
# ============================================================================

# Step 2 -- Quenthel-Favor favor type (protocol page, Step 2 item 2)
QUENTHEL_BANDS = [(1, 8, "Information"), (9, 13, "Attendance"),
                  (14, 16, "Working"), (17, 18, "Withholding"),
                  (19, 20, "Action")]
QUENTHEL_PAGE = "361e8214-84b0-81ea-a026-cd499dd554ee"

# Step 2.5 -- Cases for Gromph (protocol page, Amendment 1 block)
GROMPH_BANDS = [(1, 10, "No case this quarter; Gromph is on his own concerns."),
                (11, 16, "A case surfaces. Roll the generation table."),
                (17, 19, "High-quality case (force minimum texture 4)."),
                (20, 20, "Forgedeep-Echo-style case -- high strategic value, "
                         "low Gromph texture.")]
GROMPH_CASES_PAGE = "364e8214-84b0-813a-ab4f-e749c527de2c"

# Step 3 -- plot-thread progress outcome bands (protocol page, "How to Roll
# Plot Thread Progress")
THREAD_BANDS = [(1, 3, "Setback (complication surfaces; thread regresses or stalls)"),
                (4, 10, "Routine advance (on schedule, no scene required)"),
                (11, 16, "Productive advance (NPC brings useful intel to Arik)"),
                (17, 19, "Breakthrough (significant gain; scene-worthy)"),
                (20, 999, "Strategic windfall (rare; major session beat)")]

# Step 4 / 4.5A -- NPC / native-power action bands (protocol page, Step 4
# outcomes; Step 4.5A states "Same outcome bands as Step 4")
NPC_BANDS = [(1, 9, "No new activity -- executing standing instructions/posture"),
             (10, 14, "Routine briefing-worthy"),
             (15, 18, "Active need for a decision -- requests time this session"),
             (19, 999, "Crisis or breakthrough -- at the door demanding attention")]

# Step 4.5A -- the five native powers (protocol page table; modifiers per page)
# Dispater +3 only "while attention HIGH"; abishai +2 "while reporting posture
# holds" -- both are session-state flags, not stored facts.
HELL_POWERS = [
    ("Bel's court (via Cassiamel)", 1, "thin line / advocate"),
    ("Mammon's office (via Brakhett)", 2, "scented revenue"),
    ("Dispater's desk", None, "+3 while attention HIGH (--dispater-high)"),
    ("Zariel (Warborn contract)", 0, "contract steady"),
    ("The abishai watch (Twin Crags)", None,
     "+2 while reporting posture holds (drop with --abishai-posture-broken)"),
]

# Step 4.5B -- corridor ecology d20 (protocol page, verbatim bands)
CORRIDOR_TABLE = [
    (1, 3, "Successor pressure -- something big tests the vacuum; names itself "
           "within a tenday.  [WORLD-MOVE TRIGGER BAND]"),
    (4, 7, "Muster drift -- unanchored demon band crosses or squats; size 2d6x10; "
           "picket contact odds rise."),
    (8, 11, "Carrion economy -- the scavenger chain reorganizes around the latest "
            "killing."),
    (12, 14, "Quiet cycle -- the corridor holds its breath (quiet after HIGH "
             "attention is itself data -- log it)."),
    (15, 17, "Styx behavior -- the tributary moves; the river is an actor."),
    (18, 19, "Territorial claim-mark -- something has begun MARKING the corridor."),
    (20, 20, "Anomaly -- Avernus itself moves; scene-worthy; roll d6 age-band."),
]
CORRIDOR_AGE_BAND = [(1, 3, "recent war"), (4, 5, "old war"), (6, 6, "pre-war")]

# Step 4.5C -- Blood War tide d12 (protocol page, verbatim bands)
TIDE_TABLE = [
    (1, 3, "Front recedes -- carrion-runs thin."),
    (4, 8, "Front holds -- status quo; carrion-runs on cycle."),
    (9, 11, "Front nears -- battle-tide within Courser range; Bel's court "
            "attention on the corridor rises one step."),
    (12, 12, "A NAMED ENGAGEMENT within sight or sound.  [WORLD-MOVE TRIGGER]"),
]

# Step 4.5D -- garrison interior d20 (protocol page, verbatim bands)
GARRISON_TABLE = [
    (1, 4, "A seam-class event -- binding question / devotion anomaly (the Vresk "
           "lane). Vesper's desk.  [SEAM BAND -- see threshold note]"),
    (5, 9, "Culture forming -- the converted develop something of their own."),
    (10, 14, "Routine texture -- one name, one line."),
    (15, 17, "The old country calls -- Hell contacts a converted devil."),
    (18, 20, "A death question -- a converted devil dies; the doctrine question "
             "fires."),
]

# Step 4.5E -- Hell-Quarter Ledger six dice per City-year block (Gazetteer
# page 399e8214-84b0-81e8-a738-f93f1e833aeb, "rules of motion": six d20s;
# threshold 1-3 or 18+ on any die -> World-Move Law trigger; totals rewrite
# the city page's live numbers; interpretation happens ON the page).
LEDGER_DICE = ["Population", "Economy (Finance -- City Stats machinery)",
               "Hygiene / contagion", "Sanctity drift", "Integration index",
               "The Knot"]
GAZETTEER_PAGE = "399e8214-84b0-81e8-a738-f93f1e833aeb"

# Step 5 -- Veil intelligence surface (protocol page, Step 5; d20 15+, then d8)
VEIL_CATEGORIES = {
    1: "Aldric cold-war update",
    2: "Sembian merchant council activity",
    3: "Thayan posture (post-Unbinding only)",
    4: "Jarlaxle/Bregan D'aerthe operational update",
    5: "Embedded threat activation (one of the 8 canonized embedded threats moves)",
    6: "Ship Kurth honeypot intercept (high-value)",
    7: "Cult of the Dragon convergence on Seliara",
    8: "Unanticipated -- Lirien surfaces something unexpected (improvise)",
}

# Step 7 -- antagonist posture clocks (protocol page, Step 7, verbatim bands)
ALDRIC_BANDS = [(1, 6, "De-escalation"), (7, 14, "Status quo"),
                (15, 18, "Escalation"), (19, 20, "Open hostile action")]
SEMBIAN_BANDS = [(1, 6, "Commercial only"), (7, 14, "Intelligence operations active"),
                 (15, 18, "Economic warfare attempted"),
                 (19, 20, "Military proxy mobilization")]
THAYAN_BANDS = [(1, 12, "No movement"), (13, 16, "Investigation deepening"),
                (17, 19, "Counter-operation surfaces"), (20, 20, "Direct retaliation")]
LOLTH_THRESHOLDS = ("At 12, Lolth's network begins active investigation. "
                    "At 18, direct priestess-network operations against Crown "
                    "branches begin. At 24, divine attention.")


def band_lookup(bands, value):
    for lo, hi, text in bands:
        if lo <= value <= hi:
            return text
    return "OFF-TABLE (check the page)"

# ============================================================================
# STEP 0 / 0.5 READ CHECKLIST -- page names + IDs from the protocol page.
# Printed as text; this script never reads Notion.
# ============================================================================

READ_CHECKLIST = """\
STEP 0 / 0.5 -- READ STATE BEFORE ROLLING (fetch in Notion; script rolls only)
  0.a  Canon Change Log query FIRST (Amendment 2): data source
       83d9b4a3-9489-46e0-b7d5-d17ba224ef68 -- entries since last session,
       Change Date desc; Schema Changes first, then session-blockers.
  0.b  Date Status / Deep Horizon scan (Amendment 4): ledger page
       37ae8214-84b0-81e5-a042-c1f57b14fe66 -- entered WINDOWs, ~1yr
       graduations, resolved PENDINGs.
  0.5  Adversary Clock Processing (Amendment 3): GM Consequence Ledger
       data source 96a99cba-2be9-4d8b-a032-b9c3cfc9fbce -- entries with
       Adversary Clock Architecture headings; advance per procedure.
       (Boot-page shakedown 2026-07-01 flags this ledger as Shi'van-arc
       infrastructure -- verify lane before querying; Arik commitments
       live on boot page 390e8214-84b0-819c-9577-d8103a27467e.)
  0.1  Notion Structure Reference: 343e8214-84b0-8122-a2d7-fd5226215c9e
  0.2  Empire Financial State -- Current Reference:
       34ce8214-84b0-81d7-abb5-f5d9cf153d72
  0.3  Cash Position Reconciliation: 34ce8214-84b0-81c0-8dd4-c3122711cc8e
  Also: read the last 1-2 World-Move Register session pages (Law boot rule;
       Register DB 4ec10078-f1d0-467f-abf5-6542803658f0).
  Note the current in-world date; calculate elapsed time since last session."""

STEP8_CHECKLIST = """\
STEP 8 -- COMPOSE SESSION PREMISE (verbatim from the protocol page)
  With all rolls complete, write a 4-6 line opening briefing. Format:
  - Date and place: Where is Arik this session?
  - Standing situation: What did the rolls reveal as the dominant state?
  - Doors at the table: Which NPCs (Step 4 rolls 15+) are waiting for time?
    In what priority?
  - Background friction: What clocks advanced but did not surface? (One
    sentence each, deniable plausibility for future surface-up.)
  - Implied choice: What is Arik actually deciding this session?
  The briefing becomes Chad's opening reference. Adjust scene order to match
  the rolled state; don't override the rolls because the planned content was
  different.  (Cross-Thread Linkage Notes on the page apply during this step;
  Scene Composition Doctrine: Roll-First / Tradecraft Test / Unreliable
  Narrator.)"""

# ============================================================================
# THREADS.JSON TEMPLATE -- Step 3 threads + Step 4 principals as of the
# protocol page read 2026-07-17. USER-MAINTAINED; the page wins on conflict.
# ============================================================================

THREADS_TEMPLATE = {
    "_source": ("Session Start Protocol page 364e8214-84b0-8144-bfc4-"
                "cd1f25ae3c3a, Step 3 'Currently Active' + Step 4 tables, "
                "transcribed 2026-07-17. Edit as the page changes; on any "
                "disagreement the page wins."),
    "threads": [
        {"name": "Northern Reserve Expansion -- Phase 1 (Mithral Hall)",
         "modifier": 3, "interval": "monthly", "roll": True,
         "note": "Korgan's clan credentials +3; page 34ee8214-84b0-8106-889f-d4ba0ccd23b5"},
        {"name": "Northern Reserve Expansion -- Phase 2 (Ten-Towns)",
         "modifier": 0, "interval": "bi-monthly", "roll": True,
         "note": "No skilled lead, no modifier; low-stakes"},
        {"name": "Operation Unbinding",
         "modifier": 4, "interval": "phase-gated", "roll": True,
         "note": "Lirien + Veil network bonus +4 during planning phases; "
                 "page 34de8214-84b0-811d-8fa2-efb66949ee08"},
        {"name": "Project Burning Gate (Shi'van-side)",
         "modifier": 0, "interval": "quarterly (Shi'van-side sessions only)",
         "roll": False,
         "note": "Roll only if Shi'van-side; page 34ce8214-84b0-8125-b0cc-fa8966ff42f0"},
        {"name": "Aldric Cold-War posture",
         "modifier": 0, "interval": "monthly stance", "roll": False,
         "note": "Stance roll resolved under Step 7's Aldric band table"},
        {"name": "Lolth Attention Clock",
         "modifier": 0, "interval": "quarterly accumulator", "roll": False,
         "note": "Flag input --lolth-accumulator; thresholds 12/18/24; never stored"},
        {"name": "Klauth Gem Liquidation Pace",
         "modifier": 0, "interval": "monthly gp realized", "roll": False,
         "note": "Financial-phase math, not a d20 progress roll; "
                 "page 34ce8214-84b0-81c0-8dd4-c3122711cc8e"},
    ],
    "principals": [
        {"name": "Vara Torsten", "modifier": 2,
         "domain": "Empire finance, NCF, monetary system"},
        {"name": "Lirien Nightwalker", "modifier": 4,
         "domain": "Veil, intelligence, counter-intelligence"},
        {"name": "Korgan Bloodaxe", "modifier": 1,
         "domain": "Bloodaxe Legion, military, dwarven diplomacy"},
        {"name": "Selene Vanris", "modifier": 0,
         "domain": "Storm operations, griffon corps, Skyreach"},
        {"name": "Seliara Frostwind", "modifier": 2,
         "domain": "Eternal Dancer program, R&D"},
        {"name": "Sania Valmorra", "modifier": 1,
         "domain": "Soul-binding, dimensional research"},
        {"name": "Frieren", "modifier": 3,
         "domain": "Magical methodology, archmage consultation"},
        {"name": "Gromph Baenre", "modifier": None,
         "domain": "Hosttower, Underdark Crown integration, Lolth defense",
         "note": "variable -- apply per this session's Quenthel-Favor result"},
    ],
}


def load_threads(path: str) -> Dict:
    if not os.path.exists(path):
        raise SystemExit(
            f"No threads file at {path!r}. Run --write-threads-template first "
            f"(the protocol's thread list changes over time and must not "
            f"fossilize in code).")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ============================================================================
# PROTOCOL STEPS -- each returns printed lines; threshold states are
# appended to the shared `triggers` list for the summary.
# ============================================================================

def hdr(title: str) -> str:
    return f"\n{'=' * 68}\n{title}\n{'=' * 68}"


def step2_quenthel(out, triggers):
    out.append(hdr("STEP 2 -- QUENTHEL-FAVOR CLOCK (favor due; rolled first: "
                   "it can rewrite the premise)"))
    total, line = roll(20, "favor type")
    out.append(line)
    band = band_lookup(QUENTHEL_BANDS, total)
    out.append(f"  FAVOR TYPE: {band}  (1-8 Information / 9-13 Attendance / "
               f"14-16 Working / 17-18 Withholding / 19-20 Action)")
    sub, subline = roll(6, "favor sub-table")
    out.append(subline)
    out.append(f"  SUB-TABLE: raw d6 = {sub} -- roll interpreted against the "
               f"Quenthel-Favor Clock page {QUENTHEL_PAGE} (sub-table content "
               f"lives on the page; this script does not embed the asks).")
    out.append("  Then: decide Gromph's response per the page (Information/"
               "Attendance automatic; Working near-automatic; Withholding/"
               "Action -- explicit calculation, refusal counter). Log on the "
               "Quenthel page.")
    if band in ("Withholding", "Action"):
        triggers.append(f"Quenthel-Favor landed {band} -- can rewrite the "
                        f"session premise; surface as primary scene if it "
                        f"materially affects planned content (Step 2 item 6).")


def step25_gromph(out, triggers):
    out.append(hdr("STEP 2.5 -- CASES FOR GROMPH (quarterly opportunity; "
                   "after Step 2, before Step 4 -- Amendment 1)"))
    total, line = roll(20, "case opportunity")
    out.append(line)
    out.append(f"  RESULT: {band_lookup(GROMPH_BANDS, total)}")
    if total >= 11:
        origin, l1 = roll(8, "Origin 1d8")
        out.append(l1)
        texture, l2 = roll(6, "Texture 1d6")
        out.append(l2)
        forced = ""
        if 17 <= total <= 19 and texture < 4:
            forced = (f"  -> texture raised to 4 (17-19 forces minimum "
                      f"texture 4; raw {texture} shown above, binding value 4)")
            texture = 4
        risk, l3 = roll(6, "Risk 1d6")
        out.append(l3)
        benefit, l4 = roll(6, "Benefit 1d6")
        out.append(l4)
        if forced:
            out.append(forced)
        out.append(f"  GENERATION: Origin {origin} / Texture {texture} / "
                   f"Risk {risk} / Benefit {benefit} -- interpret against the "
                   f"Cases for Gromph page {GROMPH_CASES_PAGE}.")
        if total == 20:
            out.append("  CLASS: Forgedeep-Echo -- high strategic value, low "
                       "Gromph texture; huge empire benefit, small goodwill "
                       "yield (feeds the Gromph Favor Bank, page 364e8214-"
                       "84b0-810e-8892-cc34fbee7800).")


def step3_threads(out, triggers, threads):
    out.append(hdr("STEP 3 -- ACTIVE PLOT THREAD CLOCKS (d20 + per-thread "
                   "modifier; threads from threads.json)"))
    out.append("  Bands: 1-3 Setback / 4-10 Routine / 11-16 Productive / "
               "17-19 Breakthrough / 20+ Windfall")
    for t in threads:
        if not t.get("roll", True):
            out.append(f"  [not rolled] {t['name']} -- {t.get('note', '')}")
            continue
        mod = t.get("modifier") or 0
        total, line = roll(20, t["name"], mod, t.get("interval", ""))
        out.append(line)
        band = band_lookup(THREAD_BANDS, total)
        out.append(f"    -> {band}")
        if total <= 3:
            triggers.append(f"Thread SETBACK (1-3 band): {t['name']} -- "
                            f"complication surfaces; thread regresses or stalls.")
        elif total >= 20:
            triggers.append(f"Thread STRATEGIC WINDFALL (20+): {t['name']} -- "
                            f"major session beat.")


def step4_npcs(out, triggers, principals, gromph_mod: Optional[int]):
    out.append(hdr("STEP 4 -- MID-TIER NPC ACTION ROLLS (d20 + modifier per "
                   "principal; principals from threads.json)"))
    out.append("  Bands: 1-9 no new activity / 10-14 routine briefing / "
               "15-18 needs a decision / 19+ at the door")
    doors = []
    for p in principals:
        mod = p.get("modifier")
        note = ""
        if mod is None:
            if gromph_mod is not None:
                mod, note = gromph_mod, "variable mod supplied via --gromph-mod"
            else:
                mod, note = 0, ("VARIABLE -- modifier not applied; apply per "
                                "Quenthel-Favor result when interpreting")
        total, line = roll(20, p["name"], mod, note)
        out.append(line)
        band = band_lookup(NPC_BANDS, total)
        out.append(f"    -> {band}")
        if total >= 19:
            doors.append(p["name"])
            triggers.append(f"DOOR-KNOCK 19+ (Step 4): {p['name']} -- crisis "
                            f"or breakthrough; immediate attention.")
        elif total >= 15:
            doors.append(f"{p['name']} (15-18)")
    if doors:
        out.append(f"  RESOLVE IN PRIORITY ORDER: 19+ first, then 15-18: "
                   f"{', '.join(doors)}")

def step45_hell(out, triggers, dispater_high: bool, abishai_holds: bool,
                hell_cycles: int):
    out.append(hdr("STEP 4.5 -- AVERNUS NATIVE LAYER (Hell-side only; slots "
                   "between Step 4 and Step 5; all threshold results feed the "
                   "World-Move Law and write to the World-Move Register)"))
    # -- 4.5A native powers -------------------------------------------------
    out.append("\n  4.5A -- NATIVE POWERS ACTIVATION (1d20 each; Step 4 bands)")
    for name, mod, note in HELL_POWERS:
        if name.startswith("Dispater"):
            mod = 3 if dispater_high else 0
            note = ("attention HIGH: +3 per page" if dispater_high else
                    "attention not flagged HIGH; page names +3 only for HIGH, "
                    "no other modifier stated -- rolled flat")
        elif name.startswith("The abishai"):
            mod = 2 if abishai_holds else 0
            note = ("reporting posture holds: +2 per page" if abishai_holds
                    else "posture broken -- page's +2 not applied")
        total, line = roll(20, name, mod, note)
        out.append(line)
        out.append(f"    -> {band_lookup(NPC_BANDS, total)}")
        if total >= 19:
            triggers.append(f"HELL-SIDE DOOR-KNOCK 19+ (4.5A): {name} -- "
                            f"demand, summons, assessment, or envoy; scene "
                            f"priority alongside Step 4's 19s.")
    # -- 4.5B corridor ecology ----------------------------------------------
    out.append("\n  4.5B -- CORRIDOR ECOLOGY (1d20 per session)")
    total, line = roll(20, "corridor ecology")
    out.append(line)
    out.append(f"    -> {band_lookup(CORRIDOR_TABLE, total)}")
    if 4 <= total <= 7:
        size, sline = roll_expr_2d6x10()
        out.append(sline)
        out.append(f"    -> muster size {size}")
    if total == 20:
        age, aline = roll(6, "anomaly age-band")
        out.append(aline)
        out.append(f"    -> age-band: {band_lookup(CORRIDOR_AGE_BAND, age)}")
    if total <= 3:
        triggers.append("CORRIDOR SUCCESSOR PRESSURE (4.5B 1-3): something "
                        "big tests the vacuum; names itself within a tenday.")
    # -- 4.5C Blood War tide ------------------------------------------------
    out.append("\n  4.5C -- BLOOD WAR TIDE (1d12 per Hell-tenday or session, "
               "whichever is longer)")
    total, line = roll(12, "Blood War tide")
    out.append(line)
    out.append(f"    -> {band_lookup(TIDE_TABLE, total)}")
    if total == 12:
        triggers.append("BLOOD WAR TIDE 12 (4.5C): a named engagement within "
                        "sight or sound; Bel's demands, salvage rights, "
                        "demon-rout spillover all live.")
    # -- 4.5D garrison interior ---------------------------------------------
    out.append("\n  4.5D -- GARRISON INTERIOR (1d20 per session; the 30,000 "
               "as cast)")
    total, line = roll(20, "garrison interior")
    out.append(line)
    out.append(f"    -> {band_lookup(GARRISON_TABLE, total)}")
    if total <= 4:
        note = ("" if total <= 3 else " (page's order note names '1-3 "
                "successor/seam band' but the 4.5D seam band runs 1-4 -- "
                "flagged; interpret per page)")
        triggers.append(f"GARRISON SEAM-CLASS EVENT (4.5D 1-4): binding "
                        f"question / devotion anomaly; Vesper's desk.{note}")
    # -- standing texture dice ----------------------------------------------
    out.append("\n  STANDING TEXTURE DICE (World-Move Law, boot page: run "
               "under the Law, ALWAYS logged to the Register)")
    for i in range(hell_cycles):
        total, line = roll(8, f"dawn weather, Hell-cycle open {i + 1}")
        out.append(line)
        out.append("    -> rotate the sensorium -- Avernus has weather; "
                   "interpret in-scene.")
    total, line = roll(20, "dilation bill (once per session)")
    out.append(line)
    out.append("    -> the 27:1 gradient costs a named person something; "
               "interpret and BILL it (Law move type).")
    triggers.append("STANDING TEXTURE (Law): dawn weather + dilation bill "
                    "rolled above -- every exercise writes a World-Move "
                    "Register entry (DB 4ec10078-f1d0-467f-abf5-6542803658f0).")


def step45e_ledger(out, triggers, city_years: int):
    out.append(hdr(f"STEP 4.5E -- HELL-QUARTER LEDGER ({city_years} City-year "
                   f"block(s); 1 City-year ~ a Material fortnight at 27:1; "
                   f"batch blocks on skips)"))
    out.append(f"  Six d20 per block; interpret each die against the District "
               f"Gazetteer page {GAZETTEER_PAGE} (band meanings and live "
               f"state live on the page). Threshold: 1-3 or 18+ on any die, "
               f"or any Finance crit, is a World-Move Law trigger. Block "
               f"totals rewrite the city page's live numbers.")
    for block in range(1, city_years + 1):
        out.append(f"\n  CITY-YEAR BLOCK {block}:")
        for die_name in LEDGER_DICE:
            total, line = roll(20, die_name)
            out.append(line)
            if total <= 3 or total >= 18:
                triggers.append(f"HELL-QUARTER LEDGER (4.5E block {block}): "
                                f"{die_name} = {total} (threshold 1-3/18+) -- "
                                f"cash in-session or roll at close; Register "
                                f"entry.")
        out.append("    (Finance crit determination is City Stats machinery "
                    "-- NO COVERAGE here; interpret the Economy die on the "
                    "Gazetteer page.)")


def step5_veil(out, triggers):
    out.append(hdr("STEP 5 -- VEIL INTELLIGENCE SURFACE (d20; 15+ surfaces)"))
    total, line = roll(20, "Veil passive collection")
    out.append(line)
    if total >= 15:
        out.append("  -> INTELLIGENCE SURFACES this session. Category d8:")
        cat, cline = roll(8, "Veil category")
        out.append(cline)
        out.append(f"    -> {cat}: {VEIL_CATEGORIES[cat]}")
        out.append("    Becomes known-by-Arik state; Lirien presents and "
                   "lets Arik decide.")
    else:
        out.append("  -> No surfaced intelligence (14 or lower). The Veil is "
                   "still running.")

def step7_antagonists(out, triggers, lolth_acc: Optional[int]):
    out.append(hdr("STEP 7 -- ANTAGONIST POSTURE CLOCKS (quarterly interval "
                   "elapsed)"))
    for label, bands in (("Aldric Steelgaze stance", ALDRIC_BANDS),
                         ("Sembian Merchant Council trade-war posture", SEMBIAN_BANDS),
                         ("Thayan posture (post-Unbinding retaliation timer)", THAYAN_BANDS)):
        total, line = roll(20, label)
        out.append(line)
        out.append(f"    -> {band_lookup(bands, total)}")
        if total >= 19 or (bands is THAYAN_BANDS and total == 20):
            triggers.append(f"ANTAGONIST TOP BAND (Step 7): {label} = {total} "
                            f"({band_lookup(bands, total)}) -- GM-private; "
                            f"surfaces through visible events only.")
    out.append("\n  LOLTH ATTENTION ACCUMULATOR (flag input, never stored):")
    if lolth_acc is None:
        out.append("    (no --lolth-accumulator supplied -- read the current "
                   "value from the protocol page's Step 7 before interpreting)")
    else:
        out.append(f"    Current accumulator (as supplied): {lolth_acc}")
        out.append(f"    Thresholds: {LOLTH_THRESHOLDS}")
        for th in (12, 18, 24):
            if lolth_acc >= th:
                triggers.append(f"LOLTH ACCUMULATOR AT/OVER {th} (supplied "
                                f"value {lolth_acc}) -- threshold effect live.")
    out.append("  Note: advancing antagonist clocks does not always produce "
               "a scene this session -- sometimes the result is a noted "
               "state-change for future surface-up.")


LAW_REMINDER = """\
  World-Move Law general trigger states (boot page, binding) -- check every
  INTERPRETED result against these as well:
    attention/notice HIGH - reaction <=7 or >=16 - success margin <=3 -
    any clock at 8+ - any watcher/adversary that logged the player's
    activity - a rolled cost the player hasn't felt yet.
  Every trigger state MUST produce DESCRIBE / HINT / MOVE / BILL inside the
  session; uncashed states are rolled at close (deferred_dice.py cashin) and
  seeded into the next boot. Every exercise writes a World-Move Register
  entry (DB 4ec10078-f1d0-467f-abf5-6542803658f0, data source
  f10ce74a-dcdd-4c4d-9034-5a7a3cd9b52b)."""


def threshold_summary(out, triggers):
    out.append(hdr("THRESHOLD SUMMARY -- WORLD-MOVE LAW TRIGGER STATES "
                   "(cash in-session or roll at close; none survive a close "
                   "uncashed)"))
    if triggers:
        for i, t in enumerate(triggers, 1):
            out.append(f"  {i}. {t}")
    else:
        out.append("  (no threshold states rolled this open -- standing "
                   "texture dice still log to the Register)")
    out.append("")
    out.append(LAW_REMINDER)

# ============================================================================
# SELFTEST
# ============================================================================

def selftest() -> int:
    ok = True

    def expect(label, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        ok = ok and cond

    print("### session_open.py SELFTEST ###\n")
    print("-- band structure: full 1..20 coverage, no gaps/overlaps --")
    for name, bands, top in (("Quenthel", QUENTHEL_BANDS, 20),
                             ("Gromph", GROMPH_BANDS, 20),
                             ("Thread", THREAD_BANDS, 25),
                             ("NPC", NPC_BANDS, 25),
                             ("Corridor", CORRIDOR_TABLE, 20),
                             ("Tide", TIDE_TABLE, 12),
                             ("Garrison", GARRISON_TABLE, 20),
                             ("Aldric", ALDRIC_BANDS, 20),
                             ("Sembian", SEMBIAN_BANDS, 20),
                             ("Thayan", THAYAN_BANDS, 20)):
        cover = all(sum(1 for lo, hi, _ in bands if lo <= v <= hi) == 1
                    for v in range(1, top + 1))
        expect(f"{name} bands cover 1..{top} exactly once", cover)

    print("\n-- band boundaries vs the protocol page --")
    expect("Quenthel 8 -> Information / 9 -> Attendance ('1-8: Information / "
           "9-13: Attendance')",
           band_lookup(QUENTHEL_BANDS, 8) == "Information"
           and band_lookup(QUENTHEL_BANDS, 9) == "Attendance")
    expect("NPC 14 -> routine / 15 -> needs decision ('10-14 ... 15-18')",
           "Routine" in band_lookup(NPC_BANDS, 14)
           and "decision" in band_lookup(NPC_BANDS, 15))
    expect("Corridor 3 -> successor / 4 -> muster ('1-3 ... 4-7')",
           "Successor" in band_lookup(CORRIDOR_TABLE, 3)
           and "Muster" in band_lookup(CORRIDOR_TABLE, 4))
    expect("Gromph 10 -> no case / 11 -> case ('1-10 ... 11-16')",
           "No case" in band_lookup(GROMPH_BANDS, 10)
           and "surfaces" in band_lookup(GROMPH_BANDS, 11))
    expect("Thread 16 -> productive / 17 -> breakthrough ('11-16 ... 17-19')",
           "Productive" in band_lookup(THREAD_BANDS, 16)
           and "Breakthrough" in band_lookup(THREAD_BANDS, 17))
    expect("Tide 11 -> nears / 12 -> named engagement ('9-11 ... 12')",
           "nears" in band_lookup(TIDE_TABLE, 11)
           and "NAMED" in band_lookup(TIDE_TABLE, 12))

    print("\n-- four-throw binder --")
    expect("mode binds: [7,7,3,19] -> 7", bind_four([7, 7, 3, 19]) == (7, "mode"))
    expect("median binds: [2,5,9,16] -> 7 (mean of middle two)",
           bind_four([2, 5, 9, 16]) == (7, "median"))
    expect("two-pair tie falls to median: [5,5,9,9] -> 7",
           bind_four([5, 5, 9, 9]) == (7, "median"))
    expect("fractional median rounds down: [2,4,7,18] -> 5",
           bind_four([2, 4, 7, 18]) == (5, "median"))

    print("\n-- dice sanity: 60 d20 throws in range, not all identical --")
    vals = [_throw(20) for _ in range(60)]
    expect("all in 1..20", all(1 <= v <= 20 for v in vals))
    expect("not all identical (no-repeat sanity)", len(set(vals)) > 1)

    print("\n-- threads template round-trip --")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "threads.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(THREADS_TEMPLATE, f, indent=2)
        loaded = load_threads(p)
        expect("template loads; 7 threads, 8 principals",
               len(loaded["threads"]) == 7 and len(loaded["principals"]) == 8)
        expect("Gromph modifier is null (variable per page)",
               loaded["principals"][7]["modifier"] is None)

    print(f"\nSELFTEST {'PASSED' if ok else 'FAILED'}.")
    return 0 if ok else 1

# ============================================================================
# CLI
# ============================================================================

def main():
    global SINGLE_THROW
    p = argparse.ArgumentParser(
        description="Session Start Protocol dice layer (Arik surface "
                    "campaign). Prints the read checklist, rolls every "
                    "gated step in protocol order, ends with the World-Move "
                    "threshold summary and the Step 8 premise checklist.")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--write-threads-template", action="store_true",
                   help="Emit the current protocol thread/principal table as "
                        "the starter threads.json and exit.")
    p.add_argument("--threads", default="threads.json",
                   help="Path to the user-maintained threads.json "
                        "(default: ./threads.json).")
    p.add_argument("--months-elapsed", type=int, default=0,
                   help="Calendar months elapsed since last session "
                        "(1+ flags the Step 6 monthly business phase).")
    p.add_argument("--quarter-elapsed", action="store_true",
                   help="Quarterly interval elapsed -> roll Step 7.")
    p.add_argument("--quenthel-due", action="store_true",
                   help="Quenthel-Favor interval (3-6 in-world months) "
                        "elapsed -> roll Step 2.")
    p.add_argument("--gromph-case-due", action="store_true",
                   help="3 in-world months since last Cases-for-Gromph roll "
                        "-> roll Step 2.5.")
    p.add_argument("--gromph-mod", type=int, default=None,
                   help="Gromph's variable Step 4 modifier this session "
                        "(per Quenthel-Favor result). Omit to roll flat "
                        "with a variable-modifier note.")
    p.add_argument("--hell-side", action="store_true",
                   help="Play position is Hell-side -> run Step 4.5A-D + "
                        "standing texture dice.")
    p.add_argument("--hell-cycles", type=int, default=1,
                   help="Hell-cycle scene-opens this session (dawn weather "
                        "d8 each; default 1).")
    p.add_argument("--dispater-high", action="store_true",
                   help="Dispater attention is HIGH -> +3 on his 4.5A roll "
                        "(per page).")
    p.add_argument("--abishai-posture-broken", action="store_true",
                   help="Abishai reporting posture no longer holds -> drop "
                        "their +2.")
    p.add_argument("--city-years", type=int, default=0,
                   help="City-year blocks to roll for Step 4.5E (Inevitable "
                        "City ledger). 0 = skip.")
    p.add_argument("--lolth-accumulator", type=int, default=None,
                   help="Current Lolth accumulator value (flag input, "
                        "echoed against 12/18/24; never stored).")
    p.add_argument("--four-throw", action="store_true",
                   help="Four-throw mode-else-median bind instead of single "
                        "raw dice. Use when a roll is a RULING wanting "
                        "stability; play rolls stay single so outliers "
                        "(crits, crises, windfalls) remain possible "
                        "(Chad ruling, 17 Jul 2026).")
    p.add_argument("--single-throw", action="store_true",
                   help="(default) Kept for compatibility; single raw dice.")
    p.add_argument("--log", default=None,
                   help="Append the full roll log to FILE as a dated block "
                        "(the protocol requires roll logging).")
    args = p.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if args.write_threads_template:
        path = args.threads
        if os.path.exists(path):
            raise SystemExit(f"{path} exists -- move it aside first.")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(THREADS_TEMPLATE, f, indent=2)
        print(f"Wrote starter threads file: {path}")
        print("Maintain it by hand as the protocol page's thread list "
              "changes; the page wins on conflict.")
        return

    SINGLE_THROW = not args.four_throw   # play default: single (17 Jul 2026)
    data = load_threads(args.threads)
    triggers: List[str] = []
    out: List[str] = []

    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    out.append("=" * 68)
    out.append(f"SESSION OPEN -- ARIK SURFACE CAMPAIGN -- {stamp}")
    out.append(f"Protocol: Notion 364e8214-84b0-8144-bfc4-cd1f25ae3c3a "
               f"(amendments integrated)")
    out.append(f"Dice: python secrets; "
               f"{'single raw throws' if SINGLE_THROW else 'four throws, mode-else-median (Standing Law G2)'}")
    out.append("=" * 68)
    out.append("")
    out.append(READ_CHECKLIST)

    out.append(hdr("STEP 1 -- ADVANCE THE DATE"))
    out.append(f"  Declare the current in-world date (from Step 0 reads). "
               f"Months elapsed (as supplied): {args.months_elapsed}.")
    if args.months_elapsed >= 1:
        out.append("  -> MONTHLY BUSINESS PHASE flagged: run at the end of "
                   "this opening protocol (Step 6).")

    if args.quenthel_due:
        step2_quenthel(out, triggers)
    else:
        out.append(hdr("STEP 2 -- QUENTHEL-FAVOR CLOCK"))
        out.append("  Interval not elapsed (--quenthel-due not set); check "
                   "last roll date on page " + QUENTHEL_PAGE + ".")

    if args.gromph_case_due:
        step25_gromph(out, triggers)

    step3_threads(out, triggers, data.get("threads", []))
    step4_npcs(out, triggers, data.get("principals", []), args.gromph_mod)

    if args.hell_side:
        step45_hell(out, triggers, args.dispater_high,
                    not args.abishai_posture_broken, args.hell_cycles)
    if args.city_years > 0:
        step45e_ledger(out, triggers, args.city_years)

    step5_veil(out, triggers)

    out.append(hdr("STEP 6 -- EMPIRE OPERATIONS ENGINE (monthly phase)"))
    if args.months_elapsed >= 1:
        out.append("  Month elapsed -> run the empire-operations-engine "
                   "monthly business phase (Vara briefing, neglect tracking, "
                   "entity status, revenue/cost reconciliation). Its dice "
                   "live in that engine, not here.")
    else:
        out.append("  No month elapsed -- skipped.")

    if args.quarter_elapsed:
        step7_antagonists(out, triggers, args.lolth_accumulator)
    else:
        out.append(hdr("STEP 7 -- ANTAGONIST POSTURE CLOCKS"))
        out.append("  Quarterly interval not elapsed (--quarter-elapsed not "
                   "set) -- skipped.")

    threshold_summary(out, triggers)
    out.append("")
    out.append(STEP8_CHECKLIST)

    text = "\n".join(out)
    print(text)

    if args.log:
        with open(args.log, "a", encoding="utf-8") as f:
            f.write(f"\n\n{'#' * 68}\n# ROLL LOG BLOCK -- {stamp}\n"
                    f"{'#' * 68}\n{text}\n")
        print(f"\n[roll log appended to {args.log}]")


if __name__ == "__main__":
    main()
