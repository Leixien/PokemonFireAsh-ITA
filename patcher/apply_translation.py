"""Applica la traduzione italiana a una copia di Pokemon Fire Ash 3.4.

Uso:
    py -m pip install -r requirements.txt
    py patcher/apply_translation.py "C:\\percorso\\di\\Pokemon Fire Ash 3.4\\Game"

Cosa fa:
  1. copia translated_files/italiano.dat in <gioco>/Data/
  2. crea <gioco>/Data/english.dat (copia di messages.dat)
  3. abilita la scelta della lingua in Data/Scripts.rxdata
     (backup in Data/Scripts.rxdata.bak)
Al primo avvio il gioco chiede la lingua; si può cambiare dal menu iniziale.
"""
import hashlib
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import patch_lingua  # noqa: E402

# Impronta SHA-256 di Data/messages.dat di Pokemon Fire Ash 3.4 (versione tradotta).
MESSAGES_34 = "581ac5d20c3ab2f59acb4fae8d8c6e562d8b0299cb5e8b73e150a89587d63c6a"


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
        sys.exit(f"Non trovo {messages}: indica la cartella 'Game' di Fire Ash.")
    if sha256(messages) != MESSAGES_34 and "--forza" not in sys.argv:
        sys.exit("Questa copia del gioco non sembra Pokemon Fire Ash 3.4: la traduzione e' stata fatta\n"
                 "per la 3.4 e su altre versioni (es. 3.7.1) molti testi resterebbero in inglese o\n"
                 "potrebbero esserci problemi. Usa la copia 3.4 inclusa nel repository oppure, se sai\n"
                 "cosa stai facendo, aggiungi --forza.")
    src = os.path.join(ROOT, "translated_files", "italiano.dat")
    if not os.path.exists(src):
        sys.exit("translated_files/italiano.dat mancante: esegui prima tools/compila.py")
    shutil.copyfile(src, os.path.join(data, "italiano.dat"))
    print("Copiato italiano.dat")
    sys.argv = [sys.argv[0], game]
    patch_lingua.main()
    print("Traduzione applicata! Avvia Game.exe e scegli 'Italiano'.")


if __name__ == "__main__":
    main()
