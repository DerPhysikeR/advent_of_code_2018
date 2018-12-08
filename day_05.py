#!/usr/bin/env python
"""
2018-12-08 14:28:07
@author: Paul Reiter
"""

if __name__ == '__main__':
    with open('input_05.txt', 'r') as stream:
        polymer = list(stream.readline().strip())
        print(len(polymer))

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
    print(len(result))
