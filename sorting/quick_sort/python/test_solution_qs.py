from .solution_qs import Solution

import pytest


@pytest.fixture(scope="function")
def sol():
    return Solution()


def test_simple_input(sol):
    data = [4, 2, 1, 5, 3, 7, 0, -5]
    expect = [-5, 0, 1, 2, 3, 4, 5, 7]
    sol.sort(data)
    assert expect == data


def test_best_possible_input(sol):
    data = [-5, 0, 1, 2, 3, 4, 5, 7]
    expect = [-5, 0, 1, 2, 3, 4, 5, 7]
    sol.sort(data)
    assert expect == data
