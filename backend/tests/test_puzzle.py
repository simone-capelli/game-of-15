"""Test della logica di gioco.

Alcuni passano gia', altri no: quelli che falliscono sono la traccia della prova.
Esegui `pytest -v` per vedere subito la lista.
"""

import pytest

from app import puzzle

GOAL = list(puzzle.GOAL)


# --- gia' verdi: servono da rete di sicurezza, non toccarli --------------

def test_board_risolta():
    assert puzzle.is_solved(GOAL)
    assert not puzzle.is_solved([0] + GOAL[:-1])


def test_apply_move_scambia_tessera_e_vuoto():
    # dalla board risolta si puo' muovere il 15 (sopra il vuoto e' il 12)
    nuova = puzzle.apply_move(GOAL, 15)
    assert nuova[14] == 0 and nuova[15] == 15
    assert GOAL[14] == 15, "apply_move non deve modificare la board ricevuta"


def test_apply_move_rifiuta_tessera_lontana():
    with pytest.raises(puzzle.InvalidMove):
        puzzle.apply_move(GOAL, 1)


# --- TODO(1): bug in neighbors() ----------------------------------------

def test_apply_move_rifiuta_il_salto_di_riga():
    """L'indice 3 (fine riga 1) e l'indice 4 (inizio riga 2) NON sono adiacenti."""
    board = [1, 2, 3, 0,
             5, 6, 7, 4,
             9, 10, 11, 8,
             13, 14, 15, 12]
    # il vuoto e' all'indice 3: si possono muovere solo il 3 (indice 2)
    # e il 4 (indice 7). Il 5 sta all'indice 4, su un'altra riga.
    assert puzzle.movable_tiles(board) == [3, 4]
    with pytest.raises(puzzle.InvalidMove):
        puzzle.apply_move(board, 5)


# --- TODO(2): is_solvable ------------------------------------------------

def test_is_solvable_casi_noti():
    assert puzzle.is_solvable(GOAL) is True

    # scambiare due tessere adiacenti rende la board impossibile
    impossibile = GOAL[:13] + [15, 14, 0]
    assert puzzle.is_solvable(impossibile) is False


def test_is_solvable_dopo_mosse_valide():
    """Qualunque board raggiunta con mosse valide resta risolvibile."""
    board = list(GOAL)
    for tessera in (15, 11, 12, 8, 7, 6):
        board = puzzle.apply_move(board, tessera)
    assert puzzle.is_solvable(board) is True


# --- TODO(3): generate_board --------------------------------------------

def test_generate_board_sempre_risolvibile():
    for seed in range(60):
        board = puzzle.generate_board(seed)
        puzzle.validate_board(board)
        assert puzzle.is_solvable(board), f"board non risolvibile con seed={seed}"
        assert not puzzle.is_solved(board), f"board gia' risolta con seed={seed}"


def test_generate_board_e_riproducibile():
    assert puzzle.generate_board(42) == puzzle.generate_board(42)


def test_generate_board_cambia_con_il_seed():
    boards = {tuple(puzzle.generate_board(seed)) for seed in range(20)}
    assert len(boards) > 15, "il seed deve cambiare davvero la board"
