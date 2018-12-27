#!/usr/bin/env python3
"""
2018-12-27 18:02:04
@author: Paul Reiter
"""
import pytest
from day_12 import parse_rule, Garden


TEST_STRING = ('initial state: #..#.#..##......###...###\n'
               '\n'
               '...## => #\n'
               '..#.. => #\n'
               '.#... => #\n'
               '.#.#. => #\n'
               '.#.## => #\n'
               '.##.. => #\n'
               '.#### => #\n'
               '#.#.# => #\n'
               '#.### => #\n'
               '##.#. => #\n'
               '##.## => #\n'
               '###.. => #\n'
               '###.# => #\n'
               '####. => #\n')


@pytest.mark.parametrize('rule_string, rule_ref, result_ref', [
    ('...## => #\n', (False, False, False, True, True), True),
    ('..### => .\n', (False, False, True, True, True), False),
])
def test_parse_rule(rule_string, rule_ref, result_ref):
    rule, result = parse_rule(rule_string)
    assert rule == rule_ref
    assert result == result_ref


def test_garden_init():
    garden = Garden.from_lines(TEST_STRING.split('\n'))
    assert garden.plants == set((0, 3, 5, 8, 9, 16, 17, 18, 22, 23, 24))
    assert garden.rules[(False, False, False, True, True)] is True
    assert garden.rules[(True, True, True, True, False)] is True


def test_garden_str():
    garden = Garden.from_lines(TEST_STRING.split('\n'))
    assert str(garden) == '#..#.#..##......###...###'


def test_garden_evolve():
    garden = Garden.from_lines(TEST_STRING.split('\n'))
    for _ in range(20):
        garden.evolve()
    assert garden.value() == 325
