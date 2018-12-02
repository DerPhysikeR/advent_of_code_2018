#!/usr/bin/env python
"""
2018-12-02 09:21:22
@author: Paul Reiter

Solution for day 2
"""


def countains_doubles_or_triples(id_):
    """
    >>> countains_doubles_or_triples('abcdef')
    (False, False)
    >>> countains_doubles_or_triples('bababc')
    (True, True)
    >>> countains_doubles_or_triples('abbcde')
    (True, False)
    >>> countains_doubles_or_triples('abcccd')
    (False, True)
    >>> countains_doubles_or_triples('aabcdd')
    (True, False)
    >>> countains_doubles_or_triples('abcdee')
    (True, False)
    >>> countains_doubles_or_triples('ababab')
    (False, True)
    """
    letters = set()
    doubles = set()
    triples = set()
    for letter in id_:
        if letter in doubles:
            triples.add(letter)
            doubles.remove(letter)
        elif letter in letters:
            doubles.add(letter)
        else:
            letters.add(letter)
    return bool(doubles), bool(triples)


if __name__ == '__main__':
    doubles, triples = 0, 0
    with open('02_input.txt', 'r') as stream:
        for line in stream:
            contains_double, contains_triple = \
                countains_doubles_or_triples(line)
            doubles += contains_double
            triples += contains_triple
    print(doubles * triples)
