"""Test aggiunti per make_move (TODO 4 e 5).

I test originali controllano il codice HTTP del rifiuto; qui si controlla
che un rifiuto non modifichi la partita: una guardia che scatta dopo aver
gia' toccato lo stato non e' una guardia.
"""

from datetime import timedelta

from app import puzzle, store
from app.models import Game

GOAL = list(puzzle.GOAL)


def _partita(board: list[int], moves: int = 0, fa: timedelta = timedelta()) -> Game:
    return store.save(Game(id=store.new_id(), player="Ada", board=board, moves=moves, created_at=store.now() - fa))


def test_mossa_rifiutata_non_cambia_la_partita(client):
    game = _partita(puzzle.apply_move(GOAL, 15), moves=3)
    client.post(f"/api/games/{game.id}/moves", json={"tile": 1})  # 400

    dopo = client.get(f"/api/games/{game.id}").json()
    assert dopo["moves"] == 3
    assert dopo["board"] == game.board


def test_partita_chiusa_resta_come_al_momento_della_vittoria(client):
    game = _partita(puzzle.apply_move(GOAL, 15), moves=3)
    vinta = client.post(f"/api/games/{game.id}/moves", json={"tile": 15}).json()
    r = client.post(f"/api/games/{game.id}/moves", json={"tile": 15})  # 409

    assert r.status_code == 409
    dopo = client.get(f"/api/games/{game.id}").json()
    assert dopo["moves"] == 4
    assert dopo["finished_at"] == vinta["finished_at"]
    assert dopo["duration_ms"] == vinta["duration_ms"]
    assert dopo["movable"] == [], "su una partita chiusa non c'e' niente da cliccare"


def test_duration_ms_tiene_i_millisecondi(client):
    """Partita da 1.5 s: `timedelta.seconds` darebbe 1000, il valore giusto e' ~1500."""
    game = _partita(puzzle.apply_move(GOAL, 15), fa=timedelta(milliseconds=1500))
    body = client.post(f"/api/games/{game.id}/moves", json={"tile": 15}).json()
    assert isinstance(body["duration_ms"], int)
    assert 1_400 <= body["duration_ms"] <= 1_600
