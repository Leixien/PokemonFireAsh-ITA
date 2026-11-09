"""Applica la traduzione italiana a Pokemon Fire Ash 3.7.1.

Uso:
    py -m pip install -r requirements.txt
    py patcher/apply_translation.py "C:\\percorso\\della\\cartella\\del\\gioco"

La cartella e' quella che contiene Game.exe e la cartella Data.
Il patcher controlla la versione del gioco e:
  1. copia italian.dat in <gioco>/Data/
  2. aggiunge "Italiano" alla scelta della lingua in Data/Scripts.rxdata
     (backup in Data/Scripts.rxdata.bak)
Scegli la lingua al primo avvio o dalla voce "Language" del menu iniziale.
Su versioni non riconosciute si ferma (aggiungi --forza per tentare comunque).
"""
import hashlib
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import patch_lingua  # noqa: E402
from fa_common import VERSIONI, VERSIONE_CORRENTE, versione_da_hash  # noqa: E402


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    args = [a for a in sys.argv[1:] if a != "--forza"]
    if not args:
        sys.exit(__doc__)
    game = os.path.abspath(args[0])
    data = os.path.join(game, "Data")
    messages = os.path.join(data, "messages.dat")
    if not os.path.exists(messages):
        sys.exit(f"Non trovo {messages}: indica la cartella del gioco (quella con Game.exe).")
    versione = versione_da_hash(sha256(messages))
    if versione is None:
        if "--forza" not in sys.argv:
            sys.exit("Versione del gioco non riconosciuta. La traduzione supporta Pokemon Fire Ash\n"
                     + ", ".join(VERSIONI) + ". Su altre versioni molti testi resterebbero in inglese\n"
                     "o potrebbero esserci problemi. Se sai cosa stai facendo, aggiungi --forza.")
        versione = VERSIONE_CORRENTE
        print(f"Versione non riconosciuta: uso comunque la traduzione della {versione}.")
    else:
        print(f"Versione riconosciuta: Pokemon Fire Ash {versione}")
    nome = VERSIONI[versione]["file"]
    src = os.path.join(ROOT, "translated_files", versione, nome)
    if not os.path.exists(src):
        sys.exit(f"File di traduzione mancante: {src}")
    shutil.copyfile(src, os.path.join(data, nome))
    print(f"Copiato {nome}")
    sys.argv = [sys.argv[0], game]
    patch_lingua.main()
    print("Traduzione applicata! Avvia Game.exe e scegli 'Italiano'.")


if __name__ == "__main__":
    main()
