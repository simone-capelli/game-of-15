"""Persistenza in memoria.

Niente database: le partite vivono in un dizionario di processo e spariscono
al riavvio del server. E' voluto, non e' un TODO.
"""

from __future__ import annotations

import threading
import uuid
from datetime import datetime, timezone

from .models import Game

_lock = threading.Lock()
_games: dict[str, Game] = {}


def now() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return uuid.uuid4().hex[:12]


def save(game: Game) -> Game:
    with _lock:
        _games[game.id] = game
    return game


def get(game_id: str) -> Game | None:
    with _lock:
        return _games.get(game_id)


def all_games() -> list[Game]:
    with _lock:
        return list(_games.values())


def reset() -> None:
    """Svuota lo store (usata dai test)."""
    with _lock:
        _games.clear()
