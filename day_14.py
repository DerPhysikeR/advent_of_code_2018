#!/usr/bin/env python3
"""
2018-12-28 17:46:15
@author: Paul Reiter
"""
from collections import deque


def to_digits(number):
    return [int(letter) for letter in str(number)]


def evolve_scores(scores, elve1, elve2):
    scores.extend(to_digits(scores[elve1] + scores[elve2]))
    elve1 = (elve1 + scores[elve1] + 1) % len(scores)
    elve2 = (elve2 + scores[elve2] + 1) % len(scores)
    return scores, elve1, elve2


def score_generator(scores, elve1, elve2):
    index = 0
    while True:
        while index < len(scores):
            yield index, scores[index]
            index += 1
        scores, elve1, elve2 = evolve_scores(scores, elve1, elve2)


def find_pattern(pattern, scores, elve1, elve2):
    scores = score_generator(scores, elve1, elve2)
    score_deque = deque()
    while len(score_deque) < len(pattern):
        index, score = next(scores)
        score_deque.append(score)
    while tuple(score_deque) != tuple(pattern):
        index, score = next(scores)
        score_deque.append(score)
        score_deque.popleft()
    return index - len(pattern) + 1


if __name__ == '__main__':
    scores = [3, 7]
    elve1, elve2 = 0, 1
    digits_after = 760221
    while len(scores) < digits_after+10:
        scores, elve1, elve2 = evolve_scores(scores, elve1, elve2)
    print(''.join(str(score) for score in
                  scores[digits_after:digits_after+10]))

    index = find_pattern(tuple(to_digits(760221)), [3, 7], 0, 1)
    print(f'pattern 760221 appears after {index} recipes')
