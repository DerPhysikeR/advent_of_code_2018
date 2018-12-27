#!/usr/bin/env python3
"""
2018-12-26 11:54:50
@author: Paul Reiter
"""
from collections import namedtuple
import numpy as np
from tqdm import tqdm


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


def create_numpy_grid(minpoint, maxpoint, serial_number):
    width, heigth = maxpoint.x-minpoint.x+1, maxpoint.y-minpoint.y+1
    grid = np.empty((width, heigth), dtype=int)
    for point in grid_generator(minpoint, maxpoint):
        grid[point.y-minpoint.y, point.x-minpoint.x] = \
            power_level(point, serial_number)
    return grid


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

    def squares(self, size=3):
        iterator = grid_generator(self.minpoint,
                                  Point(self.maxpoint.x-size+1,
                                        self.maxpoint.y-size+1))
        for point in iterator:
            yield point, {point: self.grid[point] for point in
                          grid_generator(point, Point(point.x+size-1,
                                                      point.y+size-1))}

    def square_sum(self, point, size=3):
        return sum(self.grid[point] for point in
                   grid_generator(point,
                                  Point(point.x+size-1, point.y+size-1)))

    def square_sums(self, size=3):
        iterator = grid_generator(self.minpoint,
                                  Point(self.maxpoint.x-size+1,
                                        self.maxpoint.y-size+1))
        return {self.square_sum(point, size): point
                for point in iterator}


class NumGrid:

    def __init__(self, minpoint, maxpoint, serial_number):
        self.minpoint, self.maxpoint = minpoint, maxpoint
        self.serial_number = serial_number
        self.grid = create_numpy_grid(minpoint, maxpoint, serial_number)

    def __getitem__(self, key):
        rowkey, colkey = key
        rowkey = slice(rowkey.start-self.minpoint.x,
                       rowkey.stop-self.minpoint.x, rowkey.step)
        colkey = slice(colkey.start-self.minpoint.y,
                       colkey.stop-self.minpoint.y, colkey.step)
        return self.grid[rowkey, colkey]

    def square(self, point, size):
        return self[point.y:point.y+size, point.x:point.x+size]

    def square_sum(self, point, size):
        return np.sum(self.square(point, size))

    def square_sums(self, size):
        iterator = grid_generator(self.minpoint,
                                  Point(self.maxpoint.x-size+1,
                                        self.maxpoint.y-size+1))
        return {self.square_sum(point, size): point
                for point in iterator}


def max_square_sum(grid, size=3):
    sums = grid.square_sums(size)
    maxsum = max(sums)
    return sums[maxsum], maxsum


if __name__ == '__main__':
    grid = Grid(Point(1, 1), Point(300, 300), 6878)
    top_left, maxsum = max_square_sum(grid)
    print(f'top left corner: {top_left}, total power: {maxsum}')

    grid = NumGrid(Point(1, 1), Point(300, 300), 6878)
    overall_maxsum = {}
    for size in tqdm(range(1, 300+1)):
        point, maxsum = max_square_sum(grid, size)
        overall_maxsum[maxsum] = (point, size)
    highest_score = max(overall_maxsum)
    maxpoint, size = overall_maxsum[highest_score]
    print(f'The identifier for the square with the largest score ('
          f'{highest_score}) is: {maxpoint.x}, {maxpoint.y}, {size}')
