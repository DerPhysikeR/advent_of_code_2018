#!/usr/bin/env python3
"""
2018-12-27 20:53:07
@author: Paul Reiter
"""
from operator import attrgetter
from collections import namedtuple
import copy
from itertools import cycle


Point = namedtuple('Point', 'x y')


def list_of_lists_to_string(data):
    return '\n'.join(''.join(line) for line in data)


MOVE_DICT = {'>-': '>', '>\\': 'v', '>/': '^',
             '^|': '^', '^\\': '<', '^/': '>',
             '<-': '<', '<\\': '^', '</': 'v',
             'v|': 'v', 'v\\': '>', 'v/': '<'}

TURN_DICT = {'>left': '^', '^left': '<', '<left': 'v', 'vleft': '>',
             '>right': 'v', '^right': '>', '<right': '^', 'vright': '<'}


class Cart:

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.turn = cycle(['left', 'straight', 'right'])
        self.move_counter = 0

    def ahead(self):
        x, y = self.position
        return {'>': Point(x+1, y), '^': Point(x, y-1),
                '<': Point(x-1, y), 'v': Point(x, y+1)}[self.direction]

    def move(self, new_position, char):
        if char == '+':
            self.direction = TURN_DICT.get(self.direction+next(self.turn),
                                           self.direction)
        else:
            self.direction = MOVE_DICT[self.direction+char]
        self.position = new_position
        self.move_counter += 1
        return self

    def __repr__(self):
        return f'Cart({self.position}, {self.direction}, {self.move_counter})'


class Network:

    RAIL_DICT = {'>': '-', '^': '|', '<': '-', 'v': '|'}

    def __init__(self, network):
        self.network = [list(line) for line in network.split('\n')]
        self.moving_carts = {}
        self.crashes = []

        for y, line in enumerate(self.network):
            for x, letter in enumerate(line):
                if letter in Network.RAIL_DICT:
                    cart = Cart(Point(x, y), letter)
                    self.moving_carts[cart.position] = cart
                    self.network[y][x] = Network.RAIL_DICT[letter]

    def step(self):
        if self.moving_carts:
            cart = sorted(self.moving_carts.values(),
                          key=attrgetter('move_counter', 'position.y',
                                         'position.x'))[0]
            ahead = cart.ahead()
            if ahead in self.moving_carts:
                del self.moving_carts[cart.position]
                del self.moving_carts[ahead]
                self.crashes.append(ahead)
                return 'crash'
            else:
                del self.moving_carts[cart.position]
                cart.move(ahead, self[ahead])
                self.moving_carts[cart.position] = cart
                return 'move'
        else:
            return 'No more carts to move.'

    def tick(self):
        if self.moving_carts:
            move_count = min(cart.move_counter for cart in
                             self.moving_carts.values())

            while (self.moving_carts and
                   (min(cart.move_counter for cart in
                    self.moving_carts.values()) <= move_count)):
                self.step()

    def __str__(self):
        network_with_carts = copy.deepcopy(self.network)
        for y, line in enumerate(self.network):
            for x, letter in enumerate(line):
                point = Point(x, y)
                if point in self.crashes:
                    network_with_carts[y][x] = 'X'
                elif point in self.moving_carts:
                    network_with_carts[y][x] = \
                        self.moving_carts[point].direction
        return list_of_lists_to_string(network_with_carts)

    def __getitem__(self, point):
        return self.network[point.y][point.x]

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as stream:
            content = stream.read()
        return cls(content)


if __name__ == '__main__':
    network = Network.from_file('input_13.txt')
    status = ''
    while status != 'crash':
        status = network.step()
    print(f'The first crash happens at coordinate: {network.crashes[0]}')

    network = Network.from_file('input_13.txt')
    while len(network.moving_carts) > 1:
        network.tick()
    point, cart = network.moving_carts.popitem()
    print(f"The last cart that hasn't crashed ends up at {point}")
