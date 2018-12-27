#!/usr/bin/env python3
"""
2018-12-27 18:01:44
@author: Paul Reiter
"""


def parse_rule(rule_string):
    rule_string = rule_string.strip()
    rule, _, result = rule_string.partition(' => ')
    return tuple(char == '#' for char in rule), result == '#'


class Garden:

    def __init__(self, initial_state, rules):
        self.plants = set()
        for index, plant in enumerate(initial_state):
            if plant == '#':
                self.plants.add(index)
        self.rules = {}
        for rule_string in rules:
            rule, result = parse_rule(rule_string)
            self.rules[rule] = result

    def evolve(self):
        plants = set()
        for i in range(min(self.plants)-4, max(self.plants)+4+1):
            key = tuple(j in self.plants for j in range(i-2, i+3))
            if self.rules.get(key, False):
                plants.add(i)
        self.plants = plants

    def value(self):
        return sum(self.plants)

    def __str__(self):
        return ''.join('#' if i in self.plants else '.'
                       for i in range(min(self.plants),
                                      max(self.plants)+1))

    @classmethod
    def from_lines(cls, lines):
        initial_state = lines[0].partition(': ')[2].strip()
        return cls(initial_state, lines[2:])

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as stream:
            lines = stream.readlines()
        return cls.from_lines(lines)


if __name__ == '__main__':
    garden = Garden.from_file('input_12.txt')
    for _ in range(20):
        garden.evolve()
    print(f'Value after 20 generations: {garden.value()}')

    garden = Garden.from_file('input_12.txt')
    value = 0
    for i in range(110):
        new_value = garden.value()
        print(f'Garden value generation {i}: {new_value}, dvalue: '
              f'{new_value-value}')
        value = new_value
        garden.evolve()
    print(f'Value after 50000000000 generations: {5691+(50000000000-100)*62}')
