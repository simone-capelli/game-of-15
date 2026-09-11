"""Test aggiunti per `random_walk()` e `generate_board()` (TODO 3).

I test esistenti passano sempre un seed: qui si copre anche il percorso di
produzione (`seed=None`) e il contratto del cammino casuale su cui poggia
la garanzia "risolvibile per costruzione".
"""

import random

from app import puzzle

GOAL = list(puzzle.GOAL)


def test_generate_board_senza_seed():
    """E' il caso reale: create_game chiama generate_board(None)."""
    for _ in range(20):
        board = puzzle.generate_board()
        puzzle.validate_board(board)
        assert puzzle.is_solvable(board)
        assert not puzzle.is_solved(board)


def test_random_walk_fa_solo_mosse_legali():
    """Ogni board del cammino si ottiene dalla precedente con UNA mossa legale:
    e' questo che rende la board finale risolvibile per costruzione."""
    walk = puzzle.random_walk(random.Random(3), steps=200)
    previous = GOAL
    for board in walk:
        moved = [t for t in board if board.index(t) != previous.index(t) and t != 0]
        assert len(moved) == 1, f"da {previous} a {board} non e' una mossa sola"
        assert moved[0] in puzzle.movable_tiles(previous)
        previous = board


def test_random_walk_non_torna_sui_suoi_passi():
    """Due passi dopo non si e' mai sulla stessa board: la tessera appena
    mossa non viene rimessa a posto."""
    walk = [GOAL] + puzzle.random_walk(random.Random(4), steps=200)
    for i in range(2, len(walk)):
        assert walk[i] != walk[i - 2], f"passo {i}: mossa annullata"


def test_random_walk_e_riproducibile():
    a = puzzle.random_walk(random.Random(42), steps=50)
    b = puzzle.random_walk(random.Random(42), steps=50)
    assert a == b
