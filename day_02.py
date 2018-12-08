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


def distance(id_1, id_2):
    """
    >>> distance('abcde', 'axcye')
    2
    >>> distance('fghij', 'fguij')
    1
    >>> distance('abcde', 'abcde')
    0
    """
    return sum(letter_1 != letter_2 for letter_1, letter_2 in zip(id_1, id_2))


if __name__ == '__main__':
    # read all ids
    with open('input_02.txt', 'r') as stream:
        content = [line.rstrip() for line in stream.readlines()]

    # find doubles and triples and calculate checksum
    doubles, triples = 0, 0
    for line in content:
        contains_double, contains_triple = \
            countains_doubles_or_triples(line)
        doubles += contains_double
        triples += contains_triple
    print(doubles * triples)

    # find closest ids and print intersection
    close_ids = []
    for line_number, line_1 in enumerate(content):
        for line_2 in content[line_number+1:]:
            if distance(line_1, line_2) == 1:
                close_ids.append((line_1, line_2))
    print(close_ids)
    print(''.join(letter_1 for letter_1, letter_2 in zip(*close_ids[0])
                  if letter_1 == letter_2))
