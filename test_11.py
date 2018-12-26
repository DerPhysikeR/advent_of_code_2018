#!/usr/bin/env python3
"""
2018-12-26 11:56:48
@author: Paul Reiter
"""
import pytest
from day_11 import (Point, grid_generator, get_digit, power_level, Grid,
                    max_square_sum)


def test_grid_generator():
    grid = grid_generator(Point(1, 2), Point(2, 4))
    reference = [Point(1, 2), Point(2, 2), Point(1, 3), Point(2, 3),
                 Point(1, 4), Point(2, 4)]
    assert all(gr == ref for gr, ref in zip(grid, reference))


@pytest.mark.parametrize('number, digit, reference', [
    (1234, 2, 2),
    (34, 2, 0),
])
def test_get_digit(number, digit, reference):
    assert get_digit(number, digit) == reference


@pytest.mark.parametrize('point, serial_number, reference', [
    (Point(3, 5), 8, 4),
    (Point(122, 79), 57, -5),
    (Point(217, 196), 39, 0),
    (Point(101, 153), 71, 4),
])
def test_power_level(point, serial_number, reference):
    assert power_level(point, serial_number) == reference


@pytest.mark.parametrize('grid, reference', [
    (Grid(Point(32, 44), Point(36, 48), 18),
     ('-2  -4   4   4   4\n'
      '-4   4   4   4  -5\n'
      ' 4   3   3   4  -4\n'
      ' 1   1   2   4  -3\n'
      '-1   0   2  -5  -2')),
    (Grid(Point(20, 60), Point(24, 64), 42),
     ('-3   4   2   2   2\n'
      '-4   4   3   3   4\n'
      '-5   3   3   4  -4\n'
      ' 4   3   3   4  -3\n'
      ' 3   3   3  -5  -1')),
])
def test_grid_str(grid, reference):
    assert str(grid) == reference


@pytest.mark.parametrize('grid, top_left_ref, total_power_ref', [
    (Grid(Point(32, 44), Point(36, 48), 18), Point(33, 45), 29),
    (Grid(Point(20, 60), Point(24, 64), 42), Point(21, 61), 30),
])
def test_max_square_sum(grid, top_left_ref, total_power_ref):
    top_left, total_power = max_square_sum(grid)
    assert top_left == top_left_ref
    assert total_power == total_power_ref
