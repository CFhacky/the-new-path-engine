# Apocrypha

Original writing that lives beside the corpus and is addressed the same way. Nothing here is source, canon of any setting, or a claim about one. It is fiction written after the trilogy, in the manner of scripture, and it is here because the address tool should work on a book written for it as well as on a book it was reverse-engineered from.

| File | Key | Units | What it is |
|---|---|---|---|
| `third_nail.md` | `NAIL` | 9 chapters, 180 verses | The Book of the Third Nail. An astropath bound to the Throne in the first days after the Siege is commissioned to write what happened and, beside it, what will be said instead. Blinded at the binding; writes in the dark. |

Address map: `reference/addresses/nail.address.json` (edition-pinned by SHA-256). Resolve a verse with:

```
python3 scripts/verse_address.py --map reference/addresses/nail.address.json --resolve "NAIL 6:xvi" --book corpus/apocrypha/third_nail.md
```

Every chapter ends with the counter-account, marked "And this is what they will say instead," so the canon-table tool has two witnesses to the same event in one document.

Labels: the whole file is ORIGINAL. It quotes nothing from the novels and cites nothing as fact.
