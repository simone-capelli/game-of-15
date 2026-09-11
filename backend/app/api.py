"""Endpoint HTTP. Prefisso comune: /api"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from . import puzzle, store
from .models import Game, LeaderboardEntry, MoveRequest, NewGameRequest

router = APIRouter(prefix="/api", tags=["gioco del 15"])


def _with_movable(game: Game) -> Game:
    """Aggiunge alla risposta l'elenco delle tessere cliccabili."""
    playable = not game.solved and game.paused_at is None
    game.movable = puzzle.movable_tiles(game.board) if playable else []
    return game


def _get_open_game(game_id: str) -> Game:
    """La partita se esiste ed e' ancora in corso: 404 o 409 altrimenti."""
    game = store.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="partita non trovata")
    if game.solved:
        raise HTTPException(status_code=409, detail="partita gia' conclusa")
    return game


def _ms_between(start: datetime, end: datetime) -> int:
    return int((end - start).total_seconds() * 1000)


@router.post("/games", response_model=Game, status_code=201)
def create_game(payload: NewGameRequest) -> Game:
    """Crea una nuova partita e la salva in memoria."""
    board = puzzle.generate_board(payload.seed)
    game = Game(
        id=store.new_id(),
        player=payload.player.strip(),
        board=board,
        created_at=store.now(),
    )
    store.save(game)
    return _with_movable(game)


@router.get("/games", response_model=list[Game])
def list_games() -> list[Game]:
    """Tutte le partite in memoria, dalla piu' recente."""
    games = sorted(store.all_games(), key=lambda g: g.created_at, reverse=True)
    return [_with_movable(g) for g in games]


@router.get("/games/{game_id}", response_model=Game)
def get_game(game_id: str) -> Game:
    game = store.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="partita non trovata")
    return _with_movable(game)


@router.post("/games/{game_id}/moves", response_model=Game)
def make_move(game_id: str, payload: MoveRequest) -> Game:
    """Muove una tessera e aggiorna lo stato della partita."""
    game = _get_open_game(game_id)
    if game.paused_at is not None:
        raise HTTPException(status_code=409, detail="partita in pausa: riprendi prima di muovere")

    try:
        game.board = puzzle.apply_move(game.board, payload.tile)
    except puzzle.InvalidMove as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    game.moves += 1
    if puzzle.is_solved(game.board):
        game.solved = True
        game.finished_at = store.now()
        game.duration_ms = _ms_between(game.created_at, game.finished_at) - game.paused_ms

    store.save(game)
    return _with_movable(game)


@router.post("/games/{game_id}/pause", response_model=Game)
def pause_game(game_id: str) -> Game:
    """Ferma il tempo. Idempotente: mettere in pausa una partita gia' in pausa non cambia nulla."""
    game = _get_open_game(game_id)
    if game.paused_at is None:
        game.paused_at = store.now()
    store.save(game)
    return _with_movable(game)


@router.post("/games/{game_id}/resume", response_model=Game)
def resume_game(game_id: str) -> Game:
    """Riprende il tempo, scontando la pausa appena finita. Idempotente."""
    game = _get_open_game(game_id)
    if game.paused_at is not None:
        game.paused_ms += _ms_between(game.paused_at, store.now())
        game.paused_at = None
    store.save(game)
    return _with_movable(game)


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def leaderboard(limit: int = Query(default=10, ge=1, le=100)) -> list[LeaderboardEntry]:
    """Classifica delle partite completate: meno mosse prima, a parita' di
    mosse la durata piu' breve."""
    finished = [g for g in store.all_games() if g.solved]
    ranking = sorted(finished, key=lambda g: (g.moves, g.duration_ms))[:limit]
    return [
        LeaderboardEntry(
            rank=i + 1,
            player=g.player,
            game_id=g.id,
            moves=g.moves,
            duration_ms=g.duration_ms,
            finished_at=g.finished_at,
        )
        for i, g in enumerate(ranking)
    ]


@router.get("/games/{game_id}/hint")
def hint(game_id: str) -> dict:
    """BONUS facoltativo: suggerisce la prossima mossa."""
    game = store.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="partita non trovata")
    try:
        solution = puzzle.solve(game.board)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail="bonus non implementato") from exc
    return {"next": solution[0] if solution else None, "solution": solution}
