"""Divide il lavoro di traduzione in lotti e riapplica i risultati.

  py tools/lotti.py crea  <gruppo> [--max-caratteri N] [--prefisso P]
  py tools/lotti.py applica
  py tools/lotti.py stato

Gruppi:
  db-nomi      tipi, mosse, strumenti, abilita', luoghi, classi allenatori...
  db-desc      descrizioni di mosse/strumenti/abilita'/luoghi/fiocchi
  pokedex      voci del Pokedex e categorie
  dialoghi     dialoghi delle mappe, testi di script, frasi degli allenatori

Ogni lotto e' traduzione/_lavoro/<id>.json:
  {"gruppo": ..., "voci": [{"n": 1, "en": "...", "ctx": "..."}, ...]}
Il traduttore scrive traduzione/_lavoro/<id>.it.json:
  {"1": "traduzione", "2": "...", ...}

Le frasi identiche (stesso testo inglese) all'interno dello stesso ambito
vengono tradotte una sola volta e applicate ovunque.
"""
import glob
import json
import os
import sys

from fa_common import TRAD_DIR, control_codes, load_json, sanitize, save_json

WORK = os.path.join(TRAD_DIR, "_lavoro")
SEZ = os.path.join(TRAD_DIR, "sezioni")
MAPPE = os.path.join(TRAD_DIR, "mappe")

# Le sezioni con ambito "proprio" non condividono traduzioni con altre sezioni
# (es. "Psychic" tipo vs mossa, "Red" colore vs nome).
GRUPPI = {
    "db-nomi": [2, 4, 5, 7, 8, 10, 12, 13, 14, 18, 19, 21, 25, 100],
    "db-desc": [6, 9, 11, 20, 26, 101],
    "pokedex": [3],
    "dialoghi": ["mappe", 15, 16, 17, 22, 23, 24],
}
CONDIVISO = {"mappe", 15, 16, 17, 22, 23, 24}


def sez_file(i):
    m = glob.glob(os.path.join(SEZ, f"{i:03d}_*.json"))
    return m[0] if m else None


def ambito(src):
    return "dialoghi" if src in CONDIVISO else f"sez{src}"


def map_names():
    f = sez_file(21)
    return {int(e["id"]): e["en"] for e in load_json(f)} if f else {}


def sorgenti(gruppo):
    """Restituisce [(ambito, ctx, path)] nell'ordine di traduzione."""
    out = []
    names = map_names()
    for src in GRUPPI[gruppo]:
        if src == "mappe":
            for p in sorted(glob.glob(os.path.join(MAPPE, "Map*.json"))):
                mid = int(os.path.basename(p)[3:6])
                out.append((ambito(src), f"Mappa {mid}: {names.get(mid, '')}".strip(), p))
        else:
            p = sez_file(src)
            if p:
                out.append((ambito(src), os.path.basename(p)[4:-5], p))
    return out


def tutti_i_file():
    return sorted(glob.glob(os.path.join(MAPPE, "*.json")) + glob.glob(os.path.join(SEZ, "*.json")))


def ambito_di_file(p):
    if os.path.dirname(p) == MAPPE:
        return "dialoghi"
    return ambito(int(os.path.basename(p)[:3]))


def in_lavorazione():
    """Testi gia' assegnati a lotti non ancora applicati."""
    busy = set()
    for p in glob.glob(os.path.join(WORK, "*.json")):
        if p.endswith(".it.json"):
            continue
        lotto = load_json(p)
        for v in lotto["voci"]:
            busy.add((v["amb"], v["en"]))
    return busy


def crea(gruppo, max_chars=9000, prefisso=None):
    os.makedirs(WORK, exist_ok=True)
    busy = in_lavorazione()
    visti = set()
    lotti, cur, size, last_ctx = [], [], 0, None
    for amb, ctx, path in sorgenti(gruppo):
        for e in load_json(path):
            key = (amb, e["en"])
            if e["it"] or key in visti or key in busy:
                continue
            visti.add(key)
            v = {"en": e["en"], "amb": amb}
            if ctx != last_ctx:
                v["ctx"] = ctx
                last_ctx = ctx
            cur.append(v)
            size += len(e["en"])
            if size >= max_chars:
                lotti.append(cur)
                cur, size, last_ctx = [], 0, None
    if cur:
        lotti.append(cur)
    prefisso = prefisso or gruppo
    esistenti = len(glob.glob(os.path.join(WORK, f"{prefisso}_*.json")))
    ids = []
    for k, voci in enumerate(lotti, start=esistenti + 1):
        for n, v in enumerate(voci, start=1):
            v["n"] = n
        lid = f"{prefisso}_{k:03d}"
        save_json(os.path.join(WORK, lid + ".json"), {"gruppo": gruppo, "voci": voci})
        ids.append(lid)
    print(f"Creati {len(ids)} lotti ({len(visti)} testi unici).")
    for i in ids:
        print(i)


def applica():
    risultati = {}
    errori = []
    applicati = []
    for p in sorted(glob.glob(os.path.join(WORK, "*.it.json"))):
        lid = os.path.basename(p)[:-8]
        src = os.path.join(WORK, lid + ".json")
        if not os.path.exists(src):
            continue
        try:
            out = load_json(p)
        except Exception as ex:
            errori.append(f"{lid}: JSON non valido ({ex})")
            continue
        lotto = load_json(src)
        rimasti = []
        for v in lotto["voci"]:
            it = out.get(str(v["n"]))
            if not isinstance(it, str) or not it.strip():
                rimasti.append(v)
                continue
            it = sanitize(it)
            if control_codes(it) != control_codes(v["en"]):
                errori.append(f"{lid} #{v['n']}: codici diversi\n   EN: {v['en']!r}\n   IT: {it!r}")
                rimasti.append(v)
                continue
            risultati[(v["amb"], v["en"])] = it
        applicati.append((src, p, rimasti))
    # scrive nei file di traduzione
    n_voci = 0
    for path in tutti_i_file():
        amb = ambito_di_file(path)
        entries = load_json(path)
        changed = False
        for e in entries:
            t = risultati.get((amb, e["en"]))
            if t and not e["it"]:
                e["it"] = t
                n_voci += 1
                changed = True
        if changed:
            save_json(path, entries)
    # chiude i lotti applicati; quelli con voci mancanti restano come lotto ridotto
    for src, p, rimasti in applicati:
        os.remove(p)
        if rimasti:
            lotto = load_json(src)
            for n, v in enumerate(rimasti, start=1):
                v["n"] = n
            lotto["voci"] = rimasti
            save_json(src, lotto)
        else:
            os.remove(src)
    for e in errori:
        print("ERRORE:", e)
    print(f"Applicati {len(risultati)} testi unici a {n_voci} voci. Errori: {len(errori)}")
    rest = sorted(os.path.basename(s)[:-5] for s, _, r in applicati if r)
    if rest:
        print("Lotti con voci ancora da tradurre:", ", ".join(rest))


def stato():
    tot = done = 0
    for path in tutti_i_file():
        for e in load_json(path):
            tot += 1
            done += bool(e["it"])
    pend = [os.path.basename(p)[:-5] for p in glob.glob(os.path.join(WORK, "*.json"))
            if not p.endswith(".it.json")]
    print(f"Tradotte {done}/{tot} voci ({100.0 * done / tot:.1f}%). Lotti aperti: {len(pend)}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "crea":
        mc = 9000
        pre = None
        if "--max-caratteri" in args:
            mc = int(args[args.index("--max-caratteri") + 1])
        if "--prefisso" in args:
            pre = args[args.index("--prefisso") + 1]
        crea(args[1], mc, pre)
    elif args[0] == "applica":
        applica()
    elif args[0] == "stato":
        stato()
    else:
        sys.exit(__doc__)
