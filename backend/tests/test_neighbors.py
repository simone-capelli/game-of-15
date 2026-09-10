"""Test aggiunti per `neighbors()` (TODO 1).

Il test originale copre un solo caso (vuoto all'indice 3). Il bug era
geometrico, quindi qui si verifica la geometria in modo sistematico:
tutte le celle, non un esempio.
"""

import pytest

from app import puzzle

SIZE, CELLS = puzzle.SIZE, puzzle.CELLS


def _row(i: int) -> int:
    return i // SIZE


def _col(i: int) -> int:
    return i % SIZE


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, [1, 4]),           # angolo alto-sinistra
        (3, [2, 7]),           # angolo alto-destra: NON 4
        (12, [8, 13]),         # angolo basso-sinistra: NON 11
        (15, [11, 14]),        # angolo basso-destra
        (4, [0, 5, 8]),        # bordo sinistro: NON 3
        (7, [3, 6, 11]),       # bordo destro: NON 8
        (5, [1, 4, 6, 9]),     # interno
    ],
)
def test_neighbors_casi_noti(index, expected):
    assert sorted(puzzle.neighbors(index)) == expected


def test_neighbors_conta_2_3_o_4():
    """Angoli: 2 vicini, bordi: 3, interno: 4 (la docstring di movable_tiles
    promette 'da 2 a 4')."""
    for i in range(CELLS):
        on_edge = _row(i) in (0, SIZE - 1)
        on_side = _col(i) in (0, SIZE - 1)
        expected = 4 - on_edge - on_side
        assert len(list(puzzle.neighbors(i))) == expected, f"indice {i}"


def test_neighbors_stessa_riga_o_stessa_colonna():
    """Un vicino condivide la riga (passo orizzontale) o la colonna
    (passo verticale): mai entrambe diverse."""
    for i in range(CELLS):
        for j in puzzle.neighbors(i):
            assert _row(i) == _row(j) or _col(i) == _col(j), f"{i} -> {j}"


def test_neighbors_e_simmetrica():
    """Se j e' vicino di i, allora i e' vicino di j."""
    for i in range(CELLS):
        for j in puzzle.neighbors(i):
            assert i in set(puzzle.neighbors(j)), f"{i} vede {j} ma non viceversa"
