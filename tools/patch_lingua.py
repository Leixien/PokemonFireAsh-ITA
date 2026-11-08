"""Abilita l'italiano nella scelta della lingua del gioco.

Modifica Settings::LANGUAGES dentro Data/Scripts.rxdata:
  - versione 3.7.x: il gioco ha gia' English/French/Spanish/German e una riga
    commentata `#["Italian", "italian.dat"]`, che viene riattivata come
    ["Italiano", "italian.dat"] (in fondo, cosi' le lingue gia' scelte nei
    salvataggi non cambiano);
  - giochi senza lista delle lingue (es. versioni vecchie come la 3.4): diventa
    [["Italiano", "italiano.dat"], ["English", "english.dat"]], creando
    Data/english.dat come copia di messages.dat.
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

NEW_34 = (b'LANGUAGES = [\r\n    ["Italiano", "italiano.dat"],\r\n'
          b'    ["English", "english.dat"]\r\n  ]')
COMMENTED_IT = re.compile(rb'#(\s*)\["Italian",\s*"italian\.dat"\]')
MARKS = (b'["Italiano", "italiano.dat"]', b'["Italiano", "italian.dat"]')


def patch_code(code):
    """Restituisce (nuovo_codice, descrizione) oppure (None, motivo)."""
    if any(m in code for m in MARKS):
        return None, "gia' modificato"
    if COMMENTED_IT.search(code):
        return COMMENTED_IT.sub(rb'\1["Italiano", "italian.dat"]', code, count=1), "3.7"
    m = re.search(rb"LANGUAGES = \[.*?\r?\n\s*\]", code, re.S)
    if not m:
        return None, "Settings::LANGUAGES non trovato"
    body = code[m.start():m.end()]
    if re.search(rb'^\s*\["', body, re.M):
        return None, "LANGUAGES contiene gia' altre lingue in un formato non previsto"
    return code[:m.start()] + NEW_34 + code[m.end():], "3.4"


def main():
    game = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GAME
    data = os.path.join(game, "Data")
    scripts = os.path.join(data, "Scripts.rxdata")
    with open(scripts, "rb") as f:
        sc = load(f)
    for entry in sc:
        if entry[1] != b"Settings":
            continue
        new, kind = patch_code(zlib.decompress(entry[2]))
        if new is None:
            if kind == "gia' modificato":
                print("Scripts.rxdata e' gia' stato modificato.")
                return
            sys.exit("Impossibile modificare la lista delle lingue: " + kind)
        entry[2] = zlib.compress(new)
        break
    else:
        sys.exit("Script 'Settings' non trovato")
    if kind == "3.4":
        shutil.copyfile(os.path.join(data, "messages.dat"), os.path.join(data, "english.dat"))
    if not os.path.exists(scripts + ".bak"):
        shutil.copyfile(scripts, scripts + ".bak")
    with open(scripts, "wb") as f:
        f.write(writes(sc))
    if kind == "3.4":
        print("Settings::LANGUAGES aggiornato (Italiano predefinito, English opzionale).")
    else:
        print("Italiano aggiunto all'elenco delle lingue del gioco.")


if __name__ == "__main__":
    main()
