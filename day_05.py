#!/usr/bin/env python
"""
2018-12-08 14:28:07
@author: Paul Reiter
"""

if __name__ == '__main__':
    with open('input_05.txt', 'r') as stream:
        complete_polymer = stream.readline().strip()

    unique_units = ''.join(set(complete_polymer.lower()))
    result_dict = {}
    for unit in unique_units:
        polymer = list(complete_polymer.replace(unit, '')
                                       .replace(unit.swapcase(), ''))
        removed = 1
        while removed > 0:
            removed = previous = 0
            for index, element in enumerate(polymer):
                if element == '#':
                    continue
                elif polymer[previous] == element.swapcase():
                    polymer[previous] = '#'
                    polymer[index] = '#'
                    removed += 1
                else:
                    previous = index
        result = ''.join(element for element in polymer if element != '#')
        result_dict[unit] = len(result)

    length_of_shortest_polymer = min(result_dict.values())
    for unit, length in result_dict.items():
        if length == length_of_shortest_polymer:
            print(f'removing {unit} leads to a polymer of length {length}.')

