#!/usr/bin/env python3
"""
2018-12-27 20:43:26
@author: Paul Reiter
"""
from day_13 import list_of_lists_to_string, Cart, Network, Point


TEST_NETWORK = ('/->-\\        \n'
                '|   |  /----\\\n'
                '| /-+--+-\\  |\n'
                '| | |  | v  |\n'
                '\\-+-/  \\-+--/\n'
                '  \\------/   \n')

TEST_CLEAN_NETWORK = ('/---\\        \n'
                      '|   |  /----\\\n'
                      '| /-+--+-\\  |\n'
                      '| | |  | |  |\n'
                      '\\-+-/  \\-+--/\n'
                      '  \\------/   \n')


def test_cart_init():
    cart = Cart(Point(0, 0), '>')
    assert str(cart) == 'Cart(Point(x=0, y=0), >, 0)'
    assert next(cart.turn) == 'left'
    assert next(cart.turn) == 'straight'
    assert next(cart.turn) == 'right'
    assert next(cart.turn) == 'left'


def test_cart_ahead():
    assert Cart(Point(0, 0), '>').ahead() == Point(1, 0)
    assert Cart(Point(0, 0), '^').ahead() == Point(0, -1)
    assert Cart(Point(0, 0), '<').ahead() == Point(-1, 0)
    assert Cart(Point(0, 0), 'v').ahead() == Point(0, 1)


def test_move():
    cart = Cart(Point(0, 0), '>')
    assert cart.move(cart.ahead(), '-').direction == '>'
    assert cart.move(cart.ahead(), '/').direction == '^'
    assert cart.move(cart.ahead(), '|').direction == '^'


def test_network_init():
    network = Network(TEST_NETWORK)
    assert list_of_lists_to_string(network.network) == TEST_CLEAN_NETWORK
    assert Point(x=2, y=0) in network.moving_carts
    assert Point(x=9, y=3) in network.moving_carts


def test_network_str():
    network = Network(TEST_NETWORK)
    assert str(network) == TEST_NETWORK


def test_network_getitem():
    network = Network(TEST_NETWORK)
    assert network[Point(0, 0)] == '/'


with open('test_input_13.txt', 'r') as stream:
    content = stream.read()
    TEST_NETWORK_LIST = content.split('\n\n')


def test_network_evolve():
    network = Network(TEST_NETWORK_LIST[0])
    # breakpoint()
    for network_string in TEST_NETWORK_LIST[1:]:
        network.tick()
        assert str(network).strip() == network_string.strip()
