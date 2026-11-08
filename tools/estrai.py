"""Estrae i testi da Data/messages.dat in file JSON sotto traduzione/.

Uso:  py tools/estrai.py [cartella_gioco]

Ogni file JSON e' una lista di voci:
    {"id": <indice o chiave>, "en": "<testo originale>", "it": "<traduzione>"}
Il campo "it" vuoto significa "non ancora tradotto".
Rieseguire lo script conserva le traduzioni gia' presenti.
"""
import os
import sys

from rubymarshal.classes import UserDef

from fa_common import (DEFAULT_GAME, TRAD_DIR, load_json, load_messages,
                       read_ordered_hash, save_json, section_filename, to_str)


def merge(path, entries):
    old = {}
    if os.path.exists(path):
        for e in load_json(path):
            if e.get("it"):
                old[(str(e["id"]), e["en"])] = e["it"]
    for e in entries:
        e["it"] = old.get((str(e["id"]), e["en"]), "")
    save_json(path, entries)
    return len(entries), sum(1 for e in entries if e["it"])


def hash_entries(u):
    return [{"id": k, "en": v, "it": ""} for k, v in read_ordered_hash(u) if v]


def main():
    game = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GAME
    msgs = load_messages(os.path.join(game, "Data", "messages.dat"))
    total = done = 0
    for mapid, u in enumerate(msgs[0] or []):
        if not isinstance(u, UserDef):
            continue
        entries = hash_entries(u)
        if not entries:
            continue
        n, d = merge(os.path.join(TRAD_DIR, "mappe", f"Map{mapid:03d}.json"), entries)
        total += n
        done += d
    for i in range(1, len(msgs)):
        sec = msgs[i]
        if sec is None:
            continue
        if isinstance(sec, UserDef):
            entries = hash_entries(sec)
        else:
            entries = [{"id": j, "en": to_str(v), "it": ""}
                       for j, v in enumerate(sec) if to_str(v)]
        if not entries:
            continue
        n, d = merge(os.path.join(TRAD_DIR, "sezioni", section_filename(i)), entries)
        total += n
        done += d
    print(f"Estratte {total} voci, di cui {done} gia' tradotte.")


if __name__ == "__main__":
    main()
