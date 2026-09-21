# EV-05 -- The death of Sanguinius

*Class:* death  
*Witnesses:* 3  

| Address | Unit title | Narrator | Mode | Synchronism (as the verse states it) | Quote | Verification |
|---|---|---|---|---|---|---|
| TEATD2 8:xvii | Until we meet again | Horus Lupercal | second | none stated; Horus on his knees, eviscerated, then the eighth angle | "You reach along the eighth angle of space and grab." | corpus-exact |
| TEATD3 9:i | Red and Black | omniscient, over the Angel's body | omniscient | afterwards | "The Angel's eyes are open, afterwards." | corpus-exact |
| TEATD3 9:ii | Horus awaits | Rogal Dorn, told by a companion | hearsay | reported to Dorn while he surveys the warp-state landscape | "She tells him his brother is dead." | corpus-exact |

## Disagreements (kept, not harmonised)

Three modes, one death: perpetrator's second person, an unanchored view of the corpse, and hearsay. No witness gives a clock; the only relative marker is the word afterwards.

## Resolving a witness

```
python scripts/verse_address.py --map reference/addresses/<book>.address.json --resolve "TEATD2 8:xvii ¶1" --book <corpus>/<file>
```

Labels: the quote and address are SOURCE-VERIFIED when the verification column reads corpus-exact; the narrator and mode are the registry author's reading (INFERRED); the synchronism is only what the verse states.
