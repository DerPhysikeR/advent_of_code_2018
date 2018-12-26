#!/usr/bin/env python3
"""
2018-12-26 11:54:50
@author: Paul Reiter
"""
from collections import namedtuple


Point = namedtuple('Point', 'x, y')


def grid_generator(minpoint, maxpoint):
    for y in range(minpoint.y, maxpoint.y+1):
        for x in range(minpoint.x, maxpoint.x+1):
            yield Point(x, y)


def get_digit(number, digit):
    try:
        return int(str(number)[::-1][digit])
    except IndexError:
        return 0


def power_level(point, serial_number):
    rack_id = point.x + 10
    power_level = rack_id * point.y + serial_number
    power_level *= rack_id
    power_level = get_digit(power_level, 2) - 5
    return power_level


def create_grid(minpoint, maxpoint, serial_number):
    return {point: power_level(point, serial_number)
            for point in grid_generator(minpoint, maxpoint)}


class Grid:

    def __init__(self, minpoint, maxpoint, serial_number):
        self.minpoint, self.maxpoint = minpoint, maxpoint
        self.serial_number = serial_number
        self.grid = create_grid(minpoint, maxpoint, serial_number)

    def __iter__(self):
        for point in grid_generator(self.minpoint, self.maxpoint):
            yield self.grid[point]

    def __str__(self):
        longest = max(len(str(cell)) for cell in self)
        cell_list = [str(cell).rjust(longest) for cell in self]
        line_width = self.maxpoint.x - self.minpoint.x + 1
        lines = ['  '.join(line) for line in
                 zip(*[iter(cell_list)]*(line_width))]
        return '\n'.join(lines)

    def squares(self):
        iterator = grid_generator(self.minpoint,
                                  Point(self.maxpoint.x-2, self.maxpoint.y-2))
        for point in iterator:
            yield point, {point: self.grid[point] for point in
                          grid_generator(point, Point(point.x+2, point.y+2))}


def max_square_sum(grid):
    sums = {sum(square.values()): point for point, square in grid.squares()}
    maxsum = max(sums)
    return sums[maxsum], maxsum


if __name__ == '__main__':
    top_left, maxsum = max_square_sum(Grid(Point(1, 1), Point(300, 300), 6878))
    print(f'top left corner: {top_left}, total power: {maxsum}')
