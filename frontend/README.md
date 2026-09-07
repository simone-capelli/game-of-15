# Frontend — Next.js

Questa cartella è **volutamente vuota**: il frontend è la seconda metà della prova e lo
scrivi tu. Qui sotto c'è la specifica di cosa deve fare, non come farlo.

Prima di iniziare tieni il backend acceso (`uvicorn app.main:app --reload --port 8000`) e
dai un'occhiata a <http://localhost:8000/docs>: si può provare ogni endpoint dal browser.

---

## Setup

```bash
# dalla root della repo
npx create-next-app@latest frontend --ts --app --eslint
cd frontend
npm run dev        # http://localhost:3000
```

App Router, TypeScript. Per lo stile fai come preferisci (CSS Modules, Tailwind, CSS
plain): non è oggetto di valutazione, purché la griglia si legga.

Metti l'URL del backend in un file `.env.local`, non hardcodato nei componenti:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Il backend accetta già richieste da `localhost:3000` (CORS configurato).

---

## Cosa deve fare l'applicazione

### 1. Home — nuova partita

- Un campo per il nome del giocatore e un bottone "Gioca".
- Il nome è obbligatorio (1–32 caratteri): se manca, niente chiamata al server.
- Al submit si crea la partita (`POST /api/games`) e si va alla schermata di gioco.

### 2. Partita

- Griglia 4x4 con le 15 tessere e la casella vuota, costruita da `board`
  (lista piatta di 16 numeri letta per righe, `0` = vuoto).
- Cliccando una tessera si chiama `POST /api/games/{id}/moves` e si ridisegna la griglia
  con la board che torna dal server. **La logica di gioco sta sul backend: il frontend non
  deve calcolarsi da solo se una mossa è legale né spostare le tessere in locale.**
- Le tessere non muovibili devono essere visibilmente non cliccabili. Il campo `movable`
  della risposta dice quali lo sono adesso: usalo, non ricalcolarlo.
- Sempre a schermo: nome del giocatore, numero di mosse, tempo trascorso dall'inizio.
- Quando `solved` diventa `true`: messaggio di vittoria con mosse e tempo finale, e un
  collegamento alla classifica. La griglia smette di accettare click.
- La partita deve sopravvivere a un refresh della pagina: l'id sta nell'URL
  (es. `/game/[id]`) e lo stato si ricarica con `GET /api/games/{id}`.

### 3. Classifica

- Pagina `/leaderboard` con le prime 10 partite completate da `GET /api/leaderboard?limit=10`.
- Colonne: posizione, giocatore, mosse, tempo (formattato `1:23`, non 83000 ms).
- Se non ha ancora finito nessuno, dillo con una frase, non con una tabella vuota.

### 4. Errori e stati intermedi

Non serve niente di elaborato, ma non deve rompersi:

- backend spento o in errore → messaggio leggibile, non una pagina bianca;
- id di partita inesistente (404) → messaggio + link alla home;
- mossa rifiutata (400) o partita già chiusa (409) → si mostra l'errore e la griglia resta
  su uno stato coerente;
- durante una chiamata in corso non si devono poter accodare dieci mosse a caso.

---

## Tipi (copiali pure)

```ts
export type Game = {
  id: string;
  player: string;
  board: number[];        // 16 numeri, 0 = casella vuota
  moves: number;
  solved: boolean;
  created_at: string;     // ISO 8601
  finished_at: string | null;
  duration_ms: number | null;
  movable: number[];      // tessere cliccabili adesso
};

export type LeaderboardEntry = {
  rank: number;
  player: string;
  game_id: string;
  moves: number;
  duration_ms: number;
  finished_at: string;
};
```

Endpoint disponibili e codici di errore: vedi la sezione "Contratto API" nel README
della root.

---

## Consigli

- Tieni le chiamate HTTP in un unico modulo (`lib/api.ts`) invece che sparse nei componenti.
- Non servono Redux, React Query o librerie di stato: `useState` e `useEffect` bastano.
  Se ne usi una, spiega perché.
- Tre o quattro componenti sono sufficienti: `Board`, `Tile`, `GameStats`, `LeaderboardTable`.
- L'indice `i` della board sta alla riga `Math.floor(i / 4)` e alla colonna `i % 4`.

## Extra, se avanza tempo (facoltativi)

- Muovere le tessere con le frecce della tastiera.
- Una transizione quando la tessera scivola.
- Un bottone "nuova partita" che riparte con lo stesso nome giocatore.

Meglio le quattro schermate richieste fatte bene che sei mezze cose.
