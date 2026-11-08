"""Funzioni comuni per la pipeline di traduzione di Pokemon Fire Ash.

Il gioco usa Pokemon Essentials (v19). Tutti i testi traducibili sono in
Data/messages.dat, un Marshal Ruby con questa struttura:

  messages[0]          -> lista indicizzata per ID mappa, ogni elemento e' un
                          OrderedHash {testo_originale_normalizzato => testo}
                          (messages[0][0] = eventi comuni)
  messages[1..26,...]  -> Array (indice -> testo) oppure OrderedHash
                          (vedi MessageTypes in Scripts/Intl_Messages.rb)

Un file di lingua (es. Data/italiano.dat) ha la stessa identica struttura ma
contiene i testi tradotti come valori.
"""
import json
import os
import re

from rubymarshal.classes import RubyString, UserDef
from rubymarshal.reader import load, loads
from rubymarshal.writer import writes

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAD_DIR = os.path.join(ROOT, "traduzione")

# Versioni supportate. "sorgente" contiene Data/messages.dat e Data/Scripts.rxdata
# originali; "file" e' il nome del file di lingua atteso dal gioco.
VERSIONI = {
    "3.7.1": {
        "sorgente": os.path.join(ROOT, "originali", "3.7.1"),
        "file": "italian.dat",
        "messages_sha256": "65d3ee79d275cac40f7f82268cf3dac49d333eb74f8dc0223bc78246505c499d",
    },
    "3.4": {
        "sorgente": os.path.join(ROOT, "Pokemon Fire Ash 3.4", "Game"),
        "file": "italiano.dat",
        "messages_sha256": "581ac5d20c3ab2f59acb4fae8d8c6e562d8b0299cb5e8b73e150a89587d63c6a",
    },
}
VERSIONE_CORRENTE = "3.7.1"   # i JSON in traduzione/ sono allineati a questa versione
DEFAULT_GAME = VERSIONI[VERSIONE_CORRENTE]["sorgente"]


def versione_da_hash(sha):
    for v, cfg in VERSIONI.items():
        if cfg["messages_sha256"] == sha:
            return v
    return None

SECTION_NAMES = {
    1: "Species", 2: "Kinds", 3: "Entries", 4: "FormNames", 5: "Moves",
    6: "MoveDescriptions", 7: "Items", 8: "ItemPlurals", 9: "ItemDescriptions",
    10: "Abilities", 11: "AbilityDescs", 12: "Types", 13: "TrainerTypes",
    14: "TrainerNames", 15: "BeginSpeech", 16: "EndSpeechWin",
    17: "EndSpeechLose", 18: "RegionNames", 19: "PlaceNames",
    20: "PlaceDescriptions", 21: "MapNames", 22: "PhoneMessages",
    23: "TrainerLoseText", 24: "ScriptTexts", 25: "RibbonNames",
    26: "RibbonDescriptions",
}


def section_filename(i):
    name = SECTION_NAMES.get(i, "Extra")
    return f"{i:03d}_{name}.json"


def to_str(x):
    if x is None:
        return None
    if isinstance(x, RubyString):
        return x.text
    if isinstance(x, bytes):
        return x.decode("utf-8")
    return str(x)


def rstr(text):
    return RubyString(text, {"E": True})


def read_ordered_hash(u):
    keys, values = loads(u._private_data)
    return [(to_str(k), to_str(v)) for k, v in zip(keys, values)]


def make_ordered_hash(pairs):
    u = UserDef("OrderedHash")
    keys = [rstr(k) for k, _ in pairs]
    values = [rstr(v) for _, v in pairs]
    u._private_data = writes([keys, values])
    return u


def load_messages(path):
    with open(path, "rb") as f:
        return load(f)


def save_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# Codici di controllo dei messaggi Essentials che devono restare identici
# nella traduzione (\PN, \v[1], \c[2], \se[...], \wt[5], {1}, ecc.).
CONTROL_RE = re.compile(
    r"\\[A-Za-z]+\[[^\]]*\]"                              # \v[1], \wtnp[20], \ch[...]
    r"|\\(?:PN|CN|RN|PM|op|cl|wu|wm|wd|ff|G|b|r|n|l|w)"   # \PN, \b, \r, \n (anche attaccati)
    r"|\\[.|!^\\]"                                        # \. \| \! \^ \\
    r"|\{\d+\}|</?[a-z][a-z0-9]*(?:=[^<>]*)?>|\x01|%[sd]"  # {1}, <b>, <c2=...>, %s
)


def _norm_code(c):
    # \ch[var,annulla,Scelta1,Scelta2,...]: le scelte vanno tradotte, si
    # confrontano solo i primi due parametri numerici.
    if c.startswith("\\ch["):
        return "\\ch[" + ",".join(c[4:-1].split(",")[:2]) + "]"
    return c


def control_codes(text):
    return sorted(_norm_code(c) for c in CONTROL_RE.findall(text or ""))


def sanitize(t):
    """Sostituisce i caratteri tipografici non presenti nei font del gioco."""
    return (t.replace("’", "'").replace("‘", "'").replace("…", "...")
             .replace("“", '"').replace("”", '"')
             .replace("—", "-").replace("–", "-"))
