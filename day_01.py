#!/usr/bin/env python
"""
2018-12-01 19:51:26
@author: Paul Reiter
"""
from itertools import cycle


if __name__ == '__main__':
    with open('01_input.txt', 'r') as stream:
        frequency_changes = [int(frequency) for frequency
                             in stream.readlines()]

    current_frequency = 0
    for frequency_change in frequency_changes:
        current_frequency += frequency_change
    print(current_frequency)

    frequencies = set()
    current_frequency = 0
    for frequency_change in cycle(frequency_changes):
        current_frequency += frequency_change
        if current_frequency not in frequencies:
            frequencies.add(current_frequency)
        else:
            print(current_frequency)
            break
