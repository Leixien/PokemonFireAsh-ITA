# Pokemon Fire Ash - Traduzione Italiana 🇮🇹

Traduzione italiana non ufficiale di **Pokémon Fire Ash** (fan game realizzato con Pokémon Essentials).

| Versione del gioco | Supporto |
|---|---|
| **3.7.1** (quella distribuita ora) | ✅ Completa, consigliata |
| 3.4 | ✅ Completa (non più aggiornata) |
| Altre versioni | ❌ Il patcher si ferma: molti testi resterebbero in inglese |

## 📥 Come ottenere il gioco

Scarica **Pokémon Fire Ash 3.7.1** ed estrai l'archivio in una cartella, ad esempio dalla
[pagina di download](https://pokemerald.com/pokemon-fire-ash-download-v3-4-completed/) (nonostante
l'indirizzo, la pagina distribuisce la 3.7.1).

Se preferisci la **3.4**, questo repository la contiene già con la traduzione applicata, nella cartella
`Pokemon Fire Ash 3.4/Game`: scarica il repository (**Code → Download ZIP** su GitHub), estrailo e avvia
`Pokemon Fire Ash 3.4/Game/Game.exe`.

## 🚀 Come installare la traduzione

> 💡 Prima di procedere fai un backup della cartella del gioco.

### Metodo semplice (copia di 2 file, senza programmi)

Scarica questo repository (**Code → Download ZIP**) e copia nella cartella `Data` del gioco
(sovrascrivendo `Scripts.rxdata`):

| Versione | File da copiare |
|---|---|
| 3.7.1 | `translated_files/3.7.1/italian.dat` e `translated_files/3.7.1/Scripts.rxdata` |
| 3.4 | `translated_files/3.4/italiano.dat`, `english.dat` e `Scripts.rxdata` |

### Metodo automatico (con Python)

Ti serve [Python 3.8+](https://www.python.org/downloads/).

```bash
git clone https://github.com/leixien/PokemonFireAsh-ITA
cd PokemonFireAsh-ITA
py -m pip install -r requirements.txt
py patcher/apply_translation.py "C:\percorso\della\cartella\del\gioco"
```

La cartella del gioco è quella che contiene `Game.exe`. Il patcher riconosce da solo la versione
(3.7.1 o 3.4), copia il file di lingua giusto e aggiunge **Italiano** alla scelta della lingua in
`Data/Scripts.rxdata`, salvando un backup in `Scripts.rxdata.bak`.

### Scegliere l'italiano

- **3.7.1:** il gioco ha già il menu delle lingue (English, French, Spanish, German): ora c'è anche
  **Italiano**. Scegli la lingua al primo avvio oppure dalla voce **Language** del menu iniziale.
- **3.4:** al primo avvio il gioco chiede la lingua: scegli **Italiano**.

I salvataggi esistenti restano compatibili.

## 📊 Stato della traduzione

Per vedere l'avanzamento aggiornato esegui `py tools/lotti.py stato`.

**Versione 3.7.1: 42.534 testi su 42.534 (100%)**, più 35 testi dei menu che mancavano nel
`messages.dat` originale (es. "Continua", "Nuova partita", "Carica partita").

| Sezione | Voci |
|---|---|
| Dialoghi delle mappe ed eventi comuni | 20.954 |
| Menu, lotta e testi di sistema | 4.611 |
| Mosse, strumenti, abilità, tipi (nomi e descrizioni) | ~6.000 |
| Pokédex (voci e categorie) | ~2.600 |
| Allenatori, luoghi, fiocchi e altro | ~8.300 |

Restano in inglese solo i messaggi di errore del compilatore di Essentials, visibili esclusivamente
in modalità debug.

**Nomi ufficiali:** mosse, abilità, strumenti, tipi, nature, categorie dei Pokémon e luoghi dei giochi
ufficiali usano i nomi della versione italiana (confrontati con i dati di [PokeAPI](https://pokeapi.co/)),
anche quando sono citati nei dialoghi e nelle descrizioni.

> ⚠️ La traduzione è stata verificata con controlli automatici e provata in gioco, ma non ancora
> giocata dall'inizio alla fine. Segnalate errori, testi che escono dai riquadri e nomi non
> ufficiali nelle Issues.

I nomi dei Pokémon restano invariati, come nei giochi ufficiali in italiano.
In [`traduzione/DA_RIVEDERE.md`](traduzione/DA_RIVEDERE.md) trovi i termini da verificare.

_Ultimo aggiornamento: 2026-11-08_

## 🎮 Giocare con il controller

Il gioco gira su mkxp-z, che supporta i controller nativamente: collega il controller **prima** di avviare
`Game.exe` e dovrebbe funzionare subito.

Se un pulsante non fa quello che ti aspetti, premi **F1** sulla tastiera durante il gioco: si apre la
finestra delle assegnazioni, dove puoi associare a ogni azione (Use = conferma, Back = indietro,
Action = menu...) il pulsante del controller che preferisci. La configurazione viene salvata.

Se il controller non viene rilevato (capita con alcuni controller PlayStation o generici), avvia il
gioco da Steam come "gioco non Steam" con Steam Input attivo, oppure usa
[DS4Windows](https://ds4-windows.com/).

## 🛠️ Come funziona

Fire Ash usa Pokémon Essentials: tutti i testi stanno in `Data/messages.dat`. La traduzione è un file
di lingua di Essentials (`Data/italian.dat` nella 3.7.1, `Data/italiano.dat` nella 3.4) con la stessa struttura,
che il gioco carica al posto dei testi originali. I JSON in `traduzione/` sono allineati alla 3.7.1.

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
│   ├── compila.py             # JSON -> translated_files/<versione>/
│   ├── migra.py               # porta le traduzioni su una nuova versione del gioco
│   ├── patch_lingua.py        # abilita la scelta della lingua in Scripts.rxdata
│   ├── lotti.py               # divide il lavoro in lotti e li riapplica
│   ├── verifica_lotto.py      # controlla un lotto tradotto
│   ├── uniforma.py            # uniforma i termini ricorrenti
│   └── glossario.py           # genera glossario.tsv
├── patcher/apply_translation.py
├── originali/3.7.1/Data/      # messages.dat e Scripts.rxdata originali della 3.7.1
└── translated_files/          # file pronti: 3.7.1/italian.dat, 3.4/italiano.dat, Scripts.rxdata
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
