# Guida alla traduzione – Pokémon Fire Ash ITA

## Formato dei lotti

Un lotto `traduzione/_lavoro/<id>.json` contiene:

```json
{"gruppo": "dialoghi", "voci": [{"n": 1, "en": "testo inglese", "ctx": "Mappa 5: Kurt's house", "amb": "dialoghi"}]}
```

`ctx` compare solo quando cambia il contesto (mappa o sezione) e vale anche per le voci successive.
Il risultato va scritto in `traduzione/_lavoro/<id>.it.json` come oggetto JSON `{"1": "traduzione", "2": "..."}`,
con una chiave per **ogni** voce `n` del lotto. Il file deve essere JSON valido in UTF-8
(attenzione a escapare `"` e `\` → `\\`).

## Regole obbligatorie

1. **Codici di controllo: copiali identici, nello stesso numero.** Non tradurli, non spostarli fuori dal testo
   a cui si riferiscono, non aggiungerne. Esempi: `\PN` (nome giocatore), `\RN`, `\v[12]`, `\c[2]`, `\b`, `\r`,
   `\n`, `\l`, `\wt[5]`, `\wtnp[10]`, `\se[...]`, `\me[...]`, `\ts[]`, `\G`, `\CN`, `\^`, `\.`, `\|`, `\!`, `<c2=6546675A>`,
   `<ac>`, `<b>`, `</b>`, `<i>`, `<icon=...>`, `{1}`, `{2}`, `%s`, `%d`. Il compilatore scarta le traduzioni con codici diversi.
   - I codici sono spesso **attaccati alla parola**: `\bI'll stay here` = codice `\b` + "I'll stay here" →
     `\bResterò qui`. `\b` = testo blu (personaggio maschile), `\r` = testo rosso (femminile), `\n` = a capo.
     Nel JSON il backslash va raddoppiato: `"\\bResterò qui"`.
   - Eccezione: in `\ch[1,-1,Sì,No,...]` i primi due parametri restano identici, le scelte successive vanno tradotte.
   - `\sign[...]`, `\se[...]`, `\me[...]`: il contenuto tra parentesi è un nome di file, **non tradurlo**.
2. Mantieni gli a capo (`\n` reali nel testo) circa nelle stesse posizioni; il gioco va a capo da solo nelle
   finestre di dialogo, quindi non aggiungerne di nuovi.
3. Lunghezza: l'italiano tende a essere più lungo. Per **nomi** (mosse, strumenti, abilità, tipi, classi) resta
   entro ~12–14 caratteri quando possibile (i nomi ufficiali vanno comunque bene). Per testi di menu brevi
   (es. "Bag", "Save", "Yes") usa l'equivalente breve ufficiale ("Borsa", "Salva", "Sì").
4. Usa solo caratteri supportati dai font: lettere accentate italiane OK (à è é ì ò ù È). **Non** usare
   `’` `…` `“ ”` → usa `'`, `...`, `"`. Usa la `è` accentata, mai `e'`.
5. Se un testo non va tradotto (nomi propri, sigle, numeri, testo già italiano, simboli), riscrivilo identico.

## Stile

- Segui la terminologia **ufficiale italiana** dei giochi Pokémon (nomi di mosse, strumenti, abilità, tipi,
  natura, statistiche, luoghi di Kanto/Johto/Hoenn ecc.: es. Pallet Town → Biancavilla, Viridian City →
  Smeraldopoli, Pewter City → Plumbeopoli, Route 1 → Percorso 1, Viridian Forest → Bosco Smeraldo).
- I **nomi dei Pokémon** restano invariati (sono uguali nella versione italiana).
- I luoghi e personaggi **originali di Fire Ash** (es. Lappet Town, Cedolan City, Kurt) restano col nome
  originale, ma traduci la parte generica: "Cedolan City Poké Center" → "Centro Pokémon di Cedolan City",
  "Kurt's house" → "Casa di Kurt", "\PN's house" → "Casa di \PN".
- Il gioco si rivolge al giocatore col **tu**. I personaggi parlano in modo naturale e colloquiale;
  conserva tono, battute e personalità (bulli sbruffoni, scienziati pedanti, cattivi minacciosi...).
- Mantieni la punteggiatura espressiva (`!`, `?`, `...`).

## Glossario base (ufficiale)

| Inglese | Italiano |
|---|---|
| Trainer / Pokémon Trainer | Allenatore / Allenatore di Pokémon |
| Gym / Gym Leader | Palestra / Capopalestra |
| Elite Four / Champion | Superquattro / Campione |
| Pokémon Center / Poké Mart | Centro Pokémon / Pokémon Market (Poké Market) |
| Poké Ball / Great Ball / Ultra Ball | Poké Ball / Mega Ball / Ultra Ball |
| Potion / Super Potion / Hyper Potion | Pozione / Superpozione / Iperpozione |
| Revive / Max Revive | Revitalizzante / Revitalizzante Max |
| Rare Candy | Caramella Rara |
| Badge | Medaglia |
| Bag / Party / Box / PC | Borsa / Squadra / Box / PC |
| Pokédex / Pokégear / PokéNav | Pokédex / Pokégear / PokéNav |
| HM / TM / TR | MN / MT / DT |
| Move / Ability / Nature / Item | Mossa / Abilità / Natura / Strumento |
| HP / Attack / Defense / Sp. Atk / Sp. Def / Speed | PS / Attacco / Difesa / Attacco Speciale (Att. Sp.) / Difesa Speciale (Dif. Sp.) / Velocità |
| PP / Exp. Points / Level | PP / Punti Esperienza (Esp.) / Livello (Lv.) |
| Shiny | Cromatico |
| Egg / Day Care | Uovo / Pensione |
| Team Rocket / Team Aqua / Team Magma | Team Rocket / Team Idro / Team Magma |
| Professor | Professor / Prof. |
| Rival | Rivale |
| Mega Evolution / Mega Stone | Megaevoluzione / Megapietra |
| Z-Move / Z-Crystal | Mossa Z / Cristallo Z |
| Dynamax / Gigantamax / Max Move | Dynamax / Gigamax / Mossa Dynamax |
| Alolan / Galarian / Hisuian / Kantonian Form | Forma di Alola / Forma di Galar / Forma di Hisui / Forma di Kanto |
| Wild Pokémon / Foe | Pokémon selvatico / avversario |
| Fainted | Esausto / è esausto |
| Super effective / Not very effective | È superefficace! / Non è molto efficace... |
| Critical hit | Brutto colpo! |

Tipi: Normal Normale · Fire Fuoco · Water Acqua · Grass Erba · Electric Elettro · Ice Ghiaccio ·
Fighting Lotta · Poison Veleno · Ground Terra · Flying Volante · Psychic Psico · Bug Coleottero ·
Rock Roccia · Ghost Spettro · Dragon Drago · Dark Buio · Steel Acciaio · Fairy Folletto · ??? ???

Stati: Poison Avvelenamento (avvelenato) · Burn Scottatura (scottato) · Paralysis Paralisi (paralizzato) ·
Sleep Sonno (addormentato) · Freeze Congelamento (congelato) · Confusion Confusione (confuso).

## Nomi dei personaggi

Usa il nome italiano ufficiale **solo** per i personaggi ufficiali che lo hanno; tutti gli altri restano invariati
(Brock, Misty, Gary, Oak, Kukui, Hau, Kiawe, Jessie, James, Meowth, Goh, Cerise, Paul, Iris...).

Colress → Acromio · Lysandre → Elisio · Xerosic → Xante · Gladion → Iridio · Lusamine → Samina ·
Guzma → Guzman · Faba → Vicio · Saturn → Saturno · Mars → Martes · Jupiter → Giove · Archie → Ivan ·
Courtney → Rossella · Marnie → Mary · Cynthia → Camilla · Volkner → Corrado · Cilan → Spighetto ·
Clemont → Lem · Leon → Dandel · Dawn → Lucinda · May → Vera · Lillie → Lylia · Sophocles → Chrys ·
Mallow → Ibis · Drayden → Aristide · Opal → Poppy · Allister → Onion · Bea → Fabia · Lana → Suiren · Falkner → Valerio · Steven → Rocco · Grunt → Recluta · Admin → Superiore · Nurse Joy → Infermiera Joy · Officer Jenny → Agente Jenny ·
Red/Green/Gold/Ruby/Diamond/Sun (personaggi) → restano in inglese.

## Termini ricorrenti già decisi (usali sempre)

Game Corner → Casinò · coins → gettoni · Day-Care Man/Lady → Signore/Signora della Pensione ·
Loto Ticket → Biglietto della Lotteria · Move Deleter → Cancellamosse · Move Maniac/Relearner → Maniaco delle Mosse ·
Name Rater → Giudice dei Nomi · Dr. Footstep → Dott. Impronta · Bug-Catching Contest → Gara Pigliamosche ·
Cycling Road → Pista Ciclabile · Flying Taxi → Volotaxi · Indigo League → Lega Indaco · Ribbon → Fiocco ·
World Coronation Series → World Coronation Series (invariato) · Masters Eight → Otto Master ·
Great/Ultra/Master Class (WCS) → Classe Super/Iper/Master · Ultra Beast → Ultracreatura · Apricorn → Ghicocca ·
Running Shoes → Scarpe da Corsa · Darkest Day → Giorno più Buio · Lapras Launch → Traghetto Lapras ·
Nelle scelte `\ch[...]` non usare virgole dentro un'opzione (la virgola separa le opzioni).
