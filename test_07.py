#!/usr/bin/env python
"""
2018-12-13 20:13:07
@author: Paul Reiter
"""
import pytest
from day_07 import (parse_line, link, replace_with_children, Node, Tree,
                    time_of_task, Worker)


def test_parse_line():
    assert (parse_line('Step N must be finished before step X can begin.') ==
            ('N', 'X'))


def test_link():
    node1, node2 = Node('A'), Node('B')
    link(node1, node2)
    assert node1.parents == set()
    assert node1.children == set((node2, ))
    assert node2.parents == set((node1, ))
    assert node2.children == set()


def test_tree_link():
    tree = Tree(['A', 'B', 'C'])
    tree.link(('A', 'B'))
    assert tree.nodes['A'].parents == set()
    assert tree.nodes['A'].children == set((tree.nodes['B'], ))
    assert tree.nodes['B'].parents == set((tree.nodes['A'], ))
    assert tree.nodes['B'].children == set()
    assert tree.nodes['C'].parents == set()
    assert tree.nodes['C'].children == set()


def test_tree_heads():
    tree = Tree(['A', 'B', 'C', 'D'])
    tree.link_all([('A', 'C'), ('B', 'C'), ('C', 'D')])
    assert tree.heads == set((tree.nodes['A'], tree.nodes['B']))


def test_tree_tails():
    tree = Tree(['A', 'B', 'C', 'D'])
    tree.link_all([('A', 'C'), ('B', 'C'), ('C', 'D')])
    assert tree.tails == set((tree.nodes['D'], ))


def test_replace_with_children():
    nodes = [Node('A'), Node('B')]
    children = [Node('C'), Node('D')]
    nodes[1].children.add(children[0])
    nodes[1].children.add(children[1])
    assert (replace_with_children(set(nodes), nodes[1]) ==
            set((nodes[0], children[0], children[1])))


def test_tree_from_relations():
    tree = Tree.from_relations([('A', 'B'), ('B', 'C')])
    assert tree.nodes['A'].parents == set()
    assert tree.nodes['A'].children == set((tree.nodes['B'], ))
    assert tree.nodes['B'].parents == set((tree.nodes['A'], ))
    assert tree.nodes['B'].children == set((tree.nodes['C'], ))
    assert tree.nodes['C'].parents == set((tree.nodes['B'], ))
    assert tree.nodes['C'].children == set()


TEST_INPUT = ['Step C must be finished before step A can begin.',
              'Step C must be finished before step F can begin.',
              'Step A must be finished before step B can begin.',
              'Step A must be finished before step D can begin.',
              'Step B must be finished before step E can begin.',
              'Step D must be finished before step E can begin.',
              'Step F must be finished before step E can begin.']


def test_tree_iter():
    tree = Tree.from_lines(TEST_INPUT)
    assert ''.join(node.value for node in tree) == 'CABDFE'


@pytest.mark.parametrize('letter, time', [
    ('A', 61),
    ('B', 62),
    ('C', 63),
    ('Z', 86),
])
def test_time_of_task(letter, time):
    assert time_of_task(letter) == time


def test_worker():
    worker = Worker()
    assert worker.next() == '.'
    assert worker.done
    worker.add_task('A', 3)
    assert not worker.done
    assert worker.next() == 'A'
    assert worker.next() == 'A'
    assert worker.next() == 'A'
    assert worker.done
    assert worker.next() == '.'
    worker.add_task('B', 2)
    assert worker.next() == 'B'
    assert worker.next() == 'B'
    assert worker.done
    worker.add_task('C', 1)
    assert worker.next() == 'C'
    assert worker.next() == '.'


ASYNC_REFERENCE = [(0, 'C', '.', '.'),
                   (1, 'C', '.', '.'),
                   (2, 'C', '.', '.'),
                   (3, 'A', 'F', 'C'),
                   (4, 'B', 'F', 'CA'),
                   (5, 'B', 'F', 'CA'),
                   (6, 'D', 'F', 'CAB'),
                   (7, 'D', 'F', 'CAB'),
                   (8, 'D', 'F', 'CAB'),
                   (9, 'D', '.', 'CABF'),
                   (10, 'E', '.', 'CABFD'),
                   (11, 'E', '.', 'CABFD'),
                   (12, 'E', '.', 'CABFD'),
                   (13, 'E', '.', 'CABFD'),
                   (14, 'E', '.', 'CABFD'),
                   (15, '.', '.', 'CABFDE')]


def test_async_iter():
    tree = Tree.from_lines(TEST_INPUT)
    async_iter = tree.async_iter(2, offset=0)
    for time_step, reference in zip(async_iter, ASYNC_REFERENCE):
        assert time_step == reference
