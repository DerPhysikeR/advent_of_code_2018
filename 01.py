#!/usr/bin/env python
"""
2018-12-01 19:51:26
@author: Paul Reiter
"""

if __name__ == '__main__':
    output = 0
    with open('01_input.txt', 'r') as stream:
        for line in stream:
            output += int(line)
    print(output)
