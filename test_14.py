#!/usr/bin/env python3
"""
2018-12-28 17:46:29
@author: Paul Reiter
"""
import pytest
from day_14 import evolve_scores, score_generator, find_pattern


@pytest.mark.parametrize('scores, digits_after, reference', [
    ([3, 7], 9, '5158916779'),
    ([3, 7], 5, '0124515891'),
    ([3, 7], 18, '9251071085'),
    ([3, 7], 2018, '5941429882'),
])
def test_evolve_scores(scores, digits_after, reference):
    elve1, elve2 = 0, 1
    while len(scores) < digits_after+10:
        scores, elve1, elve2 = evolve_scores(scores, elve1, elve2)
    assert ''.join(str(score) for score in
                   scores[digits_after:digits_after+10]) == reference


def test_score_generator():
    reference = [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]
    scores = score_generator([3, 7], 0, 1)
    for i, ((index, score), ref) in enumerate(zip(scores, reference)):
        assert i == index
        assert score == ref


@pytest.mark.parametrize('pattern, index', [
    ((5, 1, 5, 8, 9), 9),
    ((0, 1, 2, 4, 5), 5),
    ((9, 2, 5, 1, 0), 18),
    ((5, 9, 4, 1, 4), 2018),
])
def test_find_pattern(pattern, index):
    assert index == find_pattern(pattern, [3, 7], 0, 1)
