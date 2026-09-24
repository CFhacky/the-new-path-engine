#!/usr/bin/env python3
"""teatd_realm_harvest.py -- The End and the Death warp-realm index (system: WH40K Novel).

THE PROCESS (the 40K shelf): other SOURCES are welcome in the reference layer
AS LONG AS each is clearly LABELLED. This family indexes the named and
materially described warp realms, exoplanar locations and dimensional
conditions of Dan Abnett's *The End and the Death* Volumes I-III (Black
Library, Siege of Terra), stamped `"system": "WH40K Novel"`. It is the
source-of-record for `scripts/realm_map.py` (area maps per realm) and for the
TEATD psychotecture bands of the empyrean-siege-gm skill.

    reference/teatd_realm_index.json -- every realm: name, aliases, archetype,
                                        attestations (volume, chapter, verse,
                                        short quote, verification), locked
                                        source facts, myth key + citation.
    reference/teatd_realm_index.md   -- the same, for human eyes.

WHAT IS AUTHORED HERE vs. WHAT IS SOURCE
    SOURCE (label SOURCE-VERIFIED): the attestations and `facts` rows, each tied
        to a chapter:verse of the trilogy. They come from the 2026-09-21 full
        sweep of the three Notion page bodies (page ids below) and from the
        Notion re-check recorded in each attestation's `verification` field.
        A `verification` of "index-transcribed" means the quote was carried
        over from the sweep index and has NOT been re-checked against the
        book; treat it as a citation to verify, never as verbatim wording.
    INFERRED (label INFERRED): `myth_key` -- the biblical / mythological
        referent behind each realm and the one-line "law of the place" that
        the map resolver applies. In-fiction justification: Vol. II 5:viii,
        where Malcador states that humanity's hells are refracted glimpses of
        the empyrean, and Vol. I 4:xviii, the *Regno Kao* folio. These are
        the author's reading of the text, not the text.
    CONTROL: `archetype` (one of the eight mappable grammars, or "condition"
        for cosmological designations that are not places) is an authored
        routing label for the resolver.

CORPUS
    When `--corpus DIR` points at a folder holding the three volumes as text
    (vol1.md / vol2.md / vol3.md, or files whose names contain "Volume I",
    "Volume II", "Volume III"), every quote is located exactly, its line
    number and detected verse heading are recorded, and `verification`
    becomes "corpus-exact". The default corpus folder is `corpus/teatd/` in
    this repository; without it the script prints NO COVERAGE and the
    committed quotes keep their sweep/Notion status.

WORKFLOW
    python teatd_realm_harvest.py                      # (re)build the index
    python teatd_realm_harvest.py --corpus I:/Sourcebooks/_text/Warhammer/Novels/TEATD
    python teatd_realm_harvest.py --search "Long Woe"
    python teatd_realm_harvest.py --selftest

GOVERNING SOURCES
    Notion / Horus Heresy Source Library:
        The End and the Death Volume I    1f5e8214-84b0-810f-a31e-e15021ec89fc
        The End and the Death Volume II   1f5e8214-84b0-81c2-8d41-f86a2329b9dc
        The End and the Death Volume III  1f5e8214-84b0-81c0-b251-fe878a37aee3
    Sweep record: end_and_death_warp_realms_index.md (SOURCE SWEEP COMPLETE
        2026-09-21; organised Volume -> chapter:verse).
    empyrean-siege-gm skill, "TEATD bands (modules 05-07)": expected vs.
        experienced location are tracked separately; map contradiction and
        false continuity are hazards, not flavour.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
OUT_JSON = REPO / "reference" / "teatd_realm_index.json"
OUT_MD = REPO / "reference" / "teatd_realm_index.md"
SYSTEM = "WH40K Novel"
SWEEP_DATE = "2026-09-21"

VOLUMES = {
    1: {"key": "vol1", "book": "The End and the Death Volume I",
        "notion_page_id": "1f5e8214-84b0-810f-a31e-e15021ec89fc",
        "chapters": "1-4", "clean_text_chars": 882371},
    2: {"key": "vol2", "book": "The End and the Death Volume II",
        "notion_page_id": "1f5e8214-84b0-81c2-8d41-f86a2329b9dc",
        "chapters": "5-8", "clean_text_chars": 878638},
    3: {"key": "vol3", "book": "The End and the Death Volume III",
        "notion_page_id": "1f5e8214-84b0-81c0-b251-fe878a37aee3",
        "chapters": "9-10", "clean_text_chars": 776053},
}

# The eight mappable grammars plus the non-place label. realm_map.py owns the
# tables; this is the routing vocabulary and its one-line meaning.
ARCHETYPES = {
    "composite-city": "Stolen districts stitched into one urban body; deeper is older.",
    "labyrinth": "A structure that closes behind you; the exit is granted, not found.",
    "crossing": "A bridge, stair, gate or causeway between two realms; the crossing is the encounter.",
    "junction": "An intersection, oblique, conjunction or angle: a transit coordinate, not a place to stay.",
    "fortress": "A warded seat on a contested margin; the approaches are the fight.",
    "wilderness": "Open or grown terrain that is itself alive, hostile, or dying.",
    "shore": "An edge of the sea of the warp: tide, depth, islets, the far dark.",
    "repository": "A place that keeps things: souls, dreams, roots, records.",
    "condition": "A cosmological designation or overlay, not an area. The resolver applies it as a modifier and refuses to map it.",
}

# Edge vocabulary the trilogy itself uses for moving between realms (9:xxi,
# 10:iii, 10:viii). The resolver types every exit with one of these.
EDGE_TYPES = {
    "angle": "a warped angle or oblique step sideways (9:xxi, 10:v)",
    "intersection": "a numbered intersection of the immaterial (9:xxi)",
    "conjunction": "a numbered conjunction between two realms (9:xxi)",
    "oblique": "an oblique plane with its own fixed sky (9:xxi)",
    "splice": "a doorway-sharp tear between material and immaterial (10:iii)",
    "recursion": "the containing realm found inside the contained one (10:viii)",
}


def A(vol: int, ch: int, verse: str, quote: str, **kw) -> Dict:
    """One attestation: where the book says it, and the short quote."""
    row = {"volume": vol, "chapter": ch, "verse": verse, "quote": quote,
           "verification": kw.pop("verification", "index-transcribed")}
    row.update(kw)
    return row


def M(referent: str, citation: str, rule: str, canon_first: Optional[str] = None) -> Dict:
    """Myth key: referent, its citation, and the law of the place. INFERRED."""
    key = {"referent": referent, "citation": citation, "rule": rule, "label": "INFERRED"}
    if canon_first:
        key["canon_first"] = canon_first
    return key


# ---------------------------------------------------------------------------
# THE ROSTER. Order: Volume I, II, III, then cross-volume conditions.
# ---------------------------------------------------------------------------
REALMS: List[Dict] = [
    # ---------------------------------------------------------------- Vol I
    {
        "name": "The Webway", "aliases": [],
        "archetype": "labyrinth", "classification": "Named subdimension / transit network",
        "attestations": [
            A(1, 1, "xv", "a labyrinthine subdimension that stretches across the galaxy"),
            A(1, 1, "xv", "subspace network of travel and communication"),
            A(1, 2, "xii", "psychoplastic halls"),
        ],
        "facts": [
            "Inherited and named by the aeldari; a subspace travel-and-communication network.",
            "Transit is direct, comparatively swift, and insulated from ordinary warp hazards.",
            "Runs under, around and above the warp rather than through realspace; the Emperor's Great Work was to reclaim it.",
            "Its halls are psychoplastic; Vulkan claws his way back along them (2:xii); pursuing daemons echo through them as Magnus is banished (1:xxiii).",
        ],
        "myth_key": M("The labyrinth of Daedalus and Ariadne's thread",
                      "Ovid, Metamorphoses VIII.152-182; Apollodorus, Epitome 1.9",
                      "Transit is safe only along a held thread. Leave the thread and the warp outside the wall is the encounter.",
                      canon_first="Warhammer 40,000 setting canon (name predates TEATD)"),
    },
    {
        "name": "Other spaces, realms and layers of creation", "aliases": ["other flavours of reality"],
        "archetype": "condition", "classification": "Unnamed cosmological realm-category",
        "attestations": [A(1, 1, "xvi", "other spaces, other realms, other layers of creation and other flavours of reality")],
        "facts": ["Catalogue of invader provenance; distinguishes material worlds from other ontological locations, with the warp as one member of the set."],
        "myth_key": M("The many mansions / the seven heavens",
                      "John 14:2; 2 Corinthians 12:2; 1 Enoch 71",
                      "Overlay: the folio may hold realms that are not warp at all. Tag the unknown ones as such rather than forcing them into Chaos."),
    },
    {
        "name": "The Outer Darkness", "aliases": [],
        "archetype": "shore", "classification": "Banishment destination beyond the webway",
        "attestations": [A(1, 1, "xxiii", "into the outer darkness")],
        "facts": ["Magnus's deathless corpse is banished there after Vulkan defeats him; used as a destination, not an adjective.",
                  "The verse does not define whether it is deep warp, exterior void or a distinct realm."],
        "myth_key": M("The outer darkness of the Gospel parables",
                      "Matthew 8:12; 22:13; 25:30 (\"cast him into outer darkness; there shall be weeping and gnashing of teeth\")",
                      "A terminus at the folio's edge. One-way: nothing banished there returns on its own, and no exit is rolled."),
    },
    {
        "name": "Uigebealach", "aliases": ["the labyrinth-knot", "the crossroads of inertia"],
        "archetype": "junction", "classification": "Webway singularity-node / warp crossroads / labyrinth-knot",
        "attestations": [
            A(1, 2, "xii", "the unmoving Uigebealach of the webway's singularity-node"),
            A(1, 4, "xviii", "whiche it is and is not"),
            A(3, 10, "xvi", "the labyrinth-knot of Uigebealach in the blazing warp"),
            A(3, 10, "xviii", "the crossroads of inertia in Uigebealach"),
        ],
        "facts": [
            "A known singularity-node of the webway, explicitly associated with neverness and metaphysical discontinuity (2:xii).",
            "The Regno Kao folio places the Inevitable City close by it, 'whiche it is and is not' (4:xviii; archaic spelling in the folio).",
            "A labyrinth-knot in the blazing warp (10:xvi).",
            "At its crossroads the unquiet realms of the dead and the damned, the lost and the psychic part ways as reality re-separates (10:xviii).",
            "The index keeps all four states; the tool must not collapse them into one identity.",
        ],
        "myth_key": M("The crossroads as psychopomp junction; Irish bealach (a pass, a way)",
                      "Hecate at the trivium (Theocritus, Idyll II; Ovid, Fasti I.141); Irish liminal lore of the crossroads; Deuteronomy 30:19 (the two ways)",
                      "Every road in meets every road out. The traveller's nature (dead, damned, lost, psychic) decides which exit takes them. No clock advances here."),
    },
    {
        "name": "The byssos and deep trenches of the warp", "aliases": ["deep trenches of the warp", "the yawning byssos"],
        "archetype": "shore", "classification": "Deep-warp abyss / ecologically differentiated deep regions",
        "attestations": [
            A(1, 2, "xii", "the deep trenches of the warp"),
            A(2, 6, "viii", "into the yawning byssos of the warp"),
        ],
        "facts": [
            "Translucent organisms from the deep trenches spill into the Throne Room when the webway door opens; they cannot survive realspace and decay into liquid organic waste (2:xii).",
            "Malcador rides the Throne like an incandescent chariot into the byssos; there he meets ragged universes, razor-edged realities, looping dimensions and incompatible nows (6:viii).",
        ],
        "myth_key": M("The abyss: Greek byssos, the sea-floor; the bottomless pit",
                      "Revelation 9:1-2 (abyssos); Genesis 1:2 (tehom); Job 38:16",
                      "Bathymetric: depth is pressure. Things from below die on surfacing, and things from above are crushed going down. Each interval deeper adds one band of exposure."),
    },
    {
        "name": "The void-wound", "aliases": [],
        "archetype": "crossing", "classification": "Tear where warp and realspace intermix",
        "attestations": [A(1, 2, "xii", "void-wound")],
        "facts": ["Terra falls into a void-wound cut by Horus, where the forces of two universes, warp and realspace, intermix and begin to devour one another."],
        "myth_key": M("The rent veil",
                      "Matthew 27:51; Isaiah 64:1 (\"Oh that thou wouldest rend the heavens, that thou wouldest come down\")",
                      "A tear, not a door. Both sides bleed through; the crossing has no fixed width and is widest where the fighting is."),
    },
    {
        "name": "The companion dimension", "aliases": ["warped exoplanar space"],
        "archetype": "condition", "classification": "Sindermann's theoretical designation for the source of Neverborn",
        "attestations": [A(1, 3, "xii", "a companion dimension, a warped exoplanar space that conjoins our own material reality")],
        "facts": ["In-universe attempt to explain Chaos without religious vocabulary; the other space has interacted with realspace throughout history and produced what was remembered as magic, daemons and visitation."],
        "myth_key": M("The interpretive key: myth as memory of the warp",
                      "Vol. II 5:viii (Malcador) is the in-fiction statement; compare Euhemerus and Plato, Phaedrus 229c-230a",
                      "Overlay: every earthly myth is a partial, degraded map. The folio may borrow any of them, labelled INFERRED."),
    },
    {
        "name": "Dorn's desert labyrinth", "aliases": ["the diverted teleport prison"],
        "archetype": "labyrinth", "classification": "Unnamed exoplanar trap-realm",
        "attestations": [A(1, 3, "xix", "caught in some gargantuan labyrinth")],
        "facts": [
            "Boundless soft yellow sand beneath a white haze; everything sunlit, no visible sun.",
            "Ancient pink stone walls cross the dunes in forking geometric lines; from the highest dune, more dunes and walls.",
            "Dorn is not aboard the Vengeful Spirit, alone, his transmission diverted; the place is a trap with no way out and perhaps no way in.",
        ],
        "myth_key": M("The desert as the perfect labyrinth",
                      "Borges, 'The Two Kings and the Two Labyrinths' (El Aleph, 1949); Herodotus II.148 (the Hawara labyrinth)",
                      "The desert is the labyrinth; the walls are decoys. The exit is granted by whoever set the trap, never found by search. Each interval of searching rolls exposure, not progress."),
    },
    {
        "name": "Xenos realms and exoplanar corpse-continents", "aliases": ["saponified landscapes"],
        "archetype": "wilderness", "classification": "Partially described non-Terran / exoplanar environments of Ollanius's long road",
        "attestations": [A(1, 3, "xx", "exoplanar corpse-continents")],
        "facts": ["Remembered stations of the long companions' journey: dark places, mummified cities, caves crushed by time, saponified landscapes of xenos realms, forgotten battlefields, ruined hive arcologies, exoplanar corpse-continents.",
                  "The passage does not resolve which are warp-local, extra-dimensional, temporal or simply alien."],
        "myth_key": M("The valley of dry bones; the dead kings stirring in Sheol",
                      "Ezekiel 37:1-10; Isaiah 14:9",
                      "The ground is a body. Disturb it and it remembers what it was; the terrain's hazard is the terrain waking."),
    },
    {
        "name": "The hell-pit and the Vengeful Spirit as realm-junction", "aliases": ["the primary pathway between realms"],
        "archetype": "crossing", "classification": "Hybrid materia-immateria environment / the ship as conduit",
        "attestations": [
            A(1, 3, "xxxii", "a hell-pit, a realm of horror"),
            A(1, 3, "xxxii", "the focus, the primary pathway between realms"),
        ],
        "facts": [
            "Malcador sees a hell-pit wrought by Horus and mistaken by Horus for heaven; the ship, Terra and the Solar Realm are half-sunk in the immaterium; the space around the Emperor is cankered voidmist of the empyrean.",
            "The ship is ceasing to be a Gloriana-class vessel: decks and hull become a bridge between realspace and Chaos, dimensions mangled, Neverborn able to walk.",
            "The entire Solar Realm is subsiding into the warp and the Vengeful Spirit is the focus, the primary pathway between realms.",
        ],
        "myth_key": M("Hell mistaken for heaven; the causeway over Chaos",
                      "Milton, Paradise Lost I.254-255 (\"The mind is its own place...\"); X.282-324 (Sin and Death build the bridge)",
                      "The ship is the causeway. Every deck is a bridge between two realms and both ends move; a route mapped on the way in is not the route out."),
    },
    {
        "name": "The Hall of Leng", "aliases": ["Leng"],
        "archetype": "crossing", "classification": "Material threshold with unusual dimensional sympathy",
        "attestations": [A(1, 4, "xiv", "Hall of Leng")],
        "facts": ["Sindermann: warped-space effects are uneven because some places are more connected or sympathetic to the immaterium; Leng is an ancient site of mystical significance and one reason the Palace stands where it does.",
                  "Mauer finds the Regno Kao folio there (4:xviii)."],
        "myth_key": M("The thin place; the plateau of Leng",
                      "Genesis 28:17 (Bethel, \"this is the gate of heaven\"); H. P. Lovecraft, The Dream-Quest of Unknown Kadath (1927)",
                      "A thin place. The door opens from the other side first; whoever waits at Leng is found before they find.",
                      canon_first="Warhammer 40,000 setting canon; Lovecraft's Leng beneath it"),
    },
    {
        "name": "Regno Kao, the Realm of Chaos", "aliases": ["A Realm of Chaos", "the realm of Chaos", "Chaos' own realm", "the empyric realm"],
        "archetype": "condition", "classification": "Explicit Chaos realm / the ancient mapped complex the other entries float in",
        "attestations": [
            A(1, 4, "xviii", "Regno Kao"),
            A(2, 5, "xi", "Once you are within the realm of Chaos, nothing retains the semblance of sense."),
            A(2, 6, "xxii", "split the empyric realm open"),
            A(2, 8, "ii", "raised a realm of Chaos"),
            A(3, 9, "ii", "Chaos' own realm"),
        ],
        "facts": [
            "An old folio in the Hall of Leng titled Regno Kao, labelled 'A Realm of Chaos', holding maps of a city/labyrinth and describing a mutable realm seen in visions and fitful dreams, moving with ethereal tides (4:xviii).",
            "The Vengeful Spirit has been devoured by the warp; remembered pieces of the ship become real in inconsistent arrangements (5:xi).",
            "Horus splits the empyric realm open; ship, Throneworld, Palace and the realms of warp and Chaos are fused and entwined (6:xxii, 6:xxv).",
            "Actae: Chaos has raised a realm of Chaos around Terra (8:ii). Dorn: 'Chaos' own realm' (9:ii).",
        ],
        "myth_key": M("Chaos as the first thing; the rude unordered mass",
                      "Hesiod, Theogony 116; Ovid, Metamorphoses I.5-9 (\"rudis indigestaque moles\")",
                      "It is the medium every mappable entry floats in. Not itself an area: the resolver refuses to map it and applies it as the folio's paper."),
    },
    {
        "name": "The Inevitable City", "aliases": ["Urbs Ineleuctabilis", "the inevitable realm", "Horus's realm", "the transmundane sprawl"],
        "archetype": "composite-city", "classification": "Central city/labyrinth of the Chaos realm-complex",
        "attestations": [
            A(1, 4, "xviii", "Urbs Ineleuctabilis"),
            A(2, 5, "xii", "Your Inevitable City. Your realm."),
            A(2, 6, "xxxv", "extruding and boring through its fabric"),
            A(2, 8, "xvi", "transmundane sprawl"),
            A(3, 10, "xii", "the inevitable realm"),
            A(3, 10, "xviii", "like some spectral parody of old Atlantis"),
        ],
        "facts": [
            "City and labyrinth at once; subject to ethereal currents; associated with Ruin and insanity; walls and turrets join across impossible distances and temporal relations; contains or adjoins the domain of the Four, vacant thrones, spirits of revenge and ruination (4:xviii).",
            "Horus: the Court surrounded by a palace, the palace a city, the city an eternal city that encompasses the galaxy (5:xii).",
            "Its architecture extrudes and bores through the Sanctum Imperialis like a parasite through a host (6:xxxv).",
            "Inner Sanctum, Vengeful Spirit, Inevitable City and Outer Palace warscape are randomly blended; Palatine, Anterior and Magnificans battlefields appear as smouldering intrusions (6:xlii).",
            "Enormous old walls, ancient dwellings, narrow cobbled streets, decaying tiled roofs, ivy-draped turrets, black stone fortifications; Palatine streets bisect decrepit alleys; walls collapse in huge masses of stone (7:i, 7:xxix).",
            "Thousands of square kilometres of transmundane sprawl disintegrate when the Emperor rejects the Dark King's power; the refabricated ship rocks on its psykanic moorings (8:xvi).",
            "Unseen by ordinary sight for centuries except to the saintly or insane; during the collapse it shelves away like a tilting continent and over roughly eight hours slides back into the midnight of the empyrean like some spectral parody of old Atlantis, leaving a few parts of itself in lost corners and hidden dim edges (10:xviii).",
            "Ollanius's cut lands him in a different part of the inevitable realm than expected: it has internal regions (10:xii).",
        ],
        "myth_key": M("Dis; Babylon the Great; Pandemonium; all cities blended; the ineluctable",
                      "Dante, Inferno VIII-IX; Revelation 17-18; Milton, Paradise Lost I.710-798; Calvino, Invisible Cities (1972); Plato, Timaeus 25 / Critias (Atlantis); Joyce, Ulysses ep. 3 (\"ineluctable modality of the visible\")",
                      "Every district is a stolen city. Go deeper and you go older. Two adjacent streets need not agree about which city they are in, and a wall that joins another realm is still a wall."),
    },
    {
        "name": "The Inevitable City, primeval stratum", "aliases": ["the primeval city"],
        "archetype": "composite-city", "classification": "Deep historical stratum of the named city-realm",
        "parent": "The Inevitable City",
        "attestations": [A(3, 9, "v", "all the cities that have ever been")],
        "facts": [
            "Loken's group reaches the oldest ruins yet: travelling deeper into geography is travelling deeper into history.",
            "Human-looking streets and houses become rare; monumental grey-diorite blocks, ashlar columns, skeletal black buttresses, strange lichens and moss, structures with no sign of human manufacture.",
            "Scraps of Palace and Vengeful Spirit persist only as warp-remembrances intruding into the older stratum.",
        ],
        "myth_key": M("The city before Babel; the cyclopean walls",
                      "Genesis 11:1-9; Pausanias II.16.5 (Cyclopean Mycenae); Lovecraft, At the Mountains of Madness (1936)",
                      "Nothing here was built for people. Doors are the wrong size, stairs the wrong pitch; every human-scale fragment is a memory, and memories are exits."),
    },
    {
        "name": "Calastar", "aliases": ["that impossible city"],
        "archetype": "composite-city", "classification": "Impossible exoplanar city",
        "attestations": [
            A(1, 4, "xviii", "a mere lifetime's journey"),
            A(3, 10, "xviii", "shatters loose"),
        ],
        "facts": ["The Inevitable City lies a mere lifetime's journey from Calastar, yet its walls and turrets join directly to those of 'that impossible city' (4:xviii).",
                  "Calastar shatters loose, impossibly constructed towers swaying, as the fused realities separate (10:xviii)."],
        "myth_key": M("The drowned city of Ys; the tower that reached heaven",
                      "Breton legend of Ker-Ys (Gradlon, Dahut); Genesis 11:4",
                      "Distance is measured in lifetimes and adjacency in walls. You can touch it and never arrive; you can arrive and be a lifetime older.",
                      canon_first="Warhammer 40,000 setting canon (webway city)"),
    },
    {
        "name": "The City of Dust", "aliases": ["City of Duste"],
        "archetype": "composite-city", "classification": "Warp/exoplanar city; both a district of the Inevitable City and a separable structure",
        "attestations": [
            A(1, 4, "xviii", "a moment's eternity"),
            A(2, 8, "iii", "City of Dust"),
            A(3, 10, "xviii", "skeletonised City of Dust"),
        ],
        "facts": [
            "The folio places the Inevitable City a moment's eternity from the City of Duste (4:xviii).",
            "The Emperor's path through the realm of Chaos reduces a great swathe of the Inevitable City to a City of Dust: an endless empty city of memory and melancholy, dirty roofs, overgrown byways, a broad ribbon of charred pale ash marking his progress; at once far off and just outside (8:iii).",
            "During the withdrawal the skeletonised City of Dust splits free and drifts like an iceberg into the exoplanar gulf (10:xviii).",
            "Keep both facts: district and separable realm.",
        ],
        "myth_key": M("Irkalla, the house of dust",
                      "Epic of Gilgamesh, Tablet VII (the house of dust, where the dead eat dust and clay); Genesis 3:19; Job 7:21",
                      "Nothing living trades here. Whatever you carry in is ash by the time you find the exit, and the ash is the only trail."),
    },
    {
        "name": "The supernal realm", "aliases": [],
        "archetype": "condition", "classification": "Descriptive upper warp environment in which the aperture manifests",
        "attestations": [A(1, 4, "xx", "supernal realm")],
        "facts": ["The opening warp turns against the blind, unconstellated void while lightning reaches down onto Terra."],
        "myth_key": M("The firmament above the waters",
                      "Genesis 1:6-8; Ezekiel 1:22-26",
                      "Overlay: the sky of any area may be the underside of this. Lightning arrives before its cause."),
    },
    {
        "name": "The unresolved realms of possibility", "aliases": [],
        "archetype": "condition", "classification": "Prophetic / potential realities",
        "attestations": [A(1, 4, "xxi", "the unresolved realms of possibility that only prophesy can see")],
        "facts": ["Actae: 'the Dark King' has a specific meaning in the warp and in these realms; not navigable geography but the warp's relation to prophecy, unrealised futures and god-birth."],
        "myth_key": M("The book sealed with seven seals; the things that must shortly come to pass",
                      "Revelation 5:1; Daniel 12:4",
                      "Overlay: a prophecy told inside an area seeds a facet of it. Not mappable."),
    },
    # --------------------------------------------------------------- Vol II
    {
        "name": "Hell, Gehenna and the Pit", "aliases": ["the inferno", "the underworld"],
        "archetype": "condition", "classification": "Human mythic names for glimpsed warp totality; explicitly not separate realms",
        "attestations": [A(2, 5, "viii", "Gehenna")],
        "facts": ["Malcador compares the unleashed warp to Hell, Gehenna, the inferno, the Pit, an underworld stripped of natural law and hope, then states his belief that humanity's recurring concept of hell derives from glimpses of the empyrean through dreams, nightmares, prophecy and psychic vision."],
        "myth_key": M("The Valley of Hinnom; the bottomless pit",
                      "2 Kings 23:10; Jeremiah 7:31; Matthew 5:22; Revelation 9:1-2; Dante, Inferno",
                      "The interpretive key for the whole folio: every earthly hell is a refracted map of the warp. Borrow their rules, label them INFERRED, and expect them to be partial."),
    },
    {
        "name": "The sunless sea of the empyrean", "aliases": ["Horus's frozen infinite", "the labyrinth of madness"],
        "archetype": "shore", "classification": "Descriptive deep-warp environment around the Inevitable City event",
        "attestations": [
            A(2, 5, "ix", "the sunless sea of the empyrean"),
            A(2, 5, "ix", "labyrinth of madness"),
        ],
        "facts": ["Chaos has opened the sunless sea to the Emperor, who draws directly from it.",
                  "Horus's trap is a labyrinth of madness, a frozen lawless eternity; day/night and temporal sequence are broken."],
        "myth_key": M("The sunless sea; the land of the Cimmerians",
                      "Coleridge, 'Kubla Khan' (1816); Homer, Odyssey XI.14-19",
                      "No day, no tide-table. Navigation is by memory alone, and memory is what this shore erodes."),
    },
    {
        "name": "Higher angles and unbounded dimensions of the immaterium", "aliases": ["the eighth angle of space", "the numberless angles of the empyrean", "the infinite planes", "an adjacent plane of the warp"],
        "archetype": "condition", "classification": "Extra spatial dimensionality; overlay, not a discrete realm",
        "attestations": [
            A(2, 5, "xliii", "other dimensions unfurl their properties"),
            A(2, 8, "xvii", "the eighth angle of space"),
            A(3, 9, "xxi", "numberless angles of the empyrean"),
        ],
        "facts": [
            "As Terra's reality fails, the four familiar dimensions are maimed and other dimensions unfurl with alien breadths; there is no limit to their number (5:xliii).",
            "Horus contrasts Sanguinius's three dimensions with 'the multitude' he commands and seizes him along the eighth angle of space (8:xvii).",
            "Horus bends a sword thrust away into an adjacent warp plane; fireballs attack along every axis of the infinite planes (9:xxi).",
        ],
        "myth_key": M("Dimensions beyond the third; the angles that hunt",
                      "Edwin Abbott, Flatland (1884); Frank Belknap Long, 'The Hounds of Tindalos' (1929)",
                      "Overlay: a defender with angle-access attacks from an edge the map does not draw. Every area gains one unmapped exit that only such a being can use."),
    },
    {
        "name": "The realm of shadows and candlelight", "aliases": [],
        "archetype": "condition", "classification": "Alternate/future reality perceived through the Throne",
        "attestations": [A(2, 6, "viii", "a realm of shadows and candlelight, a grim darkness of ruin and disrepair")],
        "facts": ["Among innumerable possible nows one remains dark: humans shackled by ancient duties imperfectly remembered but obsessively performed; technology and culture decayed into rote ceremony.",
                  "Reads as a vision of the future Imperium; tagged temporal/alternate, not a daemon realm."],
        "myth_key": M("The house of bondage; vanity of vanities",
                      "Exodus 20:2; Ecclesiastes 1:2-9",
                      "Overlay only. Not mappable; if it intrudes, it intrudes as ritual performed by people who have forgotten why."),
    },
    {
        "name": "The intersectional realm", "aliases": [],
        "archetype": "wilderness", "classification": "Overlap zone ravaged by the Emperor's advance",
        "attestations": [A(2, 8, "ii", "the intersectional realm")],
        "facts": ["The Scholaster Hall and surrounding city are gone; divine light has ravaged the intersectional realm for kilometres, leaving baked rubble and white ash beneath a black starless sky and a silent lightning horizon."],
        "myth_key": M("The burning of Edom; the plain of Sodom",
                      "Isaiah 34:9-10; Genesis 19:28",
                      "Aftermath terrain. Nothing casts a shadow; light comes from the horizon, so every silhouette is visible from every direction."),
    },
    {
        "name": "The warp-wilderness interlaced with the bridge", "aliases": ["the great realm of wilderness"],
        "archetype": "wilderness", "classification": "Unnamed continental realm fused with ship architecture",
        "attestations": [A(2, 8, "x", "great realm of wilderness")],
        "facts": ["Abaddon accepts that a great realm of wilderness has interlaced with the flagship's bridge; from a hill it appears endless and continental.",
                  "Land folded into impossible shelves and immense peaks; debris and dead cities cling vertically to the folds; sky stained by warpflux and pseudomatter beneath a baleful star.",
                  "The bridge hatch survives as a small bunker-like feature embedded in the landscape."],
        "myth_key": M("The frozen floor and the giants; the imaginary prisons",
                      "Dante, Inferno XXXI-XXXIV; Piranesi, Carceri d'invenzione (1750)",
                      "Vertical geography. Up and down are both routes. The way out is a hatch smaller than the door you came in by, and it is uphill."),
    },
    {
        "name": "The Lupercal Court", "aliases": ["Horus's Court", "the Court-realm", "this starless heaven"],
        "archetype": "labyrinth", "classification": "Horus's central psychofractal Court / the encompassing reality around him",
        "attestations": [
            A(2, 8, "xv", "This realm is his Court, this world, this starless heaven, this reality."),
            A(3, 10, "iv", "Lupercal Court"),
            A(3, 10, "viii", "gardens of the warp"),
        ],
        "facts": [
            "Erebus: the Court is not only the black throne chamber but the reality generated around Horus (8:xv).",
            "The Court reasserts itself as psychofractal blackness, obsidian tiles and diorite blocks; side chapels, sub-temples, galleries and processionals multiply toward impossible vanishing points (10:iv).",
            "Loken moves through its numberless angled dimensions from one duel-facet to another; a tailored ritual garden inside it has open black sky, water-mirror pools and a scrying function (10:iv).",
            "Nested: the Court surrounds the flagship, which surrounds the neverness, which surrounds the Inevitable City, which surrounds Horus's realm, then Terra, the Solar Realm, the galaxy and the warp, and all of them surround each other in reverse (10:viii).",
        ],
        "myth_key": M("The Lupercal cave; the House of Fame; the House of Pride",
                      "Livy I.4; Ovid, Fasti II.381-422; Ovid, Metamorphoses XII.39-63; Spenser, Faerie Queene I.iv",
                      "The Court makes a room for each intruder, shaped from what the intruder expects. Galleries recede forever; the only real doors are the ones the intruder did not expect.",
                      canon_first="Warhammer 40,000 setting canon (Lupercal is Horus's title)"),
    },
    # -------------------------------------------------------------- Vol III
    {
        "name": "The anti-realm of immateria and its facets", "aliases": ["the Terrestrial Realm (counterpart)", "psychic facets"],
        "archetype": "condition", "classification": "Parallel plane of combat; generator of local realm-fragments",
        "attestations": [
            A(3, 9, "xx", "in the realm of materia and the anti-realm of immateria"),
            A(3, 9, "xx", "Terrestrial Realm"),
        ],
        "facts": ["The Emperor-Horus duel is fought simultaneously across mortal and empyric planes; superimposed realities tear and peel; the Terrestrial Realm is almost completely submerged.",
                  "A throne-room fragment Loken finds himself in is a psychic fragment conjured from Horus's imagination, probably one of many."],
        "myth_key": M("The battle for the soul fought in allegorical places",
                      "Prudentius, Psychomachia (c. 405); Bunyan, The Holy War (1682)",
                      "Overlay: any area can spawn a facet, a smaller copy of itself shaped by whoever is fighting in it. Facets close when the fight ends."),
    },
    {
        "name": "The Twelfth Intersection of the Immaterial", "aliases": [],
        "archetype": "junction", "classification": "Named dimensional intersection / transit coordinate",
        "attestations": [A(3, 9, "xxi", "Twelfth Intersection of the Immaterial")],
        "facts": ["Horus dodges sideways along it while weaving between thorn trees in malnourished light to outflank the Emperor."],
        "myth_key": M("Twelve as the number of the ordered whole; the crown of thorns",
                      "Genesis 49:28; John 11:9; Matthew 27:29",
                      "A transit coordinate. Crossing it puts you beside your enemy instead of in front; the thorns take a toll from whoever crosses fastest."),
    },
    {
        "name": "The Sixty-sixth Oblique", "aliases": [],
        "archetype": "junction", "classification": "Named oblique plane; skull-coloured moon that never sets",
        "attestations": [A(3, 9, "xxi", "the Sixty-sixth Oblique where the skull-coloured moon never sets")],
        "facts": ["The Emperor takes guard there."],
        "myth_key": M("Golgotha, the place of the skull; the moon that stood still; the truncated number of the beast",
                      "Matthew 27:33; Joshua 10:12-13; Revelation 13:18",
                      "Fixed moon, no time. Every shadow points the same way: direction is free and stealth is impossible."),
    },
    {
        "name": "The Vale of Creatures", "aliases": [],
        "archetype": "wilderness", "classification": "Named warp valley populated by demented things",
        "attestations": [A(3, 9, "xxi", "Vale of Creatures")],
        "facts": ["A radiant sigil is propelled through the vale while barking, demented things writhe around Horus."],
        "myth_key": M("The valley of the shadow of death; Legion",
                      "Psalm 23:4; Mark 5:9",
                      "The population is the terrain. Move and it moves with you; stand still and it forgets you for one interval."),
    },
    {
        "name": "The Gulf of Lament", "aliases": [],
        "archetype": "crossing", "classification": "Warp gulf with a living-flesh bridge over an aeonic pit",
        "attestations": [A(3, 9, "xxi", "Gulf of Lament")],
        "facts": ["Horus crosses it by leaping along a narrow bridge of living flesh with febrile neuroplasticity, spanning a bottomless aeonic pit."],
        "myth_key": M("The Chinvat bridge that narrows for the wicked; the bridge over Chaos",
                      "Videvdat 19.29-30 and Bundahishn 30 (Chinvat); Gylfaginning 49 (Gjallarbru); Islamic tradition of as-Sirat; Milton, Paradise Lost X.282-324",
                      "Bridge width is set by the crosser. It narrows for the unworthy, it is warm, and it remembers who crossed; the pit below has no bottom to roll against."),
    },
    {
        "name": "The Bastion Stair in the realm of the red", "aliases": ["the Bastion Stair", "the realm of the red"],
        "archetype": "crossing", "classification": "Named warp stair-structure in a descriptively named realm",
        "attestations": [A(3, 9, "xxi", "the brazen, screaming steps of the Bastion Stair in the realm of the red")],
        "facts": ["The Emperor follows Horus across inter-dimensional interstices to the brazen, screaming steps.",
                  "The realm of the red has no proper noun beyond this description."],
        "myth_key": M("Jacob's ladder; the brazen altar; the mountain that smoked",
                      "Genesis 28:12; Exodus 27:1-2; Exodus 19:18",
                      "Every step is a fight. You cannot descend a step you did not win, and the steps scream the name of whoever last lost on them.",
                      canon_first="Warhammer setting canon (the Bastion Stair; red as the Blood God's colour)"),
    },
    {
        "name": "The Mists of Unreason", "aliases": [],
        "archetype": "wilderness", "classification": "Named warp region",
        "attestations": [A(3, 9, "xxi", "Mists of Unreason")],
        "facts": ["Horus tries to evade through them while the Emperor tracks him despite the changing reality."],
        "myth_key": M("The dark wood; the Slough of Despond",
                      "Dante, Inferno I.1-12; Bunyan, The Pilgrim's Progress (1678)",
                      "Reasoning fails inside. A plan made in the mist is wrong; only a plan made before entering holds, and it holds only as long as nobody revises it."),
    },
    {
        "name": "The Blizzard of Forgetting", "aliases": [],
        "archetype": "wilderness", "classification": "Named warp plateau / phenomenon-landscape",
        "attestations": [A(3, 9, "xxi", "Blizzard of Forgetting")],
        "facts": ["A bleak plateau crossed after the Mists of Unreason."],
        "myth_key": M("Lethe; the frozen ninth circle",
                      "Virgil, Aeneid VI.705-715; Dante, Purgatorio XXXI.91-102; Inferno XXXII-XXXIV (Cocytus)",
                      "Each interval costs one learned name from the lexicon ledger. The ledger is the map: what you have forgotten, you cannot navigate back to."),
    },
    {
        "name": "The Crook of Shadows", "aliases": [],
        "archetype": "labyrinth", "classification": "Explicit slanting subdimension",
        "attestations": [A(3, 9, "xxi", "that dingy, slanting subdimension where nothing is upright and everything is corners")],
        "facts": ["Horus uses it as a refuge and evasion route."],
        "myth_key": M("The hounds that come through angles; the rod and staff inverted",
                      "Frank Belknap Long, 'The Hounds of Tindalos' (1929); Psalm 23:4",
                      "Corners are doors and curves are walls. Anything that hunts by angle is already here; the only safe posture is a curve, and nothing here is curved."),
    },
    {
        "name": "The Drifting Castle", "aliases": [],
        "archetype": "labyrinth", "classification": "Named warp structure with salt-caked asymmetric chambers",
        "attestations": [A(3, 9, "xxi", "salt-caked and asymmetric chambers")],
        "facts": ["The Emperor crosses its chambers while escaping Horus's self-closing labyrinth."],
        "myth_key": M("Lot's wife; the Grail castle that moves; the floating island",
                      "Genesis 19:26; Vulgate Cycle (Corbenic); Swift, Gulliver's Travels III (Laputa)",
                      "Rooms close behind you. Salt marks every place where someone looked back; follow the salt and you find where they stopped."),
    },
    {
        "name": "The Eightieth Conjunction", "aliases": [],
        "archetype": "junction", "classification": "Named dimensional junction",
        "attestations": [A(3, 9, "xxi", "Eightieth Conjunction")],
        "facts": ["The Emperor shifts from the Drifting Castle through it toward Long Woe."],
        "myth_key": M("Fourscore years, the span of a strong life",
                      "Psalm 90:10",
                      "A lifetime's junction. Crossing it ages what crosses by one interval of exposure, whichever way it goes."),
    },
    {
        "name": "Long Woe", "aliases": [],
        "archetype": "wilderness", "classification": "Named realm of fever-meadows, twilit glades and painforests",
        "attestations": [
            A(3, 9, "xxi", "fever-meadows"),
            A(3, 10, "xviii", "twilit glades and painforests"),
        ],
        "facts": ["Contains fever-meadows (9:xxi).",
                  "Its twilit glades and painforests are swallowed by rancid superheated steam and reduced to putrescent mush that drips into a dark abyss (10:xviii)."],
        "myth_key": M("The Wood of Suicides; the garden that rots",
                      "Dante, Inferno XIII.1-108; Genesis 3:17-18",
                      "The vegetation is sentient and suffering. Cut it and it speaks; sleep in it and the fever is yours. Steam rising means the realm is ending, and it ends downhill.",
                      canon_first="Secondary: the Plague God's garden in Warhammer setting canon"),
    },
    {
        "name": "The Tree of Souls", "aliases": [],
        "archetype": "repository", "classification": "Colossal warp landmark",
        "attestations": [A(3, 9, "xxi", "Tree of Souls")],
        "facts": ["The Emperor routes around its vast, root-gnarled base to disguise his approach."],
        "myth_key": M("Yggdrasil; the tree of life; Etz Chaim",
                      "Voluspa 19; Grimnismal 31; Genesis 2:9; Revelation 22:2",
                      "The roots reach other realms. Follow a root and you arrive somewhere else on the folio; the tree keeps what it is given and gives nothing back."),
    },
    {
        "name": "The Sea of Souls", "aliases": [],
        "archetype": "shore", "classification": "Named warp sea with wild shores",
        "attestations": [A(3, 9, "xxi", "wild shores")],
        "facts": ["The Emperor hunts Horus along its wild shores in a lion aspect."],
        "myth_key": M("The sea gives up its dead",
                      "Revelation 20:13; Homer, Odyssey XI (the shore of the dead)",
                      "The tide is souls. Low tide exposes the dead and what they carried; high tide takes the living. Roll the tide on entry.",
                      canon_first="Warhammer 40,000 setting canon (the warp as Sea of Souls)"),
    },
    {
        "name": "The Marcher Fortress and the Marches", "aliases": ["Marcher Fortress", "the Marches"],
        "archetype": "fortress", "classification": "Warp fortress on the margins of the Planes of Excess, with its approaches",
        "attestations": [
            A(3, 9, "xxi", "mildewed Marcher Fortress"),
            A(3, 9, "xxi", "the dark approaches of the Marches"),
            A(3, 10, "xviii", "on the fringe of nothing"),
        ],
        "facts": ["Horus takes refuge in the mildewed Marcher Fortress, which watches the stained margins of the Planes of Excess; he floods the dark approaches of the Marches with supernatural dread (9:xxi).",
                  "It burns on the fringe of nothing during the great withdrawal (10:xviii)."],
        "myth_key": M("The Welsh Marches and their lords; the night approach on the camp",
                      "Statute of Rhuddlan (1284) and the Marcher lordships; Judges 7:16-22",
                      "A frontier keep. The approaches are the fight and the walls are not; dread on the approach is a rolled hazard, and the keep itself is mildew and quiet."),
    },
    {
        "name": "The Planes of Excess", "aliases": [],
        "archetype": "wilderness", "classification": "Named warp planes / realm-complex with stained margins",
        "attestations": [A(3, 9, "xxi", "Planes of Excess")],
        "facts": ["The Marcher Fortress overlooks their stained margins; the approaches carry psychic dread and hostile Chaos workings; the text does not assign the Planes to one god."],
        "myth_key": M("The circles of incontinence",
                      "Dante, Inferno V-VII; Proverbs 23:29-35",
                      "Every sense is a door. Whatever the traveller wants most is the terrain's weapon; roll the want before the hazard.",
                      canon_first="Warhammer setting canon by implication (the Dark Prince's domain); not assigned in the text"),
    },
    {
        "name": "The Abstraction of Plight", "aliases": [],
        "archetype": "junction", "classification": "Named dimensional evasion route / facet",
        "attestations": [A(3, 10, "v", "Abstraction of Plight")],
        "facts": ["The Emperor slides sideways through it to evade Worldbreaker; treated as a traversable warped angle, not a metaphor."],
        "myth_key": M("The narrow escape; the strait gate",
                      "Matthew 7:13-14; Psalm 124:7",
                      "An evasion vector. Sliding through it spends strength; it can be used only by someone with warp strength to spend, and each use is narrower."),
    },
    {
        "name": "The Forsaken Angle", "aliases": [],
        "archetype": "junction", "classification": "Named warped plane with twilit cliffs",
        "attestations": [A(3, 10, "v", "the twilit cliffs of the Forsaken Angle")],
        "facts": ["The Emperor circles Horus through its twilit cliffs, then spills back into the Court when his stolen warp power weakens; Horus notes he no longer has the strength for warped angles."],
        "myth_key": M("Why hast thou forsaken me",
                      "Psalm 22:1; Matthew 27:46",
                      "The last angle a weakening warp-user can reach. Entering costs the strength to return; the cliffs are the fall back into wherever you came from."),
    },
    {
        "name": "The gardens of the warp", "aliases": [],
        "archetype": "wilderness", "classification": "Partially described warp habitat where psychneuein breed",
        "attestations": [A(3, 10, "viii", "the gardens of the warp")],
        "facts": ["Psychneuein wake and begin to swarm there while all dimensions and moments fold into the Court's psychofractal point."],
        "myth_key": M("Eden inverted; the garden east of Eden",
                      "Genesis 2:8-9; 3:23-24",
                      "Something breeds here and noise wakes it. Every rolled hazard in a garden area is a swarm; the swarm follows psykers first.",
                      canon_first="Secondary: the Plague God's garden in Warhammer setting canon"),
    },
    {
        "name": "The wild, un-timed steppes of the immaterium", "aliases": [],
        "archetype": "wilderness", "classification": "Ancient warp hunting-ground",
        "attestations": [A(3, 10, "ix", "wild and un-timed steppes of the immaterium")],
        "facts": ["The sagittaries have hunted there forever, bringing down every kind of warp quarry; the Dreadful Sagittary is named at 9:xxi and 10:iv, and 10:ix speaks of the two sagittaries."],
        "myth_key": M("Chiron and the centaur-archer; the Wild Hunt; Scythia",
                      "Ovid, Fasti V.379-414; the Wild Hunt (Herne, Odin's host); Herodotus IV",
                      "Open ground with no time. The hunters have always been behind you; the only cover is another quarry."),
    },
    {
        "name": "The splice between adjacent realms", "aliases": ["the clean boundary"],
        "archetype": "condition", "classification": "Doorway-sharp tear between material and immaterial; overlay",
        "attestations": [A(3, 10, "iii", "a tear between material and immaterial")],
        "facts": ["Moriana identifies a courtyard/cell-block discontinuity: the courtyard lies in one realm and the space through the cell door in another, adjacent; such boundaries are normally blurred and gradual, this one unusually clean and sharp."],
        "myth_key": M("The door in the wall",
                      "H. G. Wells, 'The Door in the Wall' (1906); Revelation 4:1",
                      "Overlay: a splice edge is a doorway-sharp boundary. Both sides are simultaneously true; a thing standing in the doorway is in two realms and rolls against both."),
    },
    {
        "name": "The Desert of Gods", "aliases": [],
        "archetype": "wilderness", "classification": "Named warp/exoplanar landscape where no idol is permitted to stand",
        "attestations": [A(3, 10, "xviii", "where no idol is permitted to stand")],
        "facts": ["During the collapse it sags and pours away like sand through an hourglass."],
        "myth_key": M("The commandment against graven images; the wilderness of Sinai; Ozymandias",
                      "Exodus 20:4; Deuteronomy 32:10; Isaiah 40:19-20; Shelley, 'Ozymandias' (1818)",
                      "Aniconic. Any icon, banner, statue, effigy or Legion badge raised here falls within the interval. The sand runs down: the realm is a timer and the hourglass is the map."),
    },
    {
        "name": "The Dolmen Gates", "aliases": [],
        "archetype": "crossing", "classification": "Named dimensional gateway complex",
        "attestations": [A(3, 10, "xviii", "troubled in their long slumber")],
        "facts": ["The gates shudder, troubled in their long slumber, while the webway's psychoplastic conduits creak under the transition."],
        "myth_key": M("The portal tomb; the solstice passage",
                      "Neolithic dolmens (Poulnabrone, Brownshill); Newgrange winter-solstice alignment",
                      "A gate older than the webway. It opens on a schedule that is not yours; the crossing is waiting, and what waits with you is the encounter.",
                      canon_first="Warhammer 40,000 setting canon (Necron dolmen gates)"),
    },
    {
        "name": "Islets of exoplanar matter and archipelagoes of haunted warp stars", "aliases": [],
        "archetype": "shore", "classification": "Unnamed partial realm-geography that does not survive the withdrawal",
        "attestations": [A(3, 10, "xviii", "archipelagoes of haunted warp stars")],
        "facts": ["Some realms do not survive the transition at all; whole islets of exoplanar matter and archipelagoes of haunted warp stars combust or implode."],
        "myth_key": M("The Isles of the Blessed; the stars falling to earth",
                      "Hesiod, Works and Days 170-173; Revelation 6:13",
                      "Temporary ground. Every islet has a life expectancy; roll it on arrival and count it down per interval."),
    },
    {
        "name": "Shabek", "aliases": [],
        "archetype": "wilderness", "classification": "Desolate grey worm-eaten fens",
        "attestations": [A(3, 10, "xviii", "the worm-eaten fens of desolate Shabek")],
        "facts": ["Grey and forlorn; dissolves into mist during the withdrawal."],
        "myth_key": M("Sobek's marsh; the worm that dieth not; Grendel's mere; the Styx marsh",
                      "Isaiah 66:24; Mark 9:48; Beowulf 1357-1376; Dante, Inferno VII.100-VIII.64",
                      "Footing is the encounter. The worms are the wrathful and they are under the mud; what sinks stays, and the mist is the realm leaving."),
    },
    {
        "name": "The bone-beds of fossil gods", "aliases": [],
        "archetype": "wilderness", "classification": "Unnamed dry bone-beds",
        "attestations": [A(3, 10, "xviii", "bone-beds")],
        "facts": ["The dry bone-beds of fossil gods reduce to ash and blow away as the unnatural light fades."],
        "myth_key": M("The valley of dry bones; the Titans beneath Tartarus",
                      "Ezekiel 37:1-14; Hesiod, Theogony 717-735",
                      "The hills are gods. Strike the bone and it remembers being worshipped; the memory is the hazard, and it wants an offering."),
    },
    {
        "name": "Somnopolis, the Library of Lost and Mislaid Dreams", "aliases": ["Somnopolis"],
        "archetype": "repository", "classification": "Named dream/warp repository-realm",
        "attestations": [A(3, 10, "xviii", "never more remembered")],
        "facts": ["Consumed in a raging inferno during the withdrawal and never more remembered."],
        "myth_key": M("The Library of Babel; the Cave of Sleep; the burning of Alexandria",
                      "Borges, 'The Library of Babel' (1941); Ovid, Metamorphoses XI.592-632; Plutarch, Caesar 49",
                      "Everything unmade is shelved here: the plan not followed, the name not given. Take one and the shelf behind you burns; you may leave with exactly one thing."),
    },
    # -------------------------------------------------------- cross-volume
    {
        "name": "Neverness", "aliases": ["un-time", "the neverness storm", "the singularity of neverness"],
        "archetype": "condition", "classification": "Recurring atemporal warp-state; overlay",
        "attestations": [
            A(1, 2, "xii", "neverness"),
            A(3, 10, "viii", "neverness"),
        ],
        "facts": [
            "Vol. I: the abdication of metaphysical continuity when Terra is pinned in an infinite empyrean now; Uigebealach is associated with this state.",
            "Vol. II: the crisis treated throughout as an eternal, lawless present.",
            "Vol. III: a neverness storm, a singularity of neverness; ends when Horus dies and time re-forms; also an empyric archetype Horus uses in the psychomachia.",
        ],
        "myth_key": M("That which hath been is now; the never-never",
                      "Ecclesiastes 3:15; J. M. Barrie, Peter and Wendy (1911)",
                      "Overlay: no clock advances inside. Exposure is counted in intervals, not hours; nothing outside notices how long you were gone."),
    },
    {
        "name": "The exoplanar membrane and fluid territories", "aliases": [],
        "archetype": "condition", "classification": "Partially described dimensional substrate; overlay",
        "attestations": [A(2, 5, "ix", "exoplanar membrane"), A(3, 9, "xxi", "adjacent layer of the warp's fluid territories")],
        "facts": ["Hostile forms bulge from an exoplanar membrane as the Emperor draws on the sunless sea (5:ix); in the psychomachia Horus drops through an adjacent layer of the warp's fluid territories, treating the immaterium as neighbouring layers, interstices, planes and angles rather than one void (9:xxi). The sweep index had filed these under 7:i and 10:v; the corpus pass corrected them."],
        "myth_key": M("The waters above and the waters below",
                      "Genesis 1:6-7; Psalm 148:4",
                      "Overlay: the ground of any area is a membrane. Anything can bulge through it from the layer beneath; a splice edge is where it already has."),
    },
    {
        "name": "The unquiet realms of the dead, the damned, the lost and the psychic", "aliases": [],
        "archetype": "condition", "classification": "Explicit unnamed realm classes that part ways at Uigebealach",
        "attestations": [A(3, 10, "xviii", "the dead and the damned, the lost and the psychic")],
        "facts": ["Multiple distinct realms or classes of realm implied; the verse names none individually."],
        "myth_key": M("The four last things; the regions of Hades",
                      "Virgil, Aeneid VI.426-547 (the regions of the dead sorted by their deaths); Revelation 20:12-14",
                      "Overlay: a traveller belongs to one of the four classes. Junction exits are sorted by class, not by choice."),
    },
]


# ---------------------------------------------------------------------------
# Corpus lookup
# ---------------------------------------------------------------------------
_NORMALISE = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u00a0": " ", "*": "", "_": "",
})
# Heading shapes: the Notion export writes "9:xxi" verse headings and
# "PART NINE" part headings on their own lines; a markdown corpus may instead
# use "# 9" / "## xxi". Both are recognised.
PART_LINE = re.compile(r"^\s*\**PART [A-Z]+\**\s*$")
VERSE_LINE = re.compile(r"^\s*\**(\d{1,2}):([ivxl]{1,7})\**\s*$", re.IGNORECASE)
ROMAN = re.compile(r"^\s*#{1,6}\s*\**([ivxlc]{1,7})\**\s*$", re.IGNORECASE)
CHAPTER = re.compile(r"^\s*#{1,6}\s*\**(?:chapter\s+)?(\d{1,2})\**\s*$", re.IGNORECASE)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.translate(_NORMALISE)).casefold()


def find_volume_file(corpus: Path, vol: int) -> Optional[Path]:
    if not corpus.is_dir():
        return None
    direct = corpus / f"vol{vol}.md"
    if direct.is_file():
        return direct
    tag = {1: "volume i", 2: "volume ii", 3: "volume iii"}[vol]
    for p in sorted(corpus.iterdir()):
        n = p.name.casefold()
        if p.is_file() and tag in n and not (vol == 1 and "volume ii" in n) \
                and not (vol == 2 and "volume iii" in n):
            return p
    return None


class Volume:
    """A volume's lines, a whitespace-collapsed normalised text for phrase
    search across line breaks, and the chapter/verse in force at each line."""

    def __init__(self, lines: List[str]):
        self.lines = lines
        self.offsets: List[int] = []
        parts: List[str] = []
        pos = 0
        chapter: Optional[int] = None
        verse: Optional[str] = None
        self.heading: List[Tuple[Optional[int], Optional[str]]] = []
        for raw in lines:
            m = VERSE_LINE.match(raw)
            if m:
                chapter, verse = int(m.group(1)), m.group(2).lower()
            else:
                m = CHAPTER.match(raw)
                if m:
                    chapter, verse = int(m.group(1)), None
                else:
                    m = ROMAN.match(raw)
                    if m:
                        verse = m.group(1).lower()
            self.heading.append((chapter, verse))
            piece = norm(raw) + " "
            self.offsets.append(pos)
            parts.append(piece)
            pos += len(piece)
        self.text = "".join(parts)

    def verse_span(self, chapter: int, verse: str) -> Optional[Tuple[int, int]]:
        """Character span of the body text under the LAST heading line reading
        chapter:verse (the front-matter contents list repeats every heading,
        so the last occurrence is the body's)."""
        start_idx = None
        for i, raw in enumerate(self.lines):
            m = VERSE_LINE.match(raw)
            if m and int(m.group(1)) == chapter and m.group(2).lower() == verse:
                start_idx = i
        if start_idx is None:
            return None
        end_idx = len(self.lines)
        for j in range(start_idx + 1, len(self.lines)):
            if VERSE_LINE.match(self.lines[j]) or PART_LINE.match(self.lines[j]):
                end_idx = j
                break
        end = self.offsets[end_idx] if end_idx < len(self.lines) else len(self.text)
        return self.offsets[start_idx], end

    def locate(self, phrase: str, chapter: Optional[int] = None,
               verse: Optional[str] = None) -> Optional[Tuple[int, Optional[int], Optional[str], bool]]:
        """(1-based line, chapter, verse, in_expected_verse). The expected
        verse is searched first; a global search is the fallback and reports
        the verse the phrase was actually found under."""
        import bisect
        target = norm(phrase).strip()
        if not target:
            return None
        if chapter is not None and verse is not None:
            span = self.verse_span(chapter, verse)
            if span is not None:
                at = self.text.find(target, span[0], span[1])
                if at != -1:
                    idx = bisect.bisect_right(self.offsets, at) - 1
                    return idx + 1, chapter, verse, True
        at = self.text.find(target)
        if at == -1:
            return None
        idx = bisect.bisect_right(self.offsets, at) - 1
        ch, vs = self.heading[idx]
        return idx + 1, ch, vs, False


def locate(lines: List[str], phrase: str) -> Optional[Tuple[int, Optional[int], Optional[str], bool]]:
    return Volume(lines).locate(phrase)


def apply_corpus(realms: List[Dict], corpus: Optional[Path]) -> Dict[int, str]:
    """Upgrade attestations to corpus-exact where the phrase is found. Returns
    per-volume coverage strings."""
    coverage: Dict[int, str] = {}
    texts: Dict[int, "Volume"] = {}
    for vol in VOLUMES:
        path = find_volume_file(corpus, vol) if corpus else None
        if path is None:
            coverage[vol] = ("NO COVERAGE -- corpus file for volume "
                             f"{vol} not present; quotes keep their sweep / "
                             "Notion verification status")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        texts[vol] = Volume(text.splitlines())
        coverage[vol] = f"ok -- {path.name} ({len(text)} chars)"
    hits = misses = 0
    for realm in realms:
        for att in realm["attestations"]:
            vol = att["volume"]
            if vol not in texts:
                continue
            found = texts[vol].locate(att["quote"], att["chapter"], att["verse"])
            if found is None:
                att["verification"] = f"corpus-MISS ({att['verification']})"
                misses += 1
                continue
            line, ch, verse, in_verse = found
            att["line"] = line
            if in_verse:
                att["verification"] = "corpus-exact"
                hits += 1
            else:
                att["verification"] = "corpus-exact-elsewhere"
                att["found_under"] = f"{ch}:{verse}"
                misses += 1
    for vol in texts:
        coverage[vol] += f"; corpus pass: {hits} exact, {misses} missed (all volumes)"
    return coverage


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def cite(vol: int, ch: int, verse: str) -> str:
    return (f"Dan Abnett, The End and the Death Vol. {'I' * vol}, "
            f"ch. {ch} v. {verse} (Notion page id in volumes[])")


def build(corpus: Optional[Path]) -> Dict:
    realms = json.loads(json.dumps(REALMS))  # deep copy; keep the roster pristine
    coverage = apply_corpus(realms, corpus)
    rows = []
    for r in realms:
        first = r["attestations"][0]
        vol = first["volume"]
        row = {
            "name": r["name"],
            "system": SYSTEM,
            "book": VOLUMES[vol]["book"],
            "page": None,
            "citation": cite(vol, first["chapter"], first["verse"]),
            "aliases": r.get("aliases", []),
            "archetype": r["archetype"],
            "mappable": r["archetype"] != "condition",
            "classification": r["classification"],
            "attestations": r["attestations"],
            "facts": r["facts"],
            "facts_label": "SOURCE-VERIFIED (sweep " + SWEEP_DATE + "; see attestations for verbatim status)",
            "myth_key": r["myth_key"],
        }
        if r.get("parent"):
            row["parent"] = r["parent"]
        rows.append(row)
    return {
        "generated_by": "scripts/teatd_realm_harvest.py",
        "system": SYSTEM,
        "corpus": str(corpus) if corpus else "NO COVERAGE -- corpus/teatd/ not present (or pass --corpus DIR)",
        "sweep_date": SWEEP_DATE,
        "total_realms": len(rows),
        "total_mappable": sum(1 for r in rows if r["mappable"]),
        "archetypes": ARCHETYPES,
        "edge_types": EDGE_TYPES,
        "label_vocabulary": {
            "SOURCE-VERIFIED": "stated in the trilogy at the cited chapter:verse",
            "INFERRED": "the myth key and its rule: the author's reading, not the text",
            "ROLLED": "produced by realm_map.py dice; never source",
        },
        "volumes": [
            {**VOLUMES[v], "system": SYSTEM,
             "citation": f"Dan Abnett, The End and the Death Volume {'I' * v} (Black Library, Siege of Terra), chapters {VOLUMES[v]['chapters']}",
             "coverage": coverage[v]}
            for v in VOLUMES
        ],
        "realms": rows,
    }


def write_markdown(data: Dict, path: Path) -> None:
    out = ["# THE END AND THE DEATH -- WARP REALM INDEX (system: WH40K Novel)", "",
           "**Generated by scripts/teatd_realm_harvest.py. Do not hand-edit.**",
           f"Dan Abnett, *The End and the Death* Volumes I-III, sweep {data['sweep_date']}. "
           "Named realms, exoplanar locations and dimensional conditions, each tied to chapter:verse. "
           "`facts` are SOURCE-VERIFIED; `myth_key` is INFERRED; nothing here is campaign canon. "
           "Source of record for `scripts/realm_map.py`.", ""]
    for v in data["volumes"]:
        out.append(f"*{v['book']}* -- Notion `{v['notion_page_id']}` -- {v['coverage']}  ")
    out.append("")
    out.append(f"**{data['total_realms']} realms, {data['total_mappable']} mappable.** "
               "Archetypes: " + ", ".join(f"`{k}`" for k in data["archetypes"]) + ".")
    out.append("")
    out.append("| Realm | Archetype | First attestation | Myth referent |")
    out.append("|---|---|---|---|")
    for r in data["realms"]:
        a = r["attestations"][0]
        out.append(f"| {r['name']} | {r['archetype']} | Vol. {'I' * a['volume']} {a['chapter']}:{a['verse']} | {r['myth_key']['referent']} |")
    out.append("")
    for r in data["realms"]:
        out.append(f"## {r['name']}")
        if r["aliases"]:
            out.append(f"*Aliases:* {', '.join(r['aliases'])}  ")
        out.append(f"*Archetype:* `{r['archetype']}` -- {r['classification']}  ")
        if r.get("parent"):
            out.append(f"*Stratum of:* {r['parent']}  ")
        out.append("")
        out.append("**Attestations**")
        for a in r["attestations"]:
            extra = f", line {a['line']}" if "line" in a else ""
            out.append(f"- Vol. {'I' * a['volume']} {a['chapter']}:{a['verse']} -- \"{a['quote']}\" [{a['verification']}{extra}]")
        out.append("")
        out.append("**Facts (SOURCE-VERIFIED)**")
        for f in r["facts"]:
            out.append(f"- {f}")
        out.append("")
        mk = r["myth_key"]
        out.append(f"**Myth key (INFERRED)** -- {mk['referent']}  ")
        out.append(f"*Citation:* {mk['citation']}  ")
        if mk.get("canon_first"):
            out.append(f"*Canon-first:* {mk['canon_first']}  ")
        out.append(f"*Law of the place:* {mk['rule']}")
        out.append("")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def search(term: str) -> None:
    t = term.casefold()
    for r in REALMS:
        hay = " ".join([r["name"], *r.get("aliases", []), r["classification"],
                        *r["facts"], r["myth_key"]["referent"]]).casefold()
        if t in hay:
            a = r["attestations"][0]
            print(f"{r['name']}  [{r['archetype']}]  Vol. {'I' * a['volume']} {a['chapter']}:{a['verse']}")


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------
def selftest() -> int:
    fails: List[str] = []

    def check(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    names = [r["name"] for r in REALMS]
    check(len(names) == len(set(names)), "duplicate realm names")
    for r in REALMS:
        check(r["archetype"] in ARCHETYPES, f"{r['name']}: bad archetype {r['archetype']}")
        check(bool(r["attestations"]), f"{r['name']}: no attestations")
        check(bool(r["facts"]), f"{r['name']}: no facts")
        mk = r["myth_key"]
        check(all(k in mk for k in ("referent", "citation", "rule", "label")),
              f"{r['name']}: incomplete myth key")
        check(mk["label"] == "INFERRED", f"{r['name']}: myth key must be INFERRED")
        for a in r["attestations"]:
            check(a["volume"] in VOLUMES, f"{r['name']}: bad volume")
            check(re.fullmatch(r"[ivxl]+", a["verse"]) is not None, f"{r['name']}: verse not roman")
            lo, hi = {1: (1, 4), 2: (5, 8), 3: (9, 10)}[a["volume"]]
            check(lo <= a["chapter"] <= hi, f"{r['name']}: chapter {a['chapter']} outside volume {a['volume']}")
            check(len(a["quote"].split()) <= 60, f"{r['name']}: quote over 60 words")
        if r.get("parent"):
            check(r["parent"] in names, f"{r['name']}: parent not in roster")

    data = build(None)
    check(data["total_realms"] == len(REALMS), "row count mismatch")
    check(all("NO COVERAGE" in v["coverage"] for v in data["volumes"]),
          "no-corpus build must print NO COVERAGE")
    check(all(a["verification"].startswith(("index-transcribed", "notion-fetch"))
              for r in data["realms"] for a in r["attestations"]),
          "no-corpus build must not claim corpus verification")
    json.dumps(data)

    # corpus path with a fixture: chapter / verse detection and exact hit
    with tempfile.TemporaryDirectory() as td:
        corpus = Path(td)
        (corpus / "vol3.md").write_text(
            "PART NINE\n9:xxi\nnothing\nPART NINE\n9:xxi\n\nHe ran along the Twelfth\n*Intersection* of the Immaterial.\n"
            "\n9:xxii\n\nnothing\n\n10:xviii\n\nthe worm-eaten fens of desolate Shabek, grey and forlorn.\n",
            encoding="utf-8")
        d2 = build(corpus)
        by = {r["name"]: r for r in d2["realms"]}
        att = by["The Twelfth Intersection of the Immaterial"]["attestations"][0]
        check(att["verification"] == "corpus-exact" and att.get("line") == 7 and "verse_detected" not in att
              and "chapter_detected" not in att,
              f"fixture: intersection not located exactly: {att}")
        sh = by["Shabek"]["attestations"][0]
        check(sh["verification"] == "corpus-exact" and "chapter_detected" not in sh, f"fixture: shabek {sh}")
        lw = by["Long Woe"]["attestations"][0]
        check(lw["verification"].startswith("corpus-MISS"), "fixture: absent phrase must be a MISS")
        v1 = next(v for v in d2["volumes"] if v["key"] == "vol1")
        check("NO COVERAGE" in v1["coverage"], "fixture: missing vol1 must be NO COVERAGE")
        md = corpus / "out.md"
        write_markdown(d2, md)
        check("## Shabek" in md.read_text(encoding="utf-8"), "markdown missing realm section")

    for f in fails:
        print("FAIL:", f)
    print(f"SELFTEST {'OK' if not fails else 'FAILED'}: {len(REALMS)} realms, "
          f"{sum(1 for r in REALMS if r['archetype'] != 'condition')} mappable, "
          f"{len(fails)} failures")
    return 1 if fails else 0


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--corpus", default=str(REPO / "corpus" / "teatd"), help="folder holding vol1.md / vol2.md / vol3.md (default: corpus/teatd/ in this repository)")
    p.add_argument("--search", help="find realms by name, alias, fact or referent")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if args.search:
        search(args.search)
        return
    corpus = Path(args.corpus) if args.corpus and Path(args.corpus).is_dir() else None
    data = build(corpus)
    OUT_JSON.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(data, OUT_MD)
    for v in data["volumes"]:
        print(f"  {v['book']}: {v['coverage']}")
    print(f"WROTE {OUT_JSON.relative_to(REPO)} ({data['total_realms']} realms, "
          f"{data['total_mappable']} mappable) and {OUT_MD.relative_to(REPO)}")


if __name__ == "__main__":
    main()
