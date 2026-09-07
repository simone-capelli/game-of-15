# Backend — Python / FastAPI

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000   # http://localhost:8000/docs
pytest -v                                   # 8 verdi, 8 rossi: i rossi sono la traccia
```

I sei punti da completare sono marcati `TODO(1)`…`TODO(6)` nel codice e descritti in
tabella nel [README della root](../README.md). Le partite stanno in memoria
(`app/store.py`): niente database, è voluto.

## Mappa dei file

| File | Stato |
|------|-------|
| `app/main.py` | pronto — app FastAPI, CORS verso `localhost:3000`, `/health` |
| `app/models.py` | pronto — schemi Pydantic, sono il contratto con il frontend |
| `app/store.py` | pronto — dizionario in memoria con lock |
| `app/puzzle.py` | **TODO(1) bug in `neighbors`, TODO(2) `is_solvable`, TODO(3) `generate_board`** |
| `app/api.py` | **TODO(4) mosse dopo la fine, TODO(5) chiusura partita, TODO(6) classifica** |
| `tests/` | pronto — non modificare i test esistenti, aggiungerne è benvenuto |

## Come è fatta la board

Lista piatta di 16 interi letta per righe, `0` = casella vuota:

```
[ 1,  2,  3,  4]
[ 5,  6,  7,  8]     board = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
[ 9, 10, 11, 12]
[13, 14, 15,  0]     <- configurazione vinta (puzzle.GOAL)
```

`puzzle.to_grid(board)` la trasforma in una matrice 4x4, comodo per stampare in debug.
