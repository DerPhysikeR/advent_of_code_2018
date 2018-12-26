#!/usr/bin/env python3
"""
2018-12-26 09:34:14
@author: Paul Reiter
"""
import numpy as np
from day_10 import parse_line, StarImage, bounding_box, find_minimal_image


def test_parse_line():
    test_line = 'position=< 9,  1> velocity=< 0,  2>'
    assert (9, 1, 0, 2) == parse_line(test_line)


def test_star_image_from_file():
    starimage = StarImage.from_file('test_input_10.txt')
    np.testing.assert_equal(starimage.positions[0], np.array([9, 1]))
    np.testing.assert_equal(starimage.positions[-1], np.array([-3, 6]))
    np.testing.assert_equal(starimage.velocities[0], np.array([0, 2]))
    np.testing.assert_equal(starimage.velocities[-1], np.array([2, -1]))


def test_star_image_evolve():
    positions = np.array([[0, 0], [1, 2]])
    velocities = np.array([[1, 2], [3, 4]])
    starimage = StarImage(positions, velocities)
    starimage.evolve()
    np.testing.assert_equal(starimage.positions, np.array([[1, 2], [4, 6]]))


def test_bounding_box():
    positions = np.array([[0, 0], [2, -1], [3, 2], [4, 1]])
    np.testing.assert_equal(bounding_box(positions),
                            np.array([[0, -1], [4, 2]]))


def test_star_image_size():
    starimage = StarImage([[0, 0], [2, 3]], np.empty((2, 2)))
    assert starimage.size == 6


def test_star_image_str():
    starimage = StarImage([[0, 0], [2, 3]], np.empty((2, 2)))
    assert str(starimage) == '#..\n...\n...\n..#'


def test_find_minimal_image():
    starimage = StarImage.from_file('test_input_10.txt')
    result = find_minimal_image(starimage)
    reference = ('#...#..###\n'
                 '#...#...#.\n'
                 '#...#...#.\n'
                 '#####...#.\n'
                 '#...#...#.\n'
                 '#...#...#.\n'
                 '#...#...#.\n'
                 '#...#..###')
    assert str(result) == reference
