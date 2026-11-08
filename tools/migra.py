"""Porta le traduzioni su una nuova versione del gioco.

Uso:  py tools/migra.py
  1. crea una memoria di traduzione dai JSON attuali in traduzione/
     (testo inglese -> italiano, per ambito: dialoghi condivisi, sezioni separate)
  2. riestrae i testi da messages.dat della versione corrente (fa_common.VERSIONE_CORRENTE)
  3. riapplica le traduzioni ai testi inglesi identici
I testi nuovi restano con "it" vuoto: si traducono poi con tools/lotti.py.
"""
import glob
import os
import shutil

from fa_common import TRAD_DIR, load_json

CONDIVISE = {15, 16, 17, 22, 23, 24}


def ambito(path):
    if os.path.basename(os.path.dirname(path)) == "mappe":
        return "dialoghi"
    i = int(os.path.basename(path)[:3])
    return "dialoghi" if i in CONDIVISE else f"sez{i}"


def memoria():
    tm = {}
    for p in glob.glob(os.path.join(TRAD_DIR, "mappe", "*.json")) + \
            glob.glob(os.path.join(TRAD_DIR, "sezioni", "*.json")):
        amb = ambito(p)
        for e in load_json(p):
            if e["it"]:
                tm.setdefault((amb, e["en"]), e["it"])
    return tm


def main():
    tm = memoria()
    print(f"Memoria di traduzione: {len(tm)} testi")
    for sub in ("mappe", "sezioni"):
        shutil.rmtree(os.path.join(TRAD_DIR, sub), ignore_errors=True)
    import estrai
    import sys
    sys.argv = sys.argv[:1]
    estrai.main()
    from fa_common import save_json
    tot = fatti = 0
    for p in glob.glob(os.path.join(TRAD_DIR, "mappe", "*.json")) + \
            glob.glob(os.path.join(TRAD_DIR, "sezioni", "*.json")):
        amb = ambito(p)
        d = load_json(p)
        for e in d:
            tot += 1
            t = tm.get((amb, e["en"]))
            if t:
                e["it"] = t
                fatti += 1
        save_json(p, d)
    print(f"Riapplicate {fatti}/{tot} traduzioni ({100.0 * fatti / tot:.1f}%); da tradurre: {tot - fatti}")


if __name__ == "__main__":
    main()
