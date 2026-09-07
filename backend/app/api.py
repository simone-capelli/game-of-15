"""Endpoint HTTP. Prefisso comune: /api"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from . import puzzle, store
from .models import Game, LeaderboardEntry, MoveRequest, NewGameRequest

router = APIRouter(prefix="/api", tags=["gioco del 15"])


def _with_movable(game: Game) -> Game:
    """Aggiunge alla risposta l'elenco delle tessere cliccabili."""
    game.movable = [] if game.solved else puzzle.movable_tiles(game.board)
    return game


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
    game = store.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="partita non trovata")

    # TODO(4): se la partita e' gia' finita (game.solved) la mossa va rifiutata
    # con HTTP 409 e un messaggio chiaro. Adesso invece si continua a giocare
    # su una partita conclusa e il contatore delle mosse va avanti.

    try:
        game.board = puzzle.apply_move(game.board, payload.tile)
    except puzzle.InvalidMove as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    game.moves += 1

    # TODO(5): quando la board e' risolta bisogna chiudere la partita:
    #   - game.solved = True
    #   - game.finished_at = store.now()
    #   - game.duration_ms = millisecondi tra created_at e finished_at (int)
    # Solo le partite chiuse cosi' finiscono in classifica.

    store.save(game)
    return _with_movable(game)


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def leaderboard(limit: int = Query(default=10, ge=1, le=100)) -> list[LeaderboardEntry]:
    """Classifica delle partite completate.

    TODO(6): questa versione e' sbagliata in tre punti:
      - include anche le partite non ancora finite;
      - ordina solo per numero di mosse, mentre a parita' di mosse deve
        vincere chi ci ha messo meno tempo (duration_ms piu' basso);
      - ignora il parametro `limit`.
    """
    games = sorted(store.all_games(), key=lambda g: g.moves)
    return [
        LeaderboardEntry(
            rank=i + 1,
            player=g.player,
            game_id=g.id,
            moves=g.moves,
            duration_ms=g.duration_ms or 0,
            finished_at=g.finished_at or g.created_at,
        )
        for i, g in enumerate(games)
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
