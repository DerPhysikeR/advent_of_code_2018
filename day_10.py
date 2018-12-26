#!/usr/bin/env python3
"""
2018-12-26 09:33:58
@author: Paul Reiter
"""
import numpy as np
from parse import parse


def parse_line(line):
    return tuple(parse('position=<{:d}, {:d}> velocity=<{:d}, {:d}>', line))


def bounding_box(positions):
    return np.array([[np.min(positions[:, 0]), np.min(positions[:, 1])],
                     [np.max(positions[:, 0]), np.max(positions[:, 1])]])


class StarImage:

    def __init__(self, positions, velocities):
        self.positions = np.array(positions)
        self.velocities = np.array(velocities)

    def evolve(self, new=False):
        if new:
            return StarImage(self.positions + self.velocities, self.velocities)
        self.positions = self.positions + self.velocities

    def __repr__(self):
        return (f'StarImage({len(self.positions)} positions, '
                f'{len(self.velocities)} velocities, '
                f'size: {self.size}, bounding box: '
                f'{tuple(tuple(item) for item in self.bounding_box)})')

    def __str__(self):
        minx, miny, maxx, maxy = self.bounding_box.ravel()
        positions = set(tuple(position) for position in self.positions)
        result = []
        for y in range(miny, maxy+1):
            line = []
            for x in range(minx, maxx+1):
                line.append('#' if (x, y) in positions else '.')
            result.append(''.join(line))
        return '\n'.join(result)

    @property
    def bounding_box(self):
        return bounding_box(self.positions)

    @property
    def size(self):
        return ((self.bounding_box[1, 0] - self.bounding_box[0, 0]) *
                (self.bounding_box[1, 1] - self.bounding_box[0, 1]))

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as stream:
            content = [parse_line(line) for line in stream.readlines()]
        content = np.array(content)
        return cls(content[:, :2], content[:, 2:])


def find_minimal_image(starimage):
    new_starimage = starimage
    time = 0
    while new_starimage.size <= starimage.size:
        starimage = new_starimage
        time += 1
        new_starimage = starimage.evolve(new=True)
    return starimage, time-1


if __name__ == '__main__':
    starimage = StarImage.from_file('input_10.txt')
    minimal_starimage, time = find_minimal_image(starimage)
    print(f'After {time} seconds the following image will appear:')
    print(minimal_starimage)
