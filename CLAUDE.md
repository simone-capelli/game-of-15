# CLAUDE.md — regole di collaborazione

## Contesto

Prova pratica di assunzione (gioco del 15, backend FastAPI + frontend Next.js).
Consegna: **lunedì 14 settembre 2026**. Traccia completa in [README.md](README.md),
spec frontend in [frontend/README.md](frontend/README.md).

La traccia consente esplicitamente l'uso di agenti AI, ma valuta la capacità del
candidato di **spiegare quello che consegna** (dieci domande in `SOLUZIONE.md`).

## Modalità: mentoring, non ghostwriting

L'obiettivo dichiarato dell'utente è **imparare il processo di ragionamento**, non
ricevere la soluzione. Quindi:

- **Non scrivere il codice di soluzione** dei TODO(1)–(6) né del frontend, a meno
  che l'utente non lo chieda in modo esplicito e diretto per quel punto specifico.
- Spiega il *perché* e il *dove*: invarianti, trade-off, il punto esatto in cui
  guardare. Fai domande che portano l'utente alla riga sbagliata invece di indicarla.
- Se l'utente è bloccato: prima un indizio, poi un indizio più forte, poi — solo se
  lo chiede — la soluzione. Mai saltare direttamente alla fine.
- **Rivedere il codice che l'utente ha scritto è sempre benvenuto**: correttezza,
  naming, casi limite, test mancanti. Questo è il modo principale di essere utili qui.
- Regola di validazione: se l'utente non saprebbe rispondere a "perché così?" in
  colloquio, il lavoro non è finito — anche se i test sono verdi.

Scaffolding non-soluzione (setup, comandi, `.env.local`, config, formattazione di
`SOLUZIONE.md`) può essere scritto direttamente: non è la parte valutata.

## Vincoli della traccia — non violarli

- **Nessun database**: le partite vivono in `app/store.py` in memoria. È voluto.
- **Non cambiare la forma delle risposte** in `app/models.py`: è il contratto col frontend.
- **Non modificare i test esistenti.** Gli 8 verdi devono restare verdi. Aggiungerne è benvenuto.
- Librerie extra solo se servono davvero, e va scritto il perché.
- Il codice `neighbors` / `apply_move` / `is_solvable` è la base di tutto: un bug lì
  si propaga silenziosamente in `generate_board` e nelle API.

## Ambiente (Windows) — la traccia assume Linux/macOS

- Shell: PowerShell. I comandi bash del README vanno tradotti.
- `python3 -m venv .venv && source .venv/bin/activate`
  → `python -m venv .venv` poi `.venv\Scripts\Activate.ps1`
- **Python vive solo nel venv**: `backend\.venv\Scripts\python.exe` (3.13.15). Non c'è un
  `python` globale sul PATH (solo l'alias stub del Microsoft Store), quindi va attivato il
  venv, oppure si invoca direttamente `backend\.venv\Scripts\python.exe -m pytest`.
- Node v20.15.1 e npm 10.7.0 sono presenti: ok per `create-next-app`.
- Le differenze di comandi vanno annotate in `SOLUZIONE.md` (la traccia lo chiede).

## Git

La traccia dice che **interessa il percorso, non il commit finale**: un commit piccolo
per ogni TODO, messaggio che nomina il test che diventa verde. Non schiacciare la history.
