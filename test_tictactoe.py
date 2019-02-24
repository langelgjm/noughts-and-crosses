import numpy as np
import pytest

from tictactoe import is_winning_game


@pytest.mark.parametrize(
    'grid,expected',
    (
        (np.zeros((3, 3)), False),
        (np.triu(np.ones((3, 3)), 1) + np.tril(np.ones((3, 3)) * -1, -1), False),
        (np.ones((3, 3)), True),
        (np.ones((3, 3)) * -1, True),
        (np.eye(3), True),
        (np.eye(3) * -1, True),
        (np.flipud(np.eye(3)), True),
        (np.flipud(np.eye(3)) * -1, True)
    )
)
def test_is_winning_game(grid, expected):
    assert expected == is_winning_game(grid)
