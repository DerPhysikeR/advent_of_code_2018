#!/usr/bin/env python3
"""
2018-12-25 09:59:52
@author: Paul Reiter
"""
from day_08 import Node


def test_node_from_list():
    test_list = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
    root, remaining_list = Node.from_list(test_list)
    assert len(remaining_list) == 0

    assert root.n_children == 2
    assert len(root.children) == 2
    assert root.metadata == (1, 1, 2)

    child_b, child_c = root.children

    assert child_b.n_children == 0
    assert len(child_b.children) == 0
    assert child_b.metadata == (10, 11, 12)

    assert child_c.n_children == 1
    assert len(child_c.children) == 1
    assert child_c.metadata == (2,)

    child_d = child_c.children[0]

    assert child_d.n_children == 0
    assert len(child_d.children) == 0
    assert child_d.metadata == (99,)


def test_node_sum_metadata():
    test_list = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
    root, remaining_list = Node.from_list(test_list)
    assert 138 == root.sum_metadata()
