#!/usr/bin/env python
"""
2018-12-06 22:20:09
@author: Paul Reiter
"""
from collections import defaultdict
from itertools import product
from parse import parse


def get_squares(x, y, width, height):
    """Calculates square coordinates within the fabric.

    >>> list(get_squares(1, 2, 3, 2))
    [(2, 3), (2, 4), (3, 3), (3, 4), (4, 3), (4, 4)]
    """
    return product(range(x+1, x+width+1), range(y+1, y+height+1))


def parse_line(line):
    """Parse one line of the input file
    >>> parse_line('#11 @ 7,70: 27x17')
    <Result () {'id_': 11, 'x': 7, 'y': 70, 'w': 27, 'h': 17}>
    """
    return parse('#{id_:d} @ {x:d},{y:d}: {w:d}x{h:d}', line)


if __name__ == '__main__':
    fabric = defaultdict(set)
    with open('03_input.txt', 'r') as stream:
        for line in stream:
            p = parse_line(line)
            for coordinates in get_squares(p['x'], p['y'], p['w'], p['h']):
                fabric[coordinates].add(p['id_'])

    # count squares with more than one claim
    count = 0
    for square in fabric.values():
        if len(square) >= 2:
            count += 1
    print(count)
