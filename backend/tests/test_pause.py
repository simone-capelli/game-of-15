"""Test della pausa (estensione oltre la traccia).

La pausa esiste perche' il tempo lo calcola il server: un contatore fermato
solo a schermo darebbe in classifica un tempo diverso da quello mostrato.
"""

from datetime import timedelta

from app import puzzle, store
from app.models import Game

GOAL = list(puzzle.GOAL)


def _partita(secondi_fa: int = 30, **extra) -> Game:
    return store.save(Game(
        id=store.new_id(), player="Ada", board=puzzle.apply_move(GOAL, 15),
        created_at=store.now() - timedelta(seconds=secondi_fa), **extra,
    ))


def test_la_pausa_viene_scontata_dalla_durata(client):
    # partita di 30 s, in pausa da 10 s: riprendo e vinco -> 20 s
    game = _partita(secondi_fa=30, paused_at=store.now() - timedelta(seconds=10))
    ripresa = client.post(f"/api/games/{game.id}/resume").json()
    assert 9_900 <= ripresa["paused_ms"] <= 10_100
    assert ripresa["paused_at"] is None

    vinta = client.post(f"/api/games/{game.id}/moves", json={"tile": 15}).json()
    assert 19_000 <= vinta["duration_ms"] <= 21_000


def test_in_pausa_non_si_muove(client):
    game = _partita()
    in_pausa = client.post(f"/api/games/{game.id}/pause").json()
    assert in_pausa["paused_at"] is not None
    assert in_pausa["movable"] == []

    r = client.post(f"/api/games/{game.id}/moves", json={"tile": 15})
    assert r.status_code == 409
    assert client.get(f"/api/games/{game.id}").json()["moves"] == 0


def test_pausa_e_ripresa_sono_idempotenti(client):
    game = _partita()
    prima = client.post(f"/api/games/{game.id}/pause").json()["paused_at"]
    dopo = client.post(f"/api/games/{game.id}/pause").json()["paused_at"]
    assert prima == dopo, "la seconda pausa non deve spostare l'inizio"

    client.post(f"/api/games/{game.id}/resume")
    scontato = client.get(f"/api/games/{game.id}").json()["paused_ms"]
    client.post(f"/api/games/{game.id}/resume")
    assert client.get(f"/api/games/{game.id}").json()["paused_ms"] == scontato


def test_pausa_su_partita_finita_o_inesistente(client):
    game = _partita()
    client.post(f"/api/games/{game.id}/moves", json={"tile": 15})
    assert client.post(f"/api/games/{game.id}/pause").status_code == 409
    assert client.post("/api/games/non-esiste/pause").status_code == 404
