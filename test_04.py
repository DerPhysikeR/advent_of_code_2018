#!/usr/bin/env python
"""
2018-12-08 10:18:18
@author: Paul Reiter
"""
from datetime import datetime
import pytest
from day_04 import shifts, Line, parse_line, get_guard_id


@pytest.mark.parametrize('line, reference_time, reference_action', [
    ('[1518-04-21 00:57] wakes up',
     datetime(1518, 4, 21, 0, 57), 'wakes up'),
    ('[1518-09-03 00:12] falls asleep',
     datetime(1518, 9, 3, 0, 12), 'falls asleep'),
    ('[1518-04-21 00:04] Guard #3331 begins shift',
     datetime(1518, 4, 21, 0, 4), 'Guard #3331 begins shift'),
])
def test_parse_lines(line, reference_time, reference_action):
    time, action = parse_line(line)
    assert time == reference_time
    assert action == reference_action


def test_shifts():
    test_lines = [Line(None, 'Guard #1069 begins shift'),
                  Line(None, 'falls asleep'),
                  Line(None, 'wakes up'),
                  Line(None, 'Guard #1070 begins shift'),
                  Line(None, 'falls asleep'),
                  Line(None, 'wakes up'),
                  Line(None, 'Guard #1071 begins shift')]
    iterator = shifts(test_lines)
    assert next(iterator) == test_lines[:3]
    assert next(iterator) == test_lines[3:6]
    assert next(iterator) == test_lines[6:]


def test_get_guard_id():
    assert 1069 == get_guard_id('Guard #1069 begins shift')
