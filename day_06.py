#!/usr/bin/env python
"""
2018-12-09 23:40:29
@author: Paul Reiter
"""
from collections import namedtuple, defaultdict
from parse import parse


Point = namedtuple('Point', 'x y')


def distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


def parse_line(line):
    """Parses one line of the input file"""
    return Point(*parse('{:d}, {:d}', line))


def bounding_box(points):
    """Find the bounding box for a set of points"""
    minx = min(point.x for point in points)
    miny = min(point.y for point in points)
    maxx = max(point.x for point in points)
    maxy = max(point.y for point in points)
    return Point(minx, miny), Point(maxx, maxy)


def box_iter(min_point, max_point):
    for x in range(min_point.x, max_point.x+1):
        for y in range(min_point.y, max_point.y+1):
            yield Point(x, y)


def frame_iter(min_point, max_point):
    for x in range(min_point.x, max_point.x):
        yield Point(x, min_point.y)
    for y in range(min_point.y, max_point.y):
        yield Point(max_point.x, y)
    for x in range(max_point.x, min_point.x, -1):
        yield Point(x, max_point.y)
    for y in range(max_point.y, min_point.y, -1):
        yield Point(min_point.x, y)


if __name__ == '__main__':
    with open('input_06.txt', 'r') as stream:
        points = [parse_line(line) for line in stream.readlines()]

    # initialize bounding box + 1 in each direction
    min_point, max_point = bounding_box(points)
    wide_min_point = Point(min_point.x-1, min_point.y-1)
    wide_max_point = Point(max_point.x+1, max_point.y+1)

    # iterate over all cells, calculate distances and set membership
    wide_cells = {}
    for cell in box_iter(wide_min_point, wide_max_point):
        distances = [distance(cell, point) for point in points]
        min_distance = min(distances)
        if distances.count(min_distance) == 1:
            wide_cells[cell] = distances.index(min_distance)
        else:
            wide_cells[cell] = '.'

    # take only cells of actual bounding box
    cells = {point: wide_cells[point]
             for point in box_iter(min_point, max_point)}

    # count membership cells for each point for bounding box
    cell_counts = defaultdict(int)
    for index in cells.values():
        cell_counts[index] += 1

    # count membership cells for each point in wide bouding box
    wide_cell_counts = defaultdict(int)
    for index in wide_cells.values():
        wide_cell_counts[index] += 1

    # exclude areas where the membership count differs
    stable_areas = {value: count for value, count in cell_counts.items()
                    if wide_cell_counts[value] == count}
    print(max(count for value, count in cell_counts.items()
              if wide_cell_counts[value] == count))

    # calculate center point of problem and add it to close points
    center_point = Point(min_point.x + (max_point.x - min_point.x)//2,
                         min_point.y + (max_point.y - min_point.y)//2)
    close_cells = set()
    if sum(distance(center_point, point) for point in points) < 10000:
        close_cells = close_cells.union(set((center_point, )))

    # calculate frame corners
    frame_corners = [Point(center_point.x-1, center_point.y-1),
                     Point(center_point.x+1, center_point.y+1)]

    frame_distance_sums = set((5, ))
    while any(fds < 10000 for fds in frame_distance_sums):
        frame_distance_sums = set()
        for frame_cell in frame_iter(*frame_corners):
            distance_sum = sum(distance(frame_cell, point) for point in points)
            if distance_sum < 10000:
                close_cells.add(frame_cell)
            frame_distance_sums.add(distance_sum)
        frame_corners = [Point(frame_corners[0].x-1, frame_corners[0].y-1),
                         Point(frame_corners[1].x+1, frame_corners[1].y+1)]

    print(len(close_cells))
