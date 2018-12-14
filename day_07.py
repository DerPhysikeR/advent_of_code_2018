#!/usr/bin/env python
"""
2018-12-13 19:57:40
@author: Paul Reiter
"""
from parse import parse
from itertools import chain, tee


def parse_line(line):
    return tuple(parse('Step {} must be finished before step {} can begin.',
                       line))


def link(node1, node2):
    node1.children.add(node2)
    node2.parents.add(node1)


def replace_with_children(node_set, node):
    """Replaces `node` in set() `node_set` with its children"""
    node_set.remove(node)
    node_set = node_set.union(node.children)
    return node_set


class Node:

    def __init__(self, value):
        self.value = value
        self.parents, self.children = set(), set()

    def __repr__(self):
        child_values = sorted(child.value for child in self.children)
        parent_values = sorted(parent.value for parent in self.parents)
        return (f"Node(value='{self.value}', parents={parent_values}, "
                f"children={child_values})")

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


class Tree:

    def __init__(self, node_names):
        self.nodes = {}
        for node_name in node_names:
            self.nodes[node_name] = Node(node_name)

    def link(self, relation):
        link(self.nodes[relation[0]], self.nodes[relation[1]])

    def link_all(self, relations):
        for relation in relations:
            self.link(relation)

    @property
    def heads(self):
        return set(node for node in self.nodes.values()
                   if len(node.parents) == 0)

    @property
    def tails(self):
        return set(node for node in self.nodes.values()
                   if len(node.children) == 0)

    @classmethod
    def from_relations(cls, relations):
        rel1, rel2 = tee(relations)
        tree = cls(set(chain.from_iterable(relation for relation in rel1)))
        tree.link_all(rel2)
        return tree

    @classmethod
    def from_lines(cls, lines):
        return cls.from_relations(parse_line(line) for line in lines)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as stream:
            lines = stream.readlines()
        return cls.from_lines(lines)

    def __iter__(self):
        done = set()
        while len(done) < len(self.nodes):
            available = set(node for node in self.nodes.values()
                            if all(parent in done for parent in node.parents)
                            and node not in done)
            step = sorted(available)[0]
            done.add(step)
            yield step


if __name__ == '__main__':
    tree = Tree.from_file('input_07.txt')
    print(''.join(node.value for node in tree))
    breakpoint()
