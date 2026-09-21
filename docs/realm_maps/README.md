# Realm map proofs — Regno Kao folios

Example output of `scripts/realm_map.py` for three realms of *The End and the
Death*, kept so a session without a Python runtime can still read what a
folio looks like. Everything in the `.svg` and `.area.md` files below the
SOURCE-VERIFIED facts block is **ROLLED** (real dice, raws in the ledger at the
bottom of each sheet) or **INFERRED** (the myth key). None of it is canon,
none of it is source, and a live session rolls its own folio rather than
reusing these.

```
python scripts/realm_map.py long_woe.realm.state.json new --realm "Long Woe" --areas d8 --band 2
python scripts/realm_map.py long_woe.realm.state.json render
```

| Realm | Archetype | Files |
|---|---|---|
| Long Woe | wilderness | `long_woe.svg`, `long_woe.area.md` |
| The Gulf of Lament | crossing | `gulf_of_lament.svg`, `gulf_of_lament.area.md` |
| The Inevitable City, primeval stratum | composite-city | `inevitable_city_primeval.svg`, `inevitable_city_primeval.area.md` |
| The Inevitable City (band 3, d10 areas) | composite-city | `inevitable_city.svg`, `inevitable_city.area.md` |
| The Marcher Fortress and the Marches (reached through the city's A5 splice) | fortress | `marcher_fortress.svg`, `marcher_fortress.area.md` |

Beyond the trilogy: `new --realm-file <definition.json>` rolls a campaign
realm from a definition the owning project keeps (the Malcador prison's
shifting country lives in the vault, not here); `populate --pool daemon|fiend|both`
seats Neverborn or fiends per area from the engine's bestiaries as cited rows;
`export-sectors --out sectors.json` writes the rolled areas as a sector table
for the vault's `realm_population.py` (`import_rolled_sectors`) plus an atlas
block in that project's own row format.

The state files that produced them are throwaway (`*.state.json` is
gitignored). Re-rendering from a state file is deterministic; rolling a new
state is not, by design.

Routing note: the `empyrean-siege-gm` skill's TEATD band section should name
`scripts/realm_map.py` and the `*.realm.state.json` convention so a future
session reaches for the roller instead of improvising psychotecture. That
skill syncs outside this repository and is edited separately.
