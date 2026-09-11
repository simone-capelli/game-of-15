"""Test aggiunti per la classifica (TODO 6).

Il test originale copre il caso "tre finite + una in corso" con limit=2.
Qui i bordi: nessuna partita, limit oltre il numero di partite, e il rank
che deve ripartire da 1 anche quando la classifica e' tagliata.
"""

from datetime import timedelta

from app import puzzle, store
from app.models import Game

GOAL = list(puzzle.GOAL)


def _finita(client, player: str, moves: int, secondi: int) -> None:
    """Una partita chiusa passando dall'endpoint, come succede davvero."""
    game = store.save(Game(
        id=store.new_id(), player=player, board=puzzle.apply_move(GOAL, 15),
        moves=moves - 1, created_at=store.now() - timedelta(seconds=secondi),
    ))
    client.post(f"/api/games/{game.id}/moves", json={"tile": 15})


def test_classifica_vuota_senza_partite_finite(client):
    client.post("/api/games", json={"player": "Ada"})  # in corso, non conta
    assert client.get("/api/leaderboard").json() == []


def test_limit_oltre_le_partite_disponibili(client):
    _finita(client, "Ada", moves=10, secondi=5)
    assert len(client.get("/api/leaderboard?limit=50").json()) == 1


def test_rank_progressivo_anche_con_limit(client):
    for i, player in enumerate(("A", "B", "C", "D")):
        _finita(client, player, moves=10 + i, secondi=5)
    ranks = [e["rank"] for e in client.get("/api/leaderboard?limit=3").json()]
    assert ranks == [1, 2, 3]


def test_a_parita_di_mosse_e_di_tempo_entrambe_in_classifica(client):
    _finita(client, "Ada", moves=10, secondi=5)
    _finita(client, "Bob", moves=10, secondi=5)
    players = {e["player"] for e in client.get("/api/leaderboard").json()}
    assert players == {"Ada", "Bob"}
