"""Logica del gioco del 15.

La board e' una lista di 16 interi: i valori 1..15 sono le tessere,
0 e' la casella vuota. L'indice 0 e' in alto a sinistra, il 15 in basso a destra.

    [ 1,  2,  3,  4]
    [ 5,  6,  7,  8]
    [ 9, 10, 11, 12]
    [13, 14, 15,  0]   <- questa e' la configurazione risolta (GOAL)
"""

from __future__ import annotations

import random
from typing import Iterator, Sequence

SIZE = 4
CELLS = SIZE * SIZE
GOAL: tuple[int, ...] = tuple(range(1, CELLS)) + (0,)

Board = list[int]


class InvalidMove(Exception):
    """La tessera richiesta non puo' essere mossa."""


class InvalidBoard(Exception):
    """La board non contiene esattamente i numeri da 0 a 15."""


# --------------------------------------------------------------------------
# Helper gia' pronti
# --------------------------------------------------------------------------

def validate_board(board: Sequence[int]) -> None:
    if sorted(board) != list(range(CELLS)):
        raise InvalidBoard(f"board non valida: {list(board)!r}")


def blank_index(board: Sequence[int]) -> int:
    """Indice della casella vuota."""
    return list(board).index(0)


def is_solved(board: Sequence[int]) -> bool:
    return tuple(board) == GOAL


def to_grid(board: Sequence[int]) -> list[list[int]]:
    """Comodo per stampare/debuggare: da lista piatta a matrice 4x4."""
    return [list(board[r * SIZE:(r + 1) * SIZE]) for r in range(SIZE)]


def neighbors(index: int) -> Iterator[int]:
    """Indici adiacenti (sopra, sotto, sinistra, destra) a `index`.

    La board e' una lista piatta: un passo verticale (+-SIZE) resta nella
    stessa colonna e puo' solo uscire dalla lista, quindi basta il controllo
    sui limiti. Un passo orizzontale (+-1) invece, dal bordo di una riga,
    "scavalca" nella riga accanto restando dentro la lista: va escluso
    esplicitamente.
    """
    column = index % SIZE
    for delta in (-SIZE, -1, 1, SIZE):
        if delta == -1 and column == 0:
            continue  # bordo sinistro: a sinistra non c'e' niente
        if delta == 1 and column == SIZE - 1:
            continue  # bordo destro: a destra non c'e' niente
        candidate = index + delta
        if 0 <= candidate < CELLS:
            yield candidate


def movable_tiles(board: Sequence[int]) -> list[int]:
    """Tessere che in questo momento possono essere mosse (da 2 a 4)."""
    blank = blank_index(board)
    return sorted(board[i] for i in neighbors(blank))


def apply_move(board: Sequence[int], tile: int) -> Board:
    """Sposta `tile` nella casella vuota e restituisce una NUOVA board.

    Solleva InvalidMove se la tessera non esiste o non e' adiacente al vuoto.
    """
    validate_board(board)
    new_board = list(board)
    if tile not in new_board or tile == 0:
        raise InvalidMove(f"la tessera {tile} non esiste")

    blank = blank_index(new_board)
    position = new_board.index(tile)
    if position not in set(neighbors(blank)):
        raise InvalidMove(f"la tessera {tile} non e' adiacente alla casella vuota")

    new_board[blank], new_board[position] = new_board[position], new_board[blank]
    return new_board


def _inversions(board: Sequence[int]) -> int:
    """Coppie di tessere (vuoto escluso) in cui quella che viene prima
    nell'ordine di lettura e' piu' grande di quella che viene dopo."""
    tiles = [t for t in board if t != 0]
    return sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )


def _blank_row_from_bottom(board: Sequence[int]) -> int:
    """Riga della casella vuota contando dal basso, da 1 (ultima) a SIZE (prima)."""
    return SIZE - blank_index(board) // SIZE


def is_solvable(board: Sequence[int]) -> bool:
    """True se la board puo' essere portata alla configurazione GOAL.

    La parita' di `inversioni + riga del vuoto dal basso` non cambia mai con
    una mossa legale: una mossa orizzontale non tocca nessuno dei due numeri,
    una verticale fa scavalcare alla tessera SIZE-1 = 3 tessere (variazione
    dispari delle inversioni) e sposta il vuoto di una riga (altra variazione
    dispari), e le due si compensano. GOAL ha somma 0 + 1 = 1, dispari:
    quindi solo le board a somma dispari possono raggiungerlo.

    Vale per griglie di lato pari: su un 3x3 la tessera scavalcherebbe 2
    tessere e basterebbero le inversioni da sole.
    """
    return (_inversions(board) + _blank_row_from_bottom(board)) % 2 == 1


# Mosse casuali per mescolare una nuova partita. La soluzione ottima di una
# board 4x4 non supera mai le 80 mosse: un cammino di 100 passi senza
# ritorni immediati basta a portare la board lontano da GOAL.
SHUFFLE_MOVES = 100


def random_walk(rng: random.Random, steps: int, start: Sequence[int] = GOAL) -> list[Board]:
    """Le board attraversate facendo `steps` mosse legali casuali da `start`.

    Ogni mossa viene scelta con `rng` tra le tessere muovibili, escludendo
    quella appena mossa: rimetterla a posto annullerebbe il passo precedente.
    Tutta la casualita' passa da `rng`, cosi' a parita' di seed il cammino e'
    identico.
    """
    board = list(start)
    last_tile: int | None = None
    visited: list[Board] = []
    for _ in range(steps):
        candidates = [t for t in movable_tiles(board) if t != last_tile]
        last_tile = rng.choice(candidates)
        board = apply_move(board, last_tile)
        visited.append(board)
    return visited


def generate_board(seed: int | None = None) -> Board:
    """Genera la board iniziale di una nuova partita.

    Parte da GOAL e applica SHUFFLE_MOVES mosse legali casuali: una board
    raggiunta cosi' e' risolvibile per costruzione (basta rifare le mosse al
    contrario), senza dipendere da `is_solvable`. Con lo stesso `seed` esce
    sempre la stessa board.
    """
    rng = random.Random(seed)
    board = random_walk(rng, SHUFFLE_MOVES)[-1]
    while is_solved(board):  # il cammino puo' tornare su GOAL: si riparte
        board = random_walk(rng, SHUFFLE_MOVES, start=board)[-1]
    return board


# --------------------------------------------------------------------------
# BONUS (facoltativo)
# --------------------------------------------------------------------------

def solve(board: Sequence[int]) -> list[int] | None:
    """BONUS: sequenza di tessere da muovere per risolvere la board.

    Non e' richiesto per superare la prova. Se lo fai, un A* con distanza
    di Manhattan come euristica e' piu' che sufficiente.
    """
    raise NotImplementedError("bonus facoltativo")
