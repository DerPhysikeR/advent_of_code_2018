#!/usr/bin/env python3
"""
2018-12-28 17:46:29
@author: Paul Reiter
"""
import pytest
from day_14 import evolve_scores


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
