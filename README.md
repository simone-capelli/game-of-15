# Prova pratica — Gioco del 15 con classifica

> Ciao, e scusa per l'attesa nel mandarti la prova: la piattaforma è uscita da pochi
> giorni e in questo periodo stiamo rincorrendo parecchie cose insieme.
>
> Se qualcosa non ti è chiaro — la traccia, il setup, una scelta tecnica, anche solo un
> dubbio stupido — **scrivimi pure in qualsiasi momento**, per qualunque domanda. Chiedere
> non toglie niente alla valutazione, anzi: preferiamo una domanda a mezz'ora persa.

Piccola applicazione full-stack: un backend Python che genera partite del **gioco del 15**
(griglia 4x4, 15 tessere + una casella vuota), tiene traccia delle mosse e pubblica una
classifica; un frontend Next.js che permette di giocarci.

Il backend è **già scritto per l'80%**: gira, si avvia, espone le API. Ha però sei punti
lasciati aperti — alcuni da scrivere da zero, altri con un bug da trovare. Il frontend
**non esiste**: in `frontend/README.md` c'è la specifica di quello che deve fare.

**Tempo indicativo: 3–4 ore.** Non è una gara a chi fa di più: meglio poco e fatto bene.

---

## Cosa c'è nella repo

```
.
├── README.md              <- questo file: leggi tutto prima di partire
├── backend/               <- Python + FastAPI, da completare
│   ├── app/
│   │   ├── main.py        ok   app FastAPI, CORS
│   │   ├── models.py      ok   schemi Pydantic (= contratto con il frontend)
│   │   ├── store.py       ok   persistenza in memoria
│   │   ├── puzzle.py      !!   logica di gioco — TODO(1)(2)(3)
│   │   └── api.py         !!   endpoint HTTP — TODO(4)(5)(6)
│   └── tests/             ok   pytest: 8 verdi, 8 rossi. Falli diventare verdi.
└── frontend/
    └── README.md          <- specifica del frontend Next.js da costruire
```

---

## Avvio

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```

- API: <http://localhost:8000/api/games>
- Documentazione interattiva (Swagger): <http://localhost:8000/docs>
- Test: `pytest -v`

Il server parte anche adesso e ci si può già giocare — solo che circa **una partita su
due è impossibile da risolvere**. È il TODO(3).

### Frontend

Da creare tu, dentro `frontend/`. Vedi `frontend/README.md`.

---

## Parte 1 — Backend: i sei punti aperti

Ogni TODO è marcato nel codice con `TODO(n)` ed è coperto da almeno un test che oggi
fallisce. Parti da `pytest -v` e usa la lista dei rossi come to-do list.

| # | File | Cosa manca |
|---|------|-----------|
| 1 | `puzzle.py` → `neighbors()` | **Bug.** Due caselle su righe diverse vengono considerate adiacenti (fine riga / inizio riga successiva), quindi il gioco accetta mosse impossibili. |
| 2 | `puzzle.py` → `is_solvable()` | **Da scrivere.** Metà delle disposizioni della board non è risolvibile: serve saperlo prima di servire una partita. Il suggerimento (conteggio delle inversioni + riga della casella vuota) è nella docstring. |
| 3 | `puzzle.py` → `generate_board()` | **Da correggere.** Oggi mescola a caso: esce spesso una board impossibile e ogni tanto una già risolta. Deve generare **sempre** partite risolvibili e mai già finite, restando riproducibile a parità di `seed`. |
| 4 | `api.py` → `make_move()` | Una partita già conclusa deve rifiutare altre mosse con **HTTP 409**. |
| 5 | `api.py` → `make_move()` | Quando la board arriva alla configurazione finale la partita va chiusa: `solved`, `finished_at`, `duration_ms`. |
| 6 | `api.py` → `leaderboard()` | La classifica ha tre difetti: include le partite non finite, ordina solo per mosse (a parità di mosse deve vincere il tempo più basso) e ignora `limit`. |

**Bonus, del tutto facoltativo:** `puzzle.solve()` e l'endpoint `GET /api/games/{id}/hint`,
che oggi risponde 501. Un A* con distanza di Manhattan basta e avanza. Non fa punteggio se
gli altri sei non sono a posto.

### Vincoli

- **Nessun database.** Le partite vivono in memoria (`store.py`) e spariscono al riavvio: è voluto.
- Non cambiare la forma delle risposte in `models.py` senza motivo: è il contratto con il frontend.
- I test già verdi devono restare verdi.
- Puoi aggiungere test tuoi, sono benvenuti.
- Librerie extra: solo se servono davvero, e scrivi perché.

---

## Contratto API

Base URL: `http://localhost:8000`

### `POST /api/games` → 201

```jsonc
// richiesta
{ "player": "Ada", "seed": 42 }   // seed opzionale, serve a riprodurre la stessa board
```

```jsonc
// risposta (oggetto Game, lo stesso che torna da tutti gli endpoint di gioco)
{
  "id": "a1b2c3d4e5f6",
  "player": "Ada",
  "board": [5, 1, 2, 4, 9, 6, 3, 8, 13, 10, 7, 12, 0, 14, 11, 15],
  "moves": 0,
  "solved": false,
  "created_at": "2026-09-07T10:00:00Z",
  "finished_at": null,
  "duration_ms": null,
  "movable": [9, 14]      // tessere cliccabili in questo momento
}
```

`board` è una lista piatta di 16 numeri letta per righe; `0` è la casella vuota.
La configurazione vinta è `[1,2,…,15,0]`.

### Altri endpoint

| Metodo | Path | Risposta |
|--------|------|----------|
| `GET`  | `/api/games` | lista di `Game`, dalla più recente |
| `GET`  | `/api/games/{id}` | `Game` — 404 se non esiste |
| `POST` | `/api/games/{id}/moves` — body `{ "tile": 9 }` | `Game` aggiornato — 400 mossa non valida, 404 partita inesistente, 409 partita già finita |
| `GET`  | `/api/leaderboard?limit=10` | classifica |
| `GET`  | `/api/games/{id}/hint` | bonus, oggi 501 |
| `GET`  | `/health` | `{ "status": "ok" }` |

### `GET /api/leaderboard`

```jsonc
[
  {
    "rank": 1,
    "player": "Ada",
    "game_id": "a1b2c3d4e5f6",
    "moves": 84,
    "duration_ms": 61000,
    "finished_at": "2026-09-07T10:01:01Z"
  }
]
```

Ordinamento: meno mosse prima; a parità di mosse, durata più breve prima.

### Prova al volo

```bash
ID=$(curl -s -X POST localhost:8000/api/games \
      -H 'content-type: application/json' \
      -d '{"player":"Ada"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')

curl -s localhost:8000/api/games/$ID | python3 -m json.tool
curl -s -X POST localhost:8000/api/games/$ID/moves \
      -H 'content-type: application/json' -d '{"tile":9}' | python3 -m json.tool
curl -s localhost:8000/api/leaderboard | python3 -m json.tool
```

---

## Parte 2 — Frontend

Tutta la specifica è in **[`frontend/README.md`](frontend/README.md)**: cosa deve fare,
quali schermate, cosa viene valutato. Il codice lo scrivi tu da zero con
`npx create-next-app@latest`.

---

## Come viene valutata la prova

| Peso | Cosa guardiamo |
|------|----------------|
| ●●● | **Correttezza**: i 16 test passano, le partite generate sono davvero risolvibili, la classifica ordina come deve. |
| ●●● | **Il gioco funziona**: si apre il browser, si gioca una partita dall'inizio alla fine e si finisce in classifica. |
| ●● | **Leggibilità**: nomi sensati, funzioni corte, niente codice morto. Preferiamo una soluzione semplice a una furba. |
| ●● | **Gestione degli errori**: mossa non valida, partita inesistente, backend spento. Il frontend non deve rompersi. |
| ● | Test aggiunti da te, cura dell'interfaccia, accessibilità (tastiera). |

Non valutiamo: la grafica "bella", l'uso di librerie particolari, le performance.

## Domande

Rispondi in `SOLUZIONE.md`, poche righe a domanda: non cerchiamo la definizione da manuale,
vogliamo capire come ragioni. Se a una non sai rispondere scrivilo, vale più di una risposta
inventata.

**Sul codice che hai scritto**

1. Che strada hai scelto per `generate_board()` — scarta-e-riprova oppure mosse casuali a
   partire dalla configurazione vinta? Perché quella e non l'altra?
2. Perché metà delle disposizioni possibili della board non è risolvibile? Spiegalo come lo
   spiegheresti a un collega, senza formule.
3. Come hai trovato il bug del TODO(1)? Il test ti ha detto *che* qualcosa non andava:
   raccontaci i passaggi da lì alla riga sbagliata.
4. `apply_move()` restituisce una nuova board invece di modificare quella ricevuta.
   Che differenza fa? C'è un test che se ne accorge: quale?

**Sulle scelte di progetto**

5. La classifica ordina per mosse e poi per tempo. Se dovessi invece premiare "chi ha
   giocato meglio", che criterio useresti e cosa cambieresti nel codice?
6. Oggi le partite stanno in un dizionario in memoria. Cosa si rompe se il backend gira su
   due processi dietro un load balancer? E qual è il cambiamento più piccolo che lo sistema?
7. Il frontend non calcola le mosse valide: le chiede al backend a ogni click. Quali sono i
   vantaggi e qual è il prezzo che si paga? In che caso sceglieresti il contrario?
8. Un giocatore potrebbe barare con questa API? Come, e cosa aggiungeresti per impedirglielo?

**Per chiudere**

9. Cosa hai lasciato indietro e cosa faresti con altre due ore?
10. C'è qualcosa nella traccia che ti è sembrato sbagliato o poco chiaro? Dillo pure: fa parte
    della prova.

---

## Consegna

1. Fai un fork / una copia della repo con la tua soluzione (mantieni la history dei commit,
   ci interessa più il percorso del singolo commit finale).
2. Aggiungi un file `SOLUZIONE.md` con:
   - come far partire tutto, se hai cambiato qualcosa nei comandi rispetto a questo README;
   - le risposte alle dieci domande qui sopra.
3. Mandaci il link.

Se qualcosa nella traccia non è chiaro, scrivici: saper fare la domanda giusta conta,
restare bloccati in silenzio no.
