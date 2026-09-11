"""Test aggiunti per `is_solvable()` (TODO 2).

L'idea dietro la funzione e' un'invariante: le mosse legali non cambiano
mai la risolvibilita', uno scambio a mano di due tessere la ribalta.
Qui si verificano proprio queste due proprieta', piu' due board contate a
mano sulla whiteboard.
"""

import random

from app import puzzle

GOAL = list(puzzle.GOAL)

# Contata a mano: 8 inversioni, vuoto in riga 1 dal basso -> 9, dispari.
BOARD_A_MANO = [1, 2, 3, 4,
                5, 6, 7, 8,
                10, 13, 9, 14,
                12, 15, 11, 0]


def _random_walk(seed: int, steps: int) -> list[list[int]]:
    return puzzle.random_walk(random.Random(seed), steps)


def _swap_two_adjacent_tiles(board: list[int]) -> list[int]:
    """Scambia le prime due tessere adiacenti (nessuna delle due e' il vuoto):
    non e' una mossa legale."""
    swapped = list(board)
    for i in range(len(swapped) - 1):
        if swapped[i] != 0 and swapped[i + 1] != 0:
            swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
            return swapped
    raise AssertionError("impossibile: servono due tessere adiacenti")


def test_board_contata_a_mano():
    assert puzzle.is_solvable(BOARD_A_MANO) is True
    # il 14 scende nel vuoto (mossa verticale): 7 inversioni + riga 2 = 9
    dopo = puzzle.apply_move(BOARD_A_MANO, 14)
    assert puzzle.is_solvable(dopo) is True


def test_le_mosse_legali_non_cambiano_la_risolvibilita():
    for board in _random_walk(seed=0, steps=300):
        assert puzzle.is_solvable(board), board


def test_uno_scambio_a_mano_la_ribalta():
    """Ogni board risolvibile ha una gemella impossibile: per questo meta'
    delle disposizioni non si puo' risolvere."""
    for board in _random_walk(seed=1, steps=100):
        assert puzzle.is_solvable(_swap_two_adjacent_tiles(board)) is False


def test_restituisce_un_bool():
    """`% 2` da solo darebbe un int, e `is True` nei test lo boccerebbe."""
    assert isinstance(puzzle.is_solvable(GOAL), bool)
