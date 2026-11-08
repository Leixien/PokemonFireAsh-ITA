"""Compila i JSON di traduzione/ in Data/italiano.dat.

Uso:  py tools/compila.py [cartella_gioco]

Le voci non tradotte mantengono il testo originale inglese.
Stampa anche gli avvisi sui codici di controllo (\\PN, \\v[1], {1}, ...)
che non coincidono tra originale e traduzione.
"""
import os
import shutil
import sys

from rubymarshal.classes import UserDef
from rubymarshal.writer import writes

from fa_common import (DEFAULT_GAME, ROOT, TRAD_DIR, VERSIONI, VERSIONE_CORRENTE, control_codes, load_json,
                       load_messages, make_ordered_hash, read_ordered_hash,
                       rstr, sanitize, section_filename, to_str, SECTION_NAMES)

warnings = []


def translations(path):
    if not os.path.exists(path):
        return {}
    out = {}
    for e in load_json(path):
        it = e.get("it")
        if not it:
            continue
        it = sanitize(it)
        if control_codes(it) != control_codes(e["en"]):
            warnings.append(f"{os.path.basename(path)} [{e['id']}]: codici diversi\n"
                            f"    EN: {e['en']!r}\n    IT: {it!r}")
        out[(str(e["id"]), e["en"])] = it
    return out


def extra_entries(i):
    """Voci aggiuntive (testi _INTL degli script assenti da messages.dat)."""
    path = os.path.join(TRAD_DIR, "extra", section_filename(i)[:4] + SECTION_NAMES.get(i, "") + ".json")
    if not os.path.exists(path):
        return []
    return [(e["id"], sanitize(e["it"])) for e in load_json(path) if e.get("it")]


def build_hash(u, tr, extra=()):
    pairs = []
    n = 0
    for k, v in read_ordered_hash(u):
        t = tr.get((k, v)) if v else None
        if t:
            n += 1
        pairs.append((k, t or v or ""))
    known = {k for k, _ in pairs}
    pairs += [(k, t) for k, t in extra if k not in known]
    return make_ordered_hash(pairs), n, sum(1 for _, v in read_ordered_hash(u) if v)


def main():
    game = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GAME
    src = load_messages(os.path.join(game, "Data", "messages.dat"))
    out = []
    total = done = 0
    maps = []
    for mapid, u in enumerate(src[0] or []):
        if not isinstance(u, UserDef):
            maps.append(u)
            continue
        tr = translations(os.path.join(TRAD_DIR, "mappe", f"Map{mapid:03d}.json"))
        h, d, n = build_hash(u, tr)
        maps.append(h)
        total += n
        done += d
    out.append(maps)
    for i in range(1, len(src)):
        sec = src[i]
        if sec is None:
            out.append(None)
            continue
        tr = translations(os.path.join(TRAD_DIR, "sezioni", section_filename(i)))
        if isinstance(sec, UserDef):
            h, d, n = build_hash(sec, tr, extra_entries(i))
            out.append(h)
        else:
            arr = []
            d = n = 0
            for j, v in enumerate(sec):
                v = to_str(v)
                if v:
                    n += 1
                    t = tr.get((str(j), v))
                    if t:
                        d += 1
                    arr.append(rstr(t or v))
                else:
                    arr.append(rstr(v) if v is not None else None)
            out.append(arr)
        total += n
        done += d
    cfg = VERSIONI[VERSIONE_CORRENTE]
    dist = os.path.join(ROOT, "translated_files", VERSIONE_CORRENTE)
    os.makedirs(dist, exist_ok=True)
    dest = os.path.join(dist, cfg["file"])
    with open(dest, "wb") as f:
        f.write(writes(out))
    if len(sys.argv) > 1:  # copia anche in una cartella di gioco indicata
        shutil.copyfile(dest, os.path.join(game, "Data", cfg["file"]))
    for w in warnings:
        print("ATTENZIONE:", w)
    pct = 100.0 * done / total if total else 0
    print(f"Scritto {dest}")
    print(f"Tradotte {done}/{total} voci ({pct:.1f}%). Avvisi: {len(warnings)}")


if __name__ == "__main__":
    main()
