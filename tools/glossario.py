"""Genera traduzione/glossario.tsv con i nomi gia' tradotti del database
(mosse, strumenti, abilita', tipi, luoghi, classi di allenatori, ...),
da consultare durante la traduzione dei dialoghi per restare coerenti.

Uso:  py tools/glossario.py
"""
import glob
import os

from fa_common import TRAD_DIR, load_json

SEZIONI = [12, 5, 7, 10, 13, 18, 19, 21, 2, 4, 25]


def main():
    righe = []
    visti = set()
    for i in SEZIONI:
        for p in glob.glob(os.path.join(TRAD_DIR, "sezioni", f"{i:03d}_*.json")):
            nome = os.path.basename(p)[4:-5]
            for e in load_json(p):
                if e["it"] and (nome, e["en"]) not in visti:
                    visti.add((nome, e["en"]))
                    righe.append(f"{nome}\t{e['en']}\t{e['it']}")
    with open(os.path.join(TRAD_DIR, "glossario.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("sezione\tinglese\titaliano\n" + "\n".join(righe) + "\n")
    print(f"glossario.tsv: {len(righe)} voci")


if __name__ == "__main__":
    main()
