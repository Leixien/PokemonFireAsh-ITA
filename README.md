# Pokemon Fire Ash - Traduzione Italiana 🇮🇹

Traduzione italiana non ufficiale di **Pokémon Fire Ash 3.4** (fan game realizzato con Pokémon Essentials).

## 📥 Come ottenere il gioco

1. Scarica Pokemon Fire Ash 3.4 dal sito ufficiale: [DOWNLOAD](https://pokemerald.com/pokemon-fire-ash-download-v3-4-completed)
2. Estrai il gioco in una cartella

## 🚀 Come installare la traduzione

> 💡 Prima di procedere fai un backup della cartella del gioco.

### Metodo automatico (consigliato)

Ti serve [Python 3.8+](https://www.python.org/downloads/).

```bash
git clone https://github.com/leixien/PokemonFireAsh-ITA
cd PokemonFireAsh-ITA
py -m pip install -r requirements.txt
py patcher/apply_translation.py "C:\percorso\di\Pokemon Fire Ash 3.4\Game"
```

Il patcher:
- copia `translated_files/italiano.dat` nella cartella `Data` del gioco;
- crea `Data/english.dat` (i testi originali in inglese);
- abilita la scelta della lingua in `Data/Scripts.rxdata` (salvando un backup in `Scripts.rxdata.bak`).

Al primo avvio il gioco chiede la lingua: scegli **Italiano**. Puoi cambiarla in seguito
dalla voce **Lingua** del menu iniziale. I salvataggi esistenti restano compatibili.

### Metodo manuale

La cartella `Pokemon Fire Ash 3.4/Game` di questo repository contiene già il gioco con la traduzione applicata:
copia `Data/italiano.dat`, `Data/english.dat` e `Data/Scripts.rxdata` nella cartella `Data` del tuo gioco.

## 📊 Stato della traduzione

Per vedere l'avanzamento aggiornato esegui `py tools/lotti.py stato`.

**Traduzione completa: 37.452 testi su 37.452 (100%)**, più 21 testi di menu che mancavano nel
`messages.dat` originale (es. "Continua", "Nuova partita").

| Sezione | Voci |
|---|---|
| Dialoghi delle mappe ed eventi comuni | 18.308 |
| Menu, lotta e testi di sistema | 3.971 |
| Mosse, strumenti, abilità, tipi (nomi e descrizioni) | ~5.500 |
| Pokédex (voci e categorie) | ~2.600 |
| Allenatori, luoghi, fiocchi e altro | ~7.000 |

Restano in inglese solo gli 81 messaggi di errore del compilatore di Essentials, visibili esclusivamente
in modalità debug.

> ⚠️ La traduzione è stata verificata con controlli automatici, ma non è
> ancora stata giocata dall'inizio alla fine. Segnalate errori, testi che escono dai riquadri e nomi non
> ufficiali nelle Issues.

I nomi dei Pokémon restano invariati, come nei giochi ufficiali in italiano.
In [`traduzione/DA_RIVEDERE.md`](traduzione/DA_RIVEDERE.md) trovi i termini da verificare.

_Ultimo aggiornamento: 2026-11-08_

## 🛠️ Come funziona

Fire Ash usa Pokémon Essentials v19: tutti i testi stanno in `Data/messages.dat`. La traduzione è un file
di lingua di Essentials (`Data/italiano.dat`) con la stessa struttura, che il gioco carica al posto dei testi originali.

```
PokemonFireAsh-ITA/
├── traduzione/
│   ├── mappe/MapNNN.json      # dialoghi di ogni mappa  {id, en, it}
│   ├── sezioni/NNN_*.json     # database: mosse, strumenti, Pokédex, testi di script...
│   ├── extra/NNN_*.json       # testi degli script assenti da messages.dat
│   ├── GUIDA_TRADUZIONE.md    # regole, stile e glossario
│   ├── glossario.tsv          # nomi già tradotti (generato)
│   └── DA_RIVEDERE.md         # dubbi terminologici
├── tools/
│   ├── estrai.py              # messages.dat -> JSON (conserva le traduzioni esistenti)
│   ├── compila.py             # JSON -> Data/italiano.dat + translated_files/
│   ├── patch_lingua.py        # abilita la scelta della lingua in Scripts.rxdata
│   ├── lotti.py               # divide il lavoro in lotti e li riapplica
│   ├── verifica_lotto.py      # controlla un lotto tradotto
│   ├── uniforma.py            # uniforma i termini ricorrenti
│   └── glossario.py           # genera glossario.tsv
├── patcher/apply_translation.py
└── translated_files/italiano.dat
```

## 🤝 Come contribuire

Per correggere una traduzione:

1. trova la frase in `traduzione/mappe/` o `traduzione/sezioni/` (cerca il testo inglese o italiano);
2. modifica il campo `"it"` lasciando intatti i codici di controllo (`\PN`, `\v[1]`, `\b`, `\n`, `{1}`...);
3. esegui `py tools/compila.py` e prova in gioco;
4. apri una Pull Request.

Prima di iniziare leggi [la guida di traduzione](traduzione/GUIDA_TRADUZIONE.md).
Se trovi un errore ma non vuoi correggerlo tu, segnalalo nelle Issues indicando il testo e dove compare.

## 📝 Note legali

Questo è un progetto fan-made non ufficiale e non affiliato con Nintendo, The Pokémon Company o Game Freak.
Pokémon è un marchio registrato di Nintendo/Creatures Inc./GAME FREAK Inc.

## 📧 Contatti

- Issues: [GitHub Issues](https://github.com/leixien/PokemonFireAsh-ITA/issues)
- Discussions: [GitHub Discussions](https://github.com/leixien/PokemonFireAsh-ITA/discussions)

## 📜 Licenza

La traduzione è rilasciata sotto licenza [MIT](LICENSE).
