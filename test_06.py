#!/usr/bin/env python
"""
2018-12-08 20:26:51
@author: Paul Reiter
"""
from day_06 import (Point, distance, parse_line, bounding_box, box_iter)


def test_distance():
    assert 3 == distance(Point(0, 0), Point(2, 1))


def test_parse_line():
    assert Point(12, 23) == parse_line('12, 23')


def test_bounding_box():
    points = set((Point(1, 4), Point(2, 2), Point(5, 3), Point(1, 6)))
    reference = (Point(1, 2), Point(5, 6))
    assert reference == bounding_box(points)


def test_box_iter():
    reference = [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1),
                 Point(2, 0), Point(2, 1)]
    assert all([ref == point for ref, point
                in zip(reference, box_iter(Point(0, 0), Point(2, 1)))])
