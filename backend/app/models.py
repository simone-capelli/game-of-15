"""Schemi Pydantic: sono anche il contratto verso il frontend."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class NewGameRequest(BaseModel):
    player: str = Field(min_length=1, max_length=32, description="Nome del giocatore")
    seed: int | None = Field(
        default=None, description="Opzionale: rende la board riproducibile"
    )


class MoveRequest(BaseModel):
    tile: int = Field(ge=1, le=15, description="Numero della tessera da muovere")


class Game(BaseModel):
    id: str
    player: str
    board: list[int]
    moves: int = 0
    solved: bool = False
    created_at: datetime
    finished_at: datetime | None = None
    duration_ms: int | None = None

    # pausa: millisecondi gia' scontati dal tempo e, se in pausa adesso, da quando.
    # Campi aggiunti (non modificati) rispetto al contratto originale.
    paused_ms: int = 0
    paused_at: datetime | None = None

    # comodita' per il frontend: quali tessere sono cliccabili adesso
    movable: list[int] = []


class LeaderboardEntry(BaseModel):
    rank: int
    player: str
    game_id: str
    moves: int
    duration_ms: int
    finished_at: datetime
