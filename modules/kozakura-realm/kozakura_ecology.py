"""Kozakura Spirit Ecology roller (KOZAKURA_SPIRIT_ECOLOGY.md).

Python secrets only. The Realm Pulse uses the arc's standing method: 3d6 thrown
four times, lower median (second-lowest), no rerolls. Layer tables use their
native dice with the Calamity-tier modifiers the module specifies.

Usage: python3 kozakura_ecology.py --tier N [--pulse-only] [--label TEXT]
Prints every die and appends the record to kozakura_ecology_rolls.json.
"""
import argparse, datetime, json, os, secrets

def d(n): return secrets.randbelow(n) + 1

def lower_median():
    t = [sum(d(6) for _ in range(3)) for _ in range(4)]
    return t, sorted(t)[1]

PULSE = [(7, "Quiet"), (9, "Background"), (11, "Active"), (13, "Restless"),
         (15, "Summer Flies"), (17, "Unseated"), (19, "Long Night"), (99, "Iwato")]
DISASTER = {1: "Earthquake", 2: "Earthquake", 3: "Storm/typhoon", 4: "Storm/typhoon",
            5: "Cold", 6: "Cold"}
SCALE = {1: "A haunting", 2: "A dispute", 3: "A dispute", 4: "A displacement",
         5: "A displacement", 6: "A war", 7: "A god stirs", 8: "Casting"}
CATEGORY = ["Household/tsukumogami", "Water", "Sea", "Mountain powers", "Shapeshifters",
            "Oni", "Restless dead", "Serpents/dragons", "Vermin powers",
            "Trees/plants", "Weather/fire", "Wrong"]
BEHAVIOR = ["Feeding", "Claiming", "Keeping its Rule", "Procession", "Bargaining",
            "Haunting", "Displaced", "Possessing"]
CAUSE = ["Season/festival", "A broken Rule", "Absent/dead owner", "Pollution",
         "A myth rhyming", "Human exploitation", "The Calamity", "Ancient cycle"]
HITS = ["Road/ford/pass", "Shrine/rite", "Rice/stores", "The sea", "Village safety",
        "The lord's house", "Trade", "The mission itself"]
COST = ["Fear only", "Sickness/livestock/property", "Sickness/livestock/property",
        "Deaths 1-5", "Deaths 1-5", "Deaths 6+", "A village lost", "A district lost"]
RESPONSE = {1: "Nothing", 2: "Village rite", 3: "Village rite", 4: "Priest/onmyoji holding",
            5: "Priest/onmyoji holding", 6: "Resolved, Rule still broken"}
APPROACH = ["Exorcism/blade", "Appeasement", "Restore the Rule", "Bargain",
            "Enshrinement", "Set a rival on it", "Hunters", "Play the myth"]
COMPLICATION = ["Sacred", "Thin hour/place only", "Someone's ancestor", "Two owners",
                "Holding something worse down", "Unknown Rule", "The lord forbids it", "None"]
REQUIREMENT = {1: "Priest + offering, a night", 2: "Mission intervention, a day",
               3: "Mission intervention, a day", 4: "Shrine rite, a tenday",
               5: "Shrine rite, a tenday", 6: "A god's attention"}
CASCADE = ["Clean", "Another fills the niche", "Another fills the niche",
           "The rival takes it", "The rival takes it", "Keystone falls: check raise",
           "Calamity +1"]
THREAD = ["The Storm's seat", "The Sun's court", "The Yakumo-ha", "The Orochi remnant",
          "The dead", "The Red Gate", "A human power", "Standalone"]

def band(table, v):
    for top, name in table:
        if v <= top: return name

def situation(tier, log, min_scale=1):
    def rec(k, raw, val): log.append({"step": k, "raw": raw, "result": val}); print(f"  {k}: {raw} -> {val}")
    r = d(6); s = max(min_scale, min(8, r + (tier + 1) // 2)); rec("0 scale (d6+ceil(tier/2))", r, SCALE[s])
    r = d(12); rec("1A category (d12)", r, CATEGORY[r - 1])
    r = d(8); rec("1B behavior (d8)", r, BEHAVIOR[r - 1])
    r = d(8); c = r
    if tier >= 4 and r <= 3: c = 7
    elif tier >= 2 and r == 1: c = 7
    rec("1C cause (d8, Calamity override)", r, CAUSE[c - 1])
    r = d(8); rec("2A hits (d8)", r, HITS[r - 1])
    r = d(6); rec("2B cost (d6+tier)", r, COST[min(8, r + tier) - 1])
    r = d(6); rec("2C response (d6-tier, min 1)", r, RESPONSE[max(1, r - tier)])
    r = d(8); rec("3A approach (d8)", r, APPROACH[r - 1])
    r = d(8); rec("3B complication (d8)", r, COMPLICATION[r - 1])
    r = d(6); rec("3C requirement (d6)", r, REQUIREMENT[r])
    r = d(6); rec("4A cascade (d6+floor(tier/2))", r, CASCADE[min(7, r + tier // 2) - 1])
    r = d(8); rec("4B thread (d8)", r, THREAD[r - 1])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", type=int, required=True, choices=range(0, 6))
    ap.add_argument("--pulse-only", action="store_true")
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    log = []
    throws, med = lower_median(); pulse = med + 2 * a.tier; name = band(PULSE, pulse)
    print(f"REALM PULSE: throws {throws}, lower median {med} + 2x tier {a.tier} = {pulse} -> {name}")
    log.append({"step": "pulse", "throws": throws, "median": med, "total": pulse, "band": name})
    n = {"Quiet": 0, "Background": 1, "Active": 1, "Restless": 2, "Summer Flies": 1,
         "Unseated": 1, "Long Night": 2, "Iwato": 0}[name]
    if name in ("Unseated", "Long Night"):
        r = d(6); print(f"  disaster (d6): {r} -> {DISASTER[r]}"); log.append({"step": "disaster", "raw": r, "result": DISASTER[r]})
    if not a.pulse_only:
        for i in range(n):
            print(f"SITUATION {i + 1}"); situation(a.tier, log, 4 if name == "Summer Flies" else 1)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kozakura_ecology_rolls.json")
    data = json.load(open(path)) if os.path.exists(path) else {"method": "Python secrets; pulse = 3d6 x4 lower median + 2x tier; layer tables native dice", "rolls": []}
    data["rolls"].append({"utc": datetime.datetime.utcnow().isoformat(timespec="seconds"), "label": a.label, "tier": a.tier, "log": log})
    json.dump(data, open(path, "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
