"""Test degli endpoint HTTP."""

from datetime import timedelta

from app import puzzle, store
from app.models import Game

GOAL = list(puzzle.GOAL)


def _partita_quasi_finita(player: str = "Ada", moves: int = 10, secondi: int = 30) -> Game:
    """Mette in memoria una partita a una mossa dalla vittoria."""
    board = puzzle.apply_move(GOAL, 15)  # basta rimettere il 15 al suo posto
    game = Game(
        id=store.new_id(),
        player=player,
        board=board,
        moves=moves,
        created_at=store.now() - timedelta(seconds=secondi),
    )
    return store.save(game)


# --- gia' verdi ---------------------------------------------------------

def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_partita_non_trovata(client):
    assert client.get("/api/games/non-esiste").status_code == 404


def test_mossa_non_valida_restituisce_400(client):
    game = _partita_quasi_finita()
    r = client.post(f"/api/games/{game.id}/moves", json={"tile": 1})
    assert r.status_code == 400


# --- TODO(3): dipende da generate_board ---------------------------------

def test_crea_partita_e_la_ritrova_in_memoria(client):
    r = client.post("/api/games", json={"player": "Ada", "seed": 7})
    assert r.status_code == 201
    body = r.json()
    assert body["moves"] == 0 and body["solved"] is False
    assert puzzle.is_solvable(body["board"]), "la partita servita deve essere risolvibile"
    assert body["movable"], "il frontend deve sapere quali tessere sono cliccabili"

    stessa = client.get(f"/api/games/{body['id']}").json()
    assert stessa["board"] == body["board"]


# --- TODO(5): chiusura della partita ------------------------------------

def test_la_partita_si_chiude_quando_la_board_e_risolta(client):
    game = _partita_quasi_finita(moves=10, secondi=30)
    body = client.post(f"/api/games/{game.id}/moves", json={"tile": 15}).json()

    assert body["board"] == GOAL
    assert body["solved"] is True
    assert body["moves"] == 11
    assert body["finished_at"] is not None
    assert 29_000 <= body["duration_ms"] <= 31_000


# --- TODO(4): niente mosse dopo la fine ---------------------------------

def test_niente_mosse_su_una_partita_finita(client):
    game = _partita_quasi_finita()
    client.post(f"/api/games/{game.id}/moves", json={"tile": 15})
    r = client.post(f"/api/games/{game.id}/moves", json={"tile": 15})
    assert r.status_code == 409


# --- TODO(6): classifica -------------------------------------------------

def test_classifica_solo_partite_finite_e_ordinata(client):
    # tre partite completate + una ancora in corso
    lenta = _partita_quasi_finita("Lenta", moves=20, secondi=60)
    veloce = _partita_quasi_finita("Veloce", moves=20, secondi=10)
    campione = _partita_quasi_finita("Campione", moves=5, secondi=90)
    in_corso = _partita_quasi_finita("InCorso", moves=1, secondi=5)

    for g in (lenta, veloce, campione):
        client.post(f"/api/games/{g.id}/moves", json={"tile": 15})

    classifica = client.get("/api/leaderboard").json()
    assert [e["player"] for e in classifica] == ["Campione", "Veloce", "Lenta"]
    assert [e["rank"] for e in classifica] == [1, 2, 3]
    assert in_corso.player not in [e["player"] for e in classifica]

    assert len(client.get("/api/leaderboard?limit=2").json()) == 2
