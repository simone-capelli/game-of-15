# Soluzione

## Come far partire tutto

Ho lavorato su Windows 10 con PowerShell: i comandi del README sono per bash e cambiano
solo nell'attivazione del venv.

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
pytest -v
```

Frontend (Next.js 16, App Router, TypeScript, CSS plain), in un secondo terminale:

```powershell
cd frontend
npm install
npm run dev          # http://localhost:3000
```

`NEXT_PUBLIC_API_URL` in `.env.local` è opzionale: se manca, `lib/api.ts` chiama il backend
sullo stesso host della pagina, porta 8000. Così l'app si apre anche da un altro dispositivo
in rete locale (URL "Network" di `npm run dev`), a patto di avviare il backend con
`--host 0.0.0.0`; il CORS ammette le origini di rete locale.

Il frontend ha un tema arcade (font pixel, neon, Pac-Man che passeggia in fondo). Due scelte
che vanno oltre la spec e che segnalo:

- il nome del giocatore è di **tre lettere** stile high score (campo di testo, maiuscole
  automatiche, solo lettere): rientra nell'1–32 richiesto dal backend, e in
  classifica il nome è mostrato come iniziali maiuscole (il nome intero è nel `title`);
- le **frecce da tastiera** muovono la tessera adiacente al vuoto nella direzione premuta:
  il frontend mappa solo "freccia → tessera" e invia la mossa se è tra i `movable` del
  server; la legalità resta decisa dal backend.

Le animazioni decorative rispettano `prefers-reduced-motion`.

### Deploy (facoltativo)

Backend su Render (`render.yaml` alla radice: "New > Blueprint"), con la variabile
`CORS_ORIGINS` impostata al dominio del frontend. Frontend su Vercel con root directory
`frontend` e `NEXT_PUBLIC_API_URL` = URL del servizio Render. Il backend non può stare su
Vercel: le funzioni serverless non condividono la memoria tra richieste, e lo store è in
memoria (vedi domanda 6).

### Oltre la traccia: la pausa

Ho aggiunto un bottone "Pausa" nella schermata di gioco. Siccome il tempo lo calcola il
server, una pausa solo a schermo avrebbe mostrato un tempo diverso da quello in classifica.
Quindi la pausa è lato backend: `POST /api/games/{id}/pause` e `/resume`, due campi in più
su `Game` (`paused_ms`, `paused_at`) — aggiunti, non modificati — e `duration_ms` che sconta
le pause. In pausa le mosse rispondono 409 e `movable` è vuoto. Test in
`tests/test_pause.py`. È un'estensione: si può rimuovere con un revert del suo commit.

---

## Domande

### Sul codice che ho scritto

**1. `generate_board()`: scarta-e-riprova o mosse casuali da GOAL?**

Mosse casuali da GOAL. Il motivo è che la risolvibilità diventa una garanzia strutturale
invece di un controllo: una board raggiunta con mosse legali si risolve rifacendole al
contrario, punto. Con scarta-e-riprova invece la correttezza dipende da `is_solvable`: se
un giorno qualcuno ci mette un bug, il server inizia a servire partite impossibili e
nessuno se ne accorge.

Non l'ho scelta per il costo di calcolo, che all'inizio mi sembrava l'argomento: `is_solvable`
fa 105 confronti e scarta-e-riprova in media riprova due volte, quindi la strada (a) farebbe
persino meno lavoro di cento mosse. È irrilevante in entrambi i casi.

Il prezzo che pago: il cammino può in teoria tornare su GOAL (c'è una guardia che riparte),
le board non sono distribuite uniformemente tra tutte quelle risolvibili ma "vicine" a GOAL,
e un cammino ingenuo perde circa un passo su tre rimettendo a posto la tessera appena mossa.
Per quest'ultimo punto `random_walk` esclude dalle candidate l'ultima tessera mossa.

Il cammino è una funzione a sé (`puzzle.random_walk`) usata sia da `generate_board` sia dai
test di `is_solvable`: così i test verificano l'invariante esattamente sul meccanismo che
genera le partite, non su una copia.

**2. Perché metà delle disposizioni non è risolvibile?**

All'inizio ho usato il suggerimento della docstring come una regola presa per buona, senza
capirla. Per capirla ho preso una board sulla whiteboard, ho contato le inversioni (8) e la
riga del vuoto dal basso (1), poi ho fatto una mossa legale — il 14 che scende nel vuoto — e
ho ricontato: 7 e 2. La somma era 9 in tutti e due i casi.

Guardando *perché*: nella lettura per righe il 14 ha scavalcato tre tessere (12, 15, 11) e
per ognuna la coppia si è girata, quindi le inversioni cambiano sempre di un numero dispari
in una mossa verticale; nello stesso momento il vuoto cambia riga di uno. Due variazioni
dispari si compensano e la parità della somma resta quella. In una mossa orizzontale non
cambia niente: la tessera si scambia solo con il vuoto, che non conta.

Quindi quella parità è come una moneta che le mosse legali non girano mai. La board risolta
ha la moneta su "dispari", e una board con la moneta su "pari" non può arrivarci con nessuna
sequenza di mosse. Scambiare a mano due tessere adiacenti — cosa che il gioco non permette —
gira la moneta: ogni disposizione ha una gemella con la parità opposta, per questo le
disposizioni si dividono esattamente a metà.

Il "tre tessere scavalcate" vale perché la griglia ha lato pari (4 − 1 = 3). Su un 3x3
sarebbero due, la variazione sarebbe pari, e basterebbero le inversioni da sole: la regola
della docstring non è universale.

**3. Come ho trovato il bug del TODO(1)**

`pytest -v` dava `assert [3, 4, 5] == [3, 4]`: `movable_tiles` restituiva una tessera in
più, il 5. Ho letto il codice a strati, come una matrioska: `movable_tiles` si limita a
tradurre indici in tessere, `blank_index` è un `.index(0)`, quindi l'unico posto con della
logica vera era `neighbors`.

Ho disegnato la griglia 4x4 sulla whiteboard con gli indici da 0 a 15. Il vuoto sta
all'indice 3, fine della prima riga; `+1` dà 4, che nella lista è il numero successivo ma
sulla griglia è l'inizio della seconda riga. Il controllo `0 <= candidate < 16` non se ne
accorge perché 4 è un indice valido: il problema non è uscire dalla lista, è scavalcare il
bordo della riga restando dentro la lista.

Da lì ho cercato una regola valida per ogni cella, non solo per l'esempio: `index % SIZE`
dà la colonna, e dalla colonna 0 non si va a `-1`, dalla colonna 3 non si va a `+1`. I passi
verticali non hanno bisogno di niente perché restano nella stessa colonna: possono solo
uscire dalla lista, e lì il controllo esistente basta.

Per provarlo: il test rosso è verde, i tre test verdi che dipendono da `neighbors` lo sono
rimasti, e ho aggiunto `tests/test_neighbors.py` che controlla tutte e 16 le celle. Ho
verificato che la maggior parte di quei test diventi rossa se rimetto la versione buggata:
un test che non si accorge del bug non serve.

**4. `apply_move()` restituisce una nuova board: che differenza fa?**

Chi la chiama tiene la sua board intatta finché non decide di sostituirla. In `make_move`
questo vuol dire che se la mossa è illegale e `apply_move` solleva `InvalidMove`, la board
salvata non è stata toccata: il 400 non lascia tracce. Se modificasse sul posto, il rifiuto
potrebbe arrivare con la board già cambiata a metà.

Me ne sono accorto anche in `random_walk`: la lista `visited` contiene cento board diverse
solo perché ogni chiamata ne crea una nuova. Con la modifica sul posto sarebbero cento
riferimenti alla stessa lista, tutti uguali all'ultima.

Il test che se ne accorge è `test_apply_move_scambia_tessera_e_vuoto`, alla riga
`assert GOAL[14] == 15, "apply_move non deve modificare la board ricevuta"`: `GOAL` è una
costante condivisa da tutti i test, e se `apply_move` la modificasse i test successivi
partirebbero da una board sbagliata.

### Sulle scelte di progetto

**5. Classifica: premiare "chi ha giocato meglio"**

Il numero di mosse da solo premia chi ha ricevuto una board facile. "Giocare bene" è fare
poche mosse *rispetto al minimo possibile per quella board*: userei il rapporto
`mosse / mosse_ottime`, dove 1.0 è la partita perfetta.

Nel codice: implementare `puzzle.solve()` (il bonus, A* con distanza di Manhattan), calcolare
la lunghezza della soluzione ottima in `create_game` e salvarla in un campo nuovo
`optimal_moves` di `Game`; in `leaderboard` la chiave diventa
`(moves / optimal_moves, duration_ms)`. È un'aggiunta al contratto di `models.py`, non un
cambiamento: i campi esistenti restano uguali. Il prezzo è che A* su una board 4x4 può
essere lento sulle board difficili, e andrebbe misurato prima di farlo a ogni creazione.

**6. Due processi dietro un load balancer**

Ogni processo ha il suo dizionario `_games` in RAM. La partita creata sul processo A non
esiste sul processo B: la mossa successiva, se il bilanciatore la manda a B, prende 404.
La classifica mostra solo le partite del processo che risponde. Il `threading.Lock` non
aiuta: protegge i thread dentro un processo, non due processi.

Il cambiamento più piccolo: spostare il dizionario in qualcosa condiviso tra processi (Redis,
o anche un SQLite su disco) tenendo le stesse quattro funzioni di `store.py`. `api.py` non
cambierebbe di una riga, perché parla con lo store solo tramite `save`/`get`/`all_games`.

C'è anche un problema che esiste già con un processo solo: `store.get` restituisce l'oggetto
vivo, e `make_move` lo modifica fuori dal lock. Due mosse sulla stessa partita arrivate
insieme possono sovrascriversi. Con uno store esterno servirebbe una scrittura atomica
(o un lock per partita).

**7. Il frontend chiede le mosse valide al backend**

Vantaggi: la logica di gioco esiste in un posto solo, quindi non può divergere tra client e
server; il frontend è semplice (mostra quello che riceve); barare spostando tessere in
locale è impossibile, perché lo stato vero è quello del server.

Il prezzo: un giro di rete per ogni click. Con latenza alta ogni mossa si sente, e senza
rete non si gioca. In più il server fa più lavoro.

Sceglierei il contrario se la reattività fosse il requisito principale (mobile, connessione
scarsa) o servisse il gioco offline: il client muove subito le tessere e il server valida a
posteriori, rifiutando la partita se la sequenza di mosse non torna. La logica sarebbe
duplicata, e andrebbe tenuta identica nei due posti.

**8. Si può barare con questa API?**

Sì, in almeno due modi. Il primo: `POST /api/games` accetta `seed` dal client, quindi si può
scegliere una board nota, risolverla offline e rigiocare la soluzione ottima con uno script
in pochi millisecondi: primo posto con mosse minime e tempo quasi zero. Il secondo: anche
senza seed, uno script che chiama `/moves` non ha nessun limite di velocità, e il campo
`player` è un testo libero senza identità.

Cosa aggiungerei: il seed accettato solo in un ambiente di sviluppo, non in produzione; un
token per partita, restituito alla creazione e richiesto a ogni mossa, così solo chi ha
creato la partita può muovere; un limite alla frequenza delle mosse per partita (nessun
umano fa dieci mosse in un secondo). Se si implementa il bonus `hint`, va protetto o
disattivato in classifica: è un aiuto integrato a barare.

### Per chiudere

**9. Cosa ho lasciato indietro**

_(da rivedere alla fine, dopo il frontend)_

Il bonus `solve()`/`hint` non l'ho fatto. La guardia `while is_solved` in `generate_board`
non è esercitata da nessun test: con il no-ritorno servono almeno 12 mosse precise per
tornare su GOAL, e non ho voluto costruire un test artificiale. La race condition tra due
mosse simultanee sulla stessa partita (Q6) esiste e non l'ho sistemata: è fuori dai TODO e
con un processo e un giocatore per partita non si manifesta.

Con altre due ore: A* per `hint` (e con quello anche la classifica per efficienza di Q5), un
lock per partita in `make_move`, e sul frontend le frecce da tastiera.

**10. Qualcosa di sbagliato o poco chiaro nella traccia?**

- La docstring del TODO(1) dice già quali indici sono sbagliati (3 e 4): il bug si trova
  leggendo il commento, e la domanda 3 perde un po' di senso.
- `_with_movable` scrive `game.movable` sull'oggetto salvato in memoria: una `GET` modifica
  lo stato. Innocuo, ma un endpoint di lettura non dovrebbe avere effetti collaterali.
- Il tempo parte da `created_at`, cioè dalla creazione della partita, non dalla prima mossa:
  chi legge la griglia per trenta secondi prima di muovere viene penalizzato.
- Il `seed` accettato dal client è comodo per i test ma è la via più facile per barare (Q8):
  non è chiaro se sia voluto anche in produzione.
- I test originali usano durate tonde (30 s): un `timedelta.seconds` al posto di
  `total_seconds()` li passerebbe tutti perdendo i millisecondi. Ho aggiunto un test da 1,5 s.
- I comandi di avvio sono per bash; su Windows cambia l'attivazione del venv.
