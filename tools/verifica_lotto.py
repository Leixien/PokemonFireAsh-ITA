"""Verifica un lotto tradotto: JSON valido, voci complete, codici di controllo.

Uso:  py tools/verifica_lotto.py <id_lotto>
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fa_common import TRAD_DIR, control_codes, sanitize  # noqa: E402

WORK = os.path.join(TRAD_DIR, "_lavoro")


def main():
    lid = sys.argv[1].replace(".it.json", "").replace(".json", "")
    with open(os.path.join(WORK, lid + ".json"), encoding="utf-8") as f:
        voci = json.load(f)["voci"]
    try:
        with open(os.path.join(WORK, lid + ".it.json"), encoding="utf-8") as f:
            out = json.load(f)
    except json.JSONDecodeError as ex:
        sys.exit(f"JSON NON VALIDO: {ex}")
    problemi = 0
    mancanti = [v["n"] for v in voci if not str(out.get(str(v["n"]), "")).strip()]
    if mancanti:
        problemi += 1
        print(f"Voci mancanti ({len(mancanti)}): {mancanti[:50]}")
    for v in voci:
        it = out.get(str(v["n"]))
        if isinstance(it, str) and it.strip():
            a, b = control_codes(v["en"]), control_codes(sanitize(it))
            if a != b:
                problemi += 1
                print(f"#{v['n']} codici diversi: EN {a} / IT {b}\n   EN: {v['en']!r}\n   IT: {it!r}")
    print("OK" if not problemi else f"{problemi} problemi da correggere")


if __name__ == "__main__":
    main()
