"""Uniforma termini ricorrenti tradotti in modo diverso da lotti diversi.

Ogni regola: (regex sul testo inglese o None, regex sul testo italiano, sostituzione).
La sostituzione avviene solo se il testo inglese contiene il termine di origine,
cosi' non si toccano usi legittimi (es. "Mistralopoli" e' corretto per Icirrus).

Uso:  py tools/uniforma.py [--prova]
"""
import glob
import os
import re
import sys

from fa_common import TRAD_DIR, control_codes, load_json, save_json

REGOLE = [
    # luoghi
    (r"Battle Factory", r"Industria Lotta", "Fabbrica Lotta"),
    (r"Battle Hall", r"Salone Lotta", "Sala Lotta"),
    (r"Mistralton", r"Mistralopoli", "Ponentopoli"),
    (r"Floaroma", r"Fiordoropoli", "Floraria"),
    (r"Floaroma Meadow", r"Prato Fiorito", "Prato Floraria"),
    (r"Valor Lakefront", r"Sponda Valore", "Riva Lago Valore"),
    (r"Fallarbor", r"Mentania", "Brunifoglia"),
    (r"Verdanturf", r"Brunifoglia", "Mentania"),
    (r"Game Corner", r"Sala Giochi", "Casinò"),
    (r"Contest Hall", r"Salone Gare", "Sala Gare"),
    (r"Royal Avenue", r"Viale Royal", "Viale Reale"),
    (r"Poni Breaker Coast", r"Costa Frangente di Poni", "Costa Frangiflutti di Poni"),
    (r"Melemele", r"Melemele", "Mele Mele"),
    (r"Masked Royal", r"Royal Mascherato", "Reale Mascherato"),
    # anime / WCS
    (r"World Coronation Series", r"(Serie Mondiale dell'Incoronazione( Pokémon)?|Campionato Mondiale)",
     "World Coronation Series"),
    (r"Masters Eight", r"Otto Maestri", "Otto Master"),
    (r"Great Class", r"Classe (Grandi|Alta|Grande)", "Classe Super"),
    (r"Darkest Day", r"Notte Nera", "Giorno più Buio"),
    (r"Loto.?Ticket", r"Biglietto (del )?Lotto\b", "Biglietto della Lotteria"),
    # personaggi
    (r"\bBea\b", r"\bFania\b", "Fabia"),
    (r"\bOpal\b", r"\bOpal\b", "Poppy"),
    (r"Wikstrom", r"\bWikstrom\b", "Narciso"),
    # Unima: Cilan = Spighetto, Chili = Chicco, Cress = Maisello
    (r"\bChili\b(?!.*\bCress\b)", r"\bMaisello\b", "Chicco"),
    (r"\bCress\b(?!.*\bChili\b)", r"\bChicco\b", "Maisello"),
    (r"Hyper Training", r"Allenamento Speciale", "Allenamento Supremo"),
    (r"Relic Stone", r"Sacra Pietra", "Pietra Reliquia"),
    # mosse
    (r"\bSwallow\b", r"\bIntroversione\b", "Introenergia"),
]


# Citta' di Kalos: applicate solo se la frase inglese ne nomina una sola,
# perche' le traduzioni errate si scambiano tra loro.
KALOS = {
    "Camphrier": (r"Romantopoli", "Castel Vanità"),
    "Coumarine": (r"Altoripoli|Fluxopoli", "Batikopoli"),
    "Laverre": (r"Batikopoli", "Romantopoli"),
    "Anistar": (r"Temperopoli", "Fluxopoli"),
    "Geosenge": (r"Cromleckburgo|Petroglifari", "Cromleburgo"),
    "Parfum Palace": (r"Palazzo Fragranza", "Palazzo Parfum"),
    "Battle Arena": (r"Arena Lotta", "Dojo Lotta"),
}


def kalos(en, it):
    hits = [k for k in KALOS if k in en]
    if len(hits) != 1:
        return it
    pat, sost = KALOS[hits[0]]
    return re.sub(pat, sost, it)


ACC = str.maketrans("àèéìòù", "ÀÈÉÌÒÙ")
CAPS_WORD = re.compile(r"\b(?=\w*[A-Z]\w*[A-Z])(?=\w*[àèéìòù])[A-Zàèéìòù]{2,}\b")


def maiuscole(it):
    """FELICITà -> FELICITÀ (parole tutte maiuscole con accento minuscolo)."""
    return CAPS_WORD.sub(lambda m: m.group(0).translate(ACC), it)


def main():
    prova = "--prova" in sys.argv
    regole = [(re.compile(a) if a else None, re.compile(b), c) for a, b, c in REGOLE]
    tot = 0
    files = glob.glob(os.path.join(TRAD_DIR, "mappe", "*.json")) + \
        glob.glob(os.path.join(TRAD_DIR, "sezioni", "*.json"))
    for p in sorted(files):
        entries = load_json(p)
        changed = False
        for e in entries:
            it = e["it"]
            if not it:
                continue
            new = it
            for ren, rit, sost in regole:
                if ren is None or ren.search(e["en"]):
                    new = rit.sub(sost, new)
            new = kalos(e["en"], new)
            new = maiuscole(new)
            if new != it and control_codes(new) == control_codes(it):
                tot += 1
                if prova and tot <= 40:
                    print(f"{os.path.basename(p)}: {it[:70]!r} -> {new[:70]!r}")
                e["it"] = new
                changed = True
        if changed and not prova:
            save_json(p, entries)
    print(f"{'Da correggere' if prova else 'Corrette'}: {tot} voci")


if __name__ == "__main__":
    main()
