#!/usr/bin/env python3
"""
2018-12-28 19:15:27
@author: Paul Reiter
"""
from day_15 import (Point, Unit, Game, position_of_symbols_in_string,
                    get_bounding_box, grid_generator, sort_in_reading_order,
                    first_in_reading_order, update_dict, get_neighbors,
                    get_all_neighbors, neighbor_generator, move_towards,
                    get_closest_point, step_closer, find_elf_power)


def test_game_str():
    game = Game(MOVEMENT_TEST[0])
    assert str(game) == MOVEMENT_TEST[0]


def test_game_movement():
    game = Game(MOVEMENT_TEST[0])
    rounds = 0
    for test_string in MOVEMENT_TEST[1:]:
        game.run_round()
        assert str(game) == test_string
        rounds += 1
        assert game.rounds_completed == rounds


def test_game_limited_rounds():
    game = Game(GAME_TEST[0])
    for rounds in range(1, 48):
        game.run_round()
        assert game.rounds_completed == rounds
        if rounds in GAME_TEST:
            assert str(game) == GAME_TEST[rounds]


def test_game_open_ended():
    game = Game(GAME_TEST[0])
    game.run()
    assert game.rounds_completed == 47
    assert sum(unit.hp for unit in game.units.values()) == 590
    assert game.outcome() == 27730


def test_game_several_outcomes():
    for game, outcome in TEST_OUTCOMES:
        game = Game(game)
        game.run()
        assert game.outcome() == outcome


def test_position_of_symbols_in_string():
    teststring = 'abb\naac\n'
    reference = {'a': {Point(0, 0), Point(0, 1), Point(1, 1)},
                 'b': {Point(1, 0), Point(2, 0)},
                 'c': {Point(2, 1)}}
    assert position_of_symbols_in_string(teststring) == reference


def test_get_bounding_box():
    points = {Point(2, 0), Point(0, 2), Point(4, 2), Point(2, 3)}
    assert get_bounding_box(points) == (Point(0, 0), Point(4, 3))


def test_grid_generator():
    reference = [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]
    for point, ref in zip(grid_generator(Point(0, 0), Point(1, 1)), reference):
        assert point == ref


def test_sort_in_reading_order():
    test_points = (Point(1, 2), Point(3, 1), Point(2, 1))
    assert sort_in_reading_order(test_points) == [test_points[2],
                                                  test_points[1],
                                                  test_points[0]]


def test_get_neighbors():
    point = Point(0, 0)
    excluding = set((Point(1, 0), ))
    assert (get_neighbors(point, excluding) ==
            set((Point(-1, 0), Point(0, 1), Point(0, -1))))


def test_get_all_neighbors():
    points = set((Point(0, 0), Point(1, 0)))
    excluding = set((Point(2, 0), ))
    assert (get_all_neighbors(points, excluding) ==
            set((Point(-1, 0), Point(0, 1), Point(x=0, y=0), Point(x=0, y=-1),
                 Point(x=1, y=0), Point(x=1, y=-1), Point(x=1, y=1))))


def test_neighbor_generator():
    point = Point(0, 0)
    obstacles = {Point(x, 1) for x in range(-3, 3+1)}
    gen = neighbor_generator(point, obstacles)
    assert next(gen) == {point}
    assert next(gen) == {Point(1, 0), Point(0, -1), Point(-1, 0)}
    assert next(gen) == {Point(2, 0), Point(1, -1), Point(0, -2),
                         Point(-1, -1), Point(-2, 0)}


def test_get_closest_point():
    point = Point(0, 0)
    obstacles = set((Point(2, 0), Point(2, 1), Point(2, -1)))
    other_points = set((Point(3, 0), Point(4, 0)))
    assert get_closest_point(point, other_points, obstacles) == Point(3, 0)


def test_get_closest_point_same_point():
    point = Point(0, 0)
    obstacles = set((Point(2, 0), Point(2, 1), Point(2, -1)))
    other_points = set((Point(0, 0), Point(4, 0)))
    assert get_closest_point(point, other_points, obstacles) == Point(0, 0)


def test_find_elf_power():
    for game_string, outcome in ELF_POWER_GAMES:
        game = Game(game_string, find_elf_power(game_string))
        game.run()
        assert game.outcome() == outcome


MOVEMENT_TEST = ['#########\n'
                 '#G..G..G#\n'
                 '#.......#\n'
                 '#.......#\n'
                 '#G..E..G#\n'
                 '#.......#\n'
                 '#.......#\n'
                 '#G..G..G#\n'
                 '#########',
                 '#########\n'
                 '#.G...G.#\n'
                 '#...G...#\n'
                 '#...E..G#\n'
                 '#.G.....#\n'
                 '#.......#\n'
                 '#G..G..G#\n'
                 '#.......#\n'
                 '#########',
                 '#########\n'
                 '#..G.G..#\n'
                 '#...G...#\n'
                 '#.G.E.G.#\n'
                 '#.......#\n'
                 '#G..G..G#\n'
                 '#.......#\n'
                 '#.......#\n'
                 '#########',
                 '#########\n'
                 '#.......#\n'
                 '#..GGG..#\n'
                 '#..GEG..#\n'
                 '#G..G...#\n'
                 '#......G#\n'
                 '#.......#\n'
                 '#.......#\n'
                 '#########']


GAME_TEST = \
    {0: ('#######\n'
         '#.G...#\n'
         '#...EG#\n'
         '#.#.#G#\n'
         '#..G#E#\n'
         '#.....#\n'
         '#######'),
     1: ('#######\n'
         '#..G..#\n'
         '#...EG#\n'
         '#.#G#G#\n'
         '#...#E#\n'
         '#.....#\n'
         '#######'),
     2: ('#######\n'
         '#...G.#\n'
         '#..GEG#\n'
         '#.#.#G#\n'
         '#...#E#\n'
         '#.....#\n'
         '#######'),
     23: ('#######\n'
          '#...G.#\n'
          '#..G.G#\n'
          '#.#.#G#\n'
          '#...#E#\n'
          '#.....#\n'
          '#######'),
     24: ('#######\n'
          '#..G..#\n'
          '#...G.#\n'
          '#.#G#G#\n'
          '#...#E#\n'
          '#.....#\n'
          '#######'),
     25: ('#######\n'
          '#.G...#\n'
          '#..G..#\n'
          '#.#.#G#\n'
          '#..G#E#\n'
          '#.....#\n'
          '#######'),
     26: ('#######\n'
          '#G....#\n'
          '#.G...#\n'
          '#.#.#G#\n'
          '#...#E#\n'
          '#..G..#\n'
          '#######'),
     27: ('#######\n'
          '#G....#\n'
          '#.G...#\n'
          '#.#.#G#\n'
          '#...#E#\n'
          '#...G.#\n'
          '#######'),
     28: ('#######\n'
          '#G....#\n'
          '#.G...#\n'
          '#.#.#G#\n'
          '#...#E#\n'
          '#....G#\n'
          '#######'),
     47: ('#######\n'
          '#G....#\n'
          '#.G...#\n'
          '#.#.#G#\n'
          '#...#.#\n'
          '#....G#\n'
          '#######')}


TEST_OUTCOMES = [
                 (('#######\n'
                   '#G..#E#\n'
                   '#E#E.E#\n'
                   '#G.##.#\n'
                   '#...#E#\n'
                   '#...E.#\n'
                   '#######'), 36334),
                 (('#######\n'
                   '#E..EG#\n'
                   '#.#G.E#\n'
                   '#E.##E#\n'
                   '#G..#.#\n'
                   '#..E#.#\n'
                   '#######'), 39514),
                 (('#######\n'
                   '#E.G#.#\n'
                   '#.#G..#\n'
                   '#G.#.G#\n'
                   '#G..#.#\n'
                   '#...E.#\n'
                   '#######'), 27755),
                 (('#######\n'
                   '#.E...#\n'
                   '#.#..G#\n'
                   '#.###.#\n'
                   '#E#G#G#\n'
                   '#...#G#\n'
                   '#######'), 28944),
                 (('#########\n'
                   '#G......#\n'
                   '#.E.#...#\n'
                   '#..##..G#\n'
                   '#...##..#\n'
                   '#...#...#\n'
                   '#.G...G.#\n'
                   '#.....G.#\n'
                   '#########'), 18740),
                 ]


ELF_POWER_GAMES = [(('#######\n'
                     '#.G...#\n'
                     '#...EG#\n'
                     '#.#.#G#\n'
                     '#..G#E#\n'
                     '#.....#\n'
                     '#######'), 4988),
                   (('#######\n'
                     '#E..EG#\n'
                     '#.#G.E#\n'
                     '#E.##E#\n'
                     '#G..#.#\n'
                     '#..E#.#\n'
                     '#######'), 31284),
                   (('#######\n'
                     '#E.G#.#\n'
                     '#.#G..#\n'
                     '#G.#.G#\n'
                     '#G..#.#\n'
                     '#...E.#\n'
                     '#######'), 3478),
                   (('#######\n'
                     '#.E...#\n'
                     '#.#..G#\n'
                     '#.###.#\n'
                     '#E#G#G#\n'
                     '#...#G#\n'
                     '#######'), 6474),
                   (('#########\n'
                     '#G......#\n'
                     '#.E.#...#\n'
                     '#..##..G#\n'
                     '#...##..#\n'
                     '#...#...#\n'
                     '#.G...G.#\n'
                     '#.....G.#\n'
                     '#########'), 1140),
                   ]
