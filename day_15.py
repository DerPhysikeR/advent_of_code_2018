#!/usr/bin/env python3
"""
2018-12-28 19:15:21
@author: Paul Reiter
"""
from collections import namedtuple, defaultdict
from operator import attrgetter

Point = namedtuple('Point', 'x y')


class Unit:

    def __init__(self, hp=200, attack_power=3):
        self.hp = 200
        self.attack_power = attack_power

    def __repr__(self):
        return f'Unit(hp={self.hp}, ap={self.attack_power})'


class Game:

    def __init__(self, string, elfpower=3):
        positions = position_of_symbols_in_string(string)
        self.walls = positions['#']
        self.elves = {position: Unit(attack_power=elfpower)
                      for position in positions['E']}
        self.goblins = {position: Unit() for position in positions['G']}
        self.rounds_completed = 0

    def __str__(self):
        elf_dict = {position: 'E' for position in self.elves}
        goblin_dict = {position: 'G' for position in self.goblins}
        wall_dict = {position: '#' for position in self.walls}
        symbol_dict = {**elf_dict, **goblin_dict, **wall_dict}
        bounding_box = get_bounding_box(symbol_dict)
        result = [symbol_dict.get(pos, '.') for pos in
                  grid_generator(*bounding_box)]
        width = bounding_box[1].x - bounding_box[0].x + 1
        return '\n'.join(''.join(line) for line in zip(*[iter(result)]*width))

    @classmethod
    def from_file(cls, filepath, elfpower=False):
        with open(filepath, 'r') as stream:
            game_string = stream.read()
        elfpower = 3 if not elfpower else find_elf_power(game_string)
        return cls(game_string, elfpower)

    @property
    def units(self):
        return {**self.elves, **self.goblins}

    def next_unit(self):
        for position in sort_in_reading_order(self.units):
            try:
                yield position, self.units[position]
            except KeyError:
                continue

    def get_teams(self, position):
        if position in self.elves:
            return self.elves, self.goblins
        return self.goblins, self.elves

    def step(self, position, unit):
        allies, enemies = self.get_teams(position)
        obstacles = set().union(self.walls, allies)
        new_position = move_towards(position, enemies, obstacles)
        allies = update_dict(allies, position, new_position)
        self.fight(new_position, unit, enemies)

    def run_round(self):
        for position, unit in self.next_unit():
            if not self.elves or not self.goblins:
                break
            self.step(position, unit)
        else:
            self.rounds_completed += 1

    def run(self, rounds=None):
        if not rounds:
            while self.elves and self.goblins:
                self.run_round()
        else:
            for _ in range(rounds):
                self.run_round()

    def fight(self, position, unit, enemies):
        intersection = get_neighbors(position).intersection(enemies)
        if intersection:
            min_hp = min(enemies[pos].hp for pos in intersection)
            enemy_positions = {pos for pos in intersection
                               if enemies[pos].hp == min_hp}
            enemy_position = first_in_reading_order(enemy_positions)
            pos, enemy = enemy_position, enemies[enemy_position]
            enemy.hp -= unit.attack_power
            if enemy.hp <= 0:
                del enemies[pos]

    def outcome(self):
        return (sum(unit.hp for unit in self.units.values()) *
                self.rounds_completed)


def position_of_symbols_in_string(string):
    """Return dict of the form {symbol1: {Point(), Point()}, symbol2: {...}}"""
    positions = defaultdict(set)
    lines = [line.strip() for line in string.split('\n')]
    for y, line in enumerate(lines):
        for x, letter in enumerate(line):
            positions[letter].add(Point(x, y))
    return dict(positions)


def get_bounding_box(points):
    """Returns Point(minx, miny), Point(maxx,maxy) for `points`"""
    minx = min(point.x for point in points)
    maxx = max(point.x for point in points)
    miny = min(point.y for point in points)
    maxy = max(point.y for point in points)
    return Point(minx, miny), Point(maxx, maxy)


def grid_generator(minpoint, maxpoint):
    """Generator that iterates rowwise over all points inside box defined by
    `minpoint` and `maxpoint`."""
    for y in range(minpoint.y, maxpoint.y+1):
        for x in range(minpoint.x, maxpoint.x+1):
            yield Point(x, y)


def sort_in_reading_order(points):
    """Returns list of points sorted in reading order"""
    return sorted(points, key=attrgetter('y', 'x'))


def first_in_reading_order(points):
    """Returns first point in `points` in reading order"""
    return sort_in_reading_order(points)[0]


def update_dict(dictionary, old, new):
    if new is not None:
        value = dictionary[old]
        del dictionary[old]
        dictionary[new] = value
    return dictionary


def get_neighbors(point, excluding=None):
    """Returns the orthogonal neighbors of `point` excluding points in
    `excluding`."""
    x, y = point
    neighbor_set = set((Point(x+1, y), Point(x, y-1),
                        Point(x-1, y), Point(x, y+1)))
    excluding = set() if excluding is None else set(excluding)
    return neighbor_set.difference(excluding)


def get_all_neighbors(points, excluding=None):
    """Returns all orthogonal get_neighbors of set of `points` excluding points
    in `excluding`."""
    all_neighbors = set().union(*(get_neighbors(point) for point in points))
    excluding = set() if excluding is None else set(excluding)
    return all_neighbors.difference(excluding)


def neighbor_generator(point, obstacles=None):
    """Yields sets of points with distance 0, 1, 2, ... from `point`"""
    exclude = set() if obstacles is None else set(obstacles)
    neighbors = {point}
    yield neighbors
    exclude.update(neighbors)
    while neighbors:
        neighbors = get_all_neighbors(neighbors, excluding=exclude)
        yield neighbors
        exclude.update(neighbors)


def move_towards(point, targets, obstacles):
    obstacles = obstacles.difference({point})
    targets = get_all_neighbors(targets, obstacles).difference(targets)
    closest = get_closest_point(point, targets, obstacles)
    if closest:
        step = step_closer(point, closest, obstacles)
        if step:
            return step
    return point


def get_closest_point(point, other_points, obstacles=None):
    """Finds closest point to `point` in `other_points` cicumnavigating
    `obstacles`. Ties are broken in reading order."""
    for neighbors in neighbor_generator(point, obstacles):
        intersection = neighbors.intersection(other_points)
        if intersection:
            return first_in_reading_order(intersection)


def step_closer(point, target, obstacles=None):
    """Returns the next point to move to in order to get closer to target."""
    obstacles = set() if obstacles is None else set(obstacles)
    points_to_move_to = get_neighbors(point, excluding=obstacles)
    points_to_move_to.add(point)
    for neighbors in neighbor_generator(target, obstacles):
        intersection = neighbors.intersection(points_to_move_to)
        if intersection:
            return first_in_reading_order(intersection)


def find_elf_power(game_string):
    number_of_all_elves = game_string.count('E')
    number_of_elves, elf_power = 0, 2
    while number_of_elves < number_of_all_elves:
        elf_power += 1
        game = Game(game_string, elf_power)
        game.run()
        number_of_elves = len(game.elves)
    return next(iter(game.elves.values())).attack_power


if __name__ == '__main__':
    game = Game.from_file('input_15.txt')
    game.run()
    print(game)
    print(f'The outcome is: {game.outcome()}')

    game = Game.from_file('input_15.txt', True)
    game.run()
    print(game)
    print(f'The outcome with strengthened elves is: {game.outcome()}')
