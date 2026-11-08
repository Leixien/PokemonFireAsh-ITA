"""Abilita la scelta della lingua nel gioco.

Modifica Settings::LANGUAGES dentro Data/Scripts.rxdata in:
    [["Italiano", "italiano.dat"], ["English", "english.dat"]]
e crea Data/english.dat (copia di messages.dat).
Prima della modifica salva Data/Scripts.rxdata.bak (solo la prima volta).

Uso:  py tools/patch_lingua.py [cartella_gioco]
"""
import os
import re
import shutil
import sys
import zlib

from rubymarshal.reader import load
from rubymarshal.writer import writes

from fa_common import DEFAULT_GAME

NEW = (b'LANGUAGES = [\r\n    ["Italiano", "italiano.dat"],\r\n'
       b'    ["English", "english.dat"]\r\n  ]')
MARK = b'["Italiano", "italiano.dat"]'


def main():
    game = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GAME
    data = os.path.join(game, "Data")
    scripts = os.path.join(data, "Scripts.rxdata")
    shutil.copyfile(os.path.join(data, "messages.dat"), os.path.join(data, "english.dat"))
    with open(scripts, "rb") as f:
        sc = load(f)
    for entry in sc:
        if entry[1] != b"Settings":
            continue
        code = zlib.decompress(entry[2])
        if MARK in code:
            print("Scripts.rxdata e' gia' stato modificato.")
            return
        m = re.search(rb"LANGUAGES = \[.*?\r?\n\s*\]", code, re.S)
        if not m:
            sys.exit("Impossibile trovare Settings::LANGUAGES")
        entry[2] = zlib.compress(code[:m.start()] + NEW + code[m.end():])
        break
    else:
        sys.exit("Script 'Settings' non trovato")
    if not os.path.exists(scripts + ".bak"):
        shutil.copyfile(scripts, scripts + ".bak")
    with open(scripts, "wb") as f:
        f.write(writes(sc))
    print("Settings::LANGUAGES aggiornato (Italiano predefinito, English opzionale).")


if __name__ == "__main__":
    main()
