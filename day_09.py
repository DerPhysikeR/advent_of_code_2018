#!/usr/bin/env python3
"""
2018-12-25 12:40:15
@author: Paul Reiter
"""
from itertools import cycle
from dataclasses import dataclass


@dataclass
class Player:
    score: int = 0


class Marble:

    def __init__(self, value, ccw=None, cw=None):
        self.value = value
        self.ccw = ccw
        self.cw = cw

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f'Marble({self.value})'


class Circle:

    def __init__(self):
        self.marbles = set()
        self.current = None

    def place(self, number):
        marble = Marble(number)
        if len(self) == 0:
            marble.ccw, marble.cw = marble, marble
            self.marbles.add(marble)
            self.current = marble
            return 0
        elif number % 23 == 0:
            score = marble.value + self.pop(-7)
            self.current = self._marbles(-6)
            return score
        else:
            self.append(marble, 1)
            self.current = self._marbles(2)
            return 0

    def __getitem__(self, key):
        return self._marbles(key).value

    def _marbles(self, key):
        if isinstance(key, int):
            attribute = 'cw' if key >= 0 else 'ccw'
            current = self.current
            for _ in range(abs(key)):
                current = getattr(current, attribute)
            return current
        else:
            raise TypeError('Index must be int!')

    def append(self, item, index=0):
        marble = item if isinstance(item, Marble) else Marble(item)
        if len(self) == 0:
            marble.ccw, marble.cw = marble, marble
            self.marbles.add(marble)
            self.current = marble
        else:
            ccw_neighbor = self._marbles(index)
            cw_neighbor = self._marbles(index+1)
            ccw_neighbor.cw = cw_neighbor.ccw = marble
            marble.ccw, marble.cw = ccw_neighbor, cw_neighbor
            self.marbles.add(marble)
        return marble.value

    def __len__(self):
        return len(self.marbles)

    def pop(self, index):
        if index != 0:
            marble = self._marbles(index)
            ccw_neighbor = self._marbles(index-1)
            cw_neighbor = self._marbles(index+1)
            ccw_neighbor.cw, cw_neighbor.ccw = cw_neighbor, ccw_neighbor
            self.marbles.remove(marble)
            return marble.value
        raise ValueError("Can't remove current Marble!")

    def __iter__(self):
        current = self.current
        for _ in self.marbles:
            yield current.value
            current = current.cw

    @classmethod
    def from_iterable(cls, iterable):
        circle = Circle()
        for item in iterable:
            circle.append(item, -1)
        return circle

    def __repr__(self):
        return '[' + ', '.join(str(marble) for marble in self.marbles) + ']'


def game(n_players, max_marble):
    players = [Player() for _ in range(n_players)]
    circle = Circle()
    for marble, player in zip(range(max_marble+1), cycle(players)):
        player.score += circle.place(marble)
    return players


if __name__ == '__main__':
    # 428 players; last marble is worth 72061 points
    result = game(428, 72061)
    max_score = max(player.score for player in result)
    print('The max score for a game with 428 players and 72061+1 marbles is: '
          f'{max_score}')
