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


# --------------------------------------------------------------------------
# TODO (2) - da implementare
# --------------------------------------------------------------------------

def is_solvable(board: Sequence[int]) -> bool:
    """True se la board puo' essere portata alla configurazione GOAL.

    TODO(2): implementare. Meta' delle 16! disposizioni possibili NON e'
    risolvibile, quindi serve un controllo prima di consegnare una partita
    a un giocatore.

    Suggerimento (griglia di lato pari, come la nostra 4x4):
      - conta le "inversioni": le coppie di tessere (i < j, vuoto escluso)
        in cui il valore che viene prima e' piu' grande di quello che viene dopo;
      - guarda la riga in cui si trova la casella vuota, contando le righe
        dal basso partendo da 1;
      - la board e' risolvibile quando la somma dei due numeri e' dispari.

    Verifica veloce: la board GOAL ha 0 inversioni, il vuoto e' nella riga 1
    dal basso -> 0 + 1 = 1, dispari -> risolvibile.
    """
    raise NotImplementedError("TODO(2): implementare is_solvable")


# --------------------------------------------------------------------------
# TODO (3) - da correggere
# --------------------------------------------------------------------------

def generate_board(seed: int | None = None) -> Board:
    """Genera la board iniziale di una nuova partita.

    TODO(3): cosi' com'e' scritta questa funzione restituisce una board
    completamente casuale: circa una partita su due e' IMPOSSIBILE da
    risolvere, e ogni tanto esce gia' risolta.

    Deve invece restituire sempre una board risolvibile e mai gia' risolta.
    Due strade possibili (scegli tu, motivala nel README di consegna):
      a) genera a caso e riprova finche' `is_solvable` non dice di si';
      b) parti da GOAL e applica N mosse casuali valide (una board raggiunta
         con mosse valide e' risolvibile per costruzione).

    `seed` serve a rendere la generazione riproducibile nei test:
    con lo stesso seed deve uscire sempre la stessa board.
    """
    rng = random.Random(seed)
    board = list(GOAL)
    rng.shuffle(board)
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
