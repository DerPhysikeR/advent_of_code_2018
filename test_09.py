#!/usr/bin/env python3
"""
2018-12-25 16:33:32
@author: Paul Reiter
"""
import pytest
from itertools import cycle
from day_09 import Marble, Circle, Player, game


@pytest.fixture
def test_circle():
    circle = Circle()
    marble1, marble2, marble3 = Marble(1), Marble(2), Marble(3)
    circle.marbles = set((marble1, marble2, marble3))
    marble1.ccw, marble1.cw = marble3, marble2
    marble2.ccw, marble2.cw = marble1, marble3
    marble3.ccw, marble3.cw = marble2, marble1
    circle.current = marble1
    return circle


def test_circle_getitem(test_circle):
    assert test_circle[0] == 1
    assert test_circle[1] == 2
    assert test_circle[2] == 3
    assert test_circle[3] == 1
    assert test_circle[-1] == 3
    assert test_circle[-2] == 2
    assert test_circle[-3] == 1


def test_circle_append_at_end(test_circle):
    test_circle.append(4, -1)
    assert test_circle[-2] == 3
    assert test_circle[-1] == 4
    assert test_circle[0] == 1


def test_circle_append_at_beginning(test_circle):
    test_circle.append(4)
    assert test_circle[0] == 1
    assert test_circle[1] == 4
    assert test_circle[2] == 2


def test_circle_iter(test_circle):
    for circ, ref in zip(test_circle, (1, 2, 3)):
        assert circ == ref


def test_circle_from_iterable():
    start_tuple = (1, 2, 3, 4, 5)
    end_tuple = tuple(Circle.from_iterable(start_tuple))
    assert start_tuple == end_tuple


def test_circle_pop(test_circle):
    value = test_circle.pop(1)
    assert value == 2
    assert tuple(test_circle) == (1, 3)


@pytest.mark.parametrize('n_players, max_marble, max_score', [
    (9, 25, 32),
    (10, 1618, 8317),
    (13, 7999, 146373),
    (17, 1104, 2764),
    (21, 6111, 54718),
    (30, 5807, 37305),
])
def test_game(n_players, max_marble, max_score):
    result = game(n_players, max_marble)
    assert max(player.score for player in result) == max_score
