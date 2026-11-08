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
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import patch_lingua  # noqa: E402


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    game = os.path.abspath(sys.argv[1])
    data = os.path.join(game, "Data")
    if not os.path.exists(os.path.join(data, "messages.dat")):
        sys.exit(f"Non trovo {data}\\messages.dat: indica la cartella 'Game' di Fire Ash.")
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
